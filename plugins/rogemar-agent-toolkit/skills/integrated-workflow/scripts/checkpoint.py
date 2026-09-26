#!/usr/bin/env python3
"""Read-only checkpoint validation. Evidence integrity is not behavioral proof."""
import argparse
import fnmatch
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args])


def inside(path, root):
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def candidate(root, base):
    base = git(root, 'rev-parse', '--verify', base + '^{commit}').decode().strip()
    head = git(root, 'rev-parse', 'HEAD').decode().strip()
    paths = set(git(root, 'diff', '--name-only', '-z', base, '--').split(b'\0'))
    paths.update(git(root, 'diff', '--cached', '--name-only', '-z', base, '--').split(b'\0'))
    paths.update(git(root, 'ls-files', '--others', '--exclude-standard', '-z').split(b'\0'))
    rows = []
    for raw in sorted(paths - {b''}):
        name = os.fsdecode(raw)
        path = root / name
        if path.is_symlink():
            value, mode = os.readlink(path), 'symlink'
        elif path.is_file():
            value, mode = digest(path), str(path.stat().st_mode & 0o777)
        elif not path.exists():
            value, mode = '', 'deleted'
        else:
            raise ValueError('unsupported candidate path: ' + name)
        rows.append([name, mode, value])
    return {'base': base, 'head': head, 'content': hashlib.sha256(
        json.dumps(rows, ensure_ascii=True).encode() + git(root, 'diff', '--cached', '--binary', base, '--')).hexdigest()}, [r[0] for r in rows]


def matches(path, patterns):
    return any(fnmatch.fnmatchcase(path, p) for p in patterns)


def tree_file(root, revision, name):
    """Read a bounded regular Git blob as data; never check out candidate code."""
    path = PurePosixPath(name)
    if not name or path.is_absolute() or str(path) != name or '..' in path.parts or '\\' in name or '.git' in path.parts:
        raise ValueError('invalid tree path')
    row = git(root, 'ls-tree', '-z', revision, '--', ':(literal)' + name).split(b'\0')
    if len(row) != 2 or not row[0]:
        raise ValueError('missing tree file: ' + name)
    metadata, found = row[0].split(b'\t', 1)
    mode, kind, oid = metadata.decode().split()
    if mode not in ('100644', '100755') or kind != 'blob' or os.fsdecode(found) != name:
        raise ValueError('tree file is not a regular blob: ' + name)
    size = int(git(root, 'cat-file', '-s', oid))
    if not 0 < size <= 2 * 1024 * 1024:
        raise ValueError('tree file is empty or exceeds 2 MiB: ' + name)
    return git(root, 'cat-file', 'blob', oid)


def validate_mapping(root, mapping, revision=None):
    if not isinstance(mapping, dict):
        raise ValueError('verification map must be an object')
    if mapping.get('schema_version') != 1:
        raise ValueError('unsupported verification map schema')
    for key in ('runtime_paths', 'shared_paths', 'nonruntime_paths'):
        if not isinstance(mapping.get(key), list) or any(not isinstance(p, str) or not p for p in mapping[key]):
            raise ValueError('invalid map patterns: ' + key)
    features = mapping.get('features')
    if not isinstance(features, list) or not features:
        raise ValueError('feature map is empty')
    ids = set()
    for feature in features:
        if not isinstance(feature, dict):
            raise ValueError('feature must be an object')
        ident = feature.get('id')
        if not isinstance(ident, str) or not ident or ident in ids:
            raise ValueError('missing or duplicate feature ID')
        ids.add(ident)
        if not feature.get('paths') or not feature.get('platforms'):
            raise ValueError('feature lacks paths/platforms: ' + ident)
        for key in ('paths', 'platforms'):
            if not isinstance(feature[key], list) or any(not isinstance(x, str) or not x for x in feature[key]):
                raise ValueError('invalid feature ' + key)
        name = feature.get('recipe', '')
        recipe = root / name
        if revision:
            tree_file(root, revision, name)
        elif not inside(recipe, root) or not recipe.is_file():
            raise ValueError('missing or escaping recipe: ' + ident)
    return features


