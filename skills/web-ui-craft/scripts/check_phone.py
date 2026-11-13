"""Measure how far a page runs past the edge of a phone screen.

Usage:
    python check_phone.py PAGE

PAGE is the page's HTML file. Headless Chrome loads it in a frame 375 px wide,
waits 1.5 s of page time for entrance motion to settle, and measures the whole
page, not only its first screen. It prints the overflow in px and up to 10
elements whose box reaches past the right edge, each with how far it reaches.
Elements inside a box that scrolls or clips are not listed, since they cannot
widen the page; the overflow figure is measured either way. A page that hides
its overflow on both html and body measures 0 px, and the content it cuts off
is not reported.

Exit code 0 means no overflow, 1 means the page is wider than the phone, and 2
means nothing was measured: no Chrome, a missing page, a timeout or a page the
frame could not read.

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
from dataclasses import dataclass
from pathlib import Path
from string import Template

PHONE_WIDTH_PX = 375
PHONE_HEIGHT_PX = 812
SETTLE_MS = 1500
VIRTUAL_TIME_BUDGET_MS = 5000
CHROME_TIMEOUT_SECONDS = 60
MAX_ELEMENTS_LISTED = 10

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

# The report is written into the wrapper's own DOM, which Chrome prints with --dump-dom.
# Chrome lets one file:// page read another's frame only with --allow-file-access-from-files.
WRAPPER = Template("""<!doctype html>
<meta charset="utf-8">
<pre id="report">not measured</pre>
<iframe id="page" src="$page_url" width="$width" height="$height" style="border:0"></iframe>
<script>
page.onload = () => setTimeout(() => {
  const doc = page.contentDocument, root = doc.documentElement, width = root.clientWidth;
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
    const box = el.getBoundingClientRect();
    const reach = box.right - width;
    if (box.width > 0 && reach > 0.5 && !contained(el))
      wide.push({element: name(el), reach_px: Math.round(reach)});
    if (wide.length === $limit) break;
  }
  report.textContent = JSON.stringify({overflow_px: root.scrollWidth - width, elements: wide});
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
    elements: tuple[WideElement, ...]


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
    elements = tuple(WideElement(item["element"], item["reach_px"]) for item in report["elements"])
    return Measurement(overflow_px=report["overflow_px"], elements=elements)


def measure(page: Path, chrome: Path) -> Measurement:
    with tempfile.TemporaryDirectory(prefix="check-phone-") as work:
        wrapper = Path(work) / "phone.html"
        wrapper.write_text(
            WRAPPER.substitute(
                page_url=page.resolve().as_uri(),
                width=PHONE_WIDTH_PX,
                height=PHONE_HEIGHT_PX,
                limit=MAX_ELEMENTS_LISTED,
                settle_ms=SETTLE_MS,
            ),
            encoding="utf-8",
        )
        command = [
            str(chrome),
            "--headless=new",
            "--hide-scrollbars",
            "--allow-file-access-from-files",
            f"--user-data-dir={Path(work) / 'profile'}",
            f"--virtual-time-budget={VIRTUAL_TIME_BUDGET_MS}",
            "--dump-dom",
            wrapper.as_uri(),
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
    return parse_report(finished.stdout)


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
    if result.overflow_px <= 0:
        print(f"pass: no overflow at {PHONE_WIDTH_PX} px")
        return 0
    print(f"breach: the page is {result.overflow_px} px wider than a {PHONE_WIDTH_PX} px phone")
    for wide in result.elements:
        print(f"  {wide.element} reaches {wide.reach_px} px past the edge")
    return 1


if __name__ == "__main__":
    sys.exit(main())
