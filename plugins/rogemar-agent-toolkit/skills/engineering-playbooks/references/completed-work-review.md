# Review completed outcomes

Use for an authorized batch review or when repeated observed failures warrant a
bounded process investigation. Do not add a ceremony to every successful task,
replace required per-change reviews with sampling, or create a monitoring service.

1. Define the question, time window, eligible population and available evidence.
   State the selection method before examining outcomes: all cases in a small
   window, a reproducible random sample, or explicit strata such as task type and
   success/failure. Include failures, reversions and recovery work. Disclose missing
   follow-up evidence and selection bias; do not select only impressive successes.
2. For each selected case, connect the requirement and candidate with checks,
   review findings, delivery result and subsequent regressions/rework. Separate
   lack of evidence from failure. Use authorized source pointers, not copied
   private transcripts. Later production outcomes may remain unknown.
3. Group recurring causes across implementation, tooling, context, method selection,
   verification and environment. Preserve contrary examples and distinguish a
   shared cause from superficially similar symptoms.
4. Propose the smallest structural correction through the existing capability
   maintainer or Project Learning owner. Prefer repairing a verifier, tool or
   route over repeating instructions. Name scope, expected effect, validation,
   cost and rollback. A review recommendation does not promote a lesson or grant
   installation, external tracker writes or publication.
5. Where an improvement is authorized, compare later eligible work with a stated
   baseline using the same selection rules and comparable task mix/versions.
   Use ME-01 for verified outcomes, recurring defects, human interventions and
   complete-task cost, including retries and recovery. Unknown stays unknown.
   Report recurrence and coverage before attributing a causal improvement.

Return the population/selection, evidence-backed patterns or none, concrete
corrections and owners, and the next comparison criterion. Reuse the task's
existing record. When the sample is too small, say so and retain a hypothesis;
do not manufacture a process change to justify the review.
