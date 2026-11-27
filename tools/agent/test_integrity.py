"""Negative and positive fixtures using real temporary Git trees."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

import check_integrity as gate

class IntegrityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="sc-integrity-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.g("init", "-q")
        self.g("config", "user.name", "SC fixture")
        self.g("config", "user.email", "fixture@example.invalid")
        for name in sorted(gate.COMMON | {"src/js/game.js", "docs/readme.md",
                                             "tools/agent/check_integrity.py"}):
            self.put(name, b"baseline content\n")
        self.base = self.save()
        self.old = gate.inventory(self.root, self.base)

    def g(self, *args):
        return subprocess.check_output(["git", "-C", str(self.root), *args]).decode().strip()

    def put(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)

    def save(self):
        self.g("add", "-A")
        self.g("commit", "-qm", "fixture")
        return self.g("rev-parse", "HEAD")

    def report(self, head, **kw):
        return gate.compare("tihidon/test1", self.base, head, self.old,
                            gate.inventory(self.root, head), **kw)

    def assert_code(self, r, code, path):
        self.assertEqual(r["status"], "FAIL")
        self.assertIn({"code": code, "path": path}, r["failures"])

    def test_legitimate_docs_and_exact_scope(self):
        self.put("docs/readme.md", b"new documentation")
        head = self.save()
        r = self.report(head)
        self.assertEqual(r["status"], "PASS")
        self.assertEqual(r["level"], "STRUCTURAL_ONLY")
        self.assertFalse(r["authorization_verified"])
        self.assertEqual(self.report(head, approved=r["scope"], require_scope=True)["level"],
                         "EXACT_SCOPE_MATCH")
        with self.assertRaises(gate.Blocked):
            self.report(head, require_scope=True)

    def test_index_removed(self):
        (self.root / "index.html").unlink()
        r = self.report(self.save())
        self.assert_code(r, "PROTECTED_MISSING_OR_INVALID", "index.html")
        self.assert_code(r, "DELETION_OR_MODE_CHANGE", "index.html")

    def test_index_empty(self):
        self.put("index.html", b"")
        self.assert_code(self.report(self.save()), "PROTECTED_MISSING_OR_INVALID", "index.html")

    def test_index_truncated_scope_rejects(self):
        self.put("docs/readme.md", b"new")
        allowed = self.report(self.save())["scope"]
        self.put("index.html", b"x")
        self.assert_code(self.report(self.save(), approved=allowed), "SCOPE_MISMATCH", None)

    def test_both_workflows_deleted(self):
        paths = (".github/workflows/engineering-gates.yml",
                 ".github/workflows/chrome-devtools-mcp.yml")
        for p in paths:
            (self.root / p).unlink()
        r = self.report(self.save())
        for p in paths:
            self.assert_code(r, "PROTECTED_MISSING_OR_INVALID", p)

    def test_checker_removed(self):
        (self.root / "tools/agent/check_integrity.py").unlink()
        self.assert_code(self.report(self.save()), "PROTECTED_MISSING_OR_INVALID",
                         "tools/agent/check_integrity.py")

    def test_checker_noop_scope_rejects(self):
        self.put("docs/readme.md", b"new")
        approved = self.report(self.save())["scope"]
        self.put("tools/agent/check_integrity.py", b"raise SystemExit(0)\n")
        r = self.report(self.save(), approved=approved)
        self.assert_code(r, "SCOPE_MISMATCH", None)
        self.assertIn("tools/agent/check_integrity.py", r["sensitive_review_required"])

    def test_symlink_replacement(self):
        (self.root / "index.html").unlink()
        oid = subprocess.check_output(["git", "-C", str(self.root), "hash-object",
                                       "-w", "--stdin"], input=b"docs/readme.md").decode().strip()
        self.g("update-index", "--add", "--cacheinfo", "120000," + oid + ",index.html")
        self.g("commit", "-qm", "symlink")
        r = self.report(self.g("rev-parse", "HEAD"))
        self.assert_code(r, "UNSUPPORTED_OBJECT", "index.html")
        self.assert_code(r, "PROTECTED_MISSING_OR_INVALID", "index.html")

    def test_unapproved_addition_and_rename(self):
        self.put("docs/readme.md", b"new")
        approved = self.report(self.save())["scope"]
        (self.root / "docs/readme.md").rename(self.root / "docs/archive.md")
        r = self.report(self.save(), approved=approved)
        self.assert_code(r, "SCOPE_MISMATCH", None)
        self.assertEqual({c["kind"] for c in r["changes"]}, {"A", "D"})

    def test_valid_new_build_not_frozen(self):
        self.put("index.html", b"legitimate different size\n")
        self.put("src/js/game.js", b"new source\n")
        head = self.save()
        r = self.report(head)
        self.assertEqual(r["status"], "PASS")
        self.assertEqual(self.report(head, approved=r["scope"])["status"], "PASS")

    def test_critical_deletion_cannot_be_scoped_away(self):
        (self.root / "index.html").unlink()
        head = self.save()
        r = self.report(head)
        self.assert_code(self.report(head, approved=r["scope"]),
                         "PROTECTED_MISSING_OR_INVALID", "index.html")

    def test_wrong_repo_or_stale_commit(self):
        with self.assertRaises(gate.Blocked):
            gate.compare("other/repo", self.base, self.base, self.old, self.old)
        self.put("docs/readme.md", b"new")
        head = self.save()
        r = self.report(head)
        self.assert_code(self.report(head, approved=dict(r["scope"], repository="tihidon/test-cl1")),
                         "SCOPE_MISMATCH", None)
        self.put("docs/readme.md", b"newer")
        self.assert_code(self.report(self.save(), approved=r["scope"]), "SCOPE_MISMATCH", None)

    def test_cli_missing_commit_blocks(self):
        out = self.root / "report.json"
        rc = gate.main(["--root", str(self.root), "--repository", "tihidon/test1",
                        "--base", "0"*40, "--head", self.base, "--out", str(out)])
        self.assertEqual(rc, 2)
        self.assertEqual(json.loads(out.read_text())["status"], "BLOCKED")

    def test_historical_pr11_actual_tree(self):
        if os.environ.get("GITHUB_REPOSITORY") != "tihidon/test-cl1":
            self.skipTest("actual incident commit is in test-cl1, not fixture/test1")
        root = Path(__file__).resolve().parents[2]
        base = "3fa5b1b197580f92d793158fe96ed3b8fa882bab"
        head = "52da91a188f0bfcdbf1f4a83d7d41794d3d2b8f2"
        r = gate.compare("tihidon/test-cl1", base, head,
                         gate.inventory(root, base), gate.inventory(root, head))
        for p in ("index.html", ".github/workflows/engineering-gates.yml",
                  ".github/workflows/chrome-devtools-mcp.yml"):
            self.assert_code(r, "PROTECTED_MISSING_OR_INVALID", p)
        self.assertEqual(r["counts"]["D"], 205)
        self.assertEqual(r["counts"]["A"], 381)

if __name__ == "__main__":
    unittest.main()
