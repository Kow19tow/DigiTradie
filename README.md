# DigiTradie

Landing page — plain HTML/CSS, no build step, deploys to Vercel as-is.

## Deploy

1. Push this repo to GitHub.
2. In Vercel: New Project → import the GitHub repo → deploy (no config needed, it's a static site).
3. In Squarespace DNS, remove only the **Squarespace Defaults** A records and `www` CNAME, then add the A/CNAME records Vercel gives you. Leave MX records alone — that's what runs Google Workspace email.
