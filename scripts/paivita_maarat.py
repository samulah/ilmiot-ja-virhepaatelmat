#!/usr/bin/env python3
"""Laskee ilmiö- ja kategoriamäärät index.html:n hub-korteista ja päivittää
ne KAIKKIIN paikkoihin, joissa määrä mainitaan. Aja aina kun ilmiöitä
lisätään tai poistetaan — käsin ei tarvitse laskea eikä etsiä.

Päivittää:
  index.html : <title>, og:title, twitter:title, meta/og/twitter description,
               JSON-LD (WebSite name+description, CollectionPage description,
               ItemList numberOfItems + itemListElement uudelleenrakennettuna
               sivujen H1:istä, FAQ-teksti), hub-header, hub-intro,
               hub-katnav-lukumäärät, hub-kat-count-lukumäärät, näkyvä FAQ
  tietoa.html: "selittää N", "jaettu X teemaan", "numeroitu yhdestä N:een"
  llms.txt   : "selittää N yhteiskunnallista ilmiötä" SEKÄ ilmiölistan
               jäsenyys/järjestys (puuttuvat lisätään, poistuneet karsitaan;
               olemassa olevien rivien tekstiä ei ylikirjoiteta)

Idempotentti; tulostaa raportin ja kaatuu assertiin jos rakenne ei täsmää
(esim. kortin sivutiedosto puuttuu).

Ajo:  python3 scripts/paivita_maarat.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

INESSIIVI = {10: "kymmenessä", 11: "yhdessätoista", 12: "kahdessatoista",
             13: "kolmessatoista", 14: "neljässätoista", 15: "viidessätoista",
             16: "kuudessatoista"}
ILLATIIVI = {10: "kymmeneen", 11: "yhteentoista", 12: "kahteentoista",
             13: "kolmeentoista", 14: "neljääntoista", 15: "viiteentoista",
             16: "kuuteentoista"}


def illatiivipaate(n):
    """Numeroilmauksen illatiivipääte: 106 → ':een' (sataankuuteen)."""
    if n % 100 in range(11, 20):
        return ":toista"
    return {0: ":aan", 1: ":een", 2: ":een", 3: ":een", 4: ":ään",
            5: ":een", 6: ":een", 7: ":ään", 8: ":aan", 9: ":ään"}[n % 10]


def lue_kategoriat(html):
    """Palauttaa [(id, label, [slug, ...]), ...] hub-kategoria-lohkoista."""
    kategoriat = []
    for m in re.finditer(
            r'<div class="hub-kategoria" id="([^"]+)">\s*'
            r'<h2 class="hub-kat-label">(?:<span class="hub-kat-nro">\d+</span>)?([^<]+)<span class="hub-kat-count">(.*?)</span></h2>(.*?)\n</div>',
            html, re.S):
        kat_id, label, _, runko = m.groups()
        slugit = re.findall(r'href="([a-z0-9-]+)\.html" class="hub-kortti"', runko)
        kategoriat.append((kat_id, label, slugit))
    return kategoriat


def lue_kortit(html):
    """Kuten lue_kategoriat, mutta mukana kategorian kuvaus ja korttien
    nimi + kuvaus: [(label, kat_desc, [(slug, nimi, kuvaus), ...]), ...].
    Käytetään llms.txt:n entry-listan synkronointiin."""
    kategoriat = []
    for m in re.finditer(
            r'<div class="hub-kategoria" id="[^"]+">\s*'
            r'<h2 class="hub-kat-label">(?:<span class="hub-kat-nro">\d+</span>)?([^<]+)<span class="hub-kat-count">.*?</span></h2>\s*'
            r'<p class="hub-kat-desc">(.*?)</p>(.*?)\n</div>', html, re.S):
        label, kat_desc, runko = m.groups()
        kortit = re.findall(
            r'<a href="([a-z0-9-]+)\.html" class="hub-kortti"[^>]*>\s*'
            r'<span class="hub-numero">\d+</span>\s*<span class="hub-teksti">\s*'
            r'<span class="hub-nimi">(.*?)</span>\s*'
            r'<span class="hub-kuvaus">(.*?)</span>', runko, re.S)
        kat_desc = re.sub(r"<[^>]+>", "", kat_desc).strip()
        ekavirke = re.match(r"(.*?[.!?])(\s|$)", kat_desc, re.S)
        kategoriat.append((label.strip(),
                           (ekavirke.group(1) if ekavirke else kat_desc),
                           [(s, n.strip(), k.strip()) for s, n, k in kortit]))
    return kategoriat


def sivun_h1(slug):
    html = (ROOT / f"{slug}.html").read_text(encoding="utf-8")
    m = re.search(r"<h1>(.*?)</h1>", html, re.S)
    assert m, f"{slug}.html: ei H1:tä"
    return re.sub(r"<[^>]+>", "", m.group(1)).strip()


def paivita_index(raportti):
    p = ROOT / "index.html"
    html = p.read_text(encoding="utf-8")

    kategoriat = lue_kategoriat(html)
    yhteensa = sum(len(s) for k, l, s in kategoriat)
    n_kat = len(kategoriat)
    assert kategoriat, "hub-kategoria-lohkoja ei löytynyt"
    assert n_kat in INESSIIVI, f"lisää sanataulukoihin luku {n_kat}"

    # sivutiedostot olemassa + duplikaatit
    kaikki_slugit = [s for _, _, slugit in kategoriat for s in slugit]
    assert len(kaikki_slugit) == len(set(kaikki_slugit)), "duplikaattikortti"
    for s in kaikki_slugit:
        assert (ROOT / f"{s}.html").exists(), f"kortin sivu puuttuu: {s}.html"

    def korvaa(kuvaus, pattern, korvaava, maara=0):
        nonlocal html
        uusi, n = re.subn(pattern, korvaava, html)
        if maara:
            assert n == maara, f"{kuvaus}: {n} osumaa, odotettiin {maara}"
        if uusi != html:
            raportti.append(f"index.html: {kuvaus} ({n} kohtaa)")
        html = uusi

    # kokonaismäärät (kaikki sanamuodot)
    korvaa("yhteiskunnallista ilmiötä", r"\d+ yhteiskunnallista ilmiötä",
           f"{yhteensa} yhteiskunnallista ilmiötä")
    korvaa("selitettynä suomeksi: N ilmiötä", r"suomeksi: \d+ ilmiötä",
           f"suomeksi: {yhteensa} ilmiötä")
    korvaa("Sivusto selittää N ilmiötä", r"Sivusto selittää \d+ ilmiötä",
           f"Sivusto selittää {yhteensa} ilmiötä", maara=2)
    korvaa("hub-header", r"<p>\d+ ilmiötä &middot;", f"<p>{yhteensa} ilmiötä &middot;", maara=1)
    korvaa("N kategoriassa", r"\w+toista kategoriassa|kymmenessä kategoriassa",
           f"{INESSIIVI[n_kat]} kategoriassa")
    korvaa("numberOfItems", r'"numberOfItems": \d+,', f'"numberOfItems": {yhteensa},', maara=1)

    # katnav: <a href="#id">Label<span>N</span></a>
    for kat_id, label, slugit in kategoriat:
        uusi_nav = f'<a href="#{kat_id}">{label}<span>{len(slugit)}</span></a>'
        pattern = rf'<a href="#{re.escape(kat_id)}">{re.escape(label)}<span>\d+</span></a>'
        assert re.search(pattern, html), f"katnav-linkkiä ei löydy: {label}"
        if not re.search(re.escape(uusi_nav), html):
            raportti.append(f"index.html: katnav {label} → {len(slugit)}")
        html = re.sub(pattern, uusi_nav, html)

        # hub-kat-count
        pattern = (rf'(<h2 class="hub-kat-label">(?:<span class="hub-kat-nro">\d+</span>)?{re.escape(label)}'
                   rf'<span class="hub-kat-count">) · \d+ ilmiötä(</span>)')
        korvattu, n = re.subn(pattern, rf"\g<1> · {len(slugit)} ilmiötä\g<2>", html)
        assert n == 1, f"hub-kat-count ei löydy: {label}"
        if korvattu != html:
            raportti.append(f"index.html: hub-kat-count {label} → {len(slugit)}")
        html = korvattu

    # ItemList uudelleen korteista + sivujen H1:istä
    itemit = ",\n".join(
        '          {\n            "@type": "ListItem",\n'
        f'            "position": {i},\n'
        f'            "name": {json.dumps(sivun_h1(s), ensure_ascii=False)},\n'
        f'            "url": "https://www.ilmiöt.fi/{s}.html"\n          }}'
        for i, s in enumerate(kaikki_slugit, 1))
    uusi_lista = f'"itemListElement": [\n{itemit}\n        ]'
    korvattu, n = re.subn(r'"itemListElement": \[.*?\n        \]',
                          lambda m: uusi_lista, html, count=1, flags=re.S)
    assert n == 1, "itemListElement-lohkoa ei löytynyt"
    if korvattu != html:
        raportti.append(f"index.html: ItemList rakennettu uudelleen ({yhteensa} riviä)")
    html = korvattu

    # JSON-LD:n on pysyttävä parsittavana
    for blob in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        json.loads(blob)

    p.write_text(html, encoding="utf-8")
    return yhteensa, n_kat


def paivita_tietoa(yhteensa, n_kat, raportti):
    p = ROOT / "tietoa.html"
    html = p.read_text(encoding="utf-8")
    alku = html
    html = re.sub(r"joka selittää \d+", f"joka selittää {yhteensa}", html)
    html = re.sub(r"jaettu \w+ teemaan ja numeroitu yhdestä \d+:\w+",
                  f"jaettu {ILLATIIVI[n_kat]} teemaan ja numeroitu "
                  f"yhdestä {yhteensa}{illatiivipaate(yhteensa)}", html)
    if html != alku:
        raportti.append("tietoa.html: määrät päivitetty")
    p.write_text(html, encoding="utf-8")


LLMS_OTSIKKO = "## Kategoriat ja ilmiöt"


def paivita_llms(yhteensa, kortit, raportti):
    """Päivittää llms.txt:n määrän JA synkronoi ilmiölistan index.html:n
    kortteihin.

    Synkronoi vain JÄSENYYDEN ja JÄRJESTYKSEN: puuttuvat ilmiöt lisätään
    kortin nimellä + kuvauksella, poistuneet karsitaan, järjestys otetaan
    korteista. Jo olemassa olevien rivien TEKSTIÄ ei kosketa — llms.txt:ssä
    on tarkoituksellisia käsin hiottuja eroja kortteihin nähden (esim.
    "Argumenttitulva (Gish Gallop)", "Lowball-hinnoittelu"), ja ne saavat
    jäädä. Eroavaisuudet raportoidaan, jotta ne voi halutessaan yhtenäistää.
    """
    p = ROOT / "llms.txt"
    txt = p.read_text(encoding="utf-8")

    txt = re.sub(r"selittää \d+ yhteiskunnallista ilmiötä",
                 f"selittää {yhteensa} yhteiskunnallista ilmiötä", txt)

    assert LLMS_OTSIKKO in txt, f"llms.txt: '{LLMS_OTSIKKO}' puuttuu"
    ylatunniste, _, runko = txt.partition(LLMS_OTSIKKO)

    # nykyiset rivit slugeittain + kategoriakuvaukset otsikoittain
    rivit = {m.group(1): m.group(0) for m in
             re.finditer(r"^- \[[^\]]*\]\(https://www\.ilmiöt\.fi/"
                         r"([a-z0-9-]+)\.html\):.*$", runko, re.M)}
    kat_kuvaukset = {m.group(1).strip(): m.group(2).strip() for m in
                     re.finditer(r"^### (.+)\n\n(.+?)\n", runko, re.M)}

    # kategoriasivut, jos niitä on tehty (build_kategoriat.py) — label → slug
    kat_sivut = {}
    for kat_id, label, _ in lue_kategoriat((ROOT / "index.html").read_text(encoding="utf-8")):
        slug = re.sub(r"-kategoria$", "", kat_id)
        if (ROOT / f"kategoria-{slug}.html").exists():
            kat_sivut[label] = slug

    ulos, lisatyt, erot = [], [], []
    for label, kat_desc, kortit_kat in kortit:
        ulos += [f"### {label}", "", kat_kuvaukset.get(label, kat_desc), ""]
        if label in kat_sivut:
            ulos += [f"Kategoriasivu: https://www.ilmiöt.fi/"
                     f"kategoria-{kat_sivut[label]}.html", ""]
        for slug, nimi, kuvaus in kortit_kat:
            if slug in rivit:
                ulos.append(rivit[slug])
                oma = f"- [{nimi}](https://www.ilmiöt.fi/{slug}.html): {kuvaus}"
                if rivit[slug] != oma:
                    erot.append(slug)
            else:
                ulos.append(f"- [{nimi}](https://www.ilmiöt.fi/{slug}.html): {kuvaus}")
                lisatyt.append(slug)
        ulos.append("")

    kortti_slugit = {s for _, _, ks in kortit for s, _, _ in ks}
    poistetut = sorted(set(rivit) - kortti_slugit)

    uusi = ylatunniste + LLMS_OTSIKKO + "\n\n" + "\n".join(ulos).rstrip("\n") + "\n"
    if uusi != p.read_text(encoding="utf-8"):
        if lisatyt:
            raportti.append(f"llms.txt: lisätty {len(lisatyt)} ilmiötä "
                            f"({', '.join(lisatyt)})")
        if poistetut:
            raportti.append(f"llms.txt: poistettu {len(poistetut)} ilmiötä "
                            f"({', '.join(poistetut)})")
        if not lisatyt and not poistetut:
            raportti.append("llms.txt: määrä/järjestys päivitetty")
    if erot:
        raportti.append(f"llms.txt: {len(erot)} riviä poikkeaa kortin tekstistä "
                        f"(säilytetty ennallaan): {', '.join(erot)}")

    # sanity: yhtä monta riviä kuin kortteja
    n_rivit = len(re.findall(r"^- \[", uusi, re.M))
    assert n_rivit == yhteensa, f"llms.txt: {n_rivit} riviä, odotettiin {yhteensa}"
    p.write_text(uusi, encoding="utf-8")


if __name__ == "__main__":
    raportti = []
    yhteensa, n_kat = paivita_index(raportti)
    paivita_tietoa(yhteensa, n_kat, raportti)
    paivita_llms(yhteensa,
                 lue_kortit((ROOT / "index.html").read_text(encoding="utf-8")),
                 raportti)
    print(f"Laskettu korteista: {yhteensa} ilmiötä, {n_kat} kategoriaa")
    if raportti:
        for r in raportti:
            print("  ✎", r)
    else:
        print("  kaikki määrät olivat jo ajan tasalla")
