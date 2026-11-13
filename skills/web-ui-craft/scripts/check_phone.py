"""Measure how far a page runs past the edge of a phone screen.

Usage:
    python check_phone.py PAGE

PAGE is the page's HTML file. Its folder is served over HTTP on 127.0.0.1 as the
site root, so scripts that fetch files and root-relative paths work as they do
when the site is served; for an app with a build step, pass the built
index.html. Headless Chrome loads the page in a frame 375 px wide, waits 1.5 s
of page time for entrance motion to settle, and measures the whole page, not
only its first screen. It prints the overflow in px and up to 10 elements whose
box reaches past the right edge, each with how far it reaches. Elements inside a
box that scrolls or clips are not listed, since they cannot widen the page; the
overflow figure is measured either way. A page that hides its overflow on both
html and body measures 0 px, and the content it cuts off is not reported.

A page without a viewport meta tag is also a breach: a frame lays it out at its
own width, but a phone lays it out at 980 px and shrinks it.

Exit code 0 means no overflow, 1 means the page is wider than the phone or has
no viewport tag, and 2 means nothing was measured: no Chrome, a missing page, a
timeout, or a page that rendered nothing in the frame.

Chrome is found through the CHROME_PATH environment variable, then on PATH, then
in the usual install locations of Chrome and Edge.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
from dataclasses import dataclass
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from string import Template
from typing import Any
from urllib.parse import quote

PHONE_WIDTH_PX = 375
PHONE_HEIGHT_PX = 812
SETTLE_MS = 1500
VIRTUAL_TIME_BUDGET_MS = 5000
CHROME_TIMEOUT_SECONDS = 60
MAX_ELEMENTS_LISTED = 10
WRAPPER_PATH = "/__check_phone__/wrapper.html"

CHROME_NAMES = ("chrome", "google-chrome", "google-chrome-stable", "chromium", "chromium-browser")
WINDOWS_FOLDER_VARIABLES = ("ProgramFiles", "ProgramFiles(x86)", "LOCALAPPDATA")
CHROME_INSTALL_PATHS = (
    "{ProgramFiles}/Google/Chrome/Application/chrome.exe",
    "{ProgramFiles(x86)}/Google/Chrome/Application/chrome.exe",
    "{LOCALAPPDATA}/Google/Chrome/Application/chrome.exe",
    "{ProgramFiles(x86)}/Microsoft/Edge/Application/msedge.exe",
    "{ProgramFiles}/Microsoft/Edge/Application/msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
)

# The wrapper is served from the same origin as the page so it can read the frame,
# and it writes its report into its own DOM, which Chrome prints with --dump-dom.
WRAPPER = Template("""<!doctype html>
<meta charset="utf-8">
<pre id="report">not measured</pre>
<iframe id="page" src="$page_url" width="$width" height="$height" style="border:0"></iframe>
<script>
page.onload = () => setTimeout(() => {
  const doc = page.contentDocument, root = doc.documentElement, width = root.clientWidth;
  const sized = (el) => {
    const box = el.getBoundingClientRect();
    return box.width > 0 && box.height > 0;
  };
  const contained = (el) => {
    if (el.parentElement.closest("svg")) return true;
    for (let box = el.parentElement; box !== doc.body; box = box.parentElement)
      if (getComputedStyle(box).overflowX !== "visible") return true;
    return false;
  };
  const name = (el) => el.tagName.toLowerCase() + (el.id ? "#" + el.id : "")
    + [...el.classList].map((c) => "." + c).join("");
  const wide = [];
  for (const el of doc.body.querySelectorAll("*")) {
    const box = el.getBoundingClientRect(), reach = box.right - width;
    if (box.width > 0 && reach > 0.5 && !contained(el))
      wide.push({element: name(el), reach_px: Math.round(reach)});
    if (wide.length === $limit) break;
  }
  report.textContent = JSON.stringify({
    rendered: [...doc.body.querySelectorAll("*")].some(sized),
    has_viewport_meta: doc.querySelector('meta[name="viewport" i]') !== null,
    overflow_px: root.scrollWidth - width,
    elements: wide,
  });
}, $settle_ms);
</script>
""")
REPORT_PATTERN = re.compile(r'<pre id="report">(.*?)</pre>', re.DOTALL)


class MeasureError(Exception):
    """The page could not be measured."""


@dataclass(frozen=True, slots=True)
class WideElement:
    element: str
    reach_px: int


@dataclass(frozen=True, slots=True)
class Measurement:
    overflow_px: int
    has_viewport_meta: bool
    elements: tuple[WideElement, ...]


class PageHandler(SimpleHTTPRequestHandler):
    """Serves the page's folder, and the wrapper at a path no site uses."""

    def __init__(self, *args: Any, wrapper: bytes, **kwargs: Any) -> None:
        self.wrapper = wrapper
        super().__init__(*args, **kwargs)

    def do_GET(self) -> None:
        if self.path != WRAPPER_PATH:
            super().do_GET()
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(self.wrapper)))
        self.end_headers()
        self.wfile.write(self.wrapper)

    def log_message(self, *args: Any) -> None:
        """Keep request lines out of the report."""


