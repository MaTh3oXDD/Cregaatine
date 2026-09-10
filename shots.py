import asyncio, functools, http.server, socketserver, threading, pathlib, re
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).parent
SITE = ROOT / "site"
OUT = ROOT / "podglad-pdf"
PORT = 8766

def serve():
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(SITE))
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", PORT), h) as srv:
        srv.serve_forever()

def slug(p):
    rel = p.relative_to(SITE).parent.as_posix()
    if p.name != "index.html":
        rel = (rel + "/" + p.stem).strip("/")
    return re.sub(r"[^a-z0-9._-]+", "-", (rel or "home").lower())

SCROLL = """async () => {
    const step = window.innerHeight;
    for (let y = 0; y < document.body.scrollHeight; y += step) {
        window.scrollTo(0, y);
        await new Promise(r => setTimeout(r, 120));
    }
    window.scrollTo(0, 0);
    await new Promise(r => setTimeout(r, 400));
}"""

async def main():
    threading.Thread(target=serve, daemon=True).start()
    pages = sorted(SITE.rglob("*.html"))
    OUT.mkdir(exist_ok=True)
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        ctx = await browser.new_context(viewport={"width": 1440, "height": 900}, locale="pl-PL")
        page = await ctx.new_page()
        for i, f in enumerate(pages, 1):
            url = f"http://127.0.0.1:{PORT}/" + f.relative_to(SITE).as_posix()
            name = f"{i:02d}-{slug(f)}.pdf"
            try:
                await page.goto(url, wait_until="networkidle", timeout=45000)
            except Exception:
                await page.goto(url, wait_until="load", timeout=45000)
            await page.evaluate(SCROLL)
            await page.emulate_media(media="screen")
            h = await page.evaluate("document.documentElement.scrollHeight")
            await page.pdf(path=str(OUT / name), width="1440px", height=f"{h + 20}px",
                           print_background=True, page_ranges="1")
            print(f"{i:02d}/{len(pages)} {name}", flush=True)
        await browser.close()

asyncio.run(main())
