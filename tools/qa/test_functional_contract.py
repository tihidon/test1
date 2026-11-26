import copy
import unittest
from functional_contract import (CASE_IDS,purchase,durable,unchanged_inventory,accepted_cases)

class FunctionalContractTests(unittest.TestCase):
    def setUp(self):
        self.a={"saveId":"fixture","revision":3,"level":1,"sliz":1000,"diamonds":10,"tokens":3,
                "eggs":[{"id":"a","kind":0}],"snails":[{"id":"s"}],"built":[],"playerName":"QA"}
        self.b=copy.deepcopy(self.a)
        self.b.update(revision=4,sliz=900)
        self.b["eggs"].append({"id":"b","kind":0})
    def test_exact_purchase(self):
        purchase(self.a,self.b)
    def test_double_debit_rejected(self):
        self.b["sliz"]=800
        with self.assertRaises(AssertionError):purchase(self.a,self.b)
    def test_duplicate_egg_rejected(self):
        self.b["eggs"][1]["id"]="a"
        with self.assertRaises(AssertionError):purchase(self.a,self.b)
    def test_wrong_kind_rejected(self):
        self.b["eggs"][1]["kind"]=1
        with self.assertRaises(AssertionError):purchase(self.a,self.b)
    def test_not_committed_rejected(self):
        self.b["revision"]=3
        with self.assertRaises(AssertionError):purchase(self.a,self.b)
    def test_revision_may_advance_on_settlement(self):
        a=copy.deepcopy(self.b);a["revision"]+=2
        durable(self.b,a)
    def test_cold_reset_rejected(self):
        with self.assertRaises(AssertionError):durable(self.b,self.a)
    def test_identity_mismatch_rejected(self):
        a=copy.deepcopy(self.b);a["saveId"]="other"
        with self.assertRaises(AssertionError):durable(self.b,a)
    def test_negative_control_rejects_extra_mutation(self):
        with self.assertRaises(AssertionError):unchanged_inventory(self.a,self.b)
    def test_required_case_no_skip_or_zero_assertions(self):
        r={"functional_cases":{k:{"status":"PASS","assertions":1} for k in CASE_IDS}}
        self.assertTrue(accepted_cases(r))
        r["functional_cases"]["B06"]["status"]="NOT RUN"
        self.assertFalse(accepted_cases(r))
        r["functional_cases"]["B06"].update(status="PASS",assertions=0)
        self.assertFalse(accepted_cases(r))
