---
name: visual-qa
description: Use for visual QA of web or mobile interfaces, screenshot review, small-screen checks, safe areas, responsive layouts, dark and light theme validation, export/share-card framing, typography readability, spacing, touch targets, visual hierarchy, and product-specific polish.
---

# Visual QA

## Workflow

1. Run the app or relevant preview when possible.
2. Capture or inspect desktop, tablet if relevant, narrow mobile, and small-height views. Use Playwright/browser screenshots or device previews when available.
3. Check safe areas, clipping, scroll behavior, touch targets, icon clarity, loading/empty/error states, and dark/light theme contrast.
4. For generated/exported images or share cards, verify aspect ratio, crop, text wrapping, theme treatment, and output quality.
5. Compare against the product's intended feel, audience, and domain.

## Review Heuristics

- No text overlap, tiny controls, awkward truncation, accidental horizontal scroll, or decorative clutter.
- Screens should support repeated real-world use, not just polished hero screenshots.
- Visual delight should serve the workflow.

For explanatory diagrams, also inspect label/connector collisions, readable
source relationships, accessible SVG names, and export fidelity. Keep the original
source and report meaningful omissions. An attractive diagram is not proof of
its factual claims. These checks adapt Diagram Design's methods; see the
[vector integration and attribution](../vector-asset-pipeline/references/diagram-design.md).

## Output

Give prioritized UI defects, exact screen/state, suggested fix, and whether a visual re-test is needed.

## Optional delegation guidance

The orchestrator may assign a read-only visual reviewer when screenshots,
responsive states, themes, or flows can be inspected independently. Provide
the target states, viewport/device scope, expected behavior, and evidence
format. Pass the parent model and reasoning ceilings; do not allow a visual
worker to exceed them. The main agent owns reconciliation, implementation
authorization, and the final visual re-test.
