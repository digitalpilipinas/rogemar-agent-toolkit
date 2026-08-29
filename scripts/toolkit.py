#!/usr/bin/env python3
"""Verify, install, diagnose, roll back, and package Rogemar Agent Toolkit."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
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
IGNORED_PARTS = {"__pycache__", ".DS_Store"}
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


def tree_digest(skill_dir: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    files = skill_files(skill_dir)
    for path in files:
        relative = path.relative_to(skill_dir).as_posix().encode("utf-8")
        digest.update(relative)
        digest.update(b"\0")
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
        "schema_version": 1,
        "package": PACKAGE_NAME,
        "version": package_version(),
        "skills": skills,
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


def target_paths(args: argparse.Namespace) -> tuple[Path, Path, Path]:
    if args.target == "project":
        root = Path(args.project_root or Path.cwd()).expanduser().resolve()
        agents_root = root / ".agents"
        return (
            agents_root / "skills",
            agents_root / f"{PACKAGE_NAME}.lock.json",
            agents_root / f".{PACKAGE_NAME}",
        )
    agents_root = Path.home() / ".agents"
    return (
        agents_root / "skills",
        agents_root / f"{PACKAGE_NAME}.lock.json",
        agents_root / f".{PACKAGE_NAME}",
    )


def read_optional_state(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return load_json(path)


def copy_or_link(source: Path, destination: Path, link: bool) -> None:
    if link:
        destination.symlink_to(source, target_is_directory=True)
    else:
        shutil.copytree(source, destination, symlinks=False)


def command_install(args: argparse.Namespace) -> int:
    errors = structural_errors(check_lock=True)
    if errors:
        raise ToolkitError("bundle verification failed; run toolkit.py verify")
    destination_root, state_path, control_root = target_paths(args)
    state = read_optional_state(state_path)
    managed = set(state.get("skills", {}).keys()) if state else set()
    names = vendored_names()
    conflicts = [
        name
        for name in names
        if ((destination_root / name).exists() or (destination_root / name).is_symlink())
        and name not in managed
    ]
    if conflicts:
        raise ToolkitError(
            "refusing to overwrite unmanaged skill directories: " + ", ".join(conflicts)
        )

    destination_root.mkdir(parents=True, exist_ok=True)
    control_root.mkdir(parents=True, exist_ok=True)
    stage_root = control_root / f"stage-{uuid.uuid4().hex}"
    stage_root.mkdir()
    changed: list[str] = []
    try:
        for name in names:
            source = SKILLS_ROOT / name
            destination = destination_root / name
            if destination.exists() and not destination.is_symlink():
                source_digest, _ = tree_digest(source)
                destination_digest, _ = tree_digest(destination)
                if not args.link and source_digest == destination_digest:
                    continue
            copy_or_link(source, stage_root / name, args.link)
            changed.append(name)

        backup_path: Path | None = None
        backup_record: dict[str, Any] | None = None
        if changed and any((destination_root / name).exists() or (destination_root / name).is_symlink() for name in changed):
            backup_path = control_root / "backups" / f"{utc_stamp()}-{uuid.uuid4().hex[:8]}"
            backup_path.mkdir(parents=True)
            replaced = [
                name
                for name in changed
                if (destination_root / name).exists()
                or (destination_root / name).is_symlink()
            ]
            created = [name for name in changed if name not in replaced]
            backup_record = {
                "schema_version": 1,
                "replaced": replaced,
                "created": created,
                "state_before": state,
            }
            write_json_atomic(backup_path / "backup.json", backup_record)
            moved: list[str] = []
            try:
                for name in replaced:
                    os.replace(destination_root / name, backup_path / name)
                    moved.append(name)
            except Exception:
                for name in reversed(moved):
                    os.replace(backup_path / name, destination_root / name)
                raise

        installed: list[str] = []
        try:
            for name in changed:
                os.replace(stage_root / name, destination_root / name)
                installed.append(name)
        except Exception:
            recovery = control_root / "failed-installs" / f"{utc_stamp()}-{uuid.uuid4().hex[:8]}"
            recovery.mkdir(parents=True)
            for name in installed:
                current = destination_root / name
                if current.exists() or current.is_symlink():
                    os.replace(current, recovery / name)
            if backup_path and backup_record:
                for name in backup_record["replaced"]:
                    os.replace(backup_path / name, destination_root / name)
            raise

        skills_state: dict[str, Any] = {}
        for name in names:
            digest, file_count = tree_digest(SKILLS_ROOT / name)
            skills_state[name] = {"sha256": digest, "file_count": file_count}
        new_state = {
            "schema_version": 1,
            "package": PACKAGE_NAME,
            "version": package_version(),
            "profile": args.profile,
            "installed_at": datetime.now(timezone.utc).isoformat(),
            "mode": "link" if args.link else "copy",
            "skills": skills_state,
            "last_backup": str(backup_path) if backup_path else (state or {}).get("last_backup"),
        }
        write_json_atomic(state_path, new_state)
    finally:
        if stage_root.exists():
            shutil.rmtree(stage_root)

    print(
        f"Installed {len(names)} managed skills ({len(changed)} changed) into {destination_root}."
    )
    if new_state.get("last_backup"):
        print(f"Recoverable backup: {new_state['last_backup']}")
    return 0


def command_upgrade(args: argparse.Namespace) -> int:
    _destination_root, state_path, _control_root = target_paths(args)
    if not state_path.exists():
        raise ToolkitError(
            f"upgrade requires an existing managed installation at {state_path}; use install first"
        )
    return command_install(args)


def command_rollback(args: argparse.Namespace) -> int:
    destination_root, state_path, control_root = target_paths(args)
    state = read_optional_state(state_path)
    if not state:
        raise ToolkitError(f"no managed installation state at {state_path}")
    raw_backup = state.get("last_backup")
    if not raw_backup:
        raise ToolkitError("the managed installation has no prior backup")
    backup_path = Path(str(raw_backup)).resolve()
    allowed_backups = (control_root / "backups").resolve()
    if allowed_backups not in backup_path.parents:
        raise ToolkitError("state references a backup outside the managed backup root")
    backup_record = load_json(backup_path / "backup.json")
    replaced = backup_record.get("replaced", [])
    created = backup_record.get("created", [])
    if not isinstance(replaced, list) or not isinstance(created, list):
        raise ToolkitError("invalid backup record")
    missing = [
        str(name)
        for name in replaced
        if not (backup_path / str(name)).exists()
        and not (backup_path / str(name)).is_symlink()
    ]
    if missing:
        raise ToolkitError(f"backup is incomplete: missing {', '.join(missing)}")

    displaced = control_root / "displaced" / f"{utc_stamp()}-{uuid.uuid4().hex[:8]}"
    displaced.mkdir(parents=True)
    for name in [*replaced, *created]:
        current = destination_root / str(name)
        if current.exists() or current.is_symlink():
            os.replace(current, displaced / str(name))
    for name in replaced:
        previous = backup_path / str(name)
        os.replace(previous, destination_root / str(name))

    previous_state = backup_record.get("state_before")
    if previous_state is None:
        os.replace(state_path, displaced / state_path.name)
    else:
        write_json_atomic(state_path, previous_state)
    print(f"Restored the prior managed state. Displaced current files are in {displaced}.")
    return 0


def archive_files(paths: Iterable[tuple[Path, str]], destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for source, archive_name in sorted(paths, key=lambda item: item[1]):
            info = zipfile.ZipInfo(archive_name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
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


def command_package(args: argparse.Namespace) -> int:
    if structural_errors(check_lock=True):
        raise ToolkitError("bundle verification failed; run toolkit.py verify")
    output = Path(args.output or (ROOT / "dist")).expanduser().resolve()
    output.mkdir(parents=True, exist_ok=True)
    version = package_version()
    portable_archive = output / f"{PACKAGE_NAME}-agent-plugin-{version}.zip"
    codex_archive = output / f"{PACKAGE_NAME}-codex-marketplace-{version}.zip"

    archive_files(iter_archive_tree(PLUGIN_ROOT, PACKAGE_NAME), portable_archive)
    codex_sources: list[tuple[Path, str]] = []
    for path in (
        ROOT / ".agents" / "plugins" / "marketplace.json",
        ROOT / "README.md",
        ROOT / "AGENTS.md",
        ROOT / "CHANGELOG.md",
        ROOT / "LICENSE",
        CATALOG_PATH,
        LOCK_PATH,
    ):
        codex_sources.append((path, f"{PACKAGE_NAME}/{path.relative_to(ROOT).as_posix()}"))
    codex_sources.extend(
        iter_archive_tree(PLUGIN_ROOT, f"{PACKAGE_NAME}/plugins/{PACKAGE_NAME}")
    )
    codex_sources.extend(iter_archive_tree(ROOT / "docs", f"{PACKAGE_NAME}/docs"))
    codex_sources.extend(iter_archive_tree(ROOT / "scripts", f"{PACKAGE_NAME}/scripts"))
    codex_sources.extend(iter_archive_tree(ROOT / "tests", f"{PACKAGE_NAME}/tests"))
    archive_files(codex_sources, codex_archive)
    checksums = output / "SHA256SUMS"
    checksums.write_text(
        "".join(
            f"{file_sha256(path)}  {path.name}\n"
            for path in (portable_archive, codex_archive)
        ),
        encoding="utf-8",
    )
    print(f"Created {portable_archive}")
    print(f"Created {codex_archive}")
    print(f"Created {checksums}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("inventory", help="summarize vendored and external capabilities")
    subparsers.add_parser("lock", help="regenerate deterministic skill content hashes")
    subparsers.add_parser("verify", help="validate manifests, skills, paths, and hashes")
    subparsers.add_parser("doctor", help="report bundle and local harness readiness")

    for name in ("install", "upgrade", "rollback"):
        subparser = subparsers.add_parser(name)
        subparser.add_argument("--target", choices=("project", "user"), default="project")
        subparser.add_argument("--project-root")
        if name in {"install", "upgrade"}:
            subparser.add_argument("--profile", choices=("all",), default="all")
            subparser.add_argument("--link", action="store_true", help="development-only symlink install")

    package_parser = subparsers.add_parser("package", help="build portable and Codex release archives")
    package_parser.add_argument("--output")
    return parser


COMMANDS = {
    "inventory": command_inventory,
    "lock": command_lock,
    "verify": command_verify,
    "doctor": command_doctor,
    "install": command_install,
    "upgrade": command_upgrade,
    "rollback": command_rollback,
    "package": command_package,
}


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return COMMANDS[args.command](args)
    except ToolkitError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
