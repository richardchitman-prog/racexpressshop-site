# RoboCallMeNot Blog Automation — Setup Guide

This turns your blog into a self-running pipeline: twice a week, it writes a new post from a
curated fact bank (never invented statistics), deploys it automatically, and posts a link to
Bluesky and Mastodon. Total cost: $0.

## What you're setting up

```
Your GitHub repo
  ├── blog/                      ← your 4 existing pages, plus new auto-generated ones
  ├── automation/
  │   ├── topics.json            ← the fact bank — edit this to add/change topics
  │   ├── template.html          ← shared page shell (don't need to touch this)
  │   ├── hero_illustrations.py  ← 4 reusable illustration variants
  │   ├── generate_post.py       ← the script that does the work
  │   └── state.json             ← tracks which topic runs next
  ├── .github/workflows/publish.yml   ← the schedule (Mon & Thu by default)
  ├── sitemap.xml
  ├── robots.txt
  └── index.html                 ← your existing homepage
```

---

## Step 1: Create a GitHub repository

1. Go to [github.com](https://github.com) and sign up if you don't have an account (free).
2. Click **New repository**. Name it something like `racexpressshop-site`. Keep it **Public**
   (public repos get unlimited free GitHub Actions minutes; private repos get 2,000 free
   minutes/month, which is still plenty for this, but public is simplest).
3. On your computer, put **all** your site files in one folder — your existing homepage files,
   plus the `blog/`, `automation/`, `.github/`, `sitemap.xml`, and `robots.txt` files from this
   chat — and push that folder to the new repo. If you're not comfortable with git commands,
   GitHub's web interface lets you drag-and-drop files directly into the repo through the
   "Add file → Upload files" button.

## Step 2: Get a free Gemini API key

1. Go to [aistudio.google.com](https://aistudio.google.com) and sign in with a Google account.
2. Click **Get API key → Create API key**. No credit card required.
3. Copy the key — you'll paste it into GitHub in Step 5.

## Step 3 (optional but recommended): Set up Bluesky auto-posting

1. Create a free account at [bsky.app](https://bsky.app) for RoboCallMeNot if you don't have one.
2. Go to **Settings → App Passwords → Add App Password**. Name it "automation" and copy the
   generated password (not your login password — this is a separate, revocable one).
3. Note your handle (e.g. `robocallmenot.bsky.social`).

## Step 4 (optional but recommended): Set up Mastodon auto-posting

1. Create a free account on any Mastodon server (e.g. [mastodon.social](https://mastodon.social)).
2. Go to **Preferences → Development → New Application**. Name it "automation," check the
   `write:statuses` scope, and click Submit.
3. Copy the **Access Token** shown after creating it.
4. Note your server's base URL (e.g. `https://mastodon.social`).

## Step 5: Add your credentials to GitHub Secrets

In your GitHub repo: **Settings → Secrets and variables → Actions → New repository secret**.
Add each of these (skip Bluesky/Mastodon ones if you skipped Steps 3–4):

| Secret name | Value |
|---|---|
| `GEMINI_API_KEY` | the key from Step 2 |
| `BLUESKY_HANDLE` | e.g. `robocallmenot.bsky.social` |
| `BLUESKY_APP_PASSWORD` | the app password from Step 3 |
| `MASTODON_BASE_URL` | e.g. `https://mastodon.social` |
| `MASTODON_ACCESS_TOKEN` | the token from Step 4 |

## Step 6: Connect Netlify to GitHub (replaces manual drag-and-drop)

1. In the Netlify dashboard, open the **racexpressshop** site.
2. Go to **Site configuration → Build & deploy → Link repository** (or **Site settings →
   Build & deploy → Continuous deployment**).
3. Choose GitHub, authorize it, and select the repo you created in Step 1.
4. Build settings: no build command needed, publish directory is the repo root (`.` / `/`),
   since these are plain HTML files with no build step.
5. Save. From now on, every push to the repo's main branch auto-deploys — no more dragging
   folders into the dropzone.

## Step 7: Test it manually before waiting for the schedule

1. In your repo, go to the **Actions** tab.
2. Click **Auto-publish RoboCallMeNot blog post** in the left sidebar, then **Run workflow**
   (this is the `workflow_dispatch` trigger — it lets you run it on demand instead of waiting
   for Monday).
3. Watch the run. It should finish green in under a minute.
4. Check your repo's `blog/` folder for the new file, then check `racexpressshop.netlify.app/blog/`
   once Netlify finishes deploying (usually under a minute after the push).
5. Check Bluesky/Mastodon (if configured) for the new post.

## Step 8: Submit your sitemap so search engines actually crawl it

1. Go to [Google Search Console](https://search.google.com/search-console), add
   `racexpressshop.netlify.app` as a property, verify ownership (Netlify shows you how, usually
   a DNS or HTML-file method), then under **Sitemaps**, submit `sitemap.xml`.
2. Do the same at [Bing Webmaster Tools](https://www.bing.com/webmasters) — Bing also powers
   a chunk of DuckDuckGo and Yahoo results, so it's worth the extra five minutes.
3. This is a one-time setup. The sitemap itself updates automatically every time the pipeline
   publishes a new post.

---

## How to change things later

- **Change the schedule** — edit the `cron:` line in `.github/workflows/publish.yml`.
  Current default is Monday & Thursday at 14:00 UTC. [crontab.guru](https://crontab.guru) is
  useful for building the expression.
- **Add new topics** — add an entry to `automation/topics.json` following the existing format.
  Only include facts you've personally verified — the script is instructed to use only what's
  in that file, so bad data in means bad data out.
- **Pause it** — go to the Actions tab, click the workflow, and click **Disable workflow**.
  Nothing runs while it's disabled; re-enable anytime.
- **Change posting frequency of a topic** — the script cycles through `topics.json` in order
  and wraps back to the start once it reaches the end, so topics do eventually repeat
  (with fresh AI-written wording) once you've used them all.

## What this does NOT do (by design)

- **Doesn't post to X/Instagram/Facebook.** Those platforms don't have a genuinely free
  automated posting path anymore (see below). Use the social-media-snippets.md file for those,
  posted manually, or revisit this if you're ever open to a paid scheduling tool.
- **Doesn't skip human review entirely in spirit** — the LLM is locked to a pre-approved fact
  bank so it can't invent statistics, but it's worth skimming new posts occasionally to make
  sure the tone still sounds right.
- **Runs twice a week, not twice a day.** Faster than that risks both factual drift and looking
  like low-value auto-generated content to search engines — which would work against the SEO
  goal rather than for it.
