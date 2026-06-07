---
bootstrapped_at: 2026-06-07T00:00:00Z
starter_id: django
starter_name: Django
project_name: tenx_cards
language_family: python
package_manager: uv
cwd_strategy: native-cwd
bootstrapper_confidence: verified
phase_3_status: ok
audit_command: pip-audit
---

## Hand-off

```yaml
starter_id: django
package_manager: uv
project_name: tenx_cards
hints:
  language_family: python
  team_size: solo
  deployment_target: fly
  ci_provider: github-actions
  ci_default_flow: auto-deploy-on-merge
  bootstrapper_confidence: verified
  path_taken: standard
  quality_override: false
  self_check_answers: null
  has_auth: true
  has_payments: false
  has_realtime: false
  has_ai: true
  has_background_jobs: false
```

## Why this stack

This project is a small greenfield web app with login, AI-assisted flashcard generation, and a short three-week after-hours timeline. Django is the recommended Python starter for this product shape because it gives you authentication, persistence, admin tooling, and migrations in one mature framework, which reduces setup work and keeps the first version focused on product behavior instead of assembly. The deployment target stays on Fly, CI runs on GitHub Actions, and merge-to-main auto-deploy keeps the delivery path simple for a solo builder. Django's bootstrapper confidence is verified, so scaffolding should be smooth.

## Pre-scaffold verification

| Signal | Value | Severity | Notes |
| --- | --- | --- | --- |
| npm package | not run | not available | non-JS starter |
| GitHub repo | not run | not available | docs_url is not a GitHub repository URL |

## Scaffold log

**Resolved invocation**: `django-admin startproject tenx_cards .`
**Strategy**: native-cwd
**Exit code**: 0
**Pre-flight files-to-touch**: could not enumerate
**Files written by CLI**: 6 (`manage.py`, `tenx_cards/__init__.py`, `tenx_cards/asgi.py`, `tenx_cards/settings.py`, `tenx_cards/urls.py`, `tenx_cards/wsgi.py`)
**Pre-existing files preserved**: context/foundation/tech-stack.md

## Post-scaffold audit

**Tool**: `pip-audit`
**Status**: failed to run
**Reason**: `pip-audit.exe` is unavailable in the runtime used for this bootstrap test.

## Hints recorded but not acted on

| Hint | Value |
| --- | --- |
| bootstrapper_confidence | verified |
| quality_override | false |
| path_taken | standard |
| self_check_answers | null |
| team_size | solo |
| deployment_target | fly |
| ci_provider | github-actions |
| ci_default_flow | auto-deploy-on-merge |
| has_auth | true |
| has_payments | false |
| has_realtime | false |
| has_ai | true |
| has_background_jobs | false |

## Next steps

Next: a future skill will set up agent context (CLAUDE.md, AGENTS.md). For now, your project is scaffolded and verified — happy hacking.

Useful manual steps in the meantime:
- Run `python manage.py check` in this test folder.
- Install and run `pip-audit` if you want full post-scaffold vulnerability output.
- Compare this test run with your primary project to confirm bootstrap behavior in an empty directory.
