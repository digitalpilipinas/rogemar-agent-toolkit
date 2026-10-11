"""Exercise external-only scope through the real installer with a pinned local fixture."""
import copy
import importlib.util
import io
import json
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('external_only_toolkit', Path(__file__).resolve().parents[1] / 'scripts/toolkit.py')
toolkit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(toolkit)


class ExternalOnlyTests(unittest.TestCase):
    def cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = toolkit.main(list(args))
        return code, out.getvalue(), err.getvalue()

    def test_dry_run_is_offline_and_excludes_incompatible_dependencies(self):
        with tempfile.TemporaryDirectory() as project, patch.object(toolkit, 'fetch_external_source') as fetch:
            code, output, error = self.cli('install', '--project-root', project, '--profile', 'all', '--external-only', '--dry-run')
            self.assertEqual(code, 0, error)
            plan = json.loads(output)
            self.assertTrue(plan['external_only'])
            self.assertEqual(plan['skills'], [])
            self.assertEqual(plan['destinations'], {})
            self.assertNotIn('pstack', plan['external'])
            self.assertEqual(plan['external'], toolkit.resolve_selection('agent-skills', 'all', [])['external'])
            fetch.assert_not_called()
            self.assertEqual(list(Path(project).iterdir()), [])

    def test_invalid_flags_and_scope_changes_preserve_existing_state(self):
        with tempfile.TemporaryDirectory() as project:
            base = ['--project-root', project]
            for flag in ('--skip-external', '--link'):
                self.assertEqual(self.cli('install', *base, '--external-only', flag)[0], 1)
                self.assertEqual(list(Path(project).iterdir()), [])
            self.assertEqual(self.cli('install', *base, '--skip-external')[0], 0)
            state = Path(project) / '.agents/rogemar-agent-toolkit.lock.json'
            before = state.read_bytes()
            self.assertNotIn('external_only', json.loads(before))
            code, _, error = self.cli('upgrade', *base, '--external-only')
            self.assertEqual(code, 1)
            self.assertIn('cannot change a full', error)
            self.assertEqual(state.read_bytes(), before)
            self.assertEqual(self.cli('upgrade', *base, '--skip-external')[0], 0)
            self.assertEqual(state.read_bytes(), before)

    def test_clean_repeat_saved_upgrade_conflict_and_rollback(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / 'repo'
            skill = source / 'skills/example'
            (skill / 'references').mkdir(parents=True)
            (skill / 'SKILL.md').write_text('version one')
            (skill / 'references/check.md').write_text('resource')
            (source / 'LICENSE').write_text('license')
            (source / 'AGENTS.md').write_text('repository-only instructions')
            (source / 'hooks.json').write_text('{}')
            def git(*args):
                return subprocess.check_output(['git', '-C', str(source), *args], text=True).strip()
            git('init', '-q')
            git('add', '.')
            git('-c', 'user.name=Fixture', '-c', 'user.email=f@example.invalid', 'commit', '-qm', 'one')
            first = git('rev-parse', 'HEAD')
            (skill / 'SKILL.md').write_text('version two')
            git('add', '.')
            git('-c', 'user.name=Fixture', '-c', 'user.email=f@example.invalid', 'commit', '-qm', 'two')
            second = git('rev-parse', 'HEAD')
            catalog = toolkit.load_json(toolkit.CATALOG_PATH)
            catalog['packs']['fixture'] = {'skills': [], 'external': ['fixture']}
            catalog['dependencies']['fixture'] = {'kind': 'skills', 'targets': ['agent-skills'], 'auto_install': {
                'repository': 'https://github.com/example/fixture.git', 'commit': first,
                'skills': {'example': 'skills/example'}}}
            load = toolkit.load_json
            def load_fixture(path):
                return copy.deepcopy(catalog) if path == toolkit.CATALOG_PATH else load(path)
            def fetch(recipe, destination):
                subprocess.run(['git', 'clone', '-q', str(source), str(destination)], check=True)
            project = root / 'project'
            target = project / '.agents/skills'
            (target / 'unrelated').mkdir(parents=True)
            (target / 'unrelated/SKILL.md').write_text('keep me')
            state_path = target.parent / 'rogemar-agent-toolkit.lock.json'
            args = ['--project-root', str(project)]
            with patch.object(toolkit, 'load_json', side_effect=load_fixture), patch.object(toolkit, 'structural_errors', return_value=[]), patch.object(toolkit, 'fetch_external_source', side_effect=fetch) as fetcher:
                self.assertEqual(self.cli('install', *args, '--pack', 'fixture', '--external-only')[0], 0)
                state = load(state_path)
                self.assertTrue(state['external_only'])
                self.assertEqual(state['skills'], {})
                self.assertEqual({p.name for p in target.iterdir()}, {'example', 'unrelated'})
                self.assertEqual((target / 'example/references/check.md').read_text(), 'resource')
                self.assertTrue((target / 'example/upstream-notices/LICENSE').is_file())
                self.assertFalse(list(target.rglob('AGENTS.md')))
                self.assertFalse(list(target.rglob('hooks.json')))
                before = state_path.read_bytes()
                self.assertEqual(self.cli('install', *args)[0], 0)
                self.assertEqual(state_path.read_bytes(), before)
                self.assertEqual(fetcher.call_count, 1)
                catalog['dependencies']['fixture']['auto_install']['commit'] = second
                self.assertEqual(self.cli('upgrade', *args)[0], 0)
                self.assertEqual((target / 'example/SKILL.md').read_text(), 'version two')
                self.assertTrue(load(state_path)['external_only'])
                self.assertEqual(self.cli('rollback', *args)[0], 0)
                self.assertEqual((target / 'example/SKILL.md').read_text(), 'version one')
                self.assertTrue(load(state_path)['external_only'])
                (target / 'example/SKILL.md').write_text('local edit')
                code, _, error = self.cli('upgrade', *args)
                self.assertEqual(code, 1)
                self.assertIn('locally modified', error)
                self.assertEqual((target / 'example/SKILL.md').read_text(), 'local edit')
                self.assertEqual((target / 'unrelated/SKILL.md').read_text(), 'keep me')
                self.assertEqual(self.cli('upgrade', *args, '--skip-external')[0], 1)


if __name__ == '__main__':
    unittest.main()
