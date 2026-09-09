---
name: code-review-tests
description: Check a change's test evidence, regression coverage, and relevant counterexamples. Use as the testing lens within one code review or for a focused verification review; contribute findings without starting a duplicate quality review.
---

# Code Review Tests

Contribute test and counterexample evidence to the active review. Keep its target,
requirements, finding IDs, and verdict owner. For a full review requested through
this compatibility entry, use the installed `code-review-and-quality` owner once
and supply these checks within it. For a testing-only request, perform this
focused pass directly. If the owner is absent, report the focused scope rather
than claiming a complete five-axis review.

## Check behavior, not the implementation's shape

1. Inspect the actual diff, affected callers, approved requirements, and existing
   tests. Trace important requirements to the evidence that would catch their
   omission or regression; passing unrelated tests is insufficient.
2. Choose the smallest useful checks from repository-native commands and test
   conventions. A regression test should fail for the original bug or a plausible
   wrong behavior. Avoid tests that merely repeat implementation details,
   assertions with no meaningful failure, or mock-only proof of a real boundary.
3. Exercise applicable counterexamples. For sensitive or stateful changes,
   consider malformed, unauthorized, legacy, duplicate, concurrent, private,
   disabled, offline, retry, and rollback inputs. Select the cases that can
   violate this change's contract; do not impose every case on every change.
4. Check identity, ownership, access control, entitlements, and sensitive derived
   state at the trusted authority boundary. Preserve supported data and client
   contracts. For migrations, examine partial completion and safe retry as well
   as the successful final shape.
5. Verify claims against the current candidate. Record the command/procedure,
   relevant result, and environment. A proposed check is not a run; local tests
   do not establish CI, deployed behavior, or browser/device verification.

Run safe checks within task authority. Do not install tools, contact private
services, mutate shared data, or edit tests solely because this review found a
gap. When fixes are authorized, keep them scoped and validate their effect. Do
not add tests for reversible low-impact changes when a direct check is adequate.

## Return to the same review

For substantial output, follow shared
[context guidance](../workflow-orchestrator/references/context-efficiency.md):
retain the command/candidate, exit status, distinct failures, skipped or blocked
checks and original log location. Read saved diagnostics before rerunning solely
to recover omitted text; rerun affected checks when current evidence is needed.

Return concrete findings and the evidence gap they expose, ordered by impact.
Include location, violated requirement, affected scenario, and a check that can
confirm the correction. Separate demonstrated bugs from missing coverage or
unverified hypotheses. A missing test alone is not proof of a defect.

Deduplicate with other review results before reporting. Include required but
unavailable checks and any owner-approved deferrals. Do not produce a second
overall approval or run another external reviewer from this companion.
