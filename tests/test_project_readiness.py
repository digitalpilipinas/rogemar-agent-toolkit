"""project-readiness stays read-only, detects technologies and reports one honest plan."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'plugins/rogemar-agent-toolkit/skills'
INDEX = json.loads((SKILLS / 'workflow-orchestrator/references/skill-routing.json').read_text())


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


readiness = load('readiness', SKILLS / 'project-readiness/scripts/readiness.py')
CHECKPOINT = SKILLS / 'integrated-workflow/scripts/checkpoint.py'
checkpoint = load('checkpoint', CHECKPOINT) if CHECKPOINT.is_file() else None  # absent from the core archive


def snapshot(root):
    return {p: (p.stat().st_mtime_ns, p.stat().st_size) for p in Path(root).rglob('*') if p.is_file()}


class ReadinessTests(unittest.TestCase):
    def repo(self, files, git=True):
        root = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: subprocess.run(['rm', '-rf', str(root)]))
        for name, text in files.items():
            (root / name).parent.mkdir(parents=True, exist_ok=True)
            (root / name).write_text(text)
        if git:
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
        return root

    def owners(self, *names):
        """A skills folder with stand-in owners, independent of what this package installs."""
        folder = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: subprocess.run(['rm', '-rf', str(folder)]))
        for name in names:
            (folder / name).mkdir()
            (folder / name / 'SKILL.md').write_text('---\nname: %s\n---\n' % name)
        return folder

    def items(self, plan):
        return {i['id']: i for i in plan['items']}

    def test_detects_markers_and_content_markers(self):
        root = self.repo({'Package.swift': '', 'App/View.swift': 'import SwiftUI\n',
                          'supabase/config.toml': '', 'tsconfig.json': '{}'})
        tags = readiness.plan(root, INDEX)['detected_tags']
        self.assertTrue({'swift', 'swiftui', 'supabase', 'typescript'} <= set(tags))
        self.assertNotIn('swiftdata', tags)

    def test_tracked_record_under_an_ignored_folder_needs_the_owner(self):
        root = self.repo({'.gitignore': '.agents/*\n', 'AGENTS.md': 'Run `project-readiness` first.\n'})
        plan = readiness.plan(root, INDEX, skills_root=self.owners('forge-create-verification-skill'))
        item = self.items(plan)['footprint:.agents/verification.json']
        self.assertEqual((item['state'], item['kind']), ('needs-owner', 'ignore-rule'))
        self.assertIn('Unignore', item['action'])
        self.assertEqual(plan['status'], 'needs-owner')
        self.assertFalse(plan['grants_authority'])

    def test_tracked_files_under_an_ignored_footprint_need_untracking(self):
        root = self.repo({'.codex/project-learning/state/run.json': '{}'})
        subprocess.run(['git', '-C', str(root), 'add', '.'], check=True)
        (root / '.gitignore').write_text('.codex/project-learning/state/\n')
        item = self.items(readiness.plan(root, INDEX))['footprint:.codex/project-learning/state/']
        self.assertEqual(item['state'], 'needs-owner')
        self.assertIn('git rm -r --cached', item['action'])

    def test_approved_status_has_its_own_exit_code(self):
        root = self.repo({})
        plan = readiness.plan(root, INDEX)
        (root / '.agents').mkdir()
        (root / '.agents/readiness.json').write_text(json.dumps({'approved_plan_id': plan['plan_id']}))
        self.assertEqual(readiness.main(['plan', '--root', str(root)]), 3)

    def test_uninstalled_owners_add_no_items(self):
        root = self.repo({'.gitignore': '.agents/*\n'})
        empty = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: subprocess.run(['rm', '-rf', str(empty)]))
        ids = self.items(readiness.plan(root, INDEX, skills_root=empty))
        self.assertNotIn('footprint:.agents/verification.json', ids)

    def test_ignore_rules_only_for_tools_in_use(self):
        owners = self.owners('project-learning')
        unused = self.items(readiness.plan(self.repo({}), INDEX, skills_root=owners))
        self.assertNotEqual(unused['footprint:.codex/project-learning/state/']['state'], 'needs-owner')
        used = self.items(readiness.plan(self.repo({'.codex/project-learning/config.json': '{}'}), INDEX, skills_root=owners))
        self.assertEqual(used['footprint:.codex/project-learning/state/']['state'], 'needs-owner')

    def test_instruction_line_and_approval_make_the_project_ready(self):
        root = self.repo({})
        plan = readiness.plan(root, INDEX)
        self.assertEqual(self.items(plan)['instruction']['state'], 'needs-owner')
        self.assertEqual(readiness.plan(root, INDEX)['plan_id'], plan['plan_id'])
        (root / '.agents').mkdir()
        (root / '.agents/readiness.json').write_text(json.dumps({'approved_plan_id': plan['plan_id']}))
        approved = readiness.plan(root, INDEX)
        self.assertEqual(approved['plan_id'], plan['plan_id'])
        self.assertEqual(approved['status'], 'approved')  # approval alone is not readiness
        (root / 'AGENTS.md').write_text('Run the `project-readiness` skill at start.\n')
        changed = readiness.plan(root, INDEX)
        self.assertEqual(self.items(changed)['instruction']['state'], 'satisfied')
        self.assertNotEqual(changed['plan_id'], plan['plan_id'])
        self.assertEqual(changed['status'], 'ready')  # applying the last item makes it ready

    def test_outside_git_is_never_ready_even_when_approved(self):
        root = self.repo({'AGENTS.md': 'project-readiness'}, git=False)
        plan = readiness.plan(root, INDEX)
        self.assertEqual(plan['status'], 'unavailable')
        (root / '.agents').mkdir()
        (root / '.agents/readiness.json').write_text(json.dumps({'approved_plan_id': plan['plan_id']}))
        self.assertEqual(readiness.plan(root, INDEX)['status'], 'unavailable')

    def test_decline_holds_only_for_the_same_plan(self):
        root = self.repo({})
        plan = readiness.plan(root, INDEX)
        (root / '.agents').mkdir()
        (root / '.agents/readiness.json').write_text(json.dumps({'declined_plan_id': plan['plan_id']}))
        self.assertEqual(readiness.plan(root, INDEX)['status'], 'declined')
        (root / '.gitignore').write_text('.agents/*\n')
        self.assertEqual(readiness.plan(root, INDEX)['status'], 'needs-owner')

    def test_plan_and_map_write_nothing(self):
        root = self.repo({'Package.swift': '', '.gitignore': '.agents/*\n'})
        before = snapshot(root)
        readiness.plan(root, INDEX)
        readiness.situation_map(root, INDEX)
        self.assertEqual(snapshot(root), before)

    def test_situation_map_lists_applicable_and_unmanaged_skills(self):
        root = self.repo({'App/View.swift': 'import SwiftUI\n'})
        installed = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: subprocess.run(['rm', '-rf', str(installed)]))
        for name in ('swiftui-pro', 'someone-elses-skill'):
            (installed / name).mkdir()
            (installed / name / 'SKILL.md').write_text('---\nname: x\n---\n')
        text = readiness.situation_map(root, INDEX, installed)
        self.assertIn('`swiftui` work', text)
        self.assertIn('`swiftui-expert-skill`', text)
        self.assertIn('not managed by the toolkit: `someone-elses-skill`', text)
        default = readiness.situation_map(root, INDEX)  # defaults to the installed skills folder
        self.assertNotIn('`project-readiness`, ', default.split('not managed', 1)[-1])

    def test_pins_match_file_digests(self):
        folder = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: subprocess.run(['rm', '-rf', str(folder)]))
        policy, validator = folder / 'policy.json', folder / 'checkpoint.py'
        policy.write_text('{}')
        validator.write_text('print(1)')
        out = readiness.pins(policy, validator)
        self.assertEqual(out['policy_sha256'], hashlib.sha256(b'{}').hexdigest())
        self.assertEqual(out['validator_sha256'], hashlib.sha256(b'print(1)').hexdigest())
        self.assertIn('--trusted-policy', out['command'])
        job = readiness.ci_template('.claude/skills', 'policy.json', 'receipt.json')
        self.assertIn('workflow-orchestrator/references/skill-routing.json', job)  # the index travels with the checkpoint
        self.assertIn('$RUNNER_TEMP/trusted/integrated-workflow/scripts/checkpoint.py', job)

    @unittest.skipUnless(checkpoint, 'integrated-workflow is not in this selection')
    def test_checkpoint_start_includes_readiness_and_never_blocks_on_it(self):
        summary = checkpoint.readiness_summary(self.repo({}))
        self.assertIn(summary['status'], ('ready', 'needs-owner', 'unavailable'))

    def test_core_and_every_entry_skill_wire_readiness(self):
        core = json.loads((ROOT / 'catalog/skills.yaml').read_text())['packs']['core']['skills']
        self.assertIn('project-readiness', core)
        for entry in ('create-plan', 'claude-forge', 'codex-forge', 'cursor-forge', 'devin-forge',
                      'universal-forge', 'integrated-workflow'):
            if not (SKILLS / entry / 'SKILL.md').is_file():
                continue  # selected archives carry only their own entries
            with self.subTest(entry=entry):
                body = (SKILLS / entry / 'SKILL.md').read_text().split('---', 2)[2]
                self.assertIn('project-readiness', body[:600])


if __name__ == '__main__':
    unittest.main()
