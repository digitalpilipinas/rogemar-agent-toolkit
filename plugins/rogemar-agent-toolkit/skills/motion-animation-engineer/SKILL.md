---
name: motion-animation-engineer
description: Use for app or web motion work involving transitions, animations, gestures, haptics, shared-element movement, React Native Reanimated, Framer Motion, CSS/Web Animations, reduced motion, animation performance, and motion QA.
---

# Motion Animation Engineer

Use this skill when motion is part of the product behavior, not just decoration.
Prefer the repository's existing animation library, design tokens, timing
patterns, and accessibility conventions before adding dependencies.

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
