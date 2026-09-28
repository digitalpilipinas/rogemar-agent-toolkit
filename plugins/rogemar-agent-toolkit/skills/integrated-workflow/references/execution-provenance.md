# Optional execution provenance extension

The existing checkpoint remains a structural/candidate/artifact validator. This
extension compares a receipt with independently supplied protected observations.
It does not create a trusted runner, authenticate an owner, install an OS sandbox,
prove that a test is meaningful, or turn source inspection into device evidence.

## Deployment boundary

Only enable this tier when a trusted host/CI integration actually supplies the
observations independently of the implementation agent. Keep the reviewed
checkpoint and its `execution_provenance.py` helper outside the candidate checkout,
in an owner/host-protected location. The trusted policy binds the helper SHA-256.
The helper's exact bytes are verified before being executed. Never import it from
the candidate or update its pin simply to pass a product change.

An authorized protected runner may supply candidate-bound observations through an
existing trusted channel. This avoids asking the owner to manually approve routine
test runs. A model-written JSON object marked trusted, or an agent-controlled digest
in the same checkout, is not that channel. This package supplies the comparator and
checkpoint hook, not host-specific attestation provisioning.

## Trusted policy extension

Retain the current repository, mapping, boundary and required_gates fields. Add:

- `provenance_validator_sha256`: digest of the separately reviewed helper.
- `execution_evidence`: an object keyed by each gate requiring this tier.
- Each value has `observation_path` (protected absolute path outside the candidate),
  `observation_sha256`, `runner`, `check_id`, and `environment_sha256`.

Those gate IDs become required at this policy's boundary. Default policies without
the extension keep their existing behavior. Structure-only checks remain
structure-only; they do not inspect or certify runtime execution.

The observation object has exactly: schema_version 1, gate, candidate, runner,
check_id, environment_sha256, run_id, exit_code, tests_executed,
required_checks_complete, and artifact_hashes. Candidate equals the full current
checkpoint identity. `tests_executed` is a positive count of the required checks
actually performed, not a hard-coded success value. A required skipped assertion
makes required_checks_complete false. The exact expected count and semantic
coverage remain responsibilities of the qualified check and host policy.

A zero exit, nonempty run ID, exact identities and matching artifact digest set
are necessary here, not sufficient to prove the product is correct. The original
checkpoint still verifies artifact existence, integrity, platform and coverage.
Protected observation reads reject symlinks, special/hard-linked/oversized files
and changes observed during the bounded read. Platforms lacking the necessary
safe read flags report an unavailable prerequisite; they are not falsely qualified.

## Boundary results and rollout

Changed inputs invalidate the affected observations. Missing, stale, failed or
forged observations reject only their required acceptance boundary; independent
permitted work may continue. Do not quietly downgrade the policy on failure.
First run structural and comparator fixtures, then a real host trial with denied
and authorized cases. Protect secrets in paths, environment details and artifacts.

Before rollback, preserve the previous reviewed validator/helper/policy set. Revert
it only with the same owner's policy authority. Never delete failed evidence just
to make a candidate appear clean. No deployment, CI protection or host attestation
is activated by copying these files.
