"""Actual local Chromium shell test; no game source modifications."""
import argparse
import hashlib
from http.server import SimpleHTTPRequestHandler
import json
import os
import re
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from origin_transport import OriginTransport
from dom_audit import measure_dom
from cdp_diagnostic import Diagnostic, has_observations

PUBLIC = ("index.html", "sw.js", "manifest.webmanifest", "_headers",
          "privacy.html", "delete-account.html", "img")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def write(out, name, data):
    (out/name).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True, timeout=15).strip()


def capture_p1_startup(page, out, phase, version):
    # Temporary diagnostic only. Existing trace/profiler may perturb the
    # values. A submitted canvas frame is not a presented frame.
    if os.environ.get("SC_P1_CAPTURE_STARTUP") != "1":
        return
    page.wait_for_function("""() => {
        const t=window.SC_STARTUP_TRACE?.export();
        return t?.timings?.some(x=>x.label==='boot.overlayRemoved')
            && t.timings.some(x=>x.label==='canvas.firstSubmittedFrame');
    }""",timeout=30000)
    data=page.evaluate("()=>window.SC_STARTUP_TRACE.export()")
    require(data["build"]==version,"startup trace version mismatch")
    labels={x["label"] for x in data["timings"]}
    required={"boot.enter","boot.rendererInit","boot.parallelTasksStarted",
              "boot.parallelTasksComplete","boot.finalStateValidation",
              "boot.prepareIsland","boot.uiHydrate","boot.overlayRemoved",
              "canvas.firstSubmittedFrame"}
    require(required.issubset(labels),"missing startup stages: "+str(sorted(required-labels)))
    require(not any(x["label"].startswith("decode.") for x in data["timings"]),
            "decode probe must not run")
    write(out,"p1-startup-"+phase+".json",data)


def version_info(html, sw):
    versions = re.findall(r"\bconst\s+VERSION\s*=\s*['\"]([^'\"]+)['\"]", html)
    caches = re.findall(r"\bconst\s+CACHE_NAME\s*=\s*['\"]([^'\"]+)['\"]", sw)
    require(len(versions)==len(caches)==1, "ambiguous source version/cache identity")
    return versions[0], caches[0]


def scenario_steps(path):
    if not path:
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, list) and 1 <= len(data) <= 50, "scenario must contain 1–50 steps")
    for s in data:
        require(isinstance(s,dict) and s.get("op") in {"visible","click","text"}
                and isinstance(s.get("selector"),str) and s["selector"].strip(),
                "invalid scenario step")
        if s["op"] == "text":
            require(isinstance(s.get("expected"),str), "missing independent expected text")
    require(any(s["op"]=="click" for s in data) and any(s["op"] in {"visible","text"} for s in data),
            "scenario needs real action and assertion")
    require(data[-1]["op"] in {"visible","text"}, "scenario must end with assertion")
    return data


