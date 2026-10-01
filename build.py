#!/usr/bin/env python3
"""
Regenerates the /learn/ section of digitradie.com from
content/learn/DigiTradie Industry Guides.docx.

The Word doc is the single source of truth. To update a guide:
  1. Edit content/learn/DigiTradie Industry Guides.docx
  2. Run: python3 build.py
  3. Check the changed files with `git status`, then commit and push.

Doc structure this script expects, per industry:
  Heading 2 "How to market a <industry>"  - starts a guide
    Normal                                - intro paragraph (lede + meta description)
    Heading 3 <section>                   - a subsection (varies per guide)
      Normal / List Paragraph             - body text or bullets.
                                             Lines starting with "☐" -> a task list.
    Heading 3 "FAQs"                      - alternating Normal paragraphs:
                                             question, answer, question, answer...
                                             Rendered as an accordion and used for
                                             the FAQPage schema.
  Heading 2 "Tone of voice" is internal writing guidance and is never published.

Requires: pip3 install --user python-docx
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    import docx
except ImportError:
    sys.exit("Missing dependency. Run: pip3 install --user python-docx")

REPO_ROOT = Path(__file__).resolve().parent
DOCX_PATH = REPO_ROOT / "content" / "learn" / "DigiTradie Industry Guides.docx"
SITE_URL = "https://digitradie.com"

# Explicit slug + display-name map, so URLs stay stable even if the doc's
# wording changes slightly. Add a new tuple here when a new industry is
# added to the doc; unmatched industries fall back to an auto-slug.
INDUSTRY_MAP = [
    (r"hospitality", "hospitality-marketing", "Hospitality"),
    (r"service-based", "tradie-marketing", "Tradies"),
    (r"retail", "retail-marketing", "Retail"),
    (r"beauty", "beauty-salon-marketing", "Beauty"),
    (r"\bgym\b", "gym-marketing", "Gyms"),
    (r"building", "builder-marketing", "Builders"),
    (r"law firm", "law-firm-marketing", "Law Firms"),
    (r"dental", "dental-marketing", "Dental"),
    (r"accounting", "accountant-marketing", "Accountants"),
    (r"physio", "physio-marketing", "Physio & Allied Health"),
    (r"mechanic", "mechanic-marketing", "Mechanics"),
    (r"solar", "solar-marketing", "Solar"),
]

SMALL_WORDS = {"a", "an", "the", "of", "for", "in", "to", "and", "or", "your", "my"}

# Punchier on-page H1 / <title> per guide, keyed by slug. Falls back to the
# literal "How to market a <industry>" heading from the doc when a slug
# isn't listed here. Meta description still comes from the doc's intro
# paragraph, so this only overrides the headline, not the content.
HEADLINE_OVERRIDES = {
    "hospitality-marketing": "Hospitality Marketing That Fills Tables Without Discounting Every Night",
    "tradie-marketing": "Tradie Marketing That Keeps The Job Board Full",
    "retail-marketing": "Retail Marketing That Turns Browsers Into Buyers",
    "beauty-salon-marketing": "Beauty Salon Marketing That Keeps Your Books Full",
    "gym-marketing": "Gym Marketing That Keeps Members Past Month One",
    "builder-marketing": "Builder Marketing That Wins Bigger Jobs, Not Just More Quotes",
    "law-firm-marketing": "Law Firm Marketing That Brings In Clients Who Can Pay",
    "dental-marketing": "Dental Marketing That Fills The Chair, Not Just The Inbox",
    "accountant-marketing": "Accountant Marketing That Attracts Clients Worth Keeping",
    "physio-marketing": "Physio Marketing That Builds A Steady Caseload",
    "mechanic-marketing": "Mechanic Marketing That Keeps The Bays Full",
    "solar-marketing": "Solar Marketing That Turns Quotes Into Installs",
}

GTAG = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=AW-18469638617"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'AW-18469638617');
</script>"""

FONT_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@800'
    '&family=Figtree:wght@400;500;600;700&display=swap" rel="stylesheet">\n'
    '<link rel="stylesheet" href="/styles.css" />'
)

HEADER = """<header class="site-header">
  <div class="wrap">
    <a class="logo" href="/">
      <img src="/logo.png" alt="DigiTradie logo" />
      <span>DigiTradie</span>
    </a>
    <nav>
      <a href="/#how">How it works</a>
      <a href="/#packages">Packages</a>
      <a href="/blog">Blog</a>
      <a href="/contact">Contact</a>
    </nav>
    {learn_dropdown}
    <a class="btn btn-primary btn-sm" href="/contact">Book a fit check</a>
  </div>
</header>"""

