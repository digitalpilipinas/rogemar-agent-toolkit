---
name: plan-model-router
description: Resolve Codex task and worker profiles automatically within Forge through workflow-orchestrator. Use Default, Peak, Balanced, Lean, or Economy role mappings with exact-generation model availability, task-fit checks, and explicit dispatch arguments. Also use for standalone plan routing assessments.
---
# Plan Model Router

Read `references/forge-mode-status.md` from the installed `workflow-orchestrator`
skill and follow that shared contract at entry,
resume and dispatch: explicit request → task mode → saved preference; ask once
if none exists. Show role, model, effort, mode and evidence status without
repeated introductions. Setup inspection alone does not require a mode choice
or write preferences; apply the prompt when beginning an execution task.


This is the Codex implementation. Other harnesses use the installed
`universal-plan-model-router`; this script and its model catalogue are not a
portable fallback. Do not import Codex profiles into another harness.

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

The executable source is `scripts/routing_catalog.json`: five policies, parent
targets, exact-generation model tiers and supported efforts, group defaults, role overrides and verified exceptions. Use `--list-modes`
and `--role-map` to inspect it. `references/role-evidence.json` records all 225
role/mode decisions, historical findings and focused validation. Read
[role-mapping.md](references/role-mapping.md) for contracts and evidence limits.

Normal assignments obey both parent model-tier and reasoning ceilings, using
the stricter mode target and accepted actual parent. Qualified routine work,
including implementation, may use lower families and reasoning. Consequential
judgment retains the actual parent family; lower reasoning still needs validation.
Default preserves one exact user-selected profile; no-mode
retains the legacy parent ceilings. Explicit limits and actual availability
always apply. Never rename qualifications or explicit preferences across model generations;
retired preset profiles remain available only where policy and native support permit them.
Normalize Light to `low` and Extra High to `xhigh`.

Only an exact verified `hillclimb` or `hardest-tasks` exception can exceed either
model family or reasoning ceilings, including Lean and Economy. The request must cite its evidence and explain the
difficult assignment. A provisional or failed record never authorizes dispatch.
A parent fallback is ordinary execution, not a replacement for independent review.
Normal hard work inherits the actual parent within mode limits. Rank qualified
routine candidates by account-credit estimates, duration, then raw tokens; historical
worker-only usage is a proxy and excludes full coordination/retry/review costs.
Pass `implementation: true` for code-producing assignments and `consequential: true`
for security or architectural judgment within any role. Paired explanatory answers
cannot qualify implementation without the matching executable coding checks.
See [validation-v6.md](references/validation-v6.md) for the current comparison,
fresh qualification and limitations. Return the qualification's actual scope:
a readiness answer is not runtime evidence, and a SQLite pass is not a UI test.
Alternate implementation and exact exceptions require the matching
`evidence_contract`; the dispatcher derives this from the actual work and proof.

Ordinary Forge Scout/Judge assignments use unpinned read-only equivalents.
`goalbuddy_required: true` requires observed native pins and actual GoalBuddy
contracts; an incompatible mode reports the missing gate without substituting
an ordinary reviewer or repeatedly attempting the same rejected spawn.

Parent routing returns a proposal only. A saved mode cannot change the running
parent or existing workers. Apply a parent change only through a supported
current-task control and verify its effect; otherwise disclose that limitation.

For plan assessments beyond Forge role defaults, read
[routing-profiles.md](references/routing-profiles.md). Qualify the actual scope,
ambiguity, coupling, invariants, acceptance evidence, and rollback. Propose the
lowest sufficient available profile with an escalation trigger; a stronger
model never substitutes for required tests or review. Do not rewrite the plan
or duplicate its delivery gates.
