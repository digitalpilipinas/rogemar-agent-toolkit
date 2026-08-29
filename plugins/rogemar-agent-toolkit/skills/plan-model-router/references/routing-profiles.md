# GPT-5.6 model-routing profiles

Inspect the active runtime first. Recommend only exposed models and reasoning
levels. If a named choice is absent, label it unavailable and select the
nearest exposed profile. Translate `light` to `low` and `extra high` to
`xhigh`.

This is an advisory cost-quality router, not a substitute for testing, review,
or explicit release authorization. The goal is the lowest **completed-task
cost** that can meet the quality bar. A cheap choice that causes a wrong design,
retries, unnecessary rewrites, or weak verification is not an optimization.

## Planning versus implementation

For formal multi-PR coding plans, use a high-quality Sol planning profile to
establish the correct specification, invariants, dependencies, non-goals, and
validation. Cost optimization starts after the plan: route each implementation
PR independently from that quality anchor. Sol planning does not make Sol the
default implementation model.

## Portfolio roles

| Model | Use when | Avoid as the default for |
| --- | --- | --- |
| GPT-5.6 Luna | The answer is explicit, local patterns are strong, and execution or high-volume coverage is the work | Ambiguous design, trust boundaries, migrations, consistency, or open-ended diagnosis |
| GPT-5.6 Terra | Production implementation needs engineering judgment across normal code, APIs, data, tests, and conventional unfamiliar repositories | Frontier-hard ambiguity or critical security/reliability decisions |
| GPT-5.6 Sol | The correct answer is uncertain, unusually novel, security-sensitive, high-risk, or deeply coupled | Mechanical, high-volume, well-specified routine work |

Reasoning effort cannot replace base-model judgment. Change model when the
limitation is interpretation, ambiguity, hidden constraints, or novel design.
Increase reasoning when the framing is sound but deeper investigation is needed.

Role intent does not set effort by itself. Use `max` only when the worker's
bounded objective needs demanding exploration or verification and the parent
ceiling permits it; a lower-cost or high-volume role is not a blanket reason to
use `max`.

## Planning-stage profiles

Planning establishes the implementation quality bar before execution cost is
optimized. For a formal multi-PR plan, default to **Sol xhigh**. Use **Sol max**
when one tightly coupled problem needs a coherent reasoning chain, and **Sol
ultra** only when planning separates cleanly into independent streams. Then
route every PR separately with the score table below.

| Planning scope | Recommended profile | Use it for | Do not use it for |
| --- | --- | --- | --- |
| A clear, single low-risk PR requiring formal planning | Sol xhigh | Turning an established request into acceptance criteria, scope, non-goals, and checks | A mechanical edit whose plan is already self-evident; execute it directly with the appropriate lower-cost profile |
| Several conventional PRs or a moderately unfamiliar subsystem | Sol xhigh | Dependencies, contracts, risks, sequencing, and validation that need strong judgment | A simple, well-patterned change merely because it is important |
| One hard, tightly coupled programme decision | Sol max | Reconciling requirements, architecture, compatibility, migration, or safety tradeoffs in one coherent reasoning chain | A plan that divides into independent research or design streams |
| Large plan with genuinely independent planning streams | Sol ultra | Parallel repository mapping, contracts, data review, test strategy, UX review, risk review, and explicit synthesis | A context-fragile architecture decision or routine multi-PR feature planning |

The planning profile is a quality anchor, not a blanket implementation choice.
The plan must state each PR's acceptance criteria, invariants, non-goals,
dependencies, validation, and rollback needs so a lower-cost implementer can
execute without rediscovering the design.

## Uncertainty gate

Before selecting an economical implementation profile, check whether the PR has
clear acceptance criteria, owned boundaries, invariants, non-goals, verification
method, and rollback posture. If any missing item could change the design or
safety of the work, pause routing and recommend a bounded triage pass instead:

| Uncertainty shape | Recommended triage | Exit condition |
| --- | --- | --- |
| Narrow ambiguous or risky decision | Sol low | A documented decision, assumptions, and smallest safe scope |
| Several unclear dependencies or a weakly documented subsystem | Terra xhigh or Sol medium | Confirmed contracts, owners, acceptance criteria, and validation plan |
| Conflicting requirements, migration, security, or architecture uncertainty | Sol xhigh/max | Reconciled invariants, rollback plan, and explicit escalation/approval needs |

