# Security

DigiTradie is a static website (no database, no logins, no server code). The only moving parts are the lead form, which posts to Formspree, and Google's analytics and ads tags.

**Report a problem:** email digitradieau@gmail.com (also published at `/.well-known/security.txt`).

## How the 50-point "vibe-coded app" checklist applies

Status: **Fixed** = changed in this repo. **OK** = already safe, verified. **N/A** = the thing does not exist on this site. **Action** = needs you in an account dashboard.

| # | Checklist item | Status | Detail |
|---|---|---|---|
| 1 | Exposed database credentials | N/A / OK | No database. Working tree and full git history scanned: no credentials. |
| 2 | Public .env files | OK | None exist. `.vercelignore` blocks build files; live probes of `/.env`, `/.git/config` return 404. |
| 3 | Hardcoded API keys | OK | Only public IDs ship (GA4 `G-…`, Ads `AW-…`, Formspree form ID), which are public by design. No secret keys anywhere. |
| 4 | Weak or missing authentication | N/A | No logins. **Action:** turn on 2-step verification for GitHub, Vercel, Google, Formspree and Squarespace. |
| 5 | No authorization checks | N/A | No protected data. |
| 6 | Users can reach other users' data | N/A | No user accounts. |
| 7 | Open database read/write | N/A | No database. |
| 8 | Misconfigured Firebase / Supabase / S3 | N/A | Not used. |
| 9 | Admin routes unprotected | OK | None exist. |
| 10 | Debug pages in production | Fixed | Social-post sources, build scripts and docs were publicly reachable; now excluded from deploys. |
| 11 | Build logs leaking secrets | OK | The build uses no secrets or environment variables. |
| 12 | Verbose error messages | OK | Static pages and a plain custom 404. No stack traces exist. |
| 13 | Leaked GitHub repos / commit history | OK | History scanned clean. Repo visibility is an **Action** item (see below). |
| 14 | Secrets in frontend JavaScript | OK | `src/site.js` holds no keys. |
| 15 | Client-side-only security checks | OK | Form checks are convenience only; Formspree validates server-side. Nothing is gated in the browser. |
| 16 | Missing input validation | Fixed | Length limits, phone and email formats, honeypot field, URL tracking values cleaned to a safe character set. |
| 17 | SQL injection | N/A | No database. |
| 18 | NoSQL injection | N/A | No database. |
| 19 | Cross-site scripting | Fixed | No `innerHTML`/`eval`; all generated text escaped; JSON-LD cannot break out of its tag; strict CSP only runs our own scripts (matched by SHA-256 hash). |
| 20 | CSRF | N/A | No cookie-authenticated actions. Form targets restricted by CSP `form-action`. |
| 21 | Insecure file uploads | N/A | No uploads. |
| 22 | Path traversal | N/A | Static files; the build writes only fixed paths. |
| 23 | SSRF | N/A | No server code. |
| 24 | Broken password reset | N/A | No passwords. |
| 25 | Weak session management | N/A | No sessions. Only campaign IDs sit in `sessionStorage`. |
| 26 | JWT secrets | N/A | No tokens. |
| 27 | Overly permissive CORS | Fixed | Vercel's default `Access-Control-Allow-Origin: *` is overridden to this site only. |
| 28 | Rate limits | Fixed / Action | Vercel's firewall challenges scanner-like bursts (observed). Form has a honeypot. **Action:** in Formspree, restrict allowed domains and enable spam protection (see below). |
| 29 | Public test / staging environments | OK | Vercel previews sit behind login (verified). Merged `redesign` branch removed. |
| 30 | Default credentials unchanged | N/A | **Action:** use unique passwords plus 2-step verification on every account. |
| 31 | Webhooks without signatures | N/A | None. |
| 32 | Payment checks only on frontend | N/A | No payments. |
| 33 | IDOR | N/A | No object IDs. |
| 34 | API trusts user-controlled IDs/roles | N/A | No API. |
| 35 | Logs with tokens, emails, passwords | OK | Analytics events carry no name, email or phone. Form details only go to Formspree and your inbox. |
| 36 | Source maps in production | OK | None generated; live probe returns 404. |
| 37 | Dependency vulnerabilities | OK | Zero runtime dependencies (no npm packages or CDN libraries; fonts and icons are self-hosted). Build tools pinned in `requirements.txt` and watched by Dependabot. |
| 38 | Outdated packages | OK | Dependabot checks weekly (pip and GitHub Actions). |
| 39 | Prompt injection in AI features | N/A | The site has no AI features. |
| 40 | AI actions without permission checks | N/A | None. |
| 41 | Excessive database permissions | N/A | No database. |
| 42 | No audit logs | OK | Git history records every change; Vercel keeps a deployment history; GitHub keeps account audit logs. |
| 43 | No monitoring or alerting | Fixed | `site-monitor.yml` runs every 6 hours: uptime, content, headers, TLS expiry, exposed files. Failures email the repo owner. Search Console also emails indexing and security issues. |
| 44 | No backup or restore plan | Fixed | Weekly full-repo backup artifact (`backup.yml`, kept 90 days) plus the runbook below. |
| 45 | Publicly exposed internal dashboards | OK | None. The planned client dashboard must require login when built. |
| 46 | Missing security headers | Fixed | HSTS, CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, COOP, cross-domain policy (see `vercel.json`). |
| 47 | Cookies missing HttpOnly/Secure/SameSite | OK | The site sets no cookies of its own. Google's analytics cookies are set `Secure; SameSite=Lax`. (Cookies written by JavaScript cannot be HttpOnly.) |
| 48 | Unencrypted sensitive data | OK | HTTPS only with HSTS; Formspree is reached over HTTPS; CSP upgrades any stray http. |
| 49 | Poor tenant isolation | N/A | No multi-user app. |
| 50 | Over-trusting generated code | Fixed | Independent security review of the generator and browser code (7 findings, all fixed) plus automated tests: CSP violation test across every page type, link/anchor/schema audit, Lighthouse. |

