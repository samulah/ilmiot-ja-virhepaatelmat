#!/usr/bin/env python3
"""
Louhii Vedätys-pelin siemenaineiston olemassa olevista ilmiösivuista.

KERTAKÄYTTÖINEN APUVÄLINE, ei ylläpidettävä build-skripti. Tarkoitus on antaa
pelipankin kirjoittajalle (ihminen tai LLM) kaikki se, mitä sivustolla jo
sanotaan yhdestä ilmiöstä — jotta pelin repliikit kirjoitetaan sivuston omalla
äänellä eikä tyhjästä.

Poimii jokaisesta pyydetystä ilmiöstä:
  · nimi, numero, kategoria, väri, yhden lauseen määritelmä (index.html)
  · ingressi — ensimmäinen luokaton <p> p.ilmio-byline:n jälkeen (139/139 osuu)
  · "Mikä on X suomeksi?" -vastauslohko, jos sivulla sellainen on (34/139)
  · "Tunnistaminen ja vastakeinot" -osio (117/139) — tämä on pelin
    paljastusruudun "miksi se toimii" ja "mitä sanot" -raaka-aine
  · <li><strong>Alalaji:</strong> selitys</li> -listat — valmiita
    monivalintavaihtoehtoja
  · lainausmerkeissä olevat repliikit — pelin tärkein raaka-aine, koska ne ovat
    ainoita valmiita "näin se kuulostaa" -katkelmia koko sivustolla
  · liittyvät ilmiöt — harhauttajaehdokkaat, jotka ovat oikeasti lähellä

Mermaid-kaavioiden solmutekstit pudotetaan pois: ne ovat myös lainausmerkeissä
mutta ovat kaaviolabeleita, eivät repliikkejä (tunnistaa \n-merkkijonosta).

    python3 scripts/build_peli_siemen.py            # kaikki 27 vaihe 1 -ilmiötä
    python3 scripts/build_peli_siemen.py darvo gaslighting
"""
import html
import json
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).parent.parent
SIEMEN = ROOT / "pelidata" / "_siemen"

# Vaihe 1: 27 vuorovaikutusilmiötä — ne joissa joku puhuu sinulle ja joissa
# "miten reagoit" on mielekäs kysymys. Ryhmä (a1) sisältökartoituksesta.
VAIHE1 = [
    "darvo", "gaslighting", "whataboutismi", "maalitolppien-siirtaminen",
    "argumenttitulva", "omenoita-appelsiineja", "strateginen-osaamattomuus",
    "hiljainen-irtisanominen", "foot-in-the-door", "door-in-the-face",
    "painostusclose", "hintaankkurointi", "vastavuoroisuuden-ansa",
    "lowball-hinnoittelu", "ilmainen-naytetyo", "exposure-maksu",
    "tilipuristus", "bait-and-switch", "sosiaalinen-todiste", "pig-butchering",
    "toimitusjohtajahuijaus", "aaniklooni-huijaus", "ennakkomaksuhuijaus",
    "smishing", "badger-game", "honeypot-huijaus", "simple-sabotage",
]

# Vastakeino-osion otsikko vaihtelee 22 sivulla ("Vastakeinot — velanmaksu
# käytännössä:", "Varoitusmerkit:" jne.), joten tunnistus tehdään alkuosalla.
VASTAKEINO_RE = re.compile(
    r"^(Tunnistaminen|Vastakeino|Vastatoime|Torjunta|Varoitusmerkit|Suojaudu)",
    re.I,
)


def kortit() -> dict:
    """slug → {nro, nimi, kuvaus, vari} etusivun a.hub-kortti-elementeistä."""
    s = (ROOT / "index.html").read_text(encoding="utf-8")
    ulos = {}
    for href, vari, body in re.findall(
        r'<a\s+href="([^"]+)"\s+class="hub-kortti"\s+style="--c:([^"]+)"\s*>(.*?)</a>',
        s, re.S,
    ):
        def kentta(luokka):
            m = re.search(r'class="%s">(.*?)</span>' % luokka, body, re.S)
            return html.unescape(m.group(1)).strip() if m else ""
        ulos[href[:-5]] = {
            "nro": int(kentta("hub-numero")),
            "nimi": kentta("hub-nimi"),
            "kuvaus": kentta("hub-kuvaus"),
            "vari": vari,
        }
    return ulos


def puhdista(t: str) -> str:
    return re.sub(r"\s+", " ", t).strip()


