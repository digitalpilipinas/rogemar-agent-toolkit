---
name: forge-principle-build-the-lever
description: "Use a repeatable tool when repeated operations, observations or a meaningful verification gap justify it. Reuse existing instruments; keep a direct route for simple work."
license: MIT
---
# Build the lever

Use a repeatable instrument when the task needs repeated observations or operations. First inspect existing tools and checks. Build a small focused script only when it saves real repeated work or preserves evidence the next operator needs. Define inputs, outputs, failure states, side effects and a check of the instrument itself. Prefer read-only diagnostics and explicit mutations. A helper must not install dependencies or restart services silently. Keep the instrument proportionate; a reversible known-file edit does not need a new harness. Commit or publish it only within explicit authority.

Read [the Forge runtime contract](../codex-forge/references/codex-runtime.md) for authority, delegation, routing and evidence boundaries.
