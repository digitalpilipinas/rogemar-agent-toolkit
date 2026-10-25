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
test('ignores a contract inside an enclosing Markdown example',()=>{
 const sample='````markdown\n```forge-contract\n'+JSON.stringify(valid())+'\n```\n````\n';
 assert.throws(()=>parseContract(sample),/Expected one/);
 const live=valid();live.goal='Actual task';
 assert.equal(parseContract(sample+'```forge-contract\n'+JSON.stringify(live)+'\n```\n').goal,'Actual task');
});
test('supports matching fence characters, lengths, indentation and CRLF',()=>{
 for(const fence of ['```','````','~~~','~~~~']){
  const input='   '+fence+'forge-contract\r\n'+JSON.stringify(valid())+'\r\n   '+fence+'\r\n';
  assert.deepEqual(parseContract(input),valid());
 }
});
test('does not close on short or mismatched fences or accept unclosed contracts',()=>{
 for(const close of ['```','~~~~','```` trailing']){
  assert.throws(()=>parseContract('````forge-contract\n'+JSON.stringify(valid())+'\n'+close+'\n'),/Unclosed/);
 }
});
test('rejects multiple actual contracts and ignores non-contract fences',()=>{
 const block='```forge-contract\n'+JSON.stringify(valid())+'\n```\n';
 assert.throws(()=>parseContract(block+block),/Expected one/);
 assert.deepEqual(parseContract('~~~text\n```forge-contract\nnot json\n```\n~~~\n'+block),valid());
});
