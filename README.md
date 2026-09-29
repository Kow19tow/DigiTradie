# DigiTradie

Landing page — plain HTML/CSS, no build step, deploys to Vercel as-is.

## Deploy

1. Push this repo to GitHub.
2. In Vercel: New Project → import the GitHub repo → deploy (no config needed, it's a static site).
3. In Squarespace DNS, remove only the **Squarespace Defaults** A records and `www` CNAME, then add the A/CNAME records Vercel gives you. Leave MX records alone — that's what runs Google Workspace email.

## Updating the /learn guides

The `/learn` section (the DIY marketing guides, one per industry) is generated from a Word
document — you never hand-edit the guide HTML directly.

**Source of truth:** `content/learn/DigiTradie Industry Guides.docx`

**To update a guide, or add a new industry:**

1. Open `content/learn/DigiTradie Industry Guides.docx` and edit it. Keep the existing structure:
   - `Heading 2` starts a new guide — must say "How to market a &lt;industry&gt;" for the page
     title to generate correctly.
   - `Heading 3` starts a subsection within that guide.
   - A `Heading 3` titled exactly **FAQs** is special — write it as alternating plain paragraphs:
     question, answer, question, answer. These become the on-page accordion and the FAQ schema
     Google reads.
   - Bullet points use Word's normal bullet list style.
   - Lines starting with a checkbox character (☐) become the "Do this week" task list.
   - Adding a brand-new industry: just add a new `Heading 2` section following the same pattern.
     It'll get a generic URL slug automatically — open `build.py` and add it to `INDUSTRY_MAP` near
     the top if you want a specific URL slug or a shorter menu label instead.

2. Regenerate the pages:

   ```bash
   pip3 install --user python-docx   # first time only
   python3 build.py
   ```

   This rewrites everything under `/learn/`, and merges the `/learn` URLs into `sitemap.xml`
   automatically (it won't touch any other page's entries).

3. Check what changed, then commit and push as normal:

   ```bash
   git status
   git add learn/ sitemap.xml content/learn/
   git commit -m "Update learn guides"
   git push
   ```

There's no npm/Node involved anywhere in this repo — `build.py` is a plain Python script, run
directly.
