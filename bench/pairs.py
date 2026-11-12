"""Pair a round's builds blindly, write a judge brief per pair and order, and a vote page.

Usage:
    python bench/pairs.py ROUND [--votes N]

ROUND is a folder holding manifest.json, with paths relative to ROUND:

    {"seed": 1,
     "subjects": {"profiler": "../../subjects/profiler.md"},
     "builds": [{"subject": "profiler", "arm": "bare", "run": 1,
                 "capture": "captures/profiler-bare-1"}]}

Each capture folder holds the images capture.py writes. Within a subject, run i
of each arm is paired with run i of every other arm; a run whose partner is
missing is dropped from that pairing and reported. Each build's judged images
are copied to blind/<token>/, the token drawn from the seed, so no path a judge
or voter sees names an arm.

ROUND receives briefs/<pair>-<order>.md (in order 1 the pair's first build is
page A, in order 2 it is page B), an empty verdicts/ for the judges, vote.html
with N pairs (default 10) chosen to cover every subject and arm pair where N
allows, and key.json, the only file that says which build is which. Capture
paths are kept as the manifest gives them, so a round whose captures sit
inside it can be moved.

Exit code 2 means nothing was written: the manifest or a prompt is missing or
malformed, a capture lacks an image, no two arms share a subject and run, or
ROUND has a key.json already, since re-pairing would orphan any verdicts
written against it. A verdicts/ folder holding files without key.json is
refused for the same reason. Briefs and blind images left by a pairing that
failed part-way are replaced.
"""

from __future__ import annotations

import argparse
import html
import itertools
import json
import random
import shutil
import sys
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from pathlib import Path
from string import Template
from typing import Any, Literal

from views import MOTION_FRAME_SECONDS, SCROLL_DEPTHS_PERCENT, motion_image, scroll_image

Choice = Literal["A", "B", "tie"]
CHOICES: tuple[Choice, ...] = ("A", "B", "tie")
CRITERIA = ("first_screen", "whole_page", "imagery", "type", "motion", "fit", "overall")
JUDGED_IMAGES = (
    "desktop-first.png",
    "desktop-full.png",
    *(scroll_image("desktop", percent) for percent in SCROLL_DEPTHS_PERCENT),
    *(motion_image("desktop", seconds) for seconds in MOTION_FRAME_SECONDS),
    "phone-first.png",
    "phone-full.png",
)
MAX_BUILDS = 200
MIN_ARMS = 2
DEFAULT_VOTES = 10
TOKEN_SPACE = 16**6
BUILD_FIELDS: dict[str, type] = {"subject": str, "arm": str, "run": int, "capture": str}
PAIR_FIELDS: dict[str, type] = {"id": str, "subject": str, "first": str, "second": str}
RUBRIC = Path(__file__).resolve().parent / "rubric.md"


class RoundError(Exception):
    """A round's input is missing or malformed; the message names the file."""


@dataclass(frozen=True, slots=True)
class Build:
    subject: str
    arm: str
    run: int
    # As the manifest gives it: relative to the round folder, or absolute.
    capture: str


@dataclass(frozen=True, slots=True)
class Pair:
    id: str
    subject: str
    first: str
    second: str


@dataclass(frozen=True, slots=True)
class Key:
    builds: dict[str, Build]
    pairs: list[Pair]
    # Pair id to the order, 1 or 2, in which vote.html shows it.
    votes: dict[str, int]
    dropped: list[str]


@dataclass(frozen=True, slots=True)
class Manifest:
    seed: int
    prompts: dict[str, str]
    builds: list[Build]


def read_text(path: Path) -> str:
    """The UTF-8 text at path; RoundError names the file when it is missing or not UTF-8."""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as error:
        raise RoundError(f"{path} not found") from error
    except UnicodeDecodeError as error:
        raise RoundError(f"{path}: not UTF-8 text ({error.reason})") from error


# Any: the parsed JSON is checked field by field by each caller.
def read_json(path: Path) -> Any:
    """The parsed JSON at path; RoundError names the file when it cannot be read or parsed."""
    try:
        return json.loads(read_text(path))
    except json.JSONDecodeError as error:
        raise RoundError(f"{path}: not valid JSON ({error})") from error


