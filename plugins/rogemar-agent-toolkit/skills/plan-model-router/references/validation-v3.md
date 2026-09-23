# Codex Forge five-mode validation — 2026-09-13

The installed policy now has five modes. This release changes routing constraints
and supplies evidence-backed defaults; it does not claim that every profile has
passed every quality test or that the running parent switched.

## Historical, proposed and validated configurations

The unchanged historical analysis comprises 28 runs and 1,176 workers on 42 focuses.
Its 40 matching-contract focuses exclude two pinned native GoalBuddy cases from
uniform-profile causal comparisons. Three main-owned roles have no isolated worker
measurements. The frozen assignment-ledger SHA-256 is `6f1c57136d9edd2aa054e5c49f930c978717d927aef6d7b203c13964019154e2`.

| Policy | Historical parent recommendation | New parent target | Normal assignment rule |
| --- | --- | --- | --- |
| Default | Not an installed mode; uniform-profile tests existed | Exact user-selected profile | Identical ordinary parent/worker model and effort; no exceptions |
| Peak | Astra/high | Astra/xhigh | Astra core; evidence-qualified lower supporting profiles within both ceilings |
| Balanced | Sol/high | Sol/xhigh | Sol core; suitable lower supporting profiles within both ceilings |
| Lean | Terra/high | Terra/xhigh | Terra core; Luna support; no Astra/Sol |
| Economy (sprint alias) | Sprint: Terra/medium | Luna/medium | Luna low/medium normal pool; direct work when sufficient |

These historical recommendations describe the installed v2 policy, not every run's
actual coordinator; historical Peak also ran with other observed parents.
`budget` still means Lean. Current actual parent and mode ceilings both constrain
normal workers. An accepted higher parent cannot enlarge the mode. An accepted
lower parent may leave core worker dispatch unavailable; direct parent work does
not satisfy an independent gate. Parent changes remain separately verified actions.

The [45 × 5 mapping](role-mapping.md) is generated from the executable catalogue.
Its [225-row evidence ledger](role-evidence.json) carries normal and fallback
profiles, individual historical assignment IDs, findings, raw tokens, estimated
account credits, response rounds and duration. Default stays dynamic; its missing
historical coverage is explicit. Main-owned and ordinary Goal roles are not
assigned misleading native-worker historical measurements.

## Fresh controlled validation

Fourteen fresh workers covered seven profiles, two repetitions each, with ten
identical supplied focuses: authorization, hillclimb, retry-safe creation,
source tracing, bug triage, interaction alternatives, architecture, cross-judging,
correctness review and independent acceptance. Roles were deduplicated across
modes. The full packet, its hash, saved answers, five-criterion assessments,
profile metadata and usage are in [validation-v3.json](validation-v3.json).

Each worker answered all ten focuses in one batch. This differs from the historical
single-focus packet: compare fresh profiles within this cohort, not their batch
cost against a historical individual role. Usage is recorded per batch, never
invented for individual answers. The same supplied context and permitted read-only
packet access were used. Thirteen workers used one read; Sol/xhigh repetition two
first made three failed process-start attempts with wrong working directories,
then read the correct packet. Those failures and their usage remain included.

Two independent graders saw shuffled IDs, answers, source and rubric without model
or usage. Main reconciliation retained all 31 concrete findings. All 140 answers
met the 150-word bound. There were **109/140 fully passing focused answers**;
this is task-specific coverage, not a percentage of general coding intelligence.

| Fresh profile | Focuses passing (two × ten) | Worker tokens | Response rounds | Median batch seconds | Estimated Standard credits | API-equivalent USD |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Astra/xhigh | 18/20 | 161,987 | 4 | 108.4 | 20.254150 | 0.810166 |
| Sol/xhigh | 18/20 | 304,650 | 7 | 83.0 | 10.302120 | 0.412085 |
| Terra/xhigh | 16/20 | 175,806 | 4 | 63.5 | 4.456020 | 0.178241 |
| Luna/medium | 14/20 | 167,308 | 4 | 57.6 | 0.398185 | 0.015927 |
| Luna/high | 12/20 | 170,537 | 4 | 86.0 | 0.493330 | 0.019733 |
| Luna/xhigh | 18/20 | 175,905 | 4 | 131.2 | 0.649370 | 0.025975 |
| Luna/low | 13/20 | 166,504 | 4 | 44.8 | 0.372784 | 0.014911 |

These are worker-batch measurements, excluding coordinator, grading, review and
Goal probes. Cached input is already included in raw tokens; reasoning is part
of output usage. Credit and API-dollar scenarios use the frozen September 11
rate card, per response. They are neither an invoice nor subscription-cost or
current-allowance estimates. Sample size, unequal cache and one tool-retry outlier
prevent a reliable latency or intelligence ranking.

## Paired results by role

