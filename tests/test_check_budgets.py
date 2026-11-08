import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest

from check_budgets import main

KIB = 1024


@dataclass(frozen=True, slots=True)
class Page:
    """Figures for one page, written out in the shape Lighthouse 13.6.0 uses for a mobile run."""

    lcp_ms: float = 1400.0
    cls: float = 0.02
    tbt_ms: float = 50.0
    script_bytes: int = 120 * KIB
    animated: tuple[tuple[str, str, str], ...] = ()
    form_factor: str = "mobile"
    throttling: str = "simulate"


def make_report(page: Page) -> dict[str, Any]:
    animations: dict[str, Any] = {
        "id": "non-composited-animations",
        "score": 1,
        "scoreDisplayMode": "notApplicable",
    }
    if page.animated:
        animations = {
            "id": "non-composited-animations",
            "score": 1,
            "scoreDisplayMode": "informative",
            "details": {
                "type": "table",
                "items": [
                    {
                        "node": {"type": "node", "selector": selector, "nodeLabel": selector},
                        "subItems": {
                            "type": "subitems",
                            "items": [{"failureReason": reason, "animation": name}],
                        },
                    }
                    for selector, reason, name in page.animated
                ],
            },
        }
    return {
        "lighthouseVersion": "13.6.0",
        "configSettings": {"formFactor": page.form_factor, "throttlingMethod": page.throttling},
        "audits": {
            "largest-contentful-paint": {
                "scoreDisplayMode": "numeric",
                "numericValue": page.lcp_ms,
                "numericUnit": "millisecond",
            },
            "cumulative-layout-shift": {
                "scoreDisplayMode": "numeric",
                "numericValue": page.cls,
                "numericUnit": "unitless",
            },
            "total-blocking-time": {
                "scoreDisplayMode": "numeric",
                "numericValue": page.tbt_ms,
                "numericUnit": "millisecond",
            },
            "resource-summary": {
                "scoreDisplayMode": "informative",
                "details": {
                    "type": "table",
                    "items": [
                        {"resourceType": "total", "transferSize": page.script_bytes + 40 * KIB},
                        {"resourceType": "script", "transferSize": page.script_bytes},
                        {"resourceType": "document", "transferSize": 40 * KIB},
                    ],
                },
            },
            "non-composited-animations": animations,
        },
    }


def run(
    tmp_path: Path, report: object, capsys: pytest.CaptureFixture[str], *flags: str
) -> tuple[int, str]:
    path = tmp_path / "report.json"
    path.write_text(json.dumps(report), encoding="utf-8")
    code = main([str(path), *flags])
    captured = capsys.readouterr()
    return code, captured.out + captured.err


def test_report_within_every_budget_passes(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    code, output = run(tmp_path, make_report(Page()), capsys)
    assert code == 0
    assert "breach" not in output
    assert "unmeasured" not in output


@pytest.mark.parametrize(
    ("page", "expected"),
    [
        (Page(lcp_ms=3100.0), "largest-contentful-paint: 3100 ms (budget 2500 ms)"),
        (Page(cls=0.18), "cumulative-layout-shift: 0.180 (budget 0.1)"),
        (Page(tbt_ms=450.0), "total-blocking-time: 450 ms (budget 200 ms)"),
        (Page(script_bytes=400 * KIB), "script-weight: 400 KiB (budget 365 KiB)"),
    ],
)
def test_each_breach_reports_figure_and_budget(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], page: Page, expected: str
) -> None:
    code, output = run(tmp_path, make_report(page), capsys)
    assert code == 1
    breach_lines = [line for line in output.splitlines() if line.startswith("breach")]
    assert breach_lines == [f"breach {expected}"]


def test_figure_equal_to_its_budget_passes(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    report = make_report(Page(lcp_ms=2500.0, cls=0.1, tbt_ms=200.0, script_bytes=365 * KIB))
    code, _ = run(tmp_path, report, capsys)
    assert code == 0


@pytest.mark.parametrize(
    "page",
    [
        Page(lcp_ms=2500.4),
        Page(cls=0.1004),
        Page(script_bytes=365 * KIB + 400),
    ],
)
def test_breach_is_judged_at_the_printed_precision(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], page: Page
) -> None:
    code, output = run(tmp_path, make_report(page), capsys)
    assert code == 0
    assert "breach" not in output


