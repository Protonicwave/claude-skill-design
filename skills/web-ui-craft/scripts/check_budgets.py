"""Compare a Lighthouse report against page budgets.

Usage:
    python check_budgets.py REPORT [--script-kib N]

REPORT is the JSON file Lighthouse writes for a mobile run (--output=json).
Each measure prints one line starting with pass, breach or unmeasured. Figures
are judged as printed, so a figure that prints equal to its budget passes. The
script weight budget defaults to 365 KiB of transfer size and is set with
--script-kib; the other budgets are fixed.
Exit code 1 means a budget was breached. Exit code 2 means nothing breached but
a measure could not be read, or the report could not be used at all (missing
file, invalid JSON, a failed page load, a desktop or unthrottled run). Exit code 0 means every
measure passed.

Limits: reports over 50 MB are refused. At most 50 animated elements are
listed. Budgets assume the throttled mobile profile, so desktop reports and
runs with throttling left to the caller ("provided") are rejected rather than
compared.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

LCP_BUDGET_MS = 2500.0
CLS_BUDGET = 0.1
TOTAL_BLOCKING_TIME_BUDGET_MS = 200.0
DEFAULT_SCRIPT_BUDGET_KIB = 365.0
MAX_NON_COMPOSITED_ANIMATIONS = 0

BYTES_PER_KIB = 1024
MAX_REPORT_BYTES = 50_000_000
MAX_ELEMENTS_LISTED = 50
REQUIRED_FORM_FACTOR = "mobile"
THROTTLING_METHODS = frozenset({"simulate", "devtools"})

LCP_AUDIT = "largest-contentful-paint"
CLS_AUDIT = "cumulative-layout-shift"
TOTAL_BLOCKING_TIME_AUDIT = "total-blocking-time"
RESOURCE_SUMMARY_AUDIT = "resource-summary"
ANIMATIONS_AUDIT = "non-composited-animations"
SCRIPT_WEIGHT = "script-weight"


class ReportError(Exception):
    """The report cannot be compared against budgets at all."""


class Status(StrEnum):
    WITHIN_BUDGET = "pass"
    BREACH = "breach"
    UNMEASURED = "unmeasured"


@dataclass(frozen=True, slots=True)
class Unmeasured:
    reason: str


@dataclass(frozen=True, slots=True)
class AnimatedElement:
    selector: str
    causes: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Budget:
    name: str
    limit: float
    unit: str
    decimals: int

    def printed(self, value: float) -> float:
        return round(value, self.decimals)

    def figure(self, value: float) -> str:
        return f"{value:.{self.decimals}f}{self.unit}"

    def limit_text(self) -> str:
        return f"{self.limit:g}{self.unit}"


@dataclass(frozen=True, slots=True)
class Outcome:
    status: Status
    lines: tuple[str, ...]


def mapping(value: object) -> Mapping[str, object]:
    """Return the value as a mapping, or an empty one when it is not an object."""
    return value if isinstance(value, dict) else {}


def sequence(value: object) -> Sequence[object]:
    return value if isinstance(value, list) else []


def number(value: object) -> float | None:
    if isinstance(value, bool) or not isinstance(value, int | float):
        return None
    return float(value)


def load_report(path: Path) -> Mapping[str, object]:
    """Read the report and return its audits, or raise ReportError with the reason."""
    try:
        with path.open("rb") as handle:
            raw = handle.read(MAX_REPORT_BYTES + 1)
    except OSError as error:
        raise ReportError(f"{path}: cannot read report ({error.strerror or error})") from error
    if len(raw) > MAX_REPORT_BYTES:
        raise ReportError(f"{path}: report is over {MAX_REPORT_BYTES} bytes")
    try:
        # Untyped JSON enters here; everything past this function sees narrowed types.
        report: object = json.loads(raw)
    except (ValueError, RecursionError) as error:
        raise ReportError(f"{path}: invalid JSON ({error})") from error
    if not isinstance(report, dict) or not isinstance(report.get("audits"), dict):
        raise ReportError(f"{path}: not a Lighthouse report, expected an object with audits")
    if report.get("runtimeError") is not None:
        runtime_error = mapping(report["runtimeError"])
        code = runtime_error.get("code", "unknown")
        message = runtime_error.get("message", "no message")
        raise ReportError(f"{path}: Lighthouse reported a runtime error {code}: {message}")
    form_factor = mapping(report.get("configSettings")).get("formFactor")
    if form_factor != REQUIRED_FORM_FACTOR:
        raise ReportError(
            f"{path}: form factor is {form_factor!r} but budgets assume the throttled "
            f"{REQUIRED_FORM_FACTOR} profile; rerun Lighthouse without a desktop preset"
        )
    throttling = mapping(report.get("configSettings")).get("throttlingMethod")
    if throttling not in THROTTLING_METHODS:
        raise ReportError(
            f"{path}: throttling method is {throttling!r} but budgets assume throttled "
            "figures; rerun Lighthouse without --throttling-method=provided"
        )
    return mapping(report["audits"])


def find_audit(audits: Mapping[str, object], audit_id: str) -> Mapping[str, object] | Unmeasured:
    if audit_id not in audits:
        return Unmeasured(f"{audit_id} audit is absent from the report")
    audit = mapping(audits[audit_id])
    if audit.get("scoreDisplayMode") == "error":
        return Unmeasured(f"{audit_id} errored: {audit.get('errorMessage', 'no message')}")
    return audit


def read_numeric(audits: Mapping[str, object], audit_id: str) -> float | Unmeasured:
    audit = find_audit(audits, audit_id)
    if isinstance(audit, Unmeasured):
        return audit
    value = number(audit.get("numericValue"))
    return Unmeasured(f"{audit_id} has no numeric value") if value is None else value


def read_script_kib(audits: Mapping[str, object]) -> float | Unmeasured:
    audit = find_audit(audits, RESOURCE_SUMMARY_AUDIT)
    if isinstance(audit, Unmeasured):
        return audit
    for row in sequence(mapping(audit.get("details")).get("items")):
        fields = mapping(row)
        if fields.get("resourceType") == "script":
            size = number(fields.get("transferSize"))
            if size is not None:
                return size / BYTES_PER_KIB
    return Unmeasured(f"{RESOURCE_SUMMARY_AUDIT} has no script transfer size")


def read_element(item: object) -> AnimatedElement:
    fields = mapping(item)
    selector = mapping(fields.get("node")).get("selector")
    causes = []
    for sub_item in sequence(mapping(fields.get("subItems")).get("items")):
        cause = mapping(sub_item)
        reason = cause.get("failureReason", "unknown reason")
        causes.append(f"{reason} ({cause.get('animation', 'unnamed animation')})")
    return AnimatedElement(
        selector=selector if isinstance(selector, str) else "(no selector)",
        causes=tuple(causes),
    )


def read_animated_elements(
    audits: Mapping[str, object],
) -> tuple[AnimatedElement, ...] | Unmeasured:
    audit = find_audit(audits, ANIMATIONS_AUDIT)
    if isinstance(audit, Unmeasured):
        return audit
    if audit.get("scoreDisplayMode") == "notApplicable":
        return ()
    items = mapping(audit.get("details")).get("items")
    if not isinstance(items, list):
        return Unmeasured(f"{ANIMATIONS_AUDIT} lists no elements")
    return tuple(read_element(item) for item in items)


def judge_numeric(budget: Budget, reading: float | Unmeasured) -> Outcome:
    if isinstance(reading, Unmeasured):
        return Outcome(Status.UNMEASURED, (f"{Status.UNMEASURED} {budget.name}: {reading.reason}",))
    status = Status.WITHIN_BUDGET if budget.printed(reading) <= budget.limit else Status.BREACH
    line = f"{status} {budget.name}: {budget.figure(reading)} (budget {budget.limit_text()})"
    return Outcome(status, (line,))


def judge_animations(elements: tuple[AnimatedElement, ...] | Unmeasured) -> Outcome:
    if isinstance(elements, Unmeasured):
        reason = f"{Status.UNMEASURED} {ANIMATIONS_AUDIT}: {elements.reason}"
        return Outcome(Status.UNMEASURED, (reason,))
    count = len(elements)
    noun = "element" if count == 1 else "elements"
    status = Status.WITHIN_BUDGET if count <= MAX_NON_COMPOSITED_ANIMATIONS else Status.BREACH
    budget = MAX_NON_COMPOSITED_ANIMATIONS
    summary = f"{status} {ANIMATIONS_AUDIT}: {count} {noun} (budget {budget})"
    listed = [
        f"  {element.selector}: {'; '.join(element.causes) or 'no reason given'}"
        for element in elements[:MAX_ELEMENTS_LISTED]
    ]
    if count > MAX_ELEMENTS_LISTED:
        listed.append(f"  ... and {count - MAX_ELEMENTS_LISTED} more")
    return Outcome(status, (summary, *listed))


def judge(audits: Mapping[str, object], script_budget_kib: float) -> list[Outcome]:
    lcp = Budget(LCP_AUDIT, LCP_BUDGET_MS, " ms", 0)
    cls = Budget(CLS_AUDIT, CLS_BUDGET, "", 3)
    blocking = Budget(TOTAL_BLOCKING_TIME_AUDIT, TOTAL_BLOCKING_TIME_BUDGET_MS, " ms", 0)
    script = Budget(SCRIPT_WEIGHT, script_budget_kib, " KiB", 0)
    return [
        judge_numeric(lcp, read_numeric(audits, LCP_AUDIT)),
        judge_numeric(cls, read_numeric(audits, CLS_AUDIT)),
        judge_numeric(blocking, read_numeric(audits, TOTAL_BLOCKING_TIME_AUDIT)),
        judge_numeric(script, read_script_kib(audits)),
        judge_animations(read_animated_elements(audits)),
    ]


def exit_code(outcomes: Sequence[Outcome]) -> int:
    statuses = {outcome.status for outcome in outcomes}
    if Status.BREACH in statuses:
        return 1
    return 2 if Status.UNMEASURED in statuses else 0


def positive_number(text: str) -> float:
    try:
        value = float(text)
    except ValueError:
        value = math.nan
    if not math.isfinite(value) or value <= 0:
        raise argparse.ArgumentTypeError(f"expected a positive number, got {text!r}")
    return value


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else None)
    parser.add_argument("report", type=Path, help="Lighthouse JSON report from a mobile run")
    parser.add_argument(
        "--script-kib",
        type=positive_number,
        default=DEFAULT_SCRIPT_BUDGET_KIB,
        help=f"script transfer budget in KiB (default {DEFAULT_SCRIPT_BUDGET_KIB:g})",
    )
    arguments = parser.parse_args(argv)
    try:
        audits = load_report(arguments.report)
    except ReportError as error:
        print(error, file=sys.stderr)
        return 2
    outcomes = judge(audits, arguments.script_kib)
    for outcome in outcomes:
        print("\n".join(outcome.lines))
    return exit_code(outcomes)


if __name__ == "__main__":
    sys.exit(main())
