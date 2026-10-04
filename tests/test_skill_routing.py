import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import copy
import hashlib
import io
import tarfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'plugins/rogemar-agent-toolkit/skills'


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


ROUTING = module('routing_catalog_test', ROOT / 'scripts/routing_catalog.py')
SELECT = module('select_methods_test', SKILLS / 'workflow-orchestrator/scripts/select_methods.py')
METADATA = module('external_metadata_test', ROOT / 'scripts/external_metadata.py')


class SkillRoutingTests(unittest.TestCase):
    def setUp(self):
        self.index = ROUTING.expected_index(ROOT)

    def test_catalog_and_generated_index_agree(self):
        self.assertEqual(ROUTING.verify(ROOT), [])

    def test_all_selected_methods_resolve_to_original_working_skills(self):
        names = [n for n in self.index['skills'] if n not in SELECT.ENTRIES and self.index['skills'][n].get('kind') != 'external']
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

    def test_distinct_external_routes_preserve_source_policy(self):
        routes=self.index['skills']
        self.assertNotEqual(routes['convex-backup']['trigger'],routes['convex-auth']['trigger'])
        self.assertEqual(routes['interrogate']['activation'],'explicit-only')
        with self.assertRaisesRegex(ValueError,'explicit invocation'):
            SELECT.resolve(self.index,['interrogate'],SKILLS)
        for name,route in routes.items():
            if route.get('kind')=='external':
                self.assertRegex(route['source_sha256'],r'^[0-9a-f]{64}$')

    def test_changed_pin_or_missing_member_rejects_stale_metadata(self):
        catalog=json.loads((ROOT/'catalog/skills.yaml').read_text())
        for mutation in ('pin','member','resource'):
            changed=copy.deepcopy(catalog)
            recipe=changed['dependencies']['coderabbit']['auto_install']
            if mutation=='pin': recipe['commit']='0'*40
            if mutation=='member': recipe['metadata']['skills'].pop('autofix')
            if mutation=='resource': recipe['metadata']['skills']['autofix']['required_resources']=['../outside']
            with tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp);(root/'catalog').mkdir()
                (root/'catalog/skills.yaml').write_text(json.dumps(changed))
                with self.assertRaises(ValueError): ROUTING.expected_index(root)

    def test_reviewed_override_cannot_relax_source_invocation_policy(self):
        catalog=json.loads((ROOT/'catalog/skills.yaml').read_text())
        catalog['dependencies']['pstack']['auto_install']['routing_overrides']={
            'interrogate':{'activation':'conditional','reason':'invalid relaxation'}}
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'catalog').mkdir()
            (root/'catalog/skills.yaml').write_text(json.dumps(catalog))
            with self.assertRaisesRegex(ValueError,'cannot relax'):
                ROUTING.expected_index(root)

    def test_metadata_reads_pinned_instructions_and_resources_without_execution(self):
        data=b'---\nname: example\ndescription:\n  Inspect a scoped fixture.\n  Preserve its evidence.\ndisable-model-invocation: true # require explicit invocation\n---\nRead refs/check.md'
        archive=io.BytesIO()
        with tarfile.open(fileobj=archive,mode='w') as tar:
            for path,body in [('SKILL.md',data),('refs/check.md',b'evidence')]:
                info=tarfile.TarInfo(path);info.size=len(body);tar.addfile(info,io.BytesIO(body))
        recipe={'commit':'1'*40,'skills':{'example':'.'}}
        with patch.object(METADATA,'git',side_effect=[b'1'*40+b'\n',archive.getvalue()]) as git:
            result=METADATA.extract(recipe,Path('/fixture'))
        row=result['skills']['example']
        self.assertEqual(row['description'],'Inspect a scoped fixture. Preserve its evidence.')
        self.assertEqual(row['activation'],'explicit-only')
        self.assertEqual(row['required_resources'],['refs/check.md'])
        self.assertEqual(row['skill_sha256'],hashlib.sha256(data).hexdigest())
        self.assertEqual(git.call_count,2)
        self.assertEqual(git.call_args.args[1],'archive')


if __name__ == '__main__':
    unittest.main()
