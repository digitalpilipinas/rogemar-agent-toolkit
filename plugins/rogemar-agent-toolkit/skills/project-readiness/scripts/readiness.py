#!/usr/bin/env python3
"""Read-only project readiness: detected technologies, toolkit footprints, one setup plan.

Writes nothing, installs nothing and grants no authority. The owner approves the
printed plan once; agents then apply its items with their normal tools.

  readiness.py plan  --root PROJECT [--record FILE] [--json]
  readiness.py map   --root PROJECT [--skills-root DIR]
  readiness.py pins  --policy FILE --validator FILE [--provenance FILE]
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve()
DEFAULT_INDEX = HERE.parents[2] / 'workflow-orchestrator/references/skill-routing.json'
DEFAULT_RECORD = '.agents/readiness.json'
INSTRUCTION_FILES = ('AGENTS.md', 'CLAUDE.md', 'GEMINI.md', '.github/copilot-instructions.md')
INSTRUCTION_LINE = ('At the start or resume of any task in this repository, run the '
                    '`project-readiness` skill before planning or execution.')
SKIP_DIRS = {'.git', 'node_modules', '.build', 'build', 'dist', 'DerivedData', 'Pods', '.venv',
             'venv', '__pycache__', '.next', '.turbo', '.gradle', 'target', '.agent-map'}
MAX_FILES = 20000
MAX_CONTENT_FILES = 300  # per marker, so one absent marker cannot starve the others
MAX_BYTES = 65536


def project_files(root):
    """Bounded walk of project-relative paths; skips dependency and build folders."""
    found = []
    for current, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        rel = Path(current).relative_to(root)
        found.extend((rel / name).as_posix() for name in sorted(files + dirs))
        if len(found) > MAX_FILES:
            return found[:MAX_FILES], True
    return found, False


def glob_match(path, pattern):
    pattern = pattern.rstrip('/')
    candidates = {pattern, pattern[3:] if pattern.startswith('**/') else pattern}
    return any(fnmatch.fnmatchcase(path, p) or fnmatch.fnmatchcase(Path(path).name, p)
               if '/' not in p else fnmatch.fnmatchcase(path, p) for p in candidates)


def detect_tags(root, task_tags, files):
    tags = {}
    for tag, entry in sorted(task_tags.items()):
        for marker in entry.get('markers', []):
            hits = [f for f in files if glob_match(f, marker['glob'])]
            if 'contains' in marker:
                needle, matched, read = marker['contains'], None, 0
                for hit in hits:
                    if read >= MAX_CONTENT_FILES:
                        break
                    read += 1
                    try:
                        with open(root / hit, 'rb') as handle:
                            if needle.encode() in handle.read(MAX_BYTES):
                                matched = hit
                                break
                    except OSError:
                        continue
                hits = [matched] if matched else []
            if hits:
                tags[tag] = hits[0]
                break
    return tags


def git_state(root, path):
    """Return (exists, tracked, ignored) for one footprint path; None when Git is unavailable."""
    special = min([i for i in (path.find('<'), path.find('*')) if i >= 0], default=-1)
    concrete = path if special < 0 else path[:special].rsplit('/', 1)[0] + '/'
    target = root / concrete
    try:
        tracked = bool(subprocess.run(['git', '-C', str(root), 'ls-files', '--', concrete],
                                      capture_output=True, check=True, timeout=30).stdout.strip())
        ignored = subprocess.run(['git', '-C', str(root), 'check-ignore', '-q', '--no-index', concrete],
                                 capture_output=True, timeout=30).returncode == 0
    except (OSError, subprocess.SubprocessError):
        return target.exists(), None, None
    return target.exists(), tracked, ignored


def footprint_item(root, entry, location):
    path = location or entry['path']
    exists, tracked, ignored = git_state(root, path)
    item = {'id': 'footprint:' + entry['path'], 'path': path, 'owner': entry['owner'],
            'class': entry['class'], 'expected': entry['tracking']}
    if tracked is None:
        return dict(item, kind='observation', state='unavailable', action='Inspect manually; Git is unavailable.')
    if entry['tracking'] == 'tracked' and ignored:
        return dict(item, kind='ignore-rule', state='needs-owner',
                    action='Unignore this path so its records can be committed.')
    if entry['tracking'] == 'ignored' and tracked:
        # An ignore rule does not untrack files Git already tracks.
        return dict(item, kind='ignore-rule', state='needs-owner',
                    action='Stop tracking this path (git rm -r --cached) and ignore it.')
    parent = Path(path.rstrip('/')).parent
    in_use = exists or (parent != Path('.') and (root / parent).is_dir())
    if entry['tracking'] == 'ignored' and not ignored and in_use:
        return dict(item, kind='ignore-rule', state='needs-owner',
                    action='Ignore this generated or local path before it is first written.')
    state = 'satisfied' if exists else 'created-when-needed'
    return dict(item, kind='observation', state=state, action='None.')


def instruction_item(root):
    present = [name for name in INSTRUCTION_FILES if (root / name).is_file()]
    for name in present:
        try:
            if 'project-readiness' in (root / name).read_text(errors='ignore'):
                return {'id': 'instruction', 'kind': 'instruction', 'path': name, 'state': 'satisfied',
                        'action': 'None.'}
        except OSError:
            continue
    target = present[0] if present else 'AGENTS.md'
    return {'id': 'instruction', 'kind': 'instruction', 'path': target, 'state': 'needs-owner',
            'action': 'Add this line: ' + INSTRUCTION_LINE}


def load_record(root, record):
    path = root / (record or DEFAULT_RECORD)
    if not path.is_file():
        return {}
    data = json.loads(path.read_text())
    if not isinstance(data, dict):
        raise ValueError('readiness record must be an object')
    return data


def plan(root, index, record=None, skills_root=HERE.parents[2]):
    files, truncated = project_files(root)
    tags = detect_tags(root, index.get('task_tags', {}), files)
    data = load_record(root, record)
    locations = data.get('locations', {}) if isinstance(data.get('locations', {}), dict) else {}
    routes = index.get('skills', {})

    def installed(owner):
        names = [owner] if owner in routes else [n for n, r in routes.items() if r.get('dependency') == owner]
        return any((skills_root / name / 'SKILL.md').is_file() for name in names)

    def relevant(entry):
        # A footprint applies when its owner is installed and applies here, or its path is in use.
        route = routes.get(entry['owner'])
        owner_tags = set(route.get('task_tags_any', [])) if route else None
        return ((installed(entry['owner']) and owner_tags is not None and (not owner_tags or owner_tags & set(tags)))
                or (root / (locations.get(entry['path']) or entry['path']).split('<')[0].split('*')[0]).exists())

    items = [footprint_item(root, entry, locations.get(entry['path']))
             for entry in index.get('footprints', []) if relevant(entry)]
    items.append(instruction_item(root))
    pending = [i for i in items if i['state'] in ('needs-owner', 'unavailable')]
    # The id covers only what the owner approves, so recording an approval (or a file
    # appearing on first use) does not change it.
    canonical = json.dumps([{k: i[k] for k in ('id', 'path', 'kind', 'state', 'action')} for i in pending],
                           sort_keys=True).encode()
    plan_id = hashlib.sha256(canonical).hexdigest()
    approved = data.get('approved_plan_id') == plan_id
    declined = data.get('declined_plan_id') == plan_id
    if any(i['state'] == 'unavailable' for i in items):
        status = 'unavailable'  # missing evidence is never ready, approved or not
    elif not pending:
        status = 'ready'
    elif approved:
        status = 'approved'  # owner approved; items still need applying, so not ready
    else:
        status = 'declined' if declined else 'needs-owner'
    return {'schema_version': 1, 'plan_id': plan_id, 'grants_authority': False, 'status': status,
            'approved': approved, 'detected_tags': tags, 'scan_truncated': truncated,
            'items': items,
            'next_action': ('None; readiness is current.' if status == 'ready' else
                            'None this session; the owner declined this plan. Ask again only when it changes.'
                            if status == 'declined' else
                            'Inspect the unavailable items; readiness cannot be confirmed.' if status == 'unavailable' else
                            'Apply the approved items; do not ask the owner again.' if status == 'approved' else
                            'Show the owner the needs-owner items once; after approval, apply them '
                            'and record approved_plan_id in ' + (record or DEFAULT_RECORD) + '.')}


def situation_map(root, index, skills_root=HERE.parents[2]):
    files, truncated = project_files(root)
    tags = detect_tags(root, index.get('task_tags', {}), files)
    skills = index.get('skills', {})
    rows = []
    for tag in sorted(tags):
        names = sorted(n for n, r in skills.items() if tag in r.get('task_tags_any', [])
                       and r.get('activation') == 'conditional')
        if names:
            rows.append((tag, names))
    lines = ['# Situation map', '',
             'Generated by `project-readiness`; routing stays with `workflow-orchestrator`.',
             'Technologies detected: ' + (', '.join('`%s`' % t for t in sorted(tags)) or 'none') + '.'
             + (' The scan stopped at %d paths, so this may be incomplete.' % MAX_FILES if truncated else ''), '',
             'Entry and process skills (`create-plan`, the harness Forge entry, `integrated-workflow`, '
             '`workflow-orchestrator`) apply to every task; rows add technology-specific skills.', '',
             '| Situation | Skills that may apply |', '| --- | --- |']
    lines += ['| `%s` work | %s |' % (tag, ', '.join('`%s`' % n for n in names)) for tag, names in rows]
    if skills_root and Path(skills_root).is_dir():
        unmanaged = sorted(d.name for d in Path(skills_root).iterdir()
                           if (d / 'SKILL.md').is_file() and d.name not in skills)
        if unmanaged:
            lines += ['', 'Installed, not managed by the toolkit: ' + ', '.join('`%s`' % n for n in unmanaged) + '.']
    return '\n'.join(lines) + '\n'


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def pins(policy, validator, provenance=None):
    out = {'policy_sha256': sha256(policy), 'validator_sha256': sha256(validator),
           'command': ('python3 -B %s --root ROOT --base COMMIT --phase accept --receipt RECEIPT.json '
                       '--trusted-policy %s --policy-sha256 %s --validator-sha256 %s'
                       % (validator, policy, sha256(policy), sha256(validator)))}
    if provenance:
        out['provenance_validator_sha256'] = sha256(provenance)
    return out


CI_TEMPLATE = """# Method-receipt check for pull requests. Owner-approved starting point; adapt before use.
# The checkpoint, its routing index and the policy come from the protected base branch, never the PR head.
name: Method receipt
on: pull_request
permissions:
  contents: read
