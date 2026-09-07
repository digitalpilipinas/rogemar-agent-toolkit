# Motion decision and review method

Modified 2026-09-07 from the MIT-licensed
[emil-design-eng](https://github.com/digitalpilipinas/open-design/tree/ff2cc80f336f94786128113eddbbb9e3719fecc8/skills/emil-design-eng)
and [review-animations](https://github.com/digitalpilipinas/open-design/tree/ff2cc80f336f94786128113eddbbb9e3719fecc8/skills/review-animations)
bundles in OpenDesign `0.21.1`. They declare
[emilkowalski/skills](https://github.com/emilkowalski/skills) source commit
`a47903a06a05d2e24c483bd8961c85969a51a494`. The retained license names
Copyright (c) 2026 Matt Pocock; see [LICENSE.emil.txt](../LICENSE.emil.txt).
Attribution to a design method is not an endorsement or a claim to reproduce
the author's entire philosophy.

## Decide what should move

Establish purpose and frequency first. Repeated operational/keyboard actions
usually need immediate feedback and little movement; occasional transitions
can orient, confirm or explain. Existing platform and product conventions
remain the baseline. Remove movement with no useful job before adding a
different animation.

Check the relationship between trigger, input and output. Trigger-anchored
popover origins differ from centered modals. Gestures and rapidly repeated
actions should retarget from the current state without jumping, losing
velocity or locking input. Cancellation and reversal are part of the behavior.

## Focused checks

| Check | Evidence to seek |
|---|---|
| Purpose and frequency | Does movement clarify the state or delay a frequent task? |
| Timing and easing | Does feedback begin promptly and settle naturally? Compare entry, exit and deliberate-hold phases |
| Origin and continuity | Does the object move from the relevant trigger; does interruption preserve continuity? |
| Properties and performance | Inspect unexpected `transition: all`, repeated measurement, layout work and parent-driven frame updates; prefer transform/opacity when they meet the behavior |
| Input and accessibility | Reduced-motion result, keyboard alternative, hover/pointer capability, focus and gesture cancel behavior |
| Cohesion | Does motion fit the component and the product's established language? |

Upstream duration examples (button feedback roughly 100–160 ms, small popovers
125–200 ms, dropdowns 150–250 ms) can seed an experiment. They are not universal
pass/fail thresholds. Layout animation, linear progress or a longer explanatory
sequence needs context and measurement; do not flag library shorthand or a
curve name alone as a proven runtime regression.

Prefer deleting or reducing unnecessary motion, then fixing timing/origin,
interruptibility and expensive work. Add decorative choreography only when
the brief calls for it. Do not force perpetual animation, stagger, blur,
springs or press-scale on every interface. Reduced-motion may be instant or
gentler as long as it preserves the useful state and honors user preferences.

## Evidence and handoff

Inspect the real motion at normal speed and, when necessary, slow or
frame-by-frame. Source inspection identifies risks; performance tools and
interaction establish actual behavior. Use the receiving harness's supported
browser/device tooling, not a mandatory author's local setup.

Report location, observed behavior, impact, proposed correction and evidence
in the shared review record. A before/after/why table is useful for concrete
changes when no existing finding format applies. Separate verified defects,
unverified runtime concerns and optional craft preferences. Do not invent
approval from a source-only review or default to findings without evidence.
