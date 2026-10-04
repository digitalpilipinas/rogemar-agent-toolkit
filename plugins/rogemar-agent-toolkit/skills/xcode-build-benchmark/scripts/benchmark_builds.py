#!/usr/bin/env python3
"""Measure builds in run-owned DerivedData and preserve every executed phase log."""
import argparse
import json
import os
import re
import shutil
import statistics
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Optional


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    entry = parser.add_mutually_exclusive_group(required=True)
    entry.add_argument("--workspace")
    entry.add_argument("--project")
    parser.add_argument("--scheme", required=True)
    parser.add_argument("--configuration", default="Debug")
    parser.add_argument("--destination")
    parser.add_argument("--derived-data-path", help="Existing parent for a new run-owned directory; never cleaned itself")
    parser.add_argument("--output-dir", default=".build-benchmark")
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--timeout", type=float, default=900)
    parser.add_argument("--skip-warmup", action="store_true")
    parser.add_argument("--touch-file")
    parser.add_argument("--no-cached-clean", action="store_true")
    parser.add_argument("--extra-arg", action="append", default=[])
    args = parser.parse_args()
    if args.repeats < 1 or args.timeout <= 0:
        parser.error("repeats and timeout must be positive")
    # Only scoped non-path settings can be forwarded; output overrides defeat isolation.
    allowed = {"CODE_SIGNING_ALLOWED", "COMPILATION_CACHE_ENABLE_CACHING", "SWIFT_OPTIMIZATION_LEVEL", "SWIFT_COMPILATION_MODE", "DEBUG_INFORMATION_FORMAT", "ONLY_ACTIVE_ARCH"}
    if any(value.split("=", 1)[0] not in allowed or "=" not in value for value in args.extra_arg):
        parser.error("extra arguments must be supported non-path build settings")
    if args.touch_file and not Path(args.touch_file).is_file():
        parser.error("touch-file must be an existing source file")
    return args


def command_base(args, derived):
    command = ["xcodebuild", "-workspace" if args.workspace else "-project", args.workspace or args.project,
               "-scheme", args.scheme, "-configuration", args.configuration, "-derivedDataPath", str(derived)]
    if args.destination:
        command += ["-destination", args.destination]
    return command + args.extra_arg


def run_logged(command, path, timeout):
    started = time.perf_counter()
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
        code, output = result.returncode, result.stdout + result.stderr
    except subprocess.TimeoutExpired as exc:
        def decode(value):
            return value.decode(errors="replace") if isinstance(value, bytes) else value or ""
        code, output = 124, decode(exc.stdout) + decode(exc.stderr) + "\nBUILD TIMEOUT\n"
    except OSError as exc:
        code, output = 127, str(exc)
    path.write_text(output)
    return {"success": code == 0, "exit_code": code, "duration_seconds": time.perf_counter() - started,
            "command": command, "raw_log_path": str(path), "timing_summary_categories": parse_timing_summary(output)}


def stats_for(runs):
    if not runs or any(not r["success"] for r in runs):
        return {"count": len(runs), "median_seconds": None}
    values = [r["duration_seconds"] for r in runs]
    return {"count": len(values), "min_seconds": min(values), "max_seconds": max(values),
            "median_seconds": statistics.median(values), "average_seconds": statistics.fmean(values)}


_TASK_COUNT_RE = re.compile(r"^(.+?)\s*\((\d+)\s+tasks?\)$")


def _extract_task_count(name: str) -> tuple[str, Optional[int]]:
    """Split 'Category (N tasks)' into ('Category', N)."""
    match = _TASK_COUNT_RE.match(name)
    if match:
        return match.group(1).strip(), int(match.group(2))
    return name, None


