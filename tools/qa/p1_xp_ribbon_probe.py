"""Temporary P1 private CI diagnostic. Not for merge. No source writes."""
import base64
from http.server import SimpleHTTPRequestHandler
import itertools
import json
import math
from pathlib import Path
import re
import shutil
import statistics
import sys
import tempfile
from playwright.sync_api import sync_playwright, expect
from runtime_smoke import PUBLIC, git, sha, require, version_info
from origin_transport import OriginTransport
from functional_suite import read, wait_save
from functional_contract import unchanged_inventory, purchase

ROOT=Path(__file__).resolve().parents[2]
BASE="b1928ed96a368735a45f0e2ef270c4f2844a820f"
HTML_SHA="492d9de51360b6b2d16217dc6b93440b759161bfbbcbc63dab2c3416f590823a"
OUT=Path(sys.argv[1]).resolve()
REPORT={"status":"RUNNING","scope":"headless desktop, isolated online, no trace during timing; frame opportunity proxy, not presentation or INP; no GPU or Android claim","base":BASE,"runs":[],"page_errors":[],"http_errors":[]}
def save():
    (OUT/"report.json").write_text(json.dumps(REPORT,indent=2),encoding="utf-8")
def transform(html):
    css=re.search(rb'(<style\b[^>]*\bid=["\x27]sc-main-css["\x27][^>]*>)(.*?)(</style>)',html,re.S)
    require(css is not None,"canonical CSS not found")
    src=css.group(2)
    matches=list(re.finditer(rb'--sc85-xp-ribbon:\s*(url\("data:image/png;base64,([A-Za-z0-9+/=]+)"\));',src))
    require(len(matches)==1 and src.count(b'var(--sc85-xp-ribbon)')==1 and src.count(b'--sc85-xp-ribbon')==2,"XP anchors mismatch")
    m=matches[0]
    asset=base64.b64decode(m.group(2),validate=True)
    require(asset.startswith(b'\x89PNG\r\n\x1a\n'),"not PNG")
    dest=(src[:m.start()]+src[m.end():]).replace(b'var(--sc85-xp-ribbon)',m.group(1))
    require(dest.count(m.group(1))==1 and b'--sc85-xp-ribbon' not in dest,"asset duplication or unresolved reference")
    REPORT["png_sha256"]=sha(asset)
    return html[:css.start(2)]+dest+html[css.end(2):]

# The trusted click starts the probe. No layout reads, screenshots or profiling
# inside the timed callback. Event Timing entries are threshold-censored.
PROBE="""() => {
  if(window.__scPilot) throw Error('duplicate probe');
  window.__scPilot={rows:[],events:[],supported:PerformanceObserver.supportedEntryTypes.includes('event')};
  const p=window.__scPilot;
  if(p.supported){p.observer=new PerformanceObserver(list=>{for(const e of list.getEntries())if(e.name==='click')p.events.push({start:e.startTime,processingStart:e.processingStart,processingEnd:e.processingEnd,duration:e.duration,interactionId:e.interactionId})});p.observer.observe({type:'event',buffered:false,durationThreshold:16});}
  window.addEventListener('click',e=>{
    if(!e.isTrusted||!e.target.closest("#sheet button[data-action='open'][data-value='shop']"))return;
    const row={start:e.timeStamp,capture:performance.now(),firstRAF:null,secondRAF:null};
    p.rows.push(row);
    requestAnimationFrame(()=>{row.firstRAF=performance.now();requestAnimationFrame(()=>{row.secondRAF=performance.now()})});
  },true);
}"""
SHOP="#sheet button[data-action='open'][data-value='shop']"
CLOSE="#panel > button[data-action='close-panel']"
CARD="#sheet .egtgrid .egt"
BUY="#sheet button[data-action='buy-egg'][data-value='0']"
def open_shop(p,n):
    p.locator("#nav-map").click()
    expect(p.locator("#sheet .screen-island-menu")).to_be_visible()
    p.locator(SHOP).click()
    p.wait_for_function("(n)=>window.__scPilot.rows.length===n && window.__scPilot.rows[n-1].secondRAF!==null",arg=n,timeout=10000)
    expect(p.locator("#sheet .screen-shop")).to_be_visible()
    expect(p.locator(BUY)).to_be_enabled()
