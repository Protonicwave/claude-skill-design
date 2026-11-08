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

The skill's scripts need Python 3.11 or later and no packages. Its speed check runs `npx lighthouse@13.6.0`, so it needs Node and Chrome; without them the skill says so in its report and claims no budget as passed.

Claude Code picks the skill up in new sessions and uses it whenever a task involves building or restyling web UI. Invoke it directly with `/web-ui-craft`.

## Development

Requires Python 3.12 or later and [uv](https://docs.astral.sh/uv/).

```sh
uv sync
uv run pytest
uv run ruff check . && uv run ruff format --check .
uv run mypy
uv run vulture skills tests --min-confidence 80
```
