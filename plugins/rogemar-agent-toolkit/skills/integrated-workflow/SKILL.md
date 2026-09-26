---
name: integrated-workflow
description: Execute an approved coding programme by complete vertical slices, with proportional implementation checks, local review, ready-PR review and remediation, and verified delivery. Use after approval for multi-sprint, multi-PR or GoalBuddy work; route small bounded corrections through the lighter path without starting a programme.
metadata:
  short-description: Deliver approved vertical slices with proportional checks
---

# Integrated Workflow

At task start/resume, before acceptance and at verified completion, apply the shared
[automatic checkpoints](../engineering-playbooks/references/agent-friendly-workflow.md) when a project verification map or learning enrollment exists. Select the actions without waiting for skill names; preserve task authority and required evidence.

Deliver the approved outcome with one plan, one implementation owner, one evidence
record and one consolidated review process. Infer ordinary project details; the
owner need not name every supporting skill or fill out a configuration form.

## Scope and ownership

Start after plan approval. During Goal Prep, preserve its preparation-only
boundary and stop before implementation. With GoalBuddy, its execution contract
and `state.yaml` govern active tasks; otherwise resume the first incomplete,
dependency-ready increment. Do not replan or rewrite approved dependencies.

Use `workflow-orchestrator` as the sole capability and worker dispatcher. At a
materially different phase, discover only the installed or surfaced capabilities
needed for that phase and verify the selected live route before relying on it.
`first-time-right-delivery` supplies requirement-to-evidence and counterexample
checks within this same plan and review. One suitable independent review may
cover correctness, counterexamples and scope; record that coverage. A complexity-
only review cannot establish correctness or required independence.

