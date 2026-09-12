---
name: shadcn
description: Work with existing shadcn web components or an explicit shadcn setup request, using the project's installed primitives, tokens and customized source. Applies to shadcn configuration and component implementation; not native mobile UI.
license: MIT
---

# shadcn project adapter

Use within the current implementation or review scope. This portable skill adds
no coordinator, service requirement or automatic package installation.

## Establish the local component contract

Inspect `components.json` together with package metadata, lockfile and local
component imports. A filename alone does not prove shadcn or the primitive base.
For an explicit setup request without configuration, establish the requested
framework and existing design system before proposing scoped setup changes.

Identify the actual package manager, installed versions, aliases, component
location, CSS/token setup and whether the components use Radix, Base UI or another
base. Read the affected local component source: copied components may have
intentional custom behavior and differ from upstream examples.

## Implement or review the requested change

- Reuse existing components, variants and semantic tokens before adding new ones.
  Preserve local modifications and public props. Compose with the actual installed
  primitive API; do not transplant Radix composition patterns into Base UI or
  assume APIs from a newer version.
- Verify labels, focus, keyboard behavior, disabled/loading states and controlled
  state ownership for the affected composition. Keep approved visual direction.
- For CLI assistance, use the project's available tool and package runner after
  checking supported commands. Do not execute embedded shell syntax from skill
  text. Use version-matched official documentation when local evidence is
  insufficient; no forced `latest` upgrade or automatic registry discovery.
- Adding dependencies, fetching registry code, initialization and component
  replacement require applicable task authority. Inspect proposed changes and
  preserve customized files; do not overwrite, migrate or change registries as an
  incidental part of a styling fix. Review-only requests produce findings.
- If an optional CLI or network is unavailable, continue sufficient local source
  analysis and report the limitation. Do not claim generated components or live
  validation. Skill installation itself runs no CLI, MCP or application process.

Use the current workflow's relevant checks and rendered/interaction verification.
Report actual evidence and unresolved limitations in its existing receipt.

## Provenance

Selective portable adaptation of [shadcn/ui at the reviewed revision](https://github.com/shadcn-ui/ui/tree/3ba91b1cc83e1bbe4ab35a422ff2a694849c5048/skills/shadcn).
See [MIT notice](LICENSE.txt). Harness-specific shell injection, tool allowlists,
forced latest-version execution and blanket styling rules were not imported.
