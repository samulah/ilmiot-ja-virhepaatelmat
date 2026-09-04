#!/usr/bin/env python3
"""
Lisää ilmiösivuille linkin Vedätys-peliin (peli.html).

Linkki menee "Lue lisää" -lohkon eteen omana rivinään, koska siinä kohtaa
lukija on jo lukenut vastakeinot ja etsii seuraavaa askelta. Lohko on olemassa
139/139 sivulla, joten sijoituskohta on aina sama.

Käsitellään vain ne ilmiöt, joilla on kohtia pelipankissa (pelidata/*.json) —
linkki peliin on lupaus harjoittelusta, eikä sitä anneta sivulle jonka
tekniikkaa peli ei tunne.

Idempotentti: jo lisätty linkki tunnistetaan merkkijonosta "peli-harjoittele"
eikä sitä lisätä uudelleen.

    python3 scripts/lisaa_pelilinkit.py             # kuivaharjoitus
    python3 scripts/lisaa_pelilinkit.py --kirjoita  # kirjoittaa
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
PELIDATA = ROOT / "pelidata"
MERKKI = "peli-harjoittele"
ANKKURI = '<div class="lue-lisaa">'

MALLI = (
    '<p class="{merkki}" style="margin:1.4rem 0 0;padding:.7rem .9rem;'
    'background:#FBF5E0;border-left:3px solid #C9A84C;font-size:.95em">'
    '<b>Harjoittele tämän tunnistamista.</b> '
    '<a href="peli.html">Vedätys</a> on päivittäinen peli, jossa {nimi_ala} '
    'on yksi tunnistettavista tempuista — mukana on aina myös tavallisia '
    'viestejä, joissa ei ole mitään vikaa.</p>\n'
)


def ilmiot_pankissa() -> dict:
    """slug -> kohtien määrä. Rehellisten tiedostossa ilmio on null."""
    ulos = {}
    for polku in sorted(PELIDATA.glob("*.json")):
        d = json.loads(polku.read_text(encoding="utf-8"))
        slug = d.get("ilmio")
        if slug:
            ulos[slug] = len(d["kohdat"])
    return ulos


def nimi_alamuodossa(slug: str) -> str:
    """
    Ilmiön nimi sellaisena kuin se luetaan lauseen keskellä.

    Nimet ovat korttilistalla isolla alkukirjaimella. Lyhenteet (DARVO) ja
    erisnimet on jätettävä rauhaan, muut kirjoitetaan pienellä — muuten
    lauseen keskelle jää kesken virkkeen alkava iso kirjain.
    """
    from build_peli import kortit
    nimi = kortit()[slug]["nimi"]
    if nimi.isupper() or nimi.split()[0].isupper():
        return nimi
    return nimi[0].lower() + nimi[1:]


def main() -> None:
    kirjoita = "--kirjoita" in sys.argv
    pankki = ilmiot_pankissa()
    if not pankki:
        sys.exit("VIRHE: pelidata/*.json ei sisällä yhtään ilmiötä")

    sys.path.insert(0, str(ROOT / "scripts"))
    muutettu, ohitettu, puuttuu = [], [], []

    for slug in sorted(pankki):
        sivu = ROOT / f"{slug}.html"
        if not sivu.exists():
            puuttuu.append(slug)
            continue
        s = sivu.read_text(encoding="utf-8")
        if MERKKI in s:
            ohitettu.append(slug)
            continue
        if ANKKURI not in s:
            puuttuu.append(f"{slug} (ei lue-lisaa-lohkoa)")
            continue
        pala = MALLI.format(merkki=MERKKI, nimi_ala=nimi_alamuodossa(slug))
        # Vain ensimmäinen esiintymä: lohko on sivulla kerran, mutta
        # count=1 suojaa siltä varalta että joku lisää toisen.
        s = s.replace(ANKKURI, pala + ANKKURI, 1)
        if kirjoita:
            sivu.write_text(s, encoding="utf-8")
        muutettu.append(slug)

    print(f"Pelipankissa {len(pankki)} ilmiötä.")
    print(f"  Linkki lisätään: {len(muutettu)}")
    for x in muutettu:
        print(f"    + {x}")
    if ohitettu:
        print(f"  Linkki jo olemassa: {len(ohitettu)}")
    if puuttuu:
        print(f"  ONGELMIA: {len(puuttuu)}")
        for x in puuttuu:
            print(f"    ! {x}")
    if not kirjoita:
        print("\n(kuivaharjoitus — mitään ei kirjoitettu; --kirjoita tekee muutokset)")


if __name__ == "__main__":
    main()
