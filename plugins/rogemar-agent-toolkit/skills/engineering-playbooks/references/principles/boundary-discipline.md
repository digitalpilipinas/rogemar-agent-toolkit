# Boundary discipline

Validate at real trust boundaries and rely on established invariants inside them. Parse untrusted input once into a trustworthy representation; keep authorization, persistence, concurrency, foreign-interface and mutable-state checks where those boundaries actually exist. Internal code is not automatically trustworthy. Remove duplicate validation only after tracing callers, data ownership and failure behavior. Prefer explicit errors to silently converting invalid state into plausible output. Preserve security and compatibility safeguards when their invariant is unproven.

Use the active task authority, orchestrator and harness capability boundaries.
