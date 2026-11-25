"""Real isolated UI actions + read-only independent IndexedDB oracle.
Uses runtime_smoke's exact copied publish origin and external watchdog.
No production injection; no cloud actions; no player profile.
"""
import hashlib
import json
import tempfile
import time
from pathlib import Path
from playwright.sync_api import expect
from dom_audit import measure_dom
from functional_contract import (CASE_IDS,EGG_KIND,EGG_PRICE,REPEATS,PROFILE_NAME,
                                 require,snapshot,unchanged_inventory,purchase,durable,accepted_cases)

# Actual block-21.js L3310-L3388, read current after transaction completion.
# Do not create a missing DB/store or fall back to a different storage.
READ_CURRENT=r"""async () => {
 const list=await indexedDB.databases();
 if(!list.some(d=>d.name==='snail-city-rebuild'&&d.version===1))
   throw Error('expected IndexedDB missing');
 return await new Promise((resolve,reject)=>{
   const req=indexedDB.open('snail-city-rebuild',1);
   req.onupgradeneeded=()=>{req.transaction.abort();reject(Error('unexpected upgrade'));};
   req.onerror=()=>reject(req.error);
   req.onblocked=()=>reject(Error('read blocked'));
   req.onsuccess=()=>{
     const db=req.result;
     try{
       const tx=db.transaction('snapshots','readonly');
       const get=tx.objectStore('snapshots').get('current');
       tx.oncomplete=()=>{db.close();if(get.result)resolve(get.result);else reject(Error('missing current'));};
       tx.onabort=()=>{db.close();reject(tx.error||Error('read aborted'));};
     }catch(e){db.close();reject(e);}
   };
 });
}"""

def read(page):
    return page.evaluate(READ_CURRENT)

