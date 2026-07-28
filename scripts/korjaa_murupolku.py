#!/usr/bin/env python3
"""
Osoittaa ilmiösivujen murupolun toiselle tasolle oikeaan kategoriasivuun.

Ennen: taso 2 osoitti etusivun ankkuriin (https://www.ilmiöt.fi/#pesut-ja-...),
jonka Google tulkitsee samaksi sivuksi kuin etusivun — murupolku oli siis
käytännössä "Etusivu › Etusivu › Ilmiö". Kategoriasivut julkaistiin 2026-07-21,
joten oikea kohde on nyt kategoria-<slug>.html.

Korjaa kaksi asiaa samalla, jotta rakenteinen data vastaa näkyvää sisältöä
(Googlen vaatimus murupolun rich resultille):

  1. JSON-LD  BreadcrumbList → itemListElement[1].item
  2. Näkyvä   <span class="kortti-breadcrumb-kat">  →  <a href=...>

Sivutuotteena jokainen ilmiösivu saa sisältölinkin omaan kategoriaansa.

Idempotentti — voi ajaa monta kertaa.

Käyttö:
    python3 scripts/korjaa_murupolku.py            # kaikki ilmiösivut
    python3 scripts/korjaa_murupolku.py --tarkista  # ei kirjoita, raportoi vain
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
KANTA = "https://www.ilmiöt.fi"

KAT_RE = re.compile(
    r'<div class="hub-kategoria" id="([^"]+)">\s*'
    r'<h2 class="hub-kat-label">(?:<span class="hub-kat-nro">\d+</span>)?([^<]+)'
    r'<span class="hub-kat-count">', re.S)

NAKYVA_RE = re.compile(
    r'<span class="kortti-breadcrumb-kat">([^<]+)</span>')


def kategoriat() -> dict:
    """index.html → hub-kategorian id → (nimi, kategoriasivun tiedostonimi)

    Kategorian id on pääosin sama kuin sivun slug, mutta tilastokategorialla on
    id 'tilastoilla-valehtelu-kategoria' törmäyksen välttämiseksi — sama
    -kategoria-pääte riisutaan kuin build_liittyvat.py:ssä."""
    src = (ROOT / "index.html").read_text(encoding="utf-8")
    kat = {}
    for kid, nimi in KAT_RE.findall(src):
        slug = re.sub(r"-kategoria$", "", kid)
        tiedosto = f"kategoria-{slug}.html"
        assert (ROOT / tiedosto).exists(), f"{tiedosto} puuttuu"
        kat[kid] = (nimi.strip(), tiedosto)
    assert len(kat) == 12, f"kategorioita {len(kat)}, odotettiin 12"
    return kat


def korjaa(polku: Path, kat: dict) -> tuple:
    src = polku.read_text(encoding="utf-8")
    alku = src
    jsonld = nakyva = 0

    for kid, (nimi, tiedosto) in kat.items():
        vanha = f'"item": "{KANTA}/#{kid}"'
        if vanha in src:
            src = src.replace(vanha, f'"item": "{KANTA}/{tiedosto}"')
            jsonld += 1

    def linkita(m):
        nonlocal nakyva
        nimi = m.group(1)
        osuma = [t for n, t in kat.values() if n == nimi]
        if not osuma:
            return m.group(0)
        nakyva += 1
        return (f'<a href="{osuma[0]}" class="kortti-breadcrumb-kat">'
                f'{nimi}</a>')

    src = NAKYVA_RE.sub(linkita, src)

    if src != alku:
        polku.write_text(src, encoding="utf-8")
    return jsonld, nakyva


def main() -> None:
    tarkista = "--tarkista" in sys.argv
    kat = kategoriat()
    sivut = sorted(p for p in ROOT.glob("*.html")
                   if not p.name.startswith("kategoria-")
                   and p.name not in ("index.html", "tietoa.html", "random.html"))
    j = n = muutettu = 0
    for sivu in sivut:
        src = sivu.read_text(encoding="utf-8")
        if "kortti-breadcrumb-kat" not in src:
            continue
        if tarkista:
            auki = len(re.findall(rf'"item": "{re.escape(KANTA)}/#', src))
            if auki:
                print(f"  {sivu.name}: {auki} korjaamatonta JSON-LD-itemiä")
                j += auki
            continue
        dj, dn = korjaa(sivu, kat)
        j += dj
        n += dn
        if dj or dn:
            muutettu += 1
    if tarkista:
        print(f"tarkistus: {j} korjaamatonta itemiä")
    else:
        print(f"murupolku: {muutettu} sivua kirjoitettu "
              f"({j} JSON-LD-itemiä, {n} näkyvää linkkiä)")


if __name__ == "__main__":
    main()
