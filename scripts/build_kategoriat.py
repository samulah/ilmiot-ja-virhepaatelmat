#!/usr/bin/env python3
"""Generoi kategoriasivut (kategoria-<slug>.html) kahdesta lähteestä:

  1. index.html          — kategorian nimi, kuvaus ja ilmiökortit (numero, väri,
                           nimi, kuvaus). Yksi totuuden lähde, kuten
                           build_liittyvat.py:llä.
  2. kategoriat/<slug>.md — käsin kirjoitettu osuus: johdantoessee ja ilmiöiden
                           väliset kytkennät. Tämä on sivun ainoa uniikki
                           sisältö eikä sitä koskaan generoida.

Sisältötiedoston muoto:

    ---
    kat_id: tilastoilla-valehtelu-kategoria   # index.html:n hub-kategoria id
    h1: Otsikko — alaotsikko
    otsikko: <title>-teksti ilman "| Ilmiöitä"-häntää
    kuvaus: meta description (150-160 merkkiä)
    vari: "#1565c0"
    paivitetty: 2026-07-25
    naapurit:
      - kategoria-informaatio-ja-propaganda | Näkyvä linkkiteksti
    ---

    Leipätekstiä. Tyhjä rivi erottaa kappaleet.

    ## Väliotsikko

    - Lista
    - toinen kohta

    :::html
    <div class="tilasto-grid">... raakaa HTML:ää, esim. SVG ...</div>
    :::

    [[ILMIOT]]     -> generoitu korttilista
    [[NAAPURIT]]   -> generoidut naapurikategorialinkit

Ajo:
    python3 scripts/build_kategoriat.py                  # kaikki kategoriat/*.md
    python3 scripts/build_kategoriat.py tilastoilla-valehtelu
    python3 scripts/build_kategoriat.py --luonnos        # kirjoita luonnoskansioon
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SISALTO = ROOT / "kategoriat"
LUONNOSKANSIO = ROOT / "luonnokset-media"

DOMAIN = "https://www.ilmiöt.fi"
CSS_VERSIO = "20260727"   # pidä samassa kuin ilmiösivuilla (ks. muisti: CSS cache-bust)


# ───────────────────────────── index.html ──────────────────────────────

KAT_RE = re.compile(
    r'<div class="hub-kategoria" id="([^"]+)">\s*'
    r'<h2 class="hub-kat-label">(?:<span class="hub-kat-nro">\d+</span>)?([^<]+)<span class="hub-kat-count">.*?</span></h2>\s*'
    r'<p class="hub-kat-desc">(.*?)</p>(.*?)\n</div>', re.S)

KORTTI_RE = re.compile(
    r'<a href="([a-z0-9-]+)\.html" class="hub-kortti" style="--c:(#[0-9a-fA-F]{6})">\s*'
    r'<span class="hub-numero">(\d+)</span>\s*<span class="hub-teksti">\s*'
    r'<span class="hub-nimi">(.*?)</span>\s*'
    r'<span class="hub-kuvaus">(.*?)</span>', re.S)


def lue_kategoriat():
    """index.html → {kat_id: {nro, label, kuvaus, kortit, ilmioalue}}

    `nro` on kategorian järjestysnumero etusivun järjestyksessä ja `ilmioalue`
    sen kattama ilmiönumeroväli (esim. "1–7"). Ilmiöt on numeroitu juoksevasti
    kategorioiden yli, joten väli on aito tieto eikä koriste: se erottaa
    kategoriasivun ilmiösivusta, jolla on vain yksi numero."""
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    kategoriat = {}
    for nro, (kat_id, label, kuvaus, runko) in enumerate(KAT_RE.findall(html), 1):
        kortit = [{"slug": s, "vari": v, "numero": int(n),
                   "nimi": nimi.strip(), "kuvaus": k.strip()}
                  for s, v, n, nimi, k in KORTTI_RE.findall(runko)]
        numerot = [k["numero"] for k in kortit]
        # väli näytetään vain jos numerot ovat yhtenäiset
        alue = (f"{min(numerot)}&ndash;{max(numerot)}"
                if numerot and max(numerot) - min(numerot) + 1 == len(numerot)
                else None)
        # hub-kat-desc sisältää "Lue koko kategoria →" -linkin, kun
        # lisaa_kategorialinkit.py on ajettu — se ei kuulu skeemaan
        puhdas = re.sub(r'<a class="hub-kat-linkki".*?</a>', "", kuvaus, flags=re.S)
        puhdas = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", puhdas)).strip()
        kategoriat[kat_id] = {"nro": nro,
                              "label": label.strip(),
                              "kuvaus": puhdas,
                              "kortit": kortit,
                              "ilmioalue": alue}
    assert kategoriat, "index.html: hub-kategoria-lohkoja ei löytynyt"
    for k in kategoriat.values():
        k["kat_yhteensa"] = len(kategoriat)
    return kategoriat


# ─────────────────────────── sisältötiedosto ───────────────────────────

def lue_sisalto(polku):
    teksti = polku.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n(.*)", teksti, re.S)
    assert m, f"{polku.name}: front matter puuttuu"
    meta, runko = {}, m.group(2)

    avain = None
    for rivi in m.group(1).split("\n"):
        if not rivi.strip():
            continue
        if rivi.startswith(("  -", "\t-")):
            assert avain, f"{polku.name}: listarivi ilman avainta"
            meta.setdefault(avain, []).append(rivi.split("-", 1)[1].strip())
            continue
        avain, arvo = rivi.split(":", 1)
        avain, arvo = avain.strip(), arvo.strip().strip('"')
        if arvo:
            meta[avain] = arvo
        else:
            meta[avain] = []

    for pakollinen in ("kat_id", "h1", "otsikko", "kuvaus", "vari", "paivitetty"):
        assert pakollinen in meta, f"{polku.name}: '{pakollinen}' puuttuu front matterista"
    return meta, runko


def muotoile(runko):
    """Kevyt markdown → HTML. Tukee ## / ### / - lista / kappale / :::html-lohko."""
    ulos, lohkot = [], re.split(r"\n:::html\n(.*?)\n:::\n", runko, flags=re.S)
    for i, lohko in enumerate(lohkot):
        if i % 2:                       # :::html ... ::: → sellaisenaan
            ulos.append(lohko.strip())
            continue
        for pala in re.split(r"\n\s*\n", lohko):
            pala = pala.strip()
            if not pala:
                continue
            if pala.startswith("[[") and pala.endswith("]]"):
                ulos.append(pala)
            elif pala.startswith("### "):
                ulos.append(f"<h3>{linkita(pala[4:])}</h3>")
            elif pala.startswith("## "):
                ulos.append(f"<h2>{linkita(pala[3:])}</h2>")
            elif pala.startswith("- ") or re.match(r"\d+\. ", pala):
                tagi = "ul" if pala.startswith("- ") else "ol"
                rivit = "\n".join(
                    f"<li>{linkita(re.sub(r'^(- |\d+\. )', '', r.strip()))}</li>"
                    for r in pala.split("\n") if r.strip())
                ulos.append(f"<{tagi}>\n{rivit}\n</{tagi}>")
            else:
                ulos.append(f"<p>{linkita(pala)}</p>")
    return "\n".join(ulos)


