#!/usr/bin/env python3
"""Historical P3 round-trip, isolated; never writes active src/."""
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "reference/index-p3-main.html"
EXPECTED_SHA = "594026b9ffab62ceb8dbbfa181c887edea3f903ff84a27151a2330fb978dc58a"


def main():
    data = REF.read_bytes()
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA:
        print("FAIL historical reference hash")
        return 1
    if not shutil.which("node"):
        print("BLOCKED Node.js unavailable")
        return 2
    try:
        with tempfile.TemporaryDirectory(prefix="sc-historical-") as tmp:
            work = Path(tmp)
            for d in ("reference", "tools", "src/html"):
                (work / d).mkdir(parents=True)
            (work / "reference/index-p3-main.html").write_bytes(data)
            for name in ("split.py", "build.py"):
                shutil.copy2(ROOT / "tools" / name, work / "tools" / name)
                subprocess.run([sys.executable, str(work / "tools" / name)],
                               check=True, cwd=work, timeout=90)
            if (work / "dist/index.html").read_bytes() != data:
                print("FAIL historical round-trip")
                return 1
            blocks = json.loads((work / "src/html/blocks.json").read_text(encoding="utf-8"))
            scripts = [b["file"] for b in blocks if b["file"].startswith("src/js/")]
            if not scripts:
                print("FAIL zero JS files")
                return 1
            for rel in scripts:
                subprocess.run(["node", "--check", str(work / rel)], cwd=work, check=True, timeout=30)
        print("PASS historical P3 round-trip only; active src untouched")
        return 0
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
