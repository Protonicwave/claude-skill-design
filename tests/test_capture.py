import json
import os
import shutil
import socket
import sys
import time
from collections.abc import Iterator
from http.server import SimpleHTTPRequestHandler
from pathlib import Path
from typing import Any

import pytest
from playwright.sync_api import BrowserType, sync_playwright
from playwright.sync_api import Error as PlaywrightError

import capture
from capture import Budgets, main, run_lighthouse
from views import CAPTURE_BUDGET_SECONDS

CLEAN_PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Clean fixture</title>
<meta name="description" content="A page with nothing wrong.">
<meta property="og:image" content="/card.png">
<link rel="icon" href="data:,">
<style>
  .visually-hidden { position: absolute; width: 1px; height: 1px; overflow: hidden;
                     clip-path: inset(50%); white-space: nowrap; }
</style>
</head>
<body>
<main>
<h1>Clean fixture <span class="visually-hidden">with text only a screen reader reads</span></h1>
<p><a href="#more">Read more</a></p>
<label for="email">Email</label> <input id="email" type="email">
<button type="button">Send</button>
</main>
</body>
</html>
"""

FAULTY_PAGE = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Faulty fixture</title>
<style>
  #bare:focus, #bare:focus-visible { outline: none; }
  header { position: fixed; top: 0; left: 0; right: 0; height: 120px; background: #222; }
  #hidden { position: absolute; top: 40px; left: 20px; }
  main { margin-top: 160px; }
  .wide { width: 600px; height: 20px; background: #ccc; }
</style>
</head>
<body>
<a id="hidden" href="#a">Under the header</a>
<a id="offscreen" href="#c" style="position: absolute; left: -9999px">Off screen</a>
<header></header>
<main>
<h1>Faulty fixture</h1>
<button type="button"></button>
<p><a id="bare" href="#b">No focus style</a></p>
<div class="wide"></div>
<p id="clipped" style="width: 200px; overflow: hidden; white-space: nowrap">
  This sentence runs far past the edge of its narrow box</p>
<div id="scroller" style="width: 200px; overflow-x: auto; white-space: nowrap">
  This sentence runs past its box too, which scrolls to show it</div>
<img src="missing.png" alt="">
</main>
<script>console.error("fixture error");</script>
</body>
</html>
"""

TRAP_PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Trap fixture</title>
<style>html, body { overflow-x: hidden; }</style>
</head>
<body>
<main>
<span id="parked" style="position: absolute; left: -9999px">Read by screen readers only</span>
<p id="past" style="white-space: nowrap">
  This sentence is long enough to run well past the right edge of a phone screen</p>
<a href="#a">Before</a>
<label for="when">Date</label> <input id="when" type="date">
<bench-pair></bench-pair>
<button id="first" type="button">First in trap</button>
<button id="last" type="button">Last in trap</button>
<a href="#b">After</a>
</main>
<script>
  customElements.define("bench-pair", class extends HTMLElement {
    constructor() {
      super();
      this.attachShadow({mode: "open"}).innerHTML =
        '<button type="button">One</button><button type="button">Two</button>';
    }
  });
  document.getElementById("last").addEventListener("keydown", (event) => {
    if (event.key === "Tab" && !event.shiftKey) {
      event.preventDefault();
      document.getElementById("first").focus();
    }
  });
