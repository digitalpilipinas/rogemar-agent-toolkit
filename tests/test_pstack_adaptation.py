import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'plugins/rogemar-agent-toolkit/skills'
if not (SKILLS / 'codex-forge').is_dir():
    raise unittest.SkipTest('Forge was not selected for this distribution')


class PStackAdaptationTests(unittest.TestCase):
    def test_pinned_delta_dispositions_cover_added_and_removed_resources(self):
        manifest = json.loads((ROOT / 'catalog/codex-forge-upstream.json').read_text())
        self.assertEqual(manifest['commit'], '12d587dfb20741cafc376c42c696c5f6e2a64487')
        self.assertEqual(manifest['previous_commit'], '93b00b89ef425a9c1bac0d0b317dfc49c930ac99')
        deltas = manifest['deltas']
        self.assertEqual(len({row['path'] for row in deltas}), 100)
        files = {row['upstream']: row for row in manifest['files']}
        legacy = {row['upstream']: row for row in manifest['legacy_compatibility']}
        for delta in deltas:
            self.assertIn(delta['disposition'], {'adopt', 'adapt', 'retain', 'exclude'})
            self.assertTrue(delta['reason'])
            for destination in delta['destinations']:
                self.assertTrue((ROOT / destination).is_file(), destination)
            if delta['status'] == 'removed':
                self.assertNotIn(delta['path'], files)
                self.assertEqual(delta['old'], legacy[delta['path']]['upstream_sha256'])
            else:
                self.assertEqual(delta['new'], files[delta['path']]['upstream_sha256'])
        self.assertEqual(len(files), 158)
        self.assertEqual(len(legacy), 2)
        catalog = json.loads((ROOT / 'catalog/skills.yaml').read_text())
        registered = manifest['registered_skills']
        for key in ['attack-the-premise', 'test-behavior-not-implementation']:
            name = 'forge-principle-' + key
            self.assertEqual(registered['principle-' + key], name)
            self.assertIn(name, {row['name'] for row in catalog['vendored']})
            self.assertIn(name, catalog['packs']['engineering']['skills'])
            self.assertEqual((SKILLS / name / 'LICENSE.txt').read_bytes(), (SKILLS / 'codex-forge/LICENSE.txt').read_bytes())

    def test_portable_method_sources_match_reviewed_native_sources(self):
        mapping = json.loads((SKILLS / 'engineering-playbooks/references/source-map.json').read_text())
        for row in mapping['methods'] + mapping['principles']:
            self.assertEqual(row['source_sha256'], hashlib.sha256((SKILLS / row['source']).read_bytes()).hexdigest(), row['source'])
            self.assertTrue((SKILLS / 'engineering-playbooks' / row['portable']).is_file())

    def test_decision_log_initialization_preserves_existing_and_racing_records(self):
        script = SKILLS / 'forge-show-me-your-work/scripts/log.sh'
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            log = root / 'decisions.tsv'
            header = 'ts\tphase\tdecision\twhy\tevidence\tresult\n'
            def append(env=None):
                subprocess.run(['bash', str(script), str(log), 'verify', '=formula', 'line\nbreak', 'evidence', 'passed'], check=True, env=env)
            for contents in [None, '', header + 'old\trow\tstill\there\tkeep\tthis\n']:
                if contents is None:
                    if log.exists():
                        log.unlink()
                else:
                    log.write_text(contents)
                append()
                result = log.read_text()
                self.assertTrue(result.startswith(contents or header))
                self.assertIn("\t'=formula\tline break\tevidence\tpassed\n", result)
                before = result
                append()
                self.assertTrue(log.read_text().startswith(before))
            log.unlink()
            # Reproduce a writer arriving after the initialization test, before printf.
            hook = root / 'interleave.sh'
            hook.write_text('''function [() {
  builtin [ "$@"; local result=$?
  if [[ "$1" == '!' && ( "$2" == '-s' || "$2" == '-f' ) && "$3" == "$RACE_LOG" ]]; then
    printf 'existing concurrent record\\n' >> "$RACE_LOG"
  fi
  return "$result"
}
''')
            append({**os.environ, 'BASH_ENV': str(hook), 'RACE_LOG': str(log)})
            result = log.read_text()
            self.assertTrue(result.startswith('existing concurrent record\n' + header))
            self.assertIn("\t'=formula\tline break\tevidence\tpassed\n", result)
