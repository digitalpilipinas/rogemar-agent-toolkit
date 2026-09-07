import {test} from 'node:test';
import assert from 'node:assert/strict';
import {parseContract,validateContract} from './check-plan.mjs';
const valid=()=>({schema_version:1,goal:'Fix behavior',done_when:'Original repro passes',authority:{source:'User approval',allowed_actions:['edit code']},tasks:[{id:'T1',owner:'main',scope:['src/a'],depends_on:[],acceptance:['repro passes'],profile:'inherit-parent',stop_when:'environment unavailable',validation:[{check:'focused check',evidence:'result'}]}]});
test('accepts concrete contracts independent of prose punctuation and panel size',()=>{
 const c=valid(); assert.deepEqual(validateContract(parseContract('Use any style: “safe”—yes.\n```forge-contract\n'+JSON.stringify(c)+'\n```\n')),[]);
});
test('rejects missing evidence and duplicate or cyclic dependencies',()=>{
 const c=valid(); c.tasks[0].validation=[]; assert.ok(validateContract(c).length);
 const d=valid();d.tasks.push({...d.tasks[0]});assert.ok(validateContract(d).some(x=>x.includes('unique')));
 const e=valid();e.tasks[0].depends_on=['missing'];assert.ok(validateContract(e).some(x=>x.includes('unknown')));
 const f=valid();f.tasks[0].depends_on=['T1'];assert.ok(validateContract(f).some(x=>x.includes('cycle')));
});
test('does not accept model pins as a planning-time routing decision',()=>{
 const c=valid();c.tasks[0].profile='gpt-6-astra';assert.ok(validateContract(c).length);
});
