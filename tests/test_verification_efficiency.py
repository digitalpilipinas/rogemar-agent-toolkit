"""Contract checks for the shared verification-efficiency method."""
from pathlib import Path
import json
import re
import os
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "plugins/rogemar-agent-toolkit/skills"
REF = SKILLS / "workflow-orchestrator/references/verification-efficiency.md"

LINKED = [
    "workflow-orchestrator/SKILL.md",
    "test-architecture-engineer/SKILL.md",
    "bug-triage/SKILL.md",
    "integrated-workflow/SKILL.md",
    "integrated-workflow/references/execution-loop.md",
    "integrated-workflow/references/ui-ux-implementation.md",
    "visual-qa/SKILL.md",
    "forge-create-verification-skill/SKILL.md",
    "forge-maintain-verification-skill/SKILL.md",
    "e2e/SKILL.md",
    "e2e/references/setup.md",
    "e2e/references/bug-bash.md",
    "devin-forge/SKILL.md",
    "codex-forge/assets/automations/benny/skills/reproduce-and-fix-issues/references/control-adapter.md",
]


class VerificationEfficiencyTests(unittest.TestCase):
    def test_every_entry_resolves_a_real_link(self):
        """Each listed entry contains a markdown link that resolves to the reference."""
        selected = {entry['name'] for entry in json.loads((ROOT / 'catalog/skills.yaml').read_text())['vendored']}
        if 'workflow-orchestrator' not in selected:
            self.skipTest("workflow-orchestrator not in this distribution")
        self.assertTrue(REF.is_file())
        resolved_any = 0
        for rel in LINKED:
            path = SKILLS / rel
            if rel.split('/', 1)[0] not in selected:
                continue
            self.assertTrue(path.is_file(), rel)
            text = path.read_text()
            targets = re.findall(r"\]\(([^)]+verification-efficiency\.md)\)", text)
            self.assertTrue(targets, rel)
            for target in targets:
                self.assertEqual((path.parent / target).resolve(), REF.resolve(), rel)
            resolved_any += 1
        self.assertGreater(resolved_any, 0)

    def test_cadence_and_failure_rules(self):
        """Cadence is phase-driven and repeated failures route to discrimination."""
        text = REF.read_text()
        self.assertIn("commit or review comment alone is not a full", text)
        self.assertIn("commit-time static, unit", text)
        self.assertIn("second similar unexplained failure", text)
        self.assertIn("infrastructure", text)

    def test_capture_inspection_teardown_and_pins(self):
        """Captured files are not inspected evidence; teardown is owned; pins exist."""
        text = REF.read_text()
        self.assertIn("separately from inspection state", text)
        self.assertIn("pinned", text)
        self.assertIn("Never kill by process name", text)
        self.assertIn("not acceptance", text)

    def test_instruction_scenarios(self):
        """The named coverage scenarios are present."""
        text = REF.read_text()
        for fragment in (
            "A narrow logic fix",
            "A visual layout correction",
            "short recording or trace",
            "infrastructure launch blocker",
            "invalidates a previously green result",
        ):
            self.assertIn(fragment, text)

    def test_reference_stays_project_agnostic(self):
        """No product names, runtimes or local paths leak into the generic method."""
        text = REF.read_text()
        for forbidden in ("EVERSO", "27.1", "26.5", "18.6", "xcodebuild", "/Users/", "Supabase"):
            self.assertNotIn(forbidden, text)

    def test_bug_bash_command_disables_routine_media(self):
        """Execute the published shell recipe with a local CLI probe, no app/network."""
        path = SKILLS / "e2e/references/bug-bash.md"
        if not path.is_file():
            self.skipTest("e2e not in this distribution")
        blocks = re.findall(r"```bash\n(.*?)```", path.read_text(), re.S)
        command = next(block for block in blocks if "xargs -0" in block)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            probe = root / "bin" / "npx"
            probe.parent.mkdir()
            probe.write_text("#!/bin/sh\nprintf '%s\\n' \"$@\"\n")
            probe.chmod(0o755)
            env = dict(os.environ, PATH=str(probe.parent) + os.pathsep + os.environ.get("PATH", ""))
            result = subprocess.run(["bash", "-c", command], cwd=root, env=env,
                                    capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 0, result.stderr)
            first_runs = set((root / ".e2e/bugbash").iterdir())
            first_logs = {p: p.read_bytes() for p in (root / ".e2e/bugbash").rglob("*.log")}
            repeat = subprocess.run(["bash", "-c", command], cwd=root, env=env,
                                    capture_output=True, text=True, timeout=15)
            self.assertEqual(repeat.returncode, 0, repeat.stderr)
            self.assertEqual(len(set((root / ".e2e/bugbash").iterdir()) - first_runs), 1)
            self.assertEqual({p: p.read_bytes() for p in first_logs}, first_logs)
            logs = sorted((root / ".e2e/bugbash").rglob("*.log"))
            self.assertEqual(len(logs), 4)
            for log in logs:
                args = log.read_text().splitlines()
                self.assertEqual(args[:2], ["e2e", "explore"])
                self.assertEqual([a for a in args if a.startswith("--video")], ["--video=off"])
                self.assertEqual([a for a in args if a.startswith("--trace")], ["--trace=off"])

    def test_e2e_defaults_stay_truthful(self):
        """The E2E reference keeps real upstream defaults; examples choose off."""
        setup_path = SKILLS / "e2e/references/setup.md"
        if not setup_path.is_file():
            self.skipTest("e2e skill not in this distribution")
        setup = setup_path.read_text()
        self.assertIn("| `video` | `'off'` |", setup)
        self.assertIn("'retain-on-failure'", setup)
        self.assertIn("`video: 'off'` and `trace: 'off'`", setup)
        self.assertIn("usage recommendations, not changed SDK defaults", setup)


if __name__ == "__main__":
    unittest.main()
