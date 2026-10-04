"""Everything two steve-p.org deck pages link to: each card at full size, the other images, the PDFs and
the page text, into research/sources/steve-p/. py tools/crawl_steve_p.py [RWSa MaBD ...]"""
import hashlib
import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "research" / "sources" / "steve-p"
BASE = "https://steve-p.org/cards/"
AGENT = "Mozilla/5.0 (tarot study crawler)"
PAUSE = 1.5
EXTRA = ["https://steve-p.org/divm/", "https://steve-p.org/divm/divmm.html"]


def get(url, referer):
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": AGENT, "Referer": referer})
            with urllib.request.urlopen(req, timeout=60) as r:
                body = r.read()
            time.sleep(PAUSE)
            return body
        except Exception as e:
            print(f"  retry {attempt + 1} {url}: {e}")
            time.sleep(PAUSE * 4 * (attempt + 1))
    raise RuntimeError(f"gave up on {url}")


def text_of(page):
    page = re.sub(r"(?is)<(script|style)\b.*?</\1>", "", page)
    page = re.sub(r"(?i)<br\s*/?>|</(p|h\d|figcaption|li|div)>", "\n", page)
    page = html.unescape(re.sub(r"<[^>]+>", "", page))
    return re.sub(r"\n\s*\n+", "\n\n", page).strip() + "\n"


def save(path, body, url, manifest):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(body)
    manifest[path.relative_to(OUT).as_posix()] = {
        "url": url, "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest(), "fetched": date.today().isoformat()}
    print(f"  {path.relative_to(OUT).as_posix()} {len(body):,}")


def fetch_once(path, url, referer, manifest):
    if path.exists() and path.relative_to(OUT).as_posix() in manifest:
        return
    save(path, get(url, referer), url, manifest)


def crawl(deck, manifest):
    referer = BASE + deck + ".html"
    print(deck)
    page = get(referer, BASE).decode("utf-8")
    save(OUT / deck / "page.html", page.encode("utf-8"), referer, manifest)
    save(OUT / deck / "page.txt", text_of(page).encode("utf-8"), referer, manifest)
    stems = sorted(set(re.findall(r'src="small/sm_(' + re.escape(deck) + r'-[^".]+)\.\w+"', page)))
    for stem in stems:
        path = OUT / deck / "cards" / f"{stem}.png"
        if path.exists() and path.relative_to(OUT).as_posix() in manifest:
            continue
        key = get(f"{BASE}cscalc.php?fs={stem}&dt={int(time.time() * 1000)}", referer).decode().strip()
        save(path, get(f"{BASE}pixe/{stem}_{key}.png", referer), f"{BASE}pixe/{stem}_{key}.png", manifest)
    for name in sorted(set(re.findall(r'src="small/sm_([^"]+)"[^>]*dispbigsing', page))):
        fetch_once(OUT / deck / "images" / name, BASE + "pix/" + name, referer, manifest)
    for href in sorted(set(re.findall(r'href="([^"]+\.pdf)"', page))):
        url = urllib.parse.urljoin(BASE, href)
        fetch_once(OUT / "pdf" / urllib.parse.unquote(url.rsplit("/", 1)[1]), url, referer, manifest)
    return len(stems)


def main(decks):
    index = OUT / "manifest.json"
    manifest = json.loads(index.read_text(encoding="utf-8")) if index.exists() else {}
    try:
        counts = {deck: crawl(deck, manifest) for deck in decks}
        for url in EXTRA:
            name = url.rstrip("/").rsplit("/", 1)[1]
            name = "divm-index.html" if name == "divm" else name
            fetch_once(OUT / "divm" / name, url, BASE + "RWSa.html", manifest)
    finally:
        OUT.mkdir(parents=True, exist_ok=True)
        index.write_text(json.dumps(manifest, indent=1, sort_keys=True), encoding="utf-8")
    print("cards:", counts, "files:", len(manifest))


if __name__ == "__main__":
    main(sys.argv[1:] or ["RWSa", "MaBD"])
