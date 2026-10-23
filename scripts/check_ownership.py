"""Fail if PR touches files outside the author's ownership paths."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, cwd=ROOT, text=True).strip()


def changed_files(base: str, head: str) -> list[str]:
    if not base or base == "0" * 40:
        out = run(["git", "ls-tree", "-r", "--name-only", head or "HEAD"])
        return [l for l in out.splitlines() if l]
    out = run(["git", "diff", "--name-only", f"{base}...{head}"])
    return [l for l in out.splitlines() if l]


def path_owned(path: str, patterns: list[str]) -> bool:
    path = path.replace("\\", "/")
    for p in patterns:
        p = p.replace("\\", "/")
        if p.endswith("/"):
            if path.startswith(p) or path == p.rstrip("/"):
                return True
        elif path == p or path.startswith(p.rstrip("/") + "/"):
            return True
    return False


def main() -> int:
    data = json.loads((ROOT / ".github" / "ownership.json").read_text(encoding="utf-8"))
    author = (os.environ.get("PR_AUTHOR") or "").lower()
    coordinators = {c.lower() for c in data.get("coordinators", [])}
    if author in coordinators:
        print(f"coordinator {author}: ownership skipped")
        return 0

    owners = data["owners"]
    my_paths: list[str] = []
    for _key, meta in owners.items():
        if meta.get("github", "").lower() == author:
            my_paths.extend(meta.get("paths", []))
    shared = data.get("shared_readonly", [])

    if not my_paths:
        print(f"unknown author {author}; denying file changes", file=sys.stderr)
        return 1

    base = os.environ.get("BASE_SHA", "")
    head = os.environ.get("HEAD_SHA", "HEAD")
    files = changed_files(base, head)
    if not files:
        print("no changed files")
        return 0

    bad: list[str] = []
    for f in files:
        if path_owned(f, shared):
            # shared files: only coordinator should change; non-coord fail
            bad.append(f)
            continue
        if not path_owned(f, my_paths):
            bad.append(f)

    if bad:
        print("ownership violations:", file=sys.stderr)
        for f in bad:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print(f"ownership ok for {author} ({len(files)} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
