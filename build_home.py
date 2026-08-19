# -*- coding: utf-8 -*-
import json
import os
import common

ROOT = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(ROOT, "extracted", "home.json"), encoding="utf-8"))
S = {s["index"]: s for s in d["sections"]}

def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

TESTIMONIALS = [
    {"name": "Joanna Stós", "role": "@sztosfit", "img": "/wp-content/uploads/2022/01/sztoffit.jpeg",
     "quote": "Od kiedy stosuje Cregaatine, zauważyłam zwiększoną wytrzymałość na treningu a także przyspieszoną regenerację😍 Serdecznie polecam, wypróbuj i przekonaj się sam💪"},
    {"name": "Jarosław Rogowski", "role": "Ekspert Bezpieczeństwa Osobistego, Szkoleniowiec", "img": "/wp-content/uploads/2022/01/jarek.jpeg",
     "quote": "Dla mnie stosowanie Cregaatine to lepsza regeneracja, zwiększenie siły oraz przyrost masy. Stosuję ją przed i bezpośrednio po treningu a w dni nietreningowe raz dziennie rano🙂"},
    {"name": "Katarzyna Czaplejewicz", "role": "@no_age_fit", "img": "/wp-content/uploads/2022/01/noagefit.jpg",
     "quote": "Przez lata kariery sportowej i bycia instruktorką fitness próbowałam różne preparaty, natomiast dopiero w przypadku przyjmowania regularnie CreGAAtine mogę szczerze powiedzieć, że rezultaty są dla mnie pozytywnie odczuwalne. Znacznie zwiększyła się moja siła mięśniowa i szybciej się regeneruje. Dodatkowym atutem jest brak zatrzymania wody podskórnej co było dla mnie problematyczne. Szczerze polecam."},
    {"name": "Piotr Tomczyk", "role": "StrongMan", "img": "/wp-content/uploads/2022/01/piotr.jpeg",
     "quote": "Nowy poziom treningu tylko z cregaatine."},
    {"name": "Misa Balculov", "role": "Trener muay thai i kickboxingu", "img": "/wp-content/uploads/2021/07/175791811_462266004834424_7754191150956982309_n-240x300-1.jpg",
     "quote": "Dosłownie jedyna kreatyna, którą używam, a która nie szkodzi mojemu żołądkowi. Wszystkim polecam."},
    {"name": "Milan Veselinović", "role": "Trener kondycyjny", "img": "/wp-content/uploads/2021/07/60800801_716377878802726_2197132368913551553_n-300x300-1.jpg",
     "quote": ""},
    {"name": "Slobodan Maksimovic", "role": "Zawodnik MMA", "img": "/wp-content/uploads/2021/07/124667681_2873208306281979_9124896752305789321_n-300x200-1.jpg",
     "quote": ""},
    {"name": "Lara Santini", "role": "Dwukrotna światowa i dwukrotna europejska zwyciężczyni bodybuilding (Wellness category)", "img": "/wp-content/uploads/2021/07/Lara-Santini-240x300-1.jpg",
     "quote": "Prawdziwą przyjemnością było uczestnictwo w wykładzie prof. Sergeja, teraz z przekonaniem mogę stwierdzić, że jest to prawdziwa rewolucja w zażywaniu kreatyny. Po kilku tygodniach przyjmowania sama zauważyłam różnicę w treningach, także na koniec dnia mam więcej energii! Jestem pozytywnie zaskoczona!"},
]

# ---------- S0: hero ----------
s0 = S[0]
hero = f"""
<section class="hero">
  <div class="container hero-grid">
    <div>
      <span class="eyebrow">#CreGAAtine · Suplement roku 2021</span>
      <h1>{esc(s0['headings'][0])}</h1>
      <p class="lede">{esc(d['meta_description'])}</p>
      <div class="hero-ctas">
        <a class="btn btn-primary" href="{s0['buttons'][0]['href']}">{esc(s0['buttons'][0]['text'])}</a>
        <a class="btn btn-ghost" href="{s0['buttons'][1]['href']}">{esc(s0['buttons'][1]['text'])}</a>
      </div>
    </div>
    <div class="hero-mark reveal">
      <div>
        <div class="mark-num">8,5×</div>
        <div class="mark-label">więcej efektywności</div>
      </div>
    </div>
  </div>
</section>
"""

