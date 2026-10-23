"""Block .env, huge files, and obvious secret patterns."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_BYTES = 5 * 1024 * 1024
SECRET_RE = re.compile(
    r"(?i)(api[_-]?key\s*=\s*['\"]?[A-Za-z0-9_\-]{20,}|sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,})"
)
SKIP_DIRS = {".git", ".venv", "node_modules", "__pycache__"}


def main() -> int:
    bad = False
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel == ".env" or rel.endswith("/.env"):
            print(f"forbidden file: {rel}", file=sys.stderr)
            bad = True
            continue
        size = path.stat().st_size
        if size > MAX_BYTES:
            print(f"file too large ({size} bytes): {rel}", file=sys.stderr)
            bad = True
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf", ".pptx"}:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if SECRET_RE.search(text):
            print(f"possible secret in: {rel}", file=sys.stderr)
            bad = True
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
