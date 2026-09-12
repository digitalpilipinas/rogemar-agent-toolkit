# Web control craft

Use within the current polish pass for affected web controls. Reuse the approved
component system; this reference adds no separate audit or implementation scope.

- Show acknowledgment at activation, separately from asynchronous completion.
  Keep loading, success and failure truthful; a visual press effect is optional.
  Retain static feedback and focus indication when motion is reduced or absent.
- Keep the hit region stable while a child animates. Handle pointer cancellation,
  dragging away, disabled state and keyboard activation without duplicate actions.
  Do not substitute hover or animation for native control semantics.
- Limit hover-only effects to pointers that support hover; touch users still
  need access to the same information and actions. Test keyboard focus separately.
- For adjacent tooltips, use the existing provider's shared delay behavior when
  available: an initial delay can prevent accidental opening, while moving among
  already active tooltips should not repeatedly make users wait. Keep focus,
  dismissal and accessible names intact; tooltips are not the sole label.
- Match feedback to repeated use. A frequent action may benefit from immediate
  color/state feedback rather than a scale effect. There is no required press
  scale, blur or animation duration. Route actual motion changes to the existing
  motion owner; do not introduce another library for polish.

Validate the affected pointer, touch and keyboard paths with available runtime
tools. Source inspection alone does not establish interaction behavior. Add
findings to the existing record, distinguishing defects from optional preference.

Selected adaptation of Emil Kowalski and Jakub Krehel; see [sources](craft-sources.md).
