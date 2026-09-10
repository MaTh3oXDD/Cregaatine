# -*- coding: utf-8 -*-
"""Naprawy SEO dla statycznego mirrora cregaatine.pl.

Uruchamiać po fix_seo_urls.py. Idempotentny -- każdy etap sprawdza,
czy zmiana już nie została naniesiona.

Etapy:
  A  alt text dla obrazów
  B  og:image + twitter:image
  C  jeden H1 na stronę
  D  brakujące meta description
  E  skrócenie sufiksu w <title>
  F  usunięcie martwych skryptów
  G  noindex na archiwach bez wartości
  H  schema: Organization, Product+Offer, Article
  I  preload="none" na filmie 141 MB
  J  wycięcie zbędnych @font-face (TTF/WOFF -> tylko WOFF2)
  K  llms.txt, .htaccess, _redirects
"""
import os
import re
import glob
import json

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")
BASE = "https://cregaatine.pl"
OG_IMAGE = f"{BASE}/wp-content/uploads/2025/04/og-cregaatine.jpg"

stats = {}


def bump(key, n=1):
    stats[key] = stats.get(key, 0) + n


# ---------------------------------------------------------------- A. alt text

ALT = {
    # ikony korzyści -- obraz poprzedza swój nagłówek w układzie Divi
    "ico1-100x84-1.png": "Ikona: CreGAAtine daje 8,5x więcej kreatyny w mięśniach",
    "retencja.png": "Wykres: brak retencji wody podskórnej przy stosowaniu CreGAAtine",
    "ico2-100x84-1.png": "Ikona: kreatyna z GAA wnika do komórek czterema drogami",
    "ico3-100x84-1.png": "Ikona: CreGAAtine zapewnia większą siłę",
    # ikony 85x70 (angielskie nazwy plików)
    "CreGAATine-provides-up-to-8.5-times-more-creatine-in-the-cell-85x70-01-1.png":
        "Ikona: do 8,5 razy więcej kreatyny w komórce",
    "CreGAAtine-increases-brain-creatine-levels-85x70-02.png":
        "Ikona: wyższy poziom kreatyny w mózgu",
    "CreGAAtine-provides-20-more-strenght-85x70-03.png":
        "Ikona: o 20% większa siła",
    "CreGAAtine-reduces-side-effects-85x70-04.png":
        "Ikona: mniej skutków ubocznych suplementacji kreatyną",
    "Enters-the-cell-in-4-different-ways-85x70-05.png":
        "Ikona: wnikanie do komórki czterema różnymi drogami",
    "CreGAAtine-has-innovative-packaging-85x70-06.png":
        "Ikona: innowacyjne trójwarstwowe opakowanie CreGAAtine",
    # duże ikony korzyści
    "velike-ikonice-178x150-01-1.png":
        "Ikona: 3,9 razy więcej kreatyny w istocie szarej mózgu",
    "velike-ikonice-178x150-02.png":
        "Ikona: brak retencji wody podskórnej",
    "velike-ikonice-178x150-03-1.png":
        "Ikona: dodatkowe ścieżki dostarczania kreatyny do komórek",
    "velike-ikonice-178x150-04.png":
        "Ikona: trójwarstwowe opakowanie klasy farmaceutycznej",
    "velike-ikonice-178x150-05-2.png":
        "Ikona: wzrost poziomu kreatyny w mięśniach do 16,9 procent",
    "velike-ikonice-178x150-06.png":
        "Ikona: CreGAAtine dla kobiet i mężczyzn w każdym wieku",
    # produkt
    "Cregaatine-2025-png.png":
        "Opakowanie CreGAAtine 2025 -- kreatyna z GAA w saszetkach",
    "cregatine-4.png":
        "Opakowanie CreGAAtine z 60 saszetkami suplementu",
    # certyfikaty antydopingowe
    "c1-2.png": "Certyfikat antydopingowy CreGAAtine -- skan dokumentu (1 z 4)",
    "c2.png": "Certyfikat antydopingowy CreGAAtine -- skan dokumentu (2 z 4)",
    "c3.png": "Certyfikat antydopingowy CreGAAtine -- skan dokumentu (3 z 4)",
    "c4.png": "Certyfikat antydopingowy CreGAAtine -- skan dokumentu (4 z 4)",
    "Q10-Komplex-doping-free-certificate.jpg":
        "Certyfikat doping-free dla Komplex Q10 -- skan dokumentu",
    # opinie
    "sztoffit.jpeg":
        "Joanna Stós (@sztosfit) -- opinia o CreGAAtine",
    "jarek.jpeg":
        "Jarosław Rogowski, ekspert bezpieczeństwa osobistego -- opinia o CreGAAtine",
    "noagefit.jpg":
        "Katarzyna Czaplejewicz (@no_age_fit), instruktorka fitness -- opinia o CreGAAtine",
    "piotr.jpeg":
        "Piotr Tomczyk, strongman -- opinia o CreGAAtine",
    "175791811_462266004834424_7754191150956982309_n-240x300-1.jpg":
        "Misa Balculov, trener muay thai i kickboxingu -- opinia o CreGAAtine",
    "60800801_716377878802726_2197132368913551553_n-300x300-1.jpg":
        "Milan Veselinović, trener kondycyjny -- opinia o CreGAAtine",
    "124667681_2873208306281979_9124896752305789321_n-300x200-1.jpg":
        "Slobodan Maksimovic, zawodnik MMA -- opinia o CreGAAtine",
    "Lara-Santini-240x300-1.jpg":
        "Lara Santini, dwukrotna mistrzyni świata w bodybuildingu -- opinia o CreGAAtine",
    # logotypy partnerów
    "GKMA.jpg": "Logo partnera: GKMA",
    "doktor-fit-logo-1623598006.png": "Logo partnera: Doktor Fit",
    "atleta.jpg": "Logo partnera: Atleta",
    "bmsklep_logo-black-_1_.jpg": "Logo partnera: BM Sklep",
    "dobre-suple-ok.jpg": "Logo partnera: Dobre Suple",
    "sportowesuplementy-ok.jpg": "Logo partnera: Sportowe Suplementy",
    "odzyweczki-ok.png": "Logo partnera: Odżyweczki",
    "PTA.jpg": "Logo partnera: PTA",
    "strefa-mocy.png": "Logo partnera: Strefa Mocy",
    "BeSport.jpg": "Logo partnera: BeSport",
    "logo_suple-man.png": "Logo partnera: Suple Man",
    "xlogo.png.pagespeed.ic_.RN_WvpZ5JI.webp": "Logo partnera CreGAAtine",
    "logo-na-web-1.jpg": "Logo partnera CreGAAtine",
    "logo_1_big.png": "Logo partnera CreGAAtine",
    "logo.png": "Logo partnera CreGAAtine",
    "3f045470e8230593fee4de70ce8de6f3.jpg": "Logo partnera CreGAAtine",
    # pozostałe produkty Carno-Med
    "Karnozin-extra-front.jpg": "Karnozin Extra -- opakowanie suplementu Carno-Med",
    "Komplex-Q10-front.jpg": "Komplex Q10 -- opakowanie suplementu Carno-Med",
    "Kolostrum-pure-gold-ekspozycja.jpg":
        "Kolostrum Extra PURE GOLD -- ekspozycja opakowania Carno-Med",
    # miniatury wpisów
    "booster.jpg":
        "CreGAAtine -- monohydrat kreatyny dający 8,5x więcej efektywności",
    "wyklad.jpg":
        "Wykład prof. Sergeja Ostojicia o badaniach nad kreatyną i GAA",
    "QA.jpg":
        "Prof. dr Sergej Ostojić odpowiada na pytania o CreGAAtine",
    "karnozyna.jpg": "Karnozyna w mięśniach sportowca",
    "suplementacja.jpg": "Potrójna suplementacja -- karnozyna, GAA i kreatyna",
    "kreatyna-i-gaa-badania-naukowe.jpg": "GAA i kreatyna -- badania naukowe",
    "podcast.jpg": "Podcast z prof. dr. Sergejem Ostojiciem o CreGAAtine",
    "FIWE.jpg": "Targi FIWE -- CreGAAtine suplementem roku 2021",
    "241708735_2948976912057509_6837963708796457051_n.jpg":
        "Stoisko CreGAAtine na targach FIWE 2021 w Warszawie",
}


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;")


