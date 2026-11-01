import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('ci_entrypoint', ROOT / 'scripts/ci.py')
ci = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ci)


class CiEntrypointTests(unittest.TestCase):
    def test_fast_mode_skips_packaging(self):
        names = [name for name, _ in ci.steps(True, Path('/unused'))]
        self.assertEqual(names, ['verify', 'readme-inventory', 'unit-tests-fast'])
        full = [name for name, _ in ci.steps(False, Path('/unused'))]
        self.assertIn('package-all', full)
        self.assertIn('unit-tests', full)

    def test_invalid_base_fails_instead_of_falling_back(self):
        with patch.dict('os.environ', {'CI_BASE': 'not-a-commit'}):
            base, error = ci.base_commit()
            owner = dict(ci.steps(False, Path('/unused')))['owner-suites']
        self.assertIsNone(base)
        self.assertIn('not a commit', error)
        self.assertNotIn('select_checks.py', ' '.join(owner))
        if ci.git('rev-parse', 'HEAD^'):  # a Git checkout with history (not an extracted archive)
            with patch.dict('os.environ', {'CI_BASE': '0' * 40}):
                self.assertIsNotNone(ci.base_commit()[0])  # new-branch push: use the merge base

    def test_every_step_runs_and_one_failure_fails_the_receipt(self):
        fake = [('ok', [sys.executable, '-c', 'pass']), ('bad', [sys.executable, '-c', 'raise SystemExit(3)']),
                ('after', [sys.executable, '-c', 'pass'])]
        with tempfile.TemporaryDirectory() as temporary, patch.object(ci, 'steps', lambda fast, dist: fake):
            receipt_path = Path(temporary) / 'receipt.json'
            with patch('sys.stdout'):
                code = ci.main(['--receipt', str(receipt_path)])
            receipt = json.loads(receipt_path.read_text())
        self.assertEqual(code, 1)
        self.assertEqual(receipt['status'], 'failed')
        self.assertEqual([s['exit_code'] for s in receipt['steps']], [0, 3, 0])
        self.assertIn('never a hosted CI result', receipt['scope'])
        self.assertIn('python', receipt['toolchain'])
        # Outside a Git checkout (an extracted archive) cleanliness is unknown, never assumed.
        self.assertEqual(receipt['clean_worktree'] is None, not ci.git('rev-parse', 'HEAD'))


if __name__ == '__main__':
    unittest.main()
