# Execution Loop

Use this reference after an approved plan exists. Repository instructions and stronger domain, security, regulatory, or release contracts take precedence.

## 1. Resolve context without a questionnaire

Infer from the current workspace, plan, and GoalBuddy board:

- repository root and applicable instructions;
- active task, sprint, and dependencies;
- remote target/default branch;
- existing branches and worktrees;
- repository validation commands;
- changed platform and specialist capabilities;
- exclusions and recorded mutation authority.

Ask one concise question only if a missing choice materially changes scope, safety, external data exposure, production behavior, or mutation authority. Plain-language owner instructions override inferred defaults.

Apply the compact invocation controls before work begins:

- Treat `Database or migrations` as the maximum permitted environment: `NONE`, `LOCAL`, `STAGING`, or `PRODUCTION`. A higher environment never authorizes work absent from the approved plan, and destructive operations still require exact scope and safety checks.
- Treat `Delivery to main` as the delivery route and authority ceiling:
  - `LOCAL ONLY`: do not commit, push, open a PR, or merge;
  - `DIRECT COMMIT AUTHORIZED`: commit and push directly to the verified target branch only when repository policy permits;
  - `BRANCH + PR, STOP BEFORE MERGE`: create the branch, commit, push, and open/update the PR, but do not merge;
  - `BRANCH + PR + MERGE AUTHORIZED`: run the branch/PR workflow and merge only after the applicable gate clears.
- Parse `Independent external review` as `DISABLED`, `OPTIONAL`, or `REQUIRED AT <named boundary>`, followed by the exact allowed provider/model list. Use `agent-collaboration-terminal` only when enabled.
- Treat omitted `Execution strategy` as `AGILE_FOCUSED`. Select `AGILE_CONTROLLED_PARALLEL` only when an approved dependency and ownership map proves every writer lane is independent; otherwise keep the main agent actively writing and integrating.
- Apply simulator and physical-device QA exactly as selected; do not infer a stronger or weaker gate. If the owner explicitly invokes simulator testing for a named change or boundary, treat it as `REQUIRED` there.

## 2. Respect the planning and GoalBuddy boundaries

`create-plan` is read-only and produces the plan. Goal Prep compiles `goal.md` and `state.yaml`, then stops. Execution starts only in `/goal` or through an explicit request to execute the approved plan.

When a GoalBuddy board exists:

- read its adjacent execution contract;
- treat `state.yaml` as truth;
- work only the active task;
- in `AGILE_FOCUSED`, keep one active implementation/integration owner; read-only Scout, Judge, review, research, and QA work may still run concurrently;
- in `AGILE_CONTROLLED_PARALLEL`, activate concurrent writer lanes only when the board records exact files or symbols, separate branch/worktree, verification, stop conditions, and a named main-agent integration owner for each lane; require main-agent reconciliation rather than treating supervision as an idle-only role;
- limit Workers to `allowed_files` and their declared verification;
- leave a receipt for done, blocked, or escalated work;
- let only the PM select the next task or complete the goal.

When no board exists, use the approved plan's first incomplete dependency-ready increment and keep a concise native plan.

## 3. Preflight the candidate

Before editing:

1. Inspect repository root, branch, HEAD, upstream, remotes, remote target branch, status, staged and unstaged changes, and untracked files.
2. Inspect relevant instructions, package scripts, lockfiles, environment-variable names, and nearby implementation and test patterns.
3. Confirm that the compact controls agree with the plan, board, repository policy, and current task. A conflict is a material decision; do not silently choose one.
4. Preserve unrelated user work and private material. Do not place secrets, environment files, credentials, ignored material, research, GoalBuddy control files, or generated diagnostics into commits or external review scope without explicit authorization.
5. For a new sprint, create a fresh branch and separate worktree from the verified target branch. Do not silently base a new sprint on unmerged work unless the approved plan defines a stacked dependency.

## 4. Implement one coherent slice

