---
name: deliver-approved-programme
description: Execute an already approved multi-sprint, multi-PR, or GoalBuddy coding programme through bounded implementation, verification, review, pull-request remediation, merge, and exact-target proof. Use after planning and approval; do not use for creating the plan, simple one-change tasks, or unapproved deployment.
metadata:
  short-description: Deliver an approved coding programme
---

# Deliver Approved Programme

Turn an approved plan or active GoalBuddy board into verified delivery without making the user complete a configuration form.

The owner normally invokes this skill alone for programme execution. It uses
`workflow-orchestrator` as the single capability and Worker router and applies
`first-time-right-delivery` as the shared evidence discipline. Activate only
the specialists justified by the approved plan, active task, and actual diff;
the plan's capability handoff is advisory rather than an always-on bundle.

At the start of each materially different execution phase, use
`workflow-orchestrator` to run a targeted capability preflight for that phase.
The owner does not need to remember every useful skill or MCP. Revalidate the
preferred live route before relying on it, and choose a workaround only after
that route is shown unavailable, unsuitable, or outside the approved boundary.

## Invocation

Use a compact owner-control block. It keeps the decisions that legitimately vary by project while inferring ordinary repository details:

```text
/goal Follow docs/goals/<slug>/goal.md. Use $deliver-approved-programme.

Plan name: <name>
Plan path: <absolute path>
Execution strategy: AGILE_FOCUSED | AGILE_CONTROLLED_PARALLEL
Database or migrations: NONE | LOCAL | STAGING | PRODUCTION
Delivery to main: LOCAL ONLY | DIRECT COMMIT AUTHORIZED | BRANCH + PR, STOP BEFORE MERGE | BRANCH + PR + MERGE AUTHORIZED
Independent external review: DISABLED | OPTIONAL: <provider/model list> | REQUIRED AT <named risk boundary>: <provider/model list>
Simulator visual/accessibility QA: REQUIRED | CONDITIONAL | DEFERRED
Physical-device QA: REQUIRED BEFORE MERGE | DEFERRED UNTIL BUILD | NOT APPLICABLE
```

Outside GoalBuddy, replace the first line with `Use $deliver-approved-programme.` and keep the same block.

The plan name and path identify the approved source of truth. A value may be omitted when the active GoalBuddy charter already records the exact same decision. Infer the repository, target branch, current sprint, validation commands, platform, relevant skills, and exclusions from the current workspace, plan, board, and repository instructions. Ask only when a missing decision would materially change scope, authority, safety, or the result; never expand this compact block into a larger questionnaire.

Interpret the controls as follows:

- `Database or migrations` is the highest environment the plan may affect. It does not authorize unrelated, destructive, or unspecified database work.
- `Execution strategy` is `AGILE_FOCUSED` by default: use it for ambiguity, shared contracts, migrations, PR remediation, and tightly coupled UI or integration work. The main agent actively writes, integrates, and supervises; read-only research, review, and QA may run concurrently. `AGILE_CONTROLLED_PARALLEL` is permitted only after an approved dependency and ownership map proves independent write lanes. Each lane records exact files or symbols, a separate branch and worktree, verification commands, stop conditions, and the named main-agent integration owner. If a shared dependency, migration, overlap, integration conflict, or blocker appears, stop affected lanes, reconcile, and return to `AGILE_FOCUSED`.
- `Delivery to main` combines branch strategy and mainline authority so the user does not need separate commit, push, PR, and merge toggles. Direct commit still requires repository policy and validation to allow it.
- `Independent external review` selects both the requirement and the allowed provider/model list. Use `agent-collaboration-terminal`; verify only the named providers and never silently substitute another provider or model. For an authorized read-only external review, prefer its managed-background/manual-approval profile with visible fallback unless the owner explicitly requires a visible session. Pass `--review-profile code` only when the named task explicitly reviews code, a diff, branch, or PR; never infer code-review skills merely from `--mode review`. A `needs_attention` receipt is non-passing: the main agent executes the recorded fallback once when existing authority covers it, confirms native-CLI readiness, and only then submits the frozen prompt. For owner-required visible interactive sessions, treat Terminal creation, native-CLI readiness, and prompt submission as distinct evidence states. Do not claim the review started merely because a shell window opened.
- `Simulator ... CONDITIONAL` means required only for a supported project when the candidate changes visible UI or an interactive flow.
- An explicit owner instruction to run simulator testing makes it `REQUIRED` for the named change or delivery boundary, even when the standing programme control is `CONDITIONAL`.
- `Physical-device QA ... DEFERRED UNTIL BUILD` is reported as deferred and is not a passed check.

