"""Shared building blocks for every page: constants, icons, <head>, header, footer, forms, page wrapper.

Everything the site repeats lives here so a change is made once and `python3 build.py` rolls it out.
"""
import hashlib
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://www.digitradie.com"  # the host Vercel actually serves (apex redirects here)
BRAND = "DigiTradie"
FOUNDER = "Kosta Diamantopoulos"
EMAIL = "digitradieau@gmail.com"
PHONE = "0409 025 904"
PHONE_TEL = "0409025904"
PHONE_INTL = "+61409025904"
FORMSPREE = "https://formspree.io/f/xeaokqng"
GA = "G-N0PS84JLP6"
AW = "AW-18469638617"
MODIFIED = "2026-10-30"  # bump when copy changes materially; used for dateModified + sitemap lastmod

# Optional: paste the Google Ads conversion label here (looks like AbC-D_efG-h12345) to fire an Ads
# conversion on /thank-you. Left empty on purpose until it is created in the Ads account.
ADS_CONVERSION_LABEL = ""

GUIDES = [  # slug, label (kept in sync with build.py's docx parser; used for nav + footer)
    ("hospitality-marketing", "Hospitality", "utensils"),
    ("tradie-marketing", "Tradies", "wrench"),
    ("retail-marketing", "Retail", "shopping-bag"),
    ("beauty-salon-marketing", "Beauty", "scissors"),
    ("gym-marketing", "Gyms", "dumbbell"),
    ("builder-marketing", "Builders", "hard-hat"),
    ("law-firm-marketing", "Law Firms", "scale"),
    ("dental-marketing", "Dental", "tooth"),
    ("accountant-marketing", "Accountants", "calculator"),
    ("physio-marketing", "Physio & Allied Health", "activity"),
    ("mechanic-marketing", "Mechanics", "car"),
    ("solar-marketing", "Solar", "sun"),
]

SERVICES = [
    ("google-ads", "Google Ads", "Capture people already searching for what you sell.", "search"),
    ("meta-ads", "Meta Ads", "Put your offer in front of the right people on Facebook and Instagram.", "megaphone"),
    ("seo-website-optimisation", "SEO & Website Optimisation", "Be found on Google and turn more visitors into enquiries.", "globe"),
]

PACKAGES = [
    ("audit-optimise", "Audit & Optimise", "Start here", "Already running ads? We find what is wasting money and fix it.", "Once-Over", "once-off",
     ["Full account audit", "Priority fixes applied", "Walkthrough of what changed"], "clipboard-check"),
    ("ads-setup", "Dashboard + Ads Setup", "Most popular", "Launching or starting over. Built properly, then handed to you.", "Growth", "once-off",
     ["Campaigns and tracking set up", "Set and forget handover", "The basics to manage it from your phone"], "rocket"),
    ("fractional-marketer", "Fractional In-House Marketer", "Limited spots", "Hands-on help without a full-time hire, week to week.", "Your DigiTradie", "monthly, ongoing",
     ["Ongoing optimisation", "Regular check-ins", "3-month minimum, then flexible"], "handshake"),
]

_ICON_DIR = ROOT / "lib" / "icons"
_icon_cache = {}


def esc(s):
    return html.escape(str(s), quote=True)


def icon(name, cls=""):
    """Inline a Lucide icon. Size comes from CSS (1em by default)."""
    if name not in _icon_cache:
        raw = (_ICON_DIR / f"{name}.svg").read_text()
        inner = re.sub(r"^.*?<svg[^>]*>|</svg>\s*$", "", raw, flags=re.S).strip()
        _icon_cache[name] = re.sub(r"\s+", " ", inner)
    c = f"i {cls}".strip()
    return (f'<svg class="{c}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{_icon_cache[name]}</svg>')


# ---------------------------------------------------------------- assets (hashed, cache forever)
def _hash(text):
    return hashlib.sha1(text.encode()).hexdigest()[:8]


def minify_css(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{};,>])\s*", r"\1", css)
    css = re.sub(r":\s+", ":", css)
    css = css.replace(";}", "}")
    return css.strip()


def _sparks_css():
    """A fixed, seeded field of tiny twinkling squares (cheap: one element + a box-shadow list)."""
    import random
    rnd = random.Random(23)
    cols = ["rgba(255,255,255,.85)", "rgba(201,184,255,.8)", "rgba(157,180,255,.8)", "rgba(255,154,77,.7)"]
    pts = []
    for _ in range(46):
        pts.append(f"{rnd.randint(10, 1500)}px {rnd.randint(8, 760)}px 0 {rnd.choice([0, 0, 1])}px {rnd.choice(cols)}")
    return ":root{--sparks:" + ",".join(pts) + "}"


