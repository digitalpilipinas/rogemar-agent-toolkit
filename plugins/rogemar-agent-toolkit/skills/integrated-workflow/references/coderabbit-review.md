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
An early light review may help after a risky increment, but is not a mandatory
review of every intermediate commit:

```bash
coderabbit review --agent --light --uncommitted
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
work. Apply the shared minimum-sufficient-fix and convergence rules. Fix required
defects, run affected checks and obtain due focused rereview; do not require endless
full reviews until the bot has no suggestions. Follow provider wait limits and
report failure/timeout honestly without narrating unchanged polling.

## Ready-PR CodeRabbit and Codex

Before readiness, complete the local gate and applicable UI/runtime evidence.
Do not launch or poll a cloud-review monitor for a draft. Draft state does not
promise that configured bots or CI stay silent; do not disable repository checks.

At the ready transition, verify PR head/base and inventory existing reviews.
Wait for the configured automatic GitHub CodeRabbit and Codex reviews. If a due
review has no valid equivalent queued, running or completed result, request it
through the installed, authorized provider controls. For supported comment routes:

```text
@coderabbitai review
@codex review
```

Post only the missing due request, within comment authority. Keep provider states
separate and confirm an actual review response for the intended candidate; a
posted command or acknowledgement is not a completed review. A required unavailable
provider blocks its recorded cloud QA/merge boundary until the owner's disposition.
Do not reinterpret a local Codex agent review as the GitHub Codex layer.

Full CodeRabbit rereview is appropriate for materially changed architecture,
permissions, sensitive data, migrations, concurrency or a substantially changed
comparison; request `@coderabbitai full review` only when due and justified.
Unchanged scope or repeated suggestions alone do not justify it. Respect equivalent
automatic reviews and branch-protection freshness requirements.

## Consolidation and completion

Use [review convergence](execution-loop.md#review-convergence) across CodeRabbit,
Codex and every other review/comment/check surface. Collect available findings,
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
