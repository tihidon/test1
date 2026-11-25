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
