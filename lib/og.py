"""Branded 1200x630 share images (/og/<name>.jpg), rendered with headless Chrome. Cached by content hash."""
import hashlib
import html as _html
import json
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

from .core import ROOT

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FONTS = ROOT / "assets" / "fonts"
LOGO = ROOT / "assets" / "img" / "logo-512.png"

TEMPLATE = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:B;src:url("file://%(fonts)s/bricolage-grotesque-latin.woff2");font-weight:500 800}
@font-face{font-family:F;src:url("file://%(fonts)s/figtree-latin.woff2");font-weight:400 800}
*{box-sizing:border-box;margin:0;padding:0}
body{width:1200px;height:630px;overflow:hidden;color:#fff;font-family:F,sans-serif;position:relative;background:#30405c}
.top{position:absolute;left:64px;right:64px;top:48px;display:flex;justify-content:space-between;align-items:center}
.brand{display:flex;align-items:center;gap:16px;font:800 34px B;letter-spacing:-.03em}
.brand img{width:64px;height:64px;border-radius:50%%;border:3px solid #fff}
.chip{font:800 18px F;letter-spacing:.14em;text-transform:uppercase;color:#16181d;background:#ec702e;padding:10px 18px;border-radius:4px;transform:rotate(-1.5deg)}
h1{position:absolute;left:64px;right:90px;top:170px;font:800 %(size)spx/1.04 B;letter-spacing:-.04em}
h1 em{font-style:normal;background:#ec702e;color:#16181d;padding:0 .12em;-webkit-box-decoration-break:clone;box-decoration-break:clone}
.sub{position:absolute;left:64px;right:140px;bottom:96px;font:600 27px/1.35 F;color:rgba(255,255,255,.9)}
.url{position:absolute;right:64px;bottom:92px;font:800 25px F;color:#ec702e}
.tape{position:absolute;left:0;right:0;bottom:0;height:22px;background:repeating-linear-gradient(-45deg,#ec702e 0 22px,#16181d 22px 44px)}
.edge{position:absolute;left:0;right:0;bottom:22px;height:4px;background:#16181d}
</style></head><body>
<div class="top"><div class="brand"><img src="file://%(logo)s">DigiTradie</div><div class="chip">%(chip)s</div></div>
<h1>%(headline)s</h1><p class="sub">%(sub)s</p><div class="url">digitradie.com</div><div class="edge"></div><div class="tape"></div></body></html>"""

CARDS = {
    "home": ("Fractional marketing", "We don&rsquo;t take <em>just any business.</em>", "Meta Ads, Google Ads, SEO and a dashboard you can read."),
    "services": ("Services", "Meta, Google and SEO, <em>run by one marketer.</em>", "Primarily Meta Ads and Google Ads, backed by SEO and website optimisation."),
    "google-ads": ("Google Ads", "Google Ads built around <em>enquiries, not clicks.</em>", "Search campaigns, conversion tracking and a plain-English dashboard."),
    "meta-ads": ("Meta Ads", "Meta Ads that turn <em>scrolling into enquiries.</em>", "Facebook and Instagram advertising built around the offer."),
    "seo-website-optimisation": ("SEO and website", "Be found on Google. <em>Then convert.</em>", "Google Business Profile, local SEO, speed and conversion fixes."),
    "audit-optimise": ("Audit &amp; Optimise", "Find out what your ads are <em>actually wasting.</em>", "A full audit of your Meta and Google Ads, with priority fixes applied."),
    "ads-setup": ("Dashboard + Ads Setup", "Ads built properly, <em>then handed to you.</em>", "Campaigns, tracking and a dashboard, plus coaching if you want it."),
    "fractional-marketer": ("Fractional marketer", "An in-house marketer, <em>without the in-house cost.</em>", "Ongoing optimisation and regular check-ins. Limited spots."),
    "about": ("About", "Meet Kosta. <em>He runs your account.</em>", "Fractional marketing for small and medium businesses across Australia."),
    "faq": ("FAQ", "Straight answers to <em>your questions.</em>", "Cost, contracts, the fit-check call and what working together looks like."),
    "contact": ("Free fit check", "Let&rsquo;s find out if <em>we&rsquo;re a fit.</em>", "One call. We&rsquo;ll tell you straight whether we can help."),
    "blog": ("Blog", "Marketing advice, <em>straight talking.</em>", "Leads, Google, AI and offers, from someone who has run the campaigns."),
    "learn": ("Free guides", "DIY marketing for <em>your industry.</em>", "Twelve straight-talking guides for owners who want to run it themselves."),
}


def _split_em(title):
    w = title.split()
    k = max(1, int(len(w) * 0.55))
    return " ".join(w[:k]) + " <em>" + " ".join(w[k:]) + "</em>"


def add_guides(guides):
    for g in guides:
        CARDS[f"learn-{g['slug']}"] = (f"DIY guide &middot; {_html.escape(g['label'])}", _split_em(_html.escape(g["title"])), "Free, straight-talking marketing guide from DigiTradie.")


def build_all():
    out = ROOT / "og"
    out.mkdir(exist_ok=True)
    cache_file = out / ".cache.json"
    cache = json.loads(cache_file.read_text()) if cache_file.exists() else {}
    made = 0
    for name, (chip, headline, sub) in CARDS.items():
        n = len(headline)
        size = 88 if n < 48 else 78 if n < 70 else 66 if n < 96 else 58
        html = TEMPLATE % dict(fonts=FONTS, logo=LOGO, chip=chip, headline=headline, sub=sub, size=size)
        key = hashlib.sha1(html.encode()).hexdigest()
        target = out / f"{name}.jpg"
        if cache.get(name) == key and target.exists():
            continue
        with tempfile.TemporaryDirectory() as td:
            h = Path(td) / "og.html"
            png = Path(td) / "og.png"
            h.write_text(html)
            subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1", "--window-size=1200,630",
                            "--virtual-time-budget=4000", f"--screenshot={png}", f"file://{h}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            Image.open(png).convert("RGB").save(target, "JPEG", quality=84, optimize=True, progressive=True)
        cache[name] = key
        made += 1
    cache_file.write_text(json.dumps(cache, indent=1))
    return made
