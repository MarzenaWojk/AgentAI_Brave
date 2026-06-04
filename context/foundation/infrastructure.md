---
project: tenx_cards
researched_at: 2026-05-24
recommended_platform: Railway
runner_up: Render
context_type: mvp
tech_stack:
  language: Python
  framework: Django
  runtime: WSGI/ASGI
---

## Recommendation

**Deploy on Railway.**

For this MVP (solo, short timeline, after-hours, DX-first, external Supabase and OpenRouter), Railway gives the fastest path from local Django app to stable deploy with low operational overhead. The key driver is iteration speed and low setup complexity, not maximum infrastructure control.

## Platform Comparison

| Platform | CLI-first | Managed/Serverless | Agent-readable docs | Stable deploy API | MCP / Integration | Total |
|---|---|---|---|---|---|---|
| Railway | Pass | Pass | Partial | Pass | Partial | 4.0/5 |
| Render | Partial | Pass | Partial | Pass | Partial | 3.5/5 |
| Fly.io | Pass | Partial | Pass | Pass | Partial | 3.5/5 |
| Cloudflare Workers + Pages | Pass | Pass | Pass | Pass | Pass (mixed maturity) | 4.5/5 (reduced fit for Django runtime) |
| Vercel | Pass | Pass | Pass | Pass | Pass | 4.5/5 (runtime mismatch risk for Django) |
| Netlify | Pass | Pass | Partial | Partial | Pass | 3.5/5 (runtime mismatch risk for Django) |

Notes:

- Railway scored highest for practical Django MVP fit under your constraints: no persistent process requirement, DX priority, no platform familiarity bias, external providers accepted.
- Render is close second with similar ease of use and predictable operations, but usually slightly slower day-to-day loop than Railway for small teams.
- Fly.io is operationally strong and CLI-first, but requires more platform-level understanding and is less DX-optimized for a very short MVP runway.
- Cloudflare, Vercel, and Netlify score well on platform criteria in general, but were de-prioritized due to Django runtime fit friction versus container-style Python deployment.

### Shortlisted Platforms

#### 1. Railway (Recommended)

Best balance of speed, simplicity, and low operational burden for Django MVP delivery. Works well when core data and AI services are external.

#### 2. Render

Solid fallback if you prefer a straightforward PaaS model with clear deployment behavior and conservative operations.

#### 3. Fly.io

Strong CLI and operational control, especially if you expect to lean into deeper infra tuning later.

## Anti-Bias Cross-Check: Railway

### Devil's Advocate - Weaknesses

1. Cost can rise faster than expected if AI-triggered traffic grows and app sizing is not tuned early.
2. Platform convenience can hide runtime inefficiencies until load appears.
3. Operational controls are simpler than hyperscalers, which can become limiting as architecture matures.
4. Team may postpone observability discipline because deployment feels easy.

### Pre-Mortem - How This Could Fail

The team chose Railway to move fast and got an MVP online quickly. Early success created a false sense of safety: they delayed setting alerting, cost thresholds, and request-level metrics because the platform looked stable. As AI usage increased, expensive request patterns emerged (large prompts, repeated retries, no output limits), but the issue was diagnosed late because logs were used ad hoc and no budget guardrails were enforced. In parallel, database-heavy endpoints were deployed without profiling, and app instance sizing stayed at defaults. Performance became inconsistent during usage spikes, and the team interpreted symptoms as platform instability rather than app-level inefficiency. A rushed scale-up reduced immediate incidents but increased monthly cost and masked root causes. After several weeks, confidence dropped: feature delivery slowed due to reactive firefighting and unplanned optimization work. The core failure was not Railway itself, but treating MVP convenience as a substitute for basic production discipline in monitoring, cost control, and performance hygiene.

### Unknown Unknowns

- AI usage patterns can dominate total spend long before hosting does.
- Preview and production parity can drift if env vars are managed inconsistently.
- "Works at low traffic" can hide blocking ORM/query paths that only appear under bursty generation flows.
- Retry logic around external AI providers can silently multiply latency and cost.

## Operational Story

- **Preview deploys**: branch-based preview deploys; verify auth callbacks and API base URL per environment before merge.
- **Secrets**: keep runtime secrets in Railway variables, Supabase secrets in Supabase, and never commit any provider key to repo.
- **Rollback**: redeploy previous healthy revision from Railway deployment history; keep DB migrations backward-safe when possible.
- **Approval**: production publish, primary secret rotation, and destructive DB operations remain manual human gates.
- **Logs**: read deploy/runtime logs from Railway dashboard/CLI and correlate with Supabase logs for auth/data issues.

## Risk Register

| Risk | Source | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| Rising AI bill exceeds hosting cost | Research finding | M | H | Add OpenRouter monthly cap, per-request token limits, and weekly usage review. |
| Missing observability in early MVP | Pre-mortem | M | H | Define minimum monitoring baseline before first public release. |
| Performance regressions under burst traffic | Unknown unknowns | M | M | Add lightweight load test and query profiling before each major release. |
| Environment variable drift across environments | Devil's advocate | M | M | Maintain one env checklist and verify on every preview-to-prod promotion. |
| Over-reliance on default instance sizing | Devil's advocate | M | M | Re-evaluate resource sizing after first real usage week and after each major feature. |

## Getting Started

1. Create Railway project and connect repo.
2. Configure required env vars for Django, Supabase, and OpenRouter.
3. Set startup command for Django app and verify health endpoint.
4. Deploy preview, run smoke test for auth and flashcard endpoints.
5. Promote to production with manual approval and first-day log monitoring.

## Budget Snapshot (1 User + Low Traffic)

Estimated monthly cost for current stage:

| Component | Estimate / month | Notes |
|---|---:|---|
| Railway (Django app) | $0-$10 | Small MVP service footprint. |
| Supabase | $0 | Expected to stay on free tier at current usage. |
| OpenRouter | $1-$10 | Depends on model choice and generation frequency. |
| Domain (optional) | $0-$2 | Depends on registrar and annual plan. |
| **Total** | **$1-$22** | Without optional domain often around $1-$20. |

Cost guardrails for MVP:

- Set monthly usage cap/alerts in OpenRouter first (primary cost driver).
- Review Railway usage weekly after first real user activity.
- Re-check Supabase thresholds before enabling heavier AI generation flows.

## Out of Scope

The following were not evaluated in this research:
- Docker image configuration
- CI/CD pipeline setup
- Production-scale architecture (multi-region, HA, DR)
