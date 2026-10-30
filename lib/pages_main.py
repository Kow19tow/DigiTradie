"""Service, package and company pages. Copy rules: plain English, Australian spelling, no invented stats or results."""
from . import components as c
from .core import (EMAIL, PACKAGES, PHONE, PHONE_TEL, SERVICES, SITE, ADS_CONVERSION_LABEL, AW, esc, faq_node, form, icon, page)
from .pages_home import HOME_FAQS


def actions(primary="Book a free fit check", where="hero", ghost=None):
    g = f'<a class="btn btn-ghost" href="{ghost[1]}">{ghost[0]}</a>' if ghost else ""
    return f'<div class="hero-actions"><a class="btn btn-glow" href="/contact" data-cta="{where}">{primary} {icon("arrow-right")}</a>{g}</div>'


def feat_grid(items):
    inner = "".join(f'<div class="feat reveal"><span class="tile-ic">{icon(ic)}</span><h3>{t}</h3><p>{d}</p></div>' for ic, t, d in items)
    return f'<div class="feat-grid">{inner}</div>'


def facts(rows):
    inner = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in rows)
    return f'<dl class="facts facts-wrap">{inner}</dl>'


def timeline(steps):
    return '<ol class="timeline">' + "".join(f"<li><h3>{t}</h3><p>{d}</p></li>" for t, d in steps) + "</ol>"


ART = {
    "google-ads": ("search", ("Conversion tracking", "Waste controlled", "Dashboard included")),
    "meta-ads": ("megaphone", ("Offer first", "Tracked enquiries", "Dashboard included")),
    "seo-website-optimisation": ("globe", ("Found on Google", "Fast on mobile", "Clear next steps")),
    "audit-optimise": ("clipboard-check", ("Full account audit", "Fixes applied", "No lock-in")),
    "ads-setup": ("rocket", ("Built properly", "Handed to you", "Coaching available")),
    "fractional-marketer": ("handshake", ("Ongoing optimisation", "Regular check-ins", "Limited spots")),
    "services": ("layout-dashboard", ("Meta Ads", "Google Ads", "SEO and website")),
    "about": ("users", ("The person who pitched you", "Fewer clients", "Straight answers")),
}


# =========================================================== services hub
def build_services_hub():
    cards = "".join(
        f'<a class="tile tile-svc reveal" href="/services/{s}"><span class="tile-ic">{icon(ic)}</span><h3>{t}</h3><p>{d}</p><span class="go">See how it works {icon("arrow-right")}</span></a>'
        for s, t, d, ic in SERVICES)
    together = feat_grid([
        ("search", "Google catches demand", "People searching for what you sell already want it. Google Ads and local SEO put you in front of them at the moment they are looking."),
        ("megaphone", "Meta creates demand", "People who are not searching yet can still be reached with the right offer on Facebook and Instagram, early enough that you are the one they remember."),
        ("globe", "Your website closes the gap", "Traffic only pays off if the page turns it into an enquiry, so website optimisation and tracking sit behind every channel."),
    ])
    main = "\n".join([
        c.page_hero(eyebrow="Services", h1="Marketing services for small business, <em>run by one accountable marketer.</em>",
                    lede="Meta Ads and Google Ads first, then SEO and website optimisation so the traffic you pay for turns into enquiries. Every engagement starts with a free fit check and includes a dashboard you can read.",
                    crumbs=[("Home", "/"), ("Services", None)], actions=actions(where="services-hero"), visual=c.art(*ART["services"])),
        f'<section class="section what"><div class="wrap">{c.section_head("What we do", "Three channels. One plan.", "Most small businesses do not need every channel at once. We pick the ones that suit how your customers buy.")}<div class="bento" style="grid-template-columns:repeat(auto-fit,minmax(260px,1fr))">{cards}</div></div></section>',
        f'<section class="section"><div class="wrap">{c.section_head("How the channels work together", "Catch demand, create demand, convert it.", center=True)}{together}</div></section>',
        c.packages_section(heading="Pick how you want to work with us", eyebrow="Ways to work together"),
        c.faq_section(HOME_FAQS[:4], heading="Quick answers"),
        c.cta_band(),
    ])
    page("/services", title="Meta Ads, Google Ads and SEO for Small Business | DigiTradie",
         desc="Meta Ads, Google Ads, SEO and website optimisation for Australian small businesses, run by one accountable marketer with a dashboard you can read.",
         main=main, crumbs=[("Home", "/"), ("Services", "/services")], nodes=[faq_node(HOME_FAQS[:4], SITE + "/services")], page_type="CollectionPage")


