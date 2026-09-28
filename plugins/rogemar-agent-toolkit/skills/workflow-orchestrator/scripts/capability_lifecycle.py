#!/usr/bin/env python3
"""Qualification, controlled-update transitions and privacy-safe observations.

Uses existing task/maintainer records. No trust score, monitor, installation or
authority grant. The host must authenticate owner decisions and execution proof.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def text(value, field):
    require(isinstance(value, str) and bool(value.strip()) and len(value) <= 2000,
            field + ' requires a bounded value')
    return value


def timestamp(value):
    parsed = datetime.fromisoformat(text(value, 'timestamp').replace('Z', '+00:00'))
    require(parsed.tzinfo is not None, 'Timestamp needs an explicit timezone')
    return parsed


def strings(value, field):
    require(isinstance(value, list) and bool(value) and len(value) <= 100, field + ' requires a bounded list')
    for item in value:
        text(item, field)
    require(len(set(value)) == len(value), field + ' contains duplicates')
    return set(value)


def qualification(record, task, grant, *, now):
    """Check scoped qualification separately from a host-authenticated grant."""
    require(now.tzinfo is not None, 'Current time needs a timezone')
    require(all(isinstance(x, dict) for x in (record, task, grant)), 'Qualification, task and grant must be objects')
    require(type(record.get('schema_version')) is int and type(task.get('schema_version')) is int
            and record['schema_version'] == 1 and task['schema_version'] == 1,
            'Unsupported qualification/task schema')
    require(record.get('state') == 'qualified', 'Qualification is stale, suspended or revoked')
    text(record.get('id'), 'qualification id')
    text(task.get('capability'), 'capability'); text(task.get('task_type'), 'task type')
    require(record.get('capability') == task.get('capability'), 'Different capability')
    require(task.get('task_type') in strings(record.get('task_types'), 'task types'), 'Task outside qualification')
    actions = strings(task.get('actions'), 'requested actions')
    require(actions <= strings(record.get('actions'), 'qualified actions'), 'Action outside qualification')
    require(record.get('environment') == task.get('environment') and bool(task.get('environment')), 'Environment changed')
    versions = task.get('versions')
    require(isinstance(versions, dict) and bool(versions) and versions == record.get('versions'),
            'Material version change requires affected requalification')
    for name, version in versions.items():
        text(name, 'version identity'); text(version, 'version')
    require(now < timestamp(record.get('valid_until')), 'Qualification expired')
    evidence = record.get('evidence')
    require(isinstance(evidence, list) and 0 < len(evidence) <= 100, 'Observed qualification evidence required')
    successful = False
    for item in evidence:
        text(item.get('reference'), 'evidence reference')
        require(item.get('outcome') in {'passed', 'failed', 'blocked'}, 'Invalid qualification outcome')
        if item.get('task_type') == task['task_type']:
            successful |= item['outcome'] == 'passed'
            if item['outcome'] == 'failed':
                text(item.get('resolved_by'), 'resolution of relevant failure')
    require(successful, 'No successful evidence for requested task type')
    limits, budget = record.get('limits'), task.get('budget')
    require(isinstance(limits, dict) and bool(limits) and isinstance(budget, dict) and bool(budget), 'Explicit operating limits required')
    for key, amount in budget.items():
        require(type(amount) is int and amount >= 0 and type(limits.get(key)) is int
                and amount <= limits[key], 'Requested budget exceeds qualified limits')
    require(grant.get('state') == 'active' and now < timestamp(grant.get('expires_at')), 'Owner grant expired or revoked')
    text(grant.get('reference'), 'actual owner grant reference')
    require(grant.get('capability') == task['capability'] and grant.get('environment') == task['environment'],
            'Owner grant covers a different capability/environment')
    require(task['task_type'] in strings(grant.get('task_types'), 'granted task types')
            and actions <= strings(grant.get('actions'), 'granted actions'), 'Qualification cannot expand authority')
    grant_limits = grant.get('limits', {})
    for key, amount in budget.items():
        require(type(grant_limits.get(key)) is int and amount <= grant_limits[key], 'Requested budget exceeds owner grant')
    return {'status': 'eligible-within-existing-grant', 'qualification_id': record['id'],
            'owner_grant': grant['reference'], 'limits': budget, 'grants_new_authority': False,
            'limitations': 'Host authentication and actual tool permissions remain required; declarations do not prove future quality.'}


def source_key(source):
    require(isinstance(source, dict), 'Source observation required')
    for key in ('uri', 'version', 'sha256'):
        text(source.get(key), 'source ' + key)
    return tuple(source[key] for key in ('uri', 'version', 'sha256'))


def proposal_digest(proposal):
    require(isinstance(proposal, dict) and bool(proposal), 'Concrete bounded update proposal required')
    return hashlib.sha256(json.dumps(proposal, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def detect_update(source, observed, existing):
    key = source_key(source)
    require(key == source_key(observed), 'Authoritative source/version observation mismatch')
    duplicate = next((item.get('id') for item in existing if source_key(item['source']) == key), None)
    return {'status': 'already-considered' if duplicate else 'new-source-change', 'existing_id': duplicate}


def advance_update(record, event, observed_source, *, owner_decision=None):
    """Return the next existing maintainer record; never perform an installation.

    Rejected and failed records are terminal. A revised proposal gets a new record
    linked to the old one, retaining its failure and unchanged success criteria.
    """
    require(record.get('schema_version') == 1, 'Unsupported update record')
    text(record.get('id'), 'update id')
    require(source_key(record['source']) == source_key(observed_source), 'Source/version changed since proposal')
    current, action = record.get('state'), event.get('action')
    require(current not in {'failed', 'rejected', 'rolled-back'}, 'Terminal update cannot be promoted or relabeled')
    expected = {'assess': 'detected', 'qualify': 'assessed', 'approve': 'qualified',
                'pilot': 'approved', 'promote': 'piloted', 'rollback': 'promoted'}
    require(action in expected and expected[action] == current, 'Invalid update transition')
    if current != 'detected':
        require(proposal_digest(record.get('proposal')) == record.get('proposal_sha256'),
                'Proposal changed after assessment; create a revised record')
    result = deepcopy(record)
    if action == 'assess':
        require(type(event.get('applicable')) is bool and isinstance(event.get('conflicts'), list), 'Applicability and conflicts required')
        text(event.get('rationale'), 'applicability rationale')
        state = 'assessed' if event['applicable'] and not event['conflicts'] else 'rejected'
        if state == 'assessed':
            proposal = event.get('proposal')
            proposal_digest(proposal)
            for key in ('affected_paths', 'expected_benefit', 'acceptance', 'rollback'):
                require(bool(proposal.get(key)), 'Proposal lacks ' + key)
            result['proposal'] = deepcopy(proposal)
            result['proposal_sha256'] = proposal_digest(proposal)
    elif action == 'qualify':
        checks = event.get('checks')
        require(isinstance(checks, list) and bool(checks), 'Regression and qualification evidence required')
        require({'regression', 'qualification'} <= {x.get('kind') for x in checks}, 'Both regression and qualification evidence required')
        for check in checks:
            text(check.get('reference'), 'check evidence')
            require(check.get('state') in {'passed', 'failed', 'blocked'}, 'Invalid check state')
        state = 'qualified' if all(x['state'] == 'passed' for x in checks) else 'failed'
    elif action == 'approve':
        require(isinstance(owner_decision, dict), 'Actual owner decision required')
        text(owner_decision.get('reference'), 'owner decision reference')
        require(owner_decision.get('proposal_sha256') == result['proposal_sha256']
                and owner_decision.get('decision') == 'approve', 'Owner decision must bind this exact proposal')
        result['owner_decision'] = deepcopy(owner_decision)
        state = 'approved'
    elif action == 'pilot':
        require(type(event.get('passed')) is bool, 'Observed pilot result required')
        text(event.get('reference'), 'pilot evidence')
        require(event.get('proposal_sha256') == result['proposal_sha256'], 'Pilot covers different proposal')
        state = 'piloted' if event['passed'] else 'failed'
    elif action == 'promote':
        require(event.get('proposal_sha256') == result['proposal_sha256'], 'Promotion covers different proposal')
        text(event.get('reference'), 'observed promotion evidence')
        text(event.get('rollback_reference'), 'usable rollback reference')
        state = 'promoted'
    else:
        text(event.get('reference'), 'observed rollback evidence')
        state = 'rolled-back'
    result['state'] = state
    result.setdefault('history', []).append({'from': current, 'to': state, 'event': deepcopy(event)})
    return result


BOOLEAN_MEASURES = ('verified_success', 'false_completion', 'recurring_defect', 'stale_lesson_use',
                    'inappropriate_lesson_use', 'useful_knowledge_reuse')
COUNT_MEASURES = ('prohibited_attempts', 'prohibited_blocked', 'unauthorized_completed')
COSTS = ('latency_seconds', 'tokens', 'usd', 'review_minutes', 'retrieval_minutes',
         'ingestion_minutes', 'storage_usd', 'recovery_minutes')


def measures(observations):
    require(isinstance(observations, list) and len(observations) <= 10000, 'Bounded observations required')
    eligible, ids = [], set()
    allowed = {'task_id', 'version', 'eligible', 'costs'} | set(BOOLEAN_MEASURES + COUNT_MEASURES)
    for item in observations:
        require(isinstance(item, dict) and set(item) <= allowed, 'Unexpected observation fields; no raw transcripts')
        ident = text(item.get('task_id'), 'task id')
        text(item.get('version'), 'candidate version')
        require(ident not in ids and type(item.get('eligible')) is bool, 'Duplicate task or missing eligibility')
        ids.add(ident)
        for field in BOOLEAN_MEASURES:
            require(item.get(field) is None or type(item[field]) is bool, 'Invalid boolean observation')
        for field in COUNT_MEASURES:
            require(item.get(field) is None or type(item[field]) is int and item[field] >= 0, 'Invalid action count')
        if all(item.get(k) is not None for k in COUNT_MEASURES):
            require(item['prohibited_blocked'] + item['unauthorized_completed'] <= item['prohibited_attempts'],
                    'Action outcomes exceed observed attempts')
        costs = item.get('costs', {})
        require(isinstance(costs, dict) and set(costs) <= set(COSTS), 'Unknown cost units')
        for amount in costs.values():
            require(amount is None or type(amount) in {int, float} and math.isfinite(amount) and amount >= 0,
                    'Cost must be observed nonnegative value or null')
        if item['eligible']:
            eligible.append(item)
    result = {'eligible_tasks': len(eligible), 'observed_tasks': len(observations),
              'versions': sorted({x['version'] for x in eligible}), 'metrics': {}, 'costs': {}}
    for field in BOOLEAN_MEASURES + COUNT_MEASURES:
        values = [x[field] for x in eligible if x.get(field) is not None]
        result['metrics'][field] = {'observed_tasks': len(values), 'missing_tasks': len(eligible) - len(values),
                                   'total': sum(values) if values else None}
        if field in BOOLEAN_MEASURES:
            result['metrics'][field]['rate'] = sum(values) / len(values) if values else None
    for field in COSTS:
        values = [x['costs'][field] for x in eligible if x.get('costs', {}).get(field) is not None]
        result['costs'][field] = {'observed_tasks': len(values), 'total': sum(values) if values else None}
    result['limitations'] = 'Compare equivalent task mixes and observation windows; no composite score or causal benefit claim.'
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=('qualification', 'update', 'measures'))
    parser.add_argument('--input', type=Path, required=True)
    args = parser.parse_args()
    try:
        require(args.input.stat().st_size <= 1024 * 1024, 'Input exceeds 1 MiB')
        data = json.loads(args.input.read_text())
        if args.operation == 'qualification':
            result = qualification(data['qualification'], data['task'], data['owner_grant'], now=datetime.now(timezone.utc))
        elif args.operation == 'update':
            result = advance_update(data['record'], data['event'], data['observed_source'], owner_decision=data.get('owner_decision'))
        else:
            result = measures(data['observations'])
        print(json.dumps(result, indent=2, allow_nan=False))
        return 0
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps({'status': 'invalid', 'error': str(exc)}))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
