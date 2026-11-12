"""Score a paired round from its function checks, judge verdicts and votes.

Usage:
    python bench/score.py ROUND

ROUND is a folder pairs.py has paired. This reads key.json, each build's
function.json, the judges' verdicts/<pair>-<order>.json and, when present, the
votes.json exported from vote.html, and writes results.md.

A judge's choice counts only when both orders name the same build; a split is
a tie. A pair missing either verdict is unjudged, never a tie. Judge and user
agreement is taken over the pairs the user voted on that both orders judged.

Console errors leave out Chrome's "Failed to load resource" lines, since each
repeats a failed request that is counted on its own. Chrome's automatic favicon
request appears only as such a line, so a missing favicon is not counted.

Exit code 2 means nothing was written: key.json is missing, a verdict or
votes.json is malformed, or a function.json is missing or malformed. The
message names the file.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pairs import CHOICES, CRITERIA, Build, Choice, Key, Pair, RoundError, load_key, read_json
from views import CAPTURE_BUDGET_SECONDS

SERIOUS_IMPACTS = frozenset({"serious", "critical"})
RESOURCE_ERROR_PREFIX = "Failed to load resource"
BUDGET_RESULTS = {0: "pass", 1: "breach", 2: "unmeasured"}

Verdict = dict[str, Choice]
# Per criterion, the token of the build that won, or None for a tie.
Winners = dict[str, str | None]
# Per voted pair, the token of the build the user chose, or None for a tie.
Votes = dict[str, str | None]


@dataclass(frozen=True, slots=True)
class FunctionSummary:
    serious_axe: int
    hidden_focus: int
    covered_focus: int
    walk_end: str
    overflow_px: int
    console_errors: int
    failed_requests: int
    missing_head: tuple[str, ...]
    timed_out_loads: int
    budgets: str
    elapsed_seconds: float


PROBLEMS: tuple[tuple[str, Callable[[FunctionSummary], bool]], ...] = (
    ("Serious axe", lambda f: f.serious_axe > 0),
    ("Hidden focus", lambda f: f.hidden_focus > 0),
    ("Covered focus", lambda f: f.covered_focus > 0),
    ("Walk unfinished", lambda f: f.walk_end != "end"),
    ("Phone overflow", lambda f: f.overflow_px > 0),
    ("Console errors", lambda f: f.console_errors > 0),
    ("Failed requests", lambda f: f.failed_requests > 0),
    ("Missing head tags", lambda f: len(f.missing_head) > 0),
    ("Timed-out loads", lambda f: f.timed_out_loads > 0),
    ("Budget breach", lambda f: f.budgets == "breach"),
    (f"Over {CAPTURE_BUDGET_SECONDS:g} s", lambda f: f.elapsed_seconds > CAPTURE_BUDGET_SECONDS),
)


# Any: record and the value returned come from JSON; the value is checked against kinds here.
def _field(path: Path, record: Any, name: str, *kinds: type) -> Any:
    """record[name] when record is an object and the value's type is one of kinds."""
    if type(record) is not dict or type(record.get(name)) not in kinds:
        expected = " or ".join("null" if kind is type(None) else kind.__name__ for kind in kinds)
        raise RoundError(f"{path}: expected {name!r} as {expected} in a capture.py report")
    return record[name]


def _budget_result(path: Path, budgets: dict[str, Any] | None) -> str:
    if budgets is None:
        return "not run"
    exit_code = _field(path, budgets, "exit_code", int)
    if exit_code not in BUDGET_RESULTS:
        raise RoundError(f"{path}: expected a budget exit code of 0, 1 or 2, got {exit_code}")
    return BUDGET_RESULTS[exit_code]


def read_function(path: Path) -> FunctionSummary:
    raw = read_json(path)
    walk = _field(path, raw, "keyboard_walk", dict)
    stops = _field(path, walk, "stops", list)
    head = _field(path, raw, "head", dict)
    console_errors = _field(path, raw, "console_errors", list)
    return FunctionSummary(
        serious_axe=sum(
            _field(path, violation, "impact", str) in SERIOUS_IMPACTS
            for violation in _field(path, raw, "axe_violations", list)
        ),
        hidden_focus=sum(not _field(path, stop, "focus_visible", bool) for stop in stops),
        covered_focus=sum(_field(path, stop, "covered", bool) for stop in stops),
        walk_end=_field(path, walk, "ended_by", str),
        overflow_px=_field(path, raw, "phone_overflow_px", int),
        console_errors=sum(
            not str(line).startswith(RESOURCE_ERROR_PREFIX) for line in console_errors
        ),
        failed_requests=len(_field(path, raw, "failed_requests", list)),
        missing_head=tuple(tag for tag in head if not _field(path, head, tag, bool)),
        timed_out_loads=len(_field(path, raw, "timed_out_loads", list)),
        budgets=_budget_result(path, _field(path, raw, "budgets", dict, type(None))),
        elapsed_seconds=float(_field(path, raw, "elapsed_seconds", int, float)),
    )