FOOTER = """<footer class="site-footer">
  <div class="wrap footer-nav">
    <a href="/">Home</a>
    <a href="/audit-optimise">Audit &amp; Optimise</a>
    <a href="/ads-setup">Dashboard + Ads Setup</a>
    <a href="/fractional-marketer">Fractional In-House Marketer</a>
    <a href="/blog">Blog</a>
    <a href="/learn">Learn</a>
    <a href="/contact">Contact</a>
  </div>
  <div class="wrap">
    <span>&copy; <span id="year"></span> DigiTradie</span>
    <span class="footer-contact">
      <a href="mailto:digitradieau@gmail.com">digitradieau@gmail.com</a>
      <a href="tel:0409025904">0409 025 904</a>
    </span>
  </div>
</footer>

<script>
  document.getElementById('year').textContent = new Date().getFullYear();
</script>"""


def headline_case(text):
    words = text.split(" ")
    out = []
    for i, w in enumerate(words):
        lw = w.lower()
        if i != 0 and lw in SMALL_WORDS:
            out.append(lw)
        else:
            out.append(lw[:1].upper() + lw[1:])
    return " ".join(out)


def industry_slug_and_label(h2_title):
    for pattern, slug, label in INDUSTRY_MAP:
        if re.search(pattern, h2_title, re.I):
            return slug, label
    # fallback for an industry not yet in INDUSTRY_MAP
    t = re.sub(r"^How to market an?\s+", "", h2_title.strip(), flags=re.I)
    t = re.sub(r"\s+(business|firm|practice|workshop|clinic)$", "", t, flags=re.I)
    slug = re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-") + "-marketing"
    return slug, headline_case(t)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def parse_docx(path):
    d = docx.Document(str(path))
    paras = [(p.style.name, p.text.strip()) for p in d.paragraphs if p.text.strip()]

    doc_date = None
    for style, text in paras[:3]:
        m = re.search(r"([A-Z][a-z]{2} \d{1,2}, \d{4})", text)
        if m:
            doc_date = datetime.strptime(m.group(1), "%b %d, %Y").strftime("%Y-%m-%d")
            break

    guides = []
    current = None
    section = None

    for style, text in paras:
        if style == "Heading 1":
            continue
        if style == "Heading 2":
            if text.strip().lower() == "tone of voice":
                current = None
                continue
            slug, label = industry_slug_and_label(text)
            current = {
                "title": HEADLINE_OVERRIDES.get(slug, headline_case(text)),
                "slug": slug,
                "label": label,
                "intro": None,
                "sections": [],
                "faqs": [],
            }
            guides.append(current)
            section = None
            continue
        if current is None:
            continue
        if style == "Heading 3":
            section = {"heading": text, "items": [], "is_faq": text.strip().lower() == "faqs"}
            if not section["is_faq"]:
                current["sections"].append(section)
            continue
        if section is None:
            if current["intro"] is None:
                current["intro"] = text
            else:
                current["intro"] += " " + text
            continue
        if section["is_faq"]:
            section["items"].append(text)
            continue
        kind = "task" if text.startswith("☐") else ("li" if style == "List Paragraph" else "p")
        clean = text.lstrip("☐").strip()
        section["items"].append({"kind": kind, "text": clean})

    # turn each FAQ section's flat Q/A list into pairs
    for g in guides:
        # re-scan to pick up faq items, since we didn't append faq sections above
        pass

    return guides, doc_date


def parse_docx_full(path):
    """Second pass that also captures FAQ pairs (kept separate from parse_docx
    for clarity; both walk the same paragraph list)."""
    d = docx.Document(str(path))
    paras = [(p.style.name, p.text.strip()) for p in d.paragraphs if p.text.strip()]
    guides, doc_date = parse_docx(path)

    gi = -1
    section_is_faq = False
    faq_buffer = []
    for style, text in paras:
        if style == "Heading 2":
            if text.strip().lower() == "tone of voice":
                gi = -1
                continue
            gi += 1
            section_is_faq = False
            continue
        if gi == -1:
            continue
        if style == "Heading 3":
            if faq_buffer and gi < len(guides):
                pass
            section_is_faq = text.strip().lower() == "faqs"
            faq_buffer = []
            continue
        if section_is_faq:
            faq_buffer.append(text)
            guides[gi]["faqs"] = []
            pairs = []
            for i in range(0, len(faq_buffer) - 1, 2):
                pairs.append({"q": faq_buffer[i], "a": faq_buffer[i + 1]})
            guides[gi]["faqs"] = pairs

    return guides, doc_date


def render_section(section):
    heading = f'      <h2>{esc(section["heading"])}</h2>\n'
    body = []
    items = section["items"]
    i = 0
    while i < len(items):
        item = items[i]
        if item["kind"] in ("li", "task"):
            cls = ' class="tasklist"' if item["kind"] == "task" else ""
            body.append(f"      <ul{cls}>\n")
            while i < len(items) and items[i]["kind"] == item["kind"]:
                body.append(f'        <li>{esc(items[i]["text"])}</li>\n')
                i += 1
            body.append("      </ul>\n")
        else:
            body.append(f'      <p>{esc(item["text"])}</p>\n')
            i += 1
    return heading + "".join(body)


