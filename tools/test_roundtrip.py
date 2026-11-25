#!/usr/bin/env python3
"""Gate: split -> build must reproduce reference/index-p3-main.html byte-for-byte,
and every executable block must parse (node --check). Run: python3 tools/test_roundtrip.py"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "reference" / "index-p3-main.html"
EXPECTED_SHA = "594026b9ffab62ceb8dbbfa181c887edea3f903ff84a27151a2330fb978dc58a"


def main() -> int:
    failures: list[str] = []
    if hashlib.sha256(REF.read_bytes()).hexdigest() != EXPECTED_SHA:
        failures.append("reference hash changed")
    subprocess.run([sys.executable, str(ROOT / "tools/split.py")], check=True, cwd=ROOT)
    out = subprocess.run([sys.executable, str(ROOT / "tools/build.py")], check=True, cwd=ROOT,
                         capture_output=True, text=True)
    if (ROOT / "dist/index.html").read_bytes() != REF.read_bytes():
        failures.append("round-trip is NOT byte-identical")
    for b in json.loads((ROOT / "src/html/blocks.json").read_text(encoding="utf-8")):
        if b["file"].startswith("src/js/"):
            r = subprocess.run(["node", "--check", str(ROOT / b["file"])], capture_output=True, text=True)
            if r.returncode != 0:
                failures.append(f"syntax: {b['file']}: {r.stderr.strip()[:200]}")
    for f in failures:
        print("FAIL", f)
    if not failures:
        print("PASS round-trip byte-identical; JS syntax OK;", out.stdout.strip())
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
