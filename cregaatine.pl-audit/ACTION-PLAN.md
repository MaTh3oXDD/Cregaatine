# CreGAAtine — status naprawy SEO

Stan na 2026-08-30. Mirror w `site/`, 16 stron HTML.

Wynik startowy audytu: **41/100**. Wszystkie blokery Fazy 0 i całą Fazę 1 zamknięto w kodzie. Zostało pięć rzeczy, których nie da się zrobić z poziomu plików — opisane na dole w sekcji **DO ZROBIENIA PRZEZ CIEBIE**.

---

## DO ZROBIENIA PRZEZ CIEBIE

### 1. Film 141 MB — jedyny pozostały bloker

`site/wp-content/uploads/2021/09/Nowy-film.mp4` waży **141 MB** ze 146 MB całego katalogu `site/`. Jeden użytkownik mobilny na `/suplement-roku-fiwe/` zjada 141 MB transferu.

Osadzenie już ograniczono: `preload="none"` plus plakat, więc plik nie pobiera się, dopóki ktoś nie kliknie play. Ale kliknie.

Do wyboru:

- **Wrzuć na YouTube** i podmień `<video>` na iframe. Dodatkowo zyskujesz ruch z YouTube i możliwość podpięcia `VideoObject` schema z `embedUrl`.
- **Przekoduj** — na tej maszynie nie ma `ffmpeg`, więc nie zrobiłem tego automatycznie. Po instalacji:

  ```bash
  ffmpeg -i site/wp-content/uploads/2021/09/Nowy-film.mp4 \
    -vf scale=-2:720 -c:v libx264 -crf 26 -preset slow \
    -c:a aac -b:a 96k -movflags +faststart \
    site/wp-content/uploads/2021/09/nowy-film-720p.mp4
  ```

  Cel: ~5 MB. Potem podmień `src` w `site/suplement-roku-fiwe/index.html`.

**Nie wrzucaj mirrora z tym plikiem w obecnej postaci.**

### 2. Cena w `Product` schema

Na `/cregaatine-naukowa-rewolucja-kreatyny/` `Offer` ma `url`, `priceCurrency` i `availability`, ale nie ma `price` — nie znam Twojej ceny. Google potraktuje ofertę jako niekompletną i nie pokaże rich resulta z ceną.

Uzupełnij w `site/cregaatine-naukowa-rewolucja-kreatyny/index.html`, w bloku JSON-LD:

```json
"offers": {"@type":"Offer", ..., "price":"149.00", "priceValidUntil":"2027-12-31"}
```

Jeśli cena zmienia się często albo zależy od wariantu, użyj `AggregateOffer` z `lowPrice` i `highPrice`.

### 3. Prawdziwy autor zamiast „Redakcja CreGAAtine"

Adres e-mail w roli autora został usunięty — teraz wszędzie stoi „Redakcja CreGAAtine". To poprawa, ale nadal nie jest to sygnał E-E-A-T, jakiego Google oczekuje w kategorii YMYL.

Podaj imię i nazwisko realnej osoby oraz jej kwalifikacje (dietetyk, technolog żywności, farmaceuta), a podmienię `Person` schema, `author` w `Article` i tytuł archiwum autora.

Osobno: masz prof. dr. Sergeja Ostojicia i jego recenzowane badania. Jeśli zgodzi się figurować jako autor lub recenzent merytoryczny treści naukowych, to najmocniejszy pojedynczy sygnał, jaki ta strona może dostać — powiedz, a podepnę `Person` z `affiliation` i `sameAs` do publikacji.

### 4. Cienka treść na trzech stronach wideo

| Strona | Słowa |
|---|---|
| `/podcast-sergej-ostojic/` | 172 |
| `/prof-dr-sergej-ostojic-.../` | 179 |
| `/wyklad-pionier-.../` | 180 |

