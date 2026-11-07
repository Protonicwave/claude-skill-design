# claude-skill-design

Claude Code skills for designing and building web interfaces.

## Skills

### web-ui-craft

Makes Claude design web UI the way acclaimed sites are built rather than filling every unmade decision with the most common default. It writes a design brief derived from the subject before any code, challenges the brief against known generic tells, builds from tokens with evidence-based defaults for type, colour, spacing, depth, motion, navigation, states, performance and accessibility, and finishes with a critique pass.

- `skills/web-ui-craft/SKILL.md`: the process and the build sheet.
- `skills/web-ui-craft/references/`: detail loaded on demand.
- `research/`: the report and notes every rule is drawn from, with sources.

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
