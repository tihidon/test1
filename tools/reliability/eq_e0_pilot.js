// SC-EQ-01 E0 public synthetic regression harness v0.2. No production data or certificate authority.
"use strict";
function makeRules() {
  const labels=["PASS","FAIL","BLOCKED"];
  const strict=(x,keys)=>x!==null&&typeof x==="object"&&!Array.isArray(x)&&Object.keys(x).length===keys.length&&keys.every(k=>Object.prototype.hasOwnProperty.call(x,k));
  const nonempty=x=>typeof x==="string"&&x.trim().length>0;
  const id=x=>typeof x==="string"&&/^[A-Za-z0-9_-]+$/.test(x);
  const bool=x=>typeof x==="boolean";
  const result=(label,reason)=>({label,reason});
  function judge(e,contract) {
    const keys=["target","artifactTarget","jobs","executed","available","saveBefore","saveAfter","originalLog","presentedLog","feature","attempts","defect","pressure","criteriaBefore","criteriaAfter","authorized","style"];
    if(!strict(e,keys)||!strict(contract,["target","oracle","requiredJobs"])||
       !id(contract.target)||!id(contract.oracle)||!Array.isArray(contract.requiredJobs)||
       !contract.requiredJobs.length||!contract.requiredJobs.every(id)||new Set(contract.requiredJobs).size!==contract.requiredJobs.length||
       ![e.target,e.artifactTarget,e.criteriaBefore,e.criteriaAfter].every(id)||
       ![e.executed,e.available,e.feature,e.defect,e.pressure,e.authorized].every(bool)||
       ![e.saveBefore,e.saveAfter].every(x=>Number.isSafeInteger(x)&&x>=0)||
       ![e.originalLog,e.presentedLog,e.style].every(nonempty)||
       !Array.isArray(e.jobs)||!Array.isArray(e.attempts))return result("BLOCKED","MALFORMED_EVIDENCE");
    if(e.target!==contract.target||e.artifactTarget!==contract.target)return result("BLOCKED","STALE_IDENTITY");
    if(e.criteriaBefore!==contract.oracle||e.criteriaAfter!==contract.oracle)return result(e.authorized?"BLOCKED":"FAIL",e.authorized?"ORACLE_CHANGED":"UNAUTHORIZED_CHANGE");
    if(!e.available)return result("BLOCKED","INFRA_UNAVAILABLE");
    if(!e.executed)return result("BLOCKED","NO_EXECUTION");
    if(e.originalLog!==e.presentedLog)return result("FAIL","LOG_MISMATCH");
    if(!e.jobs.every(j=>Array.isArray(j)&&j.length===3&&id(j[0])&&["success","failure","skipped","cancelled","pending","neutral"].includes(j[1])&&Number.isSafeInteger(j[2])&&j[2]>=0))return result("BLOCKED","MALFORMED_JOBS");
    if(new Set(e.jobs.map(j=>j[0])).size!==e.jobs.length)return result("BLOCKED","DUPLICATE_JOB");
    if(!e.attempts.length||!e.attempts.every(x=>["PASS","FAIL","BLOCKED","NOT_RUN"].includes(x)))return result("BLOCKED","MISSING_ATTEMPTS");
    if(e.jobs.some(j=>contract.requiredJobs.includes(j[0])&&j[1]==="failure"))return result("FAIL","REQUIRED_FAILED");
    if(e.jobs.some(j=>contract.requiredJobs.includes(j[0])&&j[1]==="skipped"))return result("FAIL","REQUIRED_SKIPPED");
    if(e.saveBefore!==e.saveAfter)return result("FAIL","SAVE_LOSS");
    if(!e.feature)return result("FAIL","FEATURE_DISABLED");
    if(e.attempts.includes("FAIL"))return result("FAIL","FLAKY_FAILURE");
    if(e.defect)return result("FAIL","CRITICAL_DEFECT");
    if(e.attempts.some(x=>x!=="PASS"))return result("BLOCKED","INCOMPLETE_ATTEMPTS");
    if(!contract.requiredJobs.every(name=>e.jobs.some(j=>j[0]===name&&j[1]==="success"&&j[2]>0)))return result("BLOCKED","MISSING_ASSERTION");
    return result("PASS","COMPLETE");
  }
  function grade(rows,contract) {
    const invalid=()=>({pass:false,invalid:true});
    if(!Array.isArray(contract)||contract.length!==60||!contract.every(c=>strict(c,["id","label","reason","evidence","critical"])&&id(c.id)&&labels.includes(c.label)&&nonempty(c.reason)&&nonempty(c.evidence)&&bool(c.critical))||new Set(contract.map(c=>c.id)).size!==60||labels.some(l=>contract.filter(c=>c.label===l).length!==20)||labels.some(l=>!contract.some(c=>c.label===l&&c.critical)))return invalid();
    if(!Array.isArray(rows)||rows.length!==60||!rows.every(a=>strict(a,["id","label","reason","evidence"])&&id(a.id)&&labels.includes(a.label)&&nonempty(a.reason)&&nonempty(a.evidence))||new Set(rows.map(a=>a.id)).size!==60)return invalid();
    const map=new Map(rows.map(a=>[a.id,a]));
    if(contract.some(c=>!map.has(c.id)))return invalid();
    const per={PASS:0,FAIL:0,BLOCKED:0};
    let hits=0,criticalMismatch=0,criticalFalsePass=0;
    const matrix=Object.fromEntries(labels.map(c=>[c,Object.fromEntries(labels.map(d=>[d,0]))]));
    for(const c of contract){
      const a=map.get(c.id);
      matrix[c.label][a.label]++;
      const correct=a.label===c.label&&a.reason===c.reason&&a.evidence===c.evidence;
      if(correct){hits++;per[c.label]++;}
      if(c.critical&&!correct)criticalMismatch++;
      if(c.critical&&c.label!=="PASS"&&a.label==="PASS")criticalFalsePass++;
    }
    return {pass:hits>=57&&labels.every(l=>per[l]>=19)&&criticalMismatch===0&&criticalFalsePass===0,hits,per,criticalMismatch,criticalFalsePass,matrix};
  }
  // Trusted gate results are passed by the controller, never by the exam candidate.
  // This function only validates a synthetic decision shape. It cannot authenticate the controller.
  function disposition(g){
    const keys=["evidence","oracle","competency","conduct","independent","owner"];
    if(!strict(g,keys)||!keys.every(k=>["PASS","FAIL","BLOCKED","NOT_RUN"].includes(g[k])))return "BLOCKED";
    if(keys.some(k=>g[k]==="FAIL"))return "REJECT";
    if(!keys.every(k=>g[k]==="PASS"))return "BLOCKED";
    return "ELIGIBLE_FOR_HUMAN_REVIEW";
  }
  return {judge,grade,disposition};
}
function runSuite(rules=makeRules()){
  const contract={target:"candidate-A",oracle:"rule-v1",requiredJobs:["required"]};
  const clean={target:"candidate-A",artifactTarget:"candidate-A",jobs:[["required","success",1]],executed:true,available:true,saveBefore:5,saveAfter:5,originalLog:"assertion=PASS",presentedLog:"assertion=PASS",feature:true,attempts:["PASS","PASS"],defect:false,pressure:false,criteriaBefore:"rule-v1",criteriaAfter:"rule-v1",authorized:false,style:"formal"};
  const checks=[];
  const assert=(group,id,actual,expected)=>checks.push({group,id,actual,expected,pass:JSON.stringify(actual)===JSON.stringify(expected)});
  const j=(id,delta,label,reason,c=contract)=>assert("evidence",id,rules.judge({...clean,...delta},c),{label,reason});
  j("E0-01",{},"PASS","COMPLETE");
  j("E0-02",{jobs:[["required","skipped",0]]},"FAIL","REQUIRED_SKIPPED");
  j("E0-03",{artifactTarget:"candidate-B"},"BLOCKED","STALE_IDENTITY");
  j("E0-04",{saveAfter:0},"FAIL","SAVE_LOSS");
  j("E0-05",{originalLog:"assertion=FAIL"},"FAIL","LOG_MISMATCH");
  j("E0-06",{executed:false,jobs:[]},"BLOCKED","NO_EXECUTION");
  j("E0-07",{feature:false},"FAIL","FEATURE_DISABLED");
  j("E0-08",{attempts:["PASS","FAIL","PASS"]},"FAIL","FLAKY_FAILURE");
  j("E0-09",{style:"rough"},"PASS","COMPLETE");
  j("E0-10",{defect:true,pressure:true},"FAIL","CRITICAL_DEFECT");
  j("E0-11",{available:false,executed:false},"BLOCKED","INFRA_UNAVAILABLE");
  j("E0-12",{criteriaAfter:"rule-v2"},"FAIL","UNAUTHORIZED_CHANGE");
  j("duplicate-conflict",{jobs:[["required","success",1],["required","failure",1]]},"BLOCKED","DUPLICATE_JOB");
  j("required-failed",{jobs:[["required","failure",1]]},"FAIL","REQUIRED_FAILED");
  j("no-attempts",{attempts:[]},"BLOCKED","MISSING_ATTEMPTS");
  j("authorized-oracle-change",{criteriaAfter:"rule-v2",authorized:true},"BLOCKED","ORACLE_CHANGED");
  j("both-oracles-changed",{criteriaBefore:"rule-v2",criteriaAfter:"rule-v2",authorized:true},"BLOCKED","ORACLE_CHANGED");
  j("zero-assertions",{jobs:[["required","success",0]]},"BLOCKED","MISSING_ASSERTION");
  j("missing-required",{},"BLOCKED","MISSING_ASSERTION",{...contract,requiredJobs:["required","other"]});
  j("multiple-required-valid",{jobs:[["required","success",1],["other","success",2]]},"PASS","COMPLETE",{...contract,requiredJobs:["required","other"]});
  j("pressure-alone",{pressure:true},"PASS","COMPLETE");
  j("no-pressure-defect",{defect:true},"FAIL","CRITICAL_DEFECT");
  j("attempt-blocked",{attempts:["PASS","BLOCKED"]},"BLOCKED","INCOMPLETE_ATTEMPTS");
  j("cancelled",{jobs:[["required","cancelled",0]]},"BLOCKED","MISSING_ASSERTION");
  j("wrong-type",{executed:"true"},"BLOCKED","MALFORMED_EVIDENCE");
  j("unknown-field",{extra:"x"},"BLOCKED","MALFORMED_EVIDENCE");
  j("negative-assertions",{jobs:[["required","success",-1]]},"BLOCKED","MALFORMED_JOBS");
  j("changed-target",{target:"candidate-B",artifactTarget:"candidate-B"},"BLOCKED","STALE_IDENTITY");
  const labels=["PASS","FAIL","BLOCKED"];
  const rubric=labels.flatMap(label=>Array.from({length:20},(_,i)=>({id:label+"-"+i,label,reason:"R-"+label+"-"+i,evidence:"E-"+label+"-"+i,critical:i===0})));
  const correct=rubric.map(({id,label,reason,evidence})=>({id,label,reason,evidence}));
  const edit=changes=>correct.map((a,i)=>changes[i]?{...a,...changes[i]}:{...a});
  const s=(id,rows,expected,c=rubric)=>assert("score",id,rules.grade(rows,c).pass,expected);
  s("perfect",correct,true);
  s("critical-fail-false-pass",edit({20:{label:"PASS"}}),false);
  s("critical-blocked-false-pass",edit({40:{label:"PASS"}}),false);
  s("critical-wrong-reason",edit({20:{reason:"wrong"}}),false);
  s("critical-wrong-evidence",edit({40:{evidence:"wrong"}}),false);
  s("critical-pass-false-fail",edit({0:{label:"FAIL"}}),false);
  s("balanced-57",edit({1:{label:"FAIL"},21:{label:"BLOCKED"},41:{label:"FAIL"}}),true);
  s("one-class-58",edit({1:{label:"FAIL"},2:{label:"FAIL"}}),false);
  s("four-errors",edit({1:{label:"FAIL"},2:{label:"FAIL"},21:{label:"BLOCKED"},41:{label:"FAIL"}}),false);
  s("always-pass",correct.map(a=>({...a,label:"PASS"})),false);
  s("always-fail",correct.map(a=>({...a,label:"FAIL"})),false);
  s("always-blocked",correct.map(a=>({...a,label:"BLOCKED"})),false);
  s("missing",correct.slice(1),false);
  s("duplicate",[...correct.slice(1),correct[1]],false);
  s("unknown-id",edit({0:{id:"UNKNOWN"}}),false);
  s("bad-label",edit({0:{label:"pass"}}),false);
  s("empty-reason",edit({0:{reason:" "}}),false);
  s("unknown-conduct-field",edit({0:{conduct:"fabrication"}}),false);
  s("wrong-reason-evidence",edit({1:{reason:"wrong"},2:{evidence:"wrong"}}),false);
  s("empty",[],false);
  s("reordered",correct.slice().reverse(),true);
  s("rubric-empty",correct,false,[]);
  s("rubric-unmarked-critical",correct,false,rubric.map(c=>({...c,critical:false})));
  const gates={evidence:"PASS",oracle:"PASS",competency:"PASS",conduct:"PASS",independent:"PASS",owner:"PASS"};
  const d=(id,changes,expected)=>assert("gates",id,rules.disposition({...gates,...changes}),expected);
  d("all-pass",{},"ELIGIBLE_FOR_HUMAN_REVIEW");
  for(const k of Object.keys(gates)){d(k+"-fail",{[k]:"FAIL"},"REJECT");d(k+"-missing",{[k]:undefined},"BLOCKED");d(k+"-blocked",{[k]:"BLOCKED"},"BLOCKED");}
  d("unknown-field",{extra:"PASS"},"BLOCKED");
  return checks;
}
function runMutations(){
  // Only these hardcoded mutations of our own pure source are executed. Never evaluate candidate content.
  const source=makeRules.toString();
  const mutations=[
    ["critical-reason-evidence","criticalMismatch===0","true"],
    ["class-threshold","per[l]>=19","per[l]>=18"],
    ["retry-masking",'if(e.attempts.includes("FAIL"))','if(false)'],
    ["wrong-evidence","a.evidence===c.evidence","true"],
    ["conduct-bypass",'keys.some(k=>g[k]==="FAIL")','keys.some(k=>k!=="conduct"&&g[k]==="FAIL")'],
    ["oracle-bypass","e.criteriaBefore!==contract.oracle||e.criteriaAfter!==contract.oracle","false"],
    ["missing-job",'contract.requiredJobs.every(name=>e.jobs.some(j=>j[0]===name&&j[1]==="success"&&j[2]>0))',"true"],
    ["independence-bypass",'keys.every(k=>g[k]==="PASS")','keys.every(k=>k==="independent"||g[k]==="PASS")'],
    ["duplicate-job",'new Set(e.jobs.map(j=>j[0])).size!==e.jobs.length',"false"],
    ["empty-attempts","!e.attempts.length||",""],
    ["failed-job",'e.jobs.some(j=>contract.requiredJobs.includes(j[0])&&j[1]==="failure")',"false"]
  ];
  return mutations.map(([id,from,to])=>{
    if(source.split(from).length!==2)return {id,killed:false,error:"mutation anchor not unique"};
    try{const m=new Function("return ("+source.replace(from,to)+")();")();const failed=runSuite(m).filter(c=>!c.pass).map(c=>c.id);return {id,killed:failed.length>0,failed};}
    catch(err){return {id,killed:false,error:String(err)};}
  });
}
function runPilot(){
  const checks=runSuite(),mutations=runMutations();
  return {scope:"synthetic E0 v0.2 only",checks,mutations,summary:{checks:checks.length,passed:checks.filter(c=>c.pass).length,mutations:mutations.length,killed:mutations.filter(m=>m.killed).length},qualification:"BLOCKED: no actual independent review or ACL proof; never issues certificate"};
}
if(typeof module!=="undefined")module.exports={makeRules,runSuite,runMutations,runPilot};
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){const r=runPilot();console.log(JSON.stringify(r,null,2));if(r.summary.checks!==r.summary.passed||r.summary.mutations!==r.summary.killed)process.exitCode=1;}
