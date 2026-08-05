#!/usr/bin/env python3
"""Kääntää jsdelivr-CDN-viittaukset paikallisiin kopioihin js/-kansiossa.

CLAUDE.md: "Sivusto ei lataa mitään ulkopuoliselta palvelimelta." Paikalliset
kopiot ladattiin 28.7., mutta HTML:ää ei käännetty — tämä tekee sen.

Kuivaharjoitus oletuksena; kirjoitus --kirjoita-lipulla.
"""
import argparse
import pathlib
import re
import sys

JUURI = pathlib.Path(__file__).resolve().parent.parent

KORVAUKSET = [
    ("https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js", "js/mermaid.min.js"),
    ("https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js", "js/chart.umd.min.js"),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--kirjoita", action="store_true", help="kirjoita muutokset levylle")
    args = ap.parse_args()

    # Tarkista että paikalliset kopiot ovat olemassa ennen kuin viitataan niihin.
    for _, paikallinen in KORVAUKSET:
        p = JUURI / paikallinen
        if not p.is_file():
            sys.exit(f"VIRHE: paikallinen kopio puuttuu: {paikallinen}")

    yhteensa = 0
    jaannos = []
    for sivu in sorted(JUURI.glob("*.html")):
        teksti = sivu.read_text(encoding="utf-8")
        uusi = teksti
        osumat = []
        for cdn, paikallinen in KORVAUKSET:
            n = uusi.count(cdn)
            if n:
                uusi = uusi.replace(cdn, paikallinen)
                osumat.append(f"{n}× {paikallinen}")
        if uusi != teksti:
            yhteensa += 1
            print(f"{sivu.name}: {', '.join(osumat)}")
            if args.kirjoita:
                sivu.write_text(uusi, encoding="utf-8")
        # Jäännökset luetaan korvatusta tekstistä, jotta kuivaharjoitus
        # kertoo mitä JÄISI jäljelle eikä mitä on nyt.
        for m in re.findall(r"https://cdn\.jsdelivr\.net[^\"'\s]*", uusi):
            jaannos.append(f"{sivu.name}: {m}")

    print(f"\n{yhteensa} sivua {'muutettu' if args.kirjoita else 'muuttuisi'}")
    if jaannos:
        print(f"HUOM: {len(jaannos)} tuntematonta jsdelivr-viittausta jäi:")
        for r in jaannos[:10]:
            print(f"  {r}")
    else:
        print("Yhtään jsdelivr-viittausta ei jää jäljelle.")


if __name__ == "__main__":
    main()
