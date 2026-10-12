"""Portable Diagram Design selection, immutable profiles, offline artifacts and exports."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'plugins/rogemar-agent-toolkit/skills'
SKILL = SKILLS / 'diagram-design'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@unittest.skipUnless(SKILL.exists(), 'diagram-design not in selected release')
class DiagramDesignTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.style = load('diagram_style', SKILL / 'scripts/resolve_style.py')
        cls.toolkit = load('diagram_toolkit', ROOT / 'scripts/toolkit.py')
        cls.guide = cls.style.DEFAULT.read_text()

    def test_pack_resources_and_core_boundary(self):
        catalog = self.toolkit.load_json(self.toolkit.CATALOG_PATH)
        for harness in ('codex', 'cursor', 'claude', 'droid', 'agent-skills'):
            self.assertIn('diagram-design', self.toolkit.resolve_selection(harness, 'all', [])['skills'])
            self.assertIn('diagram-design', self.toolkit.resolve_selection(harness, 'core', ['design'])['skills'])
            core = self.toolkit.resolve_selection(harness, 'core', [])['skills']
            self.assertEqual(len(core), 6)
            self.assertNotIn('diagram-design', core)
        entry = next(x for x in catalog['vendored'] if x['name'] == 'diagram-design')
        for name in entry['required_resources']:
            self.assertNotIn('__pycache__', name)
            self.assertFalse(name.endswith('.pyc'))
            self.assertTrue((SKILL / name).is_file(), name)
        self.assertEqual(len(list(SKILL.rglob('SKILL.md'))), 1)

    def test_profiles_are_project_scoped_and_installed_files_unchanged(self):
        before = self.toolkit.tree_digest(SKILL)[0]
        with tempfile.TemporaryDirectory() as temp:
            a, b = Path(temp)/'a', Path(temp)/'b'
            a.mkdir(); b.mkdir()
            (a/'.diagram-design-profile.md').write_text(self.guide.replace('#bf4520', '#0e7490'))
            (b/'.diagram-design-profile.md').write_text(self.guide.replace('#bf4520', '#be123c'))
            first, second = self.style.resolve(a), self.style.resolve(b)
            self.assertNotEqual(first['path'], second['path'])
            self.assertEqual(first['font_source'], 'system')
            self.assertEqual(second['source'], 'project')
            self.assertFalse(first['writes_files'])
            self.assertEqual(self.style.resolve(Path(temp))['source'], 'default')
        self.assertEqual(before, self.toolkit.tree_digest(SKILL)[0])

    def test_explicit_invalid_or_missing_legacy_profile_does_not_fall_back(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp); library=p/'profiles'; library.mkdir()
            marker=p/'.diagram-design'
            for value in ('profile: ../private', 'profile: team\nrun: anything', 'profile:'):
                marker.write_text(value)
                with self.assertRaises(ValueError): self.style.resolve(p, library)
            marker.write_text('profile: missing\n')
            with self.assertRaises(FileNotFoundError): self.style.resolve(p, library)
            marker.write_text('profile: team\n')
            legacy=library/'team.md'; legacy.write_text(self.guide)
            before=legacy.read_bytes()
            self.assertEqual(self.style.resolve(p, library)['source'], 'legacy-read-only')
            self.assertEqual(legacy.read_bytes(),before)
            profile=p/'.diagram-design-profile.md'; profile.write_text('Incomplete style')
            with self.assertRaises(ValueError): self.style.resolve(p, library)
            profile.unlink(); profile.symlink_to(p/'missing')
            with self.assertRaises(FileNotFoundError): self.style.resolve(p, library)

    def test_routing_artifacts_and_unrelated_work(self):
        routes=load('diagram_routes', ROOT/'scripts/routing_catalog.py').expected_index(ROOT)
        select=load('diagram_select', SKILLS/'workflow-orchestrator/scripts/select_methods.py')
        for tag, allowed in [('diagram-artifact',True),('diagram-redraw',True),('simple-mermaid',False),('interactive-explainer',False),('scientific-plot',False),('unrelated',False)]:
            result=select.resolve(routes,['diagram-design'],SKILLS,context={'harness':'codex','platform':'darwin','task_tags':[tag]},candidate='test')
            self.assertEqual(result['methods'][0]['status']!='blocked',allowed,tag)

    def test_offline_template_and_hostile_html(self):
        template=(SKILL/'assets/template.html').read_text()
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'example.html'
            for body, success in [(template,True),(template.replace('<body>','<body onload="fetch(1)">'),False),(template.replace('</style>','@import "https://example.com/theme.css";</style>'),False)]:
                p.write_text(body)
                result=subprocess.run([sys.executable,str(SKILL/'scripts/self_check.py'),'--offline',str(p)],capture_output=True,text=True)
                self.assertEqual(result.returncode==0,success,result.stdout+result.stderr)
            p.write_text(template)
            exported=Path(temp)/'example.svg'
            result=subprocess.run([sys.executable,str(SKILL/'scripts/export_svg.py'),str(p),str(exported),'--system-fonts'],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertNotIn('fonts.googleapis',exported.read_text())
            self.assertIn('<title',exported.read_text())
            bad=SKILL/'assets/example-datalake.html'
            result=subprocess.run([sys.executable,str(SKILL/'scripts/export_svg.py'),str(bad),str(exported),'--system-fonts'],capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0)


if __name__ == '__main__':
    unittest.main()
