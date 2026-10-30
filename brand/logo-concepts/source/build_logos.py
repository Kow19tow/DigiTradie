#!/usr/bin/env python3
"""Generates the DigiTradie logo concepts: contact sheet, per-concept PNGs (icon + dark/light lockups, transparent)
and standalone SVGs for the pure-vector icons.

Run:  python3 brand/logo-concepts/source/build_logos.py
Needs Google Chrome and pillow. Fonts load from Google Fonts (Bricolage Grotesque)."""
import math, subprocess, shutil
from pathlib import Path
from PIL import Image

OUT = Path(__file__).resolve().parent.parent
TMP = OUT / "source" / "_tmp"
TMP.mkdir(exist_ok=True)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

OR, OR2, OR3 = "#EC702E", "#FF9A4D", "#E4571F"
NAVY, INK, PERI, LILAC = "#30405C", "#1a0b2e", "#7289ff", "#c9b8ff"
FONT_IMPORT = "@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&display=swap');"


# ---------- helpers ----------
def grad_bg(n, shape="sq"):
    defs = (f'<defs><linearGradient id="bg{n}" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="#1a0b4f"/><stop offset=".55" stop-color="#21219a"/><stop offset="1" stop-color="#2559d8"/></linearGradient>'
            f'<linearGradient id="og{n}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{OR2}"/><stop offset="1" stop-color="{OR3}"/></linearGradient></defs>')
    shp = f'<rect width="200" height="200" rx="46" fill="url(#bg{n})"/>' if shape == "sq" else f'<circle cx="100" cy="100" r="100" fill="url(#bg{n})"/>'
    return defs + shp


def navy_bg(n, shape="circle"):
    defs = f'<defs><linearGradient id="og{n}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{OR2}"/><stop offset="1" stop-color="{OR3}"/></linearGradient></defs>'
    shp = f'<circle cx="100" cy="100" r="100" fill="{NAVY}"/>' if shape == "circle" else f'<rect width="200" height="200" rx="46" fill="{NAVY}"/>'
    return defs + shp


def cells(rows, size, gap, ox, oy, colors, rx=5):
    out = []
    for r, row in enumerate(rows):
        for c, v in enumerate(row):
            if v:
                col = colors(r, c, v) if callable(colors) else colors
                out.append(f'<rect x="{ox + c * (size + gap)}" y="{oy + r * (size + gap)}" width="{size}" height="{size}" rx="{rx}" fill="{col}"/>')
    return "".join(out)


def swoosh(cx, cy, r, w, center, span, fill, n=60, power=.8):
    po, pi_ = [], []
    for i in range(n + 1):
        t = i / n
        a = math.radians(center - span / 2 + t * span)
        th = w * (math.sin(math.pi * t) ** power)
        po.append((cx + (r + th / 2) * math.cos(a), cy + (r + th / 2) * math.sin(a)))
        pi_.append((cx + (r - th / 2) * math.cos(a), cy + (r - th / 2) * math.sin(a)))
    pts = po + pi_[::-1]
    return '<path d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f'Z" fill="{fill}"/>'


def spark(x, y, r, fill="#fff"):
    t = r / 3.2
    return f'<rect x="{x - t / 2}" y="{y - r}" width="{t}" height="{r * 2}" fill="{fill}"/><rect x="{x - r}" y="{y - t / 2}" width="{r * 2}" height="{t}" fill="{fill}"/>'


# ---------- concepts: each returns inner SVG for a 200x200 icon ----------
def c01(n):  # Block D: solid pixel D, white stem, orange bowl
    rows = ["111100", "111110", "110011", "110011", "110011", "111110", "111100"]
    rows = [[int(ch) for ch in r] for r in rows]
    col = lambda r, c, v: "#fff" if c <= 1 else f"url(#og{n})"
    return grad_bg(n) + cells(rows, 20, 4, 30, 18, col, rx=4)


def c02(n):  # Growth bars
    s = grad_bg(n)
    hs = [30, 58, 90, 126, 160]
    for i, h in enumerate(hs):
        x = 20 + i * 34
        segs = (h + 5) // 19
        for k in range(segs):
            y = 178 - (k + 1) * 14 - k * 5
            fill = f"url(#og{n})" if i == 4 else (LILAC if i < 2 else PERI if i == 2 else "#9db4ff")
            op = "1" if i == 4 else str(.55 + i * .1)
            s += f'<rect x="{x}" y="{y}" width="24" height="14" rx="4" fill="{fill}" opacity="{op}"/>'
    return s


def c03(n):  # Roof arrow
    return (navy_bg(n) +
            f'<rect x="87" y="76" width="26" height="92" fill="#fff"/>'
            f'<polyline points="42,106 100,48 158,106" fill="none" stroke="url(#og{n})" stroke-width="26" stroke-linejoin="miter" stroke-miterlimit="10"/>')


