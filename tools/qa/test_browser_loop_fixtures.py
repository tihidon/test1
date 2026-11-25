import json
import sys
import tempfile
import unittest
from pathlib import Path
from runtime_watchdog import run_bounded

class BrowserLoopFixtures(unittest.TestCase):
    def invoke(self,mode,timeout=30):
        t=tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        p=Path(t.name)
        r=run_bounded([sys.executable,str(Path(__file__).with_name("browser_loop_fixture.py")),mode,str(p)],p,timeout)
        return r,p
    def test_valid_bounded_loop_and_raf_cleanup(self):
        r,p=self.invoke("bounded")
        self.assertEqual(r["status"],"PASS",(p/"worker.log").read_text())
        d=json.loads((p/"fixture.json").read_text())
        self.assertEqual(d["activeChains"],1)
        self.assertEqual(d["hits"],d["stopped"])
        self.assertEqual(d["bounded"],3)
    def test_duplicate_raf_fails_for_intended_reason(self):
        r,p=self.invoke("duplicate")
        self.assertEqual(r.get("exit_code"),1,(p/"worker.log").read_text())
        d=json.loads((p/"fixture.json").read_text())
        self.assertEqual(d["activeChains"],2)
        self.assertEqual(d["hits"],d["stopped"])
        self.assertEqual(d["bounded"],3)
    def test_hang_killed_externally(self):
        r,p=self.invoke("hang",20)
        self.assertEqual(r.get("exit_code"),124,(p/"worker.log").read_text())
        self.assertTrue((p/"entered-browser-js").is_file())
    def test_dom_duplicate_ids(self):
        r,p=self.invoke("dom")
        self.assertEqual(r["status"],"PASS",(p/"worker.log").read_text())
        self.assertIn("D09 duplicate IDs",json.loads((p/"fixture.json").read_text())["findings"])
