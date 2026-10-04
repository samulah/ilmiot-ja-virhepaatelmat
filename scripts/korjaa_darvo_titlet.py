#!/usr/bin/env python3
"""Korjaa 26 sivua, jotka julkaistiin pohjasivun titlellä.

Tausta: SEO-auditointi 4.10.2026 (ACTION-PLAN.md kohta 1). Roolit ja valtapelit
(9 sivua) ja Trollaus (17 sivua) rakennettiin darvo.html:n pohjalta, ja
luonnosskriptit vaihtoivat h1:n, metakuvauksen, og:titlen ja scheman mutta
eivät <title>:ä. Kaikilla 26 sivulla luki
"DARVO — manipulaatiotaktiikka suomeksi | Ilmiöitä".

Muutos per sivu (5 kenttää):
    <title>, og:title, twitter:title, JSON-LD dateModified, bylinen "Päivitetty"

og:title ja twitter:title seuraavat uutta titleä sellaisenaan. Yhdeksällä
sivulla ne olivat muotoa "— mitä se tarkoittaa", joka peruttiin 13.8.2026
(ks. korjaa_titlet.py), joten vanhaa og:titleä ei kopioida titleksi.

Brändipääte " | Ilmiöitä" on mukana aina kun title mahtuu sen kanssa 60
merkkiin, muuten se jää pois.

Toistumisen esto on lisaa_ilmiot.py:n tarkista_title() — tämä skripti korjaa
vain jo julkaistut.

Käyttö:  python3 scripts/korjaa_darvo_titlet.py            (kuivaharjoitus)
         python3 scripts/korjaa_darvo_titlet.py --kirjoita
"""
import re
import sys
from datetime import date
from pathlib import Path

JUURI = Path(__file__).resolve().parent.parent

VANHA = "DARVO — manipulaatiotaktiikka suomeksi | Ilmiöitä"
PAIVA = date(2026, 10, 4)
MAX = 60

TITLET = {
    "doksaus": "Doksaus (doxxing) — mitä se on ja miten suojaudut | Ilmiöitä",
    "draamakolmio": "Draamakolmio — Karpmanin kolme roolia suomeksi | Ilmiöitä",
    "dunkkaus": "Dunkkaus ja ratio — mitä ne tarkoittavat somessa? | Ilmiöitä",
    "harmaa-kivi": "Harmaa kivi (grey rock) — menetelmä suomeksi | Ilmiöitä",
    "huolitrollaus": "Huolitrollaus — vastustaja esiintyy huolestuneena ystävänä",
    "kafkatrapping": "Kafkatrapping — kun kiistäminen todistaa syyllisyyden",
    "kaksoissidos": "Kaksoissidos (double bind) — käsky, jota ei voi totella",
    "kuka-tahansa-voi-trollata": "Kuka tahansa voi trollata — tutkimus huonosta päivästä",
    "kunhan-kysyn": "Kunhan kysyn (just asking questions) — väite kysymyksenä",
    "maalittaminen": "Maalittaminen — mitä se on ja miten siihen varaudutaan",
    "mahdollistaja": "Mahdollistaja (enabler) — apu, joka pitää ongelman käynnissä",
    "motte-and-bailey": "Motte and bailey — rohkea väite, turvallinen perääntymistie",
    "no-contact": "No contact — mitä täydellinen katkaisu tarkoittaa | Ilmiöitä",
    "nutpicking": "Nutpicking — hölmöin kommentti koko joukon kasvoina",
    "pimea-tetradi": "Pimeä tetradi ja trollaus — mitä tutkimus sanoo? | Ilmiöitä",
    "roolinvaihto": "Roolinvaihto draamakolmiossa — mikä on switch | Ilmiöitä",
    "sealioning": "Sealioning eli merileijonointi — kun kysely ei lopu",
    "shitpostaus": "Shitpostaus (shitposting) — keskustelu hukutetaan roskaan",
    "syntipukki": "Syntipukki-rooli — miksi ryhmä tarvitsee yhden | Ilmiöitä",
    "tone-policing": "Tone policing — puhutaan sävystä, ei asiasta | Ilmiöitä",
    "trollaus": "Trollaus — mitä se on ja miksi trolli voittaa väittelyn",
    "trollin-ruokkiminen": "Älä ruoki trollia — toimiiko neuvo oikeasti? | Ilmiöitä",
    "vain-vitsi": "”Se oli vain vitsi” — kun ironia suojaa vastuulta | Ilmiöitä",
    "valirikko": "Välirikko — miksi lähtijä ja jäävä maksavat eri hinnan",
    "verkon-estottomuus": "Verkon estottomuus — miksi netissä sanotaan enemmän",
    "voittajakolmio": "Voittajakolmio — Choyn vastine draamakolmiolle | Ilmiöitä",
}


