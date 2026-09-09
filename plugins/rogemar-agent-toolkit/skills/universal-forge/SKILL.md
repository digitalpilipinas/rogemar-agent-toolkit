---
name: universal-forge
description: Apply shared Forge engineering methods across agent harnesses using their own models, skills, tools, and sub-agents. Use for substantive engineering outside a specialized Codex or Cursor route, or when Universal Forge is explicitly requested.
license: MIT
---
# Universal Forge

Follow the shared [Forge mode and status contract](../workflow-orchestrator/references/forge-mode-status.md) at entry,
resume and dispatch: explicit request → task mode → saved preference; ask once
if none exists. Show role, model, effort, mode and evidence status without
repeated introductions. Setup inspection alone does not require a mode choice
or write preferences; apply the prompt when beginning an execution task.


Use one entry point for the requested engineering outcome. The host agent
selects the relevant methods and capabilities; the user need not enumerate
skills or repeatedly request useful sub-agents. Keep this intent for relevant
follow-up work in the current task, not as a background process.

## Runtime and method selection

Accept `Harness: <name>` or an explicitly selected entry skill. Otherwise use
reliable host context; if uncertain, use this portable route without pretending
to know the host. A declared name selects a method, not proof of tools or models.
An explicit Universal Forge request remains on this route; do not bounce back
to a native entry point. Read [runtime-selection.md](references/runtime-selection.md)
when invoked through Integrated Workflow or when choosing a native adapter.

Use the installed `engineering-playbooks` shared method library: read its
matching playbook and relevant principles, retaining meaningful evidence and
stop conditions. Its 23 playbooks are maintained once for portable execution;
do not copy them into each adapter. Select relevant installed companion skills
for source/history investigation, design alternatives, critique, experiments,
writing, verification and recovery. If the library is missing, report reduced
method coverage and execute a bounded task directly when its acceptance remains
achievable; never claim full PStack coverage from this entry file alone.

`workflow-orchestrator` is the sole dispatch owner. Reuse its active context;
otherwise the main agent applies that role without creating a second coordinator.
`integrated-workflow` retains approved programme and delivery gates. Do not
invoke either entry point recursively or restart the plan when a method returns.

For substantial context or handoffs, use the orchestrator's shared
[context guidance](../workflow-orchestrator/references/context-efficiency.md).
Native adapters retain their own runtime controls; no cache or notification
behavior is implied by the portable method.

## Roles and execution

Read [roles.md](references/roles.md) for shared assignment groups and contracts.
Select only useful roles for the actual task. A role does not mandate an agent;
small or coupled work remains with the parent. Discover relevant native skills,
plugins, MCPs and tools before relying on them. Skill availability and live tool
access are distinct. Do not install, authenticate or launch external providers
merely because native capabilities are missing.

For useful authorized delegation, automatically use the installed
`universal-plan-model-router` to qualify a native model and settings. The
orchestrator applies those settings through the host's actual worker tool and
reconciles the result. If no selector exists, use native defaults only after
confirming compatibility with the selected mode, native pins and explicit limits.
Otherwise keep the dependent work with the main agent and disclose the unmet
routing constraint. Do not invent
APIs, model names, effort flags or capabilities. Missing routing controls do
not prevent direct engineering work. Required independence or device evidence
still remains unmet if unavailable.

Peak, Balanced, Lean and Sprint express routing preferences, not model equivalence
or measured costs. Resolve the mode through the shared contract; recommend Balanced when asking
for an absent choice, without silently selecting it. Do not read
Codex's preference file in another harness or write settings without a request.
Model assignments never reduce acceptance standards or broaden authority.

This portable package is ready for trials. Report host-specific evidence for
actual dispatch, effective model, runtime verification and limitations; do not
claim every harness has been tested. Parent switching requires a supported
native control and observed effect, independent of worker routing.

Inspired by Lauren Tan (poteto)'s PStack/poteto-mode. The shared method library
preserves upstream provenance and MIT notices. This is an independent adaptation.
