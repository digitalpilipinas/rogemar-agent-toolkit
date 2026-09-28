"""Synthetic regression tests for the alignment helpers, not live harness trials."""
import copy
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'plugins/rogemar-agent-toolkit/skills'


def load(name, path):
    if not path.is_file():
        catalog_path = ROOT / 'catalog/skills.yaml'
        if catalog_path.is_file():
            catalog = json.loads(catalog_path.read_text())
            selected = {entry['name'] for entry in catalog['vendored']}
            owner = path.relative_to(SKILLS).parts[0]
            if 'distribution_selection' in catalog['package'] and owner not in selected:
                return None  # Deliberately unselected optional pack, not a missing required file.
        raise FileNotFoundError('Required helper is missing: ' + str(path))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


W = load('alignment_workflow', SKILLS / 'workflow-orchestrator/scripts/workflow_contracts.py')
L = load('alignment_learning', SKILLS / 'project-learning/scripts/lifecycle_metadata.py')
E = load('alignment_execution', SKILLS / 'integrated-workflow/scripts/execution_provenance.py')
K = load('alignment_knowledge', SKILLS / 'engineering-playbooks/scripts/knowledge_checks.py')


def task(ident, deps=(), state='pending', writes=(), workspace='isolated-a'):
    return dict(id=ident, owner='fixture-owner', acceptance='observable fixture outcome',
                state=state, depends_on=list(deps), writes=list(writes), workspace=workspace,
                exclusive_resources=[], candidate='fixture-candidate', evidence=['fixture-test'])


def plan(*tasks):
    return dict(schema_version=1, candidate='fixture-candidate', assignments=list(tasks))


def lifecycle():
    return dict(schema_version=1, activity='active', verified_at='2026-09-28T00:00:00Z',
                source_versions={'source-a': 'revision-1'}, evidence_roots=['root-a'],
                review_trigger='Source revision changes', failure_class='implementation',
                counterexamples=['Source belongs to another project'])


def knowledge():
    src = dict(id='source-a', revision='v1', namespace='project-a', root_id='root-a',
               locator='docs/reference.md#contract', available=True, audience=['owner'])
    a = dict(id='page-a', kind='summary', namespace='project-a', audience=['owner'],
             sources=[dict(id='source-a', revision='v1')], depends_on=[], evidence_roots=['root-a'], links=['page-b'])
    b = dict(id='page-b', kind='comparison', namespace='project-a', audience=['owner'],
             sources=[], depends_on=['page-a'], evidence_roots=['root-a'], links=['page-a'])
    return dict(schema_version=1, sources=[src], pages=[a, b])


@unittest.skipUnless(W is not None, 'Owning optional skill is absent from this selected distribution')
class InputTests(unittest.TestCase):
    def test_strict_json_accepts_valid(self):
        self.assertEqual(W.read_json(b'{"x": [1, 2]}'), {'x': [1, 2]})

    def test_rejects_duplicate_nonfinite_and_surrogates(self):
        for raw in (b'{"x":1,"x":2}', b'NaN', b'1e999', b'{"\\ud800":1}', b'"\\ud800"'):
            with self.subTest(raw=raw), self.assertRaises(W.ContractError):
                W.read_json(raw)

    def test_input_limits(self):
        for raw in (b' ' * (W.MAX_BYTES + 1), b'[' * 40 + b'0' + b']' * 40):
            with self.assertRaises(W.ContractError):
                W.read_json(raw)

    def test_paths_reject_escaping_and_globs(self):
        for value in ('../a', '/a', '.', 'a/./b', '.git/config', 'a\\b', 'a/*', 'a:b'):
            with self.subTest(value=value), self.assertRaises(W.ContractError):
                W.relative_path(value)

    def test_portable_overlap(self):
        self.assertTrue(W.overlap('src/API', 'src/api/file.py'))
        self.assertFalse(W.overlap('src/api', 'src/apis/file.py'))


