---
name: frontend-design
description: Build or redesign working web interfaces with a clear visual direction, usable interaction states and responsive craft. Use for artifact or UI implementation after the task and design direction are understood; use the existing product system where one exists.
license: Apache-2.0 AND MIT
---

# Frontend Design

Adapted from Anthropic's frontend-design through OpenDesign, with optional
Taste methods. See [provenance.md](references/provenance.md) for licenses and
changes. This skill owns visual implementation in the receiving codebase;
the existing coordinator owns sequencing, delegation and delivery authority.

1. Read the brief, audience, primary job, existing design contract and actual
   framework/components. For a redesign, inspect the current result before
   editing; preserve what already serves the user.
2. Commit to a direction that fits the product. Make it concrete through type,
   hierarchy, density, spacing, color roles and component shape. For marketing,
   portfolio or editorial work with an open direction, read the contextual
   [Taste controls](references/taste-controls.md). Product interfaces follow
   their real task and established design system.
3. Build the real interface: semantic controls, useful content, navigation,
   loading/empty/error states and recovery. Distinguish sample content from
   facts. Do not turn a functioning product request into a static poster.
4. Use installed libraries, local assets and repository conventions. Check
   dependencies before importing them; a preferred style does not require a
   new framework, icon library, font download or animation package. For a
   standalone artifact, choose the simplest runnable form meeting the request.
5. Refine alignment, type measures, wrapping, rhythm and contrast. Use visual
   details to serve the concept; a brand color, system font or card layout is
   not automatically wrong. Remove effects that reduce comprehension or add
   no useful hierarchy. Bind repeated decisions to the existing token system.
6. Check the implemented artifact at relevant wide, narrow and short layouts,
   with keyboard/touch and applicable failure states. Inspect actual rendering
   through the host's available browser/device tools; source checks alone do
   not prove visual behavior. Report missing runtime evidence explicitly.

For flow, token, interaction or motion work, the installed specialist owns
that part: `ux-flow-architect`, `design-system-steward`, `interaction-polish`,
or `motion-animation-engineer`. Use only a helper that changes the result;
feed its findings into the same task record. A full OpenDesign application
request routes through the native `opendesign` adapter instead of pretending
its scenario or critique state exists in this codebase.

Deliver the working artifact, the meaningful design decisions, and actual
validation. Do not label a prototype production-ready or publish it because
its visual implementation is finished.
