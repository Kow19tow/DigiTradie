"""Reusable page sections. Each returns an HTML string. Copy sticks to facts already on the site (see the brief)."""
from .core import (EMAIL, GUIDES, PACKAGES, PHONE, PHONE_TEL, SERVICES, esc, form, icon)


# ---------------------------------------------------------------- small helpers
def crumbs_html(crumbs):
    parts = []
    for i, (name, path) in enumerate(crumbs):
        if i < len(crumbs) - 1:
            parts.append(f'<a href="{path}">{esc(name)}</a><span aria-hidden="true">/</span>')
        else:
            parts.append(f'<span aria-current="page">{esc(name)}</span>')
    return f'<nav class="crumbs" aria-label="Breadcrumb">{"".join(parts)}</nav>'


def plate(title, rows):
    """Equipment-style spec plate for inner-page heroes. rows = [(label, value-html)]."""
    inner = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in rows)
    return f'<aside class="plate" aria-label="{esc(title)} at a glance"><div class="plate-h"><span>{esc(title)}</span><span>At a glance</span></div><dl>{inner}</dl></aside>'


def page_hero(*, eyebrow, h1, lede, crumbs=None, actions="", visual="", tone="dark"):
    cr = crumbs_html(crumbs) if crumbs else ""
    return f"""<section class="phero phero-{tone}">
  <div class="wrap phero-in{' has-art' if visual else ''}">
    <div class="phero-copy">
      {cr}
      <p class="chip">{esc(eyebrow)}</p>
      <h1>{h1}</h1>
      {f'<p class="lede">{lede}</p>' if lede else ''}
      {actions}
    </div>
    {visual}
  </div>
  <div class="tape" aria-hidden="true"></div>
</section>"""


def section_head(eyebrow, h2, sub="", center=False, dark=False):
    c = " center" if center else ""
    d = " on-dark" if dark else ""
    sub_html = f'<p class="sub">{sub}</p>' if sub else ""
    return f'<div class="shead{c}{d}"><p class="eyebrow">{esc(eyebrow)}</p><h2>{h2}</h2>{sub_html}</div>'


# ---------------------------------------------------------------- homepage hero
def home_hero():
    return f"""<section class="hero" id="top">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <p class="chip">Fractional marketing for small &amp; medium business</p>
      <h1>We don&rsquo;t take<br><em>just any business.</em></h1>
      <p class="lede">DigiTradie is a fractional in-house marketing service for small and medium businesses across Australia. We run your Meta Ads, Google Ads, SEO and website, but only for businesses we can genuinely help. If we&rsquo;re not the right fit, we&rsquo;ll tell you on the first call.</p>
      <a class="btn btn-glow hero-cta-m" href="#contact" data-cta="hero-mobile">Book a free fit check {icon("arrow-right")}</a>
      <ul class="channels" aria-label="What we manage">
        <li class="ch ch-1">Meta Ads</li><li class="ch ch-1">Google Ads</li><li class="ch">SEO</li><li class="ch">Website optimisation</li>
      </ul>
      <ul class="ticks">
        <li>A dashboard you can check any time, even from your phone</li>
        <li>Set and forget for a once-off fee, or keep us on</li>
        <li>Learn the basics so you can run it yourself</li>
      </ul>
      <div class="owner">
        <img src="/assets/img/kosta-160.webp" width="68" height="68" alt="Kosta Diamantopoulos">
        <p><b>You deal with Kosta,</b> the person who runs your account. Never a junior.</p>
      </div>
      <a class="proof" href="/blog/renovation-leads-case-study" data-cta="hero-proof">
        <span class="proof-num"><small>$500 ad spend</small><b>$75K+</b><small>profit</small></span>
        <span class="proof-bars" aria-hidden="true"><i style="--h:18%"></i><i style="--h:30%"></i><i style="--h:44%"></i><i style="--h:62%"></i><i style="--h:100%" class="top"></i></span>
        <span class="proof-txt">One offer change for a Melbourne renovation business. <u>Read the case study</u> {icon("arrow-right")}</span>
      </a>
    </div>
    <div class="hero-form" id="contact">
      <div class="sticker" aria-hidden="true"><span>Free<b>15 min</b>fit check</span></div>
      {form("hero-form", source="home-hero")}
    </div>
  </div>
  <div class="tape" aria-hidden="true"></div>
</section>"""


# ---------------------------------------------------------------- proof + founder
def stats_band():
    return f"""<section class="section stats">
  <div class="wrap">
    <div class="stat-grid">
      <div class="stat reveal"><b>$100k+</b><p>monthly ad budgets managed on international accounts</p></div>
      <div class="stat reveal"><b>$500 <span class="arr">&rarr;</span> $75k+</b><p>ad spend to profit for one Melbourne renovation business</p></div>
      <div class="stat reveal"><b>15&ndash;20<small> min</small></b><p>one fit-check call, then a straight answer on whether we can help</p></div>
    </div>
  </div>
</section>"""


