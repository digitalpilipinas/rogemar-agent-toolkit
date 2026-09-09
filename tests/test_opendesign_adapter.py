from __future__ import annotations

import argparse
from contextlib import redirect_stderr, redirect_stdout
import importlib.util
from io import StringIO
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


catalog = json.loads((Path(__file__).resolve().parents[1] / 'catalog/skills.yaml').read_text())
if 'distribution_selection' in catalog['package'] and not set(['opendesign']).issubset({e['name'] for e in catalog['vendored']}):
    raise unittest.SkipTest('optional skills were not selected for this distribution')

SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "plugins/rogemar-agent-toolkit/skills/opendesign/scripts/opendesign_adapter.py"
)
SPEC = importlib.util.spec_from_file_location("opendesign_adapter", SCRIPT)
assert SPEC and SPEC.loader
adapter = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(adapter)


def arguments(**overrides):
    return argparse.Namespace(**{"bin": None, "node": None, "root": None, **overrides})


class OpenDesignAdapterTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.addCleanup(self.temporary.cleanup)

    def file(self, name, text="", executable=False):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        if executable:
            path.chmod(0o755)
        return path

    def source(self, built=True):
        self.file("package.json", json.dumps({"name": "open-design", "version": "0.21.1"}))
        self.file("apps/daemon/bin/od.mjs", "// source wrapper fixture")
        if built:
            self.file("apps/daemon/dist/cli.js", "// built fixture")
        return self.root

    def test_absent_configuration_does_not_select_path_od(self):
        with patch.object(adapter.shutil, "which", side_effect=AssertionError("PATH probe")):
            code, report = adapter.doctor(arguments(), {"PATH": "/usr/bin:/bin"})
        self.assertEqual(code, 2)
        self.assertEqual(report["status"], "unavailable")
        self.assertFalse(report["runtime_verified"])

    def test_rejects_posix_od_and_symlink(self):
        candidate = next((p for p in (Path("/usr/bin/od"), Path("/bin/od")) if p.is_file()), None)
        if not candidate:
            self.skipTest("POSIX od is not present on this platform")
        alias = self.root / "open-design"
        alias.symlink_to(candidate)
        for selected in (candidate, alias):
            with self.subTest(selected=selected):
                code, report = adapter.doctor(arguments(bin=str(selected)), {})
                self.assertEqual(code, 2)
                self.assertIn("octal-dump", report["error"])

    def test_invalid_explicit_configuration_does_not_fallback(self):
        good = self.file("good-launcher", "#!/bin/sh\nexit 0\n", executable=True)
        code, report = adapter.doctor(
            arguments(bin=str(self.root / "missing")), {"OD_BIN": str(good)}
        )
        self.assertEqual(code, 2)
        self.assertNotIn("command", report)

    def test_rejects_directory_and_nonexecutable_launcher(self):
        plain = self.file("launcher", "not executable")
        for selected in (self.root, plain):
            with self.subTest(selected=selected):
                code, _ = adapter.doctor(arguments(bin=str(selected)), {})
                self.assertEqual(code, 2)

    def test_explicit_and_environment_precedence(self):
        launchers = [self.file(name, "#!/bin/sh\n", executable=True) for name in ("first", "second", "third")]
        env = {"OD_BIN": str(launchers[1]), "OPEN_DESIGN_BIN": str(launchers[2])}
        command, _, _ = adapter.resolve_command(arguments(bin=str(launchers[0])), env)
        self.assertEqual(command, [str(launchers[0].resolve())])
        command, _, _ = adapter.resolve_command(arguments(), env)
        self.assertEqual(command, [str(launchers[1].resolve())])
        command, _, _ = adapter.resolve_command(arguments(), {"OPEN_DESIGN_BIN": str(launchers[2])})
        self.assertEqual(command, [str(launchers[2].resolve())])

    def test_explicit_host_cli_ignores_stale_root_hint(self):
        launcher = self.file("launcher", "#!/bin/sh\n", executable=True)
        code, report = adapter.doctor(arguments(root="/nonexistent/source"), {"OD_BIN": str(launcher)})
        self.assertEqual(code, 0)
        self.assertEqual(report["status"], "configured")

    def test_source_requires_valid_package_and_build(self):
        for package in ("broken", "[]", '{"name":"some-other-app"}'):
            self.file("package.json", package)
            code, _ = adapter.doctor(arguments(root=str(self.root)), {})
            self.assertEqual(code, 2)
        self.source(built=False)
        code, report = adapter.doctor(arguments(root=str(self.root)), {})
        self.assertEqual(code, 2)
        self.assertIn("dist/cli.js", report["error"])

    def test_broken_root_symlink_reports_configuration_error(self):
        alias = self.root / "loop"
        alias.symlink_to(alias)
        code, report = adapter.doctor(arguments(root=str(alias)), {})
        self.assertEqual(code, 2)
        self.assertIn("package.json", report["error"])

    def test_source_build_and_dependency_presence_are_separate(self):
        root = self.source()
        (root / "skills").mkdir()
        (root / "apps/daemon/node_modules/better-sqlite3").mkdir(parents=True)
        code, report = adapter.doctor(arguments(root=str(root), node=sys.executable), {})
        self.assertEqual(code, 0)
        self.assertEqual(report["source_package_version"], "0.21.1")
        self.assertTrue(report["resources_present"]["skills"])
        self.assertFalse(report["resources_present"]["design-templates"])
        self.assertTrue(report["native_package_directories_present"]["better-sqlite3"])
        self.assertFalse(report["native_package_directories_present"]["node-pty"])
        self.assertFalse(report["runtime_verified"])

    def test_wrapper_symlink_still_checks_missing_build(self):
        self.source(built=False)
        alias = self.root / "launcher"
        alias.symlink_to(self.root / "apps/daemon/bin/od.mjs")
        code, report = adapter.doctor(arguments(bin=str(alias)), {})
        self.assertEqual(code, 2)
        self.assertIn("dist/cli.js", report["error"])

    def test_javascript_requires_node_and_respects_host_runtime(self):
        cli = self.file("cli.js", "// fixture")
        code, report = adapter.doctor(arguments(bin=str(cli)), {"PATH": ""})
        self.assertEqual(code, 2)
        self.assertIn("Node-compatible", report["error"])
        command, _, kind = adapter.resolve_command(
            arguments(), {"OD_BIN": str(cli), "OD_NODE_BIN": sys.executable, "PATH": ""}
        )
        self.assertEqual(command, [str(Path(sys.executable).resolve()), str(cli.resolve())])
        self.assertEqual(kind, "node-script")

    def test_packaged_script_needs_absolute_data_dir_without_creating_it(self):
        cli = self.file("prebundled/daemon/daemon-cli.mjs", "// fixture")
        env = {"OD_BIN": str(cli), "OD_NODE_BIN": sys.executable}
        for data in (None, "relative-data"):
            with self.subTest(data=data):
                current = {**env, **({"OD_DATA_DIR": data} if data else {})}
                code, _ = adapter.doctor(arguments(), current)
                self.assertEqual(code, 2)
        data_dir = self.root / "must-not-be-created"
        code, report = adapter.doctor(arguments(), {**env, "OD_DATA_DIR": str(data_dir)})
        self.assertEqual(code, 0)
        self.assertFalse(data_dir.exists())
        self.assertNotIn(str(data_dir), json.dumps(report))

    def test_electron_requires_generated_node_mode(self):
        cli = self.file("cli.js", "// fixture")
        runtime = self.file("Open Design", "#!/bin/sh\n", executable=True)
        env = {"OD_BIN": str(cli), "OD_NODE_BIN": str(runtime)}
        code, _ = adapter.doctor(arguments(), env)
        self.assertEqual(code, 2)
        code, _ = adapter.doctor(arguments(), {**env, "ELECTRON_RUN_AS_NODE": "1"})
        self.assertEqual(code, 0)

    def test_doctor_never_runs_launcher_or_writes_or_exposes_env_values(self):
        marker = self.root / "unexpected"
        launcher = self.file("launcher", f"#!/bin/sh\ntouch '{marker}'\n", executable=True)
        original_files = sorted(str(p.relative_to(self.root)) for p in self.root.rglob("*"))
        env = {"OPEN_DESIGN_BIN": str(launcher), "OD_DAEMON_URL": "http://private.invalid/secret", "OD_PROJECT_ID": "private-project", "UNRELATED_TOKEN": "do-not-output"}
        output = StringIO()
        with patch.dict(os.environ, env, clear=True), patch.object(adapter.subprocess, "run", side_effect=AssertionError("executed")), redirect_stdout(output):
            code = adapter.main(["doctor"])
        self.assertEqual(code, 0)
        self.assertEqual(original_files, sorted(str(p.relative_to(self.root)) for p in self.root.rglob("*")))
        for secret in ("private.invalid", "private-project", "do-not-output"):
            self.assertNotIn(secret, output.getvalue())
        self.assertFalse(marker.exists())

    def test_all_seven_lanes_preserve_native_arguments_environment_and_exit(self):
        if os.name == "nt":
            self.skipTest("POSIX generated-launcher integration fixture")
        launcher = self.file(
            "generated launcher",
            f"#!{sys.executable}\nimport json, os, sys\nprint(json.dumps({{'argv':sys.argv[1:], 'context':os.environ.get('ADAPTER_TEST_CONTEXT')}}))\nsys.exit(7)\n",
            executable=True,
        )
        lanes = {
            "import": ["project", "import", "folder with spaces"],
            "create": ["run", "start", "--prompt-file", "brief with spaces.md"],
            "export": ["export", "page.html", "--format", "html"],
            "share": ["share", "url", "--url", "https://example.invalid/a?x=1&y=2"],
            "deploy": ["deploy", "fixture-project", "--provider", "cloudflare-pages"],
            "refine": ["files", "diff", "--project", "fixture-project"],
            "extend": ["plugin", "validate", "fixture-plugin"],
        }
        for lane, native_args in lanes.items():
            with self.subTest(lane=lane):
                literal = "$(touch should-never-exist); `uname`; $VARIABLE"
                result = subprocess.run(
                    [sys.executable, str(SCRIPT), "--bin", str(launcher), "run", "--", *native_args, literal],
                    cwd=self.root, env={**os.environ, "ADAPTER_TEST_CONTEXT": "retained"},
                    check=False, capture_output=True, text=True,
                )
                self.assertEqual(result.returncode, 7, result.stderr)
                payload = json.loads(result.stdout)
                self.assertEqual(payload["argv"], [*native_args, literal])
                self.assertEqual(payload["context"], "retained")
        self.assertFalse((self.root / "should-never-exist").exists())

    def test_explicit_run_requires_command(self):
        with self.assertRaises(SystemExit) as raised, redirect_stderr(StringIO()):
            adapter.main(["run", "--"])
        self.assertEqual(raised.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
