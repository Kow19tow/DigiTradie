"""Blog and Learn (docx-driven guides): article layout, indexes, related links."""
import json
import re

from . import components as c
from .core import FOUNDER, GUIDES, MODIFIED, ROOT, SITE, esc, faq_node, icon, page

BLOG_ALT = {
    "renovation-leads-case-study": "Case study graphic: $500 ad spend to $75K profit for a Melbourne renovation business, with the line The right offer beats a discount. Every time.",
    "google-for-tradies": "Example Google review reading Thanks for unblocking our drain in Reservoir, highlighting what the business does and where it does it.",
    "tradies-and-ai": "Graphic titled No callbots. Ever. showing what tradies should let AI handle and what to keep human.",
}


def _nice(iso):
    from datetime import datetime
    d = datetime.fromisoformat(iso)
    return f"{d.day} {d.strftime('%b %Y')}"


def slugify(t):
    return re.sub(r"[^a-z0-9]+", "-", re.sub(r"<[^>]+>", "", t).lower()).strip("-")


def add_ids_and_toc(body_html):
    """Gives every <h2> an id and returns (html, toc_html)."""
    items = []

    def repl(m):
        text = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        i = slugify(text)
        items.append((i, text))
        return f'<h2 id="{i}"{m.group(1)}>{m.group(2)}</h2>'

    out = re.sub(r"<h2([^>]*)>(.*?)</h2>", repl, body_html, flags=re.S)
    toc = ""
    if len(items) >= 3:
        lis = "".join(f'<li><a href="#{i}">{esc(t)}</a></li>' for i, t in items)
        toc = f'<nav class="toc" aria-label="On this page"><h2>On this page</h2><ol>{lis}</ol></nav>'
    return out, toc


def seo_title(h1, fallback=None):
    """Keeps <title> inside what search results show (about 60 characters)."""
    if len(h1) + 13 <= 63:
        return f"{h1} | DigiTradie"
    if len(h1) <= 63:
        return h1
    return fallback or h1[:60].rsplit(" ", 1)[0]


def author_box():
    return f"""<aside class="author-box"><img src="/assets/img/kosta-160.webp" width="72" height="72" loading="lazy" alt="{FOUNDER}">
<p><b>{FOUNDER}</b>Founder of DigiTradie. Runs Meta Ads, Google Ads, SEO and website optimisation for small and medium businesses across Australia, and has managed $100k+ monthly ad budgets on international accounts. <a href="/about">About Kosta</a></p></aside>"""


