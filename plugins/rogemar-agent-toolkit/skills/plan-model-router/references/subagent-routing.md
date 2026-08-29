# Sub-agent routing

Use this reference after the main plan or increment profile establishes the
quality bar. The main agent's selected model and reasoning effort are hard
ceilings for all delegated workers.

## Ceiling algorithm

1. Capture the parent model, active backend, and reasoning effort before the
   first worker is spawned.
2. Inspect the runtime model catalog and supported reasoning levels.
3. Normalize aliases such as `light` to `low` and `extra high` to `xhigh`.
4. Rank models using the active router profiles, not string comparison.
5. Remove every candidate whose model is stronger than the parent model or
   whose reasoning effort exceeds the parent effort.
6. Choose the lowest completed-task-cost candidate that satisfies the worker's
   objective and evidence burden.
7. If no candidate meets the worker's required quality, use the strongest
   permitted candidate and mark the assignment `ceiling-constrained`.
8. Return unresolved work to the main agent. Do not silently select a stronger
   model, change backend, or invent availability.

Treat any custom-agent model or effort setting as a desired profile. The
effective profile is the selected runtime-supported profile after this filter;
it must satisfy both ceilings even when the desired agent type is lower-tier.

The conservative fallback when model ordering or availability cannot be
verified is the exact parent model with an effort no higher than the parent.
Treat `ultra` as a separate parallel-work profile, not as a bypass around the
parent ceiling. It is permitted only when the parent explicitly supports and
selects an equivalent parallel profile; otherwise use an effort no higher than
the parent's ordinary reasoning level.

## Role guidance

| Worker role | Default profile shape | Required escalation |
| --- | --- | --- |
| Repository explorer | Lower-cost model, low or medium effort, read-only | Unclear ownership, hidden coupling, or contradictory evidence |
| Researcher | Lower-cost model for exact retrieval; mid-tier effort for synthesis | Current facts conflict or interpretation changes the design |
| Test or log analyst | Lower-cost model for routine output; mid-tier for flakiness or concurrency | Root cause remains ambiguous or evidence is non-deterministic |
| Implementation worker | Lowest profile that can follow the approved contract | Scope drift, new abstraction, migration, authorization, or failed validation |
| Verification reviewer | Fresh context, independent review, read-only | High-risk finding, conflicting evidence, or insufficient coverage |
| Security or privacy reviewer | Strongest permitted profile, read-only by default | Trust boundary, privacy contract, or critical risk exceeds the parent ceiling |

These are routing hints, not permanent model assignments. The increment's risk,
uncertainty, and verification cost determine the final profile.

## Role intents

Use a surfaced custom-agent type only when it improves the evidence or keeps a
bounded slice out of the main context. These intents are not a requirement to
create named agents or to spawn a Worker.

| Intent | Typical bounded use | Default ownership |
| --- | --- | --- |
| Explorer | Read-heavy code, dependency, and caller tracing | Read-only worker |
| Investigator | History, logs, documentation, or competing evidence | Read-only worker |
| Experiment worker | Repetitive, measured, independent trials | Bounded worker; parent accepts results |
| Engineer | Approved, known-contract implementation | Isolated write worker when authorized |
| Debugger | Reproduction and root-cause isolation | Read-only first; writes only when authorized |
| Reviewer | Independent counterexample or diff review | Read-only fresh context |
| Architect | Competing designs with a real unresolved decision | Read-only proposal; parent decides |
| Synthesizer | Reconciling worker evidence | Main agent by default |
| Lead escalation | Hardest unresolved judgment | Main agent or parent-inherited only |

## Worker assignment contract

Every worker assignment should include:

- Parent model and reasoning ceilings.
- Objective, evidence, owned surfaces, and non-goals.
- Dependencies and expected handoff.
- Permissions, tools, and isolation requirements.
- Assigned model and reasoning effort.
- Maximum turns or budget.
- Required output and evidence format.
- Stop and escalation conditions.

Every worker result should include status, findings, evidence, inspected
surfaces, changes, checks, assumptions, conflicts, remaining risks, and a
recommendation.

## Cost and independence

- Prefer no worker when the main context is sufficient, and one worker when
  there is one independent stream.
- Use two or three concurrent workers only for proven-disjoint evidence or
  write scopes whose benefit exceeds coordination and integration cost.
- Allow one delegation level; nested spawning requires explicit authorization.
- Keep exploration, research, tests, and review read-only where possible.
- Give each file or surface one writer and isolate independent writers.
- Summarize worker output instead of forwarding raw logs into the main context.
- Reassess the actual result and diff; a stronger parent profile never reduces
  required validation.
