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
    def test_claude_marketplace_uses_the_plugin_folder_and_versioned_entry(self):
        # claude.ai's marketplace sync rejected a root source with a skill list, so
        # Claude's plugin carries the whole folder; the managed installer still filters.
        entry = json.loads((ROOT / '.claude-plugin/marketplace.json').read_text())['plugins'][0]
        self.assertEqual(entry['source'], './plugins/rogemar-agent-toolkit')
        self.assertNotIn('skills', entry)
        self.assertEqual(entry['version'], json.loads(
            (SKILLS.parent / '.claude-plugin/plugin.json').read_text())['version'])

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