def _require(condition: bool, path: Path, message: str) -> None:
    if not condition:
        raise RoundError(f"{path}: {message}")


def _is_record(item: Any, fields: dict[str, type]) -> bool:
    return (
        type(item) is dict
        and set(item) == set(fields)
        and all(type(item[name]) is kind for name, kind in fields.items())
    )


def load_key(path: Path) -> Key:
    raw = read_json(path)
    _require(
        type(raw) is dict and set(raw) == {"builds", "pairs", "votes", "dropped"},
        path,
        'expected an object with "builds", "pairs", "votes" and "dropped"',
    )
    builds, pairs, votes, dropped = raw["builds"], raw["pairs"], raw["votes"], raw["dropped"]
    _require(
        type(builds) is dict and all(_is_record(b, BUILD_FIELDS) for b in builds.values()),
        path,
        "expected builds as an object of token to build",
    )
    _require(
        type(pairs) is list
        and all(
            _is_record(p, PAIR_FIELDS) and p["first"] in builds and p["second"] in builds
            for p in pairs
        ),
        path,
        "expected pairs as a list of pairs of builds in the key",
    )
    pair_ids = {p["id"] for p in pairs}
    _require(
        type(votes) is dict
        and all(k in pair_ids and type(v) is int and v in {1, 2} for k, v in votes.items()),
        path,
        "expected votes as an object of pair id to order 1 or 2",
    )
    _require(
        type(dropped) is list and all(type(line) is str for line in dropped),
        path,
        "expected dropped as a list of strings",
    )
    return Key(
        builds={token: Build(**build) for token, build in builds.items()},
        pairs=[Pair(**pair) for pair in pairs],
        votes=votes,
        dropped=dropped,
    )


def _parse_build(item: Any, subjects: dict[str, str], path: Path) -> Build:
    _require(
        isinstance(item, dict) and set(item) == {"subject", "arm", "run", "capture"},
        path,
        f'expected each build as {{"subject", "arm", "run", "capture"}}, got {item!r}',
    )
    subject, arm, run, capture = item["subject"], item["arm"], item["run"], item["capture"]
    _require(
        isinstance(subject, str) and subject in subjects,
        path,
        f"build names unknown subject {subject!r}",
    )
    _require(isinstance(arm, str) and arm != "", path, f"expected a non-empty arm, got {arm!r}")
    _require(type(run) is int and run > 0, path, f"expected a positive integer run, got {run!r}")
    _require(isinstance(capture, str), path, f"expected a capture path, got {capture!r}")
    return Build(subject, arm, run, capture)


def parse_manifest(path: Path) -> Manifest:
    if not path.exists():
        raise RoundError(f"no manifest.json in {path.parent}")
    raw = read_json(path)
    _require(
        isinstance(raw, dict) and set(raw) == {"seed", "subjects", "builds"},
        path,
        'expected an object with "seed", "subjects" and "builds"',
    )
    seed, subjects, items = raw["seed"], raw["subjects"], raw["builds"]
    _require(type(seed) is int, path, f"expected an integer seed, got {seed!r}")
    _require(
        isinstance(subjects, dict)
        and len(subjects) > 0
        and all(isinstance(prompt, str) for prompt in subjects.values()),
        path,
        "expected subjects as a non-empty object of name to prompt file",
    )
    _require(
        isinstance(items, list) and 0 < len(items) <= MAX_BUILDS,
        path,
        f"expected builds as a list of 1 to {MAX_BUILDS} entries",
    )
    builds = [_parse_build(item, subjects, path) for item in items]
    seen: set[tuple[str, str, int]] = set()
    for build in builds:
        cell = (build.subject, build.arm, build.run)
        _require(
            cell not in seen, path, f"{build.subject} {build.arm} run {build.run} listed twice"
        )
        seen.add(cell)
    _require(
        len({b.arm for b in builds}) >= MIN_ARMS, path, "expected builds from at least two arms"
    )
    prompts = {name: read_text(path.parent / file).strip() for name, file in subjects.items()}
    return Manifest(seed, prompts, builds)


def _check_images(round_dir: Path, builds: list[Build]) -> None:
    for build in builds:
        for name in JUDGED_IMAGES:
            image = round_dir / build.capture / name
            if not image.is_file():
                raise RoundError(f"capture image {image} not found")


