# Release procedure

1. Refresh and review `catalog/skills.yaml` from approved sources.
2. Run `python3 scripts/inventory_readme.py --write` after intentional skill or
   dependency changes so the root attribution inventory stays complete.
3. Run `python3 scripts/inventory_readme.py --check`, then
   `python3 scripts/toolkit.py lock`, `python3 scripts/toolkit.py verify`, and
   the unit tests.
4. Run `python3 scripts/toolkit.py package`, inspect both archives, and verify
   them against the generated `dist/SHA256SUMS` file.

   ```bash
   (cd dist && shasum -a 256 -c SHA256SUMS)
   ```
5. Test a fresh project install and rollback from the candidate tag.
6. Perform Codex and Cursor discovery smoke tests in fresh sessions.
7. Create a semantic-version tag only after commit/push authorization.

Breaking skill names, removed workflows, changed required dependencies, or
installer state-schema changes require a major release. Additive skills use a
minor release; compatible corrections use a patch release.

Record user-visible changes and evidence limits in `CHANGELOG.md` before
creating the release tag.

Releases never track `main` implicitly. Roll back by checking out the prior tag
and reinstalling, or use the recorded immediate-backup rollback command.
