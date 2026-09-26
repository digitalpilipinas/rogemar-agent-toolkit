# Project Learning Schemas

## Candidate Capture Request

```json
{
  "schema_version": 1,
  "session_id": "native session identifier from the calling harness",
  "turn_id": "native completed-turn identifier from the calling harness",
  "lesson": "Durable project lesson stated without chat quotations",
  "applies_when": "Concrete conditions where the lesson is relevant",
  "does_not_apply_when": "Concrete boundaries or exceptions",
  "evidence_level": "reported | observed | verified | reinforced",
  "evidence": [
    {
      "kind": "file | test | commit | review | decision | outcome",
      "reference": "Repository-relative path, command name, commit, or stable source ID",
      "summary": "Short paraphrase of what the evidence establishes"
    }
  ],
  "milestone": false,
  "source_project": null,
  "source_lesson_id": null
}
```

Required strings must be non-empty. At least one evidence item is required. References and summaries must not contain secret values, raw transcript text, or absolute home-directory paths.

## Candidate Event

The ignored JSONL store is append-only. Each line contains:

- `schema_version`, `event_id`, `candidate_id`, `event_type`, and `recorded_at`.
- `fingerprint` for captured and reinforced events.
- `source` with session and turn IDs.
- `payload` containing the validated structured lesson for captured or reinforced events.

Event types are `captured`, `reinforced`, `dismissed`, and `promoted`. A session and turn may create at most one capture outcome.

## Promotion Request

```json
{
  "schema_version": 1,
  "candidate_id": "PL-...",
  "status": "Accepted | Reinforced | Superseded",
  "lesson": "Approved lesson, optionally edited by the user",
  "applies_when": "Approved applicability",
  "does_not_apply_when": "Approved exclusions",
  "evidence_strength": "reported | observed | verified | reinforced",
  "cross_project": "No | Evaluate",
  "approved_by": "user",
  "supersedes": null
}
```

Promotion requires explicit user approval. `approved_by` is provenance, not an identity claim.

## Active Ledger Entry

Each accepted entry contains:

- Stable lesson ID and status.
- Scope and applicability boundaries.
- Lesson and evidence list.
- Evidence strength and provenance.
- Last-reviewed date.
- Cross-project evaluation status.
- Optional superseded lesson ID.

Candidates and dismissed proposals never appear in the active ledger.

## Workflow and global-proposal extensions

Config field `capture_mode` is `explicit` (the default when absent) or `workflow`. Only explicit enrollment permits automatic `--workflow` capture. Requests retain schema version 1 and native-neutral session/turn identifiers; transcript paths are not required. Workflow capture requires `evidence_level` of `verified` or `reinforced`.

An optional `proposal` object records a bounded canonical skill improvement:

```json
{
  "target_skill": "plugins/rogemar-agent-toolkit/skills/example/SKILL.md",
  "allowed_files": ["plugins/rogemar-agent-toolkit/skills/example/SKILL.md"],
  "validation": "Run the existing skill checks and a behavior rehearsal"
}
```

Supply `source_project` as the source repository directory name and `source_lesson_id` as its accepted ID, plus CLI `--source-root`. The source path is used locally and is not persisted. The source must have an Accepted or Reinforced ledger entry with verified/reinforced evidence; the target must be an existing repository-relative SKILL.md and allowed files must stay inside its directory. The owner validates canonical ownership and applicability before capture. Neither proposal capture nor its approval performs an edit.

A duplicate settled candidate never returns to pending. A distinct verified evidence reference can produce a new pending revision, with store-owned `revisits_candidate_id` provenance; approval remains required. Evidence summaries alone do not count as new evidence. Deterministic deduplication compares normalized rules and boundaries; the workflow owner also checks semantic duplicates.

The store serializes mutations with a bounded OS lock and recovers duplicate capture retries from source session/turn events. A lock timeout is reported, not retried indefinitely. Windows locking uses the native standard-library mechanism; validate in that runtime before claiming native Windows support.
