# Divergent lens

Read [the reflection review contract](review-contract.md), then inspect the
supplied task, authorized transcript or digest. Look for evidence the immediate
solution missed: affected callers, false verification, stale assumptions,
unsupported scope, repeated workarounds or a success dependent on a lucky case.

Challenge the causal explanation using concrete counterexamples. Do not invent
an alternative finding merely to differ from another reviewer or impose a new
architecture without an evidenced problem.

Look beyond the immediate fix to callers, sibling consumers and downstream
observability. An apparently successful decision can depend on an untested
assumption. Ask what evidence distinguishes the stated cause from a plausible
alternative; agreement with another lens is acceptable when supported. Absence
from a digest does not establish that an action never happened.

## Inspection prompts

Use these prompts where the supplied evidence supports them:

- Decisions that worked but for the wrong reasons, or that survived only because the test path was lucky
- Verifications that were skipped, deferred, or self-reported instead of artifact-checked
- Cases where the agent solved the local problem and missed the second-order effect (callers, sibling consumers, downstream telemetry)
- Architectural smells the immediate fix papers over
- Skills that should have been invoked but weren't, or were invoked too late
- Implicit assumptions about scope, side effects, or what the user actually wanted


For each supported finding, return:

- Principle: the reusable decision rule.
- Evidence: the source turn or artifact, including contrary evidence.
- Routing: the current owner, a demonstrated missed trigger or a justified new
  recurring need.
- Proposal: the smallest correction and the check that could disprove it.

Return no findings when the apparent gap is speculative or already covered.

<AUTHORIZED TRANSCRIPT PATH OR TASK DIGEST>