def linkita(teksti):
    """[teksti](kohde.html) → <a>, **lihavointi** → <strong>."""
    teksti = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', teksti)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", teksti)


# ──────────────────────────── sivun palaset ────────────────────────────

def korttilista(kortit):
    osat = ['<div class="kat-kortit">']
    for k in kortit:
        osat.append(
            f'<a href="{k["slug"]}.html" class="hub-kortti" style="--c:{k["vari"]}">\n'
            f'  <span class="hub-numero">{k["numero"]}</span>\n'
            f'  <span class="hub-teksti">\n'
            f'    <span class="hub-nimi">{k["nimi"]}</span>\n'
            f'    <span class="hub-kuvaus">{k["kuvaus"]}</span>\n'
            f'  </span>\n'
            f'  <span class="hub-nuoli" aria-hidden="true">›</span>\n'
            f'</a>')
    osat.append("</div>")
    return "\n".join(osat)


def siirtymanavi(edellinen, seuraava, kat, etu):
    """Edellinen/seuraava kategoria sivun lopussa + laskuri."""
    if not edellinen and not seuraava:
        return ""
    kortit = []
    for tiedot, luokka, label, nuoli in (
            (edellinen, "edellinen", "Edellinen kategoria", "&larr; "),
            (seuraava, "seuraava", "Seuraava kategoria", " &rarr;")):
        if not tiedot:
            continue
        kortit.append(
            f'    <a class="kat-siirry-kortti {luokka}" '
            f'href="kategoria-{tiedot["slug"]}.html" style="--c:{tiedot["vari"]}">\n'
            f'      <span class="kat-siirry-label">{label}</span>\n'
            f'      <span class="kat-siirry-nimi">{nuoli if luokka == "edellinen" else ""}'
            f'{tiedot["nro"]}. {tiedot["label"]}'
            f'{nuoli if luokka == "seuraava" else ""}</span>\n'
            f'    </a>')
    return (f'<nav class="kat-siirry" aria-label="Kategoriasta toiseen">\n'
            f'  <div class="kat-siirry-parit">\n' + "\n".join(kortit) + "\n  </div>\n"
            f'  <a class="kat-siirry-kaikki" href="{etu}index.html">'
            f'Kategoria <b>{kat["nro"]} / {kat["kat_yhteensa"]}</b> '
            f'&middot; katso kaikki kategoriat</a>\n'
            f'</nav>')


