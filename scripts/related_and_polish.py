#!/usr/bin/env python3
"""
H2 (related-phenomena internal links) + date refresh + Mermaid CLS mitigation.

- Adds a "Liittyvät ilmiöt" block (4–5 same-category links) to each phenomenon page.
- Sets Article datePublished/dateModified to today (2026-06-19).
- Adds .liittyvat + .mermaid CSS to the shared style.css.

Idempotent: the related block is skipped if already present.
"""
import re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).parent.parent
TODAY = "2026-06-19"

CATEGORIES = {
    "Vallan rakenteet": ["paskuuttaminen", "starve-the-beast", "overton-ikkuna",
        "saantelijan-kaappaus", "rautainen-laki", "valta-suojelee-valtaa", "hajota-hallitse"],
    "Informaatio ja propaganda": ["tilastoilla-valehtelu", "bkt-harha", "astroturf",
        "firehose-of-falsehood", "manufactured-consent", "betteridgen-laki", "inokulointiteoria"],
    "Psykologia ja kognitio": ["backfire-effect", "darvo", "halo-efekti", "konsensus-fetissi",
        "omenoita-appelsiineja", "blame-game", "gaslighting", "maalitolppien-siirtaminen",
        "argumenttitulva", "sunk-cost-harha", "jarjestelman-puolustelu"],
    "Byrokratia ja organisaatio": ["simple-sabotage", "kafka-ilmio", "catch-22", "goodhartin-laki",
        "hippo-efekti", "performatiivinen-lasnaolo", "rituaalinen-raportointi", "initiointirituaalit",
        "portinvartija-kulttuuri", "strateginen-osaamattomuus", "fofo", "sivustakatsojan-efekti"],
    "Projekti- ja ohjelmistokehitys": ["brooksin-laki", "yhdeksanyhdeksan", "hofstadterin-laki",
        "kuolonmarssi", "tekninen-velka", "conways-laki", "bikeshedding", "scope-creep"],
    "Kasvun dynamiikka": ["korkoa-korolle", "negatiivinen-korkoa", "korkokierre"],
    "Huijaukset ja petokset": ["honeypot-huijaus", "bait-and-switch", "kaarmeoljy", "ponzi-pyramidi",
        "pump-and-dump", "pig-butchering", "ennakkomaksuhuijaus", "badger-game"],
    "Myyntikikat ja painostus": ["ilmainen-naytetyo", "exposure-maksu", "lowball-hinnoittelu",
        "valittajan-skimmaus", "tilipuristus", "foot-in-the-door", "door-in-the-face",
        "hintaankkurointi", "houkutinvaihtoehto", "vastavuoroisuuden-ansa", "sosiaalinen-todiste",
        "painostusclose"],
}
CAT_OF = {s: c for c, slugs in CATEGORIES.items() for s in slugs}
ALL_ORDER = [s for slugs in CATEGORIES.values() for s in slugs]

CSS = """
/* H2: liittyvät ilmiöt -lohko */
.liittyvat { margin: 2.2rem 0 0; padding: 1.4rem 1.6rem; background: #FDFAF2;
  border: 1px solid #D4C090; border-left: 4px solid #C9A84C; }
.liittyvat h2 { font-family: 'Spectral', Georgia, serif; font-size: 1.15rem;
  color: #1C1400; margin: 0 0 0.85rem; }
.liittyvat ul { list-style: none; margin: 0; padding: 0; display: flex;
  flex-wrap: wrap; gap: 0.5rem 0.6rem; }
.liittyvat li { margin: 0; }
.liittyvat a { display: inline-block; color: #8B6914; text-decoration: none;
  font-size: 0.9rem; padding: 0.32rem 0.7rem; border: 1px solid #D4C090;
  background: #fff; transition: border-color .12s, color .12s; }
.liittyvat a:hover { border-color: #C9A84C; color: #1C1400; }

/* CLS: varaa tila Mermaid-diagrammeille ennen renderöintiä */
.mermaid { min-height: 220px; display: flex; align-items: center; justify-content: center; }
.mermaid svg { max-width: 100%; height: auto; }
"""


def related_for(slug):
    members = CATEGORIES[CAT_OF[slug]]
    i = members.index(slug)
    rel = [members[(i + k) % len(members)] for k in range(1, min(6, len(members)))]
    if len(rel) < 4:
        gi = ALL_ORDER.index(slug)
        k = 1
        while len(rel) < 4 and k < len(ALL_ORDER):
            cand = ALL_ORDER[(gi + k) % len(ALL_ORDER)]
            if cand != slug and cand not in rel:
                rel.append(cand)
            k += 1
    return rel[:5]


def main():
    # Pass 1: collect display names from each <h1>
    name = {}
    for slug in ALL_ORDER:
        fp = ROOT / f"{slug}.html"
        soup = BeautifulSoup(fp.read_text(encoding='utf-8'), 'html.parser')
        ilmio = soup.find(class_='ilmio')
        h1 = (ilmio or soup).find('h1')
        name[slug] = h1.get_text(strip=True) if h1 else slug

    # Shared CSS
    css = ROOT / "style.css"
    c = css.read_text(encoding='utf-8')
    if '.liittyvat' not in c:
        css.write_text(c.rstrip() + "\n" + CSS, encoding='utf-8')
        print("style.css: .liittyvat + .mermaid rules added")

    # Pass 2: insert related block + fix dates
    related = dated = 0
    for slug in ALL_ORDER:
        fp = ROOT / f"{slug}.html"
        txt = fp.read_text(encoding='utf-8')
        orig = txt

        # Dates -> today
        txt = txt.replace('"datePublished": "2026-06-16"', f'"datePublished": "{TODAY}"')
        if '"datePublished"' in txt and TODAY in txt:
            dated += 1

        # Related block
        if 'class="liittyvat"' not in txt and '<nav class="kortti-nav">' in txt:
            items = "\n".join(
                f'      <li><a href="{r}.html">{name[r]}</a></li>' for r in related_for(slug))
            block = ('  <aside class="liittyvat" aria-label="Liittyvät ilmiöt">\n'
                     '    <h2>Liittyvät ilmiöt</h2>\n'
                     f'    <ul>\n{items}\n    </ul>\n'
                     '  </aside>\n\n')
            txt = txt.replace('  <nav class="kortti-nav">', block + '  <nav class="kortti-nav">', 1)
            related += 1

        if txt != orig:
            fp.write_text(txt, encoding='utf-8')

    print(f"related blocks added: {related} | dates set to {TODAY}: {dated}")


if __name__ == '__main__':
    main()
