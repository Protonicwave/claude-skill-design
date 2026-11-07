# claude-skill-design

Claude Code skills for designing and building web interfaces.

## Development

Requires Python 3.12 or later and [uv](https://docs.astral.sh/uv/).

```sh
uv sync
uv run pytest
uv run ruff check . && uv run ruff format --check .
uv run mypy
uv run vulture skills tests --min-confidence 80
```
