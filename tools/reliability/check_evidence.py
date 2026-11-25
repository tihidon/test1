"""Structural evidence gate, not a truth verifier or LLM judge."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

def validate(contract, evidence, root):
    errors=[]
    if not isinstance(contract,dict) or not isinstance(evidence,dict):
        return ["contract and evidence must be objects"]
    commit=contract.get("commit")
    if not isinstance(commit,str) or not re.fullmatch(r"[0-9a-f]{40}",commit):
        errors.append("invalid contract commit")
    if evidence.get("commit")!=commit:
        errors.append("commit mismatch")
    required=contract.get("required")
    if (not isinstance(required,list) or not required or
        not all(isinstance(x,str) and x.strip() for x in required) or
        len(set(required))!=len(required)):
        return errors+["invalid required checks"]
    checks=evidence.get("checks")
    if not isinstance(checks,list):
        return errors+["invalid checks"]
    seen={}
    for check in checks:
        if not isinstance(check,dict) or not isinstance(check.get("id"),str):
            errors.append("invalid check")
            continue
        ident=check["id"]
        if ident in seen:
            errors.append("duplicate check: "+ident)
        seen[ident]=check
    root=root.resolve()
    for ident in required:
        c=seen.get(ident)
        if c is None:
            errors.append("missing check: "+ident)
            continue
        if c.get("status")!="PASS" or type(c.get("exit_code")) is not int or c["exit_code"]!=0:
            errors.append("nonpassing check: "+ident)
        if not isinstance(c.get("command"),str) or not c["command"].strip():
            errors.append("missing command: "+ident)
        rel=c.get("artifact")
        digest=c.get("sha256")
        if not isinstance(rel,str) or not rel or Path(rel).is_absolute():
            errors.append("invalid artifact path: "+ident)
            continue
        try:
            path=(root/rel).resolve()
            if not path.is_relative_to(root) or not path.is_file() or path.stat().st_size==0:
                raise ValueError("missing, empty or outside artifact root")
            if not isinstance(digest,str) or not re.fullmatch(r"[0-9a-f]{64}",digest):
                raise ValueError("invalid hash")
            h=hashlib.sha256()
            with path.open("rb") as f:
                for chunk in iter(lambda:f.read(1024*1024),b""):
                    h.update(chunk)
            if h.hexdigest()!=digest:
                raise ValueError("artifact hash mismatch")
        except (OSError,ValueError,RuntimeError) as exc:
            errors.append(f"{ident}: {exc}")
    return errors

def main():
    p=argparse.ArgumentParser()
    p.add_argument("contract",type=Path)
    p.add_argument("evidence",type=Path)
    p.add_argument("artifact_root",type=Path)
    a=p.parse_args()
    try:
        errors=validate(json.loads(a.contract.read_text(encoding="utf-8")),
                        json.loads(a.evidence.read_text(encoding="utf-8")),a.artifact_root)
    except (OSError,ValueError,TypeError) as exc:
        errors=[str(exc)]
    print(json.dumps({"structural_status":"FAIL" if errors else "PASS",
                      "behavioral_status":"NOT_RUN","errors":errors,
                      "limitation":"Independent original evidence review required."},indent=2))
    return int(bool(errors))

if __name__=="__main__":
    sys.exit(main())
