# Learning lifecycle and evidence maintenance

Keep `.codex/project-learning/` and the accepted ledger as the existing canonical
store. The directory name does not restrict the portable method to Codex. This
extension does not create a collector, hook, second writer, global memory, new
promotion authority, or automatic activation.

## Separate the decisions

Existing Status values Accepted, Reinforced and Superseded retain their meaning.
Optional `Lifecycle:` metadata describes activity and recorded source conditions.
Activity is active, quarantined or retired. A current user requirement, source
contract or verifier remains authoritative over an old lesson.

Read the actual rule, applicability, exclusions and evidence. Quarantined/retired
entries are history, not active guidance. Source-version changes trigger relevant
revalidation. Matching recorded versions alone cannot prove factual correctness,
source authenticity or semantic applicability. A legacy entry without metadata
remains readable under existing policy; absence does not manufacture freshness.

Do not infer causality from one agent narrative. Distinguish wrong guidance from
missing context, a failed trigger, routing, noncompliance, tool/environment failure,
and an implementation defect. A quote only establishes what was recorded. A
model-generated flag must never disable source verification. Resolve references
through an authorized adapter; unsupported evidence remains unverified.

Keep existing source-turn and evidence-reference deduplication. Reprocessing one
session does not create another independent witness. Stronger corroboration helps
justify a general rule, but a verified narrow bug fix or owner decision does not
need another incident. Rejected proposals remain settled until material new evidence
arrives. Prefer executable prevention to growing always-loaded instructions.

## Metadata shape

The optional capture field `lifecycle` uses the shape in
`references/lifecycle-example.json`. It is copied into the existing candidate
payload and, after the existing promotion process, into one compact `Lifecycle:`
line. Do not put transcripts, quotations, credentials, personal data or raw tool
output in this metadata. Evidence roots are source identities, not copies.

Set `verified_at` only after the relevant verification actually occurred. Use null
otherwise. `source_versions` records the versions relevant to the rule, not every
repository dependency. Counterexamples and review triggers should remain concise.

## One existing writer

To quarantine, retire or reactivate an accepted rule after actual owner approval,
use the existing candidate-store command:

```sh
python3 -B <project-learning-skill>/scripts/candidate_store.py set-lifecycle \
  --root <project> --request <approved-request.json> --permission-mode execution
```

The request contains exactly:
`schema_version: 1`, `candidate_id`, `expected_ledger_sha256`, `lifecycle`, and
`approved_by: "user"`. The latter is provenance, not authentication. The host must
bind the actual approval to the complete intended change. `--read-only`,
`--permission-mode plan`, and `--no-learning` return before persistence through
the existing mutation guard.

The command uses the existing bounded mutation lock and atomic ledger writer. It
rejects a stale ledger hash, an unknown/duplicate entry, malformed prior metadata,
or an entry that is not Accepted/Reinforced. Cooperating tools share the lock;
an exclusive write window is still needed against an arbitrary external editor.
The operation does not promote a candidate or change product acceptance. Record
its returned hash and decision in the existing maintenance receipt, not a new log
containing private transcripts. Version control or an authorized protected snapshot
supplies the recoverable previous ledger. No automatic commit is performed.

The project validator checks present lifecycle metadata. Legacy entries remain
valid. Disabling learning still does not delete records. Retention, revoked access
and authorized deletion must include derivatives; automatic erasure is not provided
by this metadata helper.

## Staged instruction improvements

Before applying a proposed skill/instruction change: inspect the actual canonical
target; bind the proposal to that version; show its diff and evidence; apply only the
approved coherent subset; validate its behavior and discovery; retain rollback.
Do not fuzzy-apply a stale proposal, copy generated installations back into source,
or promote policy merely because tests passed. Moving a rule into a triggered skill
requires trigger and non-trigger trials even if its text was preserved.

The existing writer supplies `stage-proposal`, `apply-proposal` and
`rollback-proposal`. Each requires `--permission-mode execution`, `--root` and
`--request`; staging/application also require the accepted `--source-root`.
Plan/read-only/no-learning modes return before reading requests or writing state.

Staging requires an eligible captured global proposal and an exact request with
`schema_version: 1`, `candidate_id`, `edits`, `groups`, and `validation`.
Each edit contains `path`, `before_sha256`, and the actual UTF-8 `after_text`.
`groups` maps coherent group names to paths, partitioning every edit exactly once.
Only existing files in the captured `allowed_files` may change. Adds and deletes
use a separately reviewed patch. Staging returns the actual unified diff,
proposal ID and digest without changing targets.

An application/rollback decision contains exactly `schema_version: 1`,
`proposal_id`, `proposal_sha256`, `groups` (complete selected group names), and
`owner_decision` (the actual decision reference). The host authenticates that
reference; a string is not authority. Applying rechecks the accepted source and
all target hashes. The existing writer stores before/after snapshots and operation
state under its existing state directory. It preflights all selected files before
writing; a crash can resume only the same decision and known before/after states.
An unrelated edit stops recovery. Rollback restores only approved applied groups.
This is recoverable multi-file mutation under exclusive ownership, not an OS-wide
atomic transaction. Run recorded validation before calling a proposal successful.

## Root evidence and bounded recall

Capture evidence may contain an `event_id` and `derived_from` original/known event
IDs. The writer records immutable project-scoped lineage, including aliases from
duplicate captures, and flattens summary chains before reinforcement. Conflicting
lineage and cycles reject. Declare original roots accurately: identifiers cannot
authenticate independent observations. Legacy references remain readable and need
an independence check. Repeated locators, harness names or summaries are not new
witnesses. No raw transcripts are stored.

Project identity is an opaque hash of the resolved Git common directory, shared
by worktrees in one clone and distinct across same-named repositories. Harness is
optional provenance, not a memory partition. Worktrees reuse eligible accepted
knowledge through the existing versioned ledger workflow; no peer scanning or
second global store is added. Relocation/recloning requires explicit identity and
provenance reconciliation before reuse; legacy entries remain reviewable.

`candidate_store.py recall --root <project> --query <task> --versions versions.json`
returns bounded relevant accepted guidance. Defaults are five results and 4,000
characters. Version input maps current source identities to versions. Stale,
quarantined and retired guidance is excluded; unknown/legacy freshness requires
direct-source and applicability checks. Recall is read-only and grants no new
instruction authority. Direct source reading remains the fallback.
