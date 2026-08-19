# -*- coding: utf-8 -*-
NAV_LINKS = [
    ("/", "Home"),
    ("/#cregaatine", "O CreGAAtine"),
    ("/suplement-roku-fiwe/", "Nagrody"),
    ("/#sklad", "Skład"),
    ("/blog/", "Blog"),
    ("/#wspolpraca", "Współpraca"),
    ("/#kontakt", "Kontakt"),
]

def render_nav(active=None):
    items = []
    for href, label in NAV_LINKS:
        items.append(f'<a href="{href}">{label}</a>')
    items.append('<a href="https://sklep.cregaatine.pl/" class="shop">SKLEP</a>')
    return "\n        ".join(items)

HEADER = """  <header class="site-header">
    <div class="container">
      <a href="/" class="brand">CreGAA<span class="x">×</span>tine</a>
      <nav class="main-nav" id="main-nav">
        {nav}
      </nav>
      <button class="nav-toggle" aria-expanded="false" aria-controls="main-nav" aria-label="Menu"><span></span></button>
    </div>
  </header>
""".format(nav=render_nav())

FOOTER = """  <footer class="site-footer">
    <div class="container">
      <div class="foot-top">
        <div>
          <a href="/" class="brand">CreGAA×tine</a>
          <p style="max-width:32ch;margin-top:0.9rem;font-size:0.9rem;">Naukowa rewolucja kreatyny — połączenie monohydratu kreatyny i GAA, 8,5x więcej efektywności.</p>
        </div>
        <div class="foot-links">
          <a href="/#cregaatine">O CreGAAtine</a>
          <a href="/suplement-roku-fiwe/">Nagrody</a>
          <a href="/blog/">Blog</a>
          <a href="/#wspolpraca">Współpraca</a>
          <a href="/#kontakt">Kontakt</a>
          <a href="https://sklep.cregaatine.pl/">Sklep</a>
        </div>
      </div>
      <div class="foot-bottom">
        <span>&copy; Carnomed sp. z o.o. — CreGAAtine</span>
        <span>ul. Dolnych Młynów 3/1, 31-124 Kraków · biuro@carno-med.pl</span>
      </div>
    </div>
  </footer>
"""

def page(title, description, body, canonical_path="/", extra_head=""):
    return f"""<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="https://cregaatine.pl{canonical_path}">
<link rel="icon" href="/wp-content/uploads/2021/03/cropped-FV-32x32.jpg" sizes="32x32">
<link rel="stylesheet" href="/assets/css/modern.css">
{extra_head}</head>
<body class="modern">
{HEADER}
<main>
{body}
</main>
{FOOTER}
<script src="/assets/js/main.js"></script>
</body>
</html>
"""