def run(root, out, scenario, diagnostic=False, functional=False):
    try:
        from playwright.sync_api import sync_playwright, expect
    except ImportError:
        write(out, "report.json", {"status":"BLOCKED","reason":"Playwright not installed"})
        return 2
    report = {"status":"FAIL","scope":"local Chromium shell; not complete gameplay, save or Android QA",
              "diagnostic_mode":diagnostic,"functional_mode":functional,"steps":[],"dom_snapshots":[],"page_errors":[],"local_http_errors":[],"blocked_external_requests":0}
    def stage(name):
        report["steps"].append(name)
        write(out,"report.json",report)
        print(name,flush=True)
    try:
        html = (root/"index.html").read_bytes()
        sw = (root/"sw.js").read_bytes()
        version, cache = version_info(html.decode("utf-8"),sw.decode("utf-8"))
        report.update(commit=git(root,"rev-parse","HEAD"),dirty=bool(git(root,"status","--porcelain")),
                      html_sha256=sha(html),sw_sha256=sha(sw),source_version=version,expected_cache=cache,
                      viewport={"width":360,"height":780},dpr=1)
        steps = scenario_steps(scenario)
        if scenario:
            report["scenario_sha256"]=sha(scenario.read_bytes())
        with tempfile.TemporaryDirectory(prefix="sc-publish-") as tmp:
            public=Path(tmp)
            for rel in PUBLIC:
                src=root/rel
                require(src.exists(),f"missing publish path {rel}")
                if src.is_dir():
                    shutil.copytree(src,public/rel)
                else:
                    shutil.copy2(src,public/rel)
            class Handler(SimpleHTTPRequestHandler):
                extensions_map={**SimpleHTTPRequestHandler.extensions_map,
                                ".webmanifest":"application/manifest+json"}
                def log_message(self,*args):
                    pass
                def end_headers(self):
                    self.send_header("Cache-Control","no-cache")
                    super().end_headers()
            transport=OriginTransport(lambda *a,**kw:Handler(*a,directory=tmp,**kw))
            transport.start()
            origin=transport.origin
            report["origin"]=origin
            try:
                if functional:
                    from functional_suite import run_suite
                    with sync_playwright() as pw:
                        run_suite(pw,origin,report,out,stage,transport)
                    report["status"]="PASS"
                    write(out,"report.json",report)
                    return 0
                with sync_playwright() as pw:
                    stage("launch Chromium")
                    browser=pw.chromium.launch(headless=True)
                    report["browser_version"]=browser.version
                    context=browser.new_context(viewport=report["viewport"],device_scale_factor=1,
                                                service_workers="allow")
                    def route(r):
                        if r.request.url.startswith(origin+"/"):
                            r.continue_()
                        else:
                            report["blocked_external_requests"]+=1
                            r.abort()
                    context.route("**/*",route)
                    if not diagnostic:
                        context.tracing.start(screenshots=True,snapshots=True,sources=False)
                    page=context.new_page()
                    page.set_default_timeout(10000)
                    page.on("pageerror",lambda e:report["page_errors"].append(str(e)[:500]))
                    page.on("response",lambda r:report["local_http_errors"].append(
                        {"url":r.url,"status":r.status}) if r.url.startswith(origin+"/") and r.status>=400 else None)
                    cdp=context.new_cdp_session(page)
                    profiling=False
                    probe=Diagnostic(cdp) if diagnostic else None
                    try:
                        if probe:
                            probe.start()
                        else:
                            cdp.send("Profiler.enable")
                            cdp.send("Profiler.start")
                            profiling=True
                        stage("online navigation")
                        response=page.goto(origin+"/index.html",wait_until="domcontentloaded",timeout=25000)
                        require(response is not None and response.ok,"online navigation failed")
                        report["online_response_sha256"]=sha(response.body())
                        require(report["online_response_sha256"]==report["html_sha256"],"wrong loaded HTML")
                        page.wait_for_function("""() => window.SC_PWA_STATUS?.ready === true &&
                            Boolean(navigator.serviceWorker.controller)""",timeout=30000)
                        stage("worker and version identity")
                        identity=page.evaluate("""async () => ({
                          title: document.title,
                          startup: window.SC_STARTUP_TRACE?.export()?.build ?? null,
                          diagnostic: window.SC_PWA_STATUS,
                          controller: navigator.serviceWorker.controller?.scriptURL ?? null,
                          active: (await navigator.serviceWorker.getRegistration())?.active?.state ?? null,
                          caches: await caches.keys()
                        })""")
                        report["online_identity"]=identity
                        require(identity["active"]=="activated" and identity["controller"]==origin+"/sw.js",
                                "unexpected active worker")
                        require(cache in identity["caches"],"expected shell cache missing")
                        require(identity["startup"]==version,"startup version mismatch")
                        # Fresh origin: active controller + network worker bytes + exact cached HTML.
                        actual=page.request.get(origin+"/sw.js",timeout=10000)
                        require(actual.ok and sha(actual.body())==report["sw_sha256"],"SW response bytes mismatch")
                        cached=page.evaluate("""async ([name,url]) => {
                            const response=await (await caches.open(name)).match(url);
                            if(!response)return null;
                            return Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',await response.arrayBuffer())))
                               .map(v=>v.toString(16).padStart(2,'0')).join('');
                        }""",[cache,origin+"/index.html"])
                        report["cached_html_sha256"]=cached
                        require(cached==report["html_sha256"],"wrong cached HTML")
                        capture_p1_startup(page,out,"online",version)
                        report["dom_snapshots"].append(measure_dom(page,"online-before-scenario"))
                        if probe:
                            phase=probe.capture("online-startup-identity")
                            require(has_observations(phase,origin+"/index.html"),"missing startup CDP observations")
                            write(out,"diagnostic.json",probe.report())
                        for i,s in enumerate(steps):
                            stage(f"scenario step {i+1}: {s['op']} {s['selector']}")
                            loc=page.locator(s["selector"])
                            if s["op"]=="click":
                                loc.click(timeout=10000)
                            elif s["op"]=="visible":
                                expect(loc).to_be_visible(timeout=10000)
                            else:
                                expect(loc).to_have_text(s["expected"],timeout=10000)
                            if s["op"] != "click":
                                report["dom_snapshots"].append(measure_dom(page,f"scenario assertion {i+1}"))
                                if probe:
                                    probe.capture(f"scenario-through-assertion-{i+1}")
                                    write(out,"diagnostic.json",probe.report())
                        page.screenshot(path=str(out/"online.png"),timeout=10000,animations="allow")
                        if probe:
                            probe.capture("online-before-reload")
                            write(out,"diagnostic.json",probe.report())
                        stage("offline navigation in same isolated context")
                        context.set_offline(True)
                        response=page.reload(wait_until="domcontentloaded",timeout=25000)
                        require(response is not None and response.ok,"offline navigation failed")
                        report["offline_response_sha256"]=sha(response.body())
                        require(response.from_service_worker,"offline navigation not served by SW")
                        require(report["offline_response_sha256"]==report["html_sha256"],"offline HTML differs")
                        page.wait_for_function("""() => Boolean(navigator.serviceWorker.controller)
                            && window.SC_STARTUP_TRACE?.export()?.build""",timeout=15000)
                        require(page.evaluate("() => window.SC_STARTUP_TRACE.export().build")==version,
                                "offline startup version mismatch")
                        capture_p1_startup(page,out,"offline",version)
                        report["dom_snapshots"].append(measure_dom(page,"offline-shell"))
                        page.screenshot(path=str(out/"offline.png"),timeout=10000,animations="allow")
                        if probe:
                            phase=probe.capture("offline-reload-shell")
                            require(has_observations(phase,origin+"/index.html"),"missing offline CDP observations")
                            write(out,"diagnostic.json",probe.report())
                        require(not report["page_errors"],"uncaught page errors")
                        require(not report["local_http_errors"],"local HTTP errors")
                        stage("assertions complete")
                    finally:
                        if profiling:
                            write(out,"cpu-profile.json",cdp.send("Profiler.stop")["profile"])
                        if probe:
                            probe.stop()
                            write(out,"diagnostic.json",probe.report())
                        else:
                            context.tracing.stop(path=str(out/"trace.zip"))
                        context.close()
                        browser.close()
            finally:
                transport.stop()
        report["status"]="PASS"
        report["scenario_steps_executed"]=len(steps)
    except Exception as exc:
        report["reason"]=f"{type(exc).__name__}: {exc}"[:2000]
        print(report["reason"],file=sys.stderr)
    write(out,"report.json",report)
    return 0 if report["status"]=="PASS" else 1


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--root",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--scenario",type=Path)
    mode=p.add_mutually_exclusive_group()
    mode.add_argument("--diagnostic",action="store_true")
    mode.add_argument("--functional",action="store_true")
    a=p.parse_args()
    if a.functional and a.scenario:
        p.error("functional suite uses its own reviewed contract, not --scenario")
    sys.exit(run(a.root.resolve(),a.out.resolve(),a.scenario,a.diagnostic,a.functional))
