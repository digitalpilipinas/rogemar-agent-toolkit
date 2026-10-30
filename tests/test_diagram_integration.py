"""The optional upstream route must not turn into a duplicate bundled skill."""
import importlib.util
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('diagram_toolkit',ROOT/'scripts/toolkit.py')
toolkit=importlib.util.module_from_spec(spec);spec.loader.exec_module(toolkit)

class DiagramIntegrationTests(unittest.TestCase):
    def test_upstream_is_declared_separately_and_never_copied_as_toolkit_skill(self):
        catalog=toolkit.load_json(toolkit.CATALOG_PATH)
        if 'design' not in catalog['packs']:self.skipTest('design omitted from package')
        for harness in ('codex','cursor','claude','droid','agent-skills','gemini'):
            selected=toolkit.resolve_selection(harness,'core',['design'])
            self.assertIn('diagram-design',selected['external'])
            self.assertIn('vector-asset-pipeline',selected['skills'])
            self.assertNotIn('diagram-design',selected['skills'])
            core=toolkit.resolve_selection(harness,'core',[])
            self.assertEqual(len(core['skills']),7)
            self.assertNotIn('diagram-design',core['external'])
        self.assertNotIn('auto_install',catalog['dependencies']['diagram-design'])
        self.assertFalse((toolkit.SKILLS_ROOT/'diagram-design').exists())
        entry=next(e for e in catalog['vendored'] if e['name']=='vector-asset-pipeline')
        for resource in entry['required_resources']:
            self.assertTrue((toolkit.SKILLS_ROOT/'vector-asset-pipeline'/resource).is_file())

if __name__=='__main__':unittest.main()