- Assign the active write scope from the selected strategy. In `AGILE_FOCUSED`, the main agent actively writes or integrates one coherent lane; do not create a shadow effort on the same symbols. In `AGILE_CONTROLLED_PARALLEL`, start only approved independent writer lanes in separate worktrees, each with exact scope, verification, stop conditions, and a named integration owner. On a shared dependency, migration, overlap, integration conflict, or blocker, stop affected lanes, reconcile, and resume as `AGILE_FOCUSED`.
- At package activation, route the proposed scope through the programme's reusable read-only Minimality Judge. Reuse the same Judge at pre-acceptance against the actual diff; do not create per-helper Judges or continuous monitoring. Classify verified suggestions by necessity, concrete current benefit, and actual effort/risk rather than reviewer labels. Include a beneficial optional quick win only when it is genuinely easy, localized, reversible, inside the approved product contract and recorded file scope, based on existing primitives, proportionately verifiable, and still low-risk after cumulative additions. Trust-boundary impact overrides line count. Stop for owner approval when a necessary correction genuinely needs significant complexity or scope expansion. Reject or defer significant optional, speculative, or unnecessary work without interrupting the owner unless the owner has separately prioritized it.
- Follow approved order and dependencies.
- Prefer existing repository primitives and patterns.
- Keep identity, authorization, credits, privacy, safety, and other sensitive decisions server-authoritative.
- Implement code and tests together.
- Add relevant counterexamples for authorization, ownership, privacy, legacy or malformed state, disabled behavior, duplicates, offline/restart, rollback, concurrency, media, migration, and recovery. Do not add irrelevant test permutations mechanically.
- Re-check scope before widening shared abstractions or touching files outside the active task.

## 5. Validate proportionally

Run focused checks while editing. Before delivery, run the repository-native checks that cover the final diff, such as lint, typecheck, unit/integration tests, build, database/RLS/migration checks, security scans, offline/recovery suites, and `git diff --check`.

Classify evidence honestly:

- `passed`: command or acceptance check completed successfully;
- `failed`: product or verification failure remains;
- `blocked`: required check could not run because a named prerequisite is unavailable;
- `skipped`: deliberately not applicable or outside scope;
- `deferred`: intentionally postponed under the approved acceptance policy.

Pre-existing failures must be distinguished from regressions introduced by the candidate.

## 6. Review the actual candidate

Review the complete frozen integrated candidate and tests, not a provider summary or individual Worker fragments. Use CodeRabbit according to [coderabbit-review.md](coderabbit-review.md). Run independent external review only when its compact control enables it; use the exact named providers/models through `agent-collaboration-terminal`. If multiple providers are named, parallelize only read-only review. One reviewer finding never overrides repository behavior or scope.

For an authorized read-only external review, prefer the terminal skill's managed-background/manual-approval profile with visible fallback. Select its opt-in code-review profile only when the objective explicitly reviews code, a diff, branch, or PR; `--mode review` alone does not activate code-review skills. Treat `needs_attention` as incomplete evidence; when the existing authority covers it, the main agent runs the recorded fallback once, waits for the native CLI to become ready, and submits only the frozen prompt. For code review, use the normalized finding contract and distinct provider emphases rather than asking every provider to repeat the same analysis. Keep CodeRabbit as a separate Codex-owned layer, never a nested provider action, and deduplicate provider findings against the canonical PR ledger before creating remediation work or PR comments.

Before push or PR creation, persist one review checkpoint in the active board or delivery receipt:

```text
risk: low | moderate | high
code-review-and-quality: approved | changes-required
local-coderabbit: passed | blocked:<reason> | owner-waived:<reason> | not-applicable:<reason>
github-coderabbit: pending-until-pr | passed | changes-required | unavailable:<reason>
```

- Resolve local CodeRabbit installation, version, authentication, data scope, and usage authority before publication rather than discovering them after the PR opens.
- For a high-risk candidate, do not push or open the PR while local CodeRabbit is merely blocked unless the owner explicitly authorizes authentication or explicitly waives that layer and accepts the recorded fallback.
- `code-review-and-quality`, Codex sub-agent review, Minimality, security review, tests, and CI are complementary evidence; none may be relabeled as or silently substituted for CodeRabbit.
- After the PR opens, let the automatic GitHub CodeRabbit review finish and reconcile valid issues before adding a final-CI trigger such as `run-ci`. A pending bot is not review readiness.
- Inventory all PR review surfaces after publication: top-level conversation comments, review submissions, inline threads and replies, reviewer states, and relevant check annotations. CodeRabbit is one required layer, not the whole inventory. Before final CI or merge, every actionable item must be fixed, explicitly rejected with current-code evidence, deduplicated, or deferred under an approved boundary; unresolved validated findings block the gate.

### Deduplicate PR findings before triage

Maintain one lightweight finding ledger for the lifetime of the PR in existing working state, the active board/receipt, or the PR conversation; do not create another artifact unless the repository requires it. For each canonical finding, retain only the information needed to prevent repeat work:

- semantic fingerprint: root cause + affected contract or symbol + requested outcome;
- canonical thread or comment and duplicate thread/comment IDs across all authors and review cycles;
- disposition: `fixed`, `rejected`, `rejected-overengineering`, `deferred`, `false-positive`, `awaiting-publication`, or `reopened`;
- last verified remote-head SHA plus the decisive test, code evidence, or owner decision.

Before triaging any new CodeRabbit, Codex, human, review-submission, or check-annotation item:

