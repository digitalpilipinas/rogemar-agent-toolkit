---
name: create-plan
description: Create an actionable coding plan. Use when a user explicitly asks for a plan related to a coding task; include a minimal capability handoff and invoke plan-model-router only for multi-PR, sprint, phased, materially different-risk, or explicitly routed plans.
metadata:
  short-description: Create a plan
---

# Create Plan

## Goal

Turn a user prompt into one self-contained, actionable plan. Select the output
template by delivery shape; do not compress a multi-PR programme into a small
ticket checklist.

## Minimal workflow

Throughout the entire workflow, operate in read-only mode. Do not write or update files.

1. **Scan context quickly**
   - Read `README.md` and any obvious docs (`docs/`, `CONTRIBUTING.md`, `ARCHITECTURE.md`).
   - Skim relevant files (the ones most likely touched).
   - Identify constraints (language, frameworks, CI/test commands, deployment shape).
   - Derive the capabilities the work is likely to need. When that choice
     materially affects the plan, use read-only environment discovery to
     shortlist relevant skill-family members and inspect surfaced plugin, MCP,
     connector, app, or tool routes as a separate layer. A tool may exist
     without a matching skill. Limit discovery to capabilities installed or
     surfaced in Codex; do not scan the external marketplace or load the whole
     catalog.

2. **Ask follow-ups only if blocking**
   - Ask **at most 1–2 questions**.
   - Only ask if you cannot responsibly plan without the answer; prefer multiple-choice.
   - If unsure but not blocked, make a reasonable assumption and proceed.

3. **Select the output template**
   - For one clear, low-risk change with no material contract, migration,
     security, or cross-layer risk, read and use
     [concise-plan-template.md](references/concise-plan-template.md).
   - For multiple PRs, sprints, phases, parallel lanes, a migration,
     security/privacy/authorization work, compatibility work, or materially
     different-risk increments, read and use
     [programme-plan-template.md](references/programme-plan-template.md).

4. **Select the capability handoff**
   - For non-trivial work, use `workflow-orchestrator` to identify the next
     stage entry and only the specialists justified by the affected surfaces.
     Do not turn the installed skill catalog into a mandatory bundle.
   - Record whether the next entry is direct implementation,
     `goalbuddy:goal-prep`, or `deliver-approved-programme`. When Goal Prep is
     next, its job is to copy capability names into task inputs or constraints,
     not load or execute those skills during board preparation.
   - Every specialist remains directly invocable; a handoff is an activation
     hint that execution must revalidate against the actual task and diff.
   - For a materially independent workstream, record delegation topology only
     when it earns its coordination cost: role or preferred agent type,
     independence reason, desired profile, parent-ceiling fallback, synthesis
     owner, and bounded fan-out. Do not prescribe a permanent agent model in a
     plan.
   - For each material live capability, record the need, preferred route,
     observed availability, smallest fallback, and authorization still needed.
     Distinguish installed or advertised from surfaced, enabled, authenticated,
     and callable. Planning must not install, authenticate, access private
     connector data, spend credits, or perform an external mutation.

5. **Route models only when warranted**
   - Invoke `plan-model-router` for multiple PRs, sprints, phases,
     implementation increments, materially different-risk work, or an explicit
     model/cost-routing request.
   - Skip model-routing overhead for a routine single-track plan unless the
     user asks for it.
   - For routed work, use the shared `routing-profiles.md` guidance. State the
     formal planning profile when justified and route each implementation
     increment to the lowest sufficient available model and reasoning level.

6. **Create the plan**
   - Follow the selected template's required sections and populate every
     applicable field with repository-grounded information. Mark genuinely
     unknown information as open or pending; do not invent it.
   - For a routed plan, embed the complete planning profile and per-PR
     execution handoff in the final plan; do not merely point to the router or
     its reference. Routing never replaces acceptance criteria, validation, or
     rollback planning.
   - Keep action items atomic and ordered. Use concrete paths, commands, and
     evidence where available; write no application code.

7. **Output only the selected plan**