</script>
</body>
</html>
"""


def _chrome_problem() -> str | None:
    try:
        with sync_playwright() as playwright:
            playwright.chromium.launch(channel="chrome").close()
    except PlaywrightError as error:
        return error.message
    return None


@pytest.fixture(scope="module")
def _chrome() -> None:
    problem = _chrome_problem()
    if problem is not None:
        pytest.skip(f"Chrome could not be started: {problem}")


def _build(folder: Path, html: str) -> Path:
    folder.mkdir()
    (folder / "index.html").write_text(html, encoding="utf-8")
    return folder


def _report(out: Path) -> dict[str, Any]:
    report: dict[str, Any] = json.loads((out / "function.json").read_text(encoding="utf-8"))
    return report


def _capture(build: Path, out: Path, *options: str) -> dict[str, Any]:
    assert main([str(build), str(out), *options]) == 0
    return _report(out)


@pytest.fixture(scope="module")
def clean_out(_chrome: None, tmp_path_factory: pytest.TempPathFactory) -> Path:
    root = tmp_path_factory.mktemp("clean")
    _capture(_build(root / "site", CLEAN_PAGE), root / "out", "--lighthouse")
    return root / "out"


@pytest.fixture(scope="module")
def clean(clean_out: Path) -> dict[str, Any]:
    return _report(clean_out)


def _fake_npx(folder: Path, command: str) -> None:
    """Write an npx into folder that runs one shell command and writes no report."""
    if os.name == "nt":
        (folder / "npx.cmd").write_text(f"@{command}\r\n", encoding="utf-8")
    else:
        script = folder / "npx"
        script.write_text(f"#!/bin/sh\n{command}\n", encoding="utf-8")
        script.chmod(0o755)


def _failing_npx(folder: Path) -> None:
    _fake_npx(folder, "exit /b 1" if os.name == "nt" else "exit 1")


@pytest.fixture(scope="module")
def faulty_out(_chrome: None, tmp_path_factory: pytest.TempPathFactory) -> Path:
    root = tmp_path_factory.mktemp("faulty")
    out = root / "out"
    out.mkdir()
    (out / "lighthouse.json").write_text("{}", encoding="utf-8")
    bin_folder = root / "bin"
    bin_folder.mkdir()
    _failing_npx(bin_folder)
    with pytest.MonkeyPatch.context() as patch:
        patch.setenv("PATH", str(bin_folder))
        _capture(_build(root / "site", FAULTY_PAGE), out, "--lighthouse")
    return out


@pytest.fixture(scope="module")
def faulty(faulty_out: Path) -> dict[str, Any]:
    return _report(faulty_out)


@pytest.fixture(scope="module")
def trap(_chrome: None, tmp_path_factory: pytest.TempPathFactory) -> Iterator[dict[str, Any]]:
    root = tmp_path_factory.mktemp("trap")
    # An empty PATH hides npx, so this capture also shows the Lighthouse step
    # reporting that it could not run.
    with pytest.MonkeyPatch.context() as patch:
        patch.setenv("PATH", str(root))
        yield _capture(_build(root / "site", TRAP_PAGE), root / "out", "--lighthouse")


def _stop(report: dict[str, Any], element: str) -> dict[str, Any]:
    stops: list[dict[str, Any]] = report["keyboard_walk"]["stops"]
    return next(stop for stop in stops if stop["element"].startswith(element))


def test_missing_index_exits_2(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main([str(tmp_path), str(tmp_path / "out")]) == 2
    assert str(tmp_path) in capsys.readouterr().err


def test_unlabelled_button_is_an_axe_violation(faulty: dict[str, Any]) -> None:
    rules = {violation["rule"] for violation in faulty["axe_violations"]}
    assert "button-name" in rules


def test_clean_page_has_no_axe_violations(clean: dict[str, Any]) -> None:
    assert clean["axe_violations"] == []


def test_removed_outline_is_invisible_focus(faulty: dict[str, Any]) -> None:
    assert _stop(faulty, "a#bare")["focus_visible"] is False


def test_default_focus_ring_is_visible(clean: dict[str, Any]) -> None:
    stops = clean["keyboard_walk"]["stops"]
    assert [stop["focus_visible"] for stop in stops] == [True, True, True]


def test_fixed_header_over_focused_link_is_recorded(faulty: dict[str, Any]) -> None:
    assert _stop(faulty, "a#hidden")["covered"] is True
    assert _stop(faulty, "a#bare")["covered"] is False


def test_page_wider_than_phone_overflows(faulty: dict[str, Any]) -> None:
    assert faulty["phone_overflow_px"] > 0


def test_clean_page_does_not_overflow(clean: dict[str, Any]) -> None:
    assert clean["phone_overflow_px"] == 0


def test_text_clipped_by_its_own_box_is_reported(faulty: dict[str, Any]) -> None:
    assert any(label.startswith("p#clipped") for label in faulty["phone_clipped_text"])


def test_text_in_a_box_that_scrolls_is_not_clipped(faulty: dict[str, Any]) -> None:
    assert not any(label.startswith("div#scroller") for label in faulty["phone_clipped_text"])


def test_text_past_the_phone_width_under_hidden_overflow_is_reported(
    trap: dict[str, Any],
) -> None:
    assert trap["phone_overflow_px"] == 0
    assert any(label.startswith("p#past") for label in trap["phone_clipped_text"])


def test_text_parked_wholly_off_screen_is_not_clipped(trap: dict[str, Any]) -> None:
    assert not any(label.startswith("span#parked") for label in trap["phone_clipped_text"])


def test_visually_hidden_text_is_not_clipped(clean: dict[str, Any]) -> None:
    assert clean["phone_clipped_text"] == []


def test_walk_ends_when_focus_leaves_the_page(clean: dict[str, Any]) -> None:
    assert clean["keyboard_walk"]["ended_by"] == "end"


def test_focus_trap_stops_the_walk(trap: dict[str, Any]) -> None:
    walk = trap["keyboard_walk"]
    assert walk["ended_by"] == "repeat"
    assert [stop["element"] for stop in walk["stops"]][-2:] == [
        'button#first "First in trap"',
        'button#last "Last in trap"',
    ]


def test_date_input_and_shadow_root_are_one_stop_each(trap: dict[str, Any]) -> None:
    # Tab moves between a date input's fields, and between a shadow root's
    # buttons, while the document's active element stays the same.
    elements = [stop["element"] for stop in trap["keyboard_walk"]["stops"]]
    assert elements[:3] == ['a "Before"', "input#when", "bench-pair"]


def test_focus_target_outside_the_viewport_is_invisible_focus(faulty: dict[str, Any]) -> None:
    assert _stop(faulty, "a#offscreen")["focus_visible"] is False


def test_head_tags_are_recorded(clean: dict[str, Any], faulty: dict[str, Any]) -> None:
    assert all(clean["head"].values())
    assert faulty["head"] == {
        "title": True,
        "lang": False,
        "viewport": True,
        "description": False,
        "og_image": False,
    }


def test_console_errors_are_recorded(faulty: dict[str, Any], clean: dict[str, Any]) -> None:
    assert "fixture error" in faulty["console_errors"]
    assert clean["console_errors"] == []


def test_failed_requests_are_recorded_against_the_local_path(faulty: dict[str, Any]) -> None:
    assert faulty["failed_requests"] == ["/missing.png 404"]


def test_every_view_is_captured(clean_out: Path) -> None:
    names = {path.name for path in clean_out.glob("*.png")}
    for viewport in ("desktop", "phone"):
        expected = {f"{viewport}-{view}.png" for view in ("first", "full", "reduced")}
        expected |= {f"{viewport}-scroll-{depth}.png" for depth in (25, 50, 75)}
        expected |= {f"{viewport}-motion-{s}s.png" for s in (0.25, 0.75, 1.5, 3.0)}
        assert expected <= names


def test_motion_frames_are_taken_no_earlier_than_scheduled(clean: dict[str, Any]) -> None:
    for name, seconds in clean["motion_frame_seconds"].items():
        scheduled = float(name.rsplit("-", 1)[1].removesuffix("s.png"))
        assert seconds >= scheduled


# Longer than the 1 s load timeout, so the response commits after it has passed.
SLOW_RESPONSE_SECONDS = 1.5


@pytest.fixture(scope="module")
def slow_out(_chrome: None, tmp_path_factory: pytest.TempPathFactory) -> Iterator[Path]:
    """Capture a page whose image comes from a port that accepts and never answers."""
    root = tmp_path_factory.mktemp("slow")
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        listener.listen()
        port = listener.getsockname()[1]
        html = CLEAN_PAGE.replace(
            "</main>", f'<img src="http://127.0.0.1:{port}/slow.png" alt=""></main>'
        )
        _capture(_build(root / "site", html), root / "out", "--load-timeout", "1")
        yield root / "out"


def test_load_that_never_finishes_is_recorded(slow_out: Path) -> None:
    report = _report(slow_out)
    assert report["timed_out_loads"] == ["desktop", "phone", "desktop-reduced", "phone-reduced"]
    assert (slow_out / "desktop-first.png").is_file()


@pytest.mark.usefixtures("_chrome")
def test_response_slower_than_the_load_timeout_is_still_captured(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def answer_late(handler: SimpleHTTPRequestHandler) -> None:
        time.sleep(SLOW_RESPONSE_SECONDS)
        SimpleHTTPRequestHandler.do_GET(handler)

    monkeypatch.setattr(capture._QuietHandler, "do_GET", answer_late)
    build = _build(tmp_path / "site", CLEAN_PAGE)
    report = _capture(build, tmp_path / "out", "--load-timeout", "1")
    assert (tmp_path / "out" / "phone-reduced.png").is_file()
    assert report["phone_overflow_px"] == 0


@pytest.mark.skipif(shutil.which("npx") is None, reason="npx is needed to run Lighthouse")
def test_lighthouse_report_is_judged_against_budgets(clean: dict[str, Any]) -> None:
    budgets = clean["budgets"]
    assert budgets["exit_code"] in {0, 1}
    assert budgets["lines"]
    assert all(line.split()[0] in {"pass", "breach"} for line in budgets["lines"])


def test_missing_npx_is_reported_instead_of_budgets(trap: dict[str, Any]) -> None:
    assert trap["budgets"] == {
        "exit_code": 2,
        "lines": ["lighthouse not run: npx not found on PATH"],
    }


def test_failed_lighthouse_run_is_not_judged_on_an_old_report(
    faulty_out: Path, faulty: dict[str, Any]
) -> None:
    assert not (faulty_out / "lighthouse.json").exists()
    assert faulty["budgets"]["exit_code"] == 2


def test_capture_without_lighthouse_records_no_budgets(slow_out: Path) -> None:
    assert _report(slow_out)["budgets"] is None


@pytest.mark.parametrize("seconds", ["0", "-1"])
def test_load_timeout_must_be_positive(tmp_path: Path, seconds: str) -> None:
    with pytest.raises(SystemExit) as raised:
        main([str(tmp_path), str(tmp_path / "out"), "--load-timeout", seconds])
    assert raised.value.code == 2


@pytest.fixture
def npx_bin(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A folder searched for npx before the rest of PATH."""
    folder = tmp_path / "bin"
    folder.mkdir()
    monkeypatch.setenv("PATH", f"{folder}{os.pathsep}{os.environ['PATH']}")
    return folder


