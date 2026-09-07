#!/usr/bin/env python3
"""Read-only validation of a proposed Codex worker profile or Forge preferences."""
from __future__ import annotations

import argparse
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
import sys

MODEL_RANK = {"gpt-5.6-luna": 0, "gpt-5.6-terra": 1, "gpt-5.6-sol": 2, "gpt-6-astra": 3}
EFFORT_RANK = {name: i for i, name in enumerate(("low", "medium", "high", "xhigh", "max", "ultra"))}
ALIASES = {"auto", "inherit-parent"}
ROLES = {
    "feature", "refactoring", "bug-fix", "perf-issue", "hillclimb",
    "judgment and prose", "hardest tasks", "how explorer", "how explainer",
    "how critics", "why investigators", "why synthesizer", "reflect tooling",
    "reflect judgment", "reflect divergent", "reflect synthesizer", "arena runners",
    "arena cross-judge pool", "swarm workers", "architect runners", "interrogate reviewers",
}

LEGACY_ROLES = ROLES
ROLES = {name.replace(" ", "-") for name in LEGACY_ROLES}
# Shared executable catalogue: mode pools, group defaults, role overrides and contracts.
ROUTING_CATALOG = json.loads(Path(__file__).with_name("routing_catalog.json").read_text())
MODE_ALIASES = ROUTING_CATALOG["mode_aliases"]
MODE_PROFILES = ROUTING_CATALOG["modes"]
ROLE_CONTRACTS = ROUTING_CATALOG["roles"]
ROLE_PROFILES = {
    mode: {name: dict(contract.get("overrides", {}).get(mode,
                     ROUTING_CATALOG["groups"][contract["group"]][mode]))
           for name, contract in ROLE_CONTRACTS.items()}
    for mode in MODE_PROFILES
}
ROLES = set(ROLE_CONTRACTS)
MAIN_ROLES = {name for name, contract in ROLE_CONTRACTS.items() if contract["assignment"] == "main-owned"}


def normalize_mode(value):
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError("mode must be a string or null")
    value = value.strip().lower()
    value = MODE_ALIASES.get(value, value)
    if value not in MODE_PROFILES:
        raise ValueError("unknown mode: " + value)
    return value


def effort(value):
    return {"light": "low", "extra high": "xhigh", "extra-high": "xhigh"}.get(value.strip().lower(), value.strip().lower()) if isinstance(value, str) else None


def validate_preferences(value):
    if not isinstance(value, dict):
        raise ValueError("preferences must be a JSON object")
    version = value.get("schema_version")
    if type(version) is not int or version not in (1, 2):
        raise ValueError("unsupported preference schema_version")
    fields = {"schema_version", "policy", "parent_policy", "roles"}
    if version == 2:
        fields.add("active_mode")
    if set(value) != fields:
        raise ValueError("unexpected or missing preference fields")
    if version == 2:
        normalize_mode(value["active_mode"])
    if value["policy"] != "adaptive" or value["parent_policy"] not in ({"suggest-at-phase-boundaries", "mode-adaptive"} if version == 2 else {"suggest-at-phase-boundaries"}):
        raise ValueError("unsupported routing or parent policy")
    if version == 2:
        expected_policy = "mode-adaptive" if value["active_mode"] is not None else "suggest-at-phase-boundaries"
        if value["parent_policy"] != expected_policy:
            raise ValueError("parent_policy conflicts with active_mode")
    if not isinstance(value["roles"], dict):
        raise ValueError("roles must be an object")
    for name, settings in value["roles"].items():
        if name not in (LEGACY_ROLES | ROLES if version == 1 else ROLES):
            raise ValueError("unknown role: " + name)
        if not isinstance(settings, dict) or set(settings) - {"preferred_models", "effort_hint"}:
            raise ValueError("invalid settings for " + name)
        models = settings.get("preferred_models")
        if not isinstance(models, list) or not models or any(not isinstance(m, str) or not m.strip() for m in models):
            raise ValueError("preferred_models must be a nonempty string list for " + name)
        if len(models) != len(set(models)):
            raise ValueError("duplicate model preference for " + name)
        if "effort_hint" in settings and any(m in ALIASES for m in models):
            raise ValueError("inheritance aliases inherit effort too; choose an explicit model for effort_hint")
        if "effort_hint" in settings and settings["effort_hint"] not in EFFORT_RANK:
            raise ValueError("unsupported or non-normalized effort_hint for " + name)
    return value


def migrate_preferences(value):
    """Preserve choices while moving legacy role keys to hyphenated identifiers."""
    validate_preferences(value)
    roles = {}
    for name, settings in value["roles"].items():
        key = name.replace(" ", "-")
        if key in roles:
            raise ValueError("colliding legacy and canonical role: " + key)
        roles[key] = settings
    result = {**value, "schema_version": 2, "active_mode": normalize_mode(value.get("active_mode")), "roles": roles}
    return validate_preferences(result)


