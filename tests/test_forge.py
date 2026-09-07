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

class ModeTests(unittest.TestCase):
    def request(self, mode="optimize", model="gpt-5.6-terra", effort="medium"):
        return {"parent": {"model": "gpt-6-astra", "effort": "max"},
                "catalog": [{"model": m, "efforts": list(router.EFFORT_RANK)} for m in router.MODEL_RANK],
                "mode": mode, "candidates": [{"model": model, "effort": effort, "reason": "qualified bounded task"}]}

    def test_exact_owner_pools_and_forbidden_neighbors(self):
        expected = {
            "peak": {m: {"low", "medium", "high", "xhigh", "max"} for m in ("gpt-6-astra", "gpt-5.6-sol", "gpt-5.6-terra")},
            "balanced": {"gpt-5.6-sol": {"low", "medium", "high", "xhigh"}, "gpt-5.6-terra": {"low", "medium", "high", "xhigh"}, "gpt-5.6-luna": {"max"}},
            "lean": {"gpt-5.6-terra": {"low", "medium", "high"}, "gpt-5.6-luna": {"high", "max"}},
            "sprint": {"gpt-5.6-terra": {"medium"}, "gpt-5.6-luna": {"low", "medium", "high", "max"}}}
        self.assertEqual(set(router.MODE_PROFILES), set(expected))
        for mode, profiles in expected.items():
            for m in router.MODEL_RANK:
                for e in router.EFFORT_RANK:
                    with self.subTest(mode=mode, model=m, effort=e):
                        result = router.resolve(self.request(mode,m,e))
                        self.assertEqual(result["status"] == "ready", e in profiles.get(m,set()))
        with self.assertRaises(ValueError): router.resolve(self.request("typo"))

    def test_inheritance_cannot_escape_mode(self):
        r=self.request();r["parent"]["effort"]="medium"
        for alias in ("inherit-parent", "auto"):
            r["candidates"]=[{"model":alias}]
            self.assertEqual(router.resolve(r)["status"],"blocked")
            r["mode"]="supreme"
            self.assertEqual(router.resolve(r)["requested"],{})
            r["mode"]="optimize"
        del r["candidates"]
        self.assertEqual(router.resolve(r)["status"],"blocked")

    def test_mode_supersedes_parent_defaults_but_legacy_keeps_ceilings(self):
        r=self.request("optimize","gpt-5.6-luna","max")
        r["parent"]["effort"]="medium"
        self.assertEqual(router.resolve(r)["status"],"ready")
        legacy=copy.deepcopy(r);del legacy["mode"]
        self.assertEqual(router.resolve(legacy)["status"],"blocked")
        r["parent"]["effort"]="max"
        self.assertEqual(router.resolve(r)["status"],"ready")
        r=self.request("supreme","gpt-5.6-sol","low")
        r["parent"]={"model":"gpt-5.6-terra","effort":"max"}
        self.assertEqual(router.resolve(r)["status"],"ready")
        legacy=copy.deepcopy(r);del legacy["mode"]
        self.assertEqual(router.resolve(legacy)["status"],"blocked")
        r["parent"]["model"]="gpt-6-astra"
        self.assertEqual(router.resolve(r)["status"],"ready")

    def test_unknown_metadata_and_catalog_fail_closed(self):
        r=self.request()
        for field in ("parent", "catalog"):
            c=copy.deepcopy(r);del c[field]
            self.assertEqual(router.resolve(c)["status"],"blocked")
        r["catalog"]=[x for x in r["catalog"] if x["model"]!="gpt-5.6-terra"]
        self.assertEqual(router.resolve(r)["status"],"blocked")

    def test_role_pins_and_mode_do_not_bypass_qualification(self):
        r=self.request("budget","gpt-5.6-terra","medium")
        r["role_config"]={"model":"gpt-6-astra","effort":"medium"}
        result=router.resolve(r)
        self.assertEqual(result["status"],"blocked")
        self.assertTrue(any("outside" in x for x in result["rejected"][0]["reasons"]))
        r["role_config"]={"model":"gpt-5.6-terra","effort":"medium"}
        self.assertEqual(router.resolve(r)["status"],"ready")
        self.assertIsNone(router.resolve(r)["observed_effective"])

    def test_preferences_and_task_override_are_distinct(self):
        pref={"schema_version":2,"active_mode":"budget","policy":"adaptive","parent_policy":"mode-adaptive","roles":{}}
        r=self.request("supreme","gpt-6-astra","medium");r["preferences"]=pref
        self.assertEqual(router.resolve(r)["status"],"ready")
        del r["mode"]
        self.assertEqual(router.resolve(r)["status"],"blocked")
        r["mode"]=None
        self.assertEqual(router.resolve(r)["status"],"blocked")
        self.assertEqual(pref["active_mode"],"budget")

    def test_atomic_switches_preserve_roles_backup_and_parent_config(self):
        with tempfile.TemporaryDirectory() as d:
            f=Path(d)/"forge.json";global_config=Path(d)/"config.toml"
            global_config.write_text('model = "gpt-6-astra"')
            old={"schema_version":1,"policy":"adaptive","parent_policy":"suggest-at-phase-boundaries","roles":{"how explorer":{"preferred_models":["inherit-parent"]}}}
            f.write_text(json.dumps(old))
            for mode in ("peak","balanced","lean","sprint","peak"):
                before=f.read_bytes();receipt=router.set_mode(f,mode)
                self.assertEqual(Path(receipt["backup"]).read_bytes(),before)
                actual=json.loads(f.read_text());self.assertEqual(actual["active_mode"],router.normalize_mode(mode))
                self.assertEqual(actual["roles"],{"how-explorer":{"preferred_models":["inherit-parent"]}})
                self.assertEqual(actual["parent_policy"],"mode-adaptive")
                self.assertFalse(receipt["parent_changed"])
            self.assertEqual(router.set_mode(f,"supreme")["status"],"unchanged")
            self.assertEqual(global_config.read_text(),'model = "gpt-6-astra"')
            self.assertEqual(list(Path(d).glob(".forge-*")),[])

    def test_malformed_and_colliding_preferences_are_not_overwritten(self):
        with tempfile.TemporaryDirectory() as d:
            f=Path(d)/"forge.json";f.write_text('{broken')
            with self.assertRaises(ValueError):router.set_mode(f,"budget")
            self.assertEqual(f.read_text(),'{broken')
            v={"schema_version":1,"policy":"adaptive","parent_policy":"suggest-at-phase-boundaries","roles":{"how explorer":{"preferred_models":["auto"]},"how-explorer":{"preferred_models":["auto"]}}}
            with self.assertRaises(ValueError):router.migrate_preferences(v)
            f.write_text(json.dumps(v));before=f.read_bytes()
            with self.assertRaises(ValueError):router.set_mode(f,"optimize")
            self.assertEqual(f.read_bytes(),before)
            link=Path(d)/"link";link.symlink_to(f)
            with self.assertRaises(ValueError):router.set_mode(link,"supreme")

    def test_v2_mode_and_parent_policy_must_agree(self):
        for mode, policy in [("budget","suggest-at-phase-boundaries"),(None,"mode-adaptive")]:
            v={"schema_version":2,"active_mode":mode,"parent_policy":policy,"policy":"adaptive","roles":{}}
            with self.assertRaises(ValueError):router.validate_preferences(v)

    def test_parent_profile_adaptation_is_a_proposal_not_a_switch(self):
        r=self.request("budget","gpt-5.6-terra","high")
        r["target"]="parent"
        result=router.resolve(r)
        self.assertEqual(result["status"],"ready")
        self.assertEqual(result["parent_adaptation"]["desired"],{"model":"gpt-5.6-terra","effort":"high"})
        self.assertTrue(result["parent_adaptation"]["change_needed"])
        self.assertFalse(result["parent_adaptation"]["runtime_switch_performed"])

    def test_normalized_user_labels_and_real_astra_id(self):
        r=self.request("supreme","gpt-6-astra","Extra High")
        self.assertEqual(router.resolve(r)["requested"]["reasoning_effort"],"xhigh")
        r["candidates"][0]["effort"]="Light"
        self.assertEqual(router.resolve(r)["requested"]["reasoning_effort"],"low")
        r["candidates"][0]["model"]="gpt-5.6-astra"
        self.assertEqual(router.resolve(r)["status"],"blocked")


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