def selausskripti(edellinen, seuraava):
    """Nuolinäppäimet kuten ilmiösivuilla. Vaakaswipeä EI ole tarkoituksella:
    se törmää selaimen takaisin-eleeseen ja tekstin maalaamiseen."""
    if not edellinen and not seuraava:
        return ""
    p = f"'kategoria-{edellinen['slug']}.html'" if edellinen else "null"
    n = f"'kategoria-{seuraava['slug']}.html'" if seuraava else "null"
    return f"""  <script>
(function () {{
  var PREV = {p}, NEXT = {n};
  document.addEventListener('keydown', function (e) {{
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    var t = e.target;
    if (t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName))) return;
    if (e.key === 'ArrowLeft' && PREV) location.href = PREV;
    if (e.key === 'ArrowRight' && NEXT) location.href = NEXT;
  }});
}})();
  </script>"""


def naapurilista(naapurit, ohita=()):
    """Toimituksellisesti valitut lähikategoriat.

    `ohita` karsii ne, jotka ovat jo sivun lopun edellinen/seuraava-korteissa —
    muuten sama kategoria näkyisi kahdesti peräkkäin eri sanamuodolla."""
    rivit = []
    for rivi in naapurit:
        kohde, teksti = [o.strip() for o in rivi.split("|", 1)]
        if kohde in ohita:
            continue
        rivit.append(f'  <a href="{kohde}.html">{teksti}</a>')
    if not rivit:
        return ""
    return ('<nav class="kat-naapurit" aria-label="Aiheeseen liittyvät kategoriat">\n'
            '  <p class="kat-naapurit-label">Aiheeseen liittyvät kategoriat</p>\n'
            + "\n".join(rivit) + "\n</nav>")


def skeema(meta, kat, slug):
    """Rakennetaan dictinä ja serialisoidaan json.dumpsilla.

    Aiemmin tämä oli f-string-mallipohja, jolloin index.html:stä luettu teksti
    upotettiin JSON-merkkijonoon ilman escapea — yksi lainausmerkki kuvauksessa
    rikkoi koko skeeman. Nyt lainausmerkit eivät voi rikkoa mitään.
    """
    url = f"{DOMAIN}/kategoria-{slug}.html"
    graafi = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1,
                     "name": "Ilmiöitä", "item": f"{DOMAIN}/"},
                    {"@type": "ListItem", "position": 2,
                     "name": kat["label"], "item": url},
                ],
            },
            {
                "@type": "CollectionPage",
                "@id": f"{url}#kategoria",
                "url": url,
                "name": meta["h1"],
                "headline": meta["h1"],
                "description": meta["kuvaus"],
                "inLanguage": "fi",
                "isPartOf": {"@type": "WebSite", "@id": f"{DOMAIN}/#website"},
                "publisher": {
                    "@type": "Organization",
                    "@id": f"{DOMAIN}/#organization",
                    "name": "Ilmiöitä",
                    "url": f"{DOMAIN}/",
                    "logo": {"@type": "ImageObject",
                             "url": f"{DOMAIN}/favicon.svg",
                             "width": 64, "height": 64},
                },
                "author": {"@type": "Person", "name": "Ilmiömies",
                           "url": f"{DOMAIN}/tietoa.html"},
                "dateModified": meta["paivitetty"],
                "about": {
                    "@type": "DefinedTermSet",
                    "@id": f"{url}#termisto",
                    "name": kat["label"],
                    "description": kat["kuvaus"],
                },
                "mainEntity": {
                    "@type": "ItemList",
                    "name": kat["label"],
                    "numberOfItems": len(kat["kortit"]),
                    "itemListOrder": "https://schema.org/ItemListOrderAscending",
                    "itemListElement": [
                        {"@type": "ListItem", "position": i,
                         "url": f"{DOMAIN}/{k['slug']}.html", "name": k["nimi"]}
                        for i, k in enumerate(kat["kortit"], 1)
                    ],
                },
            },
        ],
    }
    teksti = json.dumps(graafi, ensure_ascii=False, indent=2)
    return '  <script type="application/ld+json">\n' + teksti + "\n  </script>"


