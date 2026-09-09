---
name: forge-principle-exhaust-the-design-space
description: "Apply when facing a novel UI interaction or architectural decision with no precedent in the codebase. Build 2-3 competing prototypes and compare side by side before committing."
license: MIT
---
# Exhaust the relevant design space

For a consequential or uncertain design, explore structurally distinct alternatives before locking in the first plausible shape. Compare caller experience, invariants, failure modes, migration cost and implementation complexity. Scale the number and depth of alternatives to uncertainty; two grounded sketches may be enough. Read-only sketches are valid in planning mode. Request bounded independent candidates through workflow-orchestrator only when they add useful perspectives, with profiles resolved under the active routing policy. Record rejected alternatives and why. Stop exploring when further alternatives would not change a supported decision.

Read [the Forge runtime contract](../codex-forge/references/codex-runtime.md) for authority, delegation, routing and evidence boundaries.
