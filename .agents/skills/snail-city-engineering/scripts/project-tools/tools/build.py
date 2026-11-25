#!/usr/bin/env python3
"""Re-inline src/ blocks into index.html. Output must match the original bytes."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "src" / "html" / "index.template.html"
MANIFEST = ROOT / "src" / "html" / "blocks.json"
OUT = ROOT / "dist" / "index.html"


def build() -> bytes:
    text = TEMPLATE.read_text(encoding="utf-8")
    for b in json.loads(MANIFEST.read_text(encoding="utf-8")):
        body = (ROOT / b["file"]).read_bytes().decode("utf-8")
        marker = f"<!--SC-INLINE {b['id']}-->"
        if text.count(marker) != 1:
            raise SystemExit(f"marker {marker} must occur exactly once")
        text = text.replace(marker, b["open_tag"] + body + b["close_tag"], 1)
    return text.encode("utf-8")


if __name__ == "__main__":
    data = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(data)
    print(f"built {OUT.relative_to(ROOT)} {len(data)} B")
    sys.exit(0)
