---
name: plan-model-router
description: Route Codex models and reasoning for plans, execution packages, and bounded subagents, including Astra, Sol, Terra, and Luna when surfaced. Preserve the manually selected parent as the default and ceiling; recommend justified task-specific worker profiles with validation and escalation evidence.
---

# Plan Model Router

Assess an existing plan, active execution package, or worker assignment. Do not
rewrite the product plan, implement the product, spawn workers, or claim that a
model tier guarantees quality. `workflow-orchestrator` owns dispatch.

Do not auto-activate it for a routine single-track change. Use it when the user
explicitly asks for model/cost routing or when multiple PRs, sprints, phases,
implementation increments, or materially different risk levels require
different execution profiles. It remains directly invocable for a concise plan
when the user wants that recommendation.

## Policy

Use one portfolio policy: **quality-anchored cost optimization**. The owner's
manually selected main model and reasoning effort are the active defaults and
hard ceilings. This includes Astra when the owner selects it. Workers inherit
that profile unless the task justifies an available, sufficient lower profile.
Recommendations never change the parent, its settings, or its backend.

## Workflow

1. Inspect the active runtime's exposed models and reasoning levels. Recommend
   only choices that are actually available; label named but unavailable models
   as unavailable rather than guessing. Normalize `light` to `low` and `extra
   high` to `xhigh`.
2. Confirm the work shape: whether the correct design is explicit, whether it
   is tightly coupled or can be split cleanly, and whether validation can expose
   a wrong result. Use the qualification checklist in `routing-profiles.md`;
   do not infer a high profile from PR size, urgency, or importance alone.
3. Apply the uncertainty gate before routing implementation. If acceptance
   criteria, ownership, invariants, rollback, or the intended design are
   materially unclear, recommend bounded stronger triage or planning first;
   do not send an under-specified task to a cheaper implementation profile.
4. For each PR/increment, score 0–2 for each: irreversibility/blast radius,
   security/privacy/authorization, cross-layer coupling, novelty/ambiguity,
   verification cost, and rollback difficulty. State any score that reaches 2.
5. Choose the lowest *completed-task-cost* profile that can meet the quality
   bar. Prefer Luna when execution of a known answer is the work; Terra when
   implementation needs engineering judgment; Sol for substantial ambiguity
   and risk; and Astra for the most demanding unresolved work when exposed and
   permitted by the parent ceilings. These are task-fit hints, not an automatic
   upgrade ladder or verified price claims.
6. Choose effort for the problem shape: low/medium for narrow established work,
   high/xhigh for non-trivial or uncertain work, max for one hard sequential
   problem, and ultra only for deliberately separable parallel workstreams.
   Ultra is not a stronger substitute for max.
7. For a concise single-increment plan, produce one execution profile with the
   precise model and reasoning level, risk reason, cost rationale, required
   validation, and evidence-based escalation trigger. For a formal multi-PR
   plan, use the quality-anchored planning default in `routing-profiles.md`,
then produce the complete execution profile for every PR. Each complete
   profile must name the precise model and reasoning level, risk score and
   reason, why lower cost is sufficient or not, required specialist skills,
   acceptance criteria, invariants, non-goals, dependencies, non-negotiable
   validation, rollback posture, cost/latency posture, and evidence-based
   escalation trigger.
8. For medium- and high-risk work, recommend a two-pass delivery shape when it
   reduces completed-task cost: a lower sufficient implementation profile,
   followed by an independent higher-judgment review of the actual diff. Do not
   use a second pass for low-risk work where targeted validation is enough.
9. Reassess immediately before execution using the actual diff and repository
   state. Escalate model family when judgment is the limit; escalate reasoning
   when the framing is sound but deeper checking is needed. Never lower
   validation because a stronger profile was selected.

## Default routing

Read [routing-profiles.md](references/routing-profiles.md) for task-fit guidance.
For execution, Forge setup preferences, or a worker assignment, read
[runtime-routing.md](references/runtime-routing.md). Inherit the selected
parent by default, justify each departure, and preserve required validation.

## Sub-agent routing with a parent ceiling

When delegated workers are used, evaluate each worker independently, starting
from parent inheritance. Capture the active parent model and reasoning effort as
`parent_model_ceiling` and `parent_reasoning_ceiling` before spawning.

Filter every candidate worker profile against both ceilings and the active
runtime's exposed models and reasoning levels. A worker may use a lower-cost
model or lower effort, but never a stronger model or higher effort than the
parent. If the worker's required profile exceeds the ceiling, use the strongest
permitted profile, mark the assignment `ceiling-constrained`, and return any
unresolved reasoning to the main agent or Rogemar.

Custom-agent configuration can override explicit spawn settings. Inspect it
before dispatch; use an unpinned equivalent role or keep work with the parent
when an override violates either ceiling. Record desired, requested, and
observed effective settings separately. Do not claim the observed profile from
configuration, an accepted request, or the worker's self-description alone.

Use the role and risk guidance in [subagent-routing.md](references/subagent-routing.md).
The main agent remains the quality anchor and must reconcile worker evidence
against the actual diff and validation results.

## Output

Lead with the quality-anchored cost-optimization policy and a compact
planning-profile note, followed by a per-PR table. Include a short portfolio
note listing unavailable requested models and which high-risk PRs require an
independent review regardless of the recommended profile.

When the user asks to optimize cost, explicitly call out where a lower-cost
profile is enough and where a stronger profile is justified by evidence rather
than preference. Treat pricing and availability as volatile: verify the live
client before relying on them.

For delegated work, include a worker-routing table with the role, preferred
agent type, bounded objective, desired and effective model/effort, parent
ceilings, permissions, evidence requirements, budget, independence reason, and
escalation trigger. Never report a model or effort as used unless the runtime
exposes or otherwise verifies it.

When prior delivery evidence is available, calibrate against it. Compare the
planned profile with scope drift, retries, failed validation, review findings,
and final outcome; adjust future recommendations only from recurring evidence,
not one anomalous result.