def match_builds(builds: list[Build]) -> tuple[list[tuple[Build, Build]], list[str]]:
    """Pair run i of each arm with run i of every other arm, within each subject."""
    by_cell = {(b.subject, b.arm, b.run): b for b in builds}
    arms = sorted({b.arm for b in builds})
    matched: list[tuple[Build, Build]] = []
    dropped: list[str] = []
    for subject in sorted({b.subject for b in builds}):
        for run in sorted({b.run for b in builds if b.subject == subject}):
            for left_arm, right_arm in itertools.combinations(arms, 2):
                left = by_cell.get((subject, left_arm, run))
                right = by_cell.get((subject, right_arm, run))
                if left is not None and right is not None:
                    matched.append((left, right))
                elif left is not None or right is not None:
                    present, absent = (left_arm, right_arm) if left else (right_arm, left_arm)
                    dropped.append(f"{subject} run {run}: {present} has no {absent} partner")
    return matched, dropped


def choose_votes(pairs: list[Pair], key_builds: dict[str, Build], count: int) -> list[Pair]:
    """Pick count pairs, each time preferring one that adds an unseen subject, arm pair or both."""

    def arm_pair(pair: Pair) -> frozenset[str]:
        return frozenset({key_builds[pair.first].arm, key_builds[pair.second].arm})

    chosen: list[Pair] = []
    remaining = list(pairs)
    while remaining and len(chosen) < count:
        subjects = {p.subject for p in chosen}
        arm_pairs = {arm_pair(p) for p in chosen}
        cells = {(p.subject, arm_pair(p)) for p in chosen}
        best = max(
            remaining,
            key=lambda p: (
                (p.subject not in subjects)
                + (arm_pair(p) not in arm_pairs)
                + ((p.subject, arm_pair(p)) not in cells)
            ),
        )
        chosen.append(best)
        remaining.remove(best)
    return chosen


def draw_key(manifest: Manifest, vote_count: int, rng: random.Random) -> Key:
    builds = sorted(manifest.builds, key=lambda b: (b.subject, b.arm, b.run))
    tokens = [f"{n:06x}" for n in rng.sample(range(TOKEN_SPACE), len(builds))]
    token_of = dict(zip(builds, tokens, strict=True))
    matched, dropped = match_builds(builds)
    rng.shuffle(matched)
    pairs = []
    for number, (left, right) in enumerate(matched, start=1):
        first, second = rng.sample((left, right), 2)
        pairs.append(Pair(f"p{number:02d}", left.subject, token_of[first], token_of[second]))
    key_builds = dict(zip(tokens, builds, strict=True))
    voted = choose_votes(pairs, key_builds, vote_count)
    return Key(key_builds, pairs, {p.id: rng.choice((1, 2)) for p in voted}, dropped)


BRIEF = Template("""\
Goal: $verdict holds a verdict, criterion by criterion, on which of two web pages, A and B, better serves the subject below.
Task type: review
Skill: none
Read: $rubric, then the images listed below and no other file.
Change: write $verdict only.
Done when: $verdict parses as one JSON object with the keys $keys, each "A", "B" or "tie", and "reasons", a string giving the observation that decided each criterion.
Constraints: Judge from the images alone. Do not open, list or search any other path in the repository, and do not load a skill. Which page is A was decided at random, so position is no evidence. Give "tie" when the difference on a criterion is too small to name.
Ruled out: nothing.

## Subject

$subject

## Images

Each page has the same views: the first screen at 1440 by 900 after load; the whole page at 1440 wide; the screen at 25, 50 and 75% of the page's depth; the first screen 0.25, 0.75, 1.5 and 3 s after navigation, which shows its motion; the first screen at 375 by 812; the whole page at 375 wide.

## Page A

$page_a

## Page B

$page_b
""")  # noqa: E501 (each brief field is one line, as the subagent brief format expects)


def _image_list(folder: Path) -> str:
    return "\n".join(f"- {(folder / name).as_posix()}" for name in JUDGED_IMAGES)