# =========================================================== service detail pages
def _service(slug, *, title, desc, eyebrow, h1, lede, when_h2, when_html, facts_rows, setup_items, setup_h2, expect_h2, expect_html, faqs, related):
    url = f"{SITE}/services/{slug}"
    svc_name = {s[0]: s[1] for s in SERVICES}[slug]
    service_node = {
        "@type": "Service", "@id": url + "#service", "name": svc_name, "serviceType": svc_name, "url": url,
        "description": desc, "provider": {"@id": f"{SITE}/#organization"}, "areaServed": {"@type": "Country", "name": "Australia"},
        "audience": {"@type": "BusinessAudience", "name": "Small and medium businesses"},
    }
    main = "\n".join([
        c.page_hero(eyebrow=eyebrow, h1=h1, lede=lede, crumbs=[("Home", "/"), ("Services", "/services"), (svc_name, None)],
                    actions=actions(where=f"{slug}-hero", ghost=("See what is included", "#included")),
                    visual=c.art(*ART[slug])),
        f'''<section class="section"><div class="wrap split">
  <div class="prose reveal"><h2>{when_h2}</h2>{when_html}</div>
  <div class="reveal"><h2 class="sr-h" style="font-size:1.1rem;margin-bottom:12px">At a glance</h2>{facts(facts_rows)}</div>
</div></section>''',
        f'<section class="section what" id="included"><div class="wrap">{c.section_head("What we set up", setup_h2)}{feat_grid(setup_items)}</div></section>',
        f'<section class="section"><div class="wrap"><div class="prose reveal"><h2>{expect_h2}</h2>{expect_html}</div></div></section>',
        c.faq_section(faqs, heading=f"{svc_name} questions"),
        c.related_cards(related, heading="Related reading"),
        c.packages_section(heading="Ways to work with us", eyebrow="Packages"),
        c.cta_band(),
    ])
    page(f"/services/{slug}", title=title, desc=desc, main=main,
         crumbs=[("Home", "/"), ("Services", "/services"), (svc_name, f"/services/{slug}")], nodes=[service_node, faq_node(faqs, url)])


