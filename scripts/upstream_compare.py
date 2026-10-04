#!/usr/bin/env python3
"""Read selected public GitHub revisions; never install, repin, or authenticate.

Use during approved toolkit maintenance, not ordinary product tasks. Output is
comparison evidence, not an update recommendation or a capability readiness check.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from urllib.error import URLError
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
        result[repo] = dict(repository=repo, pinned=item['commit'], paths=sorted({
            skill['source'] for skill in imported['skills'] if skill['repository'] == repo}))
    return result


def repository_name(value):
    value = value.removeprefix('https://github.com/').removesuffix('.git')
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', value):
        raise ValueError('Only declared public GitHub repositories are supported')
    return value


def get_json(path):
    request = Request('https://api.github.com/repos/' + path, headers={
        'Accept': 'application/vnd.github+json', 'User-Agent': 'rogemar-toolkit-maintenance'})
    with urlopen(request, timeout=30) as response:
        raw = response.read(10_000_001)
    if len(raw) > 10_000_000:
        raise ValueError('Comparison response exceeds the inspection limit')
    return json.loads(raw)


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
        if pin == head:
            result['status'] = 'unchanged'
            return result
        data = request(repo + '/compare/' + pin + '...' + head)
        files = data['files']
        # GitHub caps this list at 300. Conservatively reject that boundary.
        if data['status'] != 'ahead' or len(files) >= 300:
            raise ValueError('Diverged history or incomplete file comparison; inspect manually')
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
    parser.add_argument('--source', action='append', required=True,
                        help='Dependency ID or imported owner/repository; repeat to select')
    args = parser.parse_args()
    declared = sources(args.root)
    unknown = set(args.source) - declared.keys()
    if unknown:
        parser.error('Unknown or unpinned source: ' + ', '.join(sorted(unknown)))
    results = {name: compare(declared[name]) for name in dict.fromkeys(args.source)}
    print(json.dumps(results, indent=2))
    return 2 if any(r['status'] == 'unavailable' for r in results.values()) else 0


if __name__ == '__main__':
    raise SystemExit(main())
