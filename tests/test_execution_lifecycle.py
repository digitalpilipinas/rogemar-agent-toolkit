import copy
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'plugins/rogemar-agent-toolkit/skills'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


E = load('boundary_tests', SKILLS / 'workflow-orchestrator/scripts/execution_boundary.py')
L = E.lifecycle
KNOWLEDGE = SKILLS / 'engineering-playbooks/scripts/knowledge_checks.py'
if KNOWLEDGE.exists():
    K = load('knowledge_runtime_tests', KNOWLEDGE)
NOW = datetime(2026, 9, 28, tzinfo=timezone.utc)


def identity():
    base = dict(capability='edit', environment='fixture-host', task_types=['maintenance'],
                actions=['write'], limits={'operations': 2})
    q = dict(base, schema_version=1, id='qualification-1', state='qualified', versions={'adapter': '1'},
             valid_until='2027-01-01T00:00:00Z', evidence=[dict(reference='fixture-trial', outcome='passed', task_type='maintenance')])
    grant = dict(base, state='active', reference='fixture-owner-grant', expires_at='2027-01-01T00:00:00Z')
    task = dict(schema_version=1, capability='edit', environment='fixture-host', versions={'adapter': '1'},
                task_type='maintenance', actions=['write'], budget={'operations': 1})
    return q, task, grant


