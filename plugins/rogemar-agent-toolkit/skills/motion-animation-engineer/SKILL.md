---
name: motion-animation-engineer
description: Use for app or web motion implementation and focused review involving transitions, animations, gestures, haptics, shared-element movement, reduced motion, animation performance and motion QA.
---

# Motion Animation Engineer

Use this skill when motion is part of the product behavior, not just decoration.
Prefer the repository's existing animation library, design tokens, timing
patterns, and accessibility conventions before adding dependencies.

For a focused motion review or a consequential timing/interaction decision,
read [motion-review.md](references/motion-review.md), adapted from the
MIT-licensed Emil design engineering and animation review sources. Keep its
findings in the current task's review record. A review request does not imply
edits; a numeric timing convention alone is not evidence of a defect.

For affected mobile behavior, read [mobile-motion.md](references/mobile-motion.md)
only when relevant. These adapted Appllama methods need no subscription or MCP
and use the existing task owner and evidence record.

For motion purpose, staging or interrupted transitions, read
[motion-craft.md](references/motion-craft.md) when relevant.

## Workflow

1. Identify the motion job: orient, confirm, reveal, dismiss, reorder, navigate,
   celebrate, recover, or explain state change.
2. Inspect the existing stack before choosing an approach: CSS/Web Animations,
   Framer Motion, GSAP, React View Transitions, React Native Reanimated,
   gesture-handler, native transitions, or platform haptics.
3. Define entry, active, exit, interruption, cancellation, loading, error, and
   reduced-motion behavior.
4. Keep animation compositor-friendly where possible: transform and opacity
   first; avoid layout thrash, expensive shadows, and repeated measurement.
5. Match motion scale to the interface. Operational tools should use restrained
   motion; games, creative tools, and celebratory states can use richer motion.
6. Verify motion with real interaction, slow/failure states when relevant, and
   a small-screen pass. Capture screenshots or recordings when visual evidence
   matters.

## Guardrails

- Do not add a new motion dependency when the repo already has a suitable one.
- Respect reduced-motion settings and provide a useful non-animated state.
- Do not make motion block core tasks, hide errors, or delay recovery.
- Treat gestures as input systems: handle cancel, bounds, velocity, accidental
  taps, keyboard/screen-reader alternatives, and disabled states.

## Output

State the chosen motion primitive, why it fits the existing stack, the states
covered, performance/accessibility notes, and the validation performed.
