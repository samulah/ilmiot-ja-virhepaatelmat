#!/usr/bin/env python3
"""Etusivun "Uusimmat ilmiöt" -lohko: kaksi viimeisintä julkaisuerää rinnakkain.

Miksi erinä eikä listana: sivut julkaistaan erissä (2.11.2026 kymmenen,
3.10.2026 26 sivua kerralla). "Kuusi uusinta" olisi lähes aina yhden erän
sisältä ja erän sisäinen järjestys sattumaa. Erä kertoo lukijalle, mitä uutta
tuli — ja uusi aihepiiri nimetään ääneen.

Miksi staattinen eikä yöajosta (data/suosio.js): lista muuttuu vain
julkaisussa, ei yöllä. Staattinen HTML näkyy ilman JavaScriptiä, ei piiloudu
suosiodatan tuoreustarkistukseen ja antaa Googlelle etusivulta linkin uusiin
sivuihin heti julkaisun jälkeen.

Lähteet:
  index.html:n .hub-kategoria-lohkot  → slug, numero, nimi, väri, aihepiiri
  sivun JSON-LD datePublished          → erä

Säännöt:
  - EI luokkaa hub-kortti (haku ja randomIlmio() keräävät ne; duplikaatti).
  - Lohko on UUSIMMAT-ALKU/-LOPPU-merkkien välissä: CSS headissa, HTML
    peli-noston ja aihepiirinavin välissä. Ei NOSTOT-lohkon sisällä, koska
    paivita_suosio.py pyyhkii sen joka injektiossa.
  - Idempotentti: aiempi injektio poistetaan ensin.

Ajo:  python3 scripts/build_uusimmat.py              # kuivaharjoitus
      python3 scripts/build_uusimmat.py --kirjoita
"""
import argparse
import html
import re
import sys
from collections import OrderedDict, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"

ERIA = 2            # montako viimeisintä erää näytetään
NOSTOJA = 4         # montako ilmiötä erää kohden

KATEGORIA_RE = re.compile(
    r'<div class="hub-kategoria" id="([^"]+)">\s*'
    r'<h2 class="hub-kat-label"><span class="hub-kat-nro">\d+</span>([^<]+)<span'
    r'.*?<a class="hub-kat-linkki" href="([^"]+)"'
    r'(.*?)</div>\s*</div>', re.S)
KORTTI_RE = re.compile(
    r'<a href="([a-z0-9-]+\.html)" class="hub-kortti" style="--c:(#[0-9a-fA-F]{6})">\s*'
    r'<span class="hub-numero">(\d+)</span>.*?<span class="hub-nimi">([^<]+)</span>', re.S)
JULKAISU_RE = re.compile(r'"datePublished":\s*"(\d{4}-\d{2}-\d{2})"')


def lue_kortit(teksti):
    kategoriat, kortit = [], []
    for kat_id, kat_nimi, kat_href, sisus in KATEGORIA_RE.findall(teksti):
        kat = {"id": kat_id, "nimi": html.unescape(kat_nimi.strip()), "href": kat_href, "koko": 0}
        for href, vari, nro, nimi in KORTTI_RE.findall(sisus):
            kortit.append({"href": href, "vari": vari, "nro": int(nro),
                           "nimi": html.unescape(nimi.strip()), "kat": kat})
            kat["koko"] += 1
        kategoriat.append(kat)
    maara = teksti.count('class="hub-kortti"')
    assert len(kortit) == maara, f"kortteja jäsennettiin {len(kortit)}, sivulla {maara}"
    return kategoriat, kortit


def julkaisupaiva(href):
    polku = ROOT / href
    assert polku.exists(), f"kortin sivu puuttuu: {href}"
    osuma = JULKAISU_RE.search(polku.read_text(encoding="utf-8"))
    assert osuma, f"{href}: JSON-LD:stä puuttuu datePublished"
    return osuma.group(1)


def valitse_nostot(kortit):
    """Vuorotellen aihepiireittäin, jotta sekaerän pieni aihepiiri ei huku isoon.

    Aihepiirijärjestys: pienin osuus ensin (yksittäinen uusi sivu vanhassa
    aihepiirissä on erän helpoimmin ohitettava), sitten sivun järjestys.
    """
    ryhmat = OrderedDict()
    for k in sorted(kortit, key=lambda k: k["nro"]):
        ryhmat.setdefault(k["kat"]["id"], []).append(k)
    jonot = sorted(ryhmat.values(), key=lambda r: (len(r), r[0]["nro"]))
    valitut = []
    while len(valitut) < NOSTOJA and any(jonot):
        for jono in jonot:
            if jono and len(valitut) < NOSTOJA:
                valitut.append(jono.pop(0))
    return sorted(valitut, key=lambda k: k["nro"])


def pvm_fi(iso):
    v, k, p = iso.split("-")
    return f"{int(p)}.{int(k)}.{v}"


