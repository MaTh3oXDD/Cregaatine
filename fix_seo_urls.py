# -*- coding: utf-8 -*-
"""Przywraca absolutne URL-e tam, gdzie SEO ich wymaga, i generuje
robots.txt + sitemap.xml dla statycznego mirrora."""
import os, re, glob, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")
BASE = "https://cregaatine.pl"

def absolutize(html):
    # canonical
    html = re.sub(r'(<link rel="canonical" href=")(/[^"]*)"',
                  lambda m: m.group(1) + BASE + m.group(2) + '"', html)
    # og:url
    html = re.sub(r'(<meta property="og:url" content=")(/[^"]*)"',
                  lambda m: m.group(1) + BASE + m.group(2) + '"', html)
    # JSON-LD: "@id":"/...", "url":"/...", "target":["/..."], urlTemplate
    def json_fix(m):
        body = m.group(2)
        body = re.sub(r'"(@id|url|urlTemplate)":"(/[^"]*)"',
                      lambda n: f'"{n.group(1)}":"{BASE}{n.group(2)}"', body)
        body = re.sub(r'"target":\["(/[^"]*)"\]',
                      lambda n: f'"target":["{BASE}{n.group(1)}"]', body)
        return m.group(1) + body + m.group(3)
    html = re.sub(r'(<script type="application/ld\+json"[^>]*>)(.*?)(</script>)',
                  json_fix, html, flags=re.S)
    return html

pages = []
for path in sorted(glob.glob(os.path.join(SITE, "**", "index.html"), recursive=True)):
    html = open(path, encoding="utf-8").read()
    fixed = absolutize(html)
    if fixed != html:
        open(path, "w", encoding="utf-8").write(fixed)
        print("naprawiono:", os.path.relpath(path, SITE))
    rel = os.path.relpath(os.path.dirname(path), SITE).replace("\\", "/")
    url = BASE + "/" if rel == "." else f"{BASE}/{rel}/"
    # archiwa i duplikat poza sitemapą
    if any(x in url for x in ("/author/", "/category/uncategorized/", "/dawka-wiedzy-naukowej/")):
        continue
    pages.append(url)

today = datetime.date.today().isoformat()
entries = "\n".join(
    f"  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>" for u in sorted(pages))
open(os.path.join(SITE, "sitemap.xml"), "w", encoding="utf-8").write(
    f'<?xml version="1.0" encoding="UTF-8"?>\n'
    f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{entries}\n</urlset>\n')

open(os.path.join(SITE, "robots.txt"), "w", encoding="utf-8").write(
    f"User-agent: *\nDisallow:\n\nSitemap: {BASE}/sitemap.xml\n")

print(f"sitemap.xml: {len(pages)} URL-i, robots.txt zapisany")
