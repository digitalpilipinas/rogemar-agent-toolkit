"""Contract checks for the shared verification-efficiency method."""
from pathlib import Path
import re
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
]


class VerificationEfficiencyTests(unittest.TestCase):
    def test_every_entry_resolves_a_real_link(self):
        """Each listed entry contains a markdown link that resolves to the reference."""
        if not REF.is_file():
            self.skipTest("workflow-orchestrator not in this distribution")
        resolved_any = 0
        for rel in LINKED:
            path = SKILLS / rel
            if not path.is_file():
                continue
            text = path.read_text()
            match = re.search(r"\]\(([^)]+verification-efficiency\.md)\)", text)
            self.assertIsNotNone(match, rel)
            resolved = (path.parent / match.group(1)).resolve()
            self.assertEqual(resolved, REF.resolve(), rel)
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
