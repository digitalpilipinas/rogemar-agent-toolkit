# Changelog

All notable changes to the private toolkit are documented here. Versions follow
Semantic Versioning.

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
- README-generated inventory for all 52 portable skills, five external skill
  groups, and 24 runtime package dependencies, including GoalBuddy and Cursor
  `pstack` provenance and install paths.

### Evidence limits

- Package structure, macOS installation behavior, rollback, and validators are
  verified locally.
- Fresh Codex discovery, Cursor UI discovery, GitHub workspace import, and a
  Linux/WSL runtime smoke test remain unverified until performed.
- Runtime-owned plugins, connectors, credentials, and system skills are
  cataloged dependencies; they are not redistributed or authenticated here.