def founder_card(compact=False):
    return f"""<section class="section founder">
  <div class="wrap founder-grid">
    <div class="founder-photo reveal">
      <img src="/assets/img/kosta-600.webp" srcset="/assets/img/kosta-400.webp 400w, /assets/img/kosta-600.webp 600w" sizes="(max-width:760px) 70vw, 360px" width="360" height="360" loading="lazy" alt="Kosta Diamantopoulos, founder of DigiTradie">
      <span class="badge-stamp" aria-hidden="true">You deal with<br><b>the person<br>who pitched you</b></span>
    </div>
    <div class="founder-copy reveal">
      <p class="eyebrow">Experience behind DigiTradie</p>
      <h2>Built on more than local experience.</h2>
      <p>Behind DigiTradie is experience across global ad agency networks, national telecom and fashion retail brands, and luxury hospitality campaigns, managing $100k+ monthly ad budgets on international accounts.</p>
      <p>Closer to home, that same approach turned $500 in ad spend into $75k+ profit for a single Melbourne renovation business. That is the experience behind every DigiTradie package, whether you&rsquo;re spending $50 a day or $5,000.</p>
      <div class="founder-cta">
        <a class="btn btn-primary" href="/blog/renovation-leads-case-study" data-cta="founder-case">Read the case study {icon("arrow-right")}</a>
        <a class="btn btn-ghost" href="/about">About Kosta</a>
      </div>
    </div>
  </div>
</section>"""


# ---------------------------------------------------------------- fit / how
GOOD = ["You&rsquo;re launching ads for the first time", "You&rsquo;re spending but can&rsquo;t tell what&rsquo;s working",
        "You want to learn enough to handle the basics yourself", "You want in-house marketing help without a full-time hire",
        "You want a DigiTradie tailored to your business, not a generic package"]
NOT = ["You want the cheapest option, not the right one", "You want a black box, not a partner who shows their work",
       "You&rsquo;re after a big agency with layers of account managers", "Your in-house team already runs ads well",
       "You want a junior handling your account, not the person who pitched you"]


def fit_section():
    good = "".join(f'<li>{icon("circle-check")}<span>{t}</span></li>' for t in GOOD)
    bad = "".join(f'<li>{icon("circle-x")}<span>{t}</span></li>' for t in NOT)
    return f"""<section class="section fit" id="fit">
  <div class="wrap">
    {section_head("Honest fit check", "Built for businesses that genuinely need a hand.", "We qualify hard, on purpose. It saves you money and it saves us both a bad engagement.")}
    <div class="fit-grid">
      <article class="ticket ticket-good reveal"><h3><span class="tag">{icon("check")}</span>Good fit</h3><ul>{good}</ul></article>
      <article class="ticket ticket-bad reveal"><h3><span class="tag">{icon("x")}</span>Probably not a fit</h3><ul>{bad}</ul></article>
    </div>
  </div>
</section>"""


def how_section(dark=False):
    steps = [
        ("01", "calendar-check", "Fit check", "One consultation to understand your business and whether ads make sense for you right now."),
        ("02", "wrench", "Build or fix", "We set up or audit your ads and plug in a dashboard that shows what they&rsquo;re actually doing."),
        ("03", "handshake", "Hand over or stay on", "Run it yourself with the basics we show you, or keep us on as your fractional marketer."),
    ]
    cards = "".join(
        f'<li class="step reveal"><span class="step-n">{n}</span><h3>{t}</h3><p>{d}</p></li>'
        for n, ic, t, d in steps)
    return f"""<section class="section how" id="how">
  <div class="wrap">
    {section_head("How it works", "How it works", "Every client starts with the same free call, so we can tell you where you actually stand.", center=True)}
    <ol class="steps">{cards}</ol>
  </div>
</section>"""


# ---------------------------------------------------------------- services bento
def services_bento():
    svc = "".join(
        f'<a class="tile tile-svc reveal" href="/services/{s}"><span class="tile-ic">{icon(ic)}</span><h3>{t}</h3><p>{d}</p><span class="go">Learn more {icon("arrow-right")}</span></a>'
        for s, t, d, ic in SERVICES)
    return f"""<section class="section what" id="services">
  <div class="wrap">
    {section_head("What we do", "We run your ads, and fix the website they send people to.", "Mostly Meta Ads and Google Ads. SEO and website work come in where they help the ads pay off.")}
    <div class="bento">
      {svc}
      <a class="tile tile-wide tile-dash reveal" href="/#dashboard"><span class="tile-ic">{icon("layout-dashboard")}</span><h3>A dashboard in every package</h3><p>Leads, cost per lead and spend in plain English, on your phone, any time. No logging in to five platforms.</p>
        <span class="mini-bars" aria-hidden="true"><i style="--h:30%"></i><i style="--h:42%"></i><i style="--h:38%"></i><i style="--h:58%"></i><i style="--h:52%"></i><i style="--h:74%"></i><i style="--h:100%"></i></span></a>
      <a class="tile tile-coach reveal" href="/ads-setup"><span class="tile-ic">{icon("graduation-cap")}</span><h3>Learn it yourself</h3><p>We build it, then teach you the basics. Coaching add-on available.</p><span class="go">See Ads Setup {icon("arrow-right")}</span></a>
    </div>
  </div>
</section>"""


