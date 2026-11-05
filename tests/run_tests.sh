#!/usr/bin/env bash
# =============================================================================
# Offline test-harness: verify the starter kit's YAML fixtures.
#
# Runs fully offline. No network, no credentials, no installs.
#
# Checks (in order):
#   1. Parity      - each tests/fixtures/*.yml is an exact copy of its
#                    workflows/*.yml source (no drift between copy-ready
#                    files and validated fixtures).
#   2. Linting     - actionlint resolves every workflow file, if actionlint
#                    is on the PATH or at tools/actionlint. Otherwise we run
#                    tests/validate_fallback.py (a structural checker) and
#                    print a clear notice.
#   3. No secrets  - scan the entire repo (code + docs) for token-shaped
#                    strings to guarantee the kit ships no real secrets.
#   4. Doc guards  - every workflow carries the "in one sentence" header,
#                    every uses: is pinned to a version (e.g. @v4).
#   5. MIT file    - LICENSE contains the exact copyright line.

# Exit on first failed check so the run stops loudly, like their own
# workflows do.
set -euo pipefail

# The kit root is one dir above the test script.
REPO=$(cd "$(dirname "$0")/.." && pwd)
cd "$REPO"

PASS=0
FAIL=0

ok()   { printf '  pass: %s\n' "$1"; PASS=$((PASS + 1)); }
bad()  { printf '  FAIL: %s\n' "$1"; FAIL=$((FAIL + 1)); }

heading() { printf '\n=== %s ===\n' "$1"; }

# -----------------------------------------------------------------------------
# 1. Fixture parity
heading "Check 1 - fixture parity (fixtures are exact copies of copy-ready files)"
for fix in tests/fixtures/[0-9]*-*.yml; do
  name=$(basename "$fix")
  if diff -q "workflows/$name" "$fix" >/dev/null 2>&1; then
    ok "$name matches workflows/$name"
  else
    bad "$name has drifted from workflows/$name (re-copy or fix)"
  fi
done

# Ensure no source workfile is missing a fixture (or vice versa).
if [ "$(ls workflows/[0-9]*-*.yml | wc -l)" -eq "$(ls tests/fixtures/[0-9]*-*.yml | wc -l)" ]; then
  ok "fixture count matches workflow count"
else
  bad "fixture count does not match workflow file count"
fi

# -----------------------------------------------------------------------------
# 2. Linting (actionlint preferred; offline structural fallback otherwise)
heading "Check 2 - lint the YAML fixtures (plus this kit's own workflow)"
ACTIONLINT_BIN=""
if command -v actionlint >/dev/null 2>&1; then
  ACTIONLINT_BIN="actionlint"
elif [ -x "tools/actionlint" ]; then
  ACTIONLINT_BIN="./tools/actionlint"
fi

LINT_TARGETS="tests/fixtures/[0-9]*-*.yml .github/workflows/*.yml"

if [ -n "$ACTIONLINT_BIN" ]; then
  echo "  using: $ACTIONLINT_BIN"
  if "$ACTIONLINT_BIN" $LINT_TARGETS; then
    ok "actionlint validated every fixture (and the self-check workflow) without errors"
  else
    bad "actionlint reported errors (see above)"
  fi
else
  echo "  - notice: no actionlint installed; using offline structural fallback"
  if python3 tests/validate_fallback.py tests/fixtures/[0-9]*-*.yml .github/workflows/*.yml; then
    ok "structural fallback validated every fixture (and the self-check workflow)"
  else
    bad "structural fallback reported errors (see above)"
  fi
fi

# -----------------------------------------------------------------------------
# 3. Secret scan
heading "Check 3 - secret scan (the kit must ship zero secrets)"
if python3 tests/scan_for_secrets.py "$(pwd)"; then
  ok "no secret-shaped strings found anywhere in the repo"
else
  bad "possible secret detected (see above)"
fi

# -----------------------------------------------------------------------------
# 4. Doc + pin guards
heading "Check 4 - beginner-safe guardrails (headers + version pins)"
for wf in workflows/[0-9]*-*.yml; do
  name=$(basename "$wf")
  if grep -q "in one sentence" "$wf"; then
    ok "$name: has the plain-English one-sentence header"
  else
    bad "$name: missing the one-sentence explanatory header"
  fi
  # Every "uses:" line should name a version (like @v4). A "uses:" line
  # without an @ would be floating whichever version the author has
  # published most recently - exactly the kind of surprise a beginner
  # kit must not teach. (Step lines may or may not carry the "- " dash,
  # depending on key order, so we match both shapes.)
  if grep -E '^[[:space:]]*(-[[:space:]]+)?uses:' "$wf" | grep -Ev '@[a-zA-Z0-9]' >/dev/null 2>&1; then
    bad "$name: found a uses: line without a version pin (should end with @v1 etc.)"
  else
    if grep -E '^[[:space:]]*(-[[:space:]]+)?uses:' "$wf" >/dev/null 2>&1; then
      ok "$name: every uses: is pinned to a version"
    else
      ok "$name: no reusable actions used"
    fi
  fi
done

# -----------------------------------------------------------------------------
# 5. MIT LICENSE
heading "Check 5 - LICENSE present with the exact copyright line"
if [ -f LICENSE ] && grep -qF "Copyright (c) 2026 Asdale Dynamics, LLC" LICENSE; then
  ok "LICENSE has exact copyright line"
else
  bad "LICENSE missing or copyright line incorrect"
fi
if [ -f LICENSE ] && grep -qE '^([[:space:]]*)Permission is hereby granted, free of charge' LICENSE; then
  ok "LICENSE reads as the MIT text"
else
  bad "LICENSE does not look like MIT text"
fi

# -----------------------------------------------------------------------------
# Summary
heading "Summary"
printf '  passed: %s   failed: %s\n' "$PASS" "$FAIL"
if [ "$FAIL" -gt 0 ]; then
  echo "  Test run did NOT pass."
  exit 1
fi
echo "  All tests passed."