def render_faqs(faqs):
    if not faqs:
        return ""
    items = "\n".join(
        f'''        <details class="faq-item">
          <summary>{esc(f["q"])}</summary>
          <p>{esc(f["a"])}</p>
        </details>'''
        for f in faqs
    )
    return f'''      <h2>FAQs</h2>
      <div class="faq-list">
{items}
      </div>
'''


def faq_ld(faqs):
    entities = [
        {"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}}
        for f in faqs
    ]
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities}


def learn_dropdown_html(all_guides):
    items = "\n".join(
        f'          <li><a href="/learn/{g["slug"]}">{esc(g["label"])}</a></li>' for g in all_guides
    )
    return f"""<details class="nav-dropdown">
      <summary>Market Your Industry <span aria-hidden="true">&#9662;</span></summary>
      <div class="nav-dropdown-panel">
        <p class="nav-dropdown-label">DIY Marketing For Your Industry</p>
        <ul class="nav-dropdown-menu">
{items}
          <li><a href="/learn" class="nav-dropdown-viewall">View all guides &rarr;</a></li>
        </ul>
      </div>
    </details>"""


def render_guide_page(guide, all_guides, doc_date):
    url = f"{SITE_URL}/learn/{guide['slug']}"
    title = f"{guide['title']} | DigiTradie"
    intro = guide["intro"] or ""
    meta_desc = intro[:155].rsplit(" ", 1)[0] + "…" if len(intro) > 155 else intro

    body_sections = "\n".join(render_section(s) for s in guide["sections"])
    faq_html = render_faqs(guide["faqs"])

    other_guides = [g for g in all_guides if g["slug"] != guide["slug"]][:3]
    related = "\n".join(
        f'''        <a class="blog-card" href="/learn/{g["slug"]}">
          <p class="blog-card-tag">DIY Guide</p>
          <h3>{esc(g["label"])}</h3>
          <p>{esc((g["intro"] or "")[:100])}…</p>
        </a>'''
        for g in other_guides
    )

    article_ld = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": guide["title"],
        "description": meta_desc,
        "author": {"@type": "Person", "name": "Kosta Diamantopoulos"},
        "publisher": {"@type": "Organization", "name": "DigiTradie", "logo": f"{SITE_URL}/logo.png"},
        "datePublished": doc_date or datetime.now().strftime("%Y-%m-%d"),
        "mainEntityOfPage": url,
    }
    breadcrumb_ld = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL + "/"},
            {"@type": "ListItem", "position": 2, "name": "Learn", "item": SITE_URL + "/learn"},
            {"@type": "ListItem", "position": 3, "name": guide["title"], "item": url},
        ],
    }

    ld_blocks = [article_ld, breadcrumb_ld]
    if guide["faqs"]:
        ld_blocks.append(faq_ld(guide["faqs"]))
    ld_scripts = "\n".join(
        f"<script type=\"application/ld+json\">\n{json.dumps(b, indent=2)}\n</script>" for b in ld_blocks
    )

    return f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
{GTAG}
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{esc(title)}</title>
<meta name="description" content="{esc(meta_desc)}" />
<link rel="canonical" href="{url}" />

<link rel="icon" type="image/png" href="/favicon.png" />
<link rel="apple-touch-icon" href="/apple-touch-icon.png" />
<meta name="theme-color" content="#C2410C" />

<meta property="og:type" content="article" />
<meta property="og:site_name" content="DigiTradie" />
<meta property="og:title" content="{esc(guide['title'])}" />
<meta property="og:description" content="{esc(meta_desc)}" />
<meta property="og:url" content="{url}" />
<meta property="og:image" content="{SITE_URL}/og-image.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />

<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{esc(guide['title'])}" />
<meta name="twitter:description" content="{esc(meta_desc)}" />
<meta name="twitter:image" content="{SITE_URL}/og-image.png" />

{FONT_LINK}

{ld_scripts}
</head>
<body>

{HEADER.format(learn_dropdown=learn_dropdown_html(all_guides))}