def find_chrome() -> Path | None:
    configured = os.environ.get("CHROME_PATH")
    if configured:
        return Path(configured) if Path(configured).is_file() else None
    for name in CHROME_NAMES:
        found = shutil.which(name)
        if found:
            return Path(found)
    # An unset folder variable leaves a path under the root that does not exist.
    folders = {key: os.environ.get(key, "") for key in WINDOWS_FOLDER_VARIABLES}
    for pattern in CHROME_INSTALL_PATHS:
        path = Path(pattern.format_map(folders))
        if path.is_file():
            return path
    return None


def parse_report(dom: str) -> Measurement:
    match = REPORT_PATTERN.search(dom)
    if match is None:
        raise MeasureError("Chrome printed no report; the wrapper page did not run")
    text = html.unescape(match.group(1))
    try:
        report = json.loads(text)
    except json.JSONDecodeError as err:
        raise MeasureError(
            f"the page did not load in its frame or could not be read there ({text!r})"
        ) from err
    if not report["rendered"]:
        raise MeasureError(
            "the page rendered nothing in its frame; for an app with a build step, "
            "pass the built index.html"
        )
    elements = tuple(WideElement(item["element"], item["reach_px"]) for item in report["elements"])
    return Measurement(
        overflow_px=report["overflow_px"],
        has_viewport_meta=report["has_viewport_meta"],
        elements=elements,
    )


def run_chrome(chrome: Path, url: str) -> str:
    with tempfile.TemporaryDirectory(prefix="check-phone-") as profile:
        command = [
            str(chrome),
            "--headless=new",
            "--hide-scrollbars",
            f"--user-data-dir={profile}",
            f"--virtual-time-budget={VIRTUAL_TIME_BUDGET_MS}",
            "--dump-dom",
            url,
        ]
        try:
            finished = subprocess.run(  # noqa: S603 (fixed argument list, no shell)
                command,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=CHROME_TIMEOUT_SECONDS,
                check=False,
            )
        except subprocess.TimeoutExpired as err:
            raise MeasureError(f"Chrome did not finish within {CHROME_TIMEOUT_SECONDS} s") from err
    if finished.returncode != 0:
        raise MeasureError(
            f"Chrome exited with code {finished.returncode}: {finished.stderr[-500:]}"
        )
    return finished.stdout


def measure(page: Path, chrome: Path) -> Measurement:
    wrapper = WRAPPER.substitute(
        page_url="/" + quote(page.name),
        width=PHONE_WIDTH_PX,
        height=PHONE_HEIGHT_PX,
        limit=MAX_ELEMENTS_LISTED,
        settle_ms=SETTLE_MS,
    ).encode("utf-8")
    handler = partial(PageHandler, wrapper=wrapper, directory=str(page.resolve().parent))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    serving = threading.Thread(target=server.serve_forever, daemon=True)
    serving.start()
    try:
        port = server.server_address[1]
        return parse_report(run_chrome(chrome, f"http://127.0.0.1:{port}{WRAPPER_PATH}"))
    finally:
        server.shutdown()
        server.server_close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Measure a page's overflow at phone width.")
    parser.add_argument("page", type=Path, help="the page's HTML file")
    page: Path = parser.parse_args(argv).page
    if not page.is_file():
        print(f"unmeasured: no page at {page}")
        return 2
    chrome = find_chrome()
    if chrome is None:
        print("unmeasured: Chrome not found; set CHROME_PATH to its executable")
        return 2
    try:
        result = measure(page, chrome)
    except MeasureError as err:
        print(f"unmeasured: {err}")
        return 2
    breached = False
    if not result.has_viewport_meta:
        print('breach: no <meta name="viewport">, so a phone lays the page out at 980 px')
        breached = True
    if result.overflow_px > 0:
        print(f"breach: the page is {result.overflow_px} px wider than a {PHONE_WIDTH_PX} px phone")
        for wide in result.elements:
            print(f"  {wide.element} reaches {wide.reach_px} px past the edge")
        breached = True
    if breached:
        return 1
    print(f"pass: no overflow at {PHONE_WIDTH_PX} px")
    return 0


if __name__ == "__main__":
    sys.exit(main())
