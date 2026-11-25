import copy
import hashlib
import tempfile
import unittest
from pathlib import Path
from check_evidence import validate

class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        (self.root/"log.txt").write_bytes(b"fixture output")
        self.contract={"commit":"a"*40,"required":["build"]}
        self.evidence={"commit":"a"*40,"checks":[{"id":"build","status":"PASS",
            "command":"fixture command","exit_code":0,"artifact":"log.txt",
            "sha256":hashlib.sha256(b"fixture output").hexdigest()}]}
    def errors(self):
        return validate(self.contract,self.evidence,self.root)
    def test_valid(self):
        self.assertEqual(self.errors(),[])
    def test_wrong_commit(self):
        self.evidence["commit"]="b"*40
        self.assertTrue(self.errors())
    def test_missing_check(self):
        self.evidence["checks"]=[]
        self.assertTrue(self.errors())
    def test_nonpassing_states(self):
        for status in ("FAIL","BLOCKED","NOT RUN","N/A"):
            with self.subTest(status=status):
                self.evidence["checks"][0]["status"]=status
                self.assertTrue(self.errors())
    def test_wrong_exit(self):
        for code in (1,False,"0"):
            with self.subTest(code=code):
                self.evidence["checks"][0]["exit_code"]=code
                self.assertTrue(self.errors())
    def test_changed_artifact(self):
        (self.root/"log.txt").write_text("changed")
        self.assertTrue(self.errors())
    def test_path_escape(self):
        self.evidence["checks"][0]["artifact"]="../outside.log"
        self.assertTrue(self.errors())
    def test_duplicate(self):
        self.evidence["checks"].append(copy.deepcopy(self.evidence["checks"][0]))
        self.assertTrue(self.errors())
    def test_empty_contract(self):
        self.contract["required"]=[]
        self.assertTrue(self.errors())
    def test_empty_log(self):
        (self.root/"log.txt").write_bytes(b"")
        self.evidence["checks"][0]["sha256"]=hashlib.sha256(b"").hexdigest()
        self.assertTrue(self.errors())
