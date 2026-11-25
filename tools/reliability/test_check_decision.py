import hashlib
import tempfile
import unittest
from pathlib import Path
from check_decision import check

class DecisionTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.root=Path(t.name)
        self.baseline="a"*40
        self.candidate="b"*40
        self.oracle="c"*64
        def artifact(ident):
            p=self.root/(ident+".log")
            p.write_text("synthetic fixture "+ident)
            return {"id":ident,"status":"PASS","exit_code":0,"command":"fixture",
                "artifact":p.name,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()}
        self.contract={"baseline":self.baseline,"oracle_sha256":self.oracle,
            "expected_failure":"wrong value","required":["regression"]}
        self.record={"baseline":self.baseline,"candidate":self.candidate,
            "before":{"commit":self.baseline,"oracle_sha256":self.oracle,"status":"FAIL",
                "failure_reason":"wrong value","capture":artifact("capture")},
            "after":{"commit":self.candidate,"oracle_sha256":self.oracle,"status":"PASS",
                "capture":artifact("capture")},
            "evidence":{"commit":self.candidate,"checks":[artifact("regression")]},
            "first_divergence":{"symbol":"f","anchor":"src/f.js","caller":"g","expected":"1","actual":"2"},
            "unresolved_contradictions":[],"decision":"PRIHVATI KANDIDAT",
            "review":{"status":"PASS","reviewer":"fixture reviewer","independent":True}}
    def errors(self):
        return check(self.contract,self.record,self.root)
    def test_valid_structure_only(self):
        self.assertEqual(self.errors(),[])
    def test_wrong_failure(self):
        self.record["before"]["failure_reason"]="timeout"
        self.assertTrue(self.errors())
    def test_changed_oracle(self):
        self.record["after"]["oracle_sha256"]="d"*64
        self.assertTrue(self.errors())
    def test_same_commit(self):
        self.record["candidate"]=self.baseline
        self.assertTrue(self.errors())
    def test_missing_review(self):
        self.record["review"]["independent"]=False
        self.assertTrue(self.errors())
    def test_missing_gate(self):
        self.record["evidence"]["checks"]=[]
        self.assertTrue(self.errors())
    def test_contradiction(self):
        self.record["unresolved_contradictions"]=["unresolved"]
        self.assertTrue(self.errors())
    def test_missing_divergence(self):
        self.record["first_divergence"]={}
        self.assertTrue(self.errors())
    def test_wrong_phase_status(self):
        self.record["before"]["status"]="PASS"
        self.assertTrue(self.errors())
    def test_missing_artifact(self):
        (self.root/"capture.log").unlink()
        self.assertTrue(self.errors())
