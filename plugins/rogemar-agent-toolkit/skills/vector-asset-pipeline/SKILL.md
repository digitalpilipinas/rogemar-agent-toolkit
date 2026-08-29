---
name: vector-asset-pipeline
description: Use for SVG, icon, logo, vector illustration, symbol, map marker, app icon source, themable vector asset, density variant, export pipeline, optimization, accessibility, provenance, and render verification work.
---

# Vector Asset Pipeline

Use this skill for vector assets. Native ImageGen remains responsible for raster
generation and photo-like editing unless the task explicitly needs SVG or icon
source.

## Workflow

1. Identify the asset purpose: icon, logo, illustration, marker, diagram,
   product graphic, app icon source, or export asset.
2. Check existing icon libraries, brand assets, design tokens, and licensing
   before creating new vectors.
3. Build or modify vectors with clean viewBox, predictable dimensions, stable
   strokes/fills, currentColor or tokenized colors when theming is needed, and
   no hidden raster payloads unless intentional.
4. Add accessible names, decorative hiding, or labels according to the asset's
   semantic role.
5. Optimize cautiously: remove editor metadata and unused groups, but preserve
   IDs, masks, gradients, and paths required by the app.
6. Verify rendered output at target sizes, dark/light backgrounds, high density,
   and export formats. Check clipping, alignment, stroke scaling, and contrast.

## Guardrails

- Do not copy unlicensed third-party vectors.
- Do not hand-roll complex icons when a repo-approved icon library already has
  the right symbol.
- Do not replace a maintainable vector with a raster image unless the product
  need is photographic or painterly.
- Do not assume an SVG is accessible just because it renders.

## Output

Report source/provenance, intended use, theming behavior, accessibility
treatment, optimization performed, and render verification.
