#!/usr/bin/env python3
"""Julkaisee Tilastoilla valehtelu -kategorian (ilmiöt 99–106).

Kertaluontoinen: siirtää luonnokset juureen (noindex pois), lisää kategorian
index.html:ään (katnav, hub-lohko, määrät 98→106, JSON-LD ItemList),
päivittää IDS-listat ja laskurit kaikilla vanhoilla sivuilla, jatkaa
PREV/NEXT-ketjun haamutyopaikat → kaksois-y-akseli, lisää sitemap- ja
llms.txt-tietueet sekä ohjauslaatikon ankkurisivulle #8.

Ajo:  python3 scripts/publish_tilasto_kategoria.py
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_tilasto_luonnokset import KORTTI, PAGES, UUDET  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DRAFTS = ROOT / "luonnokset-tilasto"
PVM = "2026-07-12"

KAT_DESC = ("Miten luvuilla ja kaavioilla johdetaan harhaan valehtelematta kertaakaan: "
            "katkaistut akselit, paisutellut symbolit, valikoidut aikavälit, väärä keskiluku "
            "ja sattuman kalastelu. Samat tekniikat toistuvat uutisissa, markkinoinnissa ja "
            "politiikassa — ja jokaisen oppii tunnistamaan parilla vakiokysymyksellä.")


def siirra_luonnokset():
    for slug in UUDET:
        html = (DRAFTS / f"{slug}.html").read_text(encoding="utf-8")
        html = html.replace('  <meta name="robots" content="noindex"><!-- POISTA-JULKAISTAESSA -->\n', "")
        assert "noindex" not in html, slug
        (ROOT / f"{slug}.html").write_text(html, encoding="utf-8")
        print(f"  julkaistu {slug}.html")


def hub_kortti(slug):
    num, vari, nimi, kuvaus = KORTTI[slug]
    return f'''<a href="{slug}.html" class="hub-kortti" style="--c:{vari}">
  <span class="hub-numero">{num}</span>
  <span class="hub-teksti">
    <span class="hub-nimi">{nimi}</span>
    <span class="hub-kuvaus">{kuvaus}</span>
  </span>
  <span class="hub-nuoli" aria-hidden="true">›</span>
</a>'''


def paivita_index():
    p = ROOT / "index.html"
    html = p.read_text(encoding="utf-8")

    # katnav
    vanha_nav = '<a href="#tyoelaman-ilmiot">Työelämän ilmiöt<span>3</span></a>'
    assert vanha_nav in html
    html = html.replace(vanha_nav, vanha_nav +
        '\n  <a href="#tilastoilla-valehtelu-kategoria">Tilastoilla valehtelu<span>8</span></a>')

    # hub-kategoria-lohko ennen hub-tyhja-diviä
    lohko = ('\n<div class="hub-kategoria" id="tilastoilla-valehtelu-kategoria">\n'
             '  <h2 class="hub-kat-label">Tilastoilla valehtelu<span class="hub-kat-count"> · 8 ilmiötä</span></h2>\n'
             f'  <p class="hub-kat-desc">{KAT_DESC}</p>\n'
             '  <div class="hub-kortit">\n'
             + "\n".join(hub_kortti(s) for s in UUDET) +
             '\n  </div>\n</div>\n')
    marker = '\n  <div class="hub-tyhja" id="hub-tyhja">'
    assert marker in html
    html = html.replace(marker, lohko + marker)

    # määrät
    assert html.count("98 ilmiötä") == 7
    html = html.replace("98 ilmiötä", "106 ilmiötä")
    html = html.replace('"numberOfItems": 98,', '"numberOfItems": 106,')
    assert html.count("yhdessätoista kategoriassa") == 2
    html = html.replace("yhdessätoista kategoriassa", "kahdessatoista kategoriassa")

    # kategorialuettelot (JSON-LD-teksti + näkyvä FAQ)
    html = html.replace(
        "pesut ja maineenhallinta sekä työelämän ilmiöt. Mukana",
        "pesut ja maineenhallinta, työelämän ilmiöt sekä tilastoilla valehtelu. Mukana")
    vanha_faq = ('<a href="#pesut-ja-maineenhallinta">pesut ja maineenhallinta</a> sekä\n'
                 '    <a href="#tyoelaman-ilmiot">työelämän ilmiöt</a>. Mukana')
    assert vanha_faq in html
    html = html.replace(vanha_faq,
        '<a href="#pesut-ja-maineenhallinta">pesut ja maineenhallinta</a>,\n'
        '    <a href="#tyoelaman-ilmiot">työelämän ilmiöt</a> sekä\n'
        '    <a href="#tilastoilla-valehtelu-kategoria">tilastoilla valehtelu</a>. Mukana')

    # JSON-LD ItemList: 8 uutta ListItemiä position 98:n perään
    viim = re.search(r'\{\s*"@type": "ListItem",\s*"position": 98,.*?\}', html, re.S)
    assert viim, "ItemList position 98 ei löytynyt"
    uudet_itemit = "".join(
        ',\n          {\n            "@type": "ListItem",\n'
        f'            "position": {KORTTI[s][0]},\n'
        f'            "name": {json.dumps(KORTTI[s][2], ensure_ascii=False)},\n'
        f'            "url": "https://www.ilmiöt.fi/{s}.html"\n          }}'
        for s in UUDET)
    html = html[:viim.end()] + uudet_itemit + html[viim.end():]

    p.write_text(html, encoding="utf-8")
    print("  index.html päivitetty")


def paivita_vanhat_sivut():
    tpl_ids = re.search(r"const IDS = \[.*?\];",
                        (ROOT / f"{UUDET[0]}.html").read_text(encoding="utf-8"),
                        re.S).group(0)
    muutettu = 0
    for f in sorted(ROOT.glob("*.html")):
        if f.name in ("index.html", "tietoa.html") or f.stem in UUDET:
            continue
        html = f.read_text(encoding="utf-8")
        if "const IDS" not in html:
            continue
        uusi = re.sub(r"const IDS = \[.*?\];", lambda m: tpl_ids, html, count=1, flags=re.S)
        uusi = re.sub(r'(kortti-nav-laskuri">\s*\d+) / 98<', r"\1 / 106<", uusi, count=1)
        if f.stem == "haamutyopaikat":
            uusi = uusi.replace("const NEXT = '';", "const NEXT = 'kaksois-y-akseli.html';")
            uusi = uusi.replace(
                '<span class="kortti-nav-btn disabled">→</span>',
                '<a class="kortti-nav-btn" href="kaksois-y-akseli.html">Kaksois-y-akseli — kaksi asteikkoa, valmis korrelaatio →</a>')
        if uusi != html:
            f.write_text(uusi, encoding="utf-8")
            muutettu += 1
    print(f"  {muutettu} vanhaa sivua päivitetty (IDS + laskuri)")


def paivita_ankkurisivu():
    p = ROOT / "tilastoilla-valehtelu.html"
    html = p.read_text(encoding="utf-8")
    linkit = ", ".join(f'<a href="{s}.html">{KORTTI[s][2]}</a>' for s in UUDET)
    laatikko = ('<div class="huomiolaatikko">\n'
                '<strong>Koko aihepiiri omana kategorianaan:</strong> tämän sivun tekniikat on avattu '
                'yksi kerrallaan <a href="index.html#tilastoilla-valehtelu-kategoria">Tilastoilla valehtelu '
                '-kategoriassa</a> — ' + linkit + '.\n</div>\n')
    marker = '<div class="lue-lisaa">'
    assert marker in html
    html = html.replace(marker, laatikko + marker, 1)
    html = html.replace("Päivitetty 19.6.2026", "Päivitetty 12.7.2026")
    html = html.replace('"dateModified": "2026-06-19"', f'"dateModified": "{PVM}"')
    p.write_text(html, encoding="utf-8")
    print("  tilastoilla-valehtelu.html: ohjauslaatikko + päiväys")


def paivita_sitemap():
    p = ROOT / "sitemap.xml"
    xml = p.read_text(encoding="utf-8")
    tietueet = "".join(
        f"  <url>\n    <loc>https://www.ilmiöt.fi/{s}.html</loc>\n"
        f"    <lastmod>{PVM}</lastmod>\n    <priority>0.8</priority>\n"
        f"    <changefreq>monthly</changefreq>\n  </url>\n"
        for s in UUDET)
    xml = xml.replace("</urlset>", tietueet + "</urlset>")
    # ankkurisivun lastmod päivittyi
    xml = re.sub(r"(tilastoilla-valehtelu\.html</loc>\s*<lastmod>)[\d-]+", rf"\g<1>{PVM}", xml)
    p.write_text(xml, encoding="utf-8")
    print("  sitemap.xml: 8 uutta URL:ää")


def paivita_llms():
    p = ROOT / "llms.txt"
    txt = p.read_text(encoding="utf-8")
    txt = txt.replace("selittää 98 yhteiskunnallista ilmiötä", "selittää 106 yhteiskunnallista ilmiötä")
    rivit = "\n".join(f"- [{KORTTI[s][2]}](https://www.ilmiöt.fi/{s}.html): {KORTTI[s][3]}" for s in UUDET)
    txt = txt.rstrip("\n") + ("\n\n### Tilastoilla valehtelu\n\n"
        "Miten luvuilla ja kaavioilla johdetaan harhaan valehtelematta kertaakaan — "
        "akseleista aikaväleihin ja sattuman kalasteluun.\n\n" + rivit + "\n")
    p.write_text(txt, encoding="utf-8")
    print("  llms.txt: kategoria + 8 riviä")


if __name__ == "__main__":
    siirra_luonnokset()
    paivita_index()
    paivita_vanhat_sivut()
    paivita_ankkurisivu()
    paivita_sitemap()
    paivita_llms()
    print("Valmis. Aja vielä build_liittyvat.py ja build_search_index.py.")