def write_brief(round_dir: Path, pair: Pair, order: int, prompt: str) -> None:
    page_a, page_b = (pair.first, pair.second) if order == 1 else (pair.second, pair.first)
    blind = round_dir.resolve() / "blind"
    text = BRIEF.substitute(
        verdict=(round_dir.resolve() / "verdicts" / f"{pair.id}-{order}.json").as_posix(),
        rubric=RUBRIC.as_posix(),
        keys=", ".join(f'"{criterion}"' for criterion in CRITERIA),
        subject=prompt,
        page_a=_image_list(blind / page_a),
        page_b=_image_list(blind / page_b),
    )
    (round_dir / "briefs" / f"{pair.id}-{order}.md").write_text(text, encoding="utf-8")


VOTE_PAGE = Template("""\
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bench votes</title>
<style>
:root { --ink: #1b1b1f; --muted: #5d5d66; --line: #d6d6dc; --paper: #fbfbf9; --panel: #f0f0ec; }
@media (prefers-color-scheme: dark) {
  :root { --ink: #ececef; --muted: #a2a2ab; --line: #3a3a42; --paper: #141417; --panel: #1e1e23; }
}
* { box-sizing: border-box; }
body { margin: 0; padding: 24px 16px 96px; background: var(--paper); color: var(--ink);
  font: 16px/1.5 system-ui, sans-serif; }
main { max-width: 1600px; margin: 0 auto; }
h1 { font-size: 1.5rem; margin: 0 0 8px; }
h2 { font-size: 1.25rem; margin: 0 0 8px; }
h3 { font-size: 1rem; margin: 0 0 8px; }
p, summary { color: var(--muted); }
pre { white-space: pre-wrap; font: inherit; background: var(--panel); padding: 16px; }
section { border-top: 1px solid var(--line); padding: 32px 0; }
.pages { display: grid; grid-template-columns: 1fr; gap: 24px; margin: 16px 0; }
@media (min-width: 900px) { .pages { grid-template-columns: 1fr 1fr; } }
.page { background: var(--panel); padding: 16px; min-width: 0; }
figure { margin: 0 0 16px; }
figcaption { font-size: 0.875rem; color: var(--muted); }
img { display: block; width: 100%; height: auto; border: 1px solid var(--line); }
.tall { max-height: 70vh; overflow-y: auto; }
.row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }
.phone { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
fieldset { border: 1px solid var(--line); padding: 12px 16px; }
label { margin-right: 24px; white-space: nowrap; }
input { accent-color: var(--ink); }
footer { position: fixed; left: 0; right: 0; bottom: 0; padding: 12px 16px;
  background: var(--paper); border-top: 1px solid var(--line); }
button { font: inherit; padding: 8px 16px; margin-left: 16px; }
:focus-visible { outline: 3px solid var(--ink); outline-offset: 2px; }
</style>
</head>
<body>
<main>
<h1>Bench votes</h1>
<p>For each pair, look at both pages and choose the better one overall, or tie.
Images open full size in a new tab. Export when done and save votes.json in the
round folder, beside key.json.</p>
<details><summary>Rubric</summary><pre>$rubric</pre></details>
<form id="votes">
$pairs
</form>
</main>
<footer><output id="count" form="votes">0</output> of $count voted
<button type="button" id="export">Export votes.json</button></footer>
<script>
const form = document.getElementById('votes');
const votes = () => Object.fromEntries(new FormData(form));
form.addEventListener('change', () => {
  document.getElementById('count').textContent = Object.keys(votes()).length;
});
document.getElementById('export').addEventListener('click', () => {
  const blob = new Blob([JSON.stringify(votes(), null, 2) + '\\n'], {type: 'application/json'});
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'votes.json';
  link.click();
  URL.revokeObjectURL(link.href);
});
</script>
</body>
</html>
""")


def _figure(token: str, name: str, caption: str, page: str) -> str:
    src = f"blind/{token}/{name}"
    alt = html.escape(f"Page {page}, {caption}")
    return (
        f'<figure><a href="{src}" target="_blank"><img src="{src}" alt="{alt}" loading="lazy">'
        f"</a><figcaption>{html.escape(caption)}</figcaption></figure>"
    )


