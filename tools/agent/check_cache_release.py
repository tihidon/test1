"""Read-only gate: changed shell bytes must have a changed cache identity."""
import argparse
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]

def contract(sw):
    s=sw.decode("utf-8")
    names=re.findall(r"(?m)^const CACHE_NAME\s*=\s*'([^']+)';$",s)
    arrays=re.findall(r"(?ms)^const CORE_PATHS\s*=\s*\[(.*?)\];$",s)
    if len(names)!=1 or not names[0].startswith("snail-city-shell-") or len(arrays)!=1:
        raise ValueError("unrecognized worker cache contract")
    paths=re.findall(r"'(\./[^']+)'",arrays[0])
    remainder=re.sub(r"'(\./[^']+)'","",arrays[0])
    if not paths or re.sub(r"[\s,]","",remainder) or len(set(paths))!=len(paths):
        raise ValueError("ambiguous core paths")
    for p in paths:
        q=PurePosixPath(p[2:])
        if q.is_absolute() or ".." in q.parts or str(q)!=p[2:] or not re.fullmatch(r"[A-Za-z0-9._/-]+",p[2:]):
            raise ValueError("unsafe core path")
    return names[0], {p[2:] for p in paths}

def compare(before,after):
    a,ap=contract(before("sw.js"))
    b,bp=contract(after("sw.js"))
    changed=[]
    if before("sw.js")!=after("sw.js"):
        changed.append("sw.js")
    for p in sorted(ap|bp):
        if p in ap and p in bp:
            if before(p)!=after(p):changed.append(p)
        elif p in ap:
            before(p);changed.append(p)
        else:
            after(p);changed.append(p)
    if changed and a==b:
        raise ValueError("changed shell with reused CACHE_NAME: "+", ".join(changed))
    return a,b,changed

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--base",required=True)
    p.add_argument("--root",type=Path,default=ROOT)
    a=p.parse_args()
    if not re.fullmatch("[0-9a-f]{40}",a.base) or a.base=="0"*40:
        p.error("full nonzero baseline commit required")
    root=a.root.resolve()
    try:
        subprocess.run(["git","-C",str(root),"merge-base","--is-ancestor",a.base,"HEAD"],check=True,timeout=15)
        def before(path):
            return subprocess.check_output(["git","-C",str(root),"show",a.base+":"+path],timeout=30)
        def after(path):
            p=root/path
            if p.is_symlink() or not p.is_file() or not p.resolve().is_relative_to(root):
                raise ValueError("missing or unsafe current resource: "+path)
            return p.read_bytes()
        old,new,changed=compare(before,after)
        print("PASS cache identity",old,"->",new,"changed:",changed)
    except (ValueError,OSError,subprocess.SubprocessError,UnicodeError) as exc:
        print("FAIL cache identity:",exc,file=sys.stderr)
        return 1
    return 0

if __name__=="__main__":
    raise SystemExit(main())