def test_lighthouse_that_overruns_is_stopped_with_its_children(
    tmp_path: Path, npx_bin: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # The child outlives npx's own process and, until stopped, holds its output.
    marker = tmp_path / "child-survived"
    child = tmp_path / "child.py"
    child.write_text(
        f"import pathlib, time\ntime.sleep(4)\npathlib.Path({str(marker)!r}).write_text('x')\n",
        encoding="utf-8",
    )
    _fake_npx(npx_bin, f'"{sys.executable}" "{child}"')
    monkeypatch.setattr(capture, "LIGHTHOUSE_TIMEOUT_SECONDS", 1.0)
    started = time.monotonic()
    budgets = run_lighthouse("http://127.0.0.1:9/", tmp_path)
    assert time.monotonic() - started < 3.5
    assert budgets == Budgets(2, ["lighthouse not run: no report within 1.0 s"])
    time.sleep(5)
    assert not marker.exists()


def _fake_check_budgets(
    tmp_path: Path, npx_bin: Path, monkeypatch: pytest.MonkeyPatch, source: str
) -> None:
    _fake_npx(npx_bin, "exit /b 0" if os.name == "nt" else "exit 0")
    script = tmp_path / "check_budgets.py"
    script.write_text(source, encoding="utf-8")
    monkeypatch.setattr(capture, "CHECK_BUDGETS", script)


def test_budget_check_that_overruns_is_unmeasured(
    tmp_path: Path, npx_bin: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _fake_check_budgets(tmp_path, npx_bin, monkeypatch, "import time\ntime.sleep(10)\n")
    monkeypatch.setattr(capture, "CHECK_BUDGETS_TIMEOUT_SECONDS", 1.0)
    assert run_lighthouse("http://127.0.0.1:9/", tmp_path) == Budgets(
        2, ["budgets not judged: check_budgets.py gave no result within 1.0 s"]
    )


def test_budget_check_that_crashes_is_unmeasured_not_a_breach(
    tmp_path: Path, npx_bin: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _fake_check_budgets(tmp_path, npx_bin, monkeypatch, "raise RuntimeError('boom')\n")
    budgets = run_lighthouse("http://127.0.0.1:9/", tmp_path)
    assert budgets.exit_code == 2
    assert budgets.lines[0] == "budgets not judged: check_budgets.py exited 1 without a breach"
    assert "RuntimeError: boom" in budgets.lines


def test_budget_check_that_reports_a_breach_is_a_breach(
    tmp_path: Path, npx_bin: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = "print('breach  LCP 3100 ms (budget 2500 ms)')\nraise SystemExit(1)\n"
    _fake_check_budgets(tmp_path, npx_bin, monkeypatch, source)
    assert run_lighthouse("http://127.0.0.1:9/", tmp_path) == Budgets(
        1, ["breach  LCP 3100 ms (budget 2500 ms)"]
    )


HUNG_PAGE = '<!doctype html><html lang="en"><title>Hung</title><script>while (true) {}</script>'


@pytest.mark.usefixtures("_chrome")
def test_page_that_never_yields_exits_2_and_leaves_no_report(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    out = tmp_path / "out"
    out.mkdir()
    (out / "function.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(capture, "ACTION_TIMEOUT_SECONDS", 2.0)
    build = _build(tmp_path / "site", HUNG_PAGE)
    assert main([str(build), str(out), "--load-timeout", "2"]) == 2
    assert str(build) in capsys.readouterr().err
    assert not (out / "function.json").exists()


def test_chrome_that_cannot_start_exits_2(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def refuse(*_args: object, **_kwargs: object) -> None:
        raise PlaywrightError("no Chrome here")

    monkeypatch.setattr(BrowserType, "launch", refuse)
    build = _build(tmp_path / "site", CLEAN_PAGE)
    assert main([str(build), str(tmp_path / "out")]) == 2
    assert "Chrome could not be started: no Chrome here" in capsys.readouterr().err


# Each scroll lengthens the page by a screen, so only the step limit ends the pass.
ENDLESS_PAGE = CLEAN_PAGE.replace(
    "</body>",
    "<script>addEventListener('scroll', () => {"
    " document.body.style.minHeight = document.body.scrollHeight + innerHeight + 'px'; });"
    "</script></body>",
)


@pytest.fixture(scope="module")
def endless(_chrome: None, tmp_path_factory: pytest.TempPathFactory) -> dict[str, Any]:
    root = tmp_path_factory.mktemp("endless")
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(capture, "MAX_TAB_STOPS", 2)
        patch.setattr(capture, "MAX_SCROLL_STEPS", 3)
        return _capture(_build(root / "site", ENDLESS_PAGE), root / "out")


def test_walk_stops_at_the_tab_stop_limit(endless: dict[str, Any]) -> None:
    walk = endless["keyboard_walk"]
    assert walk["ended_by"] == "limit"
    assert len(walk["stops"]) == 2


def test_page_that_grows_on_scroll_is_captured(endless: dict[str, Any]) -> None:
    assert endless["timed_out_loads"] == []
    assert endless["elapsed_seconds"] < CAPTURE_BUDGET_SECONDS
