#!/usr/bin/env python3
"""Generate and validate the complete skill inventory in README.md.

The catalog is intentionally JSON-compatible YAML, so this generator uses only
the Python standard library and remains usable on fresh macOS, Linux, and WSL
hosts. It never reads the source machines that produced the snapshot; all
portable descriptions and links come from the checked-in files and catalog.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
CATALOG = ROOT / "catalog" / "skills.yaml"
SKILLS_ROOT = ROOT / "plugins" / "rogemar-agent-toolkit" / "skills"
START = "<!-- BEGIN GENERATED SKILL INVENTORY -->"
END = "<!-- END GENERATED SKILL INVENTORY -->"


def load_catalog() -> dict[str, Any]:
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        if value[0] == '"':
            try:
                return str(json.loads(value))
            except json.JSONDecodeError:
                pass
        return value[1:-1]
    return value


def frontmatter(skill_path: Path) -> dict[str, str]:
    text = skill_path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        return {}
    lines = text[4:end].splitlines()
    values: dict[str, str] = {}
    description_parts: list[str] = []
    collecting_description = False
    for line in lines:
        if collecting_description:
            if line.startswith(" "):
                description_parts.append(line.strip())
                continue
            collecting_description = False
        match = re.match(r"^(name|description):\s*(.*)$", line)
        if match:
            key, raw = match.groups()
            if raw in {">", "|", ">-", "|-", ">+", "|+"}:
                collecting_description = key == "description"
                if collecting_description:
                    description_parts = []
                continue
            values[key] = scalar(raw)
            continue
        author = re.match(r"^\s+author:\s*(.*)$", line)
        if author:
            values["author"] = scalar(author.group(1))
    if description_parts:
        values["description"] = " ".join(description_parts)
    return values


def md(value: str) -> str:
    """Keep generated table cells valid without changing their meaning."""

    return re.sub(r"\s+", " ", value).strip().replace("|", "\\|")


def link(label: str, url: str | None) -> str:
    return f"[{label}]({url})" if url else "—"


def members_cell(members: list[Any]) -> str:
    """Keep large runtime inventories readable while retaining every name."""

    rendered = "<br>".join(f"`{md(str(member))}`" for member in members)
    if len(members) <= 20:
        return rendered
    # Markdown inside a raw HTML details block is not reliably rendered by GFM.
    codes = "<br>".join(f"<code>{html.escape(md(str(member)))}</code>" for member in members)
    return f"<details><summary>{len(members)} members</summary>{codes}</details>"


def packs_section(catalog: dict[str, Any]) -> list[str]:
    rows = [
        "### Pack membership", "",
        "Direct members are listed in full; the installer also resolves required skill dependencies and filters native targets. A skill can belong to several packs. External dependencies are declared, not installed.", "",
        "| Pack | Purpose | Canonical skill members | External dependencies |",
        "| --- | --- | --- | --- |",
    ]
    for name, pack in sorted(catalog.get("packs", {}).items()):
        members = members_cell(pack.get("skills", [])) or "None; dependency-only pack"
        external = "<br>".join(f"[{md(item)}](#dependency-{item})" for item in pack.get("external", [])) or "None"
        rows.append(f"| `{md(name)}` | {md(pack.get('description', ''))} | {members} | {external} |")
    return rows


def dependencies_section(catalog: dict[str, Any]) -> list[str]:
    rows = [
        "### Pack dependencies", "",
        "These are the external skills, providers, runtimes and resource libraries referenced by pack selection. Names and installation routes describe the catalog; they do not prove availability in a fresh environment. The external groups below retain separately observed runtime inventories.", "",
        "| Dependency | Kind / declared targets | Purpose and members or resources | Source, install and activation |",
        "| --- | --- | --- | --- |",
    ]
    for name, dependency in sorted(catalog.get("dependencies", {}).items()):
        targets = dependency.get("targets", list(catalog.get("harnesses", {})))
        target_text = "All declared harnesses" if set(targets) == set(catalog.get("harnesses", {})) else ", ".join(targets)
        details = md(dependency.get("purpose", ""))
        if dependency.get("members"):
            details += "<br>" + members_cell(dependency["members"])
        elif dependency.get("skill_group"):
            group = dependency["skill_group"]
            details += f"<br>Members: [{md(group)}](#external-{group})"
        if dependency.get("paths"):
            details += "<br>Resource paths: " + members_cell(dependency["paths"])
        if dependency.get("resource_counts"):
            details += "<br>Pinned resource counts: " + ", ".join(f"{md(str(k))}: {v}" for k, v in dependency["resource_counts"].items())
        for key, value in dependency.get("runtime_requirements", {}).items():
            text = ", ".join(value) if isinstance(value, list) else str(value)
            details += f"<br>{md(key)}: {md(text)}"
        if dependency.get("native_adapter"):
            details += "<br>" + md(dependency["native_adapter"])
        if dependency.get("integration"):
            details += "<br>" + link("Integration contract", dependency["integration"])
        source = link("Repository", dependency.get("repository"))
        if dependency.get("commit"):
            source += f"<br>Pinned commit: `{md(dependency['commit'])}`"
        source += f"<br>Install: `{md(dependency.get('install', 'Use the owning integration'))}`"
        for harness, command in dependency.get("install_by_harness", {}).items():
            source += f"<br>{md(harness)}: `{md(command)}`"
        for key in ("activation", "inventory_evidence", "version_observed", "upstream_status"):
            if dependency.get(key):
                source += "<br>" + md(str(dependency[key]))
        rows.append(f'| <a id="dependency-{html.escape(name, quote=True)}"></a>**`{md(name)}`** | {md(dependency.get("kind", "external"))}<br>{md(target_text)} | {details} | {source} |')
    return rows


def upstream_by_id(catalog: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(item.get("id")): item
        for item in catalog.get("upstream_repositories", [])
        if isinstance(item, dict) and item.get("id")
    }


def vendored_section(catalog: dict[str, Any]) -> list[str]:
    rows: list[str] = [
        f"### Canonical skills ({len(catalog.get('vendored', []))})",
        "",
        "| Skill | Purpose | Targets | Declared author / provenance | Source and upstream | License / redistribution |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    upstreams = upstream_by_id(catalog)
    for entry in sorted(catalog.get("vendored", []), key=lambda item: str(item.get("name"))):
        name = str(entry.get("name"))
        metadata = frontmatter(SKILLS_ROOT / name / "SKILL.md")
        purpose = metadata.get("description", "Purpose not declared in SKILL.md")
        author = metadata.get(
            "author",
            str(entry.get("author") or "Source author not declared; snapshot maintained by Rogemar"),
        )
        local = f"[SKILL.md](plugins/rogemar-agent-toolkit/skills/{name}/SKILL.md)"
        repository = entry.get("upstream_repository")
        if repository:
            source = f"{local}; {link('upstream', str(repository))}"
        else:
            source = local
        evidence = entry.get("license_evidence")
        if evidence:
            license_info = f"Evidence: `{md(str(evidence))}`; review terms before redistribution"
        else:
            license_info = str(
                entry.get("license_status")
                or "Not declared in snapshot; review before redistribution"
            )
        rows.append(
            f"| {link(f'`{name}`', f'plugins/rogemar-agent-toolkit/skills/{name}/SKILL.md')} "
            f"| {md(purpose)} | {md(', '.join(entry.get('targets', ['portable'])))} | {md(author)} | {source} | {md(license_info)} |"
        )
    return rows


GROUP_PURPOSES = {
    "codex-system-skills": "Codex-provided system skills and capability-maintenance helpers; availability is controlled by the Codex runtime.",
    "coderabbit-skills": "CodeRabbit code review and guarded pull-request autofix workflows.",
    "argent-skills": "Mobile, TV, browser, flow, profiling, screenshot, and debugging workflows from Argent.",
    "unlazy": "Depth-tree execution discipline and gate-based completion checks.",
    "pstack": "Cursor-native `/poteto-mode` and `/setup-pstack` playbooks, principles, and companion skills.",
}

GROUP_UPSTREAM_IDS = {
    "codex-system-skills": "openai-plugins",
}


def external_groups_section(catalog: dict[str, Any]) -> list[str]:
    rows: list[str] = [
        "### External and runtime-managed skill groups",
        "",
        "These are audited skill names and runtime families, not additional toolkit installs or a certification of harness support. Families can overlap; cached versions, source-only descriptors and credentials are not copied by the portable installer.",
        "",
        "| Skill group and members | Purpose | Author / status | License / redistribution | Canonical source and latest install |",
        "| --- | --- | --- | --- | --- |",
    ]
    upstreams = upstream_by_id(catalog)
    for group in sorted(catalog.get("external_skill_groups", []), key=lambda item: str(item.get("name"))):
        name = str(group.get("name"))
        members = members_cell(list(group.get("members", [])))
        upstream = upstreams.get(name) or upstreams.get(GROUP_UPSTREAM_IDS.get(name, ""), {})
        author = str(
            group.get("author")
            or (upstream or {}).get("author")
            or group.get("source")
            or "Runtime-managed"
        )
        status = str(group.get("status") or group.get("mode") or "runtime-managed")
        if group.get("version"):
            status += f"<br>version {md(str(group['version']))}"
        repository = group.get("repository") or (upstream or {}).get("repository")
        install = group.get("install_latest") or (upstream or {}).get("install_latest")
        source = link("repository", str(repository)) if repository else "No public repository declared"
        if install:
            source += f"; `{md(str(install))}`"
        notes = group.get("notes")
        if notes:
            source += f"<br>{md(str(notes))}"
        license_status = str(
            group.get("license_status")
            or (upstream or {}).get("license_status")
            or "Not declared locally; verify owner terms"
        )
        redistribution = str(
            group.get("redistribution_status")
            or "Not vendored; owner-managed"
        )
        rows.append(
            f'| <a id="external-{html.escape(name, quote=True)}"></a>**`{md(name)}`**<br>{members} | {md(str(group.get("purpose") or GROUP_PURPOSES.get(name, "External skill group")))} '
            f"| {md(author)}<br>{md(status)} | {md(license_status)}<br>{md(redistribution)} | {source} |"
        )
    return rows


def runtime_integrations_section(catalog: dict[str, Any]) -> list[str]:
    integrations = catalog.get("runtime_integrations", [])
    if not integrations:
        return []
    rows: list[str] = [
        "### Harness and provider runtimes",
        "",
        "These runtimes are catalog-audited and remain outside the portable skill archive. Their status is evidence captured during a bounded audit, not a live probe or a promise that a fresh VM or cloud worker has the same installation.",
        "",
        "| Runtime | Version / catalog status | Purpose and safe boundary | Author / license | Discovery surface | Documentation |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for runtime in sorted(integrations, key=lambda item: str(item.get("id"))):
        name = str(runtime.get("name") or runtime.get("id"))
        version = str(runtime.get("version") or "unversioned")
        status = str(runtime.get("status") or "runtime-managed")
        purpose = str(runtime.get("purpose") or "Runtime-managed integration")
        author = str(runtime.get("author") or "Runtime owner not declared")
        license_status = str(runtime.get("license_status") or "Not declared locally; verify owner terms")
        surfaces = "<br>".join(
            f"`{md(str(surface))}`" for surface in runtime.get("surfaces", [])
        ) or "—"
        repository = runtime.get("repository")
        documentation = link("documentation", str(repository)) if repository else "No public documentation declared"
        rows.append(
            f"| **`{md(name)}`** | {md(version)}<br>{md(status)} | {md(purpose)} | {md(author)}<br>{md(license_status)} | {surfaces} | {documentation} |"
        )
    return rows


def package_section(catalog: dict[str, Any]) -> list[str]:
    rows: list[str] = [
        "### Runtime plugin packages",
        "",
        "These pinned package references record the capability audit and provenance. The toolkit does not install, authenticate, or copy them.",
        "",
        "| Package (pinned version) | Purpose | Author / source | Latest path |",
        "| --- | --- | --- | --- |",
    ]
    upstreams = upstream_by_id(catalog)
    for package in sorted(catalog.get("external_packages", []), key=lambda item: str(item.get("id"))):
        package_id = str(package.get("id"))
        base, _, source_id = package_id.partition("@")
        if source_id == "goalbuddy":
            upstream = upstreams.get("goalbuddy", {})
            author = str(upstream.get("author", "tolibear"))
            source = link("GoalBuddy repository", str(upstream.get("repository")))
            latest = str(upstream.get("install_latest", "npx goalbuddy@latest"))
        elif source_id == "openai-curated" or source_id.startswith("openai-"):
            upstream = upstreams.get("openai-plugins", {})
            author = "OpenAI runtime"
            source = link("OpenAI Plugins", str(upstream.get("repository")))
            latest = "Enable through the target harness marketplace"
        elif source_id.endswith("-local") or source_id == "rg-codex-local":
            author = "Rogemar / local runtime"
            source = "Private/local dependency; no public repository declared"
            latest = "Use the approved local plugin installation"
        else:
            author = "Runtime-managed"
            source = "No public source declared"
            latest = "Install through the target harness"
        purpose = f"Provides the `{base}` runtime skill/tool family."
        if package.get("status"):
            purpose += f"<br>{md(str(package['status']))}"
        rows.append(
            f"| `{package_id}` ({package.get('version', 'unpinned')}) | {purpose} | {author}<br>{source} | `{latest}` |"
        )
    return rows


def generated_inventory(catalog: dict[str, Any]) -> str:
    lines = [
        "<!-- This section is generated by scripts/inventory_readme.py; edit the catalog or SKILL.md instead. -->",
        f"Catalog coverage: **{len(catalog.get('vendored', []))} canonical skills**, **{len(catalog.get('packs', {}))} packs**, **{len(catalog.get('dependencies', {}))} dependency records**, **{len(catalog.get('external_skill_groups', []))} external groups**, **{len(catalog.get('runtime_integrations', []))} runtime records**, and **{len(catalog.get('external_packages', []))} plugin package records**. These counts describe different units and must not be added as a unique skill total.",
        "",
        *packs_section(catalog),
        "",
        *vendored_section(catalog),
        "",
        *dependencies_section(catalog),
        "",
        *external_groups_section(catalog),
        "",
        *runtime_integrations_section(catalog),
        "",
        *package_section(catalog),
    ]
    return "\n".join(lines).rstrip()


def replace_inventory(readme: str, inventory: str) -> str:
    if START not in readme or END not in readme:
        raise ValueError("README.md is missing generated inventory markers")
    before, remainder = readme.split(START, 1)
    _old, after = remainder.split(END, 1)
    return f"{before}{START}\n{inventory}\n{END}{after}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write the generated section")
    parser.add_argument("--check", action="store_true", help="check without writing (the default)")
    args = parser.parse_args(argv)
    expected = replace_inventory(README.read_text(encoding="utf-8"), generated_inventory(load_catalog()))
    actual = README.read_text(encoding="utf-8")
    if args.write:
        if actual != expected:
            README.write_text(expected, encoding="utf-8")
            print(f"Updated {README.relative_to(ROOT)}")
        else:
            print(f"{README.relative_to(ROOT)} is already current")
        return 0
    if actual != expected:
        print("README.md generated skill inventory is stale; run scripts/inventory_readme.py --write", file=sys.stderr)
        return 1
    print("README.md generated skill inventory is current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
