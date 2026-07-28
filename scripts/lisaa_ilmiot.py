#!/usr/bin/env python3
"""Julkaisee luonnoskansiossa olevat ilmiöt sivustolle ja numeroi kaikki uudelleen.

Peilikuva poista_ilmio.py:lle. Ilmiönumero esiintyy neljässä paikassa; tämä
hoitaa kaikki:

  index.html      <span class="hub-numero">N</span>
  <sivu>.html     <div class="ilmio-tag">Ilmiö N</div>
  <sivu>.html     <span class="kortti-nav-laskuri">N / YHT</span>
  <sivu>.html     <span class="liittyvat-numero">N</span>  (build_liittyvat.py)

Lisäksi:
  - siirtää luonnokset juureen: noindex pois, ../-etuliitteet riisutaan
  - lisää hub-kortin index.html:ään oikean kategorian sisään
  - rakentaa jokaisen sivun const IDS -taulukon uudelleen korttijärjestykseen
  - kytkee PREV/NEXT-ketjun ja selausnapit uudelleen niiltä osin kuin ne muuttuvat

Ei aja regenerointiskriptejä itse — tulostaa lopuksi ajojärjestyksen.

Ajo:
    python3 scripts/lisaa_ilmiot.py                # kuivaharjoitus
    python3 scripts/lisaa_ilmiot.py --kirjoita
"""
import argparse
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LUONNOKSET = ROOT / "luonnokset-klusterit"

# Uudet ilmiöt: slug → (sijoita tämän kortin JÄLKEEN, väri, nimi, kuvaus).
# Sijoituspaikka määrää sekä kategorian että numeron — kortti menee ankkurin
# perään samaan hub-kategoria-lohkoon.
UUDET = {
    "klikkiotsikko": ("rage-bait", "#ef6c00", "Klikkiotsikko",
        "Otsikko on rakennettu tuottamaan klikki, ei kertomaan mitä juttu sisältää — tieto pidätetään tahallaan."),
    "engagement-bait": ("klikkiotsikko", "#5d4037", "Engagement bait",
        "Sisältö pyytää reaktiota suoraan, koska algoritmi palkitsee vuorovaikutuksesta riippumatta sen syystä."),
    "sinipesu": ("viherpesu", "#1565c0", "Sinipesu",
        "Vapaaehtoiseen sitoumukseen liittyminen tuottaa vastuullisen maineen ilman valvontaa tai sanktioita."),
    "urheilupesu": ("sinipesu", "#00838f", "Urheilupesu",
        "Maineongelmasta kärsivä ostaa urheilusta myönteistä huomiota — media siirtyy raportoimaan otteluista."),
    "pinkkipesu": ("urheilupesu", "#d81b60", "Pinkkipesu",
        "Sateenkaari tai pinkki nauha ilmestyy logoon kampanjakuukaudeksi ja katoaa sen päätyttyä."),
}

KORTTI_RE = re.compile(
    r'\n<a href="([a-z0-9-]+)\.html" class="hub-kortti"[^>]*>\s*'
    r'<span class="hub-numero">(\d+)</span>.*?\n</a>', re.S)


class Muutokset:
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
        alkuperaiset = {p: (p.read_text(encoding="utf-8") if p.exists() else None)
                        for p in self.puskuri}
        muuttuneet = [p for p, t in self.puskuri.items() if t != alkuperaiset[p]]
        if self.kirjoita:
            for p in muuttuneet:
                p.write_text(self.puskuri[p], encoding="utf-8")
        return muuttuneet


def lue_kortit(html):
    return [(m.group(1), int(m.group(2)), m.group(0), m.start(), m.end())
            for m in KORTTI_RE.finditer(html)]


def sivun_h1(teksti):
    m = re.search(r"<h1>(.*?)</h1>", teksti, re.S)
    assert m, "ei H1:tä"
    return m.group(1).strip()


def kortti_html(slug, vari, nimi, kuvaus, numero):
    return (f'\n<a href="{slug}.html" class="hub-kortti" style="--c:{vari}">\n'
            f'  <span class="hub-numero">{numero}</span>\n'
            f'  <span class="hub-teksti">\n'
            f'    <span class="hub-nimi">{nimi}</span>\n'
            f'    <span class="hub-kuvaus">{kuvaus}</span>\n'
            f'  </span>\n'
            f'  <span class="hub-nuoli" aria-hidden="true">›</span>\n'
            f'</a>')


