#!/usr/bin/env python3
"""Verify, install, diagnose, roll back, and package Rogemar Agent Toolkit."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import uuid
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins" / "rogemar-agent-toolkit"
SKILLS_ROOT = PLUGIN_ROOT / "skills"
CATALOG_PATH = ROOT / "catalog" / "skills.yaml"
LOCK_PATH = ROOT / "catalog" / "skills.lock.json"
CODEX_MANIFEST = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
PORTABLE_MANIFEST = PLUGIN_ROOT / "plugin.json"
MARKETPLACE_MANIFEST = ROOT / ".agents" / "plugins" / "marketplace.json"
README_PATH = ROOT / "README.md"
PACKAGE_NAME = "rogemar-agent-toolkit"
IGNORED_PARTS = {"__pycache__", ".DS_Store", "node_modules"}
IGNORED_SUFFIXES = {".pyc", ".pyo"}
SECRET_FILENAMES = {".env", "id_rsa", "id_ed25519"}
SECRET_SUFFIXES = {".pem", ".key", ".p12", ".pfx"}
MACHINE_PATH_PATTERNS = (
    re.compile(r"/Users/[A-Za-z0-9._-]+/"),
    re.compile(r"/home/[A-Za-z0-9._-]+/"),
    re.compile(r"[A-Za-z]:\\\\Users\\\\[^\\\\\s]+\\\\"),
)
SECRET_CONTENT_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bghp_[A-Za-z0-9]{30,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{40,}\b"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{32,}\b"),
)


class ToolkitError(RuntimeError):
    """Expected, user-facing toolkit failure."""


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ToolkitError(f"missing required file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ToolkitError(f"invalid JSON-compatible data in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ToolkitError(f"expected a JSON object in {path}")
    return value


def write_json_atomic(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    os.replace(temporary, path)


def package_version() -> str:
    version = load_json(PORTABLE_MANIFEST).get("version")
    if not isinstance(version, str) or not version:
        raise ToolkitError("portable plugin manifest has no valid version")
    return version


def should_ignore(path: Path) -> bool:
    return any(part in IGNORED_PARTS for part in path.parts) or path.suffix in IGNORED_SUFFIXES


def skill_files(skill_dir: Path) -> list[Path]:
    files: list[Path] = []
    for path in skill_dir.rglob("*"):
        relative = path.relative_to(skill_dir)
        if should_ignore(relative):
            continue
        if path.is_symlink():
            raise ToolkitError(f"symlink is not portable: {path}")
        if path.is_file():
            files.append(path)
    return sorted(files, key=lambda item: item.relative_to(skill_dir).as_posix())


def tree_digest(skill_dir: Path, *, legacy: bool = False) -> tuple[str, int]:
    digest = hashlib.sha256()
    files = skill_files(skill_dir)
    for path in files:
        relative = path.relative_to(skill_dir).as_posix().encode("utf-8")
        digest.update(relative)
        digest.update(b"\0")
        if not legacy:
            digest.update(b"x\0" if path.stat().st_mode & 0o111 else b"-\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest(), len(files)


def vendored_catalog() -> list[dict[str, Any]]:
    catalog = load_json(CATALOG_PATH)
    entries = catalog.get("vendored")
    if not isinstance(entries, list) or not all(isinstance(item, dict) for item in entries):
        raise ToolkitError("catalog vendored field must be an array of objects")
    return entries


def vendored_names() -> list[str]:
    names: list[str] = []
    for entry in vendored_catalog():
        name = entry.get("name")
        if not isinstance(name, str) or not name:
            raise ToolkitError("each vendored catalog entry requires a name")
        names.append(name)
    return names


def safe_name(value: Any) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value):
        raise ToolkitError(f"invalid skill or pack name: {value!r}")
    return value


def resolve_selection(harness: str, profile: str, packs: list[str]) -> dict[str, Any]:
    """Resolve only declared hard requirements. Optional routing never expands a pack."""
    catalog = load_json(CATALOG_PATH)
    if harness not in catalog["harnesses"]:
        raise ToolkitError(f"unknown harness: {harness}")
    profiles = catalog["profiles"]
    if profile not in profiles:
        raise ToolkitError(f"unknown profile: {profile}")
    selected_packs = sorted(set(profiles[profile] + packs))
    unknown = set(selected_packs) - set(catalog["packs"])
    if unknown:
        raise ToolkitError("unknown packs: " + ", ".join(sorted(unknown)))
    entries = {entry["name"]: entry for entry in catalog["vendored"]}
    defaults = catalog["vendored_defaults"]["targets"]
    selected: set[str] = set()
    external: set[str] = set()
    skipped: set[str] = set()
    visiting: set[str] = set()

    def add(name: str, required_by: str | None = None) -> None:
        safe_name(name)
        if name not in entries:
            raise ToolkitError(f"unknown skill requirement: {name}")
        if harness not in entries[name].get("targets", defaults):
            if required_by:
                raise ToolkitError(f"{required_by} requires {name}, incompatible with {harness}")
            skipped.add(name)
            return
        if name in visiting:
            raise ToolkitError(f"cyclic skill requirement at {name}")
        if name in selected:
            return
        visiting.add(name)
        for requirement in entries[name].get("requires", []):
            add(requirement, name)
        visiting.remove(name)
        selected.add(name)

    for pack_name in selected_packs:
        pack = catalog["packs"][pack_name]
        for name in pack["skills"]:
            add(name)
        for dependency in pack.get("external", []):
            if harness in catalog["dependencies"][dependency]["targets"]:
                external.add(dependency)
    return {"harness": harness, "profile": profile, "packs": selected_packs,
            "skills": sorted(selected), "external": sorted(external),
            "incompatible_skills_skipped": sorted(skipped)}


def parse_frontmatter(skill_path: Path) -> tuple[str | None, bool]:
    text = skill_path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None, False
    end = text.find("\n---", 4)
    if end < 0:
        return None, False
    frontmatter = text[4:end]
    match = re.search(r"(?m)^name:\s*['\"]?([^'\"\n]+?)['\"]?\s*$", frontmatter)
    has_description = re.search(r"(?m)^description:\s*.+$", frontmatter) is not None
    return (match.group(1).strip() if match else None), has_description


def build_lock() -> dict[str, Any]:
    catalog = load_json(CATALOG_PATH)
    skills: dict[str, Any] = {}
    for name in sorted(vendored_names()):
        digest, file_count = tree_digest(SKILLS_ROOT / name)
        skills[name] = {"sha256": digest, "file_count": file_count}
    return {
        "schema_version": 2,
        "package": PACKAGE_NAME,
        "version": package_version(),
        "hash_format": "sha256:path-nul-executable-nul-content-nul",
        "skills": skills,
        "selection": {key: catalog[key] for key in
                      ("harnesses", "profiles", "packs", "dependencies")},
        "skill_contracts": {entry["name"]: {
            "targets": entry.get("targets", catalog["vendored_defaults"]["targets"]),
            "requires": entry.get("requires", [])} for entry in catalog["vendored"]},
        "external_dependencies": {
            "skill_groups": catalog.get("external_skill_groups", []),
            "runtime_integrations": catalog.get("runtime_integrations", []),
            "upstream_repositories": catalog.get("upstream_repositories", []),
            "packages": catalog.get("external_packages", []),
        },
    }


def structural_errors(check_lock: bool = True) -> list[str]:
    errors: list[str] = []
    try:
        portable = load_json(PORTABLE_MANIFEST)
        codex = load_json(CODEX_MANIFEST)
        marketplace = load_json(MARKETPLACE_MANIFEST)
        catalog = load_json(CATALOG_PATH)
    except ToolkitError as exc:
        return [str(exc)]
    readme = README_PATH.read_text(encoding="utf-8") if README_PATH.is_file() else ""

    for label, manifest in (("portable", portable), ("Codex", codex)):
        if manifest.get("name") != PACKAGE_NAME:
            errors.append(f"{label} manifest name must be {PACKAGE_NAME}")
        if manifest.get("version") != portable.get("version"):
            errors.append(f"{label} manifest version does not match portable manifest")

    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or len(plugins) != 1:
        errors.append("marketplace must declare exactly one plugin")
    elif plugins[0].get("name") != PACKAGE_NAME:
        errors.append("marketplace plugin name does not match package")

    package = catalog.get("package")
    if not isinstance(package, dict) or package.get("name") != PACKAGE_NAME:
        errors.append("catalog package name does not match package")
    elif package.get("version") != portable.get("version"):
        errors.append("catalog version does not match manifests")

    try:
        names = vendored_names()
    except ToolkitError as exc:
        return errors + [str(exc)]
    duplicates = sorted({name for name in names if names.count(name) > 1})
    if duplicates:
        errors.append(f"duplicate vendored catalog names: {', '.join(duplicates)}")

    try:
        for name in names:
            safe_name(name)
        if catalog["package"]["default_profile"] != "core":
            errors.append("fresh environments must default to the core profile")
        for name, harness in catalog["harnesses"].items():
            safe_name(name)
            for scope in ("project", "user"):
                value = Path(harness[scope])
                if value.is_absolute() or ".." in value.parts or not value.parts:
                    errors.append(f"unsafe harness layout: {name}")
        for name, pack in catalog["packs"].items():
            safe_name(name)
            for dependency in pack.get("external", []):
                if dependency not in catalog["dependencies"]:
                    errors.append(f"{name}: unknown external dependency {dependency}")
        for name, dependency in catalog["dependencies"].items():
            safe_name(name)
            if not set(dependency["targets"]).issubset(catalog["harnesses"]):
                errors.append(f"{name}: unknown dependency target")
        covered = {name for pack in catalog["packs"].values() for name in pack["skills"]}
        if covered != set(names):
            errors.append("pack coverage differs from the vendored skill catalogue")
        for harness in catalog["harnesses"]:
            for profile in catalog["profiles"]:
                resolve_selection(harness, profile, [])
    except (KeyError, TypeError, ToolkitError) as exc:
        errors.append(f"invalid selection catalogue: {exc}")

    tree_names = sorted(
        path.name for path in SKILLS_ROOT.iterdir() if path.is_dir() and not path.is_symlink()
    ) if SKILLS_ROOT.exists() else []
    if sorted(names) != tree_names:
        missing = sorted(set(names) - set(tree_names))
        extra = sorted(set(tree_names) - set(names))
        if missing:
            errors.append(f"catalog skills missing from tree: {', '.join(missing)}")
        if extra:
            errors.append(f"uncataloged skill directories: {', '.join(extra)}")

    inventory_start = "<!-- BEGIN GENERATED SKILL INVENTORY -->"
    inventory_end = "<!-- END GENERATED SKILL INVENTORY -->"
    if inventory_start not in readme or inventory_end not in readme:
        errors.append("README.md is missing the generated skill inventory")
    for name in sorted(names):
        inventory_link = f"plugins/rogemar-agent-toolkit/skills/{name}/SKILL.md"
        if inventory_link not in readme:
            errors.append(f"README.md inventory is missing vendored skill: {name}")

    entry_by_name = {entry.get("name"): entry for entry in vendored_catalog()}
    for name in sorted(set(names) & set(tree_names)):
        skill_dir = SKILLS_ROOT / name
        skill_path = skill_dir / "SKILL.md"
        if not skill_path.is_file():
            errors.append(f"{name}: missing SKILL.md")
            continue
        parsed_name, has_description = parse_frontmatter(skill_path)
        if parsed_name != name:
            errors.append(f"{name}: frontmatter name is {parsed_name!r}")
        if not has_description:
            errors.append(f"{name}: frontmatter description is missing")
        license_evidence = entry_by_name[name].get("license_evidence")
        if license_evidence and not (skill_dir / str(license_evidence)).is_file():
            errors.append(f"{name}: missing license evidence {license_evidence}")
        try:
            files = skill_files(skill_dir)
        except ToolkitError as exc:
            errors.append(str(exc))
            continue
        for path in files:
            relative = path.relative_to(ROOT)
            lowered = path.name.lower()
            if lowered in SECRET_FILENAMES or path.suffix.lower() in SECRET_SUFFIXES:
                errors.append(f"forbidden secret-like file: {relative}")
            if path.suffix.lower() in {".md", ".txt", ".json", ".yaml", ".yml", ".py", ".sh"}:
                try:
                    text = path.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    continue
                for pattern in MACHINE_PATH_PATTERNS:
                    match = pattern.search(text)
                    if match:
                        errors.append(f"machine-specific path in {relative}: {match.group(0)}")
                        break
                for pattern in SECRET_CONTENT_PATTERNS:
                    if pattern.search(text):
                        errors.append(f"secret-like content in {relative}")
                        break

    upstreams = catalog.get("upstream_repositories")
    if not isinstance(upstreams, list) or not all(isinstance(item, dict) for item in upstreams):
        errors.append("catalog upstream_repositories must be an array of objects")
    else:
        upstream_ids: list[str] = []
        for upstream in upstreams:
            upstream_id = upstream.get("id")
            repository = upstream.get("repository")
            install_latest = upstream.get("install_latest")
            if not isinstance(upstream_id, str) or not upstream_id:
                errors.append("each upstream repository requires an id")
            else:
                upstream_ids.append(upstream_id)
            if not isinstance(repository, str) or not repository.startswith("https://github.com/"):
                errors.append(f"{upstream_id or 'upstream'}: invalid GitHub repository URL")
            elif repository not in readme:
                errors.append(f"{upstream_id}: repository is missing from README.md")
            if not isinstance(install_latest, str) or not install_latest:
                errors.append(f"{upstream_id or 'upstream'}: install_latest is required")
        duplicate_upstreams = sorted(
            {name for name in upstream_ids if upstream_ids.count(name) > 1}
        )
        if duplicate_upstreams:
            errors.append(
                "duplicate upstream repository ids: " + ", ".join(duplicate_upstreams)
            )

    runtime_integrations = catalog.get("runtime_integrations", [])
    if not isinstance(runtime_integrations, list) or not all(
        isinstance(item, dict) for item in runtime_integrations
    ):
        errors.append("catalog runtime_integrations must be an array of objects")
    else:
        runtime_ids = [item.get("id") for item in runtime_integrations]
        invalid_ids = [str(item) for item in runtime_ids if not isinstance(item, str) or not item]
        if invalid_ids:
            errors.append("each runtime integration requires a non-empty id")
        required_runtime_fields = ("name", "version", "status", "purpose")
        for runtime in runtime_integrations:
            runtime_id = str(runtime.get("id") or "runtime")
            for field in required_runtime_fields:
                value = runtime.get(field)
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"{runtime_id}: runtime integration requires {field}")
            surfaces = runtime.get("surfaces", [])
            if not isinstance(surfaces, list) or any(
                not isinstance(surface, str) or not surface.strip() for surface in surfaces
            ):
                errors.append(f"{runtime_id}: runtime integration surfaces must be strings")
        duplicate_runtime_ids = sorted(
            {str(item) for item in runtime_ids if runtime_ids.count(item) > 1}
        )
        if duplicate_runtime_ids:
            errors.append(
                "duplicate runtime integration ids: " + ", ".join(duplicate_runtime_ids)
            )

    if check_lock:
        try:
            expected = build_lock()
            actual = load_json(LOCK_PATH)
            if actual != expected:
                errors.append("skills.lock.json is stale; run toolkit.py lock")
        except ToolkitError as exc:
            errors.append(str(exc))
    return errors


def command_lock(_args: argparse.Namespace) -> int:
    errors = structural_errors(check_lock=False)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    write_json_atomic(LOCK_PATH, build_lock())
    print(f"Wrote {LOCK_PATH.relative_to(ROOT)} for {len(vendored_names())} skills.")
    return 0


def command_verify(_args: argparse.Namespace) -> int:
    errors = structural_errors(check_lock=True)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(
        f"Verified {PACKAGE_NAME} {package_version()}: "
        f"{len(vendored_names())} vendored skills, README markers, manifests, "
        f"portability/secret checks, and lockfile."
    )
    return 0


def command_inventory(_args: argparse.Namespace) -> int:
    catalog = load_json(CATALOG_PATH)
    print(f"Package: {PACKAGE_NAME} {package_version()}")
    print(f"Vendored skills: {len(vendored_names())}")
    print("Default: core; run select --harness <name> --pack <pack> for exact resolution.")
    for name, pack in catalog["packs"].items():
        print(f"  pack {name}: {len(pack['skills'])} entries; {pack['description']}")
    groups = catalog.get("external_skill_groups", [])
    packages = catalog.get("external_packages", [])
    upstreams = catalog.get("upstream_repositories", [])
    runtimes = catalog.get("runtime_integrations", [])
    print(f"External skill groups: {len(groups)}")
    print(f"External plugin packages: {len(packages)}")
    print(f"Documented upstream repositories: {len(upstreams)}")
    print(f"Runtime integrations: {len(runtimes)}")
    for group in groups:
        print(f"  dependency: {group.get('name')} ({group.get('mode')})")
    for runtime in runtimes:
        print(f"  runtime: {runtime.get('id')} ({runtime.get('status')})")
    return 0


def run_probe(command: list[str]) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, str(exc)
    output = (result.stdout + "\n" + result.stderr).strip()
    return result.returncode == 0, output


def command_doctor(_args: argparse.Namespace) -> int:
    verify_ok = not structural_errors(check_lock=True)
    print(f"bundle: {'ready' if verify_ok else 'invalid'}")
    print(f"platform: {platform.system()} {platform.machine()}")
    print(f"python: {sys.version.split()[0]} ({'ready' if sys.version_info >= (3, 9) else 'unsupported'})")
    for executable in ("git", "codex", "cursor-agent", "agent"):
        resolved = shutil.which(executable)
        print(f"{executable}: {resolved if resolved else 'missing'}")

    catalog = load_json(CATALOG_PATH)
    codex = shutil.which("codex")
    plugin_output = ""
    plugin_list_ready = False
    if codex:
        plugin_list_ready, plugin_output = run_probe([codex, "plugin", "list"])
    print(f"codex plugin catalog: {'readable' if plugin_list_ready else 'unavailable'}")
    installed_plugins = {
        match.group(1)
        for line in plugin_output.splitlines()
        if (match := re.match(r"^(\S+)\s+installed, enabled\s+", line))
    }
    for package in catalog.get("external_packages", []):
        package_id = str(package.get("id", ""))
        ready = plugin_list_ready and package_id in installed_plugins
        print(f"external {package_id}: {'detected' if ready else 'not detected'}")
    for runtime in catalog.get("runtime_integrations", []):
        runtime_id = str(runtime.get("id", "unknown"))
        status = str(runtime.get("status", "runtime-managed"))
        version = str(runtime.get("version", "unversioned"))
        print(f"runtime {runtime_id}: {version} (catalog observation; {status})")
    print("connector authentication: not inspected (intentionally out of scope)")
    return 0 if verify_ok and sys.version_info >= (3, 9) else 1


def resource_fingerprint(path: Path) -> str | None:
    if not exists(path):
        return None
    if path.is_symlink() or not path.is_dir():
        raise ToolkitError("resource destination is not a regular directory")
    digest = hashlib.sha256()
    for entry in sorted(path.rglob("*")):
        if entry.is_symlink():
            raise ToolkitError("managed resource directory contains a symlink")
        if entry.is_file():
            digest.update(entry.relative_to(path).as_posix().encode() + b"\0")
            digest.update(b"x\0" if entry.stat().st_mode & 0o111 else b"-\0")
            digest.update(entry.read_bytes())
    return digest.hexdigest()


def command_resources(args: argparse.Namespace) -> int:
    """Import only pinned Git objects, never application state or untracked files."""
    dependency = load_json(CATALOG_PATH)["dependencies"]["opendesign-library"]
    source = Path(args.source).expanduser().resolve()
    destination = Path(args.destination).expanduser().absolute()
    if destination.is_symlink():
        raise ToolkitError("resource destination must not be a symlink")
    if source == destination.resolve() or source in destination.resolve().parents:
        raise ToolkitError("resource destination must be outside the source checkout")
    commit = dependency["commit"]
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ToolkitError("resource source must be a full pinned Git commit")
    result = subprocess.run(
        ["git", "-C", str(source), "archive", "--format=tar", commit, "--", *dependency["paths"]],
        env={**os.environ, "GIT_NO_REPLACE_OBJECTS": "1"}, capture_output=True, check=False,
    )
    if result.returncode:
        raise ToolkitError("pinned OpenDesign resource objects are unavailable; obtain the declared source revision first")
    files: dict[str, bytes] = {}
    modes: dict[str, int] = {}
    with tarfile.open(fileobj=io.BytesIO(result.stdout), mode="r:") as archive:
        for member in archive.getmembers():
            path = Path(member.name)
            if path.is_absolute() or ".." in path.parts or not path.parts:
                raise ToolkitError("unsafe resource archive path")
            if path.parts[0] not in dependency["paths"]:
                raise ToolkitError("unexpected resource archive member")
            if member.isdir():
                continue
            if not member.isfile():
                raise ToolkitError(f"resource is not a regular file: {member.name}")
            handle = archive.extractfile(member)
            assert handle is not None
            data = handle.read()
            if data.startswith(b"version https://git-lfs.github.com/spec/v1"):
                raise ToolkitError(f"resource contains an unresolved Git LFS pointer: {member.name}")
            files[member.name] = data
            modes[member.name] = 0o755 if member.mode & 0o111 else 0o644
    missing = set(dependency["paths"]) - {Path(name).parts[0] for name in files}
    if missing:
        raise ToolkitError("pinned resource groups are missing: " + ", ".join(sorted(missing)))
    receipt = {"package": PACKAGE_NAME, "resource": "opendesign-library",
               "repository": dependency["repository"], "commit": commit,
               "modes": modes,
               "files": {name: hashlib.sha256(data).hexdigest() for name, data in sorted(files.items())}}
    receipt_name = ".toolkit-resources.json"
    before_fingerprint = resource_fingerprint(destination)
    previous = None
    if destination.exists():
        previous = load_json(destination / receipt_name)
        if previous.get("package") != PACKAGE_NAME or previous.get("resource") != "opendesign-library":
            raise ToolkitError("refusing to replace an unmanaged resource directory")
        actual = {p.relative_to(destination).as_posix(): file_sha256(p)
                  for p in skill_files(destination) if p.name != receipt_name}
        actual_modes = {p.relative_to(destination).as_posix(): 0o755 if p.stat().st_mode & 0o111 else 0o644
                        for p in skill_files(destination) if p.name != receipt_name}
        if previous == receipt and actual == receipt["files"] and actual_modes == modes:
            print(f"Resource library already current: {len(files)} files at {destination}")
            return 0
        if not args.backup_conflicts:
            raise ToolkitError("resource library differs; review it before --backup-conflicts")
    if args.dry_run:
        print(json.dumps({"destination": str(destination), "commit": commit,
                          "files": len(files), "paths": dependency["paths"],
                          "replaces_managed_library": previous is not None}, indent=2))
        return 0
    destination.parent.mkdir(parents=True, exist_ok=True)
    operation_lock = destination.with_name(f".{destination.name}.toolkit-operation.lock")
    try:
        lock_fd = os.open(operation_lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise ToolkitError("another resource operation is active; inspect the sibling operation lock") from exc
    os.close(lock_fd)
    stage = None
    backup = None
    try:
        stage = Path(tempfile.mkdtemp(prefix=".opendesign-resources-", dir=destination.parent))
        for name, data in files.items():
            path = stage / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            path.chmod(modes[name])
        write_json_atomic(stage / receipt_name, receipt)
        if resource_fingerprint(destination) != before_fingerprint:
            raise ToolkitError("resource destination changed during preparation; nothing replaced")
        if destination.exists():
            backup = destination.with_name(destination.name + f".backup-{utc_stamp()}-{uuid.uuid4().hex[:8]}")
            os.replace(destination, backup)
        try:
            os.replace(stage, destination)
        except Exception:
            if backup:
                os.replace(backup, destination)
            raise
    finally:
        if stage is not None and stage.exists():
            shutil.rmtree(stage)
        operation_lock.unlink()
    print(f"Imported {len(files)} pinned resource files into {destination}; no app was started.")
    if backup:
        print(f"Recoverable prior library: {backup}")
    return 0


def target_paths(args: argparse.Namespace) -> tuple[Path, Path, Path]:
    catalog = load_json(CATALOG_PATH)
    root = (Path(args.project_root or Path.cwd()).expanduser().resolve()
            if args.target == "project" else Path.home().resolve())
    harness = getattr(args, "harness", None)
    if not harness:
        candidates = {root / layout[args.target] / f"{PACKAGE_NAME}.lock.json"
                      for layout in catalog["harnesses"].values()}
        found = [path for path in candidates if exists(path)]
        if len(found) > 1:
            raise ToolkitError("multiple managed harness installations exist; specify --harness")
        if found:
            checked_path(root, found[0].relative_to(root))
            harness = read_optional_state(found[0]).get("harness")
            if harness:
                args.harness = harness
    harness = harness or "agent-skills"
    if harness not in catalog["harnesses"]:
        raise ToolkitError(f"unknown harness: {harness}")
    layout = catalog["harnesses"][harness][args.target]
    agents_root = root / layout
    paths = (agents_root / "skills", agents_root / f"{PACKAGE_NAME}.lock.json",
             agents_root / f".{PACKAGE_NAME}")
    for path in paths:
        checked_path(root, path.relative_to(root))
    return paths


def checked_path(root: Path, relative: Path) -> Path:
    """The selected root may be explicit; managed descendants may not redirect it."""
    if relative.is_absolute() or ".." in relative.parts:
        raise ToolkitError("managed path leaves its selected root")
    path = root
    for part in relative.parts:
        path = path / part
        if path.is_symlink():
            raise ToolkitError(f"managed path has a symlinked ancestor or control file: {path}")
    return path


def destination_for(name: str, args: argparse.Namespace, record: dict | None = None) -> Path:
    safe_name(name)
    skills_root, _state_path, _control_root = target_paths(args)
    # Codex discovers portable methods once in .agents; its native adapters stay in .codex.
    native = (record or {}).get("native", False)
    if record is None and (getattr(args, "harness", None) or "agent-skills") == "codex":
        native = next(item for item in vendored_catalog() if item["name"] == name).get("targets") == ["codex"]
    if native:
        if (getattr(args, "harness", None) or "agent-skills") != "codex":
            raise ToolkitError("native Codex placement requires the Codex harness")
        parent = checked_path(skills_root.parent.parent, Path(".codex/skills"))
        return parent / name
    return skills_root / name


def read_optional_state(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    state = load_json(path)
    if state.get("package") != PACKAGE_NAME or not isinstance(state.get("skills"), dict):
        raise ToolkitError("invalid managed installation state")
    for name, record in state["skills"].items():
        safe_name(name)
        if not isinstance(record, dict) or not re.fullmatch(r"[0-9a-f]{64}", str(record.get("sha256", ""))):
            raise ToolkitError(f"invalid managed hash for {name}")
    return state


def exists(path: Path) -> bool:
    return path.exists() or path.is_symlink()


def installed_digest(path: Path) -> str | None:
    if not exists(path):
        return None
    if path.is_symlink():
        return "link:" + str(path.readlink())
    if not path.is_dir():
        return "file:" + file_sha256(path)
    return tree_digest(path)[0]


def copy_or_link(source: Path, destination: Path, link: bool) -> None:
    if link:
        destination.symlink_to(source, target_is_directory=True)
    else:
        shutil.copytree(source, destination, symlinks=False,
                        ignore=shutil.ignore_patterns(*IGNORED_PARTS, "*.pyc", "*.pyo"))


def install_selection(args: argparse.Namespace, state: dict | None) -> dict[str, Any]:
    args.harness = args.harness or (state or {}).get("harness", "agent-skills")
    if state and state.get("harness", args.harness) != args.harness:
        raise ToolkitError("this shared installation has another primary harness; use a separate project or migrate it explicitly")
    if args.profile is not None and args.pack is None:
        args.pack = []  # An explicit profile starts a new selection.
    profile = args.profile if args.profile is not None else (state or {}).get("profile", "core")
    packs = args.pack if args.pack is not None else (state or {}).get("requested_packs", [])
    return resolve_selection(args.harness, profile, packs)


def command_select(args: argparse.Namespace) -> int:
    selection = resolve_selection(args.harness or "agent-skills", args.profile or "core", args.pack or [])
    catalog = load_json(CATALOG_PATH)
    selection["dependencies"] = {name: catalog["dependencies"][name] for name in selection["external"]}
    print(json.dumps(selection, indent=2))
    return 0


def command_install(args: argparse.Namespace) -> int:
    if structural_errors(check_lock=True):
        raise ToolkitError("bundle verification failed; run toolkit.py verify")
    _skills_root, state_path, control_root = target_paths(args)
    state = read_optional_state(state_path)
    if state and state.get("schema_version") == 1 and not args.harness:
        raise ToolkitError("legacy installation: specify --harness explicitly before migration")
    selection = install_selection(args, state)
    _skills_root, state_path, control_root = target_paths(args)
    state_bytes = state_path.read_bytes() if state_path.exists() else None
    managed = (state or {}).get("skills", {})
    names = selection["skills"]
    removed = sorted(set(managed) - set(names))
    fingerprints: dict[str, str | None] = {}
    previous_paths: dict[str, Path] = {}
    changed: list[str] = []
    conflicts: list[str] = []
    desired: dict[str, Any] = {}
    for name in sorted(set(names) | set(managed)):
        old_path = destination_for(name, args, managed.get(name))
        previous_paths[name] = old_path
        fingerprints[name] = installed_digest(old_path)
        if name in names:
            digest, count = tree_digest(SKILLS_ROOT / name)
            path = destination_for(name, args)
            desired[name] = {"sha256": digest, "file_count": count,
                             "native": path != _skills_root / name}
            # A placement migration may not hide a second destination collision.
            if path != old_path and exists(path):
                conflicts.append(f"{name}: new native destination already exists; reconcile it first")
            wanted = "link:" + str(SKILLS_ROOT / name) if args.link else digest
            same = fingerprints[name] == wanted and path == old_path
            if fingerprints[name] is not None and name not in managed:
                if not (same and args.adopt_identical) and not args.backup_conflicts:
                    conflicts.append(f"{name}: refusing to overwrite unmanaged skill; use --adopt-identical for exact copies or review --backup-conflicts")
            if not same:
                changed.append(name)
        if name in managed and fingerprints[name] is not None:
            expected = managed[name]["sha256"]
            if state.get("schema_version") == 1 and old_path.is_dir() and not old_path.is_symlink():
                if tree_digest(old_path, legacy=True)[0] == expected:
                    expected = fingerprints[name]
            if (state or {}).get("mode") == "link":
                expected = "link:" + str(SKILLS_ROOT / name)
            if fingerprints[name] != expected and not args.backup_conflicts:
                conflicts.append(f"{name}: local edits differ from the managed hash; review before --backup-conflicts")
    plan = {**selection, "changed": changed, "removed": removed,
            "unchanged": len(names) - len(changed), "conflicts": conflicts,
            "destinations": {name: str(destination_for(name, args)) for name in names}}
    if args.dry_run:
        print(json.dumps(plan, indent=2))
        return 1 if conflicts else 0
    if conflicts:
        raise ToolkitError("\n".join(conflicts))
    new_state = {"schema_version": 2, "package": PACKAGE_NAME, "version": package_version(),
                 "harness": args.harness, "profile": selection["profile"],
                 "requested_packs": args.pack if args.pack is not None else (state or {}).get("requested_packs", []),
                 "packs": selection["packs"], "external": selection["external"],
                 "mode": "link" if args.link else "copy", "skills": desired}
    comparable = {key: value for key, value in (state or {}).items()
                  if key not in {"installed_at", "last_backup"}}
    if not changed and not removed and new_state == comparable:
        print(f"Installed {len(names)} managed skills (0 changed); already current.")
        return 0
    control_root.mkdir(parents=True, exist_ok=True)
    lock_path = control_root / "operation.lock"
    try:
        lock_fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise ToolkitError(f"another install is active, or a prior process stopped: inspect {lock_path}") from exc
    os.close(lock_fd)
    stage_root = control_root / f"stage-{uuid.uuid4().hex}"
    backup_path = control_root / "backups" / f"{utc_stamp()}-{uuid.uuid4().hex[:8]}"
    moved: list[str] = []
    installed: list[str] = []
    try:
        checked_path(control_root, backup_path.relative_to(control_root))
        stage_root.mkdir()
        for name in changed:
            copy_or_link(SKILLS_ROOT / name, stage_root / name, args.link)
            if not args.link and tree_digest(stage_root / name)[0] != desired[name]["sha256"]:
                raise ToolkitError(f"staged content changed: {name}")
        if (state_path.read_bytes() if state_path.exists() else None) != state_bytes:
            raise ToolkitError("managed state changed during preparation; retry after inspecting it")
        for name, path in previous_paths.items():
            if installed_digest(path) != fingerprints[name]:
                raise ToolkitError(f"installed content changed during preparation: {name}")
        replaced = [name for name in changed + removed if fingerprints[name] is not None]
        created = [name for name in changed if name not in replaced]
        backup_path.mkdir(parents=True)
        # Record placement as a boolean, never accept an arbitrary restore path.
        write_json_atomic(backup_path / "backup.json", {
            "schema_version": 2, "replaced": replaced, "created": created,
            "before_placements": {name: {"native": previous_paths[name] != _skills_root / name} for name in replaced},
            "after_placements": {name: desired[name] for name in changed},
            "state_before": state})
        recovery = control_root / "failed-installs" / uuid.uuid4().hex
        checked_path(control_root, recovery.relative_to(control_root))
        recovery.mkdir(parents=True)
        try:
            for name in replaced:
                os.replace(previous_paths[name], backup_path / name)
                moved.append(name)
            for name in changed:
                destination = destination_for(name, args)
                destination.parent.mkdir(parents=True, exist_ok=True)
                os.replace(stage_root / name, destination)
                installed.append(name)
            new_state.update(installed_at=datetime.now(timezone.utc).isoformat(), last_backup=str(backup_path))
            write_json_atomic(state_path, new_state)
        except Exception:
            for name in reversed(installed):
                os.replace(destination_for(name, args), recovery / name)
            for name in reversed(moved):
                os.replace(backup_path / name, previous_paths[name])
            raise
    finally:
        if stage_root.exists():
            shutil.rmtree(stage_root)
        lock_path.unlink()
    print(f"Installed {len(names)} managed skills ({len(changed)} changed, {len(removed)} removed).")
    print(f"Recoverable backup: {backup_path}")
    if selection["external"]:
        print("External dependencies are declared, not installed or authenticated: " + ", ".join(selection["external"]))
    return 0


def command_upgrade(args: argparse.Namespace) -> int:
    _destination_root, state_path, _control_root = target_paths(args)
    if not state_path.exists():
        raise ToolkitError(f"upgrade requires an existing managed installation at {state_path}; use install first")
    return command_install(args)


def command_rollback(args: argparse.Namespace) -> int:
    destination_root, state_path, control_root = target_paths(args)
    state = read_optional_state(state_path)
    if not state:
        raise ToolkitError(f"no managed installation state at {state_path}")
    args.harness = args.harness or state.get("harness", "agent-skills")
    if args.harness != state.get("harness", args.harness):
        raise ToolkitError("rollback harness does not match installed state")
    raw_backup = state.get("last_backup")
    if not raw_backup:
        raise ToolkitError("the managed installation has no prior backup")
    backup_path = Path(str(raw_backup))
    allowed_backups = checked_path(control_root, Path("backups"))
    if not backup_path.is_absolute() or ".." in backup_path.parts or allowed_backups not in backup_path.parents:
        raise ToolkitError("state references a backup outside the managed backup root")
    checked_path(allowed_backups, backup_path.relative_to(allowed_backups) / "backup.json")
    record = load_json(backup_path / "backup.json")
    replaced, created = record.get("replaced"), record.get("created")
    if not isinstance(replaced, list) or not isinstance(created, list):
        raise ToolkitError("invalid backup record")
    affected = replaced + created
    for name in affected:
        safe_name(name)
    if len(affected) != len(set(affected)):
        raise ToolkitError("duplicate names in backup record")
    before = record.get("before_placements", {})
    after = record.get("after_placements", {})
    old_paths = {name: destination_for(name, args, before.get(name, {})) for name in replaced}
    current_paths = {name: destination_for(name, args, after.get(name, state["skills"].get(name, before.get(name, {})))) for name in affected}
    for name in replaced:
        if not exists(backup_path / name):
            raise ToolkitError(f"backup is incomplete: missing {name}")
        if old_paths[name] != current_paths[name] and exists(old_paths[name]):
            raise ToolkitError(f"rollback destination is occupied: {name}")
    lock_path = control_root / "operation.lock"
    try:
        lock_fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise ToolkitError(f"another managed operation is active: {lock_path}") from exc
    os.close(lock_fd)
    displaced = control_root / "displaced" / f"{utc_stamp()}-{uuid.uuid4().hex[:8]}"
    moved, restored = [], []
    try:
        checked_path(control_root, displaced.relative_to(control_root))
        displaced.mkdir(parents=True)
        for name, current in current_paths.items():
            if exists(current):
                os.replace(current, displaced / name)
                moved.append(name)
        for name in replaced:
            old_paths[name].parent.mkdir(parents=True, exist_ok=True)
            os.replace(backup_path / name, old_paths[name])
            restored.append(name)
        previous_state = record.get("state_before")
        if previous_state is None:
            os.replace(state_path, displaced / state_path.name)
        else:
            write_json_atomic(state_path, previous_state)
    except Exception:
        for name in reversed(restored):
            os.replace(old_paths[name], backup_path / name)
        for name in reversed(moved):
            os.replace(displaced / name, current_paths[name])
        raise
    finally:
        lock_path.unlink()
    print(f"Restored the prior managed state. Displaced current files are in {displaced}.")
    return 0


def archive_files(paths: Iterable[tuple[Path, str]], destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for source, archive_name in sorted(paths, key=lambda item: item[1]):
            info = zipfile.ZipInfo(archive_name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o100755 if source.stat().st_mode & 0o111 else 0o100644) << 16
            archive.writestr(info, source.read_bytes())


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def iter_archive_tree(source_root: Path, prefix: str) -> Iterable[tuple[Path, str]]:
    for path in source_root.rglob("*"):
        relative = path.relative_to(source_root)
        if path.is_file() and not path.is_symlink() and not should_ignore(relative):
            yield path, f"{prefix}/{relative.as_posix()}"


def release_receipt(selection: dict[str, Any]) -> dict[str, Any]:
    lock = load_json(LOCK_PATH)
    return {"schema_version": 1, "package": PACKAGE_NAME, "version": package_version(),
            "selection": selection,
            "skills": {name: lock["skills"][name] for name in selection["skills"]},
            "dependencies": {name: load_json(CATALOG_PATH)["dependencies"][name]
                             for name in selection["external"]}}


def command_package(args: argparse.Namespace) -> int:
    if structural_errors(check_lock=True):
        raise ToolkitError("bundle verification failed; run toolkit.py verify")
    output = Path(args.output or (ROOT / "dist")).expanduser().resolve()
    output.mkdir(parents=True, exist_ok=True)
    version = package_version()
    portable_archive = output / f"{PACKAGE_NAME}-agent-plugin-{version}.zip"
    codex_archive = output / f"{PACKAGE_NAME}-codex-marketplace-{version}.zip"
    portable_selection = resolve_selection(args.harness or "agent-skills", args.profile or "core", args.pack or [])
    codex_selection = resolve_selection("codex", args.profile or "core", args.pack or [])
    with tempfile.TemporaryDirectory(prefix="toolkit-release-") as temporary:
        temp = Path(temporary)
        portable = temp / "portable" / PACKAGE_NAME
        portable.mkdir(parents=True)
        shutil.copy2(PORTABLE_MANIFEST, portable / "plugin.json")
        shutil.copy2(ROOT / "LICENSE", portable / "LICENSE")
        for name in portable_selection["skills"]:
            shutil.copytree(SKILLS_ROOT / name, portable / "skills" / name)
        write_json_atomic(portable / "release-selection.json", release_receipt(portable_selection))
        archive_files(iter_archive_tree(portable, PACKAGE_NAME), portable_archive)

        # The Codex archive is a self-validating selected source distribution.
        # It retains the installer and provenance, while its plugin exposes only
        # the requested selection (core by default). Use the full repository to
        # add packs absent from a selected release.
        bundle = temp / "codex" / PACKAGE_NAME
        bundle.mkdir(parents=True)
        for name in ("README.md", "AGENTS.md", "CHANGELOG.md", "LICENSE"):
            shutil.copy2(ROOT / name, bundle / name)
        for name in ("scripts", "docs", "tests", "catalog"):
            shutil.copytree(ROOT / name, bundle / name, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        manifest_destination = bundle / ".agents/plugins/marketplace.json"
        manifest_destination.parent.mkdir(parents=True)
        shutil.copy2(MARKETPLACE_MANIFEST, manifest_destination)
        plugin = bundle / "plugins" / PACKAGE_NAME
        plugin.mkdir(parents=True)
        shutil.copy2(PORTABLE_MANIFEST, plugin / "plugin.json")
        (plugin / ".codex-plugin").mkdir()
        shutil.copy2(CODEX_MANIFEST, plugin / ".codex-plugin/plugin.json")
        selected = set(codex_selection["skills"])
        for name in sorted(selected):
            shutil.copytree(SKILLS_ROOT / name, plugin / "skills" / name)
        catalog = load_json(CATALOG_PATH)
        catalog["package"]["distribution_selection"] = codex_selection
        catalog["vendored"] = [entry for entry in catalog["vendored"] if entry["name"] in selected]
        for pack in catalog["packs"].values():
            pack["skills"] = [name for name in pack["skills"] if name in selected]
            pack["external"] = [name for name in pack.get("external", []) if name in codex_selection["external"]]
        catalog["packs"] = {name: pack for name, pack in catalog["packs"].items()
                            if pack["skills"] or pack["external"] or name == "core"}
        catalog["profiles"] = {"core": ["core"], "all": list(catalog["packs"])}
        write_json_atomic(bundle / "catalog/skills.yaml", catalog)
        write_json_atomic(bundle / "release-selection.json", release_receipt(codex_selection))
        for command in ([sys.executable, "scripts/inventory_readme.py", "--write"],
                        [sys.executable, "scripts/toolkit.py", "lock"],
                        [sys.executable, "scripts/toolkit.py", "verify"]):
            result = subprocess.run(command, cwd=bundle, capture_output=True, text=True, check=False)
            if result.returncode:
                raise ToolkitError("selected release validation failed: " + result.stderr.strip())
        archive_files(iter_archive_tree(bundle, PACKAGE_NAME), codex_archive)
    checksums = output / "SHA256SUMS"
    checksums.write_text("".join(f"{file_sha256(path)}  {path.name}\n"
                                  for path in (portable_archive, codex_archive)), encoding="utf-8")
    print(f"Created {portable_archive} ({len(portable_selection['skills'])} selected skills)")
    print(f"Created {codex_archive} ({len(codex_selection['skills'])} selected skills)")
    print(f"Created {checksums}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("inventory", help="summarize vendored and external capabilities")
    subparsers.add_parser("lock", help="regenerate deterministic skill content hashes")
    subparsers.add_parser("verify", help="validate manifests, skills, paths, and hashes")
    subparsers.add_parser("doctor", help="report bundle and local harness readiness")

    def selection_options(subparser: argparse.ArgumentParser) -> None:
        subparser.add_argument("--harness", help="receiving harness; defaults to agent-skills or installed state")
        subparser.add_argument("--profile", help="core by default; all explicitly selects every compatible pack")
        subparser.add_argument("--pack", action="append", help="optional pack; repeat to combine packs")

    selection_parser = subparsers.add_parser("select", help="show resolved skills, native exclusions and external dependencies without installing")
    selection_options(selection_parser)

    for name in ("install", "upgrade", "rollback"):
        subparser = subparsers.add_parser(name)
        subparser.add_argument("--target", choices=("project", "user"), default="project")
        subparser.add_argument("--project-root")
        if name in {"install", "upgrade"}:
            selection_options(subparser)
            subparser.add_argument("--dry-run", action="store_true")
            subparser.add_argument("--adopt-identical", action="store_true", help="manage exact existing copies after comparing every file")
            subparser.add_argument("--backup-conflicts", action="store_true", help="explicitly replace differing copies after review, retaining a recoverable backup")
            subparser.add_argument("--link", action="store_true", help="development-only symlink install")
        else:
            subparser.add_argument("--harness")

    package_parser = subparsers.add_parser("package", help="build portable and Codex release archives")
    package_parser.add_argument("--output")
    selection_options(package_parser)
    resources_parser = subparsers.add_parser("resources", help="import the complete optional OpenDesign library from pinned local Git objects")
    resources_parser.add_argument("--source", required=True)
    resources_parser.add_argument("--destination", required=True)
    resources_parser.add_argument("--dry-run", action="store_true")
    resources_parser.add_argument("--backup-conflicts", action="store_true")
    return parser


COMMANDS = {
    "inventory": command_inventory,
    "lock": command_lock,
    "verify": command_verify,
    "doctor": command_doctor,
    "select": command_select,
    "resources": command_resources,
    "install": command_install,
    "upgrade": command_upgrade,
    "rollback": command_rollback,
    "package": command_package,
}


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return COMMANDS[args.command](args)
    except (ToolkitError, OSError, tarfile.TarError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
