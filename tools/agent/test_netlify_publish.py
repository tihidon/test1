"""Run the actual repository's Netlify command in an isolated temporary copy."""
import hashlib
from pathlib import Path
import shutil
import subprocess
import tempfile
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ("index.html", "sw.js", "manifest.webmanifest", "_headers",
          "privacy.html", "delete-account.html")
FAIL_MARKER = "SC-PUBLISH-01: root HTML differs from source build"


def snapshot(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob("*") if p.is_file()}


class NetlifyPublishTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="sc-netlify-")
        self.addCleanup(self.tmp.cleanup)
        self.work = Path(self.tmp.name)
        shutil.copytree(ROOT / "src", self.work / "src")
        shutil.copytree(ROOT / "img", self.work / "img")
        (self.work / "tools").mkdir()
        shutil.copy2(ROOT / "tools/build.py", self.work / "tools/build.py")
        for name in (*PUBLIC, "netlify.toml"):
            shutil.copy2(ROOT / name, self.work / name)
        self.config = tomllib.loads((self.work / "netlify.toml").read_text())["build"]
        self.assertEqual(self.config["publish"], "dist")

    def run_build(self):
        return subprocess.run(["bash", "-c", self.config["command"]],
                              cwd=self.work, capture_output=True, text=True, timeout=120)

    def test_valid_publish_exact_whitelist(self):
        before = snapshot(self.work / "src")
        expected = {p: hashlib.sha256((self.work / p).read_bytes()).hexdigest()
                    for p in PUBLIC}
        expected.update({"img/" + p: h for p, h in snapshot(self.work / "img").items()})
        # A stale file in a previous dist must not be published.
        (self.work / "dist").mkdir()
        (self.work / "dist/stale-private.txt").write_text("fixture")
        result = self.run_build()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(snapshot(self.work / "dist"), expected)
        self.assertEqual(snapshot(self.work / "src"), before)
        self.assertEqual(hashlib.sha256((self.work / "index.html").read_bytes()).hexdigest(),
                         expected["index.html"])

    def test_stale_root_fails_before_copy(self):
        root = self.work / "index.html"
        original = root.read_bytes()
        root.write_bytes(original + b"\\n<!-- negative-control stale root -->\\n")
        before = snapshot(self.work / "src")
        result = self.run_build()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(FAIL_MARKER, result.stderr)
        self.assertEqual(snapshot(self.work / "dist"),
                         {"index.html": hashlib.sha256(original).hexdigest()})
        self.assertEqual(snapshot(self.work / "src"), before)
        self.assertNotEqual(root.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
