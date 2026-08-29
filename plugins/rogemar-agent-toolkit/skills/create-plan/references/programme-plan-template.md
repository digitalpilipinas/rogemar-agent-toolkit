# Programme Plan Template

Use this template for multi-PR, sprint, phased, migration, security-sensitive,
compatibility, or materially risky work. It is a blank structural minimum, not
a product specification: scale tables to the programme, preserve honest unknowns,
and omit only sections that are explicitly not applicable.

```markdown
# <Programme or feature name> — Implementation Plan

**Status:** Draft | Proposed | Approved

**Scope:** <sprints, PRs, or delivery boundary>

**Implementation start:** <first authorized or incomplete increment, or `Pending approval`>

<One short paragraph on outcome, delivery strategy, and the programme's
authority boundary. State that this plan does not grant implementation, commit,
deployment, or production authorization.>

## 1. Source map and repository context

### 1.1 Required sources

| Source key | Document, issue, decision, or repository source | Use before |
| --- | --- | --- |
| <KEY> | <path or stable reference> | <PR or scope> |

### 1.2 Existing patterns and likely surfaces

| Concern | Reuse point or likely path | Contract to preserve |
| --- | --- | --- |
| <concern> | <path/module/test> | <invariant> |

## 2. Locked contracts and constraints

1. <Sequencing, authority, data, compatibility, privacy, safety, or operational invariant.>
2. <Non-goal or prohibited scope expansion.>
3. <Rollout or backward-compatibility rule.>

### 2.1 Compatibility and rollout map

| Existing shape | Target behaviour | Compatibility or rollout rule |
| --- | --- | --- |
| <legacy/current shape> | <target> | <dual-read, target-write, flag, migration, or no-change rule> |

## 3. Requirement-to-evidence matrix

| Requirement | User or client behaviour | Authoritative service/data path | Compatibility, privacy, or security rule | Positive proof | Negative or counterexample proof | Rollback/disable |
| --- | --- | --- | --- | --- | --- |
| <requirement> | <behaviour> | <server/data authority> | <constraint> | <proof> | <denial or edge proof> | <safe reversal> |

## 4. Delivery sequence

### 4.1 Delivery contract and evidence status

Every increment is independently reviewable. Record actual—not assumed—local,
CI, staging, and device evidence. Define `First incomplete`, `Not started`,
and any repository-specific completion states.

### 4.2 Sprint or phase: <name>

| PR / status | Sources | Dependencies | Goal, likely paths, and risk boundary | Focused smoke and done-when evidence | Execution profile |
| --- | --- | --- | --- | --- | --- |
| <ID — status> | <source keys> | <predecessor or parallel rule> | <outcome, paths, non-goals, risk> | <positive, negative, rollback, and environment proof> | <model and reasoning> |

**Phase exit:** <ordered dependency expression and required evidence.>

Repeat this section for each phase, sprint, optional lane, and rollout gate.

## 5. Shared work contracts

### 5.1 Data, service, and compatibility

| Area | Required implementation contract |
| --- | --- |
| <area> | <authority, idempotency, migration, compatibility, or access rule> |

### 5.2 UI, package, and operational boundaries

| Area | Required implementation contract |
| --- | --- |
| <area> | <component, accessibility, performance, disclosure, or package rule> |

## 6. Implementation order and handoff

1. [ ] <First authorized increment and its predecessor gate.>
2. [ ] <Next ordered or explicitly parallel-safe increment.>
3. [ ] <Integration and hardening gate.>
4. [ ] <Evidence and release-readiness gate.>

State what may run in parallel, which unmerged contracts block later work, and
when to stop for a manual model switch or user authorization.

### 6.1 Capability handoff

| Stage or increment | Next entry skill | Conditional specialists | Activate because | GoalBuddy task handoff |
| --- | --- | --- | --- | --- |
| <planning, prep, implementation, review, or PR> | <`goalbuddy:goal-prep`, `deliver-approved-programme`, or direct specialist> | <smallest applicable set> | <surface or evidence trigger> | <task inputs/constraints, allowed files, verify, stop conditions> |

Goal Prep records this handoff in the board without loading or executing the
specialists. Execution revalidates every activation against the active task and
actual diff; listed skills are not an always-on bundle.

| Capability need | Preferred installed skill and live route | Observed availability | Smallest installed fallback | Authorization still needed |
| --- | --- | --- | --- | --- |
| <need> | <skill plus plugin, MCP, connector, app, CLI, or local tool> | <surfaced/enabled/authenticated/callable, unavailable, or unverified> | <installed fallback or `None`> | <login, private data, credits, external mutation, or `None`> |

Discovery does not grant authority. Goal Prep copies these fields into task
inputs or constraints and schedules any execution-time revalidation; it does
not activate the capabilities itself.

### 6.2 Delegation topology (only when it earns its cost)

| Increment or evidence stream | Preferred role or agent type | Independence reason | Desired profile | Parent-ceiling fallback | Fan-out and synthesis owner |
| --- | --- | --- | --- | --- | --- |
| <scope> | <role or surfaced type> | <why a fresh context improves the result> | <lowest useful profile or `None`> | <effective-profile rule or main-agent return> | <0-3 workers; main agent unless explicitly assigned> |

Do not add this table for serial, trivial, or main-agent-owned work. A desired
profile is not a permanent agent setting and does not bypass runtime or parent
ceiling checks at execution.

## 7. Model routing and review

**Portfolio policy:** Quality-anchored cost optimization.

**Planning profile:** <available Sol profile and why the plan shape justifies it.>

| PR / increment | Scope and dependencies | Score and key risk | Recommended available model and reasoning | Why lower cost is sufficient or not | Required specialist skills | Acceptance and non-goals | Required validation and rollback | Cost/latency posture | Escalate if |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

### Mandatory independent review

| Trigger or increment | Independent review needed | Required counterexample or evidence |
| --- | --- | --- |
| <migration, privacy, security, rollout, or high-risk PR> | <review scope/profile> | <proof> |

## 8. Validation and evidence plan

### 8.1 Per-PR checks

| Work type | Required local checks | Required negative cases |
| --- | --- | --- |
| <client, service, migration, UI, or compatibility work> | <commands/tests> | <denials/edge cases> |

### 8.2 Sprint, release, and environment evidence

| Evidence layer | Required proof | Status reporting rule |
| --- | --- | --- |
| Local | <commands and final-diff checks> | <passed/not run> |
| CI | <workflow evidence> | Do not infer from local checks |
| Staging | <environment, accounts, flags, rollback> | <passed/deferred/not run> |
| Physical device | <platform, accessibility, offline checks> | Deferred until performed |

## 9. Open decisions and change control

| Decision or trigger | Current state | Owner or required authorization | Effect if unresolved |
| --- | --- | --- | --- |
| <decision> | <open/approved/deferred> | <owner> | <blocked scope or safe fallback> |

Do not silently redesign, deploy, commit, or expand scope. If repository
evidence conflicts with this plan, stop at the active increment, preserve
verified work, and report the conflict with evidence.
```

Minimum quality: make the plan independently executable without re-planning.
For each material requirement, show its source, contract, delivery increment,
positive and negative proof, rollback posture, and execution profile.