def close_shop(p):
    p.locator(CLOSE).click()
    expect(p.locator("#panel")).to_be_hidden()
def visual(p):
    return p.locator(CARD).evaluate_all("""cards=>cards.map(c=>({name:c.querySelector('.sc84-egg-name').textContent, xp:c.querySelector('.xpb').textContent,button:c.querySelector('button').textContent,disabled:c.querySelector('button').disabled,background:getComputedStyle(c.querySelector('.xpb')).backgroundImage}))""")
def stats(values):
    vals=sorted(values)
    require(len(vals)>0,"no measurements")
    return {"n":len(vals),"p50":statistics.median(vals),"p95":vals[math.ceil(.95*len(vals))-1],"max":vals[-1]}
def main():
    require(OUT.is_dir() and not OUT.is_relative_to(ROOT),"output must be outside checkout")
    html=(ROOT/"index.html").read_bytes()
    sw=(ROOT/"sw.js").read_bytes()
    require(sha(html)==HTML_SHA,"baseline HTML mismatch")
    require(git(ROOT,"rev-parse","HEAD:sw.js")=="2f57bfd2fd38f8d220af090caa5c55c7580007f3","baseline SW mismatch")
    REPORT.update(commit=git(ROOT,"rev-parse","HEAD"),sw_sha256=sha(sw),probe_sha256=sha(Path(__file__).read_bytes()),viewport={"width":360,"height":780},dpr=1,version=version_info(html.decode(),sw.decode())[0],order=["".join(x) for x in itertools.permutations("ABR")],warm_repeats_per_context=5,first_open_repeats_per_variant=6,service_workers="blocked equally; online diagnostic only")
    candidate=transform(html)
    require(candidate!=html,"identical candidate")
    variants={"A":html,"B":candidate,"R":html}
    REPORT["variant_sha256"]={k:sha(v) for k,v in variants.items()}
    save()
    with tempfile.TemporaryDirectory(prefix="sc-p1-xp-") as tmp:
        public=Path(tmp)
        for rel in PUBLIC:
            src=ROOT/rel
            if src.is_dir(): shutil.copytree(src,public/rel)
            else: shutil.copy2(src,public/rel)
        class Handler(SimpleHTTPRequestHandler):
            def log_message(self,*args): pass
            def end_headers(self):
                self.send_header("Cache-Control","no-cache")
                super().end_headers()
        t=OriginTransport(lambda *a,**kw:Handler(*a,directory=tmp,**kw))
        t.start()
        try:
            with sync_playwright() as pw:
                oracle=None
                for block,order in enumerate(REPORT["order"],1):
                    browser=pw.chromium.launch(headless=True)
                    REPORT["browser_version"]=browser.version
                    try:
                        for label in order:
                            (public/"index.html").write_bytes(variants[label])
                            rec={"block":block,"variant":label,"status":"RUNNING","rows":[]}
                            REPORT["runs"].append(rec);save()
                            ctx=browser.new_context(viewport=REPORT["viewport"],device_scale_factor=1,service_workers="block")
                            try:
                                ctx.route("**/*",lambda r:r.continue_() if r.request.url.startswith(t.origin+"/") else r.abort())
                                p=ctx.new_page()
                                p.set_default_timeout(10000)
                                p.on("pageerror",lambda e:REPORT["page_errors"].append(str(e)[:500]))
                                p.on("response",lambda r:REPORT["http_errors"].append({"url":r.url,"status":r.status}) if r.url.startswith(t.origin+"/") and r.status>=400 else None)
                                response=p.goto(t.origin+"/index.html",wait_until="domcontentloaded",timeout=30000)
                                require(response is not None and response.ok and sha(response.body())==REPORT["variant_sha256"][label],"wrong served HTML")
                                expect(p.locator("#boot")).to_be_hidden(timeout=30000)
                                expect(p.locator("#scene")).to_be_visible()
                                require(p.evaluate("()=>window.SC_STARTUP_TRACE.export().build")==REPORT["version"],"wrong version")
                                before=read(p)
                                require(before["level"]==1 and len(before["eggs"])==1 and not before["built"],"fresh profile required")
                                p.evaluate(PROBE)
                                for n in range(1,7):
                                    open_shop(p,n)
                                    close_shop(p)
                                    rec["rows"]=p.evaluate("()=>window.__scPilot.rows")
                                    save()
                                rec["event_timing_supported"]=p.evaluate("()=>window.__scPilot.supported")
                                rec["event_timing"]=p.evaluate("()=>window.__scPilot.events")
                                require(len(rec["rows"])==6,"missing click observations")
                                for row in rec["rows"]:
                                    require(row["firstRAF"] is not None and row["secondRAF"] is not None and row["start"]<=row["capture"]+1 and row["capture"]<=row["firstRAF"]<=row["secondRAF"],"invalid timing order")
                                unchanged_inventory(before,read(p))
                                save()
                                # Visual and purchase verification after timing.
                                open_shop(p,7)
                                v=visual(p)
                                require(len(v)==8,"expected eight egg cards")
                                require(all(x["background"].startswith('url("data:image/png;base64,') for x in v),"ribbon missing")
                                require(all(sha(base64.b64decode(x["background"].split(",",1)[1][:-2]))==REPORT["png_sha256"] for x in v),"ribbon source changed")
                                if oracle is None: oracle=v
                                require(v==oracle,"visual text/eligibility/background changed")
                                rec["visual_signature_sha256"]=sha(json.dumps(v,sort_keys=True).encode())
                                p.locator("#sheet").screenshot(path=str(OUT/f"block-{block}-{label}.png"),timeout=10000)
                                old=read(p)
                                p.locator(BUY).click()
                                after=wait_save(p,lambda s:len(s["eggs"])==len(old["eggs"])+1,"P1 purchase")
                                purchase(old,after)
                                require(not REPORT["page_errors"] and not REPORT["http_errors"],"page or local HTTP error")
                                rec.update(status="PASS",purchase="PASS",inventory="PASS")
                                save()
                                print("PASS block",block,label,flush=True)
                            finally:
                                ctx.close()
                    finally:
                        browser.close()
        finally:
            t.stop()
    require(len(REPORT["runs"])==18 and all(r["status"]=="PASS" for r in REPORT["runs"]),"incomplete run")
    REPORT["summary"]={}
    for label in "ABR":
        runs=[r for r in REPORT["runs"] if r["variant"]==label]
        REPORT["summary"][label]={}
        for cohort,rows in [("first",[r["rows"][0] for r in runs]),("warm",[x for r in runs for x in r["rows"][1:]])]:
            REPORT["summary"][label][cohort]={"input_to_capture":stats([x["capture"]-x["start"] for x in rows]),"input_to_first_raf":stats([x["firstRAF"]-x["start"] for x in rows]),"input_to_second_raf":stats([x["secondRAF"]-x["start"] for x in rows])}
    REPORT["status"]="PASS"
    REPORT["interpretation"]="Pilot completed, not optimization acceptance. Event Timing is threshold-censored. Screenshots require review; no GPU, Android, cold-start, after-race, offline or full PL-01 release claim."
    save()
    print(json.dumps(REPORT["summary"]),flush=True)
try:
    main()
except Exception as e:
    REPORT.update(status="FAIL",reason=f"{type(e).__name__}: {e}"[:1500])
    save()
    raise
