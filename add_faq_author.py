# -*- coding: utf-8 -*-
"""FAQ z FAQPage schema na stronie produktowej, przypis do twierdzenia 8,5x
oraz usunięcie adresu e-mail z pola autora.

Odpowiedzi FAQ pochodzą wyłącznie z treści już opublikowanej na stronie --
nic nie jest dopisywane od siebie.
"""
import os
import re
import glob
import json

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")
BASE = "https://cregaatine.pl"
PROD = os.path.join(SITE, "cregaatine-naukowa-rewolucja-kreatyny", "index.html")

FAQ = [
    ("Czym CreGAAtine różni się od zwykłego monohydratu kreatyny?",
     "CreGAAtine łączy monohydrat kreatyny z kwasem guanidynooctowym (GAA). W badaniu "
     "Semeredi i in. (2018) grupa przyjmująca 1 g GAA i 3 g kreatyny dziennie przez "
     "4 tygodnie zwiększyła poziom kreatyny w mięśniach o 16,9%, a grupa przyjmująca "
     "samą kreatynę (4 g dziennie) o 2%. Stąd 8,5 raza większa efektywność."),
    ("Jak dawkować CreGAAtine?",
     "Jedna saszetka odpowiada dawce badanej naukowo: 1 g GAA i 3 g monohydratu kreatyny. "
     "W badaniach klinicznych taką dawkę przyjmowano raz dziennie przez 4 tygodnie. "
     "Opakowanie zawiera 60 saszetek."),
    ("Czy CreGAAtine powoduje retencję wody podskórnej?",
     "Nie. Brak retencji wody podskórnej ma znaczenie zwłaszcza w sportach wrażliwych "
     "na wagę, gdzie zatrzymanie wody utrudnia utrzymanie limitu kategorii."),
    ("Czy suplementacja GAA jest bezpieczna?",
     "W kontrolowanych badaniach na zdrowych ludziach przy dawce 1 g GAA w połączeniu "
     "z 3 g kreatyny przez 4 tygodnie nie zaobserwowano efektów ubocznych. W badaniu "
     "Ostojicia i in. (2013) GAA podawano w dawce 2,4 g dziennie przez 6 tygodni i nie "
     "stwierdzono istotnych statystycznie różnic względem grupy placebo."),
    ("Dlaczego połączenie GAA z kreatyną działa skuteczniej niż sama kreatyna?",
     "Kreatyna i GAA mogą korzystać z tego samego białka transportowego CRT1, które "
     "znacznie chętniej wiąże kreatynę i szybko ulega przez nią wysyceniu. Gdy oba "
     "związki są dostarczane razem, GAA trafia do komórki niezależnymi transporterami, "
     "a w mięśniu jest metabolizowany do kreatyny. Powstają więc dodatkowe ścieżki "
     "dostarczania kreatyny."),
    ("Ile GAA zawiera jedna porcja CreGAAtine?",
     "Jeden gram. To około 100 razy więcej niż w kilogramie mięsa, gdzie typowa "
     "zawartość GAA wynosi około 10 mg/kg."),
    ("Dla kogo jest CreGAAtine?",
     "Dla sportowców, dla których wysoki poziom kreatyny w mięśniach jest kluczowy, oraz "
     "dla osób niejedzących mięsa -- na diecie wegańskiej zawartość kreatyny w mięśniach "
     "bywa nawet o 25% niższa. CreGAAtine przekracza barierę krew-mózg, więc bywa też "
     "stosowana dla poprawy pamięci i koncentracji."),
    ("Dlaczego CreGAAtine jest pakowana w pojedyncze saszetki?",
     "Kreatyna jest higroskopijna: pochłania wilgoć z powietrza i z czasem przechodzi "
     "w nieaktywną kreatyninę. W opakowaniach zbiorczych produkty kreatynowe tracą nawet "
     "50% mocy. Saszetka z folii triplex klasy farmaceutycznej chroni proszek przed wilgocią."),
    ("Czy CreGAAtine ma certyfikat antydopingowy?",
     "Tak. CreGAAtine posiada certyfikat antydopingowy przyznany przez LGC Group."),
]

