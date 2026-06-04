---
project: tenx_cards
researched_at: 2026-05-24
recommended_platform: Cloudflare Workers + Pages
runner_up: Railway
context_type: mvp
tech_stack:
  language: Python
  framework: Django
  runtime: ASGI/WSGI via compatibility adapter on Cloudflare
---

## Recommendation (Alternative)

**Deploy on Cloudflare Workers + Pages despite fit risks for Django.**

This is a conscious "Cloudflare anyway" variant for MVP constraints: very low expected traffic (currently 1 user), global edge distribution potential, and low platform cost floor. The trade-off is higher integration complexity for Django than on container-first platforms like Railway/Render/Fly.

## Why This Is Not The Default

Cloudflare is strongest for edge-native JavaScript/TypeScript stacks. For Django, deployment usually needs an adapter/runtime bridge and stricter checks for framework compatibility. That increases setup risk in a short MVP timeline.

## Entry Conditions (Go / No-Go)

Use this variant only if all conditions below are true:

1. You accept a longer initial setup than Railway/Render.
2. You freeze MVP scope during deployment setup week (no parallel feature churn).
3. You keep Supabase and OpenRouter external (already chosen) to avoid extra platform coupling.
4. You define a rollback target (Railway) before first production deploy.
5. You agree on a hard stop rule: if Cloudflare setup exceeds 1-2 focused days without a stable deploy, switch to runner-up.

## Operational Risks

- **Framework fit risk**: Django runtime compatibility can require non-trivial adapter changes.
- **Debugging risk**: Error investigation may involve adapter/runtime boundaries, not only app code.
- **Lock-in risk**: Cloudflare-specific deployment conventions can make later moves slower.
- **Team DX risk**: For non-edge-first teams, day-to-day maintenance can be less intuitive.
- **Hidden complexity risk**: Early costs may be low, but engineering time can dominate.

## Mitigations

- Start with the smallest deployable Django slice (health endpoint + one API route).
- Keep all external integrations behind app-level service wrappers.
- Use staged validation gates: local pass -> preview pass -> production pass.
- Write rollback steps before first production cutover.
- Timebox platform-specific debugging.

## Cost Snapshot (Current scale: 1 user)

- Cloudflare hosting/runtime: effectively near zero at MVP scale.
- Supabase: likely free tier.
- OpenRouter: usage-based; likely minimal at current traffic.
- Main cost driver right now is engineering time, not infra billing.

## Exit Criteria (When to abandon this variant)

Switch to Railway if any of these happens:

1. Stable deploy is not achieved in the timebox.
2. Runtime limitations block core Django endpoints.
3. Debugging overhead repeatedly slows feature delivery.
4. Team confidence in operations remains low after first successful deploy.

## First Steps

1. Prepare a minimal deploy branch with one read-only API endpoint.
2. Validate Cloudflare-compatible Django adapter workflow for the exact pinned stack.
3. Deploy preview and verify logs, env vars, and error handling shape.
4. Document rollback to Railway in one page before production publish.
5. Run first production release behind a manual approval gate.
