#!/usr/bin/env python3
"""Resolve context-selected methods against actual installed files, read-only.

The active agent selects IDs from task meaning and the routing index. This helper
does not infer relevance, grant actions, install missing skills or dispatch agents.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ENTRIES = {'codex-forge', 'cursor-forge', 'universal-forge'}


def resolve(index, names, skills_root, *, explicit=(), entry=None, context=None, candidate=None,
            runtime=False, acceptance=False, additional_roots=(), worker_brief=None):
    if index.get('schema_version') != 1 or index.get('dispatcher') != 'workflow-orchestrator':
        raise ValueError('Unsupported routing contract')
    if entry is not None and entry not in ENTRIES:
        raise ValueError('Unknown execution entry')
    if len(set(names) & ENTRIES) > 1:
        raise ValueError('Select one Forge execution entry')
    if entry and any(name in ENTRIES and name != entry for name in names):
        raise ValueError('A supporting method cannot replace the active entry')
    if context is not None:
        validate_context(context)
    result = []
    skills_root = skills_root.resolve()
    roots = [skills_root, *(Path(p).resolve() for p in additional_roots)]
    if entry == 'codex-forge' and skills_root.parent.name == '.agents':
        roots.append(skills_root.parent.parent / '.codex/skills')
    groups = {}
    for name in dict.fromkeys(names):
        group = index['skills'].get(name, {}).get('alternative_group')
        if group:
            groups.setdefault(group, []).append(name)
    if context is not None and any(len(v) > 1 for v in groups.values()) and not context.get('overlap_reason'):
        raise ValueError('Overlapping methods require a concrete additional coverage reason')
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
            relative = Path(resource.split('#', 1)[0])
            if relative.is_absolute() or '..' in relative.parts:
                raise ValueError('Unsafe routing resource')
            if context and kind == 'source' and route.get('targets') and context.get('harness') and context['harness'] not in route['targets']:
                continue
            matches = []
            resolved_roots = [root.resolve() for root in roots]
            for root in roots:
                path = root / relative
                if not any(path.resolve().is_relative_to(r) for r in resolved_roots):
                    raise ValueError('Unsafe routing resource')
                if path.is_file():
                    matches.append(path)
            if not matches:
                continue
            path = matches[0]
            issues = []
            if kind == 'source' and re.search(r'^disable-model-invocation:\s*true\s*$', path.read_text().split('---', 2)[1] if path.read_text().startswith('---') else '', re.M) and name not in explicit:
                raise ValueError('Installed method requires explicit invocation: ' + name)
            if len({p.resolve() for p in matches}) > 1:
                issues.append('duplicate discovery copies; reconcile the selected roots')
            if kind == 'source':
                if route.get('source_sha256') and hashlib.sha256(path.read_bytes()).hexdigest() != route['source_sha256']:
                    issues.append('installed external instructions differ from the reviewed source pin')
                for item in route.get('required_resources', []):
                    resource_path = path.parent / item
                    if not resource_path.resolve().is_relative_to(path.parent.resolve()):
                        raise ValueError('Unsafe required resource')
                    if not resource_path.is_file():
                        issues.append('missing resource: ' + item)
                for dependency in route.get('required_skills', []):
                    if not any((root / dependency / 'SKILL.md').is_file() for root in roots):
                        issues.append('missing required skill: ' + dependency)
            if context is not None or runtime or acceptance:
                if context is None:
                    issues.append('task context required for runtime or acceptance validation')
                else:
                    issues += issues_for(route, context, candidate, runtime=runtime)
                    if acceptance:
                        issues += evidence_issues(route, context, candidate)
            selected = {'method': name, 'route': kind, 'resource': str(path),
                        'outcome': route['outcome'], 'boundary': route['boundary'],
                        'required_evidence': route.get('required_evidence', []),
                        'issues': issues,
                        'status': 'blocked' if issues else 'source-available; runtime-capabilities-unverified'}
            if not issues and runtime:
                selected['status'] = 'prerequisites-observed; execution-unverified'
            if not issues and acceptance:
                selected['status'] = 'evidence-integrity-checked; semantic-acceptance-owner-required'
            break
        result.append(selected or {'method': name, 'status': 'unavailable',
                                   'boundary': route['boundary']})
    brief = validate_brief(worker_brief, names, candidate) if worker_brief is not None else None
    if brief and runtime:
        worker_context = worker_brief.get('context')
        worker_issues = []
        if worker_context is None:
            worker_issues.append('worker runtime context has not been observed')
        else:
            validate_context(worker_context)
            for name in worker_brief['methods']:
                worker_issues += issues_for(index['skills'][name], worker_context, candidate, runtime=True)
        if worker_issues:
            brief.update(status='blocked-by-worker-readiness', issues=worker_issues)
    if brief and any(r['status'] in ('blocked', 'unavailable') for r in result):
        brief['status'] = 'blocked-by-selected-route'
    return {'dispatcher': 'workflow-orchestrator', 'entry': entry,
            'methods': result, 'worker_brief': brief, 'grants_authority': False}


def main():
    here = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skills-root', type=Path, default=here.parent)
    parser.add_argument('--index', type=Path, default=here / 'references/skill-routing.json')
    parser.add_argument('--method', action='append', required=True)
    parser.add_argument('--explicit', action='append', default=[])
    parser.add_argument('--entry', choices=sorted(ENTRIES))
    parser.add_argument('--context', type=Path, help='Existing task/readiness/evidence receipt JSON')
    parser.add_argument('--candidate', help='Current reviewed candidate identity, including dirty content when relevant')
    parser.add_argument('--runtime', action='store_true')
    parser.add_argument('--acceptance', action='store_true')
    parser.add_argument('--additional-skills-root', action='append', type=Path, default=[])
    parser.add_argument('--worker-brief', type=Path)
    args = parser.parse_args()
    try:
        result = resolve(json.loads(args.index.read_text()), args.method, args.skills_root,
                         explicit=args.explicit, entry=args.entry,
                         context=json.loads(args.context.read_text()) if args.context else None,
                         candidate=args.candidate, runtime=args.runtime, acceptance=args.acceptance,
                         additional_roots=args.additional_skills_root,
                         worker_brief=json.loads(args.worker_brief.read_text()) if args.worker_brief else None)
        print(json.dumps(result, indent=2))
        blocked = any(m['status'] in ('unavailable', 'blocked') for m in result['methods'])
        blocked |= (result.get('worker_brief') or {}).get('status', '').startswith('blocked')
        return 2 if blocked else 0
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps({'status': 'invalid', 'error': str(exc)}))
        return 1


def validate_context(context):
    if not isinstance(context, dict):
        raise ValueError('Task context must be an object')
    for key in ('task_tags',):
        if not isinstance(context.get(key, []), list) or not all(isinstance(x, str) for x in context.get(key, [])):
            raise ValueError(key + ' must be a list of strings')
    for key in ('readiness', 'evidence', 'execution'):
        if not isinstance(context.get(key, {}), dict):
            raise ValueError(key + ' must be an object')
    readiness = context.get('readiness', {})
    if not isinstance(readiness.get('capabilities', {}), dict) or not all(isinstance(v, dict) for v in readiness.get('capabilities', {}).values()):
        raise ValueError('Capabilities must contain observation objects')
    if not all(isinstance(v, dict) for v in context.get('evidence', {}).values()):
        raise ValueError('Evidence must contain receipt objects')


def issues_for(route, context, candidate, *, runtime=False):
    issues = []
    tags = set(context.get('task_tags', []))
    applies = set(route.get('task_tags_any', []))
    if applies and not tags.intersection(applies):
        issues.append('task applicability has not been established')
    if not runtime:
        return issues
    platforms = route.get('runtime_platforms', [])
    if platforms and context.get('platform') not in platforms:
        issues.append('unsupported or unverified runtime platform')
    evidence = context.get('readiness', {})
    needs = list(route.get('runtime_capabilities', []))
    auth_needs = list(route.get('authenticated_capabilities', []))
    installed_only = []
    if route.get('source') == 'e2e/SKILL.md':
        execution = context.get('execution', {})
        surface = execution.get('surface')
        if surface == 'browser':
            installed_only.append('e2e-web')
        elif surface in ('ios', 'android'):
            installed_only.append('e2e-mobile')
            needs.append('device')
        else:
            issues.append('E2E surface must be browser, ios or android')
        if execution.get('mode') == 'agent-driven':
            needs.append('model-provider'); auth_needs.append('model-provider')
            if execution.get('provider_authorized') is not True or not execution.get('provider'):
                issues.append('E2E model provider requires an existing explicit grant')
            if any(type(execution.get(k)) not in (int, float) or not 0 < execution[k] < float('inf') for k in ('max_steps', 'timeout_seconds', 'max_cost')):
                issues.append('E2E model execution requires finite positive step, time and cost limits')
        elif execution.get('mode') != 'deterministic':
            issues.append('E2E execution mode must be explicit')
    if needs or installed_only:
        if not candidate or evidence.get('candidate') != candidate:
            issues.append('missing or stale candidate-scoped readiness')
        try:
            observed = datetime.fromisoformat(evidence['observed_at'].replace('Z', '+00:00'))
            age = (datetime.now(timezone.utc) - observed).total_seconds()
            if age < -60:
                issues.append('readiness observation is future-dated')
            if evidence.get('invalidated'):
                issues.append('readiness invalidated by a material environment change')
        except (KeyError, ValueError, TypeError):
            issues.append('readiness timestamp is missing or invalid')
        for capability in needs + installed_only:
            row = evidence.get('capabilities', {}).get(capability, {})
            if row.get('installed') is not True or row.get('discoverable') is not True:
                issues.append(capability + ': unavailable')
            if capability not in installed_only and row.get('exercised') != 'passed':
                issues.append(capability + ': probe not exercised successfully')
            if capability in auth_needs and row.get('authenticated') != 'passed':
                issues.append(capability + ': authentication unverified')
    return issues


def validate_brief(brief, selected, candidate):
    if not isinstance(brief, dict):
        raise ValueError('Worker brief must be an object')
    for key in ('allowed_files', 'non_goals', 'required_evidence', 'instructions', 'methods'):
        if not isinstance(brief.get(key), list) or not all(isinstance(v, str) and v for v in brief[key]):
            raise ValueError('Worker brief ' + key + ' must list concrete values')
    required = ('owner', 'role', 'allowed_files', 'non_goals', 'authority', 'required_evidence', 'instructions', 'candidate', 'methods')
    missing = [name for name in required if not brief.get(name)]
    if missing:
        raise ValueError('Incomplete worker brief: ' + ', '.join(missing))
    if not candidate or brief['candidate'] != candidate:
        raise ValueError('Worker brief candidate differs from the current candidate')
    if not set(brief['methods']).issubset(selected):
        raise ValueError('Worker brief adds unvalidated methods')
    if brief['authority'] not in ('read-only', 'approved-task-write'):
        raise ValueError('Worker authority must be a bounded existing grant')
    return {'status': 'contract-complete', 'runtime_dispatch': 'unverified', 'grants_authority': False}


def evidence_issues(route, context, candidate):
    """Check receipt identity/integrity; semantic correctness still needs actual review."""
    import hashlib
    from pathlib import Path
    issues = []
    for key in route.get('required_evidence', []):
        record = context.get('evidence', {}).get(key, {})
        if not candidate or record.get('candidate') != candidate or record.get('status') != 'passed':
            issues.append(key + ': required evidence missing, failed or stale')
            continue
        artifact = Path(record.get('artifact', ''))
        if not artifact.is_file() or hashlib.sha256(artifact.read_bytes()).hexdigest() != record.get('sha256'):
            issues.append(key + ': evidence artifact missing or changed')
    return issues


if __name__ == '__main__':
    raise SystemExit(main())
