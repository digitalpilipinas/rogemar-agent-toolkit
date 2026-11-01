#!/usr/bin/env python3
"""Single CI entrypoint. Hosted CI, any runner vendor and local agents run this.

    python3 -B scripts/ci.py                    full gate
    python3 -B scripts/ci.py --fast             pre-push subset: no packaging tests or archives
    python3 -B scripts/ci.py --receipt FILE     also write the receipt to FILE

Owner suites are selected against CI_BASE when set (a PR base or pushed range),
else the merge base with main, so every commit on a branch counts. An invalid
CI_BASE fails that step rather than falling back.

Every step runs even after a failure, so one run reports every gate. The JSON
receipt names the commit, whether the worktree was clean, each command's exit
code and duration, and the toolchain. It is evidence for that commit only; it
never stands in for a hosted CI result.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
PY = [sys.executable, '-B']
SLOW_TESTS = 'test_selection_install'
# Discover every test module except the slow packaging module (fast mode).
FAST_TESTS = ('import sys, unittest\n'
              'suite = unittest.defaultTestLoader.discover("tests")\n'
              'def keep(s):\n'
              '    for t in s:\n'
              '        if isinstance(t, unittest.TestSuite): yield from keep(t)\n'
              '        elif not t.id().startswith("%s."): yield t\n'
              'ok = unittest.TextTestRunner().run(unittest.TestSuite(keep(suite))).wasSuccessful()\n'
              'sys.exit(0 if ok else 1)\n') % SLOW_TESTS


def base_commit():
    """Comparison base for owner-suite selection: (base, error)."""
    supplied = os.environ.get('CI_BASE', '').strip()
    if supplied and set(supplied) != {'0'}:  # all zeros: a new branch or tag push has no base
        if git('rev-parse', '--verify', '--quiet', supplied + '^{commit}'):
            return supplied, None
        return None, 'CI_BASE %r is not a commit in this checkout' % supplied
    head = git('rev-parse', 'HEAD')
    for ref in ('origin/main', 'main'):  # the first that exists; a stale local main is not consulted
        base = git('merge-base', ref, 'HEAD')
        if base:
            if base != head:
                return base, None  # every commit on this branch, plus uncommitted changes
            break
    if git('rev-parse', '--verify', '--quiet', 'HEAD^{commit}^'):
        return 'HEAD^', None
    return None, 'no comparison base: set CI_BASE'


def git(*args):
    result = subprocess.run(['git', *args], cwd=ROOT, capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else ''


def steps(fast, dist):
    plan = [('verify', PY + ['scripts/toolkit.py', 'verify']),
            ('readme-inventory', PY + ['scripts/inventory_readme.py', '--check'])]
    if fast:
        return plan + [('unit-tests-fast', PY + ['-c', FAST_TESTS])]
    plan.append(('unit-tests', PY + ['-m', 'unittest', 'discover', '-s', 'tests']))
    base, error = base_commit()
    plan.append(('owner-suites', PY + ['scripts/select_checks.py', '--base', base, '--run'] if base
                 else PY + ['-c', 'raise SystemExit(%r)' % error]))
    return plan + [('forge-inventory', PY + ['scripts/verify_forge.py']),
                   ('package-core', PY + ['scripts/toolkit.py', 'package', '--output', str(dist / 'core')]),
                   ('package-all', PY + ['scripts/toolkit.py', 'package', '--profile', 'all',
                                         '--output', str(dist / 'all')])]


def version(command):
    if not shutil.which(command[0]):
        return None
    result = subprocess.run(command, capture_output=True, text=True)
    return (result.stdout or result.stderr).strip().splitlines()[0] if result.returncode == 0 else None


def run(fast=False, dist=None):
    # Resolve against the caller's folder; package commands run from ROOT.
    dist = Path(dist).resolve() if dist else Path(tempfile.mkdtemp(prefix='toolkit-ci-'))
    results = []
    for name, command in steps(fast, dist):
        print('\n== %s: %s' % (name, ' '.join(command[:4])), flush=True)
        started = time.time()
        code = subprocess.run(command, cwd=ROOT, stdin=subprocess.DEVNULL).returncode
        results.append({'step': name, 'command': command, 'exit_code': code,
                        'seconds': round(time.time() - started, 1)})
    status = subprocess.run(['git', 'status', '--porcelain'], cwd=ROOT, capture_output=True, text=True)
    clean = status.stdout.strip() == '' if status.returncode == 0 else None  # None: unknown
    return {'schema_version': 1, 'mode': 'fast' if fast else 'full',
            'status': 'passed' if all(r['exit_code'] == 0 for r in results) else 'failed',
            'commit': git('rev-parse', 'HEAD') or None,
            'clean_worktree': clean,
            'steps': results,
            'toolchain': {'python': platform.python_version(), 'os': platform.platform(),
                          'node': version(['node', '--version']), 'bun': version(['bun', '--version'])},
            'scope': 'Evidence for this commit only; never a hosted CI result.'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--fast', action='store_true', help='pre-push subset')
    parser.add_argument('--receipt', type=Path, help='also write the receipt JSON here')
    parser.add_argument('--dist', type=Path, help='archive output folder (default: a new temp folder)')
    parser.add_argument('--print-base', action='store_true', help='print the owner-suite base and exit')
    args = parser.parse_args(argv)
    if args.print_base:
        base, error = base_commit()
        print(base or '')
        return 0 if base else (print(error, file=sys.stderr) or 1)
    receipt = run(args.fast, args.dist)
    text = json.dumps(receipt, indent=2)
    print('\n' + text)
    if args.receipt:
        args.receipt.write_text(text + '\n')
    return 0 if receipt['status'] == 'passed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
