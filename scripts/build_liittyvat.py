#!/usr/bin/env python3
"""
Kirjoittaa ilmiösivujen "Liittyvät ilmiöt" -osiot korttimuotoon.

- Tietolähde: index.html:n hub-kortit (numero, väri --c, lyhyt nimi, kuvaus).
  Yksi totuuden lähde — kun etusivun kuvaus muuttuu, aja tämä uudelleen.
- Poimii sivun nykyiset liittyvät-linkit sekä vanhasta ul-muodosta että
  uudesta korttimuodosta → idempotentti, voi ajaa monta kertaa.
- Ei muuta sitä, MITKÄ ilmiöt liittyvät mihin — vain esitystavan.

Käyttö:
    python3 scripts/build_liittyvat.py                  # kaikki sivut
    python3 scripts/build_liittyvat.py paskuuttaminen.html [muut.html ...]
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

HUB_CARD_RE = re.compile(
    r'<a href="([^"]+)" class="hub-kortti" style="--c:(#[0-9a-fA-F]{6})">\s*'
    r'<span class="hub-numero">(\d+)</span>\s*'
    r'<span class="hub-teksti">\s*'
    r'<span class="hub-nimi">(.*?)</span>\s*'
    r'<span class="hub-kuvaus">(.*?)</span>\s*'
    r'</span>', re.S)

KAT_RE = re.compile(
    r'<div class="hub-kategoria" id="([^"]+)">\s*'
    r'<h2 class="hub-kat-label">(?:<span class="hub-kat-nro">\d+</span>)?([^<]+)<span class="hub-kat-count">.*?</span></h2>\s*'
    r'<p class="hub-kat-desc">(.*?)</p>(.*?)\n</div>', re.S)

ASIDE_RE = re.compile(
    r'(<aside class="liittyvat" aria-label="Liittyvät ilmiöt">)(.*?)(</aside>)', re.S)

LINK_RE = re.compile(r'<a href="([^"]+)"')


def lue_ilmiot() -> dict:
    """index.html → href → {numero, vari, nimi, kuvaus}

    Mukana ovat sekä ilmiösivut (numero) että kategoriasivut (numeron tilalla
    ⊞). Kategoriakortti syntyy, kun ilmiösivulla on linkki muotoa
    kategoria-<slug>.html — näin ilmiöltä on ylöspäin linkki kategoriaansa
    ilman että liittyvat-lohkoon tarvitaan uutta rakennetta."""
    src = (ROOT / "index.html").read_text(encoding="utf-8")
    ilmiot = {}
    for href, vari, numero, nimi, kuvaus in HUB_CARD_RE.findall(src):
        ilmiot[href] = {
            "numero": int(numero), "vari": vari,
            "nimi": nimi.strip(), "kuvaus": kuvaus.strip(),
        }
    assert ilmiot, "index.html: hub-kortteja ei löytynyt"

    for kat_id, label, kuvaus, runko in KAT_RE.findall(src):
        eka = HUB_CARD_RE.search(runko)
        slug = re.sub(r"-kategoria$", "", kat_id)
        ilmiot[f"kategoria-{slug}.html"] = {
            "numero": None,
            "vari": eka.group(2) if eka else "#8B6914",
            "nimi": f"{label.strip()} — koko kategoria",
            "kuvaus": re.sub(r"\s+", " ",
                             re.sub(r"<[^>]+>", "", kuvaus)).strip().split(". ")[0] + ".",
        }
    return ilmiot


def kortti(href: str, tiedot: dict) -> str:
    merkki = tiedot["numero"] if tiedot["numero"] is not None else "&#8862;"
    return (
        f'    <a href="{href}" class="liittyvat-kortti" style="--c:{tiedot["vari"]}">\n'
        f'      <span class="liittyvat-numero">{merkki}</span>\n'
        f'      <span class="liittyvat-teksti">\n'
        f'        <span class="liittyvat-nimi">{tiedot["nimi"]}</span>\n'
        f'        <span class="liittyvat-kuvaus">{tiedot["kuvaus"]}</span>\n'
        f'      </span>\n'
        f'      <span class="liittyvat-nuoli" aria-hidden="true">›</span>\n'
        f'    </a>'
    )


def muunna_sivu(polku: Path, ilmiot: dict) -> bool:
    src = polku.read_text(encoding="utf-8")
    osumat = ASIDE_RE.findall(src)
    assert len(osumat) == 1, f"{polku.name}: liittyvat-lohkoja {len(osumat)}, odotettiin 1"

    vanha_sisalto = osumat[0][1]
    hrefit = LINK_RE.findall(vanha_sisalto)
    assert hrefit, f"{polku.name}: ei linkkejä liittyvat-lohkossa"
    for h in hrefit:
        assert h in ilmiot, f"{polku.name}: linkkiä {h} ei löydy index.html:n korteista"

    kortit = "\n".join(kortti(h, ilmiot[h]) for h in hrefit)
    uusi = (
        f'\n    <h2>Liittyvät ilmiöt</h2>\n'
        f'    <div class="liittyvat-kortit">\n{kortit}\n    </div>\n  '
    )
    if uusi == vanha_sisalto:
        return False
    tulos = ASIDE_RE.sub(lambda m: m.group(1) + uusi + m.group(3), src, count=1)

    # Linkkimäärä ei saa muuttua
    uudet_hrefit = LINK_RE.findall(ASIDE_RE.search(tulos).group(2))
    assert uudet_hrefit == hrefit, f"{polku.name}: linkkilista muuttui"

    polku.write_text(tulos, encoding="utf-8")
    return True


def main() -> None:
    ilmiot = lue_ilmiot()
    if len(sys.argv) > 1:
        sivut = [ROOT / a for a in sys.argv[1:]]
    else:
        sivut = sorted(ROOT / h for h, t in ilmiot.items() if t["numero"] is not None)
    muutettu = 0
    for sivu in sivut:
        assert sivu.exists(), f"{sivu} puuttuu"
        if muunna_sivu(sivu, ilmiot):
            muutettu += 1
    print(f"liittyvat: {muutettu}/{len(sivut)} sivua kirjoitettu")


if __name__ == "__main__":
    main()