def c04(n):  # Hard hat
    return (navy_bg(n) +
            f'<path d="M34 128 A66 66 0 0 1 166 128 Z" fill="url(#og{n})"/>'
            f'<rect x="88" y="62" width="24" height="66" fill="{OR3}"/>'
            f'<rect x="20" y="126" width="160" height="24" rx="12" fill="{OR2}"/>' + spark(152, 46, 11))


def c05(n):  # Swirl refresh (modernised current mark)
    s = grad_bg(n, "circle")
    s += swoosh(100, 100, 80, 24, -60, 165, OR) + swoosh(100, 100, 80, 24, 120, 165, OR)
    s += swoosh(100, 100, 62, 14, 20, 135, "#fff") + swoosh(100, 100, 62, 14, 200, 135, "#fff")
    s += (f'<text x="100" y="95" text-anchor="middle" font-family="Bricolage Grotesque" font-weight="500" font-size="21" fill="#fff">DIGI</text>'
          f'<text x="100" y="119" text-anchor="middle" font-family="Bricolage Grotesque" font-weight="800" font-size="25" fill="{OR2}">TRADIE</text>')
    return s


def c06(n):  # DT monogram
    return (grad_bg(n) +
            '<path fill-rule="evenodd" fill="#fff" d="M38 36 H100 A64 64 0 0 1 100 164 H38 Z M66 64 H100 A36 36 0 0 1 100 136 H66 Z"/>'
            f'<rect x="80" y="80" width="44" height="14" fill="{OR2}"/><rect x="95" y="94" width="14" height="30" fill="{OR2}"/>')


def c07(n):  # Tape roundel
    return (f'<defs><clipPath id="cl{n}"><circle cx="100" cy="100" r="100"/></clipPath>'
            f'<pattern id="hz{n}" width="16" height="16" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="8" height="16" fill="{OR}"/><rect x="8" width="8" height="16" fill="{INK}"/></pattern></defs>'
            f'<g clip-path="url(#cl{n})"><rect width="200" height="200" fill="{NAVY}"/>'
            f'<g transform="rotate(-26 100 100)"><rect x="-40" y="58" width="280" height="14" fill="url(#hz{n})"/>'
            f'<rect x="-40" y="72" width="280" height="56" fill="{OR}"/><rect x="-40" y="128" width="280" height="14" fill="url(#hz{n})"/>'
            f'<text x="100" y="110" text-anchor="middle" font-family="Bricolage Grotesque" font-weight="800" font-size="27" letter-spacing="1" fill="{INK}">DIGITRADIE</text></g></g>')


def c08(n):  # Pixel spark: 4-point sparkle, arms fade out
    N = 9
    size, gap = 14, 3
    ox = (200 - (N * size + (N - 1) * gap)) / 2
    out = grad_bg(n)
    on = set()
    for k in range(N):
        on.add((4, k)); on.add((k, 4))
    for r, c in [(3, 3), (3, 5), (5, 3), (5, 5), (3, 4), (5, 4), (4, 3), (4, 5)]:
        on.add((r, c))
    for r, c in sorted(on):
        d = max(abs(r - 4), abs(c - 4))
        op = 1 if d <= 1 else max(.35, 1 - (d - 1) * .2)
        fill = "#fff" if d == 0 else OR2
        out += f'<rect x="{ox + c * (size + gap):.1f}" y="{ox + r * (size + gap):.1f}" width="{size}" height="{size}" rx="3" fill="{fill}" opacity="{op:.2f}"/>'
    out += f'<rect x="150" y="38" width="9" height="9" rx="2" fill="{LILAC}" opacity=".8"/><rect x="38" y="150" width="7" height="7" rx="2" fill="{LILAC}" opacity=".6"/>'
    return out


def c10(n):  # Local pin
    return (grad_bg(n, "circle") +
            f'<path d="M100 20 C63 20 39 48 39 82 C39 126 100 184 100 184 C100 184 161 126 161 82 C161 48 137 20 100 20 Z" fill="url(#og{n})"/>'
            f'<circle cx="100" cy="82" r="38" fill="#fff"/>'
            f'<polyline points="79,94 100,72 121,94" fill="none" stroke="{OR3}" stroke-width="13" stroke-linejoin="miter"/>'
            f'<rect x="94" y="80" width="12" height="30" fill="{OR3}"/>')


