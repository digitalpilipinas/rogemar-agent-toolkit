#!/usr/bin/env python3
"""Resolve context-selected methods against actual installed files, read-only.

The active agent selects IDs from task meaning and the routing index. This helper
does not infer relevance, grant actions, install missing skills or dispatch agents.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ENTRIES = {'codex-forge', 'cursor-forge', 'universal-forge'}


def resolve(index, names, skills_root, *, explicit=(), entry=None):
    if index.get('schema_version') != 1 or index.get('dispatcher') != 'workflow-orchestrator':
        raise ValueError('Unsupported routing contract')
    if entry is not None and entry not in ENTRIES:
        raise ValueError('Unknown execution entry')
    if len(set(names) & ENTRIES) > 1:
        raise ValueError('Select one Forge execution entry')
    if entry and any(name in ENTRIES and name != entry for name in names):
        raise ValueError('A supporting method cannot replace the active entry')
    result = []
    skills_root = skills_root.resolve()
    for name in dict.fromkeys(names):
        route = index['skills'].get(name)
        if route is None:
            raise ValueError('Unknown method: ' + name)
        if route['activation'] == 'explicit-only' and name not in explicit:
            raise ValueError('Method requires explicit invocation: ' + name)
        selected = None
        for kind in ('source', 'fallback'):
            resource = route.get(kind)
            if not resource:
                continue
            path = skills_root / resource.split('#', 1)[0]
            if not path.resolve().is_relative_to(skills_root):
                raise ValueError('Unsafe routing resource')
            if path.is_file():
                selected = {'method': name, 'route': kind, 'resource': resource,
                            'outcome': route['outcome'], 'boundary': route['boundary'],
                            'status': 'source-available; runtime-capabilities-unverified'}
                break
        result.append(selected or {'method': name, 'status': 'unavailable',
                                   'boundary': route['boundary']})
    return {'dispatcher': 'workflow-orchestrator', 'entry': entry,
            'methods': result, 'grants_authority': False}


def main():
    here = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skills-root', type=Path, default=here.parent)
    parser.add_argument('--index', type=Path, default=here / 'references/skill-routing.json')
    parser.add_argument('--method', action='append', required=True)
    parser.add_argument('--explicit', action='append', default=[])
    parser.add_argument('--entry', choices=sorted(ENTRIES))
    args = parser.parse_args()
    try:
        result = resolve(json.loads(args.index.read_text()), args.method, args.skills_root,
                         explicit=args.explicit, entry=args.entry)
        print(json.dumps(result, indent=2))
        return 2 if any(m['status'] == 'unavailable' for m in result['methods']) else 0
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps({'status': 'invalid', 'error': str(exc)}))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
