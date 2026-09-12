# Selecting overlapping provider skills

Use only when more than one installed route provides the requested capability.
The current orchestrator coordinates; a provider keeps its own review or task
procedure. A source review of a skill does not authorize running its service.

## CodeRabbit

When selected by the user or the active acceptance contract, use the namespaced
CodeRabbit plugin's own skill when available. Perform its full review over the
agreed candidate, including all in-scope changes; do not substitute a quick pass,
sampled files or only selected findings. Follow the provider's supported commands,
completion and findings handling. Keep its verdict and full result available even
when the shared review record consolidates duplicates. A standalone CodeRabbit
request need not start a second generic review.

If the plugin skill is unavailable, use the installed standalone CodeRabbit skill
with the same full-review scope. Do not run both installations. Installation,
authentication, code transmission and paid use retain the applicable user
permission; selecting a skill cannot silently grant missing authority. Reuse
existing authorization without asking twice.

## Delivery review cadence

When the optional `integrated-workflow` skill is installed and owns delivery,
read its `references/coderabbit-review.md` for full initial cloud requests, the
both-reviewers completion barrier, persistent per-provider allowance and owner
extensions. Carry its receipt through PR-helper and worker handoffs. Apply the
barrier only to active ready-PR cloud waves; local/pre-ready reconciliation keeps
its existing cadence. Core-only or standalone reviews do not require installing
Integrated Workflow or activating cloud providers.

## Multiple versions or distributions

Use one established primary for overlapping names, with qualified paths when
needed. Preserve distinct tools, resources and unique skills. Compare full trees
and consumers before disabling duplicate discovery; keep backups and leave
managed caches intact. Retaining a unique method from another distribution does
not authorize duplicate review or parallel execution.

## Convex distributions

When both distributions are present, keep the maintained Convex plugin's shared
expert/authentication contract with its dependent authz methods and native
monitor tools. The curated app binding remains a distinct capability. Same-name
add, update-check, reviewer and domains skills need only one discovery owner.

For a generic new-app request, prefer the installed portable `convex-quickstart`
when available; keep the existing project/deployment identity and execute only
authorized bootstrap steps. Explicit requests for a named plugin quickstart
retain that route. Their differing bootstrap instructions require current-source
inspection: never bypass host security checks, silently rebind an existing
production/persistent deployment to anonymous mode, or enable a monitor/trust
setting without the applicable authority. Do not treat plugin version numbers
from separate distributions as a shared upgrade sequence.