def korvaa(teksti, kuvio, korvaus, nimi, kentta):
    teksti, k = re.subn(kuvio, korvaus, teksti)
    assert k == 1, f"{nimi}: {kentta} löytyi {k} kertaa, pitää olla 1"
    return teksti


def main() -> int:
    kirjoita = "--kirjoita" in sys.argv
    muutettu = virheet = 0
    nakyva = f"{PAIVA.day}.{PAIVA.month}.{PAIVA.year}"

    assert len(set(TITLET.values())) == len(TITLET), "sama title kahdella sivulla"

    for slug, uusi in TITLET.items():
        nimi = f"{slug}.html"
        polku = JUURI / nimi
        assert len(uusi) <= MAX, f"{nimi}: title {len(uusi)} merkkiä, raja {MAX}"
        assert '"' not in uusi and "&" not in uusi and "<" not in uusi, \
            f"{nimi}: title menee HTML-attribuuttiin, ei erikoismerkkejä"

        teksti = polku.read_text(encoding="utf-8")
        nykyinen = re.search(r"<title>(.*?)</title>", teksti, re.S).group(1).strip()
        if nykyinen == uusi:
            print(f"  jo kunnossa  {nimi}")
            continue
        if nykyinen != VANHA:
            # Title on muuttunut skriptin kirjoittamisen jälkeen — älä ylikirjoita.
            print(f"  OHITETTU  {nimi}\n      löytyi: {nykyinen}")
            virheet += 1
            continue

        # Korvaus funktiona, jottei titlen sisältöä tulkita ryhmäviittaukseksi.
        t = korvaa(teksti, r"<title>.*?</title>",
                   lambda m: f"<title>{uusi}</title>", nimi, "<title>")
        for omin in ('property="og:title"', 'name="twitter:title"'):
            t = korvaa(t, r'(<meta\s+' + omin + r'\s+content=")[^"]*(")',
                       lambda m: m.group(1) + uusi + m.group(2), nimi, omin)
        t = korvaa(t, r'("dateModified": ")\d{4}-\d{2}-\d{2}(")',
                   lambda m: m.group(1) + PAIVA.isoformat() + m.group(2),
                   nimi, "dateModified")
        t = korvaa(t, r'(<p class="ilmio-byline">.*?Päivitetty )[\d.]+(</p>)',
                   lambda m: m.group(1) + nakyva + m.group(2), nimi, "byline")

        print(f"  {nimi}\n      + {uusi}  ({len(uusi)} merkkiä)")
        muutettu += 1
        if kirjoita:
            polku.write_text(t, encoding="utf-8")

    tila = "kirjoitettu" if kirjoita else "KUIVAHARJOITUS — ei kirjoitettu"
    print(f"\n{muutettu} sivua muuttuisi, {virheet} ongelmaa. {tila}.")
    if not kirjoita and muutettu:
        print("Aja uudelleen --kirjoita-lipulla.")
    return 1 if virheet else 0


if __name__ == "__main__":
    raise SystemExit(main())
