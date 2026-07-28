#!/usr/bin/env python3
"""Rakentaa Media ja julkisuus -kategoriasivun luonnoksen luonnokset-media/-kansioon.

Miksi oma skripti: build_kategoriat.py lukee ilmiökortit index.html:stä, eikä
tätä kategoriaa ole siellä ennen kuin ilmiöt 109–118 on julkaistu. Tässä kortit
tulevat build_media_luonnokset.py:n OMAT_KORTIT-taulusta, mutta itse sivun
renderöi build_kategoriat.rakenna() — eli luonnos on rakenteeltaan täsmälleen
sama kuin julkaistava sivu.

Julkaistaessa tätä skriptiä ei enää tarvita: kun kategoria on index.html:ssä,
sivun tekee `python3 scripts/build_kategoriat.py media-ja-julkisuus`.

Ajo:  python3 scripts/build_media_kategoria_luonnos.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import build_kategoriat as bk                      # noqa: E402
from build_media_luonnokset import OMAT_KORTIT     # noqa: E402

OUT = ROOT / "luonnokset-media"
SLUG = "media-ja-julkisuus"

# 13. kategoria: viimeinen, joten seuraavaa ei ole. Edellinen on nykyinen
# viimeinen (12. Tilastoilla valehtelu) ja sen väri on sen ensimmäisen
# ilmiökortin väri — sama sääntö kuin build_kategoriat.py:n jarjestys-listassa.
EDELLINEN = {"slug": "tilastoilla-valehtelu", "nro": 12,
             "label": "Tilastoilla valehtelu", "vari": "#1565c0"}


def main():
    meta, runko = bk.lue_sisalto(ROOT / "kategoriat" / f"{SLUG}.md")
    meta["_runko"] = runko

    kortit = [{"slug": s, "vari": v, "numero": n, "nimi": nimi, "kuvaus": kuvaus}
              for s, (n, v, nimi, kuvaus) in OMAT_KORTIT.items()]
    kortit.sort(key=lambda k: k["numero"])
    numerot = [k["numero"] for k in kortit]
    kat = {"nro": 13, "kat_yhteensa": 13,
           "label": "Media ja julkisuus",
           "kuvaus": meta["kuvaus"],
           "kortit": kortit,
           "ilmioalue": f"{min(numerot)}&ndash;{max(numerot)}"}

    html = bk.rakenna(SLUG, meta, kat, luonnos=True, edellinen=EDELLINEN, seuraava=None)

    # rakenna(luonnos=True) etuliittää ../ kaikkiin paitsi kategoria-linkkeihin.
    # Luonnoskansiossa asetelma on päinvastainen kuin julkaistuna:
    #   ilmiöluonnokset ovat samassa kansiossa  → ei ../
    #   kategoriasivut ovat juuressa            → ../
    for s in OMAT_KORTIT:
        html = html.replace(f'href="../{s}.html"', f'href="{s}.html"')
    html = html.replace('href="kategoria-', 'href="../kategoria-')

    html = html.replace(
        '<link rel="canonical"',
        '<meta name="robots" content="noindex"><!-- POISTA-JULKAISTAESSA -->\n  <link rel="canonical"')

    kohde = OUT / f"kategoria-{SLUG}.html"
    kohde.write_text(html, encoding="utf-8")
    sanoja = len(re.sub(r"<[^>]+>", " ", bk.muotoile(runko)).split())
    varoitus = "  ⚠ alle 300 sanaa uniikkia proosaa" if sanoja < 300 else ""
    print(f"{kohde.relative_to(ROOT)}: {len(kortit)} ilmiötä, ~{sanoja} sanaa{varoitus}")


if __name__ == "__main__":
    main()
