# Social graphics

One folder per post. Every post has `source/post.html` (the design) and `exports/` (rendered PNGs: `portrait` 1080x1350 for Instagram, `square` 1080x1080, `landscape` 1200x630 for the website and link previews, each also as `@2x`).

| Post | Source content | Look |
|---|---|---|
| `renovation-case-study` | blog/renovation-leads-case-study | indigo, stat + growth bars (original, self-contained) |
| `ai-do-dont` | blog/tradies-and-ai | indigo, split cards |
| `week-checklist` | learn/tradie-marketing "Do this week" | charcoal, clipboard checklist |
| `urgent-vs-considered` | learn/tradie-marketing | navy, decision paths |
| `review-example` | blog/google-for-tradies | indigo, annotated review (labelled as an example) |
| `not-a-fit` | homepage "Good fit / Probably not a fit" | charcoal, good fit vs not a fit |

## Re-render after editing a post

```bash
bash social/render.sh ai-do-dont          # one post (all three sizes)
bash social/render.sh all                 # every post that uses the shared base
bash social/renovation-case-study/source/render.sh   # the original post has its own script
python3 social/export_web.py              # refresh the web JPGs in /images
```

Needs Google Chrome and `pip3 install --user pillow`. Layout is chosen by the URL hash on `post.html` (`#portrait`, `#square`, `#landscape`).

## Making a new post

Copy a similar folder, edit `source/post.html` (it uses `_shared/base.css` + `_shared/base.js`, so the logo, background, stars, hazard tape and top row come for free), run `render.sh`, then `export_web.py`. Pick a theme with `theme-indigo`, `theme-charcoal` or `theme-navy` on the `.post` element. Only use claims that are on the site; do not invent stats.

## Where they're used on the website

- `blog/renovation-leads-case-study`, `blog/google-for-tradies`, `blog/tradies-and-ai`: hero image + link preview + schema image.
- `learn/tradie-marketing`: hero image + link preview (set in `GUIDE_IMAGES` in `build.py`).
- `contact`: link preview only.

Brand: navy `#30405C`, orange `#EC702E` (from the logo). Fonts: Bricolage Grotesque + Figtree (same as the site).