Do not use Luna or a lower-cost Terra profile to guess the intended design.
Once the uncertainty gate is passed, route the settled implementation normally.

## Qualification checklist

Answer these questions for every planning exercise and PR. They are the
qualification criteria for choosing a model and reasoning level. Record short
evidence, not just a score.

| Question | Low-cost qualification | Higher-profile qualification |
| --- | --- | --- |
| Is the correct result explicit? | Acceptance criteria, non-goals, and expected behavior are clear | Requirements conflict, key behavior is inferred, or a design decision remains open |
| Is there a proven repository pattern? | A nearby implementation and tests can be reused without changing a contract | The subsystem is unfamiliar, poorly documented, or requires a new abstraction |
| What can break? | Failure is local, visible, reversible, and caught by targeted tests | Failure affects users, data, permissions, money, privacy, uptime, or several services |
| How many boundaries change? | One component or layer; no public, persisted, or permission contract changes | Client/server/schema, tenant, auth, cache, background job, offline, or third-party boundaries interact |
| Can validation prove correctness? | Focused tests or deterministic checks cover the behavior | Evidence needs integration, legacy, privilege, idempotency, migration, device, or operational checks |
| Is rollback safe? | Change can be reverted without data loss or mixed-version concerns | Migration, backfill, published contract, or irreversible side effect makes rollback difficult |
| What reasoning shape is needed? | Local execution or bounded debugging | Broad ambiguity, several plausible causes, hard sequential reasoning, or separate parallel streams |

### How to interpret the answers

1. If every answer falls in the left column, select Luna at the lowest effort
   that covers the number of files and tests: low for mechanical work, medium
   for a small feature, high for explicit multi-file work.
2. If the desired design is clear but one or more answers fall in the right
   column, start with Terra: medium for ordinary work, high for serious
   implementation, xhigh for difficult but bounded work, or max for a very
   hard clear single-agent problem.
3. If the correct design, root cause, safety boundary, or hidden constraint is
   itself uncertain, use bounded Sol triage or Sol implementation. Choose high
   for critical work, xhigh for systemic ambiguity, and max for the hardest
   tightly coupled chain of reasoning.
4. Use Ultra only when the last question identifies independently bounded
   streams and the plan names their boundaries and synthesis owner. Use Terra
   Ultra for conventional streams and Sol Ultra only when the streams are
   individually difficult or high-risk.
5. If a qualification cannot be answered from evidence, it is an uncertainty
   gate failure—not a reason to pick a cheaper model and proceed.

### Plain-language shortcuts

| If the work sounds like this | Start here |
| --- | --- |
| “Make this exact, local change using the existing pattern.” | Luna medium or high |
| “Implement this clear production feature across normal layers.” | Terra high |
| “Find why this familiar subsystem fails intermittently.” | Terra xhigh |
| “Perform this defined migration, permission, or concurrency change with rollback.” | Terra max |
| “Work out what is actually correct or safe before implementing.” | Sol low for triage, then Sol high or xhigh as evidence warrants |
| “Solve one deeply coupled, unresolved hard problem.” | Sol max |
| “Coordinate distinct frontend, backend, data, test, and review streams.” | Terra ultra, or Sol ultra only if the streams are themselves frontier-hard |

## Model-and-reasoning scope matrix

Use the lowest row that matches the work. These profiles are advisory and must
be checked against currently exposed client options.