@unittest.skipUnless(W is not None, 'Owning optional skill is absent from this selected distribution')
class AssignmentTests(unittest.TestCase):
    def test_sequential_and_parallel_valid(self):
        p = plan(task('a', state='passed'), task('b', ['a'], 'running', ['src/b.py']),
                 task('c', ['a'], 'running', ['src/c.py'], 'isolated-c'))
        self.assertEqual(W.validate_assignments(p)['order'], ['a', 'b', 'c'])

    def test_unknown_and_self_dependency(self):
        for dep in ('missing', 'a'):
            with self.assertRaises(W.ContractError):
                W.validate_assignments(plan(task('a', [dep])))

    def test_cycle(self):
        with self.assertRaisesRegex(W.ContractError, 'cycle'):
            W.validate_assignments(plan(task('a', ['b']), task('b', ['a'])))

    def test_running_and_passed_need_passed_prerequisites(self):
        for state in ('running', 'passed'):
            with self.assertRaises(W.ContractError):
                W.validate_assignments(plan(task('a', state='failed'), task('b', ['a'], state)))

    def test_stale_or_empty_passed_evidence(self):
        for change in ({'candidate': 'old'}, {'evidence': []}):
            t = task('a', state='passed'); t.update(change)
            with self.assertRaises(W.ContractError):
                W.validate_assignments(plan(t))

    def test_conflicting_writers(self):
        variants = [(['a.py'], ['b.py'], 'same', 'same'),
                    (['src'], ['src/b.py'], 'a', 'b')]
        for a, b, wa, wb in variants:
            with self.assertRaises(W.ContractError):
                W.validate_assignments(plan(task('a', state='running', writes=a, workspace=wa),
                                             task('b', state='running', writes=b, workspace=wb)))

    def test_shared_resources_even_read_only_workers(self):
        a, b = task('a', state='running'), task('b', state='running')
        a['exclusive_resources'] = b['exclusive_resources'] = ['fixture-database']
        with self.assertRaisesRegex(W.ContractError, 'resource'):
            W.validate_assignments(plan(a, b))

    def test_downstream_invalidation_only(self):
        p = plan(task('a', state='passed'), task('b', ['a'], 'passed'), task('c', state='passed'),
                 task('d', ['b'], 'passed'))
        self.assertEqual(W.affected_assignments(p, ['a']), ['a', 'b', 'd'])
        self.assertEqual(W.affected_assignments(p, ['c']), ['c'])

    def test_duplicate_identity_and_bool_version(self):
        with self.assertRaises(W.ContractError): W.validate_assignments(plan(task('a'), task('a')))
        p = plan(); p['schema_version'] = True
        with self.assertRaises(W.ContractError): W.validate_assignments(p)


@unittest.skipUnless(W is not None, 'Owning optional skill is absent from this selected distribution')
class InteractionTests(unittest.TestCase):
    def test_correction_eligible_but_no_permission(self):
        out = W.retry_decision(dict(attempts_used=1, attempt_limit=4, failure_kind='implementation'))
        self.assertEqual(out['decision'], 'eligible-for-scoped-correction')
        self.assertFalse(out['grants_authority'])

    def test_authority_never_retry(self):
        out = W.retry_decision(dict(attempts_used=0, attempt_limit=4, failure_kind='authority'))
        self.assertEqual(out['decision'], 'resolve-authority-no-retry')

    def test_cancellation_and_budget(self):
        base = dict(attempts_used=0, attempt_limit=3, failure_kind='implementation')
        self.assertEqual(W.retry_decision(dict(base, cancelled=True))['decision'], 'stop-and-preserve')
        self.assertEqual(W.retry_decision(dict(base, other_budget_exhausted=True))['decision'], 'budget-exhausted-reclassify')
        base['attempts_used'] = 3
        self.assertEqual(W.retry_decision(base)['decision'], 'budget-exhausted-reclassify')

    def test_nonimplementation_failure_requires_diagnosis(self):
        for kind in ('environment', 'verifier', 'context', 'routing', 'unknown'):
            self.assertEqual(W.retry_decision(dict(attempts_used=0, attempt_limit=3, failure_kind=kind))['decision'],
                             'diagnose-before-retry')

    def test_prompt_modes_and_continuation(self):
        self.assertEqual(W.framing_decision({'mode': 'prompt-only', 'approved_continuation': True})['decision'], 'produce-prompt-only')
        self.assertEqual(W.framing_decision({'mode': 'review-first'})['decision'], 'present-one-prompt-and-wait')
        self.assertEqual(W.framing_decision({'mode': 'review-first', 'approved_continuation': True})['decision'], 'continue-within-existing-authority')
        self.assertEqual(W.framing_decision({})['decision'], 'frame-proportionately-without-new-approval')
        self.assertEqual(W.framing_decision({'mode': 'direct', 'material_gap': True})['decision'], 'resolve-material-gap')

    def test_string_false_cannot_bypass(self):
        with self.assertRaises(W.ContractError): W.framing_decision({'approved_continuation': 'false'})
        with self.assertRaises(W.ContractError): W.retry_decision({'attempts_used': True, 'attempt_limit': 3, 'failure_kind': 'implementation'})


