# Mobile motion and gesture verification

Use for changed mobile gestures or transitions. Keep native defaults and existing
motion tokens when they already serve the task. Frequent interactions should
remain efficient; adding no animation is a valid outcome.

- Identify the purpose and affected states. Follow direct manipulation with the
  user's input; preserve release velocity where appropriate and settle from the
  current value. Check bounds, cancellation, re-grabbing and interruption.
- Complete dismissal/navigation at the intended lifecycle point. Do not unmount
  an animated surface before its exit finishes unless that is deliberate behavior.
  Rapid repeated actions must not stack transitions or duplicate submissions.
- Keep keyboard, sheet and scroll coordination on supported platform/library
  mechanisms. Confirm actual installed APIs rather than copying fixed Reanimated
  recipes, timings or thread helpers. Native behavior does not require recreating
  system animations in application code.
- Honor reduced motion with a useful simplified or non-animated result; preserve
  context and input feedback. Provide non-gesture alternatives where necessary.
- Exercise affected transitions at normal speed. Capture and inspect a recording
  when interruption, timing or transient visual defects require it; inspect
  relevant frames rather than recording every unchanged flow by default.
- Measure suspected performance problems on the relevant runtime/build/device,
  compare the same interaction before and after, and state the measurement method.
  Recordings alone do not prove frame rate. Physical-device or release-build
  requirements follow the existing acceptance contract, not a universal new gate.

Use the selected authorized device tooling, including Argent when available and
applicable. Do not bypass the harness's discovery and interaction rules with raw
simulator commands. When the required runtime is absent, keep that check blocked
or explicitly deferred by the owner while independent source work continues.
Stop when scoped acceptance is met; optional polish does not reopen delivery.

Adapted by Rogemar Agent Toolkit from [Appllama appllama-app-design-skill](https://github.com/Appllama/appllama-skills/tree/dd5caaec3d5d50ad7fc0324da238119c6b7c3707/skills/appllama-app-design-skill), reviewed pin `dd5caaec3d5d50ad7fc0324da238119c6b7c3707`.
Selected methods only; no endorsement or hosted-service integration.
See [MIT notice](../LICENSE.appllama.txt); existing skill licenses remain intact.
