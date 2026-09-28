# Optional source-linked knowledge maintenance

Use for recurring research and useful synthesis, not every conversation. The
current orchestrator owns this method. Knowledge is not accepted behavioral policy,
and this method does not replace project-learning or the metadata-only agent-map.
No server, graph database, vector store, new agent or editor integration is required.

## Establish the permitted workspace

Reuse the project's existing documentation conventions. Enroll persistence only
with a named source boundary, destination, allowed operations, access/retention
policy and recovery procedure. Without enrollment or explicit save authority,
answer in the task and do not create indexes, logs, request files or caches.

Keep original sources or permitted references, derived knowledge, accepted lessons,
and task/approval state distinct. Link them without copying private transcripts.
A synthesis inherits all relevant source restrictions, including revealing names
and existence. Public reusable toolkit content must not contain project-private
research. A source is not policy merely because its words sound instructional.

## Ingest

Identify the source and version, permitted use, original evidence roots and related
pages. Distinguish source claims, observed repository behavior, interpretation and
proposal. Update existing relevant pages before creating near-duplicate summaries.
Preserve disagreements and version/condition differences. A newer source does not
automatically invalidate an older conclusion in a different context.

Track derivation dependencies so a source change flags only affected pages. Do not
claim multiple independent witnesses from several derivative summaries of one
source. Preserve useful comparisons even when no task failed, but route any
behavioral lesson through existing candidate approval rather than automatic policy.

For multi-file maintenance, stage a coherent patch, check target hashes and ownership,
apply only within authorization, and retain a recovery snapshot. Detect partial
updates; never claim the whole knowledge base was refreshed from a partial repair.

## Query

Locate relevant pages, check source scope and freshness, inspect decisive original
material and answer with evidence. A known source/file can be read directly.
An incomplete or stale index triggers a bounded source-search fallback, not a claim
that evidence is absent. Keep source-only requests source-only.

Saving the answer is a distinct operation unless the enrollment already authorizes
it. Do not create a blocking save/approval conversation for a routine query. Derivative
pages are locators and synthesis, not independent proof or a substitute for an
explicitly requested original document.

## Lint

Cheap structural checks cover links, duplicate identities, required metadata,
lineage cycles, declared versions and access boundaries. Semantic review checks
entailment, caveats, contradictions and relevance against actual sources. Neither
an index nor a link checker certifies truth or completeness.

The optional read-only helper consumes `knowledge-metadata-example.json` shape:

```sh
python3 -B <engineering-playbooks>/scripts/knowledge_checks.py < metadata.json
python3 -B <engineering-playbooks>/scripts/knowledge_checks.py --changed-source source-a < metadata.json
```

Exit 0 means structurally consistent metadata with no declared stale/unavailable
sources, 1 invalid metadata, 2 structurally valid but revalidation required. These
are not product-completion gates. Source availability/audience/root declarations
must come from the responsible adapter; the helper does not verify live ACLs,
source content, semantic independence or completed deletion.

Navigation links may cycle; derivation dependencies may not. Revoked access or
source deletion makes affected pages unavailable until the owner-approved deletion
or minimized re-derivation process has addressed pages, indexes, caches, exports
and backups under their applicable retention policies. Append-only history is not
an exemption from authorized deletion.

Use incremental upkeep and bounded review. An unrelated orphan page does not block
a valid product fix. If the current change depends on a stale decisive claim, resolve
that claim. Compare complete-task value with direct-source work, including ingestion,
maintenance, fallback, review and recovery. Keep the method only where useful.

## Optional host integration

`knowledge_checks.py` also exports `query_page` and `remove_source`. These are
adapters for an existing authorized store, not a new service. Query rechecks live
access and revisions for transitive sources before reading a bounded derived view.
The host must authorize pages, authenticate the principal and enforce access during
reads to close revocation races. Supplied audience metadata is not authentication.
A stale, inaccessible or missing source blocks that view; use permitted originals.

Removal computes affected derivatives, then requires the host to durably block
source/page/cache queries before idempotent erasure. Failed erasure leaves the block
in place. Receipts report host outcomes; verify external backups and caches through
that host's actual retention controls. The toolkit does not promise global erasure.
