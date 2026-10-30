"""Each harness receives only compatible skills, and their links stay inside that set."""
import importlib.util
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'plugins/rogemar-agent-toolkit/skills'
spec = importlib.util.spec_from_file_location('toolkit_packaging', ROOT / 'scripts/toolkit.py')
toolkit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(toolkit)
LINK = re.compile(r'\]\((\.\./(?:\.\./)?([a-z0-9-]+)/[^)#\s]*)')
HARNESS_ONLY = {'codex-forge', 'cursor-forge', 'devin-forge', 'plan-model-router', 'hatch-pet',
                'forge-setup', 'cursor-forge-setup'}


@unittest.skipIf(json.loads((ROOT / 'catalog/skills.yaml').read_text()).get('package', {}).get('distribution_selection'),
                 'Harness packaging is checked in the canonical checkout')
class HarnessPackagingTests(unittest.TestCase):
    def test_claude_marketplace_lists_only_claude_skills(self):
        entry = json.loads((ROOT / '.claude-plugin/marketplace.json').read_text())['plugins'][0]
        self.assertEqual(entry['source'], './')  # root source: Claude loads only the listed skills
        listed = {path.rsplit('/', 1)[1] for path in entry['skills']}
        self.assertEqual(listed, set(toolkit.resolve_selection('claude', 'all', [])['skills']))
        self.assertFalse(listed & HARNESS_ONLY - {'claude-forge-setup'})
        for path in entry['skills']:
            self.assertTrue((ROOT / path / 'SKILL.md').is_file(), path)

    def test_links_stay_inside_each_harness_selection(self):
        for harness in ('claude', 'cursor', 'codex', 'agent-skills'):
            selected = set(toolkit.resolve_selection(harness, 'all', [])['skills'])
            for name in selected:
                for page in (SKILLS / name).rglob('*.md'):
                    for _target, skill in LINK.findall(page.read_text(errors='ignore')):
                        if (SKILLS / skill).is_dir():
                            with self.subTest(harness=harness, page=str(page.relative_to(SKILLS))):
                                self.assertIn(skill, selected)


if __name__ == '__main__':
    unittest.main()