def parse_timing_summary(output: str) -> List[Dict]:
    categories: Dict[str, float] = {}
    task_counts: Dict[str, Optional[int]] = {}
    for raw_line in output.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        for suffix in (" seconds", " second", " sec"):
            if not line.endswith(suffix):
                continue
            trimmed = line[: -len(suffix)]
            if "|" in trimmed:
                name_part, _, seconds_text = trimmed.rpartition("|")
            else:
                name_part, _, seconds_text = trimmed.rpartition(" ")
            try:
                seconds = float(seconds_text.strip())
            except ValueError:
                continue
            cleaned_name = name_part.replace("  ", " ").strip(" -:")
            if len(cleaned_name) < 3:
                continue
            base_name, count = _extract_task_count(cleaned_name)
            categories[base_name] = categories.get(base_name, 0.0) + seconds
            if count is not None:
                task_counts[base_name] = (task_counts.get(base_name) or 0) + count
            break
    result: List[Dict] = []
    for name, seconds in sorted(categories.items(), key=lambda item: item[1], reverse=True):
        entry: Dict = {"name": name, "seconds": round(seconds, 3)}
        if name in task_counts:
            entry["task_count"] = task_counts[name]
        result.append(entry)
    return result


def main():
    args = parse_args()
    output = Path(args.output_dir).resolve()
    output.mkdir(parents=True, exist_ok=True)
    evidence = Path(tempfile.mkdtemp(prefix="run-", dir=output))
    artifact = {"schema_version": "2.0.0", "status": "failed", "repeats": args.repeats,
                "build": {"path": args.workspace or args.project, "scheme": args.scheme,
                          "configuration": args.configuration, "destination": args.destination},
                "runs": {"clean": [], "incremental": []}, "phases": [],
                "incremental_kind": "edit" if args.touch_file else "zero-change"}
    touch = Path(args.touch_file) if args.touch_file else None
    touch_stat = touch.stat() if touch else None
    try:
        with tempfile.TemporaryDirectory(prefix="toolkit-xcode-", dir=args.derived_data_path) as temporary:
            derived = Path(temporary) / "DerivedData"
            base = command_base(args, derived)
            artifact["build"]["command"] = base
            def phase(label, action):
                record = run_logged(base + action, evidence / (label + ".log"), args.timeout)
                record["id"] = label
                artifact["phases"].append(record)
                if not record["success"]:
                    raise RuntimeError(label + " failed; see " + record["raw_log_path"])
                return record
            if not args.skip_warmup:
                phase("warmup", ["build"])
            settings = phase("settings", ["-showBuildSettings"])
            cached = (not args.no_cached_clean and re.search(r"COMPILATION_CACHE_ENABLE_CACHING\s*=\s*YES", Path(settings["raw_log_path"]).read_text()))
            for index in range(args.repeats):
                phase(f"clean-prep-{index}", ["clean"])
                artifact["runs"]["clean"].append(phase(f"clean-{index}", ["build", "-showBuildTimingSummary"]))
                if touch:
                    touch.touch()
                artifact["runs"]["incremental"].append(phase(f"incremental-{index}", ["build", "-showBuildTimingSummary"]))
            if cached:
                artifact["runs"]["cached_clean"] = []
                phase("cache-warmup", ["build"])
                for index in range(args.repeats):
                    # Only this run-created child can be removed, never the supplied parent.
                    if derived.exists():
                        shutil.rmtree(derived)
                    artifact["runs"]["cached_clean"].append(phase(f"cached-clean-{index}", ["build", "-showBuildTimingSummary"]))
            artifact["status"] = "complete"
    except (OSError, RuntimeError) as exc:
        artifact["error"] = str(exc)
    finally:
        if touch and touch_stat:
            os.utime(touch, ns=(touch_stat.st_atime_ns, touch_stat.st_mtime_ns))
        artifact["summary"] = {kind: stats_for(runs) for kind, runs in artifact["runs"].items()}
        result = evidence / "benchmark.json"
        result.write_text(json.dumps(artifact, indent=2) + "\n")
        print(f"{artifact['status']}: {result}")
    return 0 if artifact["status"] == "complete" else 1


if __name__ == "__main__":
    raise SystemExit(main())