## Boundaries

- This skill starts after the plan is approved. If invoked during Goal Prep, preserve Goal Prep's strict boundary: prepare the board and stop without implementation.
- The active GoalBuddy `state.yaml` is board truth. Outside GoalBuddy, continue from the first incomplete approved increment.
- Do not rewrite the approved plan or skip dependencies. Validate current assumptions and escalate only material drift or contradiction.
- Use the smallest sufficient implementation. Evaluate review suggestions by verified necessity, concrete current benefit, and actual effort/risk—not by labels such as `nice to have`, `quick win`, or `enhancement`. A beneficial optional correction may be included without another approval only when it has meaningful current-PR value and is genuinely easy, localized, reversible, inside the approved product contract and recorded file scope, uses existing primitives, adds no dependency/infrastructure/migration/provider/flag/abstraction or material verification burden, and remains low-risk cumulatively with other additions. Required easy corrections should normally be implemented. Authentication, privacy, database, concurrency, migration, and release impact can make a tiny diff significant. If a necessary correction requires significant complexity or scope expansion, pause for the owner's explicit bounded approval. Explicitly reject as over-engineering or defer optional enhancements that are not both valuable now and genuinely easy/aligned; tell CodeRabbit, Codex, or the originating reviewer not to raise them again on the same PR unless materially new current-head evidence shows a required defect or a substantially simpler high-value in-scope correction. Repetition or rewording alone never changes that disposition.
- For a multi-sprint or multi-PR programme, use `workflow-orchestrator` to assign one reusable independent read-only Minimality Judge sub-agent. It reviews proposed implementation and QA packages before activation and the actual diff before acceptance for scope drift, duplicated primitives, speculative future-proofing, unnecessary providers/infrastructure, and disproportionate testing. It does not continuously poll or add a new review cycle when nothing material changed. The Judge must apply the same necessity-versus-effort rule: approve concrete low-risk quick wins that stay inside scope, require explicit bounded owner approval for necessary unusual complexity, and reject or defer unusual optional work unless the owner separately prioritizes it.
- For every non-trivial or high-risk delivery, record the pre-publication review gate explicitly: risk level; `code-review-and-quality` verdict; and local CodeRabbit state as `passed`, `blocked`, `owner-waived`, or `not-applicable`. Check local CodeRabbit installation and authentication before push or PR creation. A Codex reviewer, Minimality Judge, security reviewer, or passing tests never substitutes for CodeRabbit evidence. If a high-risk local CodeRabbit review is blocked, pause publication until the owner authorizes authentication or explicitly waives that layer with the approved fallback recorded.
- After a PR exists, inventory every current review surface—not only CodeRabbit—including top-level conversation comments, review submissions, inline threads and replies, reviewer states, and relevant check annotations. Before triage, compare each item with every prior disposition on the PR using its semantic root cause, affected contract or symbol, and requested outcome—not wording, thread ID, author, or file alone. Keep one canonical finding per root cause. For a duplicate already fixed on the current remote head, rejected with evidence or as over-engineering, or deferred under an approved boundary, reply immediately with the canonical disposition and evidence, state explicitly that it is not being considered again for this PR and should not be reopened without materially new current-head evidence, and do not start another analysis, implementation, test, sub-agent, or owner-decision loop. A local unpublished fix is `awaiting-publication`, not fixed-on-head. Reopen and re-triage only when the current head still reproduces the failure, the fix is absent or regressed, a material change makes the prior proof stale, new evidence invalidates the earlier disposition, or a previously deferred enhancement now has a demonstrably simpler high-value in-scope implementation. Reconcile every genuinely new or reopened validated actionable finding from every author or bot before final CI or merge; document false positives, informational notices, and approved deferrals instead of silently ignoring them.
- Before manually resolving a review thread, post a concise owner disposition reply with current-head evidence; duplicate threads must point to the canonical finding and disposition. Detect and backfill bot-auto-resolved threads that lack owner feedback. After each material correction push wave, publish one visible PR head-update comment and request each applicable configured rereview once, without duplicating a review already running on that head. Give `@coderabbitai`, `@codex`, or the configured equivalents the verified head SHA, correction scope, and validation, then explicitly tell them to exclude root causes already marked fixed, rejected, rejected as over-engineering, or deferred; reopen those only for materially new current-head evidence or a demonstrably simpler high-value safe in-scope correction, and otherwise focus on regressions introduced by the update and genuinely unique unresolved issues. Keep provider command syntax intact, but treat compliance with this request as advisory: independently inventory and semantically deduplicate every response before starting work.
- For platform-visible or interactive work, record a simulator checkpoint separately from source tests and physical-device QA: selected policy (`required`, `conditional`, `deferred`, or `not-applicable`), whether a conditional trigger fired, evidence state (`passed`, `blocked`, `deferred`, or `not-applicable`), and exact worktree/SHA/runtime/route/profile when executed. Required or conditionally triggered simulator QA blocks the applicable acceptance, final-CI, or merge boundary until it passes, unless the approved plan or owner explicitly defers or waives that exact boundary. Screenshots, source tests, or a stale or ambiguous runtime do not substitute for governed simulator evidence.
- Use one write-capable owner per worktree. Reviewers, monitors, Scouts, and Judges are read-only unless a separate bounded Worker task explicitly grants write scope.
- The main agent is the primary writer, integrator, and supervisor—not a supervisor-only role. In `AGILE_FOCUSED`, it owns active implementation and integration work, including integration-heavy, ambiguous, highest-risk, and shared-surface changes; bounded read-only support may run concurrently. In `AGILE_CONTROLLED_PARALLEL`, concurrent Workers may write only in approved independent lanes with separate worktrees and explicit main-agent reconciliation. The main agent reviews every Worker diff and owns the final integrated validation. A Worker card defines scope and evidence; it does not require delegation to a sub-agent.
- Never infer authority for commits, pushes, pull requests, merges, deployments, destructive actions, production changes, credential changes, or paid external-provider usage. Apply the compact controls plus authority recorded in the approved plan or GoalBuddy charter; otherwise stop at that boundary.
- Treat the actual diff and executable checks as truth. Plans, receipts, AI reviews, screenshots, CI badges, and provider summaries are evidence inputs, not proof by themselves.
- Keep local checks, CI, staging, simulator/browser QA, physical-device QA, external review, and deployment evidence separate. Never upgrade unavailable, skipped, or deferred evidence to passed.

