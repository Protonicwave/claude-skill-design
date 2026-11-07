from pathlib import Path

import pytest

import check_slop
from check_slop import main, scan

ROCKET = chr(0x1F680)
SPARKLES = chr(0x2728)


def write(directory: Path, name: str, text: str) -> Path:
    path = directory / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def rule_ids(directory: Path) -> set[str]:
    return {finding.rule.rule_id for finding in scan([directory]).findings}


LINE_RULE_CASES = [
    ("transition-all", "a.css", ".a { transition: all 0.2s; }", ".a { transition: opacity 0.2s; }"),
    (
        "transition-all",
        "a.html",
        '<div class="transition-all">',
        '<div class="transition-opacity">',
    ),
    ("scale-zero", "a.css", ".a { transform: scale(0); }", ".a { transform: scale(0.96); }"),
    ("scale-zero", "a.tsx", "initial={{ scale: 0 }}", "initial={{ scale: 0.95 }}"),
    ("scale-zero", "a.html", '<div class="scale-0">', '<div class="scale-95">'),
    (
        "zoom-disabled",
        "a.html",
        '<meta name="viewport" content="width=device-width, user-scalable=no">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
    ),
    (
        "zoom-disabled",
        "a.html",
        '<meta name="viewport" content="width=device-width, maximum-scale=1">',
        '<meta name="viewport" content="width=device-width, maximum-scale=5">',
    ),
    (
        "layout-transition",
        "a.css",
        ".a { transition: height 0.3s ease; }",
        ".a { transition: transform 0.3s ease; }",
    ),
    (
        "layout-transition",
        "a.css",
        ".a { transition: opacity 0.2s, max-height 0.3s; }",
        ".a { transition: opacity 0.2s, transform 0.3s; }",
    ),
    ("indigo-default", "a.html", '<button class="bg-indigo-500">', '<button class="bg-accent">'),
    ("indigo-default", "a.html", '<p class="text-violet-600">', '<p class="text-stone-600">'),
    ("indigo-default", "a.css", ".a { color: #6366F1; }", ".a { color: #2f6f4e; }"),
    (
        "gradient-text",
        "a.html",
        '<h1 class="bg-gradient-to-r bg-clip-text text-transparent">',
        '<h1 class="text-balance">',
    ),
    ("gradient-text", "a.css", "-webkit-background-clip: text;", "background-clip: padding-box;"),
    (
        "default-font",
        "a.css",
        "body { font-family: 'Inter', sans-serif; }",
        "body { font-family: 'Newsreader', serif; }",
    ),
    (
        "default-font",
        "a.tsx",
        "import { Inter } from 'next/font/google'",
        "body { font-family: 'Interstate', sans-serif; }",
    ),
    (
        "default-font",
        "a.html",
        '<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400">',
        '<link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@400">',
    ),
    (
        "glow-shadow",
        "a.css",
        ".a { box-shadow: 0 0 40px rgba(99, 102, 241, 0.5); }",
        ".a { box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1); }",
    ),
    (
        "glow-shadow",
        "a.html",
        '<div class="shadow-lg shadow-cyan-500/50">',
        '<div class="shadow-lg">',
    ),
    ("emoji-icon", "a.html", f"<span>{ROCKET} Fast</span>", "<span>Fast</span>"),
    ("emoji-icon", "a.tsx", f"<h2>{SPARKLES} Features</h2>", "<h2>Features</h2>"),
    (
        "filler-copy",
        "a.html",
        "<h1>Build faster. Ship smarter.</h1>",
        "<h1>Invoices your accountant will not chase</h1>",
    ),
    ("filler-copy", "a.html", "<p>Seamless integration</p>", "<p>Integrates with Xero</p>"),
    ("trusted-by", "a.html", "<p>Trusted by 10,000+ teams</p>", "<p>Used at Royal Mail</p>"),
    (
        "accent-word",
        "a.html",
        "<h1>Proper sourdough, <em>on your doorstep</em> every Friday.</h1>",
        "<h1>Sourdough from our Bedminster oven, every Friday.</h1>",
    ),
    (
        "accent-word",
        "a.tsx",
        '<h2 className="title">Every finding has a <i>price tag</i></h2>',
        "<p>Read the <em>whole</em> report.</p>",
    ),
    (
        "uppercase-label",
        "a.html",
        '<span class="eyebrow">How it works</span>',
        '<span class="lede">',
    ),
    ("uppercase-label", "a.html", '<p class="hero-kicker">New</p>', '<p class="hero-lede">New</p>'),
    (
        "uppercase-label",
        "a.html",
        '<p class="eyebrow">New</p>',
        '<a class="overline">Read more</a>',
    ),
    ("default-font", "a.ts", "import '@fontsource/inter';", "import '@fontsource/fraunces';"),
    (
        "default-font",
        "a.css",
        "body { font-family: inter, sans-serif; }",
        "body { font-family: newsreader, serif; }",
    ),
    ("transition-all", "a.tsx", "style={{ transition: 'all 0.3s' }}", "style={{ opacity: 0 }}"),
    ("scale-zero", "a.css", ".a { scale: 0; }", ".a { scale: 0.95; }"),
    ("scale-zero", "a.tsx", "    scale: 0", "    scale: 0.9"),
    (
        "zoom-disabled",
        "a.tsx",
        "export const viewport = { maximumScale: 1, userScalable: false }",
        "export const viewport = { width: 'device-width', initialScale: 1 }",
    ),
    (
        "layout-transition",
        "a.css",
        ".a { transition: grid-template-rows 0.3s; }",
        ".a { transition: border-left-color 0.2s; }",
    ),
    (
        "layout-transition",
        "a.tsx",
        "style={{ transition: 'height .2s' }}",
        "style={{ transition: 'opacity .2s', width: '100%' }}",
    ),
    (
        "glow-shadow",
        "a.html",
        '<div class="shadow-xl shadow-violet-500/40">',
        '<div class="shadow-lg shadow-stone-900/10">',
    ),
    (
        "accent-word",
        "a.tsx",
        '<h1>Sourdough <span className="font-serif italic">every</span> Friday</h1>',
        '<h2><i class="fa fa-star"></i> Features</h2>',
    ),
    (
        "uppercase-label",
        "a.html",
        '<p class="uppercase tracking-widest text-xs">Features</p>',
        '<p class="text-sm">Features</p>',
    ),
]


