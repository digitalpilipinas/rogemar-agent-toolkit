---
name: forge-how
description: "Use for \\\"how does X work\\\", code walkthroughs before changing something, and placement / ownership / layering questions (\\\"where should this live\\\", \\\"which package owns this\\\", \\\"is this the right layer\\\"). Explains subsystem architecture, runtime flow, onboarding mental models. Can critique architecture. Use why for motivation."
license: MIT
---
# How

## Codex execution contract

Read [the Forge runtime contract](../codex-forge/references/codex-runtime.md). `workflow-orchestrator` owns delegation; `plan-model-router` resolves every worker profile under the active Forge mode, or parent defaults and ceilings when no mode is selected. Role preferences are hints, never model IDs or a fanout requirement. Work locally when delegation adds no useful independent work.

Explain how a subsystem works from current source. Use `forge-why` for the forces that led to its design.

## Explain

1. Identify the question: subsystem, feature flow, ownership, placement, layering, or runtime trace. State a reasonable scope; clarify only a material ambiguity.
2. Ground in repository instructions, current code and tests. Use a fresh project map when applicable, then targeted file and symbol searches. Trace from input or trigger to output or effect, including data, configuration, state ownership and failure paths. A filename is not evidence of behavior.
3. For a narrow question, the parent explores and explains directly using `references/explainer-prompt.md`. For a broad question, ask the orchestrator for independent read-only slices such as data model, request path, and configuration. Use the `how-explorer` role hint and `references/explorer-prompt.md`; choose only useful slices within concurrency limits. Workers return components, traced flow, files read, surprises, and gaps.
4. Synthesize locally, or request a bounded `how-explainer` only when there is useful independent work. Reconcile overlapping findings. Use concrete names and code citations to build a mental model rather than annotate every source line. Match depth to the reader and state untraced links.

## Critique (when requested or material to the design)

Explain first. Ask the orchestrator for independent critiques using the `how-critics` preference pool and `references/critic-prompt.md` when available. The number of configured models does not dictate panel size. Use read-only scopes and distinct questions; the parent can supply another perspective when workers are unavailable.

Compare findings against actual source and caller contracts. Consolidate duplicates, discard unsupported claims with reasons, and prioritize concrete architectural constraints and tradeoffs. Do not edit code during explanation or critique without implementation authority. Return the explanation, evidenced issues, uncertainty, and suggested next investigation.
