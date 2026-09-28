#!/usr/bin/env python3
"""Select owner-local checks for changed behavior. Does not install dependencies.

Repository-required lock/verify, root tests and package gates remain separate.
Use the same selection locally and in applicable PR validation.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
S = 'plugins/rogemar-agent-toolkit/skills/'
CHECKS = {
    'learning': [sys.executable, '-B', S + 'project-learning/scripts/test_project_learning.py'],
    'terminal': [sys.executable, '-B', '-m', 'unittest', 'discover', '-s',
                 S + 'agent-collaboration-terminal/tests', '-v'],
    'forge-plan': ['node', '--test', S + 'codex-forge/scripts/check-plan.test.mjs'],
    'forge-native': ['bun', 'run', 'test'],
}


def select(paths):
    selected = set()
    for path in paths:
        if path in {'scripts/select_checks.py', '.github/workflows/validate.yml'}:
            selected.update(CHECKS)
        if path.startswith(S + 'project-learning/scripts/'):
            selected.add('learning')
        if path.startswith(S + 'agent-collaboration-terminal/') and path.endswith(('.py', '.sh', '.json')):
            selected.add('terminal')
        if path.startswith(S + 'codex-forge/scripts/check-plan'):
            selected.add('forge-plan')
        if path.startswith(S + 'codex-forge/scripts/') and path.endswith(('.ts', 'package.json', 'bun.lock')):
            selected.add('forge-native')
        # These root tests exercise shared executable contracts used by owner suites.
        if path in {'tests/test_alignment_contracts.py', 'tests/test_learning_lifecycle.py'}:
            selected.add('learning')
    return sorted(selected)


def changed_paths(root, base):
    commit = subprocess.check_output(['git', 'rev-parse', '--verify', '--end-of-options', base + '^{commit}'],
                                     cwd=root, text=True).strip()
    tracked = subprocess.check_output(['git', 'diff', '--name-only', '-z', commit, '--'], cwd=root)
    added = subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard', '-z'], cwd=root)
    return sorted(set(p.decode('utf-8') for p in (tracked + added).split(b'\0') if p))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--base', required=True)
    parser.add_argument('--run', action='store_true')
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        names = select(changed_paths(root, args.base))
    except (OSError, subprocess.CalledProcessError) as exc:
        print(json.dumps({'status': 'failed', 'error': str(exc)}))
        return 1
    results = []
    failed = False
    for name in names:
        command = CHECKS[name]
        row = {'check': name, 'command': command, 'state': 'selected'}
        if args.run:
            if not shutil.which(command[0]):
                row.update(state='blocked', reason='required executable unavailable')
                failed = True
            else:
                cwd = root / (S + 'codex-forge/scripts') if name == 'forge-native' else root
                code = subprocess.run(command, cwd=cwd, check=False).returncode
                row.update(state='passed' if code == 0 else 'failed', exit_code=code)
                failed |= code != 0
        results.append(row)
    print(json.dumps({'checks': results, 'status': 'failed' if failed else ('completed' if args.run else 'selected'),
                      'unselected': 'not applicable to observed changed paths; inspect semantic dependencies separately'}, indent=2))
    return int(failed)


if __name__ == '__main__':
    raise SystemExit(main())
