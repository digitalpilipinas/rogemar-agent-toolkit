---
name: accessibility-auditor
description: Use for accessibility reviews or implementation involving semantic structure, keyboard and focus behavior, screen readers, ARIA, live announcements, contrast, touch targets, Dynamic Type, reduced motion, forms, errors, and automated plus manual a11y evidence.
---

# Accessibility Auditor

Use this skill for accessibility-sensitive planning, implementation, and review
across web, mobile, documents, and generated UI artifacts.

## Workflow

1. Identify the user task, assistive technologies, platform, and affected
   states: loading, empty, error, disabled, success, destructive, offline, and
   permission-denied.
2. Check semantic structure first: headings, landmarks, labels, roles, names,
   descriptions, grouping, and reading order.
3. Verify keyboard, focus, pointer, touch target, safe-area, and escape/cancel
   behavior. Focus must move intentionally after navigation, dialogs, errors,
   and async completion.
4. Verify screen-reader behavior: accessible names, state announcements, live
   regions, validation errors, dynamic updates, and hidden decorative content.
5. Check visual access: contrast, text scaling, wrapping, reduced motion,
   color-independent meaning, visible focus, icon labeling, and density.
6. Use automated checks when available, then do manual checks for behavior that
   automation cannot prove.

## Guardrails

- Do not use ARIA to paper over incorrect native semantics.
- Do not hide important errors, progress, or permissions from assistive tech.
- Do not claim accessibility is complete from automation alone.
- Keep accessibility fixes aligned with the existing design system.

## Output

Lead with defects by severity and affected user task. Include exact state,
expected accessible behavior, proposed fix, and evidence run or still needed.

## Optional collaboration guidance

The orchestrator may assign a read-only accessibility reviewer for an
independent state, platform, or assistive-technology evidence stream when the
target behavior can be evaluated separately. Provide the user task, affected
states, platform scope, owned surface, non-goals, parent model and reasoning
ceilings, and required evidence format. Return exact defects and evidence gaps;
do not claim complete accessibility or authorize implementation. The main
agent reconciles findings and owns the final validation decision.
