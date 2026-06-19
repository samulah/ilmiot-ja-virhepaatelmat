#!/usr/bin/env python3
"""
SEO patch script for kendom.fi/ilmiöt/
Adds meta descriptions, canonical tags, OG tags, JSON-LD schema to all pages.
Promotes first H2 to H1 on individual ilmiö pages.
Adds Mermaid defer and Google Fonts gstatic preconnect.

Idempotent: skips files that already have a canonical tag.

Usage: python3 scripts/seo_patch.py
"""

import os
import re
import json
from pathlib import Path
from bs4 import BeautifulSoup

BASE_URL = "https://kendom.fi/ilmiöt/"
SITE_NAME = "Ilmiöitä — Miten valta toimii"
PROJECT_DIR = Path(__file__).parent.parent


def get_text_clean(tag):
    if not tag:
        return ""
    return re.sub(r'\s+', ' ', tag.get_text(separator=' ', strip=True)).strip()


def truncate_description(text, max_len=155):
    if len(text) <= max_len:
        return text
    cut = text[:max_len]
    # Try to cut at a natural boundary
    for sep in ['. ', ' — ', ', ', ' ']:
        idx = cut.rfind(sep)
        if idx > max_len - 50:
            return cut[:idx + (1 if sep == '. ' else 0)].rstrip()
    return cut.rstrip('.,; ') + '…'


def build_ilmio_seo_block(name, description, canonical_url, category):
    og_title = f"{name} — Ilmiöitä"
    canonical_encoded = canonical_url.replace('ö', '%C3%B6')

    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Ilmiöitä", "item": BASE_URL},
                    {"@type": "ListItem", "position": 2, "name": category},
                    {"@type": "ListItem", "position": 3, "name": name, "item": canonical_url}
                ]
            },
            {
                "@type": "Article",
                "@id": canonical_url + "#article",
                "url": canonical_url,
                "headline": name,
                "description": description,
                "inLanguage": "fi",
                "articleSection": category,
                "isPartOf": {
                    "@type": "CollectionPage",
                    "@id": BASE_URL
                },
                "publisher": {
                    "@type": "Organization",
                    "name": "Kendom",
                    "url": "https://kendom.fi/"
                },
                "about": {
                    "@type": "DefinedTerm",
                    "name": name,
                    "description": description,
                    "inDefinedTermSet": {
                        "@type": "DefinedTermSet",
                        "name": SITE_NAME,
                        "@id": BASE_URL
                    }
                }
            }
        ]
    }

    schema_json = json.dumps(schema, ensure_ascii=False, indent=2)
    desc_escaped = description.replace('"', '&quot;')
    og_title_escaped = og_title.replace('"', '&quot;')

    return f"""
  <!-- SEO -->
  <meta name="description" content="{desc_escaped}">
  <link rel="canonical" href="{canonical_url}">
  <meta property="og:title" content="{og_title_escaped}">
  <meta property="og:description" content="{desc_escaped}">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:type" content="article">
  <meta property="og:locale" content="fi_FI">
  <meta property="og:site_name" content="{SITE_NAME}">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{og_title_escaped}">
  <meta name="twitter:description" content="{desc_escaped}">
  <style>.ilmio h1{{margin-top:0;font-family:'Spectral',Georgia,serif;}}</style>
  <script type="application/ld+json">
{schema_json}
  </script>"""


