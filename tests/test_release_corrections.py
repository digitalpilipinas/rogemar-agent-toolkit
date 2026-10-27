"""Check the observable role and license-inventory contracts."""
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "plugins/rogemar-agent-toolkit/skills"


class ReleaseCorrectionsTests(unittest.TestCase):
    def test_devin_qa_roles_and_license_scopes(self):
        skill = SKILLS / "devin-forge"
        if not skill.is_dir():
            self.skipTest("Devin Forge not selected in this distribution")
        text = (skill / "SKILL.md").read_text()
        rows = {line.split("|")[1].strip(): line for line in text.splitlines()
                if line.startswith("| ") and ("workers (" in line or line.startswith("| Clerical / monitoring"))}
        self.assertIn("accessibility-reviewer", rows["Judgment workers (independent-context reviews, judges, synthesis, design)"])
        self.assertIn("browser-qa", rows["Implementation workers (bounded writes/verification)"])
        self.assertIn("physical-device-qa", rows["Implementation workers (bounded writes/verification)"])
        self.assertNotIn("qa", rows["Clerical / monitoring (support receipts, no judgment claims)"])
        self.assertIn("license: See LICENSE.adapter.txt and LICENSE.txt", text)
        self.assertIn("Rogemar", (skill / "LICENSE.adapter.txt").read_text())
        self.assertIn("Lauren Tan", (skill / "LICENSE.txt").read_text())

    def test_inventory_exposes_all_appllama_notices_without_relicensing_snapshots(self):
        catalog = json.loads((ROOT / "catalog/skills.yaml").read_text())
        entries = {item["name"]: item for item in catalog["vendored"]}
        spec = importlib.util.spec_from_file_location("release_inventory", ROOT / "scripts/inventory_readme.py")
        inventory = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(inventory)
        rows = "\n".join(inventory.vendored_section(catalog))
        names = ("interaction-polish", "motion-animation-engineer", "ux-flow-architect", "reference-design-contract")
        for name in names:
            if name not in entries:
                continue
            self.assertTrue((SKILLS / name / "LICENSE.appllama.txt").is_file())
            row = next(line for line in rows.splitlines() if line.startswith(f"| [`{name}`]"))
            self.assertIn("LICENSE.appllama.txt", row)
        if "reference-design-contract" in entries:
            row = next(line for line in rows.splitlines() if line.startswith("| [`reference-design-contract`]"))
            self.assertIn("LICENSE.txt", row)
        if "interaction-polish" in entries:
            row = next(line for line in rows.splitlines() if line.startswith("| [`interaction-polish`]"))
            self.assertIn("Appllama adaptation: MIT", row)
            self.assertIn("original snapshot license not declared", row)


if __name__ == "__main__":
    unittest.main()
