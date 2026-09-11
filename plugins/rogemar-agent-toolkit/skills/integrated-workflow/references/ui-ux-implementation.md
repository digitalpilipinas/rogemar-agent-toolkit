# UI/UX during implementation

Apply when the candidate changes visible UI or user interaction, including
bug fixes, states, navigation, input, generated visuals and shared UI primitives.
For non-UI work, record not applicable only when relevant to the receipt; do not
create a design ceremony. The existing workflow-orchestrator selects the smallest
useful skill set and any justified workers. No extra coordinator or agent panel.

## Select methods by the affected surface

| Need | Applicable installed methods |
| --- | --- |
| Ambiguous direction | design-brief; reference-design-contract for reusable reference decisions |
| Journey, navigation or recovery states | ux-flow-architect |
| Tokens, components and product consistency | design-system-steward |
| Working web interface implementation | frontend-design; use platform-native methods for other targets |
| Semantics, input, focus, assistive technology and visual access | accessibility-auditor throughout design, implementation and verification |
| Feedback, microcopy, loading/error states and touch ergonomics | interaction-polish |
| Existing or requested motion/gesture behavior | motion-animation-engineer, including reduced-motion alternatives |
| Rendered layouts, themes, wrapping and visual regressions | visual-qa with available browser/device tools |
| Actual OpenDesign project, scenario, resources or export workflow | opendesign only when its native application services are needed |

Select only methods relevant to the change; keep specialists separate and read
their installed instructions. Skill IDs are discovery hints, not mandatory
package dependencies or proof of tool access. Ordinary codebase design work
does not need OpenDesign running. Missing optional methods can use equivalent
local evidence; missing required tools keep the affected check blocked.

For mobile work, the existing reference, UX, interaction and motion owners carry
selected Appllama methods in on-demand references. Use the current brief and
legitimately accessible evidence; no Appllama MCP/account or library retrieval is
required. Scope research and recordings to unresolved decisions and affected
behavior. Select platform targets and APIs from the project; cloud environments
without device tooling retain the existing blocked/deferred evidence boundary.

## Implementation sequence

1. Before modifying an existing interface, inspect its current rendering and
   affected flow where possible. Capture a useful baseline for the exact route,
   state and viewport/device. If runtime access is unavailable, record that
   limitation and use existing source/reference evidence without calling it a
   live baseline. Continue independent authorized work.
2. Reuse the approved brief, references, tokens and product language. Clarify
   only unresolved choices that materially affect the task. Do not restart
   planning, create competing design documents, or expand a fix into a redesign.
3. Implement the agreed behavior with accessibility built in: semantics, labels,
   keyboard/touch behavior, focus, text scaling, contrast and reduced motion as
   applicable. Cover relevant loading, empty, error, retry, offline, disabled
   and success states. Use existing components and dependencies.
4. Refine affected interactions and motion within scope. A small fix does not
   require new animations, libraries, visual variants or unrelated polish.
5. Inspect the actual result on relevant wide, narrow and short layouts and
   applicable themes. Exercise the affected flow, keyboard/focus and relevant
   assistive-technology behavior; automation alone cannot prove accessibility.
   Use required browser/simulator/device checks under the programme's existing
   policy. Screenshots, interaction tests and physical-device proof are distinct.
6. Record defects in the existing finding record. The implementation owner
   validates and fixes in-scope defects, then reruns affected checks on the
   updated candidate. Apply the existing convergence and scope rules; optional
   polish does not start an endless review loop.

## Handoff to independent code review

Complete applicable UI/UX implementation checks before final slice readiness;
use the entry skill's proportional review policy for small bounded corrections.
The shared receipt names affected surfaces/states, exact candidate contents under
the [identity contract](execution-loop.md#candidate-identity-and-evidence-reuse),
inspected runtime/viewport, checks and evidence, defect dispositions, and remaining
failed/blocked/deferred items. HEAD or a worktree path alone does not identify dirty
contents. An executed check exposing a defect is failed; unavailable runtime is blocked.
Reuse the simulator checkpoint and finding ledger rather than duplicating them.

Early architecture, security, scope or diagnostic reviews may run during building.
If a required UI runtime is unavailable, useful independent code review may still
proceed as partial work with that gap explicit; it cannot establish UI readiness
or waive the existing acceptance/final-CI/merge boundary. An authorized deferral
remains deferred, not passed. Preserve the owner's exact simulator and physical-
device policies; this sequence does not silently strengthen or weaken them.

Independent code review remains separate evidence. UI/UX checks do not replace
correctness, security or required independence, and code review does not replace
visual, interaction or accessibility proof. After reviewer-driven UI changes,
rerun the affected UI/UX checks before final acceptance; unrelated unchanged
surfaces need not be rechecked without a concrete reason.
