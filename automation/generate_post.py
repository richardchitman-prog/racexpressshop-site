#!/usr/bin/env python3
"""
Generates one new RoboCallMeNot blog post from the curated fact bank in topics.json,
inserts it into the shared template, updates index.html and sitemap.xml, and
posts a short hook + link to Bluesky and Mastodon (if credentials are configured).

Run by .github/workflows/publish.yml on a schedule. Safe to run manually too:
    python automation/generate_post.py
"""
import json
import os
import re
import sys
from datetime import date, datetime
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
AUTOMATION_DIR = ROOT / "automation"
BLOG_DIR = ROOT / "blog"
STATE_FILE = AUTOMATION_DIR / "state.json"
TOPICS_FILE = AUTOMATION_DIR / "topics.json"
TEMPLATE_FILE = AUTOMATION_DIR / "template.html"
INDEX_FILE = BLOG_DIR / "index.html"
SITEMAP_FILE = ROOT / "sitemap.xml"
SITE_BASE_URL = os.environ.get("SITE_BASE_URL", "https://racexpressshop.netlify.app/blog")

sys.path.insert(0, str(AUTOMATION_DIR))
from hero_illustrations import HERO_SVGS  # noqa: E402


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"next_index": 0, "published": []}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))


def pick_topic(topics, state):
    idx = state["next_index"] % len(topics)
    state["next_index"] = idx + 1
    return topics[idx]


def call_gemini(topic):
    api_key = os.environ["GEMINI_API_KEY"]
    model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

    facts_block = "\n".join(f"- {f}" for f in topic["facts"])

    system_instructions = (
        "You are writing one blog post section-set for RoboCallMeNot, a security app that files "
        "one-tap robocall reports to the FTC, FCC, and FBI's IC3. The brand voice is a respectful "
        "'case file' tone: calm, factual, never fear-mongering, never condescending about age or "
        "technical skill. "
        "\n\nCRITICAL RULE: You may ONLY use the facts listed below. Do not state any statistic, "
        "number, date, or factual claim that is not explicitly given to you. If you want a "
        "transition or framing sentence, keep it qualitative and general — never invent a number, "
        "a study, or a source. "
        "\n\nReturn ONLY valid JSON matching this exact schema, no markdown fences, no commentary:\n"
        "{\n"
        '  "title": "short page title, 6-9 words",\n'
        '  "meta_description": "1 sentence, under 155 characters",\n'
        '  "headline": "hero headline, punchy, under 12 words",\n'
        '  "subhead": "1-2 sentences expanding the headline, must naturally mention RoboCallMeNot",\n'
        '  "exhibit_a_title": "short section title",\n'
        '  "exhibit_a_body": "2-3 sentences using the facts, this is the main stats/evidence section",\n'
        '  "exhibit_b_title": "short section title",\n'
        '  "exhibit_b_body": "2-3 sentences, the how-it-works or why-it-matters angle",\n'
        '  "exhibit_c_title": "short section title, framed as practical takeaway",\n'
        '  "exhibit_c_body": "2-3 sentences, practical and actionable, leads into the app CTA",\n'
        '  "cta_headline": "short, under 8 words",\n'
        '  "cta_body": "1 sentence reinforcing why to get the app now",\n'
        '  "social_hook": "one punchy sentence under 220 characters for a social media post, '
        'no hashtags, no link (the link is added separately)"\n'
        "}"
    )

    prompt = (
        f"{system_instructions}\n\n"
        f"TOPIC BRIEF: {topic['topic_brief']}\n\n"
        f"FACTS YOU MAY USE (and only these):\n{facts_block}\n"
    )

    resp = requests.post(
        url,
        json={
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "responseMimeType": "application/json",
                "temperature": 0.6,
            },
        },
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    text = data["candidates"][0]["content"]["parts"][0]["text"]
    return json.loads(text)


def render_post(topic, content, case_number):
    template = TEMPLATE_FILE.read_text()
    hero_svg = HERO_SVGS.get(topic["category"], HERO_SVGS["explainer"])

    replacements = {
        "{{TITLE}}": content["title"],
        "{{META_DESC}}": content["meta_description"],
        "{{CASE_NUMBER}}": case_number,
        "{{HEADLINE}}": content["headline"],
        "{{SUBHEAD}}": content["subhead"],
        "{{HERO_SVG}}": hero_svg,
        "{{EXHIBIT_A_TITLE}}": content["exhibit_a_title"],
        "{{EXHIBIT_A_BODY}}": content["exhibit_a_body"],
        "{{STAT_NUMBER}}": topic["stat_callout_number"],
        "{{STAT_LABEL}}": topic["stat_callout_label"],
        "{{EXHIBIT_B_TITLE}}": content["exhibit_b_title"],
        "{{EXHIBIT_B_BODY}}": content["exhibit_b_body"],
        "{{EXHIBIT_C_TITLE}}": content["exhibit_c_title"],
        "{{EXHIBIT_C_BODY}}": content["exhibit_c_body"],
        "{{CTA_HEADLINE}}": content["cta_headline"],
        "{{CTA_BODY}}": content["cta_body"],
        "{{FOOTER_SOURCE_NOTE}}": (
            "Figures cited above are drawn from a curated set of published FTC, FCC, and "
            "YouMail Robocall Index research, reviewed before publication."
        ),
    }
    html = template
    for token, value in replacements.items():
        html = html.replace(token, value)
    return html


