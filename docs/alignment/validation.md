# Alignment validation

The current machine-readable delivery record is [validation.json](validation.json).
It separates this implementation from the original nested candidate's historical
fixture results. Do not reuse historical passes as proof for a changed checkout.

Required source checks are `toolkit.py lock`, `toolkit.py verify`, README inventory,
Forge/routing verification, root unit tests, relevant owner suites and both core/full
release-package checks. `select_checks.py --base <commit> --run` selects owner suites
from changed paths; inspect semantic dependencies as well. This repository's source
maintenance gates remain required. Documentation-only PRs under `docs/` and
`CHANGELOG.md` need not start CI unless effective policy requires it; README changes
retain the generated-inventory check. Changes to the owner selector or validation
workflow exercise every affected owner runner. Bun and its locked dependencies are
provisioned only when native Forge checks are selected; missing local runtimes are
reported as blocked, never passed.

The tests exercise original installation/rollback contracts and new routing,
learning/proposal recovery, qualification, update, replay/budget and source lifecycle
behavior. Actual temporary file/SQLite operations are local fixture evidence, not
live native-harness certification. Expected negative cases are not product failures.

The first integrated run found a distribution hash mismatch caused by rewriting a
skill's routing index during packaging. Packaging now preserves canonical source
bytes and validates the selected catalog subset. Early diagnostic failures from
stale generated files and a test fixture were corrected before final validation.

For this task the owner waived unavailable external reviewers. No review pass is
claimed on their behalf. Normal Integrated Workflow reviewer requirements remain
unchanged. Read actual PR checks and automatic actionable feedback before merging.

Unestablished qualifications remain explicit: independently protected host producer,
policy/verifier and runtime permission controls; live Codex/Cursor/other-harness
trials; held-out model/reasoning comparisons; production effectiveness/cost benefit;
and comprehensive execution of every optional integration/resource. The full-body
and selective-resource review labels must not be inferred from a mechanical scan.

Mermaid sources are editable documentation. Rendering requires a compatible renderer;
source inspection alone is not a rendered visual check.