def build_services():
    _service(
        "google-ads",
        title="Google Ads Management for Small Business | DigiTradie",
        desc="Google Ads management for Australian small businesses: search campaigns, conversion tracking and a plain-English dashboard. Book a free fit check.",
        eyebrow="Google Ads management",
        h1="Google Ads for small business, built around <em>enquiries, not clicks.</em>",
        lede="Google Ads puts you in front of people who are already searching for what you sell. Done properly, it is the fastest way to get the phone ringing. Done carelessly, it is the fastest way to burn a budget.",
        when_h2="When Google Ads is the right call",
        when_html="""<p>Google Ads earns its keep when someone is searching for exactly what you do and wants it soon. Think emergency callouts, same-day jobs, &ldquo;near me&rdquo; searches, and any service people look up when they are ready to book.</p>
<p>It is a weaker fit when your customers take weeks to decide. A renovation, a move or a big purchase usually starts earlier, with someone scrolling rather than searching. For that kind of work we lean on <a href="/services/meta-ads">Meta Ads</a> first and use Google to catch people when they are ready.</p>
<p>Not sure which side of the line you sit on? That is the first thing we work out on your fit-check call.</p>""",
        facts_rows=[("Best for", "Urgent or high-intent work"), ("Customer is", "Already searching"), ("Speed", "Can start producing enquiries quickly"),
                    ("Ad spend", "Paid to Google, separate from our fees"), ("Pairs well with", "SEO and website optimisation")],
        setup_h2="Built to show you which clicks become enquiries.",
        setup_items=[
            ("target", "Conversion tracking first", "Calls, forms and bookings are tracked from day one, so you see which clicks turn into enquiries and not just which ones cost money."),
            ("search", "Campaigns built around your services", "Tightly themed search campaigns for the work you actually want, matched to the words people type instead of a broad net."),
            ("shield-check", "Negative keywords and waste control", "We review search terms and block the ones that spend budget without producing enquiries."),
            ("map-pin", "Location targeting", "Ads shown in the suburbs and regions you actually serve, and nowhere else."),
            ("file-text", "Ads and pages that match", "The ad, the landing page and the offer say the same thing, which is what lifts the enquiry rate."),
            ("gauge", "Budgets tuned to a cost per lead", "Budgets and bidding are set toward your target cost per lead and reviewed on a regular rhythm."),
        ],
        expect_h2="What to expect, honestly",
        expect_html="""<p>The first weeks are about learning what works in your market. We watch the search terms that trigger your ads, trim the ones that waste money and put more behind the ones that produce enquiries.</p>
<p>We will not promise a number of leads, because no honest marketer can before seeing your market, your offer and your website. What we do promise is that you can see what is happening in your dashboard, in plain English, and that you will hear about it from the person doing the work.</p>
<div class="callout"><p><b>Paid ads do not change your organic rankings.</b> Google keeps the two separate. If you also want to show up for free, that is a job for <a href="/services/seo-website-optimisation">SEO and website optimisation</a>.</p></div>""",
        faqs=[
            ("How much should I spend on Google Ads?", "It depends on your market, how competitive your keywords are and how many enquiries you want. We work out a sensible starting budget with you on the fit-check call. Ad spend goes to Google and is separate from our fees."),
            ("Do I need a website for Google Ads?", "You need a page for people to land on, ideally one that matches the ad and makes the next step obvious. If yours is not ready, we can fix it as part of the work."),
            ("Will I see which clicks became enquiries?", "Yes. We set up conversion tracking for calls and forms first, and your dashboard shows leads, cost per lead and spend in plain English."),
            ("Should I run Google Ads or work on SEO?", "Google Ads is paid and can start quickly. SEO builds over time and costs nothing per click once it is working. Many businesses use ads while organic search builds up. Paid ads do not influence organic rankings."),
        ],
        related=[("/learn/tradie-marketing", "DIY guide", "Tradie marketing that keeps the job board full", "Urgent work goes Google first. Considered work goes social first."),
                 ("/blog/google-for-tradies", "SEO", "How local tradies actually show up on Google", "What moves the needle on Google Maps and local search, and what does not."),
                 ("/audit-optimise", "Package", "Audit and Optimise", "Already running Google Ads? We find what is wasting money and fix it.")],
    )
    _service(
        "meta-ads",
        title="Meta Ads Management for Small Business | DigiTradie",
        desc="Facebook and Instagram advertising for Australian small businesses: offers, creative, tracking and a plain-English dashboard. Book a free fit check.",
        eyebrow="Meta Ads management",
        h1="Meta Ads that turn <em>scrolling into enquiries.</em>",
        lede="Meta Ads (Facebook and Instagram) put your offer in front of people before they start searching. They suit businesses whose customers take time to decide, or who need to create demand rather than catch it.",
        when_h2="When Meta Ads is the right call",
        when_html="""<p>Meta Ads work best when the buyer is not searching yet. Renovations, moving house, a gym membership, a new hairdresser, a restaurant booking: these start with someone seeing something that catches their attention, then deciding later.</p>
<p>They also suit businesses with something worth looking at. If your work photographs well, Meta is where it can do the selling.</p>
<p>If your customers are searching in the moment, such as a burst pipe or a flat battery, <a href="/services/google-ads">Google Ads</a> usually comes first. Many businesses end up running both, each doing its own job.</p>""",
        facts_rows=[("Best for", "Considered purchases and visual businesses"), ("Customer is", "Not yet searching"), ("Speed", "Improves as offers and creative are tested"),
                    ("Ad spend", "Paid to Meta, separate from our fees"), ("Pairs well with", "Google Ads for people ready to buy")],
        setup_h2="The offer does the heavy lifting. We build around it.",
        setup_items=[
            ("megaphone", "An offer worth stopping for", "We shape the offer first, because it does more work than any targeting setting. It is the lesson behind our renovation case study."),
            ("target", "Tracking Meta can learn from", "Pixel and conversion setup so Meta optimises for real enquiries, not just clicks and likes."),
            ("eye", "Creative direction", "Clear direction on the photos, video and copy that suit feed, stories and reels, built from the work you already have."),
            ("users", "Audiences, tested", "Local targeting plus audiences built from your customers and website visitors, tested against each other so budget follows what works."),
            ("refresh-cw", "Follow-up for people who did not enquire", "Retargeting reminds visitors who looked but did not act."),
            ("trending-up", "Testing and budget moves", "We test offers and creative, then move budget toward what produces enquiries."),
        ],
        expect_h2="What we need from you",
        expect_html="""<p>Meta Ads run on real material, so the more you can share, the better they perform: photos and video of your work, a clear idea of what you want more of, and access to your Meta Business account (we request it through Meta&rsquo;s own sharing settings, so you never hand over a password).</p>
<p>From there we handle the build, the testing and the reporting, and your dashboard shows what each dollar of ad spend is producing.</p>
<div class="callout"><p><b>The right offer beats a discount.</b> One offer change turned $500 of ad spend into $75k+ profit for a Melbourne renovation business. <a href="/blog/renovation-leads-case-study">Read the case study.</a></p></div>""",
        faqs=[
            ("Are Meta Ads or Google Ads better for my business?", "It depends on how your customers buy. If they search when they need you, Google comes first. If they take weeks to decide, Meta usually comes first. Many businesses use both. We work out the split with you on the fit-check call."),
            ("Do I need to post on social media for ads to work?", "Ads can run without regular posting. People who see your ad will often visit your page, though, so it helps if it looks current."),
            ("How will I know it is working?", "Your dashboard shows leads, cost per lead and spend, with a short note on what changed and why."),
            ("Can you run Meta and Google together?", "Yes. That is the most common setup, with each channel doing the job it is best at."),
        ],
        related=[("/blog/renovation-leads-case-study", "Case study", "How the right offer can transform your renovation leads", "Why the right offer beats a discount, and how $500 became $75k+ profit."),
                 ("/learn/tradie-marketing", "DIY guide", "Tradie marketing that keeps the job board full", "How to decide between Google first and social first."),
                 ("/ads-setup", "Package", "Dashboard + Ads Setup", "Get your ads live, built properly, then handed to you.")],
    )
    _service(
        "seo-website-optimisation",
        title="SEO and Website Optimisation for Small Business | DigiTradie",
        desc="Local SEO and website optimisation for Australian small businesses: Google Business Profile, on-page SEO, speed and conversion fixes.",
        eyebrow="SEO and website optimisation",
        h1="SEO and website optimisation that <em>earns free traffic</em> and turns visits into enquiries.",
        lede="Two jobs, one goal. First, be found when people search for what you do. Second, make sure the visitors you get turn into phone calls and form fills.",
        when_h2="Why this sits behind every channel",
        when_html="""<p>Every dollar you spend on ads sends people to your website, and every free visitor from Google arrives there too. If the site is slow, confusing or hard to use on a phone, you pay for traffic that leaves.</p>
<p>SEO works on the free side: your Google Business Profile, your reviews, your service pages and the technical basics. Website optimisation works on the conversion side: speed, clear calls to action and short forms.</p>
<p>It is slower than ads, but it compounds. It also keeps working when the ad budget pauses.</p>""",
        facts_rows=[("Best for", "Local and service businesses wanting steady free traffic"), ("Customer is", "Searching, or about to"), ("Speed", "Builds over time"),
                    ("Cost per click", "None once it is working"), ("Pairs well with", "Google Ads while organic builds")],
        setup_h2="The basics that decide who gets found.",
        setup_items=[
            ("map-pin", "Google Business Profile", "Fully built out with photos, service areas, hours and clear descriptions, because this is what shows up on maps."),
            ("star", "Reviews that say something useful", "A simple way to ask for reviews that mention the work and the suburb, which tells Google what you do and where you do it."),
            ("file-text", "One page per service", "Pages written in the words your customers search, not brochure language."),
            ("gauge", "Speed on mobile", "Fast, clean pages on phones, where many of your visitors arrive."),
            ("mouse-pointer-click", "Calls to action that convert", "Click-to-call buttons, short forms and a clear next step on every page."),
            ("layers", "Structure for search and AI answers", "Structured data and clear page layout so Google and AI assistants can understand what you do and quote you accurately."),
        ],
        expect_h2="What to expect, honestly",
        expect_html="""<p>SEO is not a switch. Changes show up gradually, and the order of work matters: Google Business Profile and reviews first, because they move local results fastest, then the pages and technical work behind them.</p>
<p>We will tell you what we changed, why, and what we are watching. We will not promise a ranking, because nobody can.</p>
<div class="callout"><p><b>Paid ads do not improve organic rankings.</b> Google keeps them separate. If you want results while SEO builds, <a href="/services/google-ads">Google Ads</a> can cover the gap.</p></div>""",
        faqs=[
            ("How long does SEO take?", "It builds over time rather than overnight. Profile and review improvements tend to show first, with page and technical work compounding after that. We will not promise a ranking."),
            ("Do I need a new website?", "Often not. Many sites need clearer service pages, faster loading and better calls to action rather than a rebuild. We tell you honestly if a rebuild would help."),
            ("Is SEO worth it for a local business?", "For businesses people find through Google and Google Maps, a complete profile, useful reviews and clear service pages are some of the most cost-effective things you can do."),
            ("Does this help with AI search tools too?", "Clear page structure, accurate business details and structured data help both Google and AI assistants understand and quote your business correctly."),
        ],
        related=[("/blog/google-for-tradies", "SEO", "How local tradies actually show up on Google", "Reviews, profiles, pages and when ads are worth it."),
                 ("/learn", "DIY guides", "Free marketing guides by industry", "Straight-talking guides for twelve industries."),
                 ("/fractional-marketer", "Package", "Fractional In-House Marketer", "Ongoing SEO, ads and website optimisation in one engagement.")],
    )


