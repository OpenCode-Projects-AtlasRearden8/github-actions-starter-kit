#!/usr/bin/env python3
"""Offline structural validator for workflow YAML fixtures.

Fallback path when actionlint isn't installed: does a structural review of
each fixture - parses YAML, checks it shapes like a GitHub Actions workflow,
and rejects obvious mistakes (empty jobs, unpinned uses, secrets keys,
missing top-level keys).

This is deliberately simple and dependency-light: PyYAML when available,
otherwise plain-text checks that still catch the common beginner errors.
"""

import re
import sys
from pathlib import Path

try:
    import yaml  # PyYAML, usually present via system packages
    HAVE_YAML = True
except ImportError:
    HAVE_YAML = False

REQUIRED_TOP_KEYS = {"on", "jobs"}
FORBIDDEN_CONTEXTS = [
    "secrets.",
    "secrets[",
    "${{ secrets",
]
TOKEN_RE = re.compile(
    r"(ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{10,}|AKIA[0-9A-Z]{12,})"
)


def structural_errors(path: Path) -> list:
    errors, warnings = [], []

    if HAVE_YAML:
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as e:
            return [f"yaml parse error: {e}"]
        if not isinstance(data, dict):
            return ["top level of file is not a mapping"]

        # YAML 1.1 quirk: PyYAML parses a bare "on:" key as the boolean
        # True (like on/off/yes/no). Shift it back so we can check "on".
        if True in data:
            data["on"] = data.pop(True)

        missing = REQUIRED_TOP_KEYS - set(data)
        if missing:
            errors.append(f"top-level keys missing: {sorted(missing)}")

        name = data.get("name")
        if not (isinstance(name, str) and name.strip()):
            errors.append("no human-readable name: at top level")

        jobs = data.get("jobs")
        if not (isinstance(jobs, dict) and jobs):
            errors.append('"jobs" must be a non-empty mapping')
        else:
            for job_id, job in jobs.items():
                if not isinstance(job, dict) or not job.get("steps"):
                    errors.append(f'job "{job_id}" has no steps')
                if not isinstance(job, dict) or not job.get("runs-on"):
                    errors.append(f'job "{job_id}" has no runs-on')

        # Recursively find any secrets context or token-looking literal.
        def walk(node):
            if isinstance(node, dict):
                for v in node.values():
                    walk(v)
            elif isinstance(node, list):
                for v in node:
                    walk(v)
            elif isinstance(node, str):
                for frag in FORBIDDEN_CONTEXTS:
                    if frag in node:
                        errors.append(f"found {frag!r}, kit workflows need no secrets")
                if TOKEN_RE.search(node):
                    errors.append("found a token-shaped literal")

        walk(data)
    else:
        # No PyYAML: plain-text checks that still catch classic mistakes.
        text = path.read_text(encoding="utf-8")
        if "jobs:" not in text:
            errors.append("no jobs: section found")
        if "runs-on:" not in text:
            errors.append("no runs-on: found in any job")
        if "${{ secrets" in text or re.search(r"^\s*\w+[:=]\s*secrets\.", text, re.M):
            errors.append("found a secrets context, kit needs none")
        if TOKEN_RE.search(text):
            errors.append("token-shaped literal found")

    # Unpinned uses: (same check in both modes).
    src = path.read_text(encoding="utf-8")
    for i, line in enumerate(src.splitlines(), 1):
        if re.search(r"^\s*(-\s*)?uses:\s*[\"']?[^@\"']+['\"]?\s*$", line):
            errors.append(f"line {i}: uses: not pinned to a version")

    return errors + (["(warning) " + w for w in warnings])


def main() -> int:
    files = [Path(f) for f in sys.argv[1:]] or sorted(
        Path("tests/fixtures").glob("[0-9]*-*.yml")
    )
    if not files:
        print("no fixture files found", file=sys.stderr)
        return 1
    failures = 0
    for f in files:
        errs = structural_errors(f)
        if errs:
            failures += 1
            print(f"FAIL {f}")
            for e in errs:
                print(f"     - {e}")
        else:
            print(f"ok   {f}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
