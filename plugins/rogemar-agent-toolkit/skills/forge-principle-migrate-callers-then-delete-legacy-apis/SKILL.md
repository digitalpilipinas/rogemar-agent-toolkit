---
name: forge-principle-migrate-callers-then-delete-legacy-apis
description: "Migrate controlled API callers and remove proven dead paths while preserving supported clients, persisted formats and staged compatibility contracts."
license: MIT
---
# Migrate callers, then delete legacy APIs

Trace every known consumer before replacing an API. Migrate controlled callers, check contracts and remove dead paths once evidence shows they are unused. Published APIs, persisted formats, older clients, independently deployed internal consumers and staged rollouts may require deliberate compatibility paths and a deprecation window. Keep those paths until migration evidence and authority permit removal. Do not equate internal visibility with lockstep deployment. Test representative old/new inputs and affected consumers according to risk; report unknown consumers as a gap.

Read [the Forge runtime contract](../codex-forge/references/codex-runtime.md) for authority, delegation, routing and evidence boundaries.