POSITIVE_CASES = [(rule_id, name, positive) for rule_id, name, positive, _ in LINE_RULE_CASES]
NEAR_MISS_CASES = [(rule_id, name, near_miss) for rule_id, name, _, near_miss in LINE_RULE_CASES]


@pytest.mark.parametrize(("rule_id", "name", "text"), POSITIVE_CASES)
def test_line_rule_fires_on_the_pattern(tmp_path: Path, rule_id: str, name: str, text: str) -> None:
    write(tmp_path, name, text)
    assert rule_id in rule_ids(tmp_path)


@pytest.mark.parametrize(("rule_id", "name", "text"), NEAR_MISS_CASES)
def test_line_rule_ignores_the_near_miss(
    tmp_path: Path, rule_id: str, name: str, text: str
) -> None:
    write(tmp_path, name, text)
    assert rule_id not in rule_ids(tmp_path)


def test_findings_carry_line_numbers(tmp_path: Path) -> None:
    write(tmp_path, "a.css", ".a {}\n.b { transition: all 1s; }\n")
    [finding] = [f for f in scan([tmp_path]).findings if f.rule.rule_id == "transition-all"]
    assert finding.line == 2


def test_removed_outline_without_focus_visible_is_a_defect(tmp_path: Path) -> None:
    write(tmp_path, "a.css", "button { outline: none; }")
    assert "focus-removed" in rule_ids(tmp_path)


def test_removed_outline_is_fine_when_another_file_styles_focus_visible(tmp_path: Path) -> None:
    write(tmp_path, "a.css", "button { outline: none; }")
    write(tmp_path, "b.css", ":focus-visible { outline: 2px solid var(--accent); }")
    assert "focus-removed" not in rule_ids(tmp_path)


def test_tailwind_focus_visible_ring_satisfies_removed_outline(tmp_path: Path) -> None:
    write(tmp_path, "a.html", '<button class="focus:outline-none focus-visible:ring-2">')
    assert "focus-removed" not in rule_ids(tmp_path)


def test_motion_without_reduced_motion_is_a_defect(tmp_path: Path) -> None:
    write(tmp_path, "a.css", "@keyframes rise { from { transform: translateY(8px); } }")
    assert "no-reduced-motion" in rule_ids(tmp_path)


