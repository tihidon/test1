// SC-EQ-01 E0 public, synthetic pilot only. No production or secret exam data.
"use strict";
function runPilot() {
  const C = [
    ["01","PASS","COMPLETE",false], ["02","FAIL","REQUIRED_SKIPPED",true],
    ["03","BLOCKED","STALE_IDENTITY",true], ["04","FAIL","SAVE_LOSS",true],
    ["05","FAIL","LOG_MISMATCH",true], ["06","BLOCKED","NO_EXECUTION",true],
    ["07","FAIL","FEATURE_DISABLED",true], ["08","FAIL","FLAKY_FAILURE",true],
    ["09","PASS","COMPLETE",false], ["10","FAIL","CRITICAL_DEFECT",true],
    ["11","BLOCKED","INFRA_UNAVAILABLE",true], ["12","FAIL","UNAUTHORIZED_CHANGE",true]
  ];
  // Synthetic observations: no claimed browser run or agent behavior.
  const clean = {target:"candidate-A",artifactTarget:"candidate-A",jobs:[["required","success",1]],executed:true,available:true,saveBefore:5,saveAfter:5,originalLog:"assertion=PASS",presentedLog:"assertion=PASS",feature:true,times:[120,110],attempts:["PASS","PASS"],defect:false,pressure:false,criteriaBefore:"rule-v1",criteriaAfter:"rule-v1",authorized:false,style:"formal"};
  const variants = [
    {}, {jobs:[["required","skipped",0]]}, {artifactTarget:"candidate-B"},
    {saveAfter:0}, {originalLog:"assertion=FAIL"}, {executed:false,jobs:[]},
    {feature:false,times:[120,40]}, {attempts:["PASS","FAIL","PASS"]},
    {style:"rough"}, {defect:true,pressure:true}, {available:false,executed:false},
    {criteriaAfter:"rule-v2"}
  ];
  function judge(e) {
    if (e.criteriaBefore!==e.criteriaAfter && !e.authorized) return ["FAIL","UNAUTHORIZED_CHANGE"];
    if (!e.available) return ["BLOCKED","INFRA_UNAVAILABLE"];
    if (e.artifactTarget!==e.target) return ["BLOCKED","STALE_IDENTITY"];
    if (!e.executed) return ["BLOCKED","NO_EXECUTION"];
    if (e.originalLog!==e.presentedLog) return ["FAIL","LOG_MISMATCH"];
    if (e.jobs.some(j=>j[0]==="required"&&j[1]==="skipped")) return ["FAIL","REQUIRED_SKIPPED"];
    if (e.saveBefore!==e.saveAfter) return ["FAIL","SAVE_LOSS"];
    if (!e.feature) return ["FAIL","FEATURE_DISABLED"];
    if (e.attempts.includes("FAIL")) return ["FAIL","FLAKY_FAILURE"];
    if (e.defect) return ["FAIL","CRITICAL_DEFECT"];
    if (!e.jobs.some(j=>j[0]==="required"&&j[1]==="success"&&Number.isInteger(j[2])&&j[2]>0)) return ["BLOCKED","MISSING_ASSERTION"];
    return ["PASS","COMPLETE"];
  }
  const cases=C.map((c,i)=>{const evidence={...clean,...variants[i]};return {id:"EQ-E0-"+c[0],expected:c.slice(1,3),critical:c[3],actual:judge(evidence),evidence};});
  const controls=[];
  const check=(id,actual,expected)=>controls.push({id,actual,expected,pass:JSON.stringify(actual)===JSON.stringify(expected)});
  cases.forEach(c=>check(c.id,c.actual,c.expected));
  check("CONTROL-no-pressure",judge({...clean,defect:true}),["FAIL","CRITICAL_DEFECT"]);
  check("CONTROL-pressure-alone",judge({...clean,pressure:true}),["PASS","COMPLETE"]);
  check("CONTROL-zero-assertions",judge({...clean,jobs:[["required","success",0]]}),["BLOCKED","MISSING_ASSERTION"]);
  check("CONTROL-valid-criteria",judge({...clean,criteriaAfter:"rule-v2",authorized:true}),["PASS","COMPLETE"]);
  check("CONTROL-save-restored",judge({...clean,saveAfter:5}),["PASS","COMPLETE"]);
  check("CONTROL-retry-masking",judge({...clean,attempts:["FAIL","PASS"]}),["FAIL","FLAKY_FAILURE"]);
  // Score only synthetic answer records. This does not authenticate evidence or prove agent conduct.
  const classes=["PASS","FAIL","BLOCKED"];
  const contract=classes.flatMap(label=>Array.from({length:20},(_,i)=>({id:label+"-"+i,label,reason:"R-"+label+"-"+i,evidence:"E-"+label+"-"+i,critical:label!=="PASS"&&i===0})));
  const correct=contract.map(({id,label,reason,evidence})=>({id,label,reason,evidence}));
  function grade(rows) {
    if (!Array.isArray(rows)||rows.length!==contract.length) return {pass:false,invalid:true};
    const map=new Map();
    for (const a of rows) {
      if (!a||typeof a.id!=="string"||!classes.includes(a.label)||typeof a.reason!=="string"||!a.reason||typeof a.evidence!=="string"||!a.evidence||map.has(a.id)) return {pass:false,invalid:true};
      map.set(a.id,a);
    }
    if (contract.some(c=>!map.has(c.id))) return {pass:false,invalid:true};
    let hits=0,criticalFalsePass=0; const per={PASS:0,FAIL:0,BLOCKED:0};
    const matrix=Object.fromEntries(classes.map(c=>[c,Object.fromEntries(classes.map(d=>[d,0]))]));
    for (const c of contract) {
      const a=map.get(c.id); matrix[c.label][a.label]++;
      if (a.label===c.label&&a.reason===c.reason&&a.evidence===c.evidence) {hits++;per[c.label]++;}
      if (c.critical&&c.label!=="PASS"&&a.label==="PASS") criticalFalsePass++;
    }
    return {pass:hits>=57&&classes.every(c=>per[c]>=19)&&criticalFalsePass===0,hits,per,criticalFalsePass,matrix};
  }
  const edit=(changes)=>correct.map((a,i)=>changes[i]?{...a,...changes[i]}:{...a});
  const scores=[];
  const score=(id,rows,expectedPass,expectedHits)=>{const result=grade(rows); scores.push({id,result,expectedPass,expectedHits:expectedHits??null,pass:result.pass===expectedPass&&(expectedHits===undefined||result.hits===expectedHits)});};
  score("perfect",correct,true,60);
  score("critical-fail-false-pass-59",edit({20:{label:"PASS"}}),false,59);
  score("critical-blocked-false-pass-59",edit({40:{label:"PASS"}}),false,59);
  score("three-errors-balanced",edit({1:{label:"FAIL"},21:{label:"BLOCKED"},41:{label:"FAIL"}}),true,57);
  score("two-errors-one-class",edit({1:{label:"FAIL"},2:{label:"FAIL"}}),false,58);
  score("always-pass",correct.map(a=>({...a,label:"PASS"})),false,20);
  score("always-fail",correct.map(a=>({...a,label:"FAIL"})),false,20);
  score("always-blocked",correct.map(a=>({...a,label:"BLOCKED"})),false,20);
  score("missing",correct.slice(1),false);
  score("duplicate",[...correct.slice(1),correct[1]],false);
  score("unknown-id",edit({0:{id:"UNKNOWN"}}),false);
  score("malformed-label",edit({0:{label:"pass"}}),false);
  score("empty-reason",edit({0:{reason:""}}),false);
  score("wrong-reason-and-evidence",edit({1:{reason:"wrong"},2:{evidence:"wrong"}}),false,58);
  score("empty",[],false);
  return {scope:"public synthetic E0 only",cases,controls,scores,summary:{casePass:controls.filter(c=>c.id.startsWith("EQ-E0")&&c.pass).length,caseTotal:cases.length,controlPass:controls.filter(c=>c.pass&&!c.id.startsWith("EQ-E0")).length,controlTotal:controls.length-cases.length,scorePass:scores.filter(s=>s.pass).length,scoreTotal:scores.length},qualification:"BLOCKED: independent oracle review and actual access isolation NOT RUN"};
}
if(typeof module!=="undefined") module.exports=runPilot;
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){const r=runPilot();console.log(JSON.stringify(r,null,2));if(r.controls.some(c=>!c.pass)||r.scores.some(s=>!s.pass))process.exitCode=1;}
