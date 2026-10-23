"""Plan PRs must not mix code; section 3/4 only k1/coordinator."""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, cwd=ROOT, text=True).strip()


def main() -> int:
    base = os.environ.get("BASE_SHA", "")
    head = os.environ.get("HEAD_SHA", "HEAD")
    author = (os.environ.get("PR_AUTHOR") or "").lower()
    if not base or base == "0" * 40:
        return 0
    files = [l for l in run(["git", "diff", "--name-only", f"{base}...{head}"]).splitlines() if l]
    plan_touched = any(f == "docs/PLAN.md" or f.startswith("docs/plan-degisiklikleri/") for f in files)
    if not plan_touched:
        return 0

    codeish = [
        f
        for f in files
        if not (
            f.startswith("docs/")
            or f in {"AGENTS.md", "README.md", "CLAUDE.md", "GEMINI.md"}
        )
    ]
    if codeish:
        print("Plan PR must not include code files:", file=sys.stderr)
        for f in codeish:
            print(f"  - {f}", file=sys.stderr)
        return 1

    notes = [f for f in files if f.startswith("docs/plan-degisiklikleri/") and f.endswith(".md")]
    notes = [f for f in notes if not f.endswith("_SABLON.md")]
    if "docs/PLAN.md" in files and not notes:
        print("PLAN.md change requires a plan-degisiklikleri note", file=sys.stderr)
        return 1

    if "docs/PLAN.md" in files and author not in {"beyza24"}:
        diff = run(["git", "diff", f"{base}...{head}", "--", "docs/PLAN.md"])
        # crude: heading lines for section 3 or 4
        if re.search(r"^\+## 3\.|\+## 4\.", diff, re.M):
            print("Only k1/coordinator may change PLAN sections 3 and 4", file=sys.stderr)
            return 1
    print("plan checks ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