def stage_alt(html):
    def fix(m):
        tag = m.group(0)
        if re.search(r'alt="[^"]+"', tag):
            return tag
        src = re.search(r'src="([^"]*)"', tag)
        if not src:
            return tag
        name = src.group(1).split("/")[-1]
        # miniatury WordPressa: obetnij sufiks -WxH
        alt = ALT.get(name) or ALT.get(re.sub(r"-\d+x\d+(?=\.\w+$)", "", name))
        if not alt:
            return tag
        bump("alt")
        if 'alt=""' in tag:
            return tag.replace('alt=""', f'alt="{esc(alt)}"', 1)
        return tag.replace("<img", f'<img alt="{esc(alt)}"', 1)

    return re.sub(r"<img\b[^>]*>", fix, html)


# --------------------------------------------------------------- B. og:image

def stage_og(html):
    if "og:image" in html:
        return html
    block = (
        f'<meta property="og:image" content="{OG_IMAGE}" />\n'
        f'<meta property="og:image:width" content="1200" />\n'
        f'<meta property="og:image:height" content="630" />\n'
        f'<meta property="og:image:type" content="image/jpeg" />\n'
        f'<meta name="twitter:image" content="{OG_IMAGE}" />\n'
    )
    if '<meta name="twitter:card"' in html:
        html = html.replace('<meta name="twitter:card"', block + '<meta name="twitter:card"', 1)
    else:
        html = html.replace("</head>", block + "</head>", 1)
    bump("og_image")
    return html


