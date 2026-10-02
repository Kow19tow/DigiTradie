# Social graphics

One folder per post. Each has:

- `source/post.html` - the design (HTML/CSS). Layout is picked by the URL hash: `#portrait`, `#square`, `#landscape`.
- `source/render.sh` - re-renders every size into `exports/` (needs Google Chrome and `pip3 install --user pillow`).
- `exports/` - `portrait` 1080x1350 (Instagram), `square` 1080x1080, `landscape` 1200x630 (website / link previews). Each also has an `@2x.png`.

To change wording or colours: edit `source/post.html`, then run `bash social/<post>/source/render.sh`.

Website-ready JPGs of the exports live in `/images`.

Brand: navy `#30405C`, orange `#EC702E` (from the logo). Fonts: Bricolage Grotesque + Figtree (same as the site).