def set_mode(path, mode):
    """Explicit local preference update only; never changes Codex or a running worker."""
    mode = normalize_mode(mode)
    if mode is None:
        raise ValueError("set_mode requires a named mode")
    path = Path(path).expanduser()
    if path.is_symlink():
        raise ValueError("refusing to replace a symlink preference file")
    before = path.read_bytes() if path.exists() else None
    value = json.loads(before) if before is not None else {
        "schema_version": 1, "policy": "adaptive",
        "parent_policy": "suggest-at-phase-boundaries", "roles": {}}
    value = migrate_preferences(value)
    value["active_mode"] = mode
    value["parent_policy"] = "mode-adaptive"
    validate_preferences(value)
    after = (json.dumps(value, indent=2) + "\n").encode()
    if before == after:
        return {"status": "unchanged", "active_mode": mode, "parent_changed": False}
    path.parent.mkdir(parents=True, exist_ok=True)
    backup = None
    if before is not None:
        backup = path.with_name(path.name + ".backup-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ"))
        with backup.open("xb") as stream:
            os.chmod(backup, 0o600)
            stream.write(before)
    fd, temp = tempfile.mkstemp(prefix=".forge-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(after)
            stream.flush()
            os.fsync(stream.fileno())
        if path.is_symlink() or (path.read_bytes() if path.exists() else None) != before:
            raise ValueError("preferences changed concurrently; leaving the current file untouched")
        os.replace(temp, path)
        if validate_preferences(json.loads(path.read_text())) != value:
            raise ValueError("preference readback differs")
    finally:
        if os.path.exists(temp):
            os.unlink(temp)
    return {"status": "configured", "active_mode": mode, "backup": str(backup) if backup else None,
            "parent_changed": False, "worker_dispatch": "not-tested"}


def role_candidates(name, mode, preferences, task_reason):
    if name not in ROLES:
        raise ValueError("unknown role: " + str(name))
    if mode not in ROLE_PROFILES:
        raise ValueError("role defaults require a named Forge mode")
    if not isinstance(task_reason, str) or not task_reason.strip():
        raise ValueError("role selection requires task_reason confirming this default is sufficient")
    profile = ROLE_PROFILES[mode][name]
    settings = preferences.get("roles", {}).get(name, {}) if preferences else {}
    models = settings.get("preferred_models", [profile["model"]])
    selected_effort = settings.get("effort_hint", profile["effort"])
    return [{"model": model, "effort": selected_effort,
             "reason": task_reason, "source": "role-preference" if settings else "mode-role-default"}
            for model in models]


def resolve(request):
    if not isinstance(request, dict):
        raise ValueError("request must be a JSON object")
    target = request.get("target", "worker")
    if target not in ("parent", "worker"):
        raise ValueError("target must be parent or worker")
    preferences = request.get("preferences")
    if preferences is not None:
        preferences = migrate_preferences(preferences)
    mode = request.get("mode")
    if mode is None and preferences:
        mode = preferences.get("active_mode")
    mode = normalize_mode(mode)
    parent = request.get("parent", {})
    if not isinstance(parent, dict):
        raise ValueError("parent must be an object")
    parent_model, parent_effort = parent.get("model"), effort(parent.get("effort"))
    result = {"status": "inherit-unverified", "requested": None, "observed_effective": None,
              "parent": {"model": parent_model, "effort": parent_effort}, "target": target, "mode": mode, "profile_policy": "mode-adaptive" if mode else "parent-ceiling", "rejected": []}
    role = request.get("role_config", {})
    if not isinstance(role, dict) or set(role) - {"model", "effort"} or any(not isinstance(v, str) or not v for v in role.values()):
        raise ValueError("role_config accepts only observed nonempty model and effort settings")
    if role and (not isinstance(parent_model, str) or parent_effort not in EFFORT_RANK or not request.get("catalog")):
        result.update(status="blocked", reason="unverified parent or catalog with role pins; use a confirmed unpinned role or return work to the parent")
        return result
    if not isinstance(parent_model, str) or parent_effort not in EFFORT_RANK:
        if mode:
            result["status"] = "blocked"
        result["reason"] = "active parent metadata unavailable; keep work with the parent until runtime context can be verified"
        return result
    entries = request.get("catalog", [])
    if not isinstance(entries, list):
        raise ValueError("catalog must be a list")
    catalog = {}
    for item in entries:
        if not isinstance(item, dict) or not isinstance(item.get("model"), str) or not isinstance(item.get("efforts"), list):
            raise ValueError("each catalog entry requires model and efforts")
        if item["model"] in catalog:
            raise ValueError("duplicate catalog model")
        catalog[item["model"]] = {effort(e) for e in item["efforts"] if isinstance(e, str)}
    if parent_model not in catalog or parent_effort not in catalog[parent_model]:
        result["reason"] = "parent profile is not verified against this dispatch catalog; use a confirmed unpinned role only"
        if role or mode:
            result["status"] = "blocked"
        return result
    role_name = request.get("role")
    if role_name is not None and role_name not in ROLES:
        raise ValueError("unknown role: " + str(role_name))
    if role_name in MAIN_ROLES and target != "parent":
        raise ValueError("main-owned role requires target parent")
    result["role"] = role_name
    if role_name:
        result["role_contract"] = ROLE_CONTRACTS[role_name]
    if "candidates" in request:
        candidates = request["candidates"]
    elif role_name is not None:
        candidates = role_candidates(role_name, mode, preferences, request.get("task_reason"))
    else:
        candidates = [{"model": "inherit-parent"}]
    if not isinstance(candidates, list):
        raise ValueError("candidates must be a list")
    for candidate in candidates:
        if not isinstance(candidate, dict) or not isinstance(candidate.get("model"), str):
            raise ValueError("each candidate requires a model")
        inherit = candidate["model"] in ALIASES
        model = parent_model if inherit else candidate["model"]
        selected_effort = parent_effort if inherit else effort(candidate.get("effort"))
        actual_model = role.get("model", model)
        actual_effort = effort(role.get("effort", selected_effort))
        reasons = []
        if mode and actual_effort not in MODE_PROFILES[mode].get(actual_model, []):
            reasons.append("effective profile is outside the selected " + mode + " mode")
        if model not in catalog or selected_effort not in catalog.get(model, set()):
            reasons.append("requested arguments are not supported by the observed dispatch catalog")
        if (actual_model, actual_effort) != (model, selected_effort):
            reasons.append("role pins change the qualified candidate; requalify that exact profile or use an unpinned role")
        if actual_model not in catalog or actual_effort not in catalog.get(actual_model, set()):
            reasons.append("profile not supported by the observed dispatch catalog")
        if not mode and actual_model != parent_model:
            if actual_model not in MODEL_RANK or parent_model not in MODEL_RANK:
                reasons.append("model order is unverified; inherit the exact parent")
            elif MODEL_RANK[actual_model] > MODEL_RANK[parent_model]:
                reasons.append("model exceeds parent ceiling")
        if not mode and (actual_effort not in EFFORT_RANK or EFFORT_RANK.get(actual_effort, 99) > EFFORT_RANK[parent_effort]):
            reasons.append("reasoning effort exceeds parent ceiling or is unknown")
        if actual_effort == "ultra" and (parent_effort != "ultra" or request.get("parallel") is not True):
            reasons.append("ultra requires a matching parent and independent-work assignment")
        if (actual_model, actual_effort) != (parent_model, parent_effort) and not str(candidate.get("reason", "")).strip():
            reasons.append("departure from parent inheritance needs a task-fit reason")
        if reasons:
            result["rejected"].append({"candidate": candidate, "role_applied": {"model": actual_model, "effort": actual_effort}, "reasons": reasons})
            continue
        result.update(status="ready", requested={} if inherit else {"model": model, "reasoning_effort": selected_effort},
                      expected_from_config={"model": actual_model, "effort": actual_effort},
                      reason=candidate.get("reason") or "inherit the manually selected parent",
                      parent_adaptation={"current": {"model": parent_model, "effort": parent_effort},
                                         "mode_governs_parent_and_workers": bool(mode),
                                         "current_parent_in_mode": parent_effort in MODE_PROFILES[mode].get(parent_model, []) if mode else True,
                                         "runtime_switch_performed": False})
        if target == "parent":
            result["parent_adaptation"]["desired"] = {"model": model, "effort": selected_effort}
            result["parent_adaptation"]["change_needed"] = (model, selected_effort) != (parent_model, parent_effort)
            result["parent_adaptation"]["application"] = "requires-supported-current-task-control-or-owner-action"
        return result
    result.update(status="blocked", reason="no sufficient proposed profile passed; reassess task fit within the active policy")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", help="JSON input file; omit to read stdin")
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--validate-preferences", metavar="FILE")
    action.add_argument("--set-mode", choices=sorted(set(MODE_PROFILES) | set(MODE_ALIASES)))
    action.add_argument("--list-modes", action="store_true")
    action.add_argument("--role-map", action="store_true", help="show exact role defaults for all modes")
    parser.add_argument("--preferences", metavar="FILE", help="preference file for explicit --set-mode")
    args = parser.parse_args()
    try:
        if args.set_mode:
            if not args.preferences:
                raise ValueError("--set-mode requires an explicit --preferences FILE")
            output = set_mode(args.preferences, args.set_mode)
        elif args.role_map:
            output = {"status": "configured-defaults", "modes": ROLE_PROFILES, "roles": ROLE_CONTRACTS, "groups": ROUTING_CATALOG["groups"], "dispatch": "not-performed"}
        elif args.list_modes:
            output = {"status": "available-presets", "modes": MODE_PROFILES, "availability": "check-dispatch-catalog"}
        elif args.validate_preferences:
            validate_preferences(json.loads(Path(args.validate_preferences).read_text()))
            output = {"status": "valid", "availability": "not-checked"}
        else:
            data = json.loads(Path(args.input).read_text() if args.input else sys.stdin.read())
            output = resolve(data)
        print(json.dumps(output, indent=2))
        return 1 if output["status"] == "blocked" else 0
    except (OSError, ValueError, TypeError) as error:
        print(json.dumps({"status": "error", "error": str(error)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
