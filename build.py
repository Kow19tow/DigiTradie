#!/usr/bin/env python3
"""
Rebuilds the whole digitradie.com website. One command:

    python3 build.py

What it builds (all output is plain static files that Vercel serves):
  - every page: home, services, packages, about, faq, contact, thank-you, privacy, 404
  - /blog  (posts live in content/blog/*.html + content/blog/posts.json)
  - /learn (guides come from content/learn/DigiTradie Industry Guides.docx, the single source of truth)
  - assets/site.<hash>.css and .js (from src/), share images in /og, sitemap.xml, robots.txt,
    llms.txt, llms-full.txt, feed.xml, vercel.json, .vercelignore

To update copy:
  - Learn guides: edit the .docx, run `python3 build.py`.
  - Blog posts: edit content/blog/<slug>.html, run `python3 build.py`.
  - Design: edit src/site.css or src/site.js, run `python3 build.py`.
  - Shared parts (header, footer, form, schema): lib/core.py and lib/components.py.
Then check `git status`, commit and push. Vercel deploys from main.

Doc structure the guides parser expects, per industry:
  Heading 2 "How to market a <industry>"  - starts a guide
    Normal                                - intro paragraph (lede + meta description)
    Heading 3 <section>                   - a subsection (varies per guide)
      Normal / List Paragraph             - body text or bullets. Lines starting with the tick-box
                                             character become a task list.
    Heading 3 "FAQs"                      - alternating Normal paragraphs: question, answer, ...
  Heading 2 "Tone of voice" is internal writing guidance and is never published.

Requires: pip3 install --user python-docx pillow   (and Google Chrome, used to draw the share images)
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    import docx
except ImportError:
    sys.exit("Missing dependency. Run: pip3 install --user python-docx pillow")

REPO_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO_ROOT))
DOCX_PATH = REPO_ROOT / "content" / "learn" / "DigiTradie Industry Guides.docx"


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

# Optional per-guide image (hero + og:image + schema image), keyed by slug.

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




def tidy(text):
    """House style: no em dashes. Spaced dashes become commas (the doc is never edited)."""
    return re.sub(r"\s+[\u2014\u2013]\s+", ", ", text).replace("\u2014", ", ")


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



def main():
    from lib import core, og, pages_content, pages_home, pages_main, seo_files

    if not DOCX_PATH.exists():
        sys.exit(f"Source doc not found: {DOCX_PATH}")
    guides, doc_date = parse_docx_full(DOCX_PATH)
    if not guides:
        sys.exit("No guides found in the doc: check the Heading 2 structure.")
    for g in guides:  # house style pass (no em dashes) without touching the source doc
        g["title"] = tidy(g["title"])
        g["intro"] = tidy(g["intro"] or "")
        for s in g["sections"]:
            s["heading"] = tidy(s["heading"])
            for it in s["items"]:
                it["text"] = tidy(it["text"])
        for f in g["faqs"]:
            f["q"], f["a"] = tidy(f["q"]), tidy(f["a"])

    core.init_assets()
    pages_home.build_home()
    pages_main.build_services_hub()
    pages_main.build_services()
    pages_main.build_packages()
    pages_main.build_about()
    pages_main.build_faq()
    pages_main.build_contact()
    pages_main.build_thanks()
    pages_main.build_privacy()
    pages_main.build_404()
    pages_content.build_blog()
    pages_content.build_learn(guides, doc_date)

    posts = json.loads((REPO_ROOT / "content" / "blog" / "posts.json").read_text())
    og.add_guides(guides)
    made = og.build_all()
    seo_files.write_sitemap()
    seo_files.write_robots()
    seo_files.write_llms(guides, posts)
    seo_files.write_feed(posts)
    seo_files.write_hosting()

    print(f"Built {len(core.REGISTRY)} indexable pages, {len(guides)} guides, {len(posts)} blog posts, {made} new share images.")
    print(f"CSS {core.ASSET_CSS}  JS {core.ASSET_JS}")


if __name__ == "__main__":
    main()
