---
name: integrated-workflow
description: Execute an already approved multi-sprint, multi-PR, or GoalBuddy coding programme through bounded implementation, verification, review, pull-request remediation, merge, and exact-target proof. Use after planning and approval; do not use for creating the plan, simple one-change tasks, or unapproved deployment.
metadata:
  short-description: Implement approved work through verified delivery
---

# Integrated Workflow

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

## Shared skill responsibilities

Use one active orchestrator, the approved plan and one shared evidence record. Supporting skills contribute methods and evidence to the current package; they must not restart planning, create a competing board or launch duplicate review cycles.

- `workflow-orchestrator` alone selects capabilities and workers. Reuse its active context when a specialist hands control back.
- `first-time-right-delivery` supplies proportional requirement-to-evidence and counterexample checks. Read its "Before changing behavior" section as a gap check against the approved plan, not permission to replan. An appropriate existing independent correctness review may cover the counterexample assignment; explicitly record that coverage. A complexity-only Ponytail review cannot satisfy it.
- `unlazy` is optional completion support through the [First-Time-Right Delivery adapter](../first-time-right-delivery/references/unlazy.md). Reuse one acceptance record and the approved plan; check affected outcomes against the final candidate and measure report claims. Inspect the installed checker version, keep abandoned or deferred gates distinct from passed gates, and preserve required owner decisions. It creates no second programme, worker hierarchy, review loop, automatic hook or new installation requirement.
- `agent-map` is conditional navigation for unfamiliar architecture, multi-file impact or caller tracing. Check freshness, make one targeted query, then verify against current source/tests; skip known-file edits. Refresh only where generated local metadata is allowed by task scope and worktree hygiene. Otherwise use `rg`; do not alter ignore rules, install hooks or commit map output implicitly. Missing or stale edges are unknown, not proof of no callers.
- `project-learning` is invoked only for explicitly requested learning work. Relevant accepted project lessons may inform execution, subject to current instructions and evidence. An optional final learning note is communication only. Delivery never automatically captures or promotes lessons, installs learning hooks, writes memory or interrupts the task for learning approval.

For documentation, governance or tooling increments, independently deliverable means usable and verifiable within the approved scope; it does not require an application build or deployment. Preserve every required safety, compatibility and approval gate. Select supporting skills only when applicable and available; naming them is not evidence that their tools ran.

## Engineering implementation packages

The orchestrator selects one matching engineering playbook: complete Codex Forge in Codex, native PStack in Cursor, or the shared `engineering-playbooks` method elsewhere. Each harness retains its own available models and runtime controls. Codex uses `plan-model-router` when installed; another harness does not inherit Codex model names. Reassess material changes in task scope, capabilities or parent settings before delegation. Native evidence stores remain optional and cannot replace the approved plan, review gates or final acceptance.

## Optional Ponytail support

Use Ponytail through the existing orchestrator and minimality owner when available and useful; do not activate the whole family or add another mandatory reviewer. Select only the applicable method:

- `ponytail`: challenge speculative work, trace affected callers, and prefer existing repository code, standard library and native features before custom code or new dependencies.
- `ponytail-review`: inspect the scoped diff for unnecessary complexity as part of the existing minimality pass. Feed suggestions into the same finding ledger and convergence rule; its verdict is not correctness, security or merge approval.
- `ponytail-debt`: on a debt-report request, collect existing shortcut markers with their limits and revisit triggers. Reuse existing task/debt records; do not create a second persistent ledger or insert markers merely to populate one.
- `ponytail-audit`: a separately requested whole-repository complexity audit. An ordinary PR never authorizes that expansion; its findings do not automatically enter the active sprint.
- `ponytail-gain`: on a benchmark-display request only. Published benchmark figures are not measured savings for this repository or evidence of delivery quality.

Discover these external skills at runtime; do not vendor plugin files, hard-code cache paths or install missing capabilities. If absent, use the existing minimality discipline. Simplicity never removes requested behavior, trust-boundary validation, data-loss protection, accessibility or required checks. Reuse the repository's test framework and proportional coverage; shortest-line, single-test and terse-output preferences cannot replace the acceptance contract or truthful reporting. Apply methods within the active package without silently enabling a persistent mode in other tasks.