Każda to osadzone wideo bez tekstu. Transkrypt rozwiązuje to natychmiast: daje 1500+ słów unikalnej, cytowalnej treści od uznanego badacza i naprawia jednocześnie punkt widoczności w AI.

Wrzuć transkrypty (choćby surowe, z automatu) do repo — sformatuję je, rozbiję na sekcje z nagłówkami i podepnę `VideoObject` z `transcript`.

Alternatywa, jeśli transkryptów nie będzie: `noindex` na tych trzech stronach. Powiedz, którą drogę wybierasz.

### 5. Kategorie po stronie WordPressa

`/category/uncategorized/` dostało `noindex, follow` w mirrorze, ale nazwa kategorii siedzi w bazie WP. Zmień w panelu na tematyczne — `badania-naukowe`, `suplementacja` — i przegeneruj mirror. Sam mirror tego nie naprawi, bo przy następnym `mirror.py` wróci stara nazwa.

To samo dotyczy sklepu na `sklep.cregaatine.pl` (punkt 3.6 pierwotnego audytu) — decyzja infrastrukturalna, nie plikowa.

### 6. Po wdrożeniu

1. Google Search Console → Sitemaps → wyślij `https://cregaatine.pl/sitemap.xml`
2. GSC → Inspekcja URL → sprawdź kanoniczny wybrany przez Google dla `/`
3. **Lighthouse na `/` i `/cregaatine-naukowa-rewolucja-kreatyny/`** — sprawdź, który element jest faktycznie LCP. Obecnie `fetchpriority="high"` ma wykres `retencja.webp`; jeśli LCP okaże się logo w headerze, priorytet trzeba przenieść.
4. Rich Results Test na stronie produktowej — po uzupełnieniu ceny
5. Facebook Sharing Debugger → wymuś odświeżenie cache OG dla wszystkich 16 URL-i
6. Sprawdź, czy hosting czyta `site/_redirects` (format Netlify/Cloudflare Pages). Na Apache przepisz na `.htaccess`, na nginx na `return 301`.

---

## ZROBIONE

### Faza 0 — blokery

- **Absolutne URL-e przywrócone.** `canonical`, `og:url` i pola `@id`/`url`/`urlTemplate` w JSON-LD wskazują na `https://cregaatine.pl/...` na wszystkich 16 stronach. Linki nawigacyjne zostały względne, zgodnie z założeniem. Skrypt: `fix_seo_urls.py`.
- **`robots.txt`** z wskazaniem sitemapy.
- **`sitemap.xml`** — 11 URL-i, posortowane, bez archiwów autora, `uncategorized` i duplikatu `/dawka-wiedzy-naukowej/`.
- **Film** — `preload="none"` plus plakat WebP. Sam plik nadal do wymiany, patrz wyżej.

### Faza 1

- **`alt` na wszystkich obrazach.** Zero brakujących na 16 stronach (było 82 brakujących). Opisy rzeczowe, np. „Wykres: brak retencji wody podskórnej przy stosowaniu CreGAAtine".
- **`og:image`** 1200×630 na każdej stronie, razem z `og:image:width`, `og:image:height` i `twitter:image`. Plik `og-cregaatine.jpg` celowo zostaje JPG-iem — Facebook i LinkedIn nie renderują WebP w podglądach.
- **Schema.** Dołożone: `Product` z `Brand` i `Offer`, `Organization` z `ContactPoint` i `sameAs`, `FAQPage` z 9 realnymi pytaniami, `Article` z `author`/`datePublished`/`dateModified` na wpisach, `Person`, `ProfilePage`, `CollectionPage`. Wszystkie bloki JSON-LD parsują się poprawnie. `aggregateRating` świadomie pominięty — brak prawdziwych recenzji na stronie.
- **Autor** — e-mail zastąpiony nazwą, tytuł archiwum to „Autor bloga CreGAAtine | CreGAAtine".
- **Meta description** na wszystkich 16 stronach.
- **Jeden H1 na stronę** — wszędzie dokładnie jeden, łącznie z archiwami, które wcześniej nie miały żadnego. Logo w headerze przestało być nagłówkiem.

