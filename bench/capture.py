"""Capture one built page for the design bench and check how it functions.

Usage:
    python bench/capture.py BUILD OUT [--lighthouse] [--load-timeout SECONDS]

BUILD is a folder holding index.html. It is served over local HTTP and opened
in the installed Chrome at a desktop viewport (1440 by 900) and a phone
viewport (375 by 812). For each viewport OUT receives the first screen, the
first screen at fixed times after navigation, frames at three scroll depths,
the full page after a scroll pass, and the first screen with reduced motion.

OUT also receives function.json: axe violations, a keyboard walk recording for
each tab stop whether focus is visible and whether a fixed or sticky element
covers it, horizontal overflow at the phone width, console errors, failed
requests, head tags, and loads that hit the timeout. It also lists, by element,
text the reader cannot reach at the phone width: text running past a box whose
overflow is hidden or clipped, or past the screen's edge when the layout does
not widen to show it. With --lighthouse a mobile
Lighthouse report is written and judged by the skill's check_budgets.py.

Exit code 2 means no function.json was written: BUILD has no index.html,
Chrome could not be started, or a step of the capture failed, such as a
screenshot of a page whose script never yields. Each browser step waits at most
30 s. A function.json from an earlier capture is removed first, so OUT never
holds one that describes another build. Otherwise the exit code is 0 and the
elapsed capture time is printed beside its budget.

Limits: the keyboard walk stops after 200 presses of Tab, the scroll pass after
60 viewport heights, the clipped-text check after 5,000 text nodes and 20
elements reported, Lighthouse after 180 s with every process it started, and
the budget check after 60 s. A budget check that overruns or crashes is
recorded as unmeasured, never as a breach.

A date input, a shadow root or an iframe is one tab stop however many presses
of Tab cross it, since the document's active element stays the same, so focus
inside it is not judged separately. A focus indicator is judged visible when
any pixel around the element changes, so a moving video or canvas behind it
reads as visible. Overflow counts only content that widens the layout: content
clipped by overflow: hidden on both html and body reads as 0 px, and is
reported as clipped text instead; on either alone the layout still widens.

Text in a box that scrolls is reachable, so it is never clipped; text in a box
1 px or smaller is visually hidden for screen readers, so it is not either.
Clipping is judged across the width only, and text moved off screen, such as
in a closed drawer, reads as clipped unless its visibility is hidden.
"""

from __future__ import annotations

import argparse
import functools
import json
import os
import shutil
import signal
import subprocess
import sys
import threading
import time
from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field, replace
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Literal

from axe_playwright_python.sync_playwright import Axe
from playwright.sync_api import Browser, FloatRect, Page, sync_playwright
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from views import (
    CAPTURE_BUDGET_SECONDS,
    MOTION_FRAME_SECONDS,
    SCROLL_DEPTHS_PERCENT,
    motion_image,
    scroll_image,
)

DEFAULT_LOAD_TIMEOUT_SECONDS = 30.0
ACTION_TIMEOUT_SECONDS = 30.0
MAX_TAB_STOPS = 200
MAX_SCROLL_STEPS = 60
MAX_TEXT_NODES = 5000
MAX_CLIPPED_REPORTED = 20
SCROLL_STEP_PAUSE_MS = 120
SCROLL_SETTLE_MS = 600
FOCUS_RING_MARGIN_PX = 8
FIRST_HTTP_ERROR_STATUS = 400
LIGHTHOUSE_TIMEOUT_SECONDS = 180.0
CHECK_BUDGETS_TIMEOUT_SECONDS = 60.0
TASKKILL_TIMEOUT_SECONDS = 10.0

LIGHTHOUSE_PACKAGE = "lighthouse@13.6.0"
CHECK_BUDGETS = (
    Path(__file__).resolve().parent.parent
    / "skills"
    / "web-ui-craft"
    / "scripts"
    / "check_budgets.py"
)

