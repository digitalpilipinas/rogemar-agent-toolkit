---
name: plan-model-router
description: Resolve Codex task and worker profiles automatically within Forge through workflow-orchestrator. Use Peak, Balanced, Lean, or Sprint role mappings with live Astra, Sol, Terra, and Luna availability, task-fit checks, and explicit dispatch arguments. Also use for standalone plan routing assessments.
---
# Plan Model Router

This is the Codex implementation. Other harnesses use the installed
`universal-plan-model-router`; this script and its model catalogue are not a
portable fallback. Keep existing Codex preferences and resolution unchanged.

Own model and effort resolution. `workflow-orchestrator` alone owns worker
selection, permissions, dispatch, and reconciliation. The user invokes
`codex-forge` or `integrated-workflow`; no separate router invocation is needed.

For every justified Forge worker assignment, follow
[dispatch-contract.md](references/dispatch-contract.md). Read the saved mode,
select a role for the actual task, run `scripts/resolve_profile.py`, then return
its qualified arguments to the orchestrator. A table lookup or a written model
recommendation is not dispatch. Reassess at a mode change or materially different
assignment. Keep simple direct work with the main agent; never spawn merely to
exercise a role or change the model.

The single executable source is `scripts/routing_catalog.json`: four mode pools,
six group defaults, individual role overrides, and conditional role contracts.
Use `--list-modes` and `--role-map` to inspect it. Read
[role-mapping.md](references/role-mapping.md) for role ownership and evidence.
Do not maintain a second model table in the orchestrator or specialist skills.

A named Forge mode supersedes parent model/effort defaults for worker selection.
Without one, retain independent parent ceilings. Separate explicit user limits,
runtime availability, role pins, and authorization always apply. Supported
candidate IDs are `gpt-6-astra`, `gpt-5.6-sol`, `gpt-5.6-terra`, and
`gpt-5.6-luna` only when exposed by the current dispatch tool. Normalize Light
to `low` and Extra High to `xhigh`. The four mode pools exclude Ultra.

Parent routing returns a proposal only. A saved mode cannot change the running
parent or existing workers. Apply a parent change only through a supported
current-task control and verify its effect; otherwise disclose that limitation.

For plan assessments beyond Forge role defaults, read
[routing-profiles.md](references/routing-profiles.md). Qualify the actual scope,
ambiguity, coupling, invariants, acceptance evidence, and rollback. Propose the
lowest sufficient available profile with an escalation trigger; a stronger
model never substitutes for required tests or review. Do not rewrite the plan
or duplicate its delivery gates.
