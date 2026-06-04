---
bootstrapped_at: 2026-05-24T08:50:22Z
starter_id: django
starter_name: Django
project_name: 10x-cards
language_family: python
package_manager: uv
cwd_strategy: native-cwd
bootstrapper_confidence: verified
phase_3_status: failed
audit_command: pip-audit
---

## Hand-off

`yaml
starter_id: django
package_manager: uv
project_name: 10x-cards
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
`

## Why this stack

This project is a small greenfield web app with login, AI-assisted flashcard generation, and a short three-week after-hours timeline. Django is the recommended Python starter for this product shape because it gives you authentication, persistence, admin tooling, and migrations in one mature framework, which reduces setup work and keeps the first version focused on product behavior instead of assembly. The deployment target stays on Fly, CI runs on GitHub Actions, and merge-to-main auto-deploy keeps the delivery path simple for a solo builder. Django's bootstrapper confidence is verified, so scaffolding should be smooth.

## Pre-scaffold verification

| Signal      | Value   | Severity      | Notes                                      |
| ----------- | ------- | ------------- | ------------------------------------------ |
| npm package | not run | not available | non-JS starter                              |
| GitHub repo | not run | not available | docs_url is not a GitHub repository URL     |

## Scaffold log

**Resolved invocation**: django-admin startproject . .
**Strategy**: native-cwd
**Exit code**: 1
**Stderr (last lines)**:

`	ext
& : The term 'django-admin' is not recognized as the name of a cmdlet, function, script file, or operable program.
`

## Post-scaffold audit

**Audit not run**: scaffold halted at Step 2; no project to audit.

## Hints recorded but not acted on

| Hint                    | Value                |
| ----------------------- | -------------------- |
| bootstrapper_confidence | verified             |
| quality_override        | false                |
| path_taken              | standard             |
| self_check_answers      | null                 |
| team_size               | solo                 |
| deployment_target       | fly                  |
| ci_provider             | github-actions       |
| ci_default_flow         | auto-deploy-on-merge |
| has_auth                | true                 |
| has_payments            | false                |
| has_realtime            | false                |
| has_ai                  | true                 |
| has_background_jobs     | false                |

## Next steps

Scaffold failed because django-admin is unavailable in the current environment.

Retry path:
- Install Django in your active Python environment.
- Re-run /10x-bootstrapper @context/foundation/tech-stack.md.
