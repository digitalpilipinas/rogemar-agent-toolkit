import { describe, expect, it } from "bun:test";
import { fakeReader, pendingCheck } from "./fakes.test-helper.ts";
import { WatcherQueryError } from "./github.ts";
import { runQueued, runSimple } from "./policy.ts";
import { parsePrNumber, type ProgressVerdict } from "./types.ts";

const context = { owner: "owner", repo: "repo", number: parsePrNumber(1) };

describe("polling deadline", () => {
  for (const mode of ["single", "stack", "queued-stack", "retry"] as const) {
    for (const timeout of [1, 5, 17]) {
      for (const interval of [2, 10, 60]) {
        it(`${mode}: timeout ${timeout}, interval ${interval}`, async () => {
          let now = 0;
          const sleeps: number[] = [];
          const emitted: ProgressVerdict[] = [];
          const base = fakeReader({ fastPath: { kind: "checks", checks: [pendingCheck()] } });
          const reader = mode !== "retry" ? base : {
            ...base,
            async pullRequest() {
              throw new WatcherQueryError({ kind: "checks-unavailable", retryable: true, detail: "temporary failure" });
            },
          };
          const dependencies = {
            reader,
            clock: {
              now: () => now,
              observedAt: () => "2026-10-24T00:00:00Z",
              async sleep(seconds: number) {
                expect(seconds).toBeLessThanOrEqual(timeout - now);
                sleeps.push(seconds); now += seconds;
              },
            },
            emit: (event: ProgressVerdict) => { emitted.push(event); },
          };
          const options = { interval, timeout, sweepInterval: 300, maxQueryErrors: 100, allowDraft: false };
          const verdict = mode === "queued-stack"
            ? await runQueued({ dependencies, contexts: [context], options })
            : await runSimple({ dependencies, contexts: [context], options, mode: mode === "retry" ? "single" : mode, statusOnly: false });
          expect(verdict.kind).toBe("TIMEOUT");
          expect(now).toBe(timeout);
          expect(sleeps.every(value => value > 0)).toBe(true);
          if (mode === "retry") {
            const retries = emitted.filter(event => event.kind === "RETRY");
            expect(retries.slice(0, sleeps.length).map(event => event.retryInSeconds)).toEqual(sleeps);
          }
        });
      }
    }
  }

  it("subtracts query time without claiming to cancel an in-flight query", async () => {
    let now = 0;
    let reads = 0;
    const sleeps: number[] = [];
    const base = fakeReader({ fastPath: { kind: "checks", checks: [pendingCheck()] } });
    const result = await runSimple({
      contexts: [context], mode: "single", statusOnly: false,
      options: { interval: 60, timeout: 5, sweepInterval: 300, maxQueryErrors: 5, allowDraft: false },
      dependencies: {
        reader: { ...base, async pullRequest(pr) {
          if (++reads === 1) now += 3;
          return base.pullRequest(pr);
        } },
        clock: { now: () => now, observedAt: () => "2026-10-24", async sleep(seconds) { sleeps.push(seconds); now += seconds; } },
        emit() {},
      },
    });
    expect(result.kind).toBe("TIMEOUT");
    expect(sleeps).toEqual([2]);
    expect(now).toBe(5);
  });

  it("keeps timeout zero unbounded", async () => {
    let now = 0;
    const sleeps: number[] = [];
    const base = fakeReader({ fastPath: { kind: "checks", checks: [pendingCheck()] } });
    const result = await runSimple({
      contexts: [context], mode: "single", statusOnly: false,
      options: { interval: 60, timeout: 0, sweepInterval: 300, maxQueryErrors: 5, allowDraft: false },
      dependencies: {
        reader: { ...base, async pullRequest(pr) { return { ...await base.pullRequest(pr), ...(now >= 120 ? { state: "MERGED" as const, mergedAt: "2026-10-24" } : {}) }; } },
        clock: { now: () => now, observedAt: () => "2026-10-24", async sleep(seconds) { sleeps.push(seconds); now += seconds; } },
        emit() {},
      },
    });
    expect(result.kind).toBe("READY");
    expect(sleeps).toEqual([60, 60]);
  });
});
