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
# Shared executable catalogue: mode pools, group defaults, role overrides and contracts.
ROUTING_CATALOG = json.loads(Path(__file__).with_name("routing_catalog.json").read_text())
MODEL_RANK = {model: settings['tier'] for model, settings in ROUTING_CATALOG['models'].items()}
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
    if type(version) is not int or version not in (1, 2, 3):
        raise ValueError("unsupported preference schema_version")
    fields = {"schema_version", "policy", "parent_policy", "roles"}
    if version >= 2:
        fields.add("active_mode")
    if version == 3:
        fields.add("default_profile")
    if set(value) != fields:
        raise ValueError("unexpected or missing preference fields")
    if version >= 2:
        normalize_mode(value["active_mode"])
    if value["policy"] != "adaptive" or value["parent_policy"] not in ({"suggest-at-phase-boundaries", "mode-adaptive"} if version >= 2 else {"suggest-at-phase-boundaries"}):
        raise ValueError("unsupported routing or parent policy")
    if version >= 2:
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
    if version == 3:
        profile = value['default_profile']
        if profile is not None and (not isinstance(profile, dict) or set(profile) != {'model','effort'} or not isinstance(profile['model'], str) or not profile['model'] or profile['effort'] not in EFFORT_RANK):
            raise ValueError('invalid default_profile')
        if normalize_mode(value['active_mode']) == 'default' and profile is None:
            raise ValueError('Default mode requires an explicit default_profile')
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
    result = {**value, "schema_version": 3, "active_mode": normalize_mode(value.get("active_mode")), "roles": roles, "default_profile": value.get("default_profile")}
    return validate_preferences(result)


def set_mode(path, mode, default_profile=None):
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
    if default_profile is not None:
        value["default_profile"] = {"model": default_profile["model"], "effort": effort(default_profile["effort"])}
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


def paired(record):
    """A catalogue qualification needs two distinct verified, matching trials."""
    trials = record.get('validation', [])
    profile = {k:record.get(k) for k in ('model','effort')}
    return (record.get('status') == 'verified' and isinstance(record.get('evidence_id'),str) and bool(record['evidence_id'].strip()) and len(trials) == 2
            and len({v.get('assignment_id') for v in trials}) == 2
            and {v.get('repetition') for v in trials} == {1,2}
            and len({v.get('packet_sha256') for v in trials}) == 1
            and all(v.get('passed') is True and v.get('profile_verified') is True
                    and v.get('profile') == profile and v.get('assignment_id')
                    and v.get('packet_sha256') for v in trials))


def coding_qualified(record):
    return record.get('executable') is True and paired({**record, 'validation':record.get('coding_validation',[])})


def qualification(role, profile, implementation=False):
    return next((q for q in ROUTING_CATALOG.get('qualified_profiles', {}).get(role, [])
                 if {k:q.get(k) for k in ('model','effort')} == profile and paired(q)
                 and (not implementation or coding_qualified(q))), None)


def role_map():
    """Arrangement labels never advertise a blanket worker profile."""
    return {mode: {role: ({'assignment_role_required': True} if role in ('swarm-workers', 'arena-runners') else dict(p))
                   for role, p in profiles.items()} for mode, profiles in ROLE_PROFILES.items()}


