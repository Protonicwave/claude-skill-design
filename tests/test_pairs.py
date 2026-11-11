import json
from pathlib import Path
from typing import Any

import pytest

from pairs import JUDGED_IMAGES, load_key, main

ARMS = ("bare", "frontend-design", "web-ui-craft")
SUBJECTS = ("profiler", "restaurant")


def write_captures(root: Path, *, runs: int = 2) -> list[dict[str, Any]]:
    """Fake captures outside any round, each image's bytes naming its build."""
    builds = []
    for subject in SUBJECTS:
        for arm in ARMS:
            for run in range(1, runs + 1):
                folder = root / "captures" / f"{subject}-{arm}-{run}"
                folder.mkdir(parents=True)
                for name in JUDGED_IMAGES:
                    (folder / name).write_bytes(f"{subject} {arm} {run} {name}".encode())
                builds.append({"subject": subject, "arm": arm, "run": run, "capture": str(folder)})
    return builds


def write_round(root: Path, builds: list[dict[str, Any]], *, seed: int = 7) -> Path:
    subjects_dir = root / "subjects"
    subjects_dir.mkdir(exist_ok=True)
    for subject in SUBJECTS:
        (subjects_dir / f"{subject}.md").write_text(f"Build a page for a {subject}.\n")
    round_dir = root / f"round-{seed}"
    round_dir.mkdir()
    manifest = {
        "seed": seed,
        "subjects": {subject: f"../subjects/{subject}.md" for subject in SUBJECTS},
        "builds": builds,
    }
    (round_dir / "manifest.json").write_text(json.dumps(manifest))
    return round_dir


@pytest.fixture
def paired_round(tmp_path: Path) -> Path:
    round_dir = write_round(tmp_path, write_captures(tmp_path))
    assert main([str(round_dir)]) == 0
    return round_dir


def test_same_seed_gives_the_same_pairs_and_vote_page(tmp_path: Path) -> None:
    builds = write_captures(tmp_path)
    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    first = write_round(tmp_path / "a", builds)
    second = write_round(tmp_path / "b", builds)
    assert main([str(first)]) == 0
    assert main([str(second)]) == 0
    assert (first / "key.json").read_text() == (second / "key.json").read_text()
    assert (first / "vote.html").read_text() == (second / "vote.html").read_text()


def test_arm_names_appear_in_no_brief_and_not_in_the_vote_page(paired_round: Path) -> None:
    pages = [*sorted((paired_round / "briefs").glob("*.md")), paired_round / "vote.html"]
    assert len(pages) == 2 * 12 + 1
    for page in pages:
        text = page.read_text(encoding="utf-8").lower()
        for arm in ARMS:
            assert arm not in text, f"{arm} named in {page.name}"
        assert "captures" not in text, f"capture path in {page.name}"


def test_run_of_each_arm_is_paired_with_the_same_run_of_every_other_arm(
    paired_round: Path,
) -> None:
    key = load_key(paired_round / "key.json")
    matchups = {
        (
            pair.subject,
            frozenset({key.builds[pair.first].arm, key.builds[pair.second].arm}),
            key.builds[pair.first].run,
        )
        for pair in key.pairs
        if key.builds[pair.first].run == key.builds[pair.second].run
    }
    arm_pairs = {frozenset(p) for p in (ARMS[:2], ARMS[1:], (ARMS[0], ARMS[2]))}
    assert len(key.pairs) == 12
    assert matchups == {(s, a, r) for s in SUBJECTS for a in arm_pairs for r in (1, 2)}
    assert key.dropped == []


def test_blind_images_are_copies_of_the_build_their_token_stands_for(paired_round: Path) -> None:
    key = load_key(paired_round / "key.json")
    assert len(key.builds) == 12
    for token, build in key.builds.items():
        image = paired_round / "blind" / token / "desktop-first.png"
        assert (
            image.read_bytes()
            == f"{build.subject} {build.arm} {build.run} desktop-first.png".encode()
        )


def test_order_two_swaps_which_build_is_page_a(paired_round: Path) -> None:
    pair = load_key(paired_round / "key.json").pairs[0]
    order_1 = (paired_round / "briefs" / f"{pair.id}-1.md").read_text(encoding="utf-8")
    order_2 = (paired_round / "briefs" / f"{pair.id}-2.md").read_text(encoding="utf-8")

    def page_a(brief: str) -> str:
        return brief.split("## Page A", 1)[1].split("## Page B", 1)[0]

    assert f"blind/{pair.first}/" in page_a(order_1)
    assert f"blind/{pair.second}/" not in page_a(order_1)
    assert f"blind/{pair.second}/" in page_a(order_2)
    assert f"verdicts/{pair.id}-2.json" in order_2


