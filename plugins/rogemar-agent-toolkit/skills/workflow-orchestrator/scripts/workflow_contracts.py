#!/usr/bin/env python3
"""Read-only checks for an existing task record. No dispatcher or authority grant.

A declaration passing these checks is not proof of permission, execution, semantic
independence, or sandbox enforcement. Hosts retain authorization and state ownership.
Run with Python -B to avoid incidental bytecode writes in read-only workflows.
"""
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import math
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import PurePosixPath
from typing import Any

MAX_BYTES = 1024 * 1024
MAX_ITEMS = 500
STATES = {'pending', 'running', 'passed', 'failed', 'blocked', 'deferred', 'cancelled'}
FAILURES = {'implementation', 'environment', 'verifier', 'context', 'routing', 'authority', 'unknown'}


class ContractError(ValueError):
    """Malformed or inconsistent input, not a demonstrated product defect."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def _nonfinite(_: str) -> None:
    raise ContractError('non-finite JSON number')


def read_json(raw: bytes) -> Any:
    require(len(raw) <= MAX_BYTES, 'input exceeds 1 MiB')
    try:
        result = json.loads(raw.decode('utf-8'), object_pairs_hook=_pairs, parse_constant=_nonfinite)
    except (UnicodeError, ValueError, RecursionError) as exc:
        raise ContractError('invalid JSON input') from exc
    todo = [(result, 0)]
    count = 0
    while todo:
        item, depth = todo.pop()
        count += 1
        require(depth <= 32 and count <= 50_000, 'input structure exceeds bounds')
        if isinstance(item, dict):
            todo.extend((k, depth + 1) for k in item)
            todo.extend((v, depth + 1) for v in item.values())
        elif isinstance(item, list):
            todo.extend((v, depth + 1) for v in item)
        elif isinstance(item, float):
            require(math.isfinite(item), 'non-finite JSON number')
        elif isinstance(item, str):
            try:
                item.encode('utf-8')
            except UnicodeError as exc:
                raise ContractError('invalid Unicode scalar') from exc
    return result


def text(value: Any, field: str, limit: int = 1000) -> str:
    require(isinstance(value, str) and bool(value.strip()) and len(value) <= limit,
            field + ' must be a nonempty bounded string')
    require(not any(unicodedata.category(c) in {'Cc', 'Cf', 'Cs'} for c in value),
            field + ' contains unsafe control characters')
    return value


def relative_path(value: Any) -> str:
    value = text(value, 'path', 500)
    path = PurePosixPath(value)
    require(not path.is_absolute() and str(path) == value and value != '.'
            and '..' not in path.parts and '.git' not in path.parts
            and not any(c in value for c in '\\:*?[]'),
            'ownership path must be an exact canonical repository-relative path')
    return unicodedata.normalize('NFC', value).casefold()


def overlap(left: str, right: str) -> bool:
    left, right = relative_path(left), relative_path(right)
    return left == right or left.startswith(right + '/') or right.startswith(left + '/')


def validate_assignments(record: Any) -> dict[str, Any]:
    require(isinstance(record, dict) and type(record.get('schema_version')) is int
            and record['schema_version'] == 1, 'unsupported assignment extension')
    tasks = record.get('assignments')
    require(isinstance(tasks, list) and len(tasks) <= MAX_ITEMS, 'assignments must be a bounded array')
    by_id: dict[str, dict[str, Any]] = {}
    for task in tasks:
        require(isinstance(task, dict), 'assignment must be an object')
        ident = text(task.get('id'), 'id', 100)
        require(re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_.-]*', ident) is not None, 'invalid assignment id')
        require(ident not in by_id, 'duplicate assignment id')
        text(task.get('owner'), 'owner', 100)
        text(task.get('acceptance'), 'acceptance')
        require(task.get('state') in STATES, 'invalid assignment state')
        for key in ('depends_on', 'writes', 'exclusive_resources'):
            values = task.get(key, [])
            require(isinstance(values, list) and len(values) <= MAX_ITEMS, key + ' must be a bounded array')
            require(all(isinstance(v, str) for v in values), key + ' must contain strings')
            require(len(set(values)) == len(values), 'duplicate ' + key)
        for path in task.get('writes', []):
            relative_path(path)
        for resource in task.get('exclusive_resources', []):
            text(resource, 'resource', 200)
        if task.get('writes'):
            text(task.get('workspace'), 'workspace', 200)
        if task['state'] == 'passed':
            evidence = task.get('evidence')
            require(isinstance(evidence, list) and 0 < len(evidence) <= MAX_ITEMS,
                    'passed assignment needs bounded evidence references')
            for reference in evidence:
                text(reference, 'evidence reference')
            require(bool(record.get('candidate')) and task.get('candidate') == record['candidate'],
                    'passed assignment has stale or missing candidate')
        by_id[ident] = task
    for ident, task in by_id.items():
        require(all(dep in by_id and dep != ident for dep in task.get('depends_on', [])),
                'unknown or self dependency')
    remaining = {ident: set(task.get('depends_on', [])) for ident, task in by_id.items()}
    order: list[str] = []
    while remaining:
        ready = sorted(ident for ident, deps in remaining.items() if not deps)
        require(bool(ready), 'dependency cycle')
        order.extend(ready)
        for ident in ready:
            del remaining[ident]
        for deps in remaining.values():
            deps.difference_update(ready)
    for task in tasks:
        if task['state'] in {'running', 'passed'}:
            require(all(by_id[dep]['state'] == 'passed' for dep in task.get('depends_on', [])),
                    'active or passed assignment has incomplete prerequisites')
    running = [task for task in tasks if task['state'] == 'running']
    for index, left in enumerate(running):
        for right in running[index + 1:]:
            require(not set(left.get('exclusive_resources', [])) & set(right.get('exclusive_resources', [])),
                    'concurrent assignments share an exclusive runtime resource')
            if left.get('writes') and right.get('writes'):
                require(left['workspace'] != right['workspace'], 'serialize writers in a shared worktree')
                require(not any(overlap(a, b) for a in left['writes'] for b in right['writes']),
                        'parallel writers have overlapping source ownership')
    return {'status': 'declared-state-valid', 'order': order,
            'limitations': 'Does not discover missing semantic dependencies, attest evidence, or isolate processes.'}


def affected_assignments(record: dict[str, Any], changed: list[str]) -> list[str]:
    # Dependency discovery is separate from candidate freshness. Input is the current
    # coordination record, before a producer mutates its previously passed status.
    validate_assignments(record)
    require(isinstance(changed, list) and all(isinstance(x, str) for x in changed), 'changed IDs must be strings')
    require(set(changed) <= {t['id'] for t in record['assignments']}, 'unknown changed assignment')
    affected = set(changed)
    while True:
        expanded = affected | {t['id'] for t in record['assignments'] if set(t.get('depends_on', [])) & affected}
        if expanded == affected:
            return sorted(affected)
        affected = expanded


def retry_decision(record: Any) -> dict[str, Any]:
    require(isinstance(record, dict), 'retry input must be an object')
    used, limit = record.get('attempts_used'), record.get('attempt_limit')
    require(type(used) is int and used >= 0 and type(limit) is int and limit > 0, 'invalid attempt budget')
    kind = record.get('failure_kind')
    require(kind in FAILURES, 'invalid failure classification')
    require(type(record.get('cancelled', False)) is bool, 'cancelled must be boolean')
    require(type(record.get('other_budget_exhausted', False)) is bool, 'budget flag must be boolean')
    if record.get('cancelled'):
        decision = 'stop-and-preserve'
    elif kind == 'authority':
        decision = 'resolve-authority-no-retry'
    elif used >= limit or record.get('other_budget_exhausted'):
        decision = 'budget-exhausted-reclassify'
    elif kind != 'implementation':
        decision = 'diagnose-before-retry'
    else:
        decision = 'eligible-for-scoped-correction'
    return {'decision': decision, 'grants_authority': False}


def framing_decision(record: Any) -> dict[str, Any]:
    require(isinstance(record, dict), 'framing input must be an object')
    mode = record.get('mode', 'adaptive')
    require(mode in {'adaptive', 'review-first', 'prompt-only', 'refine-and-run', 'direct'}, 'invalid framing mode')
    for field in ('approved_continuation', 'material_gap'):
        require(type(record.get(field, False)) is bool, field + ' must be boolean')
    if mode == 'prompt-only':
        action = 'produce-prompt-only'
    elif record.get('material_gap'):
        action = 'resolve-material-gap'
    elif record.get('approved_continuation') or mode in {'direct', 'refine-and-run'}:
        action = 'continue-within-existing-authority'
    elif mode == 'review-first':
        action = 'present-one-prompt-and-wait'
    else:
        action = 'frame-proportionately-without-new-approval'
    return {'decision': action, 'grants_authority': False}


def action_digest(action: Any) -> str:
    require(isinstance(action, dict), 'action must be an object')
    fields = {'operation_id', 'tool', 'connection', 'requester', 'target', 'arguments'}
    require(set(action) == fields, 'action requires exactly the documented binding fields')
    for field in fields - {'arguments'}:
        text(action[field], field, 500)
    require(isinstance(action['arguments'], dict), 'arguments must be an object')
    try:
        raw = json.dumps(action, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False).encode()
    except (ValueError, TypeError, RecursionError) as exc:
        raise ContractError('invalid canonical action') from exc
    read_json(raw)
    return hashlib.sha256(raw).hexdigest()


def check_action_binding(action: Any, approval: Any, *, now: datetime,
                         used_operation_ids: set[str]) -> dict[str, Any]:
    """Compare a complete action with a separately authenticated host approval.

    The host must authenticate approval and atomically reserve/reconcile operation
    IDs. Supplying a matching approval object here does not grant authority.
    """
    digest = action_digest(action)
    require(isinstance(approval, dict) and set(approval) == {'action_sha256', 'expires_at', 'approval_id'},
            'invalid approval fields')
    text(approval['approval_id'], 'approval id', 200)
    expected = approval['action_sha256']
    require(isinstance(expected, str) and re.fullmatch(r'[0-9a-f]{64}', expected) is not None,
            'invalid action digest')
    require(hmac.compare_digest(expected, digest), 'approval is for a different complete action')
    try:
        expiry = datetime.fromisoformat(approval['expires_at'].replace('Z', '+00:00'))
    except (ValueError, TypeError, AttributeError) as exc:
        raise ContractError('invalid approval expiry') from exc
    require(now.tzinfo is not None and expiry.tzinfo is not None, 'approval times need time zones')
    require(now < expiry, 'approval expired')
    require(action['operation_id'] not in used_operation_ids, 'operation requires outcome reconciliation')
    return {'status': 'binding-matches', 'action_sha256': digest, 'grants_authority': False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=('assignments', 'affected', 'retry', 'framing', 'action-digest'))
    parser.add_argument('--changed', nargs='*', default=[])
    args = parser.parse_args()
    try:
        record = read_json(sys.stdin.buffer.read(MAX_BYTES + 1))
        operations = {'assignments': validate_assignments, 'retry': retry_decision,
                      'framing': framing_decision, 'action-digest': lambda x: {'action_sha256': action_digest(x), 'grants_authority': False}}
        result = {'affected': affected_assignments(record, args.changed)} if args.operation == 'affected' else operations[args.operation](record)
        print(json.dumps(result, sort_keys=True))
        return 0
    except (ContractError, TypeError, KeyError) as exc:
        print(json.dumps({'status': 'invalid', 'error': str(exc)}, ensure_ascii=True))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