def resolve(request):
    if not isinstance(request, dict):
        raise ValueError('request must be a JSON object')
    for flag in ('consequential','implementation'):
        if flag in request and type(request[flag]) is not bool:
            raise ValueError(flag + ' must be a boolean')
    evidence_contract = request.get('evidence_contract')
    if evidence_contract is not None and evidence_contract not in ('notes-store', 'note-editor-ui'):
        raise ValueError('unsupported evidence_contract')
    # Execution arrangements must preserve the participant's real function.
    arrangement = request.get('arrangement')
    if arrangement is not None and arrangement not in ('swarm', 'arena'):
        raise ValueError('arrangement must be swarm or arena')
    if request.get('role') in ('swarm-workers', 'arena-runners'):
        actual_role = request.get('assignment_role')
        if actual_role not in ROLES or actual_role in MAIN_ROLES or actual_role in ('swarm-workers', 'arena-runners'):
            return dict(status='assignment-required', reason='resolve the participant actual function before dispatch; a swarm/arena label is not a work contract', requested=None)
        routed = dict(request, role=actual_role, arrangement='swarm' if request['role']=='swarm-workers' else 'arena')
        routed.pop('assignment_role', None)
        result = resolve(routed)
        result['arrangement'] = routed['arrangement']
        result['original_role'] = request['role']
        return result
    if 'assignment_role' in request:
        raise ValueError('assignment_role is only for swarm-workers or arena-runners')
    target = request.get('target', 'worker')
    if target not in ('parent', 'worker'):
        raise ValueError('target must be parent or worker')
    preferences = migrate_preferences(request['preferences']) if request.get('preferences') is not None else None
    mode = normalize_mode(request['mode'] if 'mode' in request else preferences.get('active_mode') if preferences else None)
    raw_parent = request.get('parent', {})
    if not isinstance(raw_parent, dict):
        raise ValueError('parent must be an object')
    parent = {'model': raw_parent.get('model'), 'effort': effort(raw_parent.get('effort'))}
    result = dict(status='blocked' if mode else 'inherit-unverified', requested=None,
                  observed_effective=None, parent=parent, target=target, mode=mode,
                  profile_policy='exact-profile' if mode == 'default' else 'mode-ceiling' if mode else 'parent-ceiling', rejected=[])
    pins = request.get('role_config', {})
    if not isinstance(pins, dict) or set(pins) - {'model','effort'} or any(not isinstance(v,str) or not v for v in pins.values()):
        raise ValueError('role_config accepts only observed nonempty model and effort settings')
    entries = request.get('catalog', [])
    if not isinstance(entries, list):
        raise ValueError('catalog must be a list')
    catalog = {}
    for item in entries:
        if not isinstance(item, dict) or not isinstance(item.get('model'), str) or not isinstance(item.get('efforts'), list) or item['model'] in catalog:
            raise ValueError('invalid or duplicate catalog entry')
        observed = {effort(e) for e in item['efforts'] if isinstance(e,str)}
        supported = ROUTING_CATALOG['models'].get(item['model'], {}).get('supported_efforts', observed)
        catalog[item['model']] = observed.intersection(supported)
    if not isinstance(parent['model'],str) or parent['effort'] not in EFFORT_RANK or parent['effort'] not in catalog.get(parent['model'],set()):
        if pins: result['status'] = 'blocked'
        result['reason'] = 'active parent metadata/catalog unavailable; retain direct work without a routing claim'
        return result
    role_name = request.get('role')
    if role_name is not None and (not isinstance(role_name,str) or role_name not in ROLES):
        raise ValueError('unknown role: ' + str(role_name))
    if role_name in MAIN_ROLES and target != 'parent':
        raise ValueError('main-owned role requires target parent')
    if mode and target == 'worker' and role_name is None:
        raise ValueError('named-mode worker requests require a known role')
    if mode == 'default':
        desired = request['default_profile'] if 'default_profile' in request else (preferences or {}).get('default_profile') or parent
        if not isinstance(desired,dict) or set(desired) != {'model','effort'} or not isinstance(desired.get('model'),str) or not desired['model'] or effort(desired.get('effort')) not in EFFORT_RANK:
            raise ValueError('default_profile requires model and effort')
        desired = {'model':desired['model'], 'effort':effort(desired['effort'])}
    else:
        desired = ROUTING_CATALOG['parent_targets'].get(mode, parent)
    result.update(role=role_name, role_contract=ROLE_CONTRACTS.get(role_name),
                  task_requirements=ROUTING_CATALOG.get('task_requirements',{}).get(role_name,[]),
                  parent_adaptation={'current':parent, 'desired':desired, 'change_needed':parent != desired,
                                     'runtime_switch_performed':False, 'application':'requires-supported-current-task-control-or-owner-action'})
    limits = request.get('limits',{})
    if not isinstance(limits,dict) or set(limits) - {'model','effort'} or any(not isinstance(v,str) for v in limits.values()):
        raise ValueError('limits accepts model and effort strings only')
    def limit_reasons(profile):
        reasons = []
        if 'model' in limits and (limits['model'] not in MODEL_RANK or MODEL_RANK.get(profile['model'],99) > MODEL_RANK[limits['model']]):
            reasons.append('explicit model limit')
        if 'effort' in limits and (effort(limits['effort']) not in EFFORT_RANK or EFFORT_RANK.get(profile['effort'],99) > EFFORT_RANK[effort(limits['effort'])]):
            reasons.append('explicit reasoning limit')
        return reasons
    if target == 'parent':
        problems = limit_reasons(desired)
        if desired['effort'] not in catalog.get(desired['model'],set()):
            problems.append('desired parent profile is unavailable in the observed catalogue')
        if problems:
            result.update(status='blocked',reason='; '.join(problems))
        else:
            result.update(status='ready', requested={'model':desired['model'],'reasoning_effort':desired['effort']},
                          expected_from_config=desired, reason='parent proposal only; no switch performed')
        return result
    if mode and parent != desired:
        expected = {'mode':mode,'desired':desired,'actual':parent,'accepted':True}
        if request.get('parent_fallback') != expected or request.get('parent_fallback',{}).get('accepted') is not True:
            result.update(status='parent-choice-required', reason='clarify desired versus actual parent once before mode-dependent dispatch')
            return result
        if mode == 'default':
            result.update(status='blocked', reason='Default must remain exact; explicitly select the actual parent as the task default_profile')
            return result
    consequential = request.get('consequential',False) or role_name in ROUTING_CATALOG.get('consequential_roles',[]) or role_name == 'how-critics'
    implementation = request.get('implementation',False) or role_name in ROUTING_CATALOG.get('coding_roles',[])
    if implementation and role_name in ('ui-designer', 'ux-flow-designer', 'interaction-designer'):
        if evidence_contract not in (None, 'note-editor-ui'):
            result.update(status='blocked', reason='UI implementation requires matching UI evidence, not the database contract')
            return result
        evidence_contract = 'note-editor-ui'
    result['evidence_contract'] = evidence_contract
    result.update(consequential=consequential, implementation=implementation)
    if implementation and result.get('role_contract'):
        result['role_contract'] = {**result['role_contract'], 'assignment': 'bounded-implementation'}
    if role_name in ROUTING_CATALOG.get('review_support_roles',[]) and (implementation or consequential):
        result.update(status='blocked', reason='monitoring/consolidation is read-only support; route judgment or implementation as a separate assignment')
        return result
    binding = ROUTING_CATALOG.get('native_bindings', {}).get(role_name)
    native = request.get('goalbuddy_required', False)
    if type(native) is not bool:
        raise ValueError('goalbuddy_required must be a boolean')
    if native and not binding:
        raise ValueError('GoalBuddy native contract requires a mapped Scout or Judge role')
    if binding:
        if implementation:
            result.update(status='blocked', reason='Forge and native Scout/Judge contracts are read-only, not implementation assignments')
            return result
        result['dispatch_agent_type'] = binding['goalbuddy_agent_type' if native else 'ordinary_agent_type']
        result['native_contract_required'] = native
        if native:
            if effort(pins.get('effort')) != binding['effort']:
                result.update(status='blocked', reason='mandatory GoalBuddy pin must be observed and qualified before dispatch')
                return result
        elif pins:
            result.update(status='blocked', reason='ordinary Forge Scout/Judge needs an unpinned read-only assignment')
            return result
    if 'candidates' in request:
        candidates = request['candidates']
    elif mode == 'default':
        settings = (preferences or {}).get('roles',{}).get(role_name,{})
        models = settings.get('preferred_models',[desired['model']])
        candidates = [{'model':m,'effort':settings.get('effort_hint',desired['effort']),'reason':'exact user-selected Default profile'} for m in models]
    elif mode and native and not (preferences or {}).get('roles',{}).get(role_name):
        candidates = [{'model':parent['model'],'effort':binding['effort'],'reason':'mandatory native GoalBuddy profile subject to ceilings'}]
    elif mode and consequential and not (preferences or {}).get('roles',{}).get(role_name):
        default = ROLE_PROFILES[mode].get(role_name)
        if default and default['model'] == parent['model'] and qualification(role_name, default, implementation):
            candidates = role_candidates(role_name, mode, preferences, request.get('task_reason'))
        else:
            candidates = [{'model':'inherit-parent','reason':'task requires consequential parent-family judgment; no matching qualified default'}]
    elif mode and role_name in ('hillclimb','hardest-tasks') and not (preferences or {}).get('roles',{}).get(role_name):
        candidates = [{'model':'inherit-parent','reason':'hard work normally inherits the actual parent within normal limits'}]
    elif role_name and mode:
        candidates = role_candidates(role_name,mode,preferences,request.get('task_reason'))
        if native and not (preferences or {}).get('roles',{}).get(role_name):
            candidates = [{**c,'effort':binding['effort'],'reason':'mandatory native GoalBuddy reasoning, subject to ceilings'} for c in candidates]
    else:
        candidates = [{'model':'inherit-parent'}]
    if not isinstance(candidates,list):
        raise ValueError('candidates must be a list')
    for candidate in candidates:
        if not isinstance(candidate,dict) or not isinstance(candidate.get('model'),str):
            raise ValueError('each candidate requires model')
        inherit = candidate['model'] in ALIASES
        requested = parent if inherit else {'model':candidate['model'],'effort':effort(candidate.get('effort'))}
        actual = {'model':pins.get('model',requested['model']), 'effort':effort(pins.get('effort',requested['effort']))}
        reasons = []
        if actual != requested: reasons.append('role pins change the qualified candidate')
        if requested['effort'] not in catalog.get(requested['model'],set()) or actual['effort'] not in catalog.get(actual['model'],set()):
            reasons.append('requested or effective profile not supported by observed dispatch catalog')
        records = ROUTING_CATALOG.get('exceptions',{}).get(mode,{}).get(role_name,[])
        if isinstance(records,dict): records = [records]  # Read earlier single-profile catalogues.
        ex = next((e for e in records if e.get('evidence_id') == request.get('exception_evidence_id')
                   and {k:e.get(k) for k in ('model','effort')} == actual), {})
        if ex.get('allowed_assignment') == 'read-only-consultation' and implementation:
            reasons.append('this consultant exception permits read-only advice, not implementation')
        if ex and evidence_contract != ex.get('evidence_contract'):
            reasons.append('exception evidence does not match the declared task contract; classify the actual work before dispatch')
        exception = bool(mode not in (None,'default') and role_name in ('hillclimb','hardest-tasks')
                         and evidence_contract is not None and evidence_contract == ex.get('evidence_contract')
                         and paired(ex) and (not implementation or coding_qualified(ex))
                         and request.get('difficult_task') is True
                         and isinstance(request.get('exception_reason'),str)
                         and request['exception_reason'].strip())
        qualified = qualification(role_name,actual,implementation)
        if implementation and (not evidence_contract or evidence_contract != (qualified or {}).get('evidence_contract')):
            qualified = None
        if mode == 'default':
            if actual != desired: reasons.append('Default requires exact model and reasoning for every ordinary role')
        elif mode:
            if role_name in ROUTING_CATALOG.get('review_support_roles',[]) and actual['model'] not in ROUTING_CATALOG['review_support_models']:
                reasons.append('review monitoring/consolidation uses qualified Luna support; keep unavailable support direct with a disclosed fallback')
            if mode in ROUTING_CATALOG.get('review_separation_modes',[]) and (implementation or role_name in ROUTING_CATALOG.get('review_decision_roles',[])) and MODEL_RANK.get(actual['model'],-1)<MODEL_RANK[ROUTING_CATALOG['review_decision_minimum_model']]:
                reasons.append('finding validation, minimum-scope judgment and implementation require a non-Luna permitted profile')
            if actual['effort'] not in MODE_PROFILES[mode].get(actual['model'],[]) and not exception:
                reasons.append('effective profile is outside the selected mode normal pool; no verified exception')
            if consequential and actual['model'] != parent['model'] and not exception:
                reasons.append('consequential judgment retains the actual parent family')
            native_pin_only = native and actual['model']==parent['model'] and actual['effort']==binding['effort']
            if actual != parent and not native_pin_only and not qualified and not exception:
                reasons.append('lower or alternate profile lacks paired role qualification for this work')
        ceilings = [parent] + ([desired] if mode else [])
        for ceiling in ceilings:
            if actual['model'] != ceiling['model'] and (actual['model'] not in MODEL_RANK or ceiling['model'] not in MODEL_RANK or MODEL_RANK[actual['model']] > MODEL_RANK[ceiling['model']]) and not exception:
                reasons.append('model exceeds parent ceiling or model order is unknown')
            if EFFORT_RANK.get(actual['effort'],99) > EFFORT_RANK.get(ceiling['effort'],-1) and not exception:
                reasons.append('reasoning exceeds parent ceiling; no verified exception')
        reasons.extend(limit_reasons(actual))
        if actual != parent and not str(candidate.get('reason','')).strip():
            reasons.append('departure from parent inheritance needs a task-fit reason')
        if reasons:
            result['rejected'].append({'candidate':candidate,'role_applied':actual,'reasons':reasons})
            continue
        result.update(status='ready', requested={} if inherit else {'model':requested['model'],'reasoning_effort':requested['effort']},
                      expected_from_config=actual, reason=candidate.get('reason') or 'inherit parent',
                      exception_applied=exception, evidence_status='unverified-runtime',
                      qualification_id=(ex if exception else qualified or {}).get('evidence_id'),
                      known_quality_failures=[f for f in ROUTING_CATALOG.get('known_failures',{}).get(role_name,[]) if f['profile']==actual and (implementation or not f.get('coding_only'))],
                      quality_status='qualified-for-tested-contract' if exception or qualified else 'native-contract' if native else 'parent-profile-provisional')
        result['qualification_scope'] = (ex if exception else qualified or {}).get('scope', 'supplied benchmark contract only; not general role competence')
        if 'not general role competence' not in result['qualification_scope']:
            result['qualification_scope'] += '; not general role competence'
        result['task_fit_required'] = True
        if evidence_contract == 'note-editor-ui' and role_name not in ('ui-designer','ux-flow-designer','interaction-designer'):
            result['known_quality_failures'] += [f for f in ROUTING_CATALOG.get('known_failures',{}).get('ui-designer',[]) if f['profile']==actual]
        result['arrangement'] = arrangement
        return result
    result.update(status='blocked',reason='no sufficient proposed profile passed; retain ordinary work with parent or report missing independent evidence')
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
    parser.add_argument('--default-model', help='Explicit Default model; pair with --default-effort')
    parser.add_argument('--default-effort', help='Explicit Default reasoning')
    args = parser.parse_args()
    try:
        if args.set_mode:
            if not args.preferences:
                raise ValueError("--set-mode requires an explicit --preferences FILE")
            if bool(args.default_model) != bool(args.default_effort):
                raise ValueError('provide both --default-model and --default-effort')
            profile = {'model':args.default_model,'effort':args.default_effort} if args.default_model else None
            output = set_mode(args.preferences, args.set_mode, profile)
        elif args.role_map:
            output = {"status": "configured-defaults", "modes": role_map(), "roles": ROLE_CONTRACTS, "groups": ROUTING_CATALOG["groups"], "dispatch": "not-performed"}
        elif args.list_modes:
            output = {"status": "available-presets", "modes": MODE_PROFILES, "availability": "check-dispatch-catalog"}
        elif args.validate_preferences:
            validate_preferences(json.loads(Path(args.validate_preferences).read_text()))
            output = {"status": "valid", "availability": "not-checked"}
        else:
            data = json.loads(Path(args.input).read_text() if args.input else sys.stdin.read())
            output = resolve(data)
        print(json.dumps(output, indent=2))
        return 1 if output["status"] in ("blocked", "parent-choice-required", "assignment-required") else 0
    except (OSError, ValueError, TypeError) as error:
        print(json.dumps({"status": "error", "error": str(error)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
