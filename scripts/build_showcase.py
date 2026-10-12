#!/usr/bin/env python3
"""Rebuild the toolkit's original diagram source assets using only the standard library."""
from pathlib import Path
from html import escape
import argparse

PALETTES = {
 'light':dict(paper='#f4f7fa',panel='#ffffff',ink='#10283f',muted='#506678',line='#527487',cyan='#006b7d',coral='#a13c2b'),
 'dark':dict(paper='#091827',panel='#11263b',ink='#eaf5fa',muted='#abc0ce',line='#90b6c8',cyan='#68d7e5',coral='#ffaf99')}

# Coordinates encode the approved relationships, not runtime status.
DIAGRAMS = {
 'ownership': {
  'title':'One owner. Selected methods.',
  'desc':'Planning informs Integrated Workflow; the orchestrator selects a Forge adapter and applicable specialist methods under the same implementation owner.',
  'nodes':[(48,132,240,100,'PLAN','Create Plan','Outcome and acceptance',''),(360,132,268,100,'DELIVERY','Integrated Workflow','One owner and evidence record','coral'),(704,132,272,100,'SELECTION','Orchestrator','Choose or reuse methods','cyan'),(360,340,268,100,'ENGINEERING','Forge adapter','The receiving harness',''),(704,340,272,100,'SPECIALISTS','Relevant skills','Only the methods needed','')],
  'edges':['M288 182 H360','M628 182 H704','M784 232 V276 Q784 284 776 284 H502 Q494 284 494 292 V340','M880 232 V340'],
  'footer':'The main agent integrates and accepts the result. Delegation is conditional.'},
 'task-loop': {
  'title':'Keep moving. Keep the evidence.',
  'desc':'Select methods, check prerequisites, execute, verify, record evidence and continue to the next approved task. Dynamic multi-agent work is conditional.',
  'nodes':[(48,132,260,104,'01 / PREPARE','Select or reuse','Methods for this task','cyan'),(384,132,260,104,'02 / READINESS','Check prerequisites','Only changed requirements',''),(720,132,260,104,'03 / BUILD','Execute','Stay within approved scope',''),(720,340,260,104,'04 / VERIFY','Check the result','Behavior and required reviews','coral'),(384,340,260,104,'05 / RETAIN','Record evidence','Results, limits and next action',''),(48,340,260,104,'06 / ADVANCE','Continue','Next approved, ready task','')],
  'edges':['M308 184 H384','M644 184 H720','M850 236 V340','M720 392 H644','M384 392 H308','M178 340 V236'],
  'footer':'One continuous task loop. Parallel agents are a scoped option, never a default.'},
 'installation': {
  'title':'Install there. Verify there.',
  'desc':'A reviewed revision installs locally or inside a cloud environment. Each receiving environment verifies files, discovery, required tools and actual task evidence independently.',
  'nodes':[(48,144,250,96,'SOURCE','Reviewed revision','Toolkit and catalog pins','cyan'),(392,80,240,96,'RECEIVER','This machine','Install or upgrade',''),(392,248,240,96,'RECEIVER','Cloud environment','Install or upgrade in place',''),(736,144,240,96,'FILES','Verify content','Hashes and resources',''),(736,392,240,96,'DISCOVERY','Verify agent access','Check the actual source',''),(392,392,240,96,'CAPABILITY','Check needed tools','And applicable service access',''),(48,392,250,96,'EVIDENCE','Run the actual task','Retain observed results','coral')],
  'edges':['M298 168 H336 Q344 168 344 160 V136 Q344 128 352 128 H392','M298 208 H336 Q344 208 344 216 V288 Q344 296 352 296 H392','M632 128 H672 Q680 128 680 136 V160 Q680 168 688 168 H736','M632 296 H696 Q704 296 704 288 V216 Q704 208 712 208 H736','M856 240 V392','M736 440 H632','M392 440 H298'],
  'footer':'Repeat these checks inside each environment. A local update is not cloud proof.'}}


