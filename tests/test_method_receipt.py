"""The method receipt makes a skipped review visible and blocks acceptance by default."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'plugins/rogemar-agent-toolkit/skills/integrated-workflow/scripts/checkpoint.py'
cp = None
if SCRIPT.is_file():
    spec = importlib.util.spec_from_file_location('checkpoint_receipt', SCRIPT)
    cp = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cp)


@unittest.skipUnless(SCRIPT.is_file(), 'Optional engineering checkpoint is not in this package')
class MethodReceiptTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'repo'
        (self.root / 'App').mkdir(parents=True)
        self.git('init', '-q')
        self.git('config', 'user.email', 'fixture@example.invalid')
        self.git('config', 'user.name', 'Receipt fixture')
        (self.root / 'recipe.md').write_text('Expected behavior.')
        (self.root / 'App/View.swift').write_text('struct V {}\n')
        self.git('add', '.')
        self.git('commit', '-qm', 'fixture')
        self.base = self.git('rev-parse', 'HEAD').strip()
        (self.root / 'App/View.swift').write_text('import SwiftUI\nstruct V: View {}\n')
        self.mapping = {'schema_version': 1, 'runtime_paths': ['App/**'], 'shared_paths': [], 'nonruntime_paths': [],
                        'features': [{'id': 'view', 'paths': ['App/**'], 'recipe': 'recipe.md', 'platforms': ['ios']}]}
        self.identity, _ = cp.candidate(self.root, self.base)
        self.evidence = Path(self.tmp.name) / 'swiftui-review.md'
        self.evidence.write_text('swiftui-pro review notes')
        self.receipt = {'schema_version': 1, 'candidate': self.identity,
                        'scope': {'features': [], 'assessment': 'view changed'},
                        'map_review': {'disposition': 'unchanged with reason', 'reason': 'kept',
                                       'expected_behavior_preserved': True}, 'gates': []}

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.root), *args], stderr=subprocess.DEVNULL).decode()

    def accept(self, receipt, policy=None):
        result = cp.check(self.root, self.base, 'accept', receipt, self.mapping, [], 'accept', policy)
        return [e for e in result['errors'] if e.startswith('method')], result

    def with_methods(self, *records, **scope):
        receipt = copy.deepcopy(self.receipt)
        receipt['methods'] = list(records)
        receipt['scope'].update(scope)
        return receipt

    def test_changed_paths_derive_required_groups(self):
        index = cp.load_index({})
        self.assertIn('swiftui', cp.required_methods(index, cp.candidate_tags(self.root, ['App/View.swift'], index)))
        self.assertIn('supabase-guardian', cp.required_methods(index, cp.candidate_tags(self.root, ['supabase/migrations/1.sql'], index)))
        formal = cp.required_methods(index, cp.candidate_tags(self.root, ['spec/Sync.tla'], index))
        self.assertTrue({'statechart-verification', 'formal-verification-create', 'formal-verification-maintain'} <= set(formal))
        self.assertEqual(cp.required_methods(index, cp.candidate_tags(self.root, ['README.md'], index)), {})

    def test_skipped_review_blocks_acceptance(self):
        errors, result = self.accept(self.receipt)
        self.assertEqual(result['status'], 'rejected')
        self.assertTrue(any('no record' in e and 'swiftui-pro' in e for e in errors))

    def test_non_used_states_need_reasons(self):
        errors, _ = self.accept(self.with_methods({'id': 'swiftui-pro', 'state': 'not-applicable'}))
        self.assertTrue(any('needs a reason' in e for e in errors))
        errors, _ = self.accept(self.with_methods({'id': 'swiftui-pro', 'state': 'blocked', 'reason': 'simulator down'}))
        self.assertEqual(errors, [])
        errors, _ = self.accept(self.with_methods({'id': 'swiftui-pro', 'state': 'skipped', 'reason': 'x'}))
        self.assertTrue(any('state must be' in e for e in errors))

    def test_used_needs_existing_evidence(self):
        for evidence, ok in ([], False), (['/no/such/file.md'], False), ([str(self.evidence)], True), ([self.base], True):
            with self.subTest(evidence=evidence):
                errors, _ = self.accept(self.with_methods({'id': 'swiftui-expert-skill', 'state': 'used', 'evidence': evidence}))
                self.assertEqual(errors == [], ok, errors)

    def test_small_corrections_and_report_only_policy_do_not_block(self):
        errors, result = self.accept(self.with_methods(size='small'))
        self.assertEqual(errors, [])
        self.assertFalse(result['methods']['enforced'])
        errors, result = self.accept(self.receipt, {'methods': 'report-only'})
        self.assertEqual(errors, [])
        self.assertTrue(result['methods']['errors'])

    def test_declared_scope_tags_add_requirements(self):
        errors, _ = self.accept(self.with_methods({'id': 'swiftui-pro', 'state': 'used', 'evidence': [str(self.evidence)]},
                                                  tags=['swift-concurrency']))
        self.assertTrue(any('swift-concurrency' in e for e in errors))

    def test_unpinned_index_is_unavailable_never_passed(self):
        index = Path(self.tmp.name) / 'index.json'
        index.write_text('{}')
        _, result = self.accept(self.receipt, {'routing_index': str(index), 'routing_index_sha256': 'bad'})
        self.assertEqual(result['methods']['status'], 'unavailable')
        self.assertTrue(any('method receipt unavailable' in e for e in result['errors']))
        good = {'routing_index': str(index), 'routing_index_sha256': hashlib.sha256(b'{}').hexdigest()}
        _, result = self.accept(self.receipt, good)
        self.assertEqual(result['methods']['required'], {})

    def test_start_lists_required_methods(self):
        result = cp.check(self.root, self.base, 'start', self.receipt, self.mapping)
        self.assertIn('swiftui', result['methods']['required'])


if __name__ == '__main__':
    unittest.main()