## Default delivery shape

1. Read the approved plan, repository instructions, and—when present—the GoalBuddy execution contract, charter, and board.
2. Inspect the actual repository and worktree before editing. Preserve unrelated, ignored, untracked, research, generated, environment, secret, and control files unless they are explicitly in scope.
3. For a programme sprint, use one fresh branch and worktree from the verified target branch. Keep the sprint's approved increments together and normally open one GitHub pull request for that sprint unless the plan explicitly requires separate PRs.
4. Implement the largest safe useful slice with its focused tests. Add negative or counterexample coverage when the changed contract warrants it.
5. Run targeted validation during implementation and the applicable repository-native gates before delivery.
6. Review the actual change with the five-axis `code-review-and-quality` gate and the risk-scaled local CodeRabbit layer; remediate only validated issues and resolve the recorded simulator checkpoint when the change is visible, interactive, platform-specific, or simulator testing was explicitly invoked.
7. Stage only intentional paths, perform diff and secret checks, confirm the review and applicable simulator states are recorded, then commit, push, open or update the PR, and merge only within recorded authority. After PR creation, inventory and reconcile all reviewers and comment surfaces, including GitHub CodeRabbit, before triggering final CI labels or merge gates.
8. Verify the remote feature-branch SHA after push and the actual target-branch SHA after merge. Record a GoalBuddy receipt when applicable and advance only the next safe task.
9. Finish a programme only through a final Judge or PM audit mapped to the original goal oracle.