def _vote_page_column(token: str, page: str) -> str:
    motion = "".join(
        _figure(token, motion_image("desktop", seconds), f"{seconds} s after navigation", page)
        for seconds in MOTION_FRAME_SECONDS
    )
    desktop_full = _figure(token, "desktop-full.png", "desktop whole page", page)
    phone_full = _figure(token, "phone-full.png", "phone whole page", page)
    return (
        f'<div class="page"><h3>Page {page}</h3>'
        + _figure(token, "desktop-first.png", "desktop first screen", page)
        + f'<div class="row">{motion}</div><div class="tall">{desktop_full}</div>'
        + '<div class="phone">'
        + _figure(token, "phone-first.png", "phone first screen", page)
        + f'<div class="tall">{phone_full}</div></div></div>'
    )


def _vote_section(pair: Pair, order: int, prompt: str) -> str:
    page_a, page_b = (pair.first, pair.second) if order == 1 else (pair.second, pair.first)
    radios = "".join(
        f'<label><input type="radio" name="{pair.id}" value="{choice}"> {choice}</label>'
        for choice in CHOICES
    )
    return (
        f'<section aria-labelledby="h-{pair.id}"><h2 id="h-{pair.id}">Pair {pair.id}</h2>'
        f"<details><summary>Subject</summary><p>{html.escape(prompt)}</p></details>"
        f'<div class="pages">{_vote_page_column(page_a, "A")}{_vote_page_column(page_b, "B")}'
        f"</div><fieldset><legend>Better overall</legend>{radios}</fieldset></section>"
    )


def write_round(round_dir: Path, manifest: Manifest, key: Key) -> None:
    # Left by a pairing that failed part-way; its tokens and pair ids are not this key's.
    for stale in (round_dir / "blind", round_dir / "briefs"):
        if stale.exists():
            shutil.rmtree(stale)
    for token, build in key.builds.items():
        folder = round_dir / "blind" / token
        folder.mkdir(parents=True, exist_ok=True)
        for name in JUDGED_IMAGES:
            shutil.copyfile(round_dir / build.capture / name, folder / name)
    (round_dir / "briefs").mkdir(exist_ok=True)
    (round_dir / "verdicts").mkdir(exist_ok=True)
    for pair in key.pairs:
        for order in (1, 2):
            write_brief(round_dir, pair, order, manifest.prompts[pair.subject])
    voted = [pair for pair in key.pairs if pair.id in key.votes]
    page = VOTE_PAGE.substitute(
        rubric=html.escape(RUBRIC.read_text(encoding="utf-8")),
        pairs="\n".join(
            _vote_section(p, key.votes[p.id], manifest.prompts[p.subject]) for p in voted
        ),
        count=len(voted),
    )
    (round_dir / "vote.html").write_text(page, encoding="utf-8")
    # Written last: a run that fails part-way leaves no key, so it can be repeated.
    (round_dir / "key.json").write_text(json.dumps(asdict(key), indent=2) + "\n", encoding="utf-8")


def _positive_count(text: str) -> int:
    count = int(text)
    if count <= 0:
        raise argparse.ArgumentTypeError(f"expected a positive number of votes, got {text!r}")
    return count


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else None)
    parser.add_argument("round", type=Path, help="folder holding manifest.json")
    parser.add_argument("--votes", type=_positive_count, default=DEFAULT_VOTES)
    args = parser.parse_args(argv)
    try:
        if (args.round / "key.json").exists():
            raise RoundError(f"{args.round} is already paired: key.json exists")
        verdicts = args.round / "verdicts"
        if verdicts.is_dir() and any(verdicts.iterdir()):
            raise RoundError(f"{verdicts} holds verdicts with no key.json; move them away first")
        manifest = parse_manifest(args.round / "manifest.json")
        _check_images(args.round, manifest.builds)
        # Seeded so a round can be paired again identically; the tokens hide
        # arms from judges reading files, not from anyone holding the seed.
        key = draw_key(manifest, args.votes, random.Random(manifest.seed))  # noqa: S311
        if not key.pairs:
            raise RoundError(f"{args.round}: nothing to pair, no two arms share a subject and run")
    except RoundError as error:
        print(error, file=sys.stderr)
        return 2
    write_round(args.round, manifest, key)
    print(f"paired {len(key.pairs)} pairs, {len(key.votes)} on the vote page")
    if key.dropped:
        print(f"dropped {len(key.dropped)} pairs:")
        for line in key.dropped:
            print(f"  {line}")
    return 0


if __name__ == "__main__":  # pragma: no cover: entry point wiring only
    sys.exit(main())