### Faza 2 — wydajność

- **Fonty przycięte.** 21 deklaracji `@font-face`, prawie wyłącznie WOFF2, razem 5 KB. Wcześniej te same kroje leciały w TTF, WOFF, EOT i SVG dla trzech user-agentów.
- **Ikony.** Fontawesome zredukowany do trzech plików WOFF2 (168 KB łącznie). Wersje EOT, TTF i SVG — w tym `fa-solid-900.svg` na 896 KB — usunięte.
- **Martwy JavaScript usunięty.** `mediaelement` (3 pliki JS, 2 arkusze CSS, blok tłumaczeń i `_wpmejsSettings`) — natywny `<video controls>` odtwarza film bez skórki WordPressa. `comment-reply.min.js` — formularz komentarzy na statycznym mirrorze i tak nic nie wysyła. Pliki skasowane z `wp-includes/js/`. Wcześniej wypadły `moment.js`, `icp.library.js` i `smush-lazy-load.min.js`.
- **Wspólny CSS wyniesiony z HTML-a.** `global-styles-inline-css` (10 KB) i `divi-style-inline-inline-css` (26 KB) były bajt w bajt identyczne na wszystkich 16 stronach. Trafiły do `/assets/css/wp-global-styles.css` i `/assets/css/divi-style.css` — pobierają się raz i siedzą w cache. **36 KB mniej w każdym dokumencie**, `<head>` strony głównej spadł ze 157 KB do 121 KB.
- **Obrazy w WebP** — 119 plików. Ostatnie trzy, do których odwoływał się wyłącznie CSS (`to_webp.py` skanował tylko atrybuty HTML), dorobione teraz: `post-2.png` **1572 KB → 61 KB**, `home-section5-bg.jpg` 43 → 16 KB, `home-section3-bgok.jpg` 29 → 6 KB. Razem **1,5 MB** mniej. Oryginały skasowane, odwołania w CSS przepisane.
- **LCP** — `retencja.webp` ma `fetchpriority="high"` i `alt`. Weryfikacja w Lighthouse po stronie użytkownika, patrz punkt 6.

### Faza 3 — struktura

- **Duplikat** — `/dawka-wiedzy-naukowej/` (2161 słów, identyczne z `/gaa-i-kreatyna-badania-naukowe/`) dostał 301 w `site/_redirects` i wypadł z sitemapy.
- **Slug `/aa/` → `/podcast-sergej-ostojic/`**, z 301 ze starego adresu. Przepisanych 35 odwołań w 12 plikach, licząc `llms.txt` i `sitemap.xml`.
- **`noindex, follow`** na obu stronach archiwum autora i obu stronach `uncategorized`.
- **Tytuły.** Sufiks skrócony z „ - CreGAAtine - Naukowa rewolucja kreatyny" (42 znaki) do „ | CreGAAtine" (13). Wszystkie 16 tytułów mieści się teraz w 58 znakach po zdekodowaniu encji — wcześniej sześć przekraczało limit, najdłuższy miał 116.
- **Linkowanie wewnętrzne hub-and-spoke.** Każdy wpis linkuje kontekstowo do strony produktowej i do sąsiednich wpisów. Kontrola linków: **0 zepsutych odwołań** wewnętrznych w całym mirrorze.

### Faza 4 — widoczność w AI

- **`FAQPage`** z 9 pytaniami na stronie produktowej: różnica wobec monohydratu, dawkowanie, retencja wody, bezpieczeństwo GAA, mechanizm połączenia, zawartość GAA w porcji, grupa docelowa, saszetki, certyfikat antydopingowy.
- **`llms.txt`** w katalogu głównym, z mapą treści i linkami do sklepu.
- Odpowiedzi w pierwszym akapicie i twarde liczby z przypisem — częściowo, w ramach przepisanych treści. Transkrypty (punkt 4 listy zadań) domkną resztę.

