# Mobile control and state craft

For affected mobile controls, use the existing design system and platform-native
primitives or compatible wrappers. Custom controls remain appropriate when the
product needs them and semantics, input and accessibility are preserved. Do not
install a control, state, list or keyboard library solely to follow this method.

- Check safe areas, short/narrow layouts, text scaling and supported orientation.
  Verify relevant supported themes without turning a small fix into a new theme
  implementation. Preserve semantic colors, typography and approved brand tokens;
  no blanket single-accent or decorative-style ban.
- Keep labels visible independently of placeholders. Check appropriate keyboard,
  autofill, focus/next/submit behavior and keyboard appearance/dismissal. Inputs
  must remain reachable and errors understandable with assistive technology.
- Use platform-appropriate effective touch targets and spacing: normally at least
  44 by 44 points on iOS and 48 by 48 dp on Android. These are target areas, not
  mandatory icon sizes. Honor stricter project accessibility requirements and
  verify focus order, labels and relevant VoiceOver/TalkBack behavior separately.
- Cover relevant loading, empty, disabled, error, retry, offline and success
  states. Feedback should acknowledge input promptly without claiming a remote
  operation succeeded before it did. Check rapid taps and interrupted operations.
- Keep haptics supplementary and supported. Preserve useful feedback when haptics
  or motion are unavailable. Reuse approved assets; asset generation and provider
  spending need their own task scope and authority.
- Profile demonstrated typing, scrolling or rendering problems before changing
  state architecture, input control or virtualization. Match any library/API
  recipe to installed versions; do not prescribe FlashList or uncontrolled inputs
  for every surface. Older advice such as InteractionManager is not portable
  across React Native versions.

Use the existing visual/accessibility evidence record for the exact candidate,
route, state and runtime. A screenshot demonstrates layout, not interaction,
assistive-technology behavior or physical-device performance.

Platform guidance: [Android touch targets](https://developer.android.com/guide/topics/ui/accessibility/views/apps-views)
and [Apple accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility).

Adapted by Rogemar Agent Toolkit from [Appllama appllama-app-design-skill](https://github.com/Appllama/appllama-skills/tree/dd5caaec3d5d50ad7fc0324da238119c6b7c3707/skills/appllama-app-design-skill), reviewed pin `dd5caaec3d5d50ad7fc0324da238119c6b7c3707`.
Selected methods only; no endorsement or hosted-service integration.
See [MIT notice](../LICENSE.appllama.txt); existing skill licenses remain intact.
