# Repository Guidelines

## Project Structure & Module Organization
The runtime code lives under `src/`, structured by responsibility: `src/core/` holds the Markdown-to-HTML pipeline (`HTMLConverter`, stats tracking); `src/processors/` wraps image embedding and Mermaid transforms; `src/themes/` defines HTML skinning; `src/utils/` houses CLI formatting, scanning, and progress helpers. Entry points include `md2html.py` for script-style usage and `src/cli.py` for module invocation. Docs and analysis artifacts stay at the repository root, while `legacy/` keeps reference reports and should remain read-only.

## Build, Test, and Development Commands
- `python -m venv .venv && source .venv/bin/activate` creates an isolated environment (required for CLI extras like `markdown`).
- `python -m pip install markdown Pillow` installs the minimal runtime stack; add `pytest black flake8 isort mypy` for full tooling.
- `python md2html.py docs/report.md -o dist/` converts Markdown files; omit arguments to enter the interactive assistant.
- `python -m src.cli --list-themes` lists the available layout options for quick validation.

## Coding Style & Naming Conventions
Write Python 3.8+ code with 4-space indents, module-level docstrings, and exhaustive type hints (mirroring `src/core/converter.py`). Use `snake_case` for functions, `PascalCase` for classes, and keep CLI flags lowercase with hyphens. Format with `black --line-length 88` and `isort --profile black`; run `flake8 src` and `mypy src` before sending a change.

## Testing Guidelines
Target `pytest` with tests under `tests/`, mirroring the fixtures layout suggested in `QUICK_START_GUIDE.md`. Name files `test_<module>.py` and prefer descriptive parametrized cases. Aim for coverage of the conversion pipeline, processors, and theme rendering; use `pytest --cov=src --cov-report=term-missing` to verify. When touching I/O, rely on temporary directories or `tmp_path` fixtures.

## Commit & Pull Request Guidelines
Adopt Conventional Commit prefixes (`feat`, `fix`, `docs`, `refactor`, `chore`) followed by an imperative summary, e.g., `feat: add professional theme toggles`. Group related changes per commit and ensure PRs explain impact, include sample CLI output or screenshots for theme updates, and link any tracking issue. Request review when tests and linters pass and the CLI help text stays accurate.

## Security & Configuration Tips
Avoid checking sensitive PDFs or HTML exports; keep generated reports under `dist/` and `.gitignore` them if added. When processing external Markdown, run in virtualenvs without elevated permissions to prevent malicious asset inclusion.
