import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'plugins/rogemar-agent-toolkit/skills'
catalog = json.loads((Path(__file__).resolve().parents[1] / 'catalog/skills.yaml').read_text())
if 'distribution_selection' in catalog['package'] and not set(['plan-model-router', 'codex-forge']).issubset({e['name'] for e in catalog['vendored']}):
    raise unittest.SkipTest('optional skills were not selected for this distribution')

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path); value=importlib.util.module_from_spec(spec);spec.loader.exec_module(value);return value
router=module('forge_router',SKILLS/'plan-model-router/scripts/resolve_profile.py')
audit=module('forge_audit',SKILLS/'codex-forge/scripts/worktree_audit.py')

class RoutingTests(unittest.TestCase):
    def request(self):
        return {'parent':{'model':'gpt-6-astra','effort':'high'},'catalog':[{'model':m,'efforts':['low','medium','high','xhigh','max']} for m in router.MODEL_RANK]}
    def test_defaults_and_independent_ceilings(self):
        r=self.request();self.assertEqual(router.resolve(r)['requested'],{})
        r['candidates']=[{'model':'gpt-5.6-sol','effort':'high','reason':'bounded implementation'}]
        self.assertEqual(router.resolve(r)['status'],'ready')
        r['candidates'][0]['effort']='xhigh';self.assertEqual(router.resolve(r)['status'],'blocked')
        r['parent']={'model':'gpt-5.6-terra','effort':'high'};r['candidates'][0]['effort']='low';self.assertEqual(router.resolve(r)['status'],'blocked')
    def test_unknown_metadata_requires_unpinned_inheritance(self):
        for r in [{}, {'parent':{'model':'gpt-5.6-sol','effort':'high'}}]:
            self.assertEqual(router.resolve(r)['status'],'inherit-unverified')
            r['role_config']={'model':'gpt-6-astra','effort':'ultra'}
            self.assertEqual(router.resolve(r)['status'],'blocked')
    def test_unknown_family_is_not_ranked(self):
        r={'parent':{'model':'future','effort':'high'},'catalog':[{'model':'future','efforts':['high']},{'model':'gpt-5.6-luna','efforts':['low']}]}
        self.assertEqual(router.resolve(r)['status'],'ready')
        r['candidates']=[{'model':'gpt-5.6-luna','effort':'low','reason':'small'}]
        self.assertEqual(router.resolve(r)['status'],'blocked')
    def test_role_pins_cannot_mask_invalid_or_unqualified_request(self):
        r=self.request();r['role_config']={'model':'gpt-5.6-sol','effort':'high'}
        for m,e in [('missing','ultra'),('gpt-6-astra','high'),('gpt-5.6-luna','low')]:
            r['candidates']=[{'model':m,'effort':e,'reason':'qualified request'}]
            self.assertEqual(router.resolve(r)['status'],'blocked')
        r['candidates']=[{'model':'gpt-5.6-sol','effort':'high','reason':'qualified exact effective profile'}]
        self.assertEqual(router.resolve(r)['status'],'ready')
        self.assertIsNone(router.resolve(r)['observed_effective'])
    def test_preferences_are_schema_checked_without_claiming_availability(self):
        v={'schema_version':1,'policy':'adaptive','parent_policy':'suggest-at-phase-boundaries','roles':{}}
        self.assertEqual(router.validate_preferences(v),v)
        for change in [{'schema_version':2},{'roles':{'unknown':{}}},{'roles':{'feature':{'preferred_models':[]}}}]:
            with self.assertRaises(ValueError):router.validate_preferences({**v,**change})



class WorktreeTests(unittest.TestCase):
    def test_audit_protects_private_dirty_locked_unmerged_and_primary_work(self):
        with tempfile.TemporaryDirectory(prefix='forge worktree ') as temp:
            root=Path(temp); repo=root/'repo';repo.mkdir()
            def git(*a):return subprocess.run(['git','-C',str(repo),*a],check=True,capture_output=True,text=True).stdout.strip()
            git('init','-b','main');git('config','user.name','Fixture');git('config','user.email','fixture@example.invalid')
            (repo/'.gitignore').write_text('private.txt\n');(repo/'file').write_text('baseline\n')
            git('add','.gitignore','file');git('commit','-m','fixture baseline')
            paths={}
            for name in ['clean space','private','dirty','untracked','locked','unmerged']:
                p=root/name;git('worktree','add','--detach',str(p),'main');paths[name]=p
            (paths['private']/'private.txt').write_text('fixture private content')
            (paths['dirty']/'file').write_text('changed')
            (paths['untracked']/'notes').write_text('keep')
            git('worktree','lock',str(paths['locked']))
            subprocess.run(['git','-C',str(paths['unmerged']),'commit','--allow-empty','-m','unmerged fixture'],check=True,capture_output=True)
            result=audit.audit(repo,'main'); rows={Path(r['path']).name:r for r in result['worktrees']}
            self.assertEqual(rows['clean space']['classification'],'review-merged')
            for name in ['repo','private','dirty','untracked','locked','unmerged']: self.assertEqual(rows[name]['classification'],'hold')
            self.assertTrue(all(not r['deletion_authorized'] for r in result['worktrees']))
            self.assertTrue((paths['private']/'private.txt').exists())
            self.assertTrue(all(r['classification']=='hold' for r in audit.audit(repo)['worktrees']))