# =========================================================== package pages
def _package(slug, *, title, desc, eyebrow, h1, lede, included, facts_rows, steps_h2, steps, suits_h2, suits, faqs, extra_html=""):
    meta = next(p for p in PACKAGES if p[0] == slug)
    url = f"{SITE}/{slug}"
    service_node = {"@type": "Service", "@id": url + "#service", "name": meta[1], "url": url, "description": desc,
                    "provider": {"@id": f"{SITE}/#organization"}, "areaServed": {"@type": "Country", "name": "Australia"}}
    inc = "".join(f'<li class="reveal">{icon("circle-check")}<span>{t}</span></li>' for t in included)
    suit = "".join(f"<li>{icon('check')}{t}</li>" for t in suits)
    main = "\n".join([
        c.page_hero(eyebrow=eyebrow, h1=h1, lede=lede, crumbs=[("Home", "/"), (meta[1], None)],
                    actions=actions(where=f"{slug}-hero", ghost=("What is included", "#included")), visual=c.art(*ART[slug])),
        f'''<section class="section" id="included"><div class="wrap split">
  <div class="reveal"><p class="eyebrow">What is included</p><h2>{meta[1]}, in plain English.</h2><ul class="incl">{inc}</ul></div>
  <div class="reveal">{facts(facts_rows)}</div>
</div></section>''',
        f'<section class="section what"><div class="wrap split"><div class="reveal">{c.section_head("The process", steps_h2)}</div><div class="reveal">{timeline(steps)}</div></div></section>',
        f'<section class="section"><div class="wrap split"><div class="reveal"><p class="eyebrow">Who it suits</p><h2>{suits_h2}</h2><ul class="ticks ticks-dark">{suit}</ul>{extra_html}</div>'
        f'<div class="reveal"><div class="callout"><p><b>Not sure it is the right one?</b> Book the free fit check. We will tell you which package fits, or whether you are better off doing something else first.</p></div></div></div></section>',
        c.faq_section(faqs, heading=f"{meta[1]} questions"),
        c.packages_section(exclude=slug, heading="Compare the other packages", eyebrow="Other ways to work together", sub=""),
        c.cta_band(),
    ])
    page(f"/{slug}", title=title, desc=desc, main=main, crumbs=[("Home", "/"), (meta[1], f"/{slug}")], nodes=[service_node, faq_node(faqs, url)])


