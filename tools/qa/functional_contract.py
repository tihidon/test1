"""Reviewed functional expectations for p10. Not imported by production."""
import hashlib
import json

CASE_IDS=("B01","B02","B03","B05","B04","B06")
EGG_KIND=0
EGG_PRICE=100
REPEATS=20
PROFILE_NAME="SC-QA-B03"

def require(ok,message):
    if not ok:
        raise AssertionError(message)

def digest(value):
    return hashlib.sha256(str(value).encode("utf-8")).hexdigest()

def egg_kinds(eggs):
    pairs=[]
    for egg in eggs:
        require(isinstance(egg,dict) and "id" in egg and type(egg.get("kind")) is int,
                "invalid committed egg kind or identity")
        pairs.append([digest(egg["id"]),egg["kind"]])
    require(len({pair[0] for pair in pairs})==len(pairs),"duplicate committed egg identity")
    return sorted(pairs)

def snapshot(s):
    require(isinstance(s,dict) and isinstance(s.get("saveId"),str) and type(s.get("revision")) is int,
            "invalid committed snapshot identity")
    require(type(s.get("level")) is int and isinstance(s.get("eggs"),list) and isinstance(s.get("snails"),list),
            "invalid committed snapshot structure")
    return {"save_id_sha256":digest(s["saveId"]),"revision":s["revision"],
        "level":s["level"],"sliz":s["sliz"],"diamonds":s["diamonds"],"tokens":s["tokens"],
        "egg_ids":sorted(digest(e["id"]) for e in s["eggs"]),
        "egg_kinds":egg_kinds(s["eggs"]),
        "snail_ids":sorted(digest(n["id"]) for n in s["snails"]),
        "profile_name":s.get("playerName",""),"built":sorted(s["built"])}

def unchanged_inventory(before,after):
    a,b=snapshot(before),snapshot(after)
    for key in ("save_id_sha256","sliz","diamonds","tokens","egg_ids","egg_kinds","snail_ids","level","built","profile_name"):
        require(a[key]==b[key],"unexpected mutation: "+key)
    require(b["revision"]>=a["revision"],"revision went backwards")

def purchase(before,after):
    a,b=snapshot(before),snapshot(after)
    require(a["save_id_sha256"]==b["save_id_sha256"],"purchase changed save identity")
    require(b["revision"]>a["revision"],"purchase not committed")
    require(b["sliz"]==a["sliz"]-EGG_PRICE,"wrong debit for one standard egg")
    require(b["diamonds"]==a["diamonds"] and b["tokens"]==a["tokens"],"unexpected currency change")
    old={e["id"] for e in before["eggs"]}
    new=[e for e in after["eggs"] if e["id"] not in old]
    require(len(new)==1 and len(after["eggs"])==len(before["eggs"])+1 and
            old.issubset({e["id"] for e in after["eggs"]}) and new[0]["kind"]==EGG_KIND,
            "wrong egg addition or existing egg lost")
    current=dict(b["egg_kinds"])
    require(all(current.get(egg_id)==kind for egg_id,kind in a["egg_kinds"]),
            "existing egg kind changed")
    require(a["snail_ids"]==b["snail_ids"] and a["level"]==b["level"],"unexpected level/snail change")
    require(a["profile_name"]==b["profile_name"] and a["built"]==b["built"],
            "unexpected profile/building change")

def durable(before,after):
    unchanged_inventory(before,after)
    require(len(after["eggs"])>0,"empty egg inventory")

def accepted_cases(report):
    cases=report.get("functional_cases",{})
    return (isinstance(cases,dict) and set(cases)==set(CASE_IDS) and
            all(isinstance(cases[k],dict) and cases[k].get("status")=="PASS" and
                type(cases[k].get("assertions")) is int and cases[k]["assertions"]>0 for k in CASE_IDS))
