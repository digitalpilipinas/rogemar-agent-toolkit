"""Imported resource selection and safe Xcode runtime behavior, without requiring Xcode."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'plugins/rogemar-agent-toolkit/skills'
spec = importlib.util.spec_from_file_location('imports_toolkit', ROOT / 'scripts/toolkit.py')
toolkit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(toolkit)


class ImportedSkillsTests(unittest.TestCase):
    def test_swift_pack_resolves_all_twelve_and_resources_in_each_harness(self):
        catalog = toolkit.load_json(toolkit.CATALOG_PATH)
        if 'swift' not in catalog['packs']:
            self.skipTest('swift pack not included in this distribution')
        names = catalog['packs']['swift']['skills']
        self.assertEqual(len(set(names)), 12)
        entries = {r['name']: r for r in catalog['vendored']}
        for harness in ('codex', 'cursor', 'agent-skills'):
            selected = toolkit.resolve_selection(harness, 'core', ['swift'])
            self.assertTrue(set(names) <= set(selected['skills']))
        for name in names:
            self.assertEqual(len(list((SKILLS / name).rglob('SKILL.md'))), 1)
            for resource in entries[name]['required_resources']:
                self.assertTrue((SKILLS / name / resource).is_file(), (name, resource))
        self.assertEqual(len(toolkit.resolve_selection('agent-skills', 'core', [])['skills']), 6)

    def run_benchmark(self, root, mode='pass', extra=()):
        bindir = root / 'bin'
        bindir.mkdir(exist_ok=True)
        executable = bindir / 'xcodebuild'
        executable.write_text('''#!/usr/bin/env python3
import os,sys
from pathlib import Path
args=sys.argv[1:]
p=Path(args[args.index('-derivedDataPath')+1]); p.mkdir(parents=True,exist_ok=True)
(p/'owned').write_text('build product')
if '-showBuildSettings' in args: print('COMPILATION_CACHE_ENABLE_CACHING = YES')
if os.environ.get('FIXTURE_FAIL')=='build' and 'build' in args:
 print('intentional compiler failure');sys.exit(65)
print('SwiftCompile 1.00 seconds')
''')
        executable.chmod(0o755)
        parent = root / 'pre-existing'
        parent.mkdir(exist_ok=True)
        (parent / 'valuable').write_text('preserve me')
        env = dict(os.environ, PATH=str(bindir) + os.pathsep + os.environ['PATH'], FIXTURE_FAIL=mode)
        command = [sys.executable, str(SKILLS / 'xcode-build-benchmark/scripts/benchmark_builds.py'),
                   '--project', 'Fixture.xcodeproj', '--scheme', 'Fixture', '--repeats', '2',
                   '--derived-data-path', str(parent), '--output-dir', str(root / 'evidence'), *extra]
        result = subprocess.run(command, env=env, capture_output=True, text=True, timeout=30)
        self.assertEqual((parent / 'valuable').read_text(), 'preserve me')
        self.assertEqual([p.name for p in parent.iterdir()], ['valuable'])
        return result

    def test_builds_preserve_parent_evidence_and_reject_false_success(self):
        if not (SKILLS / 'xcode-build-benchmark').exists():
            self.skipTest('Xcode helpers not selected')
        for mode in ('pass', 'build'):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                result = self.run_benchmark(root, mode)
                self.assertEqual(result.returncode, 0 if mode == 'pass' else 1, result.stderr)
                artifact_path = next((root / 'evidence').glob('*/benchmark.json'))
                artifact = json.loads(artifact_path.read_text())
                self.assertEqual(artifact['status'], 'complete' if mode == 'pass' else 'failed')
                self.assertTrue(all(Path(p['raw_log_path']).is_file() for p in artifact['phases']))
                if mode == 'pass':
                    self.assertEqual(artifact['summary']['cached_clean']['count'], 2)
                report = subprocess.run([sys.executable, str(SKILLS / 'xcode-build-orchestrator/scripts/generate_optimization_report.py'),
                                         '--benchmark', str(artifact_path)], capture_output=True, text=True)
                self.assertEqual(report.returncode, result.returncode)

    def test_compilation_diagnostics_failure_keeps_logs_and_returns_failure(self):
        if not (SKILLS / 'xcode-compilation-analyzer').exists():
            self.skipTest('Xcode helpers not selected')
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.run_benchmark(root)
            env = dict(os.environ, PATH=str(root / 'bin') + os.pathsep + os.environ['PATH'], FIXTURE_FAIL='build')
            result = subprocess.run([sys.executable, str(SKILLS / 'xcode-compilation-analyzer/scripts/diagnose_compilation.py'),
                '--project', 'Fixture.xcodeproj', '--scheme', 'Fixture', '--derived-data-path', str(root / 'pre-existing'),
                '--output-dir', str(root / 'diagnostics')], env=env, capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 65)
            artifact = json.loads(next((root / 'diagnostics').glob('*.json')).read_text())
            self.assertFalse(artifact['build_success'])
            self.assertIn('intentional compiler failure', Path(artifact['raw_log_path']).read_text())
            self.assertEqual((root / 'pre-existing/valuable').read_text(), 'preserve me')

    def test_invalid_repeat_and_output_override_do_not_run(self):
        if not (SKILLS / 'xcode-build-benchmark').exists():
            self.skipTest('Xcode helpers not selected')
        for extra in (['--repeats', '0'], ['--extra-arg=SYMROOT=/somewhere'], ['--extra-arg=-derivedDataPath']):
            with tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                self.assertEqual(self.run_benchmark(root, extra=extra).returncode, 2)
                self.assertFalse((root / 'evidence').exists())


if __name__ == '__main__':
    unittest.main()