# Applied for the keyboard walk only. Without it a focused screenshot can show
# a frame mid-transition, or the element mid-way through a smooth scroll into
# view, away from the box that was measured.
SETTLED_FOCUS_CSS = (
    "*, *::before, *::after { transition: none !important; scroll-behavior: auto !important; }"
)

# Defines label(el): the element's tag, id and first 40 characters of its text.
ELEMENT_LABEL_JS = """
const label = (el) => {
  const text = (el.getAttribute('aria-label') || el.textContent || '').trim().slice(0, 40);
  return el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + (text ? ' "' + text + '"' : '');
};
"""

# Returns null when focus has left the page's elements (it sits on body), and
# {same: true} when focus moved within the element of the last stop. Otherwise
# returns whether the stop was reached before, a short label, its box, and
# whether a fixed or sticky element lies over its centre.
FOCUSED_STOP_JS = f"""
() => {{
  {ELEMENT_LABEL_JS}
  const el = document.activeElement;
  if (!el || el === document.body || el === document.documentElement) return null;
  if (el === window.__benchLastStop) return {{same: true}};
  window.__benchLastStop = el;
  const seen = (window.__benchStops ??= []);
  const repeat = seen.includes(el);
  if (!repeat) seen.push(el);
  const r = el.getBoundingClientRect();
  const top = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
  let covered = false;
  if (top && !el.contains(top) && !top.contains(el)) {{
    for (let n = top; n; n = n.parentElement) {{
      const position = getComputedStyle(n).position;
      if (position === 'fixed' || position === 'sticky') {{ covered = true; break; }}
    }}
  }}
  return {{same: false, repeat, label: label(el), covered,
          box: {{x: r.left, y: r.top, width: r.width, height: r.height}}}};
}}
"""

# Takes [MAX_TEXT_NODES, MAX_CLIPPED_REPORTED] and returns the labels of the
# elements holding text that runs past a clipping ancestor or the screen's
# edge. The walk up stops at body: overflow set there clips at the screen's
# edge, which the last check covers.
CLIPPED_TEXT_JS = f"""
([maxNodes, maxReported]) => {{
  {ELEMENT_LABEL_JS}
  const root = document.documentElement;
  const layoutIsWider = root.scrollWidth > root.clientWidth;
  const beyond = (r, left, right) => r.right > right + 1 || r.left < left - 1;
  const isClipped = (el, r) => {{
    for (let box = el; box && box !== document.body; box = box.parentElement) {{
      const overflow = getComputedStyle(box).overflowX;
      if (overflow === 'auto' || overflow === 'scroll') return false;
      if (overflow !== 'hidden' && overflow !== 'clip') continue;
      const b = box.getBoundingClientRect();
      if (b.width <= 1 || b.height <= 1) return false;
      if (beyond(r, b.left, b.right)) return true;
    }}
    return !layoutIsWider && beyond(r, 0, root.clientWidth);
  }};
  const clipped = new Set();
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let n = 0; n < maxNodes && clipped.size < maxReported; n++) {{
    const node = walker.nextNode();
    if (!node) break;
    const el = node.parentElement;
    if (!el || clipped.has(el) || !node.textContent.trim()) continue;
    if (getComputedStyle(el).visibility !== 'visible') continue;
    const range = document.createRange();
    range.selectNodeContents(node);
    const rects = [...range.getClientRects()].filter((r) => r.width > 0);
    if (rects.some((r) => isClipped(el, r))) clipped.add(el);
  }}
  return [...clipped].map(label);
}}
"""

HEAD_TAGS_JS = """
() => ({
  title: document.title.trim() !== '',
  lang: (document.documentElement.getAttribute('lang') || '').trim() !== '',
  viewport: document.querySelector('meta[name="viewport"]') !== null,
  description: document.querySelector('meta[name="description"]') !== null,
  og_image: document.querySelector('meta[property="og:image"]') !== null,
})
"""

