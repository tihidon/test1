'use strict';
// Review-only AST inventory. No runtime JS evaluation and no auto-fix.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const acorn = require('acorn');
const walk = require('acorn-walk');
const LOOP = new Set(['ForStatement','ForInStatement','ForOfStatement','WhileStatement','DoWhileStatement']);
const SITES = new Set(['requestAnimationFrame','cancelAnimationFrame','setInterval','clearInterval','setTimeout','clearTimeout','queueMicrotask','then','addEventListener','removeEventListener','observe','disconnect','ResizeObserver','MutationObserver']);
function fn(n) { return /^(?:FunctionDeclaration|FunctionExpression|ArrowFunctionExpression)$/.test(n.type); }
function name(n,p) {
  return n.id?.name || (p?.type==='VariableDeclarator' && p.id.type==='Identifier' ? p.id.name : null);
}
function analyze(src,file,sourceType='script') {
  const ast=acorn.parse(src,{ecmaVersion:'latest',sourceType,locations:true,allowHashBang:true});
  const loops=[], sites=[], funcs=[], calls=[], loopInventory=[], loopOperations=[];
  const owners=new Map();
  const counts={};
  walk.fullAncestor(ast,(n,_,anc)=>{
    if(fn(n)) { const item={node:n,name:name(n,anc.at(-2)),line:n.loc.start.line}; owners.set(n,item); funcs.push(item); }
  });
  walk.fullAncestor(ast,(n,_,anc)=>{
    const ownerNode=anc.slice(0,-1).reverse().find(fn);
    const owner=owners.get(ownerNode);
    const at={file,line:n.loc.start.line,owner:owner?.name || (owner?'anonymous@'+owner.line:'<top-level>')};
    if(LOOP.has(n.type)) {
      counts[n.type]=(counts[n.type]||0)+1;
      const own=anc.slice(0,-1).reverse();
      const boundary=own.findIndex(fn);
      const surrounding=boundary<0?own:own.slice(0,boundary);
      loopInventory.push({...at,column:n.loc.start.column+1,endLine:n.loc.end.line,type:n.type,
        nesting:1+surrounding.filter(x=>LOOP.has(x.type)).length,
        conditionType:n.test?.type??null,condition:n.test?src.slice(n.test.start,n.test.end).slice(0,160):null});
      const unconditional=n.type==='ForStatement' ? !n.test || n.test.type==='Literal' && n.test.value===true :
        (n.type==='WhileStatement'||n.type==='DoWhileStatement') && n.test.type==='Literal' && n.test.value===true;
      if(unconditional) loops.push({...at,kind:'constant-loop-candidate',type:n.type});
    }
    if(n.type==='CallExpression'||n.type==='NewExpression') {
      const c=n.callee;
      const callee=c.type==='Identifier'?c.name:c.type==='MemberExpression'&&!c.computed?c.property.name:null;
      if(SITES.has(callee)) sites.push({...at,kind:callee});
      const parents=anc.slice(0,-1).reverse();
      const boundary=parents.findIndex(fn);
      const sameFunction=boundary<0?parents:parents.slice(0,boundary);
      const enclosing=sameFunction.find(x=>LOOP.has(x.type));
      if(enclosing && (SITES.has(callee)||['getBoundingClientRect','getComputedStyle','insertAdjacentHTML','appendChild','replaceChildren'].includes(callee)))
        loopOperations.push({...at,column:n.loc.start.column+1,kind:callee,loopLine:enclosing.loc.start.line});
      if(owner?.name && c.type==='Identifier') calls.push({from:owner,to:c.name,at});
    }
  });
  // Unique named local functions only; name matching is not lexical resolution.
  const groups=new Map();
  for(const f of funcs) if(f.name) { if(!groups.has(f.name))groups.set(f.name,[]); groups.get(f.name).push(f); }
  const edges=new Map();
  for(const c of calls) if(groups.get(c.from.name)?.length===1 && groups.get(c.to)?.length===1) {
    if(!edges.has(c.from.name))edges.set(c.from.name,new Set()); edges.get(c.from.name).add(c.to);
  }
  const cycles=[];
  // Iterative reachability: one candidate per cyclic name; no recursive scanner itself.
  for(const start of edges.keys()) {
    const seen=new Set(), stack=[...(edges.get(start)||[])];
    let cycle=false;
    while(stack.length) {
      const next=stack.pop(); if(next===start){cycle=true;break;}
      if(seen.has(next))continue; seen.add(next);
      for(const child of edges.get(next)||[]) if(!seen.has(child))stack.push(child);
    }
    if(cycle)cycles.push({file,line:groups.get(start)[0].line,owner:start,kind:'name-cycle-candidate'});
  }
  return {file,sha256:crypto.createHash('sha256').update(src).digest('hex'),counts,loops,cycles,sites,loopInventory,loopOperations,functions:funcs.length};
}
function main(root) {
  const manifest=JSON.parse(fs.readFileSync(path.join(root,'src/html/blocks.json'),'utf8'));
  const executable=new Set(['','text/javascript','application/javascript','module']);
  const inputs=[];
  for(const b of manifest) {
    const type=(/\btype\s*=\s*["']([^"']*)["']/i.exec(b.open_tag)?.[1]||'').trim().toLowerCase();
    if(b.element!=='script'||!executable.has(type))continue;
    const abs=path.resolve(root,b.file);
    if(!abs.startsWith(path.resolve(root,'src')+path.sep)||!b.file.endsWith('.js'))throw Error('unexpected executable '+b.file);
    inputs.push([b.file,type==='module'?'module':'script']);
  }
  if(!inputs.length)throw Error('zero executable source blocks');
  if(new Set(inputs.map(x=>x[0])).size!==inputs.length)throw Error('duplicate executable paths');
  if(fs.existsSync(path.join(root,'sw.js')))inputs.push(['sw.js','script']);
  const reports=inputs.map(([f,t])=>analyze(fs.readFileSync(path.join(root,f),'utf8'),f,t));
  console.log(JSON.stringify({status:'PARSED_REVIEW_REQUIRED',parsedFiles:reports.length,
    limitations:'Name cycles are heuristic; aliases, property calls, shadowing and runtime termination are not resolved. Sites and nested loops are review candidates, not violations; no termination proof.',reports},null,2));
}
module.exports={analyze};
if(require.main===module){
  try{main(path.resolve(process.argv[2]||path.join(__dirname,'../..')));}
  catch(e){console.error('FAIL',e.message);process.exitCode=1;}
}