def louhi(slug: str, kortti: dict) -> dict:
    sivu = ROOT / f"{slug}.html"
    soup = BeautifulSoup(sivu.read_text(encoding="utf-8"), "html.parser")
    il = soup.find(class_="ilmio")

    # Mermaid pois ennen kaikkea muuta: sen labelit ovat lainausmerkeissä ja
    # menisivät muuten repliikkeihin.
    for m in il.select(".mermaid"):
        m.decompose()

    # Ingressi: ensimmäinen luokaton <p> bylinen jälkeen.
    ingressi = ""
    byline = il.find("p", class_="ilmio-byline")
    if byline:
        for p in byline.find_next_siblings("p"):
            if not p.get("class"):
                ingressi = puhdista(p.get_text(" "))
                break

    # Laatikot otsikoittain: h2.laatikko-otsikko + sitä seuraava sisältö.
    laatikot, vastakeinot, vastauslohko = [], "", ""
    for otsikko in il.select("h2.laatikko-otsikko"):
        laatikko = otsikko.parent
        teksti = puhdista(laatikko.get_text(" ").replace(otsikko.get_text(), "", 1))
        nimi = puhdista(otsikko.get_text())
        laatikot.append({"otsikko": nimi, "teksti": teksti})
        if VASTAKEINO_RE.match(nimi):
            vastakeinot = teksti
        if "vastauslohko" in (laatikko.get("class") or []):
            vastauslohko = teksti

    # <li><strong>Alalaji:</strong> selitys</li> — valmiita vaihtoehtoja.
    listat = []
    for li in il.select("li"):
        vahva = li.find("strong")
        if vahva:
            listat.append({
                "nimi": puhdista(vahva.get_text()).rstrip(":"),
                "selitys": puhdista(li.get_text(" ").replace(vahva.get_text(), "", 1)),
            })

    # Repliikit. Suodatus: liian lyhyet ovat lainattuja termejä ("sertifikaatti"),
    # ei repliikkejä. Alaraja 12 merkkiä pudottaa valtaosan niistä.
    teksti = html.unescape(il.get_text(" "))
    repliikit = []
    for r in re.findall(r'[”"„]([^”"„\n]{12,160})[”"]', teksti):
        r = puhdista(r)
        if r and "\\n" not in r and r not in repliikit:
            repliikit.append(r)

    # Liittyvät ilmiöt: harhauttajaehdokkaat, jotka ovat oikeasti lähellä.
    liittyvat = []
    aside = soup.find("aside", class_="liittyvat")
    if aside:
        for a in aside.select("a[href$='.html']"):
            liittyvat.append(a["href"][:-5])

    # Kategoria JSON-LD:n articleSection-kentästä (139/139 sivulla).
    kategoria = ""
    for tag in soup.find_all("script", type="application/ld+json"):
        m = re.search(r'"articleSection"\s*:\s*"([^"]+)"', tag.string or "")
        if m:
            kategoria = m.group(1)
            break

    return {
        "slug": slug, **kortti, "kategoria": kategoria,
        "ingressi": ingressi, "vastauslohko": vastauslohko,
        "vastakeinot": vastakeinot, "laatikot": laatikot,
        "listat": listat, "repliikit": repliikit, "liittyvat": liittyvat,
    }


def kirjoita_md(d: dict) -> str:
    r = [f"# {d['nimi']}  (ilmiö {d['nro']}, {d['kategoria']})", ""]
    r += [f"**Slug:** `{d['slug']}` · **Väri:** `{d['vari']}`", ""]
    r += ["## Yhden lauseen määritelmä", "", d["kuvaus"], ""]
    r += ["## Ingressi", "", d["ingressi"], ""]
    if d["vastauslohko"]:
        r += ["## Vastauslohko", "", d["vastauslohko"], ""]
    if d["vastakeinot"]:
        r += ["## Tunnistaminen ja vastakeinot", "", d["vastakeinot"], ""]
    if d["listat"]:
        r += ["## Nimetyt alalajit (monivalinnan raaka-ainetta)", ""]
        r += [f"- **{x['nimi']}** — {x['selitys']}" for x in d["listat"]] + [""]
    if d["repliikit"]:
        r += [f"## Repliikit sivulla ({len(d['repliikit'])} kpl)", ""]
        r += [f"- “{x}”" for x in d["repliikit"]] + [""]
    if d["laatikot"]:
        r += ["## Muut laatikot", ""]
        for x in d["laatikot"]:
            if not VASTAKEINO_RE.match(x["otsikko"]):
                r += [f"### {x['otsikko']}", "", x["teksti"], ""]
    r += ["## Liittyvät ilmiöt (harhauttajaehdokkaat)", ""]
    r += [f"- `{x}`" for x in d["liittyvat"]] + [""]
    return "\n".join(r)


def main() -> None:
    slugit = sys.argv[1:] or VAIHE1
    K = kortit()
    SIEMEN.mkdir(parents=True, exist_ok=True)
    kaikki = []
    for slug in slugit:
        if slug not in K:
            sys.exit(f"VIRHE: {slug} ei ole etusivun korttilistalla")
        if not (ROOT / f"{slug}.html").exists():
            sys.exit(f"VIRHE: {slug}.html puuttuu")
        d = louhi(slug, K[slug])
        (SIEMEN / f"{slug}.md").write_text(kirjoita_md(d), encoding="utf-8")
        kaikki.append(d)
        print(f"  {slug:28} repliikkejä {len(d['repliikit']):3}  "
              f"alalajeja {len(d['listat']):3}  "
              f"vastakeinot {'on ' if d['vastakeinot'] else 'EI '}")
    (SIEMEN / "_kaikki.json").write_text(
        json.dumps(kaikki, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n{len(kaikki)} siementiedostoa → {SIEMEN.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
