from __future__ import annotations

import copy
import importlib.util
import io
import json
import re
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('selected_toolkit', ROOT / 'scripts/toolkit.py')
toolkit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(toolkit)


def extract_archive(data, destination):
    data.extractall(destination)
    # zipfile does not restore Unix permissions; normal unzip does.
    for member in data.infolist():
        mode = member.external_attr >> 16
        if mode:
            (destination / member.filename).chmod(mode & 0o777)


class SelectionInstallTests(unittest.TestCase):
    def cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = toolkit.main(list(args))
        return code, out.getvalue(), err.getvalue()

    def state(self, project):
        return Path(project) / '.agents/rogemar-agent-toolkit.lock.json'

    def test_core_on_every_harness_excludes_native_and_optional_workflows(self):
        catalog = toolkit.load_json(toolkit.CATALOG_PATH)
        for harness in catalog['harnesses']:
            selected = toolkit.resolve_selection(harness, 'core', [])
            self.assertEqual(len(selected['skills']), 6)
            self.assertEqual(selected['external'], [])
            self.assertNotIn('codex-forge', selected['skills'])
        generic = toolkit.resolve_selection('gemini', 'core', ['engineering'])
        codex = toolkit.resolve_selection('codex', 'core', ['engineering'])
        cursor = toolkit.resolve_selection('cursor', 'core', ['engineering'])
        self.assertIn('engineering-playbooks', generic['skills'])
        self.assertNotIn('plan-model-router', generic['skills'])
        self.assertEqual(len([n for n in codex['skills'] if n == 'codex-forge' or n.startswith('forge-')]), 45)
        self.assertIn('plan-model-router', codex['skills'])
        self.assertIn('pstack', cursor['external'])
        self.assertNotIn('pstack', codex['external'])

    def test_unknown_pack_and_unsatisfied_native_requirement_fail_closed(self):
        with self.assertRaises(toolkit.ToolkitError):
            toolkit.resolve_selection('codex', 'core', ['invented-pack'])
        catalog = toolkit.load_json(toolkit.CATALOG_PATH)
        altered = copy.deepcopy(catalog)
        next(e for e in altered['vendored'] if e['name'] == 'create-plan')['requires'] = ['plan-model-router']
        with patch.object(toolkit, 'load_json', return_value=altered):
            with self.assertRaisesRegex(toolkit.ToolkitError, 'incompatible'):
                toolkit.resolve_selection('gemini', 'core', [])

    def test_codex_native_placement_and_recoverable_pack_removal(self):
        with tempfile.TemporaryDirectory() as project:
            args = ('--harness', 'codex', '--project-root', project)
            code, _, error = self.cli('install', *args, '--pack', 'engineering')
            self.assertEqual(code, 0, error)
            native = Path(project) / '.codex/skills/codex-forge/SKILL.md'
            self.assertTrue(native.exists())
            self.assertFalse((Path(project) / '.agents/skills/codex-forge').exists())
            before = self.state(project).read_bytes()
            for selection in ((), ('--profile', 'core', '--pack', 'engineering')):
                code, _, error = self.cli('upgrade', *args, *selection)
                self.assertEqual(code, 0, error)
                self.assertEqual(self.state(project).read_bytes(), before)
            code, _, error = self.cli('upgrade', *args, '--profile', '')
            self.assertEqual(code, 1)
            self.assertIn('unknown profile', error)
            self.assertEqual(self.state(project).read_bytes(), before)
            self.assertTrue(native.exists())
            # An explicit profile replaces the saved selection; omitted skills remain in backup.
            code, _, error = self.cli('upgrade', *args, '--profile', 'core')
            self.assertEqual(code, 0, error)
            self.assertFalse(native.exists())
            self.assertEqual(len(json.loads(self.state(project).read_text())['skills']), 6)
            self.assertEqual(json.loads(self.state(project).read_text())['requested_packs'], [])
            code, _, error = self.cli('rollback', *args)
            self.assertEqual(code, 0, error)
            self.assertTrue(native.exists())
            self.assertEqual(self.state(project).read_bytes(), before)

    def test_repeat_install_does_not_rewrite_state_or_create_new_backup(self):
        with tempfile.TemporaryDirectory() as project:
            args = ('install', '--project-root', project)
            self.assertEqual(self.cli(*args)[0], 0)
            before = self.state(project).read_bytes()
            code, output, error = self.cli(*args)
            self.assertEqual(code, 0, error)
            self.assertIn('already current', output)
            self.assertEqual(self.state(project).read_bytes(), before)

    def test_omitted_harness_recovers_the_single_cursor_installation(self):
        with tempfile.TemporaryDirectory() as project:
            self.assertEqual(self.cli('install', '--harness', 'cursor', '--project-root', project)[0], 0)
            state = Path(project) / '.cursor/rogemar-agent-toolkit.lock.json'
            before = state.read_bytes()
            code, _, error = self.cli('upgrade', '--project-root', project)
            self.assertEqual(code, 0, error)
            self.assertEqual(state.read_bytes(), before)
            self.assertFalse(self.state(project).exists())
            self.assertEqual(self.cli('rollback', '--project-root', project)[0], 0)
            self.assertFalse(state.exists())

    def test_symlinked_managed_ancestors_are_rejected_without_external_writes(self):
        for relative in ('.agents', '.agents/skills', '.agents/.rogemar-agent-toolkit', '.codex/skills'):
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as project, tempfile.TemporaryDirectory() as external:
                link = Path(project) / relative
                link.parent.mkdir(parents=True, exist_ok=True)
                link.symlink_to(external, target_is_directory=True)
                code, _, error = self.cli('install', '--harness', 'codex', '--pack', 'engineering', '--project-root', project)
                self.assertEqual(code, 1)
                self.assertIn('symlink', error)
                self.assertEqual(list(Path(external).iterdir()), [])
                self.assertFalse(self.state(project).exists())

    def test_copy_excludes_unhashed_cache_and_dependency_payloads(self):
        with tempfile.TemporaryDirectory() as temporary:
            source, destination = Path(temporary) / 'source', Path(temporary) / 'installed'
            source.mkdir()
            (source / 'SKILL.md').write_text('method')
            (source / 'node_modules/private-package').mkdir(parents=True)
            (source / 'node_modules/private-package/payload.js').write_text('untracked dependency')
            (source / 'cache.pyc').write_bytes(b'bytecode')
            toolkit.copy_or_link(source, destination, False)
            self.assertEqual(toolkit.tree_digest(source), toolkit.tree_digest(destination))
            self.assertEqual([p.name for p in destination.iterdir()], ['SKILL.md'])

    def test_executable_permission_drift_requires_review(self):
        with tempfile.TemporaryDirectory() as project:
            self.assertEqual(self.cli('install', '--project-root', project)[0], 0)
            skill = Path(project) / '.agents/skills/create-plan/SKILL.md'
            skill.chmod(skill.stat().st_mode ^ 0o100)
            code, _, error = self.cli('upgrade', '--project-root', project)
            self.assertEqual(code, 1)
            self.assertIn('local edits', error)

    def test_legacy_content_hash_migrates_without_false_drift(self):
        with tempfile.TemporaryDirectory() as project:
            self.assertEqual(self.cli('install', '--project-root', project)[0], 0)
            state_path = self.state(project)
            state = json.loads(state_path.read_text())
            state['schema_version'] = 1
            state.pop('harness')
            for name, record in state['skills'].items():
                record['sha256'] = toolkit.tree_digest(Path(project) / '.agents/skills' / name, legacy=True)[0]
            state_path.write_text(json.dumps(state))
            code, _, error = self.cli('upgrade', '--harness', 'agent-skills', '--project-root', project)
            self.assertEqual(code, 0, error)
            self.assertEqual(json.loads(state_path.read_text())['schema_version'], 2)

    def test_exact_adoption_preserves_unmanaged_content_on_rollback(self):
        with tempfile.TemporaryDirectory() as project:
            destination = Path(project) / '.agents/skills/create-plan'
            shutil.copytree(toolkit.SKILLS_ROOT / 'create-plan', destination)
            before = toolkit.tree_digest(destination)
            code, _, error = self.cli('install', '--project-root', project, '--adopt-identical')
            self.assertEqual(code, 0, error)
            self.assertEqual(self.cli('rollback', '--project-root', project)[0], 0)
            self.assertEqual(toolkit.tree_digest(destination), before)
            self.assertFalse(self.state(project).exists())

    def test_dry_run_is_read_only_even_with_conflicts(self):
        with tempfile.TemporaryDirectory() as project:
            destination = Path(project) / '.agents/skills/create-plan'
            destination.mkdir(parents=True)
            (destination / 'SKILL.md').write_text('user content')
            code, output, _ = self.cli('install', '--project-root', project, '--dry-run')
            self.assertEqual(code, 1)
            self.assertTrue(json.loads(output)['conflicts'])
            self.assertFalse(self.state(project).exists())
            self.assertFalse((Path(project) / '.agents/.rogemar-agent-toolkit').exists())
            self.assertEqual((destination / 'SKILL.md').read_text(), 'user content')

    def test_state_write_failure_restores_files_and_previous_state(self):
        with tempfile.TemporaryDirectory() as project:
            self.assertEqual(self.cli('install', '--project-root', project)[0], 0)
            state_path = self.state(project)
            before = state_path.read_bytes()
            skill = Path(project) / '.agents/skills/create-plan/SKILL.md'
            skill.write_text(skill.read_text() + '\nUser change\n')
            content = skill.read_bytes()
            writer = toolkit.write_json_atomic
            def fail_state(path, value):
                if path.resolve() == state_path.resolve():
                    raise OSError('injected state write failure')
                return writer(path, value)
            with patch.object(toolkit, 'write_json_atomic', side_effect=fail_state):
                code, _, error = self.cli('upgrade', '--project-root', project, '--backup-conflicts')
            self.assertEqual(code, 1)
            self.assertIn('injected', error)
            self.assertEqual(skill.read_bytes(), content)
            self.assertEqual(state_path.read_bytes(), before)

    def test_rollback_rejects_traversal_before_touching_files(self):
        with tempfile.TemporaryDirectory() as project:
            self.assertEqual(self.cli('install', '--project-root', project)[0], 0)
            state_path = self.state(project)
            before = state_path.read_bytes()
            record_path = Path(json.loads(before)['last_backup']) / 'backup.json'
            record = json.loads(record_path.read_text())
            record['created'] = ['../../outside']
            record_path.write_text(json.dumps(record))
            code, _, error = self.cli('rollback', '--project-root', project)
            self.assertEqual(code, 1)
            self.assertIn('invalid skill', error)
            self.assertEqual(state_path.read_bytes(), before)
            self.assertTrue((Path(project) / '.agents/skills/create-plan/SKILL.md').exists())

    def test_recovery_preparation_failure_precedes_any_replacement(self):
        with tempfile.TemporaryDirectory() as project:
            self.assertEqual(self.cli('install', '--project-root', project)[0], 0)
            before = self.state(project).read_bytes()
            skill = Path(project) / '.agents/skills/create-plan/SKILL.md'
            skill.write_text(skill.read_text() + '\nUser change\n')
            content = skill.read_bytes()
            mkdir = Path.mkdir
            def fail_recovery(path, *args, **kwargs):
                if 'failed-installs' in path.parts:
                    raise OSError('injected recovery preparation failure')
                return mkdir(path, *args, **kwargs)
            with patch.object(Path, 'mkdir', new=fail_recovery):
                code, _, error = self.cli('upgrade', '--project-root', project, '--backup-conflicts')
            self.assertEqual(code, 1)
            self.assertIn('injected', error)
            self.assertEqual(skill.read_bytes(), content)
            self.assertEqual(self.state(project).read_bytes(), before)
            self.assertFalse((Path(project) / '.agents/.rogemar-agent-toolkit/operation.lock').exists())

    def test_rollback_prepare_failure_releases_operation_lock(self):
        with tempfile.TemporaryDirectory() as project:
            self.assertEqual(self.cli('install', '--project-root', project)[0], 0)
            before = self.state(project).read_bytes()
            mkdir = Path.mkdir
            def fail_displaced(path, *args, **kwargs):
                if 'displaced' in path.parts:
                    raise OSError('injected backup directory failure')
                return mkdir(path, *args, **kwargs)
            with patch.object(Path, 'mkdir', new=fail_displaced):
                code, _, error = self.cli('rollback', '--project-root', project)
            self.assertEqual(code, 1)
            self.assertIn('injected', error)
            self.assertFalse((Path(project) / '.agents/.rogemar-agent-toolkit/operation.lock').exists())
            self.assertEqual(self.state(project).read_bytes(), before)

    def test_rollback_rejects_redirected_backup_directory(self):
        with tempfile.TemporaryDirectory() as project, tempfile.TemporaryDirectory() as external:
            self.assertEqual(self.cli('install', '--project-root', project)[0], 0)
            backups = Path(project) / '.agents/.rogemar-agent-toolkit/backups'
            saved = Path(external) / 'backups'
            shutil.move(backups, saved)
            backups.symlink_to(saved, target_is_directory=True)
            before = self.state(project).read_bytes()
            code, _, error = self.cli('rollback', '--project-root', project)
            self.assertEqual(code, 1)
            self.assertIn('symlink', error)
            self.assertEqual(self.state(project).read_bytes(), before)

    def test_selected_package_contains_only_core_and_extracted_catalog_verifies(self):
        with tempfile.TemporaryDirectory() as temporary:
            code, _, error = self.cli('package', '--output', temporary)
            self.assertEqual(code, 0, error)
            for archive in Path(temporary).glob('*.zip'):
                with zipfile.ZipFile(archive) as data:
                    receipt = json.loads(data.read('rogemar-agent-toolkit/release-selection.json'))
                    self.assertEqual(len(receipt['skills']), 6)
                    self.assertFalse(any('/codex-forge/SKILL.md' in n for n in data.namelist()))
                    if 'codex-marketplace' in archive.name:
                        extracted = Path(temporary) / 'extracted'
                        extract_archive(data, extracted)
                        root = extracted / 'rogemar-agent-toolkit'
                        self.assertTrue((root / 'catalog/codex-forge-upstream.json').is_file())
                        result = subprocess.run([sys.executable, 'scripts/toolkit.py', 'verify'], cwd=root, capture_output=True, text=True)
                        self.assertEqual(result.returncode, 0, result.stderr)

    def test_full_archives_preserve_native_provenance_and_all_selected_resources(self):
        with tempfile.TemporaryDirectory() as temporary:
            code, _, error = self.cli('package', '--profile', 'all', '--output', temporary)
            self.assertEqual(code, 0, error)
            for archive in Path(temporary).glob('*.zip'):
                extracted = Path(temporary) / archive.stem
                with zipfile.ZipFile(archive) as data:
                    extract_archive(data, extracted)
                root = extracted / 'rogemar-agent-toolkit'
                receipt = json.loads((root / 'release-selection.json').read_text())
                skillroot = root / 'skills' if (root / 'skills').exists() else root / 'plugins/rogemar-agent-toolkit/skills'
                if 'codex-marketplace' in archive.name:
                    self.assertEqual(len([n for n in receipt['skills'] if n == 'codex-forge' or n.startswith('forge-')]), 45)
                    self.assertTrue((root / 'catalog/codex-forge-upstream.json').is_file())
                else:
                    self.assertNotIn('codex-forge', receipt['skills'])
                    self.assertNotIn('plan-model-router', receipt['skills'])
                for name, expected in receipt['skills'].items():
                    self.assertEqual(toolkit.tree_digest(skillroot / name)[0], expected['sha256'], name)
                    for document in (skillroot / name).rglob('*.md'):
                        if 'automations' in document.parts:
                            continue  # Native inactive recipes are deliberately retained as upstream evidence.
                        for link in re.findall(r'\]\(([^)]+)\)', document.read_text()):
                            link = link.split('#')[0]
                            if link and '://' not in link and not link.startswith(('mailto:', '<')):
                                self.assertTrue((document.parent / link).exists(), str(document.relative_to(root)) + ': ' + link)


