#!/usr/bin/env python3
"""
E-E-A-T + meta-description cleanup pass for ilmiöt.fi.

Applies to the already-SEO-patched pages:
  H3  Rewrite truncated meta descriptions into clean, full-sentence Finnish (<=158 chars).
  H4  Add author (Ilmiömies) + datePublished/dateModified to Article JSON-LD,
      replace the "Kendom" publisher with the site's own Organization (Ilmiöitä),
      add a visible byline after the H1 and a footer with an About link.
  M2  Lengthen the 3 too-short phenomenon titles.

Idempotent: byline/footer/CSS are skipped if already present; descriptions and
schema are regenerated from source each run.

Usage: python3 scripts/seo_eeat.py
"""

import re
import json
from pathlib import Path
from bs4 import BeautifulSoup

PROJECT_DIR = Path(__file__).parent.parent
SITE = "https://www.ilmiöt.fi"
ORG = {"@type": "Organization", "name": "Ilmiöitä", "url": SITE + "/",
       "@id": SITE + "/#organization"}
AUTHOR = {"@type": "Person", "name": "Ilmiömies", "url": SITE + "/tietoa.html"}
DATE_PUBLISHED = "2026-06-16"
DATE_MODIFIED = "2026-06-19"

BYLINE = ('<p class="ilmio-byline">Kirjoittanut '
          '<a href="tietoa.html" rel="author">Ilmiömies</a> · '
          'Päivitetty 19.6.2026</p>')

FOOTER = ('  <footer class="ilmio-footer">\n'
          '    <p>© 2026 Ilmiöitä — Miten valta toimii · Kirjoittanut Ilmiömies · '
          '<a href="tietoa.html">Tietoa sivustosta ja tekijästä</a></p>\n'
          '  </footer>')

EEAT_CSS = """  <style>
    .ilmio-byline{font-size:.82rem;color:#8B6914;font-style:italic;margin:.15rem 0 1.3rem;}
    .ilmio-byline a{color:#8B6914;}
    .ilmio-footer{max-width:860px;margin:2.5rem auto 1.5rem;padding:1.3rem 1.5rem 0;
      border-top:1px solid rgba(139,105,20,.28);text-align:center;
      font-size:.8rem;color:#8B6914;line-height:1.6;}
    .ilmio-footer a{color:#8B6914;}
  </style>"""

TITLE_OVERRIDES = {
    'paskuuttaminen.html': 'Paskuuttaminen — palvelun tahallinen rapauttaminen | Ilmiöitä',
    'overton-ikkuna.html': 'Overton-ikkuna — mikä on poliittisesti mahdollista | Ilmiöitä',
    'starve-the-beast.html': 'Starve the beast — näännytä peto rahoituksesta | Ilmiöitä',
}


def clean_description(first_p, max_len=158, min_len=90):
    text = re.sub(r'\s+', ' ', first_p).strip()
    sentences = re.findall(r'[^.!?]*[.!?]', text) or [text]
    out = ""
    for s in (s.strip() for s in sentences):
        cand = (out + " " + s).strip() if out else s
        if len(cand) <= max_len:
            out = cand
        else:
            break
    # Sentence split fails on abbreviations/quotes ("C.", "(eng.", '"..."') ->
    # if the result is too short, fall back to a clean word-boundary cut.
    if len(out) < min_len and len(text) > len(out):
        cut = text[:max_len]
        idx = cut.rfind(' ')
        out = (cut[:idx] if idx > 40 else cut).rstrip(' ,;:—-') + '…'
    return out


def sub_meta(content, pattern, value):
    v = value.replace('"', '&quot;')
    return re.sub(pattern, lambda m: m.group(1) + v + m.group(2), content, count=1)


def modify_jsonld(content, fn):
    m = re.search(r'(<script type="application/ld\+json">\n)(.*?)(\n  </script>)',
                  content, re.S)
    if not m:
        return content
    data = json.loads(m.group(2))
    fn(data)
    new_json = json.dumps(data, ensure_ascii=False, indent=2)
    return content[:m.start(2)] + new_json + content[m.end(2):]


