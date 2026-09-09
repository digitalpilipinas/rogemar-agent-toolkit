# Forge mode and role mapping

The executable source is `scripts/routing_catalog.json`. Run
`resolve_profile.py --list-modes` or `--role-map` for current data.
Resolution follows selected mode → group default → role override → saved role
preferences → task-fit, live availability, and native role pin checks.
Explicit qualified candidates can adapt an assignment within the mode.
These defaults do not guarantee sufficiency or launch permanent agents.

| Mode | Allowed profiles |
| --- | --- |
| Peak | Astra, Sol, Terra: low, medium, high, xhigh, max |
| Balanced | Sol, Terra: low, medium, high, xhigh; Luna: max |
| Lean | Terra: low, medium, high; Luna: high, max |
| Sprint | Terra: medium; Luna: low, medium, high, max |

Compatibility aliases: supreme → peak, optimize → balanced, budget → lean.
Light is `low`; Extra High is `xhigh`. Astra is `gpt-6-astra`; the other families
use `gpt-5.6-*`. Ultra is excluded from these four pools. The names express
intent, not measured price, speed, or benchmark guarantees.

## Role contracts

Keep integration and final acceptance with the main agent. The three
main-owned roles below require `target: parent` and return proposals only.
Other roles describe bounded assignments; the orchestrator still decides
whether an independent worker is useful and grants its exact scope.

- Goal Scout and Goal Judge reuse available GoalBuddy native contracts and
  preserve their independence, permissions, and fixed settings. Pass native
  pins to the resolver; a conflict is blocked until a valid profile is qualified.
  Do not relabel an ordinary reviewer as GoalBuddy evidence to escape a pin.
- Design roles select applicable installed design skills, not copies of them.
  Skill hints are selective discovery aids, not mandatory activation lists.
- Browser, simulator, emulator, physical-device, and visual evidence remain
  distinct. A screenshot is not interaction testing; a simulator is not a
  physical-device check. Verify the requested surface and available tools.
- `scope-reviewer` may use Ponytail for simplicity; it does not replace
  correctness, security, accessibility, or final acceptance.
- `learning-curator` activates only on an explicit project-learning request.
  Prepare project-local evidence-backed proposals within that skill's contract;
  no automatic capture, promotion, memory writes, or delivery interruption.
- `status-monitor` performs bounded requested checks. Recurring monitoring
  requires a separate explicit scheduling request; it creates no automatic job.
- Dream Team offers optional perspectives to this orchestrator, not another
  coordination layer. Findings consolidation is advisory; the main agent owns
  reconciliation and the final result.

## Shared group defaults

| Group | Peak | Balanced | Lean | Sprint |
| --- | --- | --- | --- | --- |
| coordination | astra/high | sol/high | terra/high | terra/medium |
| engineering | sol/high | terra/high | terra/high | terra/medium |
| design | sol/xhigh | sol/high | terra/high | luna/max |
| verification | terra/high | terra/high | luna/high | luna/medium |
| review | astra/high | sol/high | terra/high | luna/max |
| operations-learning | terra/medium | luna/max | luna/high | luna/low |

## Individual role defaults

| Role | Group | Peak | Balanced | Lean | Sprint |
| --- | --- | --- | --- | --- | --- |
| `parent-coordinator` (main-owned) | coordination | astra/high | sol/high | terra/high | terra/medium |
| `workflow-coordinator` (main-owned) | coordination | astra/high | sol/high | terra/high | terra/medium |
| `integration-owner` (main-owned) | coordination | astra/high | sol/high | terra/high | terra/medium |
| `findings-consolidator` | coordination | astra/high | sol/high | terra/high | terra/medium |
| `why-synthesizer` | coordination | sol/high | sol/medium | terra/high | luna/high |
| `reflect-synthesizer` | coordination | sol/high | sol/medium | terra/medium | luna/high |
| `feature` | engineering | sol/high | terra/high | terra/high | terra/medium |
| `refactoring` | engineering | sol/high | terra/medium | terra/medium | terra/medium |
| `bug-fix` | engineering | astra/high | sol/high | terra/high | luna/max |
| `perf-issue` | engineering | sol/xhigh | terra/xhigh | terra/high | terra/medium |
| `hillclimb` | engineering | astra/max | sol/xhigh | terra/high | luna/max |
| `hardest-tasks` | engineering | astra/max | sol/xhigh | terra/high | luna/max |
| `how-explorer` | engineering | terra/medium | luna/max | luna/high | luna/low |
| `how-explainer` | engineering | sol/medium | terra/medium | luna/high | luna/medium |
| `why-investigators` | engineering | terra/high | terra/high | luna/high | luna/high |
| `reflect-tooling` | engineering | terra/medium | luna/max | luna/high | luna/medium |
| `swarm-workers` | engineering | terra/high | luna/max | luna/high | luna/high |
| `bug-triager` | engineering | sol/high | terra/high | terra/high | terra/medium |
| `goal-scout` | engineering | sol/high | terra/high | terra/high | luna/low |
| `judgment-and-prose` | design | sol/medium | sol/medium | terra/medium | luna/high |
| `reflect-divergent` | design | sol/high | terra/xhigh | luna/max | luna/high |
| `arena-runners` | design | sol/xhigh | terra/xhigh | luna/max | luna/max |
| `architect-runners` | design | astra/max | sol/high | terra/high | luna/max |
| `ux-flow-designer` | design | sol/xhigh | sol/high | terra/high | luna/max |
| `ui-designer` | design | sol/xhigh | sol/high | terra/high | luna/max |
| `design-system-reviewer` | design | sol/xhigh | sol/high | terra/high | luna/max |
| `interaction-designer` | design | sol/xhigh | sol/high | terra/high | luna/max |
| `accessibility-reviewer` | design | sol/xhigh | sol/high | terra/high | luna/max |
| `validation-runner` | verification | terra/high | terra/high | luna/high | luna/medium |
| `visual-reviewer` | verification | terra/high | terra/high | luna/high | luna/medium |
| `browser-qa` | verification | terra/high | terra/high | luna/high | luna/medium |
| `simulator-qa` | verification | terra/high | terra/high | luna/high | luna/medium |
| `emulator-qa` | verification | terra/high | terra/high | luna/high | luna/medium |
| `physical-device-qa` | verification | terra/high | terra/high | luna/high | luna/medium |
| `qa-runner` | verification | terra/high | terra/high | luna/high | luna/medium |
| `how-critics` | review | astra/high | sol/high | terra/high | luna/max |
| `reflect-judgment` | review | astra/high | sol/high | terra/high | luna/max |
| `arena-cross-judge-pool` | review | astra/max | sol/high | terra/high | luna/max |
| `interrogate-reviewers` | review | astra/xhigh | sol/high | terra/high | luna/max |
| `correctness-reviewer` | review | astra/high | sol/high | terra/high | luna/max |
| `scope-reviewer` | review | astra/high | sol/high | terra/high | luna/max |
| `acceptance-auditor` | review | astra/high | sol/high | terra/high | luna/max |
| `goal-judge` | review | astra/high | sol/high | terra/high | luna/max |
| `status-monitor` | operations-learning | terra/medium | luna/max | luna/high | luna/low |
| `learning-curator` | operations-learning | terra/medium | luna/max | luna/high | luna/low |
