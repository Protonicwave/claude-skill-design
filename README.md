# claude-skill-design

Claude Code skills for designing and building web interfaces.

## Skills

### web-ui-craft

Makes Claude design web UI the way acclaimed sites are built rather than filling every unmade decision with the most common default. It writes a design brief derived from the subject before any code, compares layouts and tests the brief against known generic tells and against the brief a neighbouring subject would get, builds from tokens with evidence-based defaults for type, colour, spacing, depth, motion, navigation, states, performance and accessibility, and finishes with a critique pass.

Most of the effort goes into one hero piece built in code to a fidelity checklist: a product screen with believable data, or a lit object, often playing a short loop of itself. Motion is set by site tier, product or brand. The critique measures the page with Lighthouse rather than estimating it, and holds a screenshot of the build beside one acclaimed site in the same direction.

- `skills/web-ui-craft/SKILL.md`: the process and the build sheet.
- `skills/web-ui-craft/references/`: detail loaded on demand.
- `skills/web-ui-craft/scripts/check_slop.py`: static scan for craft defects and generic tells.
- `skills/web-ui-craft/scripts/check_budgets.py`: compares a Lighthouse report with the page budgets.
- `skills/web-ui-craft/scripts/check_phone.py`: measures how far a page runs past a 375 px screen and checks its viewport tag, from headless Chrome.
- `bench/capture.py`: captures a built page for the design bench and checks how it functions.
- `bench/pairs.py` and `bench/score.py`: pair a bench round's builds blindly for judging and voting, then score the verdicts and votes against `bench/rubric.md`.
- `research/`: the report and notes every rule is drawn from, with sources. `research/notes/premium-benchmark.md` records two test pages built with the skill before and after its premium revision.

## Install

Link the skill folder into your personal skills directory so edits in this repository apply immediately.

macOS or Linux:

```sh
ln -s "$(pwd)/skills/web-ui-craft" ~/.claude/skills/web-ui-craft
```

Windows (PowerShell; a junction needs no administrator rights):

```powershell
New-Item -ItemType Junction -Path "$HOME\.claude\skills\web-ui-craft" -Target "$PWD\skills\web-ui-craft"
```

The skill's scripts need Python 3.12 or later and no packages. Its speed check runs `npx lighthouse@13.6.0`, so it needs Node and Chrome; without them the skill says so in its report and claims no budget as passed.

Claude Code picks the skill up in new sessions and uses it whenever a task involves building or restyling web UI. Invoke it directly with `/web-ui-craft`.

## Development

Requires Python 3.12 or later and [uv](https://docs.astral.sh/uv/).

```sh
uv sync
uv run pytest
uv run ruff check . && uv run ruff format --check .
uv run mypy
uv run vulture skills bench tests --min-confidence 80
```

`bench/pairs.py` and `bench/score.py` decide what a bench round concludes, so both keep full line and branch coverage:

```sh
uv run pytest tests/test_pairs.py tests/test_score.py --cov=bench --cov-branch --cov-report=
uv run coverage report --show-missing --fail-under=100 --include="bench/pairs.py,bench/score.py"
```

The capture tests drive the installed Chrome and skip when it cannot be started. The Lighthouse test also needs Node.

## Design bench

The bench compares pages built with and without the skill. Capture one build, a folder holding `index.html`:

```sh
uv run python bench/capture.py path/to/build path/to/out
```

`out` receives desktop (1440 by 900) and phone (375 by 812) screenshots: the first screen, frames at 0.25, 0.75, 1.5 and 3 s after navigation, three scroll depths, the full page and the first screen with reduced motion. It also receives `function.json`, recording axe violations, a keyboard walk, phone overflow, text clipped at the phone width, console errors, failed requests and head tags. `--lighthouse` adds a mobile Lighthouse run judged by `check_budgets.py`. The script prints its elapsed time beside the 90 s budget for one capture without Lighthouse.

### Running a round

A round compares arms, each a set of instructions given to the builder, on the same subjects. Each round lives in `bench/runs/<round>/`, which git ignores:

```
manifest.json   the builds, written by hand after they exist
arms/<arm>/     each arm's instructions, copied at the round's commit
builds/<id>/    one page per build; <id> is <subject>-<arm>-<run>
captures/<id>/  capture.py output for that build
briefs/ blind/ verdicts/ vote.html key.json   written by pairs.py
votes.json      exported from vote.html
results.md      written by score.py
```

1. Copy each arm's instructions into `arms/`: a skill's whole folder, so its references resolve inside the copy. An arm with no instructions has no folder.
2. Build each page with one subagent per build, on the same model for every arm, using the brief below. A build whose reply names a skill or file of another arm is discarded and rebuilt once.
3. Capture each build: `uv run python bench/capture.py bench/runs/<round>/builds/<id> bench/runs/<round>/captures/<id>`. An arm whose instructions have not changed since an earlier round need not be rebuilt: capture its builds from that round's `builds/` into this round's `captures/`, so every build in the round is measured by the same capture.
4. Write `manifest.json`, with paths relative to the round folder:

   ```json
   {"seed": 1,
    "subjects": {"profiler": "../../subjects/profiler.md"},
    "builds": [{"subject": "profiler", "arm": "bare", "run": 1, "capture": "captures/profiler-bare-1"}]}
   ```

5. Pair: `uv run python bench/pairs.py bench/runs/<round>`. It pairs run i of each arm with run i of every other arm within a subject, copies each build's judged images under a random token, and writes a judge brief per pair and order. A phone whole-page image taller than 2,600 px reaches judges as tiles of that height, since a taller image is shrunk before they see it. `--votes N` sets how many pairs go on the vote page (default 10). It refuses a round that already has `key.json`, since re-pairing would orphan its verdicts.
6. Judge: give each file in `briefs/` verbatim as the prompt of one fresh subagent. Each writes `verdicts/<pair>-<order>.json`. Judges see the subject and images only, never code, arm names or builder briefs.
7. Vote: open `vote.html`, choose a page or a tie for each pair, export, and save `votes.json` in the round folder.
8. Score: `uv run python bench/score.py bench/runs/<round>` writes `results.md`: judge tallies per arm pair and criterion, where a choice counts only when both orders agree; agreement between judges and votes; and each build's function checks.

Builder brief, one per build, with the subject's prompt pasted at the end:

```
Goal: bench/runs/<round>/builds/<id>/index.html is a finished page for the subject below.
Task type: ui-build
Skill: none
Read: bench/runs/<round>/arms/<arm>/SKILL.md, and follow it as your instructions, resolving its relative paths inside that folder. (Bare arm: nothing.)
Change: create files in bench/runs/<round>/builds/<id>/ only.
Done when: the folder holds index.html, the page opens without console errors, and your reply names every skill or file you read.
Constraints: Do not use the Skill tool. Read any file in your arm's folder and no other file in the repository, and no other build. Keep scratch files in a folder named <id> inside your scratchpad, since other builders share it.
Ruled out: nothing.

<subject prompt>
```

Before a round whose rubric or judge brief changed, run the known-answer check: pair two builds whose better page is already agreed, in both orders, and confirm the judges prefer it in both. If they do not, revise the rubric before paying for builds.
