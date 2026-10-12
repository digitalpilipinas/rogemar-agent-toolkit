#!/usr/bin/env python3
"""Resolve the effective diagram style without changing project or installed files."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re

DEFAULT = Path(__file__).resolve().parents[1] / 'references/style-guide.md'


def validate(path: Path) -> str:
    text = path.read_text(encoding='utf-8')
    defaults = DEFAULT.read_text(encoding='utf-8')
    for heading in ('### Semantic roles', '## Typography'):
        def keys(body):
            section = body.split(heading, 1)[1].split('\n#', 1)[0]
            return set(re.findall(r'^\| `([^`]+)` \|', section, re.MULTILINE))
        if heading not in text or not keys(defaults) <= keys(text):
            raise ValueError(f'Incomplete profile {path}: missing {heading} roles')
    match = re.search(r'^Font source: `?(system|web)`?\s*$', text, re.MULTILINE)
    if not match:
        raise ValueError(f'Invalid or missing Font source in {path}')
    return match.group(1)


def resolve(project: Path, legacy_library: Path | None = None) -> dict:
    project = project.resolve()
    profile = project / '.diagram-design-profile.md'
    source = 'project'
    if not profile.exists() and not profile.is_symlink():
        marker = project / '.diagram-design'
        profile, source = DEFAULT, 'default'
        if marker.exists() or marker.is_symlink():
            match = re.fullmatch(r'[ \t]*profile:[ \t]*([a-z0-9][a-z0-9-]{0,63})[ \t]*(?:\r?\n)?', marker.read_text(encoding='utf-8'))
            if not match:
                raise ValueError(f'Invalid legacy profile marker: {marker}')
            slug = match.group(1)
            profile = (legacy_library or Path.home() / '.diagram-design/profiles') / (slug + '.md')
            source = 'legacy-read-only'
            if slug == 'default' and not profile.exists():
                profile, source = DEFAULT, 'default'
    return {'path': str(profile), 'source': source, 'font_source': validate(profile), 'writes_files': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project-root', type=Path, required=True)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    try:
        result = resolve(args.project_root)
    except (OSError, ValueError) as exc:
        parser.exit(2, f'Profile unavailable: {exc}\n')
    print(json.dumps(result) if args.json else result['path'])


if __name__ == '__main__':
    main()
