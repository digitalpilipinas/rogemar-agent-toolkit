# Execution Loop

Use after approval for the active slice. The entry skill defines change classes,
review requirements and delivery strategy; this reference defines their evidence
and execution. Preserve stronger repository/domain gates and exact owner authority.

## 1. Resolve the slice and authority

Inspect the approved plan, repository instructions, current root/branch/HEAD,
upstream and target, staged/unstaged/untracked changes, existing worktrees and PRs,
validation commands, affected platforms and recorded exclusions. Read relevant
lockfiles, environment-variable names and nearby patterns without exposing secrets.
Preserve unrelated, ignored, private, generated and control files.

With GoalBuddy, follow its execution contract and `state.yaml`: only the PM selects
the next active task or completes the goal. Goal Prep prepares the board and stops.
Without a board, resume the first incomplete dependency-ready approved increment.
Do not invent a new board, replan or restart completed work.

For long runs, follow the shared [context guidance](../../workflow-orchestrator/references/context-efficiency.md)
and [GoalBuddy handoff](../../workflow-orchestrator/references/stage-routing.md#goalbuddy-context-handoff)
when applicable. Carry changes since the last accepted receipt alongside still-valid
constraints, source identity, dependency evidence and next action. Refresh changed
or uncertain state. Preserve original logs and decisive diagnostics, and consume
already-delivered results once. This changes no review gate or final coverage audit.

Resolve compact controls from the owner or approved plan. Invocation for approved
implementation defaults to `BRANCH + PR + MERGE AUTHORIZED`; record the route once
and continue without per-step permission requests:

- `LOCAL ONLY`: no commits, pushes, PR creation, remote review comments or merge.
  Local review remains allowed and required for substantive local-only acceptance,
  within the applicable provider/data/usage authority.
- `DIRECT COMMIT AUTHORIZED`: explicit owner choice to commit/push directly to the
  verified target, subject to repository policy. Never infer it from project size.
- `BRANCH + PR, STOP BEFORE MERGE`: authorized branch commits, pushes and PR
  preparation; ready-PR review/remediation within the recorded review authority;
  stop at verified readiness without merging.
- `BRANCH + PR + MERGE AUTHORIZED`: the same flow, followed by merge only after
  applicable gates clear and exact-target verification.
- The default covers scoped commits/pushes, PR creation or updates, ready
  transition, configured PR review requests, in-scope remediation, applicable
  authorized CI and safe merge with exact-target verification. Reuse the task PR.
  Plan approval, automatic skill selection, or discussing/editing the skill
  alone does not invoke its publication route. Require an explicit execution
  invocation or separate delivery authorization. Stricter repository requirements
  for separate publication/merge authority override the default.
- Explicit local-only, no-push, draft-only or stop-before-merge restrictions take
  precedence until changed by the owner. Ask once for a material conflict, not
  again for steps already covered by the effective route.
- Required checks, reviews, repository approvals and trusted scope evidence remain
  mandatory. Never manufacture owner approval or bypass checks. Prepare concrete
  owner-only artifacts before reporting the specific blocker. Inspect automation
  before push, PR or merge; stop before unapproved deployment, store/OTA
  publication, destructive operations or expensive builds.
- Database scope is the maximum permitted environment. Production changes,
  destructive work, provider data/credit usage and deployment need their own
  applicable authority; none follows from branch or PR creation alone.

For branch delivery, begin a new independent vertical slice from the verified
remote target in its own branch/worktree. Resume the same branch and optional
draft across its sprints and commits. Do not create per-sprint PRs automatically.
Honor an explicit stacked or multiple-PR plan without silently rebasing/replanning.
For direct-main delivery, follow that route without manufacturing a PR or separate
sprint branch; preserve user work and policy. Local-only work stops locally.

## 2. Build and validate continuously

The orchestrator selects one native/portable engineering playbook and justified
skills; apply the selected harness's routing contract when dispatching. Forge's
artifacts supplement the approved plan and cannot activate tasks or pass gates.

For new workers, use the orchestrator's
[sub-agent naming](../../workflow-orchestrator/references/subagent-naming.md)
after native profile qualification, through supported naming controls or the
handoff fallback. Reuse the existing receipt for full profile IDs,
mode and observed evidence; names do not establish verification or alter gates.

Default to one main-agent writing/integration lane. Concurrent read-only support
may earn its cost; concurrent writers require approved independent branches and
worktrees, exact files/symbols, verification, stop conditions and reconciliation.
Apply the orchestrator's [automatic strategy selection](../../workflow-orchestrator/SKILL.md#automatic-execution-strategy).
Pause and reconcile affected lanes on shared dependencies; preserve their work
and continue unaffected lanes only when independence remains established.

Use existing primitives and patterns. Keep sensitive decisions server-authoritative.
Implement coherent increments with focused tests and relevant counterexamples:
ownership/authorization, malformed or legacy state, retries/duplicates, disabled
behavior, offline/restart, concurrency, migration and recovery where affected.
Do not mechanically add every permutation or widen the approved contract.

For visible or interactive changes, follow [UI/UX implementation](ui-ux-implementation.md)
from baseline through accessible behavior and applicable runtime checks. Early
review is allowed; missing required UI evidence remains explicit and does not
establish final readiness. Reuse the existing scope/correctness reviewer where
appropriate rather than creating separate Judges for every implementation or QA helper.

Run focused checks during work and the repository-native checks covering the final
integrated diff before slice acceptance. Distinguish pre-existing failures from
regressions. Preserve required checks even for the small-change exception.

With publication authority, meaningful intermediate commits and feature-branch
pushes may accumulate while the slice is branch-only or draft. Inspect/stage only
intentional content and run applicable commit-time checks. Do not claim slice
acceptance, start PR monitoring or require a full local CodeRabbit run per commit.
A stricter project checkpoint still applies. Local full-slice review must pass
before ready-for-review, substantive direct-main publication or final local-only
slice acceptance, unless the owner explicitly waives that layer.

## Gate and evidence contract

Define each gate once in the existing board/receipt, rather than separate reviewer
or test ledgers. Retain only:

```text
gate: <check or named provider>
requirement: required | optional | not-applicable:<reason>
source: <owner instruction, repository policy, approved plan or workflow default>
trigger: <affected behavior or explicit request>
owner: <implementation owner or evidence provider>
boundary: <commit, slice-acceptance, ready-for-review, direct-main-publication, final-CI, merge>
state: pending | running | passed | failed:<evidence> | blocked:<prerequisite> | unavailable:<optional reason> | deferred:<owner decision> | not-applicable:<reason>
candidate: <comparison base, content identity and scope>
evidence: <result/artifact, environment and relevant limitations>
```

`failed` means an executed check exposed a failure. `blocked` means required
prerequisites are unavailable. Optional unavailability does not become a gate
because the change is high-risk. A waived or deferred requirement retains the
owner's disposition and never becomes `passed`. Required failures remain binding;
continue safe independent work but do not cross the affected boundary.

Record local CodeRabbit, GitHub CodeRabbit and GitHub Codex separately. Resolve
requirements from the entry skill, route and stronger project rules: substantive
local review is required; substantive ready-PR cloud CodeRabbit and Codex are
required; the small-change exception makes those layers optional unless otherwise
mandated. PR-only layers are not applicable to explicitly authorized direct-main
or local-only delivery. Additional external providers are governed by their exact
selection, data/usage authority and named boundary. `DISABLED` for additional
providers does not cancel the default CodeRabbit/Codex layers.

During branch-only/draft development, cloud layers are `pending` for the future
ready/merge boundary, not a reason to halt unfinished implementation. At readiness,
check all applicable local gates before opening ready or converting the existing
draft. Cloud review then governs final-CI/merge or stop-before-merge readiness.
Never report `requested`, `running`, thread resolution or a provider launch as a pass.

### Candidate identity and evidence reuse

Identify the exact comparison base, intended paths, file contents and modes,
including additions/deletions and explicitly included untracked files. For a
committed candidate use its commit/tree identity. For uncommitted work retain a
content manifest/hash or frozen patch plus hashes of intended additions, together
with base and scope; a HEAD SHA or worktree path alone is insufficient. Keep private
content and local-only records out of external review and PR comments.

Record runtime/build, route, fixture/account state and platform/viewport where
those affect a check. A content hash is identity, not proof the check ran.
Before commit, compare staged content to the reviewed candidate. Reuse a result
only when contents, comparison scope, relevant dependencies/environment and its
acceptance requirement remain equivalent. Committing unchanged contents does not
alone require another local review. Preserve the original evidence identity and
record equivalence rather than relabeling the old result as a new-SHA execution.
Provider freshness rules, branch protections and required CI still apply.

## 3. Ready-PR handoff and monitoring

A draft is already an open PR. Build the full approved vertical slice before
creating a ready PR or marking its draft ready; multiple sprints may contribute.
Use [CodeRabbit review](coderabbit-review.md) for the complete local candidate.
When local gates clear, verify the published feature head, base, aggregate diff
and PR state, then make the authorized ready transition.

Do not start, poll or schedule a PR-review monitor for a draft. Existing GitHub
checks or bots can still run; do not disable required automation or assume draft
status silences it. Carry any already known urgent defect forward without waiting
for readiness. At ready transition, inventory all existing review evidence so a
valid equivalent automatic review is not requested twice.

For a ready PR, active authorized delivery includes observing review/check
progress and bounded remediation. Use available native events or bounded waits;
avoid repeated full inventories and unchanged status narration. Inventory the
complete conversation, review submissions/states, inline threads/replies, all
reviewers and relevant check annotations, including auto-resolved items. GitHub
CodeRabbit and Codex are required distinct layers for substantive PRs; additional
named providers contribute to the same record.

Follow the [full initial requests, completion barrier and cloud allowance](coderabbit-review.md#ready-pr-coderabbit-and-codex).
Both initial cloud reviews cover the full PR; equivalent automatic full reviews
count without duplicate tags. Preserve the per-provider allowance across pushes
and resumes. Verify the actual response, scope and head; a request alone is not
evidence. Apply [external-provider handling](supporting-methods.md#external-review-providers)
only when additional providers are selected. A required provider timeout blocks
its boundary; optional unavailability may use a disclosed fallback.

Monitoring stops at verified completion of the allowed boundary, PR closure,
return to draft, cancellation or an actionable blocker requiring owner input.
When returning to draft, preserve findings and resume implementation without
polling; reinventory at its next ready transition. With stop-before-merge authority,
finish at verified readiness and report the handoff without merging. Recurring
follow-up after the active task yields requires an explicit scheduling request
and the harness's supported scheduler; do not create a background job by default.

### Review convergence

The completion barrier below applies to active ready-PR **cloud** review waves.
Local and pre-ready reviews reuse the consolidation, validation and minimum-fix
methods without waiting for cloud reviews; their existing cadence is unchanged.

1. **Collect and wait:** obtain both full initial cloud reviews for the intended
   candidate/base before consolidating, validating findings or applying fixes.
   While either is pending, collect raw artifacts and monitor status only; no
   early finding triage or remediation. For follow-up waves, wait for every due
   review in that wave while retaining still-valid prior coverage. Follow the
   completion barrier above for unavailable, partial or stale results; a timeout
   is not a pass and an exception requires explicit owner instruction.
2. **Consolidate and validate together:** group findings by semantic root cause,
   affected contract and failure scenario. Assess interacting recommendations,
   contradictory fixes, affected callers and cumulative complexity against the
   whole approved behavior. Preserve distinct failure modes even in the same file.
   Reproduction or decisive source/contract evidence must establish necessity;
   a reviewer label, repetition or speculative future support is insufficient.
3. **Remediate:** the implementation owner batches available validated in-scope
   corrections into one coherent wave. Reviewers remain read-only. Implement the
   smallest sufficient solution and run affected checks/local review as warranted
   before publishing. Multiple commits may form one push. If no required change
   exists, record dispositions and proceed; do not invent a fix wave or rereview.
4. **Verify and rereview:** verify the remote head and publish one concise update
   with correction scope and validation. Recheck affected UI/runtime behavior.
   Obtain only due, proportionate rereview within the shared per-provider cloud
   allowance, counting equivalent automatic runs. Exhaustion blocks further
   requests pending an explicit extension; it never grants acceptance.
   Further fix waves require a demonstrated required defect or explicit owner
   reprioritization. This never waives required checks, approvals or unresolved defects.

Material change means altered runtime behavior, API/data/permission contracts,
compatibility, migrations, executable configuration or validity of required
evidence. Judge effects, not extensions or line count: documentation may be agent
policy and tests can weaken assurance. Pure wording or formatting with no such
effect gets focused verification without another manual review request unless
required. Observe automation that still runs; never weaken CI or stale-approval
rules to reduce noise.

### Findings and minimum sufficient corrections

Keep one canonical disposition per root cause/contract/failure scenario in the
existing board, receipt, working state or PR conversation. Retain canonical and
duplicate comment IDs, current-head evidence, necessity/impact, proposed minimal
correction and disposition: `fixed`, `awaiting-publication`, `rejected`,
`rejected-overengineering`, `false-positive`, `deferred` or `reopened`.

Validate all actionable surfaces, including recommendations from CodeRabbit,
Codex, Antigravity, Grok, Junie, humans and check annotations. Resolved means
reconciled with evidence, not that every suggestion was implemented.

- Required defects get the smallest reliable correction. Significant necessary
  scope or complexity expansion needs an explicit bounded owner decision.
- A beneficial optional correction may join the batch only when valuable now,
  easy, localized, reversible, within the approved product/file scope and low-risk
  cumulatively. Prefer existing primitives; do not sneak in new dependencies,
  infrastructure, migrations, providers, flags, abstractions or material testing
  burden. Sensitive trust-boundary impact outweighs a tiny diff.
- Reject false positives and unnecessary complexity with concise evidence. Defer
  out-of-scope enhancements with a concrete revisit trigger. Do not reopen them
  for rewording, another author or a new thread alone.
- Reopen only for a reproduced current defect/regression, a missing prior fix,
  changed contracts invalidating proof, or materially new evidence of a simpler
  valuable in-scope correction. Reassessment alone does not authorize another
  optional enhancement wave.

Verify duplicates against the existing disposition before starting another
investigation, worker, test run or owner question. A local fix remains
`awaiting-publication`; do not manually resolve its PR thread until the published
head contains it. Before manual resolution ensure a concise disposition or link
already exists; backfill auto-resolved items only when missing or ambiguous.
Avoid acknowledgement-only replies.

At each remediation push, use one authorized PR update with the verified SHA,
delta, validation and canonical dispositions. Ask due reviewers to focus on new
required defects and regressions, excluding settled findings without new evidence.
Keep provider commands intact; post only missing due triggers. Bot compliance is
an optimization: independently deduplicate every response even if it ignores the
scope notice. Optional completeness cannot prolong delivery once acceptance passes.

## 4. Platform acceptance

Infer actual platform tools: web browser QA, Expo/React Native/Argent, native
simulator/emulator/device tools, or backend/database verification as applicable.
For mobile UI, identify the exact candidate, app build, Metro/project root,
environment, flags, route, fixtures/account and device profile before judging.
Use element discovery before interaction and combine rendered and runtime evidence.

Record the selected simulator checkpoint within the shared gate record:

```text
simulator-selection: required | conditional | deferred | not-applicable:<reason>
simulator-trigger: triggered:<reason> | not-triggered:<reason> | not-applicable:<reason>
simulator-evidence: pending | running | passed:<candidate/runtime/route/profile> | failed:<evidence> | blocked:<prerequisite> | deferred:<approved reason> | not-applicable:<reason>
```

- Required simulator QA applies at its named boundary; unsupported or unavailable
  required runtime blocks that boundary. Conditional QA triggers only for supported
  projects with visible UI or interactive changes. An explicit simulator request
  makes it required for its named scope. Do not silently strengthen/weaken policy.
- An executed run exposing a defect is `failed`; an unavailable or ambiguous
  candidate runtime is `blocked`. Fix valid defects and rerun affected checks.
  Source tests, screenshots alone and stale runtime do not substitute for proof.
- Required or triggered simulator QA must pass before the recorded acceptance,
  final-CI or merge boundary unless the owner explicitly defers/waives that exact
  boundary. Deferred evidence remains deferred. Continue other safe work meanwhile.
- Keep browser, simulator, manual assistive-technology and physical-device evidence
  distinct. Device `REQUIRED BEFORE MERGE` blocks merge; `DEFERRED UNTIL BUILD`
  remains deferred; `NOT APPLICABLE` needs a truthful scope reason.

## 5. Deliver and audit the outcome

Before each commit, inspect the complete intended staged contents, diff/secret
checks and applicable commit-time gates. Preserve exclusions and content parity.
Use coherent commits throughout the slice; do not require one commit per sprint.

Before final local acceptance, ready-PR handoff or substantive direct-main
publication, confirm the applicable local review and runtime gates for the exact
candidate. Only a required blocked review needs owner disposition; optional
unavailability never becomes a gate. Earlier authorized branch/draft commits may
continue under their own checkpoints without claiming final acceptance.

For direct-main delivery, verify target identity/policy, pass required local gates,
commit/push intentional content and verify the remote target contains the intended
result. PR-only reviews and PR monitoring are not applicable. For branch delivery,
verify each remote push; after the slice becomes ready, reconcile reviews and
required CI through the authorized boundary. Before final-CI triggers or merge,
refresh all review surfaces and ensure no unreconciled actionable item remains.

Merge only when authorized and required findings, checks and approvals are
satisfied. Verify the actual target contains the merge result and run required
exact-target checks from a clean candidate. Neither merging nor a SHA proves a
deployment. Record passed, failed, blocked, deferred and not-applicable evidence
truthfully, with provider identities kept separate.

Advance the next safe approved task after receipts; do not stop merely because a
sprint ended when the slice/programme remains authorized and incomplete. At the
final boundary, the main agent/PM audits the original outcome against the actual
integrated changes, required evidence and delivery state. Apply GoalBuddy's Judge/PM
contract where present without manufacturing another mandatory agent elsewhere.
Stop for missing authority, material scope drift, unsafe repository state,
unavailable required prerequisites or failures whose safe resolution changes scope.