<main>
  <nav class="breadcrumb wrap" aria-label="Breadcrumb">
    <a href="/">Home</a> <span aria-hidden="true">/</span>
    <a href="/learn">Learn</a> <span aria-hidden="true">/</span>
    <span aria-current="page">{esc(guide['title'])}</span>
  </nav>

  <section class="article-meta">
    <div class="wrap article-wrap">
      <p class="eyebrow">DIY Guide</p>
      <h1>{esc(guide['title'])}</h1>
      <p class="lede">{esc(intro)}</p>
    </div>
  </section>

  <section class="article-body">
    <div class="wrap article-wrap">
{body_sections}
{faq_html}
    </div>
  </section>

  <section class="cta-band">
    <div class="wrap cta-band-inner">
      <h2>Want us to just handle this for you?</h2>
      <a class="btn btn-light" href="/contact">Book a fit check</a>
    </div>
  </section>

  <div class="wrap">
    <a class="back-to-blog" href="/learn">&larr; Back to all guides</a>
  </div>

  <section class="blog-related">
    <div class="wrap">
      <h2>More guides</h2>
      <div class="blog-grid">
{related}
      </div>
    </div>
  </section>
</main>

{FOOTER}

</body>
</html>
"""


def render_hub_page(all_guides):
    cards = "\n".join(
        f'''      <a class="blog-card" href="/learn/{g["slug"]}">
        <p class="blog-card-tag">DIY Guide</p>
        <h3>{esc(g["label"])}</h3>
        <p>{esc((g["intro"] or "")[:140])}{"…" if len(g["intro"] or "") > 140 else ""}</p>
      </a>'''
        for g in all_guides
    )
    url = f"{SITE_URL}/learn"
    title = "Learn: DIY Marketing For Your Industry | DigiTradie"
    desc = (
        "Straight-talking, industry-specific marketing guides for tradies and small business "
        "owners who want to run their own ads first."
    )

    return f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
{GTAG}
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}" />
<link rel="canonical" href="{url}" />

<link rel="icon" type="image/png" href="/favicon.png" />
<link rel="apple-touch-icon" href="/apple-touch-icon.png" />
<meta name="theme-color" content="#C2410C" />

<meta property="og:type" content="website" />
<meta property="og:site_name" content="DigiTradie" />
<meta property="og:title" content="{esc(title)}" />
<meta property="og:description" content="{esc(desc)}" />
<meta property="og:url" content="{url}" />
<meta property="og:image" content="{SITE_URL}/og-image.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />

<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{esc(title)}" />
<meta name="twitter:description" content="{esc(desc)}" />
<meta name="twitter:image" content="{SITE_URL}/og-image.png" />

{FONT_LINK}
</head>
<body>

{HEADER.format(learn_dropdown=learn_dropdown_html(all_guides))}

<main>
  <section class="blog-hero">
    <div class="wrap">
      <p class="eyebrow">Learn</p>
      <h1>DIY Marketing For Your Industry</h1>
      <p class="lede">
        Straight-talking guides for tradies and small business owners who want to run their own
        marketing first, and know when it's time to hand it to someone else.
      </p>
    </div>
  </section>

  <section>
    <div class="wrap blog-grid">
{cards}
    </div>
  </section>
</main>

{FOOTER}

</body>
</html>
"""


def merge_sitemap(all_guides):
    sitemap_path = REPO_ROOT / "sitemap.xml"
    text = sitemap_path.read_text()
    text = re.sub(
        r"\s*<url>\s*<loc>https://digitradie\.com/learn[^<]*</loc>.*?</url>",
        "",
        text,
        flags=re.S,
    )
    entries = [f'''  <url>
    <loc>{SITE_URL}/learn</loc>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>''']
    for g in all_guides:
        entries.append(f'''  <url>
    <loc>{SITE_URL}/learn/{g["slug"]}</loc>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>''')
    text = text.replace("</urlset>", "\n".join(entries) + "\n</urlset>")
    text = re.sub(r"\n{3,}", "\n\n", text)
    sitemap_path.write_text(text)


def main():
    if not DOCX_PATH.exists():
        sys.exit(f"Source doc not found: {DOCX_PATH}")

    guides, doc_date = parse_docx_full(DOCX_PATH)
    if not guides:
        sys.exit("No guides found in the doc — check the Heading 2 structure.")

    written = []
    learn_dir = REPO_ROOT / "learn"
    learn_dir.mkdir(exist_ok=True)

    hub_path = learn_dir / "index.html"
    hub_path.write_text(render_hub_page(guides))
    written.append(str(hub_path.relative_to(REPO_ROOT)))

    for g in guides:
        guide_dir = learn_dir / g["slug"]
        guide_dir.mkdir(exist_ok=True)
        page_path = guide_dir / "index.html"
        page_path.write_text(render_guide_page(g, guides, doc_date))
        written.append(str(page_path.relative_to(REPO_ROOT)))

    merge_sitemap(guides)
    written.append("sitemap.xml")

    print(f"Parsed {len(guides)} guides from the doc:")
    for g in guides:
        print(f"  - {g['title']}  ->  /learn/{g['slug']}  ({len(g['faqs'])} FAQs)")
    print(f"\nWrote {len(written)} files:")
    for w in written:
        print(f"  - {w}")


if __name__ == "__main__":
    main()