def wait_save(page,predicate,description,timeout=10):
    deadline=time.monotonic()+timeout
    while time.monotonic()<deadline:
        state=read(page)
        if predicate(state):
            return state
        page.wait_for_timeout(100) # bounded polling of the actual durable state
    raise AssertionError("committed state not observed: "+description)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def run_suite(pw,origin,report,out,stage):
    report["scope"]="local desktop Chromium functional QA; no physical Android, cloud or full progression"
    report["functional_cases"]={k:{"status":"NOT RUN","assertions":0} for k in CASE_IDS}
    report["functional_mode"]=True
    report["functional_contract_sha256"]=sha(Path(__file__).with_name("functional_contract.py").read_bytes())
    report["functional_suite_sha256"]=sha(Path(__file__).read_bytes())
    report["functional_limitations"]=["B06 uses separate synthetic level-3 fixture imported by the actual UI; not natural progression or construction.",
        "B06 starts training, observes progress, pauses and abandons; no race completion/reward claim.",
        "B05 negative control is disabled native button and bounded observed no mutation; not direct reducer rejection or concurrent command test.",
        "Offline is same persistent desktop profile, new Chromium process/context, same origin; not installed Android/Force Stop.",
        "DOM probes and Playwright tracing are diagnostic, not performance benchmarks."]
    active=[None]
    def step(label):
        stage("functional "+label)
    def check(ok,message):
        require(ok,message)
        report["functional_cases"][active[0]]["assertions"]+=1
    def case(ident,fn):
        active[0]=ident
        rec=report["functional_cases"][ident]
        rec["status"]="RUNNING"
        step(ident+" begin")
        try:
            fn(rec)
            check(not report["page_errors"] and not report["local_http_errors"],"uncaught page/local HTTP error")
            rec["status"]="PASS"
            step(ident+" complete")
        except Exception as exc:
            rec.update(status="FAIL",reason=f"{type(exc).__name__}: {exc}"[:1500])
            step(ident+" failed")
            raise
        finally:
            active[0]=None

    def launch(profile,offline=False):
        context=pw.chromium.launch_persistent_context(str(profile),headless=True,
            viewport=report["viewport"],device_scale_factor=1,service_workers="allow",
            offline=offline)
        def route(r):
            if r.request.url.startswith(origin+"/"):
                r.continue_()
            else:
                report["blocked_external_requests"]+=1
                r.abort()
        context.route("**/*",route)
        context.tracing.start(screenshots=True,snapshots=True,sources=False)
        page=context.pages[0] if context.pages else context.new_page()
        page.set_default_timeout(10000)
        page.on("pageerror",lambda e:report["page_errors"].append(str(e)[:500]))
        page.on("response",lambda r:report["local_http_errors"].append(
            {"url":r.url,"status":r.status}) if r.url.startswith(origin+"/") and r.status>=400 else None)
        cdp=context.new_cdp_session(page)
        try:
            report["browser_version"]=cdp.send("Browser.getVersion")["product"]
        finally:
            cdp.detach()
        return context,page

    def close(context,name):
        try:
            context.tracing.stop(path=str(out/name))
        finally:
            context.close()

    def navigate(page,offline=False):
        response=page.goto(origin+"/index.html",wait_until="domcontentloaded",timeout=30000)
        require(response is not None and response.ok,"navigation failed")
        require(sha(response.body())==report["html_sha256"],"wrong HTML bytes")
        if offline:
            require(response.from_service_worker,"cold offline response not served by SW")
        page.wait_for_function("() => !!navigator.serviceWorker.controller && window.SC_STARTUP_TRACE?.export()?.build",timeout=30000)
        require(page.evaluate("()=>window.SC_STARTUP_TRACE.export().build")==report["source_version"],"wrong runtime version")
        expect(page.locator("#boot")).to_have_count(1)
        expect(page.locator("#boot")).to_be_hidden(timeout=30000)
        expect(page.locator("#scene")).to_be_visible()
        require(page.evaluate("()=>navigator.serviceWorker.controller.scriptURL")==origin+"/sw.js","wrong worker")
        require(report["expected_cache"] in page.evaluate("()=>caches.keys()"),"expected cache absent")
        if not offline:
            page.wait_for_function("()=>window.SC_PWA_STATUS?.ready === true",timeout=30000)
            actual=page.request.get(origin+"/sw.js",timeout=10000)
            require(actual.ok and sha(actual.body())==report["sw_sha256"],"SW response differs")
        return {"from_service_worker":response.from_service_worker,"html_sha256":sha(response.body())}

    def assert_open(page,key):
        expect(page.locator("#panel[open]")).to_be_visible()
        expect(page.locator("#sheet "+(".setbox" if key=="settings" else ".screen-"+key))).to_be_visible()
    def dismiss(page,key):
        selector="#sheet button[data-action='close-panel']" if key=="settings" else "#panel > button[data-action='close-panel']"
        page.locator(selector).click()
        expect(page.locator("#panel")).not_to_have_attribute("open","")
        expect(page.locator("#panel")).to_be_hidden()
        expect(page.locator("#nav-map")).to_be_visible()
    def places(page,key):
        page.locator("#nav-map").click()
        assert_open(page,"island-menu")
        page.locator(f"#sheet button[data-action='open'][data-value='{key}']").click()
        assert_open(page,key)
    def settings(page):
        page.locator("nav.navigation button[data-action='open'][data-value='settings']").click()
        assert_open(page,"settings")

    with tempfile.TemporaryDirectory(prefix="sc-functional-profile-") as tmp:
        profile=Path(tmp)/"ordinary"
        ctx,p=launch(profile)
        saved=None
        try:
            report["functional_online_identity"]=navigate(p)
            initial=read(p)
            require(initial["level"]==1 and len(initial["eggs"])==1 and not initial["built"],
                    "fresh-profile precondition not met")
            def navigation(rec):
                for key in ("collection","progress"):
                    p.locator(f"nav.navigation button[data-action='open'][data-value='{key}']").click()
                    assert_open(p,key);dismiss(p,key);check(True,key+" opened/closed")
                settings(p);dismiss(p,"settings");check(True,"settings opened/closed")
                for key in ("incubator","shop","races"):
                    places(p,key)
                    if key=="races":
                        expect(p.locator("#sheet button[data-action='build'][data-value='races']")).to_be_disabled()
                        check(True,"level-1 race gate enforced")
                    dismiss(p,key);check(True,key+" opened/closed")
                unchanged_inventory(initial,read(p));check(True,"navigation did not change durable inventory")
            case("B01",navigation)
            def repeat(rec):
                before=read(p)
                rec["cycles"]=[]
                for i in range(REPEATS):
                    step(f"B02 cycle {i+1}/{REPEATS}")
                    places(p,"shop")
                    if i in (0,REPEATS-1):
                        report["dom_snapshots"].append(measure_dom(p,f"shop-cycle-{i+1}"))
                    dismiss(p,"shop")
                    rec["cycles"].append(i+1)
                    check(True,"cycle completed")
                unchanged_inventory(before,read(p));check(len(rec["cycles"])==REPEATS,"all cycles")
            case("B02",repeat)
            def profile_write(rec):
                before=read(p)
                settings(p)
                p.locator("#player-name").fill(PROFILE_NAME)
                p.locator("#sheet button[data-action='player-name']").click()
                after=wait_save(p,lambda s:s.get("playerName")==PROFILE_NAME,"profile name")
                check(after["saveId"]==before["saveId"] and after["revision"]>before["revision"],"profile commit identity")
                expect(p.locator("#player-name")).to_have_value(PROFILE_NAME)
                check(True,"profile input matches committed name")
                rec.update(before=snapshot(before),after=snapshot(after))
                dismiss(p,"settings")
            case("B03",profile_write)
            def buy(rec):
                nonlocal saved
                places(p,"shop")
                button=p.locator(f"#sheet button[data-action='buy-egg'][data-value='{EGG_KIND}']")
                expect(button).to_be_enabled()
                before=read(p)
                button.click()
                after=wait_save(p,lambda s:len(s["eggs"])>len(before["eggs"]),"egg purchase")
                purchase(before,after);check(True,"one purchase exact debit/inventory")
                expect(button).to_be_disabled()
                button.scroll_into_view_if_needed()
                box=button.bounding_box()
                require(box is not None,"disabled control missing box")
                p.mouse.click(box["x"]+box["width"]/2,box["y"]+box["height"]/2)
                # Negative observation window, NOT a timing benchmark or proof of arbitrary future behavior.
                for _ in range(3):
                    p.wait_for_timeout(100)
                    unchanged_inventory(after,read(p))
                check(True,"full incubator blocked second purchase in observation window")
                dismiss(p,"shop")
                places(p,"incubator")
                expect(p.locator("#sheet .egg-card")).to_have_count(len(after["eggs"]))
                check(True,"incubator UI matches durable egg count")
                p.screenshot(path=str(out/"functional-purchase.png"),timeout=10000)
                dismiss(p,"incubator")
                saved=read(p)
                rec.update(before=snapshot(before),after=snapshot(saved),negative_observation_ms=300)
            case("B05",buy)
        finally:
            close(ctx,"functional-online-trace.zip")

        def cold(rec):
            require(saved is not None,"no committed purchase")
            ctx,p=launch(profile,offline=True)
            try:
                rec["identity"]=navigate(p,offline=True)
                network_failed=p.evaluate("""async () => {
                  try{await fetch('/__sc_qa_uncached_network_probe__',{cache:'no-store'});return false;}
                  catch(e){return true;}
                }""")
                check(network_failed,"uncached network probe must fail")
                after=read(p)
                durable(saved,after);check(True,"same durable save after process close/reopen")
                expect(p.locator("#level")).to_have_text(str(saved["level"]))
                check(True,"visible level")
                settings(p);expect(p.locator("#player-name")).to_have_value(PROFILE_NAME)
                check(True,"visible saved name");dismiss(p,"settings")
                places(p,"incubator");expect(p.locator("#sheet .egg-card")).to_have_count(len(saved["eggs"]))
                check(True,"visible durable eggs")
                p.screenshot(path=str(out/"functional-offline.png"),timeout=10000)
                rec.update(before=snapshot(saved),after=snapshot(after),profile_reopened=True,network_probe_failed=True)
                dismiss(p,"incubator")
            finally:
                close(ctx,"functional-offline-trace.zip")
        case("B04",cold)

        def race(rec):
            ctx,p=launch(Path(tmp)/"race-fixture")
            try:
                navigate(p)
                seed=read(p)
                require(seed["level"]==1 and not seed["built"],"race fixture not fresh")
                seed["level"]=3;seed["built"]=["races"]
                payload=json.dumps(seed).encode("utf-8")
                rec["fixture_sha256"]=sha(payload)
                rec["fixture_changes"]={"level":3,"built":["races"]}
                settings(p)
                with p.expect_file_chooser() as fc:
                    p.locator("#sheet button[data-action='import']").click()
                fc.value.set_files({"name":"qa-race-fixture.json","mimeType":"application/json","buffer":payload})
                p.locator("#sheet button[data-action='confirm-import']").click()
                imported=wait_save(p,lambda s:s["level"]==3 and "races" in s["built"],"imported race fixture")
                check(imported["saveId"]==seed["saveId"] and imported["revision"]>seed["revision"],"real UI import committed")
                navigate(p) # boot normalizes layout using existing owner
                places(p,"races")
                p.locator("#sheet button[data-action='race-mode'][data-value='training']").click()
                start=p.locator("#sheet button[data-action='start-race']")
                expect(start).to_be_enabled()
                canvas=p.locator("#scene").element_handle()
                start.click()
                expect(p.locator("#race-ui")).to_be_visible(timeout=30000)
                p.wait_for_function("()=>document.querySelector('#race-progress')?.value>0",timeout=30000)
                check(True,"actual race advanced")
                p.locator("#race-ui button[data-action='pause']").click()
                expect(p.locator("#sheet button[data-action='resume']")).to_be_visible()
                check(True,"pause UI")
                p.screenshot(path=str(out/"functional-race.png"),timeout=10000)
                p.locator("#sheet button[data-action='return-map']").click()
                expect(p.locator("#race-ui")).to_be_hidden()
                check(p.evaluate("(el)=>document.querySelector('#scene')===el",canvas),"same canvas after return")
                places(p,"shop");dismiss(p,"shop");check(True,"first post-race shop action")
                rec["scope"]="training advanced, paused, abandoned and map action; no reward/completion claim"
            finally:
                close(ctx,"functional-race-trace.zip")
        case("B06",race)
    require(accepted_cases(report),"incomplete functional cases")
    report["functional_assertions"]=sum(x["assertions"] for x in report["functional_cases"].values())
