"""The Integrated Workflow entry points an agent at one file, and Claude uses Forge mode."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "plugins/rogemar-agent-toolkit/skills"


class IntegratedWorkflowEntryTests(unittest.TestCase):
    def test_entry_names_one_file_per_situation(self):
        """The entry names one file per situation and defines sprint strategies."""
        path = SKILLS / "integrated-workflow/SKILL.md"
        if not path.is_file():
            self.skipTest("Integrated Workflow was not selected for this distribution")
        text = path.read_text()
        self.assertIn("## Open the files the active situations need", text)
        self.assertIn("A task may have several\nactive situations.", text)
        self.assertIn(
            "Open each file those situations name. Leave a file closed\n"
            "only when its situation is absent.",
            text,
        )
        self.assertNotIn("## Open only the file this task needs", text)
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
        self.assertIn("one vertical slice, or one task inside that slice", text)
        self.assertIn("more than one vertical slice or task", text)
        self.assertNotIn("one write-capable owner per worktree", text)
        self.assertNotIn("one writer at a time", text)
        self.assertIn("The parent selects the playbook and the skills", text)
        self.assertIn("choose another playbook", text)
        self.assertIn("No reusable app recipe exists", text)
        self.assertIn("An existing app recipe has drifted", text)
        self.assertIn("`forge-how`", text)
        self.assertIn("`forge-principle-prove-it-works`", text)
        self.assertIn("benchmark-checklist", text)
        contract = (SKILLS / "workflow-orchestrator/references/method-contract.md").read_text()
        self.assertIn("Name\n   the playbook and the skills in that brief.", contract)
        self.assertIn("does not choose another\n   playbook", contract)

    def test_forge_mode_includes_claude(self):
        """Forge mode applies on Claude as well as Codex, Cursor, and Universal."""
        text = (SKILLS / "workflow-orchestrator/SKILL.md").read_text()
        self.assertIn("Codex, Cursor, Claude, or Universal Forge", text)
        self.assertIn("One vertical slice, or one task inside that slice", text)
        self.assertIn("more than one vertical slice or task", text)
        self.assertNotIn("serializes writers in one worktree", text)
        self.assertNotIn("one-writer limits", text)


if __name__ == "__main__":
    unittest.main()
