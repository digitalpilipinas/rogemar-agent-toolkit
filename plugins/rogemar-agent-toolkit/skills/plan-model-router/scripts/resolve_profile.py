#!/usr/bin/env python3
"""Read-only validation of a proposed Codex worker profile or Forge preferences."""
from __future__ import annotations

import argparse
import json
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


def effort(value):
    return {"light": "low", "extra high": "xhigh"}.get(value, value) if isinstance(value, str) else None


def validate_preferences(value):
    if not isinstance(value, dict):
        raise ValueError("preferences must be a JSON object")
    if set(value) != {"schema_version", "policy", "parent_policy", "roles"}:
        raise ValueError("expected schema_version, policy, parent_policy, and roles only")
    if type(value["schema_version"]) is not int or value["schema_version"] != 1:
        raise ValueError("unsupported preference schema_version")
    if value["policy"] != "adaptive" or value["parent_policy"] != "suggest-at-phase-boundaries":
        raise ValueError("unsupported routing or parent policy")
    if not isinstance(value["roles"], dict):
        raise ValueError("roles must be an object")
    for name, settings in value["roles"].items():
        if name not in ROLES:
            raise ValueError("unknown role: " + name)
        if not isinstance(settings, dict) or set(settings) - {"preferred_models", "effort_hint"}:
            raise ValueError("invalid settings for " + name)
        models = settings.get("preferred_models")
        if not isinstance(models, list) or not models or any(not isinstance(m, str) or not m.strip() for m in models):
            raise ValueError("preferred_models must be a nonempty string list for " + name)
        if len(models) != len(set(models)):
            raise ValueError("duplicate model preference for " + name)
        if "effort_hint" in settings and settings["effort_hint"] not in EFFORT_RANK:
            raise ValueError("unsupported or non-normalized effort_hint for " + name)
    return value


def resolve(request):
    if not isinstance(request, dict):
        raise ValueError("request must be a JSON object")
    parent = request.get("parent", {})
    if not isinstance(parent, dict):
        raise ValueError("parent must be an object")
    parent_model, parent_effort = parent.get("model"), effort(parent.get("effort"))
    result = {"status": "inherit-unverified", "requested": None, "observed_effective": None,
              "parent": {"model": parent_model, "effort": parent_effort}, "rejected": []}
    role = request.get("role_config", {})
    if not isinstance(role, dict) or set(role) - {"model", "effort"} or any(not isinstance(v, str) or not v for v in role.values()):
        raise ValueError("role_config accepts only observed nonempty model and effort settings")
    if role and (not isinstance(parent_model, str) or parent_effort not in EFFORT_RANK or not request.get("catalog")):
        result.update(status="blocked", reason="unverified parent or catalog with role pins; use a confirmed unpinned role or return work to the parent")
        return result
    if not isinstance(parent_model, str) or parent_effort not in EFFORT_RANK:
        result["reason"] = "active parent metadata unavailable; do not override the inherited profile"
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
        if role:
            result["status"] = "blocked"
        return result
    candidates = request.get("candidates", [{"model": "inherit-parent"}])
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
        if model not in catalog or selected_effort not in catalog.get(model, set()):
            reasons.append("requested arguments are not supported by the observed dispatch catalog")
        if (actual_model, actual_effort) != (model, selected_effort):
            reasons.append("role pins change the qualified candidate; requalify that exact profile or use an unpinned role")
        if actual_model not in catalog or actual_effort not in catalog.get(actual_model, set()):
            reasons.append("profile not supported by the observed dispatch catalog")
        if actual_model != parent_model:
            if actual_model not in MODEL_RANK or parent_model not in MODEL_RANK:
                reasons.append("model order is unverified; inherit the exact parent")
            elif MODEL_RANK[actual_model] > MODEL_RANK[parent_model]:
                reasons.append("model exceeds parent ceiling")
        if actual_effort not in EFFORT_RANK or EFFORT_RANK.get(actual_effort, 99) > EFFORT_RANK[parent_effort]:
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
                      reason=candidate.get("reason") or "inherit the manually selected parent")
        return result
    result.update(status="blocked", reason="no sufficient proposed profile passed; use an unpinned role or return work to the parent")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", help="JSON input file; omit to read stdin")
    parser.add_argument("--validate-preferences", metavar="FILE")
    args = parser.parse_args()
    try:
        if args.validate_preferences:
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
