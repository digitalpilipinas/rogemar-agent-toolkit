---
name: dream-team
description: Use for Rogemar's optional persona-based routing and explanation layer across coding projects. Trigger when the user asks for Dream Team help, names a Dream Team persona or squad, requests plain-language translation, or wants coordinated planning, design, implementation, review, or release guidance.
---

# Dream Team

Use this skill as a lightweight communication and routing layer. Existing
specialist skills remain the authorities for planning, UX, implementation,
testing, security, research, and release work.

## Default behavior

1. Classify the request by intent: answer, research, brainstorm, plan, design,
   implement, diagnose, review, release, or monitor.
2. Identify affected surfaces and risk lenses: product scope, UX, data,
   authorization, privacy, security, compatibility, performance, accessibility,
   operations, or documentation.
3. Select the smallest effective specialist skill set. Do not activate every
   persona merely because the task is broad.
4. Produce one coordinated response by default. Add a short plain-language
   recap when it improves understanding or the user requests it.
5. State assumptions and uncertainty. Use High, Medium, or Low confidence only
   as qualitative guidance; never invent numerical confidence scores.

Read the relevant reference before using a named persona or squad:

- `references/auto-detection.md` for intent and risk routing.
- `references/personas.md` for persona aliases and boundaries.
- `references/response-standards.md` for evidence-based response structure.
- `references/templates.md` for optional output shapes.

## Persona and squad controls

- An explicit persona request is a communication preference, not permission to
  skip repository inspection, specialist skills, tests, or safety checks.
- `squad-a` means technical perspectives; `squad-b` means plain-language
  explanation; `all-hands` means a phased review using only relevant roles.
- For `all-hands`, return one reconciled result rather than sixteen duplicated
  answers. Name disagreements and unresolved decisions.
- Personas are communication aliases, not executable custom-agent roles. When
  actual delegation is useful, `workflow-orchestrator` selects the surfaced
  agent type, scope, profile, and evidence contract.
- Do not claim that a persona, sub-agent, MCP, CI job, deployment, or review ran
  unless it actually ran and evidence is available.

## Technology neutrality

Keep this skill and its references technology-agnostic. Inspect the repository
or user-provided constraints before selecting language, framework, database,
hosting, deployment, testing, or integration guidance. Do not assume a stack.

## Evidence and safety

- Use `first-time-right-delivery` for non-trivial implementation or delivery.
- Use `create-plan` for coding plans and `plan-model-router` when its routing
  policy applies.
- Use `code-review-tests`, `test-architecture-engineer`, and `bug-triage` for
  review, test strategy, and diagnosis respectively.
- Add privacy, security, accessibility, performance, offline, or release
  skills only when the task makes those risks applicable.
- Report evidence as Verified, Partial, Unverified, Blocked, or Deferred.
- Never fabricate progress percentages, quality scores, timelines, costs,
  performance targets, test results, CI status, or deployment status.

## Output

Lead with the recommendation or result. Include only the sections that help:

- Context and assumptions.
- Decision or implementation direction.
- Risks and dependencies.
- Validation or evidence status.
- Two to six prioritized next actions.
- A concise explanation or diagram when it materially improves comprehension.
