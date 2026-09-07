### Runtime forensics

**You own the diagnosis. Instrument the live process, don't theorize from source.** For "why is X leaking / spinning / slow at runtime", heap snapshots, idle-but-busy processes, intermittent glitches. The deliverable is a cited diagnosis, not a fix.

1. Capture the live signal on the matching surface via the control skill: a CPU profile for a spinning process, a heap snapshot for a leak, a CDP trace for a visual glitch. A real artifact, not a guess.
2. Reduce the artifact to the smoking gun: the function on the hot path, the retainer chain from the leaked object to a GC root, the loop firing without input. When authorized and useful, request bounded parsing of large artifacts through the orchestrator (the **guard-the-context-window** principle skill), keep the reduced finding in the main thread.
3. Prove the mechanism before believing it. Use the matching supported profiler or bounded instrumentation in an authorized development process to confirm the hypothesis. Do not alter a production process or assume CDP exists. A plausible-but-unconfirmed cause can be wrong while the real one sits one layer over.
4. Map the finding back to source: file, symbol, the line that allocates or schedules.

**Reply:** the signal captured, the reduced finding, how you proved the mechanism, the source location, artifact paths. No fix unless asked; hand back to Bug fix or Perf once the cause is known.
