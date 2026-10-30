"""Homepage."""
from . import components as c
from .core import faq_node, page, SITE

HOME_FAQS = [
    ("What is a fractional in-house marketer?",
     "A fractional marketer works inside your business part-time. You get the strategy, ad management and reporting of an in-house marketer without a full-time salary. At DigiTradie that means Meta Ads, Google Ads, SEO and website optimisation, handled by the same person you speak to on your first call."),
    ("How much does DigiTradie cost?",
     "There are three packages: a once-off audit, a once-off ads setup, and an ongoing monthly engagement. Exact investment depends on your ad spend, the channels involved and how much you want us to take on, so we confirm it on your free fit-check call instead of guessing on a web page. Your ad spend is separate from our fees."),
    ("What happens on the fit-check call?",
     "It is one call, usually 15 to 20 minutes. We learn about your business, what you are spending and what you want ads to do. Then we tell you straight whether we can help, which package fits, or whether you would be better off doing something else first. There is no obligation."),
    ("Do you lock clients into contracts?",
     "No long-term lock-in. The once-off packages finish when the work is done. The monthly Fractional In-House Marketer package has a 3-month minimum, then it is flexible."),
    ("Which businesses are a good fit?",
     "Businesses launching ads for the first time, spending on ads without being able to tell what is working, or wanting in-house marketing help without a full-time hire. If you want the cheapest option, a black box, or a big agency with layers of account managers, we are probably not the right fit, and we will say so."),
    ("Will I be able to see results myself?",
     "Yes. Every package includes a plain-English dashboard you can open any time, including on your phone. It shows leads, cost per lead and spend, with a short note on what changed and why."),
    ("Can I learn to run ads myself?",
     "Yes. We can set everything up and hand it over with the basics so you can manage it yourself, and coaching sessions are available as an add-on. Our free industry guides also cover the DIY basics."),
    ("Do you only work with tradies?",
     "No. Despite the name, DigiTradie works with small and medium businesses across industries, including hospitality, retail, beauty, gyms, dental, law, accounting, health, mechanics and solar. There is a free guide for each."),
    ("Which platforms and channels do you work on?",
     "Primarily Meta Ads (Facebook and Instagram) and Google Ads. We also help with SEO and website optimisation so the traffic you pay for turns into enquiries."),
]


def build_home():
    url = SITE + "/"
    main = "\n".join([
        c.home_hero(),
        c.stats_band(),
        c.services_bento(),
        c.fit_section(),
        c.how_section(),
        c.dashboard_section(),
        c.case_teaser(),
        c.packages_section(),
        c.founder_card(),
        c.guides_grid(),
        c.faq_section(HOME_FAQS),
        c.cta_band(),
    ])
    page("/",
         title="Fractional Marketing for Australian Small Business | DigiTradie",
         desc="Fractional in-house marketing for Australian small businesses: Meta Ads, Google Ads, SEO and a plain-English dashboard. Book a free fit check.",
         main=main,
         nodes=[faq_node(HOME_FAQS, url)],
         og_image=f"{SITE}/og/home.jpg",
         page_type="WebPage")
