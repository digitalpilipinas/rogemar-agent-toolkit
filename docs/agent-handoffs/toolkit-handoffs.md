# toolkit-handoffs: Maintain portable task handoffs

- Status: completed at implementation/local-check boundary; aggregate acceptance blocked
- As-of UTC: 2026-10-24T13:25:33.451158+00:00
- Authority/status source: active operator-approved toolkit update and harness-handoff request; this task record is the local status source.
- Owner: main toolkit maintainer; dependencies: toolkit-methods.

## Scope and decisions

Maintain one indexed record for every approved planned, active and completed task; preserve plan/board authority and distinguish local from verified remote state.

Delivery is local-only under repository instructions. No commit, push, tag,
publication, installation, connector login or background service is authorized.
Preserve preexisting local changes. Shorter text is not an acceptance criterion.

## Candidate and continuity

Branch `main`, base HEAD `3cdfb485dd8d9bbfd0caeff3c8f091c0479dda16`, with uncommitted changes.
HEAD alone does not identify this candidate. See `candidate.json` for the bounded
source manifest once validation is complete. Relevant source pointers:

- `plugins/rogemar-agent-toolkit/skills/integrated-workflow/references/durable-handoffs.md`
- `plugins/rogemar-agent-toolkit/skills/integrated-workflow/assets/task-handoff-template.md`

No task-owned external action has been started. Local test logs are transient and
are not available on another machine; rerun the recorded repository commands when
current evidence is required. Preserve unrelated tracked and untracked work.

## Methods and evidence

Codex Forge, capability maintenance, the applicable review/testing methods and
Integrated Workflow were used within one orchestration owner. Unique reflection
examples were restored; the shared rule corrections remain. Source references
and actual executable checks support the local changes; no automated semantic
selection benchmark or protected native-runner proof is claimed.

Local validation passed: 246 repository unit tests; 21 Project Learning tests;
93 watcher tests; strict TypeScript check; toolkit lock/verify; Forge verification;
generated inventory check; core and full release-package checks; Git whitespace
check. The bounded model covered 1,764 transitions; its mutation and the isolated
production mutation exposed the intended deadline defect. Twenty method/file
resolution checks passed across four entry adapters. Those file checks do not
establish native selection, independent review or cross-machine resume behavior.

This task's implementation/check boundary is complete. Aggregate Integrated
Workflow acceptance still requires the review recorded in `toolkit-host-qualification.md`.
CodeRabbit is unauthenticated. No native cross-host qualification or effective
GPT-6 Astra / High parent profile has been established. The source manifest in
`candidate.json` identifies the validated local files, not a published commit.

## Next action and decisions

Resume `toolkit-host-qualification` for the authenticated review and native trials.
Do not rerun unchanged passing checks solely because the harness changed; first
reconcile the current candidate and refresh only invalidated evidence. The local
handoff/index is discoverable through repository `AGENTS.md` and the shared entry
contract. Agents must announce the loaded task record and any material gap.

Publication is now authorized; applicable delivery gates remain required. No product-scope decision is needed
for the completed local changes. Final acceptance stays blocked until the required
review is completed or the owner explicitly changes that gate.

## Local and cloud availability

Local-only; records and associated edits are uncommitted and unpushed. GitHub
handoff availability has not been verified. A remote harness cannot recover these
dirty changes from HEAD or from these descriptions alone. Transfer the actual
candidate through an authorized route before a remote handoff.

## Harness receipt

Codex Forge Peak requested with GPT-6 Astra / High; effective parent model/effort
unverified. The router reported missing active-parent metadata, so no qualified
worker dispatch or parent switch is claimed. Integrated Workflow retains its
required gates. Local fixtures are not native multi-host qualification.