def build_packages():
    _package(
        "audit-optimise",
        title="Ads Audit and Optimisation for Small Business | DigiTradie",
        desc="A full audit of your Meta and Google Ads: what works, what wastes budget, and exactly what to fix. Priority fixes applied. Book a free fit check.",
        eyebrow="Audit & Optimise",
        h1="Find out what your ads are <em>actually wasting.</em>",
        lede="A full audit of your Meta and Google Ads accounts: what is working, what is bleeding budget, and exactly what to fix. One call. No lock-in.",
        included=["A full account audit across Meta and Google", "Priority fixes applied, not just a report", "A plain-English dashboard so you can see it yourself", "A walkthrough of what changed and why", "No long-term contract"],
        facts_rows=[("Format", "Once-off"), ("Best for", "Businesses already running ads"), ("Channels", "Meta Ads and Google Ads"), ("Includes", "Dashboard"), ("Commitment", "None beyond the work"), ("Investment", "Confirmed on your fit-check call")],
        steps_h2="From first call to fixed.",
        steps=[("Fit check", "A short call to learn what you are running, what you are spending and what you want ads to do."),
               ("Audit", "We review tracking, campaign structure, targeting, budgets, creative, offers and landing pages across your accounts."),
               ("Fix", "We apply the priority fixes, so you get the benefit and not only a list."),
               ("Walkthrough", "We show you what changed, why, and what to watch. If you want help going further, we can talk about it then.")],
        suits_h2="You are spending, and not sure it is working.",
        suits=["You are running Meta or Google Ads and cannot tell what is working", "Your cost per lead keeps creeping up", "You inherited an account and do not trust the setup", "You want a second opinion before spending more"],
        faqs=[("What do you look at in an audit?", "Conversion tracking, campaign structure, search terms and negative keywords, audiences and placements, budgets against results, ad creative and offers, and the landing pages and forms people arrive on."),
              ("Do you need access to my ad accounts?", "Yes. We request access through each platform&rsquo;s own sharing settings, so you never hand over a password, and you can remove access at any time."),
              ("How much does it cost?", "Exact investment is confirmed on your free fit-check call, because it depends on the size and complexity of your accounts."),
              ("What happens after the audit?", "Many clients take the findings and run things themselves. Others move to Dashboard + Ads Setup or the Fractional In-House Marketer package. There is no pressure either way.")],
    )
    _package(
        "ads-setup",
        title="Meta and Google Ads Setup for Small Business | DigiTradie",
        desc="We set up your Meta and Google Ads, tracking and a plain-English dashboard, then hand it over. Coaching available. Book a free fit check.",
        eyebrow="Dashboard + Ads Setup",
        h1="Get your ads live, <em>built properly, then handed to you.</em>",
        lede="We set up your Meta and Google Ads campaigns and a dashboard you can actually read, then hand it over. Add coaching if you want to learn the tools yourself.",
        included=["Campaigns and tracking built from scratch", "Set and forget handover, or keep us on", "The basics to manage it from your phone", "A plain-English dashboard", "Optional coaching add-on, per session"],
        facts_rows=[("Format", "Once-off"), ("Best for", "Launching, or starting over"), ("Channels", "Meta Ads and Google Ads"), ("Includes", "Dashboard"), ("Add-on", "Coaching sessions"), ("Investment", "Confirmed on your fit-check call")],
        steps_h2="From blank account to handover.",
        steps=[("Fit check", "A short call about your business, your offer, your goal and your budget."),
               ("Plan", "We agree what to run, where and why: channels, offer, targeting, budget and what counts as an enquiry."),
               ("Build", "Accounts, tracking, campaigns, creative direction and your dashboard, built so you can see what is happening."),
               ("Handover", "We walk you through it and teach the basics, so it runs without daily attention and you can check it from your phone."),
               ("Coaching or stay on", "Add coaching sessions to learn the tools, or move to the Fractional In-House Marketer package if you would rather we keep running it.")],
        suits_h2="You want it built right, then you want to run it.",
        suits=["You are launching ads for the first time", "Your current setup is a mess and you want a clean start", "You want to learn enough to handle the basics yourself", "You prefer a once-off cost to a monthly retainer"],
        faqs=[("What does set and forget actually mean?", "It means handed over in a state where it can run without daily attention, with a dashboard that shows when something needs a look. It does not mean no one ever checks it."),
              ("Can I learn to manage the ads myself?", "Yes. We teach the basics as part of the handover, and coaching sessions are available as an add-on if you want to go deeper."),
              ("What do you need from me?", "A clear idea of what you sell and to whom, photos or video of your work where possible, and access to your ad accounts through the platforms&rsquo; own sharing settings."),
              ("What if I want you to keep managing it?", "Then the Fractional In-House Marketer package is the better fit. We can move you across at any point.")],
    )
    _package(
        "fractional-marketer",
        title="Fractional Marketer for Small Business | DigiTradie",
        desc="An in-house marketer without the in-house cost: ongoing Meta Ads, Google Ads, SEO and website optimisation with regular check-ins. Limited spots.",
        eyebrow="Fractional In-House Marketer",
        h1="An in-house marketer, <em>without the in-house cost.</em>",
        lede="Ongoing, hands-on management of your Meta and Google Ads, plus SEO and website optimisation. Reserved for businesses we can genuinely move the needle for, week to week. Limited spots.",
        included=["Ongoing optimisation, not a one-off", "Regular check-ins, so you always know what is happening", "Meta Ads, Google Ads, SEO and website optimisation", "A plain-English dashboard", "3-month minimum, then flexible"],
        facts_rows=[("Format", "Monthly, ongoing"), ("Best for", "Businesses wanting hands-on help"), ("Channels", "Meta, Google, SEO, website"), ("Includes", "Dashboard and check-ins"), ("Commitment", "3-month minimum, then flexible"), ("Investment", "Confirmed on your fit-check call")],
        steps_h2="How an ongoing engagement runs.",
        steps=[("Fit check", "We start with the free call, because spots are limited and we only take on businesses we can help."),
               ("Baseline", "We review what is running now and set the targets we will be measured against."),
               ("Run and optimise", "We manage campaigns, test offers and creative, and keep your site and search presence working harder."),
               ("Check in and adjust", "Regular check-ins at a rhythm we agree with you, with the dashboard showing results in between.")],
        suits_h2="You want the result of a marketing hire, without the hire.",
        suits=["You are spending enough that ongoing management pays for itself", "You want one person accountable for results across channels", "You do not have the time or the in-house skills to run ads well", "You want to see the work, not be handed a black box"],
        extra_html='<p class="why-limited"><b>Why limited spots?</b> You get the person who pitched you, so we only take on as many clients as we can give real attention.</p>',
        faqs=[("What is a fractional in-house marketer?", "Someone who works inside your business part-time, giving you the strategy, ad management and reporting of an in-house marketer without a full-time salary."),
              ("Is there a contract?", "There is a 3-month minimum, then it is flexible. No long-term lock-in."),
              ("Who will actually work on my account?", "The person you speak to on your fit-check call. We would rather take fewer clients than hand your account to someone you have never met."),
              ("How much does it cost?", "Exact investment is confirmed on your fit-check call, because it depends on your ad spend, the channels involved and how much you want us to take on. Ad spend is separate from our fees.")],
    )


