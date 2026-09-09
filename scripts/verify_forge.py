#!/usr/bin/env python3
"""Check the pinned Forge inventory and portable resource graph without executing skills."""
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'plugins/rogemar-agent-toolkit/skills'

def verify():
    declared = {item['name'] for item in json.loads((ROOT/'catalog/skills.yaml').read_text())['vendored']}
    actual = {p.name for p in SKILLS.iterdir() if p.name=='codex-forge' or p.name.startswith('forge-')}
    if not actual and not any(n=='codex-forge' or n.startswith('forge-') for n in declared):
        return []
    manifest = json.loads((ROOT/'catalog/codex-forge-upstream.json').read_text())
    names = manifest['registered_skills']
    errors=[]
    if len(names)!=45 or len(set(names.values()))!=45: errors.append('Expected 45 unique mapped skills')
    actual={p.name for p in SKILLS.iterdir() if p.name=='codex-forge' or p.name.startswith('forge-')}
    if actual != set(names.values()): errors.append('Forge skill directories differ from the pinned inventory')
    for row in manifest['files']:
        dest=row.get('destination')
        if dest and (not (ROOT/dest).is_file() or not (ROOT/dest).resolve().is_relative_to(ROOT)):
            errors.append('Missing or unsafe mapped resource: '+str(dest))
    core=SKILLS/'codex-forge'
    for path,pattern,count in [(core/'playbooks','*.md',23),(core/'assets/agents','*.toml',2),(core/'assets/automations/benny','**/RECIPE.md',3)]:
        if len(list(path.glob(pattern))) != count: errors.append('Wrong resource count: '+str(path.relative_to(ROOT)))
    if list((core/'assets/automations').rglob('SKILL.md')):errors.append('Inactive recipes must not be discoverable SKILL.md files')
    for name in names.values():
        skill=SKILLS/name
        if not (skill/'LICENSE.txt').is_file() or 'Lauren Tan' not in (skill/'LICENSE.txt').read_text():errors.append(name+': missing attribution')
        if not (skill/'agents/openai.yaml').is_file():errors.append(name+': missing discovery metadata')
        text=(skill/'SKILL.md').read_text()
        if not re.search(r'^name: '+re.escape(name)+r'$',text,re.M):errors.append(name+': invalid skill name')
        for p in skill.rglob('*.md'):
            if 'node_modules' in p.parts or 'automations' in p.parts:continue
            content=p.read_text()
            for link in re.findall(r'\]\(([^)]+)\)',content):
                link=link.split('#')[0]
                if not link or '://' in link or link.startswith(('mailto:','<')):continue
                if not (p.parent/link).exists():errors.append(str(p.relative_to(ROOT))+': broken link '+link)
            if re.search(r'`(?:grok|claude)-[^`]+`|readonly[^\n]*`false`|~\/\.cursor\/|run_in_background:',content):
                errors.append(str(p.relative_to(ROOT))+': unadapted runtime instruction')
    for p in (core/'assets/agents').glob('*.toml'):
        if re.search(r'^(model|model_reasoning_effort)\s*=',p.read_text(),re.M):errors.append(p.name+': model/effort pin blocks inheritance')
    return errors

if __name__=='__main__':
    errors=verify()
    for e in errors:print(e,file=sys.stderr)
    print(json.dumps({'status':'failed' if errors else ('verified' if (SKILLS/'codex-forge').is_dir() else 'not-applicable'),'skills':45 if (SKILLS/'codex-forge').is_dir() else 0,'playbooks':23 if (SKILLS/'codex-forge').is_dir() else 0,'agents':2 if (SKILLS/'codex-forge').is_dir() else 0,'inactive_recipes':3 if (SKILLS/'codex-forge').is_dir() else 0,'errors':len(errors)}))
    raise SystemExit(bool(errors))