jobs:
  receipt:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Trusted copies from the base branch
        run: |
          T="$RUNNER_TEMP/trusted"
          mkdir -p "$T/integrated-workflow/scripts" "$T/workflow-orchestrator/references"
          git show "origin/${{ github.base_ref }}:{skills}/integrated-workflow/scripts/checkpoint.py" > "$T/integrated-workflow/scripts/checkpoint.py"
          git show "origin/${{ github.base_ref }}:{skills}/workflow-orchestrator/references/skill-routing.json" > "$T/workflow-orchestrator/references/skill-routing.json"
          git show "origin/${{ github.base_ref }}:{policy}" > "$T/policy.json"
      - name: Check the receipt
        run: |
          python3 -B "$RUNNER_TEMP/trusted/integrated-workflow/scripts/checkpoint.py" --root "$GITHUB_WORKSPACE" \\
            --base "origin/${{ github.base_ref }}" --phase accept --receipt {receipt} \\
            --trusted-policy "$RUNNER_TEMP/trusted/policy.json" \\
            --policy-sha256 "${{ vars.RECEIPT_POLICY_SHA256 }}" \\
            --validator-sha256 "${{ vars.RECEIPT_VALIDATOR_SHA256 }}"
"""


def ci_template(skills, policy, receipt):
    return CI_TEMPLATE.replace('{skills}', skills.rstrip('/')).replace('{policy}', policy).replace('{receipt}', receipt)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('plan', 'map'):
        p = sub.add_parser(name)
        p.add_argument('--root', type=Path, required=True)
        p.add_argument('--index', type=Path, default=DEFAULT_INDEX)
    sub.choices['plan'].add_argument('--record', help='Project-declared readiness record path')
    sub.choices['plan'].add_argument('--json', action='store_true')
    sub.choices['map'].add_argument('--skills-root', type=Path, default=HERE.parents[2],
                                    help='Installed skills folder; defaults to the one holding this skill')
    c = sub.add_parser('ci', help='Print a method-receipt CI job for the owner to review; writes nothing')
    c.add_argument('--skills', default='<repository path of the installed skills folder>')
    c.add_argument('--policy', default='<path to the reviewed policy JSON>')
    c.add_argument('--receipt', default='<path to the task receipt JSON>')
    p = sub.add_parser('pins')
    p.add_argument('--policy', type=Path, required=True)
    p.add_argument('--validator', type=Path, required=True)
    p.add_argument('--provenance', type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == 'ci':
            sys.stdout.write(ci_template(args.skills, args.policy, args.receipt))
            return 0
        if args.command == 'pins':
            print(json.dumps(pins(args.policy, args.validator, args.provenance), indent=2))
            return 0
        root = args.root.resolve()
        index = json.loads(args.index.read_text())
        if args.command == 'map':
            sys.stdout.write(situation_map(root, index, args.skills_root))
            return 0
        result = plan(root, index, args.record)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print('Readiness: %s (plan %s)' % (result['status'], result['plan_id'][:12]))
            print('Detected: ' + (', '.join(sorted(result['detected_tags'])) or 'none'))
            if result['scan_truncated']:
                print('Note: the scan stopped at %d paths; detected technologies may be incomplete.' % MAX_FILES)
            for item in result['items']:
                if item['state'] in ('needs-owner', 'unavailable'):
                    print('- [%s] %s: %s' % (item['state'], item['path'], item['action']))
            print('Next: ' + result['next_action'])
        return {'ready': 0, 'declined': 0, 'needs-owner': 2, 'approved': 3}.get(result['status'], 1)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({'status': 'unavailable', 'error': str(exc), 'grants_authority': False}))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
