import unittest
from check_cache_release import compare

def worker(name="a",paths="'./index.html'",extra=""):
    return ("const CACHE_NAME = 'snail-city-shell-"+name+"';\nconst CORE_PATHS = ["+paths+"];\n"+extra).encode()

class CacheReleaseTests(unittest.TestCase):
    def check(self,a,b):
        return compare(a.__getitem__,b.__getitem__)
    def test_unchanged(self):
        a={"sw.js":worker(),"index.html":b"a"}
        self.assertEqual(self.check(a,a)[2],[])
    def test_changed_html_same_name(self):
        a={"sw.js":worker(),"index.html":b"a"}
        with self.assertRaisesRegex(ValueError,"reused"):self.check(a,dict(a,**{"index.html":b"b"}))
    def test_changed_worker_same_name(self):
        a={"sw.js":worker(),"index.html":b"a"}
        with self.assertRaisesRegex(ValueError,"reused"):self.check(a,dict(a,**{"sw.js":worker(extra="//changed")}))
    def test_new_name(self):
        a={"sw.js":worker(),"index.html":b"a"}
        b={"sw.js":worker("b"),"index.html":b"b"}
        self.assertEqual(self.check(a,b)[2],["sw.js","index.html"])
    def test_new_core_path_same_name(self):
        a={"sw.js":worker(),"index.html":b"a"}
        b=dict(a,**{"sw.js":worker(paths="'./index.html','./extra.html'"),"extra.html":b"b"})
        with self.assertRaisesRegex(ValueError,"reused"):self.check(a,b)
    def test_unsafe_paths(self):
        a={"sw.js":worker(paths="'./../x'"),"index.html":b"a"}
        with self.assertRaisesRegex(ValueError,"unsafe"):self.check(a,a)
    def test_missing_core(self):
        a={"sw.js":worker()}
        with self.assertRaises(KeyError):self.check(a,a)
    def test_dynamic_list_rejected(self):
        a={"sw.js":worker(paths="'./index.html', dynamic"),"index.html":b"a"}
        with self.assertRaisesRegex(ValueError,"ambiguous"):self.check(a,a)
