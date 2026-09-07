---
name: code-review-and-quality
description: Review a code change across correctness, readability, architecture, security, and performance. Use for an independent review, quality assessment, or reconciliation of reviewer findings; own one evidence-based verdict while native reviewers and CodeRabbit remain optional provider routes.
---

# Code Review and Quality

Own one review and one finding record. Evaluate whether the change fulfills its
contract and improves or preserves code health. Prefer actionable defects and
demonstrable structural regressions over preferences or speculative concerns.

## Establish the target

Read applicable instructions and the requested requirements. Resolve the exact
candidate and comparison baseline before reviewing. For a branch, compare the
changes since its merge base with the intended base unless the user specifies
another comparison. For local work, identify which staged, unstaged, and new
files are in scope; preserve unrelated and private material.

Inspect the whole in-scope diff, relevant tests, and enough surrounding code and
callers to understand the changed paths. Continue after the first finding. If
the target is empty or unavailable, report that state rather than inventing a
review. Do not switch, stash, reset, or edit the user's work merely to read it.
Review alone grants no fix, commit, publication, or merge authority.

## Apply five axes

Scale depth to the change and actual risk. These are lenses for one pass, not
five mandatory reports or five reviewer agents.

| Axis | Check |
| --- | --- |
| Correctness | Requirements, error paths, state transitions, affected callers, races, and behavior tested against the intended contract. |
| Readability | Understandable names and flow, necessary comments, unnecessary indirection, and complexity introduced by the change. |
| Architecture | Ownership, module/type boundaries, reuse, compatibility, and whether an abstraction removes complexity instead of moving it. |
| Security | Relevant trust boundaries, authorization, input/output handling, sensitive data, secrets, and changed dependencies. |
| Performance | Work growth, bounded queries and collections, blocking work, hot paths, and resource lifetime; measure before claiming a regression size. |

For structural findings, identify the specific burden and propose the smallest
remedy: reuse an existing helper, remove an unnecessary layer, model a repeated
state distinction, or move logic to its owner. File length and line count are
inspection signals, not automatic blockers. Preserve justified compatibility
code, security checks, and published interfaces when proposing simplification.

For dependency changes, inspect relevant release/migration notes and the actual
lockfile/transitive changes. Check behavior where the dependency is used. Keep
coupled upgrades together when needed; avoid unrelated upgrade or refactor work
merely to satisfy a review preference.

## Use evidence and independent judgment

Verify the author's check results against the reviewed revision and inspect
whether tests could catch a wrong implementation. Use the installed
`code-review-tests` companion for deeper test and counterexample selection when
useful; contribute its results to this same review. If unavailable, still check
the affected behavior, its failure cases, and the existing test coverage.

An independent reviewer is useful for consequential ambiguity, unfamiliar
boundaries, risky changes, or a required project gate. The selected orchestrator
decides whether and how to dispatch through the active harness. Give a reviewer
the requirements, baseline/candidate, bounded scope, relevant raw evidence, and
finding format. Avoid priming it with the author's preferred verdict. Keep the
reviewer read-only and the final reconciliation with the review owner.

Do not require a different model, external provider, or multiple agents. A
single-agent review is valid when sufficient; disclose the absence of independent
review when material. A required independent gate remains unmet if unavailable.
Native Codex/Cursor/Grok reviewers and CodeRabbit keep their own runtime and
authentication contracts. Run a provider only when selected, available, and
authorized; never label local analysis as that provider's result.

## Reconcile findings once

Use the existing plan or PR finding ledger if present; otherwise a concise list
in the review is enough. Combine reports about the same cause into one entry,
retaining provider IDs, evidence, and any disagreement. Do not restart a full
review for each contributing skill or silently replace an existing finding ID.

Each actionable finding should include:

- Priority, location, and the violated requirement or invariant.
- Affected scenario, why it fails, and a reproduction or concrete code path.
- The smallest useful correction and the check that would confirm it.

Use the repository's priority scheme. If none exists, label **Critical** for a
severe release-blocking defect, **Required** for an actionable defect or material
regression, and **Optional** for non-blocking improvement. Separate suggestions
from defects. For change reviews, distinguish issues introduced or worsened by
the candidate from pre-existing issues; include broader debt only in a requested
audit or as clearly scoped context.

Validate feedback before acting on it. Mark each item open, fixed with evidence,
rejected with a reason, or explicitly deferred with an owner when needed. Keep
existing ledger status names when they already express those states. A provider's
confidence or a clean badge is evidence input, not authority to change scope.
After fixes, recheck the affected behavior and changed risk boundary. Repeat a
full review only when the changes or a required gate justify it. Stop a repeated
disagreement to resolve the concrete missing fact or owner decision.

## Report

Lead with findings ordered by impact, then the scoped verdict and material gaps.
If none qualify, say no actionable findings in the reviewed scope. Name the
candidate/baseline and checks actually run; distinguish source inspection, local
tests, CI, runtime/device checks, and external review. An unavailable check is
unverified or blocked, never a pass. State when coverage is partial.

A review verdict assesses the named candidate. It does not by itself establish
deployment readiness or authorize merging, posting comments, or publishing.
