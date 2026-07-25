#!/usr/bin/env python3
"""Poistaa yhden ilmiön sivustolta ja numeroi loput uudelleen 1..N.

Ilmiönumero esiintyy neljässä paikassa; tämä hoitaa kaikki:

  index.html      <span class="hub-numero">N</span>        (uudelleennumerointi)
  <sivu>.html     <div class="ilmio-tag">Ilmiö N</div>
  <sivu>.html     <span class="kortti-nav-laskuri">N / YHT</span>
  <sivu>.html     <span class="liittyvat-numero">N</span>  (build_liittyvat.py)

Lisäksi:
  - poistaa kortin index.html:stä
  - poistaa slugin jokaisen sivun const IDS -taulukosta
  - kytkee poistuvan sivun naapurit (PREV/NEXT + kortti-nav-btn) toisiinsa
  - ohjaa sivulle jääneet linkit korvaavaan osoitteeseen (--korvaa)
  - siirtää poistetun sivun arkistoon ja lisää 301-ohjauksen .htaccessiin

Ei aja regenerointiskriptejä itse — tulostaa lopuksi ajojärjestyksen.

Ajo:
    python3 scripts/poista_ilmio.py tilastoilla-valehtelu \\
        --korvaa kategoria-tilastoilla-valehtelu.html          # kuivaharjoitus
    python3 scripts/poista_ilmio.py tilastoilla-valehtelu \\
        --korvaa kategoria-tilastoilla-valehtelu.html --kirjoita
"""
import argparse
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARKISTO = ROOT / "poistetut"

KORTTI_RE = re.compile(
    r'\n<a href="([a-z0-9-]+)\.html" class="hub-kortti"[^>]*>\s*'
    r'<span class="hub-numero">(\d+)</span>.*?\n</a>', re.S)


class Muutokset:
    """Kerää tiedostokohtaiset muutokset ja kirjoittaa ne vasta lopuksi."""

    def __init__(self, kirjoita):
        self.kirjoita = kirjoita
        self.puskuri = {}
        self.loki = []

    def lue(self, polku):
        if polku not in self.puskuri:
            self.puskuri[polku] = polku.read_text(encoding="utf-8")
        return self.puskuri[polku]

    def aseta(self, polku, teksti, kuvaus):
        if self.puskuri.get(polku) != teksti:
            self.puskuri[polku] = teksti
            self.loki.append(f"{polku.relative_to(ROOT)}: {kuvaus}")

    def tallenna(self):
        alkuperaiset = {p: p.read_text(encoding="utf-8") for p in self.puskuri}
        muuttuneet = [p for p, t in self.puskuri.items() if t != alkuperaiset[p]]
        if self.kirjoita:
            for p in muuttuneet:
                p.write_text(self.puskuri[p], encoding="utf-8")
        return muuttuneet


def lue_kortit(html):
    """[(slug, numero, koko kortti-HTML, alku, loppu), ...] esiintymisjärjestyksessä."""
    return [(m.group(1), int(m.group(2)), m.group(0), m.start(), m.end())
            for m in KORTTI_RE.finditer(html)]