@unittest.skipUnless(W is not None, 'Owning optional skill is absent from this selected distribution')
class ActionTests(unittest.TestCase):
    def setUp(self):
        self.action = dict(operation_id='fixture-1', tool='write', connection='fixture-connection',
                           requester='fixture-user', target='fixture-resource', arguments={'value': 1})
        self.approval = dict(action_sha256=W.action_digest(self.action), approval_id='fixture-approval',
                             expires_at='2026-09-29T00:00:00Z')
        self.now = datetime(2026, 9, 28, tzinfo=timezone.utc)

    def check(self):
        return W.check_action_binding(self.action, self.approval, now=self.now, used_operation_ids=set())

    def test_matching_object_is_not_authorization(self):
        self.assertEqual(self.check()['status'], 'binding-matches')
        self.assertFalse(self.check()['grants_authority'])

    def test_every_binding_field_matters(self):
        for key in self.action:
            action = copy.deepcopy(self.action)
            action[key] = {'value': 2} if key == 'arguments' else 'changed'
            with self.subTest(key=key), self.assertRaises(W.ContractError):
                W.check_action_binding(action, self.approval, now=self.now, used_operation_ids=set())

    def test_expiry_replay_and_timezone(self):
        with self.assertRaises(W.ContractError):
            W.check_action_binding(self.action, self.approval, now=self.now, used_operation_ids={'fixture-1'})
        self.approval['expires_at'] = '2026-09-28T00:00:00Z'
        with self.assertRaises(W.ContractError): self.check()
        self.approval['expires_at'] = '2026-09-29T00:00:00'
        with self.assertRaises(W.ContractError): self.check()

    def test_extra_field_and_nonfinite_are_not_silently_dropped(self):
        self.action['trusted'] = True
        with self.assertRaises(W.ContractError): W.action_digest(self.action)
        del self.action['trusted']; self.action['arguments']['value'] = float('inf')
        with self.assertRaises(W.ContractError): W.action_digest(self.action)


