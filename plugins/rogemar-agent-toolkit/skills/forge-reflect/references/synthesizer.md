# Reflection synthesis

Read [the reflection review contract](review-contract.md). Reconcile the supplied
lens reports against their incident evidence and the actual current targets.
The parent may apply the same method directly; no fixed reviewer count is needed.
Keep absent lenses and unavailable sources explicit without inventing coverage.

<AVAILABLE LENS REPORTS AND SOURCE POINTERS>

For each proposed change:

1. Verify the incident, reusable rule and target applicability. A majority does
   not resolve an unsupported or disputed claim.
2. Read the target. Reject an already-clear rule as already covered. If placement
   or activation caused the failure, propose repairing that existing instruction
   or route instead of adding another copy.
3. Prefer the existing owner. Justify any new skill with an evidenced recurring
   need that cannot be covered economically by existing methods.
4. Prefer structural prevention where useful. Reject a check already enforced;
   retain a missing type, lint, script or runtime check as a concrete proposal.
5. Separate durable guidance from temporary paths, versions and one-off details.
   Keep the latter in source evidence when needed to substantiate the finding.

Return these sections, with `None` when a section has no supported items:

## Accepted

| Problem and evidence | Proposal | Existing target or justified new owner |
| --- | --- | --- |

These are review recommendations. The parent applies existing authority and
asks only for an approval that is actually missing.

## Rejected

Name each rejected proposal and its evidence-based reason: unsupported,
one-off, duplicate, already covered, already enforced or outside scope.

## Backlog

Name each structural or broader proposal, its evidence, target and validation.
Return it to the parent; this template grants no issue creation or messaging.

## Durability and specificity examples

A useful proposal changes a future decision and remains meaningful after ordinary
code drift. Preserve examples and rationale that teach that decision; text length
is not a quality score.

- A particular SHA, one file's byte count, or the date a reviewer flagged a bug
  belongs in incident evidence, not in a standing instruction.
- A repeated failure caused by parsing structured triggers with closed regex
  lists can justify schema validation when the actual interface supports it.
- A demonstrated package-manager boundary can justify documenting the supported
  command and lockfile ownership. Do not prescribe one runtime for all projects.
- A missed skill trigger can justify a clearer description or supported routing
  metadata. Verify the host supports that metadata before proposing it.
- "Write good code" does not identify a changed decision. Name the specific
  invariant, inspection step or missing mechanism instead.

Read each target before recommending an edit. When a clear rule already exists,
look for a demonstrated activation or execution failure; another copy will not
repair it. Keep enough detail in each accepted row to identify the failure,
proposed behavior and evidence. Brevity must not erase a material caveat.
