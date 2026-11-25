'use strict';
// Narrow bug profile; no autofix or inline suppression.
const {Linter}=require('eslint'),fs=require('node:fs');
const {ROOT,inputs,hash}=require('./debug_source.cjs');
const RULES=['no-constant-condition','no-unreachable','no-self-assign','no-func-assign','no-async-promise-executor','no-cond-assign','no-dupe-args','no-dupe-keys','no-dupe-class-members','no-duplicate-case','use-isnan','valid-typeof','no-unmodified-loop-condition'];
function lint({file,type,source}){
 const linter=new Linter({cwd:ROOT});
 const config={languageOptions:{ecmaVersion:'latest',sourceType:type},linterOptions:{noInlineConfig:true,reportUnusedDisableDirectives:'off'},rules:Object.fromEntries(RULES.map(x=>[x,'error']))};
 const lines=source.split(/\r?\n/);
 return {file,sha256:hash(source),messages:linter.verify(source,config,{filename:file,allowInlineConfig:false}).map(m=>({rule:m.ruleId||null,fatal:!!m.fatal,severity:m.severity,message:m.message,line:m.line,column:m.column,fingerprint:hash(JSON.stringify([file,m.ruleId,m.message,(lines[(m.line||1)-1]||'').trim()]))}))};
}
function compare(before,after){
 const old=new Map(),newFindings=[],fatal=[];
 for(const f of before)for(const m of f.messages){if(m.fatal||!m.rule)fatal.push({phase:'baseline',file:f.file,...m});old.set(m.fingerprint,(old.get(m.fingerprint)||0)+1);}
 for(const f of after)for(const m of f.messages){if(m.fatal||!m.rule)fatal.push({phase:'candidate',file:f.file,...m});const n=old.get(m.fingerprint)||0;if(n)old.set(m.fingerprint,n-1);else newFindings.push({file:f.file,...m});}
 return {status:fatal.length||newFindings.length?'FAIL':'PASS_NO_NEW_FINDINGS',newFindings,fatal};
}
function main(){
 const [base,out]=process.argv.slice(2);
 if(!base||!out||Linter.version!=='10.15.0')throw Error('expected baseline SHA, output and ESLint 10.15.0');
 const baseline=inputs(ROOT,base).map(lint),candidate=inputs().map(lint),result=compare(baseline,candidate),count=a=>a.reduce((n,x)=>n+x.messages.length,0);
 fs.writeFileSync(out,JSON.stringify({base,eslint:Linter.version,rules:RULES,baseline,candidate,...result,limitation:'Selected bug rules. Fingerprints include trimmed source line; no cross-script global resolution or runtime proof.'},null,2));
 console.log(JSON.stringify({base,status:result.status,baseline:count(baseline),candidate:count(candidate),new:result.newFindings.length,fatal:result.fatal.length,files:candidate.length}));
 process.exitCode=result.status==='FAIL'?1:0;
}
module.exports={lint,compare};
if(require.main===module){try{main()}catch(e){console.error('FAIL/BLOCKED',e.message);process.exitCode=2}}
