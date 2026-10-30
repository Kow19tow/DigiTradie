#!/usr/bin/env python3
"""Health and security check for https://www.digitradie.com. Standard library only.
Run by GitHub Actions every 6 hours (.github/workflows/site-monitor.yml); GitHub emails the repo owner if it fails.
Run it yourself any time:  python3 scripts/monitor.py
Keeps the request count low on purpose (Vercel's firewall challenges scanner-like bursts)."""
import re
import socket
import ssl
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

SITE = "https://www.digitradie.com"
UA = {"User-Agent": "DigiTradie-site-monitor/1.0 (+https://www.digitradie.com/.well-known/security.txt)"}
problems = []


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def get(url, follow=True):
    opener = urllib.request.build_opener() if follow else urllib.request.build_opener(NoRedirect)
    req = urllib.request.Request(url, headers=UA)
    try:
        with opener.open(req, timeout=20) as r:
            return r.status, dict(r.headers), r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), ""
    except Exception as e:  # network trouble
        return 0, {}, str(e)


def check(ok, msg):
    print(("ok    " if ok else "FAIL  ") + msg)
    if not ok:
        problems.append(msg)


status, hdr, body = get(SITE + "/")
h = {k.lower(): v for k, v in hdr.items()}
if status == 403 and h.get("x-vercel-mitigated") == "challenge":
    print("WARN  Vercel's firewall is challenging this runner's IP, so the site cannot be checked from here right now. Not treating it as an outage.")
    sys.exit(0)
check(status == 200, f"home returns 200 (got {status})")
check("DigiTradie" in body and "fit check" in body.lower(), "home has expected content (not defaced or blank)")
check("content-security-policy" in h and "frame-ancestors" in h.get("content-security-policy", ""), "CSP header present")
check("strict-transport-security" in h, "HSTS header present")
check(h.get("x-content-type-options") == "nosniff", "X-Content-Type-Options nosniff")
check(h.get("x-frame-options", "").upper() in ("DENY", "SAMEORIGIN"), "X-Frame-Options set")
hosts = set(re.findall(r'<script[^>]+src="https?://([^/"]+)', body))
check(hosts <= {"www.googletagmanager.com"}, f"only expected third-party scripts on home (found {sorted(hosts) or 'none'})")
check(re.search(r'action="https://formspree\.io/f/[a-z0-9]+"', body) is not None, "lead form still posts to Formspree")

s, _, b = get(SITE + "/sitemap.xml")
check(s == 200 and "<urlset" in b and b.count("<loc>") >= 25, f"sitemap OK ({b.count('<loc>')} urls)")
s, _, _ = get(SITE + "/thank-you")
check(s == 200, f"/thank-you returns 200 (got {s})")
s, _, b = get(SITE + "/.well-known/security.txt")
check(s == 200 and "Contact:" in b, "security.txt reachable")
s, _, _ = get("https://digitradie.com/", follow=False)
check(s in (301, 307, 308), f"apex redirects to www (got {s})")

for path in ("/build.py", "/lib/core.py", "/.git/config", "/content/blog/posts.json"):
    s, _, _ = get(SITE + path)
    check(s in (403, 404), f"{path} is not downloadable (got {s})")
    time.sleep(1)

try:
    ctx = ssl.create_default_context()
    with socket.create_connection(("www.digitradie.com", 443), timeout=15) as sock:
        with ctx.wrap_socket(sock, server_hostname="www.digitradie.com") as tls:
            exp = datetime.strptime(tls.getpeercert()["notAfter"], "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
    days = (exp - datetime.now(timezone.utc)).days
    check(days > 14, f"TLS certificate valid for {days} more days")
except Exception as e:
    check(False, f"TLS check failed: {e}")

if problems:
    print(f"\n{len(problems)} problem(s):")
    for p in problems:
        print(" -", p)
    sys.exit(1)
print("\nAll checks passed.")
