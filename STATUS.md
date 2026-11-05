# STATUS — GitHub Actions Starter Kit

Built: Thursday, November 5, 2026 · by Asdale Dynamics, LLC
State: complete, tested, committed locally. Never pushed, never published.

---

## What was built

A copy-ready kit of five beginner-safe GitHub Actions workflows for solo
publishers, each commented line-by-line in plain English, with zero secrets
anywhere:

1. `workflows/01-build-and-test.yml` — runs a project's tests on every
   push/pull request; auto-detects Node and Python setups and quietly
   skips when a project has no tests registered yet.
2. `workflows/02-markdown-link-check.yml` — visits every link in every
   Markdown file on each push, flags broken ones with file and line.
3. `workflows/03-static-site-deploy.yml` — deploys a static site to free
   GitHub Pages using only the built-in `GITHUB_TOKEN` (no secrets);
   includes one-time "Settings → Pages" instructions and swap-in build
   blocks for Hugo/Jekyll/MkDocs.
4. `workflows/04-release-tag-notes.yml` — pushes of `v*` tags produce a
   public Release page with auto-generated release notes.
5. `workflows/05-daily-health-check.yml` — a 05:23 UTC scheduled pass over
   the whole repo: full Markdown link sweep, a list of pinned action
   versions, and a repo-freshness line in the run summary.

Supporting files:

- `README.md` — overview, three promises (line-by-line comments, no
  secrets, free-tier honest), directory map, verification instructions;
  credits Asdale Dynamics, LLC.
- `LICENSE` — MIT, with the exact line `Copyright (c) 2026 Asdale Dynamics, LLC`.
- `docs/cost-notes.md` — free-tier truths: public repos fully free, 2,000
  free Actions minutes/month on private repos, Pages quirks (public repos
  on the free plan, ~60-day scheduled-run pause for idle repos), and why
  `GITHUB_TOKEN` is not a user-managed secret.
- `docs/copy-me-walkthrough.md` — "copy me one at a time" walkthrough:
  one workflow per session, green-dot verification after each, plain-English
  troubleshooting for the three most common early failures.
- `tests/fixtures/*.yml` — the five workflows as actionlint-validated
  snapshots; the test suite enforces byte-level parity with `workflows/`.
- `tests/run_tests.sh` — the offline test suite (see verification below).
- `tests/validate_fallback.py` — zero-dependency structural validator used
  when actionlint isn't installed (also handles the YAML `on:`/boolean quirk).
- `tests/scan_for_secrets.py` — repo-wide scanner for token-shaped strings
  (AWS, GitHub tokens, OpenAI-style keys, Slack, Google API keys, private
  key blocks, basic-auth URLs).
- `.github/workflows/self-check.yml` — the kit's own minimal CI: installs
  actionlint via the official installer and runs the same offline suite.
  No secrets, pinned actions.
- `.gitignore` — keeps local binaries (`tools/`, `bin/`) and OS clutter out.

## How to run it

- Use the kit: copy files from `workflows/` into a repo's
  `.github/workflows/` folder one at a time, per `docs/copy-me-walkthrough.md`.
- Run the offline test suite: `bash tests/run_tests.sh` (no network, no
  account, no dependencies).
- Optional stronger lint: install
  [actionlint](https://github.com/rhysd/actionlint) so the tests use it as
  the primary validator; the suite fully passes either way.
- Secret audit of any local clone: `python3 tests/scan_for_secrets.py .`

## Verification results

Environment: Linux x86_64, git 2.47.3, Python 3.13.5 (PyYAML 6.0.3),
actionlint v1.7.12 downloaded locally for verification (not committed).

- `actionlint` v1.7.12: **0 errors** on all five copy-ready workflows and
  on the kit's own `.github/workflows/self-check.yml`.
- `bash tests/run_tests.sh` with actionlint on PATH: **20 checks passed,
  0 failed.**
- `bash tests/run_tests.sh` without actionlint (structural fallback mode):
  **20 checks passed, 0 failed.**
- Negative controls (run in a sandbox copy, all restored afterward): each
  planted fault correctly failed the suite —
  - planted GitHub-token-shaped string → suite failed (secret scan),
  - edited fixture to drift from its copy-ready source → failed (parity),
  - removed a version pin from `uses: actions/checkout@v4` → failed (pins),
  - altered the LICENSE copyright line → failed (license check).
- The five fixtures in `tests/fixtures/` are byte-identical to the files
  in `workflows/` as of this commit; parity is enforced by check 1 of the
  suite.

## Known gaps

- **Workflows are validated, not executed.** actionlint proves the YAML is
  a well-formed workflow; proving run-time behavior would require pushing
  to GitHub. The self-check workflow, if anyone ever pushes this kit to
  GitHub, provides that last layer — but doing so was explicitly out of
  scope here (never push, never publish).
- **Build & Test auto-detection is intentionally simple.** It handles the
  common npm/pytest layouts; projects with Make-only or CMake-only test
  systems should replace the guarded steps with their own commands —
  the comments explain exactly where.
- **Action version pins can age.** `@v4`-style major pins drift over
  years; the Daily Health Check prints every pin so staleness is visible.
- **No shellcheck** of `run:` blocks (actionlint performs some static
  shell checks; a full shellcheck pass was out of scope).
- **Fixture set covers the five copy-ready workflows only**; the kit's own
  self-check workflow is linted by check 2 of the suite but has no parity
  fixture of its own (by design — it is the kit's housekeeping, not one of
  the five files a user copies).
- GitHub's free-tier numbers in `docs/cost-notes.md` reflect early-2026
  documentation and are soft limits; GitHub may adjust quotas over time.