def build_assets():
    """Writes assets/site.<hash>.css and .js; returns their public paths."""
    out = ROOT / "assets"
    for old in list(out.glob("site.*.css")) + list(out.glob("site.*.js")):
        old.unlink()
    css = minify_css(_sparks_css() + (ROOT / "src" / "site.css").read_text())
    js = (ROOT / "src" / "site.js").read_text()
    js = re.sub(r"^\s*//.*$", "", js, flags=re.M)
    js = re.sub(r"\n\s*\n+", "\n", js).strip()
    css_name, js_name = f"site.{_hash(css)}.css", f"site.{_hash(js)}.js"
    (out / css_name).write_text(css)
    (out / js_name).write_text(js)
    return f"/assets/{css_name}", f"/assets/{js_name}"


ASSET_CSS, ASSET_JS = "", ""


def init_assets():
    global ASSET_CSS, ASSET_JS
    ASSET_CSS, ASSET_JS = build_assets()


# ---------------------------------------------------------------- <head>
GTAG_LOADER = f"""<script>
window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}
gtag('js',new Date());gtag('config','{GA}');
var ad=/[?&](gclid|gbraid|wbraid)=/.test(location.search)||location.pathname==='/thank-you';
try{{if(/[?&](gclid|gbraid|wbraid)=/.test(location.search))sessionStorage.setItem('dt_ad','1');ad=ad||!!sessionStorage.getItem('dt_ad')}}catch(e){{}}
if(ad)gtag('config','{AW}');
(function(){{var d=0;function l(){{if(d)return;d=1;var s=document.createElement('script');s.async=1;s.src='https://www.googletagmanager.com/gtag/js?id={GA}';document.head.appendChild(s)}}
['pointerdown','keydown','scroll','touchstart'].forEach(function(e){{addEventListener(e,l,{{once:true,passive:true}})}});
window.dtLoadGtag=l;addEventListener('load',function(){{setTimeout(l,2500)}})}})();
</script>"""

PRELOAD_FONTS = (
    '<link rel="preload" href="/assets/fonts/bricolage-grotesque-latin.woff2" as="font" type="font/woff2" crossorigin>\n'
    '<link rel="preload" href="/assets/fonts/figtree-latin.woff2" as="font" type="font/woff2" crossorigin>'
)


def org_nodes():
    """Entity graph shared by every page (Organization/ProfessionalService, WebSite, founder)."""
    return [
        {
            "@type": ["Organization", "ProfessionalService"],
            "@id": f"{SITE}/#organization",
            "name": BRAND,
            "alternateName": "DigiTradie Fractional Marketing",
            "url": f"{SITE}/",
            "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/img/logo-512.png", "width": 512, "height": 512},
            "image": f"{SITE}/og/home.jpg",
            "description": ("DigiTradie is a fractional in-house marketing service for small and medium businesses in Australia: "
                            "Meta Ads, Google Ads, SEO and website optimisation, with a plain-English dashboard included."),
            "email": EMAIL,
            "telephone": PHONE_INTL,
            "areaServed": {"@type": "Country", "name": "Australia"},
            "founder": {"@id": f"{SITE}/#founder"},
            "knowsAbout": ["Google Ads", "Meta Ads", "Facebook advertising", "Instagram advertising",
                           "Search engine optimisation", "Website conversion optimisation", "Marketing dashboards"],
            "contactPoint": {"@type": "ContactPoint", "contactType": "sales", "email": EMAIL, "telephone": PHONE_INTL,
                             "areaServed": "AU", "availableLanguage": "English"},
            "makesOffer": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": p[1], "url": f"{SITE}/{p[0]}"}}
                for p in PACKAGES
            ],
        },
        {
            "@type": "WebSite",
            "@id": f"{SITE}/#website",
            "url": f"{SITE}/",
            "name": BRAND,
            "inLanguage": "en-AU",
            "publisher": {"@id": f"{SITE}/#organization"},
        },
        {
            "@type": "Person",
            "@id": f"{SITE}/#founder",
            "name": FOUNDER,
            "jobTitle": "Founder",
            "image": f"{SITE}/assets/img/kosta-600.webp",
            "url": f"{SITE}/about",
            "worksFor": {"@id": f"{SITE}/#organization"},
            "knowsAbout": ["Google Ads", "Meta Ads", "SEO", "Paid media strategy"],
        },
    ]


