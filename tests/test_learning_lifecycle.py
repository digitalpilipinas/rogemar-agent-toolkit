import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
OWNER = ROOT / 'plugins/rogemar-agent-toolkit/skills/project-learning/scripts'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


if OWNER.is_dir():
    STORE = load('lifecycle_store_test', OWNER / 'candidate_store.py')
    FIXTURE = load('lifecycle_fixture_test', OWNER / 'test_project_learning.py')


@unittest.skipUnless(OWNER.is_dir(), 'Project Learning intentionally absent from this distribution')
class LearningLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.fixture = FIXTURE.ProjectLearningTest()
        self.fixture.setUp()
        self.fixture.initialize()
        # Match the CLI's canonical repository root, including macOS /var aliases.
        self.root = self.fixture.root.resolve()
        self.addCleanup(self.fixture.tearDown)

    def request(self, data, name='request.json'):
        path = self.root / '.codex/project-learning/state' / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data))
        return path

    def capture(self, data, **kwargs):
        return self.fixture.store('capture', '--request', str(self.request(data)), **kwargs)

    def test_aliases_and_derived_summaries_do_not_reinforce_one_event(self):
        raw = json.loads(self.fixture.capture_request(1).read_text())
        raw['evidence'][0]['event_id'] = 'source-run-1'
        first = json.loads(self.capture(raw).stdout)
        raw.update(session_id='cursor-session', turn_id='another-turn', harness='cursor')
        raw['evidence'][0]['reference'] = 'new-locator-for-same-event'
        self.assertEqual(json.loads(self.capture(raw).stdout)['reason'], 'duplicate')
        raw.update(turn_id='derived-turn')
        raw['evidence'][0].update(event_id='summary-1', derived_from=['source-run-1'])
        self.assertEqual(json.loads(self.capture(raw).stdout)['reason'], 'duplicate')
        raw.update(turn_id='summary-of-summary')
        raw['evidence'][0].update(event_id='summary-2', derived_from=['summary-1'])
        self.assertEqual(json.loads(self.capture(raw).stdout)['reason'], 'duplicate')
        raw.update(turn_id='independent-turn')
        raw['evidence'][0].pop('derived_from')
        raw['evidence'][0]['event_id'] = 'source-run-2'
        result = json.loads(self.capture(raw).stdout)
        self.assertEqual(result['event_type'], 'reinforced')
        self.assertEqual(result['candidate_id'], first['candidate_id'])

    def test_lifecycle_roots_override_changed_reference_aliases(self):
        one = {'lifecycle': {'evidence_roots': ['source-1']}, 'evidence': [{'kind': 'test', 'reference': 'a'}]}
        two = {'lifecycle': {'evidence_roots': ['source-1']}, 'evidence': [{'kind': 'review', 'reference': 'b'}]}
        self.assertEqual(STORE.evidence_keys(one), STORE.evidence_keys(two))

    def test_conflicting_or_circular_lineage_does_not_persist(self):
        raw = json.loads(self.fixture.capture_request(1).read_text())
        raw['project_identity'] = 'fixture-project'
        state = self.root / 'lineage-test'
        raw['evidence'][0].update(event_id='event-a')
        STORE.resolve_lineage(raw, state)
        before = (state / 'evidence-lineage.json').read_bytes()
        raw['evidence'][0].update(derived_from=['event-b'])
        with self.assertRaises(STORE.StoreError): STORE.resolve_lineage(raw, state)
        self.assertEqual((state / 'evidence-lineage.json').read_bytes(), before)
        raw['evidence'] = [{'event_id': 'cycle-a', 'derived_from': ['cycle-b']},
                           {'event_id': 'cycle-b', 'derived_from': ['cycle-a']}]
        with self.assertRaises(STORE.StoreError): STORE.resolve_lineage(raw, state)
        self.assertEqual((state / 'evidence-lineage.json').read_bytes(), before)

    def test_project_identity_is_shared_by_worktrees_but_not_same_named_repos(self):
        subprocess.run(['git', 'add', 'AGENTS.md'], cwd=self.root, check=True)
        subprocess.run(['git', '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                        'commit', '-qm', 'fixture'], cwd=self.root, check=True)
        worktree = self.root.parent / 'worktree'
        subprocess.run(['git', 'worktree', 'add', '-q', '--detach', str(worktree)], cwd=self.root, check=True)
        self.assertEqual(STORE.project_identity(self.root), STORE.project_identity(worktree))
        with tempfile.TemporaryDirectory() as other:
            same_name = Path(other) / 'repo'
            same_name.mkdir()
            subprocess.run(['git', 'init', '-q'], cwd=same_name, check=True)
            self.assertNotEqual(STORE.project_identity(self.root), STORE.project_identity(same_name))

    def promote(self, fixture, data):
        path = fixture.root / '.codex/project-learning/state/promote-input.json'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data))
        return fixture.store('promote', '--request', str(path))

    def proposal(self):
        source = FIXTURE.ProjectLearningTest()
        source.setUp()
        source.initialize()
        self.addCleanup(source.tearDown)
        source_request = source.capture_request(1)
        raw = json.loads(source_request.read_text())
        ident = json.loads(source.store('capture', '--request', str(source_request)).stdout)['candidate_id']
        self.promote(source, {'schema_version': 1, 'candidate_id': ident, 'status': 'Accepted',
                             'lesson': raw['lesson'], 'applies_when': raw['applies_when'],
                             'does_not_apply_when': raw['does_not_apply_when'], 'evidence_strength': 'verified',
                             'cross_project': 'Evaluate', 'approved_by': 'user'})
        paths = ['skills/demo/SKILL.md', 'skills/demo/reference.md']
        for name in paths:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('Before\n')
        raw.update(session_id='proposal-session', turn_id='proposal-turn',
                   source_project=source.root.name, source_lesson_id=ident,
                   proposal={'target_skill': paths[0], 'allowed_files': paths, 'validation': 'targeted behavior checks'})
        result = self.fixture.store('capture', '--request', str(self.request(raw)), '--source-root', str(source.root))
        candidate_id = json.loads(result.stdout)['candidate_id']
        stage = {'schema_version': 1, 'candidate_id': candidate_id,
                 'edits': [{'path': name, 'before_sha256': hashlib.sha256(b'Before\n').hexdigest(),
                            'after_text': 'After\n'} for name in paths],
                 'groups': {'main': [paths[0]], 'reference': [paths[1]]},
                 'validation': 'fixture verifies content, independent groups, freshness and rollback'}
        result = self.fixture.store('stage-proposal', '--request', str(self.request(stage)),
                                    '--source-root', str(source.root), '--permission-mode', 'execution')
        staged = json.loads(result.stdout)
        decision = {'schema_version': 1, 'proposal_id': staged['proposal_id'],
                    'proposal_sha256': staged['proposal_sha256'], 'groups': ['main'],
                    'owner_decision': 'synthetic owner decision for the exact main group'}
        return source, paths, decision

    def apply(self, source, decision, command='apply-proposal', **kwargs):
        return self.fixture.store(command, '--request', str(self.request(decision)),
                                  '--source-root', str(source.root), '--permission-mode', 'execution', **kwargs)

    def test_concrete_subset_apply_is_idempotent_and_rolls_back(self):
        source, paths, decision = self.proposal()
        self.apply(source, decision)
        self.assertEqual((self.root / paths[0]).read_text(), 'After\n')
        self.assertEqual((self.root / paths[1]).read_text(), 'Before\n')
        self.apply(source, decision)
        self.apply(source, decision, 'rollback-proposal')
        self.assertEqual((self.root / paths[0]).read_text(), 'Before\n')

    def test_stale_target_or_changed_approved_digest_preserves_user_work(self):
        source, paths, decision = self.proposal()
        (self.root / paths[0]).write_text('User change\n')
        self.assertNotEqual(self.apply(source, decision, check=False).returncode, 0)
        self.assertEqual((self.root / paths[0]).read_text(), 'User change\n')
        decision['proposal_sha256'] = '0' * 64
        self.assertNotEqual(self.apply(source, decision, check=False).returncode, 0)

    def test_interrupted_apply_resumes_only_known_before_after_states(self):
        source, paths, decision = self.proposal()
        decision['groups'] = ['main', 'reference']
        request = self.request(decision)
        from argparse import Namespace
        args = Namespace(command='apply-proposal', root=str(self.root), request=str(request),
                         source_root=str(source.root), permission_mode='execution', handler=STORE.apply_proposal)
        original = STORE.atomic_text
        count = 0
        def interrupted(path, content):
            nonlocal count
            count += 1
            if count == 2:
                raise OSError('synthetic interrupted write')
            original(path, content)
        with patch.object(STORE, 'atomic_text', interrupted), self.assertRaises(OSError):
            STORE.run(args)
        self.assertEqual((self.root / paths[0]).read_text(), 'After\n')
        self.assertEqual((self.root / paths[1]).read_text(), 'Before\n')
        self.apply(source, decision)
        self.assertTrue(all((self.root / name).read_text() == 'After\n' for name in paths))

    def test_read_only_proposal_does_not_read_request_or_write(self):
        result = self.fixture.store('apply-proposal', '--request', 'absent.json', '--read-only')
        self.assertEqual(json.loads(result.stdout)['reason'], 'read_only')

    def test_recall_excludes_stale_and_retired_guidance_and_is_read_only(self):
        ledger = self.root / 'docs/project-learning/lessons.md'
        config = STORE.config_for(self.root)
        ledger = STORE.project_path(self.root, config, 'accepted_ledger')
        lifecycle = {'schema_version': 1, 'activity': 'active', 'verified_at': '2026-09-28T00:00:00Z',
                     'source_versions': {'api': 'v1'}, 'evidence_roots': ['run-1'],
                     'review_trigger': 'source change', 'failure_class': 'implementation', 'counterexamples': []}
        section = '\n## PL-AAAAAAAAAAAA\nStatus: Accepted\nLesson: Verify retries\nApplies when: retries\nDoes not apply when: read only\nLifecycle: '+json.dumps(lifecycle)+'\n'
        ledger.write_text(ledger.read_text() + section)
        versions = self.request({'api': 'v2'}, 'versions.json')
        before = ledger.read_bytes()
        result = self.fixture.store('recall', '--query', 'retries', '--versions', str(versions))
        self.assertEqual(json.loads(result.stdout)['lessons'], [])
        self.assertEqual(ledger.read_bytes(), before)
        versions.write_text(json.dumps({'api': 'v1'}))
        result = self.fixture.store('recall', '--query', 'retries', '--versions', str(versions))
        self.assertEqual(len(json.loads(result.stdout)['lessons']), 1)
        ledger.write_text(ledger.read_text().replace('"activity": "active"', '"activity": "retired"'))
        result = self.fixture.store('recall', '--query', 'retries', '--versions', str(versions))
        self.assertEqual(json.loads(result.stdout)['lessons'], [])


if __name__ == '__main__':
    unittest.main()
