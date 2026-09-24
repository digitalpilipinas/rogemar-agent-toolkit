"""Routing decisions, migrations and native boundaries; no model calls."""
import copy
from contextlib import contextmanager
import json
from pathlib import Path
import tempfile
import subprocess
import sys
import unittest
from test_forge import router as r


class ModeTests(unittest.TestCase):
    def request(self, mode='balanced', role='feature'):
        return {'parent': dict(r.ROUTING_CATALOG['parent_targets'].get(mode, {'model': 'gpt-6-sol', 'effort': 'xhigh'})),
                'mode': mode, 'role': role, 'task_reason': 'bounded task fits recorded contract',
                'evidence_contract': 'note-editor-ui' if role in ('ui-designer', 'ux-flow-designer', 'interaction-designer') else 'notes-store',
                'catalog': [{'model': m, 'efforts': list(r.EFFORT_RANK)} for m in r.MODEL_RANK]}

    @contextmanager
    def qualified_fixture(self, role, model='gpt-5.6-sol', effort='medium', executable=False, exception_mode=None):
        """Synthetic unit proof only; never saved to the actual catalogue."""
        original = copy.deepcopy(r.ROUTING_CATALOG)
        p = {'model': model, 'effort': effort}
        proof = [{'assignment_id': 'unit-'+str(i), 'repetition': i, 'passed': True,
                  'profile_verified': True, 'profile': p, 'packet_sha256': 'unit-packet'} for i in (1, 2)]
        record = {**p, 'status': 'verified', 'evidence_id': 'unit-proof', 'validation': proof,
                  'executable': executable, 'coding_validation': copy.deepcopy(proof) if executable else [],
                  'evidence_contract': 'notes-store', 'scope': 'synthetic unit policy fixture'}
        r.ROUTING_CATALOG['qualified_profiles'].setdefault(role, []).insert(0, record)
        if exception_mode:
            r.ROUTING_CATALOG['exceptions'].setdefault(exception_mode, {})[role] = [record]
        try:
            yield record
        finally:
            r.ROUTING_CATALOG = original

    def test_all_225_roles(self):
        for mode in r.MODE_PROFILES:
            for role in r.ROLES:
                q = self.request(mode, role)
                if role in r.MAIN_ROLES: q['target'] = 'parent'
                if role in ('swarm-workers', 'arena-runners'): q['assignment_role'] = 'how-explorer'
                x = r.resolve(q)
                self.assertEqual(x['status'], 'ready', (mode, role, x))
                self.assertIsNone(x['observed_effective'])
                if mode == 'default': self.assertEqual(x['expected_from_config'], q['parent'])
                elif role not in r.MAIN_ROLES:
                    p = x['expected_from_config']
                    self.assertIn(p['effort'], r.MODE_PROFILES[mode][p['model']])
                    self.assertLessEqual(r.MODEL_RANK[p['model']], r.MODEL_RANK[q['parent']['model']])
                    self.assertLessEqual(r.EFFORT_RANK[p['effort']], r.EFFORT_RANK[q['parent']['effort']])
                    if x['consequential']: self.assertEqual(p['model'], q['parent']['model'])

    def test_all_normal_boundaries_and_qualification(self):
        for mode in r.ROUTING_CATALOG['parent_targets']:
            for model in r.MODEL_RANK:
                for effort in r.EFFORT_RANK:
                    for role in ('feature', 'how-explorer', 'acceptance-auditor'):
                        q = self.request(mode, role); p = dict(model=model, effort=effort)
                        q['candidates'] = [{**p, 'reason': 'tested task fit'}]
                        family = role not in r.ROUTING_CATALOG['consequential_roles'] or model == q['parent']['model']
                        qualified = p == q['parent'] or bool(r.qualification(role, p, role in r.ROUTING_CATALOG['coding_roles']))
                        separation = not (mode in r.ROUTING_CATALOG['review_separation_modes'] and role == 'feature' and r.MODEL_RANK[model] < r.MODEL_RANK[r.ROUTING_CATALOG['review_decision_minimum_model']])
                        allowed = effort in r.MODE_PROFILES[mode].get(model, []) and family and qualified and separation
                        self.assertEqual(r.resolve(q)['status'] == 'ready', allowed, (mode, role, model, effort))

    def test_default_exact_and_supported_ultra(self):
        for model in ('gpt-6-astra', 'gpt-6-sol', 'gpt-5.6-sol', 'gpt-5.6-terra'):
            q = self.request('default'); q['parent'] = {'model': model, 'effort': 'ultra'}
            self.assertEqual(r.resolve(q)['expected_from_config'], q['parent'])
            q['candidates'] = [dict(model=model, effort='max', reason='cheaper')]
            self.assertEqual(r.resolve(q)['status'], 'blocked')
        q = self.request('default'); q['parent'] = {'model': 'gpt-6-luna', 'effort': 'ultra'}
        self.assertEqual(r.resolve(q)['status'], 'blocked')

    def test_scoped_ui_and_scout_qualifications(self):
        for mode in r.ROUTING_CATALOG['parent_targets']:
            x = r.resolve(self.request(mode, 'goal-scout'))
            self.assertEqual(x['dispatch_agent_type'], 'default')
            self.assertFalse(x['native_contract_required'])
            x = r.resolve(self.request(mode, 'ui-designer'))
            self.assertTrue(x['implementation']); self.assertTrue(x['task_fit_required'])
            self.assertEqual(x['role_contract']['assignment'], 'bounded-implementation')
            if x['qualification_id']:
                self.assertIn('form', x['qualification_scope'])
                self.assertEqual(x['evidence_contract'], 'note-editor-ui')
        self.assertFalse(r.qualification('visual-reviewer', {'model': 'gpt-6-sol', 'effort': 'xhigh'}, True))

    def test_qualification_requires_matching_executable_contract(self):
        with self.qualified_fixture('refactoring', executable=True) as record:
            q = self.request(); q.update(role='refactoring', candidates=[dict(model=record['model'], effort=record['effort'], reason='implementation')])
            self.assertEqual(r.resolve(q)['status'], 'ready')
            self.assertEqual(r.resolve({**q, 'evidence_contract': 'note-editor-ui'})['status'], 'blocked')
            q.pop('evidence_contract'); self.assertEqual(r.resolve(q)['status'], 'blocked')
            q['evidence_contract'] = 'notes-store'; record['coding_validation'][0]['passed'] = False
            self.assertEqual(r.resolve(q)['status'], 'blocked')
        q = self.request('balanced', 'ui-designer'); q['evidence_contract'] = 'notes-store'
        self.assertEqual(r.resolve(q)['status'], 'blocked')

    def test_parent_bound_choice_and_stricter_fallback(self):
        with self.qualified_fixture('how-explorer', 'gpt-6-luna', 'low'):
            q = self.request('balanced', 'how-explorer'); q['parent'] = {'model': 'gpt-6-luna', 'effort': 'medium'}
            self.assertEqual(r.resolve(q)['status'], 'parent-choice-required')
            q['parent_fallback'] = {'mode': 'balanced', 'desired': r.ROUTING_CATALOG['parent_targets']['balanced'], 'actual': q['parent'], 'accepted': True}
            q['candidates'] = [dict(model='gpt-6-luna', effort='low', reason='bounded support')]
            self.assertEqual(r.resolve(q)['status'], 'ready')
            q['candidates'][0]['effort'] = 'high'; self.assertEqual(r.resolve(q)['status'], 'blocked')
            q['parent'] = {'model': 'gpt-6-astra', 'effort': 'max'}
            self.assertEqual(r.resolve(q)['status'], 'parent-choice-required')
            q['parent_fallback']['actual'] = q['parent']; q['candidates'][0].update(model='gpt-6-astra', effort='low')
            self.assertEqual(r.resolve(q)['status'], 'blocked')

    def test_parent_proposal_not_switch(self):
        q = self.request(); q.update(target='parent', role='parent-coordinator', parent={'model': 'gpt-6-astra', 'effort': 'low'})
        x = r.resolve(q); self.assertEqual(x['status'], 'ready')
        self.assertTrue(x['parent_adaptation']['change_needed']); self.assertFalse(x['parent_adaptation']['runtime_switch_performed'])

    def test_exception_needs_exact_verified_profile_role_contract_and_need(self):
        with self.qualified_fixture('hillclimb', 'gpt-6-luna', 'max', True, 'economy') as ex:
            q = self.request('economy', 'hillclimb')
            q.update(candidates=[dict(model=ex['model'], effort=ex['effort'], reason='parent insufficiency')], implementation=True)
            self.assertEqual(r.resolve(q)['status'], 'blocked')
            q.update(exception_evidence_id=ex['evidence_id'], difficult_task=True, exception_reason='Concrete unmet measured requirement')
            self.assertTrue(r.resolve(q)['exception_applied'])
            for change in ({'role': 'feature'}, {'exception_evidence_id': 'forged'}, {'difficult_task': False}, {'limits': {'effort': 'medium'}}, {'evidence_contract': 'note-editor-ui'}):
                self.assertEqual(r.resolve({**q, **change})['status'], 'blocked')
            good = copy.deepcopy(ex['validation'])
            for change in ({'passed': False}, {'assignment_id': 'unit-1'}, {'repetition': 1}, {'profile_verified': False}, {'packet_sha256': 'different'}, {'profile': {'model': 'gpt-5.6-luna', 'effort': 'max'}}):
                ex['validation'] = copy.deepcopy(good); ex['validation'][1].update(change)
                self.assertEqual(r.resolve(q)['status'], 'blocked')

    def test_native_and_ordinary_goal_contracts(self):
        for role, agent in [('goal-scout', 'default'), ('goal-judge', 'verification_reviewer')]:
            q = self.request('default', role); x = r.resolve(q)
            self.assertEqual(x['dispatch_agent_type'], agent); self.assertEqual(x['expected_from_config'], q['parent'])
            q['goalbuddy_required'] = True; self.assertEqual(r.resolve(q)['status'], 'blocked')
        for role, pin in [('goal-scout', 'low'), ('goal-judge', 'high')]:
            q = self.request('lean', role); q.update(goalbuddy_required=True, role_config={'effort': pin})
            x = r.resolve(q); self.assertEqual(x['status'], 'ready'); self.assertEqual(x['expected_from_config']['effort'], pin)
        for mode, role, pin in [('economy', 'goal-judge', 'high'), ('default', 'goal-scout', 'low')]:
            q = self.request(mode, role); q.update(goalbuddy_required=True, role_config={'effort': pin})
            self.assertEqual(r.resolve(q)['status'], 'blocked')

    def test_aliases_and_explicit_no_mode(self):
        for a, c in [('supreme', 'peak'), ('optimize', 'balanced'), ('budget', 'lean'), ('sprint', 'economy')]: self.assertEqual(r.normalize_mode(a), c)
        q = self.request(); q['preferences'] = {'schema_version': 2, 'active_mode': 'lean', 'policy': 'adaptive', 'parent_policy': 'mode-adaptive', 'roles': {}}
        self.assertEqual(r.resolve(q)['mode'], 'balanced'); q.update(mode=None, role=None)
        self.assertIsNone(r.resolve(q)['mode'])

    def test_overrides_preserved_but_cannot_escape_policy(self):
        pref = {'schema_version': 1, 'policy': 'adaptive', 'parent_policy': 'suggest-at-phase-boundaries', 'roles': {'how explorer': {'preferred_models': ['inherit-parent']}}}
        v = r.migrate_preferences(pref); self.assertEqual(v['schema_version'], 3); self.assertIn('how-explorer', v['roles']); self.assertEqual(pref['schema_version'], 1)
        for model in ('gpt-5.6-terra', 'gpt-5.6-luna'):
            q = self.request(); q['preferences'] = {'schema_version': 2, 'policy': 'adaptive', 'parent_policy': 'mode-adaptive', 'active_mode': 'balanced', 'roles': {'feature': {'preferred_models': [model], 'effort_hint': 'medium'}}}
            x = r.resolve(q); self.assertEqual(x['status'], 'blocked'); self.assertTrue(x['rejected'])
            self.assertEqual(x['rejected'][0]['candidate']['model'], model)

    def test_atomic_default_migration_and_preservation(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)/'forge.json'; p.write_text(json.dumps({'schema_version': 2, 'policy': 'adaptive', 'parent_policy': 'mode-adaptive', 'active_mode': 'sprint', 'roles': {}})); before = p.read_bytes()
            x = r.set_mode(p, 'economy'); self.assertEqual(Path(x['backup']).read_bytes(), before); self.assertEqual(json.loads(p.read_text())['schema_version'], 3)
            with self.assertRaises(ValueError): r.set_mode(p, 'default')
            r.set_mode(p, 'default', {'model': 'gpt-6-sol', 'effort': 'Extra High'})
            self.assertEqual(json.loads(p.read_text())['default_profile']['effort'], 'xhigh'); self.assertEqual(r.set_mode(p, 'default')['status'], 'unchanged')
            p.write_text('{bad'); before = p.read_bytes()
            with self.assertRaises(ValueError): r.set_mode(p, 'peak')
            self.assertEqual(p.read_bytes(), before); link = Path(tmp)/'link'; link.symlink_to(p)
            with self.assertRaises(ValueError): r.set_mode(link, 'peak')

    def test_unavailable_explicit_limits_and_role_pins(self):
        q = self.request(); q['catalog'] = []; self.assertEqual(r.resolve(q)['status'], 'blocked')
        q = self.request('balanced', 'architect-runners'); q.update(candidates=[{**q['parent'], 'reason': 'judgment'}], limits={'effort': 'medium'})
        self.assertEqual(r.resolve(q)['status'], 'blocked')
        q = self.request(); q['role_config'] = {'model': 'gpt-6-astra', 'effort': 'xhigh'}; self.assertEqual(r.resolve(q)['status'], 'blocked')
        q = self.request(); q.pop('role')
        with self.assertRaises(ValueError): r.resolve(q)
        for value in ({}, [], False, 0, '', None, {'model': [], 'effort': 'high'}):
            with self.assertRaises(ValueError): r.resolve({**self.request('default'), 'default_profile': value})

    def test_lower_implementation_and_consequential_flag(self):
        with self.qualified_fixture('refactoring', executable=True) as proof:
            q = self.request('balanced', 'refactoring'); q['candidates'] = [{**{k: proof[k] for k in ('model', 'effort')}, 'reason': 'tested routine implementation'}]
            self.assertEqual(r.resolve(q)['status'], 'ready')
            q['consequential'] = True; self.assertEqual(r.resolve(q)['status'], 'blocked')
            q.pop('candidates'); self.assertEqual(r.resolve(q)['expected_from_config']['model'], q['parent']['model'])
        for flag in ('consequential', 'implementation'):
            with self.assertRaises(ValueError): r.resolve({**self.request(), flag: 'false'})

    def test_qualified_consequential_default_can_reduce_reasoning_only(self):
        role = 'acceptance-auditor'; previous = r.ROLE_PROFILES['balanced'][role]
        try:
            with self.qualified_fixture(role, 'gpt-6-sol', 'high'):
                r.ROLE_PROFILES['balanced'][role] = {'model': 'gpt-6-sol', 'effort': 'high'}
                self.assertEqual(r.resolve(self.request('balanced', role))['expected_from_config'], r.ROLE_PROFILES['balanced'][role])
                q = self.request('balanced', role); q.update(consequential=False, candidates=[dict(model='gpt-6-luna', effort='low', reason='cheap')])
                self.assertEqual(r.resolve(q)['status'], 'blocked')
        finally:
            r.ROLE_PROFILES['balanced'][role] = previous

    def test_hard_inheritance_and_cross_family_consultant(self):
        for mode in r.ROUTING_CATALOG['parent_targets']:
            for role in ('hillclimb', 'hardest-tasks'):
                q = self.request(mode, role); x = r.resolve(q)
                self.assertEqual(x['expected_from_config'], q['parent']); self.assertFalse(x['exception_applied'])
        for mode in ('lean', 'economy'):
            with self.qualified_fixture('hardest-tasks', 'gpt-6-sol', 'max', True, mode) as ex:
                q = self.request(mode, 'hardest-tasks'); q.update(candidates=[dict(model=ex['model'], effort=ex['effort'], reason='bounded consultant')], difficult_task=True, exception_reason='Concurrent retry requirement not met', exception_evidence_id=ex['evidence_id'])
                self.assertTrue(r.resolve(q)['exception_applied'])
                q['limits'] = {'model': q['parent']['model']}; self.assertEqual(r.resolve(q)['status'], 'blocked')
        q = self.request('economy', 'hardest-tasks'); q['parent'] = {'model': 'gpt-6-astra', 'effort': 'ultra'}
        q['parent_fallback'] = {'mode': 'economy', 'desired': r.ROUTING_CATALOG['parent_targets']['economy'], 'actual': q['parent'], 'accepted': True}
        self.assertEqual(r.resolve(q)['status'], 'blocked')

    def test_unqualified_max_ultra_cannot_escalate(self):
        for level in ('max', 'ultra'):
            q = self.request('peak', 'hardest-tasks'); q.update(candidates=[dict(model='gpt-6-astra', effort=level, reason='hard')], difficult_task=True, exception_evidence_id='made-up', exception_reason='harder')
            self.assertEqual(r.resolve(q)['status'], 'blocked')

    def test_desired_parent_is_not_an_unqualified_fallback_escape(self):
        original = copy.deepcopy(r.ROUTING_CATALOG['qualified_profiles']['feature'])
        try:
            r.ROUTING_CATALOG['qualified_profiles']['feature'] = []
            q = self.request(); desired = q['parent']; q['parent'] = {'model': 'gpt-6-astra', 'effort': 'xhigh'}
            q['parent_fallback'] = {'mode': 'balanced', 'desired': desired, 'actual': q['parent'], 'accepted': True}
            q['candidates'] = [{**desired, 'reason': 'desired profile'}]
            self.assertEqual(r.resolve(q)['status'], 'blocked')
            q = self.request(); q['candidates'] = [{**q['parent'], 'reason': 'disclosed parent fallback'}]
            x = r.resolve(q); self.assertEqual(x['status'], 'ready'); self.assertEqual(x['quality_status'], 'parent-profile-provisional')
        finally:
            r.ROUTING_CATALOG['qualified_profiles']['feature'] = original

    def test_native_pin_is_not_lower_family_or_coding_qualification(self):
        q = self.request('balanced', 'goal-scout'); q.update(goalbuddy_required=True, role_config={'effort': 'low'}, candidates=[dict(model='gpt-6-luna', effort='low', reason='cheaper')])
        self.assertEqual(r.resolve(q)['status'], 'blocked')
        q.pop('candidates'); self.assertEqual(r.resolve(q)['status'], 'ready')
        q['implementation'] = True; self.assertEqual(r.resolve(q)['status'], 'blocked')

    def test_review_support_and_decision_separation(self):
        for mode in r.ROUTING_CATALOG['parent_targets']:
            for role in r.ROUTING_CATALOG['review_support_roles']:
                q = self.request(mode, role); x = r.resolve(q)
                self.assertEqual(x['status'], 'ready'); self.assertIn(x['expected_from_config']['model'], r.ROUTING_CATALOG['review_support_models'])
                for flag in ('implementation', 'consequential'): self.assertEqual(r.resolve({**q, flag: True})['status'], 'blocked')
                q['candidates'] = [{**q['parent'], 'reason': 'monitor'}]
                if mode != 'economy': self.assertEqual(r.resolve(q)['status'], 'blocked')
        for mode in r.ROUTING_CATALOG['review_separation_modes']:
            for role in r.ROUTING_CATALOG['review_decision_roles']:
                q = self.request(mode, role); x = r.resolve(q); self.assertEqual(x['status'], 'ready')
                self.assertGreaterEqual(r.MODEL_RANK[x['expected_from_config']['model']], r.MODEL_RANK[r.ROUTING_CATALOG['review_decision_minimum_model']])
                q['candidates'] = [dict(model='gpt-6-luna', effort='low', reason='cheap')]
                self.assertEqual(r.resolve(q)['status'], 'blocked')

    def test_review_phase_respects_default_caps_and_missing_profiles(self):
        for role in ('status-monitor', 'findings-consolidator', 'scope-reviewer'):
            q = self.request('default', role); self.assertEqual(r.resolve(q)['expected_from_config'], q['parent'])
        q = self.request('balanced', 'status-monitor'); q['catalog'] = [x for x in q['catalog'] if x['model'] != 'gpt-6-luna']
        self.assertEqual(r.resolve(q)['status'], 'blocked')
        q = self.request('balanced', 'scope-reviewer'); q['limits'] = {'model': 'gpt-6-luna'}; self.assertEqual(r.resolve(q)['status'], 'blocked')

    def test_arrangements_preserve_actual_function_without_blanket_profile(self):
        for mode, mapping in r.role_map().items():
            self.assertEqual(len(mapping), 45)
            for wrapper in ('swarm-workers', 'arena-runners'):
                self.assertEqual(mapping[wrapper], {'assignment_role_required': True})
                q = self.request(mode, wrapper); self.assertEqual(r.resolve(q)['status'], 'assignment-required')
                for role in ('how-explorer', 'refactoring', 'correctness-reviewer'):
                    q['assignment_role'] = role
                    actual = r.resolve(q); direct = r.resolve(self.request(mode, role))
                    self.assertEqual(actual['status'], direct['status']); self.assertEqual(actual.get('expected_from_config'), direct.get('expected_from_config')); self.assertEqual(actual['role'], role)
                q['assignment_role'] = wrapper; self.assertEqual(r.resolve(q)['status'], 'assignment-required')

    def test_no_mode_preserves_legacy_but_enforces_declared_work(self):
        q = self.request(None, 'feature')
        q['parent'] = {'model': 'gpt-6-astra', 'effort': 'xhigh'}
        candidate = {'model': 'gpt-5.6-sol', 'effort': 'high', 'reason': 'bounded implementation'}
        q['candidates'] = [candidate]
        legacy = {k: v for k, v in q.items() if k not in ('role', 'evidence_contract')}
        self.assertEqual(r.resolve(legacy)['quality_status'], 'alternate-profile-provisional')
        legacy.pop('candidates')
        self.assertEqual(r.resolve(legacy)['quality_status'], 'parent-profile-provisional')
        with self.qualified_fixture('feature', 'gpt-5.6-sol', 'high', executable=True):
            q['implementation'] = True
            self.assertEqual(r.resolve(q)['status'], 'ready')
            for contract in (None, 'note-editor-ui'):
                self.assertEqual(r.resolve({**q, 'evidence_contract': contract})['status'], 'blocked')
        q = self.request(None, 'acceptance-auditor')
        q['parent'] = {'model': 'gpt-6-astra', 'effort': 'xhigh'}
        q['candidates'] = [{'model': 'gpt-6-luna', 'effort': 'medium', 'reason': 'cheap'}]
        self.assertEqual(r.resolve(q)['status'], 'blocked')
        q['role'] = 'goal-scout'
        q.update(goalbuddy_required=True, role_config={'effort': 'low'})
        q['candidates'] = [{'model': 'gpt-6-astra', 'effort': 'low', 'reason': 'native observed pin'}]
        self.assertEqual(r.resolve(q)['quality_status'], 'native-contract')
        q['candidates'][0]['model'] = 'gpt-6-luna'
        self.assertEqual(r.resolve(q)['status'], 'blocked')

    def test_unresolved_arrangement_cli_fails(self):
        for role in ('swarm-workers', 'arena-runners'):
            result = subprocess.run([sys.executable, r.__file__],
                                    input=json.dumps(self.request(role=role)),
                                    text=True, capture_output=True)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(json.loads(result.stdout)['status'], 'assignment-required')

    def test_architectural_critics_cannot_opt_out(self):
        q = self.request('balanced', 'how-critics'); q['consequential'] = False
        x = r.resolve(q); self.assertTrue(x['consequential']); self.assertEqual(x['expected_from_config']['model'], q['parent']['model'])
        q['candidates'] = [dict(model='gpt-6-luna', effort='low', reason='cheap')]; self.assertEqual(r.resolve(q)['status'], 'blocked')

    def test_fixture_scope_is_not_general_quality(self):
        x = r.resolve(self.request('balanced', 'ui-designer'))
        self.assertTrue(x['task_fit_required']); self.assertIn('not general role competence', x['qualification_scope'])
        self.assertNotEqual(x['expected_from_config']['model'], 'gpt-6-luna')
