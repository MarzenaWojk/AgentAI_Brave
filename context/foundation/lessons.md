# Lessons Learned

> Append-only register of recurring rules and patterns. Re-read at start by /10x-frame, /10x-research, /10x-plan, /10x-plan-review, /10x-implement, /10x-impl-review.

## Always Set Kill Date For Feature Flags

- **Context**: Any work that introduces or modifies feature flags across backend and frontend, especially rollout planning and post-release cleanup.
- **Problem**: Flags without an expiration point stay in code indefinitely, increasing branching complexity, testing surface, and risk of inconsistent behavior between environments.
- **Rule**: Every feature flag must have an owner and a kill date at creation time. Before the kill date, either remove the flag and dead paths or explicitly renew it with a new date.
- **Applies to**: plan, implement, impl-review

## Validate Onboarding In A Fresh Session

- **Context**: After creating or updating agent onboarding rules (for example AGENTS.md, CLAUDE.md, or tool-specific instruction files) and before considering them done.
- **Problem**: Rule quality is overestimated when judged only by reading; hidden ambiguities appear only when the agent has to make real decisions on real code without prior conversational context.
- **Rule**: Always run at least one real implementation task in a fresh agent session to validate onboarding instructions. Treat the onboarding as accepted only if the agent makes correct decisions without additional clarifications.
- **Applies to**: all

## Keep 405 Tests On Unsupported Methods

- **Rule**: When adding support for a new HTTP method on an endpoint, update METHOD_NOT_ALLOWED tests to call a still-unsupported method (for example PUT) so 405 assertions remain valid.

## Keep METHOD_NOT_ALLOWED Tests On Unsupported Methods

- **Context**: Przy każdej zmianie obsługiwanych metod HTTP w endpointach w views.py i testach API w tests.py.
- **Problem**: Po dodaniu nowej metody endpointu test METHOD_NOT_ALLOWED dalej sprawdzał metodę, która już stała się dozwolona, więc asercja 405 dawała fałszywy wynik.
- **Rule**: Po dodaniu nowej dozwolonej metody HTTP zawsze aktualizuj test METHOD_NOT_ALLOWED, aby używał nadal nieobsługiwanej metody (np. PUT), zanim zatwierdzisz zmianę.
- **Applies to**: implement, impl-review
