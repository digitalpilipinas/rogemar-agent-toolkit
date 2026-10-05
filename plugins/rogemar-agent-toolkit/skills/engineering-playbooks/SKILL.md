---
name: engineering-playbooks
description: Apply a reusable engineering playbook for features, bug fixes, investigation, refactoring, performance, experiments, phased delivery, PR stacks, or session recovery across agent harnesses. Select one matching method; keep model and tool routing with the active harness.
license: MIT
---
# Engineering playbooks

Follow the [applicable method contract](../workflow-orchestrator/references/method-contract.md) at entry, every task handoff and delegation,
material changes, resume and acceptance. Select relevant methods automatically; preserve one owner,
required evidence and the original working fallback. Query the routing index only
for the current task; do not load or activate the whole catalog.

At task start/resume, before acceptance and at verified completion, apply the shared
[automatic checkpoints](references/agent-friendly-workflow.md) when a project verification map or learning enrollment exists. Select the actions without waiting for skill names; preserve task authority and required evidence.

When selected by Universal Forge or a native adapter, stay in this method library; do not redirect recursively to another entry. Select one method for the task below and read only its relevant principles. This is the shared engineering playbook layer used by universal-forge. Codex Forge remains the complete Codex-native implementation. Cursor PStack remains the Cursor-native implementation. Claude Forge is the Claude binding over this library. Do not activate both a native entry and this portable owner for the same work.

`workflow-orchestrator` owns delegation and the final reconciliation. `create-plan` owns planning; `code-review-and-quality` owns independent review. Simple changes can stay in the parent. An installed skill is useful without an MCP when its method only requires files, reasoning or an existing CLI.

## Runtime binding

- Before entry selection, Codex normally prefers installed `codex-forge`. Once this portable library is selected, execute its method here without redirecting. The separate Codex implementation and its router remain intact.
- In Cursor, the entry selector prefers cursor-forge when installed, otherwise native PStack. Once this portable library is selected, execute its method here. Keep Cursor's own model names, tools and supervision rules.
- On Claude, the entry selector prefers installed `claude-forge`. Once this portable library is selected, execute its method here. Keep Claude's own model names, tools and permission rules.
- Elsewhere, execute the shared method with the active harness's exposed capabilities. Inherit its current model when no selector exists; never invent a model, effort knob, worker role, browser, watcher or persistent goal. The playbook does not change parent model selection or spend provider credits.
- Optional workers require authorized delegation, disjoint scope and a supported runtime. If those conditions are absent, the parent executes the same method sequentially. Available model and effort controls remain bounded by the owner's policy.
- Publications, installs, monitoring and external actions follow the current task's actual authority. Reuse approval already given for the concrete action. A playbook title does not grant it.

## Choose the method

- [authoring-a-skill](playbooks/authoring-a-skill.md)
- [autonomous-run](playbooks/autonomous-run.md)
- [autopilot-full](playbooks/autopilot-full.md)
- [autopilot-stack](playbooks/autopilot-stack.md)
- [babysit](playbooks/babysit.md)
- [bug-fix](playbooks/bug-fix.md)
- [eval](playbooks/eval.md)
- [feature](playbooks/feature.md)
- [hillclimb](playbooks/hillclimb.md)
- [investigation](playbooks/investigation.md)
- [multi-phase-plan](playbooks/multi-phase-plan.md)
- [opening-a-pr](playbooks/opening-a-pr.md)
- [orchestrate](playbooks/orchestrate.md)
- [pause-safely](playbooks/pause-safely.md)
- [perf-issue](playbooks/perf-issue.md)
- [prototype](playbooks/prototype.md)
- [refactoring](playbooks/refactoring.md)
- [runtime-forensics](playbooks/runtime-forensics.md)
- [session-pickup](playbooks/session-pickup.md)
- [shipping](playbooks/shipping.md)
- [trace-forensics](playbooks/trace-forensics.md)
- [visual-parity](playbooks/visual-parity.md)
- [worktree-cleanup](playbooks/worktree-cleanup.md)

## Additional portable methods

These additions are separate from the 23 retained native playbook mappings:

- [Knowledge maintenance](playbooks/knowledge-maintenance.md): enrolled ingest,
  read-only query, and bounded lint; no second learning store.
- [Focused or comprehensive security review](playbooks/security-audit.md):
  source-grounded findings, bounded coverage, actual execution isolation.
- [External collaboration](playbooks/external-collaboration.md): native provider
  handoff with explicit identity, permissions, full agreed review and recovery.

Select only the method needed. These entries do not install services, start
background tasks, grant writes, or dispatch another coordinator.

## Companion methods

The playbooks use functional names so they do not require a particular harness's slash commands. Source tracing follows callers, data and failure paths with current code evidence. History investigation uses bounded blame/log evidence to explain motivation. Design exploration compares a few consequential alternatives and names a tradeoff; skip it for obvious edits. Assumption critique attacks the falsifiable assumption that would most change the plan. Regression-first verification reproduces the defect before a meaningful fix. Blinded alternatives use isolated equivalent inputs, hidden labels and one judging rubric. Decision logging records hypothesis, attempt, evidence and verdict only for sustained work. Comment review preserves explanations of constraints and removes restatements. Technical writing and plain-language editing lead with behavior, then evidence and limits. Scoped session recovery reads only the supplied task trail and verifies volatile state.

For principles, read the relevant entry from [the principle index](references/principles.md). They are decision aids, not mandatory ceremonies: preserve justified compatibility guards, choose proportionate validation and change only authorized scope.

The [source map](references/source-map.json) records all 23 native playbooks. The portable adaptations replace native tools and optional boards with verified runtime bindings; they retain the outcome, causal evidence, ownership, verification, publication and stop boundaries. Native automation scripts remain with their original packages.
