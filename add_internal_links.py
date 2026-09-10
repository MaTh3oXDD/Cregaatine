# -*- coding: utf-8 -*-
"""Linkowanie wewnętrzne hub-and-spoke dla trzech cienkich stron wideo.

/aa/, /wyklad-.../ i /prof-dr-sergej-ostojic-.../ nie linkowały do strony
produktowej wcale -- ruch z nich nie płynął nigdzie dalej. Dodajemy blok
"Przeczytaj także" z anchorami opisowymi, taki sam jak na pozostałych wpisach.
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")

LINKS = [
    ("/cregaatine-naukowa-rewolucja-kreatyny/",
     "CreGAAtine &#8211; kreatyna z GAA, 8,5x efektywniejsza od monohydratu"),
    ("/gaa-i-kreatyna-badania-naukowe/",
     "GAA i kreatyna &#8211; 25 badań naukowych"),
    ("/karnozyna-w-miesniach-sportowca/",
     "Karnozyna w mięśniach sportowca"),
    ("/potrojna-suplementacja-karnozyna-gaa-i-kreatyna/",
     "Potrójna suplementacja: karnozyna, GAA i kreatyna"),
]

CSS = (
    '<style id="related-inline-css">'
    '.rel-seo{max-width:1080px;margin:0 auto;padding:32px 20px}'
    '.rel-seo h2{font-size:24px;margin:0 0 16px}'
    '.rel-seo ul{margin:0;padding:0;list-style:none}'
    '.rel-seo li{padding:10px 0;border-bottom:1px solid rgba(0,0,0,.1)}'
    '.rel-seo a{text-decoration:none;font-weight:600}'
    '.rel-seo a:hover{text-decoration:underline}'
    '</style>'
)

PAGES = {
    "aa": "/aa/",
    "wyklad-pionier-w-badaniu-kreatyny-i-gaa-prof-sergej-ostojic":
        "/wyklad-pionier-w-badaniu-kreatyny-i-gaa-prof-sergej-ostojic/",
    "prof-dr-sergej-ostojic-odpowiada-na-pytania-dotyczace-cregaatine-czesc-1":
        "/prof-dr-sergej-ostojic-odpowiada-na-pytania-dotyczace-cregaatine-czesc-1/",
}

MARKER = '<div class="et_post_meta_wrapper">'


def block(self_url):
    items = "".join(
        f'<li><a href="{href}">{label}</a></li>'
        for href, label in LINKS if href != self_url)
    return ('<section class="rel-seo"><h2>Przeczytaj także</h2>'
            f'<ul>{items}</ul></section>')


for rel, url in PAGES.items():
    path = os.path.join(SITE, rel.replace("/", os.sep), "index.html")
    html = open(path, encoding="utf-8").read()
    if 'class="rel-seo"' in html:
        print(f"[pomijam] {rel} -- blok już jest")
        continue
    # drugie wystąpienie: to, które zamyka treść wpisu
    i = html.find(MARKER)
    i = html.find(MARKER, i + 1)
    if i < 0:
        print(f"[BŁĄD] {rel} -- nie znaleziono miejsca wstawienia")
        continue
    html = html[:i] + block(url) + html[i:]
    html = html.replace("</head>", CSS + "\n</head>", 1)
    open(path, "w", encoding="utf-8").write(html)
    print(f"[dodano] {rel} -- {len(LINKS)-1} linki kontekstowe")
