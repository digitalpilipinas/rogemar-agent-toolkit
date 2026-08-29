---
name: privacy-safety-review
description: Use for product privacy, safety, and honesty reviews involving profiles, location, health or wellness signals, social features, leaderboards, badges, community data, media sharing, permissions, sensitive storage, generated insights, and surfaces where missing backend data must not be fabricated.
---

# Privacy Safety Review

## Workflow

1. Identify personal, location, health/wellness, social, media, financial, and gamification data on the surface.
2. Trace where the data comes from and whether backend support actually exists.
3. Check consent, visibility, sharing defaults, deletion/reconciliation, user switching, and cache isolation.
4. Replace fabricated social, wellness, leaderboard, badge, analytics, or community data with honest unavailable, empty, pending, or queued states unless the user explicitly requests demo data.
5. Review permission prompts and copy for clarity, necessity, and least surprise.
6. For social, discovery, leaderboard, or sharing features, define a disclosure
   matrix across consent, profile discoverability, relationship, record
   visibility, and metric eligibility. Verify every forbidden combination is
   rejected server-side and cannot influence aggregates.
7. Review adversarial cases: private/opted-out/legacy/malformed data,
   unauthenticated callers, non-owners, and unavailable backend support.

## Standards

- Prefer user trust over vanity metrics or artificial progress.
- Treat location, images, health/wellness, social graph, and private activity as sensitive.
- Keep safety copy practical and calm.
- Do not make claims the product cannot substantiate.
- Prefer explicit default-off consent, field allowlists, data minimisation, and
  truthful unavailable states over client-only privacy wording.

## Output

List privacy risks, user trust risks, backend truth gaps, and recommended product copy/state changes.

## Optional delegation guidance

For broad surfaces, the orchestrator may assign a read-only privacy reviewer
to inspect one bounded data flow, consent path, disclosure combination, or
truthfulness gap. Require evidence for data origin, visibility, consent,
deletion, cache isolation, and unavailable states. Pass the parent model and
reasoning ceilings; never allow the reviewer to exceed them. The main agent
reconciles findings and owns product, authorization, and remediation decisions.
