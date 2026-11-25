"""Main page CDP diagnostics only; no performance claims."""
class Diagnostic:
    def __init__(self, cdp):
        self.cdp=cdp
        self.scripts={}
        self.styles={}
        self.phases=[]
        self.active=False

    def start(self):
        c=self.cdp
        c.on("Debugger.scriptParsed",lambda e:self.scripts.update({e["scriptId"]:{
            k:e.get(k) for k in ("url","startLine","startColumn","endLine","endColumn","hash")}}))
        c.on("CSS.styleSheetAdded",lambda e:self.styles.update({e["header"]["styleSheetId"]:{
            k:e["header"].get(k) for k in ("sourceURL","startLine","startColumn","endLine","endColumn","length","isInline")}}))
        c.send("Debugger.enable")
        c.send("DOM.enable")
        c.send("CSS.enable")
        c.send("Profiler.enable")
        c.send("Profiler.startPreciseCoverage",{"callCount":True,"detailed":True})
        try:
            c.send("CSS.startRuleUsageTracking")
        except Exception:
            c.send("Profiler.stopPreciseCoverage")
            raise
        self.active=True

    def capture(self,label):
        if not self.active:
            raise RuntimeError("diagnostic not started")
        js=self.cdp.send("Profiler.takePreciseCoverage")
        css=self.cdp.send("CSS.takeCoverageDelta")
        phase={"label":label,"js_timestamp":js["timestamp"],"js":js["result"],
               "css_timestamp":css["timestamp"],"css":css["coverage"]}
        self.phases.append(phase)
        return phase

    def stop(self):
        if self.active:
            try:
                self.cdp.send("CSS.stopRuleUsageTracking")
            finally:
                self.cdp.send("Profiler.stopPreciseCoverage")
                self.active=False

    def report(self):
        return {"scope":"main page CDP target; no SW/worker/GPU coverage","timing_comparable":False,
                "scripts":self.scripts,"stylesheets":self.styles,"phases":self.phases,
                "limitations":"JS counts reset per capture. CSS deltas are newly observed rules, not dead code or exhaustive per-phase coverage. IDs session local; offsets need source identity."}

def has_observations(phase,url):
    return any(s.get("url")==url and any(f.get("ranges") and f["ranges"][0]["count"]>0
        for f in s["functions"]) for s in phase["js"]) and any(r["used"] for r in phase["css"])
