---
name: universal-plan-model-router
description: Qualify task and role profiles using the current harness's native models and controls. Use internally with Universal Forge or as Cursor Forge fallback, or for portable plan routing; keep native defaults when model selection is unavailable.
---
# Universal Plan Model Router

Cursor Forge first uses `cursor-forge-setup`. Activate this route there only
for unavailable native adapter/mappings, carrying explicit limits and reporting
the fallback. Never bypass a primary rejection or permission boundary.

Resolve execution profiles; do not dispatch, create agents, rewrite the plan,
or serve as a fallback engineering workflow. `workflow-orchestrator` owns
actual dispatch and reconciliation. The user need not invoke this separately.
Codex's existing `plan-model-router` remains the default Codex implementation;
do not import its model catalogue into this portable path.

## Qualify the assignment

1. Read the selected mode, role, task scope, acceptance evidence, owner limits,
   and any explicit host-local preferences. Unknown task details that determine
   safety or sufficiency require bounded investigation before implementation.
2. Discover model IDs and settings actually accepted by the native worker tool.
   Separately inspect current parent identity, native role pins, tool access,
   permissions, independent-context support and any current-parent control.
   Prefer the live tool schema/catalogue; configured or advertised models alone
   do not prove availability. Do not probe a paid provider or launch another CLI
   without task authorization.
3. Choose a sufficient native profile using the mode below and a concrete
   task-fit reason. Do not impose a cross-provider ranking or translate effort
   labels mechanically. A model's family name or high effort is not proof of
   capability, cost, or speed. Reuse verified host-specific mappings if present;
   otherwise state that the task-fit choice is a heuristic.
4. Check native pins and explicit user ceilings. Requalify the exact effective
   profile when pins change a proposal; never discard overrides silently.
   A portable mode does not independently authorize exceeding owner limits.
5. Return the role, mode, native profile/settings, reason, evidence requirements,
   exact supported dispatch arguments and source of availability to the existing
   orchestrator. It copies the qualified arguments into the host's actual tool,
   with a bounded assignment. Do not call a Codex or Cursor tool by analogy.
6. Record proposed, requested, accepted and runtime-observed settings separately.
   A worker's self-report is not authoritative runtime identity. Missing metadata
   is Unverified; it does not erase valid task evidence. Reassess on task or mode
   changes. Reuse a worker only if its profile and contract still fit.

## Portable modes

| Mode | Selection preference |
| --- | --- |
| Peak | Strongest suitable permitted profiles for demanding reasoning |
| Balanced | Strong judgment where needed; efficient bounded execution elsewhere |
| Lean | Lower-cost suitable profiles where supported by evidence; selective escalation |
| Sprint | Fast narrow assignments and minimal coordination overhead |

These preferences do not define prices, model equivalence, fan-out counts or
universal effort levels. Acceptance requirements remain unchanged. Escalation
must remain within mode intent and explicit limits; if insufficient, explain
and recommend a mode change rather than silently claiming success.

## Partial capabilities

- Workers available, model selector absent: use native inheritance/defaults,
  label model selection uncontrolled, and still assign useful authorized roles.
- Catalogue incomplete: use a confirmed supported profile or native default;
  do not invent IDs. If an explicit restriction cannot be established, keep the
  dependent assignment blocked while continuing independent allowed work.
- Workers absent: main executes sequentially. Required independent review stays
  unmet, not passed. Missing optional routing does not block all engineering.
- Parent switch available: propose a justified change at a task boundary and
  use only its supported control within owner authority; verify parent identity.
  A saved preference, selected worker or next-session default is not a live switch.
- No parent control: retain the parent and disclose the unapplied suggestion.

Use the existing plan or receipt; no extra persistent board is needed. Never
claim an actual switch merely because the profile was resolved. When no router
script is available, these steps are a reasoning procedure performed by the host;
they are not a background routing service or executable enforcement layer.