# Kolme sivutasoa erottuvat rakenteesta, eivät koristeesta:
#   etusivu      — tumma tarttuva header, tiheä korttiruudukko, leveä
#   KATEGORIASIVU— tumma täysleveä luvun aloitus, essee kapeassa palstassa,
#                  korttiruudukko rikkoo palstan leveämmäksi. EI valkoista korttia.
#   ilmiösivu    — valkoinen kortti kermalla, värillinen yläreuna, kapea
# Ilmiösivun tunnus on yksi numero ("Ilmiö 8"), kategoriasivun numeroväli
# ("Ilmiöt 1–7"). Se on sivun ainoa varsinainen riski: ilman valkoista korttia
# sivu ei näytä artikkelilta, mikä on koko pointti.
TYYLI = """  <style>
    body { max-width: none; margin: 0; padding: 0; }

    /* ── Luvun aloitus ── */
    .kat-masthead {
      background: var(--c-primary-dark, #1C1400);
      border-bottom: 4px solid var(--kat, #C9A84C);
      padding: 1rem 1.5rem 2.6rem;
      position: relative;
      overflow: hidden;
    }
    .kat-masthead-sisus { max-width: 1080px; margin: 0 auto; position: relative; }
    /* Vesileima on absoluuttinen eli maalautuisi tekstin PÄÄLLE ilman tätä:
       positioidut elementit voittavat positioimattomat samassa pinossa. */
    .kat-masthead-teksti { position: relative; z-index: 1; }
    .kat-paluu {
      display: inline-flex; align-items: center; gap: 0.45rem;
      color: rgba(255,255,255,0.66); text-decoration: none;
      font-family: var(--font-ui, 'DM Sans', sans-serif);
      font-size: 0.8rem; padding: 0.35rem 0; margin-bottom: 2.2rem;
      border-bottom: 1px solid transparent; transition: color 0.12s, border-color 0.12s;
    }
    .kat-paluu:hover { color: var(--c-primary, #C9A84C); border-bottom-color: currentColor; }
    .kat-paluu img { width: 20px; height: 20px; display: block; }
    .kat-masthead a:focus-visible { outline: 2px solid var(--c-primary, #C9A84C);
      outline-offset: 3px; }
    .kat-eyebrow {
      font-family: var(--font-ui, 'DM Sans', sans-serif);
      font-size: 0.68rem; font-weight: 600;
      text-transform: uppercase; letter-spacing: 0.2em;
      color: var(--c-primary, #C9A84C);
      margin-bottom: 0.9rem;
    }
    h1.kat-nimi {
      font-family: var(--font-display, 'Spectral', Georgia, serif);
      font-size: clamp(1.9rem, 5vw, 2.9rem);
      font-weight: 700; line-height: 1.1; letter-spacing: -0.015em;
      color: #fff; margin: 0; max-width: 20ch;
    }
    /* Oma <p> h1:n ulkopuolella. font-family toistetaan tässä, koska ulkoasu
       periytyi aiemmin h1:ltä — nyt periytymisketju ei enää kulje sen kautta. */
    p.kat-alaotsikko {
      margin: 0.5rem 0 0;
      font-family: var(--font-display, 'Spectral', Georgia, serif);
      font-size: clamp(0.95rem, 2.2vw, 1.18rem);
      font-weight: 400; font-style: italic; line-height: 1.4;
      color: rgba(255,255,255,0.6); max-width: 34ch;
    }
    .kat-meta {
      margin-top: 1.5rem;
      font-family: var(--font-ui, 'DM Sans', sans-serif);
      font-size: 0.8rem; letter-spacing: 0.04em;
      color: rgba(201,168,76,0.85);
    }
    .kat-meta span { color: rgba(255,255,255,0.32); margin: 0 0.55em; }
    /* Luvun numero vesileimana — sivun ainoa koristeellinen elementti */
    .kat-vesileima {
      position: absolute; right: 0; top: 50%; transform: translateY(-48%);
      font-family: var(--font-display, 'Spectral', Georgia, serif);
      font-size: clamp(7rem, 16vw, 15rem); font-weight: 700; line-height: 0.8;
      color: rgba(201,168,76,0.10);
      user-select: none; pointer-events: none; z-index: 0;
    }
    @media (max-width: 860px) { .kat-vesileima { display: none; } }

    /* ── Runko ── */
    .kat-runko {
      max-width: 660px; margin: 0 auto;
      padding: 2.6rem 1.5rem 3.5rem;
      font-size: 1.02rem;
    }
    .kat-runko > h2 {
      font-family: var(--font-display, 'Spectral', Georgia, serif);
      font-size: 1.42rem; line-height: 1.25; letter-spacing: -0.01em;
      margin: 2.6rem 0 0.9rem; padding-top: 1.4rem;
      border-top: 1px solid rgba(139,105,20,0.22);
    }
    .kat-runko > h2:first-child { margin-top: 0; padding-top: 0; border-top: 0; }
    .kat-runko h3 { font-size: 1.06rem; margin: 1.5rem 0 0.4rem; }
    .kat-runko p { margin-bottom: 1rem; }
    .kat-runko ul, .kat-runko ol { margin: 0.8em 0 1.4em; padding-left: 1.3em; }
    .kat-runko li { margin-bottom: 0.75em; }
    .kat-runko a { color: var(--c-primary-mid, #8B6914); }

    /* Korttiruudukko pysyy tekstipalstan levyisenä — leveämpänä se irtosi
       muusta sivusta eikä mikään reuna ollut linjassa. */
    .kat-kortit {
      margin: 1.4rem 0 2.2rem;
      display: grid; grid-template-columns: repeat(auto-fill, minmax(255px, 1fr));
      gap: 0.5rem 0.45rem;
    }
    .hub-kortti { display: flex; align-items: flex-start; gap: 0.6rem; padding: 0.65rem 0.8rem;
      background: var(--c-surface, #FDFAF2); border: 1.5px solid var(--c-border, #D4C090);
      border-left: 4px solid var(--c, #2c3e50);
      text-decoration: none; color: var(--c-text, #1A1100); font-size: 0.865rem; line-height: 1.3;
      transition: border-color 0.1s, box-shadow 0.1s, transform 0.1s; }
    .hub-kortti:hover { border-color: var(--c, #2c3e50);
      box-shadow: 0 2px 10px rgba(0,0,0,0.09); transform: translateX(3px); }
    .hub-numero { flex-shrink: 0; width: 1.9em; height: 1.9em; background: var(--c, #2c3e50);
      color: #fff; font-size: 0.76em; font-weight: 700;
      display: flex; align-items: center; justify-content: center; }
    .hub-teksti { flex: 1; min-width: 0; }
    .hub-nimi { display: block; font-weight: 600; }
    .hub-kuvaus { display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;
      overflow: hidden; margin-top: 0.2em; font-size: 0.8em; line-height: 1.35;
      color: var(--c-muted, #6B5020); }
    .hub-nuoli { align-self: center; color: #d0cdc8; flex-shrink: 0; transition: color 0.1s; }
    .hub-kortti:hover .hub-nuoli { color: var(--c, #2c3e50); }

    /* ── Kategoriasta toiseen ──
       Ei vaakaswipeä: se törmää selaimen takaisin-eleeseen ja tekstin
       maalaamiseen, ja pitkällä lukusivulla peukalo liikkuu pystysuunnassa.
       Sen sijaan iso nimetty kortti siinä kohtaa, missä lukeminen loppuu. */
    .kat-siirry { margin-top: 2.6rem; padding-top: 1.6rem;
      border-top: 1px solid rgba(139,105,20,0.22); }
    .kat-siirry-parit { display: grid; gap: 0.6rem;
      grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); }
    .kat-siirry-kortti {
      display: block; padding: 0.85rem 1rem;
      background: var(--c-surface, #FDFAF2);
      border: 1.5px solid var(--c-border, #D4C090);
      border-left: 4px solid var(--c, #8B6914);
      text-decoration: none; color: var(--c-text, #1A1100);
      transition: border-color 0.12s, box-shadow 0.12s, transform 0.12s;
    }
    .kat-siirry-kortti:hover { border-color: var(--c, #8B6914);
      box-shadow: 0 2px 10px rgba(0,0,0,0.09); transform: translateY(-2px); }
    .kat-siirry-kortti.seuraava { text-align: right; }
    .kat-siirry-label {
      display: block; font-family: var(--font-ui, 'DM Sans', sans-serif);
      font-size: 0.68rem; font-weight: 600; text-transform: uppercase;
      letter-spacing: 0.14em; color: var(--c-primary-mid, #8B6914);
      margin-bottom: 0.3rem;
    }
    .kat-siirry-nimi {
      display: block; font-family: var(--font-display, 'Spectral', Georgia, serif);
      font-size: 1.05rem; font-weight: 600; line-height: 1.25;
    }
    .kat-siirry-kaikki {
      display: block; text-align: center; margin-top: 1.1rem;
      font-family: var(--font-ui, 'DM Sans', sans-serif); font-size: 0.78rem;
      letter-spacing: 0.03em; color: var(--c-primary-mid, #8B6914);
    }
    .kat-siirry-kaikki b { font-weight: 600; }

    /* ── Naapurikategoriat ── */
    .kat-naapurit { display: flex; flex-wrap: wrap; gap: 0.5rem;
      margin-top: 2.4rem; padding-top: 1.4rem;
      border-top: 1px solid rgba(139,105,20,0.22); }
    .kat-naapurit-label { flex-basis: 100%; margin: 0 0 0.25rem;
      font-family: var(--font-ui, 'DM Sans', sans-serif);
      font-size: 0.68rem; font-weight: 600; text-transform: uppercase;
      letter-spacing: 0.14em; color: var(--c-primary-mid, #8B6914); }
    .kat-naapurit a { font-size: 0.82rem; color: var(--c-primary-mid, #8B6914);
      text-decoration: none; border: 1.5px solid var(--c-border, #D4C090);
      padding: 0.4rem 0.75rem; background: var(--c-surface, #FDFAF2);
      transition: border-color 0.12s, background 0.12s; }
    .kat-naapurit a:hover { border-color: var(--c-primary-mid, #8B6914); background: #fff; }

    /* ── Laatikot ja pylväskaaviot — sama kieli kuin ilmiösivuilla ── */
    .infolaatikko { background: #f0f6fd; border-left: 6px solid #2980b9;
      padding: 1em 1.2em; margin: 1.6rem 0; }
    .huomiolaatikko { background: #fdf6ec; border-left: 6px solid #e67e22;
      padding: 1em 1.2em; margin: 1.6rem 0; }
    .infolaatikko h2.laatikko-otsikko, .huomiolaatikko h2.laatikko-otsikko {
      display: inline; font: inherit; font-weight: 700; color: inherit;
      margin: 0; padding: 0; border: 0; letter-spacing: inherit; }
    .tilasto-grid { display: flex; gap: 2rem; flex-wrap: wrap; margin: 1.5rem 0;
      align-items: flex-end; }
    .tilasto-esimerkki { flex: 1 1 200px; text-align: center; }
    .tilasto-esimerkki h4 { margin: 0 0 0.5rem; font-size: 0.9em; }
    .pylvas-wrapper { display: flex; justify-content: center; align-items: flex-end;
      gap: 0.6rem; height: 120px; border-bottom: 2px solid #333; padding: 0 0.5rem; }
    .pylvas { width: 36px; background: #2980b9; display: flex; align-items: flex-start;
      justify-content: center; font-size: 0.75em; color: #fff; padding-top: 4px; }
    .pylvas-label { font-size: 0.78em; color: #555; margin-top: 0.3rem; }

    .kat-footer { max-width: 660px; margin: 0 auto; padding: 0 1.5rem 3rem;
      font-size: 0.8rem; color: var(--c-primary-mid, #8B6914); }
    .kat-footer a { color: inherit; }

    @media (max-width: 640px) {
      .kat-masthead { padding: 0.8rem 1.2rem 2rem; }
      .kat-paluu { margin-bottom: 1.6rem; }
      .kat-runko { padding: 2rem 1.2rem 2.5rem; }
      .kat-siirry-kortti { padding: 1rem 1.1rem; }
      .kat-siirry-kortti.seuraava { text-align: left; }
    }
    @media (prefers-reduced-motion: reduce) {
      .hub-kortti, .kat-naapurit a, .kat-paluu, .kat-siirry-kortti { transition: none; }
      .hub-kortti:hover, .kat-siirry-kortti:hover { transform: none; }
    }
  </style>"""


