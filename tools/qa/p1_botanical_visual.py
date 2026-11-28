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
BASE="f0a5b4ca04e134e4f987a77e9fece7f0f979fce1"
HTML_SHA="492d9de51360b6b2d16217dc6b93440b759161bfbbcbc63dab2c3416f590823a"
OUT=Path(sys.argv[1]).resolve()
REPORT={"status":"RUNNING","scope":"headless desktop, isolated online, no trace during timing; frame opportunity proxy, not presentation or INP; no GPU or Android claim","base":BASE,"runs":[],"page_errors":[],"http_errors":[]}
def save():
    (OUT/"report.json").write_text(json.dumps(REPORT,indent=2),encoding="utf-8")
def transform(html):
    css=re.search(rb'(<style\b[^>]*\bid=["\x27]sc-main-css["\x27][^>]*>)(.*?)(</style>)',html,re.S)
    require(css is not None,"canonical CSS not found")
    src=css.group(2)
    matches=list(re.finditer(rb'--sc85-botanical-corner:\s*(url\("data:image/png;base64,([A-Za-z0-9+/=]+)"\));',src))
    require(len(matches)==1 and src.count(b'--sc85-botanical-corner')==4,"botanical anchors mismatch")
    m=matches[0]
    asset=base64.b64decode(m.group(2),validate=True)
    require(asset.startswith(b'\x89PNG\r\n\x1a\n') and html.count(m.group(2))==1,"PNG identity or duplicate mismatch")
    dest=src[:m.start()]+src[m.end():]
    for suffix,count in [(b' top right/contain no-repeat',2),(b' center/contain no-repeat',1)]:
        token=b'background:var(--sc85-botanical-corner)'+suffix
        require(dest.count(token)==count,"consumer mismatch")
        dest=dest.replace(token,b'background:none')
    require(b'--sc85-botanical-corner' not in dest and m.group(2) not in dest,"unresolved botanical resource")
    REPORT.update(png_sha256=sha(asset),png_bytes=len(asset),base64_bytes=len(m.group(2)),removed_consumer_backgrounds=3)
    result=html[:css.start(2)]+dest+html[css.end(2):]
    REPORT["html_bytes"]={"A":len(html),"B":len(result),"R":len(html)}
    return result

def decoration(p,label,selector,pseudo,expected_count=None):
    vals=p.locator(selector).evaluate_all("(nodes,pseudo)=>nodes.map(n=>getComputedStyle(n,pseudo).backgroundImage)",pseudo)
    require(bool(vals),"missing decoration consumer: "+selector)
    if expected_count is not None:
        require(len(vals)==expected_count,"unexpected consumer count: "+selector)
    for value in vals:
        if label=="B":
            require(value=="none","removed decoration still rendered")
        else:
            require(value.startswith('url("data:image/png;base64,') and sha(base64.b64decode(value.split(",",1)[1][:-2],validate=True))==REPORT["png_sha256"],"original decoration missing or changed")
    return len(vals)


def open_place(p,key,action="open",value=None):
    p.locator("#nav-map").click()
    expect(p.locator("#sheet .screen-island-menu")).to_be_visible()
    p.locator(f"#sheet button[data-action='{action}'][data-value='{value or key}']").click()
    expect(p.locator("#sheet .screen-"+key)).to_be_visible()
def close(p):
    p.locator("#panel > button[data-action='close-panel']").click()
    expect(p.locator("#panel")).to_be_hidden()
def inspect(p,rec,label,key,rows=False):
    sel="#sheet .screen-"+key
    expect(p.locator(sel)).to_be_visible()
    rec[key]={"head":decoration(p,label,sel,"::before",1)}
    if rows:
        rec[key]["rows"]=decoration(p,label,sel+" .sn-row","::before",2)
    rec[key]["controls"]=p.locator(sel+" button, "+sel+" select, "+sel+" input").evaluate_all("""nodes=>nodes.map(n=>[n.tagName,n.dataset.action??'',n.dataset.value??'',n.id,n.disabled])""")
    p.locator("#sheet").screenshot(path=str(OUT/(label+"-"+key+".png")),timeout=10000)
    close(p)
