import re
import os
import time
import urllib.request
from urllib.parse import urljoin, urlparse, urldefrag

BASE = "https://cregaatine.pl"
DOMAIN = "cregaatine.pl"
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Accept-Language": "pl-PL,pl;q=0.9",
}

# Real navigable pages only (discovered by crawl). Query-string shortlinks (?p=NNN),
# xmlrpc, feeds, wp-json are WP artifacts, not clickable content -- excluded.
PAGES = [
    "/",
    "/blog/",
    "/suplement-roku-fiwe/",
    "/aa/",
    "/cregaatine-naukowa-rewolucja-kreatyny/",
    "/gaa-i-kreatyna-badania-naukowe/",
    "/dawka-wiedzy-naukowej/",
    "/wyklad-pionier-w-badaniu-kreatyny-i-gaa-prof-sergej-ostojic/",
    "/prof-dr-sergej-ostojic-odpowiada-na-pytania-dotyczace-cregaatine-czesc-1/",
    "/karnozyna-w-miesniach-sportowca/",
    "/potrojna-suplementacja-karnozyna-gaa-i-kreatyna/",
    "/author/marcincarno-med-pl/",
    "/author/marcincarno-med-pl/page/2/",
    "/category/promo/",
    "/category/uncategorized/",
    "/category/uncategorized/page/2/",
]

def fetch_bytes(url, retries=5):
    last_err = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
                ctype = resp.headers.get("Content-Type", "")
                return data, ctype
        except Exception as e:
            last_err = e
            time.sleep(1.5 * (attempt + 1))
    raise last_err

def fetch_text(url, retries=5):
    for attempt in range(retries):
        data, ctype = fetch_bytes(url, retries=1)
        text = data.decode("utf-8", errors="strict") if b"\xef\xbf\xbd" not in data else None
        if text is None or "�" in text:
            # corrupted/mojibake response from flaky server -- retry
            time.sleep(1.5 * (attempt + 1))
            continue
        return text, ctype
    # last resort: return whatever we have, decoded leniently
    data, ctype = fetch_bytes(url, retries=1)
    return data.decode("utf-8", errors="replace"), ctype

def is_internal(url):
    p = urlparse(url)
    return p.netloc == "" or p.netloc == DOMAIN

link_re = re.compile(r'''(href|src|srcset|data-src|data-bg-image)=["']([^"']+)["']''', re.IGNORECASE)
css_url_re = re.compile(r'''url\(\s*(['"]?)([^'")]+)\1\s*\)''')

def find_asset_urls(html_or_css, base_url, is_css=False):
    found = set()
    if is_css:
        for m in css_url_re.finditer(html_or_css):
            val = m.group(2)
            if val.startswith("data:"):
                continue
            absu = urljoin(base_url, val)
            absu, _ = urldefrag(absu)
            if is_internal(absu):
                found.add(absu)
    else:
        for attr, val in link_re.findall(html_or_css):
            candidates = [val]
            if attr == "srcset":
                candidates = [p.strip().split(" ")[0] for p in val.split(",") if p.strip()]
            elif attr == "data-bg-image":
                m = css_url_re.search(val)
                candidates = [m.group(2)] if m else []
            for c in candidates:
                if not c or c.startswith(("data:", "mailto:", "tel:", "javascript:", "#")):
                    continue
                absu = urljoin(base_url, c)
                absu, _ = urldefrag(absu)
                if is_internal(absu):
                    found.add(absu)
    return found

def local_path_for(url):
    p = urlparse(url)
    path = p.path
    if path == "" or path == "/":
        return os.path.join(OUT, "index.html")
    if path.endswith("/"):
        return os.path.join(OUT, path.strip("/"), "index.html")
    return os.path.join(OUT, path.lstrip("/"))

def save_bytes(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)

def strip_domain(text):
    text = text.replace("https://" + DOMAIN, "")
    text = text.replace("http://" + DOMAIN, "")
    text = text.replace("//" + DOMAIN, "")
    return text

def main():
    os.makedirs(OUT, exist_ok=True)
    page_texts = {}
    asset_urls = set()

    print("=== Fetching pages ===")
    for path in PAGES:
        url = BASE + path
        try:
            text, ctype = fetch_text(url)
        except Exception as e:
            print(f"[FAIL] {url}: {e}")
            continue
        page_texts[url] = text
        n_assets = len(find_asset_urls(text, url))
        print(f"[OK] {url} ({len(text)} chars, {n_assets} asset refs)")
        asset_urls |= find_asset_urls(text, url)
        asset_urls |= find_asset_urls(text, url, is_css=True)  # catches url(...) inside inline <style> blocks

    print(f"=== {len(asset_urls)} unique asset URLs discovered from pages ===")

    print("=== Downloading assets (pass 1) ===")
    downloaded = {}
    css_assets_to_scan = []
    for url in sorted(asset_urls):
        local = local_path_for(url)
        if os.path.exists(local):
            downloaded[url] = local
            if local.endswith(".css"):
                css_assets_to_scan.append((url, local))
            continue
        try:
            data, ctype = fetch_bytes(url)
        except Exception as e:
            print(f"[FAIL asset] {url}: {e}")
            continue
        save_bytes(local, data)
        downloaded[url] = local
        if local.endswith(".css") or "css" in ctype:
            css_assets_to_scan.append((url, local))
        print(f"[asset] {url} -> {os.path.relpath(local, ROOT)}")

    print(f"=== Scanning {len(css_assets_to_scan)} CSS files for nested url(...) assets ===")
    nested = set()
    for url, local in css_assets_to_scan:
        try:
            with open(local, "rb") as f:
                css_text = f.read().decode("utf-8", errors="replace")
        except Exception:
            continue
        nested |= find_asset_urls(css_text, url, is_css=True)

    nested_new = {u for u in nested if u not in downloaded}
    print(f"=== Downloading {len(nested_new)} nested CSS assets (fonts/images referenced via url()) ===")
    for url in sorted(nested_new):
        local = local_path_for(url)
        if os.path.exists(local):
            downloaded[url] = local
            continue
        try:
            data, ctype = fetch_bytes(url)
        except Exception as e:
            print(f"[FAIL nested asset] {url}: {e}")
            continue
        save_bytes(local, data)
        downloaded[url] = local
        print(f"[nested asset] {url} -> {os.path.relpath(local, ROOT)}")

    print("=== Writing pages with domain-stripped (root-relative) links ===")
    for url, text in page_texts.items():
        rewritten = strip_domain(text)
        local = local_path_for(url)
        os.makedirs(os.path.dirname(local), exist_ok=True)
        with open(local, "w", encoding="utf-8") as f:
            f.write(rewritten)
        print(f"[page] {url} -> {os.path.relpath(local, ROOT)}")

    print("=== Rewriting CSS files (domain-stripped) ===")
    for url, local in downloaded.items():
        if local.endswith(".css"):
            try:
                with open(local, "r", encoding="utf-8", errors="replace") as f:
                    css_text = f.read()
                new_css = strip_domain(css_text)
                if new_css != css_text:
                    with open(local, "w", encoding="utf-8") as f:
                        f.write(new_css)
            except Exception as e:
                print(f"[css rewrite fail] {local}: {e}")

    print("=== DONE ===")
    print(f"Pages saved: {len(page_texts)}")
    print(f"Assets saved: {len(downloaded)}")

if __name__ == "__main__":
    main()