---

## Narzędzia w repo

| Skrypt | Rola |
|---|---|
| `mirror.py` | pobiera produkcję i buduje `site/` |
| `fix_seo_urls.py` | absolutne URL-e, `robots.txt`, `sitemap.xml` |
| `seo_fixes.py` | meta description, tytuły, H1, `og:image` |
| `add_faq_author.py` | `FAQPage`, `Product`, `Organization`, `Person` |
| `add_internal_links.py` | linkowanie hub-and-spoke |
| `to_webp.py` | konwersja obrazów z HTML-a (odwołania z CSS obsłużone osobno) |
| `trim_fonts.py`, `trim_iconfonts.py` | redukcja `@font-face` i Fontawesome |
| `unlazy.py` | `data-src` → `src` po usunięciu lazy-loadera |
| `inject_enhance.py` | wstrzykuje `/assets/css/enhance.css` i `/assets/js/enhance.js` |
| `postprocess.py` | martwy JS, wspólny CSS do plików, slug `/aa/`, obrazy z CSS, sortowanie sitemapy, kontrola linków |
| `bridge_sklep.py` | most do sklepu Carnomed: cel przycisków, etykiety, płyta z informacją, `bridge.css` |

**Uwaga przy ponownym uruchomieniu `mirror.py`:** nadpisze wszystkie poprawki. Uruchom pipeline w tej kolejności:

```
mirror.py → unlazy.py → fix_seo_urls.py → seo_fixes.py → add_faq_author.py
→ add_internal_links.py → trim_fonts.py → trim_iconfonts.py → to_webp.py
→ inject_enhance.py → postprocess.py → bridge_sklep.py
```

`bridge_sklep.py` idzie po `postprocess.py` i też jest idempotentny.

`postprocess.py` musi iść przed nim i jest idempotentny — puszczony drugi raz nic nie zmieni. Na koniec sam sprawdza linki wewnętrzne i wypisuje `[ok] 0 zepsutych linków`. Jeśli zobaczysz tam listę, coś w pipelinie poszło nie tak.

---

## Most do sklepu Carnomed

CreGAAtine sprzedaje Carnomed, na własnej domenie i we własnym motywie. Klient
wychodził więc z czarno-żółtej strony produktu na biało-zieloną stronę sklepu,
w chwili, w której ma podać dane karty. Do tego pozycja **SKLEP** w menu
prowadziła na `https://sklep.cregaatine.pl/`, a ten adres zwraca **503** i
stronę-zaślepkę Sellingo — główny przycisk zakupowy witryny nie prowadził
donikąd.

`bridge_sklep.py` naprawia to po stronie cregaatine.pl:

- wszystkie odnośniki do sklepu (menu i przyciski) prowadzą na
  `https://sklep.carno-med.pl/cregaatine-kreatyna-gaa`,
- przyciski mówią jednym głosem: **Kup w sklepie Carnomed**,
- pod przyciskami staje czarna płyta ze znakiem Carnomed, zdaniem
  „Zamówienie przyjmuje Carnomed sp. z o.o., wyłączny dystrybutor CreGAAtine
  w Polsce." i adresem sklepu; w hero to samo zdanie idzie jedną linią,
- wygląd płyty siedzi w `site/assets/css/bridge.css`, znak w
  `site/assets/img/carnomed-logo-white.svg`.

Druga połowa mostu jest po stronie sklepu, w
`Carnomed/sklep/custom.src.css`, sekcja **17. Strony CreGAAtine**: karta
produktu i kategoria CreGAAtine noszą czerń i żółć marki zamiast zieleni
Carnomedu, a nad okruszkami stoi bliźniacza płyta — tam ze znakiem CreGAAtine
i zdaniem w drugą stronę. Zmiana zdania po jednej stronie wymaga zmiany po
drugiej.