def c11(n):  # Blueprint hat: line-art hat on a drawing grid
    grid = "".join(f'<line x1="{v}" y1="0" x2="{v}" y2="200" stroke="#fff" stroke-opacity=".09" stroke-width="1.5"/><line x1="0" y1="{v}" x2="200" y2="{v}" stroke="#fff" stroke-opacity=".09" stroke-width="1.5"/>' for v in range(20, 200, 20))
    return (grad_bg(n) + f'<defs><clipPath id="cp{n}"><rect width="200" height="200" rx="46"/></clipPath></defs><g clip-path="url(#cp{n})">{grid}</g>'
            '<path d="M38 128 A62 62 0 0 1 162 128" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>'
            '<rect x="24" y="128" width="152" height="24" rx="12" fill="none" stroke="#fff" stroke-width="9"/>'
            f'<path d="M89 68 V128 M111 68 V128" stroke="{OR2}" stroke-width="9" stroke-linecap="round"/>' + spark(154, 44, 11, OR2))


def c12(n):  # Hazard type (DT + tape)
    return (f'<defs><clipPath id="cl{n}"><rect width="200" height="200" rx="46"/></clipPath>'
            f'<pattern id="hz{n}" width="24" height="24" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="12" height="24" fill="{OR}"/><rect x="12" width="12" height="24" fill="{INK}"/></pattern></defs>'
            f'<g clip-path="url(#cl{n})"><rect width="200" height="200" fill="{NAVY}"/><rect y="160" width="200" height="40" fill="url(#hz{n})"/>'
            f'<text x="100" y="128" text-anchor="middle" font-family="Bricolage Grotesque" font-weight="800" font-size="104" letter-spacing="-3"><tspan fill="#fff">D</tspan><tspan fill="{OR2}">T</tspan></text></g>')


# Concepts using HTML (need real text positioning)
def html_i_icon():
    return ('<div class="i9" style="width:200px;height:200px;border-radius:46px;background:linear-gradient(135deg,#1a0b4f,#21219a 55%,#2559d8);display:flex;align-items:center;justify-content:center;'
            "font:800 118px 'Bricolage Grotesque';color:#fff;letter-spacing:-4px\"><span>D<span class=\"di\" style=\"--dot:" + OR2 + '">ı</span></span></div>')


CONCEPTS = [
    ("01", "Block D", "A pixel-built D with one orange growth block", c01),
    ("02", "Growth Bars", "The post chart as a mark: segmented bars climbing to orange", c02),
    ("03", "Roof Arrow", "A house gable that is also an up arrow: trade + growth", c03),
    ("04", "Hard Hat", "Hard hat with a digital sparkle", c04),
    ("05", "Swirl Refresh", "Your current swirl, rebuilt as clean vector on the new indigo", c05),
    ("06", "DT Monogram", "A D that holds a T", c06),
    ("07", "Tape Roundel", "Caution-tape band across a roundel", c07),
    ("08", "Pixel Spark", "The sparkle from the posts as a pixel star", c08),
    ("09", "Pixel i-Dots", "Wordmark where every i-dot is a pixel", None),
    ("10", "Local Pin", "Map pin with an up arrow: local + growth", c10),
    ("11", "Blueprint Hat", "Line-art hard hat on a drawing grid", c11),
    ("12", "Hazard Type", "DT on navy with a hazard-tape base", c12),
    ("13", "Recommended", "DT monogram icon + hazard-tape wordmark", c06),
]


# ---------- HTML assembly ----------
def icon_html(num, fn, size):
    if fn is None:
        return f'<div style="width:{size}px;height:{size}px;overflow:hidden;border-radius:{size*.23}px"><div style="transform:scale({size/200});transform-origin:0 0">{html_i_icon()}</div></div>'
    return f'<svg viewBox="0 0 200 200" width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg">{fn(num)}</svg>'


def wordmark(num, variant):
    dark = variant == "dark"
    c1 = "#fff" if dark else "#1a2540"
    c2 = OR2 if dark else OR3
    if num == "09":
        return f'<div class="wm" style="color:{c1}"><span style="font-weight:500">D<span class="di" style="--dot:{LILAC if dark else PERI}">ı</span>g<span class="di" style="--dot:{LILAC if dark else PERI}">ı</span></span><span style="font-weight:800;color:{c2}">Tra<span style="">d</span><span class="di" style="--dot:{OR2 if dark else OR}">ı</span>e</span></div>'
    if num in ("12", "13"):
        return f'<div class="wm caps" style="color:{c1}"><span style="font-weight:800">DIGI</span><span style="font-weight:800;color:{c2}">TRADIE</span></div>'
    return f'<div class="wm" style="color:{c1}"><span style="font-weight:500">Digi</span><span style="font-weight:800;color:{c2};margin-left:.035em">Tradie</span></div>'


def lockup_html(num, fn, variant, icon_size=200):
    return f'<div class="lk">{icon_html(num, fn, icon_size)}{wordmark(num, variant)}</div>'


