# -*- coding: utf-8 -*-
import json
import os
import common

ROOT = os.path.dirname(os.path.abspath(__file__))

def esc(t):
    return (t or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

ARCHIVES = [
    {"json": "blog", "out": "blog", "heading": "Blog", "eyebrow": "Baza wiedzy", "next": None},
    {"json": "author-marcin", "out": "author/marcincarno-med-pl", "heading": "Wpisy autora: marcin@carno-med.pl", "eyebrow": "Autor", "next": "/author/marcincarno-med-pl/page/2/"},
    {"json": "author-marcin-p2", "out": "author/marcincarno-med-pl/page/2", "heading": "Wpisy autora: marcin@carno-med.pl", "eyebrow": "Autor · strona 2", "next": None, "prev": "/author/marcincarno-med-pl/"},
    {"json": "category-promo", "out": "category/promo", "heading": "Kategoria: promo", "eyebrow": "Kategoria", "next": None},
    {"json": "category-uncategorized", "out": "category/uncategorized", "heading": "Kategoria: Uncategorized", "eyebrow": "Kategoria", "next": "/category/uncategorized/page/2/"},
    {"json": "category-uncategorized-p2", "out": "category/uncategorized/page/2", "heading": "Kategoria: Uncategorized", "eyebrow": "Kategoria · strona 2", "next": None, "prev": "/category/uncategorized/"},
]

for a in ARCHIVES:
    data = json.load(open(os.path.join(ROOT, "extracted", a["json"] + ".json"), encoding="utf-8"))
    cards = data.get("cards") or []
    card_html = ""
    for c in cards:
        date, cats = None, None
        if c.get("excerpt"):
            parts = [p.strip() for p in c["excerpt"].split("|")]
            date = parts[1] if len(parts) > 1 else None
        meta = f'<span class="blog-meta">{esc(date)}</span>' if date else ""
        card_html += f"""      <a class="blog-card" href="{c['href']}">
        <div class="thumb"><img src="{c['image']}" alt="{esc(c['title'])}" loading="lazy"></div>
        <div class="body">
          {meta}
          <h3>{esc(c['title'])}</h3>
          <span class="read-more">czytaj więcej</span>
        </div>
      </a>
"""
    pag = ""
    if a.get("next") or a.get("prev"):
        pag = '<div class="pagination">'
        if a.get("prev"):
            pag += f'<a href="{a["prev"]}">&larr; poprzednia</a>'
        if a.get("next"):
            pag += f'<a href="{a["next"]}">następna &rarr;</a>'
        pag += "</div>"

    body = f"""
<div class="archive-hero">
  <div class="container">
    <span class="eyebrow">{esc(a['eyebrow'])}</span>
    <h1 style="margin-top:0.6rem;">{esc(a['heading'])}</h1>
  </div>
</div>
<section class="section">
  <div class="container">
    <div class="blog-grid">
{card_html}    </div>
    {pag}
  </div>
</section>
"""
    html = common.page(
        title=data.get("title") or a["heading"],
        description=data.get("meta_description") or "",
        body=body,
        canonical_path="/" + a["out"] + "/",
    )
    out_dir = os.path.join(ROOT, "site", a["out"])
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", out_path, len(cards), "cards")