def juurisivuksi(teksti):
    """Luonnos → juuren sivu: noindex pois, ../-etuliitteet riisutaan."""
    teksti = re.sub(
        r'\s*<meta name="robots" content="noindex"><!-- POISTA-JULKAISTAESSA -->', "", teksti)
    teksti = teksti.replace('href="../', 'href="').replace('src="../', 'src="')
    teksti = teksti.replace("'../js/mermaid.min.js'", "'js/mermaid.min.js'")
    teksti = teksti.replace("window.location.href = '../' + id + '.html';",
                            "window.location.href = id + '.html';")
    teksti = teksti.replace("naytaSiirtyma('Satunnainen ilmiö', '../' + id + '.html');",
                            "naytaSiirtyma('Satunnainen ilmiö', id + '.html');")
    teksti = teksti.replace(
        "'<img class=\"random-siirtyma-logo\" src=\"../favicon.svg\" alt=\"\">'",
        "'<img class=\"random-siirtyma-logo\" src=\"favicon.svg\" alt=\"\">'")
    # PREV/NEXT osoittivat luonnoskansiosta juureen; ketju kirjoitetaan
    # myöhemmin uusiksi, mutta polku suoristetaan jo tässä
    teksti = re.sub(r"(const (?:PREV|NEXT) = ')\.\./", r"\1", teksti)
    assert "noindex" not in teksti, "noindex jäi jäljelle"
    assert "../" not in teksti, "../-polku jäi jäljelle"
    return teksti


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kirjoita", action="store_true")
    args = ap.parse_args()

    M = Muutokset(args.kirjoita)
    index = ROOT / "index.html"
    html = M.lue(index)

    kortit = lue_kortit(html)
    vanha_jarjestys = [k[0] for k in kortit]
    vanhat_numerot = {k[0]: k[1] for k in kortit}
    vanha_yht = len(kortit)
    uusi_yht = vanha_yht + len(UUDET)

    for slug, (ankkuri, *_) in UUDET.items():
        assert (LUONNOKSET / f"{slug}.html").exists(), f"luonnos {slug}.html puuttuu"
        assert not (ROOT / f"{slug}.html").exists(), f"{slug}.html on jo juuressa"
        assert slug not in vanhat_numerot, f"{slug} on jo index.html:ssä"
        assert ankkuri in vanhat_numerot or ankkuri in UUDET, \
            f"{slug}: ankkuria {ankkuri} ei ole"

    # ── 1. uusi järjestys: kortti ankkurinsa perään ───────────────────
    uusi_jarjestys = list(vanha_jarjestys)
    lisaamatta = dict(UUDET)
    while lisaamatta:
        eteni = False
        for slug, (ankkuri, *_) in list(lisaamatta.items()):
            if ankkuri in uusi_jarjestys:
                uusi_jarjestys.insert(uusi_jarjestys.index(ankkuri) + 1, slug)
                del lisaamatta[slug]
                eteni = True
        assert eteni, f"ankkuriketju ei ratkea: {list(lisaamatta)}"
    assert len(uusi_jarjestys) == uusi_yht
    uudet_numerot = {s: i for i, s in enumerate(uusi_jarjestys, 1)}

    # ── 2. index.html: kortit uuteen järjestykseen ────────────────────
    kortti_lahde = {k[0]: k[2] for k in kortit}
    for slug, (_, vari, nimi, kuvaus) in UUDET.items():
        kortti_lahde[slug] = kortti_html(slug, vari, nimi, kuvaus, 0)

    palat, edellinen = [], 0
    for s, _, vanha_kortti, alku, loppu in kortit:
        palat.append(html[edellinen:alku])
        palat.append(re.sub(r'(<span class="hub-numero">)\d+(</span>)',
                            rf"\g<1>{uudet_numerot[s]}\g<2>", vanha_kortti, count=1))
        # ankkurin perään kuuluvat uudet kortit, oikeassa keskinäisessä
        # järjestyksessä (uusi_jarjestys ratkaisee)
        for uusi in uusi_jarjestys[uudet_numerot[s]:]:
            if uusi not in UUDET:
                break
            palat.append(re.sub(r'(<span class="hub-numero">)\d+(</span>)',
                                rf"\g<1>{uudet_numerot[uusi]}\g<2>",
                                kortti_lahde[uusi], count=1))
        edellinen = loppu
    palat.append(html[edellinen:])
    uusi_index = "".join(palat)

    tarkista = lue_kortit(uusi_index)
    assert [k[0] for k in tarkista] == uusi_jarjestys, "index: korttijärjestys ei täsmää"
    assert [k[1] for k in tarkista] == list(range(1, uusi_yht + 1)), \
        "index: numerointi ei ole 1..N"

    siirtyneet = sum(1 for s in vanha_jarjestys
                     if uudet_numerot[s] != vanhat_numerot[s])
    M.aseta(index, uusi_index,
            f"{len(UUDET)} korttia lisätty, {siirtyneet} uudelleennumeroitu, "
            f"{vanha_yht} → {uusi_yht} ilmiötä")

    # ── 3. luonnokset juureen (puskuriin; tiedostosiirto vasta lopuksi) ─
    for slug in UUDET:
        M.puskuri[ROOT / f"{slug}.html"] = juurisivuksi(
            (LUONNOKSET / f"{slug}.html").read_text(encoding="utf-8"))
        M.loki.append(f"{slug}.html: luonnos → juuri (noindex pois, polut suoristettu)")

    # ── 4. jokainen ilmiösivu ─────────────────────────────────────────
    ids_js = "const IDS = [" + ", ".join(f'"{s}"' for s in uusi_jarjestys) + "];"
    naapurit = {s: (uusi_jarjestys[i - 1] if i else None,
                    uusi_jarjestys[i + 1] if i + 1 < uusi_yht else None)
                for i, s in enumerate(uusi_jarjestys)}
    otsikot = {s: sivun_h1(M.lue(ROOT / f"{s}.html")) for s in uusi_jarjestys}

    for s in uusi_jarjestys:
        polku = ROOT / f"{s}.html"
        teksti = M.puskuri[polku]
        alku = teksti
        n = uudet_numerot[s]
        syyt = []

        teksti, k = re.subn(r'(<div class="ilmio-tag">Ilmiö )\d+(</div>)',
                            rf"\g<1>{n}\g<2>", teksti, count=1)
        assert k == 1, f"{polku.name}: ilmio-tagia ei löytynyt"

        teksti, k = re.subn(r'(<span class="kortti-nav-laskuri">)\s*\d+ / \d+(</span>)',
                            rf"\g<1>{n} / {uusi_yht}\g<2>", teksti, count=1)
        assert k == 1, f"{polku.name}: kortti-nav-laskuria ei löytynyt"
        if teksti != alku:
            syyt.append(f"numero → {n} / {uusi_yht}")

        ennen_ids = teksti
        teksti, k = re.subn(r"const IDS = \[.*?\];", lambda m: ids_js, teksti,
                            count=1, flags=re.S)
        assert k == 1, f"{polku.name}: const IDS -taulukkoa ei löytynyt"
        if teksti != ennen_ids:
            syyt.append("IDS")

        edell, seur = naapurit[s]
        for vakio, kohde in (("PREV", edell), ("NEXT", seur)):
            uusi_arvo = f"{kohde}.html" if kohde else ""
            teksti, k = re.subn(rf"const {vakio} = '[^']*';",
                                f"const {vakio} = '{uusi_arvo}';", teksti, count=1)
            assert k == 1, f"{polku.name}: const {vakio} puuttuu"

        def paivita_nav(m):
            lohko = m.group(0)
            paikat = list(re.finditer(
                r'<a class="kortti-nav-btn"[^>]*>.*?</a>'
                r'|<span class="kortti-nav-btn disabled">.*?</span>', lohko, re.S))
            assert len(paikat) == 2, f"{polku.name}: navissa {len(paikat)} nappia"
            for paikka, kohde, muoto in ((paikat[0], edell, "← {}"),
                                         (paikat[1], seur, "{} →")):
                if kohde is None:
                    uusi_nappi = ('<span class="kortti-nav-btn disabled">'
                                  f'{"←" if muoto.startswith("←") else "→"}</span>')
                else:
                    uusi_nappi = (f'<a class="kortti-nav-btn" href="{kohde}.html">'
                                  f'{muoto.format(otsikot[kohde])}</a>')
                # kosketaan vain jos kohde tosiasiassa muuttuu — muuten
                # napin oma muotoilu (<em> ym.) säilyy
                if kohde is not None and f'href="{kohde}.html"' in paikka.group(0):
                    continue
                lohko = lohko.replace(paikka.group(0), uusi_nappi, 1)
            return lohko

        ennen_nav = teksti
        teksti, k = re.subn(r'<nav class="kortti-nav">.*?</nav>', paivita_nav,
                            teksti, count=1, flags=re.S)
        assert k == 1, f"{polku.name}: kortti-nav-lohkoa ei löytynyt"
        if teksti != ennen_nav:
            syyt.append("selausnappi")

        if teksti != alku:
            M.aseta(polku, teksti, ", ".join(syyt) or "päivitetty")

    # ── raportti ──────────────────────────────────────────────────────
    muuttuneet = M.tallenna()
    tila = "KIRJOITETTU" if args.kirjoita else "KUIVAHARJOITUS — mitään ei kirjoitettu"
    print(f"\n{tila}\n")
    for rivi in M.loki[:12]:
        print("  " + rivi)
    if len(M.loki) > 12:
        print(f"  … ja {len(M.loki) - 12} muuta")
    print(f"\n  {len(muuttuneet)} tiedostoa, {vanha_yht} → {uusi_yht} ilmiötä")
    print("  uudet numerot: " + ", ".join(
        f"{s} {uudet_numerot[s]}" for s in UUDET))
    print(f"  uudelleennumeroituja vanhoja sivuja: {siirtyneet}"
          f" (pienin muuttunut numero {min((uudet_numerot[s] for s in vanha_jarjestys if uudet_numerot[s] != vanhat_numerot[s]), default=0)})")

    if args.kirjoita:
        for slug in UUDET:
            (LUONNOKSET / f"{slug}.html").unlink()
        if not any(LUONNOKSET.iterdir()):
            LUONNOKSET.rmdir()
        print("\n  luonnokset-klusterit/ tyhjennetty")
        print("\n  Aja seuraavaksi:")
        for k in ("build_kategoriat.py", "paivita_maarat.py", "build_liittyvat.py",
                  "build_sitemap.py", "build_search_index.py"):
            print(f"    python3 scripts/{k}")
    else:
        print("\n  Aja uudelleen --kirjoita-lipulla kun tarkistus on tehty.")


if __name__ == "__main__":
    main()
