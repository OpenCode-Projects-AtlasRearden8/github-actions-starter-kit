# GitHub Actions Starter Kit

*A copy-ready kit of beginner-safe GitHub Actions workflows for solo publishers.*

**By Asdale Dynamics, LLC** — plain English, step by step, never condescending.
Licensed MIT. Zero secrets, ever.

---

## What's in the box

Five workflows you can copy into any repository, each one commented
**line-by-line** so you understand every word you're borrowing — plus tests
that prove the files actually work before you ever meet them:

| # | Workflow                      | What it does for you (one breath)                              |
|---|-------------------------------|----------------------------------------------------------------|
| 1 | **Build & Test**              | Runs your project's tests on every push or pull request        |
| 2 | **Markdown Link Check**       | Visits every link in your Markdown and flags broken ones       |
| 3 | **Static Site Deploy**        | Publishes your site to free GitHub Pages on every push         |
| 4 | **Release Tag & Notes**       | Turns a `v1.0`-style tag into a public Release with neat notes |
| 5 | **Daily Health Check**        | One calm robot pass over the whole repo every morning          |

The five copy-ready files live in [`workflows/`](workflows/). Fixture
copies, already run through the [actionlint](https://github.com/rhysd/actionlint)
checker, live in [`tests/fixtures/`](tests/fixtures/) — the tests below
prove those two stay in agreement.

## The three promises

1. **Line-by-line plain English.** Every workflow file explains itself in
   comments as though a friendly colleague were sitting next to you. No
   acronym left unexplained, no "you should already know".
2. **No secrets, ever.** No API keys, no personal data, no tokens to
   store. Where a workflow needs permission, it uses `GITHUB_TOKEN` — the
   short-lived identity GitHub creates *for each run* and throws away
   afterward. The kit even ships a scanner that proves zero secret-shaped
   strings exist anywhere in the repository.
3. **Free tier honest.** Everything here runs on GitHub's free plan.
   `docs/cost-notes.md` documents exactly where the soft limits sit, with
   no marketing gloss.

## Start here

Read [`docs/copy-me-walkthrough.md`](docs/copy-me-walkthrough.md) — a
one-file-at-a-time walkthrough with a green-dot check after every step.
Copy **one** workflow, watch it go green in your repo's Actions tab, then
move to the next. That pace is the whole method.

Then skim [`docs/cost-notes.md`](docs/cost-notes.md) for the free-tier
truths (the important ones: public repos are completely free; private
repos get 2,000 free Actions minutes a month; Pages sites on the free plan
live in public repos; long-idle repos see scheduled runs paused).

## Verifying the kit itself (optional, offline, no account needed)

The kit tests itself so it works offline on your machine, with no GitHub
account, keys, or network use:

```
bash tests/run_tests.sh
```

Checks: fixture payloads are exact copies of the copy-ready files;
fixtures parse and lint cleanly; the repo contains zero secret-shaped
strings; every reusable action is pinned to a version; and the MIT
LICENSE carries the exact intended copyright line.

If you have [actionlint](https://github.com/rhysd/actionlint) installed
(`actionlint` on your PATH), the tests use it as the primary validator;
otherwise a structural fallback runs. Either way, tests pass offline.

## Which file is which

```
workflows/                 <- copy THESE files into your repo (.github/workflows/)
  01-build-and-test.yml
  02-markdown-link-check.yml
  03-static-site-deploy.yml
  04-release-tag-notes.yml
  05-daily-health-check.yml
tests/                     <- the kit's own offline test suite
  run_tests.sh             <- run me with: bash tests/run_tests.sh
  fixtures/                <- actionlint-validated copies of the five files
  validate_fallback.py     <- structural checker (fallback, PyYAML optional)
  scan_for_secrets.py      <- proves the kit holds zero secrets
.github/workflows/
  self-check.yml           <- the kit's OWN minimal CI: runs the test suite
docs/
  copy-me-walkthrough.md   <- "copy me one at a time" instructions
  cost-notes.md            <- free-tier truths, plainly stated
LICENSE                    <- MIT, Copyright (c) 2026 Asdale Dynamics, LLC
STATUS.md                  <- what was built, how it was verified, known gaps
```

## Family of guides from Asdale Dynamics, LLC

- `github-for-everyone-handbook` — the broader manual: what GitHub is,
  what repos/branches/PRs mean, and everyday usage.
- `opencode-free-coding-handbook` — free AI coding tools, in the same
  plain-English voice.

This kit is the *hands-on toolset*: it assumes (or quickly teaches) only
"there's a repo and a main branch", and hands you working automation.
The handbook explains the concepts; the kit does the chores.

## Credits, license, and the fine print

Brought to you by **Asdale Dynamics, LLC** (Indiana, USA) — Dylan Asdale's
company for beginner-friendly AI education, books, and practical tools.
Learn more at <https://dylanasdale.github.io>.

Licensed under the MIT License — see [`LICENSE`](LICENSE). Use it, copy
it, remix it; attribution never required, gratitude always welcome.

*Every workflow here favors calm defaults: version-pinned actions, zero
secrets, and machine-readability nobody needs. If anything looks
confusing, the comments above each line exist to fix that.*