def test_reduced_motion_in_another_file_satisfies_motion(tmp_path: Path) -> None:
    write(tmp_path, "a.css", "@keyframes rise { from { transform: translateY(8px); } }")
    write(tmp_path, "b.css", "@media (prefers-reduced-motion: reduce) { * { animation: none; } }")
    assert "no-reduced-motion" not in rule_ids(tmp_path)


def test_tailwind_motion_safe_variant_satisfies_motion(tmp_path: Path) -> None:
    write(tmp_path, "a.html", '<div class="motion-safe:animate-bounce">')
    assert "no-reduced-motion" not in rule_ids(tmp_path)


def test_colour_only_transition_needs_no_reduced_motion(tmp_path: Path) -> None:
    write(tmp_path, "a.css", ".a { transition: color 150ms ease-out; }")
    assert "no-reduced-motion" not in rule_ids(tmp_path)


def test_missing_reduced_motion_is_reported_once(tmp_path: Path) -> None:
    write(tmp_path, "a.css", "@keyframes a {}\n@keyframes b {}\n")
    findings = [f for f in scan([tmp_path]).findings if f.rule.rule_id == "no-reduced-motion"]
    assert len(findings) == 1


def test_blur_on_many_surfaces_is_a_tell(tmp_path: Path) -> None:
    write(tmp_path, "a.html", '<div class="backdrop-blur-md">\n' * 4)
    assert "glass-everywhere" in rule_ids(tmp_path)


def test_blur_on_few_surfaces_is_not_a_tell(tmp_path: Path) -> None:
    write(tmp_path, "a.html", '<div class="backdrop-blur-md">\n' * 3)
    assert "glass-everywhere" not in rule_ids(tmp_path)


def test_dependency_and_build_folders_are_skipped(tmp_path: Path) -> None:
    write(tmp_path, "node_modules/lib/a.css", ".a { transition: all 1s; }")
    write(tmp_path, "dist/a.css", ".a { transition: all 1s; }")
    write(tmp_path, ".next/a.css", ".a { transition: all 1s; }")
    assert scan([tmp_path]).files_scanned == 0


def test_unsupported_file_types_are_ignored(tmp_path: Path) -> None:
    write(tmp_path, "a.py", "transition: all 1s")
    assert scan([tmp_path]).files_scanned == 0


def test_a_single_file_path_is_scanned(tmp_path: Path) -> None:
    path = write(tmp_path, "a.css", ".a { transition: all 1s; }")
    assert scan([path]).files_scanned == 1


def test_oversized_files_are_reported_as_skipped(tmp_path: Path) -> None:
    path = tmp_path / "huge.css"
    path.write_bytes(b"a" * (check_slop.MAX_FILE_BYTES + 1))
    result = scan([tmp_path])
    assert result.skipped == [path]
    assert result.files_scanned == 0


def test_scan_stops_at_the_file_limit(tmp_path: Path) -> None:
    for index in range(check_slop.MAX_FILES + 1):
        (tmp_path / f"f{index}.css").write_text("", encoding="utf-8")
    result = scan([tmp_path])
    assert result.files_scanned == check_slop.MAX_FILES
    assert result.truncated


def test_invalid_utf8_is_scanned_without_crashing(tmp_path: Path) -> None:
    (tmp_path / "a.css").write_bytes(b"\xff\xfe .a { transition: all 1s; }")
    assert "transition-all" in rule_ids(tmp_path)


