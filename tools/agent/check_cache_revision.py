"""PW-01: changed SW or cached bytes require a new namespace vs the actual baseline."""
import argparse
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NAME = re.compile(r"(?m)^const CACHE_NAME = '([a-zA-Z0-9._-]+)';$")
CORE = re.compile(r"(?ms)^const CORE_PATHS = \[(.*?)^\];$")
PATH = re.compile(r"'(\./[a-zA-Z0-9_./-]+)'")

def inventory(text):
    names = NAME.findall(text)
    arrays = CORE.findall(text)
    if len(names) != 1 or len(arrays) != 1:
        raise ValueError("ambiguous SW cache inventory")
    paths = PATH.findall(arrays[0])
    if not paths or PATH.sub("", arrays[0]).strip(" \t\r\n,"):
        raise ValueError("unsupported SW core inventory syntax")
    rel = [p[2:] for p in paths]
    if len(set(rel)) != len(rel) or any(not p or any(part in ("", ".", "..") for part in p.split("/")) for p in rel):
        raise ValueError("invalid or duplicate core path")
    return names[0], set(rel)

def evaluate(old, new, changed):
    old_name, old_paths = inventory(old)
    new_name, new_paths = inventory(new)
    relevant = sorted(set(changed) & (old_paths | new_paths | {"sw.js"}))
    if relevant and old_name == new_name:
        raise ValueError("changed shell without new CACHE_NAME: "+", ".join(relevant))
    return relevant, old_name, new_name

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--base", required=True)
    a = p.parse_args()
    try:
        if not re.fullmatch(r"[0-9a-f]{40}", a.base) or a.base == "0"*40:
            raise ValueError("full nonzero baseline commit SHA required")
        def git(*args):
            return subprocess.check_output(["git", *args], cwd=ROOT, timeout=45)
        git("merge-base", "--is-ancestor", a.base, "HEAD")
        old = git("show", a.base+":sw.js").decode("utf-8")
        new = (ROOT/"sw.js").read_text(encoding="utf-8")
        _, op = inventory(old)
        _, np = inventory(new)
        changed = git("diff", "--name-only", "-z", a.base, "HEAD", "--", *sorted(op | np | {"sw.js"})).decode("utf-8").split("\0")
        relevant, before, after = evaluate(old, new, changed)
        print("PASS PW-01 cache revision", a.base, before, after, relevant)
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        print("FAIL PW-01 cache revision:", exc)
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
