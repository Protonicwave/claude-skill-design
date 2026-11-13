from pathlib import Path

import pytest

from check_phone import MeasureError, Measurement, WideElement, find_chrome, main, parse_report

needs_chrome = pytest.mark.skipif(find_chrome() is None, reason="Chrome is needed to measure pages")

PAGE_HEAD = """<!doctype html><meta charset="utf-8">
<style>body { margin: 0; font: 16px sans-serif; } * { box-sizing: border-box; }</style>
"""


def write_page(folder: Path, body: str) -> Path:
    page = folder / "index.html"
    page.write_text(PAGE_HEAD + body, encoding="utf-8")
    return page


def test_reads_the_report_chrome_prints() -> None:
    dom = (
        '<html><body><pre id="report">{"overflow_px": 24, "elements": '
        '[{"element": "a.btn", "reach_px": 24}]}</pre></body></html>'
    )
    assert parse_report(dom) == Measurement(24, (WideElement("a.btn", 24),))


def test_reads_an_escaped_report() -> None:
    dom = (
        '<pre id="report">{"overflow_px": 3, "elements": '
        '[{"element": "a&amp;b", "reach_px": 3}]}</pre>'
    )
    assert parse_report(dom).elements == (WideElement("a&b", 3),)


def test_rejects_a_frame_that_never_loaded() -> None:
    with pytest.raises(MeasureError, match="did not load in its frame"):
        parse_report('<pre id="report">not measured</pre>')


def test_rejects_output_without_a_report() -> None:
    with pytest.raises(MeasureError, match="no report"):
        parse_report("")


def test_reports_a_missing_page_as_unmeasured(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([str(tmp_path / "absent.html")]) == 2
    assert capsys.readouterr().out.startswith("unmeasured: no page")


def test_reports_missing_chrome_as_unmeasured(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("CHROME_PATH", str(tmp_path / "no-chrome.exe"))
    assert main([str(write_page(tmp_path, "<p>Fits.</p>"))]) == 2
    assert "Chrome not found" in capsys.readouterr().out


@needs_chrome
def test_passes_a_page_that_fits(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert (
        main([str(write_page(tmp_path, "<header><a href='#'>Home</a></header><p>Fits.</p>"))]) == 0
    )
    assert capsys.readouterr().out.startswith("pass")


@needs_chrome
def test_names_the_element_past_the_right_edge(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    page = write_page(
        tmp_path, '<header><div class="band" style="width: 440px">Install</div></header>'
    )
    assert main([str(page)]) == 1
    out = capsys.readouterr().out
    assert "65 px wider" in out
    assert "div.band reaches 65 px" in out


@needs_chrome
def test_measures_below_the_first_screen(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    page = write_page(
        tmp_path, '<div style="height: 6000px"></div><pre style="width: 400px">x</pre>'
    )
    assert main([str(page)]) == 1
    assert "pre reaches 25 px" in capsys.readouterr().out


@needs_chrome
def test_ignores_content_in_its_own_scroll_box(tmp_path: Path) -> None:
    page = write_page(tmp_path, '<div style="overflow: auto"><p style="width: 900px">W</p></div>')
    assert main([str(page)]) == 0


@needs_chrome
def test_lists_an_svg_but_not_its_shapes(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    page = write_page(
        tmp_path, '<svg width="420" height="20"><rect width="420" height="20"/></svg>'
    )
    assert main([str(page)]) == 1
    out = capsys.readouterr().out
    assert "svg reaches 45 px" in out
    assert "rect" not in out


@needs_chrome
def test_lists_at_most_ten_elements(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    page = write_page(tmp_path, '<p style="width: 400px">wide</p>' * 14)
    assert main([str(page)]) == 1
    assert capsys.readouterr().out.count("p reaches 25 px") == 10