def patch_ilmio_page(filepath):
    content = filepath.read_text(encoding='utf-8')

    if '<link rel="canonical"' in content:
        print(f"  SKIP (already patched): {filepath.name}")
        return False

    soup = BeautifulSoup(content, 'html.parser')

    filename = filepath.name
    canonical_url = f"{BASE_URL}{filename}"

    # Extract ilmiö name from first h2 in .ilmio div
    ilmio_div = soup.find(class_='ilmio')
    h2 = ilmio_div.find('h2') if ilmio_div else soup.find('h2')
    name = get_text_clean(h2) if h2 else filepath.stem.replace('-', ' ').title()

    # Category from breadcrumb
    category_tag = soup.find(class_='kortti-breadcrumb-kat')
    category = get_text_clean(category_tag) if category_tag else ""

    # First paragraph text for description
    first_p_text = ""
    if ilmio_div:
        paras = ilmio_div.find_all('p', recursive=False)
        if not paras:
            paras = ilmio_div.find_all('p')
        if paras:
            first_p_text = get_text_clean(paras[0])

    if first_p_text:
        desc_raw = f"{name}: {first_p_text}"
    else:
        desc_raw = f"{name} — {category}. Kendom selittää tämän ilmiön mekanismin, tunnistamisen ja esimerkit."

    description = truncate_description(desc_raw)

    # Build and insert SEO block before </head>
    seo_block = build_ilmio_seo_block(name, description, canonical_url, category)
    new_content = content.replace('</head>', seo_block + '\n</head>', 1)

    # Promote first H2 in body to H1
    body_idx = new_content.find('<body')
    if body_idx != -1 and h2:
        after_body = new_content[body_idx:]
        # Replace first <h2> occurrence (no attributes expected on these tags)
        after_body = after_body.replace('<h2>', '<h1>', 1)
        after_body = after_body.replace('</h2>', '</h1>', 1)
        new_content = new_content[:body_idx] + after_body

    # Add defer to Mermaid script
    new_content = re.sub(
        r'<script src="(https://cdn\.jsdelivr\.net/npm/mermaid[^"]*)"',
        r'<script defer src="\1"',
        new_content
    )

    # Add gstatic preconnect if missing
    if 'fonts.googleapis.com' in new_content and 'fonts.gstatic.com' not in new_content:
        new_content = new_content.replace(
            '<link rel="preconnect" href="https://fonts.googleapis.com">',
            '<link rel="preconnect" href="https://fonts.googleapis.com">\n  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
            1
        )

    filepath.write_text(new_content, encoding='utf-8')
    print(f"  PATCHED: {filepath.name} — {name}")
    return True


HUB_DESC = (
    "Ilmiöitä — 68 sosiaalista ilmiötä selitettynä: valtarakenteet, propaganda, "
    "kognitiiviset harhat, byrokratia, projektihallinnan lait, myyntikikat ja petokset. "
    "Suomenkielinen tietopankki."
)

