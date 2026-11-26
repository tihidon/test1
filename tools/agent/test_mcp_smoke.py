import unittest
from mcp_smoke import fixture_page_id

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

if __name__ == "__main__":
    unittest.main()
