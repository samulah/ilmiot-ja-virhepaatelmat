#!/usr/bin/env python3
"""
Ohjaa ilmiösivujen murupolku kategoriasivulle etusivun fragmentin sijaan.

Ennen: murupolun keskimmäinen taso oli umpikuja. Näkyvässä murupolussa
kategoria oli pelkkä <span> (ei linkkiä lainkaan), ja JSON-LD:n
BreadcrumbList osoitti osoitteeseen https://www.ilmiöt.fi/#<kategoria>
eli etusivun ankkuriin. Kategoriasivujen julkaisun jälkeen molemmille on
oikea kohde.

Muutos per sivu (108 kpl):
  1. <span class="kortti-breadcrumb-kat">Nimi</span>
     -> <a href="kategoria-<slug>.html" class="kortti-breadcrumb-kat">Nimi</a>
  2. JSON-LD BreadcrumbList: "https://www.ilmiöt.fi/#<frag>"
     -> "https://www.ilmiöt.fi/kategoria-<slug>.html"
  3. CSS-tarkkuus: .kortti-breadcrumb-kat -> .kortti-breadcrumb .kortti-breadcrumb-kat
     jotta harmaa väri voittaa yhä .kortti-breadcrumb a -säännön nyt kun
     elementti on linkki. Ulkoasu ei siis muutu, vain klikattavuus.

Kategoriakartta luetaan index.html:stä (.hub-kategoria[id] + .hub-kat-linkki),
joten se pysyy synkassa eikä sisällä kovakoodattuja slugeja. Huom:
tilastoilla-valehtelun fragmentti on `tilastoilla-valehtelu-kategoria`
(nimitörmäyksen takia), joten fragmentti ja slug eivät aina vastaa toisiaan.

Deterministinen ja idempotentti: aja uudelleen turvallisesti.
    python3 scripts/murupolku_kategoriaan.py [--kuivaharjoitus]
"""
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).parent.parent
KANTA = "https://www.ilmiöt.fi/"


def kategoriakartta():
    """fragmentti -> kategoriasivun tiedostonimi."""
    soup = BeautifulSoup((ROOT / "index.html").read_text(encoding="utf-8"), "html.parser")
    kartta = {}
    for kat in soup.select(".hub-kategoria[id]"):
        linkki = kat.select_one(".hub-kat-linkki")
        if linkki and linkki.get("href"):
            kartta[kat["id"]] = linkki["href"]
    return kartta


def kasittele(polku, kartta, kuiva):
    teksti = polku.read_text(encoding="utf-8")
    alkup = teksti

    osuma = re.search(rf'"item": "{re.escape(KANTA)}#([a-z0-9-]+)"', teksti)
    if osuma:
        frag = osuma.group(1)
        sivu = kartta.get(frag)
        if sivu is None:
            return f"{polku.name}: VAROITUS — tuntematon kategoria #{frag}", False
        teksti = teksti.replace(f'"item": "{KANTA}#{frag}"', f'"item": "{KANTA}{sivu}"', 1)
    else:
        # Jo ajettu: poimi kohde olemassa olevasta linkistä idempotenssia varten.
        jo = re.search(r'<a href="(kategoria-[a-z0-9-]+\.html)" class="kortti-breadcrumb-kat">', teksti)
        if not jo:
            return f"{polku.name}: ohitettu — ei murupolun kategoriatasoa", True
        sivu = jo.group(1)

    teksti = re.sub(
        r'<span class="kortti-breadcrumb-kat">(.*?)</span>',
        lambda m: f'<a href="{sivu}" class="kortti-breadcrumb-kat">{m.group(1)}</a>',
        teksti,
        count=1,
    )
    # Idempotenssi: pelkkä .replace() ei riitä, koska tulos sisältää lähtökuvion
    # osajonona — jokainen uusi ajo kasvatti jälkeläisketjua yhdellä tasolla,
    # ja kolmen ajon jälkeen selektori oli nelinkertainen eikä täsmännyt enää
    # mihinkään. Normalisoidaan ketju aina yhteen tasoon.
    teksti = re.sub(
        r"(?:\.kortti-breadcrumb )+\.kortti-breadcrumb-kat \{ color: #666; \}",
        ".kortti-breadcrumb .kortti-breadcrumb-kat { color: #666; }",
        teksti,
        count=1,
    )
    if ".kortti-breadcrumb .kortti-breadcrumb-kat" not in teksti:
        teksti = teksti.replace(
            ".kortti-breadcrumb-kat { color: #666; }",
            ".kortti-breadcrumb .kortti-breadcrumb-kat { color: #666; }",
            1,
        )

    muuttui = teksti != alkup
    if muuttui and not kuiva:
        polku.write_text(teksti, encoding="utf-8")
    return f"{polku.name}: -> {sivu}" + ("" if muuttui else " (ei muutosta)"), True


def main():
    kuiva = "--kuivaharjoitus" in sys.argv
    if kuiva:
        print("KUIVAHARJOITUS — mitään ei kirjoiteta\n")
    kartta = kategoriakartta()
    print(f"{len(kartta)} kategoriaa luettu index.html:stä\n")

    ohitettu = muutettu = 0
    ok = True
    for polku in sorted(ROOT.glob("*.html")):
        if polku.name.startswith(("index", "kategoria-", "tietoa", "random", "artikkel")):
            continue
        rivi, onnistui = kasittele(polku, kartta, kuiva)
        ok = ok and onnistui
        if "ohitettu" in rivi:
            ohitettu += 1
        else:
            muutettu += 1
        if not onnistui or "VAROITUS" in rivi:
            print(rivi)
    print(f"{muutettu} sivua käsitelty, {ohitettu} ohitettu.")
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
