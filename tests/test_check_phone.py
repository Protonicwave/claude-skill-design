import subprocess
from pathlib import Path
from typing import Any

import pytest

import check_phone
from check_phone import (
    MAX_ELEMENTS_LISTED,
    MeasureError,
    Measurement,
    WideElement,
    find_chrome,
    main,
    parse_report,
)

needs_chrome = pytest.mark.skipif(find_chrome() is None, reason="Chrome is needed to measure pages")

PAGE_HEAD = """<!doctype html><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>body { margin: 0; font: 16px sans-serif; } * { box-sizing: border-box; }</style>
"""


def write_page(folder: Path, body: str, head: str = PAGE_HEAD) -> Path:
    page = folder / "index.html"
    page.write_text(head + body, encoding="utf-8")
    return page


def report_dom(fields: str) -> str:
    return f'<html><body><pre id="report">{{{fields}}}</pre></body></html>'


def test_reads_the_report_chrome_prints() -> None:
    dom = report_dom(
        '"rendered": true, "has_viewport_meta": true, "overflow_px": 24, '
        '"elements": [{"element": "a.btn", "reach_px": 24}]'
    )
    assert parse_report(dom) == Measurement(24, True, (WideElement("a.btn", 24),))


def test_reads_an_escaped_report() -> None:
    dom = report_dom(
        '"rendered": true, "has_viewport_meta": true, "overflow_px": 3, '
        '"elements": [{"element": "a&amp;b", "reach_px": 3}]'
    )
    assert parse_report(dom).elements == (WideElement("a&b", 3),)


def test_rejects_a_page_that_rendered_nothing() -> None:
    dom = report_dom(
        '"rendered": false, "has_viewport_meta": true, "overflow_px": 0, "elements": []'
    )
    with pytest.raises(MeasureError, match="rendered nothing"):
        parse_report(dom)


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


def test_finds_chrome_in_an_install_folder(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    chrome = tmp_path / "Google" / "Chrome" / "Application" / "chrome.exe"
    chrome.parent.mkdir(parents=True)
    chrome.write_bytes(b"")
    monkeypatch.delenv("CHROME_PATH", raising=False)
    monkeypatch.setattr("check_phone.shutil.which", lambda _name: None)
    monkeypatch.setenv("ProgramFiles", str(tmp_path))
    assert find_chrome() == chrome


@pytest.fixture
def stand_in_chrome(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A file for CHROME_PATH to name, for tests that replace the Chrome process."""
    chrome = tmp_path / "chrome.exe"
    chrome.write_bytes(b"")
    monkeypatch.setenv("CHROME_PATH", str(chrome))
    return chrome


@pytest.mark.usefixtures("stand_in_chrome")
def test_reports_a_chrome_timeout_as_unmeasured(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    def time_out(command: list[str], **_kwargs: Any) -> subprocess.CompletedProcess[str]:
        raise subprocess.TimeoutExpired(command, check_phone.CHROME_TIMEOUT_SECONDS)

    monkeypatch.setattr("check_phone.subprocess.run", time_out)
    assert main([str(write_page(tmp_path, "<p>Fits.</p>"))]) == 2
    assert "did not finish within" in capsys.readouterr().out


@pytest.mark.usefixtures("stand_in_chrome")
def test_reports_a_chrome_failure_as_unmeasured(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    def fail(command: list[str], **_kwargs: Any) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(command, 1, stdout="", stderr="no display")

    monkeypatch.setattr("check_phone.subprocess.run", fail)
    assert main([str(write_page(tmp_path, "<p>Fits.</p>"))]) == 2
    assert "exited with code 1: no display" in capsys.readouterr().out


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
def test_lists_at_most_the_element_limit(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    page = write_page(tmp_path, '<p style="width: 400px">wide</p>' * (MAX_ELEMENTS_LISTED + 4))
    assert main([str(page)]) == 1
    assert capsys.readouterr().out.count("p reaches 25 px") == MAX_ELEMENTS_LISTED


@needs_chrome
def test_breaches_a_page_without_a_viewport_tag(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    page = write_page(tmp_path, "<p>Fits.</p>", head='<!doctype html><meta charset="utf-8">')
    assert main([str(page)]) == 1
    assert 'no <meta name="viewport">' in capsys.readouterr().out


@needs_chrome
def test_measures_content_a_script_fetches(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (tmp_path / "band.json").write_text('{"width_px": 430}', encoding="utf-8")
    page = write_page(
        tmp_path,
        '<div id="band">Install</div><script>fetch("band.json").then((r) => r.json())'
        '.then((b) => { document.getElementById("band").style.width = b.width_px + "px"; });'
        "</script>",
    )
    assert main([str(page)]) == 1
    assert "div#band reaches 55 px" in capsys.readouterr().out


@needs_chrome
def test_resolves_root_relative_paths_against_the_page_folder(tmp_path: Path) -> None:
    (tmp_path / "site.css").write_text(".band { width: 420px; }", encoding="utf-8")
    page = write_page(tmp_path, '<link rel="stylesheet" href="/site.css"><div class="band">x</div>')
    assert main([str(page)]) == 1


@needs_chrome
def test_reports_an_unbuilt_app_as_unmeasured(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    page = write_page(
        tmp_path, '<div id="root"></div><script type="module" src="/src/main.tsx"></script>'
    )
    assert main([str(page)]) == 2
    assert "rendered nothing" in capsys.readouterr().out