def svg(name, theme='light'):
 d=DIAGRAMS[name]; c=PALETTES[theme]; slug=name+'-'+theme
 out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 560" role="img" aria-labelledby="{slug}-title {slug}-desc">',f'<title id="{slug}-title">{escape(d["title"])}</title>',f'<desc id="{slug}-desc">{escape(d["desc"])}</desc>',f'<defs><marker id="{slug}-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10" fill="{c["line"]}"/></marker></defs>',f'<rect width="1024" height="560" fill="{c["paper"]}"/>',f'<text x="48" y="42" fill="{c["muted"]}" font-family="system-ui,sans-serif" font-size="12" letter-spacing="2">ROGEMAR / {name.upper().replace("-"," ")}</text>',f'<text x="48" y="82" fill="{c["ink"]}" font-family="system-ui,sans-serif" font-size="28" font-weight="700">{escape(d["title"])}</text>' if name!='installation' else '']
 if name=='installation': out[4]='<rect width="1024" height="560" fill="'+c['paper']+'"/>'; out[5]=f'<text x="48" y="42" fill="{c["ink"]}" font-family="system-ui,sans-serif" font-size="24" font-weight="700">{escape(d["title"])}</text>'
 out += [f'<path d="{path}" fill="none" stroke="{c["line"]}" stroke-width="2" marker-end="url(#{slug}-arrow)"/>' for path in d['edges']]
 for i,(x,y,w,h,tag,title,detail,accent) in enumerate(d['nodes']):
  border=c.get(accent,c['line']);out += [f'<g data-step="{i}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{c["panel"]}" stroke="{border}" stroke-width="2"/>',f'<text x="{x+16}" y="{y+24}" fill="{border}" font-family="system-ui,sans-serif" font-size="11" letter-spacing="1">{escape(tag)}</text>',f'<text x="{x+16}" y="{y+52}" fill="{c["ink"]}" font-family="system-ui,sans-serif" font-size="19" font-weight="650">{escape(title)}</text>',f'<text x="{x+16}" y="{y+78}" fill="{c["muted"]}" font-family="system-ui,sans-serif" font-size="13">{escape(detail)}</text></g>']
 out.append(f'<text x="48" y="536" fill="{c["muted"]}" font-family="system-ui,sans-serif" font-size="14">{escape(d["footer"])}</text></svg>')
 return '\n'.join(out)+'\n'


def build(output):
 output.mkdir(parents=True,exist_ok=True)
 for name,d in DIAGRAMS.items():
  for theme in PALETTES:
   figure=svg(name,theme);(output/f'{name}-{theme}.svg').write_text(figure)
   html='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>'+escape(d['title'])+'</title><style>body{margin:0;background:'+PALETTES[theme]['paper']+'}main{overflow-x:auto}svg{display:block;width:100%;min-width:760px}</style></head><body><main>'+figure+'</main></body></html>'
   (output/f'{name}-{theme}.html').write_text(html)

def update_gallery(output):
 gallery=output.parent/'index.html'
 if not gallery.exists(): return
 descriptions={
 'ownership':'Planning and delivery share one accountable owner. The orchestrator selects a harness adapter and only the specialist methods the task needs.',
 'task-loop':'Reassess methods at each task handoff. Reuse valid evidence and continue within approved scope; missing required evidence stays visible.',
 'installation':'A redraw of the handbook’s Mermaid diagram: seven nodes and seven directed relationships, with no omissions. Run the shared check recipe independently in each receiving environment.'}
 blocks=[]
 for name,d in DIAGRAMS.items():
  blocks.append(f'<section class="diagram-panel" id="{name}" aria-labelledby="{name}-heading"><div class="diagram-heading"><h3 id="{name}-heading">{escape(d["title"])}</h3><p>{escape(descriptions[name])}</p></div><div class="diagram-scroll" tabindex="0" role="region" aria-label="{name.replace("-"," ")} diagram; scroll horizontally on narrow screens">')
  for theme in PALETTES: blocks.append(f'<div class="theme-{theme}">'+svg(name,theme)+'</div>')
  blocks.append('</div><div class="diagram-actions"><p>Editable SVG · complete static meaning</p>'+f'<a data-download="{name}" href="diagrams/{name}-light.svg" download>Download SVG ↓</a></div>')
  if name=='task-loop': blocks.append('<div class="playback" hidden><div class="playback-buttons"><button type="button" id="play" aria-pressed="false">Play</button><button type="button" id="step">Next step</button><button type="button" id="reset">Reset</button></div><p class="step-status" id="step-status" aria-live="polite"></p><p class="motion-note" id="motion-note"></p></div>')
  blocks.append('</section>')
 text=gallery.read_text(); start=text.index('<!-- DIAGRAMS:START -->')+len('<!-- DIAGRAMS:START -->'); end=text.index('<!-- DIAGRAMS:END -->')
 gallery.write_text(text[:start]+'\n'+'\n'.join(blocks)+'\n '+text[end:])

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,default=Path(__file__).resolve().parents[1]/'docs/showcase/diagrams'); args=parser.parse_args();build(args.output);update_gallery(args.output)
