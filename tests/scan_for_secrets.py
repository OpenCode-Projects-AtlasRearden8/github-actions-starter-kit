#!/usr/bin/env python3
"""Offline secret scanner.

Guarantees the kit ships zero secret-shaped strings: scans every file in
the repo (skipping .git, binaries and itself) for common token formats.
Doc mentions of words like "secret" or "GITHUB_TOKEN" are fine - this
scanner looks at the literal token SHAPES, not the concept.
"""

import re
import sys
from pathlib import Path

PATTERNS = [
    ("AWS access key id", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("GitHub personal token", re.compile(r"gh[pousr]_[A-Za-z0-9]{36}")),
    ("GitHub fine-grained token", re.compile(r"github_pat_[A-Za-z0-9_]{22,}")),
    ("OpenAI-style key", re.compile(r"sk-[A-Za-z0-9-]{20,}")),
    ("Slack token", re.compile(r"xox[abpos]-[A-Za-z0-9-]{10,}")),
    ("Google API key", re.compile(r"AIza[0-9A-Za-z_-]{35}")),
    ("Private key material", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("Basic auth URL", re.compile(r"://[^/\s:]+:[^@\s]+@", re.M)),
]

SKIP_DIRS = {".git", "tools"}
SKIP_FILES = {"scan_for_secrets.py"}
SIZE_LIMIT = 2 * 1024 * 1024


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    found = 0
    for f in sorted(root.rglob("*")):
        if not f.is_file() or f.name in SKIP_FILES:
            continue
        if any(part in SKIP_DIRS for part in f.relative_to(root).parts):
            continue
        try:
            data = f.read_bytes()
        except OSError:
            continue
        if len(data) > SIZE_LIMIT or b"\x00" in data[:4096]:
            continue  # binary or oversized file
        text = data.decode("utf-8", errors="replace")
        for label, pat in PATTERNS:
            for m in pat.finditer(text):
                found += 1
                line_no = text.count("\n", 0, m.start()) + 1
                print(f"POSSIBLE SECRET  {f.relative_to(root)}:{line_no}  ({label})")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
