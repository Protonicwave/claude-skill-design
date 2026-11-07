"""Structural checks every skill in the repository must pass to load and stay navigable."""

import re
from pathlib import Path

import pytest

SKILLS_ROOT = Path(__file__).resolve().parent.parent / "skills"
SKILL_DIRS = sorted(path.parent for path in SKILLS_ROOT.glob("*/SKILL.md"))
MAX_DESCRIPTION_CHARS = 1024
MAX_SKILL_MD_LINES = 500
FILE_REFERENCE = re.compile(r"`([\w./-]+\.(?:md|py))`")


def read_frontmatter(skill_md: Path) -> dict[str, str]:
    lines = skill_md.read_text(encoding="utf-8").splitlines()
    assert lines[0] == "---", f"{skill_md} must start with a frontmatter fence"
    closing = lines.index("---", 1)
    fields: dict[str, str] = {}
    for line in lines[1:closing]:
        key, separator, value = line.partition(": ")
        assert separator, f"{skill_md}: frontmatter line is not 'key: value': {line!r}"
        fields[key] = value
    return fields


def referenced_paths(markdown_file: Path, skill_dir: Path) -> list[Path]:
    """Resolve each backticked file name against the skill root, then the file's own folder."""
    resolved = []
    for name in FILE_REFERENCE.findall(markdown_file.read_text(encoding="utf-8")):
        from_root = skill_dir / name
        resolved.append(from_root if from_root.exists() else markdown_file.parent / name)
    return resolved


def test_repository_contains_a_skill() -> None:
    assert SKILL_DIRS


@pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=lambda path: path.name)
def test_frontmatter_names_the_folder(skill_dir: Path) -> None:
    assert read_frontmatter(skill_dir / "SKILL.md").get("name") == skill_dir.name


@pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=lambda path: path.name)
def test_description_fits_the_loader_limit(skill_dir: Path) -> None:
    description = read_frontmatter(skill_dir / "SKILL.md").get("description", "")
    assert 0 < len(description) <= MAX_DESCRIPTION_CHARS
    assert "<" not in description
    assert ">" not in description


@pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=lambda path: path.name)
def test_skill_md_stays_short(skill_dir: Path) -> None:
    line_count = len((skill_dir / "SKILL.md").read_text(encoding="utf-8").splitlines())
    assert line_count <= MAX_SKILL_MD_LINES


@pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=lambda path: path.name)
def test_every_referenced_file_exists(skill_dir: Path) -> None:
    missing = [
        f"{markdown_file.name} -> {path.name}"
        for markdown_file in skill_dir.rglob("*.md")
        for path in referenced_paths(markdown_file, skill_dir)
        if not path.exists()
    ]
    assert missing == []


@pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=lambda path: path.name)
def test_every_bundled_file_is_reachable_from_skill_md(skill_dir: Path) -> None:
    reachable = {path.resolve() for path in referenced_paths(skill_dir / "SKILL.md", skill_dir)}
    bundled = {
        path.resolve()
        for folder in ("references", "scripts")
        for path in (skill_dir / folder).glob("*")
        if path.is_file()
    }
    assert bundled - reachable == set()
