---
name: integrated-workflow
description: Execute an approved coding programme by complete vertical slices, with proportional implementation checks, local review, ready-PR review and remediation, and verified delivery. Use after approval for multi-sprint, multi-PR or GoalBuddy work; route small bounded corrections through the lighter path without starting a programme.
metadata:
  short-description: Deliver approved vertical slices with proportional checks
---

# Integrated Workflow

Follow the [applicable method contract](../workflow-orchestrator/references/method-contract.md) at entry, every task handoff and delegation,
material changes, resume and acceptance. Select relevant methods automatically; preserve one owner,
required evidence and the original working fallback. Query the routing index only
for the current task; do not load or activate the whole catalog.

Use [execution provenance](references/execution-provenance.md) only when the
protected acceptance policy requires that evidence tier. Preserve the existing
receipt and review waves; the extension creates no runner or publication authority.

At task start/resume, before acceptance and at verified completion, apply the shared
[automatic checkpoints](../engineering-playbooks/references/agent-friendly-workflow.md) when a project verification map or learning enrollment exists. Select the actions without waiting for skill names; preserve task authority and required evidence.

Deliver the approved outcome with one plan, one accountable implementation
owner, one evidence record and one consolidated review process. The owner
supervises the sprint. Assigned workers may write inside their assignment.
Infer ordinary project details; the owner need not name every supporting skill
or fill out a configuration form.

## Open only the file this task needs

Classify the task first. `workflow-orchestrator` remains the only skill router.
It reads `skill-routing.json` for the current task. Do not open the rest of the
catalog, and do not open every file linked from this skill.

| Situation | Open |
| --- | --- |
| Small bounded correction | The proportional-checks section below. Leave the review, UI, and delivery files closed. |
| Approved implementation on a named harness | The harness table below, then that harness's Forge entry. |
| Visible or interactive UI | [UI/UX implementation](references/ui-ux-implementation.md) |
| Unlazy, Ponytail, navigation, or project learning | [Supporting methods](references/supporting-methods.md) |
| Gate evidence, commit, or merge | [Execution loop](references/execution-loop.md) |
| CodeRabbit or a ready-PR review | [CodeRabbit review](references/coderabbit-review.md) |
| A selected tool is missing | [Capability fallbacks](references/capability-fallbacks.md) |
| Swift, Xcode, or an end-to-end journey | [Route readiness](../workflow-orchestrator/references/route-readiness.md) |

`e2e`, the SwiftUI skills, and `opendesign` are selected only for those situations.
They install with the `web`, `mobile`, `swift`, `ios`, and `opendesign` packs.
`plan-model-router` is the Codex router. Cursor uses `cursor-forge-setup`, Claude
uses `claude-forge-setup`, and every other harness uses `universal-plan-model-router`.

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

The parent agent supervises, integrates, and writes. It is the accountable
implementation owner and owns final acceptance. `workflow-orchestrator` assigns
sub-agents when search, QA, building, or testing earns a separate context.
Those workers may read and write inside the assignment in either strategy.
An assignment does not expand the user's grant, host permissions, or release
authority. A worker that only judges a diff stays read-only. A worker assigned
to build, fix, or add tests writes the files it owns. Two writers do not edit
the same file at the same time. That file rule is separate from the sprint strategy.

Default to `AGILE_FOCUSED`: one vertical slice, or one task inside that slice,
is active in the sprint. The parent and its workers finish that slice or task
before starting another. A slice may continue into a later sprint on the same
branch and draft pull request.

The orchestrator selects `AGILE_CONTROLLED_PARALLEL` when the sprint contains
more than one vertical slice or task, those slices or tasks do not conflict,
and its [strategy selection criteria](../workflow-orchestrator/SKILL.md#automatic-execution-strategy)
show the parent can integrate them. Conflict means shared files, contracts,
generated outputs, databases, or runtime resources. Different filenames alone
are not enough. The owner need not choose per package. An explicit strategy
takes precedence.

When independence is unclear, stay focused. On a new conflict, pause the
affected slices or tasks, preserve their work, and continue them one at a time.
Unaffected slices or tasks may continue.

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
  Start both with full-PR coverage and wait for both to complete before
  consolidating, validating findings or fixing. Follow the shared
  [cloud review allowance](references/coderabbit-review.md#cloud-review-allowance);
  local review cadence remains unchanged and invoked local providers review fully.
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

Automatic selection remains with `workflow-orchestrator`. For Swift, Xcode, E2E,
capability readiness and portable verification maintenance, apply its installed
`references/route-readiness.md` when relevant. Select methods from task meaning,
validate the chosen files/prerequisites, and carry the same evidence into worker
briefs. No second dispatcher or routine full-catalog audit is needed.

## Harness and engineering methods

Accept `Harness: <name>` or an explicitly invoked engineering entry. Otherwise
infer from reliable host context and use the portable route when uncertain.
Through the existing orchestrator, select one compatible route:

| Harness | Engineering methods | Profile selection |
| --- | --- | --- |
| Codex | `codex-forge` and shared `forge-*` methods | `plan-model-router` |
| Cursor | `cursor-forge` and shared `forge-*` methods. Upstream PStack only when those skills are absent | `cursor-forge-setup`. Universal router only as a constraint-preserving fallback |
| Claude | `claude-forge` and shared `forge-*` methods | `claude-forge-setup` |
| Other or unknown | `universal-forge` and shared `forge-*` methods. Shared `engineering-playbooks` if those skills are unavailable | `universal-plan-model-router` using observed native capabilities |

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
Execution strategy: AGILE_FOCUSED (one slice or task this sprint) | AGILE_CONTROLLED_PARALLEL (several non-conflicting slices or tasks)
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

## Local and cloud review assignments

Use the orchestrator's [review support/decision roles](../workflow-orchestrator/references/provider-routing.md#review-support-and-decision-roles)
for authorized local pre-commit reviews, complete-slice reviews and ready-PR review
waves. Separate low-usage status
monitoring and feedback consolidation from correctness validation, minimum-viable
scope decisions and implementation. Consolidation preserves every provider finding
and its provenance; a qualified decision owner validates and disposes the combined
set before the implementation owner applies the smallest sufficient fixes. The main
agent retains final acceptance. This adds no review cycle or mandatory agent panel.

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

For an active ready-PR cloud review wave with substantive or explicitly required
coverage, wait for both full initial cloud reviews to complete before consolidating,
validating findings or fixing. For later waves, wait for every due review in the
wave and retain only still-valid prior coverage under the
[shared completion barrier and allowance](references/coderabbit-review.md#ready-pr-coderabbit-and-codex).
Then consolidate duplicate and interacting findings and validate the combined
proposed correction against the whole affected contract.
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
