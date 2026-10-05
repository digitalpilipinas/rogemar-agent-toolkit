"""The Integrated Workflow entry points an agent at one file, and Claude uses Forge mode."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "plugins/rogemar-agent-toolkit/skills"


class IntegratedWorkflowEntryTests(unittest.TestCase):
    def test_entry_names_one_file_per_situation(self):
        text = (SKILLS / "integrated-workflow/SKILL.md").read_text()
        self.assertIn("## Open only the file this task needs", text)
        for target in (
            "references/ui-ux-implementation.md",
            "references/supporting-methods.md",
            "references/execution-loop.md",
            "references/coderabbit-review.md",
            "references/capability-fallbacks.md",
            "../workflow-orchestrator/references/route-readiness.md",
        ):
            self.assertIn(target, text)
            self.assertTrue((SKILLS / "integrated-workflow" / target).is_file(), target)
        self.assertIn("plan-model-router", text)
        self.assertIn("universal-plan-model-router", text)

    def test_forge_mode_includes_claude(self):
        text = (SKILLS / "workflow-orchestrator/SKILL.md").read_text()
        self.assertIn("Codex, Cursor, Claude, or Universal Forge", text)


if __name__ == "__main__":
    unittest.main()
