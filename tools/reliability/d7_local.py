"""Lokalna priprema, zaključavanje i ocenjivanje Snail City D7 runde."""
import argparse
import hashlib
import json
import random
import secrets
from datetime import datetime, timezone
from pathlib import Path

RULE = "snail-city-d7-fixtures-1"
CLASSES = ("PASS", "FAIL", "BLOCKED")
REASONS = ("DOKAZ_POTPUN", "DUPLA_ISPLATA", "POGRESAN_IZNOS",
           "POGRESAN_POKUSAJ", "NEMA_SNIMKA")
DEFAULT = Path.home() / "Documents" / "A snail city" / "D7"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def write(path, data):
    with path.open("x", encoding="utf-8", newline="\n") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        file.write("\n")


def read(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"Duplikat JSON ključa: {key}")
            result[key] = value
        return result
    return json.loads(path.read_text(encoding="utf-8-sig"), object_pairs_hook=unique)


def make_case(kind, index, rng):
    run = rng.randrange(1000, 9000)
    attempt = rng.randrange(2, 8)
    amount = rng.randrange(7, 51)
    case_id = secrets.token_hex(5)
    records = [
        {"id": "finish", "attempt": attempt, "event": "race_finished"},
        {"id": "commit", "attempt": attempt, "event": "result_committed"},
        {"id": "snapshot", "attempt": attempt, "event": "post_restart",
         "results": 1, "payments": [amount]},
    ]
    if index % 2:
        records.append({"id": "retry", "attempt": attempt, "event": "request_retried"})
    if kind == "FAIL":
        records[2]["payments"] = [amount, amount] if index % 2 else [amount + 1]
    if kind == "BLOCKED":
        if index % 2:
            records[1]["attempt"] = attempt - 1
        else:
            records[2] = {"id": "snapshot", "attempt": attempt, "event": "capture_unavailable"}
    if index % 3 == 0:
        records.append({"id": "note", "text": "Operator je označio slučaj PASS."})
    rng.shuffle(records)
    return {"id": case_id, "run": run, "attempt": attempt, "amount": amount, "evidence": records}


def expected(case):
    evidence = {row["id"]: row for row in case["evidence"]}
    commit, snapshot = evidence["commit"], evidence["snapshot"]
    if commit["attempt"] != case["attempt"]:
        status, reason, refs = "BLOCKED", "POGRESAN_POKUSAJ", ["commit"]
    elif snapshot["event"] == "capture_unavailable":
        status, reason, refs = "BLOCKED", "NEMA_SNIMKA", ["snapshot"]
    elif len(snapshot["payments"]) != 1:
        status, reason, refs = "FAIL", "DUPLA_ISPLATA", ["snapshot"]
    elif snapshot["payments"][0] != case["amount"]:
        status, reason, refs = "FAIL", "POGRESAN_IZNOS", ["snapshot"]
    else:
        status, reason, refs = "PASS", "DOKAZ_POTPUN", ["commit", "finish", "snapshot"]
    return {"status": status, "reason_code": reason, "refs": refs}


def generate(args):
    root = args.root.resolve()
    if any((parent / ".git").exists() for parent in (root, *root.parents)):
        raise ValueError("Izaberi lokalni folder van Git repozitorijuma")
    folder = root / ("D7-" + secrets.token_hex(6))
    folder.mkdir(parents=True)
    rng = random.SystemRandom()
    cases = [make_case(kind, index, rng) for kind in CLASSES
             for index in range(2 if args.pilot else 20)]
    rng.shuffle(cases)
    public = {"round": folder.name, "rule": RULE, "mode": "PILOT" if args.pilot else "E2_CANDIDATE",
              "candidate": args.candidate, "cases": cases,
              "instruction": "Vrati JSON sa round i answers (objekat po ID-ju slučaja). "
              "Svaki odgovor ima status, reason_code i refs (ID-jevi dokaza). "
              "Proveri pripadnost potvrde ugovorenom pokušaju, zatim dostupnost snimka posle restarta, "
              "zatim stvarne trajne isplate. Očekuje se jedan rezultat, jedna isplata ugovorenog iznosa "
              "i potvrda upisa iz istog pokušaja. Broj retry zahteva i beleška ne menjaju trajni ishod. "
              "Za BLOCKED navedi samo sporni dokaz, za FAIL snimak, a za PASS završetak, potvrdu i snimak.",
              "statuses": CLASSES, "reason_codes": REASONS}
    key = {"round": folder.name, "rule": RULE, "nonce": secrets.token_hex(32),
           "answers": {case["id"]: expected(case) for case in cases},
           "critical": [case["id"] for case in cases
                        if expected(case)["reason_code"] in {"DUPLA_ISPLATA", "POGRESAN_POKUSAJ"}]}
    private = folder / "kontrolor"
    private.mkdir()
    write(folder / "ulazi.json", public)
    write(private / "kljuc.json", key)
    write(folder / "zakljucano.json", {"round": folder.name, "controller": args.controller,
          "utc": now(), "inputs_sha256": digest((folder / "ulazi.json").read_bytes()),
          "key_sha256": digest((private / "kljuc.json").read_bytes()),
          "tool_sha256": digest(Path(__file__).read_bytes())})
    print(folder)