# =========================================================== company pages
def build_about():
    principles = feat_grid([
        ("handshake", "A straight answer before a sale", "If we are not the right fit, we say so on the first call. It saves you money and saves us a bad engagement."),
        ("layout-dashboard", "Numbers you can read", "Every package includes a plain-English dashboard, so you can see what your ad spend is doing without asking us."),
        ("users", "Fewer clients, done properly", "You deal with the person who pitched you, not a junior. That only works if we keep the client list small."),
        ("graduation-cap", "Teach, do not gatekeep", "We would rather you understand your ads. That is why we teach the basics and publish free guides for twelve industries."),
    ])
    main = "\n".join([
        c.page_hero(eyebrow="About DigiTradie", h1="Meet Kosta. <em>He runs your account.</em>",
                    lede="DigiTradie is a fractional marketing service for small and medium businesses across Australia. When you book a fit check you speak to Kosta, and if we work together, you still do.",
                    crumbs=[("Home", "/"), ("About", None)], actions=actions(where="about-hero", primary="Book a free fit check", ghost=("Read the case study", "/blog/renovation-leads-case-study")), visual=c.art(*ART["about"])),
        c.founder_card(),
        f'<section class="section what"><div class="wrap">{c.section_head("How we work", "Four rules we do not break.")}{principles}</div></section>',
        f'''<section class="section"><div class="wrap split"><div class="prose reveal"><h2>Experience behind the work</h2>
<p>Kosta Diamantopoulos has worked across global ad agency networks, national telecom and fashion retail brands, and luxury hospitality campaigns, managing $100k+ monthly ad budgets on international accounts.</p>
<p>The same approach has worked closer to home: $500 in ad spend turned into $75k+ profit for a single Melbourne renovation business, by changing the offer rather than cutting the price.</p>
<p>That range is why DigiTradie works for a business spending $50 a day as well as one spending $5,000.</p></div>
<div class="reveal">{facts([("Founder", "Kosta Diamantopoulos"), ("Works with", "Small and medium businesses across Australia"), ("Services", "Meta Ads, Google Ads, SEO, website optimisation"), ("First step", "Free fit check, usually 15 to 20 minutes"), ("Contact", f'<a href="mailto:{EMAIL}">{EMAIL}</a><br><a href="tel:{PHONE_TEL}">{PHONE}</a>')])}</div></div></section>''',
        c.guides_grid(limit=12, heading="Industries we write for", sub="Free DIY guides for twelve industries, written for owners who want to run their own marketing first."),
        c.cta_band(),
    ])
    page("/about", title="About Kosta Diamantopoulos | DigiTradie", desc="Meet Kosta Diamantopoulos, founder of DigiTradie: a fractional marketer for Australian small businesses with global agency and local trade experience.",
         main=main, crumbs=[("Home", "/"), ("About", "/about")], page_type="AboutPage")


