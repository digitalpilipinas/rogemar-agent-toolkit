---
name: code-review-tests
description: Use when reviewing code diffs, pull requests, bug fixes, migrations, or feature branches for correctness, regressions, security-sensitive behavior, missing tests, and focused verification steps.
---

# Code Review + Tests

## Review Workflow

1. Inspect the actual diff and surrounding code before judging.
2. Trace the diff against the approved requirements or PR evidence matrix;
   identify omitted planned behaviour before judging implementation details.
3. Prioritize findings by user impact: correctness, data loss, auth/privacy, security, migrations, and regression risk.
4. Ground every finding in a file and line when possible.
5. Suggest focused tests that would catch the issue. Prefer repo-native test patterns.
6. If asked to implement fixes, keep changes scoped and verify them.
7. Perform a counterexample pass before approving risky work: try malformed,
   legacy, unauthorized, concurrent, disabled, private, and rollback inputs.
   Test the stated invariant rather than only the current implementation.

## Output Shape

For reviews, lead with findings ordered by severity. Include open questions and a short residual-risk note only after findings.

## Sensitive System Biases

- Treat auth identity, permissions, roles, payments, credits, safety state,
  health/wellness data, storage, privacy flows, migrations, and row/object-level
  access controls as high-risk.
- Do not trust client-supplied sensitive state when a server-authoritative path
  is possible.
- Preserve existing data contracts unless the user explicitly asks for a breaking change.
- Tie acceptance claims to evidence from the reviewed commit; distinguish local
  checks, CI, staging/production, and deferred manual/device QA.

## Helpful MCPs

- `github` for PRs, issues, comments, and checks.
- `openaiDeveloperDocs`, official framework docs, or package docs for current technical behavior.
- `supabase` for database, RLS, migrations, functions, and logs.

## Optional collaboration guidance

For broad or high-risk diffs, the orchestrator may assign independent,
read-only reviewers for correctness, security, regression, or test gaps when
the review surfaces are separable. Give each reviewer the approved
requirements, owned files, non-goals, evidence standard, parent model and
reasoning ceilings, and required finding format. Reviewers return concrete
findings and checks, not overall approval or readiness claims. The orchestrator
deduplicates and sequences follow-up work; the main agent owns reconciliation
and the final review decision.
