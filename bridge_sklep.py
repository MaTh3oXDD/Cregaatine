# -*- coding: utf-8 -*-
"""Most między cregaatine.pl a sklepem Carnomed.

Uruchamiaj po `inject_enhance.py`. Skrypt jest idempotentny — drugie
uruchomienie nic nie zmieni (wstawione bloki są znakowane `data-cm-bridge`).

Robi cztery rzeczy:

1. Naprawia pozycję „SKLEP" w menu. Prowadziła na https://sklep.cregaatine.pl/,
   a ten adres zwraca 503 i stronę-zaślepkę Sellingo — czyli główny przycisk
   zakupowy na całej witrynie nie prowadził donikąd. Nowy cel to karta
   produktu w sklepie, który faktycznie sprzedaje CreGAAtine.
2. Ujednolica etykiety przycisków prowadzących do sklepu. Były trzy różne
   („#CreGAAtine - Zamów już teraz", „przejdź do sklepu"), a żadna nie mówiła,
   czyj jest sklep. Wszystkie brzmią teraz tak samo, tak jak nazywa się
   czynność po drugiej stronie.
3. Dokłada pod przyciskami płytę z informacją, kto prowadzi sklep i pod jakim
   adresem, ze znakiem Carnomed. Ten sam znak stoi w nagłówku sklepu.
4. Podpina arkusz `bridge.css`.

Tekst płyty jest bliźniaczy z tym w Carnomed/sklep/custom.src.css
(sekcja „strony CreGAAtine"). Zmiana tu wymaga zmiany tam.
"""
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")

SKLEP_MARTWY = "https://sklep.cregaatine.pl/"
SKLEP = "https://sklep.carno-med.pl/cregaatine-kreatyna-gaa"

ETYKIETA = "Kup w sklepie Carnomed"

CSS_TAG = '<link rel="stylesheet" id="cm-bridge-css" href="/assets/css/bridge.css">\n'

ZDANIE = ("Zamówienie przyjmuje Carnomed sp. z o.o., wyłączny dystrybutor "
          "CreGAAtine w Polsce.")

PLYTA = (
    '<div class="cm-bridge" data-cm-bridge>'
    '<img class="cm-bridge__mark" src="/assets/img/carnomed-logo-white.svg" '
    'alt="Carnomed" width="148" height="17" loading="lazy" decoding="async">'
    '<p class="cm-bridge__text">' + ZDANIE +
    '<span class="cm-bridge__host">sklep.carno-med.pl</span></p>'
    '</div>'
)

LINIA = (
    '<p class="cm-bridge cm-bridge--inline" data-cm-bridge>' + ZDANIE +
    ' Kupujesz na <span class="cm-bridge__host">sklep.carno-med.pl</span>.</p>'
)

# Przyciski sklepu siedzą w Divi w takim opakowaniu:
#   <div class="et_pb_button_module_wrapper ..."> <a ...>etykieta</a> </div>
# Płyta wchodzi za całym opakowaniem, nie za samym <a>, żeby nie wpaść
# do środka wyśrodkowanego bloku przycisku i nie odziedziczyć jego szerokości.
WRAPPER = re.compile(
    r'(<div class="et_pb_button_module_wrapper[^"]*"[^>]*>\s*'
    r'<a class="[^"]*"[^>]*href="https://sklep\.carno-med\.pl[^"]*"[^>]*>'
    r'[^<]*</a>\s*</div>)',
    re.S,
)

HERO_CTA = re.compile(
    r'(<div class="hero-ctas">.*?</div>)',
    re.S,
)

ANCHOR_SKLEP = re.compile(
    r'(<a\b[^>]*href="https://sklep\.carno-med\.pl[^"]*"[^>]*>)([^<]*)(</a>)'
)


def strony():
    for katalog, _, pliki in os.walk(SITE):
        if "assets" in katalog.split(os.sep):
            continue
        if "index.html" in pliki:
            yield os.path.join(katalog, "index.html")


def przerob(html):
    zmiany = []

    # 1. martwa domena sklepu -> karta produktu
    if SKLEP_MARTWY in html:
        html = html.replace(SKLEP_MARTWY, SKLEP)
        zmiany.append("menu")

    # 2. jedna etykieta dla wszystkich przycisków sklepu
    def etykieta(m):
        tekst = m.group(2).strip()
        if not tekst or tekst == ETYKIETA:
            return m.group(0)
        return m.group(1) + ETYKIETA + m.group(3)

    # W menu zostaje „SKLEP": tam etykieta jest pozycją nawigacji, nie
    # wezwaniem do działania, a pełne zdanie rozwaliłoby rząd nawigacji.
    # Klasy `menu-item` siedzą na <li>, nie na <a>, więc rozpoznajemy po treści.
    def poza_menu(m):
        if m.group(2).strip().upper() == "SKLEP":
            return m.group(0)
        return etykieta(m)

    nowy = ANCHOR_SKLEP.sub(poza_menu, html)
    if nowy != html:
        html = nowy
        zmiany.append("etykiety")

    # 3. płyta pod przyciskami i linia pod hero
    if "data-cm-bridge" not in html:
        if WRAPPER.search(html):
            html = WRAPPER.sub(lambda m: m.group(1) + PLYTA, html)
            zmiany.append("plyta")
        if HERO_CTA.search(html) and "sklep.carno-med.pl" in html:
            html = HERO_CTA.sub(lambda m: m.group(1) + LINIA, html, count=1)
            zmiany.append("linia")

    # 4. arkusz
    if "cm-bridge-css" not in html and "</head>" in html:
        html = html.replace("</head>", CSS_TAG + "</head>", 1)
        zmiany.append("css")

    return html, zmiany


def main():
    zmienione = 0
    for sciezka in strony():
        html = open(sciezka, encoding="utf-8").read()
        nowy, zmiany = przerob(html)
        if nowy != html:
            with open(sciezka, "w", encoding="utf-8") as f:
                f.write(nowy)
            zmienione += 1
            print(os.path.relpath(sciezka, SITE), "->", ", ".join(zmiany))
    print("stron zmienionych:", zmienione)


if __name__ == "__main__":
    main()