FAQ_GROUPS = [
    ("About DigiTradie", HOME_FAQS[0:1] + HOME_FAQS[7:9] + [
        ("Where is DigiTradie based and who do you work with?", "DigiTradie is based in Australia and works with small and medium businesses across the country. Calls and reporting are remote, so location is rarely an issue.")]),
    ("Cost and contracts", [HOME_FAQS[1], HOME_FAQS[3],
        ("Is ad spend included in your fees?", "No. Ad spend is paid to platforms such as Google and Meta and is separate from our fees. We talk through a sensible starting budget with you on the fit-check call.")]),
    ("Working with us", [HOME_FAQS[2], HOME_FAQS[4],
        ("Do you need access to my ad accounts?", "Yes, for the work we do. We request access through each platform&rsquo;s own sharing settings, so you never hand over a password, and you can remove access at any time."),
        ("Who will actually work on my account?", "The person you speak to on your fit-check call. We would rather take fewer clients than hand your account to someone you have never met.")]),
    ("Ads, results and learning", [HOME_FAQS[5], HOME_FAQS[6],
        ("Can you guarantee results?", "No, and be wary of anyone who does. We can promise a clear plan, honest reporting and a dashboard that shows what your ad spend is producing."),
        ("Should I run Meta Ads or Google Ads?", "It depends on how your customers buy. If they search when they need you, Google usually comes first. If they take weeks to decide, Meta usually comes first. Many businesses run both.")]),
]


def build_faq():
    allq = [qa for _, qs in FAQ_GROUPS for qa in qs]
    blocks = "".join(
        f'<div class="faq-group"><h2>{esc(g)}</h2><div class="faq-list">' +
        "".join(f'<details class="faq"><summary><span>{esc(q)}</span>{icon("chevron-down")}</summary><div class="faq-a"><p>{a}</p></div></details>' for q, a in qs) +
        "</div></div>" for g, qs in FAQ_GROUPS)
    main = "\n".join([
        c.page_hero(eyebrow="FAQ", h1="Straight answers to the <em>questions we get asked.</em>",
                    lede="Cost, contracts, the fit-check call and what working together looks like. If your question is not here, ask it on the call.",
                    crumbs=[("Home", "/"), ("FAQ", None)], actions=actions(where="faq-hero")),
        f'<section class="section faqs"><div class="wrap faq-wrap">{blocks}</div></section>',
        c.cta_band(),
    ])
    page("/faq", title="FAQ: Cost, Contracts and the Fit-Check Call | DigiTradie", desc="Answers to common questions about DigiTradie: cost, contracts, the free fit-check call, ad spend, dashboards and who works on your account.",
         main=main, crumbs=[("Home", "/"), ("FAQ", "/faq")], nodes=[faq_node(allq, SITE + "/faq")])


def build_contact():
    steps = timeline([("You send the form", "Takes about a minute. Two quick steps."), ("We get in touch to book a time", "By email or phone, whichever you gave us."), ("One call, usually 15 to 20 minutes", "We tell you straight whether we can help, and which package fits.")])
    main = "\n".join([
        c.page_hero(eyebrow="Get in touch", h1="Let&rsquo;s find out if <em>we&rsquo;re a fit.</em>",
                    lede="One call. We&rsquo;ll tell you straight whether we can help, with no sales pitch and no pressure. If we&rsquo;re not the right fit for your business, we&rsquo;ll say so.",
                    crumbs=[("Home", "/"), ("Contact", None)]),
        f'''<section class="section"><div class="wrap split">
  <div class="reveal"><p class="eyebrow">What happens next</p><h2>Simple, and no obligation.</h2>{steps}
    <div class="callout"><p><b>Prefer to reach out directly?</b><br><a href="mailto:{EMAIL}" data-track="email">{EMAIL}</a><br><a href="tel:{PHONE_TEL}" data-track="phone">{PHONE}</a></p></div></div>
  <div class="reveal">{form("contact-form", source="contact-page", heading="Book your free fit check")}</div>
</div></section>''',
        c.faq_section([HOME_FAQS[1], HOME_FAQS[2], HOME_FAQS[3], HOME_FAQS[4]], heading="Before you book"),
    ])
    page("/contact", title="Contact DigiTradie | Book a Free Fit Check", desc="Book a free fit check with DigiTradie. One call, usually 15 to 20 minutes, and a straight answer on whether we can help your business.",
         main=main, crumbs=[("Home", "/"), ("Contact", "/contact")], page_type="ContactPage", nodes=[faq_node([HOME_FAQS[1], HOME_FAQS[2], HOME_FAQS[3], HOME_FAQS[4]], SITE + "/contact")])


