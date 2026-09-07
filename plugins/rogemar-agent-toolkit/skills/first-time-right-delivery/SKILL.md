---
name: first-time-right-delivery
description: Keep requirements, implementation, and acceptance evidence aligned during a non-trivial software change. Use when missed behavior, compatibility, or premature readiness claims are a material risk; supplement the current plan and review without creating another workflow.
---

# First-Time-Right Delivery

Apply evidence discipline inside the current task. `create-plan` can own a needed
plan, `code-review-and-quality` can own the review, and the selected orchestrator
owns coordination. This skill contributes acceptance checks; it does not start
a second plan, board, review, or model-routing process.

## Before changing behavior

- Read the repository instructions, current changes, relevant requirements,
  implementation patterns, and verification commands. Preserve unrelated work.
- Separate locked requirements, discoverable facts, assumptions, and material
  owner decisions. State what observable result completes the request.
- Connect each important requirement to a check. Use an existing acceptance list;
  use a matrix only when multiple contracts make it easier to audit. Add authority,
  compatibility, failure, or recovery details only where they matter.
- Sequence coherent increments by their real dependencies. An increment needs
  a reviewable result and a useful check; it need not be its own deployment or
  commit. If delegated, preserve explicit ownership, allowed scope, isolation,
  and required verification under the active harness's policy.

## During implementation

- Complete the behavior across the affected UI, API, persistence, access control,
  cache/offline state, configuration, and tests as applicable. Avoid completing
  only the visible path while leaving a required consumer or failure state out.
- Keep security-sensitive decisions at their trusted authority boundary; do not
  accept a client-supplied override of server-owned identity or permissions.
- Preserve supported inputs, clients, and persisted data. For data transitions,
  verify partial completion, safe retries, and recovery or disable behavior.
- Include the applicable loading, empty, error, denied, unavailable, retry, or
  offline states in acceptance. Never fabricate success data to fill a gap.
- Reconcile changed scope or new evidence with the existing plan. Resolve only
  the dependent work when a material product choice remains open.

## Before claiming completion

1. Compare the actual final diff and results with the original outcome. Check
   omitted requirements as well as defective code. Use the active review's test
   and counterexample pass; do not duplicate it here.
2. Run the relevant repository checks against final content. Verify the surface
   affected: an original repro for a bug, runtime behavior for an interaction,
   supported cases for compatibility, or a comparable baseline for a performance
   claim. A low-impact edit may need only a direct check.
3. Seek independent review when it adds meaningful evidence or a project gate
   requires it. Use the selected runtime's permitted capabilities; model choice
   never substitutes for validation. Disclose unavailable independent evidence
   and keep any required gate unmet.
4. State what is implemented, verified, blocked, or explicitly deferred. Keep
   local tests, CI, staging/production, external review, and manual/device checks
   distinct. Report a required check that could not run without calling it passed.

## Optional Unlazy completion checks

When the owner requests `unlazy`, or substantial work needs runnable checks to
prevent omitted outcomes, apply the [Unlazy adapter](references/unlazy.md) to the
existing acceptance record. This skill owns evidence quality; Unlazy contributes
gate checking and measured reporting. Keep one gate record and the active
orchestrator. It adds no mandatory plan, worker tree, hook, provider or install.
If Unlazy is unavailable, run the repository checks directly and retain the same
evidence and incomplete-outcome reporting.

## Delivery boundary

Release work applies only when authorized. Before a commit or publication,
reinspect the selected files and applicable secret, whitespace, and project
checks. Preserve unrelated and local-only material. After an authorized push or
deployment, verify the remote revision and the corresponding CI or runtime
evidence before claiming that phase complete.

Pause dependent work when a required prior contract is absent, a material owner
decision changes the scope, or verification shows the increment unsafe. Continue
independent authorized work. An explicitly accepted deferral remains a deferral;
neither a plan, a worker receipt, nor this skill grants additional external-action
authority.
