# -*- coding: utf-8 -*-
"""Poprawki, które nie mają swojego miejsca w pozostałych skryptach pipeline'u.

Uruchamiaj jako ostatni krok po `mirror.py`, w kolejności opisanej
w cregaatine.pl-audit/ACTION-PLAN.md. Skrypt jest idempotentny --
drugie uruchomienie nic nie zmieni.

Robi pięć rzeczy:

1. Wyrzuca martwy JavaScript: mediaelement (natywny <video controls>
   odtwarza film bez skórki WordPressa) i comment-reply (formularz
   komentarzy na statycznym mirrorze i tak nic nie wysyła).
2. Wynosi z HTML-a te bloki inline CSS, które są bajt w bajt identyczne
   na wszystkich stronach. Ładują się raz i siedzą w cache.
3. Zmienia slug /aa/ na /podcast-sergej-ostojic/ i dopisuje 301.
4. Konwertuje do WebP obrazy, do których odwołuje się wyłącznie CSS --
   to_webp.py skanuje tylko atrybuty HTML i takie pliki pomija.
5. Sortuje sitemap.xml.
"""
import os
import re
import glob
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")

OLD_SLUG = "/aa/"
NEW_SLUG = "/podcast-sergej-ostojic/"

SHARED_CSS = {
    "global-styles-inline-css": "assets/css/wp-global-styles.css",
    "divi-style-inline-inline-css": "assets/css/divi-style.css",
}

DEAD_ASSETS = [
    (r'<script[^>]*id=["\']comment-reply-js["\'][^>]*></script>', "comment-reply"),
    (r'<script[^>]*id=["\']mediaelement-js-extra["\'][^>]*>.*?</script>', "mejs-i18n"),
    (r'<script[^>]*id=["\']mediaelement-core-js-before["\'][^>]*>.*?</script>', "mejs-settings"),
    (r'<script[^>]*src=["\'][^"\']*mediaelement[^"\']*["\'][^>]*></script>', "mejs-js"),
    (r'<link[^>]*id=["\'](?:wp-)?mediaelement-css["\'][^>]*/?>', "mejs-css"),
]

DEAD_FILES = [
    "wp-includes/js/mediaelement",
    "wp-includes/js/comment-reply.min.js",
]


def pages():
    return sorted(glob.glob(os.path.join(SITE, "**", "index.html"), recursive=True))


def read(p):
    return open(p, encoding="utf-8").read()


def write(p, s):
    open(p, "w", encoding="utf-8").write(s)


def strip_dead_assets():
    saved = 0
    for p in pages():
        h = orig = read(p)
        for pat, _ in DEAD_ASSETS:
            h = re.sub(pat, "", h, flags=re.S)
        if h != orig:
            write(p, h)
            saved += len(orig) - len(h)
    for rel in DEAD_FILES:
        target = os.path.join(SITE, rel.replace("/", os.sep))
        if os.path.isdir(target):
            shutil.rmtree(target)
        elif os.path.exists(target):
            os.remove(target)
    print(f"[1] martwy JS: {saved // 1024} KB usunięte z HTML-a")


def externalize_shared_css():
    extracted = {}
    saved = 0
    for p in pages():
        h = orig = read(p)
        for sid, out in SHARED_CSS.items():
            m = re.search(r'<style id="' + sid + r'">(.*?)</style>', h, re.S)
            if not m:
                continue
            css = m.group(1)
            prev = extracted.get(out)
            if prev is not None and prev != css:
                raise SystemExit(f"[2] PRZERWANO: {sid} różni się między stronami ({p})")
            extracted[out] = css
            link = f'<link rel="stylesheet" id="{sid}" href="/{out}?v=1" media="all" />'
            h = h[:m.start()] + link + h[m.end():]
        if h != orig:
            write(p, h)
            saved += len(orig) - len(h)
    for out, css in extracted.items():
        target = os.path.join(SITE, out.replace("/", os.sep))
        os.makedirs(os.path.dirname(target), exist_ok=True)
        write(target, css.strip() + "\n")
    print(f"[2] wspólny CSS: {len(extracted)} plików, {saved // 1024} KB mniej w HTML-u")


