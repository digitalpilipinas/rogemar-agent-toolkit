"""Opt-in readiness hooks stay small, read-only toward the project and never break a session."""
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'plugins/rogemar-agent-toolkit/skills'
spec = importlib.util.spec_from_file_location('readiness_hooks', SKILLS / 'project-readiness/scripts/hooks.py')
hooks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hooks)
HAS_CHECKPOINT = (SKILLS / 'integrated-workflow/scripts/checkpoint.py').is_file()


def snapshot(root):
    return {p: p.stat().st_mtime_ns for p in Path(root).rglob('*') if p.is_file() and '.git' not in p.parts}


class ReadinessHookTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'repo'
        (self.root / 'App').mkdir(parents=True)
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        (self.root / 'App/View.swift').write_text('import SwiftUI\n')
        cache = Path(self.tmp.name) / 'cache'
        patcher = mock.patch.dict(os.environ, {'PROJECT_READINESS_CACHE': str(cache)})
        patcher.start()
        self.addCleanup(patcher.stop)
        self.data = {'cwd': str(self.root)}

    def test_session_start_reports_and_caches_outside_the_repository(self):
        before = snapshot(self.root)
        text = hooks.session_start(self.data)
        self.assertIn('Project readiness:', text)
        self.assertIn('swiftui:', text)
        self.assertEqual(snapshot(self.root), before)
        resolved = hooks.project_root(self.data)  # Git's resolved root keys the cache
        self.assertTrue(hooks.cache_path(resolved).is_file())
        self.assertFalse(str(hooks.cache_path(resolved)).startswith(str(resolved)))

    def test_prompt_note_only_for_mentioned_technology_and_stays_small(self):
        hooks.session_start(self.data)
        self.assertEqual(hooks.prompt_note(dict(self.data, prompt='update the README wording')), '')
        note = hooks.prompt_note(dict(self.data, prompt='Fix the SwiftUI settings screen'))
        self.assertIn('swiftui-pro', note)
        self.assertLessEqual(len(note), hooks.MAX_PROMPT_NOTE)

    def test_prompt_without_a_session_cache_is_silent(self):
        self.assertEqual(hooks.prompt_note(dict(self.data, prompt='SwiftUI')), '')

    @unittest.skipUnless(HAS_CHECKPOINT, 'integrated-workflow is not in this selection')
    def test_stop_warns_until_the_receipt_records_the_method(self):
        warning = hooks.stop_warning(self.data)
        self.assertIn('swiftui', warning)
        self.assertEqual(hooks.stop_warning(dict(self.data, stop_hook_active=True)), '')  # no loops
        (self.root / 'receipt.json').write_text(json.dumps({'methods': [{'id': 'swiftui-pro', 'state': 'used'}]}))
        self.assertEqual(hooks.stop_warning(self.data, 'receipt.json'), '')

    def test_claude_settings_register_three_events(self):
        settings = hooks.claude_settings('receipt.json')['hooks']
        self.assertEqual(set(settings), {'SessionStart', 'UserPromptSubmit', 'Stop'})
        self.assertIn('--receipt "receipt.json"', settings['Stop'][0]['hooks'][0]['command'])

    def test_hooks_never_fail_the_harness(self):
        # Harnesses send hook input on stdin and close it; supply that here.
        with mock.patch('sys.stdin', io.StringIO('{}')):
            self.assertEqual(hooks.main(['session-start-typo']), 2)
        with mock.patch('sys.stdin', io.StringIO('{}')), \
                mock.patch.object(hooks, 'session_start', side_effect=RuntimeError('boom')):
            self.assertEqual(hooks.main(['session-start']), 0)


if __name__ == '__main__':
    unittest.main()