| Profile | Scope that justifies it | Typical work | Escalate when |
| --- | --- | --- | --- |
| Luna low | Mechanical, isolated, obvious result | Search, rename, formatting, small fixture/type/test edits | A behavior, contract, or downstream effect is unclear |
| Luna medium | Small clear feature following a nearby pattern | Standard component, endpoint, validation, unit tests | Work spans several layers or requirements need interpretation |
| Luna high | Explicit multi-file execution with stable architecture | Pattern-led feature, ordinary refactor, integration/test repair | Compatibility, ambiguity, or unusual failure modes appear |
| Luna xhigh | Tricky but bounded problem with a settled design | Familiar subsystem bug, state/data-flow trace, focused review | The correct design or root cause is uncertain |
| Luna max | Exhaustive, token-heavy execution of a complete specification | Repetitive migration application, broad known-pattern changes, bounded suite repair | Security, architecture, tenant isolation, concurrency, or an unsettled design appears |
| Terra low | Narrow production edit where local judgment matters | Small safe fix, repository-native SQL/API/validation change, quick diff review | Broader effects or deeper checking are needed |
| Terra medium | Everyday full-stack development | Normal workflow, API/UI integration, reproducible bug, modest review | Several modules, compatibility, or difficult diagnosis enter scope |
| Terra high | Serious bounded production implementation | Multi-module feature, contract/data-model change, semantic refactor, broad tests | Asynchrony, weak documentation, intermittent failure, or migration risk emerges |
| Terra xhigh | Difficult but well-scoped engineering | Complex integration, unfamiliar subsystem, compatibility refactor, async bug, final large-diff review | The task framing, risk boundary, or root cause remains genuinely uncertain |
| Terra max | Very hard but clear single-agent work | Architecture within known constraints, RBAC, migration, idempotency, concurrency, consistency | Novel/ambiguous design, critical safety risk, or repeated failed investigation requires Sol judgment |
| Terra ultra | Large conventional project with separable streams | Parallel frontend, backend, schema, test, documentation, or repository audit work | Streams are tightly coupled or individually frontier-hard |
| Sol low | Fast expert direction for a narrow risky or ambiguous question | Triage, architectural choice, risky-diff review, hidden-assumption check | Full implementation or deeper evidence is required |
| Sol medium | Complex implementation where requirements need interpretation | Unfamiliar system, architecture-aware feature/refactor, ambiguous debugging | Critical risk, deep coupling, or more exhaustive investigation appears |
| Sol high | Reliability-first high-risk implementation | Auth/authorization, critical transformation, distributed workflow, difficult release review | Multiple hidden interactions, conflict, or a sequential investigation persists |
| Sol xhigh | Systemic, high-ambiguity, or adversarial work | Security review, subtle concurrency, complex migration, conflicting requirements, multi-service regression | One coherent problem remains exceptionally deep and sequential |
| Sol max | Hardest tightly coupled single-agent problem | Race condition, protocol/runtime work, mixed-version migration, conflicting code/tests/specs | The work instead divides into clean independent streams |
| Sol ultra | Large, divisible programme whose streams are individually difficult | Broad security/correctness audit, ambitious multi-system modernization, parallel hypotheses | The scope is routine, small, or too context-fragile for delegation |

## Max versus Ultra

| Effort | Choose it when | Avoid it when |
| --- | --- | --- |
| `max` | A hard, sequential, tightly coupled problem needs one coherent chain of reasoning | The work has bounded, independent streams |
| `ultra` | Frontend, backend, data, test, review, or documentation streams can be independently investigated and cleanly synthesized | A narrow bug, small task, or context-fragile sequential problem |

Ultra is a parallel execution strategy, not simply a smarter Max. Luna has no
Ultra profile in the current research; verify actual availability in the client.

## Score routing

Score each increment 0–2 for: irreversibility/blast radius; security, privacy,
authorization, or ownership impact; cross-layer coupling; novelty/ambiguity;
verification cost or observability gap; and rollback difficulty.

| Score | Work shape | Default profile | Required evidence |
| --- | --- | --- | --- |
| 0–2 | Docs, labels, formatting, deterministic config, isolated fixtures | Luna low/medium; Terra low if local judgment matters | Diff review and one targeted check |
| 3–4 | Small repository-native code edit; nearby tests; no contract change | Luna medium/high; Terra medium if interpretation matters | Focused unit, type, or lint check; state blast radius |
| 5–6 | Clear multi-file feature, ordinary refactor, endpoint plus client/test change | Luna high for explicit patterns; Terra high when judgment is needed | Focused tests, type/lint, and relevant UI states |
| 7–8 | Compatibility work, meaningful refactor, schema-adjacent or integration change | Terra high/xhigh; Terra max for a clear single-agent deep investigation | Integration and legacy checks; independent high/xhigh counterexample review |
| 9–10 | Contract, RLS/auth, privacy, offline/concurrency, migration/backfill, entitlement/ownership work | Terra max if design and rollback are clear; Sol high/xhigh if ambiguity or critical risk dominates | Boundary, privilege, legacy, retry, idempotency, rollback, and observability evidence as applicable |
| 11–12 | Ambiguous architecture, production incident, security-sensitive multi-system change, difficult-to-roll-back refactor | Sol xhigh/max | Full relevant validation, rollback or kill switch, independent high-risk review |
| Exception | Large work with genuinely independent streams | Terra ultra; Sol ultra only when individual streams are frontier-hard | Explicit stream boundaries, synthesis owner, integration validation |

