---
name: forge-principle-redesign-from-first-principles
description: "Apply when integrating a new requirement into an existing design. Redesign as if the requirement had been a foundational assumption from day one, instead of bolting it on."
license: MIT
---
# Redesign From First Principles

## Codex execution contract

Read [the Forge runtime contract](../codex-forge/references/codex-runtime.md) before dispatch or a runtime action. This skill supplies methods and bounded collaboration hints; `workflow-orchestrator` alone selects specialists and subagents. `plan-model-router` resolves task profiles under the manually selected parent defaults and ceilings.



When integrating a change, don't bolt it onto the existing design. Redesign as if the requirement had been there from the start. The result should look like what we would have built if we'd known on day one.

- Read all affected files and understand the current design holistically
- Ask: "if we were writing this from scratch with this new requirement, what would we build?"
- Propagate the change through every reference: types, docs, examples, rationale sections
- Think about the redesign holistically, then deliver it incrementally

This is the method for preserving option value when integrating changes into an existing design.
