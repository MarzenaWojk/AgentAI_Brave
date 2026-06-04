# Repository Guidelines

Agent onboarding for this repository. Keep this file short and project-specific.

## Hard Rules

- Never write to `context/archive/`. This area is immutable. See `@context/archive/README.md`.
- Keep task artifacts in `context/changes/<change-id>/` and long-lived docs in `context/foundation/`. Do not mix these scopes.
- Update foundation docs in place. Do not create dated duplicates in `context/foundation/`.
- Keep agent/process instructions only in `AGENTS.md` and `.github/` instruction files.
- Use `.venv/Scripts/python.exe` for all Django commands in this workspace.

## Project Map

- Django entrypoint: `@manage.py`
- Core project wiring: `@tenx_cards/settings.py`, `@tenx_cards/urls.py`, `@tenx_cards/asgi.py`, `@tenx_cards/wsgi.py`
- Cards app: `@cards/models.py`, `@cards/views.py`, `@cards/urls.py`, `@cards/tests.py`
- Product context: `@context/foundation/prd.md`, `@context/foundation/tech-stack.md`, `@context/foundation/shape-notes.md`
- Lessons register: `@context/foundation/lessons.md`

## Implementation Conventions

- Keep app routes in the app module (`cards/urls.py`) and include them in `tenx_cards/urls.py`.
- Keep Python package/module names as valid identifiers with underscores (no hyphens).
- Extend API behavior in `cards/views.py` and cover it with tests in `cards/tests.py` in the same change.

## Domain Decision Rules

- Do not invent enum values, statuses, or allowed literals. Use the source of truth from `context/foundation/prd.md` (or existing model/constants in code). If no source defines them, ask first.
- When business/domain requirements are underspecified, stop and ask one focused clarification question before implementation. Do not assume domain defaults.

## Validation Commands

Run before handoff:

- `.venv/Scripts/python.exe manage.py check`
- `.venv/Scripts/python.exe manage.py migrate`
- `.venv/Scripts/python.exe manage.py test cards`

Useful during implementation:

- `.venv/Scripts/python.exe manage.py makemigrations`
- `.venv/Scripts/python.exe manage.py runserver 0.0.0.0:8000`
- `.venv/Scripts/python.exe manage.py createsuperuser`

## Onboarding Validation Rule

After changing onboarding instructions, validate them in a fresh agent session on one real implementation task. Accept the onboarding change only if the agent follows these rules without extra clarifications.