HUB_ITEM_LIST = [
    (1,  "Paskuuttaminen", "paskuuttaminen.html"),
    (2,  "Starve the beast", "starve-the-beast.html"),
    (3,  "Overton-ikkuna", "overton-ikkuna.html"),
    (4,  "Sääntelijän kaappaus", "saantelijan-kaappaus.html"),
    (5,  "Rautainen laki oligarkiasta — organisaatioiden väistämätön mätäneminen", "rautainen-laki.html"),
    (6,  "Valta suojelee valtaa", "valta-suojelee-valtaa.html"),
    (7,  "Hajota ja hallitse — divide et impera", "hajota-hallitse.html"),
    (8,  "Tilastoilla valehtelu — visuaaliset ansat", "tilastoilla-valehtelu.html"),
    (9,  "BKT-harha — Irlannin paradoksi", "bkt-harha.html"),
    (10, "Astroturf — keinotekoinen kansanliike", "astroturf.html"),
    (11, "Firehose of falsehood — valheiden paloletku", "firehose-of-falsehood.html"),
    (12, "Manufactured consent — suostumus tehdään", "manufactured-consent.html"),
    (13, 'Betteridgen laki — kysymysmerkki tarkoittaa "ei"', "betteridgen-laki.html"),
    (14, "Inokulointiteoria — mentaalinen rokotus", "inokulointiteoria.html"),
    (15, "Backfire effect — väärinkäsityksen vahvistuminen", "backfire-effect.html"),
    (16, "DARVO — uhrin ja syyttäjän roolien kääntäminen", "darvo.html"),
    (17, "Halo-efekti ja stigma — ensivaikutelman loukku", "halo-efekti.html"),
    (18, "Konsensus fetissi — kun yksimielisyydestä tulee itseisarvo", "konsensus-fetissi.html"),
    (19, "Omenoita ja appelsiineja — vertailun harha", "omenoita-appelsiineja.html"),
    (20, "The Blame Game — syyttelyn kehä", "blame-game.html"),
    (21, "Gaslighting — todellisuuden järjestelmällinen kiistäminen", "gaslighting.html"),
    (22, "Maalitolppien siirtäminen — liikkuva maaliviiva", "maalitolppien-siirtaminen.html"),
    (23, "Argumenttitulva — Gish Gallop", "argumenttitulva.html"),
    (24, "Sunk cost -harha — upponneiden kustannusten loukku", "sunk-cost-harha.html"),
    (25, "Järjestelmän puolustelu — menestyneen puolesta taisteleva häviäjä", "jarjestelman-puolustelu.html"),
    (26, "Simple Sabotage Field Manual (1944)", "simple-sabotage.html"),
    (27, "Kafka-ilmiö — byrokratian labyrintti", "kafka-ilmio.html"),
    (28, "Catch-22 — pakenematon ansa", "catch-22.html"),
    (29, "Goodhartin laki — mittari syö tavoitteen", "goodhartin-laki.html"),
    (30, "HIPPO-efekti — johtajan mielipide voittaa datan", "hippo-efekti.html"),
    (31, "Performatiivinen läsnäolo — näytelmä sitoutumisesta", "performatiivinen-lasnaolo.html"),
    (32, "Rituaalinen raportointi — kontrollin näytelmä", "rituaalinen-raportointi.html"),
    (33, "Initiointirituaalit — hierarkian naturalisointi", "initiointirituaalit.html"),
    (34, "Portinvartija-kulttuuri — tieto suodattuu ennen johtajaa", "portinvartija-kulttuuri.html"),
    (35, "Strateginen osaamattomuus — välineellistetty epäpätevyys", "strateginen-osaamattomuus.html"),
    (36, "FOFO — pelko löytää totuus", "fofo.html"),
    (37, "Sivustakatsojan efekti — vastuun hajoaminen", "sivustakatsojan-efekti.html"),
    (38, "Brooksin laki — lisähenkilö myöhästyttää", "brooksin-laki.html"),
    (39, 'Yhdeksän-yhdeksän-sääntö — "melkein valmis" -illuusio', "yhdeksanyhdeksan.html"),
    (40, "Hofstadterin laki — rekursiivinen aikataululaki", "hofstadterin-laki.html"),
    (41, "Kuolonmarssi — projekti jota ei voi lopettaa", "kuolonmarssi.html"),
    (42, "Tekninen velka — oikoteiden korko", "tekninen-velka.html"),
    (43, "Conwayn laki — organisaatio heijastuu arkkitehtuuriin", "conways-laki.html"),
    (44, "Bikeshedding — triviaalisuuslaki", "bikeshedding.html"),
    (45, "Scope creep — vaatimusten hiljaa laajeneminen", "scope-creep.html"),
    (46, "Korkoa korolle -efekti — eksponentiaalinen kasvu", "korkoa-korolle.html"),
    (47, "Negatiivinen korkoa korolle — eksponentiaalinen hajoaminen", "negatiivinen-korkoa.html"),
    (48, "Negatiivinen korkokierre — velkaeksponentti 30 vuodessa", "korkokierre.html"),
    (49, "Honeypot-huijaus — ansa josta pääsee sisään muttei ulos", "honeypot-huijaus.html"),
    (50, "Bait and switch — syötti ja vaihto", "bait-and-switch.html"),
    (51, "Käärmeöljy — ihmetuote joka parantaa kaiken", "kaarmeoljy.html"),
    (52, "Ponzi ja pyramidihuijaus — tuotot tulevat uusilta uhreilta", "ponzi-pyramidi.html"),
    (53, "Pump and dump — pumppaa ja dumppaa", "pump-and-dump.html"),
    (54, "Pig butchering — uhrin lihottaminen ennen teurastusta", "pig-butchering.html"),
    (55, "Ennakkomaksuhuijaus (419) — maksa vähän saadaksesi paljon", "ennakkomaksuhuijaus.html"),
    (56, "Badger game — houkuttele kiusalliseen tilanteeseen, kiristä vaikenemisesta", "badger-game.html"),
    (57, 'Ilmainen näytetyö — "tee koetehtävä, valitsemme parhaan"', "ilmainen-naytetyo.html"),
    (58, 'Maksu näkyvyydellä — "tästä saat hyvää referenssiä"', "exposure-maksu.html"),
    (59, "Lowball — matala aloitushinta, joka nousee sitoutumisen jälkeen", "lowball-hinnoittelu.html"),
    (60, "Välittäjän skimmaus — siivu molemmilta, marginaali piilossa", "valittajan-skimmaus.html"),
    (61, "Tilipuristus — maksun viivytys aseena", "tilipuristus.html"),
    (62, "Foot-in-the-door — pieni myönnytys avaa oven suuremmalle", "foot-in-the-door.html"),
    (63, 'Door-in-the-face — kohtuuton pyyntö ensin, "kohtuullinen" perään', "door-in-the-face.html"),
    (64, "Hintaankkurointi — ensimmäinen luku ohjaa koko neuvottelua", "hintaankkurointi.html"),
    (65, "Houkutinvaihtoehto — tahallaan huono vaihtoehto ohjaa valintaa", "houkutinvaihtoehto.html"),
    (66, "Vastavuoroisuuden ansa — ilmainen lahja luo velan", "vastavuoroisuuden-ansa.html"),
    (67, 'Sosiaalinen todiste -manipulaatio — "muutkin jo ostivat"', "sosiaalinen-todiste.html"),
    (68, 'Painostus-close — keinotekoinen niukkuus ja "nyt tai ei koskaan"', "painostusclose.html"),
]


