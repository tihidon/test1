import unittest
from check_cache_revision import evaluate, inventory

def worker(name="old", paths="'./index.html','./manifest.webmanifest'"):
    return "const CACHE_NAME = '"+name+"';\nconst CORE_PATHS = [\n  "+paths+"\n];\n"

class CacheRevisionTests(unittest.TestCase):
    def test_docs_only(self):
        self.assertEqual(evaluate(worker(),worker(),["docs/README.md"])[0],[])
    def test_html_changed_same_name(self):
        with self.assertRaisesRegex(ValueError,"without new CACHE_NAME"):
            evaluate(worker(),worker(),["index.html"])
    def test_sw_changed_same_name(self):
        with self.assertRaises(ValueError):
            evaluate(worker(),worker(),["sw.js"])
    def test_updated_namespace(self):
        self.assertEqual(evaluate(worker(),worker("new"),["sw.js","index.html"])[0],["index.html","sw.js"])
    def test_removed_core_path_still_checked(self):
        with self.assertRaises(ValueError):
            evaluate(worker(),worker(paths="'./index.html'"),["manifest.webmanifest"])
    def test_duplicate_path(self):
        with self.assertRaises(ValueError):
            inventory(worker(paths="'./index.html','./index.html'"))
    def test_parent_path(self):
        with self.assertRaises(ValueError):
            inventory(worker(paths="'./../index.html'"))
    def test_unparsed_expression(self):
        with self.assertRaises(ValueError):
            inventory(worker(paths="'./index.html',someFunction()"))

if __name__ == "__main__":
    unittest.main()
