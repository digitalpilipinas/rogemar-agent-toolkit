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
    spec = importlib.util.spec_from_file_location('checkpoint', SCRIPT)
    cp = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cp)


@unittest.skipUnless(SCRIPT.is_file(), 'Optional engineering checkpoint is not in this package')
class CheckpointTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'repo'
        self.root.mkdir()
        self.git('init', '-q')
        self.git('config', 'user.email', 'fixture@example.invalid')
        self.git('config', 'user.name', 'Checkpoint fixture')
        (self.root / 'app.py').write_text('old')
        (self.root / 'recipe.md').write_text('Expected user behavior; real action and observable result.')
        self.git('add', '.')
        self.git('commit', '-qm', 'fixture')
        self.base = self.git('rev-parse', 'HEAD').strip()
        (self.root / 'app.py').write_text('new')
        self.mapping = {'schema_version': 1, 'runtime_paths': ['*.py'], 'shared_paths': ['shared.py'], 'nonruntime_paths': ['docs/**'],
                        'features': [{'id': 'open', 'paths': ['app.py'], 'recipe': 'recipe.md', 'platforms': ['ios']},
                                     {'id': 'resume', 'paths': ['resume.py'], 'recipe': 'recipe.md', 'platforms': ['ios']}]}
        self.identity, _ = cp.candidate(self.root, self.base)
        proof = Path(self.tmp.name) / 'proof.txt'
        proof.write_text('Synthetic test evidence; not live application proof')
        gate = {'gate': 'open:ios', 'feature': 'open', 'platform': 'ios', 'requirement': 'required',
                'source': 'fixture policy', 'trigger': 'app.py', 'owner': 'fixture', 'boundary': 'accept',
                'state': 'passed', 'candidate': self.identity,
                'runtime': {'target': 'open', 'fixture': 'synthetic', 'actions': ['tap'], 'observed': 'form', 'cleanup': 'owned session stopped'},
                'evidence': [{'path': str(proof), 'sha256': cp.digest(proof), 'kind': 'runtime', 'platform': 'ios', 'candidate': self.identity}]}
        self.receipt = {'schema_version': 1, 'candidate': self.identity, 'scope': {'features': [], 'assessment': 'app behavior changed'},
                        'map_review': {'disposition': 'unchanged with reason', 'reason': 'contract preserved', 'expected_behavior_preserved': True},
                        'gates': [gate]}

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.root), *args], stderr=subprocess.DEVNULL).decode()

    def check(self, receipt=None, phase='accept'):
        return cp.check(self.root, self.base, phase, receipt or self.receipt, self.mapping)

    def test_valid_identity_selection_and_resume(self):
        self.assertEqual(self.check()['status'], 'validated-record')
        self.assertEqual(self.check(phase='start')['selected'][0]['id'], 'open')
        self.assertIn('learning candidate', self.check(phase='close')['next_action'])
        (self.root / 'shared.py').write_text('shared')
        self.assertEqual(len(self.check(phase='start')['selected']), 2)
        self.assertEqual(self.check()['status'], 'rejected')

    def test_proportional_docs_and_missing_recipe(self):
        (self.root / 'app.py').write_text('old')
        (self.root / 'docs').mkdir()
        (self.root / 'docs/readme.md').write_text('wording')
        self.assertEqual(self.check(phase='start')['selected'], [])
        (self.root / 'recipe.md').unlink()
        with self.assertRaisesRegex(ValueError, 'missing'):
            self.check()

    def test_fails_closed_for_actual_counterexamples(self):
        mutations = [lambda r: r.update(candidate={}),
                     lambda r: r['gates'][0].update(platform='web'),
                     lambda r: r['gates'][0].update(state='blocked'),
                     lambda r: r['gates'][0].update(requirement='optional'),
                     lambda r: r['gates'][0]['evidence'][0].update(path='/does-not-exist'),
                     lambda r: r['gates'][0]['evidence'][0].update(sha256='wrong'),
                     lambda r: r['gates'][0]['evidence'][0].update(kind='unit'),
                     lambda r: r['map_review'].update(expected_behavior_preserved=False),
                     lambda r: r['gates'].clear()]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                r = copy.deepcopy(self.receipt)
                mutate(r)
                self.assertEqual(self.check(r)['status'], 'rejected')
        (self.root / 'new.py').write_text('unmapped runtime')
        self.assertEqual(self.check(phase='start')['coverage_gaps'], ['new.py'])
        self.assertEqual(self.check()['status'], 'rejected')

    def test_outstanding_gate_cannot_disappear_at_resume(self):
        gate = copy.deepcopy(self.receipt['gates'][0])
        gate.update(gate='local-review', state='blocked')
        gate.pop('platform'); gate.pop('feature')
        self.receipt['gates'].append(gate)
        self.assertEqual(self.check(phase='close')['status'], 'rejected')
        gate['boundary'] = 'ready-for-review'
        self.assertEqual(self.check(phase='close')['status'], 'validated-record')

    def test_malformed_evidence_and_runtime_are_rejected(self):
        for key, value in [('evidence', {}), ('evidence', [None]), ('evidence', None), ('runtime', 'not an object')]:
            with self.subTest(key=key, value=value):
                receipt = copy.deepcopy(self.receipt)
                receipt['gates'][0][key] = value
                result = self.check(receipt)
                self.assertEqual(result['status'], 'rejected')
                self.assertTrue(any('must be an' in error for error in result['errors']))

    def test_deferral_never_becomes_completion(self):
        self.receipt['gates'][0].update(state='deferred', owner_decision='recorded owner decision 17')
        result = self.check(phase='close')
        self.assertEqual(result['status'], 'deferred')
        self.assertIn('do not capture', result['next_action'])

    def test_trusted_policy_and_validator_pins(self):
        (self.root / '.agents').mkdir()
        (self.root / '.agents/verification.json').write_text(json.dumps(self.mapping))
        # Refresh identity after adding the tracked-policy candidate file.
        identity, _ = cp.candidate(self.root, self.base)
        self.receipt['candidate'] = identity
        self.receipt['gates'][0]['candidate'] = identity
        self.receipt['gates'][0]['evidence'][0]['candidate'] = identity
        receipt = Path(self.tmp.name) / 'receipt.json'
        receipt.write_text(json.dumps(self.receipt))
        policy = Path(self.tmp.name) / 'policy.json'
        policy.write_text(json.dumps({'repository': str(self.root.resolve()), 'mapping': self.mapping, 'required_gates': []}))
        args = ['python3', str(SCRIPT), '--root', str(self.root), '--base', self.base, '--phase', 'accept', '--receipt', str(receipt)]
        self.assertEqual(subprocess.run(args, capture_output=True).returncode, 1)
        args += ['--trusted-policy', str(policy), '--policy-sha256', cp.digest(policy), '--validator-sha256', cp.digest(SCRIPT)]
        self.assertEqual(subprocess.run(args, capture_output=True).returncode, 0)
        altered = copy.deepcopy(self.mapping)
        altered['features'][0]['platforms'] = ['web']
        (self.root / '.agents/verification.json').write_text(json.dumps(altered))
        out = subprocess.run(args, capture_output=True, text=True)
        self.assertEqual(out.returncode, 1)
        self.assertIn('separate policy review', out.stdout)

    def test_tree_inspection_ignores_worktree_and_rejects_unsafe_recipes(self):
        self.git('add', '.')
        self.git('commit', '-qm', 'candidate fixture')
        revision = self.git('rev-parse', 'HEAD').strip()
        (self.root / 'recipe.md').write_text('mutable worktree bytes')
        self.assertNotEqual(cp.tree_file(self.root, revision, 'recipe.md'), b'mutable worktree bytes')
        cp.validate_mapping(self.root, self.mapping, revision)
        for name in ('../recipe.md', '/recipe.md', '.git/config', './recipe.md', 'absent.md'):
            with self.subTest(path=name), self.assertRaises(ValueError):
                cp.tree_file(self.root, revision, name)
        (self.root / 'link.md').symlink_to('recipe.md')
        (self.root / 'empty.md').write_text('')
        self.git('add', 'link.md', 'empty.md')
        self.git('commit', '-qm', 'unsafe fixture')
        revision = self.git('rev-parse', 'HEAD').strip()
        for name in ('link.md', 'empty.md'):
            with self.subTest(path=name), self.assertRaises(ValueError):
                cp.tree_file(self.root, revision, name)

    def test_cli_structure_uses_immutable_tree_and_never_claims_runtime(self):
        (self.root / '.agents').mkdir()
        (self.root / '.agents/verification.json').write_text(json.dumps(self.mapping))
        self.git('add', '.')
        self.git('commit', '-qm', 'mapping fixture')
        revision = self.git('rev-parse', 'HEAD').strip()
        policy = Path(self.tmp.name) / 'policy.json'
        policy.write_text(json.dumps({'repository': str(self.root.resolve()), 'mapping': self.mapping}))
        (self.root / '.agents/verification.json').write_text('invalid mutable data')
        args = ['python3', str(SCRIPT), '--root', str(self.root), '--base', revision,
                '--phase', 'start', '--structure', '--tree', revision, '--receipt', str(policy.parent / 'absent.json'),
                '--trusted-policy', str(policy), '--policy-sha256', cp.digest(policy), '--validator-sha256', cp.digest(SCRIPT)]
        result = subprocess.run(args, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)['runtime'], 'unverified')
        self.assertEqual(json.loads(result.stdout)['tree'], revision)
        args[args.index('--tree') + 1] = 'HEAD'
        self.assertNotEqual(subprocess.run(args, capture_output=True).returncode, 0)


if __name__ == '__main__':
    unittest.main()