def build_hub_schema():
    item_list_elements = [
        {
            "@type": "ListItem",
            "position": pos,
            "name": name,
            "url": f"{BASE_URL}{slug}"
        }
        for pos, name, slug in HUB_ITEM_LIST
    ]

    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebSite",
                "@id": "https://kendom.fi/#website",
                "name": "Kendom",
                "url": "https://kendom.fi/",
                "inLanguage": "fi"
            },
            {
                "@type": "Organization",
                "@id": "https://kendom.fi/#organization",
                "name": "Kendom",
                "url": "https://kendom.fi/"
            },
            {
                "@type": "CollectionPage",
                "@id": f"{BASE_URL}#collectionpage",
                "url": BASE_URL,
                "name": SITE_NAME,
                "description": HUB_DESC,
                "inLanguage": "fi",
                "isPartOf": {"@id": "https://kendom.fi/#website"},
                "publisher": {"@id": "https://kendom.fi/#organization"},
                "mainEntity": {
                    "@type": "ItemList",
                    "@id": f"{BASE_URL}#itemlist",
                    "name": "Kaikki ilmiöt",
                    "numberOfItems": 68,
                    "itemListElement": item_list_elements
                }
            }
        ]
    }
    return json.dumps(schema, ensure_ascii=False, indent=2)


def patch_index_page(filepath):
    content = filepath.read_text(encoding='utf-8')

    if '<link rel="canonical"' in content:
        print(f"  SKIP (already patched): {filepath.name}")
        return False

    hub_url = BASE_URL
    desc_escaped = HUB_DESC.replace('"', '&quot;')
    schema_json = build_hub_schema()

    hub_seo = f"""
  <!-- SEO -->
  <meta name="description" content="{desc_escaped}">
  <link rel="canonical" href="{hub_url}">
  <meta property="og:title" content="{SITE_NAME}">
  <meta property="og:description" content="{desc_escaped}">
  <meta property="og:url" content="{hub_url}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="fi_FI">
  <meta property="og:site_name" content="{SITE_NAME}">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{SITE_NAME}">
  <meta name="twitter:description" content="{desc_escaped}">
  <script type="application/ld+json">
{schema_json}
  </script>"""

    new_content = content.replace('</head>', hub_seo + '\n</head>', 1)

    # Convert .hub-kat-label <p> tags to <h2>
    new_content = re.sub(
        r'<p class="hub-kat-label">([^<]+)</p>',
        r'<h2 class="hub-kat-label">\1</h2>',
        new_content
    )

    # Add gstatic preconnect if missing
    if 'fonts.googleapis.com' in new_content and 'fonts.gstatic.com' not in new_content:
        new_content = new_content.replace(
            '<link rel="preconnect" href="https://fonts.googleapis.com">',
            '<link rel="preconnect" href="https://fonts.googleapis.com">\n  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
            1
        )

    filepath.write_text(new_content, encoding='utf-8')
    print(f"  PATCHED: {filepath.name} (hub page)")
    return True


def main():
    print(f"SEO patch — project: {PROJECT_DIR}")
    patched = 0
    skipped = 0

    html_files = sorted(PROJECT_DIR.glob("*.html"))

    for html_file in html_files:
        if html_file.name == "random.html":
            continue
        elif html_file.name == "index.html":
            result = patch_index_page(html_file)
        else:
            result = patch_ilmio_page(html_file)

        if result:
            patched += 1
        else:
            skipped += 1

    print(f"\nDone: {patched} patched, {skipped} skipped.")


if __name__ == "__main__":
    main()
