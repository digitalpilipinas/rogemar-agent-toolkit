#!/usr/bin/env python3
"""Pure optional lifecycle metadata for the existing project-learning writer.

No store, hook, promotion authority, or transcript collector is created here.
Existing ledger Status values retain their meaning; activity/freshness are separate.
"""
from __future__ import annotations
import hashlib
import json
import re
import unicodedata
from datetime import datetime
from typing import Any


class LifecycleError(ValueError):
    pass


def require(ok: bool, message: str) -> None:
    if not ok:
        raise LifecycleError(message)


def _text(value: Any, name: str) -> str:
    require(isinstance(value, str) and bool(value.strip()) and len(value) <= 700,
            name + ' must be a nonempty bounded string')
    require(not any(unicodedata.category(c) in {'Cc', 'Cf', 'Cs'} for c in value), name + ' must be one line')
    return value


def validate_lifecycle(value: Any) -> dict[str, Any]:
    require(isinstance(value, dict), 'lifecycle must be an object')
    required = {'schema_version', 'activity', 'verified_at', 'source_versions',
                'evidence_roots', 'review_trigger', 'failure_class', 'counterexamples'}
    require(set(value) == required, 'unexpected or missing lifecycle field')
    require(type(value['schema_version']) is int and value['schema_version'] == 1, 'unsupported lifecycle schema')
    require(isinstance(value['activity'], str) and value['activity'] in {'active', 'quarantined', 'retired'}, 'invalid activity')
    require(isinstance(value['failure_class'], str) and value['failure_class'] in {'not-applicable', 'guidance', 'context', 'retrieval', 'routing',
                                     'noncompliance', 'tool', 'environment', 'implementation', 'unknown'},
            'invalid failure class')
    at = value['verified_at']
    if at is not None:
        _text(at, 'verified_at')
        try:
            parsed = datetime.fromisoformat(at.replace('Z', '+00:00'))
        except ValueError as exc:
            raise LifecycleError('invalid verification time') from exc
        require(parsed.tzinfo is not None, 'verification time requires a timezone')
    versions = value['source_versions']
    require(isinstance(versions, dict) and len(versions) <= 50, 'source_versions must be a bounded object')
    for key, revision in versions.items():
        _text(key, 'source identity')
        _text(revision, 'source version')
    for key in ('evidence_roots', 'counterexamples'):
        values = value[key]
        require(isinstance(values, list) and len(values) <= 50, key + ' must be a bounded array')
        for item in values:
            _text(item, key)
        require(len(set(values)) == len(values), 'duplicate ' + key)
    _text(value['review_trigger'], 'review_trigger')
    # Bound the complete encoded record as well as each field so the writer
    # cannot produce a line that the ledger reader would later reject.
    encoded = json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":"))
    require(len(encoded) + 1 <= 100_000, 'lifecycle record exceeds ledger line bounds')
    # Return a detached value, never mutate caller-owned state.
    return json.loads(encoded)


def _unique_pairs(pairs):
    out = {}
    for key, value in pairs:
        require(key not in out, 'duplicate lifecycle JSON key')
        out[key] = value
    return out


def section_lifecycle(section: str) -> dict[str, Any] | None:
    matches = re.findall(r'^Lifecycle:([^\n]*)$', section, re.M)
    require(len(matches) <= 1, 'duplicate lifecycle lines')
    if not matches:
        return None
    require(len(matches[0]) <= 100_000, 'lifecycle line exceeds bounds')
    try:
        return validate_lifecycle(json.loads(matches[0], object_pairs_hook=_unique_pairs))
    except (ValueError, TypeError, RecursionError) as exc:
        raise LifecycleError('invalid lifecycle line') from exc


def section_active(section: str) -> bool:
    value = section_lifecycle(section)
    return value is None or value['activity'] == 'active'


def assess_lifecycle(value: Any, current_versions: dict[str, str], *, accepted: bool) -> dict[str, Any]:
    value = validate_lifecycle(value)
    require(type(accepted) is bool and isinstance(current_versions, dict), 'invalid applicability context')
    changed, unavailable = [], []
    for identity, revision in value['source_versions'].items():
        if identity not in current_versions:
            unavailable.append(identity)
        elif current_versions[identity] != revision:
            changed.append(identity)
    freshness = ('stale' if changed else 'unverified' if unavailable or value['verified_at'] is None
                 or not value['source_versions'] else 'matches-recorded-versions')
    return {'accepted': accepted, 'activity': value['activity'], 'freshness': freshness,
            'changed_sources': sorted(changed), 'unavailable_sources': sorted(unavailable),
            'eligible_for_source_review': accepted and value['activity'] == 'active' and not changed and not unavailable,
            'limitations': 'Matching declarations do not authenticate evidence, prove correctness, or establish semantic applicability.'}


def replace_lifecycle(ledger: str, candidate_id: str, value: Any, expected_sha256: str) -> str:
    """Build new ledger text. Existing sole writer supplies locking and persistence."""
    require(isinstance(candidate_id, str) and re.fullmatch(r'PL-[A-F0-9]{12}', candidate_id) is not None, 'invalid candidate ID')
    require(hashlib.sha256(ledger.encode('utf-8')).hexdigest() == expected_sha256, 'stale ledger proposal')
    value = validate_lifecycle(value)
    pattern = re.compile(r'(^## ' + re.escape(candidate_id) + r'\s*$)(.*?)(?=^## PL-[A-F0-9]{12}\s*$|\Z)', re.M | re.S)
    matches = list(pattern.finditer(ledger))
    require(len(matches) == 1, 'missing or duplicate accepted entry')
    match = matches[0]
    section = match.group(2)
    require(re.search(r'^Status: (?:Accepted|Reinforced)$', section, re.M) is not None,
            'lifecycle changes require an accepted or reinforced entry')
    section_lifecycle(section)  # Refuse malformed existing metadata, never silently repair it.
    line = 'Lifecycle: ' + json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(',', ':'))
    if re.search(r'^Lifecycle: ', section, re.M):
        section = re.sub(r'^Lifecycle: .+$', lambda _: line, section, flags=re.M)
    else:
        section = section.rstrip('\n') + '\n' + line + '\n\n'
    return ledger[:match.start(2)] + section + ledger[match.end(2):]
