# Plan: reliable automatic method selection and maintained skill distribution

Status: approved for execution on 2026-10-05 by the owner through Integrated
Workflow. Active increment: A. Delivery: branch + PR + safe merge, followed by B
and authorized managed rollout. No additional provider or deployment authority.

Prepared 2026-10-05 against clean local `main` at
`e1e21aa2bf30cf18e48ff5e9e79fce46b1aacda7`. The source review covered closed
PRs 1–13, the current workflow and installer, and pinned upstream sources.
Refresh the target, working tree and relevant upstream evidence when execution
starts; a planning snapshot is not permission to discard intervening work.

## Outcome

Once Integrated Workflow is invoked for an approved programme, the owner
selects or deliberately reuses applicable methods for every task and worker
handoff, checks the prerequisites needed now, verifies the result, and advances
to the next approved dependency-ready task through the authorized PR boundary.
The user normally needs only `create-plan` and `integrated-workflow`.

New compatible environments can install the selected toolkit and declared
third-party skill files from reviewed revisions. Maintenance detects relevant
upstream drift without silently changing task instructions or runtime tools.

Completion requires coherent source changes, the required package and behavioral
checks, and a separate installation/discovery receipt for each environment that
is actually updated. An unreachable cloud environment remains unverified; it
does not turn source delivery into a claim of complete environment alignment.

## Ownership and fixed boundaries

- `create-plan` owns planning; `workflow-orchestrator` selects methods and
  dispatches workers; Integrated Workflow owns approved delivery; the matched
  Forge adapter supplies native bindings. Keep one implementation owner and
  the existing acceptance record.
- Use `AGILE_FOCUSED`: the main agent writes and integrates. Independent
  read-only support is optional when useful. This work shares catalogs,
  generated artifacts and contracts, so parallel writers are unnecessary.
- Preserve the minimal core profile and full compatible profile, current
  entry names, explicit-only skill controls, native model controls, and
  independent review/provider procedures.
- Keep preparation in the existing workflow. Environment provisioning and
  task readiness are separate stages, not new top-level workflows.
- Keep semantic selection with the agent. Validate concrete selection
  constraints mechanically; do not build a keyword dispatcher or claim
  universal model compliance.
- Preserve task authority, platform limits, user changes, secret handling,
  inactive learning candidates, licenses and recoverable installations.
- Do not add a second board, scheduler, permanent watcher, new global hook,
  mandatory retro, or full dependency audit to every task. Do not change
  native sandbox or approval settings.
- This plan does not authorize implementation or publication. An explicit
  execution instruction supplies the delivery boundary. Existing review
  requirements apply unless the owner explicitly changes the affected gate;
  prior task-specific waivers are not inherited.

## Delivery sequence

Use two ordered, coherent PRs, followed by installation of the accepted version.
These are delivery slices, not a requirement for a PR or review per task.

| Increment | Scope and observable result | Depends on |
| --- | --- | --- |
| A — accurate routing and continuous task handoffs | Correct method identity, individual external metadata, consistent shared/native contracts, and focused behavioral coverage | Refreshed source preflight |
| B — maintained sources and bounded supporting methods | Reviewed upstream updates, useful Matt Pocock adaptations, and a repeatable maintenance comparison | A accepted and target verified |
| C — managed rollout and environment evidence | Accepted revision installed and checked in each reachable authorized destination; remaining conflicts/access limits named | B accepted and target verified |

### A. Accurate routing and continuous task handoffs

1. Reconcile every current vendored routing record with its actual skill
   description, instructions and portable fallback. Fix confirmed differences,
   starting with `forge-interrogate`, `forge-setup` and the broad
   `forge-automate-me` route. Preserve adversarial review, Codex profile setup
   and personal-style capture as their actual purposes. Route ordinary
   clarification to planning and capability setup to the capability maintainer.
2. Extend the existing dependency recipe records with per-skill metadata
   obtained from each pinned source, retaining the current name-to-path map.
   Store source identity, description and invocation policy, plus reviewed
   applicability, prerequisite, overlap and resource information where needed.
   Do not invent prerequisites from keywords. Keep native metadata distinct
   from documented toolkit adaptations.
