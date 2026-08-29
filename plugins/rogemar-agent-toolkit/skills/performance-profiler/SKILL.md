---
name: performance-profiler
description: Use for performance investigations, profiling, or optimization involving React renders, Core Web Vitals, interaction latency, bundle size, images, virtualization, memory leaks, React Native frame drops, startup time, database/API latency, and measured evidence.
---

# Performance Profiler

Use this skill when performance matters to the task or the user reports slowness,
jank, high memory use, poor startup, slow queries, or bundle regressions.

## Workflow

1. Define the user-visible performance target: startup, navigation, input
   latency, render jank, scrolling, sync, export, query, memory, or bundle size.
2. Reproduce and measure before optimizing. Prefer repo-native profiling,
   browser performance tools, React Profiler, bundle analyzers, logs, query
   plans, emulator/device traces, or controlled timing scripts.
3. Find the bottleneck layer: render frequency, data fetching, caching, image
   loading, layout, animations, list virtualization, storage, network, database,
   bundle, native bridge, or startup work.
4. Make the smallest change that addresses the measured cause. Preserve product
   behavior and compatibility.
5. Re-measure the same scenario and report before/after evidence. If exact
   measurement is unavailable, say so and provide the strongest available proxy.

## Guardrails

- Do not optimize from intuition alone when measurement is practical.
- Do not trade correctness, privacy, or accessibility for speed.
- Do not add caching without invalidation, ownership, and stale-state behavior.
- Do not hide a slow server-authoritative path by trusting client data.

## Output

Report the performance symptom, measurement method, likely bottleneck, change
made or proposed, before/after evidence, and any remaining risk.

## Optional collaboration guidance

The orchestrator may assign a read-only measurement analyst for a clearly
bounded baseline, trace, bottleneck, or comparison when the measurement stream
is independent and repeatable. Provide the target metric, scenario, environment
boundary, owned surface, non-goals, parent model and reasoning ceilings, and
required before/after evidence. Return measurements and uncertainty, not a
readiness claim or unapproved optimization. The main agent reconciles results
and owns the final performance decision.
