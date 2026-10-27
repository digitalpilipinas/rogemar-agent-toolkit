# Release procedure

1. Review source/target/dependency and license changes in `catalog/skills.yaml`.
2. Generate the inventory with `python3 scripts/inventory_readme.py --write`.
3. Run `python3 scripts/toolkit.py lock`, `python3 scripts/toolkit.py verify`, `python3 scripts/verify_forge.py`, and `python3 -m unittest discover -s tests -v`.
4. Build both default and full selections with `python3 scripts/toolkit.py package --output dist/core` and `python3 scripts/toolkit.py package --profile all --output dist/all`.
5. Check `SHA256SUMS`, every selected skill digest, and the extracted Codex archive's `toolkit.py verify` and `verify_forge.py`, then run `python3 -m unittest discover -s tests -v` in each extracted Codex archive. Unselected optional skills should be skipped; absent Forge should report `not-applicable`, never `verified`. Exercise a clean install, repeat install, upgrade, drift refusal, pack removal and rollback.
6. Report fresh target-harness discovery, Linux/WSL execution, OpenDesign runtime/rendering and device evidence separately. A local simulated layout is not a cloud smoke test.
7. Publish a reviewed commit/release only within the operator's publication authority. Use a pinned tag or commit for cloud setup; never silently track main as a reproducibility guarantee.

Packaging reads Git-tracked files from the working tree, including their current
uncommitted contents; review the tracked diff and candidate before distribution.
Untracked or ignored files are excluded unless explicitly named, one file per
`--include-source path` argument. Intended new skill files must be named or added
to the Git index so their locked skill digest matches. Symlinks, excluded cache
paths, secret-like files and out-of-scope paths are rejected. A source tree without
Git metadata fails closed; only after inspecting and trusting its complete eligible
contents may the operator pass `--trust-unversioned-source`. This flag deliberately
includes eligible files from that Git-less tree; it is not a privacy filter. The
same explicit flag is needed when repackaging an extracted release archive.

Default archives expose the six-skill core. The portable archive contains compatible selected skill trees plus the selection/hash receipt. The Codex marketplace archive contains a selected, self-validating source distribution, including the installer and full Forge provenance manifest. Its optional packs are limited to the contents of that archive; use the full source checkout to add other packs.

Version 1.0 changes installation state and defaults. Legacy state migration requires an explicit harness. Subsequent breaking names, required dependencies or state schemas require a major version. Additive optional packs use a minor version; compatible corrections use a patch version.

Resource updates retain the entire previous managed library when replacement is explicitly requested. Restore that backup directory to roll back resources. Skill updates have a separate managed rollback command. Never use either rollback to replace unrelated data.
