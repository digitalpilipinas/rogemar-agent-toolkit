# CodeRabbit Review

Preserve two separate evidence layers for substantive branch delivery:
**local CodeRabbit on the complete slice**, then **GitHub CodeRabbit on the ready
PR**, alongside the separate GitHub Codex review. The entry skill's small-change
exception and explicit owner/project gates govern applicability. Direct-main and
local-only delivery retain substantive local review; PR-only layers do not apply.
No layer replaces tests, domain acceptance or required independent evidence.

## Availability, scope and identity

When selected or required, check the CLI version and supported flags with
`coderabbit --version` and `coderabbit review --help`; prefer the explicit command
over an ambiguous `cr` alias. Check authentication with the supported agent status
command, such as `coderabbit auth status --agent`. Apply relevant repository
instructions/configuration through supported options.

Verify installation, authentication, scope and existing usage authority early.
Do not install/authenticate, pass credentials, expose ignored/private files or
spend additional paid credits implicitly; never add `--use-credits` by default.
A blocked required local layer prevents its named final-acceptance/ready/direct-main
boundary unless the owner explicitly waives it. A missing optional layer does not
block small-change work. Native review is distinct evidence, not CodeRabbit proof.

Freeze the exact allowed candidate, comparison base and contents using the
[shared identity contract](execution-loop.md#candidate-identity-and-evidence-reuse).
Keep unrelated dirty work out of the review. Use an isolated authorized candidate
when CLI selection cannot exclude it. Include untracked files only when those
exact additions are intentional and authorized for external review; do not infer
that every untracked file belongs to the change.

## Local cadence

Focused tests and coherent commits continue during branch-only/draft development.
An early full review may help after a risky increment, but is not a mandatory
review of every intermediate commit:

```bash
coderabbit review --agent --uncommitted
```

At completion of the vertical slice, obtain one complete local review of the
aggregate candidate before final local acceptance, creating a ready PR, marking
a draft ready, or substantive direct-main commit/push. Choose the supported scope
that covers the whole intended change:

```bash
coderabbit review --agent --uncommitted
# Or, for the complete committed feature branch:
coderabbit review --agent --base <verified-target-branch>
```

Use `--base-commit <sha>` when that frozen baseline is the correct comparison.
An uncommitted-only review is insufficient if earlier feature commits also belong
to the slice. Likewise, a branch review must cover any intended final dirty
changes through a supported scope or a fully committed candidate. Verify the
actual reviewed file/diff coverage; flags alone do not establish it. Add
`--include-untracked` only for exactly authorized additions. A path-restricted
review is adequate only for genuinely isolated work, including affected callers.

Do not automatically run both uncommitted and branch reviews on equivalent
contents. If the first complete review already covers the same aggregate diff,
baseline, dependencies and scope, record content equivalence after commit and
reuse it where repository policy permits. If scope differs or materially changed,
obtain the missing review coverage. This reuse never removes the separate GitHub
CodeRabbit or GitHub Codex layer required on a substantive ready PR.

Record completion and validate findings against current behavior. Classify
required defects, beneficial optional improvements, false positives and out-of-scope
work. Apply the shared minimum-sufficient-fix and local consolidation methods;
the cloud completion barrier does not apply to local or pre-ready reviews. Fix required
defects, run affected checks and obtain due review coverage; do not require endless
full reviews until the bot has no suggestions. Every invoked local CodeRabbit
review uses its own full procedure on the complete agreed candidate, without
`--light` or sampling. The cloud allowance below does not change local cadence or
impose a local cycle cap. Explicitly selected terminal code reviewers likewise
review their full agreed candidate through `agent-collaboration-terminal`.
Follow provider wait limits and
report failure/timeout honestly without narrating unchanged polling.

## Ready-PR CodeRabbit and Codex

Before readiness, complete the local gate and applicable UI/runtime evidence.
Do not launch or poll a cloud-review monitor for a draft. Draft state does not
promise that configured bots or CI stay silent; do not disable repository checks.

At the ready transition, verify PR head/base and inventory existing reviews.
The initial GitHub CodeRabbit and GitHub Codex reviews must both cover the full
agreed PR diff against its base, including relevant surrounding code. Start with
full review; do not save it for a final pass after a series of standard reviews.
When an initial request is due, use the supported provider command, separately:

```text
@coderabbitai full review
```

```text
@codex review the entire PR diff against its base, including all changed files and relevant surrounding code.
```

Codex uses its native `@codex review` trigger with an explicit full-scope request;
do not invent an `@codex full review` command or claim a separate full-review mode.
Check actual response scope and limitations; request wording is not coverage proof.
See the official [CodeRabbit commands](https://docs.coderabbit.ai/reference/review-commands)
and [Codex GitHub review guide](https://learn.chatgpt.com/docs/third-party/github).

Reuse an equivalent full automatic review already queued, running or completed;
do not duplicate it with a tag. Confirm its scope rather than assuming every
automatic or earlier incremental result is full. Post only missing due requests
within comment authority. Preserve repository triggers, including PR-open plus
manual-tag configurations; a push or commit does not itself prove a review starts.

### Both-reviewers completion barrier

Before consolidating, validating findings or making reviewer-driven fixes, require
completed full initial reviews from **both GitHub CodeRabbit and GitHub Codex**
for the same intended candidate/base. While either is pending, only collect raw
artifacts and monitor status; do not start partial synthesis, finding validation,
thread disposition or remediation from the faster provider. Ordinary configured
CI and unrelated safe work may continue without changing the review candidate.

Keep provider states and reports separate. Completion requires an actual terminal
review response with adequate scope; a command, acknowledgement, green check,
timeout or quota notice is insufficient. A completed review may contain blocking
findings: completion is not approval. If either provider is unavailable, failed,
partial or stale, preserve the other's report and block consolidation/remediation
and the recorded cloud QA/merge boundary until the gap is resolved or the owner
explicitly changes that requirement. Do not silently bypass this barrier, even
for an urgent finding; surface the need for an explicit exception. A local Codex
agent review cannot substitute for the GitHub Codex layer.

### Cloud review allowance

For each PR, allow **two accepted review runs per provider** by default: the
initial full review and at most one justified follow-up. This is an allowance,
not a mandatory number of runs. With automatic initial reviews, ordinarily only
one follow-up tag per provider is needed. Apply it separately to GitHub CodeRabbit
and GitHub Codex; it does not limit local CodeRabbit or selected terminal reviewers.

Carry counts, provider/run or request identifiers, reviewed head/base and scope,
status, last trigger and any owner extension in the existing receipt or PR record.
Count automatic and manual runs alike; queued/running accepted runs reserve a
slot, and accepted runs that later fail or become stale still count. These are
workflow counts, not claims about provider billing. Never reset counts on commits,
pushes, draft/ready transitions, resumed sessions or changed review wording.
Recover history before requesting another run; unknown history is not zero.

Do not retag an equivalent queued/running/completed review. Record a quota rejection
or uncertain dispatch without a retry loop; inspect whether a run was accepted
before any retry. A rejected request is not completed evidence or permission to
try repeatedly. Wait for the actual prerequisite or obtain an owner disposition.

After both initial reviews complete, consolidate and validate all findings, batch
required fixes, run affected checks/local reviews as warranted, and publish one
correction wave. Use the remaining slot only for a provider whose required coverage
needs refreshing; do not automatically retag both or request another run for pure
wording changes, settled suggestions or optional completeness. A CodeRabbit
follow-up may use `@coderabbitai review` for the changed commits. Use
`@coderabbitai full review` again only when material change invalidates whole-PR
coverage; either command consumes the same remaining slot. Codex follow-ups retain
the supported `@codex review` trigger and state the changed scope.

For a follow-up wave, wait for every review requested or otherwise required for
that wave before consolidating, validating findings or fixing again. Carry a
previous provider result only when its coverage remains valid for the final
candidate; do not force a redundant rerun merely to form a pair. Preserve both
initial full reports and explain any content-equivalence or delta coverage.

A third or later run requires a concrete remaining risk or required evidence gap
and an explicit owner extension naming the provider and additional allowance.
If the allowance is exhausted, stop new review requests and report the exact gap.
Required fixes, tests, freshness rules and repository approvals still apply;
exhaustion never makes a candidate safe to merge or silently waives missing review.
Do not purchase credits, change bot settings or reopen a replacement PR to evade it.

## Consolidation and completion

Use [review convergence](execution-loop.md#review-convergence) across CodeRabbit,
Codex and every other review/comment/check surface. Enforce the completion barrier
above before consolidating or validating findings and before reviewer-driven fixes;
deduplicate semantic causes and validate the combined correction against the
whole affected behavior before routine edits. The implementation owner batches
the smallest sufficient fixes and proportionate checks. Rejected over-engineering
and approved deferrals remain visible dispositions rather than recurring work.

After a correction wave, verify the remote head, publish one concise update and
request only missing due rereviews. Inventory new and auto-resolved comments;
before manual resolution, link a clear canonical disposition and verify published
fixes. Never mark a local unpublished fix as resolved remotely. Bots may ignore a
scope notice, so the owner still deduplicates their responses independently.

Before a final-CI trigger or merge, reconcile all actionable findings and required
review results on the applicable candidate. Do not trigger final CI while required
cloud reviews are pending; ordinary configured CI may run concurrently. Valid
required defects block acceptance regardless of a provider's severity label or
approval. Optional improvements cannot prolong delivery without owner reprioritization.

Do not default to bot autofix or use bot approval/thread resolution as proof of
correctness. Any authorized low-risk autofix still needs actual diff and test
verification. Preserve required automation; changing bot settings or pause/resume
needs explicit authority and cannot bypass review. Stop monitoring at the allowed
completion boundary, closure, return to draft, cancellation or actionable block.
