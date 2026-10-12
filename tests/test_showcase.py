"""Generated diagram consistency, portable assets and source fidelity."""
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
SHOWCASE=ROOT/'docs/showcase'


@unittest.skipUnless(SHOWCASE.exists(),'showcase not included')
class ShowcaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec=importlib.util.spec_from_file_location('build_showcase',ROOT/'scripts/build_showcase.py')
        cls.builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.builder)

    def test_generated_diagrams_and_gallery_are_current(self):
        with tempfile.TemporaryDirectory() as temp:
            output=Path(temp)/'diagrams';shutil.copy2(SHOWCASE/'index.html',Path(temp)/'index.html')
            self.builder.build(output);self.builder.update_gallery(output)
            for p in output.iterdir():self.assertEqual(p.read_bytes(),(SHOWCASE/'diagrams'/p.name).read_bytes(),p.name)
            self.assertEqual((Path(temp)/'index.html').read_bytes(),(SHOWCASE/'index.html').read_bytes())

    def test_accessible_offline_figures_and_theme_pairs(self):
        ns={'s':'http://www.w3.org/2000/svg'}
        for p in (SHOWCASE/'diagrams').glob('*.svg'):
            svg=ET.fromstring(p.read_text());ids={x.get('id') for x in svg.iter() if x.get('id')}
            self.assertEqual(svg.get('role'),'img')
            self.assertEqual(svg[0].tag,'{http://www.w3.org/2000/svg}title')
            self.assertTrue(set(svg.get('aria-labelledby').split()) <= ids)
            self.assertEqual(len(svg.findall('s:g',ns)),len(self.builder.DIAGRAMS[p.stem.rsplit('-',1)[0]]['nodes']))
            self.assertNotIn('fonts.googleapis',p.read_text())
        html=(SHOWCASE/'index.html').read_text()
        for resource in re.findall(r'(?:src|href)="([^"]+)"',html):
            if resource.startswith(('https:', '#')):continue
            self.assertTrue((SHOWCASE/resource).is_file(),resource)
        self.assertNotIn('<iframe',html)

    def test_readme_inventory_and_static_alternative_retained(self):
        text=(ROOT/'README.md').read_text()
        for marker in ('## Complete skill inventory','## Who does what','## How delivery works','## Local and cloud environments','workflow-demo.gif','task-loop-dark.png'):
            self.assertIn(marker,text)
        # No Netscape looping extension: the illustrated GIF plays once.
        gif=(ROOT/'docs/assets/readme/workflow-demo.gif').read_bytes()
        self.assertTrue(gif.startswith(b'GIF89a'));self.assertNotIn(b'NETSCAPE2.0',gif)

    def test_deployment_is_scoped_and_not_from_prs(self):
        path=ROOT/'.github/workflows/showcase.yml'
        if not path.exists():self.skipTest('selected archive excludes CI workflows')
        text=path.read_text()
        self.assertIn('path: docs/showcase',text)
        self.assertIn("github.ref == 'refs/heads/main' && github.event_name != 'pull_request'",text)
        for action in re.findall(r'uses: (\S+)',text):self.assertRegex(action,r'@[0-9a-f]{40}$')


if __name__=='__main__':unittest.main()
