---
name: forge-automate-me
description: "Use for \\\"automate me\\\", \\\"create/update/refresh my -mode skill\\\", \\\"turn/capture my preferences or working style into a skill\\\", or wanting agents to follow how the user works. Drafts or revises a personal -mode skill via create-skill + unslop, optionally pulling fresh evidence from recent transcripts."
license: MIT
---
# Automate me

## Codex execution contract

Read [the Forge runtime contract](../codex-forge/references/codex-runtime.md). `workflow-orchestrator` owns delegation; `plan-model-router` resolves every worker profile under the manually selected parent model and effort defaults and ceilings. Role preferences are hints, never model IDs or a fanout requirement. Work locally when delegation adds no useful independent work.

Turn the user's working conventions into a personal mode skill. Sequence evidence gathering, Codex `skill-creator`, and `forge-unslop` without replacing their ownership.

1. **Find an existing mode.** Inspect the explicitly relevant project or personal skill location. Preserve its name and scope for an update; do not create duplicates across skill roots. An explicit update request settles the choice.
2. **Gather evidence.** Start with current instructions and the existing skill. Use `forge-recall` only for a verified task/workspace/time window the user has authorized. For broad authorized history, request disjoint read-only extraction slices through the orchestrator. Look for response style, autonomy, delegation, verification, code discipline, and process corrections. Repeated evidence supports durable rules; contradictory one-offs remain questions.
3. **Clarify intent.** Ask a small number of material preference questions using the actual exposed input tool schema. Do not invent multi-select parameters or force unnecessary rounds when the user's preferences are already explicit.
4. **Cluster.** Keep only specific nondefault rules. Reference existing owner skills rather than duplicating their policy. The `codex-forge` skill is an example of granularity, not a template for the user's personality.
5. **Draft.** Follow `skill-creator` for Codex frontmatter, placement and validation. Default to a single personal directory for personal conventions; project rules stay project-local. Use `agents/openai.yaml` with `policy.allow_implicit_invocation: false` when the mode should require explicit invocation. Do not use Cursor-only frontmatter fields. Preserve uncontradicted existing sections and avoid unnecessary rewrites.
6. **Review and apply.** Apply `forge-unslop`, show the concrete draft, and use approval already provided for creation or editing. If broader persistence authority is missing, ask only after the draft is reviewable. Do not save memories implicitly. Commit, push and PR creation are separate authorized actions.
7. **Validate.** Check skill structure and realistic trigger examples; assess subjective voice with the user. Do not add a benchmark harness for a small prose-only preference change. Report saved scope and any fresh-session discovery requirement honestly.
