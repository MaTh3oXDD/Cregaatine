"""Copy site/ to demo/ and prefix root-relative URLs for GitHub Pages (main branch, root).

Run before every push: python build_pages.py
Published at https://math3oxdd.github.io/Cregaatine/ (root index.html redirects to demo/).
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "site"
OUT = ROOT / "demo"
BASE = (sys.argv[1] if len(sys.argv) > 1 else "/Cregaatine/demo").rstrip("/")

ATTR_RE = re.compile(r"""(\b(?:href|src|action|poster|content|data-[\w-]+)\s*=\s*["'])/(?!/)""", re.I)
SRCSET_RE = re.compile(r"""(\bsrcset\s*=\s*)(["'])(.*?)\2""", re.I | re.S)
CSS_URL_RE = re.compile(r"""(url\(\s*["']?)/(?!/)""", re.I)


def fix_srcset(m):
    parts = [p.strip() for p in m.group(3).split(",")]
    parts = [BASE + p if p.startswith("/") and not p.startswith("//") else p for p in parts]
    return f"{m.group(1)}{m.group(2)}{', '.join(parts)}{m.group(2)}"


def rewrite(text, is_html):
    if is_html:
        text = ATTR_RE.sub(lambda m: m.group(1) + BASE + "/", text)
        text = SRCSET_RE.sub(fix_srcset, text)
    return CSS_URL_RE.sub(lambda m: m.group(1) + BASE + "/", text)


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(SRC, OUT, ignore=shutil.ignore_patterns(".htaccess", "_redirects"))
    count = 0
    for path in OUT.rglob("*"):
        if path.suffix.lower() not in (".html", ".css"):
            continue
        text = path.read_text(encoding="utf-8", errors="surrogateescape")
        new = rewrite(text, path.suffix.lower() == ".html")
        if new != text:
            path.write_text(new, encoding="utf-8", errors="surrogateescape")
            count += 1
    (ROOT / ".nojekyll").touch()
    (ROOT / "index.html").write_text(
        f'<!doctype html><meta charset="utf-8"><title>CreGAAtine</title>'
        f'<meta http-equiv="refresh" content="0; url={BASE}/">'
        f'<a href="{BASE}/">CreGAAtine</a>\n',
        encoding="utf-8",
    )
    print(f"Rewrote {count} files with base {BASE}")


if __name__ == "__main__":
    main()