def breadcrumb_node(crumbs, url):
    return {
        "@type": "BreadcrumbList",
        "@id": url + "#breadcrumb",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, **({"item": SITE + p} if p else {})}
            for i, (n, p) in enumerate(crumbs)
        ],
    }


def faq_node(faqs, url):
    return {
        "@type": "FAQPage",
        "@id": url + "#faq",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}}
            for q, a in faqs
        ],
    }


def head(*, title, desc, path, og_image=None, og_type="website", nodes=None, robots="index,follow", page_type="WebPage",
         crumbs=None, modified=MODIFIED, published=None, preload_hero=None):
    url = SITE + (path if path != "/" else "/")
    og_image = og_image or f"{SITE}/og/home.jpg"
    graph = org_nodes()
    page = {
        "@type": page_type if isinstance(page_type, str) else page_type,
        "@id": url + "#webpage",
        "url": url,
        "name": title,
        "description": desc,
        "inLanguage": "en-AU",
        "isPartOf": {"@id": f"{SITE}/#website"},
        "about": {"@id": f"{SITE}/#organization"},
        "primaryImageOfPage": {"@type": "ImageObject", "url": og_image},
        "dateModified": modified,
    }
    if published:
        page["datePublished"] = published
    if crumbs:
        page["breadcrumb"] = {"@id": url + "#breadcrumb"}
        graph.append(breadcrumb_node(crumbs, url))
    graph.append(page)
    graph.extend(nodes or [])
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    pre = preload_hero or ""
    return f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="{robots},max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<meta name="theme-color" content="#f4f1ea">
<meta name="author" content="{FOUNDER}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="48x48" href="/favicon-48.png">
<link rel="icon" type="image/png" sizes="192x192" href="/icon-192.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="alternate" type="application/rss+xml" title="DigiTradie blog" href="/feed.xml">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:locale" content="en_AU">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(title)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{og_image}">
{PRELOAD_FONTS}
{pre}<link rel="stylesheet" href="{ASSET_CSS}">
<script>document.documentElement.className+=' js'</script>
{GTAG_LOADER}
<script type="application/ld+json">{ld}</script>
</head>
"""


# ---------------------------------------------------------------- header / footer
def _dd(label, items, extra=""):
    lis = "".join(f'<li><a href="{h}">{esc(t)}</a></li>' for h, t in items)
    return (f'<div class="dd"><button class="dd-btn" type="button" aria-expanded="false">{label}{icon("chevron-down", "dd-chev")}</button>'
            f'<div class="dd-panel"><ul>{lis}</ul>{extra}</div></div>')


def header(active=""):
    services = [("/services", "All services")] + [(f"/services/{s[0]}", s[1]) for s in SERVICES]
    packages = [(f"/{p[0]}", p[1]) for p in PACKAGES]
    guides_cols = "".join(f'<li><a href="/learn/{g[0]}">{icon(g[2])}{esc(g[1])}</a></li>' for g in GUIDES)
    mobile_guides = "".join(f'<a href="/learn/{g[0]}">{esc(g[1])}</a>' for g in GUIDES)
    mobile = f"""<div class="mmenu" id="mmenu" hidden>
  <div class="wrap">
    <p class="mm-h">Services</p>
    <div class="mm-links">{"".join(f'<a href="{h}">{esc(t)}</a>' for h, t in services)}</div>
    <p class="mm-h">Packages</p>
    <div class="mm-links">{"".join(f'<a href="{h}">{esc(t)}</a>' for h, t in packages)}</div>
    <p class="mm-h">Free DIY guides</p>
    <div class="mm-links mm-grid">{mobile_guides}<a href="/learn" class="mm-all">All guides &rarr;</a></div>
    <p class="mm-h">Company</p>
    <div class="mm-links"><a href="/about">About</a><a href="/blog">Blog</a><a href="/faq">FAQ</a><a href="/contact">Contact</a></div>
    <div class="mm-cta"><a class="btn btn-glow btn-block" href="/contact" data-cta="menu">Book a free fit check</a>
    <a class="mm-call" href="tel:{PHONE_TEL}" data-track="phone">{icon("phone")} {PHONE}</a></div>
  </div>
