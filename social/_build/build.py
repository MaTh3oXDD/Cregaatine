# -*- coding: utf-8 -*-
"""Generuje HTML dla wszystkich formatów social i renderuje je do PNG (1080x1080 @2x).

Uruchomienie:  python _build/build.py           (z katalogu social/)
"""
import os, subprocess, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

HEAD = """<!doctype html>
<meta charset="utf-8">
<title>{title}</title>
<link rel="stylesheet" href="../_assets/fonts/fonts.css">
<link rel="stylesheet" href="../_assets/base.css">
<style>{css}</style>
"""


def page(folder, name, title, css, html):
    path = os.path.join(ROOT, folder, name + ".html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(HEAD.format(title=title, css=css) + html)
    return path


PAGES = []


def add(folder, name, title, css, html):
    PAGES.append(page(folder, name, title, css, html))


# =====================================================================
# TŁA — 5 templatek. Czyste, bez tekstu. Wrzucasz na nie własny copy.
# =====================================================================

add("templates", "tlo-01-klin", "Tło 01 — Klin", """
.wedge-top { top:0; left:0; width:1080px; height:288px; }
.glow { position:absolute; left:50%; top:288px; width:520px; height:520px; transform:translate(-50%,-42%);
        background:radial-gradient(circle, rgba(249,223,28,0.16) 0%, transparent 62%); }
.base-rule { position:absolute; left:92px; right:92px; bottom:92px; }
""", """
<div class="canvas">
  <div class="wedge wedge-top"></div>
  <div class="glow"></div>
  <div class="rule base-rule"></div>
</div>
""")

add("templates", "tlo-02-siatka", "Tło 02 — Siatka", """
.cell { position:absolute; width:60px; height:60px; background:var(--yellow); }
.c1 { left:92px; top:848px; }
.c2 { left:152px; top:908px; background:rgba(249,223,28,0.30); }
""", """
<div class="canvas">
  <div class="grid-bg"></div>
  <div class="cell c1"></div>
  <div class="cell c2"></div>
  <div class="vignette"></div>
</div>
""")

add("templates", "tlo-03-zolte", "Tło 03 — Żółte pole", """
.canvas { background: var(--yellow); }
.notch { top:0; right:0; width:300px; height:158px; }
.seam { position:absolute; left:56px; right:56px; bottom:210px; height:1.5px; background:rgba(14,14,14,0.18); }
""", """
<div class="canvas">
  <div class="wedge ink notch"></div>
  <div class="frame"></div>
  <div class="seam"></div>
</div>
""")

add("templates", "tlo-04-skos", "Tło 04 — Skos", """
.canvas { background: var(--yellow); }
.dark { position:absolute; inset:0; background:var(--ink);
        clip-path: polygon(0 0, 1080px 0, 1080px 300px, 0 760px); }
.seam { position:absolute; inset:0; border:0;
        background:linear-gradient(163.6deg, transparent 0 calc(50% - 1px), rgba(249,223,28,0.9) calc(50% - 1px) calc(50% + 1px), transparent calc(50% + 1px)); opacity:0; }
.mark { position:absolute; left:92px; bottom:92px; width:88px; height:46px; }
""", """
<div class="canvas">
  <div class="dark"></div>
  <div class="wedge ink mark"></div>
</div>
""")

add("templates", "tlo-05-papier", "Tło 05 — Papier", """
.canvas { background: var(--paper); }
.tri { position:absolute; left:92px; bottom:92px; width:64px; height:34px; }
.top-rule { position:absolute; left:92px; right:92px; top:250px; height:1.5px; background:rgba(14,14,14,0.16); }
""", """
<div class="canvas">
  <div class="frame"></div>
  <div class="top-rule"></div>
  <div class="wedge tri"></div>
</div>
""")

# =====================================================================
# POSTY — 3 propozycje w kolorystyce marki
# =====================================================================

add("posty", "post-1-8-5x", "Post 1 — 8,5×", """
.wedge-top { top:0; left:0; width:1080px; height:230px; }
.head { top:96px; text-align:center; }
.head .eyebrow { color:var(--ink); }
.num { position:absolute; left:92px; top:330px; font-size:300px; color:var(--yellow); }
.claim { top:660px; }
.claim .display { font-size:78px; color:#fff; }
.foot { bottom:92px; }
.stats { display:flex; gap:64px; margin-top:26px; }
.stat b { display:block; font-family:'Saira Condensed',sans-serif; font-weight:800; font-size:52px; color:#fff; line-height:1; }
.stat span { font-size:18px; letter-spacing:0.12em; text-transform:uppercase; color:var(--mist); }
""", """
<div class="canvas">
  <div class="wedge wedge-top"></div>
  <div class="stack head"><div class="eyebrow">Kreatyna w mięśniach · pomiar</div></div>
  <div class="display oblique num">8,5&times;</div>
  <div class="stack claim">
    <div class="display">więcej kreatyny<br>niż monohydrat</div>
  </div>
  <div class="stack foot">
    <div class="rule"></div>
    <div class="stats">
      <div class="stat"><b>2,0%</b><span>monohydrat</span></div>
      <div class="stat"><b>16,9%</b><span>CreGAAtine</span></div>
      <div class="stat"><b>GAA</b><span>kwas guanidynooctowy</span></div>
    </div>
  </div>
</div>
""")

add("posty", "post-2-porownanie", "Post 2 — Porównanie", """
.canvas { background: var(--yellow); }
.dark { position:absolute; inset:0; background:var(--ink);
        clip-path: polygon(0 0, 1080px 0, 1080px 430px, 0 600px); }
.top { top:96px; }
.top .display { font-size:104px; color:#fff; }
.bot { bottom:92px; }
.bot .display { font-size:104px; color:var(--ink); }
.bars { margin:44px 0 34px; }
.brow { display:flex; align-items:center; gap:22px; margin-bottom:16px; }
.brow small { font-size:19px; letter-spacing:0.12em; text-transform:uppercase;
              color:rgba(14,14,14,0.78); width:230px; flex:none; }
.bar { height:12px; background:rgba(14,14,14,0.32); }
.bar.hi { background:var(--ink); }
.foot-meta { font-size:22px; color:rgba(14,14,14,0.7); }
""", """
<div class="canvas">
  <div class="dark"></div>
  <div class="stack top">
    <div class="eyebrow">Kreatyna w mięśniach</div>
    <div class="display" style="margin-top:24px">Kreatyna<br>jest dobra.</div>
  </div>
  <div class="stack bot">
    <div class="display oblique">CreGAAtine<br>jest lepsza.</div>
    <div class="bars">
      <div class="brow"><small>Monohydrat 2,0%</small><div class="bar" style="width:70px"></div></div>
      <div class="brow"><small>CreGAAtine 16,9%</small><div class="bar hi" style="width:590px"></div></div>
    </div>
    <div class="foot-meta">Opatentowana mieszanka kreatyny i jej prekursora GAA.</div>
  </div>
</div>
""")

add("posty", "post-3-retencja", "Post 3 — Bez retencji", """
.canvas { background: var(--paper); }
.notch { top:0; right:120px; width:260px; height:137px; background:var(--yellow); }
.head { top:250px; }
.head .display { font-size:132px; color:var(--ink); }
.head .body-copy { margin-top:36px; }
.foot { bottom:92px; }
.foot .meta { color:rgba(14,14,14,0.45); margin-top:24px; }
""", """
<div class="canvas">
  <div class="wedge notch"></div>
  <div class="frame"></div>
  <div class="stack head">
    <div class="eyebrow on-yellow">Sporty wagowe</div>
    <div class="display" style="margin-top:26px">Bez wody<br>pod skórą</div>
    <div class="body-copy on-light">CreGAAtine nie zatrzymuje wody podskórnej. Waga zostaje tam, gdzie ją ustawiłeś — rośnie tylko to, co ma rosnąć.</div>
  </div>
  <div class="stack foot">
    <div class="rule on-light"></div>
    <div class="meta">cregaatine.pl · 60 saszetek · 2&times;2000 mg</div>
  </div>
</div>
""")

# =====================================================================
# START — 3 posty na powrót po przerwie
# =====================================================================

add("start", "start-1-wracamy", "Start 1 — Wracamy", """
.wedge-top { top:0; left:50%; margin-left:-190px; width:380px; height:200px; }
.head { top:388px; }
.head .display { font-size:184px; color:var(--yellow); }
.head .body-copy { margin-top:44px; }
.foot { bottom:92px; }
.logo-row { display:flex; align-items:center; justify-content:space-between; margin-top:26px; }
""", """
<div class="canvas">
  <div class="wedge wedge-top"></div>
  <div class="stack head">
    <div class="display oblique">Wracamy</div>
    <div class="body-copy">Kilka lat ciszy na tym profilu. Od dziś publikujemy tu badania nad kreatyną i GAA, rozbiory składów i odpowiedzi na wasze pytania.</div>
  </div>
  <div class="stack foot">
    <div class="rule"></div>
    <div class="logo-row">
      <img class="logo" src="../_assets/logo.png" alt="CreGAAtine">
      <div class="meta">cregaatine.pl</div>
    </div>
  </div>
</div>
""")

add("start", "start-2-fiwe", "Start 2 — FIWE Awards", """
.canvas { background: var(--paper); }
.badge { position:absolute; left:50%; top:250px; margin-left:-95px; width:190px; height:100px; }
.head { top:430px; text-align:center; }
.head .display { font-size:120px; color:var(--ink); }
.head .eyebrow { color:rgba(14,14,14,0.55); }
.head .body-copy { margin:34px auto 0; text-align:center; }
.foot { bottom:92px; text-align:center; }
.foot .meta { color:rgba(14,14,14,0.45); margin-top:24px; }
""", """
<div class="canvas">
  <div class="frame"></div>
  <div class="wedge badge"></div>
  <div class="stack head">
    <div class="eyebrow">FIWE Awards 2021</div>
    <div class="display" style="margin-top:26px">Suplement<br>roku</div>
    <div class="body-copy on-light">Nagroda targów FIWE dla CreGAAtine. Do tego wyróżnienie Europejskiego Towarzystwa Żywienia Klinicznego i Metabolizmu (ESPEN) za wyniki badań.</div>
  </div>
  <div class="stack foot">
    <div class="rule on-light"></div>
    <div class="meta">Opatentowane · zweryfikowane pod kątem dopingu</div>
  </div>
</div>
""")

add("start", "start-3-gaa", "Start 3 — Co to GAA", """
.cell { position:absolute; width:60px; height:60px; background:var(--yellow); right:120px; top:180px; }
.head { top:150px; }
.head .display { font-size:126px; color:#fff; }
.head .body-copy { margin-top:36px; }
.spec { position:absolute; left:92px; right:92px; bottom:230px; }
.row { display:flex; justify-content:space-between; align-items:baseline; padding:22px 0; border-bottom:1.5px solid rgba(255,255,255,0.14); }
.row span { font-size:26px; color:rgba(255,255,255,0.78); }
.row b { font-family:'Saira Condensed',sans-serif; font-weight:800; font-size:44px; color:var(--yellow); }
.foot { bottom:92px; }
""", """
<div class="canvas">
  <div class="grid-bg"></div>
  <div class="vignette"></div>
  <div class="cell"></div>
  <div class="stack head">
    <div class="eyebrow">Skład · porcja dzienna</div>
    <div class="display" style="margin-top:26px">Czym jest<br>GAA?</div>
    <div class="body-copy">Kwas guanidynooctowy — naturalny prekursor kreatyny. Organizm robi z niego kreatynę tam, gdzie monohydrat sam nie dociera: w mięśniach i w mózgu.</div>
  </div>
  <div class="spec">
    <div class="row"><span>Kwas guanidynooctowy (GAA)</span><b>2000 mg</b></div>
    <div class="row"><span>Monohydrat kreatyny</span><b>2000 mg</b></div>
  </div>
  <div class="stack foot">
    <div class="meta">2 saszetki dziennie · 60 saszetek w opakowaniu</div>
  </div>
</div>
""")


# =====================================================================
# Render
# =====================================================================
def render(paths):
    for p in paths:
        out = p[:-5] + ".png"
        if os.path.exists(out):
            os.remove(out)
        cmd = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
               "--force-device-scale-factor=2", "--window-size=1080,1080",
               "--default-background-color=00000000",
               "--virtual-time-budget=4000",
               "--screenshot=" + out, "file:///" + p.replace("\\", "/")]
        subprocess.run(cmd, capture_output=True)
        size = os.path.getsize(out) if os.path.exists(out) else 0
        print(("OK  " if size else "FAIL"), os.path.relpath(out, ROOT), size)


if __name__ == "__main__":
    render(PAGES)
