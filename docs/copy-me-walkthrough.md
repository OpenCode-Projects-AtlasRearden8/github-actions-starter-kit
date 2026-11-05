# Copy me one at a time — a gentle walkthrough

This page is your first driving lesson with the seatbelts on: how to take
the five workflows in this kit and install them into a real repository,
one at a time, with a calm check after each. Never rush ahead to the next
one until the current one shows you a green dot first.

> You need: a GitHub account, a repository you own (public keeps it all
> free), and ~20 minutes total for workflow #1. Git commands shown use the
> terminal, but every step is also possible in the GitHub website editor.

---

## The mental model (read once, then forget it)

- Workflows live in a hidden folder of your repo: `.github/workflows/`.
- Any file in there ending in `.yml` is a workflow. That's the whole rule.
- Files here will never, ever hold a secret. GitHub supplies what runs are
  allowed to use, and expires it after the run.
- A run either goes green (worked) or red (failed) in the **Actions** tab.

---

## Workflow #1 — Build & Test

1. In your repo folder, create the folder:
   ```
   mkdir -p .github/workflows
   ```
2. Copy `workflows/01-build-and-test.yml` from this kit into that folder.
3. Commit and push:
   ```
   git add .github/workflows/01-build-and-test.yml
   git commit -m "Add build-and-test workflow"
   git push
   ```
4. Check: open the repo's **Actions** tab. You should see "Build and Test"
   running, then a green check next to a commit name.
   - If it's red: open the log, find the first step with a red X. Common
     first-week causes: a failing test (great news — the robot caught it),
     or a typo in a file the tests expect.
   - If steps say "skipped": your project has no registered tests yet —
     that's the workflow politely bowing out, not an error.

**Green?** Move on. **Red?** Fix or simplify, then move on. One workflow at
a time beats five disasters at once.

---

## Workflow #2 — Markdown Link Check

1. Copy `02-markdown-link-check.yml` into `.github/workflows/`.
2. Push it the same way as workflow #1.
3. Check: the run will visit every link in your Markdown files. On a repo
   with README and a few docs, this concludes in under a minute.
   - Any broken or robot-blocked links appear as red with the file name
     and line number in the log.
   - Robot-blocked sites (login walls, some store pages) can never verify
     from a server. That is not a workflow error: rewrite the link or
     accept the known-unknown consciously.

---

## Workflow #3 — Static Site Deploy

1. **One-time prep:** in your repository open *Settings → Pages*; under
   "Build and deployment" set **Source: GitHub Actions**. (This is the
   step everyone forgets. It takes four clicks.)
2. Copy `03-static-site-deploy.yml` into `.github/workflows/`.
3. Push. Check the green run, then open `https://YOURNAME.github.io/YOURREPO/`.
4. If your repo isn't a plain-HTML site, see the "Adapt it" block at the
   bottom of the file for Hugo, Jekyll, and MkDocs variants.
5. Troubleshooting note: if the *Configure Pages* step says something like
   "Pages not enabled" — the Settings → Pages step above wasn't done.

The site deploys only on pushes to `main`. Pull requests never publish
anything — that's deliberate, and it's a good rule to keep.

---

## Workflow #4 — Release Tag & Notes

There's nothing else to copy — the file already knows everything. Once it's
in `.github/workflows/` use it with two commands whenever you feel a
version is ready to be called a version:

```
git tag v1.0
git push origin v1.0
```

The Actions tab then shows a short run that ends with a real Release page
at `https://github.com/YOURNAME/YOURREPO/releases`, containing notes
GitHub assembled from your commits automatically. To cut the next version,
just push `v1.1` later.

---

## Workflow #5 — Daily Health Check

1. Copy `05-daily-health-check.yml` into `.github/workflows/`.
2. Push.
3. In the Actions tab, notice the run it fired immediately if you used the
   manual run button (`workflow_dispatch` also exists on its page); the
   daily alarm is set to 05:23 UTC.
4. Deep breath: you're done. Tracking now happens on autopilot.

Remember Truth 4 from `docs/cost-notes.md`: if a repo goes months without
commits, GitHub pauses the daily alarm and emails you once about it. Push
anything to wake the robot back up.

---

## After all five: your calm maintenance routine

- **Morning:** glance at yesterday's Daily Health Check. Green? Done.
- **Whenever you push docs:** link check runs itself. You read only when
  red.
- **Whenever you publish a version:** push a tag. Release notes write
  themselves.
- **Never:** store a secret, key, or personal data inside any file here.
  If a step ever asks you to, it's not from this kit — stop and read.

---

## The five-minute self-audit

Once a month, run this kit's own audits against your repo with two commands:

```
python3 tests/scan_for_secrets.py YOUR_REPO_PATH   # zero secrets, verified
actionlint .github/workflows/*.yml                 # gentle YAML lint (optional tool)
```

Both are free, run offline, and confirm what this kit promises: simple,
safe, and zero surprises.
