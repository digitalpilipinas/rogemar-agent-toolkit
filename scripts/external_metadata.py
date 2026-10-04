#!/usr/bin/env python3
"""Inspect pinned Git objects for external skill metadata; never fetch or execute them.

Run during approved maintenance with --dependency NAME --checkout PATH. Review
the JSON before using --write. Ordinary selection and verification stay offline.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import tarfile

ROOT = Path(__file__).resolve().parents[1]


def scalar(text, key):
    """Read the plain/quoted/block scalars used by the reviewed skill sources.

    This is deliberately not a general YAML loader: unsupported syntax fails
    maintenance instead of silently inventing a routing description.
    """
    match = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)', text, re.S)
    if not match:
        raise ValueError('Missing skill frontmatter')
    lines = match[1].splitlines()
    for i, line in enumerate(lines):
        if not line.startswith(key + ':'):
            continue
        value = line.partition(':')[2].strip()
        if value in ('', '>', '>-', '|', '|-'):
            parts = []
            for following in lines[i + 1:]:
                if following and not following[0].isspace():
                    break
                parts.append(following.strip())
            return ' '.join(parts).strip()
        if value.startswith('"'):
            return json.loads(value)
        if value.startswith("'") and value.endswith("'"):
            return value[1:-1].replace("''", "'")
        if value.startswith(('&', '*', '!', '{', '[')):
            raise ValueError('Unsupported scalar: ' + key)
        return value
    return None


def git(checkout, *args):
    return subprocess.check_output(['git', '-C', str(checkout), *args], timeout=60)


def extract(recipe, checkout):
    commit = recipe['commit']
    if not re.fullmatch('[0-9a-f]{40}', commit):
        raise ValueError('Expected exact commit')
    if git(checkout, 'rev-parse', commit + '^{commit}').decode().strip() != commit:
        raise ValueError('Source commit mismatch')
    for source in recipe['skills'].values():
        if Path(source).is_absolute() or '..' in Path(source).parts or source.startswith('-'):
            raise ValueError('Unsafe source path')
    archive_bytes = git(checkout, 'archive', commit, '--', *recipe['skills'].values())
    records = {}
    with tarfile.open(fileobj=io.BytesIO(archive_bytes)) as archive:
        members = {m.name: m for m in archive.getmembers()}
        for name, source in recipe['skills'].items():
            records[name] = extract_skill(archive, members, name, source)
    return {'commit': commit, 'skills': records}


def extract_skill(archive, members, name, source):
    if Path(source).is_absolute() or '..' in Path(source).parts:
        raise ValueError('Unsafe source path')
    entry = members[(Path(source) / 'SKILL.md').as_posix()]
    if not entry.isfile():
        raise ValueError('Non-regular SKILL.md')
    data = archive.extractfile(entry).read()
    description = scalar(data.decode(), 'description')
    if not description:
        raise ValueError('Missing description: ' + name)
    resources = []
    for path, member in members.items():
        if member.isdir():
            continue
        try:
            relative = Path(path).relative_to(source).as_posix()
        except ValueError:
            continue
        if not member.isfile() or '..' in Path(relative).parts:
            raise ValueError('Non-regular skill resource: ' + path)
        if relative != 'SKILL.md':
            resources.append(relative)
    return {
        'source': source, 'description': description,
        'activation': 'explicit-only' if scalar(data.decode(), 'disable-model-invocation') == 'true' else 'conditional',
        'skill_sha256': hashlib.sha256(data).hexdigest(),
        'required_resources': sorted(resources),
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--dependency', required=True)
    parser.add_argument('--checkout', type=Path, required=True)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    path = args.root / 'catalog/skills.yaml'
    catalog = json.loads(path.read_text())
    if catalog.get('package', {}).get('distribution_selection'):
        parser.error('Maintain metadata in the canonical checkout')
    recipe = catalog['dependencies'][args.dependency]['auto_install']
    metadata = extract(recipe, args.checkout)
    if args.write:
        recipe['metadata'] = metadata
        path.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + '\n')
    else:
        print(json.dumps(metadata, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
