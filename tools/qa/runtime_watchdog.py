"""Out-of-process wall-clock watchdog for trusted local QA (POSIX only)."""
import argparse
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
from functional_contract import accepted_cases

ROOT = Path(__file__).resolve().parents[2]


def run_bounded(command, out, timeout):
    started = time.monotonic()
    result = {"status": "BLOCKED", "reason": "POSIX process groups required"}
    if os.name == "posix":
        with (out / "worker.log").open("wb") as log:
            proc = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT,
                                    start_new_session=True)
            try:
                code = proc.wait(timeout=timeout)
                result = {"status": "PASS" if code == 0 else ("BLOCKED" if code == 2 else "FAIL"),
                          "exit_code": code}
            except subprocess.TimeoutExpired:
                result = {"status": "FAIL", "reason": "external watchdog deadline",
                          "exit_code": 124}
                try:
                    os.killpg(proc.pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass
                try:
                    proc.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    pass
            finally:
                # Also remove descendants if the worker exited before its browser.
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                proc.wait(timeout=5)
    result["elapsed_s"] = round(time.monotonic()-started, 3)
    (out / "watchdog.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--root", type=Path, default=ROOT)
    p.add_argument("--scenario", type=Path)
    mode=p.add_mutually_exclusive_group()
    mode.add_argument("--diagnostic", action="store_true")
    mode.add_argument("--functional", action="store_true")
    p.add_argument("--timeout", type=int, default=120)
    a = p.parse_args()
    if a.functional and a.scenario:
        p.error('functional suite uses its own reviewed contract')
    root, out = a.root.resolve(), a.out.resolve()
    if out.is_relative_to(root) or not 5 <= a.timeout <= 600:
        p.error("new output outside checkout; timeout 5–600 seconds")
    out.mkdir(parents=True, exist_ok=False)
    command = [sys.executable, str(Path(__file__).with_name("runtime_smoke.py")),
               "--root", str(root), "--out", str(out)]
    if a.scenario:
        command += ["--scenario", str(a.scenario.resolve())]
    if a.diagnostic:
        command.append("--diagnostic")
    if a.functional:
        command.append("--functional")
    result = run_bounded(command, out, a.timeout)
    if result["status"] == "PASS":
        try:
            report = json.loads((out / "report.json").read_text(encoding="utf-8"))
            required = ("diagnostic.json", "online.png", "offline.png") if a.diagnostic else ("trace.zip", "cpu-profile.json", "online.png", "offline.png")
            if a.functional:
                required=("functional-online-trace.zip","functional-offline-trace.zip","functional-race-trace.zip",
                          "functional-purchase.png","functional-offline.png","functional-race.png")
                if not accepted_cases(report):
                    raise ValueError("missing or nonpassing functional cases")
            if bool(report.get("functional_mode")) != a.functional:
                raise ValueError("functional mode mismatch")
            if bool(report.get("diagnostic_mode")) != a.diagnostic:
                raise ValueError("diagnostic mode mismatch")
            if report["status"] != "PASS" or not all((out/f).stat().st_size > 0 for f in required):
                raise ValueError("missing required evidence")
        except (OSError, ValueError, KeyError) as exc:
            result.update(status="FAIL", reason=str(exc))
            (out/"watchdog.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result))
    return {"PASS":0,"FAIL":1,"BLOCKED":2}[result["status"]]


if __name__ == "__main__":
    sys.exit(main())
