# Mobile navigation and recovery

Apply only to the affected mobile journey. Keep the existing router and approved
platform targets. Map these decisions in the existing flow/acceptance record;
do not create a second specification or introduce a framework by default.

- Define each destination's role: deeper detail, peer tab, self-contained modal,
  short sheet, overlay, or replacement of an obsolete step. Select presentation
  from task semantics and the platform's conventions, not its screenshot alone.
- Define back, dismiss and cancel outcomes, including hardware/system back and
  gestures where supported. Preserve unsaved work with an appropriate recovery
  choice; avoid trapping the user. Handle interrupted gestures and nested routes.
- After authentication requested by an action, return to the originating context.
  After completed onboarding or a completed transaction, prevent navigation from
  re-exposing an obsolete action. Keep valid history, receipts and recovery paths;
  completing an operation does not make every previous screen invalid.
- Preserve peer-tab context where the product requires it. Verify direct/deep-link
  entry and cold start without assuming a prior navigation stack or flashing an
  unauthorized destination while session state resolves.
- Prevent rapid taps, retries and back/re-entry from submitting the same operation
  twice. Navigation guards do not replace server authorization or idempotency.
  Optimistic feedback must not falsely confirm payments or irreversible actions.

Verify the changed forward and return paths, cancel, slow/error states and the
relevant session transitions on supported targets. Do not require iOS for an
Android-only app. Framework examples must match the installed router version;
use current project patterns rather than copying Expo-specific APIs universally.

Adapted by Rogemar Agent Toolkit from [Appllama appllama-app-design-skill](https://github.com/Appllama/appllama-skills/tree/dd5caaec3d5d50ad7fc0324da238119c6b7c3707/skills/appllama-app-design-skill), reviewed pin `dd5caaec3d5d50ad7fc0324da238119c6b7c3707`.
Selected methods only; no endorsement or hosted-service integration.
See [MIT notice](../LICENSE.appllama.txt); existing skill licenses remain intact.