def rakenna(slug, meta, kat, luonnos=False, edellinen=None, seuraava=None):
    etu = "../" if luonnos else ""
    runko = muotoile(meta["_runko"])
    runko = runko.replace("[[ILMIOT]]", korttilista(kat["kortit"]))
    ohita = {f"kategoria-{t['slug']}" for t in (edellinen, seuraava) if t}
    runko = runko.replace("[[NAAPURIT]]",
                          naapurilista(meta.get("naapurit", []), ohita))
    if luonnos:   # luonnoskansiosta sivuston juureen — paitsi toisiin
        #           kategoriasivuihin, jotka ovat samassa luonnoskansiossa
        runko = re.sub(r'href="(?!https?:|#|\.\./|kategoria-)', f'href="{etu}', runko)
    runko += "\n" + siirtymanavi(edellinen, seuraava, kat, etu)

    otsikko = f"{meta['otsikko']} — Ilmiöitä"
    url = f"{DOMAIN}/kategoria-{slug}.html"

    # h1 on tasan kategorian nimi; alaotsikko on oma <p> h1:n ULKOPUOLELLA.
    # Aiemmin alaotsikko oli h1:n sisällä <span>issä ilman välimerkkiä, jolloin
    # h1 luki tekstinä "Alustatalous ja algoritmitmiksi syöte…" — hakukone,
    # ruudunlukija ja LLM näkivät sanajonon, jota kukaan ei hae.
    osat = meta["h1"].split(" — ", 1)
    paaotsikko = osat[0]
    alaotsikko = (f'<p class="kat-alaotsikko">{osat[1]}</p>'
                  if len(osat) > 1 else "")
    ilmioalue = (f'<span>·</span>Ilmiöt {kat["ilmioalue"]}'
                 if kat["ilmioalue"] else "")
    return f"""<!DOCTYPE html>
<html lang="fi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" type="image/svg+xml" href="{etu}favicon.svg">
  <title>{otsikko}</title>
  <link rel="stylesheet" href="{etu}style.css?v={CSS_VERSIO}">

  <!-- SEO -->
  <meta name="description" content="{meta['kuvaus']}">
  <link rel="canonical" href="{url}">
  <meta property="og:title" content="{otsikko}">
  <meta property="og:description" content="{meta['kuvaus']}">
  <meta property="og:url" content="{url}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="fi_FI">
  <meta property="og:site_name" content="Ilmiöitä — Miten valta toimii">
  <meta property="og:image" content="{DOMAIN}/og/brand.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Ilmiöitä — Miten valta toimii">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{otsikko}">
  <meta name="twitter:description" content="{meta['kuvaus']}">
  <meta name="twitter:image" content="{DOMAIN}/og/brand.png">
{skeema(meta, kat, slug)}
{TYYLI}
</head>
<body>

  <header class="kat-masthead" style="--kat:{meta['vari']}">
    <div class="kat-masthead-sisus">
      <div class="kat-vesileima" aria-hidden="true">{kat['nro']}</div>
      <div class="kat-masthead-teksti">
        <a class="kat-paluu" href="{etu}index.html">
          <img src="{etu}favicon.svg" alt="" width="20" height="20">Kaikki ilmiöt
        </a>
        <p class="kat-eyebrow">Kategoria {kat['nro']} / {kat['kat_yhteensa']}</p>
        <h1 class="kat-nimi">{paaotsikko}</h1>
        {alaotsikko}
        <p class="kat-meta">{len(kat['kortit'])} ilmiötä{ilmioalue}<span>·</span>Päivitetty {suomipvm(meta['paivitetty'])}</p>
      </div>
    </div>
  </header>

  <main class="kat-runko">
{runko}
  </main>

  <footer class="kat-footer">
    <p>&copy; 2026 <strong>Ilmiöitä — Miten valta toimii</strong> · Kirjoittanut
    <a href="{etu}tietoa.html" rel="author">Ilmiömies</a> ·
    <a href="{etu}tietoa.html">Tietoa sivustosta ja tekijästä</a></p>
  </footer>

{selausskripti(edellinen, seuraava)}

</body>
</html>
"""


