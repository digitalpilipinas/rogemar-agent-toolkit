---
name: "gh-fix-ci"
description: "CLI fallback for debugging GitHub Actions PR checks when the GitHub plugin is unavailable, unauthenticated, or the user explicitly requests gh CLI. Prefer the GitHub-plugin gh-fix-ci skill when its connected PR context is available."
---


# Gh Pr Checks Plan Fix

## Overview

Use gh to locate failing PR checks, fetch GitHub Actions logs for actionable failures, summarize the failure snippet, then fix them within recorded programme authority or after explicit approval. Prefer the GitHub-plugin `gh-fix-ci` skill when its connected PR context is available; this skill is the connector-independent fallback.
- Reuse the accepted plan and remediation authority. Use create-plan only when meaningful new work needs planning; do not reopen approval for an already authorized fix.

Prereq: run `gh auth status` normally before triaging checks. If blocked, use only a supported permission flow; do not invent elevation flags or bypass a denial. If authentication is absent, ask the user to authorize or complete `gh auth login` (repo and workflow scopes are typically required).

## Inputs

- `repo`: path inside the repo (default `.`)
- `pr`: PR number or URL (optional; defaults to current branch PR)
- `gh` authentication for the repo host

## Quick start

- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "<number-or-url>"`
- Add `--json` if you want machine-friendly output for summarization.

## Workflow

1. Verify gh authentication.
   - Run `gh auth status` in the repo with normal permissions; retry only on a network or sandbox denial using narrowly scoped elevation.
   - If unauthenticated, ask the user to run `gh auth login` (ensuring repo + workflow scopes) before proceeding.
2. Resolve the PR.
   - Prefer the current branch PR: `gh pr view --json number,url`.
   - If the user provides a PR number or URL, use that directly.
3. Inspect failing checks (GitHub Actions only).
   - Preferred: run the bundled script (handles gh field drift and job-log fallbacks):
     - `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "<number-or-url>"`
     - Add `--json` for machine-friendly output.
   - Manual fallback:
     - `gh pr checks <pr> --json name,state,bucket,link,startedAt,completedAt,workflow`
       - If a field is rejected, rerun with the available fields reported by `gh`.
     - For each failing check, extract the run id from `detailsUrl` and run:
       - `gh run view <run_id> --json name,workflowName,conclusion,status,url,event,headBranch,headSha`
       - `gh run view <run_id> --log`
     - If the run log says it is still in progress, fetch job logs directly:
       - `gh api "/repos/<owner>/<repo>/actions/jobs/<job_id>/logs" > "<path>"`
4. Scope non-GitHub Actions checks.
   - If `detailsUrl` is not a GitHub Actions run, label it as external and only report the URL.
   - Do not attempt Buildkite or other providers; keep the workflow lean.
5. Summarize failures for the user.
   - Provide the failing check name, run URL (if any), and a concise log snippet.
   - Call out missing logs explicitly.
6. Resolve the execution contract.
   - If an approved plan or active programme already covers remediation of the
     exact failing check, use that bounded task and do not create a duplicate
     plan or approval loop.
   - Otherwise use `create-plan` for a concise fix plan and request approval.
7. Implement within authority.
   - Apply only the approved remediation scope, summarize diffs and tests, and
     stop before any commit, push, PR, or merge boundary that is not already
     authorized.
8. Recheck status.
   - After changes, suggest re-running the relevant tests and `gh pr checks` to confirm.

For later calls, preserve the actual host permission boundary. A denied operation remains blocked unless the supported authorization flow permits it.

## Bundled Resources

### scripts/inspect_pr_checks.py

Fetch failing PR checks, pull GitHub Actions logs, and extract a failure snippet. Exits non-zero when failures remain so it can be used in automation.

Usage examples:
- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "123"`
- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "https://github.com/org/repo/pull/123" --json`
- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --max-lines 200 --context 40`