1. Match it semantically against the ledger. Similar wording, author, file, or line is not enough; distinct failure modes remain separate even when they touch the same symbol.
2. If it is a duplicate of a finding already fixed on the current remote head, rejected with evidence or as over-engineering, or deferred under an approved boundary, verify that disposition still applies, then reply immediately with the canonical item, head/evidence or approved boundary. State explicitly that it is not being considered again for this PR and ask the reviewer not to raise it again unless materially new current-head evidence shows a required defect or a substantially simpler high-value in-scope correction. Do not start another investigation, worker, implementation, test run, or owner-approval loop for that duplicate.
3. If the canonical fix exists only locally, reply `duplicate; fix awaiting publication`, link the canonical finding, and keep the thread open. Do not count it as a new issue or claim it fixed on the PR head.
4. Reopen and re-triage only when the current remote head still reproduces the failure, the canonical fix is absent or regressed, a material change makes its proof stale, new evidence materially invalidates the earlier disposition, or a previously deferred enhancement now has a demonstrably simpler high-value in-scope implementation. Record the new evidence once on the canonical entry. Repetition, rewording, or a different reviewer is not new evidence.
5. Keep one active remediation lane per root cause. Reply to duplicate threads before resolving them, but do not multiply commits, tests, rereview requests, owner questions, or status reporting for the same issue.

For every review thread and actionable non-thread review item, post a concise owner reply before manual resolution. Classify it as `fixed`, `rejected`, `duplicate`, or `deferred`, with current-code evidence. For a correction, first publish and verify the remote PR head; only then reply or manually resolve, citing that head SHA and the relevant validation or honest blocked/deferred evidence. During every inventory, detect bot-auto-resolved threads that lack an owner reply and backfill the disposition evidence before final CI or merge.

After every material correction push wave to an existing PR, verify the remote head and add one visible PR conversation update naming the head SHA, correction scope, validation results, and blocked/deferred evidence. Then request rereview from each applicable configured reviewer once unless that reviewer is already reviewing the current head; choose incremental or full review proportionately to risk.

Make the rereview scope explicit in that update:

- tell `@coderabbitai`, `@codex`, or the configured equivalents to exclude root causes already recorded as fixed, rejected, rejected as over-engineering, or deferred;
- permit a settled root cause to be raised again only with materially new evidence against the current head, a reproduced regression, or a demonstrably simpler high-value safe in-scope correction to a prior deferral;
- ask reviewers to focus on regressions introduced by the new correction wave and genuinely unique unresolved issues;
- link concise canonical PR dispositions when useful, but do not expose private tracker or local-only evidence; and
- keep each provider's required command on its own intact line. If a provider requires a standalone trigger comment, post the scope notice immediately before that command as one rereview wave rather than omitting the notice.

Use this compact shape and omit inapplicable reviewer commands:

```text
Head update: <verified remote-head SHA>
Delta: <concise correction scope>
Validation: <passed/blocked/deferred evidence>

Review scope: exclude root causes already fixed, rejected, rejected as over-engineering, or deferred. Reopen only with materially new current-head evidence, a reproduced regression, or a demonstrably simpler high-value safe in-scope correction. Focus on regressions from this update and genuinely unique unresolved issues.

@coderabbitai review
@codex review
```

Reviewer compliance is an optimization, not a gate. Bots may ignore the scope notice or lose prior context, so independently inventory and semantically deduplicate every response before analysis, implementation, testing, delegation, or owner escalation. Do not send another rereview request merely because a duplicate was repeated.

For canonical new, reopened, or still-unresolved findings from any reviewer or PR comment surface:

1. verify against current HEAD;
2. identify the concrete failure and impact;
3. classify necessity (`required`, `beneficial-optional`, `false-positive`, or `out-of-scope`) and actual effort/risk (`easy-low-risk` or `significant`), treating reviewer labels as advisory only;
4. implement the smallest valid required correction and consider a beneficial optional correction only when it is easy, low-risk, and remains inside the approved scope; seek bounded owner approval for significant necessary work, and reject or defer significant optional work;
5. add regression coverage when warranted;
6. rerun affected checks;
7. preserve rejected findings with a concise evidence-based explanation.

For a first-time optional enhancement, implement it only when it provides meaningful value to the current PR and is genuinely easy, localized, low-risk, aligned with the approved contract, and proportionately verifiable. Otherwise classify it as `rejected-overengineering` or `deferred`, reply explicitly that it is not considered for this PR, and ask CodeRabbit, Codex, or the originating reviewer not to raise it again without the new evidence required by the deduplication gate. Do not repeatedly return the same optional enhancement to the owner.

