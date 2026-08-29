# Changelog

All notable changes to the private toolkit are documented here. Versions follow
Semantic Versioning.

## 0.2.0 - 2026-08-30

### Added

- Expanded runtime inventory for Cursor built-ins, pstack, Cursor Team Kit,
  cached Cursor plugins, Antigravity/Gemini, Grok Build, Junie, Command Code,
  and codex-router.
- Explicit provenance, observed versions, install guidance, compatibility
  status, and non-vendoring boundaries for external runtimes and providers.
- Root README navigation, Mermaid lifecycle map, harness matrix, and agile
  web/mobile workflow-to-skill mapping.
- Grok supervisor package and public upstream records for the observed provider
  plugin families.

### Changed

- Corrected pstack status to reflect the audit-observed local `0.14.2` label and
  recorded the newer cached `0.14.5` separately.
- Expanded pstack's catalog from 24 names to the 44 local skill entries.
- Added runtime integration data to the lockfile and `doctor` output.

## 0.1.0 - 2026-08-30

### Added

- Canonical bundle of 52 vendored, validated Agent Skills.
- Portable Agent Plugin and Codex marketplace manifests.
- Project-local and user-level copied installation, plus development-only links.
- Managed upgrades with collision refusal, recoverable backups, and rollback.
- Deterministic skill hashes, portability and secret-signature checks, doctor,
  release archives, and SHA-256 checksums.
- macOS and Linux CI coverage on Python 3.9 and 3.11.
- Audited attribution, canonical repository links, and author-supported latest
  install commands for represented third-party and upstream skills.
- README-generated inventory for all 52 portable skills, external skill groups,
  runtime integrations, and runtime package dependencies, including GoalBuddy
  and Cursor `pstack` provenance and owner-managed install guidance.

### Evidence limits

- Package structure, macOS installation behavior, rollback, and validators are
  verified locally.
- Fresh Codex discovery, Cursor UI discovery, GitHub workspace import, and a
  Linux/WSL runtime smoke test remain unverified until performed.
- Runtime-owned plugins, connectors, credentials, and system skills are
  cataloged dependencies; they are not redistributed or authenticated here.
