import argparse
import shutil
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent / "project-tools" / "tools"

def main():
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--repo", type=Path)
    g.add_argument("--fixtures", action="store_true")
    args = p.parse_args()
    node = shutil.which("node")
    if not node:
        print("BLOCKED: Node.js unavailable")
        return 2
    if args.fixtures:
        cwd = TOOLS.parent
        tasks = [[sys.executable, "-m", "unittest", "discover", "-s", str(TOOLS/"agent"), "-p", "test_*.py", "-v"], [node, "--test", str(TOOLS/"agent/test_audit_loops.cjs")]]
    else:
        cwd = args.repo.resolve()
        if not (cwd/"src/html/blocks.json").is_file() or not (cwd/"tools/build.py").is_file():
            print("BLOCKED: incompatible checkout")
            return 2
        tasks = [[sys.executable, str(TOOLS/"agent/check_build.py"), "--root", str(cwd), "--require-publish-match"], [node, str(TOOLS/"agent/audit_loops.cjs"), str(cwd)]]
    for task in tasks:
        print("RUN", task, flush=True)
        try:
            r = subprocess.run(task, cwd=cwd, timeout=240, check=False)
        except (OSError, subprocess.TimeoutExpired) as exc:
            print(f"BLOCKED: {exc}")
            return 2
        if r.returncode:
            return r.returncode
    print("Scoped gates completed; AST candidates require review, not runtime QA.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
