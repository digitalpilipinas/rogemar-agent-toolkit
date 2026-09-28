# Bounded task framing

Use inside the current task owner, not as another planner. The original request,
current repository contract, explicit source boundary and actual permissions stay
authoritative. A shorter or more polished prompt is a candidate improvement, not
proof of better execution.

## Select the interaction once

| Context | Behavior |
| --- | --- |
| Prompt-only request | Return the requested prompt; no downstream execution. |
| Explicit review-first request | Present one copy-ready prompt with material changes and gaps; wait. |
| Precise request or approved continuation | Preserve the existing brief and proceed within authority. |
| Authorized implementation | Use a brief internal framing pass; do not ask again for routine edits or checks. |
| Consequential unresolved ambiguity | Pause only the dependent action and resolve the missing decision. |
| Direct / refine-and-run | Respect that mode, but never treat rewriting as additional permission. |

Dedicated prompt-refinement tools may retain their configured review-first default.
Do not silently replace that user preference. Ordinary implementation uses adaptive
framing, not a compulsory prompt-review checkpoint. The optional orchestrator
`workflow_contracts.py framing` operation validates this selection from explicit
inputs; it does not infer intent or grant authority.

## Smallest complete brief

Carry the requested deliverable, relevant baseline, accepted scope/non-goals,
permitted actions, decisive evidence, observable acceptance, and material unknowns.
For large handoffs, include source locations and revisions plus whether the receiver
can actually access them. Do not duplicate complete transcripts or expose private
source merely to make a handoff self-contained.

Use only the affected disciplines. A visual change does not imply a backend
migration; a review does not imply fixes; drafting does not imply sending. Keep
creative choices open where the user specified an outcome rather than an approach.
Preserve supplied exact text and source-only requests. Research-enabled work may
add current primary evidence within its permission boundary; source-faithful work
must not silently import outside conclusions.

## Reuse and evaluate

Keep one plan and original requirement record. A materially changed requirement
needs reconciliation, not silent rewriting. Skip recursive refinement and redundant
plans. Compare original and refined briefs on equivalent held-out tasks, including
intent fidelity, successful authorized work, missed constraints, review effort,
clarification burden, latency and total cost. Retain failures as evidence. Do not
claim this procedure trained model weights or that a prompt file applied runtime
permissions.
