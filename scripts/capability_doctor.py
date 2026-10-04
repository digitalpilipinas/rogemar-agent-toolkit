"""Scoped read-only capability probes. No login, install, model calls or secret output."""
from datetime import datetime, timezone
import json
import os
import re
import platform
import shutil
import subprocess
from pathlib import Path

CAPABILITIES = {
    'git': ('git', ['--version'], None),
    'github': ('gh', ['--version'], ['auth', 'status']),
    'coderabbit': ('coderabbit', ['--version'], ['auth', 'status']),
    'node': ('node', ['--version'], None),
    'xcode': ('xcodebuild', ['-version'], None),
    'android': ('adb', ['version'], None),
    'swift': ('swift', ['--version'], None),
    'droid': ('droid', ['--version'], None),
    'cursor': ('agent', ['--version'], None),
    'codex': ('codex', ['--version'], ['login', 'status']),
}


def probe(command):
    try:
        # Outputs can contain account identifiers; only an exit status leaves this function.
        result = subprocess.run(command, capture_output=True, timeout=15, check=False,
                                env={**os.environ, 'E2E_TELEMETRY_DISABLED': '1', 'DO_NOT_TRACK': '1'})
        if result.returncode != 0:
            return 'failed'
        output = (result.stdout + result.stderr).decode(errors='replace').lower()
        if command[0].endswith('coderabbit') and 'auth' in command:
            if re.search(r'not (?:authenticated|logged in)|signed out', output):
                return 'failed'
            if not re.search(r'authenticated|logged in', output):
                return 'unverified'
        if Path(command[0]).name == 'node' and command[1:] == ['--version']:
            match = re.fullmatch(r'v(\d+)\.(\d+)\.(\d+)\s*', output)
            if not match or tuple(map(int, match.groups())) < (22, 12, 0):
                return 'failed'
        return 'passed'
    except (OSError, subprocess.TimeoutExpired):
        return 'failed'


def inspect_capabilities(names, *, auth_check=False, exercise=False, candidate=None, project_root=None):
    packages = {'e2e': ('e2e', '0.17.0'), 'e2e-web': ('@e2e-dev/web', '0.12.0'), 'e2e-mobile': ('@e2e-dev/mobile', '0.9.2')}
    unknown = set(names) - CAPABILITIES.keys() - packages.keys()
    if unknown:
        raise ValueError('Unknown capability: ' + ', '.join(sorted(unknown)))
    records = {}
    for name in dict.fromkeys(names):
        if name in packages:
            package, expected = packages[name]
            root = Path(project_root or Path.cwd())
            manifest = root / 'node_modules' / package / 'package.json'
            try:
                actual = json.loads(manifest.read_text()).get('version')
            except (OSError, ValueError):
                actual = None
            row = {'installed': actual is not None, 'discoverable': actual == expected,
                   'version': actual, 'expected_version': expected, 'authenticated': 'not-required',
                   'exercised': 'unverified', 'functional_evidence': 'unverified',
                   'discovery_scope': 'project dependency files; browser/device execution is separate'}
            if name == 'e2e' and exercise and actual == expected:
                node = shutil.which('node')
                cli = root / 'node_modules/e2e/dist/cli/bin.js'
                if node and cli.is_file():
                    row['exercised'] = probe([node, str(cli), '--version'])
                    row['exercise_scope'] = 'CLI version probe only'
            records[name] = row
            continue
        executable, version, auth = CAPABILITIES[name]
        found = shutil.which(executable)
        row = {'installed': bool(found), 'discoverable': bool(found),
               'discovery_scope': 'current process PATH, not an agent UI/tool registry',
               'authenticated': 'unverified' if auth or name in ('droid', 'cursor') else 'not-required',
               'exercised': 'unverified', 'functional_evidence': 'unverified'}
        if exercise and found:
            row['exercised'] = probe([found, *version])
            row['exercise_scope'] = 'CLI version probe only'
        if auth_check and auth and found:
            row['authenticated'] = probe([found, *auth])
        records[name] = row
    return {'schema_version': 1, 'observed_at': datetime.now(timezone.utc).isoformat(),
            'candidate': candidate, 'platform': platform.system().lower(), 'capabilities': records,
            'grants_authority': False}
