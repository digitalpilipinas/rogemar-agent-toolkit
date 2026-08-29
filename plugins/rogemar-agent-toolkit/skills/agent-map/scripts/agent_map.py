#!/usr/bin/env python3
"""Build and query a small, local repository navigation map.

The script deliberately uses only the Python standard library. It stores metadata,
symbols, imports, and line locators; it never stores source bodies or calls a
network service. It is a locator, not a replacement for reading current source.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator


SCHEMA = 2
PARSER_VERSION = "1.0"
DEFAULT_OUTPUT = ".agent-map"
MAX_FILES = 20000
MAX_REFERENCES_PER_SYMBOL = 20
MAX_FIND_RESULTS = 30
MAX_OUTPUT_LINES = 120

SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "vendor",
    "dist",
    "build",
    "out",
    "target",
    "coverage",
    ".next",
    ".nuxt",
    ".gradle",
    "Pods",
    "__pycache__",
    ".venv",
    "venv",
}
SECRET_BASENAMES = {
    ".env",
    ".env.local",
    ".env.production",
    ".env.development",
}
SECRET_SUFFIXES = (".pem", ".key", ".p12", ".pfx", ".crt")

EXTENSIONS = {
    ".ts": "typescript",
    ".tsx": "typescript",
    ".mts": "typescript",
    ".cts": "typescript",
    ".js": "javascript",
    ".jsx": "javascript",
    ".mjs": "javascript",
    ".cjs": "javascript",
    ".py": "python",
    ".pyi": "python",
    ".go": "go",
    ".java": "java",
    ".rs": "rust",
    ".c": "c",
    ".h": "c",
    ".cc": "cpp",
    ".cpp": "cpp",
    ".cxx": "cpp",
    ".hh": "cpp",
    ".hpp": "cpp",
    ".cs": "csharp",
    ".rb": "ruby",
    ".php": "php",
    ".kt": "kotlin",
    ".kts": "kotlin",
    ".swift": "swift",
    ".scala": "scala",
    ".ex": "elixir",
    ".exs": "elixir",
    ".sol": "solidity",
    ".ml": "ocaml",
    ".mli": "ocaml",
    ".zig": "zig",
    ".dart": "dart",
    ".sh": "shell",
    ".bash": "shell",
    ".zsh": "shell",
    ".fish": "shell",
    ".sql": "sql",
    ".md": "markdown",
    ".mdx": "markdown",
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".toml": "toml",
    ".xml": "xml",
    ".html": "html",
    ".htm": "html",
    ".css": "css",
    ".scss": "css",
    ".vue": "vue",
    ".svelte": "svelte",
    ".proto": "protobuf",
}

DECLARATION_PATTERNS = {
    "typescript": re.compile(
        r"^\s*(?:export\s+)?(?:default\s+)?(?:async\s+)?"
        r"(function|class|interface|type|enum|namespace)\s+([A-Za-z_$][\w$]*)"
        r"|^\s*(?:export\s+)?(?:const|let|var)\s+([A-Za-z_$][\w$]*)"
    ),
    "javascript": re.compile(
        r"^\s*(?:export\s+)?(?:default\s+)?(?:async\s+)?"
        r"(function|class)\s+([A-Za-z_$][\w$]*)"
        r"|^\s*(?:export\s+)?(?:const|let|var)\s+([A-Za-z_$][\w$]*)"
    ),
    "python": re.compile(r"^\s*(async\s+def|def|class)\s+([A-Za-z_]\w*)"),
    "go": re.compile(r"^\s*(func|type|var|const)\s+([A-Za-z_]\w*)"),
    "java": re.compile(
        r"^\s*(?:public\s+|private\s+|protected\s+|abstract\s+|final\s+|static\s+)*"
        r"(class|interface|enum|record)\s+([A-Za-z_]\w*)"
    ),
    "csharp": re.compile(
        r"^\s*(?:public\s+|private\s+|protected\s+|internal\s+|abstract\s+|sealed\s+|static\s+)*"
        r"(class|interface|struct|enum|record)\s+([A-Za-z_]\w*)"
    ),
    "rust": re.compile(r"^\s*(?:pub\s+)?(fn|struct|enum|trait|mod|type)\s+([A-Za-z_]\w*)"),
    "ruby": re.compile(r"^\s*(class|module|def)\s+([A-Za-z_][\w!?=]*)"),
    "php": re.compile(r"^\s*(?:abstract\s+|final\s+)?(class|interface|trait|function)\s+([A-Za-z_]\w*)"),
    "kotlin": re.compile(r"^\s*(?:public\s+|private\s+|internal\s+|protected\s+)?(?:data\s+)?(class|object|interface|fun|typealias)\s+([A-Za-z_]\w*)"),
    "swift": re.compile(r"^\s*(?:public\s+|private\s+|internal\s+|fileprivate\s+|open\s+)*(class|struct|enum|protocol|func)\s+([A-Za-z_]\w*)"),
    "scala": re.compile(r"^\s*(class|object|trait|def|type)\s+([A-Za-z_]\w*)"),
    "generic": re.compile(r"^\s*(?:export\s+)?(function|class|struct|interface|enum|module|def|fn)\s+([A-Za-z_]\w*)"),
}

IMPORT_PATTERNS = [
    re.compile(r"^\s*import\s+(?:.+?\s+from\s+)?[\"']([^\"']+)[\"']"),
    re.compile(r"^\s*export\s+.+?\s+from\s+[\"']([^\"']+)[\"']"),
    re.compile(r"\brequire\(\s*[\"']([^\"']+)[\"']\s*\)"),
    re.compile(r"^\s*from\s+([A-Za-z0-9_./-]+)\s+import\b"),
    re.compile(r"^\s*#include\s*[<\"]([^>\"]+)[>\"]"),
    re.compile(r"^\s*using\s+([A-Za-z0-9_.]+)\s*;"),
]
WORD_RE = re.compile(r"\b[A-Za-z_$][A-Za-z0-9_$!?=]*\b")


@dataclass
class RepoState:
    root: Path
    branch: str
    head: str
    dirty: bool


def run_git(root: Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return ""
    return result.stdout.strip()


def repo_state(root: Path) -> RepoState:
    branch = run_git(root, "branch", "--show-current") or "(detached/non-git)"
    head = run_git(root, "rev-parse", "HEAD") or "(no-commit)"
    # Ignore untracked generated output such as .agent-map/. Source changes are
    # still detected by the manifest's file hashes during status().
    dirty = bool(run_git(root, "status", "--porcelain=v1", "--untracked-files=no"))
    return RepoState(root=root, branch=branch, head=head, dirty=dirty)


def is_secret(path: Path) -> bool:
    name = path.name.lower()
    return name in SECRET_BASENAMES or name.endswith(SECRET_SUFFIXES)


def is_skipped(path: Path, root: Path, output: Path) -> bool:
    try:
        path.relative_to(output)
        return True
    except ValueError:
        pass
    if is_secret(path):
        return True
    try:
        rel_parts = path.relative_to(root).parts
    except ValueError:
        return True
    return any(part in SKIP_DIRS or part.startswith(".env.") for part in rel_parts)


def candidate_paths(root: Path, output: Path) -> list[Path]:
    git_files = run_git(root, "ls-files", "--cached", "--others", "--exclude-standard")
    if git_files:
        candidates = (root / line for line in git_files.splitlines() if line)
    else:
        candidates = (p for p in root.rglob("*") if p.is_file())
    return [path for path in candidates if path.is_file() and not is_skipped(path, root, output)]


def iter_files(root: Path, output: Path) -> Iterator[Path]:
    count = 0
    for path in candidate_paths(root, output):
        if count >= MAX_FILES:
            break
        if path.suffix.lower() not in EXTENSIONS:
            continue
        try:
            path.stat()
        except OSError:
            continue
        count += 1
        yield path


def coverage_summary(root: Path, output: Path) -> dict:
    candidates = candidate_paths(root, output)
    unsupported = Counter(path.suffix.lower() or "(no extension)" for path in candidates if path.suffix.lower() not in EXTENSIONS)
    supported_count = len(candidates) - sum(unsupported.values())
    return {
        "candidate_files": len(candidates),
        "indexed_files": min(supported_count, MAX_FILES),
        "unsupported_files": sum(unsupported.values()),
        "unsupported_extensions": dict(unsupported.most_common(20)),
        "max_files": MAX_FILES,
        "truncated": supported_count > MAX_FILES,
    }


def rel_path(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def declaration_name(match: re.Match[str]) -> tuple[str, str] | None:
    groups = match.groups()
    if len(groups) == 2:
        return groups[0], groups[1]
    if len(groups) >= 3:
        kind = groups[0] or "value"
        name = groups[1] or groups[2]
        return kind, name
    return None


def estimate_end(lines: list[str], start: int, language: str) -> int:
    """Estimate a useful span without claiming parser-grade boundaries."""
    first = lines[start - 1]
    if language == "python":
        indent = len(first) - len(first.lstrip())
        end = start
        for index in range(start, len(lines)):
            line = lines[index]
            if line.strip() and len(line) - len(line.lstrip()) <= indent:
                break
            end = index + 1
        return end
    depth = first.count("{") - first.count("}")
    if depth <= 0:
        return start
    end = start
    for index in range(start, len(lines)):
        depth += lines[index].count("{") - lines[index].count("}")
        end = index + 1
        if depth <= 0:
            break
    return end


def declaration_signature(line: str, kind: str, name: str) -> str:
    """Keep a locator signature without copying initializer/body text."""
    stripped = line.strip()
    if kind == "value":
        keyword = next((item for item in ("const", "let", "var") if re.search(rf"\b{item}\b", stripped)), "value")
        return f"{keyword} {name}"
    if "{" in stripped:
        stripped = stripped.split("{", 1)[0].rstrip()
    if kind in {"function", "def", "async def", "fn", "fun", "method"} and "=" in stripped:
        stripped = stripped.split("=", 1)[0].rstrip()
    return stripped[:160]


def extract_symbols(text: str, language: str) -> list[dict]:
    lines = text.splitlines()
    pattern = DECLARATION_PATTERNS.get(language, DECLARATION_PATTERNS["generic"])
    symbols: list[dict] = []
    for number, line in enumerate(lines, start=1):
        match = pattern.search(line)
        if not match:
            continue
        parsed = declaration_name(match)
        if not parsed:
            continue
        kind, name = parsed
        if not name or name in {"if", "for", "while", "switch"}:
            continue
        symbols.append(
            {
                "name": name,
                "kind": kind,
                "start": number,
                "end": estimate_end(lines, number, language),
                "signature": declaration_signature(line, kind, name),
            }
        )
    return symbols


def extract_imports(text: str) -> list[dict]:
    imports: list[dict] = []
    seen: set[tuple[str, int]] = set()
    for number, line in enumerate(text.splitlines(), start=1):
        for pattern in IMPORT_PATTERNS:
            match = pattern.search(line)
            if not match:
                continue
            value = match.group(1)
            key = (value, number)
            if key not in seen:
                imports.append({"value": value, "line": number})
                seen.add(key)
            break
    return imports


def resolve_import(root: Path, source: str, value: str) -> str | None:
    if not value.startswith(".") and not value.startswith("/"):
        return None
    base = (root / source).parent
    candidate = (base / value).resolve()
    possibilities = [candidate]
    code_exts = [
        ".ts", ".tsx", ".mts", ".cts", ".js", ".jsx", ".mjs", ".cjs",
        ".py", ".go", ".java", ".rs", ".rb", ".php", ".kt", ".swift",
    ]
    if candidate.suffix in {".js", ".jsx", ".mjs", ".cjs"}:
        possibilities.extend(candidate.with_suffix(ext) for ext in code_exts)
    elif not candidate.suffix:
        possibilities.extend(candidate.with_suffix(ext) for ext in code_exts)
        possibilities.extend(candidate / f"index{ext}" for ext in code_exts)
    for item in possibilities:
        if item.is_file():
            try:
                return item.relative_to(root.resolve()).as_posix()
            except ValueError:
                continue
    return None


def load_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def output_dir(root: Path, raw: str | None) -> Path:
    candidate = Path(raw) if raw else Path(DEFAULT_OUTPUT)
    return (candidate if candidate.is_absolute() else root / candidate).resolve()


def file_records(root: Path, output: Path, old: dict, full: bool) -> tuple[dict, int, int]:
    records: dict = {}
    changed = 0
    reused = 0
    for path in iter_files(root, output):
        relative = rel_path(path, root)
        try:
            digest = sha256_file(path)
            stat = path.stat()
        except OSError:
            continue
        prior = old.get(relative)
        if not full and prior and prior.get("sha256") == digest and prior.get("parser") == PARSER_VERSION:
            reused_record = dict(prior)
            reused_record["bytes"] = stat.st_size
            reused_record["mtime_ns"] = stat.st_mtime_ns
            records[relative] = reused_record
            reused += 1
            continue
        text = read_text(path)
        language = EXTENSIONS.get(path.suffix.lower(), "unknown")
        records[relative] = {
            "path": relative,
            "language": language,
            "bytes": stat.st_size,
            "mtime_ns": stat.st_mtime_ns,
            "sha256": digest,
            "symbols": extract_symbols(text, language),
            "imports": extract_imports(text),
            "test": bool(re.search(r"(^|[/_.-])(test|tests|spec|__tests__)([/_.-]|$)", relative, re.I)),
            "parser": PARSER_VERSION,
        }
        changed += 1
    return records, changed, reused


def build_relationships(root: Path, records: dict) -> dict:
    symbol_defs: dict[str, list[str]] = defaultdict(list)
    for path, record in records.items():
        for symbol in record.get("symbols", []):
            symbol_defs[symbol["name"]].append(path)

    imports: list[dict] = []
    for path, record in records.items():
        for item in record.get("imports", []):
            target = resolve_import(root, path, item["value"])
            imports.append({"from": path, "to": target, "value": item["value"], "line": item["line"]})

    known = set(symbol_defs)
    callers: dict[str, list[dict]] = defaultdict(list)
    # Scan each file once and intersect tokens with known symbols. Avoid a
    # per-symbol regex pass: on large repositories that turns into a quadratic
    # scan and defeats the purpose of a cheap local map refresh.
    for path in records:
        text = read_text(root / path)
        line_number = 1
        next_newline = text.find("\n")
        for match in WORD_RE.finditer(text):
            # Matches are ordered by offset. Advance a single newline cursor
            # instead of calling text.count(..., 0, offset) for every token;
            # the latter makes large files quadratic during a cold rebuild.
            while next_newline != -1 and next_newline < match.start():
                line_number += 1
                next_newline = text.find("\n", next_newline + 1)
            symbol_name = match.group(0)
            if symbol_name not in known:
                continue
            if path in symbol_defs[symbol_name] and len(symbol_defs[symbol_name]) == 1:
                continue
            if len(callers[symbol_name]) >= MAX_REFERENCES_PER_SYMBOL:
                continue
            callers[symbol_name].append({"path": path, "line": line_number})
    return {
        "definitions": {key: sorted(value) for key, value in sorted(symbol_defs.items())},
        "imports": imports,
        "callers": {key: value for key, value in sorted(callers.items())},
    }


def top_clusters(records: dict) -> list[dict]:
    clusters: dict[str, dict] = defaultdict(lambda: {"files": 0, "languages": Counter(), "tests": 0, "symbols": []})
    for path, record in records.items():
        parts = Path(path).parts
        cluster_name = parts[0] if len(parts) > 1 else "."
        cluster = clusters[cluster_name]
        cluster["files"] += 1
        cluster["languages"][record["language"]] += 1
        cluster["tests"] += int(record.get("test", False))
        cluster["symbols"].extend(symbol["name"] for symbol in record.get("symbols", []))
    result = []
    for name, value in clusters.items():
        result.append(
            {
                "name": name,
                "files": value["files"],
                "tests": value["tests"],
                "languages": dict(value["languages"].most_common(5)),
                "symbols": value["symbols"][:12],
            }
        )
    return sorted(result, key=lambda item: (-item["files"], item["name"]))


def entry_points(records: dict) -> list[str]:
    names = {"main", "index", "app", "server", "cli", "router", "routes", "bootstrap", "entry", "manage"}
    result = []
    for path in records:
        stem = Path(path).stem.lower()
        if stem in names or Path(path).name.lower() in {"package.json", "pyproject.toml", "go.mod", "cargo.toml"}:
            result.append(path)
    return sorted(result)[:30]


def hub_files(records: dict, relationships: dict) -> list[dict]:
    inbound = Counter(item["to"] for item in relationships["imports"] if item.get("to"))
    return [{"path": path, "inbound_imports": count} for path, count in inbound.most_common(20) if path in records]


def build_index(root: Path, state: RepoState, records: dict, relationships: dict, coverage: dict, changed: int, reused: int) -> str:
    clusters = top_clusters(records)
    entries = entry_points(records)
    hubs = hub_files(records, relationships)
    languages = Counter(record["language"] for record in records.values())
    lines = [
        "# Agent Map",
        "",
        f"- Status: `fresh after refresh` (changed {changed}, reused {reused})",
        f"- Branch: `{state.branch}`",
        f"- HEAD: `{state.head[:12]}`",
        f"- Working tree: `{'dirty' if state.dirty else 'clean'}`",
        f"- Files: `{len(records)}` | Symbols: `{sum(len(r.get('symbols', [])) for r in records.values())}`",
        f"- Languages: {', '.join(f'{name} ({count})' for name, count in languages.most_common(10))}",
        f"- Coverage: `{coverage['indexed_files']}/{coverage['candidate_files']}` candidate files indexed; `{coverage['unsupported_files']}` unsupported; `{'truncated' if coverage['truncated'] else 'complete'}`",
        "",
        "## Directory clusters",
        "",
    ]
    for cluster in clusters[:20]:
        langs = ", ".join(f"{key} {value}" for key, value in cluster["languages"].items())
        symbols = ", ".join(cluster["symbols"][:6]) or "(no declarations detected)"
        lines.append(f"- `{cluster['name']}/` — {cluster['files']} files; {cluster['tests']} test-like; {langs}; symbols: {symbols}")
    lines.extend(["", "## Likely entry points", ""])
    lines.extend(f"- `{path}`" for path in entries[:20])
    if not entries:
        lines.append("- (none detected; inspect project documentation and package metadata)")
    lines.extend(["", "## Import hubs", ""])
    lines.extend(f"- `{item['path']}` — {item['inbound_imports']} inbound imports" for item in hubs[:20])
    if not hubs:
        lines.append("- (none resolved)")
    lines.extend(
        [
            "",
            "## Query guidance",
            "",
            "Use `find` to locate a concept, `skeleton` to inspect a file API, and `callers` before changing a shared symbol. Verify all results against current source.",
            "See `RELATIONSHIPS.md` for a bounded human-readable relationship summary; use the JSON only for scripted queries.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_relationships_report(records: dict, relationships: dict) -> str:
    """Render a small human-readable view instead of requiring a huge JSON file."""
    inbound = Counter(item["to"] for item in relationships.get("imports", []) if item.get("to"))
    caller_counts = Counter({name: len(items) for name, items in relationships.get("callers", {}).items()})
    lines = [
        "# Relationship Summary",
        "",
        "This is a bounded navigation view. Verify every relationship against current source.",
        "Use the bundled `callers` command for a specific symbol; `relationships.json` is machine-readable and may be large.",
        "",
        "## Import hubs",
        "",
    ]
    if inbound:
        for path, count in inbound.most_common(80):
            lines.append(f"- `{path}` — {count} inbound relative imports")
    else:
        lines.append("- (none resolved)")
    lines.extend(["", "## Frequently referenced symbols", ""])
    for name, count in caller_counts.most_common(80):
        definitions = relationships.get("definitions", {}).get(name, [])
        definition = ", ".join(f"`{path}`" for path in definitions[:3]) or "(definition not unique)"
        lines.append(f"- `{name}` — {count} indexed call sites; defined in {definition}")
    if not caller_counts:
        lines.append("- (none detected)")
    lines.extend(["", "## Query examples", "", "```bash", "python3 <skill-dir>/scripts/agent_map.py callers <symbol> --root .", "python3 <skill-dir>/scripts/agent_map.py find \"<concept>\" --root .", "```", ""])
    return "\n".join(lines)


def refresh(root: Path, out: Path, full: bool) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    old_manifest = load_json(out / "manifest.json", {})
    old_records = load_json(out / "files.json", {})
    state = repo_state(root)
    coverage = coverage_summary(root, out)
    compatible = old_manifest.get("schema") == SCHEMA and old_manifest.get("parser") == PARSER_VERSION
    records, changed, reused = file_records(root, out, old_records if compatible else {}, full or not compatible)
    relationships = build_relationships(root, records)
    manifest = {
        "schema": SCHEMA,
        "parser": PARSER_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "branch": state.branch,
        "head": state.head,
        "dirty": state.dirty,
        "file_count": len(records),
        "coverage": coverage,
        "files": {
            path: {
                "sha256": record["sha256"],
                "bytes": record.get("bytes"),
                "mtime_ns": record.get("mtime_ns"),
            }
            for path, record in sorted(records.items())
        },
    }
    write_json(out / "files.json", records)
    write_json(out / "relationships.json", relationships)
    write_json(out / "manifest.json", manifest)
    (out / "INDEX.md").write_text(build_index(root, state, records, relationships, coverage, changed, reused), encoding="utf-8")
    (out / "RELATIONSHIPS.md").write_text(build_relationships_report(records, relationships), encoding="utf-8")
    return {"changed": changed, "reused": reused, "files": len(records), "coverage": coverage, "output": str(out)}


def current_file_state(root: Path, out: Path) -> dict[str, dict]:
    state = {}
    for path in iter_files(root, out):
        try:
            stat = path.stat()
        except OSError:
            continue
        state[rel_path(path, root)] = {"bytes": stat.st_size, "mtime_ns": stat.st_mtime_ns, "path": path}
    return state


def status(root: Path, out: Path, quiet: bool = False, full_hash: bool = False) -> int:
    manifest = load_json(out / "manifest.json", {})
    if not manifest:
        if not quiet:
            print("status: missing (run refresh)")
        return 1
    state = repo_state(root)
    current = current_file_state(root, out)
    expected = manifest.get("files", {})
    reasons = []
    if manifest.get("schema") != SCHEMA or manifest.get("parser") != PARSER_VERSION:
        reasons.append("schema/parser changed")
    if manifest.get("branch") != state.branch or manifest.get("head") != state.head:
        reasons.append("branch or HEAD changed")
    if manifest.get("dirty") != state.dirty:
        reasons.append("working-tree state changed")
    if set(current) != set(expected):
        reasons.append("file set changed")
    else:
        changed_stats = [
            path
            for path, value in current.items()
            if not isinstance(expected[path], dict)
            or value["bytes"] != expected[path].get("bytes")
            or value["mtime_ns"] != expected[path].get("mtime_ns")
        ]
        if changed_stats:
            reasons.append(f"{len(changed_stats)} file(s) changed")
        elif full_hash:
            changed_hashes = [
                path
                for path, value in current.items()
                if sha256_file(value["path"]) != expected[path].get("sha256")
            ]
            if changed_hashes:
                reasons.append(f"{len(changed_hashes)} file(s) content changed")
    if reasons:
        if not quiet:
            print(f"status: stale ({'; '.join(reasons)})")
        return 1
    if not quiet:
        print(f"status: fresh ({len(current)} files; branch {state.branch}; HEAD {state.head[:12]})")
    return 0


def ensure_fresh(root: Path, out: Path) -> None:
    if status(root, out, quiet=True) != 0:
        result = refresh(root, out, full=False)
        print(f"map refreshed: {result['changed']} changed, {result['reused']} reused")


def load_map(out: Path) -> tuple[dict, dict, dict]:
    return (
        load_json(out / "files.json", {}),
        load_json(out / "relationships.json", {"definitions": {}, "imports": [], "callers": {}}),
        load_json(out / "manifest.json", {}),
    )


def command_map(root: Path, out: Path) -> int:
    ensure_fresh(root, out)
    index = out / "INDEX.md"
    try:
        lines = index.read_text(encoding="utf-8").splitlines()
    except OSError:
        print("map: missing INDEX.md; run refresh", file=sys.stderr)
        return 1
    print("\n".join(lines[:MAX_OUTPUT_LINES]))
    return 0


def command_find(root: Path, out: Path, query: str) -> int:
    ensure_fresh(root, out)
    records, relationships, _ = load_map(out)
    needle = query.lower()
    results: list[tuple[int, str]] = []
    for path, record in records.items():
        score = 0
        if needle in path.lower():
            score += 8
        for symbol in record.get("symbols", []):
            if needle in symbol["name"].lower():
                score += 10
        for item in record.get("imports", []):
            if needle in item["value"].lower():
                score += 4
        if score:
            results.append((score, path))
    for item in relationships.get("imports", []):
        if needle in item.get("value", "").lower() and item.get("from"):
            results.append((5, f"{item['from']}:{item['line']} imports {item['value']}"))
    if not results:
        print(f"find: no indexed match for {query!r}; fall back to rg/source search")
        return 0
    seen = set()
    for score, value in sorted(results, key=lambda item: (-item[0], item[1])):
        if value in seen:
            continue
        seen.add(value)
        print(f"{score:>2}  {value}")
        if len(seen) >= MAX_FIND_RESULTS:
            break
    return 0


def command_callers(root: Path, out: Path, symbol: str) -> int:
    ensure_fresh(root, out)
    records, relationships, _ = load_map(out)
    definitions = relationships.get("definitions", {}).get(symbol, [])
    callers = relationships.get("callers", {}).get(symbol, [])
    print(f"symbol: {symbol}")
    print("defined in:")
    for path in definitions:
        print(f"- {path}")
    print("call sites:")
    for item in callers[:MAX_REFERENCES_PER_SYMBOL]:
        if item.get("path") in records:
            print(f"- {item['path']}:{item['line']}")
    if not definitions and not callers:
        print("- no indexed callers; fall back to rg and verify exact spelling")
    return 0


def command_skeleton(root: Path, out: Path, raw_path: str) -> int:
    ensure_fresh(root, out)
    records, _, _ = load_map(out)
    path = Path(raw_path).as_posix()
    record = records.get(path)
    if not record:
        print(f"skeleton: {path} is not indexed; check the path or use rg", file=sys.stderr)
        return 1
    print(f"file: {path} ({record['language']}, {record['bytes']} bytes)")
    for symbol in record.get("symbols", []):
        print(f"- {symbol['kind']} {symbol['name']} L{symbol['start']}-L{symbol['end']}: {symbol['signature']}")
    if not record.get("symbols"):
        print("- no declarations detected; read the file or use language-native tooling")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Local, metadata-only repository map")
    parser.add_argument("command", choices=["status", "refresh", "map", "find", "callers", "skeleton"])
    parser.add_argument("query", nargs="?", help="query, symbol, or relative file path")
    parser.add_argument("--root", default=".", help="repository root (default: current directory)")
    parser.add_argument("--output-dir", default=None, help="map directory relative to root or absolute path")
    parser.add_argument("--full", action="store_true", help="force a complete re-index during refresh")
    parser.add_argument("--full-hash", action="store_true", help="hash every file during status (paranoid mode)")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"root does not exist or is not a directory: {root}", file=sys.stderr)
        return 2
    out = output_dir(root, args.output_dir)
    if args.command == "status":
        return status(root, out, full_hash=args.full_hash)
    if args.command == "refresh":
        result = refresh(root, out, full=args.full)
        print(json.dumps(result, indent=2))
        return 0
    if args.command == "map":
        return command_map(root, out)
    if args.command == "find":
        if not args.query:
            print("find requires a query", file=sys.stderr)
            return 2
        return command_find(root, out, args.query)
    if args.command == "callers":
        if not args.query:
            print("callers requires a symbol", file=sys.stderr)
            return 2
        return command_callers(root, out, args.query)
    if args.command == "skeleton":
        if not args.query:
            print("skeleton requires a relative file path", file=sys.stderr)
            return 2
        return command_skeleton(root, out, args.query)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
