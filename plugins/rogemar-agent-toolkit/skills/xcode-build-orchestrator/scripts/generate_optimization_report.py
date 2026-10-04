#!/usr/bin/env python3
"""Summarize completed measurements; never infer a speedup from settings alone."""
import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--benchmark', required=True)
    parser.add_argument('--recommendations')
    parser.add_argument('--diagnostics')
    parser.add_argument('--project-path', help='Recorded context only; does not resolve build settings')
    parser.add_argument('--output')
    args = parser.parse_args()
    data = json.loads(Path(args.benchmark).read_text())
    runs = data.get('runs', {})
    complete = (data.get('status') == 'complete' and data.get('repeats', 0) > 0
                and all(kind in runs for kind in ('clean', 'incremental'))
                and all(len(group) == data['repeats'] and all(r.get('success') for r in group) for group in runs.values())
                and all(p.get('success') for p in data.get('phases', [])))
    lines = ['# Build measurements', '', f"Evidence: {'complete' if complete else 'FAILED OR INCOMPLETE'}", '',
             'Compare only matching project, scheme, configuration, destination, machine and cache conditions.']
    if complete:
        for kind, group in runs.items():
            import statistics
            values = [r['duration_seconds'] for r in group]
            lines += ['', f'{kind}: median {statistics.median(values):.3f}s ({len(values)} runs).']
    else:
        lines += ['', 'No accepted baseline or optimization verdict can be produced from this artifact.']
    for field in ('recommendations', 'diagnostics'):
        path = getattr(args, field)
        if path:
            extra = json.loads(Path(path).read_text())
            lines += ['', f'{field}: {path}; inspect the original evidence before accepting any finding.']
            if field == 'diagnostics' and not extra.get('build_success'):
                lines += ['Diagnostic build failed; absence of warnings is not a pass.']
    lines += ['', 'Settings scans are hypotheses, not measured gains. Check resolved xcodebuild settings.',
              'Retain changes only with measured benefit or a separately approved non-performance reason.',
              'Reuse existing task authority; this report neither grants nor requires a second approval.']
    text = '\n'.join(lines) + '\n'
    if args.output:
        Path(args.output).write_text(text)
    else:
        print(text)
    return 0 if complete else 1


if __name__ == '__main__':
    raise SystemExit(main())
