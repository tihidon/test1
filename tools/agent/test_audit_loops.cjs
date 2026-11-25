'use strict';
const test=require('node:test');
const assert=require('node:assert/strict');
const {analyze}=require('./audit_loops.cjs');
test('constant and ordinary loops separated',()=>{
  const r=analyze('while(true){break;} for(let i=0;i<3;i++){} for(;;){}','fixture.js');
  assert.equal(r.loops.length,2);
  assert.equal(r.counts.ForStatement,2);
});
test('name cycle candidate, not proven bug',()=>{
  const r=analyze('function a(){b()} function b(){a()} function c(){return 1}','fixture.js');
  assert.deepEqual(r.cycles.map(x=>x.owner).sort(),['a','b']);
});
test('scheduler sites and cleanup inventory',()=>{
  const r=analyze('function a(){requestAnimationFrame(a);cancelAnimationFrame(1);setInterval(a,20);clearInterval(1)}','fixture.js');
  assert.equal(r.sites.length,4);
  assert.equal(r.cycles.length,0);
});
test('invalid JS fails parsing',()=>assert.throws(()=>analyze('function {','bad.js')));
test('duplicate names are not resolved by name alone',()=>{
  const r=analyze('function a(){a()} function a(){}','fixture.js');
  assert.equal(r.cycles.length,0);
});

test('all ordinary loops have locations and nested depth',()=>{
  const r=analyze('function f(){for(let i=0;i<2;i++){while(i<1){break;}}}','fixture.js');
  assert.equal(r.loopInventory.length,2);
  assert.deepEqual(r.loopInventory.map(x=>x.nesting).sort(),[1,2]);
  assert.ok(r.loopInventory.every(x=>x.owner==='f' && x.line===1 && x.column>0));
});
test('scheduler and DOM inside loop are candidates, callback function boundary respected',()=>{
  const r=analyze('function f(){for(let i=0;i<2;i++){setTimeout(()=>{requestAnimationFrame(f)},1);el.getBoundingClientRect();}}','fixture.js');
  assert.deepEqual(r.loopOperations.map(x=>x.kind).sort(),['getBoundingClientRect','setTimeout']);
});
test('bounded while remains inventory not constant candidate',()=>{
  const r=analyze('function f(){let i=0;while(i<3){i++;}}','fixture.js');
  assert.equal(r.loopInventory.length,1);assert.equal(r.loops.length,0);
});
