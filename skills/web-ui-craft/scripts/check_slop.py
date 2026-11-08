"""Scan front-end source for generic AI tells and craft defects.

Usage:
    python check_slop.py PATH [PATH ...]

PATH is a file or a directory. Directories are walked for front-end file
types, skipping dependency and build output folders; a file named directly is
always scanned. Defects break accessibility or feel and make the exit code 1.
Tells are patterns typical of generated UI: each one should be changed or kept
with a stated reason, and they do not affect the exit code. Exit code 2 means
a path could not be found.

Focus and reduced-motion rules look for a satisfying style anywhere in the
scan, so pass the whole front-end source rather than only the files changed.

Limits: rules read one line at a time, so a declaration or element split over
several lines can be missed. The scan reads text, not rendered pages, so it
cannot judge contrast, layout or motion as experienced.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from collections import Counter
from collections.abc import Iterator, Sequence
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path

MAX_FILES = 2000
MAX_FILE_BYTES = 1_000_000
MAX_SHOWN_PER_RULE = 25
MAX_BLUR_SURFACES = 3

SCANNED_SUFFIXES = frozenset(
    {".html", ".htm", ".css", ".scss", ".sass", ".less", ".js", ".jsx", ".ts", ".tsx"}
    | {".mjs", ".cjs", ".mts", ".cts", ".vue", ".svelte", ".astro", ".mdx"}
)
SKIPPED_DIRS = frozenset(
    {"node_modules", ".git", "dist", "build", "out", ".next", ".nuxt", ".svelte-kit"}
    | {".output", ".vercel", ".turbo", "coverage", "vendor", ".venv", "__pycache__"}
)


class Severity(StrEnum):
    DEFECT = "defect"
    TELL = "tell"


@dataclass(frozen=True, slots=True)
class Rule:
    rule_id: str
    severity: Severity
    message: str
    fix: str


@dataclass(frozen=True, slots=True)
class LineRule:
    rule: Rule
    pattern: re.Pattern[str]


@dataclass(frozen=True, slots=True)
class Finding:
    path: Path
    line: int
    rule: Rule


@dataclass(frozen=True, slots=True)
class SourceFile:
    path: Path
    lines: tuple[str, ...]


@dataclass(slots=True)
class Collection:
    sources: list[SourceFile] = field(default_factory=list)
    skipped: list[Path] = field(default_factory=list)
    unreadable: list[Path] = field(default_factory=list)
    truncated: bool = False


@dataclass(frozen=True, slots=True)
class ScanResult:
    findings: list[Finding]
    files_scanned: int
    skipped: list[Path]
    unreadable: list[Path]
    truncated: bool


DEFAULT_FONTS = (
    r"inter|roboto|open[ +_-]sans|lato|poppins|montserrat|space[ +_-]grotesk"
    r"|instrument[ +_-]serif|playfair[ +_-]display|geist(?![ +_-]mono)"
)
FONT_CONTEXT = r"font-family|fontFamily|fonts\.googleapis\.com|@fontsource|next/font|--font"
FILLER_PHRASES = (
    r"build faster|ship faster|ship smarter|supercharge|unlock the power|seamless(?:ly)?"
    r"|revolutioni[sz]e|next-generation|game[- ]chang|effortless(?:ly)?|elevate your"
    r"|all-in-one platform|cutting-edge|empower your"
)
EMOJI = "[\U0001f300-\U0001faff\u2728\u26a1\u2705\u2b50]"
LAYOUT_PROPERTIES = (
    r"(?:max-|min-)?(?:width|height)|top|left|right|bottom|inset(?:-[a-z-]+)?"
    r"|margin(?:-[a-z-]+)?|padding(?:-[a-z-]+)?|grid-template-(?:rows|columns)"
)
RIGHT_ARROW = r"(?:→|&rarr;|&#8594;|&#x2192;|\\2192)"
SATURATED_HUES = (
    r"red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple"
    r"|fuchsia|pink|rose"
)

LINE_RULES: tuple[LineRule, ...] = (
    LineRule(
        Rule(
            "transition-all",
            Severity.DEFECT,
            "transitions every property, including layout ones and any added later",
            "list the properties, usually opacity and transform",
        ),
        re.compile(r"transition(?:-property)?\s*:\s*['\"`]?all\b|\btransition-all\b"),
    ),
    LineRule(
        Rule(
            "scale-zero",
            Severity.DEFECT,
            "animating from scale 0 looks like popping out of nowhere",
            "start from scale 0.9 to 0.97 with opacity 0",
        ),
        re.compile(r"scale\(\s*0(?:\.0+)?\s*\)|\bscale\s*:\s*0(?:\.0+)?\s*(?:[,;}]|$)|\bscale-0\b"),
    ),
    LineRule(
        Rule(
            "zoom-disabled",
            Severity.DEFECT,
            "the viewport blocks pinch zoom, which fails people who need to enlarge text",
            "remove the user-scalable and maximum-scale settings from the viewport",
        ),
        re.compile(
            r"user-scalable\s*=\s*(?:no|0)\b|maximum-scale\s*=\s*1(?:\.0+)?(?![\d.])"
            r"|maximumScale\s*:\s*1(?![\d.])|userScalable\s*:\s*(?:false|['\"]no['\"])"
        ),
    ),
    LineRule(
        Rule(
            "layout-transition",
            Severity.DEFECT,
            "transitioning a layout property forces layout on every frame and shifts content",
            "animate transform and opacity instead, or use a View Transition",
        ),
        re.compile(
            r"transition(?:-property)?\s*:\s*['\"`]?[^;{}'\"`]*?"
            rf"(?<![\w-])(?:{LAYOUT_PROPERTIES})(?![\w-])"
        ),
    ),
    LineRule(
        Rule(
            "indigo-default",
            Severity.TELL,
            "indigo, violet or purple is the default accent of generated UI",
            "take the accent from the subject and reference it through a token",
        ),
        re.compile(
            r"\b(?:bg|text|from|via|to|border|ring|fill|stroke|shadow|outline|decoration"
            r"|accent|caret|divide)-(?:indigo|violet|purple)-\d{2,3}\b"
            r"|#(?:6366f1|4f46e5|818cf8|8b5cf6|7c3aed|a855f7|9333ea)\b",
            re.IGNORECASE,
        ),
    ),
    LineRule(
        Rule(
            "gradient-text",
            Severity.TELL,
            "gradient-filled headline text is one of the most common generated-hero patterns",
            "let size, weight and setting carry the headline",
        ),
        re.compile(r"\bbg-clip-text\b|background-clip\s*:\s*text\b"),
    ),
    LineRule(
        Rule(
            "default-font",
            Severity.TELL,
            "this typeface is a default or second-wave default of generated UI",
            "choose a family for the subject's voice, or state why this one fits",
        ),
        re.compile(rf"^(?=.*(?:{FONT_CONTEXT}))(?=.*\b(?:{DEFAULT_FONTS})\b)", re.IGNORECASE),
    ),
    LineRule(
        Rule(
            "glow-shadow",
            Severity.TELL,
            "a coloured glow shadow models no light source",
            "use tone steps or a layered neutral shadow from one light direction",
        ),
        re.compile(
            r"box-shadow\s*:\s*0(?:px)?\s+0(?:px)?\s+(?:[2-9]\d|\d{3,})px"
            rf"|\bshadow-(?:{SATURATED_HUES})-\d{{2,3}}(?:/\d+)?\b"
        ),
    ),
    LineRule(
        Rule(
            "emoji-icon",
            Severity.TELL,
            "emoji used as interface icons",
            "use one consistent icon family, or no icon",
        ),
        re.compile(EMOJI),
    ),
    LineRule(
        Rule(
            "filler-copy",
            Severity.TELL,
            "generic marketing phrase that could describe any product",
            "say what is specific, for whom",
        ),
        re.compile(rf"\b(?:{FILLER_PHRASES})", re.IGNORECASE),
    ),
    LineRule(
        Rule(
            "trusted-by",
            Severity.TELL,
            "a 'trusted by' strip is template filler unless it supports a specific claim",
            "use named proof next to the claim it supports",
        ),
        re.compile(r"\btrusted by\b|\bloved by \d", re.IGNORECASE),
    ),
    LineRule(
        Rule(
            "uppercase-label",
            Severity.TELL,
            "all-caps tracked eyebrow labels above sections are a template habit",
            "remove the label, or make the heading say it",
        ),
        re.compile(
            r"\buppercase\b[^\"'\n]*\btracking-(?:wide|wider|widest)\b"
            r"|\btracking-(?:wide|wider|widest)\b[^\"'\n]*\buppercase\b"
            r"|class(?:Name)?=[\"'][^\"']*\b(?:eyebrow|kicker)\b"
        ),
    ),
    LineRule(
        Rule(
            "accent-word",
            Severity.TELL,
            "an italic accent word inside a heading is a fast-spreading generated tell",
            "let the whole heading carry the voice through size, weight and setting",
        ),
        re.compile(r"<h[1-6]\b[^>]*>[^<]*<(?:em\b|i>|span\b[^>]*\bitalic\b)"),
    ),
    LineRule(
        Rule(
            "arrow-suffix",
            Severity.TELL,
            "an arrow appended to link or button text is generated template chrome",
            "let the label say where it goes; keep an arrow only where it shows direction",
        ),
        re.compile(
            rf"{RIGHT_ARROW}\s*(?:</span>\s*)?</(?:a|button|link)\s*>"
            rf"|content\s*:\s*['\"]\s*{RIGHT_ARROW}\s*['\"]",
            re.IGNORECASE,
        ),
    ),
    LineRule(
        Rule(
            "assistant-palette",
            Severity.TELL,
            "cream #F4F1EA and terracotta #D97757 (Claude's own accent) are a generated default",
            "take the neutral tint and the accent from the subject",
        ),
        re.compile(r"#(?:f4f1ea|d97757)(?:[0-9a-f]{2})?(?![0-9a-f])", re.IGNORECASE),
    ),
)

FOCUS_REMOVED = Rule(
    "focus-removed",
    Severity.DEFECT,
    "the focus outline is removed and no :focus-visible style exists anywhere in the scan",
    "add a visible :focus-visible ring of at least 2px",
)
NO_REDUCED_MOTION = Rule(
    "no-reduced-motion",
    Severity.DEFECT,
    "animation is used but prefers-reduced-motion is never handled",
    "put movement behind prefers-reduced-motion: no-preference and fall back to opacity",
)
GLASS_EVERYWHERE = Rule(
    "glass-everywhere",
    Severity.TELL,
    f"backdrop blur is used on more than {MAX_BLUR_SURFACES} surfaces",
    "keep glass for the one surface content scrolls under, if any",
)

# A line that removes the outline but adds a ring or shadow replaces it rather than removing it.
OUTLINE_REMOVED_PATTERN = re.compile(
    r"^(?!.*(?:box-shadow|\bring-))(?=.*(?:outline\s*:\s*(?:none|0)(?![\w.])|\boutline-none\b))"
)
FOCUS_VISIBLE_PATTERN = re.compile(r":focus-visible|\bfocus-visible:")
MOTION_PATTERN = re.compile(
    r"@keyframes|\banimation(?:-name)?\s*:(?!\s*none\b)|\banimate-(?!none\b)[a-z]|\bgsap\b"
    r"|framer-motion|motion/react|startViewTransition|scroll-behavior\s*:\s*smooth"
    r"|transition(?:-property)?\s*:[^;{}]*\btransform\b|\btransition-transform\b"
)
REDUCED_MOTION_PATTERN = re.compile(
    r"prefers-reduced-motion|\bmotion-(?:safe|reduce):|useReducedMotion|MotionConfig"
)
# One surface often needs a prefixed copy and an @supports fallback; count neither.
BLUR_PATTERN = re.compile(
    r"^(?!.*@supports)(?=.*(?:(?<!-webkit-)backdrop-filter\s*:(?!\s*none\b)|\bbackdrop-blur\b))"
)


def iter_candidate_files(roots: Sequence[Path], unreadable: list[Path]) -> Iterator[Path]:
    for root in roots:
        if root.is_file():
            yield root
            continue
        walk = os.walk(root, onerror=lambda error: unreadable.append(Path(str(error.filename))))
        for directory, subdirectories, filenames in walk:
            subdirectories[:] = sorted(d for d in subdirectories if d not in SKIPPED_DIRS)
            for filename in sorted(filenames):
                path = Path(directory, filename)
                if path.suffix.lower() in SCANNED_SUFFIXES:
                    yield path


def collect_sources(roots: Sequence[Path]) -> Collection:
    collection = Collection()
    seen: set[Path] = set()
    for path in iter_candidate_files(roots, collection.unreadable):
        resolved = path.resolve()
        if resolved in seen:
            continue
        if len(seen) == MAX_FILES:
            collection.truncated = True
            break
        seen.add(resolved)
        try:
            if not path.is_file():
                continue  # a broken symlink: nothing to read
            if path.stat().st_size > MAX_FILE_BYTES:
                collection.skipped.append(path)
                continue
            text = path.read_bytes().decode("utf-8", errors="replace")
        except OSError:
            collection.unreadable.append(path)
            continue
        collection.sources.append(SourceFile(path, tuple(text.splitlines())))
    return collection


def locations(sources: Sequence[SourceFile], pattern: re.Pattern[str]) -> list[tuple[Path, int]]:
    return [
        (source.path, number)
        for source in sources
        for number, text in enumerate(source.lines, start=1)
        if pattern.search(text)
    ]


def check_lines(sources: Sequence[SourceFile]) -> list[Finding]:
    return [
        Finding(source.path, number, line_rule.rule)
        for source in sources
        for number, text in enumerate(source.lines, start=1)
        for line_rule in LINE_RULES
        if line_rule.pattern.search(text)
    ]


def check_project(sources: Sequence[SourceFile]) -> list[Finding]:
    """Rules judged across every scanned file, because styles often live elsewhere."""
    findings = []
    if not locations(sources, FOCUS_VISIBLE_PATTERN):
        findings += [
            Finding(path, line, FOCUS_REMOVED)
            for path, line in locations(sources, OUTLINE_REMOVED_PATTERN)
        ]
    motion = locations(sources, MOTION_PATTERN)
    if motion and not locations(sources, REDUCED_MOTION_PATTERN):
        findings.append(Finding(*motion[0], NO_REDUCED_MOTION))
    blur = locations(sources, BLUR_PATTERN)
    if len(blur) > MAX_BLUR_SURFACES:
        findings.append(Finding(*blur[0], GLASS_EVERYWHERE))
    return findings


def scan(roots: Sequence[Path]) -> ScanResult:
    collection = collect_sources(roots)
    return ScanResult(
        findings=check_lines(collection.sources) + check_project(collection.sources),
        files_scanned=len(collection.sources),
        skipped=collection.skipped,
        unreadable=collection.unreadable,
        truncated=collection.truncated,
    )


def counted(number: int, noun: str) -> str:
    return f"{number} {noun}" if number == 1 else f"{number} {noun}s"


def format_report(result: ScanResult) -> str:
    lines = []
    shown: Counter[str] = Counter()
    ordered = sorted(result.findings, key=lambda f: (f.rule.severity, str(f.path), f.line))
    for finding in ordered:
        rule = finding.rule
        shown[rule.rule_id] += 1
        if shown[rule.rule_id] <= MAX_SHOWN_PER_RULE:
            lines.append(
                f"{finding.path}:{finding.line}: {rule.severity} {rule.rule_id}: "
                f"{rule.message}. Fix: {rule.fix}."
            )
    lines += [
        f"... and {count - MAX_SHOWN_PER_RULE} more {rule_id}"
        for rule_id, count in sorted(shown.items())
        if count > MAX_SHOWN_PER_RULE
    ]
    severities = Counter(finding.rule.severity for finding in result.findings)
    summary = (
        f"{counted(severities[Severity.DEFECT], 'defect')}, "
        f"{counted(severities[Severity.TELL], 'tell')} "
        f"in {counted(result.files_scanned, 'file')}."
    )
    if result.skipped:
        names = ", ".join(str(path) for path in result.skipped)
        summary += f" Skipped (over {MAX_FILE_BYTES} bytes): {names}."
    if result.unreadable:
        summary += f" Could not read: {', '.join(str(path) for path in result.unreadable)}."
    if result.truncated:
        summary += f" Stopped after {MAX_FILES} files; scan a narrower path."
    lines.append(summary)
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else None)
    parser.add_argument("paths", nargs="+", type=Path, help="files or directories to scan")
    arguments = parser.parse_args(argv)
    missing = [path for path in arguments.paths if not path.exists()]
    if missing:
        print(f"path not found: {', '.join(map(str, missing))}", file=sys.stderr)
        return 2
    result = scan(arguments.paths)
    print(format_report(result))
    has_defect = any(finding.rule.severity is Severity.DEFECT for finding in result.findings)
    return 1 if has_defect else 0


if __name__ == "__main__":
    sys.exit(main())
