import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
catalog = json.loads((Path(__file__).resolve().parents[1] / 'catalog/skills.yaml').read_text())
if 'distribution_selection' in catalog['package'] and not set(['plan-model-router']).issubset({e['name'] for e in catalog['vendored']}):
    raise unittest.SkipTest('optional skills were not selected for this distribution')

FILE=ROOT/'plugins/rogemar-agent-toolkit/skills/plan-model-router/scripts/resolve_profile.py'
spec=importlib.util.spec_from_file_location('role_router',FILE)
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)

class RoleEvidenceTests(unittest.TestCase):
    def test_qualifications_trace_exact_profiles_and_passing_artifacts(self):
        answers, batches = {}, {}
        for path in sorted((FILE.parents[1]/'references').glob('validation-v*.json')):
            data = json.loads(path.read_text())
            answers.update({a['id']: a for a in data.get('answers', [])})
            for batch in data.get('batches', []):
                batch = dict(batch)
                if 'packet_sha256' not in batch:
                    batch['packet_sha256'] = hashlib.sha256(data['packet_text'].encode()).hexdigest()
                batches[batch['id']] = batch
        records = [q for qs in r.ROUTING_CATALOG['qualified_profiles'].values() for q in qs]
        records += [q for roles in r.ROUTING_CATALOG['exceptions'].values() for qs in roles.values() for q in qs]
        for record in records:
            if not r.paired(record): continue
            profile = {k: record[k] for k in ('model', 'effort')}
            for proof in record['validation']:
                actual = answers[proof['assignment_id']]
                self.assertTrue(actual['passed'], proof)
                self.assertTrue(actual['profile_verified'], proof)
                self.assertEqual(actual['profile'], profile)
                self.assertEqual(actual['packet_sha256'], proof['packet_sha256'])
                self.assertEqual(actual['repetition'], proof['repetition'])
            for proof in record.get('coding_validation', []):
                batch_id, artifact = proof['assignment_id'].rsplit(':', 1)
                actual = batches[batch_id]
                self.assertEqual(actual.get('profile', {k: actual.get(k) for k in ('model', 'effort')}), profile)
                self.assertEqual(actual['packet_sha256'], proof['packet_sha256'])
                self.assertEqual(actual['repetition'], proof['repetition'])
                self.assertTrue(actual['profile_verified'])
                check = actual.get('artifact_adjudication', actual.get('artifact_check', actual.get('coding_check' if artifact == 'sqlite' else 'browser_check', {})))
                self.assertTrue(check.get('passed'), proof)
                self.assertEqual(record.get('evidence_contract'), 'notes-store' if artifact == 'sqlite' else 'note-editor-ui')

    def test_evidence_covers_all_policies_and_roles(self):
        evidence=json.loads((FILE.parents[1]/'references/role-evidence.json').read_text())['rows']
        self.assertEqual(len(evidence),225)
        self.assertEqual(len({(x['mode'],x['role']) for x in evidence}),225)
        for x in evidence:
            self.assertTrue(x['playbook']['purpose'])
            self.assertTrue(x['qualification_scope'])
            if x['kind']=='arrangement':
                self.assertIsNone(x['normal'])
                self.assertEqual(x['evidence_status'],'task-dependent')
                continue
            if x['mode']=='default':continue
            if x['kind']=='consequential':self.assertEqual(x['normal']['model'],r.ROUTING_CATALOG['parent_targets'][x['mode']]['model'])
            self.assertTrue(x['rationale'])
            if x['qualification_id']:
                self.assertTrue(r.qualification(x['role'],x['normal'],x['role'] in r.ROUTING_CATALOG['coding_roles']))
                self.assertIn(x['evidence_status'],('newly-verified','historically-verified'))
            elif x['kind']!='main-owned':self.assertEqual(x['evidence_status'],'provisional')
            if x['role'] in ('goal-scout','goal-judge') and x['observation']:
                self.assertEqual(x['observation']['contract'], 'ordinary-forge-worker')
                self.assertFalse(x['observation']['native_goalbuddy_gate'])

    def test_shared_cursor_metadata_unchanged(self):
        path=ROOT/'plugins/rogemar-agent-toolkit/skills/cursor-forge-setup/references/roles.json'
        if not path.exists():self.skipTest('optional Cursor package absent')
        shared={n:{k:v for k,v in cfg.items() if k!='overrides'} for n,cfg in r.ROLE_CONTRACTS.items()}
        self.assertEqual(json.loads(path.read_text())['roles'],shared)
