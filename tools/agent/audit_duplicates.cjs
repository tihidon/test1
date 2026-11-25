'use strict';
const fs=require('node:fs'),acorn=require('acorn'),walk=require('acorn-walk');
const {inputs,hash}=require('./debug_source.cjs');
const FN=new Set(['FunctionDeclaration','FunctionExpression','ArrowFunctionExpression']);
function scan({file,source,type}){
 const ast=acorn.parse(source,{ecmaVersion:'latest',sourceType:type,locations:true,allowHashBang:true}),functions=[];
 walk.fullAncestor(ast,(n,_,anc)=>{
  if(!FN.has(n.type))return;
  const p=anc.at(-2),name=n.id?.name||p?.id?.name||p?.key?.name||p?.key?.value||'(anonymous)',chars=n.end-n.start;
  let nodes=0;walk.full(n,()=>nodes++);
  const f={file,name,line:n.loc.start.line,column:n.loc.start.column+1,endLine:n.loc.end.line,lines:n.loc.end.line-n.loc.start.line+1,chars,nodes,hash:null};
  if(nodes>=12&&chars<=100000)f.hash=hash(JSON.stringify({type:n.type,async:n.async,generator:n.generator,params:n.params,body:n.body},(k,v)=>['start','end','loc'].includes(k)?undefined:typeof v==='bigint'?v.toString()+'n':v));
  functions.push(f);
 });
 return {file,sha256:hash(source),functions};
}
function clusters(reports){
 const g=new Map();for(const r of reports)for(const f of r.functions)if(f.hash){if(!g.has(f.hash))g.set(f.hash,[]);g.get(f.hash).push(f);}
 return [...g].filter(([,a])=>a.length>1).map(([hash,members])=>({hash,members}));
}
function main(){
 const reports=inputs().map(scan),all=reports.flatMap(r=>r.functions),duplicates=clusters(reports);
 fs.writeFileSync(process.argv[2],JSON.stringify({status:'REVIEW_REQUIRED',parsedFiles:reports.length,functions:all.length,excludedSmallOrLarge:all.filter(f=>!f.hash).length,duplicates,largest:all.sort((a,b)=>b.chars-a.chars).slice(0,30),limitation:'Exact AST bodies/parameters/type. No alpha-renaming or semantic equivalence. Different bindings/closure/owners may be legitimate.'},null,2));
 console.log(JSON.stringify({parsedFiles:reports.length,functions:all.length,clusters:duplicates.length}));
}
module.exports={scan,clusters};
if(require.main===module){try{main()}catch(e){console.error('FAIL/BLOCKED',e.message);process.exitCode=2}}