## Invocation

Use a compact owner-control block. It keeps the decisions that legitimately vary by project while inferring ordinary repository details:

```text
/goal Follow docs/goals/<slug>/goal.md. Use $integrated-workflow.

Plan name: <name>
Plan path: <absolute path>
Execution strategy: AGILE_FOCUSED | AGILE_CONTROLLED_PARALLEL
Database or migrations: NONE | LOCAL | STAGING | PRODUCTION
Delivery to main: LOCAL ONLY | DIRECT COMMIT AUTHORIZED | BRANCH + PR, STOP BEFORE MERGE | BRANCH + PR + MERGE AUTHORIZED
Independent external review: DISABLED | OPTIONAL: <provider/model list> | REQUIRED AT <named risk boundary>: <provider/model list>
Simulator visual/accessibility QA: REQUIRED | CONDITIONAL | DEFERRED
Physical-device QA: REQUIRED BEFORE MERGE | DEFERRED UNTIL BUILD | NOT APPLICABLE
```

Outside GoalBuddy, replace the first line with `Use $integrated-workflow.` and keep the same block.

The plan name and path identify the approved source of truth. A value may be omitted when the active GoalBuddy charter already records the exact same decision. Infer the repository, target branch, current sprint, validation commands, platform, relevant skills, and exclusions from the current workspace, plan, board, and repository instructions. Ask only when a missing decision would materially change scope, authority, safety, or the result; never expand this compact block into a larger questionnaire.

Interpret the controls as follows:

- `Database or migrations` is the highest environment the plan may affect. It does not authorize unrelated, destructive, or unspecified database work.
- `Execution strategy` is `AGILE_FOCUSED` by default: use it for ambiguity, shared contracts, migrations, PR remediation, and tightly coupled UI or integration work. The main agent actively writes, integrates, and supervises; read-only research, review, and QA may run concurrently. `AGILE_CONTROLLED_PARALLEL` is permitted only after an approved dependency and ownership map proves independent write lanes. Each lane records exact files or symbols, a separate branch and worktree, verification commands, stop conditions, and the named main-agent integration owner. If a shared dependency, migration, overlap, integration conflict, or blocker appears, stop affected lanes, reconcile, and return to `AGILE_FOCUSED`.
- `Delivery to main` combines branch strategy and mainline authority so the user does not need separate commit, push, PR, and merge toggles. Direct commit still requires repository policy and validation to allow it.
- `Independent external review` selects both the requirement and the allowed provider/model list. For terminal providers, use `agent-collaboration-terminal`; verify only the named providers and never silently substitute another provider or model. GitHub Cloud Antigravity is a PR-native reviewer: name it in the controls and use the exact `@agy /review` conversation trigger described in Reviews, not the terminal route. For an authorized read-only external review, prefer its managed-background/manual-approval profile with visible fallback unless the owner explicitly requires a visible session. Pass `--review-profile code` only when the named task explicitly reviews code, a diff, branch, or PR; never infer code-review skills merely from `--mode review`. A `needs_attention` receipt is non-passing: the main agent executes the recorded fallback once when existing authority covers it, confirms native-CLI readiness, and only then submits the frozen prompt. For owner-required visible interactive sessions, treat Terminal creation, native-CLI readiness, and prompt submission as distinct evidence states. Do not claim the review started merely because a shell window opened.
- `Simulator ... CONDITIONAL` means required only for a supported project when the candidate changes visible UI or an interactive flow.
- An explicit owner instruction to run simulator testing makes it `REQUIRED` for the named change or delivery boundary, even when the standing programme control is `CONDITIONAL`.
- `Physical-device QA ... DEFERRED UNTIL BUILD` is reported as deferred and is not a passed check.

## Boundaries