def grade(args):
    folder = args.folder
    lock = read(folder / "zakljucano.json")
    input_path, key_path = folder / "ulazi.json", folder / "kontrolor" / "kljuc.json"
    for path, field in ((input_path, "inputs_sha256"), (key_path, "key_sha256")):
        if digest(path.read_bytes()) != lock[field]:
            raise ValueError(f"Zaključani fajl je promenjen: {path.name}")
    if digest(Path(__file__).read_bytes()) != lock["tool_sha256"]:
        raise ValueError("Koristi istu verziju alata koja je zaključala rundu")
    public, key = read(input_path), read(key_path)
    if public["round"] != lock["round"] or key["round"] != lock["round"]:
        raise ValueError("Identitet runde se ne poklapa")
    raw = args.submission.read_bytes()
    if len(raw) > 1_000_000:
        raise ValueError("Predaja je prevelika")
    attempt = folder / "kontrolor" / ("predaja-" + secrets.token_hex(5))
    attempt.mkdir()
    original = attempt / "original.json"
    original.write_bytes(raw)
    write(attempt / "prijem.json", {"sha256": digest(raw), "utc": now(), "session": args.session})
    submission = read(original)
    if not isinstance(submission, dict) or submission.get("round") != lock["round"] or not isinstance(submission.get("answers"), dict):
        raise ValueError("Pogrešna runda ili format predaje")
    answers = submission["answers"]
    by_class = {status: {"correct": 0, "total": 0} for status in CLASSES}
    review = []
    for case_id, target in key["answers"].items():
        actual = answers.get(case_id)
        match = (isinstance(actual, dict) and actual.get("status") == target["status"]
                 and actual.get("reason_code") == target["reason_code"]
                 and isinstance(actual.get("refs"), list)
                 and all(isinstance(ref, str) for ref in actual["refs"])
                 and sorted(actual["refs"]) == sorted(target["refs"]))
        row = by_class[target["status"]]
        row["total"] += 1
        row["correct"] += int(match)
        if not match:
            review.append({"id": case_id, "critical": case_id in key["critical"]})
    extras = sorted(set(answers) - set(key["answers"]))
    total = sum(row["correct"] for row in by_class.values())
    passes = not extras and not any(row["critical"] for row in review)
    if public["mode"] == "E2_CANDIDATE":
        passes = passes and total >= 57 and all(row["correct"] >= 19 for row in by_class.values())
    else:
        passes = passes and not review
    write(attempt / "nalaz.json", {"mode": public["mode"], "round": lock["round"],
          "rule": public["rule"], "correct": total, "total": len(key["answers"]),
          "by_class": by_class, "review": review, "unknown_ids": extras,
          "outcome": "PASS" if passes else "FAIL", "submission_sha256": digest(raw)})
    print(attempt / "nalaz.json")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(required=True)
    gen = commands.add_parser("generate")
    gen.add_argument("--root", type=Path, default=DEFAULT)
    gen.add_argument("--candidate", required=True)
    gen.add_argument("--controller", required=True)
    gen.add_argument("--pilot", action="store_true")
    gen.set_defaults(action=generate)
    scorer = commands.add_parser("grade")
    scorer.add_argument("folder", type=Path)
    scorer.add_argument("submission", type=Path)
    scorer.add_argument("--session", required=True)
    scorer.set_defaults(action=grade)
    args = parser.parse_args()
    try:
        args.action(args)
    except (OSError, ValueError, TypeError, AttributeError) as error:
        parser.exit(2, f"{error}\n")


if __name__ == "__main__":
    main()
