"""Temporary isolated startup A/B/R experiment, not for merge."""
from http.server import SimpleHTTPRequestHandler
import difflib
import itertools
import json
import math
from pathlib import Path
import shutil
import statistics
import sys
import tempfile
from playwright.sync_api import sync_playwright, expect
from runtime_smoke import PUBLIC, git, sha, require, version_info
from origin_transport import OriginTransport
from functional_suite import read
from functional_contract import unchanged_inventory

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(sys.argv[1]).resolve()
BASE="e1d856242fc02faf5a41375416cffc9b2ea162f2"
HTML_SHA="492d9de51360b6b2d16217dc6b93440b759161bfbbcbc63dab2c3416f590823a"
REPORT={"status":"RUNNING","base":BASE,"runs":[],"page_errors":[],"http_errors":[],"scope":"headless desktop localhost; online fresh contexts and same-context offline reload; existing startup marks; no profiler or trace during timing; submitted frame not presentation, no physical device or GPU completion proof"}
def save():
    (OUT/"report.json").write_text(json.dumps(REPORT,indent=2),encoding="utf-8")
def transform(html):
    old="""    const scMapLoad=scT?.begin();
    const image=await loadImage('data:image/webp;base64,'+raw);
    scT?.end('map.imageOnload',scMapLoad);scT?.probeDecode(image,'map');
    this.mapImage=image;
    const fountainElement=document.getElementById('illustrated-fountain-webp');
    if(!fountainElement)throw Error('Nedostaje animirana fontana.');
    this.fountainImage=await loadImage('data:image/webp;base64,'+fountainElement.textContent.trim());
"""
    new="""    const scMapLoad=scT?.begin();
    const mapPending=loadImage('data:image/webp;base64,'+raw);
    const fountainElement=document.getElementById('illustrated-fountain-webp');
    const fountainPending=fountainElement?loadImage('data:image/webp;base64,'+fountainElement.textContent.trim()).then(value=>({ok:true,value}),error=>({ok:false,error})):null;
    const image=await mapPending;
    scT?.end('map.imageOnload',scMapLoad);scT?.probeDecode(image,'map');
    this.mapImage=image;
    if(!fountainElement)throw Error('Nedostaje animirana fontana.');
    const fountainResult=await fountainPending;
    if(!fountainResult.ok)throw fountainResult.error;
    this.fountainImage=fountainResult.value;
"""
    require(html.count(old.encode())==1,"startup anchor mismatch")
    candidate=html.replace(old.encode(),new.encode())
    (OUT/"isolated-source.diff").write_text("".join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile="A",tofile="B")),encoding="utf-8")
    return candidate
def readout(p,version):
    p.wait_for_function("""() => {
      const t=window.SC_STARTUP_TRACE?.export();
      return t?.timings?.some(x=>x.label==='boot.overlayRemoved') &&
             t.timings.some(x=>x.label==='canvas.firstSubmittedFrame');
    }""",timeout=30000)
    t=p.evaluate("()=>window.SC_STARTUP_TRACE.export()")
    require(t["build"]==version,"wrong build")
    labels={x["label"]:x for x in t["timings"]}
    needed={"boot.enter","boot.overlayRemoved","boot.parallelTasksComplete","map.artTotal","canvas.firstSubmittedFrame","idb.load.transaction"}
    require(needed.issubset(labels),"missing startup marks: "+str(needed-labels.keys()))
    require(not any(x.startswith("decode.") for x in labels),"decode probe enabled")
    return {"trace":t,"first_submitted_ms":labels["canvas.firstSubmittedFrame"]["startMs"],"overlay_removed_ms":labels["boot.overlayRemoved"]["startMs"],"map_art_ms":labels["map.artTotal"]["durationMs"],"idb_complete_ms":labels["idb.load.transaction"]["startMs"]+labels["idb.load.transaction"]["durationMs"]}
def stats(vals):
    v=sorted(vals);require(len(v)==24,"incomplete cohort")
    return {"n":len(v),"p50":statistics.median(v),"p95":v[math.ceil(.95*len(v))-1],"max":v[-1]}