def article_page(*, path, kind, tag, title, h1, desc, lede, body_html, date, image=None, image_alt="", faqs=None, related=None, cta_text, og=None, modified=MODIFIED):
    url = SITE + path
    body_html, toc = add_ids_and_toc(body_html)
    words = len(re.sub(r"<[^>]+>", " ", body_html).split())
    mins = max(1, -(-words // 200))
    hero_img = (f'<img class="article-hero-img" src="{image}" width="1200" height="630" alt="{esc(image_alt)}">' if image else "")
    faq_html = ""
    if faqs:
        items = "".join(f'<details class="faq"><summary><span>{esc(q)}</span>{icon("chevron-down")}</summary><div class="faq-a"><p>{esc(a)}</p></div></details>' for q, a in faqs)
        faq_html = f'<h2 id="faqs">FAQs</h2><div class="faq-list">{items}</div>'
        if toc:
            toc = toc.replace("</ol>", '<li><a href="#faqs">FAQs</a></li></ol>')
    listing = ("Blog", "/blog") if kind == "blog" else ("Learn", "/learn")
    byline = (f'<div class="byline"><img src="/assets/img/kosta-160.webp" width="46" height="46" alt="{FOUNDER}"><span>{FOUNDER} &middot; DigiTradie Founder'
              f'<small>{mins} min read &middot; Updated {_nice(modified)}</small></span></div>')
    hero = c.page_hero(eyebrow=tag, h1=esc(h1), lede=esc(lede) if lede else "", crumbs=[("Home", "/"), listing, (h1, None)], actions=byline)
    related_html = c.related_cards(related, heading="Keep reading") if related else ""
    main = f"""{hero}
<section class="section" style="padding-top:0"><div class="wrap article-grid">
  {toc or "<div></div>"}
  <article class="prose">{hero_img}{body_html}{faq_html}{author_box()}</article>
</div></section>
{related_html}
{c.cta_band(heading=esc(cta_text), sub="One call. We&rsquo;ll tell you straight whether we can help.", fid=f"{kind}-cta-form", source=f"{kind}-{path.split('/')[-1]}")}"""
    article = {
        "@type": "Article", "@id": url + "#article", "headline": h1, "description": desc, "wordCount": words,
        "author": {"@id": f"{SITE}/#founder"}, "publisher": {"@id": f"{SITE}/#organization"},
        "datePublished": date, "dateModified": modified, "mainEntityOfPage": {"@id": url + "#webpage"},
        "image": image and (SITE + image if image.startswith("/") else image) or (og or f"{SITE}/og/home.jpg"),
        "articleSection": tag, "inLanguage": "en-AU",
    }
    nodes = [article] + ([faq_node(faqs, url)] if faqs else [])
    page(path, title=title, desc=desc, main=main, crumbs=[("Home", "/"), listing, (h1, path)], nodes=nodes, og_type="article",
         og_image=og or (SITE + image if image else None), published=date, modified=modified)


# ------------------------------------------------------------------ blog
def build_blog():
    posts = json.loads((ROOT / "content" / "blog" / "posts.json").read_text())
    for p in posts:
        body = (ROOT / "content" / "blog" / f"{p['slug']}.html").read_text()
        lede = ""
        related = [(f"/blog/{o['slug']}", o["tag"], o["h1"], o["desc"]) for o in posts if o["slug"] != p["slug"]]
        related.append(("/services/google-ads" if p["slug"] != "google-for-tradies" else "/services/seo-website-optimisation",
                        "Service", "Google Ads for small business" if p["slug"] != "google-for-tradies" else "SEO and website optimisation",
                        "How we run it, what to expect, and who it suits."))
        article_page(path=f"/blog/{p['slug']}", kind="blog", tag=p["tag"], title=p.get("seo_title") or seo_title(p["h1"]), h1=p["h1"], desc=p["desc"], lede=lede,
                     body_html=body, date=p["date"], image=p["image"], image_alt=BLOG_ALT[p["slug"]], related=related[:3], cta_text=p["cta"],
                     og=SITE + p["image"])
    cards = "".join(
        f'<a class="rcard reveal" href="/blog/{p["slug"]}"><img class="rcard-img" src="{p["image"]}" width="1200" height="630" loading="lazy" alt="{esc(BLOG_ALT[p["slug"]])}">'
        f'<span class="rtag">{esc(p["tag"])}</span><h3>{esc(p["h1"])}</h3><p>{esc(p["desc"])}</p><span class="go">Read {icon("arrow-right")}</span></a>'
        for p in posts)
    itemlist = {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{SITE}/blog/{p['slug']}", "name": p["h1"]} for i, p in enumerate(posts)]}
    main = "\n".join([
        c.page_hero(eyebrow="DigiTradie blog", h1="Straight-talking marketing advice <em>for small business.</em>",
                    lede="Leads, Google, AI and offers, from someone who has run the campaigns, not just talked about them.", crumbs=[("Home", "/"), ("Blog", None)]),
        f'<section class="section"><div class="wrap"><h2 class="sr-only">Latest articles</h2><div class="rgrid">{cards}</div></div></section>',
        c.guides_grid(limit=12, heading="Looking for a guide for your industry?"),
        c.cta_band(),
    ])
    page("/blog", title="Marketing Advice for Small Business | DigiTradie Blog", desc="Straight-talking marketing advice for small business: leads, Google, AI and offers, from someone who has actually run the campaigns.",
         main=main, crumbs=[("Home", "/"), ("Blog", "/blog")], nodes=[itemlist], page_type="CollectionPage")


# ------------------------------------------------------------------ learn
def render_section(section):
    out = [f"<h2>{esc(section['heading'])}</h2>"]
    items = section["items"]
    i = 0
    while i < len(items):
        it = items[i]
        if it["kind"] in ("li", "task"):
            cls = ' class="tasklist"' if it["kind"] == "task" else ""
            out.append(f"<ul{cls}>")
            while i < len(items) and items[i]["kind"] == it["kind"]:
                out.append(f"<li>{esc(items[i]['text'])}</li>")
                i += 1
            out.append("</ul>")
        else:
            out.append(f"<p>{esc(it['text'])}</p>")
            i += 1
    return "\n".join(out)


GUIDE_IMAGES = {
    "tradie-marketing": ("/images/urgent-vs-considered-1200x630.jpg",
                         "Urgency decides the channel: urgent tradie jobs go Google first, considered jobs go social first. DigiTradie DIY guide."),
}


def build_learn(guides, doc_date):
    modified = MODIFIED
    icon_for = {g[0]: g[2] for g in GUIDES}
    for g in guides:
        img, alt = GUIDE_IMAGES.get(g["slug"], (None, ""))
        body = "\n".join(render_section(s) for s in g["sections"])
        intro = g["intro"] or ""
        desc = intro if len(intro) <= 155 else intro[:155].rsplit(" ", 1)[0] + "…"
        others = [o for o in guides if o["slug"] != g["slug"]]
        # nearby guides first for variety; always 3
        idx = guides.index(g)
        rel = [guides[(idx + k) % len(guides)] for k in (1, 2, 3)]
        related = [(f"/learn/{o['slug']}", "DIY guide", o["title"], (o["intro"] or "")[:110].rsplit(" ", 1)[0] + "…") for o in rel]
        article_page(path=f"/learn/{g['slug']}", kind="learn", tag=f"DIY guide: {g['label']}", title=seo_title(g["title"], f"{g['label']} Marketing Guide for Small Business | DigiTradie"), h1=g["title"], desc=desc, lede=intro,
                     body_html=body, date=doc_date or MODIFIED, image=img, image_alt=alt, faqs=[(f["q"], f["a"]) for f in g["faqs"]] or None, related=related,
                     cta_text="Want us to just handle this for you?", og=f"{SITE}/og/learn-{g['slug']}.jpg" if not img else SITE + img, modified=modified)
    tiles = "".join(
        f'<a class="rcard reveal" href="/learn/{g["slug"]}"><span class="gic" style="margin-bottom:14px">{icon(icon_for.get(g["slug"], "file-text"))}</span><span class="rtag">DIY guide</span>'
        f'<h3>{esc(g["label"])}</h3><p>{esc((g["intro"] or "")[:150].rsplit(" ", 1)[0])}…</p><span class="go">Read the guide {icon("arrow-right")}</span></a>'
        for g in guides)
    itemlist = {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{SITE}/learn/{g['slug']}", "name": g["title"]} for i, g in enumerate(guides)]}
    main = "\n".join([
        c.page_hero(eyebrow="Learn", h1="DIY marketing for <em>your industry.</em>",
                    lede="Straight-talking guides for tradies and small business owners who want to run their own marketing first, and know when it is time to hand it to someone else.",
                    crumbs=[("Home", "/"), ("Learn", None)]),
        f'<section class="section"><div class="wrap"><h2 class="sr-only">All industry guides</h2><div class="rgrid">{tiles}</div></div></section>',
        c.cta_band(heading="Rather have us run it?", sub="One call. We&rsquo;ll tell you straight whether we can help, and which package fits."),
    ])
    page("/learn", title="Free DIY Marketing Guides for Your Industry | DigiTradie", desc="Straight-talking, industry-specific marketing guides for tradies and small business owners who want to run their own ads and marketing first.",
         main=main, crumbs=[("Home", "/"), ("Learn", "/learn")], nodes=[itemlist], page_type="CollectionPage")
