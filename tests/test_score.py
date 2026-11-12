import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

import pytest

from pairs import CRITERIA, Build, Choice, Key, Pair
from score import agreement, main, resolve

FIRST_WINS_EVERYWHERE: dict[str, Choice] = dict.fromkeys(CRITERIA, "A")


def verdict(**choices: Choice) -> dict[str, Choice]:
    ties: dict[str, Choice] = dict.fromkeys(CRITERIA, "tie")
    return ties | choices


def function_report(**overrides: Any) -> dict[str, Any]:
    report: dict[str, Any] = {
        "elapsed_seconds": 20.0,
        "axe_violations": [],
        "keyboard_walk": {
            "stops": [{"element": "a", "focus_visible": True, "covered": False}],
            "ended_by": "end",
        },
        "phone_overflow_px": 0,
        "head": dict.fromkeys(("title", "lang", "viewport", "description", "og_image"), True),
        "console_errors": [],
        "failed_requests": [],
        "timed_out_loads": [],
        "motion_frame_seconds": {},
        "budgets": None,
    }
    return report | overrides


@pytest.fixture
def round_dir(tmp_path: Path) -> Path:
    """Two pairs: p01 profiler (t1 bare first, t2 craft second), p02 restaurant (t4 craft first)."""
    cells = {
        "t1": ("profiler", "bare"),
        "t2": ("profiler", "craft"),
        "t3": ("restaurant", "bare"),
        "t4": ("restaurant", "craft"),
    }
    folder = tmp_path / "round"
    builds = {}
    for token, (subject, arm) in cells.items():
        capture = folder / "captures" / token
        capture.mkdir(parents=True)
        (capture / "function.json").write_text(json.dumps(function_report()))
        builds[token] = Build(subject, arm, 1, f"captures/{token}")
    key = Key(
        builds=builds,
        pairs=[Pair("p01", "profiler", "t1", "t2"), Pair("p02", "restaurant", "t4", "t3")],
        votes={"p01": 1, "p02": 2},
        dropped=["restaurant run 2: bare has no craft partner"],
    )
    (folder / "verdicts").mkdir()
    (folder / "key.json").write_text(json.dumps(asdict(key)))
    return folder


def write_verdict(round_dir: Path, name: str, content: Any) -> Path:
    path = round_dir / "verdicts" / f"{name}.json"
    path.write_text(content if isinstance(content, str) else json.dumps(content))
    return path


def results(round_dir: Path) -> str:
    assert main([str(round_dir)]) == 0
    return (round_dir / "results.md").read_text(encoding="utf-8")


PAIR = Pair("p01", "profiler", "t1", "t2")


def test_agreeing_verdicts_across_orders_score_a_win() -> None:
    # Order 1 shows t1 as page A; order 2 shows it as page B.
    winners = resolve(PAIR, verdict(overall="A", type="B"), verdict(overall="B", type="A"))
    assert winners["overall"] == "t1"
    assert winners["type"] == "t2"
    assert winners["imagery"] is None


def test_opposite_verdicts_across_orders_score_a_tie() -> None:
    # Choosing page A in both orders names a different build each time.
    winners = resolve(PAIR, FIRST_WINS_EVERYWHERE, FIRST_WINS_EVERYWHERE)
    assert set(winners.values()) == {None}


def test_one_tie_against_one_choice_scores_a_tie() -> None:
    assert resolve(PAIR, verdict(overall="A"), verdict())["overall"] is None


def test_agreement_counts_only_voted_pairs_both_orders_judged() -> None:
    judged: dict[str, dict[str, str | None]] = {
        "p01": {"overall": "t1"},
        "p02": {"overall": None},
        "p03": {"overall": "t5"},
    }
    votes = {"p01": "t1", "p02": "t3", "p04": "t7"}
    assert agreement(judged, votes) == (1, 2)


def test_judged_pairs_are_tallied_by_arm_and_criterion(round_dir: Path) -> None:
    write_verdict(round_dir, "p01-1", verdict(overall="B", type="A"))
    write_verdict(round_dir, "p01-2", verdict(overall="A", type="B"))
    write_verdict(round_dir, "p02-1", verdict(overall="A"))
    write_verdict(round_dir, "p02-2", verdict(overall="B"))
    text = results(round_dir)
    assert "| overall | 0 | 0 | 2 |" in text
    assert "| type | 1 | 1 | 0 |" in text
    assert "| imagery | 0 | 2 | 0 |" in text
    assert "Both orders agreed on overall for 2 of 2 judged pairs." in text
    assert "Page A was chosen in 2 of 4 overall choices of a page." in text


def test_a_missing_verdict_leaves_the_pair_unjudged_not_tied(round_dir: Path) -> None:
    write_verdict(round_dir, "p01-1", verdict(overall="B"))
    write_verdict(round_dir, "p01-2", verdict(overall="A"))
    write_verdict(round_dir, "p02-1", verdict(overall="A"))
    text = results(round_dir)
    assert "| overall | 0 | 0 | 1 |" in text
    assert "Unjudged: p02." in text
    assert "| p02 | restaurant | craft against bare | unjudged |" in text


