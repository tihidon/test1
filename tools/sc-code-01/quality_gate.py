"""Use canonical SC-CODE-01 metrics; add location and current-base evidence."""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tinycss2
from sc_code_metrics import _Extractor, RATCHET, css_metrics, js_metrics

ROOT = Path(__file__).resolve().parents[2]
HISTORICAL = Path(__file__).with_name("baseline-0.8.92-css-unified-p1.json")

def parse(raw):
    p = _Extractor()
    p.feed(raw.decode("utf-8"))
    p.close()
    if not p.out["css"] or not p.out["js"]:
        raise ValueError("zero CSS or executable JS blocks")
    return p.out

def locations(blocks):
    selectors = defaultdict(list)
    values = []
    rulesizes = []
    errors = []
    unhandled = set()
    def walk(rules, ctx, block):
        for r in rules:
            if r.type == "error":
                errors.append({"block":block,"line":r.source_line,"message":r.message})
            elif r.type == "qualified-rule":
                parts, current = [], []
                for token in r.prelude:
                    if token.type == "literal" and token.value == ",":
                        parts.append(tinycss2.serialize(current).strip())
                        current = []
                    else:
                        current.append(token)
                parts.append(tinycss2.serialize(current).strip())
                at = {"block":block,"line":r.source_line,"column":r.source_column}
                decls = tinycss2.parse_declaration_list(r.content, skip_comments=True, skip_whitespace=True)
                rulesizes.append({**at,"context":ctx,"selector":",".join(parts)[:200],
                                  "declarations":sum(d.type=="declaration" for d in decls)})
                for sel in parts:
                    selectors[(ctx,sel)].append(at)
                for d in decls:
                    if d.type == "error":
                        errors.append({"block":block,"line":d.source_line,"message":d.message})
                    elif d.type == "declaration":
                        n = len(tinycss2.serialize(d.value))
                        if n > 4096:
                            values.append({"block":block,"line":d.source_line,"property":d.name,
                                           "characters":n,"custom_property":d.name.startswith("--")})
            elif r.type == "at-rule" and r.content is not None:
                k = r.lower_at_keyword
                if k in ("media","supports","container","layer","scope","starting-style"):
                    walk(tinycss2.parse_rule_list(r.content,skip_comments=True,skip_whitespace=True),
                         ctx+" @"+k+" "+tinycss2.serialize(r.prelude).strip(),block)
                else:
                    unhandled.add(k)
    for i,b in enumerate(blocks,1):
        walk(tinycss2.parse_stylesheet(b,skip_comments=True,skip_whitespace=True),"",i)
    return {"duplicate_exact_selectors":[{"context":ctx,"selector":sel[:200],"locations":at}
            for (ctx,sel),at in selectors.items() if len(at)>1],
            "large_values":sorted(values,key=lambda x:-x["characters"]),
            "largest_rules":sorted(rulesizes,key=lambda x:-x["declarations"])[:20],
            "parse_errors":errors,"uninspected_at_rules":sorted(unhandled),
            "limitation":"Location diagnostics, not cascade equivalence; comments, fallback declarations, nesting and other at-rules need review."}

def measure(raw):
    p = parse(raw)
    return {"html_sha256":hashlib.sha256(raw).hexdigest(),"css":css_metrics(p["css"],p["links"]),
            "js":js_metrics(p["js"]),"css_locations":locations(p["css"])}

def increases(before, after):
    return [{"metric":s+"."+k,"before":before[s][k],"after":after[s][k]}
            for s,k in RATCHET if after[s][k]>before[s][k]]

def verdict(before, after, historical):
    growth=increases(before,after)
    history=increases(historical,after)
    # Existing debt never silently disappears; on runtime edits retain the historical gate.
    changed=before["html_sha256"]!=after["html_sha256"]
    errors=after["css_locations"]["parse_errors"]
    old_errors=before["css_locations"]["parse_errors"]
    parse_growth=len(errors)>len(old_errors)
    blocked=bool(growth or parse_growth or (changed and history))
    return {"status":"FAIL" if blocked else "PASS_NO_GROWTH",
            "historical_status":"FAIL" if history else "PASS",
            "historical_increases":history,"increases":growth,
            "css_parse_error_growth":parse_growth,"runtime_html_changed":changed,
            "limitation":"No-growth is not full SC-CODE compliance, visual QA, or performance proof."}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--base",required=True,help="reviewed baseline commit SHA")
    ap.add_argument("--out",type=Path,required=True)
    args=ap.parse_args()
    try:
        if len(args.base)!=40 or any(c not in "0123456789abcdef" for c in args.base):
            raise ValueError("expected full baseline commit SHA")
        raw=subprocess.check_output(["git","show",args.base+":index.html"],cwd=ROOT,timeout=45)
        before=measure(raw)
        after=measure((ROOT/"index.html").read_bytes())
        result=verdict(before,after,json.loads(HISTORICAL.read_text(encoding="utf-8")))
        report={"base_commit":args.base,"base":before,"candidate":after,**result}
        args.out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
        print(json.dumps(result,ensure_ascii=False))
        return int(result["status"]=="FAIL")
    except (OSError,ValueError,KeyError,subprocess.SubprocessError) as e:
        print("FAIL/BLOCKED: "+str(e),file=sys.stderr)
        return 2

if __name__=="__main__":
    sys.exit(main())