def rename_slug():
    old_dir = os.path.join(SITE, "aa")
    new_dir = os.path.join(SITE, NEW_SLUG.strip("/"))
    if os.path.isdir(old_dir) and not os.path.isdir(new_dir):
        os.rename(old_dir, new_dir)

    targets = pages() + [
        os.path.join(SITE, "llms.txt"),
        os.path.join(SITE, "sitemap.xml"),
        os.path.join(SITE, "assets", "css", "enhance.css"),
    ]
    n = 0
    for p in targets:
        if not os.path.exists(p):
            continue
        h = read(p)
        if OLD_SLUG in h:
            n += h.count(OLD_SLUG)
            write(p, h.replace(OLD_SLUG, NEW_SLUG))

    redirects = os.path.join(SITE, "_redirects")
    rule = f"{OLD_SLUG}  {NEW_SLUG}  301"
    lines = read(redirects).rstrip("\n").split("\n") if os.path.exists(redirects) else []
    if rule not in lines:
        lines.append(rule)
        write(redirects, "\n".join(lines) + "\n")
    print(f"[3] slug {OLD_SLUG} -> {NEW_SLUG}: {n} odwołań przepisanych")


def css_images_to_webp():
    from PIL import Image

    css_files = glob.glob(os.path.join(SITE, "**", "*.css"), recursive=True)
    pat = re.compile(r'url\((["\']?)(/wp-content/uploads/[^)"\']+\.(?:png|jpe?g))\1\)', re.I)

    refs = set()
    for p in css_files:
        refs |= {m.group(2) for m in pat.finditer(open(p, encoding="utf-8", errors="ignore").read())}

    conv, saved = {}, 0
    for u in sorted(refs):
        local = os.path.join(SITE, u.lstrip("/").replace("/", os.sep))
        if not os.path.exists(local):
            continue
        webp = os.path.splitext(local)[0] + ".webp"
        if not os.path.exists(webp):
            im = Image.open(local)
            if im.mode in ("P", "LA"):
                im = im.convert("RGBA")
            elif im.mode == "CMYK":
                im = im.convert("RGB")
            im.save(webp, "WEBP", quality=82, method=6)
        o, n = os.path.getsize(local), os.path.getsize(webp)
        if n >= o:
            os.remove(webp)
            continue
        conv[u] = os.path.splitext(u)[0] + ".webp"
        saved += o - n

    for p in css_files:
        h = read(p)
        new = h
        for a, b in conv.items():
            new = new.replace(a, b)
        if new != h:
            write(p, new)

    for u in conv:
        local = os.path.join(SITE, u.lstrip("/").replace("/", os.sep))
        if os.path.exists(local):
            os.remove(local)
    print(f"[4] obrazy z CSS: {len(conv)} przekonwertowanych, {saved // 1024} KB mniej")


def sort_sitemap():
    p = os.path.join(SITE, "sitemap.xml")
    if not os.path.exists(p):
        print("[5] brak sitemap.xml -- pomijam")
        return
    h = read(p)
    urls = sorted(set(re.findall(r"<url>.*?</url>", h, re.S)),
                  key=lambda u: re.search(r"<loc>(.*?)</loc>", u).group(1))
    head = h.split("<url>")[0].rstrip()
    write(p, head + "\n" + "\n".join("  " + u for u in urls) + "\n</urlset>\n")
    print(f"[5] sitemap.xml: {len(urls)} URL-i, posortowane")


def check_links():
    have = {"/" + os.path.relpath(p, SITE).replace(os.sep, "/")
            for p in glob.glob(os.path.join(SITE, "**", "*"), recursive=True)}
    bad = set()
    for p in pages():
        h = read(p)
        for u in re.findall(r'(?:href|src)=["\'](/[^"\'#]*)', h):
            u = u.split("?")[0]
            if not u:
                continue
            if not ({u, u.rstrip("/") + "/index.html", u + "index.html"} & have):
                bad.add((os.path.relpath(p, SITE), u))
    if bad:
        print(f"[!] {len(bad)} zepsutych linków wewnętrznych:")
        for b in sorted(bad)[:20]:
            print("   ", b)
    else:
        print("[ok] 0 zepsutych linków wewnętrznych")


if __name__ == "__main__":
    strip_dead_assets()
    externalize_shared_css()
    rename_slug()
    css_images_to_webp()
    sort_sitemap()
    check_links()
