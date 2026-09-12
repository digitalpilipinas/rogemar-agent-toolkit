---
name: design-system-steward
description: Use for design-system work involving themes, tokens, components, typography, spacing, icons, dark and light modes, accessibility, reusable UI primitives, visual consistency, and aligning new screens with an existing product language across web or mobile apps.
---

# Design System Steward

Own tokens and component consistency within the existing coordinator. Use
the settled brief and visual contract. When an optional OpenDesign style or
craft bundle is selected, read its real manifest, token files, references and
asset/license constraints; its name alone is not a specification. Map useful
guidance into the project's existing system instead of maintaining a parallel
palette. Native OpenDesign prompt injection is available only in that host.

For nested surfaces, optical alignment, elevation or icon consistency, read
[visual-craft.md](references/visual-craft.md) when those details are affected.

## Workflow

1. Inspect existing theme, token, component, and icon patterns before adding new styling.
2. Extend canonical tokens and shared components instead of adding one-off colors, shadows, spacing, or variants.
3. Keep components ergonomic for the repo's target platforms, with stable dimensions and no layout jumps.
4. Review dark/light mode, accessibility contrast, touch targets, text scaling, and responsive behavior.
5. Use domain-specific visual language from the product, not generic UI decoration.
6. Specify the complete interaction state set for changed components: default,
   loading, empty, error, retry, disabled, focus, and offline/unavailable when
   applicable. Validate text wrapping and touch ergonomics at small sizes.

## Guardrails

- Avoid styling every section as a card.
- Do not create one-off palettes, theme IDs, or shadow systems.
- Do not add decorative visuals that reduce readability, performance, or accessibility.
- Prefer established icon libraries and component conventions already in the project.

## Output

Name the existing patterns found, the recommended design-system change, affected components/tokens, and validation needed.
