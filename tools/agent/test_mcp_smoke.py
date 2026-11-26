import unittest
from mcp_smoke import fixture_page_id, snapshot_button_uid, has_marker

URL = "http://127.0.0.1:12345/"
def result(text):
    return {"content": [{"type": "text", "text": text}]}

class PageIdentityTests(unittest.TestCase):
    def test_titled(self):
        self.assertEqual(fixture_page_id(result("## Pages\n1: about:blank\n7: SC MCP fixture ("+URL+") [selected]"), URL), 7)
    def test_bare(self):
        self.assertEqual(fixture_page_id(result("## Pages\n3: "+URL), URL), 3)
    def test_duplicate(self):
        with self.assertRaisesRegex(RuntimeError, "not uniquely listed"):
            fixture_page_id(result("1: "+URL+"\n2: fixture ("+URL+")"), URL)
    def test_wrong_url(self):
        for text in ("1: "+URL+"wrong", "1: fixture ("+URL+"wrong)", "1: about:blank [selected]"):
            with self.subTest(text=text), self.assertRaisesRegex(RuntimeError, "not uniquely listed"):
                fixture_page_id(result(text), URL)

class InteractionOracleTests(unittest.TestCase):
    def test_unique_button(self):
        self.assertEqual(snapshot_button_uid(result('uid=2_1 button "Advance fixture"')), "2_1")
    def test_missing_or_duplicate_button(self):
        for value in ('uid=2_1 button "Other"', 'uid=2_1 button "Advance fixture"\nuid=2_2 button "Advance fixture"'):
            with self.subTest(value=value), self.assertRaisesRegex(RuntimeError, "not uniquely listed"):
                snapshot_button_uid(result(value))
    def test_marker_boundaries(self):
        self.assertTrue(has_marker(result('"SC-MCP-ACTION-42"'), "SC-MCP-ACTION-42"))
        for value in ("SC-MCP-ACTION-420", "XSC-MCP-ACTION-42", "SC-MCP-NEGATIVE-99"):
            self.assertFalse(has_marker(result(value), "SC-MCP-ACTION-42"))

if __name__ == "__main__":
    unittest.main()