@pytest.mark.parametrize(
    "content",
    [
        "{",
        "[]",
        verdict() | {"first-screen": "A"},
        {key: value for key, value in verdict().items() if key != "motion"},
        {**verdict(), "overall": "left"},
    ],
)
def test_a_malformed_verdict_exits_2_naming_the_file(
    round_dir: Path, capsys: pytest.CaptureFixture[str], content: Any
) -> None:
    path = write_verdict(round_dir, "p02-2", content)
    assert main([str(round_dir)]) == 2
    assert str(path) in capsys.readouterr().err
    assert not (round_dir / "results.md").exists()


def test_a_verdict_may_carry_reasons(round_dir: Path) -> None:
    write_verdict(round_dir, "p01-1", verdict(overall="A") | {"reasons": "A has a focal point."})
    write_verdict(round_dir, "p01-2", verdict(overall="B"))
    assert "| overall | 1 | 0 | 0 |" in results(round_dir)


def test_votes_are_mapped_through_the_order_the_vote_page_showed(round_dir: Path) -> None:
    # p02 was shown in order 2, so page A was t3 (bare).
    (round_dir / "votes.json").write_text(json.dumps({"p01": "B", "p02": "A"}))
    write_verdict(round_dir, "p01-1", verdict(overall="B"))
    write_verdict(round_dir, "p01-2", verdict(overall="A"))
    text = results(round_dir)
    assert "| p01 | profiler | bare against craft | craft | craft |" in text
    assert "| p02 | restaurant | craft against bare | unjudged | bare |" in text
    assert "Judges and the user agreed on 1 of 1 voted pairs both orders judged." in text
    assert "| bare against craft | 1 | 0 | 1 |" in text


def test_without_votes_the_results_say_so(round_dir: Path) -> None:
    assert "No votes.json yet." in results(round_dir)


@pytest.mark.parametrize(
    "votes",
    ["{", "[]", {"p09": "A"}, {"p01": "left"}],
)
def test_malformed_votes_exit_2_naming_the_file(
    round_dir: Path, capsys: pytest.CaptureFixture[str], votes: Any
) -> None:
    path = round_dir / "votes.json"
    path.write_text(votes if isinstance(votes, str) else json.dumps(votes))
    assert main([str(round_dir)]) == 2
    assert str(path) in capsys.readouterr().err


def write_function(round_dir: Path, token: str, report: dict[str, Any]) -> None:
    key = json.loads((round_dir / "key.json").read_text())
    (round_dir / key["builds"][token]["capture"] / "function.json").write_text(json.dumps(report))


def test_function_problems_are_counted_per_build_and_per_arm(round_dir: Path) -> None:
    write_function(
        round_dir,
        "t2",
        function_report(
            axe_violations=[
                {"rule": "label", "impact": "critical", "nodes": 2},
                {"rule": "region", "impact": "moderate", "nodes": 1},
            ],
            keyboard_walk={
                "stops": [
                    {"element": "a", "focus_visible": False, "covered": True},
                    {"element": "b", "focus_visible": False, "covered": False},
                ],
                "ended_by": "repeat",
            },
            phone_overflow_px=40,
            head=function_report()["head"] | {"og_image": False},
            console_errors=[
                "Failed to load resource: the server responded with a status of 404 (Not Found)",
                "boom",
            ],
            failed_requests=["/missing.png 404"],
            timed_out_loads=["phone"],
            budgets={"exit_code": 1, "lines": []},
            elapsed_seconds=95.0,
        ),
    )
    text = results(round_dir)
    assert (
        "| profiler | craft | 1 | 1 | 2 | 1 | repeat | 40 | 1 | 1 | og_image | 1 | breach | 95.0 |"
        in text
    )
    assert (
        "| profiler | bare | 1 | 0 | 0 | 0 | end | 0 | 0 | 0 | none | 0 | not run | 20.0 |" in text
    )
    assert "| craft | 2 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |" in text
    assert "| bare | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |" in text


@pytest.mark.parametrize(("exit_code", "shown"), [(0, "pass"), (2, "unmeasured")])
def test_budget_exit_codes_are_named(round_dir: Path, exit_code: int, shown: str) -> None:
    write_function(round_dir, "t1", function_report(budgets={"exit_code": exit_code, "lines": []}))
    assert f"| {shown} | 20.0 |" in results(round_dir)


def test_a_missing_function_report_exits_2_naming_it(
    round_dir: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = round_dir / "captures" / "t3" / "function.json"
    path.unlink()
    assert main([str(round_dir)]) == 2
    assert str(path) in capsys.readouterr().err


def test_a_malformed_function_report_exits_2_naming_it(
    round_dir: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    write_function(round_dir, "t4", {"elapsed_seconds": 1.0})
    assert main([str(round_dir)]) == 2
    assert "function.json" in capsys.readouterr().err


def test_dropped_pairs_are_listed(round_dir: Path) -> None:
    assert "- restaurant run 2: bare has no craft partner" in results(round_dir)


def test_an_unpaired_round_exits_2(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main([str(tmp_path)]) == 2
    assert "no key.json" in capsys.readouterr().err


def test_a_moved_round_still_finds_its_captures(round_dir: Path) -> None:
    moved = round_dir.rename(round_dir.with_name("moved"))
    assert "| profiler | bare | 1 |" in results(moved)
