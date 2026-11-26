"""Actual MCP stdio + Chrome smoke; synthetic loopback only, Linux."""
import http.server
import json
import os
from pathlib import Path
import queue
import re
import signal
import subprocess
import sys
import threading
import time
import tomllib

ROOT = Path(__file__).resolve().parents[2]
MARKER = "SC-MCP-FIXTURE-41"
REQUIRED = {"list_pages", "new_page", "evaluate_script", "take_snapshot",
            "performance_start_trace", "performance_stop_trace", "set_logpoints",
            "take_heapsnapshot", "compare_heapsnapshots"}

class Fixture(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"<!doctype html><title>SC MCP fixture</title><main id='probe'>SC-MCP-FIXTURE-41</main>"
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

def require(condition, reason):
    if not condition:
        raise RuntimeError(reason)

def fixture_page_id(pages, url):
    # v1.14.0 McpResponse.formatPage: title (url), or bare url without title.
    # Match an entire page label; never guess the selected tab or accept a prefix.
    page_text = "\n".join(c.get("text", "") for c in pages.get("content", []))
    suffix = r"(?: \[selected\])?\s*$"
    label = r"(?:" + re.escape(url) + r"|[^\r\n]+ \(" + re.escape(url) + r"\))"
    ids = re.findall(r"(?m)^[ \t]*(\d+):[ \t]*" + label + suffix, page_text)
    require(len(ids) == 1, "fixture page ID not uniquely listed")
    return int(ids[0])

def main(out):
    out.mkdir(parents=True, exist_ok=False)
    config = tomllib.loads((ROOT / "tools/agent/chrome-devtools-mcp.toml").read_text())["mcp_servers"]["chrome-devtools"]
    report = {"status": "NOT RUN", "scope": "synthetic tool smoke, not game",
              "commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
              "command": [config["command"], *config["args"]], "checks": []}
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Fixture)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{server.server_port}/"
    proc = None
    try:
        with (out / "stderr.log").open("w") as stderr, (out / "rpc.jsonl").open("w") as raw:
            proc = subprocess.Popen(report["command"], stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, stderr=stderr, text=True, encoding="utf-8",
                env={**os.environ, **config["env"]}, start_new_session=True)
            messages = queue.Queue()
            def reader():
                for line in proc.stdout:
                    messages.put(line)
                messages.put(None)
            threading.Thread(target=reader, daemon=True).start()
            counter = 0
            def send(method, params=None, notification=False):
                nonlocal counter
                counter += 1
                req = {"jsonrpc": "2.0", "method": method}
                if params is not None:
                    req["params"] = params
                if not notification:
                    req["id"] = counter
                raw.write(json.dumps({"send": req}) + "\n"); raw.flush()
                proc.stdin.write(json.dumps(req) + "\n"); proc.stdin.flush()
                if notification:
                    return None
                deadline = time.monotonic() + 90
                while True:
                    remaining = deadline - time.monotonic()
                    require(remaining > 0, "MCP response deadline: " + method)
                    try:
                        line = messages.get(timeout=remaining)
                    except queue.Empty:
                        raise RuntimeError("MCP response deadline: " + method)
                    require(line is not None, "MCP stdout closed: " + method)
                    raw.write(line); raw.flush()
                    msg = json.loads(line)
                    if msg.get("id") != counter:
                        continue
                    require("error" not in msg, str(msg.get("error")))
                    result = msg["result"]
                    require(not result.get("isError"), str(result))
                    return result
            info = send("initialize", {"protocolVersion": "2025-11-25",
                "capabilities": {}, "clientInfo": {"name": "snail-city-smoke", "version": "1"}})
            report["serverInfo"] = info["serverInfo"]
            require(info["protocolVersion"] in ("2025-11-25", "2025-06-18", "2025-03-26", "2024-11-05"), "unsupported protocol")
            report["checks"].append("initialize")
            send("notifications/initialized", notification=True)
            names = set()
            cursor = None
            seen = set()
            while True:
                result = send("tools/list", {"cursor": cursor} if cursor else {})
                names.update(t["name"] for t in result["tools"])
                cursor = result.get("nextCursor")
                if not cursor:
                    break
                require(cursor not in seen, "tool pagination loop")
                seen.add(cursor)
            report["tools"] = sorted(names)
            require(REQUIRED <= names, "required tools missing: " + str(sorted(REQUIRED - names)))
            report["checks"].append("tool discovery")
            send("tools/call", {"name": "new_page", "arguments": {"url": url}})
            pages = send("tools/call", {"name": "list_pages", "arguments": {}})
            page_id = fixture_page_id(pages, url)
            result = send("tools/call", {"name": "evaluate_script", "arguments": {
                "pageId": page_id, "function": "() => document.querySelector('#probe').textContent"}})
            require(any(MARKER in c.get("text", "") for c in result.get("content", [])), "fixture DOM oracle failed")
            report["checks"].append("real Chrome DOM read")
            report["status"] = "PASS"
    except Exception as exc:
        report.update(status="FAIL", reason=str(exc))
        raise
    finally:
        if proc is not None:
            try:
                proc.stdin.close()
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid, signal.SIGTERM)
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(proc.pid, signal.SIGKILL)
                    proc.wait()
        server.shutdown()
        server.server_close()
        (out / "report.json").write_text(json.dumps(report, indent=2) + "\n")
        print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main(Path(sys.argv[1]))