The main agent writes, integrates and owns final acceptance. Default to
`AGILE_FOCUSED`: one write-capable owner per worktree, with useful read-only support.
The orchestrator automatically selects `AGILE_CONTROLLED_PARALLEL` when existing
approval permits delegation and its [strategy selection criteria](../workflow-orchestrator/SKILL.md#automatic-execution-strategy)
prove independent, isolated and worthwhile write lanes. The owner need not choose
per package. Explicit strategy or one-writer restrictions take precedence.
When independence is uncertain, stay focused. On a new conflict, pause affected
writers, preserve their work and reconcile sequentially; unaffected independent
lanes may continue. Reviewers remain read-only unless assigned bounded write scope.

For optional scope-review, Ponytail, Unlazy, navigation and Project Learning,
read [supporting methods](references/supporting-methods.md) only when relevant.
They add methods to the existing owner, not another board, reviewer hierarchy or
mandatory cycle. Documentation and tooling increments need proof of their own
outcome, not an unrelated app build or deployment.

## Choose proportional checks

Classify by effects and risk, not line count, file type or project size.

- **Small bounded correction:** localized, reversible, understood behavior with
  limited impact and focused verification. Inspect the actual diff and affected
  behavior; run applicable checks and UI/accessibility checks when relevant.
  Local CodeRabbit and independent providers, including PR CodeRabbit/Codex,
  are optional unless repository policy or the approved contract requires them.
  Do not start a programme, board, reviewer panel or delivery ceremony for it.
- **Substantive work:** an ordinary feature, vertical slice or meaningful bug fix
  requires scoped implementation evidence, `code-review-and-quality`, and local
  CodeRabbit at slice acceptance. Branch delivery also requires separate GitHub
  CodeRabbit and Codex reviews once the complete slice is ready for review.
- **Sensitive work:** add the independent domain evidence warranted by changed
  authorization, privacy, data integrity, migrations, concurrency, compatibility
  or recovery. A tiny sensitive edit is not automatically a small correction.

The small-change exception never weakens an existing required gate, hides a
substantive slice behind individually small commits, or turns review absence into
a pass. Additional providers such as Antigravity, Grok and Junie are conditional
on explicit selection and authority; do not activate them all by default.

Define each gate once in the existing receipt using the
[gate and evidence contract](references/execution-loop.md#gate-and-evidence-contract).
An optional capability failure remains optional at every later checkpoint.
Required unavailable evidence blocks its named boundary while safe independent
work may continue. Model modes affect execution profiles, not acceptance standards.

## Harness and engineering methods

Accept `Harness: <name>` or an explicitly invoked engineering entry. Otherwise
infer from reliable host context and use the portable route when uncertain.
Through the existing orchestrator, select one compatible route:

| Harness | Engineering methods | Profile selection |
| --- | --- | --- |
| Codex | `codex-forge` | `plan-model-router` |
| Cursor | `cursor-forge`; upstream PStack/poteto-mode if absent | `cursor-forge-setup`; universal router only as a constraint-preserving fallback |
| Other or unknown | `universal-forge`; shared `engineering-playbooks` if unavailable | `universal-plan-model-router` using observed native capabilities |

Honor compatible explicit choices. Reassess task fit, capabilities and applicable
parent/mode constraints before delegation. A harness name, saved mode or installed
skill does not prove tool access, worker dispatch or a live parent-model switch.
Keep one engineering owner and never import another harness's model IDs or controls.

## Invocation and delivery boundaries

Invoking this workflow to execute approved work authorizes the default branch-and-PR
route through safe merge. Plan approval, automatic skill selection, or discussing/editing this skill alone
does not grant publication authority. The owner must explicitly invoke this
workflow for execution or separately authorize the delivery route. Usually this is enough:

```text
Use $integrated-workflow to implement the approved plan at <path>.
Harness: <name, or infer>
```

Accept these optional controls when the owner needs to specify them; reuse
recorded decisions and ask only for material missing scope or authority:

```text
Plan name/path: <approved source, or active GoalBuddy charter>
Execution strategy: AGILE_FOCUSED | AGILE_CONTROLLED_PARALLEL
Database or migrations: NONE | LOCAL | STAGING | PRODUCTION
Delivery to main: LOCAL ONLY | DIRECT COMMIT AUTHORIZED | BRANCH + PR, STOP BEFORE MERGE | BRANCH + PR + MERGE AUTHORIZED
Independent external review: DISABLED | OPTIONAL: <providers/models> | REQUIRED AT <boundary>: <providers/models>
Simulator visual/accessibility QA: REQUIRED | CONDITIONAL | DEFERRED
Physical-device QA: REQUIRED BEFORE MERGE | DEFERRED UNTIL BUILD | NOT APPLICABLE
```

- Default to `BRANCH + PR + MERGE AUTHORIZED` for approved implementation.
  Invocation authorizes scoped branch commits and pushes, opening or updating the
  task PR, marking it ready when eligible, requesting configured PR reviews,
  addressing findings, applicable authorized CI, and merging after required gates
  pass. Continue through exact-target verification without per-step approval;
  reuse the existing task PR when present.
- Stricter repository authorization requirements take precedence over this
  default. If a repository requires a separate explicit publication or merge
  instruction, obtain the missing authority before that action; a skill cannot
  waive it.
- Explicit task restrictions such as `LOCAL ONLY`, no-push, draft-only or
  `STOP BEFORE MERGE` override this default until the owner changes them. Record
  the effective route once. Ask only for a material conflict or missing decision,
  not to reconfirm authority already supplied by invocation.
- Safe merge requires current-head checks, required reviews, repository approvals
  and trusted scope evidence. Never self-approve an owner-controlled record,
  bypass protection or weaken a gate. Prepare the exact owner-only artifact and
  explain the remaining action when genuinely blocked.
- Inspect push, PR and merge automation before triggering it. This route does not
  authorize deployment, store/OTA publication, unapproved expensive builds,
  destructive operations or additional paid providers. Stop before an excluded
  action and request its specific authorization.
- Direct commit and push to the verified target branch require the owner's
  explicit instruction and repository-policy permission. Small or personal
  projects do not imply this choice. Preserve applicable local checks and local
  CodeRabbit for substantive work; PR-only gates are not applicable on this route.
- `Independent external review` controls additional independent providers. It
  does not silently disable the substantive local CodeRabbit and ready-PR
  CodeRabbit/Codex requirements above. A separate explicit owner waiver or
  stricter project contract must be recorded at the affected gate.
- Database scope is the maximum authorized environment, not permission for
  unrelated or destructive operations. Production and deployment authority
  remain separate.
- Conditional simulator QA applies to supported projects with visible or
  interactive changes. An explicit simulator-testing request makes it required
  for the named scope. Device deferral remains deferred, not passed.

## Build continuously; review a complete vertical slice

Use one branch and optional draft PR per complete vertical slice, even when the
slice spans several sprints and commits. Reuse that branch/draft while resuming
work. Start a new branch/worktree from the verified target for a new independent
slice; preserve explicitly approved stacked dependencies or separate-PR plans.
Do not create another PR merely because a sprint ended.

A draft PR is already an open GitHub PR. Treat **ready for review** as the cloud
QA handoff. With publication authority, push incremental commits to the feature
branch and optionally maintain its draft. Run proportionate local checks as work
progresses. The final full local CodeRabbit review belongs at slice acceptance,
before creating a ready PR or converting the draft; do not require a full review
of every intermediate commit. Any stricter recorded checkpoint still applies.

Keep the slice draft or branch-only until its approved functionality is complete,
the integrated diff and applicable local/UI/runtime evidence are ready, and local
review requirements are satisfied. Draft status is not a way to merge incomplete
work. Avoid accumulating unrelated features into one unreviewable PR; follow the
approved slice boundary and surface material scope drift.

## UI/UX during implementation

For visible or interactive changes, select the relevant design, UX and
accessibility methods automatically through the orchestrator. Follow
[UI/UX implementation](references/ui-ux-implementation.md): inspect the existing
interface, implement accessible behavior, refine affected interactions, and
verify the rendered result before final candidate readiness. Activate only the
specialists justified by the affected surface; OpenDesign services are conditional.

Early architecture, security and diagnostic reviews may proceed while building.
Missing required runtime evidence remains blocked or explicitly deferred; useful
partial code review does not establish UI readiness. Record simulator `failed`
when an executed check finds a defect, and `blocked` when its prerequisite is
unavailable. Preserve browser, simulator, assistive-technology and physical-device
evidence separately. After reviewer-driven UI changes, rerun affected UI checks.

## Ready-PR monitoring and remediation

When authorized branch delivery reaches a ready PR, the active workflow includes
monitoring and resolving its review/check results through the allowed boundary.
Observe GitHub CodeRabbit and Codex as separate reviewers, plus all applicable
human, bot, conversation, inline-thread and check-annotation surfaces. Optional
selected providers feed the same process. A posted request is not a completed review.

Do not start or poll a PR-review monitor while the PR is draft. Configured GitHub
checks or bots may still run; do not disable them or claim draft status suppresses
them. At ready transition, inspect existing results and the exact head before
requesting missing due reviews. Reuse a valid equivalent review where the
provider and repository allow it, without passing stale evidence forward.

Collect available reviews, consolidate duplicate and interacting findings, then
validate the combined proposed correction against the whole affected contract.
The implementation owner applies the smallest sufficient batch of valid fixes;
reviewers do not independently patch competing suggestions. Reconcile all
recommendations, including ones that merit rejection or deferral, rather than
implementing every suggestion. Follow
[review convergence and dispositions](references/execution-loop.md#review-convergence).

Reject false positives, speculative support and unnecessary complexity with
concise evidence. Include optional improvements only when valuable now, easy,
localized, reversible, within approved scope and low-risk cumulatively. Required
significant scope/complexity changes need the owner's bounded decision. Keep
settled dispositions across reviewers; reopen only with materially new evidence.

Verify the published fix on the remote head before claiming a PR issue resolved.
Obtain due focused rereview, honor required CI/approvals and stop optional churn
once acceptance is satisfied. Monitoring ends on verified completion at the
allowed boundary, closure, return to draft, cancellation or an actionable block.
For stop-before-merge delivery, report readiness and stop without merging.

This is active-task follow-through, not installation of a permanent background
job. Use a harness scheduler only for an explicit request to keep watching after
the task yields; preserve scope, changed-only updates and stop conditions.

## Verify and report delivery

Read [execution loop](references/execution-loop.md) for gate evidence, candidate
identity, review convergence, simulator acceptance and exact-target delivery.
Read [CodeRabbit review](references/coderabbit-review.md) when applying its local
or GitHub layer. Read [capability fallbacks](references/capability-fallbacks.md)
only when the selected capability cannot be used.

Review the complete intended candidate and affected callers, including intended
untracked additions, deletions and file modes. Identify its comparison base,
contents and runtime; HEAD alone does not identify uncommitted changes. Before
committing, compare staged contents to the reviewed candidate and proportionately
revalidate differences. Reuse unchanged evidence only within its recorded scope.

Commit, push, request reviews, merge and deploy only within existing explicit
authority. Confirm remote feature-head identity after pushes and target contents
after direct-main delivery or merge. No merge or SHA receipt alone proves deployment.
Finish through a main-agent/PM audit against the original outcome; use GoalBuddy's
Judge/PM contract where applicable, without inventing a mandatory extra agent.

Report completed and incomplete increments, intentional changes, evidence grouped
as passed/failed/blocked/deferred/not applicable, review dispositions, relevant
branch/PR/SHAs, preserved exclusions and the next safe action. Optional polish and
duplicate findings do not restart delivery once required gates are satisfied.