# --------------------------------------------------------------------- C. H1

ARCHIVE_H1 = {
    "category/promo": "Artykuły w kategorii: promo",
    "category/uncategorized": "Artykuły w kategorii: Uncategorized",
    "category/uncategorized/page/2": "Artykuły w kategorii: Uncategorized -- strona 2",
    "author/marcincarno-med-pl": "Artykuły autora bloga CreGAAtine",
    "author/marcincarno-med-pl/page/2": "Artykuły autora bloga CreGAAtine -- strona 2",
}


def stage_h1(html, rel):
    head, body = html.split("</head>", 1)

    # duplikat w treści: <h1 style="text-align: left;"> -> h2
    n = len(re.findall(r'<h1 style="text-align: left;">', body))
    if n:
        body = body.replace('<h1 style="text-align: left;">',
                            '<h2 style="text-align: left;">')
        # zamknięcia h1 należące do tych bloków -- policz i zamień od końca
        for _ in range(n):
            i = body.rfind("</h1>")
            # ostrożnie: zamieniamy tylko te </h1>, które nie należą do entry-title
            # entry-title występuje wcześniej w dokumencie, więc idziemy od końca
            body = body[:i] + "</h2>" + body[i + 5:]
        bump("h1_demoted", n)

    # /blog/ -- promocja pierwszego h2 do h1
    if rel == "" and False:
        pass
    if rel == "blog" and "<h1" not in body:
        m = re.search(r"<h2([^>]*)>(\s*BLOG[^<]*)</h2>", body)
        if m:
            body = body[:m.start()] + f"<h1{m.group(1)}>{m.group(2)}</h1>" + body[m.end():]
            bump("h1_promoted")

    # archiwa -- wstrzyknięcie H1 na początku listy wpisów
    if "<h1" not in body and rel in ARCHIVE_H1:
        marker = '<div id="left-area">'
        if marker in body:
            body = body.replace(
                marker,
                marker + f'\n<h1 class="entry-title archive-title">{ARCHIVE_H1[rel]}</h1>',
                1)
            bump("h1_injected")

    return head + "</head>" + body


def stage_home_h1(html):
    old = "<h1 class=\"et_pb_module_header\">Naukowa rewolucja kreatyny</h1>"
    new = ("<h1 class=\"et_pb_module_header\">CreGAAtine &#8211; kreatyna z GAA, "
           "8,5&#215; efektywniejsza od monohydratu</h1>")
    if old in html:
        bump("h1_home")
        return html.replace(old, new, 1)
    return html


# -------------------------------------------------------- D. meta description