Avoid endless review loops. Normally converge through one `review -> validate -> fix -> test -> verify` cycle; repeat only for new material issues or a substantially changed candidate.

## 7. Platform acceptance

Select platform skills from repository reality:

- Expo/React Native: Expo and Argent workflows;
- web applications: the relevant browser, visual, accessibility, and web-build workflows;
- native iOS or macOS: the corresponding build, simulator, accessibility, and release workflows;
- backend/database: server-authority, migration, RLS, privacy, and security workflows.

For visible mobile changes, confirm the exact worktree, SHA, Metro project root, environment, feature flags, route, fixture/account state, and app build before visual judgment. Use element discovery before interaction and combine screenshots with structural or runtime evidence.

Apply the selected QA gates:

- Simulator `REQUIRED`: obtain governed simulator visual/accessibility evidence before the delivery gate; if unsupported or unavailable, block that gate.
- Simulator `CONDITIONAL`: require it only when a supported project changes visible UI or an interactive flow.
- Simulator `DEFERRED`: do not run it; report it as deferred.
- Physical device `REQUIRED BEFORE MERGE`: do not merge without the required device evidence.
- Physical device `DEFERRED UNTIL BUILD`: report it as deferred and do not represent it as a merge pass.
- Physical device `NOT APPLICABLE`: record why it is outside the project or change scope.

Before accepting a platform-visible or interactive package, persist a simulator checkpoint in the active board or delivery receipt:

```text
simulator-selection: required | conditional | deferred | not-applicable:<reason>
simulator-trigger: triggered:<reason> | not-triggered:<reason> | not-applicable:<reason>
simulator-evidence: passed:<worktree/SHA/runtime/route/profile> | blocked:<reason> | deferred:<approved reason> | not-applicable:<reason>
```

- Resolve the conditional trigger from the actual diff. Visible UI or interactive-flow changes in a supported project trigger it; backend-only or documentation-only work ordinarily does not.
- An explicit simulator-testing invocation is `required` for its named scope and cannot be downgraded to an untriggered conditional check.
- `passed` requires evidence from the exact candidate worktree and SHA with the runtime, route, fixture/account state, and platform profile identified. Source tests, screenshots alone, or a stale/ambiguous runtime are not substitutes.
- A required or conditionally triggered check that is not passed blocks the selected package-acceptance, final-CI, or merge boundary. Continue only when the approved plan or owner explicitly records a deferral or waiver for that exact boundary.
- Keep simulator, browser, manual assistive-technology, and physical-device evidence separate; one does not silently satisfy another.

If a valid runtime cannot be established, do not inspect a stale or ambiguous UI. Record platform QA as blocked or deferred and continue only if that evidence is not a required merge gate.

## 8. Prepare and deliver

Before commit:

1. inspect status and the complete diff;
2. confirm plan increments as complete, partial, or not started;
3. stage only intentional paths;
4. run `git diff --check`, staged secret review, and final applicable validation;
5. ensure excluded material remains untracked or unstaged.
6. confirm the review checkpoint exists and that any high-risk local CodeRabbit block has an explicit owner decision before publication;
7. confirm the applicable simulator checkpoint is resolved for the current delivery boundary.

Prefer one coherent sprint commit unless repository policy or the plan calls for multiple atomic commits. Record scope, important compatibility or migration notes, feature flags, validation, and deferred QA in the commit or PR description as appropriate.

Follow the selected delivery route:

- For direct-main delivery, first verify repository policy permits it, inspect the exact target branch, run the same applicable pre-commit gates, commit only intentional files, push, and verify the remote target contains the pushed SHA.
- For branch/PR delivery, verify the remote feature branch contains the pushed SHA, open or update the PR, run the configured review loop, and keep unexplained failures visible. Stop before merge when instructed. When merge is authorized, merge only after the gate is clear, verify the actual target branch contains the merge result, and run required exact-target checks from a clean candidate.
- Before a final-CI trigger or merge, refresh the PR inventory and confirm no newly added or still-unreconciled actionable conversation comment, review submission, inline thread, reviewer state, or check annotation remains.

Do not claim deployment merely because code merged.

## 9. Advance or stop

Update the GoalBuddy receipt and board when applicable. Continue to the next safe active task rather than stopping after a single sprint when the approved programme remains incomplete.

Stop and request direction only for:

- missing mutation or production authority;
- a material scope or product decision;
- destructive or irreversible action not already authorized;
- unsafe or ambiguous repository state;
- required credentials or external data access;
- a required acceptance capability that has no valid fallback;
- repeated verification failure whose smallest safe resolution changes scope.

The final task is a skeptical audit against the original goal oracle, receipts, actual diff history, merge state, and required acceptance evidence.