3. Generate the routing index from that catalog. Stop substituting the family
   purpose for every member's trigger. Offline verification checks that the
   metadata matches its recorded pin and complete skill membership. Source
   extraction/comparison occurs only during approved maintenance, never during
   ordinary task selection or offline verification.
4. Extend the existing resolver only where concrete constraints need checking:
   explicit-only invocation, selected resources/dependencies, harness/platform
   eligibility, conflicting copies, overlapping methods and worker handoffs.
   Preserve existing callers and supported receipt fields. Metadata describes
   applicability; it cannot prove a model made the right semantic choice.
5. Establish one shared task-boundary contract and link to it from the lifecycle
   and affected playbooks. At each new task, delegation, resume or material
   change, select or reuse the smallest sufficient route. A small known-file
   correction can require no specialist or helper invocation.
6. Carry the choice and its relevant instructions, readiness observations,
   required evidence and next action in the existing task/worker receipt.
   Reuse valid observations with their provenance. Refresh only facts affected
   by changed scope, skill/dependency content, environment, credentials or
   runtime state. Keep behavior evidence bound to the actual candidate.
7. Continue from accepted work to the next authorized dependency-ready task.
   Reuse a slice's branch/draft across sprints, preserve intended PR dependencies
   and recompute the next safe task after a merge or changed prerequisite.
   Missing required authority/evidence blocks its dependent action; sufficient
   independent approved work can continue. Stop at the named delivery boundary.

Primary files:

- `catalog/skills.yaml`, `scripts/routing_catalog.py`, and the generated
  `workflow-orchestrator/references/skill-routing.json`.
- `workflow-orchestrator/scripts/select_methods.py` and its existing
  method, stage, readiness and worker-handoff references.
- `integrated-workflow/SKILL.md` and `references/execution-loop.md`.
- Shared `engineering-playbooks` and affected Codex playbook counterparts:
  feature, bug-fix, investigation, refactoring, perf-issue, autonomous-run,
  autopilot-full, autopilot-stack, orchestrate, session-pickup and skill authoring.
- `codex-forge`, `cursor-forge`, `universal-forge`, the portable companion
  references and source maps. Keep upstream native PStack files intact.
- Existing create-plan templates, worker briefs and evidence instructions.
  There is no need to create a separate workbook system.

All skill paths above are relative to
`plugins/rogemar-agent-toolkit/skills/` unless otherwise identified.

### B. Maintained sources and bounded supporting methods

1. Refresh the reviewed comparisons before choosing update commits. The
   2026-10-05 review identified these relevant candidates:

   | Source | Reviewed candidate | Benefit |
   | --- | --- | --- |
   | CodeRabbit | `59945da347a93f9937d3fb09f5ba81a16010351f` | Authentication recovery and faithful reported severity |
   | Argent | `19461cb7a96822b75996a7387ba05d9fade615f5` | Correct clipboard guidance |
   | Expo | `13ad8e05874195633b5c185f6947bb6400e228fc` | Remote iOS crash/log investigation |
   | Convex | `2cfe645c87f971242cfc8ef3eb53662cbec26a53` | Explicit request for transcript-feedback submission |
   | Ponytail | `c982cd411abb53323c4baa1baa3c2f020b8d0b08` | Reuse guidance, deletion investigation and debt scanning |

   Supabase's newer commits were release metadata only. Update its recorded
   metadata only where useful; do not present it as a behavior change. Retain
   unchanged Swift, PStack, Unlazy, OpenDesign, Matt Pocock and TesterArmy pins
   unless a newly reviewed relevant change justifies updating them. Installing
   new skill text does not silently upgrade the corresponding runtime or plugin.
2. Preserve notices and required resources, regenerate the per-skill metadata
   using A, and check changed external instructions against the toolkit's
   provider, privacy and invocation boundaries. Preserve independently installed
   or edited copies instead of silently taking ownership.
3. Classify existing third-party records as selected-pack skill requirements,
   conditional runtime integrations, or reference-only sources. Required skill
   files need a usable pinned installation recipe; a URL alone is insufficient.
   Keep unverified redistribution rights and provider-owned caches external.
   Repair stale source identities and counts, including the GoalBuddy redirect
   and Argent family-count prose. Generate inventories where practical.
4. Add a small read-only comparison helper to the existing maintainer workflow:
   report pinned versus observed revisions, affected paths and comparison
   failures for selected declared sources. It must never install, repin, log in,
   execute fetched code, or treat a network failure as 'current'. Use existing
   source records and UP-01; do not create a general update service or scheduler.