Read [references/execution-loop.md](references/execution-loop.md) for the full implementation and delivery sequence.

## Reviews

Select the smallest effective review set based on risk. Run `code-review-and-quality` for non-trivial or high-risk candidates. Use local CodeRabbit when it is installed, authenticated, within authorized usage, and useful; use GitHub CodeRabbit as a separate independent PR layer. Before publication, record local CodeRabbit as passed, blocked, owner-waived, or not applicable rather than silently replacing it with another reviewer. After publication, inspect the complete PR conversation and every review thread across all authors, deduplicate new comments against the PR's canonical finding dispositions, and validate only genuinely new, reopened, or still-unresolved findings against the current code and tests. Read [references/coderabbit-review.md](references/coderabbit-review.md) whenever CodeRabbit is used or its availability affects the delivery gate.

Use independent external providers only when the owner or approved plan authorizes their data scope and credit usage. Review the frozen integrated candidate, not individual Worker fragments. For an explicit code, diff, branch, or PR review, pass the terminal skill's opt-in code-review profile and give providers non-overlapping emphasis: Antigravity performs the five-axis quality review and applicable focused test review; Grok emphasizes security, privacy, trust boundaries, authorization, architecture, and minimality; Cursor provides an independent pragmatic code-navigation, implementation-quality, maintainability, user-reliability, and focused-test perspective; Junie is used selectively for runtime, reproduction, or test evidence. Do not apply that profile to non-code tasks, and do not ask any provider to invoke CodeRabbit or another external reviewer. Normalize and deduplicate provider findings against the PR's canonical finding ledger before creating tasks or comments. External-provider artifacts remain advisory until reconciled against the actual diff and executable checks.

Keep the two capability preflights distinct. Codex selects from capabilities
installed or surfaced in Codex; each authorized terminal provider inspects its
own installed or surfaced native skills, MCPs, plugins, and tools through the
generated prompt. Neither tier searches an external marketplace, installs or
authenticates capabilities, or expands the approved workspace, data, credit, or
external-action authority. Named provider skills and methods are non-exhaustive
unless the approved task explicitly requires them; within the manifest's hard
boundaries, providers retain native judgment over how to achieve the objective.

## Capability failures

Verify a capability before relying on it. Search the currently exposed skill
and plugin/MCP/connector/tool catalog narrowly for the active need; do not assume
that an installed skill or plugin makes its underlying live tool callable. An
optional reviewer, plugin, connector, model, simulator, or provider being
unavailable is not automatically a programme blocker. Use the discovery and
fallback protocol in
[references/capability-fallbacks.md](references/capability-fallbacks.md), label
the evidence boundary, and continue safe work. Discovery never authorizes an
installation, login, private-data access, credit spend, file exposure, or
external mutation. Stop only when the missing capability is required by the
approved acceptance contract or a material owner decision is needed.

## Completion report

At each sprint boundary, report only what helps the owner verify delivery:

- completed and incomplete approved increments;
- intentional files changed;
- checks grouped as passed, failed, blocked, skipped, or deferred;
- local, CI, staging, platform QA, physical-device, and reviewer evidence separately;
- branch, commit, PR, merge, and target-branch SHAs when applicable;
- preserved excluded work, remaining risks, and the next active task.
