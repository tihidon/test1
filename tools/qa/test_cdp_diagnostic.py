import unittest
from playwright.sync_api import sync_playwright
from cdp_diagnostic import Diagnostic, has_observations

class DiagnosticTests(unittest.TestCase):
    def test_real_call_counts_and_late_css(self):
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True)
            try:
                context=browser.new_context()
                page=context.new_page()
                page.set_default_timeout(5000)
                d=Diagnostic(context.new_cdp_session(page))
                d.start()
                try:
                    page.set_content("""<style>.now{color:red}.late{color:blue}</style>
                    <div id="t" class="now">fixture</div>
                    <script>function scCount(){return 7;} scCount();scCount();scCount();</script>""")
                    self.assertEqual(page.locator("#t").evaluate("(e)=>getComputedStyle(e).color"),"rgb(255, 0, 0)")
                    a=d.capture("startup")
                    def count(phase):
                        return sum(f["ranges"][0]["count"] for s in phase["js"] for f in s["functions"] if f["functionName"]=="scCount")
                    self.assertEqual(count(a),3)
                    page.evaluate("()=>{scCount();scCount();document.querySelector('#t').className='late';}")
                    self.assertEqual(page.locator("#t").evaluate("(e)=>getComputedStyle(e).color"),"rgb(0, 0, 255)")
                    b=d.capture("interaction")
                    self.assertEqual(count(b),2)
                    first={(x["styleSheetId"],x["startOffset"],x["endOffset"]) for x in a["css"] if x["used"]}
                    second={(x["styleSheetId"],x["startOffset"],x["endOffset"]) for x in b["css"] if x["used"]}
                    self.assertTrue(first)
                    self.assertTrue(second-first,"newly exercised CSS rule expected")
                    self.assertFalse(d.report()["timing_comparable"])
                finally:
                    d.stop()
                    context.close()
            finally:
                browser.close()

    def test_empty_or_wrong_origin_is_not_evidence(self):
        self.assertFalse(has_observations({"js":[],"css":[]},"expected"))
        phase={"js":[{"url":"other","functions":[{"ranges":[{"count":1}]}]}],"css":[{"used":True}]}
        self.assertFalse(has_observations(phase,"expected"))
