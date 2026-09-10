# -*- coding: utf-8 -*-
"""Skleja pojedyncze PDF-y podstron w jeden dokument z nawigacją:
klikalny spis treści, zakładki w panelu bocznym i pasek prev/next/spis na każdej stronie."""
import pathlib, re, html, pymupdf as fitz

ROOT = pathlib.Path(__file__).parent
SITE = ROOT / "site"
PDFS = ROOT / "podglad-pdf"
OUTFILE = ROOT / "cregaatine-podglad.pdf"

REG = r"C:\Windows\Fonts\segoeui.ttf"
BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
F_REG, F_BOLD = fitz.Font(fontfile=REG), fitz.Font(fontfile=BOLD)

W = 1080.0            # 1440 px * 0.75 = punkty PDF
MARGIN, ROW = 60.0, 34.0
TITLE_MAX = 620.0     # szerokość kolumny tytułu
BLUE, GREY, DARK = (0.09, 0.35, 0.70), (0.45, 0.45, 0.45), (0.10, 0.10, 0.12)

def title_of(f):
    txt = f.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"<title[^>]*>(.*?)</title>", txt, re.S | re.I)
    if not m:
        return f.parent.name or "Strona główna"
    t = html.unescape(re.sub(r"\s+", " ", m.group(1))).strip()
    return re.split(r"\s+[-|–]\s+(CreGAAtine|Carnomed)", t)[0].strip() or t

def clip(text, size, maxw):
    if F_REG.text_length(text, size) <= maxw:
        return text
    while text and F_REG.text_length(text + "…", size) > maxw:
        text = text[:-1]
    return text + "…"

pdfs = sorted(PDFS.glob("*.pdf"))
htmls = sorted(SITE.rglob("*.html"))
assert len(pdfs) == len(htmls), f"{len(pdfs)} PDF vs {len(htmls)} HTML"
titles = [title_of(h) for h in htmls]
paths = ["/" + (h.relative_to(SITE).parent.as_posix().strip("/")) for h in htmls]

out = fitz.open()

# --- spis treści ---
toc = out.new_page(width=W, height=MARGIN * 2 + 110 + ROW * len(pdfs))
toc.insert_font(fontname="pl", fontfile=REG)
toc.insert_font(fontname="plb", fontfile=BOLD)
toc.insert_text((MARGIN, MARGIN + 20), "CreGAAtine — podgląd podstron",
                fontsize=28, fontname="plb", color=DARK)
toc.insert_text((MARGIN, MARGIN + 52), f"{len(pdfs)} podstron. Kliknij tytuł, żeby przejść.",
                fontsize=12, fontname="pl", color=GREY)
rows, y = [], MARGIN + 110
for i, (t, p) in enumerate(zip(titles, paths), 1):
    label = clip(f"{i:02d}.  {t}", 13, TITLE_MAX)
    toc.insert_text((MARGIN, y), label, fontsize=13, fontname="pl", color=BLUE)
    wtxt = F_REG.text_length(label, 13)
    toc.draw_line(fitz.Point(MARGIN, y + 4), fitz.Point(MARGIN + wtxt, y + 4),
                  color=BLUE, width=0.4)
    toc.insert_text((MARGIN + TITLE_MAX + 30, y), clip(p, 10, W - MARGIN * 2 - TITLE_MAX - 30),
                    fontsize=10, fontname="pl", color=GREY)
    rows.append(fitz.Rect(MARGIN, y - 13, MARGIN + wtxt, y + 6))
    y += ROW

# --- wklejenie podstron ---
starts = []
for f in pdfs:
    starts.append(out.page_count)
    with fitz.open(f) as src:
        out.insert_pdf(src)

# linki ze spisu treści (obiekt strony trzeba pobrać ponownie po insert_pdf)
toc = out[0]
for rect, target in zip(rows, starts):
    toc.insert_link({"kind": fitz.LINK_GOTO, "from": rect, "page": target, "to": fitz.Point(0, 0)})

# --- pasek nawigacji na pierwszej stronie każdej podstrony ---
def nav_button(page, x_right, y_top, text, target):
    w = F_REG.text_length(text, 11) + 22
    r = fitz.Rect(x_right - w, y_top, x_right, y_top + 24)
    page.draw_rect(r, color=(0.80, 0.83, 0.88), fill=(1, 1, 1), width=0.8)
    page.insert_textbox(r + (0, 6, 0, 0), text, fontsize=11, fontname="pl",
                        color=BLUE, align=fitz.TEXT_ALIGN_CENTER)
    page.insert_link({"kind": fitz.LINK_GOTO, "from": r, "page": target, "to": fitz.Point(0, 0)})
    return r.x0

for i, start in enumerate(starts):
    page = out[start]
    page.insert_font(fontname="pl", fontfile=REG)
    x, y = page.rect.width - 24, 16
    if i + 1 < len(starts):
        x = nav_button(page, x, y, "Następna ›", starts[i + 1]) - 8
    if i > 0:
        x = nav_button(page, x, y, "‹ Poprzednia", starts[i - 1]) - 8
    nav_button(page, x, y, "Spis treści", 0)

# --- zakładki w panelu bocznym ---
out.set_toc([[1, f"{i:02d}. {t}", s + 1] for i, (t, s) in enumerate(zip(titles, starts), 1)])
out.set_metadata({"title": "CreGAAtine — podgląd podstron", "author": "CreGAAtine"})
out.save(OUTFILE, garbage=4, deflate=True)
out.close()
print(f"OK -> {OUTFILE}  ({OUTFILE.stat().st_size/1024/1024:.1f} MB, {len(pdfs)} podstron)")