def test_a_run_without_a_partner_is_dropped_and_reported(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    builds = [
        b
        for b in write_captures(tmp_path)
        if (b["subject"], b["arm"], b["run"]) != ("profiler", "web-ui-craft", 2)
    ]
    round_dir = write_round(tmp_path, builds)
    assert main([str(round_dir)]) == 0
    key = load_key(round_dir / "key.json")
    assert len(key.pairs) == 10
    assert len(key.dropped) == 2
    assert all(line.startswith("profiler run 2:") for line in key.dropped)
    assert "dropped 2 pairs" in capsys.readouterr().out


def test_vote_pairs_cover_every_subject_and_arm_pair(tmp_path: Path) -> None:
    round_dir = write_round(tmp_path, write_captures(tmp_path))
    assert main([str(round_dir), "--votes", "3"]) == 0
    key = load_key(round_dir / "key.json")
    voted = [pair for pair in key.pairs if pair.id in key.votes]
    assert len(voted) == 3
    assert {pair.subject for pair in voted} == set(SUBJECTS)
    arm_pairs = {frozenset({key.builds[p.first].arm, key.builds[p.second].arm}) for p in voted}
    assert len(arm_pairs) == 3
    assert set(key.votes.values()) <= {1, 2}
    page = (round_dir / "vote.html").read_text(encoding="utf-8")
    assert page.count('type="radio"') == 3 * 3


def test_more_votes_than_pairs_puts_every_pair_on_the_vote_page(tmp_path: Path) -> None:
    round_dir = write_round(tmp_path, write_captures(tmp_path, runs=1))
    assert main([str(round_dir), "--votes", "50"]) == 0
    key = load_key(round_dir / "key.json")
    assert len(key.votes) == len(key.pairs) == 6


def test_an_already_paired_round_exits_2_and_keeps_its_key(
    paired_round: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    before = (paired_round / "key.json").read_text()
    assert main([str(paired_round)]) == 2
    assert "already paired" in capsys.readouterr().err
    assert (paired_round / "key.json").read_text() == before


def test_a_capture_missing_an_image_exits_2_naming_it_and_writes_nothing(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    builds = write_captures(tmp_path)
    missing = Path(builds[3]["capture"]) / "phone-full.png"
    missing.unlink()
    round_dir = write_round(tmp_path, builds)
    assert main([str(round_dir)]) == 2
    assert str(missing) in capsys.readouterr().err
    assert sorted(p.name for p in round_dir.iterdir()) == ["manifest.json"]


def test_a_missing_subject_prompt_exits_2_naming_it(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    round_dir = write_round(tmp_path, write_captures(tmp_path))
    (tmp_path / "subjects" / "restaurant.md").unlink()
    assert main([str(round_dir)]) == 2
    assert "restaurant.md" in capsys.readouterr().err


def test_a_missing_manifest_exits_2(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main([str(tmp_path)]) == 2
    assert "no manifest.json" in capsys.readouterr().err


GOOD_BUILD = {"subject": "profiler", "arm": "bare", "run": 1, "capture": "c"}


@pytest.mark.parametrize(
    ("manifest", "message"),
    [
        ("{", "not valid JSON"),
        ([], "expected an object"),
        ({"seed": 1, "subjects": {}}, "expected an object"),
        ({"seed": True, "subjects": {"profiler": "p.md"}, "builds": []}, "integer seed"),
        ({"seed": 1, "subjects": {}, "builds": []}, "subjects"),
        ({"seed": 1, "subjects": {"profiler": 3}, "builds": []}, "subjects"),
        ({"seed": 1, "subjects": {"profiler": "p.md"}, "builds": []}, "builds"),
        ({"seed": 1, "subjects": {"profiler": "p.md"}, "builds": [[]]}, "expected each build"),
        (
            {"seed": 1, "subjects": {"profiler": "p.md"}, "builds": [GOOD_BUILD | {"run": 0}]},
            "positive integer run",
        ),
        (
            {"seed": 1, "subjects": {"profiler": "p.md"}, "builds": [GOOD_BUILD | {"arm": ""}]},
            "arm",
        ),
        (
            {"seed": 1, "subjects": {"profiler": "p.md"}, "builds": [GOOD_BUILD | {"capture": 4}]},
            "capture",
        ),
        (
            {
                "seed": 1,
                "subjects": {"profiler": "p.md"},
                "builds": [GOOD_BUILD | {"subject": "x"}],
            },
            "unknown subject 'x'",
        ),
        (
            {"seed": 1, "subjects": {"profiler": "p.md"}, "builds": [GOOD_BUILD, GOOD_BUILD]},
            "profiler bare run 1 listed twice",
        ),
        (
            {"seed": 1, "subjects": {"profiler": "p.md"}, "builds": [GOOD_BUILD]},
            "at least two arms",
        ),
    ],
)
def test_a_malformed_manifest_exits_2_with_the_reason(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], manifest: Any, message: str
) -> None:
    text = manifest if isinstance(manifest, str) else json.dumps(manifest)
    (tmp_path / "manifest.json").write_text(text)
    assert main([str(tmp_path)]) == 2
    err = capsys.readouterr().err
    assert "manifest.json" in err
    assert message in err


def test_too_many_builds_exits_2(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    builds = [GOOD_BUILD | {"run": run} for run in range(1, 1000)]
    manifest = {"seed": 1, "subjects": {"profiler": "p.md"}, "builds": builds}
    (tmp_path / "manifest.json").write_text(json.dumps(manifest))
    assert main([str(tmp_path)]) == 2
    assert "builds" in capsys.readouterr().err


def test_votes_must_be_positive(paired_round: Path) -> None:
    with pytest.raises(SystemExit):
        main([str(paired_round), "--votes", "0"])


def test_a_run_only_one_arm_has_is_dropped_once_per_other_arm(tmp_path: Path) -> None:
    builds = [
        b
        for b in write_captures(tmp_path)
        if b["run"] == 1 or (b["subject"], b["arm"]) == ("profiler", "web-ui-craft")
    ]
    round_dir = write_round(tmp_path, builds)
    assert main([str(round_dir)]) == 0
    assert load_key(round_dir / "key.json").dropped == [
        "profiler run 2: web-ui-craft has no bare partner",
        "profiler run 2: web-ui-craft has no frontend-design partner",
    ]
