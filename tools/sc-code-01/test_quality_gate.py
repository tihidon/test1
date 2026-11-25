import copy
import unittest
from quality_gate import parse, locations, increases, verdict, RATCHET

class QualityGateTests(unittest.TestCase):
    def test_requires_actual_css_and_js(self):
        with self.assertRaises(ValueError):
            parse(b"<html><script>let a=1;</script></html>")
    def test_context_and_functional_commas(self):
        r=locations([".a:is(.x,.y){color:red}.a:is(.x,.y){color:blue}@media(max-width:2px){.a:is(.x,.y){color:red}}"])
        self.assertEqual(len(r["duplicate_exact_selectors"]),1)
        self.assertEqual(len(r["duplicate_exact_selectors"][0]["locations"]),2)
    def test_large_payload_not_dumped(self):
        r=locations([".a{--asset:"+("x"*4097)+"}"])
        self.assertEqual(r["large_values"][0]["characters"],4097)
        self.assertNotIn("value",r["large_values"][0])
    def test_parse_error_visible(self):
        self.assertTrue(locations([".a{broken}"])["parse_errors"])
    def base(self):
        r={"html_sha256":"a","css":{},"js":{},"css_locations":{"parse_errors":[]}}
        for s,k in RATCHET:r[s][k]=0
        return r
    def test_growth_rejected(self):
        a=self.base();b=copy.deepcopy(a);b["css"]["important"]=1
        self.assertEqual(verdict(a,b,a)["status"],"FAIL")
    def test_historical_debt_not_erased(self):
        old=self.base();a=copy.deepcopy(old);a["css"]["important"]=1
        r=verdict(a,a,old)
        self.assertEqual(r["status"],"PASS_NO_GROWTH")
        self.assertEqual(r["historical_status"],"FAIL")
        b=copy.deepcopy(a);b["html_sha256"]="b"
        self.assertEqual(verdict(a,b,old)["status"],"FAIL")
    def test_canonical_css_metrics_detect_growth(self):
        from sc_code_metrics import css_metrics
        a=self.base();b=copy.deepcopy(a)
        a["css"].update(css_metrics([".a{color:var(--c)}"],0))
        b["css"].update(css_metrics([".a{color:var(--c)}.a .b .c .d{color:#fff!important}"],0))
        names={v["metric"] for v in increases(a,b)}
        self.assertTrue({"css.selectorsOver3Parts","css.important","css.rawHexColors"}<=names)
