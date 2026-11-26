"""QA-003 diagnostic, not a release acceptance test. Isolated synthetic origin only."""
import argparse
import hashlib
import json
import re
import tempfile
import traceback
from http.server import BaseHTTPRequestHandler
from pathlib import Path

from origin_transport import OriginTransport
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
BASE_BLOB = "446a11bc377c036f2dcc5b74217a7b4a4abcab5b"
OLD = "snail-city-shell-qa003-old-fixture"
FOREIGN = "qa003-unrelated"
PATHS = {"/index.html", "/manifest.webmanifest", "/img/icon-192.png",
         "/img/icon-512.png", "/img/icon-maskable.png", "/privacy.html", "/delete-account.html"}

STATE = """async()=>{const o={}; for(const n of await caches.keys()){
 const c=await caches.open(n);o[n]={};for(const k of await c.keys()){
 const r=await c.match(k);const h=await crypto.subtle.digest('SHA-256',await r.arrayBuffer());
 o[n][new URL(k.url).pathname]=Array.from(new Uint8Array(h),x=>x.toString(16).padStart(2,'0')).join('');
 }}return o}"""
UPDATE = """async()=>{const r=await navigator.serviceWorker.getRegistration();
 return new Promise((ok,bad)=>{const t=setTimeout(()=>bad(Error('update timeout')),12000);
 r.addEventListener('updatefound',()=>{const w=r.installing;
 const f=()=>{if(['activated','redundant'].includes(w.state)){clearTimeout(t);ok(w.state)}};
 w.addEventListener('statechange',f);f()},{once:true});
 r.update().catch(e=>{clearTimeout(t);bad(e)})})}"""
READ = """()=>new Promise((ok,bad)=>{const q=indexedDB.open('qa003-sentinel',1);
 q.onupgradeneeded=()=>{q.transaction.abort();bad(Error('missing original DB'))};
 q.onerror=()=>bad(q.error);q.onsuccess=()=>{const d=q.result,t=d.transaction('s','readonly'),
 g=t.objectStore('s').get('current');t.oncomplete=()=>{d.close();ok(g.result)};
 t.onerror=()=>bad(t.error);t.onabort=()=>bad(t.error)}})"""
SEED = """async name=>{const c=await caches.open(name);await c.put('/foreign',new Response('keep'));
 await new Promise((ok,bad)=>{const q=indexedDB.open('qa003-sentinel',1);
 q.onupgradeneeded=()=>q.result.createObjectStore('s');q.onerror=()=>bad(q.error);
 q.onsuccess=()=>{const d=q.result,t=d.transaction('s','readwrite');
 t.objectStore('s').put('test-only','current');t.oncomplete=()=>{d.close();ok()};
 t.onerror=()=>bad(t.error);t.onabort=()=>bad(t.error)}})}"""

