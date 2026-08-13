#!/usr/bin/env python3
"""Korvaa geneeriset "— mitä se tarkoittaa?" -titlet kuvailevilla.

Tausta: GSC 13.8.2026. Sijoituksella 6-12 geneerisen titlen sivut saivat
1597 näyttöä ja 4 klikkiä (0,25 %); kuvailevan titlen sivut 899 näyttöä ja
8 klikkiä (0,89 %) — käytännössä samalla keskisijalla (9,10 vs 9,12).

Nämä 11 sivua kantavat 42 % koko sivuston näyttökerroista. Kaikilla on jo
hyvä, kuvaileva H1; title vain heittää sen pois ja lupaa määritelmän — juuri
sen, minkä Wikipedia ja AI-yhteenveto antavat SERPissä yläpuolella.

Vain <title> muuttuu. Metakuvauksiin, dateModifiediin ja näkyvään
"Päivitetty"-päivään ei kosketa, jotta seuraava GSC-otos mittaa yhtä muuttujaa
eikä sitemapin lastmod valehtele.

Käyttö:  python3 scripts/korjaa_titlet.py            (kuivaharjoitus)
         python3 scripts/korjaa_titlet.py --kirjoita
"""
import re
import sys
from pathlib import Path

JUURI = Path(__file__).resolve().parent.parent

# tiedosto -> (vanha title, uusi title). Uusi seuraa sivun omaa H1-kulmaa.
TITLET = {
    "hyvesignalointi.html": (
        "Hyvesignalointi — mitä se tarkoittaa? | Ilmiöitä",
        "Hyvesignalointi — hyvettä yleisölle, ei tekoja | Ilmiöitä",
    ),
    "ai-slop.html": (
        "AI slop suomeksi — mitä se tarkoittaa? | Ilmiöitä",
        "AI slop suomeksi — näin tunnistat koneellisen sisällön | Ilmiöitä",
    ),
    "whataboutismi.html": (
        "Whataboutismi — mitä se tarkoittaa? | Ilmiöitä",
        "Whataboutismi — entäs-argumentti ja vastaus siihen | Ilmiöitä",
    ),
    "dunning-kruger.html": (
        "Dunning–Kruger-ilmiö — mitä se tarkoittaa? | Ilmiöitä",
        "Dunning–Kruger-ilmiö — itsevarmuus ilman taitoa | Ilmiöitä",
    ),
    "doomscrolling.html": (
        "Doomscrolling suomeksi — mitä se tarkoittaa? | Ilmiöitä",
        "Doomscrolling suomeksi — näin katkaiset kierteen | Ilmiöitä",
    ),
    "halo-efekti.html": (
        "Halo-efekti — mitä se tarkoittaa? | Ilmiöitä",
        "Halo-efekti — ensivaikutelman loukku päätöksissä | Ilmiöitä",
    ),
    "hanlonin-partaveitsi.html": (
        "Hanlonin partaveitsi — mitä se tarkoittaa? | Ilmiöitä",
        "Hanlonin partaveitsi — tyhmyys ennen pahuutta | Ilmiöitä",
    ),
    "kaarmeoljy.html": (
        "Käärmeöljy — mitä se tarkoittaa? | Ilmiöitä",
        "Käärmeöljy — ihmetuote joka parantaa kaiken | Ilmiöitä",
    ),
    "honeypot-huijaus.html": (
        "Honeypot-huijaus — mitä se tarkoittaa? | Ilmiöitä",
        "Honeypot-huijaus — ansa josta ei pääse ulos | Ilmiöitä",
    ),
    "peterin-periaate.html": (
        "Peterin periaate — mitä se tarkoittaa? | Ilmiöitä",
        "Peterin periaate — ylennys epäpätevyyden tasolle | Ilmiöitä",
    ),
    "streisand-ilmio.html": (
        "Streisand-ilmiö — mitä se tarkoittaa? | Ilmiöitä",
        "Streisand-ilmiö — salailu levittää tiedon | Ilmiöitä",
    ),
}


def main() -> int:
    kirjoita = "--kirjoita" in sys.argv
    muutettu = virheet = 0

    for nimi, (vanha, uusi) in TITLET.items():
        polku = JUURI / nimi
        if not polku.exists():
            print(f"  PUUTTUU  {nimi}")
            virheet += 1
            continue

        teksti = polku.read_text(encoding="utf-8")
        osuma = re.search(r"<title>(.*?)</title>", teksti, re.S)
        if not osuma:
            print(f"  EI TITLEÄ {nimi}")
            virheet += 1
            continue

        nykyinen = osuma.group(1).strip()
        if nykyinen == uusi:
            print(f"  jo kunnossa  {nimi}")
            continue
        if nykyinen != vanha:
            # Title on muuttunut skriptin kirjoittamisen jälkeen — älä ylikirjoita.
            print(f"  OHITETTU  {nimi}\n      odotettiin: {vanha}\n      löytyi:     {nykyinen}")
            virheet += 1
            continue

        # og:title ja twitter:title seuraavat samaa tekstiä, jos ne vastaavat vanhaa.
        uusi_teksti = teksti.replace(f"<title>{osuma.group(1)}</title>", f"<title>{uusi}</title>", 1)
        for omin in ('property="og:title"', 'name="twitter:title"'):
            uusi_teksti = re.sub(
                r'(<meta\s+' + omin + r'\s+content=")' + re.escape(vanha) + r'(")',
                r"\1" + uusi.replace("\\", "\\\\") + r"\2",
                uusi_teksti,
            )

        print(f"  {nimi}\n      - {vanha}  ({len(vanha)} merkkiä)\n      + {uusi}  ({len(uusi)} merkkiä)")
        muutettu += 1
        if kirjoita:
            polku.write_text(uusi_teksti, encoding="utf-8")

    tila = "kirjoitettu" if kirjoita else "KUIVAHARJOITUS — ei kirjoitettu"
    print(f"\n{muutettu} sivua muuttuisi, {virheet} ongelmaa. {tila}.")
    if not kirjoita and muutettu:
        print("Aja uudelleen --kirjoita-lipulla.")
    return 1 if virheet else 0


if __name__ == "__main__":
    raise SystemExit(main())