def suomipvm(iso):
    v, k, p = iso.split("-")
    return f"{int(p)}.{int(k)}.{v}"


# ──────────────────────────────── ajo ──────────────────────────────────

def main(argv):
    luonnos = "--luonnos" in argv
    valitut = [a for a in argv if not a.startswith("--")]

    kategoriat = lue_kategoriat()
    tiedostot = ([SISALTO / f"{s}.md" for s in valitut] if valitut
                 else sorted(SISALTO.glob("*.md")))
    assert tiedostot, f"ei sisältötiedostoja kansiossa {SISALTO}"

    kohdekansio = LUONNOSKANSIO if luonnos else ROOT
    kohdekansio.mkdir(exist_ok=True)

    # Edellinen/seuraava lasketaan VAIN niistä kategorioista, joilla on
    # sisältötiedosto — muuten vaiheittainen julkaisu tuottaisi 404-linkkejä.
    # Järjestys on etusivun järjestys, ei tiedostojärjestys.
    tehdyt = {p.stem for p in SISALTO.glob("*.md")}
    jarjestys = [
        {"slug": re.sub(r"-kategoria$", "", kid), "nro": k["nro"],
         "label": k["label"],
         "vari": k["kortit"][0]["vari"] if k["kortit"] else "#8B6914"}
        for kid, k in kategoriat.items()
        if re.sub(r"-kategoria$", "", kid) in tehdyt]
    sijainti = {t["slug"]: i for i, t in enumerate(jarjestys)}

    for polku in tiedostot:
        assert polku.exists(), f"puuttuu: {polku}"
        meta, meta_runko = lue_sisalto(polku)
        meta["_runko"] = meta_runko
        kat_id = meta["kat_id"]
        # Kategoria voi olla luonnos: sisältötiedosto on olemassa, mutta
        # kategoriaa ei ole vielä index.html:ssä, koska sen ilmiöitä ei ole
        # julkaistu. Massa-ajo ohittaa sellaisen; nimeltä pyydettäessä
        # puuttuva kat_id on edelleen virhe (kirjoitusvirheet kiinni).
        if kat_id not in kategoriat:
            assert not valitut, \
                f"{polku.name}: kat_id '{kat_id}' ei ole index.html:ssä"
            print(f"ohitetaan {polku.name}: kat_id '{kat_id}' ei ole vielä index.html:ssä")
            continue
        # tiedostonimi määrää URLin; muut skriptit johtavat sen kat_id:stä
        assert re.sub(r"-kategoria$", "", kat_id) == polku.stem, \
            (f"{polku.name}: tiedoston nimen pitää olla "
             f"{re.sub(r'-kategoria$', '', kat_id)}.md (kat_id '{kat_id}')")
        kat = kategoriat[kat_id]

        i = sijainti[polku.stem]
        html = rakenna(polku.stem, meta, kat, luonnos,
                       edellinen=jarjestys[i - 1] if i > 0 else None,
                       seuraava=jarjestys[i + 1] if i + 1 < len(jarjestys) else None)
        # skeeman on pysyttävä parsittavana (sama varmistus kuin paivita_maarat.py:ssä)
        for blob in re.findall(r'<script type="application/ld\+json">(.*?)</script>',
                               html, re.S):
            json.loads(blob)
        kohde = kohdekansio / f"kategoria-{polku.stem}.html"
        kohde.write_text(html, encoding="utf-8")

        sanoja = len(re.sub(r"<[^>]+>", " ", muotoile(meta_runko)).split())
        varoitus = "  ⚠ alle 300 sanaa uniikkia proosaa" if sanoja < 300 else ""
        print(f"{kohde.relative_to(ROOT)}: {len(kat['kortit'])} ilmiötä, "
              f"~{sanoja} sanaa{varoitus}")


if __name__ == "__main__":
    main(sys.argv[1:])