# The layout width, not innerWidth: mobile Chrome zooms out to fit content
# wider than the screen, which widens innerWidth to match it. Content clipped
# by overflow: hidden on both html and body does not widen the layout, so it
# reads as 0 px although the reader cannot reach it.
OVERFLOW_JS = "() => document.documentElement.scrollWidth - document.documentElement.clientWidth"


@dataclass(frozen=True, slots=True)
class Viewport:
    name: str
    width: int
    height: int
    is_phone: bool


DESKTOP = Viewport("desktop", 1440, 900, is_phone=False)
PHONE = Viewport("phone", 375, 812, is_phone=True)


@dataclass(frozen=True, slots=True)
class TabStop:
    element: str
    focus_visible: bool
    covered: bool


@dataclass(frozen=True, slots=True)
class KeyboardWalk:
    stops: list[TabStop]
    # end: focus left the page's elements; repeat: focus came back to an
    # earlier stop without leaving them (a trap); limit: MAX_TAB_STOPS presses
    # of Tab, which is also how a single element that keeps focus ends.
    ended_by: Literal["end", "repeat", "limit"]


@dataclass(frozen=True, slots=True)
class Violation:
    rule: str
    impact: str
    nodes: int


@dataclass(frozen=True, slots=True)
class HeadTags:
    title: bool
    lang: bool
    viewport: bool
    description: bool
    og_image: bool


@dataclass(frozen=True, slots=True)
class Budgets:
    exit_code: int
    lines: list[str]


@dataclass(slots=True)
class PageEvents:
    """Problems reported by any page opened during a capture."""

    console_errors: set[str] = field(default_factory=set)
    failed_requests: set[str] = field(default_factory=set)
    timed_out_loads: list[str] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class FunctionReport:
    elapsed_seconds: float
    axe_violations: list[Violation]
    keyboard_walk: KeyboardWalk
    phone_overflow_px: int
    phone_clipped_text: list[str]
    head: HeadTags
    console_errors: list[str]
    failed_requests: list[str]
    timed_out_loads: list[str]
    motion_frame_seconds: dict[str, float]
    budgets: Budgets | None


class _QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args: Any) -> None:
        """Keep request lines out of the capture's output."""


@contextmanager
def serve_folder(folder: Path) -> Iterator[str]:
    """Serve folder on a free local port and yield its base URL."""
    handler = functools.partial(_QuietHandler, directory=str(folder))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}/"
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


@dataclass(frozen=True, slots=True)
class CaptureRun:
    """What every load in one capture shares."""

    browser: Browser
    url: str
    out: Path
    load_timeout_ms: float
    events: PageEvents


def _watch(page: Page, run: CaptureRun) -> None:
    def local(url: str) -> str:
        return url.replace(run.url, "/", 1)

    events = run.events
    page.on(
        "console",
        lambda message: (
            events.console_errors.add(message.text) if message.type == "error" else None
        ),
    )
    page.on("pageerror", lambda error: events.console_errors.add(str(error)))
    page.on(
        "requestfailed",
        lambda request: events.failed_requests.add(f"{local(request.url)} {request.failure}"),
    )
    page.on(
        "response",
        lambda response: (
            events.failed_requests.add(f"{local(response.url)} {response.status}")
            if response.status >= FIRST_HTTP_ERROR_STATUS
            else None
        ),
    )


def _open(run: CaptureRun, viewport: Viewport, *, reduced: bool) -> tuple[Page, float]:
    """Navigate a new context and return its page with the moment the response committed."""
    context = run.browser.new_context(
        viewport={"width": viewport.width, "height": viewport.height},
        device_scale_factor=2 if viewport.is_phone else 1,
        is_mobile=viewport.is_phone,
        has_touch=viewport.is_phone,
        reduced_motion="reduce" if reduced else "no-preference",
    )
    context.set_default_timeout(ACTION_TIMEOUT_SECONDS * 1000)
    page = context.new_page()
    _watch(page, run)
    # Bounded by the action timeout, not the load timeout: a commit slower than
    # a short load timeout would otherwise fail the capture instead of being
    # recorded as a load that timed out.
    page.goto(run.url, wait_until="commit")
    return page, time.monotonic()


