# Project Learning Schemas

## Candidate Capture Request

```json
{
  "schema_version": 1,
  "session_id": "session identifier from the Stop hook",
  "turn_id": "turn identifier from the Stop hook",
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
