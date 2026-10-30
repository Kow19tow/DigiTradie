# DigiTradie website

Static site, deployed on Vercel from the `main` branch of this repo. Domain: https://www.digitradie.com

## Change something

Everything is rebuilt by one command:

```bash
python3 build.py
```

Then check `git status`, commit and push. Vercel deploys `main` automatically.

| I want to change | Edit this | Then |
|---|---|---|
| A /learn guide | `content/learn/DigiTradie Industry Guides.docx` | `python3 build.py` |
| A blog post | `content/blog/<slug>.html` (text) and `content/blog/posts.json` (title, description, date) | `python3 build.py` |
| Homepage copy, FAQs | `lib/pages_home.py`, `lib/components.py` | `python3 build.py` |
| Service, package, about, FAQ, contact, privacy pages | `lib/pages_main.py` | `python3 build.py` |
| Header, footer, lead form, schema, tracking | `lib/core.py` | `python3 build.py` |
| Colours, fonts, layout | `src/site.css` | `python3 build.py` |
| Site behaviour (menu, form steps, events) | `src/site.js` | `python3 build.py` |

Needs: Python 3, `pip3 install --user python-docx pillow`, and Google Chrome (draws the share images).

## What the build writes

`index.html` and every page folder, `404.html`, `assets/site.<hash>.css|js` (cache-busted automatically), `og/*.jpg` (share image per page), `sitemap.xml`, `robots.txt`, `llms.txt`, `llms-full.txt`, `feed.xml`, `vercel.json`, `.vercelignore`.
Do not hand-edit those files; edit the sources above.

## Tracking

- GA4 `G-N0PS84JLP6` and Google Ads `AW-18469638617` load after the page is interactive (see `GTAG_LOADER` in `lib/core.py`).
- Events sent: `form_start`, `form_step_complete`, `form_submit`, `cta_click`, `phone_click`, `email_click`, and `generate_lead` on `/thank-you`.
- To count Google Ads conversions, create a conversion action in Google Ads, copy its label and paste it into `ADS_CONVERSION_LABEL` in `lib/core.py`, then rebuild.
- Each form submission carries utm_*, gclid, landing page and referrer, so the email from Formspree shows which ad or search produced the lead.

## Other folders

- `social/` social post designs and renderer (see `social/README.md`). Web copies of the posts live in `images/`.
- `brand/` logo concept explorations. Not deployed.
- `Tool Icons/` source icons (CC BY 3.0, game-icons.net). Credited in the site footer. Not deployed.
- Rollback point for the pre-redesign site: git tag `pre-redesign-2026-10-30`.
