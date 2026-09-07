# Orchestrate

Use for a programme that benefits from bounded parallel work. `workflow-orchestrator` is the sole delegation owner; `integrated-workflow` retains approved-programme authority. Forge supplies briefs, drain discipline and optional local evidence tools.

## Frame and choose ownership

Define the completion oracle, scope, dependencies, current slice, acceptance and stop conditions. The main agent can own implementation directly. Parallelize independent research or reviews; parallel repository writers require isolated worktrees and reconciliation. Cap concurrency at the lower of the runtime limit and three by default. Avoid a coordinator layer when the main agent can drain the work itself. No worker creates descendants without an explicit bounded exception from the orchestrator.

## Brief contract

Every assignment names goal, owner, allowed files or symbols, exclusions, acceptance, non-goals, upstream inputs, verification command, stop condition, output location, and concise receipt format. Include relevant standing constraints or a readable authoritative reference, not a full transcript. Tell writers they share the codebase, must preserve unrelated edits, and must report conflicts. The router resolves the role hint at dispatch under the active routing policy, including saved role pins. A changed profile needs a fresh bounded assignment.

## Optional local store

Use an existing approved plan or GoalBuddy state as the source of truth. `scripts/orch/orch.ts` is an opt-in local evidence store: units, agent pointers, reports, frontier and head-keyed verdict ledger. It never dispatches, wakes, grants authority or marks programme tasks complete. Do not initialize a second board for routine work. If its scope, task ID, head or state disagrees with the authoritative plan, stop dependent dispatch, reconcile the difference and record the disposition. Never overwrite the authoritative record with stale store state.

When needed, run `orch --help`, initialize an explicit private store location, and capture only task evidence. Commands must not silently install dependencies. Frontier discovery uses verified Git/GitHub branch and PR relationships; ambiguous topology is blocked, never guessed from PR number. Explicit pins are assertions checked against discovered order.

## Execute and drain

1. Pilot one useful package through implementation and verification before scaling an unfamiliar workflow.
2. Request a rolling window of independent assignments through the orchestrator and do useful local work while they run.
3. At each drain, read actual artifacts, head identity and checks. Classify each receipt as verified, needs verification, failed, blocked, abandoned or absorbed by the parent. Track missing coverage explicitly.
4. Reconcile outputs and conflicts before advancing dependencies. Current head and base invalidate stale evidence; matching patch IDs alone cannot prove the new integration context.
5. Update only concise evidence needed to resume. Sample brief quality if recurring errors suggest a shared instruction problem.
6. At major boundaries audit the actual diff against the completion oracle. Adjust decomposition or recommend a user-applied parent change only when evidence warrants it.

## Recovery and liveness

Use exposed status/read tools; resuming an idle worker can start work and is not a read-only probe. Do not infer liveness from transcript modification times. Cloud persistence, nested-agent depth, restart recovery and background wakeups are capability-gated. Without a verified watcher/automation, remain in the current task and state the continuity limit. Do not create a task or recurring job implicitly.

For repeated failures, narrow scope, change the hypothesis or return work to the parent. After two equivalent failures, reassess before retrying. Preserve partial artifacts and known-good evidence. On restart, rediscover actual agent status and reconcile each assignment before replacing it; never assume local agents died or remote agents survived.

Close with reconciled receipts, remaining gaps, actual verification and explicit publication state. Keep useful local evidence private; do not send reports, commit, push or merge without the corresponding authority.
