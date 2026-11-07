"""Scan front-end source for generic AI tells and craft defects.

Usage:
    python check_slop.py PATH [PATH ...]

PATH is a file or a directory. Directories are walked, skipping dependency
and build output folders. Defects break accessibility or feel and make the
exit code 1. Tells are patterns typical of generated UI: each one should be
changed or kept with a stated reason, and they do not affect the exit code.
Exit code 2 means a path could not be found.

The scan reads text, not rendered pages, so it cannot judge contrast, layout
or motion as experienced. Check those in a browser.
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
    | {".mjs", ".vue", ".svelte", ".astro", ".mdx"}
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
    rule_id: str
    severity: Severity
    message: str
    fix: str


@dataclass(frozen=True, slots=True)
class SourceFile:
    path: Path
    lines: tuple[str, ...]


@dataclass(slots=True)
class ScanResult:
    findings: list[Finding] = field(default_factory=list)
    skipped: list[Path] = field(default_factory=list)
    files_scanned: int = 0
    truncated: bool = False


DEFAULT_FONTS = (
    r"Inter|Roboto|Open[ +_]Sans|Lato|Poppins|Montserrat|Space[ +_]Grotesk"
    r"|Instrument[ +_]Serif|Geist"
)
FONT_CONTEXT = r"font-family|fontFamily|fonts\.googleapis\.com|@fontsource|next/font|--font"
FILLER_PHRASES = (
    r"build faster|ship faster|ship smarter|supercharge|unlock the power|seamless(?:ly)?"
    r"|revolutioni[sz]e|next-generation|game[- ]chang|effortless(?:ly)?|elevate your"
    r"|all-in-one platform|cutting-edge|empower your"
)
EMOJI = "[\U0001f300-\U0001faff✨⚡✅⭐]"
LAYOUT_PROPERTIES = r"width|height|top|left|right|bottom|inset|margin[\w-]*|padding[\w-]*"

LINE_RULES: tuple[LineRule, ...] = (
    LineRule(
        Rule(
            "transition-all",
            Severity.DEFECT,
            "transitions every property, including layout ones and any added later",
            "list the properties, usually opacity and transform",
        ),
        re.compile(r"transition(?:-property)?\s*:\s*all\b|\btransition-all\b"),
    ),
    LineRule(
        Rule(
            "scale-zero",
            Severity.DEFECT,
            "animating from scale 0 looks like popping out of nowhere",
            "start from scale 0.9 to 0.97 with opacity 0",
        ),
        re.compile(r"scale\(\s*0(?:\.0+)?\s*\)|\bscale:\s*0\s*[,}]|\bscale-0\b"),
    ),
    LineRule(
        Rule(
            "zoom-disabled",
            Severity.DEFECT,
            "the viewport blocks pinch zoom, which fails people who need to enlarge text",
            "remove user-scalable and maximum-scale from the viewport meta tag",
        ),
        re.compile(r"user-scalable\s*=\s*(?:no|0)\b|maximum-scale\s*=\s*1(?:\.0+)?(?![\d.])"),
    ),
    LineRule(
        Rule(
            "layout-transition",
            Severity.DEFECT,
            "transitioning a layout property forces layout on every frame and shifts content",
            "animate transform and opacity instead, or use a grid-rows or View Transition",
        ),
        re.compile(rf"transition(?:-property)?\s*:[^;{{}}]*\b(?:{LAYOUT_PROPERTIES})\b"),
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
        re.compile(rf"^(?=.*(?:{FONT_CONTEXT}))(?=.*\b(?:{DEFAULT_FONTS})\b)"),
    ),
    LineRule(
        Rule(
            "glow-shadow",
            Severity.TELL,
            "a zero-offset coloured glow models no light source",
            "use tone steps or a layered neutral shadow from one light direction",
        ),
        re.compile(
            r"box-shadow\s*:\s*0(?:px)?\s+0(?:px)?\s+(?:[2-9]\d|\d{3,})px"
            r"|\bshadow-(?!(?:sm|md|lg|xl|2xl|inner|none)\b)[a-z]+-\d{2,3}(?:/\d+)?\b"
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
            r"|class(?:Name)?=[\"'][^\"']*\b(?:eyebrow|kicker|overline)\b"
        ),
    ),
    LineRule(
        Rule(
            "accent-word",
            Severity.TELL,
            "an italic accent word inside a heading is a fast-spreading generated tell",
            "let the whole heading carry the voice through size, weight and setting",
        ),
        re.compile(r"<h[1-6]\b[^>]*>[^<]*<(?:em|i)\b"),
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

OUTLINE_REMOVED_PATTERN = re.compile(r"outline\s*:\s*(?:none|0)\b|\boutline-none\b")
FOCUS_VISIBLE_PATTERN = re.compile(r":focus-visible|\bfocus-visible:")
MOTION_PATTERN = re.compile(
    r"@keyframes|\banimation(?:-name)?\s*:|\banimate-(?!none\b)[a-z]|\bgsap\b"
    r"|framer-motion|motion/react|startViewTransition|scroll-behavior\s*:\s*smooth"
)
REDUCED_MOTION_PATTERN = re.compile(
    r"prefers-reduced-motion|\bmotion-(?:safe|reduce):|useReducedMotion|MotionConfig"
)
BLUR_PATTERN = re.compile(r"backdrop-filter\s*:|\bbackdrop-blur\b")


def iter_candidate_files(roots: Sequence[Path]) -> Iterator[Path]:
    for root in roots:
        if root.is_file():
            if root.suffix.lower() in SCANNED_SUFFIXES:
                yield root
            continue
        for directory, subdirectories, filenames in os.walk(root):
            subdirectories[:] = sorted(d for d in subdirectories if d not in SKIPPED_DIRS)
            for filename in sorted(filenames):
                path = Path(directory, filename)
                if path.suffix.lower() in SCANNED_SUFFIXES:
                    yield path


def read_sources(roots: Sequence[Path], result: ScanResult) -> list[SourceFile]:
    sources: list[SourceFile] = []
    for path in iter_candidate_files(roots):
        if len(sources) + len(result.skipped) == MAX_FILES:
            result.truncated = True
            break
        if not path.is_file():
            continue  # a broken symlink: nothing to read
        if path.stat().st_size > MAX_FILE_BYTES:
            result.skipped.append(path)
            continue
        text = path.read_bytes().decode("utf-8", errors="replace")
        sources.append(SourceFile(path, tuple(text.splitlines())))
    result.files_scanned = len(sources)
    return sources


def finding_at(rule: Rule, path: Path, line: int) -> Finding:
    return Finding(path, line, rule.rule_id, rule.severity, rule.message, rule.fix)


def locations(sources: Sequence[SourceFile], pattern: re.Pattern[str]) -> list[tuple[Path, int]]:
    return [
        (source.path, number)
        for source in sources
        for number, text in enumerate(source.lines, start=1)
        if pattern.search(text)
    ]


def check_lines(sources: Sequence[SourceFile]) -> list[Finding]:
    return [
        finding_at(line_rule.rule, source.path, number)
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
            finding_at(FOCUS_REMOVED, path, line)
            for path, line in locations(sources, OUTLINE_REMOVED_PATTERN)
        ]
    motion = locations(sources, MOTION_PATTERN)
    if motion and not locations(sources, REDUCED_MOTION_PATTERN):
        findings.append(finding_at(NO_REDUCED_MOTION, *motion[0]))
    blur = locations(sources, BLUR_PATTERN)
    if len(blur) > MAX_BLUR_SURFACES:
        findings.append(finding_at(GLASS_EVERYWHERE, *blur[0]))
    return findings


def scan(roots: Sequence[Path]) -> ScanResult:
    result = ScanResult()
    sources = read_sources(roots, result)
    result.findings = check_lines(sources) + check_project(sources)
    return result


def counted(number: int, noun: str) -> str:
    return f"{number} {noun}" if number == 1 else f"{number} {noun}s"


def format_report(result: ScanResult) -> str:
    lines = []
    shown: Counter[str] = Counter()
    for finding in sorted(result.findings, key=lambda f: (f.severity, str(f.path), f.line)):
        shown[finding.rule_id] += 1
        if shown[finding.rule_id] <= MAX_SHOWN_PER_RULE:
            lines.append(
                f"{finding.path}:{finding.line}: {finding.severity} {finding.rule_id}: "
                f"{finding.message}. Fix: {finding.fix}."
            )
    lines += [
        f"... and {count - MAX_SHOWN_PER_RULE} more {rule_id}"
        for rule_id, count in sorted(shown.items())
        if count > MAX_SHOWN_PER_RULE
    ]
    severities = Counter(finding.severity for finding in result.findings)
    summary = (
        f"{counted(severities[Severity.DEFECT], 'defect')}, "
        f"{counted(severities[Severity.TELL], 'tell')} "
        f"in {counted(result.files_scanned, 'file')}."
    )
    if result.skipped:
        names = ", ".join(str(path) for path in result.skipped)
        summary += f" Skipped (over {MAX_FILE_BYTES} bytes): {names}."
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
    has_defect = any(finding.severity is Severity.DEFECT for finding in result.findings)
    return 1 if has_defect else 0


if __name__ == "__main__":
    sys.exit(main())
