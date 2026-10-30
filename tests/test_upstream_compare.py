"""Read-only upstream observations must not turn missing evidence into current."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock

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

    def trees(self, before, after, truncated=False):
        pin, head = 'a' * 40, 'b' * 40
        responses = {
            'owner/repo/commits/HEAD': {'sha': head},
            f'owner/repo/compare/{pin}...{head}': dict(status='ahead', files=[dict(filename='x', status='modified')] * 300),
            f'owner/repo/git/trees/{pin}:skills': {'tree': [dict(path='selected', type='tree', sha='old')]},
            f'owner/repo/git/trees/{head}:skills': {'tree': [dict(path='selected', type='tree', sha='new')]},
            f'owner/repo/git/trees/{pin}:skills/selected?recursive=1': {'tree': before},
            f'owner/repo/git/trees/{head}:skills/selected?recursive=1': {'tree': after, 'truncated': truncated}}
        return lambda path: responses[path]

    def test_capped_comparison_diffs_selected_paths_directly(self):
        blob = lambda name, sha: dict(path=name, type='blob', sha=sha)
        result = upstream.compare(self.source, self.trees(
            [blob('SKILL.md', '1'), blob('old.md', '2')], [blob('SKILL.md', '3'), blob('new.md', '4')]))
        self.assertEqual((result['status'], result['scope'], result['method']), ('changed', 'selected-content', 'tree'))
        self.assertEqual({f['path']: f['status'] for f in result['files']}, {
            'skills/selected/SKILL.md': 'modified', 'skills/selected/old.md': 'removed',
            'skills/selected/new.md': 'added'})
        self.assertEqual(upstream.compare(self.source, self.trees([], [], truncated=True))['status'], 'unavailable')

    def test_adaptation_pins_supersede_archive_pins(self):
        source = upstream.sources(ROOT)['mattpocock/skills']
        self.assertIn('skills/productivity/grilling', source['paths'])
        self.assertNotEqual(set(source['path_pins'].values()), {source['pinned']})
        reviewed = upstream.sources(ROOT)['cursor/plugins']['path_pins']
        self.assertEqual(set(reviewed.values()), {'4dd1d05818d19792e7cd6e818f1667f95f7e1dbe'})
        head = {'sha': '4dd1d05818d19792e7cd6e818f1667f95f7e1dbe'}
        request = Mock(return_value=head)
        self.assertEqual(upstream.compare(upstream.sources(ROOT)['cursor/plugins'], request)['status'], 'unchanged')
        self.assertEqual(request.call_count, 1)

    def test_sources_without_skill_rows_conservatively_compare_whole_repository(self):
        source = upstream.sources(ROOT)['tester-army/e2e']
        request = Mock(side_effect=[{'sha': 'b' * 40}, dict(status='ahead', files=[
            dict(filename='instructions/SKILL.md', status='modified')])])
        result = upstream.compare(source, request)
        self.assertEqual(result['scope'], 'selected-content')


if __name__ == '__main__':
    unittest.main()
