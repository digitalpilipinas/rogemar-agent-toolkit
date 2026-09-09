---
name: forge-principle-subtract-before-you-add
description: "Apply when sequencing an addition, refactor, or rewrite. Remove dead weight, redundant validators, and stub references first, then build on the simpler base."
license: MIT
---
# Subtract Before You Add

## Codex execution contract

Read [the Forge runtime contract](../codex-forge/references/codex-runtime.md) before dispatch or a runtime action. This skill supplies methods and bounded collaboration hints; `workflow-orchestrator` alone selects specialists and subagents. `plan-model-router` resolves task profiles under the active Forge mode, or parent defaults and ceilings when no mode is selected.



When evolving a system, remove complexity first, then build. Deletion gives you a simpler base, which makes the next addition smaller and less brittle.

**Why:** Adding to a complex system compounds complexity. Removing first cuts the surface area, reveals the essential structure, and usually makes the next design obvious. Default to subtraction.

Make simplification a continual investment. Leave the design slightly simpler and more capable behind the same or smaller surface than you found it.

**The pattern:**
- Sequence removal before construction
- Cut before you polish (get to the minimum before investing in quality)
- Design for observed usage, not speculative edge cases
- No speculative validators, parsers, or guards beyond what the spec demands
- Out-of-spec features drag validators behind them. Persistence, retry-on-startup, and schema migration each need guards to defend their inputs.
- Simplify prompts (remove redundant instructions, excessive templates)
- When a reference has no novel content, delete it rather than leaving a stub