# ---------- S1: stat strip ----------
s1 = S[1]
items = ""
for h, img in zip(s1["headings"], s1["images"]):
    items += f"""      <div class="stat-item">
        <img src="{img['src']}" alt="" loading="lazy">
        <h3>{esc(h)}</h3>
      </div>
"""
stat_strip = f"""
<section class="section section-dim">
  <div class="container">
    <div class="stat-strip reveal">
{items}    </div>
  </div>
</section>
"""

# ---------- S2: about / why better ----------
s2 = S[2]
about_p = s2["paragraphs"]
feature_html = ""
for h, p in zip(s2["headings"][1:], about_p[2:]):
    feature_html += f"""        <div class="feature"><h4>{esc(h)}</h4><p>{esc(p)}</p></div>
"""
about = f"""
<section class="section" id="cregaatine">
  <div class="container">
    <div class="split reveal">
      <div class="split-media">
        <img src="{s2['images'][0]['src']}" alt="CreGAAtine" loading="lazy">
      </div>
      <div>
        <span class="badge-pill">{esc(s2['paragraphs'][0])}</span>
        <h2>{esc(s2['headings'][0])}</h2>
        <p style="color:var(--muted);margin-top:1rem;max-width:60ch;">{esc(s2['paragraphs'][1])}</p>
        <div class="feature-list">
{feature_html}        </div>
        <div class="hero-ctas" style="margin-top:2rem;">
          <a class="btn btn-dark" href="{s2['buttons'][0]['href']}">{esc(s2['buttons'][0]['text'])}</a>
          <a class="btn btn-ghost" href="{s2['buttons'][1]['href']}">{esc(s2['buttons'][1]['text'])}</a>
        </div>
      </div>
    </div>
  </div>
</section>
"""

# ---------- S3: video teaser ----------
s3 = S[3]
video_src = "https://www.youtube.com/embed/bF8d3nrxzCk"
video = f"""
<section class="section section-dark">
  <div class="container">
    <div class="video-block reveal">
      <div>
        <span class="eyebrow">Zobacz jak działa</span>
        <h2 style="margin-top:0.6rem;">{esc(s3['headings'][0])}</h2>
        <p style="color:var(--muted-dark);margin-top:1rem;max-width:48ch;">{esc(s3['paragraphs'][0])}</p>
      </div>
      <div class="video-frame">
        <iframe src="{video_src}" title="CreGAAtine wideo" loading="lazy" allowfullscreen></iframe>
      </div>
    </div>
  </div>
</section>
"""

# ---------- S4: benefits grid ----------
s4 = S[4]
cards = ""
for h, p, img in zip(s4["headings"][1:], s4["paragraphs"], s4["images"]):
    cards += f"""      <div class="benefit-card">
        <img src="{img['src']}" alt="" loading="lazy">
        <h4>{esc(h)}</h4>
        <p>{esc(p)}</p>
      </div>
"""
benefits = f"""
<section class="section section-dark section-line-top">
  <div class="container">
    <div class="eyebrow-row"><span class="eyebrow">Dlaczego to działa</span></div>
    <h2 style="max-width:22ch;margin-bottom:2.5rem;">{esc(s4['headings'][0])}</h2>
    <div class="benefit-grid reveal">
{cards}    </div>
    <div class="hero-ctas" style="margin-top:2.5rem;">
      <a class="btn btn-primary" href="{s4['buttons'][0]['href']}">{esc(s4['buttons'][0]['text'])}</a>
      <a class="btn btn-ghost" href="{s4['buttons'][1]['href']}">{esc(s4['buttons'][1]['text'])}</a>
    </div>
  </div>
</section>
"""