def test_script_budget_follows_the_brief(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    report = make_report(Page(script_bytes=120 * KIB))
    code, output = run(tmp_path, report, capsys, "--script-kib", "75")
    assert code == 1
    assert "75 KiB" in output


@pytest.mark.parametrize("value", ["0", "-5", "lots"])
def test_script_budget_must_be_a_positive_number(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], value: str
) -> None:
    with pytest.raises(SystemExit) as stopped:
        run(tmp_path, make_report(Page()), capsys, "--script-kib", value)
    assert stopped.value.code == 2


def test_non_composited_animations_are_listed_by_element(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    animated = (
        ("body > div#bar", "Unsupported CSS Properties: width, box-shadow", "grow"),
        ("main > .glow", "Unsupported CSS Property: filter", "pulse"),
    )
    code, output = run(tmp_path, make_report(Page(animated=animated)), capsys)
    assert code == 1
    assert "non-composited-animations" in output
    assert "2 elements" in output
    for selector, reason, name in animated:
        line = next(line for line in output.splitlines() if selector in line)
        assert reason in line
        assert name in line


@pytest.mark.parametrize(
    "audit_id",
    [
        "largest-contentful-paint",
        "cumulative-layout-shift",
        "total-blocking-time",
        "resource-summary",
        "non-composited-animations",
    ],
)
def test_missing_audit_is_unmeasured(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], audit_id: str
) -> None:
    report = make_report(Page())
    del report["audits"][audit_id]
    code, output = run(tmp_path, report, capsys)
    assert code == 2
    assert any(line.startswith("unmeasured") and audit_id in line for line in output.splitlines())


def test_errored_audit_is_unmeasured_with_its_reason(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    report = make_report(Page())
    report["audits"]["largest-contentful-paint"] = {
        "scoreDisplayMode": "error",
        "errorMessage": "NO_LCP",
    }
    code, output = run(tmp_path, report, capsys)
    assert code == 2
    assert "NO_LCP" in output


def test_script_summary_without_a_script_row_is_unmeasured(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    report = make_report(Page())
    items = report["audits"]["resource-summary"]["details"]["items"]
    report["audits"]["resource-summary"]["details"]["items"] = [
        item for item in items if item["resourceType"] != "script"
    ]
    code, output = run(tmp_path, report, capsys)
    assert code == 2
    assert "script-weight" in output


def test_breach_outranks_an_unmeasured_figure(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    report = make_report(Page(tbt_ms=900.0))
    del report["audits"]["cumulative-layout-shift"]
    code, output = run(tmp_path, report, capsys)
    assert code == 1
    assert "unmeasured" in output


def test_failed_page_load_exits_2_with_the_runtime_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    report = make_report(Page())
    report["runtimeError"] = {
        "code": "ERRORED_DOCUMENT_REQUEST",
        "message": "Lighthouse was unable to reliably load the page you requested.",
    }
    code, output = run(tmp_path, report, capsys)
    assert code == 2
    assert "ERRORED_DOCUMENT_REQUEST" in output


def test_desktop_report_is_rejected(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    code, output = run(tmp_path, make_report(Page(form_factor="desktop")), capsys)
    assert code == 2
    assert "mobile" in output


@pytest.mark.parametrize("throttling", ["provided", "unknown"])
def test_unthrottled_report_is_rejected(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], throttling: str
) -> None:
    code, output = run(tmp_path, make_report(Page(throttling=throttling)), capsys)
    assert code == 2
    assert "throttl" in output


def test_devtools_throttling_is_accepted(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    code, _ = run(tmp_path, make_report(Page(throttling="devtools")), capsys)
    assert code == 0


def test_deeply_nested_json_exits_2(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "report.json"
    path.write_text("[" * 100_000 + "]" * 100_000, encoding="utf-8")
    code = main([str(path)])
    assert code == 2
    assert "report.json" in capsys.readouterr().err


def test_missing_file_exits_2_with_the_path(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "absent.json"
    code = main([str(path)])
    assert code == 2
    assert "absent.json" in capsys.readouterr().err


def test_invalid_json_exits_2_with_the_reason(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "report.json"
    path.write_text("{not json", encoding="utf-8")
    code = main([str(path)])
    error = capsys.readouterr().err
    assert code == 2
    assert "report.json" in error
    assert "JSON" in error


@pytest.mark.parametrize("report", [[], "text", {"audits": []}])
def test_report_of_the_wrong_shape_exits_2(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], report: object
) -> None:
    code, _ = run(tmp_path, report, capsys)
    assert code == 2
