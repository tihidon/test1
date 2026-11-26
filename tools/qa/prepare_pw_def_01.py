"""Create isolated PW-DEF-01 p11 candidate. Never modify active checkout."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

BASE_SW="446a11bc377c036f2dcc5b74217a7b4a4abcab5b"
OLD="0.8.92-css-unified-p10"
NEW="0.8.92-css-unified-p11"
ROOT=Path(__file__).resolve().parents[2]

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--worktree",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    r=a.worktree.resolve()
    out=a.out.resolve()
    if r==ROOT or r.is_relative_to(ROOT) or out.is_relative_to(r) or out.is_relative_to(ROOT):
        p.error("isolated worktree and artifact directory required")
    if subprocess.check_output(["git","-C",str(r),"status","--porcelain"],text=True).strip():
        raise ValueError("worktree not clean")
    sw=(r/"sw.js").read_bytes()
    blob=hashlib.sha1(b"blob "+str(len(sw)).encode()+b"\0"+sw).hexdigest()
    if blob!=BASE_SW:raise ValueError("wrong baseline worker")
    original_html=(r/"index.html").read_bytes()
    if original_html.count(OLD.encode())!=2:raise ValueError("wrong baseline HTML version")
    for rel in ("src/js/block-00.js","src/js/block-21.js"):
        path=r/rel
        b=path.read_bytes()
        if b.count(OLD.encode())!=1:raise ValueError("unexpected version anchor "+rel)
        path.write_bytes(b.replace(OLD.encode(),NEW.encode()))
    anchor=b"    const cache=await caches.open(CACHE_NAME);"
    if sw.count(anchor)!=1:raise ValueError("unexpected install owner")
    guard=b"    // Refuse a reused namespace before any mutation; preserve the active shell.\n    if (await caches.has(CACHE_NAME)) throw Error('Offline cache name already exists: '+CACHE_NAME);\n"
    candidate=sw.replace(anchor,guard+anchor,1).replace(OLD.encode(),NEW.encode())
    (r/"sw.js").write_bytes(candidate)
    subprocess.run([sys.executable,str(r/"tools/build.py")],cwd=r,check=True,timeout=90)
    data=(r/"dist/index.html").read_bytes()
    if data!=original_html.replace(OLD.encode(),NEW.encode()):
        raise ValueError("candidate build changed beyond two version anchors")
    (r/"index.html").write_bytes(data)
    subprocess.run([sys.executable,str(r/"tools/agent/check_build.py"),"--root",str(r),"--require-publish-match"],check=True,timeout=240)
    out.mkdir(parents=True,exist_ok=False)
    paths=["index.html","sw.js","src/js/block-00.js","src/js/block-21.js"]
    report={"status":"ISOLATED_CANDIDATE_BUILT","source_commit":subprocess.check_output(["git","-C",str(r),"rev-parse","HEAD"],text=True).strip(),"dirty":True,"base_worker_blob":blob,"files":{}}
    for rel in paths:
        data=(r/rel).read_bytes()
        dst=out/rel
        dst.parent.mkdir(parents=True,exist_ok=True)
        dst.write_bytes(data)
        report["files"][rel]=hashlib.sha256(data).hexdigest()
    (out/"identity.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report),flush=True)

if __name__=="__main__":
    main()
