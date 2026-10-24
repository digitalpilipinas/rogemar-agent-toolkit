"""Finite transition model for watcher-owned sleeps, not network cancellation.

Correspondence and exclusions: docs/watch-deadline-model.md.
Production replay: codex-forge/scripts/watch-pr/deadline.test.ts.
"""
import unittest


def sleep_transition(timeout, elapsed, query_duration, requested, *, mutant=False):
    after_query = elapsed + query_duration
    if timeout and after_query >= timeout:
        return after_query, 0
    sleep = requested if mutant or not timeout else min(requested, timeout - after_query)
    return after_query + sleep, sleep


def counterexamples(*, mutant=False):
    failures = []
    # Exhaust this finite domain, including queries that consume the deadline.
    for timeout in range(1, 8):
        for elapsed in range(timeout + 3):
            for query_duration in range(4):
                for requested in range(1, 10):
                    end, sleep = sleep_transition(timeout, elapsed, query_duration, requested, mutant=mutant)
                    remaining = max(0, timeout - elapsed - query_duration)
                    if not 0 <= sleep <= remaining:
                        failures.append((timeout, elapsed, query_duration, requested, end))
    return failures


class WatchDeadlineModelTests(unittest.TestCase):
    def test_bounded_sleep_invariant_over_finite_domain(self):
        self.assertEqual(counterexamples(), [])

    def test_model_detects_original_unbounded_sleep_mutation(self):
        failures = counterexamples(mutant=True)
        self.assertTrue(failures)
        self.assertIn((5, 0, 0, 9, 9), failures)
        # Same five-second/sixty-second counterexample replayed by the TS runner.
        self.assertEqual(sleep_transition(5, 0, 0, 60, mutant=True), (60, 60))
        self.assertEqual(sleep_transition(5, 0, 0, 60), (5, 5))

    def test_unbounded_timeout_is_not_a_liveness_claim(self):
        self.assertEqual(sleep_transition(0, 120, 3, 60), (183, 60))


if __name__ == '__main__':
    unittest.main()
