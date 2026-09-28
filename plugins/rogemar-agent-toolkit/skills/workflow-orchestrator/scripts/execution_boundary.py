#!/usr/bin/env python3
"""Opt-in host adapter for the existing orchestrator, not a second dispatcher.

The host owns authentication, registered tools, a protected state database and
OS/network permissions. Do not put this database or trusted callbacks under the
candidate's write access. Import this module at the host's action boundary.
Standalone declarations and unit fixtures do not provision such a host.
"""
from copy import deepcopy
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import sqlite3


def sibling(name):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


contracts = sibling('workflow_contracts')
lifecycle = sibling('capability_lifecycle')


def transition(record, assignment_id, state, *, evidence=None):
    """Apply a checked transition to the caller's existing coordination record."""
    contracts.validate_assignments(record)
    result = deepcopy(record)
    task = next((x for x in result['assignments'] if x['id'] == assignment_id), None)
    contracts.require(task is not None, 'Unknown assignment')
    allowed = {'pending': {'running', 'blocked', 'cancelled'},
               'running': {'passed', 'failed', 'blocked', 'cancelled'}}
    contracts.require(state in allowed.get(task['state'], set()), 'Invalid assignment transition')
    if state == 'passed':
        contracts.require(isinstance(evidence, str) and bool(evidence.strip()), 'Observed completion evidence required')
        task['evidence'] = [evidence]
        task['candidate'] = result.get('candidate')
    task['state'] = state
    contracts.validate_assignments(result)
    return result


def invalidate(record, changed):
    affected = contracts.affected_assignments(record, changed)
    result = deepcopy(record)
    for task in result['assignments']:
        if task['id'] in affected:
            contracts.require(task['state'] != 'running', 'Cancel and reconcile active work before invalidation')
            task['state'] = 'pending'
            task.pop('evidence', None)
    contracts.validate_assignments(result)
    return result


class ActionBoundary:
    """Single-use complete-action binding, live grants and explicit uncertainty.

    authenticate(action) must look up the current authenticated owner decision,
    not echo approval data from action arguments. A callback exception, including
    a process interruption after reservation, leaves the operation uncertain.
    The host reconciles that operation outside this adapter before a new action.
    """
    def __init__(self, database, authenticate, registered_tools):
        self.database = str(database)
        self.authenticate = authenticate
        self.tools = dict(registered_tools)
        with sqlite3.connect(self.database) as connection:
            connection.execute('CREATE TABLE IF NOT EXISTS operations (id TEXT PRIMARY KEY, digest TEXT NOT NULL, state TEXT NOT NULL)')
            connection.execute('CREATE TABLE IF NOT EXISTS budgets (grant_id TEXT PRIMARY KEY, consumed TEXT NOT NULL)')

    def execute(self, action, *, now=None):
        # Freeze input before lookup and invocation so a caller cannot mutate the
        # arguments after approval validation or during callback execution.
        action = deepcopy(action)
        now = now or datetime.now(timezone.utc)
        digest = contracts.action_digest(action)
        trusted = self.authenticate(deepcopy(action))
        contracts.require(isinstance(trusted, dict), 'Authenticated host decision unavailable')
        lifecycle.qualification(trusted['qualification'], trusted['task'], trusted['grant'], now=now)
        contracts.require(action['tool'] in trusted['task']['actions'], 'Tool outside qualified action scope')
        contracts.require(action['tool'] in self.tools, 'Tool has no registered host adapter')
        contracts.check_action_binding(action, trusted['approval'], now=now, used_operation_ids=set())
        with sqlite3.connect(self.database) as connection:
            connection.execute('BEGIN IMMEDIATE')
            grant_id = trusted['grant']['reference']
            previous = connection.execute('SELECT consumed FROM budgets WHERE grant_id = ?', (grant_id,)).fetchone()
            consumed = json.loads(previous[0]) if previous else {}
            for key, amount in trusted['task']['budget'].items():
                consumed[key] = consumed.get(key, 0) + amount
                contracts.require(consumed[key] <= trusted['grant']['limits'][key], 'Cumulative owner budget exhausted')
            try:
                connection.execute('INSERT INTO operations VALUES (?, ?, ?)',
                                   (action['operation_id'], digest, 'uncertain'))
            except sqlite3.IntegrityError as exc:
                raise ValueError('Operation already reserved; reconcile its outcome before further action') from exc
            connection.execute('INSERT OR REPLACE INTO budgets VALUES (?, ?)', (grant_id, json.dumps(consumed)))
        result = self.tools[action['tool']](deepcopy(action))
        with sqlite3.connect(self.database) as connection:
            connection.execute('UPDATE operations SET state = ? WHERE id = ? AND digest = ?',
                               ('completed', action['operation_id'], digest))
        return result
