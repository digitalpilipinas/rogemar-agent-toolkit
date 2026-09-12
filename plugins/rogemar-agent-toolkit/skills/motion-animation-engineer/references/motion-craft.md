# Contextual motion diagnostics

Supplement the existing motion review only for affected motion. Animation
principles are diagnostic lenses, not a requirement to animate every interface.

- Start with the action's purpose and frequency. Repeated operational actions
  should remain responsive; use staging to direct attention only where it helps
  users understand a real change. Do not delay interaction for a flourish.
- Check continuity when input reverses or interrupts movement. Continue from the
  current visual state; avoid snapping back to the initial keyframe. Use existing
  primitives suited to cancellation and gesture velocity rather than requiring
  springs for every transition.
- Consider anticipation, follow-through and overlap only if they clarify cause
  and effect. Decorative bounce, squash, arcs or secondary motion may be unsuitable
  for forms, dense tools or accessibility needs; omitting them is valid.
- Choose timing and easing for distance, input and platform expectations. Upstream
  advice differs on exit easing and stagger intervals: no curve, duration ceiling,
  fixed press scale or stagger value is a universal correctness rule. The approved
  system and observed interaction govern the choice.
- Keep final state and feedback understandable with reduced motion, including
  interruption, dismissal and failure. Avoid relying on blur or spatial travel to
  communicate essential state. Preserve keyboard and assistive-technology access.

Exercise rapid repeat input, reversal, cancellation and reduced-motion behavior
in the actual runtime when available. Separate source observations from observed
behavior and retain the current review record; no extra mandatory review cycle.

Selected adaptation of Emil Kowalski and Raphael Salaja's animation principles;
see [sources](craft-sources.md). Existing motion-review guidance remains intact.
