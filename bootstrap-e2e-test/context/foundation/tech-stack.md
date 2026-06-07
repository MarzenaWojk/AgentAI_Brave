---
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
---

## Why this stack

This project is a small greenfield web app with login, AI-assisted flashcard generation, and a short three-week after-hours timeline. Django is the recommended Python starter for this product shape because it gives you authentication, persistence, admin tooling, and migrations in one mature framework, which reduces setup work and keeps the first version focused on product behavior instead of assembly. The deployment target stays on Fly, CI runs on GitHub Actions, and merge-to-main auto-deploy keeps the delivery path simple for a solo builder. Django’s bootstrapper confidence is verified, so scaffolding should be smooth.