5. Adapt the selected Matt Pocock methods from reviewed source
   `24fe0ef7737efae15c87225755e9f6f5965e4888`, preserving MIT attribution and
   recording the local adaptations in the existing provenance system:

   | Method | Existing owner and bounded behavior |
   | --- | --- |
   | Grilling | `create-plan`: investigate facts, ask only material unresolved decisions in useful batches, and reuse settled answers. A user can request a fuller interview; ordinary tasks do not require one. |
   | Retro | Shared reflection and capability maintenance: diagnose evidenced environment/navigation/tooling friction and propose economical prevention. Enrolled Project Learning remains the only candidate writer. |
   | Writing for agents | Skill authoring/maintenance: precise triggers, completion criteria, conditional references and removal of duplicated guidance. |
   | Domain modeling | Existing planning/architecture methods: consistent terms and concrete edge cases; use project documentation conventions and create records only when useful. |
   | Diagnosis and TDD | Existing bug-triage/test methods: exact symptom reproduction, meaningful behavioral assertions and narrow feedback loops, without mandatory approval of every test boundary. |
   | PR and handoff | Existing delivery templates: concise before/after evidence, reversibility and useful method pointers. |

6. Prefer attributed references under existing owners over new discoverable
   wrapper skills. Preserve `forge-reflect` and portable reflection coverage;
   keep `forge-interrogate` an adversarial-review method. Do not install Matt
   Pocock's competing execution/router flows or remove upstream explicit-only
   restrictions to make an unadapted command automatic.
7. Integrate economical retro assessment at a verified milestone when there is
   meaningful evidence or friction. No forced finding, new reviewer, global
   memory write, automatic lesson promotion or mandatory retrospective report.
   A useful correction already within approved scope may proceed; a broader
   policy/environment change remains a concrete proposal.

Likely additional files: existing dependency/provenance records; the capability
maintainer and its references; `create-plan` references; shared reflection and
`forge-reflect` references; Project Learning integration guidance if needed;
bug-triage/testing and PR/handoff references; installation/compatibility docs,
README inventory and changelog. Preserve existing learning storage and schemas.

### C. Managed installation and environment verification

1. Use the accepted target revision and the managed installer. Preview each
   destination before mutation. Preserve saved selections unless full-profile
   alignment is explicitly part of the execution grant; the intended owner
   outcome here is the full compatible skill set on authorized destinations.
2. Inventory the existing local Codex, Cursor, Claude, Droid and shared layouts.
   Choose one primary managed copy per discovery path; do not copy provider
   caches, erase unique local changes or install duplicate wrappers. Reconcile
   any conflict using its actual ownership and reviewed contents. Unresolved
   conflicts remain visible, not reported as full alignment.
3. Update reachable cloud/project environments through their existing supported
   shell/setup route, preserving project dependency setup. Record any persistent
   setup-script change separately from an update to a running environment.
   Do not create replacement projects or assume a saved environment rebuild
   retroactively changes an existing VM.
4. Verify the toolkit revision, selected packs, per-skill resource/content
   hashes and actual harness discovery inside each receiving environment.
   Use selected tool/authentication checks only where relevant; copying skill
   files does not establish native plugins, devices, accounts or paid services.
5. Verify how the actual host refreshes discovery. Report a needed reload/new
   session only when observed or documented for that host; do not promise live
   refresh or rely on a local sync indicator. Existing sessions may be able to
   read an updated file explicitly even when their discovery list is stale.
6. Keep the installer backups and operation receipts for rollback. Do not
   roll back unrelated user changes or delete independent installations.

Cloud targets and shell/control access are not qualified by this planning pass.
If access is absent at execution, supply the exact reviewed bootstrap/update
instructions and the missing verification step; report those environments as
unverified while completing reachable authorized destinations.

## Acceptance and proportional verification

