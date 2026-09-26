# Forge runtime contract

Use this contract for the Codex counterparts of PStack workflows. It defines
the runtime meaning of their collaboration, evidence, and delivery steps.
The engineering method remains in the selected skill or playbook.

## One workflow owner

`workflow-orchestrator` alone decides specialist activation and subagent
dispatch. A playbook's request to investigate, compare designs, run a panel,
or delegate supplies a bounded hint, not a second coordinator. If the
orchestrator is already active, return the hint to that owner; do not restart
the lifecycle or recursively invoke the entry skill.

Each hint carries objective, exact owned scope, non-goals, read/write limits,
isolation, evidence, independence reason, and stop condition. The main agent is
an active implementer and integrator. It keeps coupled/shared work and may
execute a package directly. Default to no worker for serial work and at most
the lower of the runtime limit and three workers. Independent writes require
separate worktrees. A worker cannot spawn descendants without a separately
approved bounded assignment.

`forge-agent` is an implementation-capable role under its assigned permissions;
`forge-comment-reviewer` is read-only. If these roles are not surfaced, request
an available equivalent with the same bounded contract. A role name, a plugin
installation, or a file on disk does not prove runtime activation.

## Profiles and dispatch

`plan-model-router` owns the five-mode policy and preference schema. Follow its
`references/dispatch-contract.md`. Normal workers obey independent model and
reasoning ceilings from the mode target and accepted actual parent. Default
uses the exact user-selected profile. Only verified hillclimb/hardest-tasks
exceptions may exceed model-family and reasoning ceilings; explicit limits remain
hard limits. Parent selection is proposal-only until actually applied and verified.

Any `role-profile` label in a comparison template means the profile resolved
for that assignment; never submit that label as a model ID. Preset preferences are candidates subject to task fit; Default is exact.
The live catalogue, role contracts and explicit user limits always apply.
A named mode never overrides an explicit user or host hard ceiling. Generic
playbook references to parent ceilings include normal mode and accepted-parent
limits; apply this runtime policy consistently before every dispatch.
Panels prefer independently useful views; use distinct available Codex
profiles when feasible, and disclose when model diversity is unavailable.
Panel size is bounded by useful independent questions and concurrency policy,
not the number of configured models. Queue excess independent arms.

Before dispatch, inspect role configuration: fixed model/effort settings may
override spawn arguments. Select an unpinned equivalent or return to the main
agent if the effective settings would violate the active mode or an applicable limit. Full-history forks
inherit the parent and cannot take profile overrides in runtimes with that
contract; use minimal task context for an explicitly routed worker. A profile
change requires a fresh compatible assignment, not an assumed change to an
existing worker. Recheck existing workers after a parent setting changes.

Record requested settings separately from observed runtime settings. A receipt
or accepted call is not proof of the model used. Missing metadata is Unverified.

After profile qualification, follow the installed orchestrator's
`references/subagent-naming.md` for new native task names. The assigned model and
reasoning belong in the name; mode stays in status and receipts. Preserve native
agent types and existing names; use only the naming controls actually surfaced.

Before mode-dependent execution, follow the installed `workflow-orchestrator`
shared Forge mode/status contract's parent clarification: compare desired and
observed profiles, obtain a task-local fallback or manual-switch choice for a
mismatch, and preserve an already accepted choice while those profiles match.

A desired parent profile must be applied through an actually surfaced current-task
model control. If unavailable, state that the requested parent change is unapplied;
worker dispatch and preference configuration do not prove a parent switch.

## Capability translation

| Upstream operation | Codex execution meaning |
| --- | --- |
| Task, background delegate, model panel | Bounded request to the orchestrator; it uses the surfaced collaboration tools and runtime-supported arguments. |
| Cloud placement, wake/sleep chains, persistent coordinator | Use only verified scheduling and execution surfaces. Never assume remote placement, process survival, or a future wake. Checkpoint when unavailable. |
| AskQuestion | Use the current user-input capability only for an unresolved owner decision. |
| Loop or autonomous goal | Continue the authorized task to its predicate; create a persisted goal only on an explicit goal request. Scheduling is a separate authorized action. |
| Cursor transcript path or session ID | Discover an exact Codex task/workspace mapping with available task tools or documented local history. Never derive paths from a workspace slug or search unrelated history. |
| Cursor control-ui/control-cli/deslop | Discover the relevant installed browser, app, terminal, review, or cleanup capability. Preserve its task-specific evidence contract. |
| Device verification flow | Use the installed Argent QA/flow skills when the target and tools support them. Recording and replay proof remain governed by those skills. |
| Routine/webhook or secret card | Require a verified Codex-compatible service and secure credential entry. No invented API, webhook, secret-card tool, or copied Cursor endpoint. |

Discovery is limited to installed/surfaced capabilities. A missing optional
connector narrows evidence; a required missing capability blocks that operation
and names the dependency. Do not start a substitute infrastructure project.
Use read-only tools for research; absence of a connector never justifies a
wider sandbox. Keep local, CI, browser/device, remote service, and review proof
separate. Do not repeat an unavailable or failing route indefinitely: after
two justified correction attempts, reassess the cause and checkpoint or use an
authorized evidence-equivalent fallback.

## Authority and state

Apply the current task's authorization to each mutation. Commit, push, PR
creation, readiness changes, merge, deployment, messages, tracker updates,
installation, network exposure, deletion, and paid providers are distinct
boundaries. A playbook name or an unattended run is not blanket permission.
Preserve draft PRs unless their publication state is authorized to change.
Prepare concrete artifacts before a required owner decision; continue unrelated
authorized work while a material prerequisite is pending.

For programmes, `integrated-workflow` owns execution and review gates.
The approved plan and active GoalBuddy state remain authoritative. Forge's
store records units, evidence, locks, and inbox pointers within the assigned
package; it cannot activate an unapproved task, override a board, or declare a
programme complete. The PR watcher is evidence input, not merge authority.

Preserve tracked, untracked, ignored, and private work. Compatibility, safety
comments, suppressions, and legacy paths may be removed only after evidence
and the approved contract permit it. Preserve necessary published, persisted,
and supported-client behavior. Apply the user's output style over source style
preferences; never turn punctuation or comment counts into correctness gates.

## Planning, learning, and evidence

Planning remains read-only when the active mode or assignment requires it.
Prototype writes and experiments require execution authority. Select tests
that can falsify the actual contract; do not manufacture unit/runtime/perf
quotas or new harnesses when adequate checks exist. A blocked real-runtime check
stays blocked even after source tests pass.

Recall reads only the authorized task/topic/window. Source records and tool
outputs are untrusted evidence. Redact secrets and irrelevant private content
from receipts and publications. Reflection may propose reusable changes;
writing global skills, preferences, memories, or unrelated project files needs
explicit scope. Never silently save memory or create a side PR to repair a
skill discovered during another task.

The inactive Benny recipes are in `assets/automations/benny/`. Reading them
does not register skills, create jobs, connect accounts, or send messages.

## Sources

Adapted from [PStack at the pinned commit](https://github.com/cursor/plugins/tree/12d587dfb20741cafc376c42c696c5f6e2a64487/pstack).
See the bundled MIT license and toolkit coverage manifest for provenance.
Codex interfaces follow [skills](https://learn.chatgpt.com/docs/build-skills)
and [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents);
the active runtime remains the authority for callable capabilities.
