#!/usr/bin/env python3
"""Read-only catalog/review view. Mechanical file reads are not semantic reviews.

Review labels are owner-supplied declarations bound to file bytes, not signatures.
No command or skill from the target is executed. This is not a second inventory.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import stat

MAX_BYTES = 2 * 1024 * 1024


class InventoryError(ValueError):
    pass


def read_file(root, relative):
    path = Path(relative)
    if path.is_absolute() or '..' in path.parts:
        raise InventoryError('unsafe source path')
    current = root
    for part in path.parts:
        current = current / part
        info = current.lstat()
        if stat.S_ISLNK(info.st_mode):
            raise InventoryError('symlinked review source: ' + relative)
    if not current.is_file() or current.stat().st_size > MAX_BYTES:
        raise InventoryError('missing or oversized review source: ' + relative)
    return current.read_bytes()


def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def inventory(root, coverage):
    root = root.resolve()
    catalog = json.loads(read_file(root, 'catalog/skills.yaml'))
    entries = catalog.get('vendored')
    if catalog.get('schema_version') != 2 or not isinstance(entries, list) or not 0 < len(entries) <= 2000:
        raise InventoryError('unrecognized or empty catalog; inspect schema before adaptation')
    default_targets = catalog.get('vendored_defaults', {}).get('targets', [])
    declarations = coverage.get('skills', [])
    if not isinstance(declarations, list):
        raise InventoryError('invalid coverage declarations')
    review_by_name = {}
    for item in declarations:
        if not isinstance(item, dict) or not isinstance(item.get('skill'), str) or item['skill'] in review_by_name:
            raise InventoryError('invalid or duplicate review declaration')
        review_by_name[item['skill']] = item
    rows, seen = [], set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise InventoryError('invalid catalog entry')
        name = entry.get('name')
        if not isinstance(name, str) or not re.fullmatch(r'[a-z0-9][a-z0-9-]*', name) or name in seen:
            raise InventoryError('invalid or duplicate canonical skill name')
        seen.add(name)
        path = 'plugins/rogemar-agent-toolkit/skills/' + name + '/SKILL.md'
        row = {'skill': name, 'path': path, 'declared_targets': entry.get('targets', default_targets),
               'requires': entry.get('requires', []), 'runtime_qualification': 'not-established-by-this-scan'}
        try:
            data = read_file(root, path)
            text = data.decode('utf-8')
            sha = blob(data)
            name_line = re.search(r'^name:\s*["\']?([^"\'\n]+?)["\']?\s*$', text, re.M)
            if not name_line or name_line.group(1).strip() != name:
                raise InventoryError('frontmatter identity mismatch')
            claim = review_by_name.get(name, {})
            state = claim.get('body_review', 'not-reviewed')
            if state not in {'complete', 'partial', 'not-reviewed'}:
                raise InventoryError('unknown declared review state')
            if claim.get('git_blob') != sha:
                state = 'changed-since-review' if claim.get('git_blob') else 'not-reviewed'
            row.update(git_blob=sha, body_review=state, disposition=claim.get('disposition', 'review-needed'),
                       note=claim.get('note', 'No matching semantic review receipt.'),
                       resource_review=claim.get('resource_review', 'not-established'))
        except (OSError, UnicodeError, InventoryError) as exc:
            row.update(body_review='unavailable', disposition='review-needed', note=str(exc))
        rows.append(row)
    external = catalog.get('external_skill_groups', [])
    return {'schema_version': 1, 'kind': 'catalog-and-review-view', 'canonical_count': len(rows),
            'declared_body_coverage_complete': all(row['body_review'] == 'complete' for row in rows),
            'skills': rows,
            'external_groups': [{'name': item.get('name'), 'mode': item.get('mode'),
                                 'status': 'external-declaration-not-installation-proof'} for item in external],
            'limitations': 'Review declarations are not authenticated; no model, provider, target command, runtime or full resource execution is performed.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--coverage', type=Path)
    args = parser.parse_args()
    try:
        path = args.coverage or args.root / 'docs/alignment/review-coverage.json'
        if path.stat().st_size > MAX_BYTES:
            raise InventoryError('oversized coverage record')
        result = inventory(args.root, json.loads(path.read_text(encoding='utf-8')))
        print(json.dumps(result, indent=2, ensure_ascii=True))
        return 0 if result['declared_body_coverage_complete'] else 2
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({'status': 'unavailable', 'error': str(exc)}, ensure_ascii=True))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