DESCRIPTIONS = {
    "": None,  # ma już opis
    "aa": "Posłuchaj podcastu z prof. dr. Sergejem Ostojiciem, pionierem badań nad "
          "kreatyną i GAA. Rozmowa o tym, jak CreGAAtine zwiększa poziom kreatyny w komórkach.",
    "blog": "Artykuły o kreatynie, GAA i karnozynie: badania naukowe, dawkowanie i efekty "
            "suplementacji. Blog ekspercki CreGAAtine.",
    "suplement-roku-fiwe": "CreGAAtine zdobyła tytuł suplementu roku 2021 na targach FIWE "
                           "w Warszawie. Zobacz relację i dowiedz się, co przekonało jury.",
    "karnozyna-w-miesniach-sportowca": "Czym jest karnozyna, jak działa w mięśniach sportowca "
                                       "i dlaczego warto łączyć ją z kreatyną. Sprawdź badania i zalecane dawkowanie.",
    "wyklad-pionier-w-badaniu-kreatyny-i-gaa-prof-sergej-ostojic":
        "Wykład prof. Sergeja Ostojicia o połączeniu kreatyny z kwasem GAA. Zobacz, skąd bierze "
        "się 8,5x większa efektywność CreGAAtine.",
    "prof-dr-sergej-ostojic-odpowiada-na-pytania-dotyczace-cregaatine-czesc-1":
        "Prof. dr Sergej Ostojić odpowiada na pytania o CreGAAtine: dawkowanie, bezpieczeństwo "
        "i różnice względem monohydratu kreatyny. Część 1.",
    "category/promo": "Artykuły promocyjne i nowości CreGAAtine -- kreatyny połączonej z kwasem GAA.",
    "category/uncategorized": "Wszystkie artykuły bloga CreGAAtine o kreatynie, GAA i suplementacji sportowej.",
    "category/uncategorized/page/2": "Wszystkie artykuły bloga CreGAAtine o kreatynie, GAA i suplementacji sportowej -- strona 2.",
    "author/marcincarno-med-pl": "Artykuły autora bloga CreGAAtine o kreatynie, GAA, karnozynie i suplementacji sportowej.",
    "author/marcincarno-med-pl/page/2": "Artykuły autora bloga CreGAAtine o kreatynie, GAA, karnozynie i suplementacji sportowej -- strona 2.",
}


def stage_description(html, rel):
    if '<meta name="description"' in html:
        return html
    desc = DESCRIPTIONS.get(rel)
    if not desc:
        return html
    tag = f'<meta name="description" content="{esc(desc)}" />\n'
    og = f'<meta property="og:description" content="{esc(desc)}" />\n'
    tw = f'<meta name="twitter:description" content="{esc(desc)}" />\n'
    extra = tag
    if "og:description" not in html:
        extra += og
    if "twitter:description" not in html:
        extra += tw
    anchor = '<link rel="canonical"'
    if anchor in html:
        html = html.replace(anchor, extra + anchor, 1)
    else:
        html = html.replace("</head>", extra + "</head>", 1)
    bump("description")
    return html


# ------------------------------------------------------------------ E. tytuły

TITLES = {
    "aa": "Prof. Sergej Ostojić &#8211; podcast o kreatynie | CreGAAtine",
    "author/marcincarno-med-pl": "Autor bloga CreGAAtine | CreGAAtine",
    "author/marcincarno-med-pl/page/2": "Autor bloga CreGAAtine &#8211; strona 2 | CreGAAtine",
    "blog": "Blog o kreatynie, GAA i suplementacji | CreGAAtine",
    "category/promo": "Promocje i nowości | CreGAAtine",
    "category/uncategorized": "Wszystkie artykuły | CreGAAtine",
    "category/uncategorized/page/2": "Wszystkie artykuły &#8211; strona 2 | CreGAAtine",
    "karnozyna-w-miesniach-sportowca": "Karnozyna w mięśniach sportowca | CreGAAtine",
    "prof-dr-sergej-ostojic-odpowiada-na-pytania-dotyczace-cregaatine-czesc-1":
        "Prof. Ostojić o CreGAAtine &#8211; pytania cz. 1 | CreGAAtine",
    "suplement-roku-fiwe": "Targi FIWE &#8211; CreGAAtine suplementem roku 2021 | CreGAAtine",
    "wyklad-pionier-w-badaniu-kreatyny-i-gaa-prof-sergej-ostojic":
        "Wykład prof. Ostojicia o kreatynie i GAA | CreGAAtine",
}


def stage_title(html, rel):
    new = TITLES.get(rel)
    if not new:
        return html
    m = re.search(r"<title>([^<]*)</title>", html)
    if not m or m.group(1) == new:
        return html
    bump("title")
    html = html[:m.start()] + f"<title>{new}</title>" + html[m.end():]
    # og:title musi zostać spójny
    html = re.sub(r'(<meta property="og:title" content=")[^"]*(")',
                  lambda x: x.group(1) + new + x.group(2), html, count=1)
    return html


# ---------------------------------------------------------- F. martwe skrypty