FAQ_CSS = (
    '<style id="faq-inline-css">'
    '.faq-seo{max-width:1080px;margin:0 auto;padding:40px 20px}'
    '.faq-seo h2{font-size:28px;line-height:1.3;margin:0 0 24px}'
    '.faq-seo details{border-bottom:1px solid rgba(0,0,0,.12)}'
    '.faq-seo summary{cursor:pointer;list-style:none;padding:18px 34px 18px 0;'
    'position:relative;font-weight:600;font-size:17px;line-height:1.45}'
    '.faq-seo summary::-webkit-details-marker{display:none}'
    '.faq-seo summary::after{content:"+";position:absolute;right:6px;top:16px;'
    'font-size:24px;font-weight:400;line-height:1}'
    '.faq-seo details[open] summary::after{content:"\\2013"}'
    '.faq-seo details p{margin:0 0 20px;line-height:1.65}'
    '</style>'
)


def build_faq_html():
    items = "".join(
        f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQ)
    return ('<div class="et_pb_module et_pb_text et_pb_text_align_left et_pb_bg_layout_light">'
            '<div class="et_pb_text_inner"><section class="faq-seo" id="faq">'
            f'<h2>Najczęstsze pytania o CreGAAtine</h2>{items}</section></div></div>')


def add_faq():
    html = open(PROD, encoding="utf-8").read()
    if 'class="faq-seo"' in html:
        print("[FAQ] juz jest")
        return
    anchor = ('<div class="et_pb_module et_pb_text et_pb_text_20  '
              'et_pb_text_align_left et_pb_bg_layout_light">')
    if anchor not in html:
        print("[FAQ] BLAD: nie znaleziono miejsca wstawienia")
        return
    html = html.replace(anchor, build_faq_html() + anchor, 1)
    html = html.replace("</head>", FAQ_CSS + "\n</head>", 1)

    m = re.search(r'(<script type="application/ld\+json"[^>]*>)(.*?)(</script>)', html, re.S)
    data = json.loads(m.group(2))
    if not any(n.get("@type") == "FAQPage" for n in data["@graph"]):
        data["@graph"].append({
            "@type": "FAQPage",
            "@id": BASE + "/cregaatine-naukowa-rewolucja-kreatyny/#faq",
            "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in FAQ],
        })
    new = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    html = html[:m.start()] + m.group(1) + new + m.group(3) + html[m.end():]
    open(PROD, "w", encoding="utf-8").write(html)
    print("[FAQ] dodano %d pytan + FAQPage schema" % len(FAQ))


CITE = (' <cite style="font-style:normal;font-size:.9em">(Semeredi i in., '
        '<a href="https://www.sciencedirect.com/science/article/abs/pii/S0899900718303484" '
        'rel="nofollow noopener" target="_blank"><em>Nutrition</em>, 2018</a>)</cite>')

MARKER = ("Powyższe badanie wskazuje więc, że strategia suplementacyjna oparta o "
          "jednoczesne przyjmowanie GAA i kreatyny podnosi poziom kreatyny w "
          "mięśniach aż 8.5 razy skuteczniej niż sama kreatyna.")


def add_citation():
    html = open(PROD, encoding="utf-8").read()
    if "Semeredi i in." in html:
        print("[przypis] juz jest")
        return
    if MARKER not in html:
        print("[przypis] BLAD: nie znaleziono zdania z twierdzeniem 8,5x")
        return
    open(PROD, "w", encoding="utf-8").write(html.replace(MARKER, MARKER + CITE, 1))
    print("[przypis] dodano cytowanie przy twierdzeniu 8,5x")


AUTHOR_OLD = "marcin@carno-med.pl"
AUTHOR_NEW = "Redakcja CreGAAtine"


def fix_author():
    """Adres e-mail jako nazwa autora to najslabszy sygnal E-E-A-T na stronie
    o suplementach. Docelowo powinno tu stac imie i nazwisko eksperta z biogramem."""
    n = 0
    for path in glob.glob(os.path.join(SITE, "**", "index.html"), recursive=True):
        html = open(path, encoding="utf-8").read()
        if AUTHOR_OLD not in html:
            continue
        new = html.replace(AUTHOR_OLD, AUTHOR_NEW)
        new = new.replace("mailto:" + AUTHOR_NEW, "mailto:" + AUTHOR_OLD)
        if new != html:
            open(path, "w", encoding="utf-8").write(new)
            n += 1
    print("[autor] zamieniono e-mail na nazwe redakcyjna w %d plikach" % n)


if __name__ == "__main__":
    add_faq()
    add_citation()
    fix_author()
