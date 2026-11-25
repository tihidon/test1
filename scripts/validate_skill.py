import shutil
import subprocess
import sys
from pathlib import Path

def main():
    root = Path(__file__).resolve().parent.parent
    cli = shutil.which("skills-ref")
    if not cli:
        print("BLOCKED: skills-ref not on PATH")
        return 2
    for cmd in ("validate", "read-properties", "to-prompt"):
        try:
            r = subprocess.run([cli, cmd, str(root)], timeout=60, check=False)
        except (OSError, subprocess.TimeoutExpired) as exc:
            print(f"BLOCKED: {exc}")
            return 2
        if r.returncode:
            return r.returncode
    print("PASS official CLI format only, not agent/runtime QA")
    return 0

if __name__ == "__main__":
    sys.exit(main())