def era_html(paiva, kortit):
    e = html.escape
    n = len(kortit)
    per_kat = defaultdict(int)
    for k in kortit:
        per_kat[k["kat"]["id"]] += 1
    kat_by_id = {k["kat"]["id"]: k["kat"] for k in kortit}
    # Uusi aihepiiri = erä toi aihepiirin jokaisen ilmiön
    uudet = [kat_by_id[i] for i in per_kat if per_kat[i] == kat_by_id[i]["koko"]]
    uudet.sort(key=lambda kat: min(k["nro"] for k in kortit if k["kat"] is kat))

    saate = f'{n} {"uusi ilmiö" if n == 1 else "uutta ilmiötä"}'
    if uudet:
        linkit = ", ".join(f'<a href="{e(kat["href"])}">{e(kat["nimi"])}</a>' for kat in uudet)
        saate += f' · {"uusi aihepiiri" if len(uudet) == 1 else "uudet aihepiirit"} {linkit}'

    rivit = []
    for k in valitse_nostot(kortit):
        rivit.append(
            f'      <li><a href="{e(k["href"])}" style="--c:{k["vari"]}">'
            f'<span class="uusimmat-nimi">{e(k["nimi"])}</span>'
            f'<span class="uusimmat-kat">{e(k["kat"]["nimi"])}</span></a></li>')
    loput = n - len(rivit)
    lisaa = (f'\n    <p class="uusimmat-lisaa"><a href="muutokset.html">+{loput} muuta '
             f'&rarr;</a></p>') if loput > 0 else ""

    return (f'  <article class="uusimmat-era">\n'
            f'    <h3 class="uusimmat-pvm"><time datetime="{paiva}">{pvm_fi(paiva)}</time></h3>\n'
            f'    <p class="uusimmat-saate">{saate}</p>\n'
            f'    <ul class="uusimmat-lista">\n' + "\n".join(rivit) + '\n    </ul>'
            f'{lisaa}\n  </article>')


UUSIMMAT_CSS = """<!-- UUSIMMAT-ALKU --><style>
/* Uusimmat ilmiöt — scripts/build_uusimmat.py injektoi, älä muokkaa käsin. */
.uusimmat { max-width: 1100px; margin: 0 auto 1.8rem; }
.uusimmat-otsikko {
  font-family: 'Spectral', Georgia, serif; font-size: 1.15em; font-weight: 600;
  color: var(--c-primary-dark); margin: 0 0 0.6rem;
}
.uusimmat-erat { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; }
.uusimmat-era { background: #fff; border: 1px solid #E8DFC8; border-radius: 8px; padding: 0.85rem 1rem 0.7rem; }
.uusimmat-pvm { font-size: 0.78em; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase;
  color: var(--c-primary-mid); margin: 0; }
.uusimmat-saate { font-size: 0.86em; color: #5a4a20; margin: 0.15rem 0 0.5rem; line-height: 1.45; }
.uusimmat-saate a { color: var(--c-primary-mid); font-weight: 600; }
.uusimmat-lista { list-style: none; margin: 0; padding: 0; }
.uusimmat-lista a {
  display: flex; justify-content: space-between; align-items: baseline; gap: 0.8rem;
  padding: 0.42rem 0 0.42rem 0.65rem; border-left: 3px solid var(--c, var(--c-primary));
  margin: 0.2rem 0; text-decoration: none; color: inherit; transition: background 0.15s;
}
.uusimmat-lista a:hover { background: #FBF3DC; }
.uusimmat-nimi { font-weight: 600; color: var(--c-primary-dark); }
.uusimmat-kat { font-size: 0.78em; color: #8a7a50; text-align: right; flex-shrink: 0; max-width: 45%; }
.uusimmat-lisaa { margin: 0.45rem 0 0; font-size: 0.85em; }
.uusimmat-lisaa a { color: var(--c-primary-mid); font-weight: 600; text-decoration: none; }
@media (max-width: 600px) {
  .uusimmat-erat { grid-template-columns: 1fr; gap: 0.7rem; }
  .uusimmat-kat { display: none; }
}
@media (prefers-reduced-motion: reduce) { .uusimmat-lista a { transition: none; } }
</style><!-- UUSIMMAT-LOPPU -->"""


def rakenna(teksti):
    _, kortit = lue_kortit(teksti)
    erat = defaultdict(list)
    for k in kortit:
        erat[julkaisupaiva(k["href"])].append(k)
    paivat = sorted(erat, reverse=True)[:ERIA]
    lohko = ('<!-- UUSIMMAT-ALKU — scripts/build_uusimmat.py, älä muokkaa käsin -->\n'
             '<section class="uusimmat" aria-labelledby="uusimmat-otsikko">\n'
             '  <h2 class="uusimmat-otsikko" id="uusimmat-otsikko">Uusimmat ilmiöt</h2>\n'
             '  <div class="uusimmat-erat">\n'
             + "\n".join(era_html(p, erat[p]) for p in paivat) +
             '\n  </div>\n</section>\n<!-- UUSIMMAT-LOPPU -->')
    return lohko, [(p, len(erat[p])) for p in paivat]


def poista(teksti):
    return re.sub(r"\n?<!-- UUSIMMAT-ALKU.*?UUSIMMAT-LOPPU -->", "", teksti, flags=re.S)


def injektoi(teksti, lohko):
    teksti = poista(teksti)
    assert teksti.count("</head>") == 1
    teksti = teksti.replace("</head>", UUSIMMAT_CSS + "\n</head>", 1)
    ankkuri = '\n<nav class="hub-katnav"'
    assert teksti.count(ankkuri) == 1, "aihepiirinavin alku ei osu"
    return teksti.replace(ankkuri, "\n" + lohko + ankkuri, 1)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--kirjoita", action="store_true", help="kirjoita index.html")
    args = ap.parse_args()

    vanha = INDEX.read_text(encoding="utf-8")
    lohko, erat = rakenna(vanha)
    uusi = injektoi(vanha, lohko)
    for p, n in erat:
        print(f"  erä {pvm_fi(p)}: {n} ilmiötä")
    if uusi == vanha:
        print("  index.html: ei muutoksia")
    elif args.kirjoita:
        INDEX.write_text(uusi, encoding="utf-8")
        print("  index.html: Uusimmat-lohko päivitetty")
    else:
        print("  index.html muuttuisi — aja --kirjoita-lipulla")
    return 0


if __name__ == "__main__":
    sys.exit(main())
