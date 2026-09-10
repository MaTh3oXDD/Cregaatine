# -*- coding: utf-8 -*-
"""Zostawia wyłącznie warianty WOFF2 w inline'owych deklaracjach @font-face.

Divi wkleja ten sam krój trzy razy (TTF, WOFF, WOFF2), po jednej kopii na
user-agenta. Każda przeglądarka od 2016 roku obsługuje WOFF2, więc TTF i WOFF
to martwy balast w krytycznej ścieżce renderowania. Wagi zostają wszystkie --
nie zgadujemy, których używa motyw.
"""
import os, re, glob

SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")
FACE = re.compile(r"@font-face\s*\{[^}]*\}")
saved = 0
for path in sorted(glob.glob(os.path.join(SITE, "**", "index.html"), recursive=True)):
    html = open(path, encoding="utf-8").read()
    before = len(html)

    def trim(m):
        css = m.group(2)
        faces = FACE.findall(css)
        if len(faces) < 6:
            return m.group(0)
        keep, seen = [], set()
        for f in faces:
            if "format('woff2')" not in f and 'format("woff2")' not in f:
                continue
            fam = re.search(r"font-family:\s*'([^']+)'", f)
            wt = re.search(r"font-weight:\s*(\d+)", f)
            st = re.search(r"font-style:\s*(\w+)", f)
            key = (fam.group(1) if fam else "?",
                   wt.group(1) if wt else "400",
                   st.group(1) if st else "normal")
            if key in seen:
                continue
            seen.add(key)
            keep.append(f)
        if not keep:
            return m.group(0)
        return f"<style{m.group(1)}>" + "".join(keep) + FACE.sub("", css) + "</style>"

    html = re.sub(r"<style([^>]*)>(.*?)</style>", trim, html, flags=re.S)
    if len(html) != before:
        open(path, "w", encoding="utf-8").write(html)
        saved += before - len(html)
        print(f"{os.path.relpath(path, SITE):70} -{(before-len(html))//1024} KB")
print(f"\nrazem zaoszczędzone: {saved//1024} KB")