# ---------- S5: order / product panel ----------
s5 = S[5]
p = s5["paragraphs"]
spec_rows = f"""
      <div class="spec-row"><dt>Skład (2 saszetki)</dt><dd>{esc(p[2])}</dd></div>
      <div class="spec-row"><dt>Dzienna porcja</dt><dd>{esc(p[3])}</dd></div>
      <div class="spec-row"><dt>Dieta</dt><dd>{esc(p[4])}</dd></div>
      <div class="spec-row"><dt>Kod EAN</dt><dd>{esc(p[5])}</dd></div>
"""
order = f"""
<section class="section" id="sklad">
  <div class="container">
    <div class="product-panel reveal">
      <div class="split-media">
        <img src="{s5['images'][0]['src']}" alt="CreGAAtine" loading="lazy">
      </div>
      <div>
        <span class="eyebrow">{esc(s5['headings'][1])}</span>
        <h2 style="margin-top:0.6rem;">{esc(s5['headings'][0])}</h2>
        <p style="color:var(--muted);margin-top:0.75rem;">{esc(p[0])}</p>
        <div class="price-row">
          <span class="price">{esc(s5['headings'][2])}</span>
          <span class="unit">{esc(s5['headings'][3])} · {esc(p[9])}</span>
        </div>
        <a class="btn btn-dark" href="{s5['buttons'][0]['href']}">{esc(s5['buttons'][0]['text'])}</a>
        <div class="spec-list">{spec_rows}      </div>
        <p class="spec-note">{esc(p[6])}<br>{esc(p[7])}<br>{esc(p[8])}</p>
      </div>
    </div>
  </div>
</section>
"""

# ---------- S6: facts ----------
s6 = S[6]
facts = ""
for h, p6 in zip(s6["headings"][1:], s6["paragraphs"]):
    facts += f"""      <div class="fact-card"><h4>{esc(h)}</h4><p>{esc(p6)}</p></div>
"""
fact_section = f"""
<section class="section section-dim">
  <div class="container">
    <h2 style="margin-bottom:2rem;">{esc(s6['headings'][0])}</h2>
    <div class="fact-grid reveal">
{facts}    </div>
  </div>
</section>
"""

# ---------- S7: gallery ----------
s7 = S[7]
gallery_imgs = "".join(f'      <img src="{im["src"]}" alt="" loading="lazy">\n' for im in s7["images"])
gallery = f"""
<section class="section">
  <div class="container">
    <div class="gallery-strip reveal">
{gallery_imgs}    </div>
  </div>
</section>
"""

# ---------- S8: testimonials ----------
s8 = S[8]
testi_cards = ""
for t in TESTIMONIALS:
    quote_html = f"<p>{esc(t['quote'])}</p>" if t["quote"] else "<p></p>"
    testi_cards += f"""      <div class="testi-card">
        {quote_html}
        <div class="testi-person">
          <img src="{t['img']}" alt="{esc(t['name'])}" loading="lazy">
          <div><strong>{esc(t['name'])}</strong><span>{esc(t['role'])}</span></div>
        </div>
      </div>
"""
testimonials = f"""
<section class="section section-dark section-line-top">
  <div class="container">
    <h2 style="margin-bottom:2.5rem;">{esc(s8['headings'][0])}</h2>
    <div class="testi-grid reveal">
{testi_cards}    </div>
  </div>
</section>
"""

# ---------- S9: cooperation ----------
s9 = S[9]
coop = f"""
<section class="section" id="wspolpraca">
  <div class="container">
    <div class="split reveal">
      <div>
        <span class="eyebrow">Współpraca</span>
        <h2 style="margin-top:0.6rem;">{esc(s9['headings'][0])}</h2>
        <p style="color:var(--muted);margin-top:1rem;max-width:60ch;">{esc(s9['paragraphs'][0])}</p>
      </div>
      <div>
        <a class="btn btn-dark" href="https://www.instagram.com/cregaatine.pl/">{esc(s9['list_items'][0])} @cregaatine.pl</a>
      </div>
    </div>
  </div>
</section>
"""

# ---------- S10: partners ----------
s10 = S[10]
partners = "".join(f'      <img src="{im["src"]}" alt="" loading="lazy">\n' for im in s10["images"])
partners_section = f"""
<section class="section section-dim">
  <div class="container">
    <span class="eyebrow">{esc(s10['headings'][0])}</span>
    <div class="partner-grid reveal" style="margin-top:2rem;">
{partners}    </div>
  </div>
</section>
"""

# ---------- S11: blog teaser ----------
blog_cards = ""
for c in d["cards"]:
    blog_cards += f"""      <a class="blog-card" href="{c['href']}">
        <div class="thumb"><img src="{c['image']}" alt="{esc(c['title'] or '')}" loading="lazy"></div>
        <div class="body">
          <h3>{esc(c['title'] or '')}</h3>
          <span class="read-more">czytaj więcej</span>
        </div>
      </a>
"""
blog_teaser = f"""
<section class="section" id="blog">
  <div class="container">
    <span class="eyebrow">{esc(S[11]['headings'][0])}</span>
    <div class="blog-grid reveal" style="margin-top:1.5rem;">
{blog_cards}    </div>
  </div>
</section>
"""

