---
name: forge-interrogate
description: "Use for \\\"interrogate\\\", \\\"adversarial review\\\", \\\"multi-model review\\\", \\\"challenge this\\\", \\\"stress test this code\\\", \\\"find blind spots\\\", or \\\"tear this apart\\\". Multiple LLM reviewers challenge changes from independent angles."
license: MIT
---
# Interrogate

Adversarially review code, a diff or a proposed design against its stated intent. The deliverable is a synthesized verdict; do not auto-apply changes. A separate implementation assignment can act on approved findings afterward.

Read [the Forge runtime contract](../codex-forge/references/codex-runtime.md). The orchestrator owns all reviewer requests; the router qualifies profiles under the active Forge mode, or parent model and effort ceilings when no mode is selected. Explicit user and host limits always apply. Another Codex model is optional and must be available. Independent agreement is supporting evidence, never a substitute for tracing the actual issue.

## 1. Determine scope and intent

Use the user-specified files or diff. Otherwise verify the current branch and appropriate base before collecting recent work. Include enough caller and contract context to assess behavior. State one paragraph of intent from the request, plan, commits and PR evidence. Clarify only an ambiguity that would materially change the review.

## 2. Prepare the common review contract

Read `references/reviewer-prompt.md`, `references/rubric.md` and `references/code-quality-review.md`. Fill the same reviewer template with the intent, relevant source/diff, rubric and quality lens. Ask `workflow-orchestrator` for the smallest useful set of independent read-only reviewers using the `interrogate-reviewers` preference pool. Pools do not mandate one worker per entry. Reviewers receive scope, exclusions, evidence requirements and a stop condition; they do not dispatch descendants.

For an unavailable or ceiling-constrained model, the router chooses an eligible profile or returns work to the parent. Do not exceed applicable mode, user or host limits (or parent ceilings without a mode), silently edit preferences or open a side PR to fix model names. Record requested and observed profiles separately; do not claim unobserved diversity.

## 3. Reconcile independent findings

Parse every finding, deduplicate equivalent issues, identify independent agreement and lone-reviewer findings, and retain explicit disagreements. Trace each material claim against source and actual constraints. A serious lone finding can be actionable; a popular unsupported preference is not a defect.

## 4. Lead judgment

Read `references/lead-judgment.md`. Classify every supported finding as Act on, Consider, Noted or Dismissed, with the reviewer label, evidence, consequence and one-line rationale. Respect existing compatibility and scope constraints. Size preferences are prompts to inspect, not automatic blockers. Do not hide material defects to fit a finding quota.

## Output

Return stated intent, reviewer coverage and metadata evidence, actionable findings, tradeoffs to consider, low-impact notes, dismissed claims with reasons, and an agreement map when it adds information. Use actual code citations. Preserve a review-only result unless implementation authority is separately supplied.
