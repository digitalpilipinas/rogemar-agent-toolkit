from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('inventory_readme', ROOT / 'scripts/inventory_readme.py')
inventory = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inventory)


class InventoryReadmeTests(unittest.TestCase):
    def test_dependency_only_skill_members_and_native_install_routes_are_visible(self):
        catalog = copy.deepcopy(inventory.load_catalog())
        catalog['dependencies']['example-kit'] = {
            'kind': 'skills', 'purpose': 'Optional example methods',
            'targets': ['codex'], 'members': ['example-unique-method'],
            'install': 'install-example',
            'install_by_harness': {'codex': 'install-native-example'},
        }
        catalog['packs']['example'] = {'description': 'Example pack', 'skills': [], 'external': ['example-kit']}
        output = inventory.generated_inventory(catalog)
        self.assertIn('example-unique-method', output)
        self.assertIn('install-native-example', output)
        self.assertIn('[example-kit](#dependency-example-kit)', output)
        self.assertIn('id="dependency-example-kit"', output)

    def test_complete_dependency_metadata_and_linked_external_members_are_retained(self):
        catalog = inventory.load_catalog()
        output = inventory.generated_inventory(catalog)
        for name, dependency in catalog['dependencies'].items():
            self.assertIn(f'id="dependency-{name}"', output)
            for member in dependency.get('members', []):
                self.assertIn(member, output)
            if dependency.get('skill_group'):
                self.assertIn(f'id="external-{dependency["skill_group"]}"', output)
        for path in catalog['dependencies']['opendesign-library']['paths']:
            self.assertIn(path, output)
        self.assertIn('Electron renderer', output)
        self.assertIn('convex-migrate-rehearse', output)
        self.assertIn('codex-with-chatgpt', output)
        self.assertIn('webmcp-kit:verify', output)

    def test_collapsed_lists_use_escaped_html_instead_of_literal_markdown(self):
        output = inventory.members_cell(['ordinary'] * 20 + ['<script>'])
        self.assertIn('<details>', output)
        self.assertIn('<code>&lt;script&gt;</code>', output)
        self.assertNotIn('<script>', output)
        self.assertNotIn('`ordinary`', output)


if __name__ == '__main__':
    unittest.main()
