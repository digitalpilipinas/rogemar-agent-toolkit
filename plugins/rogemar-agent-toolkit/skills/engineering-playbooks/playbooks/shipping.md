# Shipping

Land only a contiguous verified run from the bottom of an explicitly authorized stack. GitHub mergeability is one input; it does not grant authority or prove programme acceptance.

1. Confirm repository, PR order, actual publication/merge authority, operator gates, and currently exposed authenticated forge tools. Use `integrated-workflow` where applicable. Resolve each link's head and base from live evidence.
2. Verify each PR's acceptance and review dispositions independently at its current integration context. Request bounded independent reviewers through the orchestrator where useful; do not require cloud agents or a fixed panel. Keep review evidence local unless posting is authorized.
3. Walk from the lowest unmerged link and stop at the first missing, stale, failed or unresolved verdict. An independently verified link above a gap is not landable through that gap.
4. Recheck head, base, diff, required checks, review decisions and every relevant comment/annotation surface immediately before landing. Patch identity does not validate a changed base. A changed head invalidates checks tied to the old SHA.
5. Prepare and merge only the bottom eligible PR. Respect the repository merge strategy. Auto-merge is a distinct action and must be explicitly authorized; verify it was armed. Never infer queued descendants from a single auto-merge flag.
6. Watch that PR with the authorized exposed tool. `READY` is a snapshot, not a merge. Confirm MERGED and its merge commit before advancing. A pending or unknown state is not ready; diagnose blocked requirements without mutating the rest of the queue.
7. Recompute topology and current trunk after every merge. Inspect any automatic retargeting, revalidate the next link and repeat only within the authorized verified run.
8. Report landed PRs and SHAs, anything armed and how verified, the first remaining gap, and deployment status separately. Do not extend the approved run by inference.

After merge preparation, require CI for the actual current head. A green run for a previous SHA does not satisfy this gate. A changed base, source, dependency, configuration or generated runtime input invalidates affected evidence; rerun the affected checks. Do not preserve runtime proof merely because patch IDs match or rebuilt artifacts differ only in presumed build noise. Record required checks that cannot run as blocked or explicitly deferred under the acceptance contract.
