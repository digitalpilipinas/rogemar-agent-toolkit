# Optional Unlazy adapter

Use [Unlazy](https://github.com/Leonxlnx/unlazy) as completion support for requested
or omission-prone substantial work. First-Time-Right Delivery owns acceptance
evidence, Integrated Workflow owns approved programme execution, and
`workflow-orchestrator` owns any delegation. Unlazy remains an external skill;
discover its installed directory rather than assuming a harness-specific path.

## One acceptance record

1. Reuse the approved outcome, scope and requirement IDs. Add observable gates
   where evidence would otherwise be lost; do not restart planning or create a
   second board. If the existing acceptance file supports Unlazy's format, use
   it directly. Otherwise make one `GATES.md` the gate evidence record and
   reference it from the plan; avoid maintaining duplicate checkboxes elsewhere.
2. Attach repository checks to applicable outcomes. Inspect each `CHECK` and the
   scripts it calls before execution: a gate file contains shell commands, and
   no skill grants new filesystem, network, deployment or provider authority.
   Use the intended worktree, inputs and supported runtime.
3. Record command results and decisive evidence against the current candidate.
   Rerun affected checks after relevant changes; an old checked box is not fresh
   verification. Keep manual or external evidence distinct from command results.
4. Before reporting completion, compare the gates to the original request and
   remeasure any reported counts. Report met, unmet and explicitly deferred
   outcomes separately. Reuse the active review and its finding record.

For substantial logs and handoffs, use the orchestrator's
[context guidance](../../workflow-orchestrator/references/context-efficiency.md).
Keep original diagnostics recoverable and preserve every unmet gate. An inherited
report or checker status from an earlier candidate is not fresh evidence after
a change. Record current commands and results when rerunning the checker against
the current candidate; those results may supply fresh evidence.

## Select commands by the installed version

Read the installed `SKILL.md` and checker before choosing flags. Node is needed
only when using the optional checker. The checker is not an MCP or a sandbox.

- **Installed 2.0:** `--status` inspects the named ledger without executing checks.
  Normal mode executes unchecked runnable gates. It does not recheck completed
  gates; reset an affected gate to unchecked with `EVIDENCE: pending` before
  rerunning it. Its `EXPECT` match can accept a nonzero exit, so prefer an
  exit-code check without `EXPECT`, or a success marker emitted only after all
  assertions pass. Inspect the underlying result before accepting evidence.
- **2.1 source:** the reviewed upstream documentation adds exact command approval
  and `--reverify`, and requires both a zero exit and matching expectation. Use
  those controls only when the installed checker actually supports them, within
  existing task authority. Do not pass newer flags to 2.0 and assume they work.

For example, after verifying the installed directory and reviewing the ledger:

```text
node <installed-unlazy-directory>/scripts/gate-check.mjs --status <acceptance-file>
```

On 2.0, normal execution is the same command without `--status`. On a compatible
2.1 installation, follow its approval and re-verification contract. Missing Node
or an unavailable checker is optional-tool status; run authorized checks directly
and preserve the evidence record rather than installing tools implicitly.

## Keep delivery proportionate

Do not import fixed tree depths, minimum work durations, automatic fresh workers,
or repeated improvement passes into routine delivery. Decompose only at real
dependencies and let the existing orchestrator decide whether delegation helps.
An adequate final check is not a reason to invent another task or review cycle.

An `ABANDON` entry is an incomplete outcome or handoff, never a passed acceptance
gate or permission to waive a required check. Version 2.0 can return zero with
abandoned gates; inspect the ledger, not only the checker exit. Required gates
remain unmet until satisfied or explicitly waived by the owner. Continue useful
authorized work and report the remaining boundary honestly.

Do not install stop hooks or change persistent harness settings automatically.
Unlazy's optional Claude Code hook is specific to that harness and needs explicit
authority. Other harnesses keep their own continuation, model and permission
controls. No hook was installed by this toolkit integration.

## Provenance

Method: Leonxlnx, MIT. This is a toolkit integration contract, not a vendored copy
of the upstream skill or scripts. The local 2.0 descriptor and checker informed
the compatibility notes. Upstream [2.1 source documentation](https://github.com/Leonxlnx/unlazy/tree/16671491f6679ad9378f52604d3bc2415b4120c7)
was checked on 2026-09-07; it describes source changes rather than an asserted
tagged release. Reinspect the installed version before execution.
