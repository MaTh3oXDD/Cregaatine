import json
import os
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")
OUT = os.path.join(ROOT, "extracted")
os.makedirs(OUT, exist_ok=True)

PAGES = {
    "home": "index.html",
    "blog": "blog/index.html",
    "suplement-roku-fiwe": "suplement-roku-fiwe/index.html",
    "aa": "aa/index.html",
    "cregaatine-naukowa-rewolucja-kreatyny": "cregaatine-naukowa-rewolucja-kreatyny/index.html",
    "gaa-i-kreatyna-badania-naukowe": "gaa-i-kreatyna-badania-naukowe/index.html",
    "dawka-wiedzy-naukowej": "dawka-wiedzy-naukowej/index.html",
    "wyklad-pionier": "wyklad-pionier-w-badaniu-kreatyny-i-gaa-prof-sergej-ostojic/index.html",
    "prof-ostojic-czesc-1": "prof-dr-sergej-ostojic-odpowiada-na-pytania-dotyczace-cregaatine-czesc-1/index.html",
    "karnozyna": "karnozyna-w-miesniach-sportowca/index.html",
    "potrojna-suplementacja": "potrojna-suplementacja-karnozyna-gaa-i-kreatyna/index.html",
    "author-marcin": "author/marcincarno-med-pl/index.html",
    "author-marcin-p2": "author/marcincarno-med-pl/page/2/index.html",
    "category-promo": "category/promo/index.html",
    "category-uncategorized": "category/uncategorized/index.html",
    "category-uncategorized-p2": "category/uncategorized/page/2/index.html",
}

def clean_img_src(img):
    src = img.get("src") or ""
    if src.startswith("data:"):
        src = img.get("data-src") or img.get("data-lazy-src") or src
    return src

def el_to_struct(el):
    """Recursively describe an element's text-bearing structure, skip svg/script/style."""
    if el.name in ("script", "style", "svg", "noscript"):
        return None
    if el.name == "img":
        return {"type": "img", "src": clean_img_src(el), "alt": el.get("alt", "")}
    if el.name in ("h1", "h2", "h3", "h4", "h5", "h6"):
        t = el.get_text(" ", strip=True)
        return {"type": el.name, "text": t} if t else None
    if el.name == "a":
        t = el.get_text(" ", strip=True)
        href = el.get("href", "")
        if t:
            return {"type": "link", "text": t, "href": href}
        return None
    if el.name in ("p", "li", "span", "div"):
        # leaf text check: does it have element children with their own text?
        children_structs = []
        for c in el.find_all(recursive=False):
            s = el_to_struct(c)
            if s:
                children_structs.append(s)
        own_text = el.find(string=True, recursive=False)
        direct_text = el.get_text(" ", strip=True) if not children_structs else None
        if children_structs:
            return {"type": "group", "tag": el.name, "children": children_structs}
        elif direct_text:
            return {"type": "text", "tag": el.name, "text": direct_text}
        return None
    return None

def extract_flow(container):
    """Document-order sequence of content blocks: heading/paragraph/list/image/video."""
    blocks = []
    if not container:
        return blocks
    seen_lists = set()
    for el in container.find_all(["h1","h2","h3","h4","h5","h6","p","ul","ol","img","iframe","blockquote"]):
        if el.find_parent(["ul","ol"]) is not None and el.name != "img":
            continue  # skip nested li-content already covered by parent ul/ol capture below
        if el.name in ("h1","h2","h3","h4","h5","h6"):
            t = el.get_text(" ", strip=True)
            if t:
                blocks.append({"type": el.name, "text": t})
        elif el.name == "p":
            if el.find_parent(["ul","ol","li"]):
                continue
            t = el.get_text(" ", strip=True)
            if t:
                blocks.append({"type": "p", "text": t})
        elif el.name in ("ul", "ol"):
            if id(el) in seen_lists:
                continue
            seen_lists.add(id(el))
            items = [li.get_text(" ", strip=True) for li in el.find_all("li", recursive=False) if li.get_text(strip=True)]
            if items:
                blocks.append({"type": el.name, "items": items})
        elif el.name == "img":
            if el.find_parent(["ul","ol"]):
                continue
            src = clean_img_src(el)
            if src and not src.startswith("data:"):
                blocks.append({"type": "img", "src": src, "alt": el.get("alt","")})
        elif el.name == "iframe":
            src = el.get("data-src") or el.get("src") or ""
            if "youtube" in src or "vimeo" in src:
                blocks.append({"type": "video", "src": src.split("?")[0], "title": el.get("title","")})
        elif el.name == "blockquote":
            t = el.get_text(" ", strip=True)
            if t:
                blocks.append({"type": "blockquote", "text": t})
    return blocks