- This skill starts after the plan is approved. If invoked during Goal Prep, preserve Goal Prep's strict boundary: prepare the board and stop without implementation.
- The active GoalBuddy `state.yaml` is board truth. Outside GoalBuddy, continue from the first incomplete approved increment.
- Do not rewrite the approved plan or skip dependencies. Validate current assumptions and escalate only material drift or contradiction.
- Use the smallest sufficient implementation. Evaluate review suggestions by verified necessity, concrete current benefit, and actual effort/risk—not by labels such as `nice to have`, `quick win`, or `enhancement`. A beneficial optional correction may be included without another approval only when it has meaningful current-PR value and is genuinely easy, localized, reversible, inside the approved product contract and recorded file scope, uses existing primitives, adds no dependency/infrastructure/migration/provider/flag/abstraction or material verification burden, and remains low-risk cumulatively with other additions. Required easy corrections should normally be implemented. Authentication, privacy, database, concurrency, migration, and release impact can make a tiny diff significant. If a necessary correction requires significant complexity or scope expansion, pause for the owner's explicit bounded approval. Explicitly reject as over-engineering or defer optional enhancements that are not both valuable now and genuinely easy/aligned; tell CodeRabbit, Codex, or the originating reviewer not to raise them again on the same PR unless materially new current-head evidence shows a required defect or a substantially simpler high-value in-scope correction. Repetition or rewording alone never changes that disposition.
- For a multi-sprint or multi-PR programme with authorized and available independent workers, use `workflow-orchestrator` to assign one reusable read-only reviewer for scope and unnecessary complexity. When workers are unavailable, the parent performs the same bounded audit; any contractually required independence remains unmet and must be reported. It reviews proposed implementation and QA packages before activation and the actual diff before acceptance for scope drift, duplicated primitives, speculative future-proofing, unnecessary providers/infrastructure, and disproportionate testing. It does not continuously poll or add a new review cycle when nothing material changed. The Judge must apply the same necessity-versus-effort rule: approve concrete low-risk quick wins that stay inside scope, require explicit bounded owner approval for necessary unusual complexity, and reject or defer unusual optional work unless the owner separately prioritizes it.
- For non-trivial delivery, record risk, the `code-review-and-quality` verdict and the independent evidence required by the approved contract. Record CodeRabbit separately when selected or required. Missing optional CodeRabbit does not create a new gate; an existing mandatory CodeRabbit gate remains binding and needs the owner's disposition if unavailable. Never relabel another review as CodeRabbit evidence.
- Apply [review convergence](references/execution-loop.md#review-convergence) to all reviewers: collect current-head reviews, consolidate findings and fixes, publish one remediation wave, then obtain one appropriate rereview. Further waves require demonstrated required defects or explicit owner reprioritization; optional completeness must not keep the PR open. This never waives unresolved required findings or repository approval/check requirements.
- Inventory every review surface and keep one canonical disposition per semantic root cause, affected contract and failure scenario. Repeated wording, authors or syntax variants are not automatically new work. Reopen only with material current-head evidence; distinguish a reproduced required defect from hypothetical future support. Record fixes as awaiting publication until verified on the remote head.
- Before manually resolving a thread, ensure it has a concise disposition with current-head evidence or a link to the canonical finding. Backfill automatically resolved items only when disposition is missing or ambiguous; do not add acknowledgement-only replies. Reuse one PR update per wave. Automatic reviews already queued, running or completed for that head count toward the review request; do not also request them manually. Follow the convergence rule before triggering any additional configured reviewer.
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
6. Review the actual change using the [pre-commit review brief](#pre-commit-review-brief) with the five-axis `code-review-and-quality` gate and the risk-scaled local CodeRabbit layer; remediate only validated issues and resolve the recorded simulator checkpoint when the change is visible, interactive, platform-specific, or simulator testing was explicitly invoked.
7. Stage only intentional paths, perform diff and secret checks, confirm the review and applicable simulator states are recorded, then commit, push, open or update the PR, and merge only within recorded authority. After PR creation, inventory and reconcile all reviewers and comment surfaces, including GitHub CodeRabbit and GitHub Cloud Antigravity, before triggering final CI labels or merge gates.
8. Verify the remote feature-branch SHA after push and the actual target-branch SHA after merge. Record a GoalBuddy receipt when applicable and advance only the next safe task.
9. Finish a programme only through a final Judge or PM audit mapped to the original goal oracle.

Read [references/execution-loop.md](references/execution-loop.md) for the full implementation and delivery sequence.

## Reviews

Select the smallest effective review set based on risk. Run `code-review-and-quality` for non-trivial or high-risk candidates. Use local CodeRabbit when it is installed, authenticated, within authorized usage, and useful; use GitHub CodeRabbit as a separate independent PR layer. Before publication, record local CodeRabbit as passed, blocked, owner-waived, or not applicable rather than silently replacing it with another reviewer. After publication, inspect the complete PR conversation and every review thread across all authors, deduplicate new comments against the PR's canonical finding dispositions, and validate only genuinely new, reopened, or still-unresolved findings against the current code and tests. Read [references/coderabbit-review.md](references/coderabbit-review.md) whenever CodeRabbit is used or its availability affects the delivery gate.

When the GitHub Cloud Antigravity app is installed, authorized, and named by the approved review controls, treat it as a PR-native review surface rather than a terminal provider. When an initial review or rereview is due under the convergence rule, and no equivalent Antigravity review is queued, running or completed for that head, post one top-level conversation comment with the verified head SHA, correction scope, and validation, followed by this exact standalone trigger on its own line:

```text
@agy /review
```

The posted command means `requested`, not `passed`: wait for and inventory the resulting Antigravity review submission, reviewer state, and check annotations before counting its evidence toward CI or merge. If the app does not respond, record `unavailable` (and block a required Antigravity boundary) rather than treating the comment as a successful review. Do not route this GitHub Cloud trigger through `agent-collaboration-terminal`, and do not duplicate it while a review for the same head is running.

Use independent external providers only when the owner or approved plan authorizes their data scope and credit usage. Review the frozen integrated candidate, not individual Worker fragments. For an explicit code, diff, branch, or PR review performed by a terminal provider, pass the terminal skill's opt-in code-review profile and give providers non-overlapping emphasis: terminal Antigravity performs the five-axis quality review and applicable focused test review; Grok emphasizes security, privacy, trust boundaries, authorization, architecture, and minimality; Cursor provides an independent pragmatic code-navigation, implementation-quality, maintainability, user-reliability, and focused-test perspective; Junie is used selectively for runtime, reproduction, or test evidence. GitHub Cloud Antigravity is separate: use the PR conversation trigger above instead of treating the app as a terminal provider. Do not apply that profile to non-code tasks, and do not ask any provider to invoke CodeRabbit, GitHub Cloud Antigravity, or another external reviewer. Normalize and deduplicate provider findings against the PR's canonical finding ledger before creating tasks or comments. External-provider artifacts remain advisory until reconciled against the actual diff and executable checks.

Keep the two capability preflights distinct. The parent selects from capabilities
installed or surfaced in its own harness; each authorized terminal provider inspects its
own installed or surfaced native skills, MCPs, plugins, and tools through the
generated prompt. Neither tier searches an external marketplace, installs or
authenticates capabilities, or expands the approved workspace, data, credit, or
external-action authority. Named provider skills and methods are non-exhaustive
unless the approved task explicitly requires them; within the manifest's hard
boundaries, providers retain native judgment over how to achieve the objective.

## Pre-commit review brief

Use this brief at the existing candidate-review step for local and authorized external reviewers, preserving their assigned emphasis. It adds no mandatory reviewer, provider invocation, hook or review cycle:

> Review the complete intended candidate and the surrounding code needed to assess its effects. Identify concrete bugs, regressions, security issues, and unnecessary complexity within the approved scope. Reuse existing patterns; justify simplifications by current benefit. Report severity, precise evidence, impact, and the smallest sufficient correction. Consolidate duplicate findings and distinguish required fixes from optional improvements. Remain read-only. The implementation owner validates and batches corrections, runs relevant checks, and obtains focused rereview under the existing convergence rule. Before committing, confirm the staged contents match the reviewed candidate, including intended additions, deletions, and file modes.

Identify the candidate's base, worktree/head and intended paths; include intended untracked additions explicitly rather than assuming a Git diff contains them. The implementation owner performs the staged-content comparison and reconciles mismatches before committing. Changes since review receive proportional verification under [review convergence](references/execution-loop.md#review-convergence); reviewer count or an earlier verdict cannot establish coverage of changed contents.

DRY/KISS guide justified simplification, not automatic refactoring. Tests and documentation are assessed by their effects, not presumed safe by file type. A review may report no findings. Completion means required defects are resolved and applicable checks pass, with required approvals still honored; optional improvements do not restart an unbounded "until clean" loop.

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
