#!/usr/bin/env python3
"""Split the single-file 0.8.92 build into editable source files.

Lossless by construction: every <script>/<style> body is written verbatim to
src/, and src/html/index.template.html keeps a placeholder where the block was.
tools/build.py re-inlines them; the round-trip must reproduce the original bytes.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ORIG = ROOT / "reference" / "index-p3-main.html"
TEMPLATE = ROOT / "src" / "html" / "index.template.html"
MANIFEST = ROOT / "src" / "html" / "blocks.json"

RAW_B64_RE = re.compile(r"[A-Za-z0-9+/=\\s]+")
BLOCK_RE = re.compile(r"<(script|style)\b([^>]*)>(.*?)</\1>", re.S | re.I)


def classify(tag: str, attrs: str, body: str) -> tuple[str, str]:
    """Return (directory, extension) for a block."""
    if tag.lower() == "style":
        return "css", "css"
    t = re.search(r'type\s*=\s*"([^"]+)"', attrs, re.I)
    kind = t.group(1).lower() if t else "text/javascript"
    if RAW_B64_RE.fullmatch(body.strip()):
        # Raw base64 payload (e.g. a WebP sprite), whatever the script type says.
        return "data", "b64"
    if "json" in kind:
        return "data", "json"
    if "text/plain" in kind:
        return "data", "txt"
    return "js", "js"


def main() -> int:
    text = ORIG.read_bytes().decode("utf-8")
    blocks = []
    pieces: list[str] = []
    last = 0
    for i, m in enumerate(BLOCK_RE.finditer(text)):
        tag, attrs, body = m.group(1), m.group(2), m.group(3)
        d, ext = classify(tag, attrs, body)
        block_id = f"{i:02d}"
        rel = f"src/{d}/block-{block_id}.{ext}"
        out = ROOT / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(body.encode("utf-8"))
        open_tag = m.group(0)[: m.group(0).index(">", 0) + 1]
        close_tag = f"</{tag}>"
        blocks.append({
            "id": block_id,
            "element": tag.lower(),
            "open_tag": open_tag,
            "close_tag": close_tag,
            "file": rel,
            "sha256": __import__("hashlib").sha256(body.encode("utf-8")).hexdigest(),
        })
        pieces.append(text[last:m.start()])
        pieces.append(f"<!--SC-INLINE {block_id}-->")
        last = m.end()
    pieces.append(text[last:])
    TEMPLATE.write_text("".join(pieces), encoding="utf-8", newline="")
    MANIFEST.write_text(json.dumps(blocks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"blocks: {len(blocks)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
