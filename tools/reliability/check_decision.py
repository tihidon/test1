"""Bug-fix decision structure check; not a truth verifier or merge authorization."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

from check_evidence import validate

def hexstr(value, size):
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{"+str(size)+r"}", value) is not None

def check(contract, record, root):
    if not isinstance(contract, dict) or not isinstance(record, dict):
        return ["invalid contract or record"]
    errors = []
    baseline = contract.get("baseline")
    candidate = record.get("candidate")
    oracle = contract.get("oracle_sha256")
    reason = contract.get("expected_failure")
    if not hexstr(baseline,40) or not hexstr(candidate,40) or candidate == baseline:
        errors.append("distinct valid baseline and candidate required")
    if not hexstr(oracle,64) or not isinstance(reason,str) or not reason.strip():
        errors.append("invalid frozen oracle or failure reason")
    if record.get("baseline") != baseline:
        errors.append("baseline mismatch")
    required = contract.get("required")
    errors.extend(validate({"commit":candidate,"required":required},record.get("evidence"),root))
    for key, commit, status in (("before",baseline,"FAIL"),("after",candidate,"PASS")):
        phase = record.get(key)
        if not isinstance(phase,dict):
            errors.append("missing phase "+key)
            continue
        if phase.get("commit") != commit or phase.get("oracle_sha256") != oracle or phase.get("status") != status:
            errors.append("phase identity/oracle/status mismatch: "+key)
        if key == "before" and phase.get("failure_reason") != reason:
            errors.append("baseline failed for wrong reason")
        # Existing checker verifies artifact bytes; phase FAIL is represented as
        # successful capture of the expected negative control, not a test PASS.
        capture = phase.get("capture")
        errors.extend(key+": "+e for e in validate({"commit":commit,"required":["capture"]}, {"commit":commit,"checks":[capture]},root))
    divergence = record.get("first_divergence")
    if not isinstance(divergence,dict) or not all(isinstance(divergence.get(k),str) and divergence[k].strip() for k in ("symbol","anchor","caller","expected","actual")):
        errors.append("missing divergence evidence description")
    if record.get("unresolved_contradictions") != []:
        errors.append("unresolved or unreported contradictions")
    if record.get("decision") != "PRIHVATI KANDIDAT":
        errors.append("record does not request candidate acceptance")
    review=record.get("review")
    if not isinstance(review,dict) or review.get("status")!="PASS" or not isinstance(review.get("reviewer"),str) or not review["reviewer"].strip() or review.get("independent") is not True:
        errors.append("independent review declaration missing")
    return errors

def main():
    p=argparse.ArgumentParser()
    p.add_argument("contract",type=Path)
    p.add_argument("record",type=Path)
    p.add_argument("artifact_root",type=Path)
    p.add_argument("--contract-sha256",required=True)
    a=p.parse_args()
    try:
        raw=a.contract.read_bytes()
        if hashlib.sha256(raw).hexdigest()!=a.contract_sha256:
            errors=["frozen contract hash mismatch"]
        else:
            errors=check(json.loads(raw),json.loads(a.record.read_bytes()),a.artifact_root)
    except (OSError,ValueError,TypeError) as exc:
        errors=[str(exc)]
    print(json.dumps({"structural_status":"FAIL" if errors else "PASS","errors":errors,
        "independence_verified":False,"release_authorized":False,
        "limitation":"Original logs, oracle, reviewer identity and approval must be independently verified."},indent=2))
    return int(bool(errors))

if __name__=="__main__":
    sys.exit(main())