## Recovery runbook

Everything needed to rebuild the site is in this repository.

1. **Bad deploy:** Vercel dashboard, Deployments, pick the last good one, "Instant Rollback". Or `git revert <commit>` and push.
2. **Whole site lost or defaced:** `git clone` the repo (or restore `digitradie-backup.bundle` from the latest Actions "Weekly backup" artifact: `git clone digitradie-backup.bundle site`), then `python3 build.py` and push `main`. Tag `pre-redesign-2026-10-30` is the previous design.
3. **Vercel project lost:** import the GitHub repo into a new Vercel project (framework: Other, no build command, output directory: root), then add the domain `www.digitradie.com`.
4. **DNS records to restore** (never remove the Google Workspace MX records or verification TXT records):
   - `MX` aspmx.l.google.com (1), alt1/alt2.aspmx.l.google.com (5), alt3/alt4.aspmx.l.google.com (10)
   - `TXT` SPF: `v=spf1 include:_spf.google.com include:spf.instantly.ai ~all`
   - `TXT` `_dmarc`: `v=DMARC1; p=quarantine; rua=mailto:admin@digitradie.com`
   - `TXT` two `google-site-verification=…` records (leave as they are)
   - `CNAME` www to `cname.vercel-dns.com`; apex `A` to Vercel's address shown in the Vercel domain settings
5. **Leads:** Formspree keeps submissions; turn on email forwarding there as well.

## Account settings to check (cannot be done from code)

- 2-step verification on GitHub, Vercel, Google (Workspace, Ads, Analytics), Formspree, Squarespace Domains.
- GitHub: secret scanning and push protection on; consider making the repository private (Vercel keeps deploying private repos).
- Formspree: allowed domains set to `www.digitradie.com`; spam filter / reCAPTCHA on.
- Google Ads and GA4: automatic form-data collection and automatic enhanced conversions off (otherwise the form's email and phone would be hashed and sent to Google).
- Google Workspace: set up DKIM signing (Admin console, Apps, Gmail, Authenticate email) to complement SPF and DMARC.
