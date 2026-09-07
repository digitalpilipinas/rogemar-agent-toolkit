---
name: create-plan
description: Plan a software change from repository evidence, clear scope, practical increments, and observable acceptance. Use for an explicit planning request or when non-trivial work needs sequencing; keep routine changes brief and leave model selection to the active harness.
license: Apache-2.0
metadata:
  short-description: Create a proportionate implementation plan
---

# Create Plan

Produce one actionable plan that another capable implementer can use without
reconstructing the conversation. Reuse an existing approved plan and its task
IDs rather than creating a competing plan, board, or execution workflow.

## Match the depth to the work

- For an obvious, reversible change, skip formal planning unless requested. A
  short statement of the change and its check is enough.
- For a bounded change, use a short outcome, scope, ordered steps, and acceptance.
  The [concise template](references/concise-plan-template.md) is an optional shape.
- For multiple dependent increments, a migration, or material operational risk,
  add the relevant parts of the
  [programme template](references/programme-plan-template.md). Complexity or
  risk determines the detail; neither requires a large document by itself.

## Build the plan

1. **Inspect before deciding.** Read applicable instructions, the named issue or
   specification, current changes, relevant source and tests, and the existing
   verification commands. Follow nearby contracts and conventions. Inspect only
   what can change the plan; do not load every installed skill or every document.
2. **Define the outcome and boundary.** State observable success, affected paths
   or systems, non-goals, and locked requirements. Separate verified facts from
   assumptions. Preserve the user's product choices and authorized scope.
3. **Resolve consequential uncertainty.** Discover repository and environment
   facts before asking the user. Ask only for an unresolved decision that would
   materially change scope, behavior, authority, risk, or acceptance; include a
   recommendation and its tradeoff. Proceed with a labeled assumption when safe.
   Compare alternatives only when there is a real fork. If an empirical question
   needs an experiment outside planning authority, specify that experiment as a
   step rather than quietly implementing a prototype.
4. **Sequence useful increments.** Prefer the largest coherent slice that has a
   bounded scope and a meaningful check. Name dependencies and the interfaces
   later work relies on. Keep coupled work together; split at an independently
   reviewable outcome, not at every helper or tool call. Identify likely files
   and commands when known without inventing signatures or writing the entire
   implementation into the plan.
5. **Connect acceptance to evidence.** For each important requirement, name the
   behavior that proves it and the focused check that could disprove it. Add
   failure, permission, concurrency, compatibility, runtime, or rollback cases
   where the change makes them relevant. State missing prerequisites and which
   required checks will remain blocked until they are available.
6. **Check coverage and hand off once.** Ensure the sequence covers the agreed
   outcome, has no contradictory contracts or missing dependencies, and states
   the first next action. Where useful, name a specialist and why it is needed.
   An already selected orchestrator keeps coordination; model, tool, and agent
   bindings come from the installed adapter for the active harness. A runtime
   with one model or no delegation can still use this plan.

## Keep the boundary clear

A planning-only request does not authorize implementation, experiments, runtime
setup, external review, commits, or publication. Save a plan artifact when
requested or within the agreed task scope; otherwise deliver it in the response.
When planning is part of already authorized implementation, continue that work
without requesting the same approval again. Pause only the work that depends on
an unresolved owner decision or unmet required prerequisite.

Record capability requirements only when they affect execution. Installed files,
advertised tools, authenticated access, and observed execution are different
states. Do not claim a capability was used or a check passed during planning.

Modified by Rogemar Agent Toolkit on 2026-09-07 for portable, proportionate planning.
