# -*- coding: utf-8 -*-
import json
import os
import re
import common

ROOT = os.path.dirname(os.path.abspath(__file__))

POSTS = [
    {"json": "cregaatine-naukowa-rewolucja-kreatyny", "slug": "cregaatine-naukowa-rewolucja-kreatyny"},
    {"json": "gaa-i-kreatyna-badania-naukowe", "slug": "gaa-i-kreatyna-badania-naukowe"},
    {"json": "dawka-wiedzy-naukowej", "slug": "dawka-wiedzy-naukowej"},
    {"json": "wyklad-pionier", "slug": "wyklad-pionier-w-badaniu-kreatyny-i-gaa-prof-sergej-ostojic"},
    {"json": "prof-ostojic-czesc-1", "slug": "prof-dr-sergej-ostojic-odpowiada-na-pytania-dotyczace-cregaatine-czesc-1"},
    {"json": "karnozyna", "slug": "karnozyna-w-miesniach-sportowca"},
    {"json": "potrojna-suplementacja", "slug": "potrojna-suplementacja-karnozyna-gaa-i-kreatyna"},
    {"json": "suplement-roku-fiwe", "slug": "suplement-roku-fiwe"},
    {"json": "aa", "slug": "aa"},
]

def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def parse_byline(excerpt):
    # "utworzone przez marcin@carno-med.pl | kwi 7, 2021 | promo , Uncategorized | 0 komentarzy"
    if not excerpt:
        return None, None
    parts = [p.strip() for p in excerpt.split("|")]
    date = parts[1] if len(parts) > 1 else None
    cats = parts[2] if len(parts) > 2 else None
    return date, cats

def render_flow(flow):
    out = []
    for b in flow:
        t = b["type"]
        if t in ("h1", "h2", "h3", "h4", "h5", "h6"):
            tag = "h2" if t in ("h1", "h2") else ("h3" if t == "h3" else "h4")
            out.append(f"<{tag}>{esc(b['text'])}</{tag}>")
        elif t == "p":
            out.append(f"<p>{esc(b['text'])}</p>")
        elif t in ("ul", "ol"):
            items = "".join(f"<li>{esc(i)}</li>" for i in b["items"])
            out.append(f"<{t}>{items}</{t}>")
        elif t == "img":
            out.append(f'<img src="{b["src"]}" alt="{esc(b.get("alt","") or "")}" loading="lazy">')
        elif t == "video":
            out.append(f'<div class="video-frame"><iframe src="{b["src"]}" title="{esc(b.get("title","") or "")}" loading="lazy" allowfullscreen></iframe></div>')
        elif t == "blockquote":
            out.append(f"<blockquote>{esc(b['text'])}</blockquote>")
    return "\n".join(out)

for post in POSTS:
    data = json.load(open(os.path.join(ROOT, "extracted", post["json"] + ".json"), encoding="utf-8"))
    title = data.get("post_title") or data.get("title") or post["slug"]
    date, cats = parse_byline(data["cards"][0]["excerpt"]) if data.get("cards") else (data.get("post_date"), None)
    date = date or data.get("post_date") or ""
    flow = (data.get("post_body") or {}).get("flow") or []
    if flow and flow[0]["type"] in ("h1", "h2") and flow[0]["text"] == title:
        flow = flow[1:]
    body_html = render_flow(flow)
    hero_img = None
    if data.get("cards"):
        hero_img = data["cards"][0].get("image")
    if not hero_img and data.get("sections") and data["sections"][0].get("images"):
        hero_img = data["sections"][0]["images"][0]["src"]

    meta_row = f'<span class="post-meta">{esc(date)}{" · " + esc(cats) if cats else ""}</span>' if date else ""

    hero_img_html = f'<img src="{hero_img}" alt="{esc(title)}" style="width:100%;border-radius:14px;margin-top:2rem;" loading="lazy">' if hero_img else ""

    body = f"""
<article>
  <div class="post-hero">
    <div class="container">
      <a class="back-link" href="/blog/" style="color:var(--muted-dark);">&larr; Wróć do bloga</a>
      {meta_row}
      <h1>{esc(title)}</h1>
    </div>
  </div>
  <div class="container">
    {hero_img_html}
    <div class="prose-wrap">
      <div class="prose">
{body_html}
      </div>
    </div>
  </div>
</article>
"""
    html = common.page(
        title=data.get("title") or title,
        description=data.get("meta_description") or "",
        body=body,
        canonical_path=f"/{post['slug']}/",
    )
    out_dir = os.path.join(ROOT, "site", post["slug"])
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", out_path, len(html), "bytes,", len(flow), "blocks")