def read_verdict(path: Path) -> Verdict | None:
    """The verdict at path, or None when the judge has not written one."""
    if not path.exists():
        return None
    raw = read_json(path)
    if not isinstance(raw, dict) or set(raw) - {"reasons"} != set(CRITERIA):
        raise RoundError(f"{path}: expected an object with the keys {', '.join(CRITERIA)}")
    wrong = [criterion for criterion in CRITERIA if raw[criterion] not in CHOICES]
    if wrong:
        raise RoundError(f'{path}: expected "A", "B" or "tie" for {", ".join(wrong)}')
    return {criterion: raw[criterion] for criterion in CRITERIA}


def chosen_build(pair: Pair, order: int, choice: Choice) -> str | None:
    """The token of the build a choice names when the pair was shown in order 1 or 2."""
    if choice == "tie":
        return None
    page_a, page_b = pair.pages(order)
    return page_a if choice == "A" else page_b


def resolve(pair: Pair, order_1: Verdict, order_2: Verdict) -> Winners:
    """Per criterion, the build both orders chose, or None when they did not agree."""
    winners: Winners = {}
    for criterion in CRITERIA:
        first = chosen_build(pair, 1, order_1[criterion])
        second = chosen_build(pair, 2, order_2[criterion])
        winners[criterion] = first if first == second else None
    return winners


def read_votes(path: Path, key: Key) -> Votes | None:
    """Per voted pair, the build the user chose (None for a tie), or None without votes.json."""
    if not path.exists():
        return None
    raw = read_json(path)
    if not isinstance(raw, dict):
        raise RoundError(f"{path}: expected an object of pair id to choice")
    pairs = {pair.id: pair for pair in key.pairs}
    votes: Votes = {}
    for pair_id, choice in raw.items():
        if pair_id not in key.votes:
            raise RoundError(f"{path}: pair {pair_id!r} was not on the vote page")
        if choice not in CHOICES:
            raise RoundError(f'{path}: expected "A", "B" or "tie" for {pair_id}, got {choice!r}')
        votes[pair_id] = chosen_build(pairs[pair_id], key.votes[pair_id], choice)
    return votes


def agreement(judged: Mapping[str, Winners], votes: Mapping[str, str | None]) -> tuple[int, int]:
    """How many voted pairs both orders judged, and on how many of them judge and user agree."""
    compared = [pair_id for pair_id in votes if pair_id in judged]
    agreed = sum(judged[pair_id]["overall"] == votes[pair_id] for pair_id in compared)
    return agreed, len(compared)


def _table(header: Sequence[str], rows: Sequence[Sequence[object]]) -> list[str]:
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    lines += ["| " + " | ".join(str(cell) for cell in row) + " |" for row in rows]
    return lines


@dataclass(frozen=True, slots=True)
class Round:
    key: Key
    verdicts: dict[tuple[str, int], Verdict]
    judged: dict[str, Winners]
    votes: Votes | None
    functions: dict[str, FunctionSummary]

    def arm(self, token: str) -> str:
        return self.key.builds[token].arm

    def outcome(self, winner: str | None) -> str:
        """The winning build's arm, or "tie" for display when there was no winner."""
        return "tie" if winner is None else self.arm(winner)

    def tally(self, winners: Sequence[str | None], left: str, right: str) -> list[int]:
        """How many winners are of the left arm, ties, and of the right arm."""
        arms = [None if winner is None else self.arm(winner) for winner in winners]
        return [arms.count(left), arms.count(None), arms.count(right)]

    def arm_pair(self, pair: Pair) -> tuple[str, str]:
        left, right = sorted((self.arm(pair.first), self.arm(pair.second)))
        return left, right


def read_round(round_dir: Path) -> Round:
    key_path = round_dir / "key.json"
    if not key_path.exists():
        raise RoundError(f"no key.json in {round_dir}: run pairs.py first")
    key = load_key(key_path)
    verdicts = {}
    for pair in key.pairs:
        for order in (1, 2):
            found = read_verdict(round_dir / "verdicts" / f"{pair.id}-{order}.json")
            if found is not None:
                verdicts[pair.id, order] = found
    judged = {
        pair.id: resolve(pair, verdicts[pair.id, 1], verdicts[pair.id, 2])
        for pair in key.pairs
        if (pair.id, 1) in verdicts and (pair.id, 2) in verdicts
    }
    functions = {
        token: read_function(round_dir / build.capture / "function.json")
        for token, build in key.builds.items()
    }
    return Round(key, verdicts, judged, read_votes(round_dir / "votes.json", key), functions)