def _finish_loading(run: CaptureRun, page: Page, load_name: str) -> None:
    try:
        page.wait_for_load_state("load", timeout=run.load_timeout_ms)
    except PlaywrightTimeoutError:
        run.events.timed_out_loads.append(load_name)


def _shoot_motion_strip(
    page: Page, committed_at: float, out: Path, prefix: str
) -> dict[str, float]:
    taken_at: dict[str, float] = {}
    for seconds in MOTION_FRAME_SECONDS:
        wait_ms = (committed_at + seconds - time.monotonic()) * 1000
        if wait_ms > 0:
            page.wait_for_timeout(wait_ms)
        name = motion_image(prefix, seconds)
        page.screenshot(path=out / name)
        taken_at[name] = round(time.monotonic() - committed_at, 2)
    return taken_at


def _scroll_to(page: Page, fraction: float) -> None:
    page.evaluate(
        "(f) => window.scrollTo({top: f * (document.documentElement.scrollHeight"
        " - window.innerHeight), behavior: 'instant'})",
        fraction,
    )


def _shoot_scroll(page: Page, out: Path, prefix: str) -> None:
    for percent in SCROLL_DEPTHS_PERCENT:
        _scroll_to(page, percent / 100)
        page.wait_for_timeout(SCROLL_SETTLE_MS)
        page.screenshot(path=out / scroll_image(prefix, percent))
    # A pass to the foot of the page triggers reveal-on-scroll content before
    # the full-page shot, which would otherwise show it in its hidden state.
    for _ in range(MAX_SCROLL_STEPS):
        at_foot = page.evaluate(
            "() => { window.scrollBy({top: window.innerHeight, behavior: 'instant'});"
            " return window.scrollY + window.innerHeight"
            " >= document.documentElement.scrollHeight - 1; }"
        )
        page.wait_for_timeout(SCROLL_STEP_PAUSE_MS)
        if at_foot:
            break
    _scroll_to(page, 0)
    page.wait_for_timeout(SCROLL_SETTLE_MS)
    page.screenshot(path=out / f"{prefix}-full.png", full_page=True)


def shoot_viewport(run: CaptureRun, viewport: Viewport) -> tuple[Page, dict[str, float]]:
    """Take the default-motion shots and return the page, still open, for checks."""
    page, committed_at = _open(run, viewport, reduced=False)
    taken_at = _shoot_motion_strip(page, committed_at, run.out, viewport.name)
    _finish_loading(run, page, viewport.name)
    page.screenshot(path=run.out / f"{viewport.name}-first.png")
    _shoot_scroll(page, run.out, viewport.name)
    return page, taken_at


def shoot_reduced_motion(run: CaptureRun, viewport: Viewport) -> None:
    load_name = f"{viewport.name}-reduced"
    page, _ = _open(run, viewport, reduced=True)
    try:
        _finish_loading(run, page, load_name)
        page.screenshot(path=run.out / f"{load_name}.png")
    finally:
        page.context.close()


def _clip(box: dict[str, float], viewport: Viewport) -> FloatRect | None:
    left = max(box["x"] - FOCUS_RING_MARGIN_PX, 0.0)
    top = max(box["y"] - FOCUS_RING_MARGIN_PX, 0.0)
    right = min(box["x"] + box["width"] + FOCUS_RING_MARGIN_PX, float(viewport.width))
    bottom = min(box["y"] + box["height"] + FOCUS_RING_MARGIN_PX, float(viewport.height))
    if right <= left or bottom <= top:
        return None
    return {"x": left, "y": top, "width": right - left, "height": bottom - top}


