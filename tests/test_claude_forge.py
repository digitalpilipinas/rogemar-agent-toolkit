"""Claude Forge stays on the shared playbooks and off the other harness entries."""
import importlib.util
import json
import re
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "plugins/rogemar-agent-toolkit/skills"
if not (SKILLS / "claude-forge").is_dir():
    raise unittest.SkipTest("Claude Forge was not selected for this distribution")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ClaudeForgeTests(unittest.TestCase):
    def test_playbooks_match_the_shared_methods(self):
        sync = load("claude_forge_sync", SKILLS / "claude-forge/scripts/sync_playbooks.py")
        expected = sync.render_all()
        self.assertEqual(len(expected), 23)
        actual = {path.stem: path.read_text() for path in (SKILLS / "claude-forge/playbooks").glob("*.md")}
        self.assertEqual(actual, expected)
        for name, text in actual.items():
            self.assertNotIn("plan-model-router", text, name)
            self.assertNotIn("$forge-", text, name)

    def test_claude_forge_links_resolve(self):
        for skill in ("claude-forge", "claude-forge-setup"):
            for path in (SKILLS / skill).rglob("*.md"):
                for link in re.findall(r"\]\(([^)]+)\)", path.read_text()):
                    target = link.split("#", 1)[0]
                    if not target or "://" in target or target.startswith("mailto:"):
                        continue
                    self.assertTrue((path.parent / target).exists(), f"{path.relative_to(SKILLS)}: {link}")

    def test_claude_engineering_selection_uses_claude_entries_only(self):
        toolkit = load("claude_toolkit", ROOT / "scripts/toolkit.py")
        catalog = toolkit.load_json(toolkit.CATALOG_PATH)
        for harness in catalog["harnesses"]:
            selected = toolkit.resolve_selection(harness, "core", ["engineering"])["skills"]
            self.assertEqual("claude-forge" in selected, harness == "claude")
            self.assertEqual("claude-forge-setup" in selected, harness == "claude")
            self.assertEqual("cursor-forge" in selected, harness == "cursor")
            self.assertEqual("codex-forge" in selected, harness == "codex")

    def test_role_inventory_matches_the_cursor_model_free_contract(self):
        cursor = json.loads((SKILLS / "cursor-forge-setup/references/roles.json").read_text())
        claude = json.loads((SKILLS / "claude-forge-setup/references/roles.json").read_text())
        self.assertEqual(claude, cursor)
        self.assertGreaterEqual(len(claude["roles"]), 45)


if __name__ == "__main__":
    unittest.main()
