---
name: design-brief
description: Turn natural-language or structured design input into a concise buildable brief with audience, visual dimensions, constraints and acceptance evidence. Use before design work when the desired direction is ambiguous; do not restart an already settled product brief.
license: Apache-2.0
---

# Design Brief

Adapted from OpenDesign's structured briefing method; see
[provenance.md](references/provenance.md). Use the receiving harness's existing
planning owner and task record. A routine component edit does not need a new
design document.

1. Read the requested artifact, audience, main task and existing product
   language. Reuse provided references, design tokens and prior decisions.
2. Resolve the useful dimensions: palette, accent roles, body and display
   typography, layout, mood, density and explicit exclusions. Natural language
   is sufficient. Accept structured I-Lang input when provided; its symbols
   are input labels, not a mandatory closed vocabulary or a substitute for
   actual tokens.
3. Record what was provided, observed and inferred. Translate adjectives into
   choices the builder can implement: content measure, information density,
   hierarchy, spacing, color roles and component behavior. Keep existing tokens
   authoritative; new values are proposals when no system exists.
4. Include responsive, keyboard/touch, text-scaling and reduced-motion needs
   that affect this artifact. Identify factual content/assets still missing.
   A design brief must not depend on a template silently adding those needs.
5. Ask only for a material choice that the current evidence cannot settle.
   Otherwise state the useful assumption and continue within authorization.
6. Put the brief in the current task artifact or the project's existing design
   document. When a reusable visual contract is needed, use the installed
   `reference-design-contract` method or its equivalent. Avoid two competing
   `DESIGN.md` formats and do not overwrite an existing contract from scratch.

A concise brief can use this shape:

```text
Artifact / audience / primary task:
Existing product or reference evidence:
Direction: palette roles; typography; layout; mood; density
Constraints: content/assets; platform; accessibility; performance
Assumptions and unresolved decisions:
First artifact must demonstrate:
```

Create a token/component preview only when it helps settle a visual choice or
is requested. Check that another builder can identify the direction, scope,
constraints and success condition without re-interviewing the user. Planning
does not authorize implementation, installation or publication beyond the
current request.
