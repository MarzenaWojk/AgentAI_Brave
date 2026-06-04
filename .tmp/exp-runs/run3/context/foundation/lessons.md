# Lessons Learned

> Append-only register of recurring rules and patterns. Re-read at start by /10x-frame, /10x-research, /10x-plan, /10x-plan-review, /10x-implement, /10x-impl-review.

## Always Set Kill Date For Feature Flags

- **Context**: Any work that introduces or modifies feature flags across backend and frontend, especially rollout planning and post-release cleanup.
- **Problem**: Flags without an expiration point stay in code indefinitely, increasing branching complexity, testing surface, and risk of inconsistent behavior between environments.
- **Rule**: Every feature flag must have an owner and a kill date at creation time. Before the kill date, either remove the flag and dead paths or explicitly renew it with a new date.
- **Applies to**: plan, implement, impl-review
