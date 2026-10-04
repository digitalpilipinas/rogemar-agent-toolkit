import hashlib
import io
from contextlib import redirect_stdout
import importlib.util
import json
from pathlib import Path
from datetime import datetime, timezone
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'plugins/rogemar-agent-toolkit/skills'

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value

ROUTES = module('readiness_catalog', ROOT / 'scripts/routing_catalog.py')
SELECT = module('readiness_select', SKILLS / 'workflow-orchestrator/scripts/select_methods.py')
DOCTOR = module('readiness_doctor', ROOT / 'scripts/capability_doctor.py')
TOOLKIT = module('readiness_toolkit', ROOT / 'scripts/toolkit.py')


class SelectedReadinessTests(unittest.TestCase):
    def setUp(self):
        self.index = ROUTES.expected_index(ROOT)
        self.context = {'harness': 'cursor', 'platform': 'darwin', 'task_tags': ['swiftui'],
                        'readiness': {'candidate': 'current', 'observed_at': datetime.now(timezone.utc).isoformat(),
                         'capabilities': {'xcode': {'installed': True, 'discoverable': True, 'exercised': 'passed'}}}}

    def route(self, name='swiftui-expert-skill', **kwargs):
        if name not in self.index['skills']:
            self.skipTest('Specialist not selected in this distribution')
        return SELECT.resolve(self.index, [name], SKILLS, context=self.context, candidate='current', **kwargs)['methods'][0]

    def test_task_cases_and_unrelated_work(self):
        cases = {'swiftui-expert-skill': 'swiftui', 'swift-concurrency': 'swift-concurrency',
                 'swiftdata-pro': 'swiftdata', 'swift-testing-pro': 'swift-testing',
                 'xcode-build-benchmark': 'xcode-performance', 'e2e': 'e2e', 'codebase-design': 'architecture'}
        for method, tag in cases.items():
            if method not in self.index['skills']:
                continue
            self.context['task_tags'] = [tag]
            self.assertNotEqual(self.route(method)['status'], 'blocked')
            self.context['task_tags'] = ['unrelated-copy-edit']
            self.assertEqual(self.route(method)['status'], 'blocked')

    def test_static_source_needs_no_auth_but_runtime_needs_current_observation(self):
        self.context['readiness'] = {}
        self.assertNotEqual(self.route()['status'], 'blocked')
        self.assertEqual(self.route(runtime=True)['status'], 'blocked')
        self.setUp()
        self.assertEqual(self.route(runtime=True)['status'], 'prerequisites-observed; execution-unverified')
        self.context['readiness']['candidate'] = 'previous'
        self.assertEqual(self.route(runtime=True)['status'], 'blocked')
        self.setUp(); self.context['platform'] = 'linux'
        self.assertEqual(self.route(runtime=True)['status'], 'blocked')
        self.setUp(); self.context['readiness']['invalidated'] = True
        self.assertEqual(self.route(runtime=True)['status'], 'blocked')

    def test_overlap_requires_coverage_reason(self):
        if 'swiftui-pro' not in self.index['skills']:
            self.skipTest('Swift pack absent')
        with self.assertRaises(ValueError):
            SELECT.resolve(self.index, ['swiftui-pro', 'swiftui-expert-skill'], SKILLS, context=self.context)
        self.context['overlap_reason'] = 'Review API usage after implementation diagnostics'
        result = SELECT.resolve(self.index, ['swiftui-pro', 'swiftui-expert-skill'], SKILLS, context=self.context)
        self.assertEqual(len(result['methods']), 2)

    def test_task_handoffs_reselect_and_reuse_only_applicable_methods(self):
        # Behavioral fixture, not proof of native agent dispatch or compliance.
        if 'swiftui-expert-skill' not in self.index['skills']:
            self.skipTest('Swift pack absent')
        first = self.route(runtime=True)
        self.assertNotEqual(first['status'], 'blocked')
        self.assertEqual(self.route(runtime=True), first)  # unchanged observations
        self.context['task_tags'] = ['e2e']
        self.assertEqual(self.route()['status'], 'blocked')  # stale method choice
        self.context['execution'] = {'surface':'browser', 'mode':'deterministic'}
        for name in ('node', 'e2e', 'e2e-web'):
            self.context['readiness']['capabilities'][name] = {'installed':True, 'discoverable':True, 'exercised':'passed'}
        self.assertNotEqual(self.route('e2e', runtime=True)['status'], 'blocked')
        self.context = {'task_tags':['small-doc-fix']}
        result = SELECT.resolve(self.index, [], SKILLS, context=self.context)
        self.assertEqual(result['methods'], [])  # no forced specialist or login

    def test_external_pin_conflict_and_missing_reference_are_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); skill=root/'sample'; skill.mkdir()
            data='---\nname: sample\ndescription: Scoped method\n---\nRead reference.md'
            (skill/'SKILL.md').write_text(data)
            route={'source':'sample/SKILL.md', 'activation':'conditional', 'outcome':'method',
                   'boundary':'scope', 'source_sha256':hashlib.sha256(data.encode()).hexdigest(),
                   'required_resources':['reference.md']}
            index={'schema_version':1, 'dispatcher':'workflow-orchestrator', 'skills':{'sample':route}}
            def resolve(): return SELECT.resolve(index,['sample'],root)['methods'][0]
            self.assertEqual(resolve()['status'],'blocked')
            (skill/'reference.md').write_text('instructions')
            self.assertNotEqual(resolve()['status'],'blocked')
            (skill/'SKILL.md').write_text(data+' local edit')
            self.assertEqual(resolve()['status'],'blocked')

    def test_worker_runtime_does_not_inherit_parent_capabilities(self):
        if 'swiftui-expert-skill' not in self.index['skills']:
            self.skipTest('Swift pack absent')
        brief={'owner':'main','role':'implementation','allowed_files':['view.swift'],
               'non_goals':['deployment'],'authority':'approved-task-write',
               'required_evidence':['affected behavior'],'instructions':['read selected skill'],
               'candidate':'current','methods':['swiftui-expert-skill']}
        def resolve():
            return SELECT.resolve(self.index,brief['methods'],SKILLS,context=self.context,
                candidate='current',runtime=True,worker_brief=brief)
        self.assertEqual(resolve()['worker_brief']['status'],'blocked-by-worker-readiness')
        brief['context']={'task_tags':['swiftui'],'platform':'linux','readiness':{}}
        self.assertEqual(resolve()['worker_brief']['status'],'blocked-by-worker-readiness')
        brief['context']=self.context
        self.assertEqual(resolve()['worker_brief']['status'],'contract-complete')
        self.assertEqual(resolve()['worker_brief']['runtime_dispatch'],'unverified')

    def test_missing_resources_duplicates_and_explicit_external(self):
        with tempfile.TemporaryDirectory() as tmp:
            a, b = Path(tmp)/'one', Path(tmp)/'two'
            for root in (a,b):
                (root/'external').mkdir(parents=True)
                (root/'external/SKILL.md').write_text('---\nname: external\n---\nInstructions')
            index = {'schema_version': 1, 'dispatcher': 'workflow-orchestrator', 'skills': {
                'external': {'source':'external/SKILL.md','activation':'conditional','outcome':'method','boundary':'scope', 'required_resources':['reference.md']}}}
            result = SELECT.resolve(index,['external'],a,additional_roots=[b])['methods'][0]
            self.assertEqual(result['status'],'blocked')
            self.assertEqual(len(result['issues']),2)
            (a/'external/reference.md').write_text('resource')
            (b/'external/SKILL.md').unlink()
            (b/'external/SKILL.md').symlink_to(a/'external/SKILL.md')
            self.assertNotEqual(SELECT.resolve(index,['external'],a,additional_roots=[b])['methods'][0]['status'],'blocked')
            (a/'external/SKILL.md').write_text('---\nname: external\ndisable-model-invocation: true\n---\nInstructions')
            with self.assertRaises(ValueError): SELECT.resolve(index,['external'],a)
            SELECT.resolve(index,['external'],a,explicit=['external'])
            for value in ('true # explicit invocation required', 'TRUE # explicit'):
                (a/'external/SKILL.md').write_text('---\nname: external\ndisable-model-invocation: '+value+'\n---\nInstructions')
                with self.assertRaisesRegex(ValueError, 'explicit invocation'):
                    SELECT.resolve(index,['external'],a)
                SELECT.resolve(index,['external'],a,explicit=['external'])

    def test_worker_harness_must_support_selected_source_but_not_native_fallback(self):
        if 'forge-how' not in self.index['skills']:
            self.skipTest('Native companion not selected in this distribution')
        brief={'owner':'main','role':'investigation','allowed_files':['source.py'],
               'non_goals':['writes'],'authority':'read-only',
               'required_evidence':['source trace'],'instructions':['read selected method'],
               'candidate':'current','methods':['forge-how'],
               'context':{'harness':'cursor'}}
        def resolve(harness):
            return SELECT.resolve(self.index,brief['methods'],SKILLS,context={'harness':harness},
                                  candidate='current',runtime=True,worker_brief=brief)
        result=resolve('codex')
        self.assertEqual(result['methods'][0]['route'],'source')
        self.assertEqual(result['worker_brief']['status'],'blocked-by-worker-readiness')
        brief['context']['harness']='codex'
        self.assertEqual(resolve('codex')['worker_brief']['status'],'contract-complete')
        brief['context']['harness']='cursor'
        result=resolve('cursor')
        self.assertEqual(result['methods'][0]['route'],'fallback')
        self.assertEqual(result['worker_brief']['status'],'contract-complete')

    def test_e2e_provider_and_mobile_are_separate(self):
        self.context.update(task_tags=['e2e'], execution={'surface':'browser','mode':'deterministic'})
        caps = self.context['readiness']['capabilities']
        for name in ('node','e2e','e2e-web','e2e-mobile'):
            caps[name] = {'installed':True,'discoverable':True,'exercised':'passed'}
        self.assertNotEqual(self.route('e2e',runtime=True)['status'],'blocked')
        self.context['execution'].update(mode='agent-driven',provider='approved-provider',provider_authorized=True,max_steps=3,timeout_seconds=30,max_cost=1)
        caps['model-provider'] = {'installed':True,'discoverable':True,'exercised':'passed','authenticated':'unverified'}
        self.assertEqual(self.route('e2e',runtime=True)['status'],'blocked')
        caps['model-provider']['authenticated']='passed'
        self.assertNotEqual(self.route('e2e',runtime=True)['status'],'blocked')
        self.context['execution']['max_cost'] = float('inf')
        self.assertEqual(self.route('e2e',runtime=True)['status'],'blocked')
        self.context['execution']={'surface':'ios','mode':'deterministic'}
        self.assertEqual(self.route('e2e',runtime=True)['status'],'blocked')

    def test_receipt_integrity_and_worker_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            artifact=Path(tmp)/'run.json';artifact.write_text('{"assertions":1}')
            record={'status':'passed','candidate':'current','artifact':str(artifact),'sha256':hashlib.sha256(artifact.read_bytes()).hexdigest()}
            self.context['evidence']={'affected-behavior':record}
            self.assertNotEqual(self.route(acceptance=True)['status'],'blocked')
            artifact.write_text('changed')
            self.assertEqual(self.route(acceptance=True)['status'],'blocked')
        brief={'owner':'main','role':'review','allowed_files':['source.swift'],'non_goals':['writes'],
               'authority':'read-only','required_evidence':['review findings'],'instructions':['project policy'],
               'candidate':'current','methods':['swiftui-expert-skill']}
        self.assertFalse(SELECT.validate_brief(brief,brief['methods'],'current')['grants_authority'])
        brief['methods']=['unvalidated']
        with self.assertRaises(ValueError): SELECT.validate_brief(brief,['swiftui-expert-skill'],'current')
        for invalid in ([], {'readiness':[]}, {'task_tags':'swiftui'}, {'evidence':{'a':None}}):
            with self.assertRaises(ValueError): SELECT.validate_context(invalid)