</div>"""
    return f"""<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap bar">
    <a class="brand" href="/" aria-label="DigiTradie home">
      <img src="/assets/img/logo-80.webp" srcset="/assets/img/logo-80.webp 1x, /assets/img/logo-160.webp 2x" width="40" height="40" alt="">
      <span>DigiTradie</span>
    </a>
    <nav class="nav" aria-label="Main">
      {_dd("Services", services)}
      {_dd("Packages", packages)}
      <div class="dd"><button class="dd-btn" type="button" aria-expanded="false">Guides{icon("chevron-down", "dd-chev")}</button>
        <div class="dd-panel dd-wide"><p class="dd-label">Free DIY marketing guides by industry</p><ul class="dd-cols">{guides_cols}</ul>
        <a class="dd-all" href="/learn">View all guides &rarr;</a></div></div>
      <a href="/blog">Blog</a>
      <a href="/about">About</a>
    </nav>
    <div class="bar-end">
      <a class="btn btn-primary btn-sm" href="/contact" data-cta="header">Book a fit check</a>
      <button class="menu-btn" type="button" aria-expanded="false" aria-controls="mmenu" aria-label="Open menu">{icon("menu", "mb-open")}{icon("x", "mb-close")}</button>
    </div>
  </div>
  {mobile}
</header>
"""


def footer():
    svc = "".join(f'<li><a href="/services/{s[0]}">{esc(s[1])}</a></li>' for s in SERVICES)
    pk = "".join(f'<li><a href="/{p[0]}">{esc(p[1])}</a></li>' for p in PACKAGES)
    gd = "".join(f'<li><a href="/learn/{g[0]}">{esc(g[1])}</a></li>' for g in GUIDES)
    return f"""<footer class="site-footer">
  <div class="tape" aria-hidden="true"></div>
  <div class="wrap foot-grid">
    <div class="foot-brand">
      <a class="brand" href="/"><img src="/assets/img/logo-80.webp" srcset="/assets/img/logo-80.webp 1x, /assets/img/logo-160.webp 2x" width="44" height="44" alt="" loading="lazy"><span>DigiTradie</span></a>
      <p>Fractional in-house marketing for small and medium businesses across Australia. Meta Ads, Google Ads, SEO and website optimisation, with a dashboard you can read.</p>
      <p class="foot-contact"><a href="mailto:{EMAIL}" data-track="email">{icon("mail")}{EMAIL}</a><a href="tel:{PHONE_TEL}" data-track="phone">{icon("phone")}{PHONE}</a></p>
      <a class="btn btn-glow" href="/contact" data-cta="footer">Book a free fit check</a>
    </div>
    <div><h2>Services</h2><ul>{svc}<li><a href="/services">All services</a></li></ul>
      <h2>Packages</h2><ul>{pk}</ul></div>
    <div><h2>Free guides</h2><ul class="two">{gd}</ul><ul><li><a href="/learn">All guides</a></li></ul></div>
    <div><h2>Company</h2><ul><li><a href="/about">About Kosta</a></li><li><a href="/blog">Blog</a></li><li><a href="/blog/renovation-leads-case-study">Case study</a></li><li><a href="/faq">FAQ</a></li><li><a href="/contact">Contact</a></li><li><a href="/privacy">Privacy</a></li></ul></div>
  </div>
  <div class="wrap foot-base">
    <span>&copy; <span id="year">2026</span> DigiTradie. Australia.</span>
    <span class="credit">Tool illustrations by Lorc, Delapouite and others via <a href="https://game-icons.net" rel="noopener">game-icons.net</a> (CC BY 3.0). UI icons by <a href="https://lucide.dev" rel="noopener">Lucide</a>.</span>
  </div>
</footer>
<div class="sticky-cta" id="stickycta">
  <a class="btn btn-glow" href="/contact" data-cta="sticky">Book a free fit check</a>
  <a class="sc-call" href="tel:{PHONE_TEL}" aria-label="Call DigiTradie" data-track="phone">{icon("phone")}</a>