def selected_features(mapping, paths, requested):
    known = {f['id'] for f in mapping['features']}
    if set(requested) - known:
        raise ValueError('unknown requested feature')
    relevant = [p for p in paths if not matches(p, mapping['nonruntime_paths'])]
    shared = any(matches(p, mapping['shared_paths']) for p in relevant)
    selected = [f for f in mapping['features'] if shared or f['id'] in requested or
                any(matches(p, f['paths']) or p == f['recipe'] for p in relevant)]
    uncovered = [p for p in relevant if matches(p, mapping['runtime_paths']) and
                 not matches(p, mapping['shared_paths']) and
                 not any(matches(p, f['paths']) for f in mapping['features'])]
    return selected, uncovered


def check(root, base, phase, receipt, mapping, required_gates=(), boundary="accept"):
    if not isinstance(receipt, dict) or not isinstance(receipt.get('scope', {}), dict) or not isinstance(receipt.get('map_review', {}), dict):
        raise ValueError('receipt, scope and map_review must be objects')
    validate_mapping(root, mapping)
    identity, paths = candidate(root, base)
    scope = receipt.get('scope', {})
    selected, uncovered = selected_features(mapping, paths, scope.get('features', []))
    result = {'phase': phase, 'boundary': boundary, 'candidate': identity, 'changed_paths': paths,
              'selected': [{'id': f['id'], 'recipe': f['recipe'], 'platforms': f['platforms']}
                           for f in selected], 'coverage_gaps': uncovered, 'errors': [], 'deferred': []}
    if phase == 'start':
        result['status'] = 'preparation'
        result['next_action'] = 'Read selected expected behavior and accepted lessons; choose checks before editing. Resolve gaps; attempt draft proof when authorized.'
        return result
    errors = result['errors']
    if receipt.get('schema_version') != 1 or receipt.get('candidate') != identity:
        errors.append('receipt is missing or has stale candidate identity')
    if not scope.get('assessment'):
        errors.append('missing source-grounded scope assessment')
    review = receipt.get('map_review', {})
    if selected or uncovered:
        if review.get('disposition') not in ('updated', 'unchanged with reason', 'coverage gap') or not review.get('reason'):
            errors.append('missing feature-map review disposition')
        if review.get('expected_behavior_preserved') is not True:
            errors.append('expected behavior must remain authoritative; investigate product regressions')
    if uncovered or review.get('disposition') == 'coverage gap':
        errors.append('required behavior has a coverage gap')
    expected = {f["id"] + ':' + p: (f['id'], p) for f in selected for p in f['platforms']}
    for name in required_gates:
        expected.setdefault(name, (None, None))
    gates = receipt.get('gates', [])
    if not isinstance(gates, list) or any(not isinstance(g, dict) for g in gates):
        raise ValueError('gates must be an array of gate records')
    for gate in gates:
        if not isinstance(gate.get('gate'), str) or not gate['gate'].strip():
            raise ValueError('gate records require nonempty IDs')
        if gate.get('requirement') == 'required' and gate.get('boundary') == boundary:
            expected.setdefault(gate['gate'], (None, None))
    by_id = {g.get('gate'): g for g in gates}
    if len(by_id) != len(gates):
        errors.append('duplicate gate records')
    for name, (feature, platform) in expected.items():
        g = by_id.get(name, {})
        prefix = name + ': '
        if g.get('requirement') != 'required' or any(not g.get(k) for k in ('source', 'trigger', 'owner', 'boundary')):
            errors.append(prefix + 'missing required gate disposition')
        if g.get('boundary') != boundary:
            errors.append(prefix + 'wrong acceptance boundary')
        if g.get('candidate') != identity:
            errors.append(prefix + 'stale gate candidate')
        if platform and (g.get('platform') != platform or g.get('feature') != feature):
            errors.append(prefix + 'wrong feature/platform')
        if g.get('state') == 'deferred':
            if not g.get('owner_decision'):
                errors.append(prefix + 'deferral lacks owner decision')
            result['deferred'].append(name)
            continue
        if g.get('state') != 'passed':
            errors.append(prefix + 'required evidence is ' + str(g.get('state', 'missing')))
            continue
        evidence = g.get('evidence', [])
        if not isinstance(evidence, list) or any(not isinstance(item, dict) for item in evidence):
            errors.append(prefix + 'evidence must be an array of objects')
            evidence = []
        if not evidence:
            errors.append(prefix + 'no evidence artifacts')
        for artifact in evidence:
            path = Path(artifact.get('path', ''))
            if not path.is_absolute() or not path.is_file() or not path.stat().st_size:
                errors.append(prefix + 'missing/nonabsolute/empty artifact')
            elif digest(path) != artifact.get('sha256'):
                errors.append(prefix + 'artifact digest mismatch')
            if artifact.get('candidate') != identity:
                errors.append(prefix + 'artifact candidate mismatch')
            if platform and (artifact.get('platform') != platform or artifact.get('kind') != 'runtime'):
                errors.append(prefix + 'runtime artifact has wrong evidence kind/platform')
        if platform:
            runtime = g.get('runtime', {})
            if not isinstance(runtime, dict):
                errors.append(prefix + 'runtime must be an object')
                runtime = {}
            if any(not runtime.get(k) for k in ('target', 'fixture', 'actions', 'observed', 'cleanup')):
                errors.append(prefix + 'missing runtime action/outcome/cleanup record')
    result['status'] = 'rejected' if errors else 'deferred' if result['deferred'] else 'validated-record'
    result['limitations'] = 'Checks recorded identity, coverage and artifact integrity; cannot attest execution, semantic coverage or owner approval.'
    if phase == 'close':
        result['next_action'] = ('Assess at most one evidenced learning candidate using the enrolled project-learning workflow; retain its native source-turn ID. No automatic activation.'
                                 if result['status'] == 'validated-record' else 'Resolve outstanding gates; do not capture a verified-completion lesson.')
    return result


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', required=True, type=Path)
    p.add_argument('--base', required=True)
    p.add_argument('--phase', choices=['start', 'accept', 'close'], required=True)
    p.add_argument('--receipt', required=True, type=Path)
    p.add_argument('--structure', action='store_true', help='Trusted CI map check only; never runtime acceptance')
    p.add_argument('--tree', help='Full immutable commit for structure-only Git blob inspection; no candidate checkout')
    p.add_argument('--map', default='.agents/verification.json')
    p.add_argument('--trusted-policy', type=Path)
    p.add_argument('--policy-sha256')
    p.add_argument('--validator-sha256')
    a = p.parse_args(argv)
    try:
        root = a.root.resolve()
        if Path(git(root, 'rev-parse', '--show-toplevel').decode().strip()).resolve() != root:
            raise ValueError('--root must be repository root')
        if a.tree and (not a.structure or not re.fullmatch(r'[0-9a-f]{40}', a.tree)):
            raise ValueError('--tree requires --structure and a full commit SHA')
        if a.tree and git(root, 'rev-parse', '--verify', a.tree + '^{commit}').decode().strip() != a.tree:
            raise ValueError('--tree must identify a commit')
        mapping_path = root / a.map
        if not inside(mapping_path, root):
            raise ValueError('map escapes repository')
        mapping = json.loads(tree_file(root, a.tree, a.map) if a.tree else mapping_path.read_bytes())
        required = []
        boundary = "accept"
        if a.phase != 'start' or a.structure:
            if not a.trusted_policy or inside(a.trusted_policy, root) or inside(Path(__file__), root):
                raise ValueError('acceptance requires reviewed validator and policy outside candidate checkout')
            if not a.validator_sha256 or digest(__file__) != a.validator_sha256:
                raise ValueError('validator pin mismatch')
            if not a.policy_sha256 or digest(a.trusted_policy) != a.policy_sha256:
                raise ValueError('policy pin mismatch')
            policy = json.loads(a.trusted_policy.read_text())
            if policy.get('repository') != str(root) or policy.get('mapping') != mapping:
                raise ValueError('candidate changed reviewed policy; obtain separate policy review')
            required = policy.get('required_gates', [])
            boundary = policy.get('boundary', 'accept')
            if not isinstance(required, list) or any(not isinstance(x, str) or not x for x in required) or not isinstance(boundary, str) or not boundary:
                raise ValueError('invalid trusted gate/boundary policy')
        if a.structure:
            validate_mapping(root, mapping, a.tree)
            print(json.dumps({'status': 'structure-only', 'runtime': 'unverified', 'policy': a.policy_sha256, 'tree': a.tree}))
            return 0
        receipt = json.loads(a.receipt.read_text()) if a.receipt.exists() else {}
        result = check(root, a.base, a.phase, receipt, mapping, required, boundary)
        print(json.dumps(result, indent=2))
        return 1 if result['errors'] else 2 if result.get('deferred') else 0
    except (ValueError, OSError, KeyError, TypeError, subprocess.CalledProcessError) as exc:
        print(json.dumps({'status': 'rejected', 'error': str(exc)}))
        return 1


if __name__ == '__main__':
    sys.exit(main())
