#!/usr/bin/env python3
"""Generate and check the installed routing index from the canonical catalog.

The index describes conditional methods, not installed capabilities or permission.
Selection remains with workflow-orchestrator; no prompt keyword dispatcher runs.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SKILLS = Path('plugins/rogemar-agent-toolkit/skills')
OUTPUT = SKILLS / 'workflow-orchestrator/references/skill-routing.json'


def expected_index(root):
    catalog = json.loads((root / 'catalog/skills.yaml').read_text())
    routes = {}
    for item in catalog['vendored']:
        route = dict(item['routing'])
        route['source'] = item['name'] + '/SKILL.md'
        route['kind'] = 'vendored'
        route['required_resources'] = item.get('required_resources', [])
        route['required_skills'] = item.get('requires', [])
        route['targets'] = item.get('targets', [])
        routes[item['name']] = route
    for dependency, item in catalog['dependencies'].items():
        recipe = item.get('auto_install', {})
        if not recipe:
            continue
        metadata = recipe.get('metadata', {})
        if metadata.get('commit') != recipe['commit']:
            raise ValueError(dependency + ': external metadata pin differs from installation pin')
        if set(metadata.get('skills', {})) != set(recipe['skills']):
            raise ValueError(dependency + ': external metadata membership differs from installation')
        overrides = recipe.get('routing_overrides', {})
        if set(overrides) - set(recipe['skills']):
            raise ValueError(dependency + ': routing override names an uninstalled skill')
        for name in recipe.get('skills', {}):
            if name in routes:
                raise ValueError('Duplicate external/vendored route: ' + name)
            source = metadata['skills'][name]
            if (source.get('source') != recipe['skills'][name]
                    or not re.fullmatch('[0-9a-f]{64}', source.get('skill_sha256', ''))
                    or not isinstance(source.get('description'), str) or not source['description'].strip()):
                raise ValueError(name + ': invalid pinned source metadata')
            for resource in source.get('required_resources', []):
                if not isinstance(resource, str) or Path(resource).is_absolute() or '..' in Path(resource).parts:
                    raise ValueError(name + ': unsafe external resource')
            routes[name] = {'source': name + '/SKILL.md', 'kind': 'external',
                           'dependency': dependency, 'commit': recipe['commit'],
                           'source_sha256': source['skill_sha256'],
                           'trigger': source['description'], 'outcome': 'Use applicable upstream method after reading its installed source',
                           'boundary': 'Files do not establish live tools, authentication or permission',
                           'activation': source['activation'], 'targets': item.get('targets', []),
                           'required_resources': source.get('required_resources', [])}
            override = overrides.get(name, {})
            if override:
                if not override.get('reason') or set(override) - {'reason', 'activation', 'boundary', 'alternative_group'}:
                    raise ValueError(name + ': invalid reviewed routing override')
                if source['activation'] == 'explicit-only' and override.get('activation', 'explicit-only') != 'explicit-only':
                    raise ValueError(name + ': cannot relax upstream explicit invocation')
                routes[name].update({k: v for k, v in override.items() if k != 'reason'})
                routes[name]['adaptation'] = override['reason']
    return {'schema_version': 1, 'generated_by': 'scripts/routing_catalog.py',
            'dispatcher': 'workflow-orchestrator',
            'skills': dict(sorted(routes.items()))}


def verify(root=ROOT):
    errors = []
    try:
        expected = expected_index(root)
        for name, route in expected['skills'].items():
            for field in ('trigger', 'outcome', 'boundary'):
                value = route.get(field)
                if not isinstance(value, str) or not value.strip():
                    errors.append(name + ': missing routing ' + field)
            if route.get('activation') not in {'conditional', 'explicit-only'}:
                errors.append(name + ': invalid activation policy')
            for field in ('source', 'fallback'):
                value = route.get(field)
                if not value:
                    continue
                if field == 'source' and route.get('kind') == 'external':
                    continue
                relative, _, anchor = value.partition('#')
                path = root / SKILLS / relative
                if (Path(relative).is_absolute() or '..' in Path(relative).parts
                        or not path.is_file() or not path.resolve().is_relative_to((root / SKILLS).resolve())):
                    errors.append(name + ': missing or unsafe ' + field + ': ' + value)
                elif anchor and ('## ' + anchor.replace('-', ' ')).lower() not in path.read_text().lower():
                    errors.append(name + ': missing method anchor: ' + value)
        actual = json.loads((root / OUTPUT).read_text())
        selected = json.loads((root / 'catalog/skills.yaml').read_text()).get('package', {}).get('distribution_selection')
        if selected:
            # Preserve the exact canonical skill payload in selected archives.
            # Uninstalled routes remain discovery metadata, never availability.
            actual = dict(actual, skills={name: actual.get('skills', {}).get(name)
                                         for name in expected['skills']})
        if actual != expected:
            errors.append('Routing index is stale; run python3 scripts/routing_catalog.py --write')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append('Invalid routing catalog: ' + str(exc))
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    root = args.root.resolve()
    if args.write:
        if json.loads((root / 'catalog/skills.yaml').read_text()).get('package', {}).get('distribution_selection'):
            parser.error('Regenerate routing only in the canonical source checkout')
        output = root / OUTPUT
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(expected_index(root), indent=2, ensure_ascii=False) + '\n')
    errors = verify(root)
    print(json.dumps({'status': 'failed' if errors else 'verified', 'errors': errors}))
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
