#!/usr/bin/env node
import fs from 'node:fs';
import { pathToFileURL } from 'node:url';

export function parseContract(text) {
  if (text.trimStart().startsWith('{')) return JSON.parse(text);
  const blocks = [...text.matchAll(/^```forge-contract\s*\n([\s\S]*?)^```\s*$/gm)];
  if (blocks.length !== 1) throw new Error('Expected one forge-contract JSON block, or a JSON file.');
  return JSON.parse(blocks[0][1]);
}
export function validateContract(c) {
  const errors = [];
  const nonempty = v => typeof v === 'string' && v.trim().length > 0;
  const strings = v => Array.isArray(v) && v.length > 0 && v.every(nonempty);
  if (!c || typeof c !== 'object' || Array.isArray(c)) return ['Contract must be an object.'];
  if (c.schema_version !== 1) errors.push('schema_version must be 1.');
  if (!nonempty(c.goal)) errors.push('A concrete goal is required.');
  if (!nonempty(c.done_when)) errors.push('done_when must name observable completion evidence.');
  if (!c.authority || !nonempty(c.authority.source) || !strings(c.authority.allowed_actions))
    errors.push('authority needs a source and nonempty allowed_actions.');
  if (!Array.isArray(c.tasks) || c.tasks.length === 0) return [...errors, 'At least one task is required.'];
  const ids = new Set();
  for (const t of c.tasks) {
    if (!t || typeof t !== 'object' || Array.isArray(t)) { errors.push('Task must be an object.'); continue; }
    if (!nonempty(t.id) || ids.has(t.id)) errors.push('Task IDs must be nonempty and unique.');
    ids.add(t.id);
    for (const k of ['owner', 'stop_when']) if (!nonempty(t[k])) errors.push(`${t.id}: ${k} is required.`);
    for (const k of ['scope', 'acceptance']) if (!strings(t[k])) errors.push(`${t.id}: ${k} needs nonempty strings.`);
    if (!Array.isArray(t.depends_on) || !t.depends_on.every(nonempty)) errors.push(`${t.id}: depends_on must be an array of task IDs.`);
    if (!Array.isArray(t.validation) || !t.validation.length || t.validation.some(v =>
      !v || !nonempty(v.check) || !nonempty(v.evidence))) errors.push(`${t.id}: validation needs check and evidence for every entry.`);
    if (t.profile !== 'inherit-parent') errors.push(`${t.id}: profile must be inherit-parent; resolve justified worker overrides at dispatch.`);
  }
  const tasks = new Map(c.tasks.filter(t => t && typeof t === 'object').map(t => [t.id, t]));
  const visiting = new Set(), visited = new Set();
  function visit(id) {
    if (visiting.has(id)) { errors.push(`Dependency cycle at ${id}.`); return; }
    if (visited.has(id)) return;
    visiting.add(id);
    const deps = tasks.get(id)?.depends_on;
    for (const d of Array.isArray(deps) ? deps : []) {
      if (!ids.has(d)) errors.push(`${id}: unknown dependency ${d}.`);
      else visit(d);
    }
    visiting.delete(id); visited.add(id);
  }
  for (const id of ids) visit(id);
  return [...new Set(errors)];
}
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try {
    if (!process.argv[2]) throw new Error('Usage: node check-plan.mjs <plan.md|contract.json>');
    const errors = validateContract(parseContract(fs.readFileSync(process.argv[2], 'utf8')));
    console.log(JSON.stringify({status: errors.length ? 'invalid' : 'structurally-valid', errors,
      execution_verified: false, authority_verified: false}));
    process.exitCode = errors.length ? 1 : 0;
  } catch (error) { console.error(error.message); process.exitCode = 2; }
}
