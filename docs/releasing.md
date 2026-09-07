# Release procedure

1. Review source/target/dependency and license changes in `catalog/skills.yaml`.
2. Generate the inventory with `python3 scripts/inventory_readme.py --write`.
3. Run `python3 scripts/toolkit.py lock`, `verify`, `python3 scripts/verify_forge.py`, and `python3 -m unittest discover -s tests -v`.
4. Build both default and full selections with `python3 scripts/toolkit.py package --output dist/core` and `python3 scripts/toolkit.py package --profile all --output dist/all`.
5. Check `SHA256SUMS`, every selected skill digest, and the extracted Codex archive's `toolkit.py verify` and `verify_forge.py`. Exercise a clean install, repeat install, upgrade, drift refusal, pack removal and rollback.
6. Report fresh target-harness discovery, Linux/WSL execution, OpenDesign runtime/rendering and device evidence separately. A local simulated layout is not a cloud smoke test.
7. Publish a reviewed commit/release only within the operator's publication authority. Use a pinned tag or commit for cloud setup; never silently track main as a reproducibility guarantee.

Default archives expose the six-skill core. The portable archive contains compatible selected skill trees plus the selection/hash receipt. The Codex marketplace archive contains a selected, self-validating source distribution, including the installer and full Forge provenance manifest. Its optional packs are limited to the contents of that archive; use the full source checkout to add other packs.

Version 1.0 changes installation state and defaults. Legacy state migration requires an explicit harness. Subsequent breaking names, required dependencies or state schemas require a major version. Additive optional packs use a minor version; compatible corrections use a patch version.

Resource updates retain the entire previous managed library when replacement is explicitly requested. Restore that backup directory to roll back resources. Skill updates have a separate managed rollback command. Never use either rollback to replace unrelated data.
