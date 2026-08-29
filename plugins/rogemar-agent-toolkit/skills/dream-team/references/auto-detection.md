# Intent and Risk Routing

Use task intent, affected surfaces, and risk—not isolated keywords—to select
the smallest useful capability set. If the request is ambiguous, state the
most reasonable assumption or ask one focused question.

## Primary routes

1. **Strategy, brainstorming, and prioritization**
   - Use the strategy persona as a communication label.
   - Route planning to `create-plan`, research to `research-synthesizer`, and
     complex delivery to `first-time-right-delivery`.

2. **Research and validation**
   - Use the research persona as a translator of evidence.
   - Use `research-synthesizer` or `knowledge-base-answering` according to the
     source boundary and freshness requirement.

3. **UX, interaction, and visual design**
   - Use the design or flow personas as optional explanations.
   - Route to `ux-flow-architect`, `design-system-steward`,
     `accessibility-auditor`, `interaction-polish`, or `visual-qa` as needed.

4. **Implementation and integration**
   - Use the technical persona as an implementation label.
   - Route through `first-time-right-delivery` and add only the relevant
     domain-specific skill discovered from the repository.

5. **Bug, review, and test strategy**
   - Use `bug-triage` for diagnosis.
   - Use `code-review-tests` for diff review and `test-architecture-engineer`
     when the question is what evidence is sufficient.

6. **Security, privacy, performance, and accessibility**
   - Add the matching specialist only when the behavior or data makes it
     applicable. Treat authorization, privacy, sensitive data, migrations,
     and destructive operations as high-risk until inspected.

7. **Release and operations**
   - Use `deploy-checklist` plus the target-specific release skill only when a
     release or deployment is actually in scope.

8. **Documentation and explanation**
   - Use the documentation persona for plain-language translation, not as a
     substitute for source verification or technical review.

## Uncertainty guidance

- **High:** proceed with the selected route and identify evidence required.
- **Medium:** proceed with explicit assumptions and a bounded fallback.
- **Low:** ask one question or present two or three concrete interpretations.

## Manual controls

- A named persona narrows communication style but does not bypass safety or
  validation.
- `squad-a` requests technical perspectives.
- `squad-b` requests plain-language perspectives.
- `all-hands` requests a phased, reconciled review; do not duplicate every
  role when a specialist skill already owns the work.
