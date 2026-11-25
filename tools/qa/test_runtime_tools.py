import json
from pathlib import Path
import tempfile
import unittest
import sys
import os

from runtime_watchdog import run_bounded
from runtime_smoke import version_info, scenario_steps, require


class RuntimeTools(unittest.TestCase):
    def test_positive_child(self):
        with tempfile.TemporaryDirectory() as d:
            result=run_bounded([sys.executable,"-c","print('ok')"],Path(d),5)
            self.assertEqual(result["status"],"PASS" if os.name=="posix" else "BLOCKED")

    def test_negative_child(self):
        with tempfile.TemporaryDirectory() as d:
            result=run_bounded([sys.executable,"-c","raise SystemExit(1)"],Path(d),5)
            self.assertEqual(result["status"],"FAIL" if os.name=="posix" else "BLOCKED")

    def test_hung_child(self):
        with tempfile.TemporaryDirectory() as d:
            result=run_bounded([sys.executable,"-c","while True: pass"],Path(d),1)
            if os.name=="posix":
                self.assertEqual(result["exit_code"],124)
                self.assertEqual(result["status"],"FAIL")
            else:
                self.assertEqual(result["status"],"BLOCKED")

    def test_identity(self):
        self.assertEqual(version_info("const VERSION='x';","const CACHE_NAME='y';"),("x","y"))
        with self.assertRaises(AssertionError):
            version_info("const VERSION='x';const VERSION='z';","const CACHE_NAME='y';")

    def test_assertion_rejects(self):
        with self.assertRaises(AssertionError):
            require(False,"negative control")

    def test_scenario_requires_action_and_assertion(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"scenario.json"
            p.write_text(json.dumps([{"op":"click","selector":"button"}]))
            with self.assertRaises(AssertionError):
                scenario_steps(p)
            p.write_text(json.dumps([{"op":"click","selector":"button"},{"op":"text","selector":"#result","expected":"done"}]))
            self.assertEqual(len(scenario_steps(p)),2)
