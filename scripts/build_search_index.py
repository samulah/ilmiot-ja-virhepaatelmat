#!/usr/bin/env python3
"""
Rakentaa etusivun (index.html) kokotekstihaun indeksin: search-index.js.

- Lukee korttilistan index.html:stä (a.hub-kortti) → autoritatiivinen sivulista.
- Indeksoi lisäksi 12 kategoriasivua (a.hub-kat-linkki index.html:stä). Niiden
  teksti tulee .kat-runko-säiliöstä, josta pudotetaan pois .hub-kortti-kortit:
  ne toistavat ilmiösivujen omaa tekstiä, joten mukaan jää vain kategorian
  johdantoessee. Etusivun haku käyttää tätä pitääkseen kategoriaosion näkyvissä,
  kun haku osuu esseeseen muttei yhteenkään yksittäiseen ilmiöön.
- Poimii jokaisen ilmiösivun .ilmio-säiliöstä haettavan tekstin:
  leipätekstin, listat, tietolaatikot JA mermaid-kaavioiden labelit.
- Jättää pois .ilmio-byline + .ilmio-tag (kohina) ja — koska ne ovat .ilmio:n
  sisaruksia — automaattisesti .liittyvat + .kortti-nav.
- Kirjoittaa search-index.js:n joka asettaa globaalin window.ILMIO_HAKU-taulukon
  (ladataan tavallisella <script src> -tagilla, toimii myös file://-protokollalla).

Deterministinen ja idempotentti: sama sisältö → byte-identtinen tulos.

Aja aina kun ilmiösivujen sisältö muuttuu, ennen committia:
    python3 scripts/build_search_index.py
"""
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).parent.parent

# Mermaidin quotetut labelit, esim.  O["Omistus"]  tai  U["a\nb"]
LABEL_RE = re.compile(r'"([^"]*)"')


def extract_text(html_path: Path) -> str:
    """Palauttaa yhden ilmiösivun haettavan tekstin (alkuperäinen kirjainkoko)."""
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")
    il = soup.find(class_="ilmio")
    if il is None:
        return ""

    # Kohina pois ennen tekstin poimintaa.
    for sel in ("ilmio-byline", "ilmio-tag"):
        for el in il.find_all(class_=sel):
            el.decompose()

    # Mermaid: korvaa raaka kaaviolähde pelkillä label-sanoilla.
    for m in il.find_all(class_="mermaid"):
        labels = LABEL_RE.findall(m.get_text())  # BS4 dekoodaa &gt; jo
        labels = [l.replace("\\n", " ") for l in labels]
        m.replace_with(" ".join(labels))

    text = il.get_text(separator=" ")
    return " ".join(text.split())


def extract_kategoria_text(html_path: Path) -> str:
    """Kategoriasivun johdantoessee ilman ilmiökortteja."""
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")
    runko = soup.find(class_="kat-runko")
    if runko is None:
        return ""
    for sel in ("hub-kortti", "kat-siirry", "kat-vesileima"):
        for el in runko.find_all(class_=sel):
            el.decompose()
    return " ".join(runko.get_text(separator=" ").split())


def main() -> None:
    index_html = ROOT / "index.html"
    soup = BeautifulSoup(index_html.read_text(encoding="utf-8"), "html.parser")

    entries = []
    for a in soup.select("a.hub-kortti"):
        href = a.get("href")
        if not href:
            continue
        page = ROOT / href
        if not page.exists():
            print(f"  VAROITUS: {href} puuttuu — ohitetaan")
            continue
        text = extract_text(page)
        if not text:
            print(f"  VAROITUS: {href} — .ilmio-säiliötä ei löytynyt tai tyhjä")
            continue
        entries.append({"u": href, "x": text})

    ilmioita = len(entries)
    for a in soup.select("a.hub-kat-linkki"):
        href = a.get("href")
        if not href:
            continue
        page = ROOT / href
        if not page.exists():
            print(f"  VAROITUS: {href} puuttuu — ohitetaan")
            continue
        text = extract_kategoria_text(page)
        if not text:
            print(f"  VAROITUS: {href} — .kat-runko-säiliötä ei löytynyt tai tyhjä")
            continue
        entries.append({"u": href, "x": text})
    kategorioita = len(entries) - ilmioita

    payload = (
        "window.ILMIO_HAKU="
        + json.dumps(entries, ensure_ascii=False, separators=(",", ":"))
        + ";\n"
    )
    out = ROOT / "search-index.js"
    out.write_text(payload, encoding="utf-8")
    print(
        f"search-index.js: {len(entries)} sivua "
        f"({ilmioita} ilmiötä + {kategorioita} kategoriaa), "
        f"{len(payload.encode('utf-8')) // 1024} KB"
    )


if __name__ == "__main__":
    main()
