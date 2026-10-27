"""Exercise package input selection against real temporary Git and Git-less trees."""
import importlib.util
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("package_input_toolkit", ROOT / "scripts/toolkit.py")
toolkit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(toolkit)


class PackageInputsTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "docs").mkdir()
        (self.root / "docs/tracked.md").write_text("tracked\n")
        (self.root / "docs/private.md").write_text("private\n")
        (self.root / "docs/intentional.md").write_text("intentional\n")

    def init_git(self):
        if not shutil.which("git"):
            self.skipTest("Git is needed for tracked-input selection")
        subprocess.run(["git", "init", "--quiet", str(self.root)], check=True)
        subprocess.run(["git", "-C", str(self.root), "add", "docs/tracked.md"], check=True)

    def test_tracked_only_and_explicit_addition_reach_real_copy(self):
        self.init_git()
        selected = toolkit.package_source_paths(self.root, ["docs/intentional.md"], False)
        self.assertEqual(selected, {"docs/tracked.md", "docs/intentional.md"})
        output = self.root / "output"
        with patch.object(toolkit, "ROOT", self.root):
            toolkit.copy_package_tree(self.root / "docs", output, selected)
        self.assertEqual((output / "tracked.md").read_text(), "tracked\n")
        self.assertEqual((output / "intentional.md").read_text(), "intentional\n")
        self.assertFalse((output / "private.md").exists())

    def test_unversioned_requires_explicit_trust(self):
        with self.assertRaisesRegex(toolkit.ToolkitError, "--trust-unversioned-source"):
            toolkit.package_source_paths(self.root, [], False)
        self.assertEqual(toolkit.package_source_paths(self.root, [], True),
                         {"docs/tracked.md", "docs/private.md", "docs/intentional.md"})

    def test_untrusted_paths_and_symlinks_are_rejected(self):
        self.init_git()
        for value in ("../outside", "docs/.env.local", "docs", "other/file"):
            with self.subTest(value=value), self.assertRaises(toolkit.ToolkitError):
                toolkit.package_source_paths(self.root, [value], False)
        (self.root / "docs/link.md").symlink_to(self.root / "docs/private.md")
        with self.assertRaisesRegex(toolkit.ToolkitError, "symlink"):
            toolkit.package_source_paths(self.root, ["docs/link.md"], False)

    def test_trust_flag_cannot_bypass_git_selection(self):
        self.init_git()
        with self.assertRaisesRegex(toolkit.ToolkitError, "only for"):
            toolkit.package_source_paths(self.root, [], True)


if __name__ == "__main__":
    unittest.main()