class ScopedDoctorTests(unittest.TestCase):
    def test_managed_link_content_and_missing_resource(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); installed=root/'skills'; source=root/'source'; installed.mkdir(); source.mkdir()
            (source/'SKILL.md').write_text('instructions')
            (installed/'example').symlink_to(source, target_is_directory=True)
            digest=TOOLKIT.tree_digest(source)[0]
            state={'skills':{'example':{'sha256':digest}}}
            catalog={'harnesses':['agent-skills'],'vendored':[{'name':'example','required_resources':[]}]}
            def check():
                out=io.StringIO()
                with redirect_stdout(out):
                    args=TOOLKIT.build_parser().parse_args(['doctor','--method','example','--json'])
                    code=TOOLKIT.command_doctor(args)
                return code,json.loads(out.getvalue())
            with patch.object(TOOLKIT,'structural_errors',return_value=[]), patch.object(TOOLKIT,'load_json',return_value=catalog), patch.object(TOOLKIT,'target_paths',return_value=(installed,root/'state',root)), patch.object(TOOLKIT,'read_optional_state',return_value=state), patch.object(TOOLKIT,'destination_for',return_value=installed/'example'):
                code,result=check()
                self.assertEqual(code,0)
                self.assertTrue(result['skills']['example']['managed_hash_matches'])
                self.assertEqual(result['skills']['example']['harness_discovery'],'unverified')
                catalog['vendored'][0]['required_resources']=['missing.py']
                code,result=check()
                self.assertEqual(code,1)
                self.assertFalse(result['skills']['example']['installed'])

    def test_no_implicit_auth_or_processes(self):
        with patch.object(DOCTOR.shutil,'which',return_value='/bin/gh'), patch.object(DOCTOR,'probe') as probe:
            result=DOCTOR.inspect_capabilities(['github'])
            self.assertEqual(set(result['capabilities']),{'github'})
            self.assertEqual(result['capabilities']['github']['authenticated'],'unverified')
            probe.assert_not_called()
        with patch.object(DOCTOR.shutil,'which',return_value=None):
            self.assertFalse(DOCTOR.inspect_capabilities(['xcode'])['capabilities']['xcode']['installed'])

    def test_auth_failure_and_version_are_not_feature_proof(self):
        with patch.object(DOCTOR.shutil,'which',return_value='/bin/gh'), patch.object(DOCTOR,'probe',return_value='failed'):
            row=DOCTOR.inspect_capabilities(['github'],auth_check=True,exercise=True)['capabilities']['github']
            self.assertEqual(row['authenticated'],'failed')
            self.assertEqual(row['functional_evidence'],'unverified')
        with patch.object(DOCTOR.subprocess,'run') as run:
            run.return_value.returncode=0; run.return_value.stderr=b''
            run.return_value.stdout=b'Not authenticated'
            self.assertEqual(DOCTOR.probe(['/bin/coderabbit','auth','status']),'failed')
            run.return_value.stdout=b'v20.18.0\n'
            self.assertEqual(DOCTOR.probe(['/bin/node','--version']),'failed')
            run.return_value.stdout=b'v22.12.0\n'
            self.assertEqual(DOCTOR.probe(['/bin/node','--version']),'passed')

    def test_exact_project_engine_versions_not_global_npx(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest=Path(tmp)/'node_modules/@e2e-dev/web/package.json';manifest.parent.mkdir(parents=True)
            manifest.write_text('{"version":"0.11.0"}')
            row=DOCTOR.inspect_capabilities(['e2e-web'],project_root=tmp)['capabilities']['e2e-web']
            self.assertTrue(row['installed']);self.assertFalse(row['discoverable'])
            manifest.write_text('{"version":"0.12.0"}')
            row=DOCTOR.inspect_capabilities(['e2e-web'],project_root=tmp)['capabilities']['e2e-web']
            self.assertTrue(row['discoverable']);self.assertEqual(row['exercised'],'unverified')

if __name__ == '__main__': unittest.main()
