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
    def test_failed_upstream_does_not_block_later_install_and_retry_preserves_success(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "repo"
            (source / "skills/example").mkdir(parents=True)
            (source / "skills/example/SKILL.md").write_text("fixture")
            for command in (["init", "-q"], ["add", "."],
                            ["-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "fixture"]):
                subprocess.run(["git", "-C", str(source), *command], check=True, capture_output=True)
            commit = subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"], text=True).strip()
            selection = {"dependencies": {
                name: {"kind": "skills", "auto_install": {
                    "repository": "https://github.com/example/skills.git", "commit": commit,
                    "skills": {name: "skills/example"}}}
                for name in ("broken", "healthy")}}
            for failure in ("fetch", "archive", "timeout"):
                with self.subTest(failure=failure):
                    target = root / failure
                    target.mkdir()
                    calls = []

                    def fetch(recipe, destination):
                        calls.append(recipe["dependency"])
                        if recipe["dependency"] == "broken":
                            if failure == "fetch":
                                raise toolkit.ToolkitError("upstream unavailable")
                            if failure == "timeout":
                                raise subprocess.TimeoutExpired(["git", "fetch"], 180)
                            destination.mkdir()  # No Git archive can be produced.
                            return
                        subprocess.run(["git", "clone", "-q", str(source), str(destination)], check=True)

                    with patch.object(toolkit, "fetch_external_source", side_effect=fetch):
                        with self.assertRaisesRegex(toolkit.ToolkitError, "broken"):
                            toolkit.install_external_skills(selection, target)
                        self.assertEqual(calls, ["broken", "healthy"])
                        self.assertEqual((target / "healthy/SKILL.md").read_text(), "fixture")
                        self.assertFalse((target / "broken").exists())
                        (target / "healthy/SKILL.md").write_text("preserved local edit")
                        calls.clear()
                        with self.assertRaisesRegex(toolkit.ToolkitError, "broken"):
                            toolkit.install_external_skills(selection, target)
                        self.assertEqual(calls, ["broken"])
                        self.assertEqual((target / "healthy/SKILL.md").read_text(), "preserved local edit")

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
                with self.assertRaisesRegex(toolkit.ToolkitError, "locally modified"):
                    toolkit.install_external_skills(selection, target)
                self.assertEqual(fetcher.call_count, 1)
                self.assertEqual((target / "example/SKILL.md").read_text(), "personal edit")
            (target / "example/SKILL.md").unlink()
            self.assertIn("incomplete", str(toolkit.external_skill_plan(selection, target)[0]["conflicts"]))
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

    def test_upgrade_rollback_preserves_modified_and_independent_copies(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source"
            source.mkdir()
            (source / "SKILL.md").write_text("version one")
            def git(*args):
                return subprocess.check_output(["git", "-C", str(source), *args], text=True).strip()
            git("init", "-q")
            git("add", ".")
            git("-c", "user.name=Fixture", "-c", "user.email=f@example.invalid", "commit", "-qm", "one")
            first = git("rev-parse", "HEAD")
            (source / "SKILL.md").write_text("version two")
            git("add", ".")
            git("-c", "user.name=Fixture", "-c", "user.email=f@example.invalid", "commit", "-qm", "two")
            second = git("rev-parse", "HEAD")
            selection = {"dependencies": {"fixture": {"kind": "skills", "auto_install": {
                "repository": "https://github.com/example/fixture.git", "commit": first,
                "skills": {"fixture": "."}}}}}
            target = root / "project/.agents/skills"
            target.mkdir(parents=True)
            def fetch(recipe, destination):
                subprocess.run(["git", "clone", "-q", str(source), str(destination)], check=True)
            with patch.object(toolkit, "fetch_external_source", side_effect=fetch):
                toolkit.install_external_skills(selection, target)
                selection["dependencies"]["fixture"]["auto_install"]["commit"] = second
                toolkit.install_external_skills(selection, target)
                self.assertEqual((target / "fixture/SKILL.md").read_text(), "version two")
                self.assertEqual(toolkit.main(["rollback", "--project-root", str(root / "project"), "--harness", "agent-skills"]), 0)
                self.assertEqual((target / "fixture/SKILL.md").read_text(), "version one")
                (target / "fixture/SKILL.md").write_text("local edit")
                with self.assertRaisesRegex(toolkit.ToolkitError, "locally modified"):
                    toolkit.install_external_skills(selection, target)
                self.assertEqual((target / "fixture/SKILL.md").read_text(), "local edit")
                (target / "fixture/.toolkit-upstream.json").unlink()
                with self.assertRaisesRegex(toolkit.ToolkitError, "independently installed"):
                    toolkit.install_external_skills(selection, target)

    def test_legacy_provenance_is_reconstructed_and_concurrent_destination_is_preserved(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source"
            source.mkdir()
            (source / "SKILL.md").write_text("old source")
            for args in (["init", "-q"], ["add", "."], ["-c", "user.name=Fixture", "-c", "user.email=f@example.invalid", "commit", "-qm", "one"]):
                subprocess.run(["git", "-C", str(source), *args], check=True, capture_output=True)
            commit = subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"], text=True).strip()
            recipe = {"repository": "https://github.com/example/fixture.git", "commit": commit,
                      "skills": {"fixture": "."}, "missing": {"fixture": "."}, "dependency": "fixture"}
            selection = {"dependencies": {"fixture": {"kind": "skills", "auto_install": recipe}}}
            target = root / "project/.agents/skills"
            target.mkdir(parents=True)
            def fetch(recipe, destination):
                subprocess.run(["git", "clone", "-q", str(source), str(destination)], check=True)
            with patch.object(toolkit, "fetch_external_source", side_effect=fetch):
                toolkit.stage_external_recipe(recipe, target, legacy=True)
                (target / "fixture/SKILL.md").write_text("edited legacy")
                with self.assertRaisesRegex(toolkit.ToolkitError, "legacy copy differs"):
                    toolkit.install_external_skills(selection, target)
                (target / "fixture/SKILL.md").write_text("old source")
                toolkit.install_external_skills(selection, target)
                self.assertEqual(json.loads((target / "fixture/.toolkit-upstream.json").read_text())["schema_version"], 2)
            other = root / "other"
            other.mkdir()
            plan = toolkit.external_skill_plan(selection, other)[0]
            (other / "fixture").mkdir()
            (other / "fixture/SKILL.md").write_text("concurrent")
            with self.assertRaisesRegex(toolkit.ToolkitError, "changed since planning"):
                toolkit.install_external_recipe(plan, other)
            self.assertEqual((other / "fixture/SKILL.md").read_text(), "concurrent")

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