| Requirement | Meaningful proof / counterexample |
| --- | --- |
| Correct method identity | Adversarial review selects the real interrogate method; clarification and general tool setup do not select that method or Codex model setup by mistake. Inspect instructions as well as metadata. |
| Individual external routes | Distinct methods in the same family have distinct useful triggers. Every recipe member is represented with matching pin and invocation policy; missing/stale metadata is detected. |
| Continuous selection | An approved multi-task fixture changes from SwiftUI work to E2E to a small documentation task. Selection changes appropriately, completed tasks stay completed and the next dependency-ready task is reached without repeated workflow invocation. |
| Minimal overhead | The documentation correction does not start an interview, load unrelated specialists, authenticate services or trigger a whole dependency audit. Unchanged readiness can be reused with its provenance. |
| Explicit invocation and authority | Explicit-only methods remain explicit. Feedback submission, paid runtimes, publication and global learning changes never gain authority from automatic selection. |
| Worker continuity | An available bounded worker receives the actual applicable methods, instructions, scope, readiness limits and required evidence. A worker without required capabilities does not report success. |
| Missing/stale prerequisites | Missing resources, conflicting copies, unsupported platforms, invalidated authentication/readiness and altered artifacts produce useful blocked/unverified results. Optional absence uses a sufficient existing fallback. |
| Bounded grilling and retro | Settled decisions are reused; routine work does not trigger exhaustive questioning. Retro proposals cite a real failure/friction and preserve learning enrollment and inactive-candidate boundaries. |
| Controlled update comparison | Changed, unchanged, metadata-only and unavailable-source cases are distinguishable. The helper makes no installs, pin edits or authentication changes. |
| Distribution and recovery | Clean install, repeat install, unchanged-owned upgrade, local-change conflict preservation, duplicate discovery and rollback retain their expected behavior across supported layouts. |
| Actual environment result | Installed hashes/resources and host discovery are observed per destination. Local proof, package proof and cloud proof remain separate. |

Extend existing routing/readiness, execution-lifecycle, external-install and
imported-skill tests for the affected behavior. Avoid tests that merely assert
prose contains a prescribed phrase. Unit fixtures validate the helpers; they do
not prove that a real agent selected correctly or continued work.

During implementation, exercise representative Codex, Cursor and portable
handoffs where their native runtimes are reachable. Use task-owned fixtures and
the current authorized runtime; no new paid provider is required by this plan.
Do not rerun application/device suites just because skill text changed. A real
device/runtime change, if later required, receives its own applicable checks.
Unavailable native trials remain unverified and limit the portability claim.

After each coherent source/dependency slice:

1. Regenerate changed routing/inventory artifacts and then `toolkit.py lock`.
2. Run `toolkit.py verify`, routing verification, README inventory checks and
   Forge verification.
3. Run the repository unit suite and change-relevant owner suites selected by
   `scripts/select_checks.py`; preserve the current CI matrix.
4. Build/check both core and full release packages, retaining canonical payload
   and resource checks. Core-only operation must remain usable.
5. Review the complete slice once at its existing acceptance boundary; rerun
   affected checks after material fixes. Reuse valid evidence. Do not create a
   full provider review cycle for every intermediate task or commit.
6. Complete the active Integrated Workflow's required local/PR review and CI
   gates before merge. Any owner-approved exception must be explicit for this
   plan's affected gate and recorded as waived, not passed.

## Risks, recovery and completion report

- Metadata can agree structurally while describing the wrong behavior. Use
  source-grounded scenario review and actual host trials, not only a green hash.
- New upstream text may expand permissions, tool assumptions or dependencies.
  Review its instructions and resource changes before adopting the pin.
- Shared/native adaptations may legitimately differ. Check equivalent outcomes
  and preserved native limits rather than requiring byte-identical adapters.
- Excess preparation can cost more than the failure it prevents. Keep the task
  boundary check lightweight, reuse evidence and omit irrelevant methods.
- Local edits and unavailable cloud access can prevent complete alignment.
  Preserve them and name the exact remaining destination or conflict.

Source recovery is a normal reviewed revert of the affected slice. Installation
recovery uses the existing operation receipts/backups and rollback mechanism;
independently owned files remain outside automatic replacement.

Report accepted and incomplete increments, source/PR revisions, meaningful
checks and review dispositions, installed destinations, conflicts, runtime
limitations and the next safe action. Do not infer speed, token savings,
all-model reliability or universal cloud alignment from structural success.

First execution action after approval: refresh the source preflight, confirm the
effective delivery route, and begin A using the existing canonical source and
acceptance record. No new planning ceremony is needed for later increments.
