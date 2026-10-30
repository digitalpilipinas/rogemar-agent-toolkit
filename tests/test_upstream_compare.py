"""Read-only upstream observations must not turn missing evidence into current."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock
from urllib.error import HTTPError

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('upstream_compare', ROOT / 'scripts/upstream_compare.py')
upstream = importlib.util.module_from_spec(spec)
spec.loader.exec_module(upstream)


class UpstreamCompareTests(unittest.TestCase):
    source = dict(repository='https://github.com/owner/repo.git', pinned='a' * 40,
                  paths=['skills/selected'])

    def check(self, files, **extra):
        request = Mock(side_effect=[{'sha': 'b' * 40}, dict(status='ahead', files=files, **extra)])
        return upstream.compare(self.source, request)

    def test_unchanged_does_not_request_diff(self):
        request = Mock(return_value={'sha': 'a' * 40})
        self.assertEqual(upstream.compare(self.source, request)['status'], 'unchanged')
        self.assertEqual(request.call_count, 1)

    def test_changed_and_renamed_selected_files(self):
        result = self.check([dict(filename='archive/SKILL.md', previous_filename='skills/selected/SKILL.md', status='renamed')])
        self.assertEqual(result['status'], 'changed')
        self.assertEqual(result['selected_files'], ['skills/selected/SKILL.md'])

    def test_release_only_and_manifest_are_distinct(self):
        self.assertEqual(self.check([dict(filename='CHANGELOG.md', status='modified')])['status'], 'metadata-only')
        self.assertEqual(self.check([dict(filename='package.json', status='modified')])['status'], 'changed')

    def test_root_skill_matches_all_paths_including_release_files(self):
        request = Mock(side_effect=[{'sha': 'b' * 40}, dict(status='ahead', files=[
            dict(filename='SKILL.md', status='modified'),
            dict(filename='CHANGELOG.md', status='modified')])])
        result = upstream.compare(dict(self.source, paths=['.']), request)
        self.assertEqual(result['selected_files'], ['CHANGELOG.md', 'SKILL.md'])
        self.assertEqual(result['scope'], 'selected-content')
        self.assertEqual(result['status'], 'changed')

    def test_unavailable_malformed_diverged_and_truncated_stay_unverified(self):
        for second in [OSError('network unavailable'), {}, {'status': 'behind', 'files': []}]:
            with self.subTest(second=str(second)[:60]):
                request = Mock(side_effect=[{'sha': 'b' * 40}, second])
                self.assertEqual(upstream.compare(self.source, request)['status'], 'unavailable')
        self.assertEqual(upstream.compare(self.source, Mock(side_effect=OSError('offline')))['status'], 'unavailable')

    def test_repository_and_revision_are_validated_before_lookup(self):
        for update in [dict(repository='https://untrusted.example/repo'), dict(pinned='main')]:
            request = Mock()
            self.assertEqual(upstream.compare(dict(self.source, **update), request)['status'], 'unavailable')
            request.assert_not_called()

    def test_reads_existing_catalogs_without_mutation(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); (root / 'catalog').mkdir()
            payloads = {'skills.yaml': {'dependencies': {'fixture': {'auto_install': {
                'repository': 'owner/repo', 'commit': 'a' * 40, 'skills': {'selected': 'skills/selected'}}}}},
                'imported-sources.json': {'sources': [{'repository': 'owner/import', 'commit': 'b' * 40}],
                    'skills': [{'repository': 'owner/import', 'source': 'skills/imported'}]}}
            for name, data in payloads.items(): (root / 'catalog' / name).write_text(json.dumps(data))
            before = {p: p.read_bytes() for p in (root / 'catalog').iterdir()}
            found = upstream.sources(root)
            self.assertEqual(set(found), {'fixture', 'owner/import'})
            for p, original in before.items(): self.assertEqual(p.read_bytes(), original)
            self.assertEqual(set(root.iterdir()), {root / 'catalog'})

    def trees(self, before, after, truncated=False, pin_parent=True):
        pin, head = 'a' * 40, 'b' * 40
        selected = lambda sha: {'tree': [dict(path='selected', type='tree', sha=sha, mode='040000')]}
        responses = {
            'owner/repo/commits/HEAD': {'sha': head},
            f'owner/repo/compare/{pin}...{head}': dict(status='ahead', files=[dict(filename='x', status='modified')] * 300),
            f'owner/repo/git/trees/{pin}:skills': selected('old') if pin_parent else None,
            f'owner/repo/git/trees/{head}:skills': selected('new'),
            f'owner/repo/git/trees/{pin}:skills/selected?recursive=1': {'tree': before},
            f'owner/repo/git/trees/{head}:skills/selected?recursive=1': {'tree': after, 'truncated': truncated}}

        def request(path):
            # Unknown URLs fail the test instead of masquerading as unavailable evidence.
            if path not in responses:
                raise AssertionError('unexpected request: ' + path)
            if responses[path] is None:
                raise HTTPError(path, 404, 'Not Found', {}, None)
            return responses[path]
        return request

    def test_capped_comparison_diffs_selected_paths_directly(self):
        blob = lambda name, sha, mode='100644': dict(path=name, type='blob', sha=sha, mode=mode)
        result = upstream.compare(self.source, self.trees(
            [blob('SKILL.md', '1'), blob('old.md', '2'), blob('run.sh', '5')],
            [blob('SKILL.md', '3'), blob('new.md', '4'), blob('run.sh', '5', '100755')]))
        self.assertEqual((result['status'], result['scope'], result['method']), ('changed', 'selected-content', 'tree'))
        self.assertEqual({f['path']: f['status'] for f in result['files']}, {
            'skills/selected/SKILL.md': 'modified', 'skills/selected/old.md': 'removed',
            'skills/selected/new.md': 'added', 'skills/selected/run.sh': 'modified'})

    def test_tree_gaps_stay_unavailable(self):
        truncated = upstream.compare(self.source, self.trees([], [], truncated=True))
        self.assertEqual(truncated['status'], 'unavailable')
        self.assertIn('Truncated', truncated['error'])
        # A selected path missing at its pin (or an unreachable pin) is missing evidence, not "no change".
        missing = upstream.compare(self.source, self.trees([], [], pin_parent=False))
        self.assertEqual(missing['status'], 'unavailable')
        self.assertIn('not found at pin', missing['error'])

    def test_adaptation_pins_supersede_archive_pins(self):
        source = upstream.sources(ROOT)['mattpocock/skills']
        self.assertIn('skills/productivity/grilling', source['paths'])
        self.assertNotEqual(set(source['path_pins'].values()), {source['pinned']})
        catalog = json.loads((ROOT / 'catalog/imported-sources.json').read_text())
        reviewed = next(a['reviewed'] for a in catalog['adaptations'] if a.get('reviewed'))
        repository = next(a['repository'] for a in catalog['adaptations'] if a.get('reviewed'))
        source = upstream.sources(ROOT)[repository]
        self.assertEqual(set(source['path_pins'].values()), {reviewed})
        request = Mock(return_value={'sha': reviewed})
        self.assertEqual(upstream.compare(source, request)['status'], 'unchanged')
        self.assertEqual(request.call_count, 1)

    def test_sources_without_skill_rows_conservatively_compare_whole_repository(self):
        source = upstream.sources(ROOT)['tester-army/e2e']
        request = Mock(side_effect=[{'sha': 'b' * 40}, dict(status='ahead', files=[
            dict(filename='instructions/SKILL.md', status='modified')])])
        result = upstream.compare(source, request)
        self.assertEqual(result['scope'], 'selected-content')


if __name__ == '__main__':
    unittest.main()