@unittest.skipUnless(L is not None, 'Owning optional skill is absent from this selected distribution')
class LearningTests(unittest.TestCase):
    def test_combined_metadata_cannot_exceed_reader_bound(self):
        value = lifecycle()
        value['source_versions'] = {f'source-{i}': 'v'*700 for i in range(50)}
        value['evidence_roots'] = [f'{i:02d}' + 'e'*698 for i in range(50)]
        value['counterexamples'] = [f'{i:02d}' + 'c'*698 for i in range(50)]
        with self.assertRaisesRegex(L.LifecycleError, 'ledger line bounds'):
            L.validate_lifecycle(value)

    def test_activity_is_not_approval(self):
        out = L.assess_lifecycle(lifecycle(), {'source-a': 'revision-1'}, accepted=False)
        self.assertFalse(out['eligible_for_source_review'])
        self.assertEqual(out['freshness'], 'matches-recorded-versions')

    def test_stale_missing_and_quarantine(self):
        for current, expected in (({'source-a': 'revision-2'}, 'stale'), ({}, 'unverified')):
            out = L.assess_lifecycle(lifecycle(), current, accepted=True)
            self.assertEqual(out['freshness'], expected)
            self.assertFalse(out['eligible_for_source_review'])
        value = lifecycle(); value['activity'] = 'quarantined'
        self.assertFalse(L.assess_lifecycle(value, {'source-a': 'revision-1'}, accepted=True)['eligible_for_source_review'])

    def test_legacy_ledger_preserved(self):
        self.assertTrue(L.section_active('Status: Accepted\nLesson: Fixture.\n'))

    def test_metadata_does_not_autoverify(self):
        value = lifecycle(); value['verified_at'] = None
        self.assertEqual(L.assess_lifecycle(value, {'source-a': 'revision-1'}, accepted=True)['freshness'], 'unverified')
        self.assertIsNone(value['verified_at'])

    def test_duplicate_evidence_roots_rejected(self):
        value = lifecycle(); value['evidence_roots'] = ['a', 'a']
        with self.assertRaises(L.LifecycleError): L.validate_lifecycle(value)

    def test_unknown_fields_and_control_text_rejected(self):
        value = lifecycle(); value['usedRawTranscript'] = True
        with self.assertRaises(L.LifecycleError): L.validate_lifecycle(value)
        value = lifecycle(); value['review_trigger'] = '\u202eunsafe'
        with self.assertRaises(L.LifecycleError): L.validate_lifecycle(value)

    def test_duplicate_or_empty_lifecycle_line_rejected(self):
        for section in ('Lifecycle: \n', 'Lifecycle: {}\nLifecycle: {}\n',
                        'Lifecycle: {"schema_version":1,"schema_version":1}\n'):
            with self.assertRaises(L.LifecycleError): L.section_lifecycle(section)

    def test_update_is_exact_and_preserves_other_sections(self):
        ledger = '# Lessons\n\n## PL-123456789ABC\n\nStatus: Accepted\nLesson: Preserve fixture.\n\n## PL-ABCDEF123456\nStatus: Accepted\nLesson: Other.\n'
        value = lifecycle(); value['activity'] = 'retired'
        updated = L.replace_lifecycle(ledger, 'PL-123456789ABC', value, hashlib.sha256(ledger.encode()).hexdigest())
        self.assertIn('Lesson: Preserve fixture.', updated)
        self.assertEqual(updated.split('## PL-ABCDEF123456')[1], ledger.split('## PL-ABCDEF123456')[1])
        self.assertIn('"activity":"retired"', updated)
        self.assertNotIn('Lifecycle:', ledger)

    def test_stale_unknown_and_nonaccepted_updates_rejected(self):
        ledger = '## PL-123456789ABC\nStatus: Superseded\n'
        with self.assertRaises(L.LifecycleError): L.replace_lifecycle(ledger, 'PL-123456789ABC', lifecycle(), '0' * 64)
        with self.assertRaises(L.LifecycleError): L.replace_lifecycle(ledger, 'PL-123456789ABC', lifecycle(), hashlib.sha256(ledger.encode()).hexdigest())


@unittest.skipUnless(E is not None, 'Owning optional skill is absent from this selected distribution')
class ExecutionTests(unittest.TestCase):
    def setUp(self):
        self.candidate = {'base': 'fixture-base', 'head': 'fixture-head', 'content': 'fixture-content'}
        self.gate = {'gate': 'test:web', 'candidate': self.candidate, 'evidence': [{'sha256': 'a' * 64}]}
        self.obs = dict(schema_version=1, gate='test:web', candidate=self.candidate, runner='fixture-runner',
                        check_id='fixture-check', environment_sha256='b' * 64, run_id='fixture-run',
                        exit_code=0, tests_executed=3, required_checks_complete=True, artifact_hashes=['a' * 64])

    def check(self, obs=None, known_hash=None):
        raw = json.dumps(self.obs if obs is None else obs, sort_keys=True).encode()
        req = dict(observation_sha256=known_hash or hashlib.sha256(raw).hexdigest(), runner='fixture-runner',
                   check_id='fixture-check', environment_sha256='b' * 64)
        return E.validate_execution(self.gate, self.candidate, req, raw)

    def test_matching_independent_observation(self):
        self.assertEqual(self.check()['status'], 'matches-protected-observation')

    def test_forged_observation_does_not_match_protected_digest(self):
        with self.assertRaises(E.ProvenanceError): self.check(known_hash='0' * 64)

    def test_outcome_mutations_rejected_even_with_new_digest(self):
        for key, value in [('candidate', {'head': 'old'}), ('runner', 'pretend'), ('check_id', 'other'),
                           ('environment_sha256', 'c' * 64), ('exit_code', 1), ('exit_code', False),
                           ('tests_executed', 0), ('required_checks_complete', False), ('artifact_hashes', []),
                           ('run_id', '')]:
            observed = copy.deepcopy(self.obs); observed[key] = value
            with self.subTest(key=key), self.assertRaises(E.ProvenanceError): self.check(observed)

    def test_boolean_schema_and_extra_trust_fields_rejected(self):
        observed = dict(self.obs, schema_version=True)
        with self.assertRaises(E.ProvenanceError): self.check(observed)
        observed = dict(self.obs, trusted=True)
        with self.assertRaises(E.ProvenanceError): self.check(observed)

    def test_duplicate_json_rejected(self):
        raw = b'{"gate":"x","gate":"y"}'
        req = dict(observation_sha256=hashlib.sha256(raw).hexdigest(), runner='r', check_id='c', environment_sha256='b' * 64)
        with self.assertRaises(E.ProvenanceError): E.validate_execution(self.gate, self.candidate, req, raw)