class ResourceTests(unittest.TestCase):
    def fixture(self, extra=None):
        stream = io.BytesIO()
        with tarfile.open(fileobj=stream, mode='w') as archive:
            for name in ['design-templates/sample/SKILL.md', 'design-templates/sample/assets/example.svg', 'design-systems/style/DESIGN.md', 'craft/lesson.md', 'LICENSE']:
                data = name.encode()
                item = tarfile.TarInfo(name)
                item.size = len(data)
                archive.addfile(item, io.BytesIO(data))
            if extra:
                archive.addfile(extra)
        return subprocess.CompletedProcess([], 0, stdout=stream.getvalue(), stderr=b'')

    def cli(self, *args):
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            return toolkit.main(list(args))

    def test_complete_resource_payload_is_copied_pinned_and_idempotent(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / 'resources'
            args = ('resources', '--source', temporary, '--destination', str(destination))
            # The source may be anywhere, but the library may not be nested in that checkout.
            args = ('resources', '--source', str(Path(temporary) / 'checkout'), '--destination', str(destination))
            with patch.object(toolkit.subprocess, 'run', return_value=self.fixture()) as run:
                self.assertEqual(self.cli(*args, '--dry-run'), 0)
                self.assertFalse(destination.exists())
                self.assertEqual(self.cli(*args), 0)
                self.assertTrue((destination / 'design-templates/sample/assets/example.svg').exists())
                receipt = (destination / '.toolkit-resources.json').read_bytes()
                self.assertEqual(self.cli(*args), 0)
                self.assertEqual((destination / '.toolkit-resources.json').read_bytes(), receipt)
                self.assertIn(toolkit.load_json(toolkit.CATALOG_PATH)['dependencies']['opendesign-library']['commit'], run.call_args[0][0])

    def test_symlink_archive_member_is_rejected_without_writes(self):
        member = tarfile.TarInfo('design-templates/escape')
        member.type = tarfile.SYMTYPE
        member.linkname = '/outside'
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / 'resources'
            with patch.object(toolkit.subprocess, 'run', return_value=self.fixture(member)):
                self.assertEqual(self.cli('resources', '--source', str(Path(temporary) / 'checkout'), '--destination', str(destination)), 1)
                self.assertFalse(destination.exists())

    def test_destination_created_during_preparation_is_never_displaced(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / 'resources'
            writer = toolkit.write_json_atomic
            def concurrent_creation(path, value):
                writer(path, value)
                destination.mkdir()
                (destination / 'personal.txt').write_text('keep me')
            with patch.object(toolkit.subprocess, 'run', return_value=self.fixture()), patch.object(toolkit, 'write_json_atomic', side_effect=concurrent_creation):
                self.assertEqual(self.cli('resources', '--source', str(Path(temporary) / 'checkout'), '--destination', str(destination)), 1)
            self.assertEqual((destination / 'personal.txt').read_text(), 'keep me')
            self.assertEqual(list(Path(temporary).glob('resources.backup-*')), [])
            self.assertFalse((Path(temporary) / '.resources.toolkit-operation.lock').exists())


if __name__ == '__main__':
    unittest.main()