def patch_phenomenon(fp):
    content = fp.read_text(encoding='utf-8')
    soup = BeautifulSoup(content, 'html.parser')
    ilmio = soup.find(class_='ilmio')
    h1 = ilmio.find('h1') if ilmio else soup.find('h1')
    name = h1.get_text(strip=True) if h1 else fp.stem
    paras = ilmio.find_all('p') if ilmio else []
    # first non-byline paragraph
    first_p = ""
    for p in paras:
        if 'ilmio-byline' in (p.get('class') or []):
            continue
        first_p = p.get_text(separator=' ', strip=True)
        break
    desc = clean_description(first_p) if first_p else f"{name} — selitettynä."

    # Meta tags
    content = sub_meta(content, r'(<meta name="description" content=")[^"]*(">)', desc)
    content = sub_meta(content, r'(<meta property="og:description" content=")[^"]*(">)', desc)
    content = sub_meta(content, r'(<meta name="twitter:description" content=")[^"]*(">)', desc)

    # Title (M2) for the few short ones
    if fp.name in TITLE_OVERRIDES:
        content = re.sub(r'<title>.*?</title>',
                         f'<title>{TITLE_OVERRIDES[fp.name]}</title>', content, count=1)

    # JSON-LD: Article author/dates/publisher/description + DefinedTerm description
    def fix(data):
        for node in data.get('@graph', []):
            if node.get('@type') == 'Article':
                node['author'] = AUTHOR
                node['datePublished'] = DATE_PUBLISHED
                node['dateModified'] = DATE_MODIFIED
                node['publisher'] = ORG
                node['description'] = desc
                if isinstance(node.get('about'), dict):
                    node['about']['description'] = desc
    content = modify_jsonld(content, fix)

    # Byline + footer + CSS (idempotent)
    if 'ilmio-byline' not in content:
        content = content.replace('</head>', EEAT_CSS + '\n</head>', 1)
        content = content.replace('</h1>', '</h1>\n' + BYLINE, 1)
        content = content.replace('</body>', FOOTER + '\n</body>', 1)

    fp.write_text(content, encoding='utf-8')
    return name, desc


def patch_index(fp):
    content = fp.read_text(encoding='utf-8')

    def fix(data):
        for node in data.get('@graph', []):
            if node.get('@type') == 'Organization':
                node['name'] = 'Ilmiöitä'
                node['url'] = SITE + '/'
                node['@id'] = SITE + '/#organization'
            if node.get('@type') == 'CollectionPage':
                pub = node.get('publisher')
                if isinstance(pub, dict) and '@id' in pub:
                    pub['@id'] = SITE + '/#organization'
    content = modify_jsonld(content, fix)

    if 'ilmio-footer' not in content:
        content = content.replace('</head>', EEAT_CSS + '\n</head>', 1)
        content = content.replace('</body>', FOOTER + '\n</body>', 1)
    fp.write_text(content, encoding='utf-8')


def patch_random(fp):
    content = fp.read_text(encoding='utf-8')
    if 'name="robots"' not in content:
        inject = ('  <meta name="robots" content="noindex, follow">\n'
                  f'  <link rel="canonical" href="{SITE}/random.html">\n')
        content = content.replace('</head>', inject + '</head>', 1)
        fp.write_text(content, encoding='utf-8')
        return True
    return False


def main():
    count = 0
    for fp in sorted(PROJECT_DIR.glob('*.html')):
        if fp.name == 'index.html':
            patch_index(fp)
            print(f"  index: footer + de-Kendom Organization")
        elif fp.name == 'random.html':
            r = patch_random(fp)
            print(f"  random: noindex {'added' if r else '(already)'}")
        else:
            name, desc = patch_phenomenon(fp)
            count += 1
            print(f"  {fp.name}: {desc[:70]}...")
    print(f"\nDone: {count} phenomenon pages + index + random.")


if __name__ == '__main__':
    main()
