"""Concrete proposal transformations used only through candidate_store's lock.

No external approval is authenticated here. The calling host must supply the
actual owner's decision for the exact digest/groups and maintain exclusive write
scope. Existing UTF-8 files only; adds/deletes require a separately reviewed patch.
"""
from __future__ import annotations

import difflib
import hashlib
import json
from pathlib import Path
import re


def sha(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def read_text(path):
    with path.open('r', encoding='utf-8', newline='') as handle:
        return handle.read()


def digest(proposal):
    return sha(json.dumps(proposal, sort_keys=True, separators=(',', ':'), ensure_ascii=True))


def target(root, name, allowed):
    path = Path(name)
    if name not in allowed or path.is_absolute() or '..' in path.parts or str(path) != name:
        raise ValueError('Proposal path is outside its approved candidate scope')
    current = root
    for part in path.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError('Proposal paths must not traverse symlinks')
    if not current.is_file() or not current.resolve().is_relative_to(root.resolve()):
        raise ValueError('Proposal target must be an existing repository file')
    if current.stat().st_size > 1024 * 1024:
        raise ValueError('Proposal file exceeds size limit')
    return current


def stage(root, request, candidate):
    if (set(request) != {'schema_version', 'candidate_id', 'edits', 'groups', 'validation'}
            or type(request['schema_version']) is not int or request['schema_version'] != 1):
        raise ValueError('Invalid staged proposal request')
    payload = candidate['payload']
    scope = payload.get('proposal')
    if not scope:
        raise ValueError('Staging requires a captured global proposal with accepted source provenance')
    edits, groups = request['edits'], request['groups']
    if not isinstance(edits, list) or not 1 <= len(edits) <= 20 or not isinstance(groups, dict) or not groups:
        raise ValueError('Proposal needs bounded edits and coherent groups')
    files = []
    for edit in edits:
        if not isinstance(edit, dict) or set(edit) != {'path', 'before_sha256', 'after_text'}:
            raise ValueError('Each edit requires path, before_sha256 and after_text')
        path = target(root, edit['path'], scope['allowed_files'])
        before = read_text(path)
        if sha(before) != edit['before_sha256']:
            raise ValueError('Stale proposal target: ' + edit['path'])
        after = edit['after_text']
        if not isinstance(after, str) or len(after.encode('utf-8')) > 1024 * 1024 or before == after:
            raise ValueError('Edit must contain a bounded actual UTF-8 change')
        files.append({'path': edit['path'], 'before': before, 'after': after,
                      'before_sha256': sha(before), 'after_sha256': sha(after),
                      'diff': ''.join(difflib.unified_diff(before.splitlines(True), after.splitlines(True),
                                                         fromfile='a/' + edit['path'], tofile='b/' + edit['path']))})
    names = [f['path'] for f in files]
    grouped = []
    for group, paths in groups.items():
        if (not isinstance(group, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,99}', group)
                or not isinstance(paths, list) or not paths or not all(isinstance(x, str) for x in paths)):
            raise ValueError('Invalid coherent group')
        grouped.extend(paths)
    if len(set(names)) != len(names) or sorted(grouped) != sorted(names):
        raise ValueError('Groups must partition edits exactly once')
    if not isinstance(request['validation'], str) or not request['validation'].strip():
        raise ValueError('Proposal requires validation evidence/command references')
    return {'schema_version': 1, 'candidate_id': request['candidate_id'],
            'source_project': payload['source_project'], 'source_lesson_id': payload['source_lesson_id'],
            'source_project_identity': payload.get('source_project_identity'),
            'allowed_files': scope['allowed_files'], 'files': files, 'groups': groups,
            'validation': request['validation'], 'evidence': payload['evidence']}


def selected_files(record, decision, *, rollback=False):
    if set(decision) != {'schema_version', 'proposal_id', 'proposal_sha256', 'groups', 'owner_decision'}:
        raise ValueError('Invalid proposal decision')
    if (type(decision['schema_version']) is not int or decision['schema_version'] != 1
            or decision['proposal_sha256'] != digest(record['proposal'])):
        raise ValueError('Decision is for different proposal contents')
    owner = decision['owner_decision']
    if not isinstance(owner, str) or not owner.strip() or len(owner) > 1000:
        raise ValueError('Actual owner decision reference is required')
    groups = decision['groups']
    if (not isinstance(groups, list) or not groups or not all(isinstance(x, str) for x in groups)
            or len(set(groups)) != len(groups)):
        raise ValueError('Select complete coherent groups')
    if not set(groups) <= record['proposal']['groups'].keys():
        raise ValueError('Unknown coherent group')
    if rollback and not set(groups) <= set(record.get('applied_groups', [])):
        raise ValueError('Cannot roll back groups that were not applied')
    paths = {p for g in groups for p in record['proposal']['groups'][g]}
    return [f for f in record['proposal']['files'] if f['path'] in paths]
