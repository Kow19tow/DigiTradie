"""sitemap.xml, robots.txt, llms.txt, llms-full.txt, feed.xml, vercel.json, .vercelignore. All generated so they never drift from the pages."""
import json
from datetime import datetime, timezone

from . import core
from .core import EMAIL, GUIDES, PACKAGES, PHONE, ROOT, SERVICES, SITE

AI_BOTS = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-User", "Claude-SearchBot", "PerplexityBot", "Perplexity-User",
           "Google-Extended", "Applebot-Extended", "Amazonbot", "CCBot", "Bytespider", "meta-externalagent"]


def write_sitemap():
    rows = []
    for path, pri, freq, mod in sorted(core.REGISTRY, key=lambda r: (-float(r[1]), r[0])):
        loc = SITE + (path if path != "/" else "/")
        rows.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{mod}</lastmod>\n    <changefreq>{freq}</changefreq>\n    <priority>{pri}</priority>\n  </url>")
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(rows) + "\n</urlset>\n")


def write_robots():
    bots = "\n\n".join(f"User-agent: {b}\nAllow: /" for b in AI_BOTS)
    (ROOT / "robots.txt").write_text(
        f"""# DigiTradie. Search engines and AI assistants are welcome to read and cite this site.
User-agent: *
Allow: /
Disallow: /thank-you

# AI search and assistant crawlers (allowed on purpose)
{bots}

Sitemap: {SITE}/sitemap.xml
""")


def _lines(items):
    return "\n".join(items)


def write_llms(guides, posts):
    svc = _lines(f"- [{s[1]}]({SITE}/services/{s[0]}): {s[2]}" for s in SERVICES)
    pk = _lines(f"- [{p[1]}]({SITE}/{p[0]}): {p[3]}" for p in PACKAGES)
    gd = _lines(f"- [{g['title']}]({SITE}/learn/{g['slug']}): DIY marketing guide for {g['label'].lower()}" for g in guides)
    bl = _lines(f"- [{p['h1']}]({SITE}/blog/{p['slug']}): {p['desc']}" for p in posts)
    txt = f"""# DigiTradie

> DigiTradie is a fractional in-house marketing service for small and medium businesses in Australia. It runs Meta Ads (Facebook and Instagram), Google Ads, SEO and website optimisation, and gives every client a plain-English dashboard. It qualifies clients hard: every lead books one free fit-check call (usually 15 to 20 minutes) and is told straight whether DigiTradie can help. Founder: Kosta Diamantopoulos.

Key facts
- Service area: Australia (remote). Despite the name, clients span industries, not only trades.
- Packages (exact pricing is confirmed on the fit-check call; ad spend is separate): Audit & Optimise (once-off), Dashboard + Ads Setup (once-off, coaching add-on), Fractional In-House Marketer (monthly, 3-month minimum, then flexible, limited spots).
- Evidence: $500 in ad spend turned into $75k+ profit for one Melbourne renovation business by changing the offer. Founder experience includes global ad agency networks, national telecom and fashion retail brands, luxury hospitality campaigns and $100k+ monthly ad budgets on international accounts.
- Contact: {EMAIL}, {PHONE}, {SITE}/contact

## Services
{svc}

## Packages
{pk}

## Company
- [About Kosta]({SITE}/about): who runs DigiTradie and how it works
- [FAQ]({SITE}/faq): cost, contracts, the fit-check call, ad spend, results
- [Contact and book a fit check]({SITE}/contact)

## Blog
{bl}

## Free DIY marketing guides by industry
{gd}
"""
    (ROOT / "llms.txt").write_text(txt)
    # fuller text for assistants that prefer one file
    from .pages_home import HOME_FAQS
    from .pages_main import FAQ_GROUPS
    import re
    strip = lambda s: re.sub(r"<[^>]+>|&rsquo;", lambda m: "'" if m.group(0) == "&rsquo;" else "", s)
    faq = "\n\n".join(f"### {q}\n{strip(a)}" for _, qs in FAQ_GROUPS for q, a in qs)
    (ROOT / "llms-full.txt").write_text(txt + f"\n## Frequently asked questions\n\n{faq}\n")


def write_feed(posts):
    items = []
    for p in sorted(posts, key=lambda p: p["date"], reverse=True):
        d = datetime.fromisoformat(p["date"]).replace(tzinfo=timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
        items.append(f"<item><title>{core.esc(p['h1'])}</title><link>{SITE}/blog/{p['slug']}</link><guid>{SITE}/blog/{p['slug']}</guid><pubDate>{d}</pubDate><description>{core.esc(p['desc'])}</description></item>")
    (ROOT / "feed.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>DigiTradie blog</title><link>{SITE}/blog</link>'
        f"<description>Straight-talking marketing advice for small business.</description><language>en-AU</language>{''.join(items)}</channel></rss>\n")


def write_hosting():
    sec = [{"key": "X-Content-Type-Options", "value": "nosniff"}, {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
           {"key": "X-Frame-Options", "value": "SAMEORIGIN"}, {"key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()"}]
    cfg = {
        "cleanUrls": True,
        "trailingSlash": False,
        "headers": [
            {"source": "/assets/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]},
            {"source": "/(images|og)/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=2592000"}]},
            {"source": "/(.*)", "headers": sec},
        ],
        "redirects": [{"source": "/index.html", "destination": "/", "permanent": True}],
    }
    (ROOT / "vercel.json").write_text(json.dumps(cfg, indent=2) + "\n")
    (ROOT / ".vercelignore").write_text("# Not part of the website: source files, working folders and scripts\nsocial\nbrand\nTool Icons\nPics of me\nContent Used\ncontent\nlib\nsrc\nbuild.py\nREADME.md\n*.py\nog/.cache.json\n.DS_Store\n")