# ---------------------------------------------------------------- dashboard preview
def _chart():
    pts = [14, 18, 17, 24, 29, 27, 36, 41]
    w, h, base = 560, 200, 168
    bw, gap = 50, 22
    x0 = (w - (len(pts) * bw + (len(pts) - 1) * gap)) / 2
    bars = ""
    for i, v in enumerate(pts):
        bh = v / 45 * (base - 24)
        x = x0 + i * (bw + gap)
        cls = "bar-top" if i == len(pts) - 1 else "bar-b"
        bars += (f'<rect class="{cls}" x="{x:.1f}" y="{base - bh:.1f}" width="{bw}" height="{bh:.1f}"/>'
                 f'<text x="{x + bw / 2:.1f}" y="{base - bh - 7:.1f}" text-anchor="middle">{v}</text>'
                 f'<text x="{x + bw / 2:.1f}" y="{base + 20}" text-anchor="middle">Wk {i + 1}</text>')
    return (f'<svg class="chart" viewBox="0 0 {w} {h}" role="img" aria-label="Sample bar chart of leads per week rising over eight weeks">'
            f'<line class="base" x1="0" x2="{w}" y1="{base}" y2="{base}"/>{bars}</svg>')


def dashboard_section():
    return f"""<section class="section dash" id="dashboard">
  <div class="wrap dash-grid">
    <div class="dash-copy reveal">
      <p class="eyebrow">Your dashboard</p>
      <h2>See what your ads are actually doing.</h2>
      <p>Every package comes with a plain-English dashboard you can open any time. No logins to five platforms, no guessing, no waiting for a monthly PDF.</p>
      <ul class="ticks">
        <li>Leads, cost per lead and spend on one screen</li>
        <li>A plain note on what changed and why</li>
        <li>Works on your phone</li>
      </ul>
      <a class="btn btn-glow" href="/contact" data-cta="dash">Book a free fit check {icon("arrow-right")}</a>
    </div>
    <div class="dash-mock reveal" role="group" aria-label="Sample dashboard, illustrative data only">
      <div class="win-bar"><span>Your dashboard &middot; this month</span><em>Sample data</em></div>
      <div class="kpis">
        <div class="kpi"><span>Leads</span><b>41</b><small class="up">{icon("trending-up")} 18%</small></div>
        <div class="kpi"><span>Cost per lead</span><b>$38</b><small class="up">{icon("trending-down")} 22%</small></div>
        <div class="kpi"><span>Spend</span><b>$1.6k</b><small>on plan</small></div>
      </div>
      <div class="chart-wrap"><p>Leads by week</p>{_chart()}</div>
      <ul class="changes">
        <li><span>Wk 7</span>Paused 3 keywords that were spending without producing enquiries</li>
        <li><span>Wk 6</span>Moved budget to the ad set that brings in phone calls</li>
        <li><span>Wk 5</span>Added call tracking to the contact page</li>
      </ul>
      <p class="mock-note">Illustrative sample data, not a client result.</p>
    </div>
  </div>
</section>"""


# ---------------------------------------------------------------- case study + packages + guides
def case_teaser():
    return f"""<section class="section case">
  <div class="wrap case-grid">
    <a class="case-poster" href="/blog/renovation-leads-case-study">
      <span class="cp-row"><small>Ad spend</small><b>$500</b></span>
      <span class="cp-arrow" aria-hidden="true">&darr;</span>
      <span class="cp-row cp-big"><small>Profit</small><b>$75K+</b></span>
      <span class="cp-foot">One Melbourne renovation business. One offer change.</span>
    </a>
    <div class="case-copy reveal">
      <p class="eyebrow">Case study</p>
      <h2>The right offer beats a discount. Every time.</h2>
      <p>One offer change turned a tiny ad budget into six figures of profit for a Melbourne renovation business. Here is what changed, and why the right offer beat a discount.</p>
      <a class="btn btn-primary" href="/blog/renovation-leads-case-study" data-cta="case">Read the case study {icon("arrow-right")}</a>
    </div>
  </div>
</section>"""