CSS = FONT_IMPORT + """
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Bricolage Grotesque',sans-serif}
.lk{display:inline-flex;align-items:center;gap:42px}
.wm{font-family:'Bricolage Grotesque';font-size:112px;letter-spacing:-.025em;line-height:1;white-space:nowrap;position:relative}
.wm.caps{letter-spacing:.04em;font-size:92px;padding-bottom:30px}
.wm.caps:after{content:"";position:absolute;left:0;right:0;bottom:0;height:16px;background:repeating-linear-gradient(-45deg,#EC702E 0 14px,#1a0b2e 14px 28px)}
.di{position:relative;display:inline-block}
.di:after{content:"";position:absolute;left:50%;top:.075em;width:.175em;height:.175em;transform:translateX(-50%);background:var(--dot)}
"""


def screenshot(html_path, png_path, w, h, scale=2, transparent=False):
    args = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--force-device-scale-factor={scale}",
            f"--window-size={w},{h}", "--virtual-time-budget=12000", f"--screenshot={png_path}"]
    if transparent:
        args.append("--default-background-color=00000000")
    subprocess.run(args + [f"file://{html_path}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)


def export_concept(num, name, fn):
    slug = f"{num}-{name.lower().replace(' ', '-')}"
    d = OUT / slug
    d.mkdir(exist_ok=True)
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}html,body{{background:transparent}}</style></head><body>
<div style="position:absolute;left:0;top:0">{icon_html(num, fn, 512)}</div>
<div style="position:absolute;left:0;top:560px">{lockup_html(num, fn, 'dark')}</div>
<div style="position:absolute;left:0;top:860px">{lockup_html(num, fn, 'light')}</div></body></html>"""
    p = TMP / f"exp-{num}.html"
    p.write_text(html)
    shot = TMP / f"exp-{num}.png"
    screenshot(p, shot, 1500, 1200, scale=2, transparent=True)
    im = Image.open(shot).convert("RGBA")
    im.crop((0, 0, 1024, 1024)).save(d / "icon.png")
    for name_, y0, y1 in (("lockup-on-dark", 1120, 1720), ("lockup-on-light", 1720, 2320)):
        region = im.crop((0, y0, 3000, y1))
        bb = region.getbbox()
        region.crop(bb).save(d / f"{name_}.png")
    if fn is not None:
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="512" height="512"><style>{FONT_IMPORT}</style>{fn(num)}</svg>'
        (d / "icon.svg").write_text(svg)
    return slug


def build_sheet():
    tiles = []
    for num, name, blurb, fn in CONCEPTS:
        tiles.append(f"""<div class="tile"><div class="tn"><b>{num}</b> {name}<span>{blurb}</span></div>
<div class="strip dk"><div class="sc">{lockup_html(num, fn, 'dark')}</div></div>
<div class="strip lt"><div class="sc">{lockup_html(num, fn, 'light')}</div></div></div>""")
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}
body{{background:#0f0a2e;color:#fff;width:2112px;padding:36px 36px 36px}}
h1{{font-size:54px;letter-spacing:-.03em;font-weight:800}} h1 em{{font-style:normal;color:{OR2}}}
.sub{{font-family:Figtree,sans-serif;color:{LILAC};margin:8px 0 28px;font-size:24px;font-family:'Bricolage Grotesque'}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}}
.tile{{background:#17123f;border:1.5px solid rgba(255,255,255,.1);border-radius:26px;overflow:hidden}}
.tn{{padding:18px 24px 14px;font-size:30px;font-weight:800}} .tn b{{color:{OR2};margin-right:8px}}
.tn span{{display:block;font-size:17px;font-weight:500;color:{LILAC};margin-top:4px}}
.strip{{height:200px;display:flex;align-items:center;padding-left:28px;overflow:hidden}}
.strip.dk{{background:linear-gradient(135deg,#1a0b4f,#2559d8)}} .strip.lt{{background:#F4F1EA}}
.sc{{transform:scale(.6);transform-origin:left center;width:1000px}}
</style></head><body><h1>Logo concepts: <em>DigiTradie</em></h1>
<div class="sub">12 directions drawn from the posts: pixel blocks, growth bars, hazard tape, hard hat, the swirl. Each shown on dark and on the site cream.</div>
<div class="grid">{''.join(tiles)}</div></body></html>"""
    p = TMP / "sheet.html"
    p.write_text(html)
    screenshot(p, OUT / "contact-sheet.png", 2112, 2300, scale=1)
    # contact sheet height varies: crop whitespace
    im = Image.open(OUT / "contact-sheet.png").convert("RGB")
    return im.size


if __name__ == "__main__":
    for num, name, blurb, fn in CONCEPTS:
        print("exported", export_concept(num, name, fn))
    print("sheet", build_sheet())
    shutil.rmtree(TMP, ignore_errors=True)
