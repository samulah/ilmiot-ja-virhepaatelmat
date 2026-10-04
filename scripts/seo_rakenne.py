#!/usr/bin/env python3
"""Lisää ilmiösivuille osioankkurit ja <main>-elementin.

Tausta: SEO-auditointi 4.10.2026 (ACTION-PLAN.md kohta 12). Yhdelläkään h2:lla
ei ollut id:tä, joten osioon ei voinut linkittää eikä hakukone voinut tarjota
"siirry kohtaan" -linkkiä, eikä sivuilla ollut <main>-elementtiä.

Muutos per sivu:
  1. jokainen .ilmio-säiliön <h2> saa id:n otsikkotekstistä
     ("Tunnistaminen ja vastakeinot:" → id="tunnistaminen-ja-vastakeinot")
  2. <main> avautuu ennen .ilmio-säiliötä ja sulkeutuu Liittyvät ilmiöt
     -lohkon jälkeen

Kaksi rajausta, molemmat tarkoituksella:

- .ilmio-säiliö pysyy <div>:nä eikä sen avaus- tai lopputagiin kosketa.
  Luonnosskriptit (build_*_luonnokset.py) korvaavat pohjasivun sisällön
  kuviolla '<div class="ilmio" id="…">.*?\\n</div>\\n\\n  <aside', joten
  <article>-tagi tai mikä tahansa lisäys noiden kahden kohdan väliin rikkoisi
  seuraavan erän rakentamisen.
- "Liittyvät ilmiöt" -otsikko jää ilman id:tä: build_liittyvat.py kirjoittaa
  koko lohkon uudelleen ja pudottaisi sen joka ajolla.

Olemassa olevaa id:tä ei koskaan muuteta, joten ankkuri pysyy samana vaikka
otsikon teksti myöhemmin muuttuisi. Idempotentti. Uudet sivut saavat id:nsä,
kun tämä ajetaan julkaisun jälkeen (lisaa_ilmiot.py tulostaa sen ajolistaan).

Käyttö:  python3 scripts/seo_rakenne.py            (kuivaharjoitus)
         python3 scripts/seo_rakenne.py --kirjoita
"""
import html
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

H2_RE = re.compile(r"<h2((?:\s[^>]*)?)>(.*?)</h2>", re.S)
ILMIO_ALKU = re.compile(r'\n  <div class="ilmio" id="[^"]+">\n')
ASIDE_RE = re.compile(r'(<aside class="liittyvat".*?</aside>)', re.S)


def tunniste(otsikko):
    """Otsikkoteksti → ankkuri: pienet kirjaimet, ä→a, ö→o, muu → väliviiva."""
    t = html.unescape(re.sub(r"<[^>]+>", "", otsikko)).lower()
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t[:60].rstrip("-") or "osio"


def kasittele(slug, teksti):
    alut = ILMIO_ALKU.findall(teksti)
    asidet = ASIDE_RE.findall(teksti)
    assert len(alut) == 1, f"{slug}: .ilmio-säiliön avauksia {len(alut)}, pitää olla 1"
    assert len(asidet) == 1, f"{slug}: Liittyvät-lohkoja {len(asidet)}, pitää olla 1"

    alku = ILMIO_ALKU.search(teksti).start() + 1
    aside_alku = ASIDE_RE.search(teksti).start()
    assert alku < aside_alku, f"{slug}: Liittyvät-lohko on ennen sisältöä"

    # 1. h2-ankkurit vain .ilmio-säiliön sisällä
    varatut = set(re.findall(r'\bid="([^"]+)"', teksti))
    uusia = 0

    def ankkuroi(m):
        nonlocal uusia
        if re.search(r"\bid=", m.group(1)):
            return m.group(0)
        pohja = tunniste(m.group(2))
        tunnus, i = pohja, 2
        while tunnus in varatut:
            tunnus, i = f"{pohja}-{i}", i + 1
        varatut.add(tunnus)
        uusia += 1
        return f'<h2{m.group(1)} id="{tunnus}">{m.group(2)}</h2>'

    runko = H2_RE.sub(ankkuroi, teksti[alku:aside_alku])
    teksti = teksti[:alku] + runko + teksti[aside_alku:]

    # 2. <main> sisällön ja Liittyvät-lohkon ympärille
    main = 0
    if "<main" not in teksti:
        teksti = teksti[:alku] + "  <main>\n" + teksti[alku:]
        teksti, k = ASIDE_RE.subn(lambda m: m.group(1) + "\n  </main>", teksti)
        assert k == 1
        main = 1
    assert teksti.count("<main") == 1 and teksti.count("</main>") == 1, \
        f"{slug}: <main> ei ole parillinen"
    assert teksti.index("<main") < teksti.index("</main>")
    return teksti, uusia, main


def main(argv):
    kirjoita = "--kirjoita" in argv
    index = (ROOT / "index.html").read_text(encoding="utf-8")
    slugit = re.findall(r'<a href="([a-z0-9-]+)\.html" class="hub-kortti"', index)
    assert slugit, "index.html: kortteja ei löytynyt"

    sivuja = ankkureita = maineja = 0
    for slug in slugit:
        polku = ROOT / f"{slug}.html"
        vanha = polku.read_text(encoding="utf-8")
        uusi, a, m = kasittele(slug, vanha)
        ankkureita += a
        maineja += m
        if uusi != vanha:
            sivuja += 1
            if kirjoita:
                polku.write_text(uusi, encoding="utf-8")

    tila = "kirjoitettu" if kirjoita else "KUIVAHARJOITUS — ei kirjoitettu"
    print(f"{len(slugit)} sivua luettu: {sivuja} muuttuisi, "
          f"{ankkureita} h2-ankkuria, {maineja} <main>-elementtiä. {tila}.")


if __name__ == "__main__":
    main(sys.argv[1:])
