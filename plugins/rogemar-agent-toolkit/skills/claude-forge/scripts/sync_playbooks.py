#!/usr/bin/env python3
"""Regenerate Claude Forge playbooks from the shared engineering playbooks."""
from __future__ import annotations

import json
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
SKILLS = SKILL.parent
PORTABLE = SKILLS / "engineering-playbooks" / "playbooks"
SOURCE_MAP = SKILLS / "engineering-playbooks" / "references" / "source-map.json"
DEST = SKILL / "playbooks"

REPLACEMENTS = (
    ("](../references/", "](../../engineering-playbooks/references/"),
    ("](../upstream-notices/", "](../../engineering-playbooks/upstream-notices/"),
)


def title_from(text: str) -> str:
    first = text.splitlines()[0]
    if not first.startswith("#"):
        raise ValueError("playbook missing heading")
    return first.lstrip("#").strip()


def body_after_heading(text: str) -> str:
    lines = text.splitlines(keepends=True)
    rest = "".join(lines[1:])
    if rest.startswith("\n"):
        rest = rest[1:]
    return rest


def render(source: str) -> str:
    title = title_from(source)
    body = body_after_heading(source)
    for old, new in REPLACEMENTS:
        body = body.replace(old, new)
    return (
        f"# {title}\n\n"
        "Read [the Claude runtime contract](../references/claude-runtime.md) before any worker, model, tool, or publication action. "
        "Resolve companion names through [the companion index](../references/companions.md). "
        "The method below is the shared engineering playbook, with links adjusted so they resolve from this package.\n\n"
        + body
    )


def render_all() -> dict[str, str]:
    methods = json.loads(SOURCE_MAP.read_text())["methods"]
    rendered = {}
    for row in methods:
        name = row["method"]
        rendered[name] = render((PORTABLE / f"{name}.md").read_text())
    return rendered


def main() -> None:
    DEST.mkdir(exist_ok=True)
    written = render_all()
    for name, text in written.items():
        (DEST / f"{name}.md").write_text(text)
    for path in DEST.glob("*.md"):
        if path.stem not in written:
            path.unlink()
    print(f"Wrote {len(written)} Claude playbooks")


if __name__ == "__main__":
    main()
