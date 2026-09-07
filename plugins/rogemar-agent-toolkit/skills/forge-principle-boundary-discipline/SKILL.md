---
name: forge-principle-boundary-discipline
description: "Apply when wiring validation, error handling, or framework adapters. Concentrate guards at system boundaries (CLI, config, network, external APIs); trust internal types and keep business logic in pure functions."
license: MIT
---
# Boundary discipline

Validate at real trust boundaries and rely on established invariants inside them. Parse untrusted input once into a trustworthy representation; keep authorization, persistence, concurrency, foreign-interface and mutable-state checks where those boundaries actually exist. Internal code is not automatically trustworthy. Remove duplicate validation only after tracing callers, data ownership and failure behavior. Prefer explicit errors to silently converting invalid state into plausible output. Preserve security and compatibility safeguards when their invariant is unproven.

Read [the Forge runtime contract](../codex-forge/references/codex-runtime.md) for authority, delegation, routing and evidence boundaries.