DEAD_ALWAYS = [
    "intelly-countdown/assets/deps/moment/moment.js",   # widget nie renderuje się nigdzie
    "intelly-countdown/assets/js/icp.library.js",
    "wp-smushit/app/assets/js/smush-lazy-load.min.js",  # zastąpiony przez unlazy.py
]
MEDIAELEMENT = [
    "mediaelement/mediaelement-and-player.min.js",
    "mediaelement/mediaelement-migrate.min.js",
    "mediaelement/wp-mediaelement.min.js",
]


def drop_script(html, needle):
    pat = re.compile(r'<script[^>]*src="[^"]*' + re.escape(needle) + r'[^"]*"[^>]*>\s*</script>\s*')
    html, n = pat.subn("", html)
    if n:
        bump("scripts_removed", n)
    return html


def stage_scripts(html, rel):
    for n in DEAD_ALWAYS:
        html = drop_script(html, n)
    # mediaelement zostaje tylko tam, gdzie faktycznie jest <video>
    if "<video" not in html.split("</head>", 1)[1]:
        for n in MEDIAELEMENT:
            html = drop_script(html, n)
        html = re.sub(
            r"<script[^>]*id=\"mediaelement-core-js-before\"[^>]*>.*?</script>\s*",
            "", html, flags=re.S)
    return html


# ------------------------------------------------------------------ G. noindex

NOINDEX = {
    "author/marcincarno-med-pl",
    "author/marcincarno-med-pl/page/2",
    "category/uncategorized",
    "category/uncategorized/page/2",
    "dawka-wiedzy-naukowej",
}


def stage_noindex(html, rel):
    if rel not in NOINDEX:
        return html
    if re.search(r'<meta name="robots"[^>]*noindex', html):
        return html
    tag = '<meta name="robots" content="noindex, follow" />\n'
    if '<meta name="robots"' in html:
        html = re.sub(r'<meta name="robots"[^>]*>', tag.strip(), html, count=1)
    else:
        html = html.replace('<link rel="canonical"', tag + '<link rel="canonical"', 1)
    bump("noindex")
    return html


# ------------------------------------------------------------------- H. schema

ORGANIZATION = {
    "@type": "Organization",
    "@id": f"{BASE}/#organization",
    "name": "CreGAAtine",
    "url": f"{BASE}/",
    "logo": {
        "@type": "ImageObject",
        "url": f"{BASE}/wp-content/uploads/2021/03/logo-cregaatine-400px.png",
        "width": 400,
        "height": 213,
    },
    "sameAs": [
        "https://www.facebook.com/cregaatine.polska",
        "https://www.instagram.com/cregaatine.pl/",
        "https://sklep.cregaatine.pl/",
    ],
}

PRODUCT = {
    "@type": "Product",
    "@id": f"{BASE}/cregaatine-naukowa-rewolucja-kreatyny/#product",
    "name": "CreGAAtine",
    "description": ("Monohydrat kreatyny połączony z kwasem guanidynooctowym (GAA). "
                    "Podnosi poziom kreatyny w mięśniach do 16,9% zamiast około 2% "
                    "przy samym monohydracie, bez retencji wody podskórnej."),
    "brand": {"@type": "Brand", "name": "Carno-Med"},
    "image": [f"{BASE}/wp-content/uploads/2025/04/Cregaatine-2025-png.png"],
    "category": "Suplementy diety / Kreatyna",
    "url": f"{BASE}/cregaatine-naukowa-rewolucja-kreatyny/",
    "offers": {
        "@type": "Offer",
        "url": "https://sklep.cregaatine.pl/",
        "priceCurrency": "PLN",
        "availability": "https://schema.org/InStock",
        "seller": {"@id": f"{BASE}/#organization"},
    },
}

ARTICLES = {
    "gaa-i-kreatyna-badania-naukowe": "GAA i kreatyna -- badania naukowe",
    "karnozyna-w-miesniach-sportowca": "Karnozyna w mięśniach sportowca",
    "potrojna-suplementacja-karnozyna-gaa-i-kreatyna":
        "Potrójna suplementacja -- karnozyna, GAA i kreatyna",
    "cregaatine-naukowa-rewolucja-kreatyny":
        "CreGAAtine -- poznaj monohydrat kreatyny w nowej odsłonie",
    "suplement-roku-fiwe": "Targi FIWE -- CreGAAtine suplementem roku 2021",
    "wyklad-pionier-w-badaniu-kreatyny-i-gaa-prof-sergej-ostojic":
        "Wykład pioniera w badaniu kreatyny i GAA -- prof. Sergej Ostojić",
    "prof-dr-sergej-ostojic-odpowiada-na-pytania-dotyczace-cregaatine-czesc-1":
        "Prof. dr Sergej Ostojić odpowiada na pytania o CreGAAtine (część 1)",
    "aa": "Prof. dr Sergej Ostojić -- podcast",
}