## Two-pass delivery rule

Use a second, independent review only when it is cheaper than repeated
implementation failure or the consequence of a missed defect. Review the
actual diff and evidence, not merely the initial plan.

| Risk score | Default delivery shape | Independent review |
| --- | --- | --- |
| 0–4 | One implementation pass plus targeted validation | Not normally required |
| 5–6 | Luna high or Terra high implementation plus required tests | Terra high/xhigh review when the diff crosses a contract or has non-obvious edge cases |
| 7–8 | Terra high/xhigh implementation plus integration evidence | Independent Terra xhigh review |
| 9–10 | Terra max or Sol implementation plus boundary evidence | Independent Sol high/xhigh review |
| 11–12 | Sol xhigh/max implementation plus full relevant evidence | Independent high-risk/adversarial review; do not treat the author profile as the review |

The review may return the same profile when an independent executor and fresh
context are available. Model strength never substitutes for independence,
required tests, or release authorization.

## Workload crossovers

| Situation | Cost-effective choice | Escalate instead when |
| --- | --- | --- |
| Explicit, repetitive, token-heavy execution | Luna max | Design becomes ambiguous or a sensitive boundary appears: Terra or Sol |
| Clear serious production feature | Terra high | Compatibility, unfamiliar architecture, or difficult diagnosis needs more checking: Terra xhigh |
| Difficult but well-scoped implementation | Terra xhigh | Root cause, ownership, or task framing is uncertain: Sol high |
| Very hard but defined, tightly coupled work | Terra max | Novel architecture, hidden requirements, or critical risk limits confidence: Sol high/max |
| Broad conventional project that divides well | Terra ultra | The streams are individually frontier-hard: Sol ultra |
| Fast risky or ambiguous triage | Sol low | Full investigation and implementation are required: Sol high or max |

## Escalation

Start only as high as evidence warrants:

`Luna medium -> Luna high -> Terra high -> Terra xhigh -> Terra max -> Sol high -> Sol xhigh -> Sol max`

Use Ultra only after confirming clean workstream boundaries. Move from Luna to
Terra when interpretation is the limitation; Terra to Sol when the correct
design, risk assessment, or hidden constraint is the limitation. Do not raise
a smaller model's effort repeatedly when base judgment is the problem.

Escalate immediately if requirements conflict; a sensitive trust boundary,
irreversible migration, concurrency concern, or new subsystem appears; two
reasonable attempts fail without clear cause; the diff crosses the planned
boundary; or a product decision remains unresolved.

## Cost controls

- Use concise progress and failure summaries; output tokens cost materially.
- Define scope and non-goals; prefer targeted patches over unrelated refactors.
- Reuse stable repository and specification context instead of regenerating it.
- Keep the selected execution profile stable for the PR. Switch model or effort
  only when a documented escalation trigger appears; needless switching loses
  context and can add cost.
- Use Fast mode only when time is worth its premium; switching from Sol to
  Terra or Terra to Luna usually changes cost more.
- A stronger profile never lowers test, review, security, migration, or device
  validation requirements.

## Calibration loop

After each material PR, record a compact private routing outcome:

| Planned profile | Risk score | Scope drift | Retry/escalation | Validation or review finding | Human correction or retained change | Cost per delivered PR | Outcome |
| --- | --- | --- | --- | --- | --- | --- | --- |

Review these outcomes periodically by task shape. Raise a default only after a
recurring failure pattern; lower it only after repeated clean delivery with the
same validation gates. Treat one-off incidents, unusually poor specifications,
and external failures as context to investigate rather than automatic model
changes.

## Output shape

For each PR or sprint increment, output:

| Increment | Scope and dependencies | Score and key risk | Recommended profile | Why lower cost is sufficient or not | Required specialist skills | Acceptance and non-goals | Required validation and rollback | Cost/latency posture | Escalate if |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Close with unavailable requested profiles, which increments need independent
review, and whether the selection assumes a clear specification, a single-agent
reasoning chain, or deliberately separable workstreams.
