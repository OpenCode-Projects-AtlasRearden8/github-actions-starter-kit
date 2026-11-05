# Cost notes — free-tier truths

Everything in this kit runs on **GitHub's free tier**. No credit card, no
subscription, no billing alerts. This page is the honest fine print: what
"is free" really means, and where the soft limits actually sit. Plain
English throughout, and a promise kept: nothing here requires a secret, a
key, or a paid plan.

---

## The four free-tier truths

### Truth 1 — Public repositories are free. Completely.

Actions minutes, Pages hosting, release pages, link checks: a public repo
pays nothing. GitHub's business rests on teams keeping work private; your
public book or tool repo is welcome traffic. If a project can be public,
every workflow in this kit costs literally $0.

### Truth 2 — Private repositories get a refillable free allowance.

If you keep a project private, a free personal account gets **2,000 free
Actions minutes per month**, refilled at the start of every month. Unused
minutes do not roll over, but the bucket refills like a phone plan.

For one small repo wearing this kit, a typical month looks like:

| Workflow                | Typical run time | Rough monthly usage    |
| ----------------------- | ---------------- | ---------------------- |
| Build & test            | ~1–2 min         | each push (optional)   |
| Markdown link check     | ~1 min           | each Markdown push     |
| Static-site deploy      | ~1 min           | each site push         |
| Release tag & notes     | ~1 min           | each tag (rare)        |
| Daily health check      | under 1 min      | ~20–30 min per month   |

That is a rounding error against 2,000 minutes. A solo publisher with a
dozen small repos still uses a tiny sliver of the allowance.

### Truth 3 — Pages is free, with a couple of quiet rules.

- Pages sites on the free plan must live in **public repositories**.
  Publishing from a private repo needs a paid plan — which is exactly why
  most author hubs are public anyway.
- Sites must be **static**: plain files, no server-side code or database.
  That suits hubs, landing pages, and book previews perfectly.
- Soft limits: about 1 GB site size, 100 GB bandwidth/month, 10 builds per
  hour. A book-hub repo is nowhere near any of these.
- Custom domains are supported and free on Pages; the only thing you might
  ever pay a registrar for is the domain name itself, and that is optional.

### Truth 4 — Scheduled runs are free, with three quirks.

The daily health check uses `schedule:`. Three plain-English truths:

1. Cron runs can be **jittery** — a 05:23 UTC job might start minutes
   late. Punctuality is a bonus here, not a guarantee.
2. If a repository has **no commits for a very long stretch (typically
   60 days), scheduled runs are paused automatically** until there is new
   activity. Solo repos with rare commits will hit this eventually; it is
   not a bug in your workflow.
3. Minutes still tick for scheduled runs on private repos — but one
   one-minute check per day is far below the allowance.

---

## Any paid trap hiding in this kit?

**No.** What this kit deliberately avoids:

- No secret, token, or API key anywhere. Verify it yourself:
  `python3 tests/scan_for_secrets.py .`
- No third-party paid actions. All five workflows use either GitHub's own
  actions (`actions/checkout`, `actions/setup-node`, the Pages actions and
  friends) or free community actions
  (`gaurav-nelson/github-action-markdown-link-check`,
  `softprops/action-gh-release`).
- No "Pro feature" workflows. Nothing here even requires a billing
  profile to view the Actions tab.

A note on **GITHUB_TOKEN** (one time, and finally): it is *not* your
secret. GitHub mints a fresh, narrowly-scoped token for each run, hands it
delicately to the workflow, and expires it when the run ends. You never
type it, store it, or renew it. That is why the deploy and release
workflows are secret-free.

---

## If you ever outgrow the free tier

You won't for a solo publishing drip, but for honesty's sake: a paid plan
would only matter if you (a) ran heavy builds (compiling large apps, big
data jobs) or (b) hosted Pages sites from private repos. Both are far down
the road. The practical advice: start free, stay free, and enjoy the
watch-your-wallet-stay-closed quarterly reviews.