def write_post_file(slug, html):
    BLOG_DIR.mkdir(exist_ok=True)
    path = BLOG_DIR / f"{slug}.html"
    path.write_text(html)
    return path


def update_index(slug, content):
    if not INDEX_FILE.exists():
        return
    index_html = INDEX_FILE.read_text()
    card = f"""
      <a href="{slug}.html" class="post-card">
        <div class="post-thumb">
          <svg viewBox="0 0 140 130" xmlns="http://www.w3.org/2000/svg">
            <g transform="translate(35 25)"><path d="M0 15 L70 15 L65 78 Q65 84 58 84 L12 84 Q5 84 5 78 Z" fill="#f2ede0" stroke="#202a3a" stroke-width="2"/><path d="M0 15 L13 4 L57 4 L70 15 Z" fill="#e4dcc4" stroke="#202a3a" stroke-width="2"/></g>
            <g transform="translate(95 20) rotate(-10)"><circle cx="0" cy="0" r="16" fill="none" stroke="#a63a2e" stroke-width="2.5"/><text x="0" y="4" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="7" font-weight="700" fill="#a63a2e">NEW</text></g>
          </svg>
        </div>
        <div class="post-body">
          <span class="post-tag">Exhibit File</span>
          <h3>{content['title']}</h3>
          <p>{content['meta_description']}</p>
          <span class="readmore">Open the file →</span>
        </div>
      </a>
"""
    updated = index_html.replace("<!-- AUTO-POSTS-END -->", card + "      <!-- AUTO-POSTS-END -->")
    INDEX_FILE.write_text(updated)


def update_sitemap(slug):
    if not SITEMAP_FILE.exists():
        return
    sitemap = SITEMAP_FILE.read_text()
    today = date.today().isoformat()
    entry = (
        f"  <url>\n"
        f"    <loc>{SITE_BASE_URL}/{slug}.html</loc>\n"
        f"    <lastmod>{today}</lastmod>\n"
        f"    <changefreq>monthly</changefreq>\n"
        f"    <priority>0.7</priority>\n"
        f"  </url>\n"
    )
    marker = "  <!-- AUTO-SITEMAP-ENTRIES will be appended above this line by automation/generate_post.py -->"
    updated = sitemap.replace(marker, entry + marker)
    SITEMAP_FILE.write_text(updated)


def post_to_bluesky(text, url):
    handle = os.environ.get("BLUESKY_HANDLE")
    app_password = os.environ.get("BLUESKY_APP_PASSWORD")
    if not handle or not app_password:
        print("Bluesky credentials not set, skipping.")
        return
    try:
        session_resp = requests.post(
            "https://bsky.social/xrpc/com.atproto.server.createSession",
            json={"identifier": handle, "password": app_password},
            timeout=30,
        )
        session_resp.raise_for_status()
        session = session_resp.json()

        full_text = f"{text}\n\n{url}"
        text_bytes = full_text.encode("utf-8")
        url_start = full_text.rfind(url)
        byte_start = len(full_text[:url_start].encode("utf-8"))
        byte_end = byte_start + len(url.encode("utf-8"))

        record = {
            "$type": "app.bsky.feed.post",
            "text": full_text,
            "createdAt": datetime.utcnow().isoformat() + "Z",
            "facets": [
                {
                    "index": {"byteStart": byte_start, "byteEnd": byte_end},
                    "features": [{"$type": "app.bsky.richtext.facet#link", "uri": url}],
                }
            ],
        }
        post_resp = requests.post(
            "https://bsky.social/xrpc/com.atproto.repo.createRecord",
            headers={"Authorization": f"Bearer {session['accessJwt']}"},
            json={"repo": session["did"], "collection": "app.bsky.feed.post", "record": record},
            timeout=30,
        )
        post_resp.raise_for_status()
        print("Posted to Bluesky.")
    except Exception as e:
        print(f"Bluesky post failed (non-fatal): {e}")


def post_to_mastodon(text, url):
    base_url = os.environ.get("MASTODON_BASE_URL")
    token = os.environ.get("MASTODON_ACCESS_TOKEN")
    if not base_url or not token:
        print("Mastodon credentials not set, skipping.")
        return
    try:
        resp = requests.post(
            f"{base_url.rstrip('/')}/api/v1/statuses",
            headers={"Authorization": f"Bearer {token}"},
            data={"status": f"{text}\n\n{url}"},
            timeout=30,
        )
        resp.raise_for_status()
        print("Posted to Mastodon.")
    except Exception as e:
        print(f"Mastodon post failed (non-fatal): {e}")


def main():
    topics = json.loads(TOPICS_FILE.read_text())
    state = load_state()
    topic = pick_topic(topics, state)

    print(f"Generating post for topic: {topic['id']}")
    content = call_gemini(topic)

    case_number = f"RCN-{date.today().strftime('%Y%m%d')}"
    html = render_post(topic, content, case_number)
    path = write_post_file(topic["slug"], html)
    print(f"Wrote {path}")

    update_index(topic["slug"], content)
    update_sitemap(topic["slug"])

    state["published"].append(
        {"slug": topic["slug"], "topic_id": topic["id"], "date": date.today().isoformat()}
    )
    save_state(state)

    post_url = f"{SITE_BASE_URL}/{topic['slug']}.html"
    hook = content.get("social_hook", content["headline"])
    post_to_bluesky(hook, post_url)
    post_to_mastodon(hook, post_url)

    print("Done.")


if __name__ == "__main__":
    main()