def test_exit_code_is_zero_for_a_clean_project(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    write(tmp_path, "a.css", ".a { transition: opacity 150ms ease-out; }")
    assert main([str(tmp_path)]) == 0
    assert "0 defects, 0 tells" in capsys.readouterr().out


def test_exit_code_is_zero_when_only_tells_are_found(tmp_path: Path) -> None:
    write(tmp_path, "a.html", '<button class="bg-indigo-500">Go</button>')
    assert main([str(tmp_path)]) == 0


def test_exit_code_is_one_when_a_defect_is_found(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    write(tmp_path, "a.css", ".a { transition: all 1s; }")
    assert main([str(tmp_path)]) == 1
    output = capsys.readouterr().out
    assert "a.css:1: defect transition-all:" in output
    assert "Fix:" in output


def test_exit_code_is_two_for_a_missing_path(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    missing = tmp_path / "nowhere"
    assert main([str(missing)]) == 2
    assert "nowhere" in capsys.readouterr().err


def test_repeated_findings_are_summarised_beyond_the_display_limit(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    repeats = check_slop.MAX_SHOWN_PER_RULE + 5
    write(tmp_path, "a.css", ".a { transition: all 1s; }\n" * repeats)
    main([str(tmp_path)])
    output = capsys.readouterr().out
    assert output.count("defect transition-all:") == check_slop.MAX_SHOWN_PER_RULE
    assert "5 more transition-all" in output


def test_oversized_files_count_towards_the_file_limit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(check_slop, "MAX_FILES", 2)
    monkeypatch.setattr(check_slop, "MAX_FILE_BYTES", 10)
    for index in range(3):
        write(tmp_path, f"f{index}.css", "a" * 20)
    result = scan([tmp_path])
    assert len(result.skipped) == 2
    assert result.truncated


def test_broken_symlinks_are_ignored(tmp_path: Path) -> None:
    link = tmp_path / "gone.css"
    try:
        link.symlink_to(tmp_path / "missing.css")
    except OSError:
        pytest.skip("this platform does not allow creating symlinks here")
    assert scan([tmp_path]).files_scanned == 0


def test_partial_outline_width_is_not_removal(tmp_path: Path) -> None:
    write(tmp_path, "a.css", ".a { outline: 0.5px solid red; }")
    assert "focus-removed" not in rule_ids(tmp_path)


def test_tailwind_focus_ring_replaces_removed_outline(tmp_path: Path) -> None:
    write(tmp_path, "a.html", '<button class="focus:outline-none focus:ring-2">')
    assert "focus-removed" not in rule_ids(tmp_path)


def test_box_shadow_ring_on_the_same_rule_replaces_removed_outline(tmp_path: Path) -> None:
    write(tmp_path, "a.css", "button:focus { outline: none; box-shadow: 0 0 0 3px var(--ring); }")
    assert "focus-removed" not in rule_ids(tmp_path)


def test_animation_none_is_not_motion(tmp_path: Path) -> None:
    write(tmp_path, "a.css", ".a { animation: none; }")
    assert "no-reduced-motion" not in rule_ids(tmp_path)


def test_transform_transition_is_motion(tmp_path: Path) -> None:
    write(tmp_path, "a.css", ".card { transition: transform 200ms ease-out; }")
    assert "no-reduced-motion" in rule_ids(tmp_path)


def test_one_glass_header_with_prefix_and_fallback_counts_once(tmp_path: Path) -> None:
    write(
        tmp_path,
        "a.css",
        ".h {\n  backdrop-filter: blur(12px);\n  -webkit-backdrop-filter: blur(12px);\n}\n"
        "@supports not (backdrop-filter: blur(1px)) { .h { background: white; } }\n"
        ".menu { backdrop-filter: blur(8px); }\n",
    )
    assert "glass-everywhere" not in rule_ids(tmp_path)


def test_overlapping_paths_scan_each_file_once(tmp_path: Path) -> None:
    path = write(tmp_path, "a.css", ".a { transition: all 1s; }")
    result = scan([tmp_path, path])
    assert result.files_scanned == 1
    assert len(result.findings) == 1


def test_a_named_file_is_scanned_whatever_its_suffix(tmp_path: Path) -> None:
    path = write(tmp_path, "page.php", '<div class="transition-all">')
    assert scan([path]).files_scanned == 1


def test_commonjs_and_typescript_module_suffixes_are_scanned(tmp_path: Path) -> None:
    for name in ("a.cjs", "b.mts", "c.cts"):
        write(tmp_path, name, "")
    assert scan([tmp_path]).files_scanned == 3


def test_unreadable_files_are_reported_not_fatal(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    locked = write(tmp_path, "locked.css", ".a { transition: all 1s; }")
    real_read_bytes = Path.read_bytes

    def read_bytes(self: Path) -> bytes:
        if self == locked:
            raise PermissionError(13, "Permission denied", str(self))
        return real_read_bytes(self)

    monkeypatch.setattr(Path, "read_bytes", read_bytes)
    assert scan([tmp_path]).unreadable == [locked]
    assert main([str(tmp_path)]) == 0
    assert "Could not read" in capsys.readouterr().out
