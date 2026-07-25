#!/usr/bin/env python3
"""Nostaa .infolaatikko / .huomiolaatikko -laatikoiden <strong>-otsikot <h2>:ksi.

Miksi: 2026-07-25 auditissa 97/111 sivulla oli vain kaksi otsikkoa (h1 ja
"Liittyvät ilmiöt"). Sivuston siteerattavin sisältö — "Ilmiö arjessa",
"Tunnistaminen ja vastakeinot", "Tunnettuja tapauksia" jne. — oli merkattu
lihavoituna tekstinä divin sisällä, ei otsikkona. Google (passage ranking,
featured snippet) ja AI-hakujen retrieval pilkkovat dokumentin
otsikkorajoista, joten artikkeli näyttäytyi yhtenä erittelemättömänä
möykkynä.

Otsikkotekstejä EI kirjoiteta uusiksi — ne ovat jo valmiiksi hyviä ja
artikkelikohtaisia (181 laatikkoa, 139 eri tekstiä). Vain merkkaus muuttuu.

Ulkoasu säilyy täsmälleen ennallaan: h2 tyylitellään `display:inline` +
`font:inherit`, jolloin se renderöityy kuten <strong> ennenkin. CSS:n
display ei vaikuta otsikkosemantiikkaan, joten crawlerit ja ruudunlukijat
saavat oikean rakenteen vaikka lukija ei näe eroa.

Idempotentti: jo muunnetut laatikot ohitetaan.

Ajo:  python3 scripts/laatikko_otsikot.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LAATIKKO = re.compile(
    r'(<div class="(?:info|huomio)laatikko">)\s*<strong>(.*?)</strong>', re.S)

# Riittävän spesifinen (0,2,1) voittaakseen `.ilmio h2` (0,1,1) ja
# style.css:n `h1, h2, h3` -säännön riippumatta sääntöjen järjestyksestä.
CSS = """
.infolaatikko h2.laatikko-otsikko, .huomiolaatikko h2.laatikko-otsikko {
  display: inline; font: inherit; font-weight: 700; color: inherit;
  margin: 0; padding: 0; letter-spacing: inherit;
}"""

CSS_TUNNISTE = "h2.laatikko-otsikko"


def muunna(html):
    """Palauttaa (uusi_html, muunnettuja_laatikoita)."""
    uusi, n = LAATIKKO.subn(
        lambda m: f'{m.group(1)}\n<h2 class="laatikko-otsikko">{m.group(2)}</h2>',
        html)
    if n and CSS_TUNNISTE not in uusi:
        # lisätään sääntö siihen <style>-lohkoon, jossa laatikkotyylit ovat
        kohde = None
        for m in re.finditer(r'<style[^>]*>(.*?)</style>', uusi, re.S):
            if re.search(r'\.(?:info|huomio)laatikko\s*\{', m.group(1)):
                kohde = m
        assert kohde, "laatikko-CSS:ää ei löytynyt <style>-lohkoista"
        loppu = kohde.end() - len("</style>")
        uusi = uusi[:loppu] + CSS + "\n" + uusi[loppu:]
    return uusi, n


if __name__ == "__main__":
    yht_sivut = yht_laatikot = 0
    for p in sorted(ROOT.glob("*.html")):
        html = p.read_text(encoding="utf-8")
        if 'laatikko">' not in html:
            continue
        uusi, n = muunna(html)
        if uusi != html:
            p.write_text(uusi, encoding="utf-8")
            yht_sivut += 1
            yht_laatikot += n
            print(f"  ✎ {p.name}: {n} laatikkoa")
    if yht_sivut:
        print(f"\nMuunnettu {yht_laatikot} laatikkoa {yht_sivut} sivulla")
    else:
        print("Kaikki laatikot olivat jo h2-muodossa")