def main():
    require(OUT.is_dir() and not OUT.is_relative_to(ROOT),"output outside checkout")
    html=(ROOT/"index.html").read_bytes();sw=(ROOT/"sw.js").read_bytes()
    require(sha(html)==HTML_SHA,"wrong HTML")
    require(git(ROOT,"rev-parse","HEAD:sw.js")=="2f57bfd2fd38f8d220af090caa5c55c7580007f3","wrong SW")
    version,cache=version_info(html.decode(),sw.decode())
    variants={"A":html,"B":transform(html),"R":html}
    REPORT.update(commit=git(ROOT,"rev-parse","HEAD"),version=version,cache=cache,variant_sha256={k:sha(x) for k,x in variants.items()},sw_sha256=sha(sw),viewport={"width":360,"height":780},dpr=1,orders=["".join(x) for x in itertools.permutations("ABR")],repetitions=4)
    save()
    with tempfile.TemporaryDirectory(prefix="sc-startup-abr-") as tmp:
        public=Path(tmp)
        for rel in PUBLIC:
            src=ROOT/rel
            if src.is_dir():shutil.copytree(src,public/rel)
            else:shutil.copy2(src,public/rel)
        class Handler(SimpleHTTPRequestHandler):
            extensions_map={**SimpleHTTPRequestHandler.extensions_map,".webmanifest":"application/manifest+json"}
            def log_message(self,*args):pass
            def end_headers(self):
                self.send_header("Cache-Control","no-cache")
                super().end_headers()
        t=OriginTransport(lambda *a,**kw:Handler(*a,directory=tmp,**kw));t.start()
        try:
            with sync_playwright() as pw:
                for block,order in enumerate(REPORT["orders"],1):
                    browser=pw.chromium.launch(headless=True);REPORT["browser_version"]=browser.version
                    try:
                        for repeat in range(1,5):
                            for label in order:
                                (public/"index.html").write_bytes(variants[label])
                                rec={"block":block,"repeat":repeat,"variant":label,"status":"RUNNING"}
                                REPORT["runs"].append(rec);save()
                                ctx=browser.new_context(viewport=REPORT["viewport"],device_scale_factor=1,service_workers="allow")
                                try:
                                    ctx.route("**/*",lambda r:r.continue_() if r.request.url.startswith(t.origin+"/") else r.abort())
                                    p=ctx.new_page()
                                    p.on("pageerror",lambda e:REPORT["page_errors"].append(str(e)[:500]))
                                    p.on("response",lambda r:REPORT["http_errors"].append({"url":r.url,"status":r.status}) if r.url.startswith(t.origin+"/") and r.status>=400 else None)
                                    response=p.goto(t.origin+"/index.html",wait_until="domcontentloaded",timeout=30000)
                                    require(response is not None and response.ok and sha(response.body())==REPORT["variant_sha256"][label],"wrong online bytes")
                                    rec["online"]=readout(p,version);save()
                                    expect(p.locator("#boot")).to_be_hidden(timeout=30000)
                                    expect(p.locator("#scene")).to_be_visible()
                                    p.wait_for_function("()=>window.SC_PWA_STATUS?.ready===true && !!navigator.serviceWorker.controller",timeout=30000)
                                    require(p.evaluate("()=>navigator.serviceWorker.controller.scriptURL")==t.origin+"/sw.js","worker mismatch")
                                    before=read(p)
                                    require(before["level"]==1 and len(before["snails"])==2 and not before["built"],"fresh profile required")
                                    if repeat==1:p.screenshot(path=str(OUT/f"online-{block}-{label}.png"),timeout=10000)
                                    ctx.set_offline(True)
                                    response=p.reload(wait_until="domcontentloaded",timeout=30000)
                                    require(response is not None and response.ok and response.from_service_worker and sha(response.body())==REPORT["variant_sha256"][label],"wrong offline bytes or missing SW")
                                    rec["offline"]=readout(p,version);save()
                                    expect(p.locator("#boot")).to_be_hidden(timeout=30000)
                                    expect(p.locator("#scene")).to_be_visible()
                                    unchanged_inventory(before,read(p))
                                    if repeat==1:p.screenshot(path=str(OUT/f"offline-{block}-{label}.png"),timeout=10000)
                                    require(not REPORT["page_errors"] and not REPORT["http_errors"],"page/local HTTP error")
                                    rec["status"]="PASS";save()
                                finally:ctx.close()
                    finally:browser.close()
        finally:t.stop()
    require(len(REPORT["runs"])==72 and all(r["status"]=="PASS" for r in REPORT["runs"]),"incomplete run")
    REPORT["summary"]={label:{phase:{metric:stats([r[phase][metric] for r in REPORT["runs"] if r["variant"]==label]) for metric in ("first_submitted_ms","overlay_removed_ms","map_art_ms","idb_complete_ms")} for phase in ("online","offline")} for label in "ABR"}
    REPORT["status"]="PASS";save()
    print(json.dumps(REPORT["summary"]),flush=True)
try:main()
except Exception as e:
    REPORT.update(status="FAIL",reason=f"{type(e).__name__}: {e}"[:1500]);save();raise
