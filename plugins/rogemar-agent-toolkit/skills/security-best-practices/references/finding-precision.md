# Finding precision

This is a method within the existing review, not a new approval ledger or an
automatic comprehensive audit. Preserve the named candidate, scope, provider IDs,
source limitations and existing severity scheme.

An established security defect identifies the lower-trust actor, accepted input
or action, protected resource, intended control, actual source path, strongest
preventing controls, and demonstrated consequence. Use the narrowest safe evidence
that settles the claim. Source-visible defects can be reported with their actual
source evidence; do not claim runtime reproduction that did not occur. When a
runtime, identity, deployment or provider fact is decisive and unavailable, retain
a specific needs-validation hypothesis and its next safe observation.

Keep three categories distinct:

| Category | Evidence and disposition |
| --- | --- |
| Established defect | Actual violated contract, conditions, impact, priority, smallest fix and regression check. |
| Needs validation | Source-grounded hypothesis, exact decisive gap and bounded next check; investigation priority is not confirmed vulnerability severity. |
| Hardening | Useful additional defense or best-practice alignment without a demonstrated current violation; not a fabricated vulnerability. |

An existing layer that prevents the claimed effect matters. Missing redundant
defense alone does not prove exploitability. Do not guess deployment configuration,
upgrade a local crash to remote code execution, or describe intentional same-user
capability as a cross-principal attack without the missing intent/boundary.

For consequential claims, an independent verifier should reconstruct the strongest
controls and try to refute the candidate. It may see the candidate and raw evidence,
but not another verifier's preferred conclusion. Deduplicate by root cause and
preserve rejected claims without suppressing review of the entire subsystem.
Reports must match final records; clean scope can legitimately have zero findings.

Permission is not intent. Check action/approval binding after argument normalization,
and compare direct, queued, batch, retry, resume and delegated paths. Review memory
writers and later consumers; summaries and tool metadata must not grant authority.
Structured output validates shape, not resource authorization or source truth.

Full audit execution is an optional separately scoped method. Untrusted target
code requires enforced isolation, dummy data, bounded resources, safe artifact
handling and appropriate independent validation. Missing controls block execution,
not useful source analysis. Do not blanket-apply an audit's offline/no-install rules
to unrelated authorized development or invoke extra providers automatically.
