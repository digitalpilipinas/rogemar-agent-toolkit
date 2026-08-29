# Toolkit maintenance contract

- Treat `plugins/rogemar-agent-toolkit/skills/` as the canonical vendored skill
  tree. Do not edit generated installation copies as source.
- Keep the bundle project-agnostic. Repository-specific policy belongs in that
  repository's `AGENTS.md` or an explicit overlay.
- Never add credentials, connector sessions, local configuration, machine-bound
  paths, runtime-managed system skills, or proprietary plugin cache contents.
- Preserve upstream license evidence. Catalog runtime-owned or external skills
  as dependencies instead of copying them without redistribution authority.
- After an intentional skill or dependency change, run `toolkit.py lock`, then
  `toolkit.py verify`, the unit tests, and both release-package checks.
- Do not commit, push, tag, publish, register a marketplace, or install the
  plugin without explicit operator authorization.