def extract_page(path):
    full = os.path.join(SITE, path)
    if not os.path.exists(full):
        return {"error": "missing", "path": path}
    html = open(full, encoding="utf-8").read()
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    meta_desc = ""
    md = soup.find("meta", attrs={"name": "description"})
    if md:
        meta_desc = md.get("content", "")

    article = soup.select_one("#main-content") or soup.body
    all_secs = article.find_all("div", class_="et_pb_section") if article else []
    top = [s for s in all_secs if not s.find_parent("div", class_="et_pb_section")]

    sections = []
    for i, sec in enumerate(top):
        headings = [h.get_text(" ", strip=True) for h in sec.find_all(["h1","h2","h3","h4"])]
        paragraphs = [p.get_text(" ", strip=True) for p in sec.find_all("p") if p.get_text(strip=True)]
        buttons = [{"text": a.get_text(" ", strip=True), "href": a.get("href","")}
                   for a in sec.select("a.et_pb_button, a.dica_button, a.more-link")]
        images = []
        for img in sec.find_all("img"):
            src = clean_img_src(img)
            if src and not src.startswith("data:"):
                images.append({"src": src, "alt": img.get("alt","")})
        list_items = [li.get_text(" ", strip=True) for li in sec.find_all("li") if li.get_text(strip=True)]
        videos = []
        for iframe in sec.find_all("iframe"):
            src = iframe.get("data-src") or iframe.get("src") or ""
            if "youtube" in src or "vimeo" in src:
                videos.append({"src": src.split("?")[0], "title": iframe.get("title", "")})
        sections.append({
            "videos": videos,
            "index": i,
            "id": sec.get("id"),
            "classes": sec.get("class"),
            "headings": headings,
            "paragraphs": paragraphs,
            "list_items": list_items,
            "buttons": buttons,
            "images": images,
            "text_preview": sec.get_text(" ", strip=True)[:600],
        })

    # blog post specific: entry-content article body for single posts, in document order
    entry_content = soup.select_one(".entry-content")
    post_body = None
    if entry_content:
        flow = extract_flow(entry_content)
        if flow:
            post_body = {"flow": flow}

    # post meta (title, date, author) for blog posts
    post_title_el = soup.select_one(".entry-title, h1.entry-title")
    post_title = post_title_el.get_text(" ", strip=True) if post_title_el else None
    post_date_el = soup.select_one(".published, .post-meta .updated, time")
    post_date = post_date_el.get_text(" ", strip=True) if post_date_el else None

    # blog listing / archive: list of post cards
    cards = []
    for card in soup.select(".et_pb_post, article.post"):
        h = card.find(["h1","h2","h3"])
        link = card.find("a", href=True)
        excerpt_el = card.select_one(".post-content p, p")
        img = card.find("img")
        cards.append({
            "title": h.get_text(" ", strip=True) if h else None,
            "href": link.get("href") if link else None,
            "excerpt": excerpt_el.get_text(" ", strip=True) if excerpt_el else None,
            "image": clean_img_src(img) if img else None,
        })

    return {
        "title": title,
        "meta_description": meta_desc,
        "sections": sections,
        "post_title": post_title,
        "post_date": post_date,
        "post_body": post_body,
        "cards": cards,
    }

for name, relpath in PAGES.items():
    data = extract_page(relpath)
    outpath = os.path.join(OUT, name + ".json")
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print("done")
