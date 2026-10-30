#!/usr/bin/env python3
"""Read selected public GitHub revisions; never install, repin, or log in.

Requests are unauthenticated unless GITHUB_TOKEN is set (CI uses its read-only token).

Use during approved toolkit maintenance, not ordinary product tasks. Output is
comparison evidence, not an update recommendation or a capability readiness check.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def sources(root):
    catalog = json.loads((root / 'catalog/skills.yaml').read_text())
    imported = json.loads((root / 'catalog/imported-sources.json').read_text())
    result = {}
    for name, item in catalog['dependencies'].items():
        recipe = item.get('auto_install')
        if recipe:
            result[name] = dict(repository=recipe['repository'], pinned=recipe['commit'],
                                paths=list(recipe['skills'].values()))
    for item in imported['sources']:
        repo = item['repository']
        pins = {skill['source']: item['commit'] for skill in imported['skills'] if skill['repository'] == repo}
        for adaptation in imported.get('adaptations', []):
            if adaptation['repository'] == repo:
                # A later adaptation pin supersedes the archive pin for its paths; `reviewed`
                # records upstream changes inspected and deliberately not adopted.
                pin = adaptation.get('reviewed', adaptation.get('commit', item['commit']))
                pins.update(dict.fromkeys(adaptation.get('paths', ['.']), pin))
        # Archive-only sources have no individual skill rows: inspect all changes.
        pins = pins or {'.': item['commit']}
        result[repo] = dict(repository=repo, pinned=item['commit'], paths=sorted(pins))
        if set(pins.values()) != {item['commit']}:
            result[repo]['path_pins'] = dict(sorted(pins.items()))
    return result


def repository_name(value):
    value = value.removeprefix('https://github.com/').removesuffix('.git')
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', value):
        raise ValueError('Only declared public GitHub repositories are supported')
    return value


def get_json(path):
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'rogemar-toolkit-maintenance'}
    if os.environ.get('GITHUB_TOKEN'):
        headers['Authorization'] = 'Bearer ' + os.environ['GITHUB_TOKEN']
    request = Request('https://api.github.com/repos/' + path, headers=headers)
    with urlopen(request, timeout=30) as response:
        raw = response.read(10_000_001)
    if len(raw) > 10_000_000:
        raise ValueError('Comparison response exceeds the inspection limit')
    return json.loads(raw)


def tree_files(source, repo, head, request):
    """Diff each selected path's blobs at its own pin against head.

    Used when per-path pins differ or GitHub's 300-file compare cap hides the
    selected paths, as in large multi-plugin repositories.
    """
    listings = {}

    def listing(commit, path, recursive=False):
        key = (commit, path, recursive)
        if key not in listings:
            ref = commit if path == '.' else commit + ':' + quote(path, safe='/')
            try:
                data = request(repo + '/git/trees/' + ref + ('?recursive=1' if recursive else ''))
            except HTTPError as exc:
                if exc.code != 404:
                    raise
                data = None
            if data is not None and data.get('truncated'):
                raise ValueError('Truncated tree listing; inspect manually')
            listings[key] = data
        return listings[key]

    def entry(commit, path):
        if path == '.':
            return ('tree', listing(commit, '.')['sha'])
        parent, _, name = path.rpartition('/')
        data = listing(commit, parent or '.')
        found = [e for e in (data or {}).get('tree', []) if e['path'] == name]
        return (found[0]['type'], found[0]['sha']) if found else None

    def blobs(commit, path, found):
        if found is None:
            return {}
        if found[0] == 'blob':
            return {path: found[1]}
        prefix = '' if path == '.' else path + '/'
        return {prefix + e['path']: e['sha'] for e in listing(commit, path, True)['tree'] if e['type'] == 'blob'}

    files = []
    pins = source.get('path_pins') or dict.fromkeys(source['paths'], source['pinned'])
    for path, pin in pins.items():
        if not re.fullmatch(r'[0-9a-f]{40}', pin):
            raise ValueError('Source needs an exact reviewed commit')
        old, new = entry(pin, path), entry(head, path)
        if old == new:
            continue
        before, after = blobs(pin, path, old), blobs(head, path, new)
        for name in sorted(before.keys() | after.keys()):
            if before.get(name) != after.get(name):
                status = 'added' if name not in before else 'removed' if name not in after else 'modified'
                files.append(dict(path=name, previous=None, status=status))
    return files


def compare(source, request=get_json):
    result = dict(source, observed=None, status='unavailable', files=[])
    try:
        repo = repository_name(source['repository'])
        pin = source['pinned']
        if not re.fullmatch(r'[0-9a-f]{40}', pin):
            raise ValueError('Source needs an exact reviewed commit')
        head = request(repo + '/commits/HEAD')['sha']
        if not re.fullmatch(r'[0-9a-f]{40}', head):
            raise ValueError('Invalid observed commit')
        result['observed'] = head
        pins = set((source.get('path_pins') or {}).values()) or {pin}
        if pins == {head}:
            result['status'] = 'unchanged'
            return result
        if source.get('path_pins'):
            result['method'] = 'tree'
            result['files'] = tree_files(source, repo, head, request)
        else:
            data = request(repo + '/compare/' + pin + '...' + head)
            files = data['files']
            if data['status'] != 'ahead':
                raise ValueError('Diverged history; inspect manually')
            if len(files) >= 300:
                # GitHub caps this list at 300; diff the selected paths directly instead.
                result['method'] = 'tree'
                result['files'] = tree_files(source, repo, head, request)
            else:
                result['files'] = [dict(path=f['filename'], previous=f.get('previous_filename'),
                                        status=f['status']) for f in files]
        touched = {p for f in result['files'] for p in (f['path'], f['previous']) if p}
        selected = [p for p in touched if any(prefix == '.' or p == prefix or p.startswith(prefix + '/')
                                             for prefix in source['paths'])]
        result['selected_files'] = sorted(selected)
        # Do not label package/manifest changes metadata-only: they may change behavior.
        release_only = bool(touched) and all(
            p == 'CHANGELOG.md' or p == '.release-please-manifest.json'
            or p.startswith('.changeset/') for p in touched)
        result['status'] = 'metadata-only' if release_only and not selected else 'changed'
        result['scope'] = 'selected-content' if selected else 'outside-selected-paths'
    except (OSError, URLError, ValueError, KeyError, TypeError) as exc:
        result['error'] = str(exc)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--source', action='append',
                       help='Dependency ID or imported owner/repository; repeat to select')
    group.add_argument('--all', action='store_true', help='Compare every pinned source')
    args = parser.parse_args()
    declared = sources(args.root)
    if args.all:
        args.source = sorted(declared)
    unknown = set(args.source) - declared.keys()
    if unknown:
        parser.error('Unknown or unpinned source: ' + ', '.join(sorted(unknown)))
    results = {name: compare(declared[name]) for name in dict.fromkeys(args.source)}
    print(json.dumps(results, indent=2))
    return 2 if any(r['status'] == 'unavailable' for r in results.values()) else 0


if __name__ == '__main__':
    raise SystemExit(main())
