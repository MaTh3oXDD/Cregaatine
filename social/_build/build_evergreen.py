# -*- coding: utf-8 -*-
"""10 postów evergreen — treści ogólne: czym jest produkt, dla kogo, czym się różni.
Renderuje do social/evergreen/ jako PNG 2160x2160.

Uruchomienie:  python _build/build_evergreen.py   (z katalogu social/)
"""
import os, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
OUT = "evergreen"

HEAD = """<!doctype html>
<meta charset="utf-8">
<title>{title}</title>
<link rel="stylesheet" href="../_assets/fonts/fonts.css">
<link rel="stylesheet" href="../_assets/base.css">
<style>{css}</style>
"""

PAGES = []


def add(name, title, css, html):
    os.makedirs(os.path.join(ROOT, OUT), exist_ok=True)
    path = os.path.join(ROOT, OUT, name + ".html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(HEAD.format(title=title, css=css) + html)
    PAGES.append(path)


# --- wspólne bloki powtarzane w kilku postach -------------------------
LIST_CSS = """
.rows { position:absolute; left:92px; right:92px; }
.row { padding:22px 0; border-bottom:1.5px solid rgba(14,14,14,0.16); }
.row.dark { border-bottom-color:rgba(255,255,255,0.14); }
.row b { font-family:'Saira Condensed',sans-serif; font-weight:800; text-transform:uppercase;
         font-size:42px; line-height:1; display:block; }
.row span { display:block; margin-top:8px; font-size:25px; color:rgba(14,14,14,0.66); }
.row.dark span { color:rgba(255,255,255,0.68); }
.bullet { display:flex; gap:22px; align-items:flex-start; margin-bottom:30px; }
.bullet i { flex:none; width:26px; height:14px; margin-top:12px; background:var(--ink);
            clip-path:polygon(0 0, 100% 0, 50% 100%); }
.bullet i.y { background:var(--yellow); }
.bullet p { font-size:29px; line-height:1.4; color:rgba(14,14,14,0.78); }
.bullet p.on-dark { color:rgba(255,255,255,0.8); }
"""

# =====================================================================
# 01 — Czym jest CreGAAtine
# =====================================================================
add("ever-01-czym-jest", "Czym jest CreGAAtine", """
.wedge-top { top:0; left:0; width:1080px; height:230px; }
.head { top:96px; text-align:center; }
.head .eyebrow { color:var(--ink); }
.title { top:320px; right:auto; width:600px; }
.title .display { font-size:104px; color:var(--yellow); }
.copy { top:530px; right:auto; width:460px; }
.copy .body-copy { font-size:26px; }
.shot { position:absolute; right:-60px; bottom:150px; width:580px;
        filter: drop-shadow(0 30px 50px rgba(0,0,0,0.6)); }
.foot { bottom:92px; }
.foot .meta { margin-top:24px; }
""", """
<div class="canvas">
  <div class="tex tex-lattice on-ink"></div>
  <div class="tex-fade-ink"></div>
  <div class="wedge wedge-top"></div>
  <div class="stack head"><div class="eyebrow">Podstawy</div></div>
  <div class="stack title"><div class="display oblique">Kreatyna<br>+ GAA</div></div>
  <div class="stack copy">
    <div class="body-copy">Opatentowana mieszanka kreatyny i GAA. Organizm sam robi z GAA kreatynę — także w mózgu, gdzie monohydrat dociera słabo.</div>
  </div>
  <img class="shot" src="../_assets/produkt.png" alt="Opakowanie CreGAAtine">
  <div class="stack foot">
    <div class="rule"></div>
    <div class="meta">2&times;2000 mg dziennie · 60 saszetek · cregaatine.pl</div>
  </div>
</div>
""")

# =====================================================================
# 02 — Dla kogo
# =====================================================================
add("ever-02-dla-kogo", "Dla kogo", """
.canvas { background: var(--paper); color: var(--ink); }
.tri { position:absolute; right:92px; top:92px; width:80px; height:42px; }
.head { top:120px; }
.head .display { font-size:112px; color:var(--ink); }
.rows { top:330px; }
.row b { color:var(--ink); }
.foot { bottom:92px; }
.foot .meta { color:rgba(14,14,14,0.45); }
""" + LIST_CSS, """
<div class="canvas">
  <div class="tex tex-rules on-paper"></div>
  <div class="tex-fade-paper"></div>
  <div class="frame"></div>
  <div class="wedge tri"></div>
  <div class="stack head">
    <div class="eyebrow on-yellow">Komu to służy</div>
    <div class="display" style="margin-top:24px">Dla kogo</div>
  </div>
  <div class="rows">
    <div class="row"><b>Siłownia</b><span>Więcej kreatyny w mięśniu to więcej powtórzeń w seriach na sile.</span></div>
    <div class="row"><b>Sporty walki i wagowe</b><span>Bez retencji wody — waga rano taka, jakiej się spodziewasz.</span></div>
    <div class="row"><b>Wytrzymałość</b><span>Lepsza bioenergetyka komórki przy powtarzanych wysiłkach.</span></div>
    <div class="row"><b>Praca umysłowa</b><span>Kreatyna zasila mózg: pamięć, uwaga, decyzje pod zmęczeniem.</span></div>
    <div class="row"><b>Po czterdziestce</b><span>Deficyt kreatyny rośnie z wiekiem, niezależnie od płci.</span></div>
  </div>
  <div class="stack foot"><div class="meta">cregaatine.pl</div></div>
</div>
""")

# =====================================================================
# 03 — Dla kogo NIE jest
# =====================================================================
add("ever-03-nie-dla-kazdego", "Nie dla każdego", """
.canvas { background: var(--yellow); color: var(--ink); }
.notch { top:0; right:0; width:300px; height:158px; }
.head { top:230px; }
.head .display { font-size:124px; color:var(--ink); }
.list { position:absolute; left:92px; right:150px; top:520px; }
.foot { bottom:92px; }
.foot .meta { color:rgba(14,14,14,0.55); margin-top:24px; }
""" + LIST_CSS, """
<div class="canvas">
  <div class="tex tex-lattice on-gold"></div>
  <div class="tex-fade-gold"></div>
  <div class="wedge ink notch"></div>
  <div class="frame"></div>
  <div class="stack head">
    <div class="eyebrow on-yellow">Uczciwie</div>
    <div class="display" style="margin-top:24px">Nie dla<br>każdego</div>
  </div>
  <div class="list">
    <div class="bullet"><i></i><p>Kobiety w ciąży i karmiące — najpierw rozmowa z lekarzem.</p></div>
    <div class="bullet"><i></i><p>Dzieci — produkt nie jest dla nich przeznaczony.</p></div>
    <div class="bullet"><i></i><p>Uczulenie na którykolwiek ze składników.</p></div>
    <div class="bullet"><i></i><p>Nikt nie zastąpi suplementem diety i snu. To dodatek, nie fundament.</p></div>
  </div>
  <div class="stack foot">
    <div class="rule on-light"></div>
    <div class="meta">Pełny skład i ostrzeżenia: cregaatine.pl</div>
  </div>
</div>
""")

# =====================================================================
# 04 — 2% vs 16,9%
# =====================================================================
add("ever-04-2-vs-16", "2% vs 16,9%", """
.canvas { background: var(--yellow); }
.dark { position:absolute; inset:0; background:var(--ink);
        clip-path: polygon(0 0, 1080px 0, 1080px 430px, 0 600px); }
.top { top:96px; }
.top .num { font-size:150px; color:#fff; }
.top .lab { font-size:27px; color:rgba(255,255,255,0.7); margin-top:14px; }
.bot { bottom:92px; }
.bot .num { font-size:170px; color:var(--ink); }
.bot .lab { font-size:29px; color:rgba(14,14,14,0.78); margin-top:16px; max-width:820px; }
.bot .meta2 { font-size:22px; color:rgba(14,14,14,0.6); margin-top:30px; }
""", """
<div class="canvas">
  <div class="tex tex-lattice on-gold"></div>
  <div class="tex-fade-gold"></div>
  <div class="dark"></div>
  <div class="tex tex-grid on-ink" style="clip-path: polygon(0 0, 1080px 0, 1080px 430px, 0 600px)"></div>
  <div class="stack top">
    <div class="eyebrow">Monohydrat sam</div>
    <div class="display num" style="margin-top:16px">2,0%</div>
    <div class="lab">Tyle kreatyny przybywa w mięśniu. Jedna droga wejścia do komórki.</div>
  </div>
  <div class="stack bot">
    <div class="eyebrow on-yellow">CreGAAtine</div>
    <div class="display oblique num" style="margin-top:16px">16,9%</div>
    <div class="lab">Osiem i pół raza więcej z tej samej porcji, bo GAA otwiera komórce cztery dodatkowe drogi dostarczania.</div>
    <div class="meta2">Nie mamy nic do monohydratu. Po prostu zmierzyliśmy, ile z niego dociera.</div>
  </div>
</div>
""")

# =====================================================================
# 05 — Jak wybrać kreatynę
# =====================================================================
add("ever-05-jak-wybrac", "Jak wybrać kreatynę", """
.canvas { background: var(--paper); color: var(--ink); }
.head { top:130px; }
.head .display { font-size:92px; color:var(--ink); }
.list { position:absolute; left:92px; right:120px; top:420px; }
.bullet p { font-size:27px; }
.foot { bottom:92px; }
.foot .meta { color:rgba(14,14,14,0.45); margin-top:24px; }
""" + LIST_CSS, """
<div class="canvas">
  <div class="tex tex-rules on-paper"></div>
  <div class="tex-fade-paper"></div>
  <div class="frame"></div>
  <div class="stack head">
    <div class="eyebrow on-yellow">Poradnik</div>
    <div class="display" style="margin-top:24px">Czego szukać<br>na etykiecie</div>
  </div>
  <div class="list">
    <div class="bullet"><i></i><p><b style="font-weight:600">Odmierzona porcja.</b> Saszetka zamiast miarki w wiaderku — dawka zawsze ta sama.</p></div>
    <div class="bullet"><i></i><p><b style="font-weight:600">Krótki skład.</b> Substancje czynne i przeciwzbrylająca. Reszta to wypełniacz.</p></div>
    <div class="bullet"><i></i><p><b style="font-weight:600">Badania, nie hasła.</b> Producent podaje wyniki i publikacje, a nie same przymiotniki.</p></div>
    <div class="bullet"><i></i><p><b style="font-weight:600">Kontrola antydopingowa.</b> Konieczna, jeśli startujesz w zawodach.</p></div>
  </div>
  <div class="stack foot"><div class="meta">cregaatine.pl</div></div>
</div>
""")

# =====================================================================
# 06 — Mózg też ją zużywa
# =====================================================================
add("ever-06-mozg", "Mózg też ją zużywa", """
.cell { position:absolute; width:60px; height:60px; background:var(--yellow); right:120px; top:180px; }
.head { top:150px; }
.head .display { font-size:112px; color:#fff; }
.head .body-copy { margin-top:34px; }
.rows { position:absolute; left:92px; right:92px; bottom:230px; }
.row { border-bottom:1.5px solid rgba(255,255,255,0.14); display:flex; justify-content:space-between; align-items:baseline; }
.row span { font-size:26px; color:rgba(255,255,255,0.78); }
.row b { font-family:'Saira Condensed',sans-serif; font-weight:800; font-size:52px; color:var(--yellow); }
.foot { bottom:92px; }
""", """
<div class="canvas">
  <div class="tex tex-grid on-ink"></div>
  <div class="tex tex-rings on-ink" style="--tex-x:78%; --tex-y:18%"></div>
  <div class="vignette"></div>
  <div class="cell"></div>
  <div class="stack head">
    <div class="eyebrow">Nie tylko mięśnie</div>
    <div class="display" style="margin-top:26px">Mózg też<br>ją zużywa</div>
    <div class="body-copy">Kreatyna zasila komórki nerwowe tak samo jak mięśniowe. GAA dowozi ją tam skuteczniej, bo korzysta z innych dróg transportu niż sam monohydrat.</div>
  </div>
  <div class="rows">
    <div class="row"><span>Kreatyna w istocie szarej</span><b>3,9&times;</b></div>
    <div class="row"><span>Kreatyna w istocie białej</span><b>1,9&times;</b></div>
  </div>
  <div class="stack foot"><div class="meta">Pamięć · uwaga · uczenie się · decyzje</div></div>
</div>
""")

# =====================================================================
# 07 — Mit: kreatyna zalewa wodą
# =====================================================================
add("ever-07-mit-woda", "Mit — kreatyna zalewa wodą", """
.canvas { background: var(--yellow); color: var(--ink); }
.notch { top:0; right:120px; width:260px; height:137px; }
.head { top:250px; }
.head .display { font-size:100px; color:var(--ink); }
.seam { position:absolute; left:92px; right:92px; top:640px; height:1.5px; background:rgba(14,14,14,0.25); }
.answer { top:700px; }
.answer .lead { font-family:'Saira Condensed',sans-serif; font-weight:800; text-transform:uppercase;
                font-size:44px; color:var(--ink); }
.answer .body-copy { margin-top:20px; max-width:840px; }
.foot { bottom:92px; }
.foot .meta { color:rgba(14,14,14,0.5); }
""", """
<div class="canvas">
  <div class="tex tex-rings on-gold" style="--tex-x:88%; --tex-y:12%"></div>
  <div class="tex-fade-gold"></div>
  <div class="wedge ink notch"></div>
  <div class="frame"></div>
  <div class="stack head">
    <div class="eyebrow on-yellow">Mit</div>
    <div class="display" style="margin-top:26px">„Kreatyna<br>zalewa wodą”</div>
  </div>
  <div class="seam"></div>
  <div class="stack answer">
    <div class="lead">Nie ta kreatyna</div>
    <div class="body-copy on-light">CreGAAtine nie zatrzymuje wody podskórnej. Dlatego sięgają po nią zawodnicy w sportach wrażliwych na wagę.</div>
  </div>
  <div class="stack foot"><div class="meta">cregaatine.pl</div></div>
</div>
""")

# =====================================================================
# 08 — Mleko matki
# =====================================================================
add("ever-08-mleko", "Natura to już wymyśliła", """
.wedge-top { top:0; left:50%; margin-left:-190px; width:380px; height:200px; }
.head { top:330px; }
.head .display { font-size:112px; color:var(--yellow); }
.head .body-copy { margin-top:40px; }
.foot { bottom:92px; }
.foot .meta { margin-top:24px; }
""", """
<div class="canvas">
  <div class="tex tex-rings on-ink" style="--tex-x:50%; --tex-y:6%"></div>
  <div class="tex-fade-ink"></div>
  <div class="wedge wedge-top"></div>
  <div class="stack head">
    <div class="eyebrow">Ciekawostka</div>
    <div class="display oblique" style="margin-top:26px">Natura to już<br>wymyśliła</div>
    <div class="body-copy">Ludzkie mleko zawiera i kreatynę, i GAA. Ten sam duet, który mamy w saszetce — organizm dostaje go od pierwszych dni życia, bo obie cząsteczki są mu potrzebne razem.</div>
  </div>
  <div class="stack foot">
    <div class="rule"></div>
    <div class="meta">cregaatine.pl</div>
  </div>
</div>
""")

# =====================================================================
# 09 — Ponad 200 badań
# =====================================================================
add("ever-09-badania", "Ponad 200 badań", """
.head { top:130px; }
.num { position:absolute; left:92px; top:215px; font-size:270px; color:var(--yellow); }
.lab { position:absolute; left:92px; right:92px; top:560px; }
.lab .display { font-size:76px; color:#fff; }
.rows { position:absolute; left:92px; right:92px; bottom:170px; }
.row { border-bottom:1.5px solid rgba(255,255,255,0.14); display:flex; justify-content:space-between; align-items:baseline; padding:20px 0; }
.row span { font-size:25px; color:rgba(255,255,255,0.75); }
.row b { font-family:'Saira Condensed',sans-serif; font-weight:800; font-size:34px; color:var(--yellow);
         text-transform:uppercase; }
.foot { bottom:92px; }
""", """
<div class="canvas">
  <div class="tex tex-grid on-ink"></div>
  <div class="tex tex-lattice on-ink"></div>
  <div class="vignette"></div>
  <div class="stack head"><div class="eyebrow">Skąd wiemy, że działa</div></div>
  <div class="display oblique num">200+</div>
  <div class="lab"><div class="display">badań naukowych<br>nad GAA</div></div>
  <div class="rows">
    <div class="row"><span>Nagroda za wyniki badań</span><b>ESPEN</b></div>
    <div class="row"><span>Badania nad kreatyną i GAA prowadzi</span><b>prof. Sergej Ostojić</b></div>
  </div>
  <div class="stack foot"><div class="meta">Podsumowanie naukowe do pobrania na cregaatine.pl</div></div>
</div>
""")

# =====================================================================
# 10 — Saszetka zamiast wiaderka
# =====================================================================
add("ever-10-saszetka", "Saszetka zamiast wiaderka", """
.canvas { background: var(--yellow); }
.dark { position:absolute; inset:0; background:var(--ink);
        clip-path: polygon(0 0, 1080px 0, 1080px 360px, 0 500px); }
.top { top:96px; }
.top .display { font-size:96px; color:#fff; }
.bot { bottom:92px; }
.bot .display { font-size:96px; color:var(--ink); }
.bot .body-copy { margin-top:28px; }
.specs { display:flex; gap:56px; margin-top:36px; }
.spec b { display:block; font-family:'Saira Condensed',sans-serif; font-weight:800; font-size:40px;
          color:var(--ink); line-height:1; }
.spec span { font-size:18px; letter-spacing:0.12em; text-transform:uppercase; color:rgba(14,14,14,0.62); }
""", """
<div class="canvas">
  <div class="tex tex-lattice on-gold"></div>
  <div class="tex-fade-gold"></div>
  <div class="dark"></div>
  <div class="tex tex-grid on-ink" style="clip-path: polygon(0 0, 1080px 0, 1080px 360px, 0 500px)"></div>
  <div class="stack top">
    <div class="eyebrow">Opakowanie</div>
    <div class="display" style="margin-top:24px">Miarka<br>to loteria.</div>
  </div>
  <div class="stack bot">
    <div class="display oblique">Saszetka<br>nie kłamie.</div>
    <div class="body-copy on-light">Kreatyna luzem traci moc, a każda miarka jest inna. Tu porcja jest odmierzona i zamknięta w trójwarstwowej folii klasy farmaceutycznej.</div>
    <div class="specs">
      <div class="spec"><b>60</b><span>saszetek</span></div>
      <div class="spec"><b>2&times;2000 mg</b><span>porcja dzienna</span></div>
      <div class="spec"><b>3</b><span>warstwy folii</span></div>
    </div>
  </div>
</div>
""")


def render(paths):
    for p in paths:
        out = p[:-5] + ".png"
        if os.path.exists(out):
            os.remove(out)
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=2", "--window-size=1080,1080",
                        "--virtual-time-budget=4000",
                        "--screenshot=" + out, "file:///" + p.replace("\\", "/")],
                       capture_output=True)
        size = os.path.getsize(out) if os.path.exists(out) else 0
        print(("OK  " if size else "FAIL"), os.path.relpath(out, ROOT), size)


if __name__ == "__main__":
    render(PAGES)
