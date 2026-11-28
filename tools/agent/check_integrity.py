#!/usr/bin/env python3
"""SC-INTEGRITY-01: read-only Git tree gate, never executes candidate code."""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

SHA = re.compile(r"[0-9a-f]{40}\Z")
REPOS = {"tihidon/test1", "tihidon/test-cl1"}
COMMON = {
    "index.html", "sw.js", "manifest.webmanifest", "_headers",
    "privacy.html", "delete-account.html", "img/icon-192.png",
    "img/icon-512.png", "img/icon-maskable.png", "src/html/blocks.json",
    "src/html/index.template.html", "tools/build.py", "netlify.toml",
    "AGENTS.md", ".github/workflows/engineering-gates.yml",
    ".github/workflows/chrome-devtools-mcp.yml",
}
CLOUDFLARE = {"_redirects", "wrangler.toml", "tools/cloudflare-build.sh"}

class Blocked(Exception):
    pass

def git(root, *args):
    try:
        return subprocess.run(
            ["git", "-C", str(root), *args], check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60,
        ).stdout
    except (OSError, subprocess.SubprocessError) as exc:
        raise Blocked("Git operation failed: " + " ".join(args[:2])) from exc

def commit(root, sha):
    if not SHA.fullmatch(sha):
        raise Blocked("Expected a full 40-character commit SHA")
    if git(root, "rev-parse", "--verify", sha + "^{commit}").decode().strip() != sha:
        raise Blocked("Commit identity mismatch")
    return sha

def inventory(root, sha):
    result = {}
    for record in git(root, "ls-tree", "-r", "-l", "-z", "--full-tree", sha).split(b"\0"):
        if not record:
            continue
        try:
            meta, name = record.split(b"\t", 1)
            mode, kind, oid, size = meta.decode("ascii").split()
            path = name.decode("utf-8", errors="strict")
            if path in result or not SHA.fullmatch(oid):
                raise ValueError("duplicate path or invalid object")
            result[path] = {"mode": mode, "type": kind, "oid": oid,
                            "size": int(size) if size != "-" else None}
        except (ValueError, UnicodeError) as exc:
            raise Blocked("Malformed or unsupported Git inventory") from exc
    if not result:
        raise Blocked("Empty Git inventory")
    return result

def regular(entry):
    return (entry is not None and entry["type"] == "blob"
            and entry["mode"] in ("100644", "100755")
            and isinstance(entry["size"], int) and entry["size"] > 0)

def compare(repo, base, head, old, new, approved=None, require_scope=False):
    if repo not in REPOS:
        raise Blocked("Unknown repository identity")
    protected = COMMON | (CLOUDFLARE if repo.endswith("/test-cl1") else set())
    protected |= {p for p in old if p.startswith(("src/", ".github/workflows/"))
                  or p in ("tools/agent/check_integrity.py", "tools/agent/test_integrity.py")}
    changes = []
    for path in sorted(old.keys() | new.keys()):
        a, b = old.get(path), new.get(path)
        if a == b:
            continue
        kind = "A" if a is None else "D" if b is None else (
            "T" if (a["mode"], a["type"]) != (b["mode"], b["type"]) else "M")
        changes.append({"path": path, "kind": kind, "before": a, "after": b})
    identity = {"repository": repo, "base": base, "head": head}
    scope = {**identity, "changes": changes}
    failures = []
    if require_scope and approved is None:
        raise Blocked("External approved scope is required")
    if approved is not None and approved != scope:
        failures.append({"code": "SCOPE_MISMATCH", "path": None})
    for path in sorted(protected):
        if not regular(new.get(path)):
            failures.append({"code": "PROTECTED_MISSING_OR_INVALID", "path": path})
    for c in changes:
        p, k, after = c["path"], c["kind"], c["after"]
        if k in ("D", "T") and approved is None:
            failures.append({"code": "DELETION_OR_MODE_CHANGE", "path": p})
        if after is not None and (after["type"] != "blob"
                                  or after["mode"] not in ("100644", "100755")):
            failures.append({"code": "UNSUPPORTED_OBJECT", "path": p})
    sensitive = [c["path"] for c in changes if c["path"].startswith(
        (".github/", "tools/", ".agents/", "docs/tehnika/standardi/"))
        or c["path"] in ("AGENTS.md", "netlify.toml", "wrangler.toml")]
    return {**identity, "status": "FAIL" if failures else "PASS",
            "level": "EXACT_SCOPE_MATCH" if approved is not None else "STRUCTURAL_ONLY",
            "authorization_verified": False,
            "counts": {"base": len(old), "head": len(new),
                       **{k: sum(c["kind"] == k for c in changes) for k in "ADMT"}},
            "changes": changes, "sensitive_review_required": sensitive,
            "failures": failures, "scope": scope}

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--repository", required=True, choices=sorted(REPOS))
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--scope", type=Path)
    parser.add_argument("--require-scope", action="store_true")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        base, head = commit(args.root, args.base), commit(args.root, args.head)
        git(args.root, "merge-base", "--is-ancestor", base, head)
        approved = json.loads(args.scope.read_text(encoding="utf-8")) if args.scope else None
        if args.scope and not isinstance(approved, dict):
            raise Blocked("Scope must be a JSON object")
        report = compare(args.repository, base, head, inventory(args.root, base),
                         inventory(args.root, head), approved, args.require_scope)
        rc = 1 if report["status"] == "FAIL" else 0
    except (Blocked, OSError, ValueError, TypeError) as exc:
        report = {"status": "BLOCKED", "reason": str(exc),
                  "repository": args.repository, "base": args.base, "head": args.head}
        rc = 2
    args.out.write_text(json.dumps(report, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print("SC-INTEGRITY-01", report["status"], report.get("level", ""), report.get("counts", ""))
    for item in report.get("failures", []):
        print(item["code"], repr(item["path"]))
    if rc == 0:
        print("Tree check only; independent review, authorization and existing build/QA gates remain required.")
    return rc

if __name__ == "__main__":
    sys.exit(main())