</div>
<script src="{ASSET_JS}" defer></script>
</body>
</html>
"""


# ---------------------------------------------------------------- the lead form (used everywhere)
def form(fid, *, source, heading="Book a free fit check", sub="One call, usually 15 to 20 minutes. We'll tell you straight whether we can help.",
         need="launch", dark=False, compact=False):
    pills = [("launch", "Launch ads", "rocket"), ("learn", "Learn ads", "graduation-cap"), ("optimise", "Optimise ads", "gauge")]
    pill_html = "".join(
        f'<label class="pill"><input type="radio" name="need" value="{v}"{" checked" if v == need else ""}>'
        f'<span>{icon(ic)}{t}</span></label>'
        for v, t, ic in pills
    )
    head_tag = "h2" if not compact else "h3"
    return f"""<div class="fitcard{' fitcard-dark' if dark else ''}{' fitcard-compact' if compact else ''}" id="{fid}-card">
  <div class="fitcard-head">
    <{head_tag} class="fitcard-title">{esc(heading)}</{head_tag}>
    <p>{esc(sub)}</p>
    <div class="steps-dots" aria-hidden="true"><span class="on"></span><span></span><em>Step <b data-stepnum>1</b> of 2</em></div>
  </div>
  <form class="fitform" id="{fid}" action="{FORMSPREE}" method="POST" data-form="{esc(source)}">
    <input type="hidden" name="_next" value="{SITE}/thank-you">
    <input type="hidden" name="_subject" value="New DigiTradie fit check request">
    <input type="hidden" name="page" value="{esc(source)}">
    <input type="hidden" name="utm_source" value=""><input type="hidden" name="utm_medium" value=""><input type="hidden" name="utm_campaign" value="">
    <input type="hidden" name="utm_term" value=""><input type="hidden" name="gclid" value=""><input type="hidden" name="landing_page" value=""><input type="hidden" name="referrer" value="">
    <input class="hp" type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true">
    <div class="fstep" data-step="1">
      <fieldset class="needs"><legend>What do you need?</legend><div class="pills">{pill_html}</div></fieldset>
      <label class="field"><span>Current monthly ad spend</span>
        <select name="spend"><option>Not running ads yet</option><option>Under $1k</option><option>$1k&ndash;$5k</option><option>Over $5k</option></select></label>
      <button type="button" class="btn btn-primary btn-block btn-next" data-next>Continue {icon("arrow-right")}</button>
    </div>
    <div class="fstep" data-step="2">
      <div class="two-col">
        <label class="field"><span>Your name</span><input type="text" name="name" autocomplete="name" required></label>
        <label class="field"><span>Business name</span><input type="text" name="business" autocomplete="organization" required></label>
      </div>
      <div class="two-col">
        <label class="field"><span>Email</span><input type="email" name="email" autocomplete="email" required></label>
        <label class="field"><span>Phone</span><input type="tel" name="phone" autocomplete="tel" required></label>
      </div>
      <button type="submit" class="btn btn-primary btn-block btn-submit">Check if we&rsquo;re a fit {icon("arrow-right")}</button>
      <button type="button" class="back-link" data-back>&larr; Back</button>
    </div>
    <p class="fine">{icon("shield-check")} No obligation. No lock-in contracts. We only use your details to reply.</p>
  </form>
</div>"""


# ---------------------------------------------------------------- page wrapper
def write_page(path, html_head, body, *, crumbs=None):
    """path like '/services/google-ads' or '/'. Writes <path>/index.html."""
    out = ROOT / path.strip("/") / "index.html" if path != "/" else ROOT / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html_head + body)
    return out


REGISTRY = []  # (path, priority, changefreq, lastmod) for sitemap.xml


def _prio(path):
    if path == "/":
        return "1.0", "weekly"
    if path in ("/services", "/audit-optimise", "/ads-setup", "/fractional-marketer", "/contact"):
        return "0.9", "monthly"
    if path.startswith("/services/"):
        return "0.9", "monthly"
    if path in ("/about", "/blog", "/learn"):
        return "0.8", "weekly" if path != "/about" else "monthly"
    if path == "/privacy":
        return "0.2", "yearly"
    return "0.7", "monthly"


def page(path, *, title, desc, main, nodes=None, crumbs=None, og_image=None, robots="index,follow", og_type="website",
         page_type="WebPage", modified=MODIFIED, published=None, nav=""):
    if og_image is None:
        from . import og as _og
        name = (path.strip("/").split("/")[-1] or "home")
        if name in _og.CARDS:
            og_image = f"{SITE}/og/{name}.jpg"
    h = head(title=title, desc=desc, path=path, og_image=og_image, og_type=og_type, nodes=nodes, robots=robots,
             page_type=page_type, crumbs=crumbs, modified=modified, published=published)
    body = header(nav) + f'<main id="main">\n{main}\n</main>\n' + footer()
    if robots.startswith("index"):
        pr, fr = _prio(path)
        REGISTRY.append((path, pr, fr, modified))
    return write_page(path, h, body)
