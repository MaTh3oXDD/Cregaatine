# CreGAAtine — folder social media

Materiały na profil FB **facebook.com/cregaatine.polska**. Wszystko 1080×1080 px,
wyrenderowane w 2× (pliki PNG mają 2160×2160 — Facebook nie zmiękczy typografii).

## Co jest w środku

```
social/
├─ templates/   5 czystych teł — wrzucasz na nie własny tekst
├─ posty/       3 gotowe propozycje postów
├─ start/       3 posty na powrót po przerwie
├─ evergreen/   10 postów ogólnych (czym jest, dla kogo, czym się różni)
├─ _assets/     base.css (system), logo, fonty w base64
└─ _build/      build.py — generuje HTML i renderuje PNG
```

## System wizualny

| element | wartość |
|---|---|
| żółty | `#F9DF1C` (ze strony) |
| grafit / czerń | `#282828` / `#0E0E0E` |
| papier | `#F2F1EC` |
| display | Saira Condensed 800, wersaliki, pochylenie −7° |
| tekst | Inter 400/500 |
| margines bezpieczny | 92 px |

Sygnaturą jest **odwrócony trójkąt z logotypu**. Wraca na każdym formacie jako
element konstrukcyjny: pasek nagłówka, wcięcie w rogu, znacznik kończący linię.
Dzięki temu post jest rozpoznawalny w feedzie, zanim ktoś przeczyta pierwsze słowo.

## Tła (templates/)

1. **tlo-01-klin** — czerń, żółty klin u góry. Pod nim jedno mocne zdanie.
2. **tlo-02-siatka** — czerń z mikro-siatką. Pod treści naukowe, wykresy, cytaty z badań.
3. **tlo-03-zolte** — żółte pole z czarnym wcięciem. Krótkie hasła, promocje.
4. **tlo-04-skos** — skos czerń/żółć. Porównania „przed / po”, „to vs tamto”.
5. **tlo-05-papier** — jasne tło, cienka ramka. Dłuższe teksty, cytaty eksperta.

Tekst kładź w obrębie 92 px marginesu, w wersalikach Saira Condensed.
Nagłówek 90–130 px, tekst 28–32 px.

## Posty (posty/)

**post-1-8-5x** — liczba jako bohater. 8,5× to najmocniejszy argument, jaki macie.
Podpis:
> Zwykła kreatyna podnosi poziom w mięśniach o około 2%. CreGAAtine — o 16,9%.
> To 8,5 razy więcej z tej samej porcji, bo obok monohydratu dostajesz GAA,
> prekursor kreatyny. Szczegóły i badania: cregaatine.pl

**post-2-porownanie** — zdanie ze strony głównej rozbite na dwa pola.
Podpis:
> Nie mamy nic do monohydratu. Po prostu zmierzyliśmy, ile kreatyny naprawdę
> dociera do mięśni — i dołożyliśmy GAA, żeby dotarło jej więcej.

**post-3-retencja** — jedna korzyść, zero ozdób. Pod sporty wagowe.
Podpis:
> Bez wody podskórnej. Waga rano taka, jakiej się spodziewasz — to ma znaczenie,
> gdy walczysz o kategorię. 60 saszetek, 2×2000 mg dziennie.

## Start (start/) — kolejność publikacji po przerwie

Publikuj w tej kolejności, co 2–3 dni. Najpierw powiedz, że wracacie, potem
przypomnij, dlaczego warto słuchać, dopiero na końcu wchodź w produkt.

**1. start-1-wracamy** — otwarcie. Bez wymówek, bez „przepraszamy za ciszę”.
> Wracamy na ten profil. Będą tu badania nad kreatyną i GAA, rozbiory składów
> i odpowiedzi na wasze pytania — bez marketingowego lania wody.
> Piszcie w komentarzach, co chcecie rozłożyć na czynniki pierwsze.

**2. start-2-fiwe** — dowód. Nagroda FIWE 2021 i wyróżnienie ESPEN.
> Suplement roku FIWE 2021 i nagroda ESPEN za wyniki badań. Formuła jest
> opatentowana i zweryfikowana pod kątem dopingu — sprawdzana, zanim trafi do saszetki.

**3. start-3-gaa** — edukacja. Ludzie znają kreatynę, nie znają GAA.
> GAA to kwas guanidynooctowy: prekursor, z którego organizm sam robi kreatynę —
> również w mózgu, gdzie monohydrat dociera słabo. W porcji dziennej masz
> 2000 mg GAA i 2000 mg monohydratu. Pytania zadawajcie w komentarzach.

