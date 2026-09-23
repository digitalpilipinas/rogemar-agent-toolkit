"""Generation identity, native support and preserved explicit legacy choices."""
import copy
import unittest
from unittest.mock import patch
from test_forge import router as r


class GenerationTests(unittest.TestCase):
    def request(self, model, effort='xhigh', mode='default', role='how-explorer'):
        return {'mode': mode, 'role': role, 'parent': {'model': model, 'effort': effort},
                'task_reason': 'bounded source inspection',
                'catalog': [{'model': m, 'efforts': c['supported_efforts']}
                            for m, c in r.ROUTING_CATALOG['models'].items()]}

    def test_named_pools_and_targets_are_exact(self):
        pools = {'peak': ['gpt-6-astra', 'gpt-6-sol', 'gpt-5.6-sol', 'gpt-6-luna'],
                 'balanced': ['gpt-6-sol', 'gpt-5.6-sol', 'gpt-6-luna'],
                 'lean': ['gpt-5.6-sol', 'gpt-6-luna'], 'economy': ['gpt-6-luna']}
        for mode, models in pools.items():
            self.assertEqual(set(r.MODE_PROFILES[mode]), set(models))
            level = 'medium' if mode == 'economy' else 'xhigh'
            self.assertEqual(r.ROUTING_CATALOG['parent_targets'][mode],
                             {'model': models[0], 'effort': level})
            for allowed in r.MODE_PROFILES[mode].values():
                self.assertEqual(set(allowed), set(list(r.EFFORT_RANK)[:r.EFFORT_RANK[level]+1]))
        self.assertLess(r.MODEL_RANK['gpt-6-luna'], r.MODEL_RANK['gpt-5.6-sol'])
        self.assertLess(r.MODEL_RANK['gpt-5.6-sol'], r.MODEL_RANK['gpt-6-sol'])
        self.assertLess(r.MODEL_RANK['gpt-6-sol'], r.MODEL_RANK['gpt-6-astra'])

    def test_exact_default_preserves_generations_and_legacy_profiles(self):
        for model, config in r.ROUTING_CATALOG['models'].items():
            for level in config['supported_efforts']:
                q = self.request(model, level)
                self.assertEqual(r.resolve(q)['expected_from_config'], q['parent'])
                other = 'gpt-6-sol' if model != 'gpt-6-sol' else 'gpt-5.6-sol'
                q['candidates'] = [{'model': other, 'effort': level, 'reason': 'successor'}]
                self.assertEqual(r.resolve(q)['status'], 'blocked')
        q = self.request('gpt-5.5')
        q['catalog'].append({'model': 'gpt-5.5', 'efforts': ['low', 'medium', 'high', 'xhigh']})
        self.assertEqual(r.resolve(q)['expected_from_config'], q['parent'])
        q['candidates'] = [{'model': 'gpt-5.5', 'effort': 'high', 'reason': 'Lower usage'}]
        self.assertEqual(r.resolve(q)['status'], 'blocked')

    def test_luna_ultra_rejected_even_with_overbroad_runtime_fixture(self):
        q = self.request('gpt-6-luna', 'ultra')
        for item in q['catalog']:
            item['efforts'] = list(r.EFFORT_RANK)
        self.assertEqual(r.resolve(q)['status'], 'blocked')
        q['parent']['effort'] = 'max'
        self.assertEqual(r.resolve(q)['status'], 'ready')

    def test_legacy_preferences_are_preserved_not_translated(self):
        prefs = {'schema_version': 3, 'policy': 'adaptive', 'parent_policy': 'mode-adaptive',
                 'active_mode': 'balanced', 'default_profile': {'model': 'gpt-5.6-terra', 'effort': 'max'},
                 'roles': {'how-explorer': {'preferred_models': ['gpt-5.6-luna'], 'effort_hint': 'low'}}}
        self.assertEqual(r.migrate_preferences(prefs), prefs)
        result = r.resolve({**self.request('gpt-6-sol', mode='balanced'), 'preferences': prefs})
        self.assertEqual(result['status'], 'blocked')
        self.assertEqual(result['rejected'][0]['candidate']['model'], 'gpt-5.6-luna')
        self.assertTrue(any('normal pool' in reason for reason in result['rejected'][0]['reasons']))
        self.assertEqual(r.normalize_mode('sprint'), 'economy')
        self.assertEqual(r.normalize_mode('budget'), 'lean')

    def test_explicit_legacy_limit_is_not_upgraded(self):
        q = self.request('gpt-6-sol', mode='balanced', role='architect-runners')
        q['limits'] = {'model': 'gpt-5.6-sol'}
        result = r.resolve(q)
        self.assertEqual(result['status'], 'blocked')
        self.assertIn('explicit model limit', result['rejected'][0]['reasons'])

    def test_qualification_cannot_transfer_generation_or_contract(self):
        p = {'model': 'gpt-5.6-sol', 'effort': 'high'}
        record = {**p, 'status': 'verified', 'evidence_id': 'fixture-only', 'executable': True,
                  'evidence_contract': 'notes-store',
                  'validation': [{'assignment_id': str(i), 'repetition': i, 'packet_sha256': 'packet',
                                  'profile': p, 'profile_verified': True, 'passed': True} for i in (1, 2)]}
        record['coding_validation'] = copy.deepcopy(record['validation'])
        with patch.dict(r.ROUTING_CATALOG['qualified_profiles'], {'ui-designer': [record]}):
            self.assertIsNone(r.qualification('ui-designer', {'model': 'gpt-6-sol', 'effort': 'high'}, True))
            q = self.request('gpt-6-sol', mode='balanced', role='ui-designer')
            q.update(implementation=True, evidence_contract='note-editor-ui',
                     candidates=[{**p, 'reason': 'fixture'}])
            self.assertEqual(r.resolve(q)['status'], 'blocked')
            record['model'] = 'gpt-6-sol'
            self.assertFalse(r.paired(record))

    def test_review_support_uses_catalogue_owned_profile(self):
        p = {'model': 'gpt-6-luna', 'effort': 'low'}
        record = {**p, 'status': 'verified', 'evidence_id': 'support-fixture-only',
                  'validation': [{'assignment_id': str(i), 'repetition': i, 'packet_sha256': 'support',
                                  'profile': p, 'profile_verified': True, 'passed': True} for i in (1, 2)]}
        q = self.request('gpt-6-sol', mode='balanced', role='status-monitor')
        q['candidates'] = [{**p, 'reason': 'Clerical status only'}]
        with patch.dict(r.ROUTING_CATALOG['qualified_profiles'], {'status-monitor': [record]}):
            self.assertEqual(r.resolve(q)['status'], 'ready')
            with patch.dict(r.ROUTING_CATALOG, {'review_support_models': ['gpt-5.6-luna']}):
                self.assertEqual(r.resolve(q)['status'], 'blocked')
            for flag in ('consequential', 'implementation'):
                self.assertEqual(r.resolve({**q, flag: True})['status'], 'blocked')

    def test_every_active_consultant_resolves_with_its_declared_scope(self):
        for mode, roles in r.ROUTING_CATALOG['exceptions'].items():
            parent = r.ROUTING_CATALOG['parent_targets'][mode]
            for role, records in roles.items():
                for ex in records:
                    with self.subTest(mode=mode, role=role, evidence=ex['evidence_id']):
                        profile = {k: ex[k] for k in ('model', 'effort')}
                        failures = [f for f in r.ROUTING_CATALOG['known_failures'].get(role, [])
                                    if f['profile'] == profile and not f.get('coding_only')]
                        self.assertEqual(failures, [], 'Known defects cannot qualify active consultants')
                        read_only = ex.get('allowed_assignment') == 'read-only-consultation'
                        q = self.request(parent['model'], parent['effort'], mode, role)
                        q.update(candidates=[{**profile, 'reason': 'Bounded consultant for an unmet contract'}],
                                 difficult_task=True, exception_reason='Parent needs independent retry-concurrency advice',
                                 exception_evidence_id=ex['evidence_id'], evidence_contract=ex['evidence_contract'],
                                 implementation=not read_only)
                        result = r.resolve(q)
                        self.assertEqual(result['status'], 'ready', result)
                        self.assertTrue(result['exception_applied'])
                        if read_only:
                            denied = r.resolve({**q, 'implementation': True})
                            self.assertEqual(denied['status'], 'blocked')

    def test_failed_legacy_hard_task_exception_is_retired(self):
        q = self.request('gpt-6-luna', 'medium', 'economy', 'hardest-tasks')
        q.update(candidates=[{'model': 'gpt-5.6-sol', 'effort': 'xhigh', 'reason': 'Legacy consultant'}],
                 implementation=True, difficult_task=True, evidence_contract='notes-store',
                 exception_evidence_id='v4-hardest-tasks-gpt-5.6-sol-xhigh',
                 exception_reason='Need safe legacy-note preservation')
        self.assertEqual(r.resolve(q)['status'], 'blocked')

    def test_new_parent_generation_invalidates_old_fallback_choice(self):
        q = self.request('gpt-6-astra', mode='balanced', role='architect-runners')
        q['parent_fallback'] = {'mode': 'balanced', 'actual': q['parent'],
                                'desired': {'model': 'gpt-5.6-sol', 'effort': 'xhigh'}, 'accepted': True}
        result = r.resolve(q)
        self.assertEqual(result['status'], 'parent-choice-required')
        self.assertEqual(result['parent_adaptation']['desired']['model'], 'gpt-6-sol')
        self.assertFalse(result['parent_adaptation']['runtime_switch_performed'])


if __name__ == '__main__':
    unittest.main()