def stage_schema(html, rel):
    m = re.search(r'(<script type="application/ld\+json"[^>]*>)(.*?)(</script>)', html, re.S)
    if not m:
        return html
    try:
        data = json.loads(m.group(2))
    except json.JSONDecodeError:
        return html
    graph = data.get("@graph")
    if not isinstance(graph, list):
        return html
    types = {n.get("@type") for n in graph}
    changed = False

    if "Organization" not in types:
        graph.append(ORGANIZATION)
        types.add("Organization")
        changed = True
        bump("schema_org")

    # WebSite i WebPage powinny wskazywać wydawcę
    for node in graph:
        if node.get("@type") == "WebSite" and "publisher" not in node:
            node["publisher"] = {"@id": f"{BASE}/#organization"}
            changed = True
        if node.get("@type") == "WebPage" and "isPartOf" in node:
            if "primaryImageOfPage" not in node:
                node["primaryImageOfPage"] = {"@type": "ImageObject", "url": OG_IMAGE}
                changed = True

    if rel == "cregaatine-naukowa-rewolucja-kreatyny" and "Product" not in types:
        graph.append(PRODUCT)
        changed = True
        bump("schema_product")

    if rel in ARTICLES and "Article" not in types:
        page = next((n for n in graph if n.get("@type") == "WebPage"), {})
        art = {
            "@type": "Article",
            "@id": f"{BASE}/{rel}/#article",
            "headline": ARTICLES[rel],
            "isPartOf": {"@id": page.get("@id", f"{BASE}/{rel}/")},
            "mainEntityOfPage": {"@id": page.get("@id", f"{BASE}/{rel}/")},
            "inLanguage": "pl-PL",
            "image": OG_IMAGE,
            "publisher": {"@id": f"{BASE}/#organization"},
            "author": {"@id": f"{BASE}/#organization"},
        }
        for k in ("datePublished", "dateModified"):
            if page.get(k):
                art[k] = page[k]
        graph.append(art)
        changed = True
        bump("schema_article")

    if not changed:
        return html
    new = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    return html[:m.start()] + m.group(1) + new + m.group(3) + html[m.end():]


# -------------------------------------------------------------------- I. wideo

def stage_video(html):
    if 'preload="metadata"' in html and "<video" in html:
        bump("video_preload")
        return html.replace('preload="metadata"', 'preload="none"')
    return html


# --------------------------------------------------------------- J. @font-face

FONTFACE_RE = re.compile(r"@font-face\s*\{[^}]*\}")


def stage_fonts(html):
    """Divi wkleja Open Sans dla trzech user-agentów (TTF + WOFF + WOFF2).
    Przeglądarka bierze jeden wariant -- zostawiamy WOFF2 i tylko wagi 400/600/700."""
    def trim(m):
        css = m.group(1)
        faces = FONTFACE_RE.findall(css)
        if len(faces) < 10:
            return m.group(0)
        keep = []
        seen = set()
        for f in faces:
            if "format('woff2')" not in f and 'format("woff2")' not in f:
                continue
            w = re.search(r"font-weight:\s*(\d+)", f)
            s = re.search(r"font-style:\s*(\w+)", f)
            fam = re.search(r"font-family:\s*'([^']+)'", f)
            weight = w.group(1) if w else "400"
            if weight not in ("400", "600", "700"):
                continue
            key = (fam.group(1) if fam else "?", weight, s.group(1) if s else "normal")
            if key in seen:
                continue
            seen.add(key)
            keep.append(f)
        if not keep:
            return m.group(0)
        rest = FONTFACE_RE.sub("", css)
        bump("fontfaces_removed", len(faces) - len(keep))
        return m.group(0).replace(css, "".join(keep) + rest)

    return re.sub(r"<style id=\"et-divi-open-sans-inline-css\">(.*?)</style>",
                  trim, html, flags=re.S)


# ------------------------------------------------------------------ pipeline