Do każdego posta dawaj link do cregaatine.pl. Zdjęcie profilowe i cover zrób
z `tlo-01-klin` — profil i feed będą trzymały jedną linię.

## Evergreen (evergreen/) — 10 postów ogólnych

Treści bez terminu ważności: czym jest produkt, dla kogo, czym się różni od
konkurencji. Można je publikować w dowolnej kolejności i wracać do nich za rok.
Rozruch profilu: **01 → 02 → 04 → 06 → 10**. Najpierw kim jesteście i dla kogo,
potem różnica, na końcu detale produktu.

**ever-01-czym-jest** — post-kotwica, przypnij na górze profilu.
> CreGAAtine to kreatyna z GAA — kwasem guanidynooctowym, z którego organizm sam
> produkuje kreatynę. Dwa składniki, 2×2000 mg w porcji dziennej.

**ever-02-dla-kogo** — pięć grup, po jednym powodzie.
> Siłownia, sporty walki, wytrzymałość, praca umysłowa, wiek 40+. Kreatyny
> potrzebuje każda z tych grup, tylko z innego powodu.

**ever-03-nie-dla-kazdego** — komu odradzamy. Buduje zaufanie mocniej niż dziesięć
postów o korzyściach.
> Ciąża, karmienie, dzieci, uczulenie na składnik. I to, o czym mało kto pisze:
> suplement nie zastąpi diety ani snu.

**ever-04-2-vs-16** — liczba i mechanizm zamiast przymiotników.
> Monohydrat podnosi poziom kreatyny w mięśniu o 2%. CreGAAtine o 16,9%.
> Różnicę robi GAA, który otwiera komórce dodatkowe drogi dostarczania.

**ever-05-jak-wybrac** — poradnik branżowy, nie reklama.
> Cztery rzeczy do sprawdzenia na każdej kreatynie: odmierzona porcja, krótki
> skład, badania i kontrola antydopingowa.

**ever-06-mozg** — temat, o którym konkurencja milczy.
> Kreatyna zasila też komórki nerwowe. CreGAAtine dostarcza jej 3,9× więcej do
> istoty szarej i 1,9× do białej.

**ever-07-mit-woda** — seria „mity”, wracaj co miesiąc z nowym.
> „Kreatyna zalewa wodą” — nie ta. CreGAAtine nie zatrzymuje wody podskórnej.

**ever-08-mleko** — ciekawostka pod udostępnienia.
> Ludzkie mleko zawiera i kreatynę, i GAA. Ten sam duet, który jest w saszetce.

**ever-09-badania** — dla sceptyków pytających o dowody.
> Ponad 200 badań nad GAA, nagroda ESPEN, prof. Sergej Ostojić. Podsumowanie
> naukowe do pobrania na cregaatine.pl.

**ever-10-saszetka** — różnica widoczna bez powoływania się na badania.
> Kreatyna luzem traci moc, a każda miarka jest inna. 60 odmierzonych saszetek
> w trójwarstwowej folii.

Przebudowa: `python _build/build_evergreen.py`

### Struktury tła

Żaden post nie stoi na płaskim polu. Cztery tekstury, wszystkie poniżej 9%
kontrastu, przypisane do tematu:

| klasa | co to jest | gdzie |
|---|---|---|
| `.tex-lattice` | krata pod kątem 46,4° — kąt zboczy klina z logo | 01, 03, 04, 09, 10 |
| `.tex-grid` | siatka pomiarowa 60 px | 04, 06, 09, 10 |
| `.tex-rings` | koncentryczne pierścienie: kreatyna rozchodząca się do komórki | 06, 07, 08 |
| `.tex-rules` | poziome linie, jak notatki laboratoryjne | 02, 05 |

Natężenie ustawia klasa podłoża (`.on-ink`, `.on-gold`, `.on-paper`), a warstwa
`.tex-fade-*` wygasza teksturę na środku kadru, żeby nie właziła pod typografię.
Wszystko siedzi w `_assets/base.css` — działa też dla `templates/`.

## Jak zmienić treść

Teksty siedzą w `_build/build.py`. Zmieniasz string, uruchamiasz:

```
cd social
python _build/build.py
```

Posty evergreen siedzą w `_build/build_evergreen.py` i mają własne wywołanie.
Skrypt nadpisuje HTML-e i renderuje PNG przez Chrome (headless, 2×).
Fonty są wklejone w `_assets/fonts/fonts.css` jako base64 — render działa offline.
