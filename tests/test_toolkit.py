from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "toolkit", REPOSITORY_ROOT / "scripts" / "toolkit.py"
)
assert SPEC and SPEC.loader
toolkit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(toolkit)


class ToolkitTests(unittest.TestCase):
    def run_cli(self, *arguments: str) -> tuple[int, str, str]:
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            result = toolkit.main(list(arguments))
        return result, stdout.getvalue(), stderr.getvalue()

    def test_verify_clean_bundle(self) -> None:
        result, output, errors = self.run_cli("verify")
        self.assertEqual(result, 0, errors)
        self.assertIn("52 vendored skills", output)

    def test_readme_inventory_is_current(self) -> None:
        result = subprocess.run(
            [sys.executable, str(REPOSITORY_ROOT / "scripts" / "inventory_readme.py"), "--check"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("inventory is current", result.stdout)

    def test_project_install_records_managed_state(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            result, output, errors = self.run_cli(
                "install", "--target", "project", "--project-root", str(project)
            )
            self.assertEqual(result, 0, errors)
            self.assertIn("Installed 52 managed skills", output)
            state_path = project / ".agents" / "rogemar-agent-toolkit.lock.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(len(state["skills"]), 52)
            self.assertTrue(
                (project / ".agents" / "skills" / "create-plan" / "SKILL.md").is_file()
            )

    def test_unmanaged_collision_is_not_overwritten(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            collision = project / ".agents" / "skills" / "create-plan"
            collision.mkdir(parents=True)
            marker = collision / "SKILL.md"
            marker.write_text("unmanaged\n", encoding="utf-8")
            result, _output, errors = self.run_cli(
                "install", "--target", "project", "--project-root", str(project)
            )
            self.assertEqual(result, 1)
            self.assertIn("refusing to overwrite unmanaged", errors)
            self.assertEqual(marker.read_text(encoding="utf-8"), "unmanaged\n")

    def test_update_backup_and_rollback_are_recoverable(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            install_args = (
                "install", "--target", "project", "--project-root", str(project)
            )
            self.assertEqual(self.run_cli(*install_args)[0], 0)
            installed = (
                project / ".agents" / "skills" / "accessibility-auditor" / "SKILL.md"
            )
            original = installed.read_text(encoding="utf-8")
            local_change = original + "\nlocal recovery marker\n"
            installed.write_text(local_change, encoding="utf-8")

            upgrade_args = (
                "upgrade", "--target", "project", "--project-root", str(project)
            )
            result, _output, errors = self.run_cli(*upgrade_args)
            self.assertEqual(result, 0, errors)
            self.assertEqual(installed.read_text(encoding="utf-8"), original)

            result, output, errors = self.run_cli(
                "rollback", "--target", "project", "--project-root", str(project)
            )
            self.assertEqual(result, 0, errors)
            self.assertIn("Restored the prior managed state", output)
            self.assertEqual(installed.read_text(encoding="utf-8"), local_change)

    def test_upgrade_requires_managed_installation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            result, _output, errors = self.run_cli(
                "upgrade", "--target", "project", "--project-root", temporary
            )
            self.assertEqual(result, 1)
            self.assertIn("use install first", errors)

    def test_package_builds_both_archives(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            result, output, errors = self.run_cli("package", "--output", temporary)
            self.assertEqual(result, 0, errors)
            archives = sorted(Path(temporary).glob("*.zip"))
            self.assertEqual(len(archives), 2)
            checksums = (Path(temporary) / "SHA256SUMS").read_text(encoding="utf-8")
            self.assertIn(archives[0].name, checksums)
            self.assertIn(archives[1].name, checksums)
            self.assertIn("agent-plugin", output)
            self.assertIn("codex-marketplace", output)
            portable = next(path for path in archives if "agent-plugin" in path.name)
            with zipfile.ZipFile(portable) as archive:
                names = archive.namelist()
            self.assertIn("rogemar-agent-toolkit/plugin.json", names)
            self.assertIn(
                "rogemar-agent-toolkit/skills/create-plan/SKILL.md", names
            )


if __name__ == "__main__":
    unittest.main()
