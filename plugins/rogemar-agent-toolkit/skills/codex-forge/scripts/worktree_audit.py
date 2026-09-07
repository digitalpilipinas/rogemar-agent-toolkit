#!/usr/bin/env python3
"""Inspect worktrees without fetching, modifying refs, mining history, or deleting files."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import subprocess


def git(repo, *args, check=True):
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, check=False)
    if check and result.returncode:
        raise ValueError("Git inspection failed: " + result.stderr.decode(errors="replace").strip())
    return result


def worktrees(repo):
    records, item = [], {}
    for field in git(repo, "worktree", "list", "--porcelain", "-z").stdout.split(b"\0"):
        if not field:
            if item:
                records.append(item)
                item = {}
            continue
        key, _, value = field.decode(errors="surrogateescape").partition(" ")
        item[key] = value
    if item:
        records.append(item)
    return records


def target_ref(repo, explicit=None):
    if explicit:
        candidate = explicit
    else:
        remotes = git(repo, "remote").stdout.decode().splitlines()
        if len(remotes) != 1:
            return None
        ref = git(repo, "symbolic-ref", "--quiet", "refs/remotes/" + remotes[0] + "/HEAD", check=False)
        if ref.returncode:
            return None
        candidate = ref.stdout.decode().strip()
    found = git(repo, "rev-parse", "--verify", "--end-of-options", candidate + "^{commit}", check=False)
    return found.stdout.decode().strip() if found.returncode == 0 else None


def audit(repo, target=None):
    records = worktrees(repo)
    base = target_ref(repo, target)
    output = []
    for index, entry in enumerate(records):
        path = entry["worktree"]
        reasons = []
        if index == 0:
            reasons.append("primary-worktree")
        if "locked" in entry or "prunable" in entry:
            reasons.append("locked-or-prunable-requires-inspection")
        status = git(path, "status", "--porcelain=v1", "-z", "--untracked-files=all", "--ignored=matching", check=False)
        if status.returncode:
            reasons.append("status-unavailable")
        elif status.stdout:
            reasons.append("tracked-untracked-or-ignored-work-present")
        head = entry.get("HEAD")
        merged = None
        if base and head:
            probe = git(repo, "merge-base", "--is-ancestor", head, base, check=False)
            merged = True if probe.returncode == 0 else False if probe.returncode == 1 else None
        if merged is not True:
            reasons.append("target-ancestry-unverified" if merged is None else "head-not-merged-into-target")
        output.append({"path": path, "head": head, "branch": entry.get("branch"),
                       "merged_by_local_ancestry": merged, "classification": "hold" if reasons else "review-merged",
                       "reasons": reasons, "deletion_authorized": False})
    return {"target_commit": base, "target_evidence": "local-refs-only" if base else "unverified",
            "pr_evidence": "not-queried; a closed PR is not merge proof",
            "history_evidence": "not-queried", "worktrees": output}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", nargs="?", default=".")
    parser.add_argument("--repo", dest="repo_option")
    parser.add_argument("--target", help="Explicit branch/ref; otherwise use an unambiguous remote HEAD")
    args = parser.parse_args()
    try:
        print(json.dumps(audit(Path(args.repo_option or args.repo).resolve(), args.target), indent=2))
        return 0
    except (OSError, ValueError) as error:
        parser.exit(2, str(error) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
