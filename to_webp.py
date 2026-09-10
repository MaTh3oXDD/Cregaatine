# -*- coding: utf-8 -*-
"""Konwersja obrazów z wp-content/uploads do WebP + przepisanie odwołań.

Konwertujemy tylko pliki, do których strony faktycznie się odwołują, i tylko
wtedy, gdy WebP wychodzi mniejszy. Oryginały zostają na dysku jako kopia
zapasowa -- nic ich już nie ładuje.

Pomijamy og-cregaatine.jpg (Facebook i LinkedIn nie renderują WebP w podglądach)
oraz favikony.
"""
import os, re, glob
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")
SKIP = ("og-cregaatine", "cropped-FV-")
EXT = (".png", ".jpg", ".jpeg")

# 1. zbierz odwołania
refs = set()
htmls = sorted(glob.glob(os.path.join(SITE, "**", "index.html"), recursive=True))
pat = re.compile(r'(?:src|href|srcset|content)="([^"]*wp-content/uploads/[^"]*)"')
for p in htmls:
    for val in pat.findall(open(p, encoding="utf-8").read()):
        for part in val.split(","):
            u = part.strip().split(" ")[0]
            if u.lower().endswith(EXT):
                refs.add(u.split("?")[0])

print(f"odwołań do obrazów: {len(refs)}")

# 2. konwersja
converted, before_b, after_b, skipped = {}, 0, 0, 0
for u in sorted(refs):
    if any(s in u for s in SKIP):
        continue
    local = os.path.join(SITE, u.lstrip("/").replace("/", os.sep))
    if not os.path.exists(local):
        continue
    webp = os.path.splitext(local)[0] + ".webp"
    if not os.path.exists(webp):
        try:
            im = Image.open(local)
            if im.mode in ("P", "LA"):
                im = im.convert("RGBA")
            elif im.mode == "CMYK":
                im = im.convert("RGB")
            im.save(webp, "WEBP", quality=82, method=6)
        except Exception as e:
            print(f"  [pomijam] {u}: {e}")
            continue
    o, n = os.path.getsize(local), os.path.getsize(webp)
    if n >= o:
        os.remove(webp)
        skipped += 1
        continue
    converted[u] = os.path.splitext(u)[0] + ".webp"
    before_b += o
    after_b += n

print(f"skonwertowano {len(converted)} plików, {skipped} pominięto (WebP nie był mniejszy)")
print(f"{before_b/1048576:.1f} MB -> {after_b/1048576:.1f} MB "
      f"({100*(before_b-after_b)/before_b:.0f}% mniej)")

# 3. przepisz odwołania
rx = re.compile("|".join(re.escape(k) for k in sorted(converted, key=len, reverse=True)))
for p in htmls:
    html = open(p, encoding="utf-8").read()
    new = rx.sub(lambda m: converted[m.group(0)], html)
    if new != html:
        open(p, "w", encoding="utf-8").write(new)
        print(f"  przepisano: {os.path.relpath(p, SITE)}")