def _focus_shows(page: Page, clip: FloatRect | None) -> bool:
    """Compare the area around the focused element with and without focus."""
    if clip is None:
        return False
    focused = page.screenshot(clip=clip, animations="disabled")
    page.evaluate(
        "() => { const el = document.activeElement; window.__benchLast = el; el.blur(); }"
    )
    unfocused = page.screenshot(clip=clip, animations="disabled")
    page.evaluate("() => window.__benchLast.focus()")
    return focused != unfocused


def walk_keyboard(page: Page, viewport: Viewport) -> KeyboardWalk:
    page.add_style_tag(content=SETTLED_FOCUS_CSS)
    page.evaluate("() => { window.scrollTo(0, 0); document.activeElement?.blur(); }")
    stops: list[TabStop] = []
    for _ in range(MAX_TAB_STOPS):
        page.keyboard.press("Tab")
        stop = page.evaluate(FOCUSED_STOP_JS)
        if stop is None:
            return KeyboardWalk(stops, "end")
        if stop["same"]:
            continue
        if stop["repeat"]:
            return KeyboardWalk(stops, "repeat")
        visible = _focus_shows(page, _clip(stop["box"], viewport))
        stops.append(TabStop(str(stop["label"]), visible, bool(stop["covered"])))
    return KeyboardWalk(stops, "limit")


def run_axe(page: Page) -> list[Violation]:
    response = Axe().run(page).response
    violations = [
        Violation(str(v["id"]), str(v["impact"]), len(v["nodes"])) for v in response["violations"]
    ]
    return sorted(violations, key=lambda v: v.rule)


def read_head(page: Page) -> HeadTags:
    # HEAD_TAGS_JS returns exactly HeadTags' fields, each already a boolean.
    return HeadTags(**page.evaluate(HEAD_TAGS_JS))