# ---------- S12: cross-sell ----------
s12 = S[12]
products = [
    {"name": s12["headings"][1], "tag": s12["paragraphs"][0], "feat1": s12["headings"][2], "desc1": s12["paragraphs"][1],
     "feat2": s12["headings"][3], "desc2": s12["paragraphs"][2], "img": s12["images"][0]["src"], "href": s12["buttons"][0]["href"], "cta": s12["buttons"][0]["text"]},
    {"name": s12["headings"][4], "tag": s12["paragraphs"][3], "feat1": s12["headings"][5], "desc1": s12["paragraphs"][4],
     "feat2": s12["headings"][6], "desc2": s12["paragraphs"][5], "img": s12["images"][1]["src"], "href": s12["buttons"][1]["href"], "cta": s12["buttons"][1]["text"]},
    {"name": s12["headings"][7], "tag": s12["paragraphs"][6], "feat1": s12["headings"][8], "desc1": s12["paragraphs"][7],
     "feat2": s12["headings"][9], "desc2": s12["paragraphs"][8], "img": s12["images"][2]["src"], "href": s12["buttons"][2]["href"], "cta": s12["buttons"][2]["text"]},
]
cross_cards = ""
for pr in products:
    cross_cards += f"""      <div class="crosssell-card">
        <div class="thumb"><img src="{pr['img']}" alt="{esc(pr['name'])}" loading="lazy"></div>
        <div>
          <h4>{esc(pr['name'])}</h4>
          <span class="tag">{esc(pr['tag'])}</span>
        </div>
        <p class="feat"><strong>{esc(pr['feat1'])}:</strong> {esc(pr['desc1'])}</p>
        <p class="feat"><strong>{esc(pr['feat2'])}:</strong> {esc(pr['desc2'])}</p>
        <a class="btn btn-ghost" href="{pr['href']}">{esc(pr['cta'])}</a>
      </div>
"""
crosssell = f"""
<section class="section section-dim">
  <div class="container">
    <h2 style="margin-bottom:2rem;">{esc(s12['headings'][0])}</h2>
    <div class="crosssell-grid reveal">
{cross_cards}    </div>
  </div>
</section>
"""

# ---------- S13: cta banner ----------
s13 = S[13]
cta = f"""
<section class="section section-dark">
  <div class="container cta-banner reveal">
    <h2>{esc(s13['headings'][0])}</h2>
    <a class="btn btn-primary" href="{s13['buttons'][0]['href']}">{esc(s13['buttons'][0]['text'])}</a>
  </div>
</section>
"""

# ---------- S14: contact ----------
s14 = S[14]
p14 = s14["paragraphs"]
contact = f"""
<section class="section" id="kontakt">
  <div class="container">
    <div class="contact-grid">
      <div>
        <span class="eyebrow">Kontakt</span>
        <h2 style="margin-top:0.6rem;">{esc(s14['headings'][0])}</h2>
        <p style="color:var(--muted);margin-top:1rem;max-width:44ch;">{esc(p14[0])}</p>
      </div>
      <form class="contact-form" action="mailto:biuro@carno-med.pl" method="post">
        <div class="row2">
          <div class="field"><label for="f-name">{esc(p14[1])}</label><input id="f-name" name="name" type="text" required></div>
          <div class="field"><label for="f-phone">{esc(p14[2])}</label><input id="f-phone" name="phone" type="tel"></div>
        </div>
        <div class="field"><label for="f-email">{esc(p14[3])}</label><input id="f-email" name="email" type="email" required></div>
        <div class="field"><label for="f-message">{esc(p14[4])}</label><textarea id="f-message" name="message" required></textarea></div>
        <button class="btn btn-dark" type="submit" style="justify-self:start;">Wyślij</button>
      </form>
    </div>
  </div>
</section>
"""

body = "\n".join([hero, stat_strip, about, video, benefits, order, fact_section, gallery,
                   testimonials, coop, partners_section, blog_teaser, crosssell, cta, contact])

html = common.page(
    title=d["title"],
    description=d["meta_description"],
    body=body,
    canonical_path="/",
)

out_path = os.path.join(ROOT, "site", "index.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html)

print("wrote", out_path, len(html), "bytes")
