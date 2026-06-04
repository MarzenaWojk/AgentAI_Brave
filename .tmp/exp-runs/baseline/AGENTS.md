# Repository Guidelines

This repository is a Python Django project scaffolded through 10x-cli lesson flows, with long-lived project context stored under context/ and skill definitions under .github/skills/.

## Hard Rules First

- Never write to context/archive/. Archived items are read-only by convention and should only be produced through archive flow. See @context/archive/README.md.
- Keep change-scoped artifacts under context/changes/<change-id>/ and keep long-lived project docs under context/foundation/. Do not mix them. See @context/changes/README.md and @context/foundation/README.md.
- When updating product direction or stack decisions, edit foundation files in place instead of creating dated copies. Archive only when fully superseded. See @context/foundation/README.md.
- Keep agent/tooling guidance in .github/ and AGENTS.md; do not scatter process rules into Django app modules.

## Project Structure and Modules

- Django entrypoint: @manage.py
- Django settings and core wiring: @tenx_cards/settings.py, @tenx_cards/urls.py, @tenx_cards/asgi.py, @tenx_cards/wsgi.py
- Current DB: SQLite at @db.sqlite3 (configured in @tenx_cards/settings.py)
- Product and stack context: @context/foundation/prd.md, @context/foundation/tech-stack.md, @context/foundation/shape-notes.md
- Skill definitions and references: @.github/skills/

## Build, Test, and Development Commands

Use the workspace virtual environment Python executable for all Django commands:

- .venv/Scripts/python.exe manage.py check
- .venv/Scripts/python.exe manage.py migrate
- .venv/Scripts/python.exe manage.py runserver 0.0.0.0:8000
- .venv/Scripts/python.exe manage.py createsuperuser

## Coding Style and Naming

- Follow Django defaults from the generated project structure already present in @tenx_cards/.
- Keep project package names valid Python identifiers (letters, digits, underscore), not hyphenated names.
- Register URL routes in @tenx_cards/urls.py until feature apps introduce their own urls.py modules.

## Testing and Quality

- No dedicated test config is committed yet (no pytest.ini, no CI workflow files detected).
- Before any commit or handoff, run manage.py check and manage.py migrate to verify project integrity.

## Commit and Pull Request Guidelines

- Git metadata is not available in this workspace (no .git directory detected), so commit-style conventions cannot be inferred yet.
- Before opening the first PR, define one commit format and keep it consistent across the repository history.

## Security and Configuration

- Do not commit real secrets. Replace development defaults in @tenx_cards/settings.py before any production deployment.
- Keep DEBUG=True only for local development; switch to production-safe values as deployment work begins.