def run_lighthouse(url: str, out: Path) -> Budgets:
    """Run a mobile Lighthouse pass and judge it with check_budgets.py."""
    npx = shutil.which("npx")
    if npx is None:
        return Budgets(2, ["lighthouse not run: npx not found on PATH"])
    report = out / "lighthouse.json"
    # A report left by an earlier capture must not be judged if this run fails.
    report.unlink(missing_ok=True)
    command = [npx, "--yes", LIGHTHOUSE_PACKAGE, url, "--output=json", f"--output-path={report}"]
    command += ["--quiet", "--chrome-flags=--headless=new"]
    if not _run_bounded(command, LIGHTHOUSE_TIMEOUT_SECONDS):
        return Budgets(2, [f"lighthouse not run: no report within {LIGHTHOUSE_TIMEOUT_SECONDS} s"])
    # check_budgets.py reports a missing or failed report itself, with exit code 2.
    try:
        judged = subprocess.run(  # noqa: S603 (arguments are constants and paths this script made)
            [sys.executable, str(CHECK_BUDGETS), str(report)],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=CHECK_BUDGETS_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return Budgets(
            2,
            [
                "budgets not judged: check_budgets.py gave no result"
                f" within {CHECK_BUDGETS_TIMEOUT_SECONDS} s"
            ],
        )
    lines = (judged.stdout + judged.stderr).splitlines()
    breached = any(line.startswith("breach") for line in lines)
    if judged.returncode in {0, 2} or (judged.returncode == 1 and breached):
        return Budgets(judged.returncode, lines)
    # A crash exits 1 too, so exit 1 is a breach only when a breach was printed.
    message = f"budgets not judged: check_budgets.py exited {judged.returncode} without a breach"
    return Budgets(2, [message, *lines])


def _run_bounded(command: list[str], timeout_seconds: float) -> bool:
    """Run command with its output discarded; False when it overran and was stopped.

    npx starts node, which starts Chrome, so stopping npx alone would leave both
    running. The whole process tree is stopped instead.
    """
    process = subprocess.Popen(  # noqa: S603 (arguments are constants and paths this script made)
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=sys.platform != "win32",
    )
    try:
        process.wait(timeout=timeout_seconds)
    except subprocess.TimeoutExpired:
        _stop_tree(process)
        return False
    return True


def _stop_tree(process: subprocess.Popen[bytes]) -> None:
    if sys.platform == "win32":
        # The exit code is not checked: taskkill also fails when the tree has
        # already ended, and kill() below stops the parent either way.
        subprocess.run(  # noqa: S603 (arguments are constants and a process id)
            ["taskkill", "/T", "/F", "/PID", str(process.pid)],  # noqa: S607 (a Windows system tool)
            check=False,
            capture_output=True,
            timeout=TASKKILL_TIMEOUT_SECONDS,
        )
    else:
        os.killpg(process.pid, signal.SIGKILL)
    process.kill()
    process.wait()


def capture_build(browser: Browser, url: str, out: Path, load_timeout_ms: float) -> FunctionReport:
    started = time.monotonic()
    run = CaptureRun(browser, url, out, load_timeout_ms, PageEvents())
    desktop, taken_at = shoot_viewport(run, DESKTOP)
    phone, phone_taken_at = shoot_viewport(run, PHONE)
    overflow_px = int(phone.evaluate(OVERFLOW_JS))
    clipped_text = [
        str(label)
        for label in phone.evaluate(CLIPPED_TEXT_JS, [MAX_TEXT_NODES, MAX_CLIPPED_REPORTED])
    ]
    phone.context.close()
    head = read_head(desktop)
    violations = run_axe(desktop)
    walk = walk_keyboard(desktop, DESKTOP)
    desktop.context.close()
    for viewport in (DESKTOP, PHONE):
        shoot_reduced_motion(run, viewport)
    return FunctionReport(
        elapsed_seconds=round(time.monotonic() - started, 1),
        axe_violations=violations,
        keyboard_walk=walk,
        phone_overflow_px=max(overflow_px, 0),
        phone_clipped_text=clipped_text,
        head=head,
        console_errors=sorted(run.events.console_errors),
        failed_requests=sorted(run.events.failed_requests),
        timed_out_loads=run.events.timed_out_loads,
        motion_frame_seconds=taken_at | phone_taken_at,
        budgets=None,
    )


def _positive_seconds(text: str) -> float:
    seconds = float(text)
    if seconds <= 0:
        raise argparse.ArgumentTypeError(f"expected a positive number of seconds, got {text!r}")
    return seconds


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else None)
    parser.add_argument("build", type=Path, help="folder holding index.html")
    parser.add_argument("out", type=Path, help="folder for images and function.json")
    parser.add_argument("--lighthouse", action="store_true", help="also judge page budgets")
    parser.add_argument(
        "--load-timeout", type=_positive_seconds, default=DEFAULT_LOAD_TIMEOUT_SECONDS
    )
    args = parser.parse_args(argv)
    if not (args.build / "index.html").is_file():
        print(f"no index.html in {args.build}", file=sys.stderr)
        return 2
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "function.json").unlink(missing_ok=True)
    with serve_folder(args.build) as url, sync_playwright() as playwright:
        try:
            browser = playwright.chromium.launch(channel="chrome")
        except PlaywrightError as error:
            print(f"Chrome could not be started: {error.message}", file=sys.stderr)
            return 2
        try:
            report = capture_build(browser, url, args.out, args.load_timeout * 1000)
        except PlaywrightError as error:
            print(f"capture of {args.build} failed: {error.message}", file=sys.stderr)
            return 2
        finally:
            browser.close()
        if args.lighthouse:
            report = replace(report, budgets=run_lighthouse(url, args.out))
    (args.out / "function.json").write_text(
        json.dumps(asdict(report), indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"captured {args.build} in {report.elapsed_seconds} s"
        f" (budget {CAPTURE_BUDGET_SECONDS} s, Lighthouse excluded)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
