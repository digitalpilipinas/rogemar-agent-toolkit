import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
catalog = json.loads((Path(__file__).resolve().parents[1] / 'catalog/skills.yaml').read_text())
if 'distribution_selection' in catalog['package'] and not set(['plan-model-router']).issubset({e['name'] for e in catalog['vendored']}):
    raise unittest.SkipTest('optional skills were not selected for this distribution')

FILE=ROOT/'plugins/rogemar-agent-toolkit/skills/plan-model-router/scripts/resolve_profile.py'
spec=importlib.util.spec_from_file_location('role_router',FILE)
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)

class RoleMappingTests(unittest.TestCase):
    def request(self, mode='optimize', role='how-explorer'):
        return {'parent':{'model':'gpt-6-astra','effort':'medium'},
                'catalog':[{'model':m,'efforts':list(r.EFFORT_RANK)} for m in r.MODEL_RANK],
                'mode':mode,'role':role,'task_reason':'bounded read-only investigation with checkable evidence'}

    def test_all_role_defaults_resolve_inside_their_mode(self):
        for mode, roles in r.ROLE_PROFILES.items():
            self.assertEqual(set(roles),r.ROLES)
            for role,profile in roles.items():
                request=self.request(mode,role)
                if role in r.MAIN_ROLES:request['target']='parent'
                result=r.resolve(request)
                with self.subTest(mode=mode,role=role):
                    self.assertEqual(result['status'],'ready')
                    self.assertEqual(result['expected_from_config'],profile)
                    self.assertIsNone(result['observed_effective'])
                    self.assertIn(profile['effort'],r.MODE_PROFILES[mode][profile['model']])

    def test_saved_switches_change_same_role_without_explicit_candidates(self):
        expected=[('peak','gpt-5.6-terra','medium'),('balanced','gpt-5.6-luna','max'),('lean','gpt-5.6-luna','high'),('sprint','gpt-5.6-luna','low')]
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'forge.json'
            for mode,model,effort in expected:
                r.set_mode(p,mode)
                request=self.request();del request['mode']
                request['preferences']=json.loads(p.read_text())
                result=r.resolve(request)
                self.assertEqual(result['requested'],{'model':model,'reasoning_effort':effort})
                self.assertEqual(result['mode'],mode)

    def test_requires_task_qualification_and_known_role(self):
        request=self.request();del request['task_reason']
        with self.assertRaises(ValueError):r.resolve(request)
        request=self.request(role='typo')
        with self.assertRaises(ValueError):r.resolve(request)
        with self.assertRaises(ValueError):r.resolve(self.request(role='parent-coordinator'))

    def test_unavailable_default_does_not_silently_fallback(self):
        request=self.request();request['catalog']=[x for x in request['catalog'] if x['model']!='gpt-5.6-luna']
        self.assertEqual(r.resolve(request)['status'],'blocked')

    def test_saved_preferences_are_used_but_cannot_escape_mode(self):
        request=self.request()
        request['preferences']={'schema_version':2,'active_mode':'optimize','policy':'adaptive','parent_policy':'mode-adaptive','roles':{'how-explorer':{'preferred_models':['gpt-5.6-terra'],'effort_hint':'high'}}}
        self.assertEqual(r.resolve(request)['requested'],{'model':'gpt-5.6-terra','reasoning_effort':'high'})
        request['preferences']['roles']['how-explorer']['preferred_models']=['gpt-6-astra']
        self.assertEqual(r.resolve(request)['status'],'blocked')
        request['preferences']['roles']['how-explorer']['preferred_models']=['inherit-parent']
        with self.assertRaises(ValueError):r.resolve(request)
        del request['preferences']['roles']['how-explorer']['effort_hint']
        self.assertEqual(r.resolve(request)['status'],'blocked')

    def test_explicit_task_adaptation_remains_checked(self):
        request=self.request();request['candidates']=[{'model':'gpt-5.6-sol','effort':'high','reason':'actual scope requires more judgment'}]
        self.assertEqual(r.resolve(request)['status'],'ready')
        request['role_config']={'model':'gpt-6-astra','effort':'medium'}
        self.assertEqual(r.resolve(request)['status'],'blocked')

    def test_legacy_mode_aliases_preserve_saved_choices(self):
        for alias,canonical in [('supreme','peak'),('optimize','balanced'),('budget','lean')]:
            pref={'schema_version':2,'active_mode':alias,'parent_policy':'mode-adaptive','policy':'adaptive',
                  'roles':{'feature':{'preferred_models':['gpt-5.6-terra'],'effort_hint':'medium'}}}
            original=copy.deepcopy(pref)
            migrated=r.migrate_preferences(pref)
            self.assertEqual(migrated['active_mode'],canonical)
            self.assertEqual(migrated['roles'],original['roles'])
            self.assertEqual(pref,original)
            self.assertEqual(r.resolve(self.request(alias))['mode'],canonical)

    def test_group_defaults_role_overrides_and_saved_preferences(self):
        self.assertEqual(r.resolve(self.request('balanced','validation-runner'))['requested'],
                         {'model':'gpt-5.6-terra','reasoning_effort':'high'})
        for role in ['hillclimb','hardest-tasks']:
            self.assertEqual(r.resolve(self.request('balanced',role))['requested'],
                             {'model':'gpt-5.6-sol','reasoning_effort':'xhigh'})
        request=self.request('balanced','hardest-tasks')
        request['preferences']={'schema_version':2,'active_mode':'lean','parent_policy':'mode-adaptive','policy':'adaptive',
                               'roles':{'hardest-tasks':{'preferred_models':['gpt-5.6-terra'],'effort_hint':'high'}}}
        self.assertEqual(r.resolve(request)['requested'],{'model':'gpt-5.6-terra','reasoning_effort':'high'})

    def test_main_owned_roles_cannot_be_dispatched_as_workers(self):
        for role in ['parent-coordinator','workflow-coordinator','integration-owner']:
            with self.assertRaises(ValueError):r.resolve(self.request('balanced',role))
            request=self.request('balanced',role);request['target']='parent'
            self.assertFalse(r.resolve(request)['parent_adaptation']['runtime_switch_performed'])

    def test_native_goal_pins_require_exact_qualified_profile(self):
        request=self.request('sprint','goal-scout');request['role_config']={'effort':'low'}
        self.assertEqual(r.resolve(request)['status'],'ready')
        request=self.request('sprint','goal-judge');request['role_config']={'effort':'high'}
        self.assertEqual(r.resolve(request)['status'],'blocked')
        request['candidates']=[{'model':'gpt-5.6-luna','effort':'high','reason':'native judge pin and bounded check'}]
        self.assertEqual(r.resolve(request)['status'],'ready')

    def test_documented_role_table_matches_executable_mapping(self):
        doc=(FILE.parents[1]/'references/role-mapping.md').read_text()
        for role in r.ROLES:
            row=next(line for line in doc.splitlines() if line.startswith('| `'+role+'`'))
            for mode in r.MODE_PROFILES:
                profile=r.ROLE_PROFILES[mode][role]
                self.assertIn(profile['model'].split('-')[-1]+'/'+profile['effort'],row)
