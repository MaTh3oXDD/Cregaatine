# -*- coding: utf-8 -*-
"""Ogranicza @font-face ikon Divi (FontAwesome, ETmodules) do WOFF2.

Deklaracje wyliczają eot/ttf/svg/woff/woff2 w jednej liście src. Przeglądarka
pobiera tylko pierwszy obsługiwany format, więc reszta nie kosztuje transferu --
ale zajmuje 3,5 MB w katalogu wdrożeniowym i nigdy nie zostanie użyta.
"""
import os, re, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")
DEAD_EXT = (".eot", ".ttf", ".svg", ".woff")

def keep_woff2(m):
    src = m.group(0)
    woff2 = re.search(r"url\((['\"]?)([^)'\"]+\.woff2)\1\)\s*format\((['\"])woff2\3\)", src)
    if not woff2:
        return src
    return f"src:url({woff2.group(2)}) format('woff2')"

changed = 0
for path in sorted(glob.glob(os.path.join(SITE, "**", "*.html"), recursive=True)) + \
            sorted(glob.glob(os.path.join(SITE, "**", "*.css"), recursive=True)):
    txt = open(path, encoding="utf-8", errors="replace").read()
    new = re.sub(r"src:\s*url\([^;{}]*?\)\s*format\([^;{}]*?\)(?:\s*,\s*url\([^;{}]*?\)\s*format\([^;{}]*?\))+",
                 keep_woff2, txt)
    # osobno: src z wiodącym eot bez format()
    new = re.sub(r"src:url\([^)]*\.eot\);", "", new)
    if new != txt:
        open(path, "w", encoding="utf-8").write(new)
        changed += 1

print(f"zmienionych plików: {changed}")

removed, freed = 0, 0
for base in ("wp-content/themes/Divi/core/admin/fonts",):
    for dirpath, _, files in os.walk(os.path.join(SITE, base)):
        for f in files:
            if f.lower().endswith(DEAD_EXT):
                p = os.path.join(dirpath, f)
                rel = "/" + os.path.relpath(p, SITE).replace(os.sep, "/")
                still = any(rel in open(h, encoding="utf-8", errors="replace").read()
                            for h in glob.glob(os.path.join(SITE, "**", "*.html"), recursive=True))
                if still:
                    continue
                freed += os.path.getsize(p)
                os.remove(p)
                removed += 1
print(f"usunięto {removed} nieużywanych plików czcionek, {freed/1048576:.1f} MB")