def _judge_section(scored: Round) -> list[str]:
    key = scored.key
    agreed_orders = sum(
        chosen_build(pair, 1, scored.verdicts[pair.id, 1]["overall"])
        == chosen_build(pair, 2, scored.verdicts[pair.id, 2]["overall"])
        for pair in key.pairs
        if pair.id in scored.judged
    )
    choices = [verdict["overall"] for verdict in scored.verdicts.values()]
    picked = [choice for choice in choices if choice != "tie"]
    unjudged = [pair.id for pair in key.pairs if pair.id not in scored.judged]
    lines = [
        "## Judges",
        "",
        f"Both orders agreed on overall for {agreed_orders} of {len(scored.judged)} judged pairs."
        f" Page A was chosen in {picked.count('A')} of {len(picked)} overall choices of a page.",
        f"Unjudged: {', '.join(unjudged)}."
        if unjudged
        else "Every pair was judged in both orders.",
    ]
    for left, right in sorted({scored.arm_pair(pair) for pair in key.pairs}):
        judged = [
            scored.judged[pair.id]
            for pair in key.pairs
            if scored.arm_pair(pair) == (left, right) and pair.id in scored.judged
        ]
        rows = [
            [criterion, *scored.tally([w[criterion] for w in judged], left, right)]
            for criterion in CRITERIA
        ]
        lines += ["", f"### {left} against {right}", ""]
        lines += _table(["Criterion", left, "tie", right], rows)
    return lines


def _vote_section(scored: Round) -> list[str]:
    votes = scored.votes
    if votes is None:
        return ["## Votes", "", "No votes.json yet."]
    agreed, compared = agreement(scored.judged, votes)
    pairs = {pair.id: pair for pair in scored.key.pairs}
    rows = []
    for left, right in sorted({scored.arm_pair(pairs[pair_id]) for pair_id in votes}):
        chosen = [
            build
            for pair_id, build in votes.items()
            if scored.arm_pair(pairs[pair_id]) == (left, right)
        ]
        rows.append([f"{left} against {right}", *scored.tally(chosen, left, right)])
    return [
        "## Votes",
        "",
        f"The user voted on {len(votes)} of {len(scored.key.votes)} pairs on the vote page."
        f" Judges and the user agreed on {agreed} of {compared} voted pairs both orders judged.",
        "",
        *_table(["Arms", "First arm", "Tie", "Second arm"], rows),
    ]


def _pairs_section(scored: Round) -> list[str]:
    rows = []
    votes = scored.votes or {}
    for pair in scored.key.pairs:
        judged = scored.judged.get(pair.id)
        rows.append(
            [
                pair.id,
                pair.subject,
                f"{scored.arm(pair.first)} against {scored.arm(pair.second)}",
                "unjudged" if judged is None else scored.outcome(judged["overall"]),
                scored.outcome(votes[pair.id]) if pair.id in votes else "not voted",
            ]
        )
    return ["## Pairs", "", *_table(["Pair", "Subject", "Arms", "Judges", "User"], rows)]


BUILD_COLUMNS = (
    "Subject",
    "Arm",
    "Run",
    "Serious axe",
    "Hidden focus",
    "Covered focus",
    "Walk",
    "Overflow px",
    "Console errors",
    "Failed requests",
    "Missing head",
    "Timed-out loads",
    "Budgets",
    "Capture s",
)


def _build_row(build: Build, f: FunctionSummary) -> list[object]:
    return [
        build.subject,
        build.arm,
        build.run,
        f.serious_axe,
        f.hidden_focus,
        f.covered_focus,
        f.walk_end,
        f.overflow_px,
        f.console_errors,
        f.failed_requests,
        ", ".join(f.missing_head) or "none",
        f.timed_out_loads,
        f.budgets,
        f.elapsed_seconds,
    ]


def _function_section(scored: Round) -> list[str]:
    builds = sorted(
        scored.key.builds.items(), key=lambda item: (item[1].subject, item[1].arm, item[1].run)
    )
    per_arm = []
    for arm in sorted({build.arm for build in scored.key.builds.values()}):
        summaries = [scored.functions[t] for t, b in scored.key.builds.items() if b.arm == arm]
        per_arm.append([arm, len(summaries), *(sum(map(test, summaries)) for _, test in PROBLEMS)])
    return [
        "## Function",
        "",
        "Builds with each problem, per arm.",
        "",
        *_table(["Arm", "Builds", *(label for label, _ in PROBLEMS)], per_arm),
        "",
        *_table(BUILD_COLUMNS, [_build_row(build, scored.functions[t]) for t, build in builds]),
    ]


def render(round_name: str, scored: Round) -> str:
    dropped = [f"- {line}" for line in scored.key.dropped] or ["None."]
    sections = [
        [f"# Bench results: {round_name}"],
        _judge_section(scored),
        _vote_section(scored),
        _pairs_section(scored),
        _function_section(scored),
        ["## Dropped pairs", "", *dropped],
    ]
    return "\n\n".join("\n".join(section) for section in sections) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else None)
    parser.add_argument("round", type=Path, help="folder pairs.py has paired")
    args = parser.parse_args(argv)
    try:
        scored = read_round(args.round)
    except RoundError as error:
        print(error, file=sys.stderr)
        return 2
    results = args.round / "results.md"
    results.write_text(render(args.round.resolve().name, scored), encoding="utf-8")
    print(f"wrote {results}")
    return 0


if __name__ == "__main__":  # pragma: no cover: entry point wiring only
    sys.exit(main())
