#!/usr/bin/env python3
"""Lisää etusivun kategorioihin linkin niiden omalle kategoriasivulle.

Linkki menee `hub-kat-desc`-kappaleen loppuun, EI otsikkoon. Syy: kolme muuta
skriptiä (paivita_maarat.py, build_liittyvat.py, build_kategoriat.py) lukevat
otsikkoa regexillä

    <h2 class="hub-kat-label">([^<]+)<span class="hub-kat-count">

joten <a>-elementti otsikon sisällä rikkoisi ne kaikki. Kuvauskappaleen loppu
on sekä turvallinen että luettavuudeltaan parempi paikka.

Idempotentti: jo lisättyä linkkiä ei kahdenneta, ja poistetun kategoriasivun
linkki siivotaan pois.

Ajo:
    python3 scripts/lisaa_kategorialinkit.py            # vain olemassa olevat sivut
    python3 scripts/lisaa_kategorialinkit.py --kaikki   # kaikki 12 (esikatselu)
    python3 scripts/lisaa_kategorialinkit.py --kaikki --luonnos
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LUONNOSKANSIO = ROOT / "luonnokset-kategoriat"

TYYLI = """    .hub-kat-nro {
      display: inline-block;
      margin-right: 0.45em;
      font-weight: 700;
      letter-spacing: 0.02em;
      color: var(--c-primary-mid);
    }
    .hub-kat-nro::after { content: "."; }
    /* Oma rivi kuvauksen jälkeen. Kappaleen sisällä tämä katosi tekstiin:
       .hub-kat-desc on 0.76em, joten peritty koko oli liian pieni. */
    .hub-kat-linkki {
      display: inline-flex;
      align-items: center;
      gap: 0.45em;
      margin: 0 0 0.7rem 0.15rem;
      padding: 0.32rem 0.8rem;
      background: #fff;
      border: 1.5px solid #D4C090;
      color: var(--c-primary-mid);
      font-size: 0.8rem;
      font-weight: 600;
      letter-spacing: 0.01em;
      text-decoration: none;
      transition: border-color 0.12s, background 0.12s, color 0.12s;
    }
    .hub-kat-linkki:hover {
      border-color: var(--c-primary-mid);
      background: #FBF5E0;
      color: var(--c-primary-dark);
    }
    .hub-kat-linkki:focus-visible {
      outline: 2px solid var(--c-primary-mid);
      outline-offset: 2px;
    }

"""

# Linkki sijoitetaan kuvauskappaleen JÄLKEEN, ei sen sisään: ryhmä 4 on
# kappaleen ja korttiruudukon välinen tila, joka rakennetaan joka ajolla
# uudelleen — siksi skripti on idempotentti.
KAT_LOHKO_RE = re.compile(
    r'(<div class="hub-kategoria" id="([^"]+)">\s*'
    r'<h2 class="hub-kat-label">)(?:<span class="hub-kat-nro">\d+</span>)?'
    r'([^<]+<span class="hub-kat-count">.*?</span></h2>\s*'
    r'<p class="hub-kat-desc">.*?</p>)(.*?)'
    r'(<div class="hub-kortit">)', re.S)

LINKKI_RE = re.compile(r'<a class="hub-kat-linkki"[^>]*>.*?</a>', re.S)


def kategoriasivu_olemassa(slug, kaikki):
    return kaikki or (ROOT / f"kategoria-{slug}.html").exists()


def main(argv):
    kaikki = "--kaikki" in argv
    luonnos = "--luonnos" in argv

    html = (ROOT / "index.html").read_text(encoding="utf-8")
    lisatyt, poistetut = [], []
    laskuri = [0]

    def korvaa(m):
        alku, kat_id, keski, vali, kortit = m.groups()
        slug = re.sub(r"-kategoria$", "", kat_id)
        laskuri[0] += 1
        # numero HTML:ään (ei CSS-counteria: etusivun haku piilottaa
        # kategorioita, jolloin counter numeroisi ne uudelleen kesken haun)
        nro = f'<span class="hub-kat-nro">{laskuri[0]}</span>'

        if kategoriasivu_olemassa(slug, kaikki):
            lisatyt.append(slug)
            vali = (f'\n  <a class="hub-kat-linkki" href="kategoria-{slug}.html">'
                    f'Lue koko kategoria <span aria-hidden="true">&rarr;</span></a>\n  ')
        else:
            if LINKKI_RE.search(vali):
                poistetut.append(slug)
            vali = "\n  "
        return alku + nro + keski + vali + kortit

    uusi, n = KAT_LOHKO_RE.subn(korvaa, html)
    assert n, "index.html: hub-kategoria-lohkoja ei löytynyt"

    if ".hub-kat-nro" not in uusi:
        merkki = "    /* ── Tietoa-osio ── */"
        assert merkki in uusi, "index.html: tyylien ankkuria ei löytynyt"
        uusi = uusi.replace(merkki, TYYLI + merkki, 1)

    if luonnos:
        LUONNOSKANSIO.mkdir(exist_ok=True)
        # luonnoskansiosta juureen — paitsi kategoriasivut, jotka ovat vieressä
        uusi = re.sub(r'(href|src)="(?!https?:|#|\.\./|kategoria-)', r'\1="../', uusi)
        uusi = uusi.replace('"../search-index.js"', '"../search-index.js"')
        kohde = LUONNOSKANSIO / "index.html"
    else:
        kohde = ROOT / "index.html"

    kohde.write_text(uusi, encoding="utf-8")
    print(f"{kohde.relative_to(ROOT)}: {laskuri[0]} numeroitu, {len(lisatyt)} kategorialinkkiä"
          + (f", {len(poistetut)} poistettu" if poistetut else "")
          + ("  [--kaikki: myös sivut joita ei vielä ole]" if kaikki else ""))


if __name__ == "__main__":
    main(sys.argv[1:])
