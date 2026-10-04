#!/usr/bin/env python3
"""Siivoaa ilmiösivujen JSON-LD:n vastaamaan sivua.

Tausta: SEO-auditointi 4.10.2026 (ACTION-PLAN.md kohta 13). Jokainen kenttä
johdetaan lähteestä, joka on jo sivulla tai etusivun kortissa, joten skripti
voidaan ajaa uudelleen aina kun metakuvaus, kortin nimi tai jakokuva muuttuu.

Article-solmu:
  description   ← <meta name="description"> (115 sivulla vanhentunut, 59
                  katkennut "…"-merkkiin)
  image.url     ← og:image (sivukohtainen jakokuva, jos build_og.py on tehnyt)
  isPartOf      → WebSite #website. Osoitti solmuun "https://www.ilmiöt.fi/",
                  jota ei ole: etusivun solmut ovat #website ja #collectionpage.
  publisher.logo→ og/logo.png 512×512. favicon.svg oli ilmoitettu 64×64:ksi,
                  Googlen vähimmäiskoko on 112×112.
  about         → DefinedTerm, name = etusivun kortin nimi (termi, ei koko
                  otsikko), kaikille sivuille. Termistö saa oman tunnisteen
                  #ilmiot; aiemmin se jakoi IRI:n etusivun kanssa.

FAQPage-solmu poistetaan. 68 sivun 136 vastauksesta yksikään ei ollut sivulla
sanatarkasti, eikä Google näytä FAQ-rikastetuloksia (lopetettu 7.5.2026).
Rakenteinen data, joka ei vastaa näkyvää sisältöä, on pelkkä riski. Etusivun
FAQPage jää: sen kysymykset ovat sivulla näkyvissä.

Koskee vain <script type="application/ld+json"> -lohkoa. JSON kirjoitetaan
samalla muotoilulla kuin se on sivuilla (indent=2), joten muuttumaton lohko
pysyy tavulleen samana ja "dateModified": "…" -rivit, joita muut skriptit
lukevat säännöllisellä lausekkeella, säilyvät.

Käyttö:  python3 scripts/seo_schema.py            (kuivaharjoitus)
         python3 scripts/seo_schema.py --kirjoita
"""
import html
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_kategoriat import DOMAIN, lue_kategoriat  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

LD_RE = re.compile(r'(<script type="application/ld\+json">\n)(.*?)(\n *</script>)', re.S)
LOGO = {"@type": "ImageObject", "url": f"{DOMAIN}/og/logo.png",
        "width": 512, "height": 512}
SIVUSTO = {"@type": "WebSite", "@id": f"{DOMAIN}/#website"}
TERMISTO = {"@type": "DefinedTermSet", "name": "Ilmiöitä — Miten valta toimii",
            "@id": f"{DOMAIN}/#ilmiot"}
# Article-solmun kenttäjärjestys; about lisätään publisherin perään sivuille,
# joilta se puuttui.
JARJESTYS = ["@type", "image", "@id", "url", "headline", "description",
             "inLanguage", "articleSection", "isPartOf", "publisher", "about",
             "author", "datePublished", "dateModified"]


def meta(teksti, kuvio, nimi, slug):
    m = re.findall(kuvio, teksti)
    assert len(m) == 1, f"{slug}: {nimi} löytyi {len(m)} kertaa, pitää olla 1"
    return html.unescape(m[0])


def kasittele(slug, teksti, termi, laskuri):
    lohkot = LD_RE.findall(teksti)
    assert len(lohkot) == 1, f"{slug}: JSON-LD-lohkoja {len(lohkot)}, pitää olla 1"
    vanha = lohkot[0][1]
    d = json.loads(vanha)
    assert json.dumps(d, ensure_ascii=False, indent=2) == vanha, \
        f"{slug}: JSON-LD ei ole indent=2-muodossa — uudelleenkirjoitus muuttaisi koko lohkon"

    kuvaus = meta(teksti, r'<meta name="description" content="([^"]*)">', "metakuvaus", slug)
    kuva = meta(teksti, r'<meta property="og:image" content="([^"]*)">', "og:image", slug)

    artikkelit = [n for n in d["@graph"] if n["@type"] == "Article"]
    assert len(artikkelit) == 1, f"{slug}: Article-solmuja {len(artikkelit)}"
    art = artikkelit[0]
    ennen = json.dumps(art, ensure_ascii=False, sort_keys=True)

    def aseta(avain, kohde, arvo):
        if kohde.get(avain) != arvo:
            kohde[avain] = arvo
            laskuri[avain] += 1

    aseta("description", art, kuvaus)
    aseta("url", art["image"], kuva)
    aseta("isPartOf", art, dict(SIVUSTO))
    aseta("logo", art["publisher"], dict(LOGO))
    aseta("about", art, {"@type": "DefinedTerm", "name": termi,
                         "description": kuvaus,
                         "inDefinedTermSet": dict(TERMISTO)})

    assert set(art) <= set(JARJESTYS), f"{slug}: tuntematon kenttä {set(art) - set(JARJESTYS)}"
    jarjestetty = {k: art[k] for k in JARJESTYS if k in art}
    art.clear()
    art.update(jarjestetty)

    ilman_faq = [n for n in d["@graph"] if n["@type"] != "FAQPage"]
    if len(ilman_faq) != len(d["@graph"]):
        d["@graph"] = ilman_faq
        laskuri["FAQPage pois"] += 1

    uusi = json.dumps(d, ensure_ascii=False, indent=2)
    json.loads(uusi)
    return teksti.replace(vanha, uusi, 1) if uusi != vanha else teksti


def main(argv):
    kirjoita = "--kirjoita" in argv
    assert (ROOT / "og" / "logo.png").exists(), "og/logo.png puuttuu"
    termit = {k["slug"]: html.unescape(re.sub(r"<[^>]+>", "", k["nimi"]))
              for kat in lue_kategoriat().values() for k in kat["kortit"]}

    laskuri, sivuja = Counter(), 0
    for slug, termi in termit.items():
        polku = ROOT / f"{slug}.html"
        vanha = polku.read_text(encoding="utf-8")
        uusi = kasittele(slug, vanha, termi, laskuri)
        if uusi != vanha:
            sivuja += 1
            if kirjoita:
                polku.write_text(uusi, encoding="utf-8")

    tila = "kirjoitettu" if kirjoita else "KUIVAHARJOITUS — ei kirjoitettu"
    print(f"{len(termit)} sivua luettu, {sivuja} muuttuisi. {tila}.")
    for avain, n in sorted(laskuri.items()):
        print(f"  {avain}: {n} sivua")


if __name__ == "__main__":
    main(sys.argv[1:])
