# Attack the Premise

When two or more fixes assume the same thing and fail the same check, examine the shared assumption before trying another variation.

1. Write the premise, failed attempts, observed failure and a plausible alternative explanation.
2. Choose the smallest rerunnable check whose possible outcomes distinguish those explanations. State the expected result for each before running it.
3. For an imbalance among actors, measure per actor when that distinction matters. Include relevant workload, timing, sample count and uncertainty. For other bugs, use the measurement appropriate to the mechanism.
4. Compare observation with prediction. Concentration can motivate tracing the assignment of work; it does not establish causation. An even distribution does not conclusively eliminate a cause: a shared fault, short sample or hidden dimension may mask it.
5. Keep the evidence, revise the hypothesis and make the smallest authorized change that the result supports. Verify the original failure again. An unavailable or inconclusive experiment remains a gap.

Example: two load-balancing fixes leave timeouts unchanged. Measure queue wait and service time per worker under the same load before changing the scheduler again. Equal timeout counts alone cannot rule out scheduling if every worker shares the same queue lock. A relevant next check compares lock wait with service time; it does not blindly rotate worker roles.