def build_thanks():
    steps = timeline([("We read your details", "Your request has landed in our inbox."), ("We get in touch to book your call", "By email or phone, usually to find a time that suits you."), ("One call, usually 15 to 20 minutes", "We tell you straight whether we can help.")])
    conv = (f"gtag('event','conversion',{{send_to:'{AW}/{ADS_CONVERSION_LABEL}'}});" if ADS_CONVERSION_LABEL else "")
    script = f"""<script>
(function(){{var k='dt_lead_sent';try{{if(sessionStorage.getItem(k))return;sessionStorage.setItem(k,'1')}}catch(e){{}}
if(window.dtLoadGtag)dtLoadGtag();
gtag('event','generate_lead',{{method:'fit_check_form',currency:'AUD'}});{conv}}})();
</script>"""
    main = "\n".join([
        c.page_hero(eyebrow="Enquiry received", h1="Thanks. <em>We&rsquo;ve got it.</em>",
                    lede="Your fit-check request just landed in our inbox. We&rsquo;ll be in touch shortly to book your call.", crumbs=None),
        f'''<section class="section"><div class="wrap split">
  <div class="reveal"><p class="eyebrow">What happens next</p><h2>Three steps.</h2>{steps}</div>
  <div class="reveal"><div class="callout"><p><b>While you wait,</b> have a look at how we work or read a couple of things we have learned running campaigns.</p></div>
  <div class="hero-actions"><a class="btn btn-primary" href="/#how">How it works</a><a class="btn btn-ghost" href="/blog/renovation-leads-case-study">Read the case study</a><a class="btn btn-ghost" href="/learn">Free guides</a></div></div>
</div></section>{script}''',
    ])
    page("/thank-you", title="Thanks, we've got your request | DigiTradie", desc="Your fit-check request has been received.", main=main, robots="noindex,follow")


def build_privacy():
    main = "\n".join([
        c.page_hero(eyebrow="Privacy", h1="Privacy policy", lede="What DigiTradie collects, why, and who sees it. Short and plain.", crumbs=[("Home", "/"), ("Privacy", None)]),
        f'''<section class="section"><div class="wrap"><div class="prose">
<p><b>Last updated:</b> 30 October 2026.</p>
<h2>Who we are</h2><p>DigiTradie is a marketing service for small and medium businesses in Australia, run by Kosta Diamantopoulos. You can contact us at <a href="mailto:{EMAIL}">{EMAIL}</a> or on <a href="tel:{PHONE_TEL}">{PHONE}</a>.</p>
<h2>What we collect</h2><ul>
<li><b>Details you give us.</b> When you complete the fit-check form: your name, business name, email, phone number, what you need and your approximate monthly ad spend.</li>
<li><b>Where you came from.</b> The page you landed on, the site that referred you, and campaign details such as UTM tags or an ad click ID, so we can see which ads or searches bring enquiries.</li>
<li><b>Site usage.</b> Anonymous information about how the site is used, such as pages viewed, device type and approximate location, collected through Google Analytics and the Google Ads tag.</li></ul>
<h2>How we use it</h2><p>To reply to your enquiry and run your fit-check call, to understand which marketing brings enquiries, and to improve this website. We do not sell your details.</p>
<h2>Who else handles it</h2><ul>
<li><b>Formspree</b> receives form submissions and forwards them to us by email.</li>
<li><b>Google</b> (Analytics and Ads) receives site usage information through cookies and tags, under its own privacy policy.</li>
<li><b>Vercel</b> hosts this website.</li></ul>
<h2>Cookies</h2><p>Google Analytics and the Google Ads tag set cookies to measure visits and ad performance. You can block or delete cookies in your browser settings.</p>
<h2>Your choices</h2><p>You can ask us to show, correct or delete the personal information we hold about you by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Changes</h2><p>If this policy changes, the date above will change with it.</p></div></div></section>''',
    ])
    page("/privacy", title="Privacy Policy | DigiTradie", desc="What DigiTradie collects when you use this website or book a fit check, how it is used, and who else handles it.", main=main,
         crumbs=[("Home", "/"), ("Privacy", "/privacy")], robots="index,follow")


def build_404():
    from .core import head, header, footer, write_page, ROOT
    h = head(title="Page not found | DigiTradie", desc="That page could not be found.", path="/404", robots="noindex,follow")
    main = f"""<section class="phero phero-dark"><div class="phero-bg" aria-hidden="true"><span class="grid"></span><span class="sparks"></span></div>
<div class="wrap phero-in"><div class="phero-copy"><p class="chip"><span class="dot"></span>Error 404</p><h1>That page has <em>gone missing.</em></h1>
<p class="lede">The link may be old or mistyped. Here is where most people want to go.</p>
<div class="hero-actions"><a class="btn btn-glow" href="/">Back to the homepage</a><a class="btn btn-ghost" href="/contact">Book a fit check</a><a class="btn btn-ghost" href="/learn">Free guides</a></div></div></div><div class="tape" aria-hidden="true"></div></section>"""
    body = header() + f'<main id="main">{main}</main>' + footer()
    (ROOT / "404.html").write_text(h + body)
