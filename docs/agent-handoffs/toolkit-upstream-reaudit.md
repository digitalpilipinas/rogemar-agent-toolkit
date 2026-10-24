# Interview and upstream re-audit

Date: 2026-10-24. Status: review complete; recommendations below are not implemented by this audit.
Owner: current toolkit maintainer. Scope: the supplied Matt/Lauren transcript,
PStack and Matt Pocock upstream changes, and the canonical local adaptations.
This record carries findings; it grants no publication or installation authority.

## Sources and candidate

| Source | Reviewed identity |
| --- | --- |
| [Interview transcript](https://gist.github.com/ayush-that/809328c80b267ffa1d23349f4bfebbac) | Gist revision `97218e7720e331a1df7215d0f53a80919f395f60`; full transcript reread |
| [PStack](https://github.com/cursor/plugins/tree/9580c23696ac8d7abed0c166f2f9918800afb819/pstack) | `9580c23696ac8d7abed0c166f2f9918800afb819` |
| [Matt Pocock skills](https://github.com/mattpocock/skills/tree/5beb35b040e3de97e54fa9e386d7e42d15c295c2) | `5beb35b040e3de97e54fa9e386d7e42d15c295c2` |
| Local base | `3cdfb485dd8d9bbfd0caeff3c8f091c0479dda16`, with existing dirty and untracked changes |
| Cached origin/main | `93c0860cb5091bdbcca9f8eb78714b0dd579e125` |
| Live toolkit main | `475ae282a086cc6932b82f3044cb66f3978de605` |

The upstream heads match the previous review. Local source pins still name
PStack `e43c7ee26e0038c6c1fa8380dd34ce86ff94cb2a` and Matt
`24fe0ef7737efae15c87225755e9f6f5965e4888`. Selective adaptations do not constitute
a full upstream upgrade.

Complete old/current PStack subtree inventories were compared; neither was
truncated. There are 141 changed or added files in that subtree. Direct
`skills/*/SKILL.md` entries grew from 50 to 58; including the three inactive
automation skills gives the earlier 53-to-61 count. The repository-wide GitHub
comparison is capped at 300 files and omits important PStack paths, including
statechart. It must not be the sole coverage source.

Review depth: full interview; complete subtree inventories; Matt's changed skill
patches; detailed reading of formal creation, maintenance, statechart, Claude
translation and generation, debugging and TDD; relevant local owners and helpers.
This is not a line-by-line security audit or execution of every upstream script.

## Required corrections

### R1. Reconcile writer isolation policy

`workflow-orchestrator/references/global-working-instructions.md` explicitly
permits simultaneous writers sharing a worktree with non-conflicting scopes.
`workflow-orchestrator/references/operating-contracts.md` serializes writers in a
shared worktree. `skill-collaboration.md`, Codex runtime and Claude runtime require
isolated worktrees for concurrent writers. Integrated Workflow's file ownership
rule does not resolve this contradiction.

Effect: the same assignment can be accepted or rejected depending on which
entry/reference the agent loads. These rules must share one authoritative policy,
with harness-specific restrictions explicit. Preserve the operator's existing
collaboration edits when reconciling; do not silently choose a different policy.
Acceptance: identical scenarios resolve consistently across entry points,
including separate files with shared generated outputs or mutable resources.

### R2. Make plan-contract extraction respect Markdown fences

`codex-forge/scripts/check-plan.mjs:parseContract` uses a multiline regex that
matches a triple-backtick `forge-contract` nested inside a four-backtick example.
During this audit, a document containing only such an example produced
`parsedGoal: "Example only"` and an empty structural-error list. The existing
three parser tests passed. This is a pre-existing helper defect, not a regression
introduced by the timeout changes.

Effect: an example can be mistaken for the live task contract; an example plus a
real contract can also look like two contracts. Parse fence context and matching
delimiter lengths. Add behavioral cases for an outer example, one real contract
after an example, multiple actual contracts, and malformed closing fences.
Tilde-fence support should be explicit rather than assumed. Upstream fixed related
fence parsing, but our contract format differs, so port the behavior and tests
rather than replacing our checker wholesale.

### R3. Record selective upstream provenance

`catalog/imported-sources.json`, `catalog/codex-forge-upstream.json` and the
playbook source map retain the older pins. The new mutation, readiness, framing
and formal-verification adaptations are not fully traceable there to the newer
reviewed sources. Existing MIT notices remain present.

Keep base pins truthful and add per-adaptation source paths, revisions, local
owners, intentional differences and verification status. Do not advance every
pin to imply a complete import. Regenerate hashes and routing only after this
metadata and the actual changes agree.

### R4. Integrate the current toolkit main before aggregate acceptance

Local base is 12 commits behind live main. The earlier byte-level comparison
found 18 local-only files, 69 differing shared files, 50 remote-only files and
nine locally untracked files identical to remote. Remote-only files were absent
from local HEAD, not deleted by our work. Newer main includes harness manifests,
installation improvements, Devin support, Diagram Design integration and assets.

Preserve both sides and reconcile overlapping contracts and generated catalogs.
Existing passing checks validate the older local combination, not this future
integration. Keep the initial snapshots and pending user edits intact.

## Capability extensions needed for the stated objective

### C1. Complete the formal-verification lifecycle

The local `code-review-tests/references/formal-verification.md` is a useful bounded
method. Its watcher pilot checks a sleep-budget property, not general concurrency
or liveness. The broader capability remains partial.

Adopt these missing parts from upstream's
[creator](https://github.com/cursor/plugins/blob/9580c23696ac8d7abed0c166f2f9918800afb819/pstack/skills/create-formal-verification-skill/SKILL.md),
[maintainer](https://github.com/cursor/plugins/blob/9580c23696ac8d7abed0c166f2f9918800afb819/pstack/skills/maintain-formal-verification-skill/SKILL.md)
and [statechart](https://github.com/cursor/plugins/blob/9580c23696ac8d7abed0c166f2f9918800afb819/pstack/skills/statechart/SKILL.md):

- Select the technique by the property: event-order model checking, verification
  of implementation code, generated inputs through real code, or proof where
  unbounded claims require it. Do not label generated tests as formal proof.
- Generate an executable project-specific verification skill with actual commands,
  covered symbols, bounds, tool versions and synchronization metadata; run those
  instructions as a fresh consumer would.
- Review all changes since synchronization, including renamed/moved symbols and
  newly introduced writers of guarded state. Existing symbol lists alone can miss
  a new mutation path. Record intentional specification changes and reduced bounds.
- Provide executable statechart/model conversion, orthogonal-state support,
  safety versus reachability interpretation, readable counterexample paths,
  omissions and replay through implementation entry points.
- Keep model drift, product defects and blocked verification distinct; do not
  weaken properties to make checks pass or claim code correctness from a drawing.

Dedicated creator, maintainer and statechart methods are justified if they make
these responsibilities easier to discover and execute. They should contribute to
the existing testing owner and orchestrator. Add conditional routes and retain
specialist examples. Upstream `tlc-tools.mjs` can install Java/TLC automatically;
adapt this to existing dependency preparation and actual installation authority.
Do not run it during a read-only source review.

Acceptance: a nontrivial retry/concurrency example; an intentionally broken real
implementation caught by checks; drift caused by a new state writer; and a model
counterexample classified correctly after implementation replay.

### C2. Port concrete Claude compatibility improvements

The official adapter is a
[translation guide](https://github.com/cursor/plugins/blob/9580c23696ac8d7abed0c166f2f9918800afb819/pstack/docs/harness/claude-code.md)
plus a [generated harness tree](https://github.com/cursor/plugins/blob/9580c23696ac8d7abed0c166f2f9918800afb819/scripts/generate-pstack-harness-trees.mjs).
Calling it an inherently competing orchestration framework was inaccurate.

Our runtime already has schema discovery, profile evidence, required/optional
failure behavior and scoped recovery. Extend it with tested handling of:

- A skill invocation tool refusing an explicit-only skill: read its instructions
  only when the current invocation/adaptation policy permits that use.
- Reviewer agent types that still expose shell writes: a role label alone is not
  isolation; inspect changes against the pre-existing dirty baseline afterward.
- Worker-specific MCP/tool availability, missing resume support, result-based
  continuation and actual completion notifications.
- Packaged adapter/resources/links, consistent skill names and generated-tree drift.

Keep our stronger rules where upstream suggests guessing the current transcript
from the newest file or skipping unavailable required operations with placeholders.
Do not hard-code upstream model aliases as proof of current availability.
Integrate newer toolkit manifests before adding duplicate packaging infrastructure.

### C3. Qualify automatic routing and cross-harness continuation behavior

The method receipt now distinguishes selected/read/applied/verified, but the file
resolver does not evaluate task-to-method selection or native execution. The
interview emphasizes observing actual outcomes and removing human bottlenecks.
Metrics fields and instructions create the measurement method, not evidence that
supervision or cost has fallen.

Exercise representative tasks with expected outcomes, failure cases and controls:
small correction needing no specialist; UI startup with missing fixtures;
correlated reports with distinct reproductions; consequential state-machine work;
unavailable required versus optional tools; interrupted handoff with stale evidence;
and a receiving harness lacking the sender's tools or uncommitted code.

Record outcome quality, missed/irrelevant methods, human corrections, context
transfers, retries, elapsed time and total tokens when actual telemetry exists.
Compare equivalent tasks, include unsuccessful attempts and keep host results
separate. Existing host-qualification and CodeRabbit gates remain unresolved.
This review did not retest credentials or establish the requested Astra High
parent identity.

## Existing improvements to retain

| Interview/upstream practice | Local state |
| --- | --- |
| Correlate reports before dispatch | Added to bug-triage, preserving separate cases and uncertainty |
| Review completed outcomes for structural prevention | Added under Engineering Playbooks; native/process effectiveness unmeasured |
| Count avoidable human intervention | Added to ME-01; no measured reduction claimed |
| State qualification limits and reversibility | Added to AQ-01 |
| Respect remaining polling timeout | Fixed and regression-tested in earlier implementation |
| Verify initialization and usable journeys | Added to verification creation and maintenance |
| Confirm deliberate mutations and relevant failure | Added to debugging/test guidance |
| State test-boundary coverage and blind spots | Added to code-review-tests |
| Cheap diagnostic signal after expensive debugging | Added to root-cause guidance |
| Complete pending-decision catch-ups and framing lens | Added within existing owners |
| Read and communicate existing task handoffs | Added to entry/resume guidance; local records exist |
| Preserve unique reflection guidance | Restored useful examples while retaining shared rules |
| Watcher thread pagination and fork discrimination | Already handled locally; no duplicate upstream patch needed |
| Worktree default-branch portability | Local Python helper already resolves the target rather than assuming origin/main |

Matt's changed debugging/TDD practices are substantially covered. Additional useful
refinements are explicit repository-standards discovery and tracker identity
discipline: resolve actual ticket references before work, create real IDs before
linking dependencies, and distinguish research decisions from implementation-ready
tasks. Adapt these only in the corresponding review/planning/tracker route; his
tracker commands and wizard fixes are not automatically applicable local defects.
His experimental chief-of-staff can inform dated, source-cited knowledge, but its
blanket delegation/continuous-improvement behavior is not a default to import.

Preserve proportional delegation, existing authorization, bounded history recovery,
and durable repository handoffs. Upstream temporary handoffs do not replace the
operator's explicit cross-machine continuity requirement. Current records are
local-only until authorized publication is completed and remote contents checked.

## Order and completion evidence

1. Reconcile local/main and instruction ownership; fix the parser and provenance.
2. Complete formal creation, maintenance and statechart methods with real examples.
3. Extend and qualify Claude translation and package behavior.
4. Run task-based routing, failure/recovery and cross-harness trials; measure cost
   per accepted outcome rather than text length or PR volume.

Any subsequent skill/dependency changes require lock, verify, unit tests and both
release-package checks, plus affected behavior tests and outstanding review gates.
Do not delete unique guidance to achieve a size target. A broad capability matrix
should identify supported, tested, partial and unavailable task families; these two
upstream libraries alone cannot establish coverage of every possible project.

Audit validation: three existing plan-parser tests passed; a separate controlled
input demonstrated the nested-example parsing defect. Source inventories and
selected executable paths were inspected. No full suite, native cross-harness
trial, formal tool installation or CodeRabbit review ran in this audit.
Only this review record and its index entry were added. No skill or runtime code
was changed, committed, pushed or installed.

Next action: implement the required corrections on a reconciled candidate, then
advance the capability and host-qualification work above. These recommendations
do not retroactively mark earlier implementation tasks or their gates accepted.

## Implementation follow-through

The subsequent operator request authorized the necessary updates and committing
all intended changes to align GitHub. See [integration and publication](toolkit-publication.md)
for fixes, combined-candidate checks and outstanding runtime/delivery gates. This
review remains a historical observation of its named candidate, not current
publication or qualification evidence.
