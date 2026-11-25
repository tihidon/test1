import json
import shutil
import tempfile
import unittest
from pathlib import Path

from check_build import assemble, verify

ROOT = Path(__file__).resolve().parents[2]


class BuildTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for d in ("src/html", "src/js", "tools"):
            (self.root / d).mkdir(parents=True)
        self.template = self.root / "src/html/index.template.html"
        self.template.write_text("<html><!--SC-INLINE 00--></html>", encoding="utf-8")
        self.block = self.root / "src/js/block-00.js"
        self.block.write_text("const sentinel=2;", encoding="utf-8")
        self.manifest = self.root / "src/html/blocks.json"
        self.manifest.write_text(json.dumps([{"id":"00","file":"src/js/block-00.js","element":"script","open_tag":"<script>","close_tag":"</script>"}]))
        shutil.copy2(ROOT / "tools/build.py", self.root / "tools/build.py")

    def test_source_edit_survives(self):
        if not shutil.which("node"):
            self.skipTest("Node unavailable")
        verify(self.root)
        self.assertEqual(self.block.read_text(), "const sentinel=2;")
        self.assertFalse((self.root / "dist").exists())

    def test_duplicate_marker(self):
        self.template.write_text("<!--SC-INLINE 00--><!--SC-INLINE 00-->")
        with self.assertRaises(ValueError):
            assemble(self.root)

    def test_missing_marker(self):
        self.template.write_text("<html></html>")
        with self.assertRaises(ValueError):
            assemble(self.root)

    def test_bad_path(self):
        blocks = json.loads(self.manifest.read_text())
        blocks[0]["file"] = "src/../../outside.js"
        self.manifest.write_text(json.dumps(blocks))
        with self.assertRaises(ValueError):
            assemble(self.root)

    def test_publish_mismatch(self):
        if not shutil.which("node"):
            self.skipTest("Node unavailable")
        (self.root / "sw.js").write_text("// fixture")
        (self.root / "index.html").write_text("wrong")
        with self.assertRaises(ValueError):
            verify(self.root, True)

    def test_invalid_syntax(self):
        if not shutil.which("node"):
            self.skipTest("Node unavailable")
        self.block.write_text("const = ;")
        import subprocess
        with self.assertRaises(subprocess.CalledProcessError):
            verify(self.root)

    def test_source_mutation_detected(self):
        if not shutil.which("node"):
            self.skipTest("Node unavailable")
        p = self.root / "tools/build.py"
        p.write_text(p.read_text().replace("    sys.exit(0)", '    (ROOT / "src/js/block-00.js").write_text("changed")\n    sys.exit(0)'))
        with self.assertRaises(ValueError):
            verify(self.root)
        self.assertEqual(self.block.read_text(), "const sentinel=2;")