Each cell is passing repetitions out of two. A failed cell remains evidence of
that omission even when a more capable profile is available.

| Role | Astra/xhigh | Sol/xhigh | Terra/xhigh | Luna/medium | Luna/high | Luna/xhigh | Luna/low |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bug-fix` | 2/2 | 2/2 | 2/2 | 2/2 | 1/2 | 1/2 | 1/2 |
| `hillclimb` | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 |
| `hardest-tasks` | 2/2 | 2/2 | 2/2 | 1/2 | 1/2 | 2/2 | 0/2 |
| `how-explorer` | 2/2 | 1/2 | 2/2 | 1/2 | 0/2 | 2/2 | 2/2 |
| `bug-triager` | 1/2 | 1/2 | 0/2 | 0/2 | 0/2 | 1/2 | 0/2 |
| `reflect-divergent` | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 |
| `architect-runners` | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 |
| `arena-cross-judge-pool` | 2/2 | 2/2 | 1/2 | 2/2 | 1/2 | 2/2 | 2/2 |
| `correctness-reviewer` | 1/2 | 2/2 | 1/2 | 0/2 | 1/2 | 2/2 | 0/2 |
| `acceptance-auditor` | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 |

## Promotion and remaining gaps

- **Economy hillclimb: Luna/high qualified**, with two passing repetitions and
  exact evidence ID `economy-hillclimb-v3`. Luna/medium also passed both fresh
  hillclimb focuses; the historical omission justifies keeping a selective
  exception available, not a claim that High is always necessary or better.
- **Economy hardest-tasks: Luna/xhigh qualified**, with two passing repetitions,
  versus one of two for Luna/medium. Evidence ID `economy-hardest-tasks-v3`.
  The evidence covers a reasoned authorization/idempotency boundary, not a
  deployed concurrent storage implementation. Luna/max is not substituted.
- **Bug triage remains unresolved across all seven tested profiles** under the
  two-pass requirement. Errors include omitted update authorization and UI
  failures. Updated handoffs require a full defect inventory before prioritizing;
  this instruction change is installed but its effectiveness is not yet proven
  by another paired cohort. No unproven model substitution or retry loop is used.
- **Terra/xhigh** passed the new exploration and interaction pairs, while its
  second cross-judge incorrectly called supplied timing evidence absent. Source
  tracing requirements distinguish absent evidence from weak evidence.
- **Sol/xhigh** passed the new cross-judge pair. A source-tracing answer still
  misstated the presence of executable source; raising effort is not a remedy
  established by these tests.
- **Astra/xhigh** still omitted a pending-duplicate UI defect and understated a
  valid non-contiguous-ID collision. Core review remains consequential work;
  lower cost alone does not justify reducing the parent's reasoning.

Normal mapping evidence states: **31 newly verified**, **119 historical**,
**10 provisional**, **65 unavailable**. Unavailable includes the 45 dynamic Default
rows, 12 preset parent-owned rows and eight ordinary Goal Scout/Judge rows.
Only covered profile/focus pairs receive new quality verification. Provisional
rows retain the disclosed parent fallback with unresolved quality status.
Supporting defaults use eligible historical criteria/checks, estimated account
credits then duration; they still require current task fit. Core rows start with
the parent profile. No role-name-only ceiling escape is permitted.

## Executable and runtime evidence

- Fourteen proposed authorization functions passed 70 bounded checks for owners,
  non-owners, missing IDs and preservation. Three needed literal-newline/markdown
  decoding to run; their original formatting failures remain in the grading.
- Seven source/data-boundary counterexamples reproduced unauthorized reading,
  unguarded updating, whitespace updates, blank creation, duplicate retries,
  non-contiguous ID collisions and uniqueness without a replay-return branch.
- All 14 fresh workers' effective models and efforts matched native metadata.
  Catalogue tests cover every 225 role/mode combination, Default exactness,
  aliases, both ceilings, explicit limits, fallback binding, role requirements,
  preference migration, unsupported profiles and exact paired exceptions.
- Ordinary Scout and Judge used Luna/medium through unpinned read-only agent types.
  Native Scout used Terra/low and native Judge Terra/high, with their own
  GoalBuddy JSON receipts. Judge rejected an unsupported completion claim.
  These four one-shot probes establish routing/receipt behavior, not general
  role quality. Incompatible mandatory pins are rejected before dispatch.
- The independent router review found and verified fixes for missing-role bypass,
  malformed Default override fallback, parent-proposal limit bypass and rejected
  fallback when the desired model was unavailable.

Mode changes qualify newly dispatched workers; they do not switch existing
workers or prove parent coordination quality. This maintenance task used explicit
trial profiles and fixture parents for policy checks. No live parent switch,
rendered app, browser/device qualification, GitHub publication, external-provider
review or dashboard redeployment is claimed.
