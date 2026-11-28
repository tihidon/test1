"""Open training pilot: Chromium primitives, not Snail City gameplay or agent evaluation.
20 predeclared positive/negative controls. Separate fresh context per case.
Uses the existing pinned CI browser and no additional dependencies.
"""
import json
import unittest
from playwright.sync_api import sync_playwright

ORIGIN = "http://127.0.0.1:18765/"
HTML = "<!doctype html><html><head><meta charset='utf-8'></head><body></body></html>"
DB_HELPER = """async () => {
 const db=await new Promise((ok,bad)=>{const r=indexedDB.open('sc-pilot',1);
 r.onupgradeneeded=()=>r.result.createObjectStore('ops');
 r.onsuccess=()=>ok(r.result);r.onerror=()=>bad(r.error)});
 return db;
}"""


class CodeHealthBrowserPilot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pw=sync_playwright().start()
        cls.addClassCleanup(cls.pw.stop)
        cls.browser=cls.pw.chromium.launch(headless=True, timeout=15000)
        cls.addClassCleanup(cls.browser.close)
        print("CH-PILOT browser="+cls.browser.version, flush=True)

    def setUp(self):
        self.ctx=self.browser.new_context(service_workers="block")
        self.addCleanup(self.ctx.close)
        self.ctx.set_default_timeout(5000)
        self.ctx.route("**/*", lambda route: route.fulfill(
            status=200, content_type="text/html", body=HTML
        ) if route.request.url==ORIGIN else route.abort())
        self.page=self.ctx.new_page()
        self.page.goto(ORIGIN, wait_until="load", timeout=5000)

    def check(self, script, expected):
        observed=self.page.evaluate(script)
        print("CH-PILOT",self._testMethodName,
              json.dumps({"expected":expected,"observed":observed},sort_keys=True),flush=True)
        self.assertEqual(observed,expected)

    def test_01_same_listener_is_not_duplicate(self):
        self.check("""() => {const x=new EventTarget();let n=0;const f=()=>n++;
            for(let i=0;i<5;i++)x.addEventListener('probe',f);
            x.dispatchEvent(new Event('probe'));return n}""",1)

    def test_02_distinct_listener_accumulates(self):
        self.check("""() => {const x=new EventTarget();let n=0;
            for(let i=0;i<5;i++)x.addEventListener('probe',()=>n++);
            x.dispatchEvent(new Event('probe'));return n}""",5)

    def test_03_listener_cleanup(self):
        self.check("""() => {const x=new EventTarget();let n=0;const f=()=>n++;
            x.addEventListener('probe',f);x.dispatchEvent(new Event('probe'));
            x.removeEventListener('probe',f);x.dispatchEvent(new Event('probe'));return n}""",1)

    def test_04_dynamic_delegation(self):
        self.check("""() => {let n=0;const p=document.createElement('div');
            document.body.append(p);p.addEventListener('click',e=>{if(e.target.matches('button'))n++});
            const b=document.createElement('button');p.append(b);b.click();p.click();return n}""",1)

    def test_05_sequential_raf_cancel(self):
        self.check("""() => new Promise((ok,bad)=>{let n=0;
            const t=setTimeout(()=>bad(Error('RAF timeout')),2000);
            const old=requestAnimationFrame(()=>n+=100);cancelAnimationFrame(old);
            requestAnimationFrame(()=>{n++;clearTimeout(t);ok(n)})})""",1)

    def test_06_parallel_raf_detected(self):
        self.check("""() => new Promise((ok,bad)=>{let n=0;
            const t=setTimeout(()=>bad(Error('RAF timeout')),2000);
            requestAnimationFrame(()=>n++);requestAnimationFrame(()=>n++);
            requestAnimationFrame(()=>{clearTimeout(t);ok(n)})})""",2)

    def test_07_same_canvas_width_write_resets_pixels(self):
        self.check("""() => {const c=document.createElement('canvas');c.width=2;c.height=2;
            const g=c.getContext('2d');g.fillRect(0,0,1,1);
            const before=g.getImageData(0,0,1,1).data[3];c.width=2;
            return [before,g.getImageData(0,0,1,1).data[3]]}""",[255,0])

    def test_08_guarded_canvas_resize_preserves_pixels(self):
        self.check("""() => {const c=document.createElement('canvas');c.width=2;c.height=2;
            const g=c.getContext('2d');g.fillRect(0,0,1,1);
            if(c.width!==2)c.width=2;return g.getImageData(0,0,1,1).data[3]}""",255)

    def test_09_legitimate_css_state_override(self):
        self.check("""() => {const s=document.createElement('style');
            s.textContent='.panel{color:rgb(255,0,0)}.panel.open{color:rgb(0,128,0)}';
            document.head.append(s);const e=document.createElement('div');
            e.className='panel';document.body.append(e);const a=getComputedStyle(e).color;
            e.classList.add('open');return [a,getComputedStyle(e).color]}""",
            ["rgb(255, 0, 0)","rgb(0, 128, 0)"])

    def test_10_css_order_changes_result(self):
        self.check("""() => {const s=document.createElement('style');
            s.textContent='.panel{color:red}.panel{color:blue}';document.head.append(s);
            const e=document.createElement('div');e.className='panel';document.body.append(e);
            const a=getComputedStyle(e).color;s.textContent='.panel{color:blue}.panel{color:red}';
            return [a,getComputedStyle(e).color]}""",["rgb(0, 0, 255)","rgb(255, 0, 0)"])

    def test_11_lifecycle_removes_panel(self):
        self.check("""() => {let e;for(let i=0;i<5;i++){e=document.createElement('div');
            e.className='panel';document.body.append(e);e.remove()}
            return document.querySelectorAll('.panel').length}""",0)

    def test_12_missing_cleanup_accumulates_panel(self):
        self.check("""() => {for(let i=0;i<5;i++){const e=document.createElement('div');
            e.className='panel';document.body.append(e)}return document.querySelectorAll('.panel').length}""",5)

    def test_13_timer_coalescing(self):
        self.check("""() => new Promise(ok=>{let id,n=0;for(let i=0;i<5;i++){
            clearTimeout(id);id=setTimeout(()=>n++,0)}setTimeout(()=>ok(n),60)})""",1)

    def test_14_timer_cleanup(self):
        self.check("""() => new Promise(ok=>{let n=0;const id=setTimeout(()=>n++,0);
            clearTimeout(id);setTimeout(()=>ok(n),60)})""",0)

    def test_15_untrusted_text_remains_text(self):
        self.check("""() => {const e=document.createElement('div');document.body.append(e);
            e.textContent='<b>fixture</b>';return [e.childElementCount,e.textContent]}""",
            [0,"<b>fixture</b>"])

    def test_16_constant_html_is_not_alone_a_security_defect(self):
        self.check("""() => {const e=document.createElement('div');document.body.append(e);
            e.innerHTML='<b>fixed fixture</b>';return [e.childElementCount,e.firstElementChild.tagName,e.textContent]}""",
            [1,"B","fixed fixture"])

    def test_17_idb_commit_survives_reload(self):
        self.check("""async () => {const db=await ("""+DB_HELPER+""")();
            const tx=db.transaction('ops','readwrite');
            await new Promise((ok,bad)=>{tx.oncomplete=ok;tx.onabort=()=>bad(tx.error);
                tx.objectStore('ops').put(42,'op')});db.close();return true}""",True)
        self.page.reload(wait_until="load",timeout=5000)
        self.check("""async () => {const db=await ("""+DB_HELPER+""")();
            const v=await new Promise((ok,bad)=>{const r=db.transaction('ops').objectStore('ops').get('op');
                r.onsuccess=()=>ok(r.result);r.onerror=()=>bad(r.error)});db.close();return v}""",42)

    def test_18_idb_request_success_can_abort(self):
        self.check("""async () => {const db=await ("""+DB_HELPER+""")();
            let success=false;const tx=db.transaction('ops','readwrite');
            await new Promise((ok,bad)=>{tx.onabort=ok;tx.oncomplete=()=>bad(Error('unexpected commit'));
                const r=tx.objectStore('ops').put(42,'op');r.onsuccess=()=>{success=true;tx.abort()}});
            const v=await new Promise((ok,bad)=>{const r=db.transaction('ops').objectStore('ops').get('op');
                r.onsuccess=()=>ok(r.result??null);r.onerror=()=>bad(r.error)});
            db.close();return [success,v]}""",[True,None])

    def test_19_idb_same_key_idempotent_record(self):
        self.check("""async () => {const db=await ("""+DB_HELPER+""")();
            const tx=db.transaction('ops','readwrite');
            await new Promise((ok,bad)=>{tx.oncomplete=ok;tx.onabort=()=>bad(tx.error);
                const s=tx.objectStore('ops');s.put({op:'reward',amount:5},'op');s.put({op:'reward',amount:5},'op')});
            const a=await new Promise((ok,bad)=>{const r=db.transaction('ops').objectStore('ops').getAll();
                r.onsuccess=()=>ok(r.result);r.onerror=()=>bad(r.error)});db.close();return a}""",
            [{"op":"reward","amount":5}])

    def test_20_idb_duplicate_operation_distinct_keys(self):
        self.check("""async () => {const db=await ("""+DB_HELPER+""")();
            const tx=db.transaction('ops','readwrite');
            await new Promise((ok,bad)=>{tx.oncomplete=ok;tx.onabort=()=>bad(tx.error);
                const s=tx.objectStore('ops');s.put({op:'reward',amount:5},'tx1');s.put({op:'reward',amount:5},'tx2')});
            const a=await new Promise((ok,bad)=>{const r=db.transaction('ops').objectStore('ops').getAll();
                r.onsuccess=()=>ok(r.result);r.onerror=()=>bad(r.error)});db.close();
            return [a.filter(v=>v.op==='reward').length,a.reduce((s,v)=>s+v.amount,0)]}""",[2,10])


if __name__ == "__main__":
    unittest.main(verbosity=2)