@unittest.skipUnless(K is not None, 'Owning optional skill is absent from this selected distribution')
class KnowledgeTests(unittest.TestCase):
    def test_navigation_cycles_and_single_evidence_root_valid(self):
        out = K.inspect(knowledge())
        self.assertEqual(out['declared_root_counts'], {'page-a': 1, 'page-b': 1})
        self.assertFalse(out['review_required'])

    def test_changed_source_propagates_without_mutation(self):
        value = knowledge(); before = copy.deepcopy(value)
        self.assertEqual(K.inspect(value, ['source-a'])['affected_pages'], ['page-a', 'page-b'])
        self.assertEqual(value, before)

    def test_stale_and_unavailable_propagate(self):
        value = knowledge(); value['sources'][0]['revision'] = 'v2'; value['sources'][0]['available'] = False
        out = K.inspect(value)
        self.assertEqual(out['stale_pages'], ['page-a', 'page-b'])
        self.assertEqual(out['unavailable_pages'], ['page-a', 'page-b'])
        self.assertTrue(out['review_required'])

    def test_derivation_cycle_rejected(self):
        value = knowledge(); value['pages'][0]['depends_on'] = ['page-b']
        with self.assertRaises(K.KnowledgeError): K.inspect(value)

    def test_false_corroboration_root_rejected(self):
        value = knowledge(); value['pages'][1]['evidence_roots'].append('invented-root')
        with self.assertRaises(K.KnowledgeError): K.inspect(value)

    def test_private_audience_and_namespace_preserved(self):
        for field, value in [('audience', ['*']), ('namespace', 'other-project')]:
            record = knowledge(); record['pages'][1][field] = value
            with self.assertRaises(K.KnowledgeError): K.inspect(record)

    def test_public_sources_can_cross_namespace(self):
        value = knowledge(); value['sources'][0]['audience'] = ['*']; value['sources'][0]['namespace'] = 'public'
        self.assertEqual(K.inspect(value)['status'], 'metadata-valid')

    def test_policy_injection_unknown_reference_and_mixed_public_rejected(self):
        variants = [('kind', 'policy'), ('authority', 'approved'), ('links', ['absent']), ('audience', ['*', 'owner'])]
        for key, item in variants:
            record = knowledge(); record['pages'][0][key] = item
            with self.subTest(key=key), self.assertRaises(K.KnowledgeError): K.inspect(record)

    def test_duplicate_and_nonfinite_json(self):
        for raw in (b'{"a":1,"a":2}', b'Infinity', b'1e999', b'"\\ud800"'):
            with self.assertRaises((K.KnowledgeError, ValueError)): K.parse_input(raw)

    def test_cli_stale_is_two_not_pass(self):
        record = knowledge(); record['sources'][0]['available'] = False
        result = subprocess.run([sys.executable, '-B', str(SKILLS / 'engineering-playbooks/scripts/knowledge_checks.py')],
                                input=json.dumps(record), text=True, capture_output=True, timeout=5)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertTrue(json.loads(result.stdout)['review_required'])


if __name__ == '__main__':
    unittest.main()
