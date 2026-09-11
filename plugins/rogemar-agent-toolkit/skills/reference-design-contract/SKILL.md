---
name: reference-design-contract
description: Turn screenshots, URLs, product notes and visual references into an evidence-based reusable design contract and implementation handoff. Use when a prototype, deck or redesign needs a consistent visual direction across artifacts or builders.
license: Apache-2.0
---

# Reference Design Contract

Adapted from OpenDesign; see [provenance.md](references/provenance.md). The
deliverable is a set of explicit design decisions, not a longer generation
prompt. Use one existing project contract where possible.

1. Identify artifact, audience, constraints and the decision the references
   need to resolve. Inspect the supplied images/pages/docs using capabilities
   actually available to the receiving harness. Missing evidence stays missing.
2. For each reference distinguish observed qualities, user-provided intent and
   inference. Record what to keep, what to change, and which source-specific
   marks/assets/content are outside the intended reuse. Preserve controllable
   qualities such as rhythm, composition, density or material without silently
   copying another product's factual claims or identity.
3. Select one coherent direction grounded in the brief. Prototype alternatives
   only for an unresolved consequential choice. Do not manufacture options for
   a settled direction.
4. Update the existing `DESIGN.md` or equivalent. If the project has no format,
   the portable default below covers the necessary decisions. For an actual
   OpenDesign design-system package, use that runtime's current manifest/token
   schema; a standalone document does not claim native package compatibility.
5. Add a compact evidence/decision record and implementation handoff in the
   same document. Split files only when different consumers need them or the
   user requested the OpenDesign three-file output. A preview is optional.
6. Validate against [checklist.md](references/checklist.md) before handing off.

For unresolved reference decisions, read [reference-research.md](references/reference-research.md)
only when relevant. These adapted Appllama methods need no subscription or MCP
and use the existing task owner and evidence record.

## Default contract shape

1. Visual theme and atmosphere: audience, purpose, stance and reference evidence.
2. Color: semantic roles, accessible combinations and existing token mappings.
3. Typography: hierarchy, readable measures, fallback/local font availability.
4. Spacing and grid: density, rhythm and responsive constraints.
5. Layout and composition: primary task, content order and narrow/short layouts.
6. Components: existing primitives and applicable interaction states.
7. Motion and interaction: purpose, input behavior and reduced-motion result.
8. Voice and brand: supplied facts, tone and asset/provenance constraints.
9. Anti-patterns: specific failure conditions for this design.

The handoff names files/resources to read, binding choices, allowed variation,
missing inputs, the first artifact's proof and the relevant visual/interaction
checks. Keep authoring, runtime inspection and publication evidence distinct.
