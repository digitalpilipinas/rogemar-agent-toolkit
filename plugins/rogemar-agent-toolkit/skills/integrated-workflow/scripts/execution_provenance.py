#!/usr/bin/env python3
"""Compare gate claims with independently supplied, protected execution observations.

The policy and observation digest must be produced/reviewed through a trusted
host channel outside candidate control. This module neither runs checks nor creates
that channel. Its results never certify semantic coverage or owner authorization.
"""
from __future__ import annotations
import hashlib
import json
import re
from typing import Any

MAX_BYTES = 1024 * 1024


class ProvenanceError(ValueError):
    pass


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ProvenanceError(message)


def unique(pairs):
    obj = {}
    for key, value in pairs:
        require(key not in obj, 'duplicate observation key')
        obj[key] = value
    return obj


def reject_constant(_):
    raise ProvenanceError('non-finite observation number')


def validate_execution(gate: dict[str, Any], candidate: dict[str, Any],
                       requirement: dict[str, Any], observation_bytes: bytes) -> dict[str, str]:
    required = {'observation_sha256', 'runner', 'check_id', 'environment_sha256'}
    require(isinstance(requirement, dict) and set(requirement) == required, 'invalid trusted execution requirement')
    for key in required:
        require(isinstance(requirement[key], str) and bool(requirement[key].strip()), 'empty trusted requirement')
    for key in ('observation_sha256', 'environment_sha256'):
        require(re.fullmatch(r'[0-9a-f]{64}', requirement[key]) is not None, 'invalid trusted digest')
    require(len(observation_bytes) <= MAX_BYTES, 'observation exceeds 1 MiB')
    require(hashlib.sha256(observation_bytes).hexdigest() == requirement['observation_sha256'], 'untrusted observation bytes')
    try:
        observed = json.loads(observation_bytes.decode('utf-8'), object_pairs_hook=unique, parse_constant=reject_constant)
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise ProvenanceError('invalid observation JSON') from exc
    require(isinstance(observed, dict), 'observation must be an object')
    expected_fields = {'schema_version', 'gate', 'candidate', 'runner', 'check_id', 'environment_sha256',
                       'run_id', 'exit_code', 'tests_executed', 'required_checks_complete', 'artifact_hashes'}
    require(set(observed) == expected_fields, 'unexpected or missing observation field')
    require(type(observed['schema_version']) is int and observed['schema_version'] == 1, 'unsupported observation schema')
    require(isinstance(gate, dict) and isinstance(candidate, dict) and bool(candidate), 'invalid gate or candidate')
    require(observed['candidate'] == candidate == gate.get('candidate'), 'stale execution candidate')
    require(observed['gate'] == gate.get('gate') and isinstance(observed['gate'], str), 'wrong execution gate')
    for key in ('runner', 'check_id', 'environment_sha256'):
        require(observed[key] == requirement[key], 'execution identity mismatch: ' + key)
    require(isinstance(observed['run_id'], str) and bool(observed['run_id'].strip())
            and len(observed['run_id']) <= 300, 'missing execution run ID')
    require(type(observed['exit_code']) is int and observed['exit_code'] == 0, 'execution failed')
    require(type(observed['tests_executed']) is int and observed['tests_executed'] > 0, 'no checks executed')
    require(observed['required_checks_complete'] is True, 'required checks incomplete or skipped')
    evidence = gate.get('evidence')
    require(isinstance(evidence, list) and bool(evidence), 'gate lacks artifacts')
    hashes = []
    for item in evidence:
        require(isinstance(item, dict), 'invalid artifact')
        digest = item.get('sha256')
        require(isinstance(digest, str) and re.fullmatch(r'[0-9a-f]{64}', digest) is not None, 'invalid artifact digest')
        hashes.append(digest)
    observed_hashes = observed['artifact_hashes']
    require(isinstance(observed_hashes, list) and all(isinstance(x, str) for x in observed_hashes), 'invalid observed artifacts')
    require(sorted(hashes) == sorted(observed_hashes), 'execution artifact set mismatch')
    return {'status': 'matches-protected-observation',
            'limitations': 'Policy authenticity and host isolation are external prerequisites; actual artifact integrity remains the checkpoint validator responsibility.'}
