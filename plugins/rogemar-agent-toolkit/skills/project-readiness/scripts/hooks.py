#!/usr/bin/env python3
"""Opt-in harness hooks around project readiness. Read-only toward the project.

  hooks.py session-start   readiness status and situation map for the session
  hooks.py prompt          only the situation rows a request mentions (stdin: hook JSON)
  hooks.py stop            warn when changed files call for unrecorded methods
  hooks.py claude-settings print the Claude Code settings snippet for owner approval

Each command reads the harness's hook JSON on stdin when present and never fails the
harness: errors become a short note. The only file written is a per-project cache of
the situation map in the system temp folder, outside the repository.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve()
SKILLS = HERE.parents[2]
INDEX = SKILLS / 'workflow-orchestrator/references/skill-routing.json'
MAX_PROMPT_NOTE = 600


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def hook_input():
    try:
        data = json.loads(sys.stdin.read() or '{}') if not sys.stdin.isatty() else {}
    except ValueError:
        data = {}
    return data if isinstance(data, dict) else {}


def project_root(data):
    cwd = data.get('cwd') or os.getcwd()
    try:
        return Path(subprocess.check_output(['git', '-C', cwd, 'rev-parse', '--show-toplevel'],
                                            stderr=subprocess.DEVNULL, timeout=10).decode().strip())
    except (OSError, subprocess.SubprocessError):
        return Path(cwd)


def cache_path(root):
    folder = Path(os.environ.get('PROJECT_READINESS_CACHE', tempfile.gettempdir())) / 'project-readiness'
    return folder / (hashlib.sha256(str(root).encode()).hexdigest()[:16] + '.json')


def session_start(data):
    root = project_root(data)
    readiness = load('readiness', HERE.with_name('readiness.py'))
    index = json.loads(INDEX.read_text())
    plan = readiness.plan(root, index)
    rows = situation_rows(root, index, readiness)
    path = cache_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({'status': plan['status'], 'rows': rows}))
    lines = ['Project readiness: %s (plan %s). %s' % (plan['status'], plan['plan_id'][:12], plan['next_action'])]
    if rows:
        lines.append('Situation map (technology -> skills that may apply):')
        lines += ['- %s: %s' % (tag, ', '.join(names)) for tag, names in rows.items()]
    lines.append('Announce the playbook and selected skills at slice start; record each in the method receipt.')
    return '\n'.join(lines)


def situation_rows(root, index, readiness):
    files, _ = readiness.project_files(root)
    tags = readiness.detect_tags(root, index.get('task_tags', {}), files)
    rows = {}
    for tag in sorted(tags):
        names = sorted(n for n, r in index.get('skills', {}).items()
                       if tag in r.get('task_tags_any', []) and r.get('activation') == 'conditional')
        if names:
            rows[tag] = names
    return rows


def prompt_note(data):
    root = project_root(data)
    try:
        cached = json.loads(cache_path(root).read_text())
    except (OSError, ValueError):
        return ''
    text = str(data.get('prompt', '')).lower()
    hits = {tag: names for tag, names in cached.get('rows', {}).items()
            if tag.replace('-', ' ') in text or tag in text or any(n in text for n in names)}
    if not hits:
        return ''
    note = 'Skills that may apply to this request: ' + '; '.join(
        '%s -> %s' % (tag, ', '.join(names)) for tag, names in hits.items())
    return note[:MAX_PROMPT_NOTE]


def stop_warning(data, receipt=None):
    if data.get('stop_hook_active'):
        return ''  # already continuing because of a stop hook: never loop
    root = project_root(data)
    checkpoint_path = SKILLS / 'integrated-workflow/scripts/checkpoint.py'
    if not checkpoint_path.is_file():
        return ''
    checkpoint = load('checkpoint_hook', checkpoint_path)
    try:
        changed = subprocess.check_output(['git', '-C', str(root), 'status', '--porcelain', '--untracked-files=all'],
                                          stderr=subprocess.DEVNULL, timeout=20).decode().splitlines()
    except (OSError, subprocess.SubprocessError):
        return ''
    paths = [line[3:].split(' -> ')[-1] for line in changed if len(line) > 3]
    index = checkpoint.load_index({})
    required = checkpoint.required_methods(index, checkpoint.candidate_tags(root, paths, index))
    if not required:
        return ''
    recorded = set()
    if receipt:
        try:
            recorded = {r.get('id') for r in json.loads((root / receipt).read_text()).get('methods', [])}
        except (OSError, ValueError, AttributeError):
            recorded = set()
    missing = [group for group, names in required.items() if not set(names) & recorded]
    if not missing:
        return ''
    return ('Method receipt: these changes call for %s, not yet recorded as used, unavailable, '
            'blocked or not applicable.' % ', '.join(missing))


def claude_settings(receipt=None):
    script = str(HERE)
    stop = 'python3 -B "%s" stop' % script + (' --receipt "%s"' % receipt if receipt else '')
    command = lambda sub: {'type': 'command', 'command': 'python3 -B "%s" %s' % (script, sub)}
    return {'hooks': {
        'SessionStart': [{'matcher': 'startup|resume|compact', 'hooks': [command('session-start')]}],
        'UserPromptSubmit': [{'hooks': [command('prompt')]}],
        'Stop': [{'hooks': [{'type': 'command', 'command': stop}]}],
    }}


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    command = argv[0] if argv else ''
    receipt = argv[argv.index('--receipt') + 1] if '--receipt' in argv[:-1] else None
    try:
        if command == 'claude-settings':
            print(json.dumps(claude_settings(receipt), indent=2))
            return 0
        data = hook_input()
        if command == 'session-start':
            print(session_start(data))
        elif command == 'prompt':
            note = prompt_note(data)
            if note:
                print(note)
        elif command == 'stop':
            warning = stop_warning(data, receipt)
            if warning:  # shown to the owner, and fed back to the agent without blocking
                print(json.dumps({'systemMessage': warning, 'hookSpecificOutput': {
                    'hookEventName': 'Stop', 'additionalContext': warning}}))
        else:
            print(__doc__, file=sys.stderr)
            return 2
    except Exception as exc:  # a hook must never break the session
        print('project-readiness hook unavailable: %s' % exc, file=sys.stderr)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
