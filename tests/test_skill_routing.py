import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'plugins/rogemar-agent-toolkit/skills'


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


ROUTING = module('routing_catalog_test', ROOT / 'scripts/routing_catalog.py')
SELECT = module('select_methods_test', SKILLS / 'workflow-orchestrator/scripts/select_methods.py')


class SkillRoutingTests(unittest.TestCase):
    def setUp(self):
        self.index = ROUTING.expected_index(ROOT)

    def test_catalog_and_generated_index_agree(self):
        self.assertEqual(ROUTING.verify(ROOT), [])

    def test_all_selected_methods_resolve_to_original_working_skills(self):
        names = [n for n in self.index['skills'] if n not in SELECT.ENTRIES]
        result = SELECT.resolve(self.index, names, SKILLS,
                                explicit=['deliver-approved-programme'])
        self.assertTrue(all(r['route'] == 'source' for r in result['methods']))
        self.assertFalse(result['grants_authority'])

    def test_each_entry_retains_its_own_execution_owner(self):
        for entry in SELECT.ENTRIES & self.index['skills'].keys():
            result = SELECT.resolve(self.index, [entry, 'create-plan'], SKILLS, entry=entry)
            self.assertEqual(result['entry'], entry)
            self.assertEqual(len(result['methods']), 2)
        with self.assertRaises(ValueError):
            SELECT.resolve(self.index, ['codex-forge', 'universal-forge'], SKILLS)
        with self.assertRaises(ValueError):
            SELECT.resolve(self.index, ['codex-forge'], SKILLS, entry='cursor-forge')

    def test_explicit_only_alias_is_not_implicitly_selected(self):
        if 'deliver-approved-programme' not in self.index['skills']:
            self.skipTest('Legacy alias not selected in this distribution')
        with self.assertRaises(ValueError):
            SELECT.resolve(self.index, ['deliver-approved-programme'], SKILLS)
        self.assertEqual(SELECT.resolve(self.index, ['deliver-approved-programme'], SKILLS,
                         explicit=['deliver-approved-programme'])['methods'][0]['route'], 'source')

    def test_portable_fallback_and_missing_capability_are_distinct(self):
        if 'forge-how' not in self.index['skills']:
            self.skipTest('Native companion not selected in this distribution')
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            method = root / 'engineering-playbooks/references/companion-methods.md'
            method.parent.mkdir(parents=True)
            method.write_text('## How\nTrace relevant source.\n')
            result = SELECT.resolve(self.index, ['forge-how'], root, entry='universal-forge')
            self.assertEqual(result['methods'][0]['route'], 'fallback')
            method.unlink()
            result = SELECT.resolve(self.index, ['forge-how'], root, entry='universal-forge')
            self.assertEqual(result['methods'][0]['status'], 'unavailable')

    def test_unknown_methods_and_unsafe_resources_are_rejected(self):
        with self.assertRaises(ValueError):
            SELECT.resolve(self.index, ['invented-native-tool'], SKILLS)
        self.index['skills']['create-plan']['source'] = '../../outside.md'
        with self.assertRaises(ValueError):
            SELECT.resolve(self.index, ['create-plan'], SKILLS)

    def test_unrelated_skills_are_not_added_to_a_focused_selection(self):
        result = SELECT.resolve(self.index, ['create-plan', 'create-plan'], SKILLS)
        self.assertEqual([r['method'] for r in result['methods']], ['create-plan'])


if __name__ == '__main__':
    unittest.main()
