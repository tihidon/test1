"""Disposable Chromium fixtures only. Never executes or edits Snail City."""
import json
from pathlib import Path
import sys
from playwright.sync_api import sync_playwright
from dom_audit import measure_dom

def main(mode, out):
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True)
        try:
            page=browser.new_page()
            page.set_content("<style>.x{color:red}</style><div id='a'><span></span></div>")
            if mode=="hang":
                # Receipt establishes we reached actual Chromium JS, not a setup failure.
                (out/"entered-browser-js").write_text("hang fixture dispatched")
                page.evaluate("() => { while(true) {} }")
                return 3
            if mode=="dom":
                page.set_content("<style>.x{color:red}</style><div id='a'></div><div id='a'></div>")
                data=measure_dom(page,"fixture")
                (out/"fixture.json").write_text(json.dumps(data))
                return 0 if data["elements"]==2 and data["duplicateIds"]==[{"id":"a","count":2}] else 1
            if mode not in ("bounded","duplicate"):
                return 3
            # Independent expected invariant: one self-rescheduling chain,
            # canceled at the end. Deliberate duplicate executes two chains.
            data=page.evaluate("""async duplicate => {
              let hits=[0,0], handles=[];
              function start(i){const tick=()=>{hits[i]++;handles[i]=requestAnimationFrame(tick);};
                handles[i]=requestAnimationFrame(tick);}
              start(0);if(duplicate)start(1);
              await new Promise(resolve=>{let n=0;function frame(){if(++n>=5)resolve();else requestAnimationFrame(frame)}requestAnimationFrame(frame)});
              handles.forEach(id=>cancelAnimationFrame(id));
              const stopped=hits.slice();
              await new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)));
              let bounded=0;while(bounded<3)bounded++;
              return {hits,stopped,bounded,activeChains:stopped.filter(n=>n>0).length};
            }""",mode=="duplicate")
            (out/"fixture.json").write_text(json.dumps(data))
            return 0 if data["activeChains"]==1 and data["hits"]==data["stopped"] and data["bounded"]==3 else 1
        finally:
            browser.close()

if __name__=="__main__":
    sys.exit(main(sys.argv[1],Path(sys.argv[2])))
