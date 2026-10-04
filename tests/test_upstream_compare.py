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
        for second in [OSError('network unavailable'), {}, {'status': 'behind', 'files': []},
                       {'status': 'ahead', 'files': [dict(filename='file', status='modified')] * 300}]:
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


if __name__ == '__main__':
    unittest.main()
