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

ASIDE_RE = re.compile(
    r'(<aside class="liittyvat" aria-label="Liittyvät ilmiöt">)(.*?)(</aside>)', re.S)

LINK_RE = re.compile(r'<a href="([^"]+)"')


def lue_ilmiot() -> dict:
    """index.html → href → {numero, vari, nimi, kuvaus}"""
    src = (ROOT / "index.html").read_text(encoding="utf-8")
    ilmiot = {}
    for href, vari, numero, nimi, kuvaus in HUB_CARD_RE.findall(src):
        ilmiot[href] = {
            "numero": int(numero), "vari": vari,
            "nimi": nimi.strip(), "kuvaus": kuvaus.strip(),
        }
    assert len(ilmiot) == 91, f"index.html: odotettiin 91 korttia, löytyi {len(ilmiot)}"
    return ilmiot


def kortti(href: str, tiedot: dict) -> str:
    return (
        f'    <a href="{href}" class="liittyvat-kortti" style="--c:{tiedot["vari"]}">\n'
        f'      <span class="liittyvat-numero">{tiedot["numero"]}</span>\n'
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
        sivut = sorted(ROOT / h for h in ilmiot)
    muutettu = 0
    for sivu in sivut:
        assert sivu.exists(), f"{sivu} puuttuu"
        if muunna_sivu(sivu, ilmiot):
            muutettu += 1
    print(f"liittyvat: {muutettu}/{len(sivut)} sivua kirjoitettu")


if __name__ == "__main__":
    main()