def main():
    require(OUT.is_dir() and not OUT.is_relative_to(ROOT),"output outside checkout")
    html=(ROOT/"index.html").read_bytes()
    require(sha(html)==HTML_SHA,"wrong HTML")
    require(git(ROOT,"rev-parse","HEAD:sw.js")=="2f57bfd2fd38f8d220af090caa5c55c7580007f3","wrong SW")
    variants={"A":html,"B":transform(html),"R":html}
    REPORT.update(commit=git(ROOT,"rev-parse","HEAD"),variant_sha256={k:sha(x) for k,x in variants.items()},scope="visual coverage of five affected screens; synthetic level 6 breeding fixture; not a timing benchmark or physical Android",viewport={"width":360,"height":780},dpr=1)
    save()
    with tempfile.TemporaryDirectory(prefix="sc-p1-botanical-visual-") as tmp:
        public=Path(tmp)
        for rel in PUBLIC:
            src=ROOT/rel
            if src.is_dir():shutil.copytree(src,public/rel)
            else:shutil.copy2(src,public/rel)
        class Handler(SimpleHTTPRequestHandler):
            def log_message(self,*args):pass
            def end_headers(self):
                self.send_header("Cache-Control","no-cache")
                super().end_headers()
        t=OriginTransport(lambda *a,**kw:Handler(*a,directory=tmp,**kw))
        t.start()
        try:
            with sync_playwright() as pw:
                browser=pw.chromium.launch(headless=True)
                REPORT["browser_version"]=browser.version
                try:
                    oracle=None
                    for label in "ABR":
                        (public/"index.html").write_bytes(variants[label])
                        rec={"variant":label,"status":"RUNNING","screens":{}}
                        REPORT["runs"].append(rec);save()
                        ctx=browser.new_context(viewport=REPORT["viewport"],device_scale_factor=1,service_workers="block")
                        try:
                            ctx.route("**/*",lambda r:r.continue_() if r.request.url.startswith(t.origin+"/") else r.abort())
                            p=ctx.new_page()
                            p.set_default_timeout(10000)
                            p.on("pageerror",lambda e:REPORT["page_errors"].append(str(e)[:500]))
                            p.on("response",lambda r:REPORT["http_errors"].append({"url":r.url,"status":r.status}) if r.url.startswith(t.origin+"/") and r.status>=400 else None)
                            def nav():
                                response=p.goto(t.origin+"/index.html",wait_until="domcontentloaded",timeout=30000)
                                require(response is not None and response.ok and sha(response.body())==REPORT["variant_sha256"][label],"wrong served HTML")
                                expect(p.locator("#boot")).to_be_hidden(timeout=30000)
                                expect(p.locator("#scene")).to_be_visible()
                            nav()
                            seed=read(p)
                            require(seed["level"]==1 and len(seed["snails"])==2 and not seed["built"],"fresh fixture required")
                            seed["level"]=6;seed["built"]=["breeding"]
                            payload=json.dumps(seed).encode("utf-8")
                            rec["fixture_sha256"]=sha(payload)
                            p.locator("nav.navigation button[data-action='open'][data-value='settings']").click()
                            expect(p.locator("#sheet .setbox")).to_be_visible()
                            with p.expect_file_chooser() as fc:
                                p.locator("#sheet button[data-action='import']").click()
                            fc.value.set_files({"name":"qa-botanical-level6.json","mimeType":"application/json","buffer":payload})
                            p.locator("#sheet button[data-action='confirm-import']").click()
                            loaded=wait_save(p,lambda s:s["level"]==6 and "breeding" in s["built"],"level6 fixture")
                            require(loaded["saveId"]==seed["saveId"] and loaded["revision"]>seed["revision"],"fixture not committed")
                            nav()
                            before=read(p)
                            screens=rec["screens"]
                            open_place(p,"shop")
                            inspect(p,screens,label,"shop")
                            p.locator("nav.navigation button[data-action='open'][data-value='collection']").click()
                            expect(p.locator("#sheet .screen-collection")).to_be_visible()
                            p.locator("#sheet button[data-action='collection-mode'][data-value='mine']").click()
                            inspect(p,screens,label,"collection",True)
                            open_place(p,"tree");inspect(p,screens,label,"tree",True)
                            open_place(p,"habitat","habitat-open","h1");inspect(p,screens,label,"habitat",True)
                            open_place(p,"breeding")
                            expect(p.locator("#parent-a")).to_be_visible()
                            expect(p.locator("#parent-b")).to_be_visible()
                            inspect(p,screens,label,"breeding")
                            unchanged_inventory(before,read(p))
                            controls={k:v["controls"] for k,v in screens.items()}
                            if oracle is None:oracle=controls
                            require(controls==oracle,"control signature changed")
                            require(not REPORT["page_errors"] and not REPORT["http_errors"],"page/local HTTP error")
                            rec["status"]="PASS";save()
                        finally:ctx.close()
                finally:browser.close()
        finally:t.stop()
    require(len(REPORT["runs"])==3 and all(r["status"]=="PASS" and len(r["screens"])==5 for r in REPORT["runs"]),"incomplete visual coverage")
    REPORT["status"]="PASS";save()
try:main()
except Exception as e:
    REPORT.update(status="FAIL",reason=f"{type(e).__name__}: {e}"[:1500]);save();raise