def packages_section(exclude=None, heading="Packages", sub=None, eyebrow="Packages"):
    sub = sub if sub is not None else ("Built for small and medium businesses: affordable, and useful wherever you&rsquo;re at in your growth. "
                  "Prefer a once-off setup with no monthly retainer? We&rsquo;ll build it and show you how to run it yourself. "
                  "Final scope is agreed after your fit check, and every package includes your dashboard.")
    cards = []
    for slug, name, tag, desc, label, cadence, feats, ic in PACKAGES:
        if slug == exclude:
            continue
        cls = {"audit-optimise": "tier-start", "ads-setup": "tier-pop", "fractional-marketer": "tier-dark"}[slug]
        feat = "".join(f"<li>{icon('check')}{f}</li>" for f in feats)
        addon = '<p class="tier-addon">Coaching add-on available</p>' if slug == "ads-setup" else ""
        cards.append(f"""<a class="tier {cls} reveal" href="/{slug}">
  <p class="tier-tag">{tag}</p>
  <h3>{esc(name)}</h3>
  <p class="tier-desc">{desc}</p>
  <p class="tier-price"><b>{label}</b> <span>{cadence}</span></p>
  <ul class="tier-feats">{feat}</ul>{addon}
  <span class="tier-cta">Learn more {icon("arrow-right")}</span>
</a>""")
    return f"""<section class="section tiers" id="packages">
  <div class="wrap">
    {section_head(eyebrow, heading, sub, center=True)}
    <div class="tier-grid">{"".join(cards)}</div>
    <p class="tier-foot">Exact investment is confirmed on your fit-check call. Ad spend is separate from our fees.</p>
  </div>
</section>"""


def guides_grid(limit=None, heading="Free DIY marketing guides for your industry", sub=None, dark=False):
    sub = sub or "Straight-talking, industry-specific guides for owners who want to run their own marketing first, and know when it is time to hand it over."
    items = GUIDES[:limit] if limit else GUIDES
    tiles = "".join(
        f'<a class="gtile reveal" href="/learn/{s}"><span class="gic">{icon(ic)}</span><b>{esc(lbl)}</b><span class="go">{icon("arrow-up-right")}</span></a>'
        for s, lbl, ic in items)
    return f"""<section class="section guides">
  <div class="wrap">
    {section_head("Learn", heading, sub)}
    <div class="gtiles">{tiles}</div>
    <p class="center"><a class="btn btn-ghost" href="/learn">See all guides {icon("arrow-right")}</a></p>
  </div>
</section>"""


# ---------------------------------------------------------------- faq + cta
def faq_section(faqs, heading="Questions we get asked", eyebrow="FAQ", sub="", dark=False):
    items = "".join(f'<details class="faq"><summary><span>{esc(q)}</span>{icon("chevron-down")}</summary><div class="faq-a"><p>{a}</p></div></details>' for q, a in faqs)
    return f"""<section class="section faqs">
  <div class="wrap faq-wrap">
    {section_head(eyebrow, heading, sub)}
    <div class="faq-list">{items}</div>
  </div>
</section>"""


def cta_band(heading="Let&rsquo;s find out if we&rsquo;re a fit.", sub="One call. We&rsquo;ll tell you straight whether we can help, even if the answer is &ldquo;not yet&rdquo;.", fid="cta-form", source="cta-band"):
    return f"""<section class="section cta" id="book">
  <div class="cta-bg" aria-hidden="true"><span class="tools"></span></div>
  <div class="wrap cta-grid">
    <div class="cta-copy reveal">
      <p class="eyebrow">Free fit check</p>
      <h2>{heading}</h2>
      <p>{sub}</p>
      <ul class="ticks">
        <li>One call, usually 15 to 20 minutes</li>
        <li>No obligation, no lock-in contracts</li>
        <li>A straight answer, even if it is &ldquo;not yet&rdquo;</li>
      </ul>
      <p class="cta-direct">Prefer to reach out directly? <a href="mailto:{EMAIL}" data-track="email">{EMAIL}</a> &middot; <a href="tel:{PHONE_TEL}" data-track="phone">{PHONE}</a></p>
    </div>
    <div class="cta-form reveal">{form(fid, source=source, dark=False, compact=True, heading="Book your free fit check")}</div>
  </div>
  <div class="tape" aria-hidden="true"></div>
</section>"""


def related_cards(cards, heading="Keep reading"):
    inner = "".join(
        f'<a class="rcard reveal" href="{h}"><span class="rtag">{esc(tag)}</span><h3>{esc(t)}</h3><p>{esc(d)}</p><span class="go">Read {icon("arrow-right")}</span></a>'
        for h, tag, t, d in cards)
    return f"""<section class="section related"><div class="wrap">{section_head("More from DigiTradie", heading)}<div class="rgrid">{inner}</div></div></section>"""