def run_case(pw, sw, new, case, preserve=False):
    same = case == "same_name_failure"
    fail = case in ("distinct_failure", "same_name_failure")
    old = new if same else OLD
    data = {"sw": sw.replace(new.encode(), old.encode(), 1), "label": "old", "fail": False}
    requests, checks = [], []
    result = {"case": case, "checks": checks, "requests": requests, "status": "FAIL"}
    def check(name, ok, observed=None):
        checks.append({"name": name, "pass": bool(ok), "observed": observed})
        if not ok:
            raise AssertionError(name)
    def page_bytes(label):
        return ("<html><body>"+label+"</body></html>").encode()
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass
        def do_GET(self):
            path = self.path.split("?")[0]
            status = 200
            if path == "/sw.js":
                payload, mime = data["sw"], "application/javascript"
            elif data["fail"] and path == "/img/icon-512.png":
                status, payload, mime = 503, b"controlled failure", "text/plain"
            elif path.startswith("/img/"):
                payload, mime = b"synthetic image bytes", "image/png"
            elif path == "/manifest.webmanifest":
                payload, mime = b"{}", "application/manifest+json"
            else:
                payload, mime = page_bytes(data["label"]), "text/html"
            requests.append({"path": path, "status": status, "label": data["label"]})
            self.send_response(status)
            self.send_header("Content-Type", mime)
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
    transport = OriginTransport(Handler)
    ctx = None
    try:
        transport.start()
        origin = transport.origin
        with tempfile.TemporaryDirectory() as profile:
            ctx = pw.chromium.launch_persistent_context(profile, headless=True)
            try:
                p = ctx.pages[0]
                p.set_default_timeout(12000)
                p.goto(origin+"/index.html", wait_until="domcontentloaded")
                p.evaluate("""async()=>{await navigator.serviceWorker.register('/sw.js',{updateViaCache:'none'});
                    await navigator.serviceWorker.ready}""")
                p.wait_for_function("!!navigator.serviceWorker.controller")
                p.evaluate(SEED, FOREIGN)
                before = p.evaluate(STATE)
                check("old cache complete", set(before.get(old, {})) == PATHS, before)
                check("old HTML exact", before[old]["/index.html"] == hashlib.sha256(page_bytes("old")).hexdigest())
                check("synthetic IDB committed", p.evaluate(READ) == "test-only")
                tab = ctx.new_page()
                tab.set_default_timeout(12000)
                tab.goto(origin+"/index.html", wait_until="domcontentloaded")
                tab.wait_for_function("!!navigator.serviceWorker.controller")
                tab.evaluate("window.changes=0;navigator.serviceWorker.addEventListener('controllerchange',()=>window.changes++)")
                data.update(sw=sw+b"\n// QA-003 intentionally reused cache name\n" if same else sw,
                            label="new", fail=fail)
                outcome = p.evaluate(UPDATE)
                check("terminal worker state", outcome == ("redundant" if fail else "activated"), outcome)
                after = p.evaluate(STATE)
                check("foreign cache bytes unchanged", after.get(FOREIGN) == before[FOREIGN], after)
                check("synthetic IDB online", p.evaluate(READ) == "test-only")
                if fail:
                    if same and preserve:
                        check("reused cache rejected before resource fetch", not any(r["label"]=="new" and r["path"] in PATHS for r in requests), requests)
                    else:
                        check("controlled HTTP failure observed", any(r["path"]=="/img/icon-512.png" and
                              r["status"]==503 for r in requests), requests)
                    check("old controller retained", tab.evaluate("window.changes===0 && !!navigator.serviceWorker.controller"))
                    if not same or preserve:
                        check("old cache bytes unchanged", after.get(old) == before[old], after)
                    if not same:
                        check("partial new cache removed", new not in after, after)
                else:
                    check("new cache complete", set(after.get(new, {})) == PATHS, after)
                    check("new HTML exact", after[new]["/index.html"] == hashlib.sha256(page_bytes("new")).hexdigest())
                    check("old cache removed", old not in after, after)
                    tab.wait_for_function("window.changes>0")
                    check("second tab controller changed", tab.evaluate("window.changes")>0)
                if case == "rollback":
                    data.update(sw=sw.replace(new.encode(), OLD.encode(), 1), label="old")
                    check("rollback activated", p.evaluate(UPDATE)=="activated")
                    after = p.evaluate(STATE)
                    check("rollback bytes restored", after.get(OLD)==before[OLD], after)
                    check("new cache removed on rollback", new not in after)
                    check("foreign preserved on rollback", after.get(FOREIGN)==before[FOREIGN])
                transport.stop()
                transport.assert_closed()
                ctx.set_offline(True)
                response = None
                nav_error = None
                body = None
                try:
                    response = p.goto(origin+"/index.html", wait_until="domcontentloaded")
                    body = p.locator("body").inner_text()
                except Exception as exc:
                    nav_error = str(exc)
                result["offline"] = {"error": nav_error, "body": body,
                                     "from_sw": response.from_service_worker if response else False}
                check("real transport remains closed", (transport.assert_closed() is None))
                check("synthetic IDB offline", tab.evaluate(READ)=="test-only")
                if same and not preserve:
                    # This explicit diagnostic expectation is NOT a passing product invariant.
                    # No other failure is accepted as reproduction.
                    check("known cache deletion reproduced", old not in after, after)
                    check("known offline navigation failure reproduced", response is None and
                          nav_error is not None and "net::ERR_FAILED" in nav_error, nav_error)
                    result["status"] = "DEFECT_REPRODUCED"
                else:
                    expected = "old" if fail or case=="rollback" else "new"
                    check("offline navigation exact", response is not None and response.ok and
                          response.from_service_worker and body==expected, result["offline"])
                    result["status"] = "PASS"
            finally:
                ctx.close()
                ctx = None
    except Exception:
        result["error"] = traceback.format_exc()
    finally:
        if ctx is not None:
            ctx.close()
        transport.stop()
    return result

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--worker", type=Path)
    ap.add_argument("--preserve", action="store_true")
    args = ap.parse_args()
    if args.preserve != bool(args.worker):
        ap.error("candidate worker and preserve mode required together")
    args.out.mkdir(parents=True, exist_ok=True)
    sw = (args.worker or ROOT/"sw.js").read_bytes()
    blob = hashlib.sha1(b"blob "+str(len(sw)).encode()+b"\0"+sw).hexdigest()
    report = {"source_blob": blob, "scope": "actual Chromium, synthetic origin/resources and sentinel IDB; not game migration or physical quota",
              "status": "NOT_RUN", "cases": []}
    def save():
        (args.out/"report.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    save()
    try:
        if not args.preserve and blob != BASE_BLOB:
            raise AssertionError("diagnostic baseline SW changed; review oracle before running")
        names = re.findall(rb"const CACHE_NAME = '([^']+)'", sw)
        if len(names)!=1:
            raise AssertionError("ambiguous CACHE_NAME")
        with sync_playwright() as pw:
            for case in ("success","distinct_failure","same_name_failure","rollback"):
                r = run_case(pw,sw,names[0].decode(),case,args.preserve)
                report["cases"].append(r)
                print(json.dumps(r),flush=True)
                save()
        expected = ["PASS"]*4 if args.preserve else ["PASS","PASS","DEFECT_REPRODUCED","PASS"]
        success = "PASS" if args.preserve else "DIAGNOSTIC_COMPLETE_DEFECT_OPEN"
        report["status"] = success if [r["status"] for r in report["cases"]]==expected else "FAIL"
    except Exception:
        report["status"] = "BLOCKED_OR_FAIL"
        report["error"] = traceback.format_exc()
    finally:
        save()
        print(json.dumps({"status":report["status"],"source_blob":blob}),flush=True)
    return 0 if report["status"]==("PASS" if args.preserve else "DIAGNOSTIC_COMPLETE_DEFECT_OPEN") else 1

if __name__ == "__main__":
    raise SystemExit(main())
