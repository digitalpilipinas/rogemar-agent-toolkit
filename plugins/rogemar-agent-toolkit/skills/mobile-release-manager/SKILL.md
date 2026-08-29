---
name: mobile-release-manager
description: Use for Expo, React Native, iOS, Android, or other mobile release readiness work involving build profiles, app config, env checks, icons, splash screens, permissions, App Store and Play Store checklists, QA plans, release notes, rollback notes, and production deployment preparation.
---

# Mobile Release Manager

## Workflow

1. Inspect branch state, changed files, app config, package scripts, env requirements, and recent commits.
2. Verify release scope: user-facing changes, backend/schema changes, permissions, analytics, privacy, offline behavior, and platform-specific impact.
3. Check build readiness: Expo/EAS or native profiles, bundle IDs/package names, icons, splash, deep links, permissions copy, versioning, and platform config.
4. Run repo-native validation where applicable: lint, typecheck, targeted tests, build/prebuild checks, and UI smoke tests.
5. Produce release notes, manual QA, rollback plan, and store-review risk notes.

## QA Coverage

- Auth/session, onboarding, core creation/update flows, offline behavior, sharing/export, profile/settings, subscriptions, and destructive actions.
- iOS safe areas, Android back behavior, small devices, dark/light themes, poor network, airplane mode, cold launch, and upgrade-from-previous-version.
- Env files must stay local and ignored.

## Output

Use sections: Scope, Build Readiness, Validation, Manual QA, Store Notes, Rollback.
