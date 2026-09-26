"""External provisioning uses pinned fixtures, never the network in unit tests."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("external_toolkit", Path(__file__).resolve().parents[1] / "scripts/toolkit.py")
toolkit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(toolkit)


class ExternalSkillsTests(unittest.TestCase):
    def test_missing_only_preserves_resources_license_and_user_edits(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source, target = root / "repo", root / "installed"
            source.mkdir()
            target.mkdir()
            skill = source / "skills/example"
            (skill / "references").mkdir(parents=True)
            (skill / "SKILL.md").write_text("---\nname: example\ndescription: example\n---\n")
            (skill / "references/check.md").write_text("proof")
            (source / "LICENSE").write_text("fixture license")
            for command in (["init", "-q"], ["add", "."],
                            ["-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "fixture"]):
                subprocess.run(["git", "-C", str(source), *command], check=True, capture_output=True)
            commit = subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"], text=True).strip()
            selection = {"dependencies": {"example": {"kind": "skills", "auto_install": {
                "repository": "https://github.com/example/skills.git", "commit": commit,
                "skills": {"example": "skills/example"}}}}}

            def fetch(recipe, destination):
                subprocess.run(["git", "clone", "-q", str(source), str(destination)], check=True)

            with patch.object(toolkit, "fetch_external_source", side_effect=fetch) as fetcher:
                toolkit.install_external_skills(selection, target)
                self.assertEqual((target / "example/references/check.md").read_text(), "proof")
                self.assertEqual((target / "example/upstream-notices/LICENSE").read_text(), "fixture license")
                self.assertEqual(json.loads((target / "example/.toolkit-upstream.json").read_text())["commit"], commit)
                (target / "example/SKILL.md").write_text("personal edit")
                toolkit.install_external_skills(selection, target)
                self.assertEqual(fetcher.call_count, 1)
                self.assertEqual((target / "example/SKILL.md").read_text(), "personal edit")
            (target / "example/SKILL.md").unlink()
            with self.assertRaisesRegex(toolkit.ToolkitError, "incomplete"):
                toolkit.external_skill_plan(selection, target)
            selection["dependencies"]["example"]["auto_install"]["skills"] = {"bad": "../escape"}
            with self.assertRaisesRegex(toolkit.ToolkitError, "invalid external source"):
                toolkit.external_skill_plan(selection, target)

    def test_current_managed_install_still_retries_externals_and_dry_run_is_offline(self):
        with tempfile.TemporaryDirectory() as root:
            args = ["install", "--project-root", root]
            with patch.object(toolkit, "install_external_skills", side_effect=toolkit.ToolkitError("network unavailable")):
                self.assertEqual(toolkit.main(args), 1)
            with patch.object(toolkit, "install_external_skills") as provision:
                self.assertEqual(toolkit.main(args), 0)
                provision.assert_called_once()
                provision.reset_mock()
                self.assertEqual(toolkit.main(args + ["--dry-run"]), 0)
                provision.assert_not_called()

    def test_shared_learning_and_droid_selection(self):
        catalog = toolkit.load_json(toolkit.CATALOG_PATH)
        if "distribution_selection" in catalog["package"]:
            self.skipTest("cross-harness selection requires the source catalog")
        for harness in catalog["harnesses"]:
            selected = toolkit.resolve_selection(harness, "core", ["engineering"])
            self.assertIn("project-learning", selected["skills"])
            self.assertIn("ponytail", selected["external"])
        selected = toolkit.resolve_selection("droid", "all", [])
        self.assertIn("universal-forge", selected["skills"])
        self.assertIn("agent-collaboration-terminal", selected["skills"])
        self.assertNotIn("codex-forge", selected["skills"])


if __name__ == "__main__":
    unittest.main()
