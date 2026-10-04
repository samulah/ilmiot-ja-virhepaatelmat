#!/usr/bin/env python3
"""Yksi fonttilähde per sivu, esilataus kahdelle ensimmäisen näkymän fontille
ja CSS:n versiomerkki.

Tausta: SEO-auditointi 4.10.2026 (ACTION-PLAN.md kohta 2). Mobiilin CLS oli
labrassa 0,21 (etusivu) ja 0,19 (artikkeli) ja nolla, kun fontit estettiin:
siirtymä syntyy, kun varafontti vaihtuu verkkofonttiin ensimmäisen piirron
jälkeen. Artikkeli haki seitsemän fonttitiedostoa, joista kolme oli sama
tiedosto eri nimellä, koska sekä style.css että fonts/fonts.css määrittelivät
fontit ja 141 sivua linkitti molemmat.

Muutos per sivu (vain <head>):
  - sivu, joka linkittää style.css:n: versio → VERSIO, fonts/fonts.css- ja
    fonts/spectral.css-linkit pois (style.css kantaa samat @font-facet)
  - sivu, joka ei linkitä style.css:ää (index, tietoa, muutokset, peli):
    fonts/fonts.css?v=VERSIO, fonts/spectral.css-linkki pois (sen kaksi
    perhettä ovat fonts.css:ssä)
  - <link rel="preload"> kahdelle fontille ennen ensimmäistä tyylitiedostoa.
    Esilataus alkaa heti HTML:n alusta eikä vasta, kun CSS on haettu ja
    asettelu tietää tarvitsevansa fontin.

Mitä esiladataan, on mitattu sivutyypeittäin (mitä ensimmäisen näkymän teksti
käyttää): ilmiö- ja kategoriasivuilla leipäteksti on Source Sans 3, muilla
DM Sans; h1 on kaikilla Spectral 700. Vain latin-osajoukko — suomen ä ja ö
ovat siinä, latin-ext haetaan vain jos sivulla on sen merkkejä.

Kun style.css tai fonts/fonts.css muuttuu: nosta VERSIO ja aja tämä. Myös
build_kategoriat.py:n CSS_VERSIO on nostettava samaan (kategoriasivut
generoidaan, joten tämä skripti ei saa olla niiden ainoa lähde).

Idempotentti.
Käyttö:  python3 scripts/fontit_esilataus.py            (kuivaharjoitus)
         python3 scripts/fontit_esilataus.py --kirjoita
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERSIO = "20261004"

STYLE_RE = re.compile(r'(<link rel="stylesheet" href="style\.css)(?:\?v=\d+)?(">)')
FONTS_RE = re.compile(r'(<link rel="stylesheet" href="fonts/fonts\.css)(?:\?v=\d+)?(">)')
POIS_RE = re.compile(r'[ \t]*<link rel="stylesheet" href="fonts/(?:fonts|spectral)\.css(?:\?v=\d+)?">\n')
SPECTRAL_RE = re.compile(r'[ \t]*<link rel="stylesheet" href="fonts/spectral\.css(?:\?v=\d+)?">\n')
ESILATAUS_RE = re.compile(r'[ \t]*<link rel="preload" href="fonts/[^"]+" as="font"[^>]*>\n')


def esilataus(fontit):
    return "".join(
        f'  <link rel="preload" href="fonts/{f}-latin.woff2" as="font" '
        f'type="font/woff2" crossorigin>\n' for f in fontit)


def kasittele(nimi, teksti):
    """Palauttaa uuden tekstin tai None, jos sivu ei lataa sivuston fontteja."""
    paa_loppu = teksti.find("</head>")
    assert paa_loppu > 0, f"{nimi}: </head> puuttuu"
    paa, loppu = teksti[:paa_loppu], teksti[paa_loppu:]

    paa = ESILATAUS_RE.sub("", paa)          # vanha esilataus pois → idempotentti
    if STYLE_RE.search(paa):
        paa = POIS_RE.sub("", paa)
        paa, k = STYLE_RE.subn(rf"\g<1>?v={VERSIO}\g<2>", paa)
        assert k == 1, f"{nimi}: style.css-linkkejä {k}"
        fontit, ankkuri = ("sourcesans3-var", "spectral-700"), STYLE_RE
    elif FONTS_RE.search(paa):
        paa = SPECTRAL_RE.sub("", paa)
        paa, k = FONTS_RE.subn(rf"\g<1>?v={VERSIO}\g<2>", paa)
        assert k == 1, f"{nimi}: fonts.css-linkkejä {k}"
        fontit, ankkuri = ("dmsans-400", "spectral-700"), FONTS_RE
    else:
        return None

    for f in fontit:
        assert (ROOT / "fonts" / f"{f}-latin.woff2").exists(), f"fonts/{f}-latin.woff2 puuttuu"
    m = ankkuri.search(paa)
    rivin_alku = paa.rfind("\n", 0, m.start()) + 1
    paa = paa[:rivin_alku] + esilataus(fontit) + paa[rivin_alku:]
    return paa + loppu


def main(argv):
    kirjoita = "--kirjoita" in argv
    muuttuu = ohi = 0
    for polku in sorted(ROOT.glob("*.html")):
        vanha = polku.read_text(encoding="utf-8")
        uusi = kasittele(polku.name, vanha)
        if uusi is None:
            ohi += 1
            print(f"  ohitettu (ei tyylilinkkiä): {polku.name}")
            continue
        if uusi != vanha:
            muuttuu += 1
            if kirjoita:
                polku.write_text(uusi, encoding="utf-8")
    tila = "kirjoitettu" if kirjoita else "KUIVAHARJOITUS — ei kirjoitettu"
    print(f"{muuttuu} sivua muuttuisi, {ohi} ohitettu. {tila}.")


if __name__ == "__main__":
    main(sys.argv[1:])