def rel_for(path):
    d = os.path.relpath(os.path.dirname(path), SITE).replace("\\", "/")
    return "" if d == "." else d


def main():
    for path in sorted(glob.glob(os.path.join(SITE, "**", "index.html"), recursive=True)):
        rel = rel_for(path)
        html = open(path, encoding="utf-8").read()
        orig = html

        html = stage_alt(html)
        html = stage_og(html)
        html = stage_h1(html, rel)
        if rel == "":
            html = stage_home_h1(html)
        html = stage_description(html, rel)
        html = stage_title(html, rel)
        html = stage_scripts(html, rel)
        html = stage_noindex(html, rel)
        html = stage_schema(html, rel)
        html = stage_video(html)
        html = stage_fonts(html)

        if html != orig:
            open(path, "w", encoding="utf-8").write(html)
            print(f"[zmieniono] {rel or '/'}  ({len(orig)-len(html):+d} B)")

    # ------------------------------------------------------------ K. pliki
    open(os.path.join(SITE, "llms.txt"), "w", encoding="utf-8").write(f"""# CreGAAtine

> CreGAAtine to monohydrat kreatyny połączony z kwasem guanidynooctowym (GAA).
> Połączenie podnosi poziom kreatyny w mięśniach do 16,9% zamiast około 2%
> przy samym monohydracie -- 8,5 raza więcej -- bez retencji wody podskórnej.
> Formuła opiera się na badaniach prof. dr. Sergeja Ostojicia (Applied Bioenergetics).

## Strony kluczowe

- [Produkt CreGAAtine]({BASE}/cregaatine-naukowa-rewolucja-kreatyny/): skład, działanie, dawkowanie
- [Badania naukowe nad GAA i kreatyną]({BASE}/gaa-i-kreatyna-badania-naukowe/): wyniki badań prof. Ostojicia
- [Wykład prof. Sergeja Ostojicia]({BASE}/wyklad-pionier-w-badaniu-kreatyny-i-gaa-prof-sergej-ostojic/)
- [Odpowiedzi prof. Ostojicia na pytania]({BASE}/prof-dr-sergej-ostojic-odpowiada-na-pytania-dotyczace-cregaatine-czesc-1/)
- [Podcast z prof. Ostojiciem]({BASE}/aa/)

## Powiązane

- [Karnozyna w mięśniach sportowca]({BASE}/karnozyna-w-miesniach-sportowca/)
- [Potrójna suplementacja: karnozyna, GAA i kreatyna]({BASE}/potrojna-suplementacja-karnozyna-gaa-i-kreatyna/)
- [Blog]({BASE}/blog/)

## Sklep

- https://sklep.cregaatine.pl/
""")
    print("[zapisano] llms.txt")

    redirects = [
        ("/dawka-wiedzy-naukowej/", "/gaa-i-kreatyna-badania-naukowe/"),
        ("/aa/", "/podcast-sergej-ostojic/"),
    ]
    open(os.path.join(SITE, "_redirects"), "w", encoding="utf-8").write(
        "\n".join(f"{a}  {b}  301" for a, b in redirects[:1]) + "\n")
    open(os.path.join(SITE, ".htaccess"), "w", encoding="utf-8").write(
        "# 301: duplikat treści -> wersja kanoniczna\n"
        "Redirect 301 /dawka-wiedzy-naukowej/ https://cregaatine.pl/gaa-i-kreatyna-badania-naukowe/\n"
        "\n"
        "# Kompresja i cache dla statycznych assetów\n"
        "<IfModule mod_deflate.c>\n"
        "  AddOutputFilterByType DEFLATE text/html text/css application/javascript "
        "application/json image/svg+xml\n"
        "</IfModule>\n"
        "<IfModule mod_expires.c>\n"
        "  ExpiresActive On\n"
        "  ExpiresByType image/webp \"access plus 1 year\"\n"
        "  ExpiresByType image/jpeg \"access plus 1 year\"\n"
        "  ExpiresByType image/png \"access plus 1 year\"\n"
        "  ExpiresByType text/css \"access plus 1 year\"\n"
        "  ExpiresByType application/javascript \"access plus 1 year\"\n"
        "</IfModule>\n")
    print("[zapisano] _redirects, .htaccess")

    print("\n=== PODSUMOWANIE ===")
    for k in sorted(stats):
        print(f"  {k}: {stats[k]}")


if __name__ == "__main__":
    main()