def sivun_h1(polku):
    """H1 sisäisine tageineen — selausnapit käyttävät samaa muotoilua (<em>)."""
    m = re.search(r"<h1>(.*?)</h1>", polku.read_text(encoding="utf-8"), re.S)
    assert m, f"{polku.name}: ei H1:tä"
    return m.group(1).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", help="poistettavan ilmiön slug ilman .html-päätettä")
    ap.add_argument("--korvaa", required=True,
                    help="osoite, johon vanhat linkit ja 301 ohjataan")
    ap.add_argument("--kirjoita", action="store_true",
                    help="kirjoita muutokset (ilman tätä vain kuivaharjoitus)")
    args = ap.parse_args()

    slug, korvaava = args.slug, args.korvaa
    poistuva = ROOT / f"{slug}.html"
    assert poistuva.exists(), f"{poistuva} ei ole olemassa"
    if args.kirjoita and not (ROOT / korvaava).exists():
        raise SystemExit(
            f"VIRHE: korvaava sivu {korvaava} ei ole olemassa.\n"
            f"301-ohjaus ja sisäiset linkit osoittaisivat 404:ään. Julkaise se ensin\n"
            f"(python3 scripts/build_kategoriat.py) ja aja tämä vasta sen jälkeen.")

    M = Muutokset(args.kirjoita)
    index = ROOT / "index.html"
    html = M.lue(index)

    kortit = lue_kortit(html)
    slugit = [k[0] for k in kortit]
    assert slug in slugit, f"{slug} ei ole index.html:n korteissa"
    vanha_yht = len(kortit)
    uusi_yht = vanha_yht - 1

    # ── 1. index.html: kortin poisto + uudelleennumerointi ────────────
    jaljelle = [k for k in kortit if k[0] != slug]
    uudet_numerot = {k[0]: i for i, k in enumerate(jaljelle, 1)}
    vanhat_numerot = {k[0]: k[1] for k in kortit}

    palat, edellinen = [], 0
    for s, _, kortti_html, alku, loppu in kortit:
        palat.append(html[edellinen:alku])
        if s != slug:
            palat.append(re.sub(r'(<span class="hub-numero">)\d+(</span>)',
                                rf"\g<1>{uudet_numerot[s]}\g<2>", kortti_html, count=1))
        edellinen = loppu
    palat.append(html[edellinen:])
    uusi_index = "".join(palat)

    # jäljelle jääneet linkit etusivulla (esim. vastakeino-listan leipäteksti)
    uusi_index = uusi_index.replace(f'href="{slug}.html"', f'href="{korvaava}"')

    siirtyneet = sum(1 for s in uudet_numerot if uudet_numerot[s] != vanhat_numerot[s])
    M.aseta(index, uusi_index,
            f"kortti poistettu, {siirtyneet} korttia uudelleennumeroitu, "
            f"{vanha_yht} → {uusi_yht} ilmiötä")

    # ── 2. ilmiösivut ─────────────────────────────────────────────────
    uusi_jarjestys = [k[0] for k in jaljelle]
    naapurit = {s: (uusi_jarjestys[i - 1] if i else None,
                    uusi_jarjestys[i + 1] if i + 1 < uusi_yht else None)
                for i, s in enumerate(uusi_jarjestys)}
    otsikot = {s: sivun_h1(ROOT / f"{s}.html") for s in uusi_jarjestys}

    menetti_linkin = []
    for s in uusi_jarjestys:
        polku = ROOT / f"{s}.html"
        teksti = M.lue(polku)
        alku = teksti
        n = uudet_numerot[s]
        syyt = []

        uusi, k = re.subn(r'(<div class="ilmio-tag">Ilmiö )\d+(</div>)',
                          rf"\g<1>{n}\g<2>", teksti, count=1)
        assert k == 1, f"{polku.name}: ilmio-tagia ei löytynyt"
        if uusi != teksti:
            syyt.append(f"ilmio-tag → {n}")
        teksti = uusi

        uusi, k = re.subn(r'(<span class="kortti-nav-laskuri">)\s*\d+ / \d+(</span>)',
                          rf"\g<1>{n} / {uusi_yht}\g<2>", teksti, count=1)
        assert k == 1, f"{polku.name}: kortti-nav-laskuria ei löytynyt"
        if uusi != teksti:
            syyt.append(f"laskuri → {n} / {uusi_yht}")
        teksti = uusi

        # IDS-taulukko: poistuva slug pois (vain taulukon sisältä)
        def karsi_ids(m):
            return m.group(1) + re.sub(rf'"{re.escape(slug)}", ?|, ?"{re.escape(slug)}"',
                                       "", m.group(2)) + m.group(3)

        uusi, k = re.subn(r"(const IDS = \[)(.*?)(\];)", karsi_ids, teksti, count=1)
        assert k == 1, f"{polku.name}: const IDS -taulukkoa ei löytynyt"
        if uusi != teksti:
            syyt.append("IDS-taulukko")
        teksti = uusi

        # PREV/NEXT ja selausnapit: kosketaan VAIN niihin, jotka osoittivat
        # poistuvaan sivuun. Muiden nappien tekstissä voi olla <em>-muotoilua,
        # jota H1:stä uudelleenrakentaminen hukkaisi.
        edell, seur = naapurit[s]
        for vakio, kohde in (("PREV", edell), ("NEXT", seur)):
            if kohde is None:
                continue
            uusi = teksti.replace(f"const {vakio} = '{slug}.html'",
                                  f"const {vakio} = '{kohde}.html'")
            if uusi != teksti:
                syyt.append(f"{vakio} → {kohde}")
            teksti = uusi

        # Navissa on aina kaksi paikkaa: ensimmäinen edellinen, toinen seuraava.
        # Kumpikin voi olla <a> tai disabloitu <span>.
        def paivita_nav(m):
            lohko = m.group(0)
            paikat = list(re.finditer(
                r'<a class="kortti-nav-btn"[^>]*>.*?</a>'
                r'|<span class="kortti-nav-btn disabled">.*?</span>', lohko, re.S))
            assert len(paikat) == 2, f"{polku.name}: navissa {len(paikat)} nappia"
            for paikka, kohde, muoto in ((paikat[0], edell, "← {}"),
                                         (paikat[1], seur, "{} →")):
                if kohde is None or f'href="{slug}.html"' not in paikka.group(0):
                    continue
                lohko = lohko.replace(
                    paikka.group(0),
                    f'<a class="kortti-nav-btn" href="{kohde}.html">'
                    f'{muoto.format(otsikot[kohde])}</a>', 1)
            return lohko

        uusi, k = re.subn(r'<nav class="kortti-nav">.*?</nav>', paivita_nav,
                          teksti, count=1, flags=re.S)
        assert k == 1, f"{polku.name}: kortti-nav-lohkoa ei löytynyt"
        if uusi != teksti:
            syyt.append("selausnappi")
        teksti = uusi

        # jäljelle jääneet linkit poistuvaan sivuun
        if f'href="{slug}.html"' in teksti:
            aside = re.search(r'<aside class="liittyvat".*?</aside>', teksti, re.S)
            if aside and f'href="{slug}.html"' in aside.group(0):
                menetti_linkin.append(s)
            teksti = teksti.replace(f'href="{slug}.html"', f'href="{korvaava}"')
            syyt.append(f"linkki → {korvaava}")

        if teksti != alku:
            M.aseta(polku, teksti, ", ".join(syyt))

    # ── 3. .htaccess: 301 ─────────────────────────────────────────────
    hta = ROOT / ".htaccess"
    hta_teksti = M.lue(hta)
    ohjaus = (f"# Ilmiö siirretty kategoriasivuksi\n"
              f"RewriteRule ^{slug}\\.html$ /{korvaava} [R=301,L]\n\n")
    if ohjaus not in hta_teksti:
        merkki = "# ── Turvaotsakkeet"
        assert merkki in hta_teksti, ".htaccess: turvaotsakkeiden osiota ei löytynyt"
        M.aseta(hta, hta_teksti.replace(merkki, ohjaus + merkki, 1),
                f"301 /{slug}.html → /{korvaava}")

    # ── raportti ──────────────────────────────────────────────────────
    muuttuneet = M.tallenna()
    tila = "KIRJOITETTU" if args.kirjoita else "KUIVAHARJOITUS — mitään ei kirjoitettu"
    print(f"\n{tila}\n")
    for rivi in M.loki:
        print("  " + rivi)
    print(f"\n  {len(muuttuneet)} tiedostoa, {vanha_yht} → {uusi_yht} ilmiötä")

    if menetti_linkin:
        print("\n  Liittyvät ilmiöt -lohkossa oleva linkki ohjattiin kategoriasivulle "
              f"({len(menetti_linkin)} sivua):")
        print("    " + ", ".join(menetti_linkin))
        print("  → build_liittyvat.py osaa renderöidä kategoriakortin.")

    if args.kirjoita:
        ARKISTO.mkdir(exist_ok=True)
        shutil.move(str(poistuva), str(ARKISTO / poistuva.name))
        print(f"\n  {poistuva.name} → poistetut/{poistuva.name}")
        print("\n  Aja seuraavaksi:")
        for k in ("paivita_maarat.py", "build_liittyvat.py",
                  "build_sitemap.py", "build_search_index.py"):
            print(f"    python3 scripts/{k}")
    else:
        print(f"\n  Aja uudelleen --kirjoita-lipulla kun tarkistus on tehty.")


if __name__ == "__main__":
    main()