class ExecutionLifecycleTests(unittest.TestCase):
    def test_qualification_requires_live_matching_scope_versions_grant(self):
        q, task, grant = identity()
        self.assertFalse(L.qualification(q, task, grant, now=NOW)['grants_new_authority'])
        for target, field, value in [(q, 'state', 'revoked'), (task, 'environment', 'other'),
                                     (task, 'versions', {'adapter': '2'}), (grant, 'state', 'revoked'),
                                     (task, 'actions', ['publish'])]:
            old = target[field]
            target[field] = value
            with self.assertRaises(ValueError): L.qualification(q, task, grant, now=NOW)
            target[field] = old

    def test_action_boundary_rejects_replay_changed_target_and_exhausted_budget(self):
        q, task, grant = identity()
        action = dict(operation_id='one', tool='write', connection='fixture', requester='owner', target='file', arguments={'text': 'one'})
        digest = E.contracts.action_digest(action)
        def authenticate(_):
            return dict(qualification=q, task=task, grant=grant,
                        approval=dict(approval_id='owner-decision', action_sha256=digest, expires_at='2027-01-01T00:00:00Z'))
        with tempfile.TemporaryDirectory() as folder:
            calls = []
            def write(value):
                calls.append(value)
                Path(folder, 'output').write_text(value['arguments']['text'])
                return 'written'
            boundary = E.ActionBoundary(Path(folder, 'host.sqlite'), authenticate, {'write': write})
            changed = dict(action, target='elsewhere')
            with self.assertRaises(ValueError): boundary.execute(changed, now=NOW)
            self.assertEqual(boundary.execute(action, now=NOW), 'written')
            with self.assertRaises(ValueError): boundary.execute(action, now=NOW)
            action['operation_id'] = 'two'; digest = E.contracts.action_digest(action)
            boundary.execute(action, now=NOW)
            action['operation_id'] = 'three'; digest = E.contracts.action_digest(action)
            with self.assertRaises(ValueError): boundary.execute(action, now=NOW)
            self.assertEqual(len(calls), 2)
            self.assertEqual(Path(folder, 'output').read_text(), 'one')

    def test_uncertain_outcome_is_not_retried(self):
        q, task, grant = identity()
        action = dict(operation_id='one', tool='write', connection='fixture', requester='owner', target='file', arguments={})
        trusted = dict(qualification=q, task=task, grant=grant, approval=dict(approval_id='decision',
                       action_sha256=E.contracts.action_digest(action), expires_at='2027-01-01T00:00:00Z'))
        calls = []
        def interrupted(_):
            calls.append('side-effect')
            raise RuntimeError('lost acknowledgement')
        with tempfile.TemporaryDirectory() as folder:
            boundary = E.ActionBoundary(Path(folder, 'host.sqlite'), lambda _: trusted, {'write': interrupted})
            with self.assertRaises(RuntimeError): boundary.execute(action, now=NOW)
            recovered = E.ActionBoundary(Path(folder, 'host.sqlite'), lambda _: trusted, {'write': interrupted})
            with self.assertRaises(ValueError): recovered.execute(action, now=NOW)
            self.assertEqual(calls, ['side-effect'])

    def test_assignment_dependencies_completion_and_invalidation(self):
        task = dict(owner='one', acceptance='verified output', state='pending')
        record = dict(schema_version=1, candidate='tree-1', assignments=[dict(task, id='a'), dict(task, id='b', depends_on=['a'])])
        with self.assertRaises(ValueError): E.transition(record, 'b', 'running')
        record = E.transition(record, 'a', 'running')
        with self.assertRaises(ValueError): E.transition(record, 'a', 'passed')
        record = E.transition(record, 'a', 'passed', evidence='run-1')
        record = E.transition(record, 'b', 'running')
        record = E.transition(record, 'b', 'passed', evidence='run-2')
        reset = E.invalidate(record, ['a'])
        self.assertEqual([x['state'] for x in reset['assignments']], ['pending', 'pending'])

    def test_controlled_update_actual_sequence_tamper_failed_pilot_and_rollback(self):
        source = dict(uri='https://example.invalid/source', version='1', sha256='a' * 64)
        record = dict(schema_version=1, id='update-1', state='detected', source=source)
        proposal = dict(affected_paths=['skill.md'], expected_benefit='clear routing', acceptance='route passes', rollback='previous tree')
        record = L.advance_update(record, dict(action='assess', applicable=True, conflicts=[], rationale='relevant', proposal=proposal), source)
        tampered = copy.deepcopy(record); tampered['proposal']['affected_paths'] = ['other']
        checks = [dict(kind=k, state='passed', reference='fixture-' + k) for k in ('regression', 'qualification')]
        with self.assertRaises(ValueError): L.advance_update(tampered, dict(action='qualify', checks=checks), source)
        record = L.advance_update(record, dict(action='qualify', checks=checks), source)
        decision = dict(reference='fixture-owner', proposal_sha256=record['proposal_sha256'], decision='approve')
        record = L.advance_update(record, dict(action='approve'), source, owner_decision=decision)
        pilot = dict(action='pilot', passed=False, reference='fixture-pilot', proposal_sha256=record['proposal_sha256'])
        failed = L.advance_update(record, pilot, source)
        with self.assertRaises(ValueError): L.advance_update(failed, dict(action='promote'), source)
        pilot['passed'] = True
        record = L.advance_update(record, pilot, source)
        record = L.advance_update(record, dict(action='promote', reference='observed-fixture-promotion', rollback_reference='previous-tree', proposal_sha256=record['proposal_sha256']), source)
        self.assertEqual(L.advance_update(record, dict(action='rollback', reference='observed-fixture-rollback'), source)['state'], 'rolled-back')
        self.assertEqual(L.detect_update(source, source, [record])['status'], 'already-considered')

    def test_measures_unknown_is_not_zero_and_attempts_are_not_completed(self):
        rows = [dict(task_id='a', version='v1', eligible=True, verified_success=True, prohibited_attempts=1,
                     prohibited_blocked=1, unauthorized_completed=0, costs={'tokens': 25}),
                dict(task_id='b', version='v1', eligible=True)]
        value = L.measures(rows)
        self.assertEqual(value['metrics']['verified_success']['missing_tasks'], 1)
        self.assertIsNone(value['metrics']['recurring_defect']['total'])
        self.assertEqual(value['metrics']['unauthorized_completed']['total'], 0)
        with self.assertRaises(ValueError): L.measures(rows + [rows[0]])

    @unittest.skipUnless(KNOWLEDGE.exists(), 'Optional knowledge distribution absent')
    def test_live_revocation_staleness_and_transitive_removal(self):
        record = json.loads((SKILLS / 'engineering-playbooks/playbooks/knowledge-metadata-example.json').read_text())
        record['sources'][0]['available'] = True
        page = record['pages'][0]
        record['pages'].append(dict(page, id='derived', sources=[], depends_on=[page['id']]))
        live = dict(available=True, allowed=True, revision='example-revision')
        with tempfile.TemporaryDirectory() as folder:
            blocked, reads = set(), []
            for ident in ['source-a', page['id'], 'derived']:
                Path(folder, ident).write_text('fixture content')
            def read(ident, _):
                reads.append(ident)
                return Path(folder, ident).read_text()
            def query():
                return K.query_page(record, 'derived', 'owner', observe_source=lambda *_: live,
                                    authorize_page=lambda ident, _: ident not in blocked, read_page=read)
            self.assertEqual(query()['content'], 'fixture content')
            live['allowed'] = False
            with self.assertRaises(ValueError): query()
            live.update(allowed=True, revision='new')
            with self.assertRaises(ValueError): query()
            self.assertEqual(reads, ['derived'])
            def block(ids): blocked.update(ids); return True
            def erase(ident):
                Path(folder, ident).unlink(missing_ok=True)
                return 'fixture-erasure:' + ident
            self.assertEqual(len(K.remove_source(record, 'source-a', block=block, erase=erase)['receipts']), 3)
            with self.assertRaises(ValueError): query()
            self.assertFalse(list(Path(folder).iterdir()))
