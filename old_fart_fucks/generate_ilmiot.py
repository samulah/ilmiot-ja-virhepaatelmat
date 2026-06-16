#!/usr/bin/env python3
"""Generoi yksittäiset ilmiösivut index.html:stä -> ilmiot/"""

import os
import re
from bs4 import BeautifulSoup

INDEX_PATH = os.path.join(os.path.dirname(__file__), 'index.html')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'ilmiot')

# Chart.js canvas ID -> kortti ID -kartoitus
CANVAS_TO_CARD = {
    'kkk-kasvu-graafi': 'korkoa-korolle',
    'ebbinghaus-graafi': 'negatiivinen-korkoa',
    'velka-graafi': 'negatiivinen-korkoa',
    'korkokierre-graafi': 'korkokierre',
}
CHART_CARDS = set(CANVAS_TO_CARD.values())


def load_source():
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        return f.read()


def extract_inline_css(soup):
    style_tag = soup.find('style')
    return style_tag.string if style_tag else ''


def extract_scripts(soup):
    """Palauttaa (chartjs_block, share_block) merkkijonoina."""
    chartjs = ''
    share = ''
    for script in soup.find_all('script'):
        src = script.get('src', '')
        if src:
            continue
        text = script.string or ''
        if 'kkk-kasvu-graafi' in text or ("new Chart" in text and "ebbinghaus" in text):
            chartjs = text
        elif 'ilmio-jaa' in text or 'pageUrl' in text:
            share = text
    return chartjs, share


def make_chartjs_safe(js):
    """Lisää null-tarkistus jokaiseen new Chart(...) kutsuun."""
    for canvas_id in CANVAS_TO_CARD:
        safe = canvas_id.replace('-', '_')
        old = f"new Chart(document.getElementById('{canvas_id}'), {{"
        new_ = (
            f"var _{safe} = document.getElementById('{canvas_id}');\n"
            f"  if (_{safe}) new Chart(_{safe}, {{"
        )
        js = js.replace(old, new_)
    return js


def extract_card_colors(css):
    """Kerää id -> accent-väri CSS:stä."""
    colors = {}
    for m in re.finditer(r'#([\w-]+)\s*\{[^}]*border-top-color:\s*(#[0-9a-fA-F]{3,6})', css):
        colors[m.group(1)] = m.group(2)
    return colors


def get_categories(soup):
    """Palauttaa dict {card_id: category_name}."""
    cats = {}
    for hak in soup.select('.hak-kategoria'):
        otsikko_el = hak.find(class_='hak-otsikko')
        cat = otsikko_el.get_text(strip=True) if otsikko_el else ''
        for a in hak.find_all('a', href=True):
            href = a['href']
            if href.startswith('#'):
                cats[href[1:]] = cat
    return cats


def get_card_number(card):
    tag = card.find(class_='ilmio-tag')
    if tag:
        m = re.search(r'\d+', tag.get_text())
        if m:
            return int(m.group())
    return 0


def fix_share_widget(share_js):
    """Yksittäisillä sivuilla jaetaan sivun URL itsessään."""
    return share_js.replace(
        "window.location.href.split('#')[0] + '#' + id",
        "window.location.href.split('#')[0]"
    )


def build_page(card, prev_card, next_card, n, total, all_card_ids,
               inline_css, chartjs_block, share_js, categories, card_colors):
    card_id = card['id']
    h2 = card.find('h2')
    title = h2.get_text(strip=True) if h2 else card_id
    cat = categories.get(card_id, '')
    accent = card_colors.get(card_id, '#2c3e50')
    has_mermaid = bool(card.find(class_='mermaid'))
    has_canvas = bool(card.find('canvas'))

    prev_url = f'{prev_card["id"]}.html' if prev_card else ''
    next_url = f'{next_card["id"]}.html' if next_card else ''

    # Prev/next nav
    if prev_card is not None:
        prev_h2 = prev_card.find('h2')
        prev_title = prev_h2.get_text(strip=True) if prev_h2 else prev_card['id']
        prev_link = f'<a class="kortti-nav-btn" href="{prev_url}">← {prev_title}</a>'
    else:
        prev_link = '<span class="kortti-nav-btn disabled">←</span>'

    if next_card is not None:
        next_h2 = next_card.find('h2')
        next_title = next_h2.get_text(strip=True) if next_h2 else next_card['id']
        next_link = f'<a class="kortti-nav-btn" href="{next_url}">{next_title} →</a>'
    else:
        next_link = '<span class="kortti-nav-btn disabled">→</span>'

    mermaid_cdn = ''
    mermaid_init = ''
    if has_mermaid:
        mermaid_cdn = '<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>'
        mermaid_init = "<script>mermaid.initialize({ startOnLoad: true, themeVariables: { fontSize: '12px' } });</script>"

    chartjs_cdn = ''
    chartjs_init = ''
    if has_canvas:
        chartjs_cdn = '<script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script>'
        chartjs_init = f'<script>\n(function () {{\n{chartjs_block}\n}})();\n</script>'

    card_html = str(card)
    cat_breadcrumb = f'<span class="kortti-breadcrumb-sep">›</span><span class="kortti-breadcrumb-kat">{cat}</span>' if cat else ''

    # JS-taulukko kaikista ID:istä (satunnainen + näppäimistönavigointi)
    ids_js = '[' + ','.join(f'"{i}"' for i in all_card_ids) + ']'

    page = f"""<!DOCTYPE html>
<html lang="fi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — Ilmiöitä</title>
  <link rel="stylesheet" href="../style.css">
  {mermaid_cdn}
  {mermaid_init}
  {chartjs_cdn}
  <style>
{inline_css}

    /* Yksilösivun navigointi */
    .kortti-breadcrumb {{
      font-size: 0.85em;
      color: #888;
      margin-bottom: 1.2rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      flex-wrap: wrap;
    }}
    .kortti-breadcrumb a {{ color: #2980b9; text-decoration: none; }}
    .kortti-breadcrumb a:hover {{ text-decoration: underline; }}
    .kortti-breadcrumb-sep {{ color: #ccc; }}
    .kortti-breadcrumb-kat {{ color: #666; }}
    .kortti-random-btn {{
      margin-left: auto;
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      background: #2c3e50;
      color: #fff;
      border: none;
      border-radius: 6px;
      padding: 0.3rem 0.75rem;
      font-size: 0.82em;
      font-family: inherit;
      font-weight: 600;
      cursor: pointer;
      text-decoration: none;
      transition: background 0.12s;
      white-space: nowrap;
    }}
    .kortti-random-btn:hover {{ background: #1a252f; }}
    .kortti-random-btn:active {{ transform: scale(0.97); }}

    .kortti-nav {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.75rem;
      margin-top: 2rem;
      padding: 1rem 0;
      border-top: 1px solid #e0e4e8;
    }}
    .kortti-nav-btn {{
      display: inline-block;
      background: #f5f4f0;
      color: #333;
      border: 1px solid #ddd;
      border-radius: 6px;
      padding: 0.5rem 0.9rem;
      font-size: 0.85em;
      text-decoration: none;
      cursor: pointer;
      transition: background 0.12s;
      max-width: 42%;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }}
    .kortti-nav-btn:hover {{ background: #eae8e2; }}
    .kortti-nav-btn.disabled {{ opacity: 0.35; pointer-events: none; }}
    .kortti-nav-center {{
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 0.3rem;
      flex-shrink: 0;
    }}
    .kortti-nav-laskuri {{ color: #999; font-size: 0.78em; white-space: nowrap; }}
    .kortti-nav-vinkki {{
      font-size: 0.7em;
      color: #ccc;
    }}
    .kortti-nav-vinkki kbd {{
      background: #f0ede8;
      border: 1px solid #ddd;
      border-bottom-width: 2px;
      border-radius: 3px;
      padding: 0.05em 0.35em;
      font-family: inherit;
      color: #888;
    }}
    .touch-vinkki {{ display: none; }}

    /* ── Mobiili ── */
    @media (max-width: 560px) {{
      .kortti-nav-btn {{ max-width: 36%; padding: 0.55rem 0.6rem; font-size: 0.8em; }}
    }}
    @media (max-width: 480px) {{
      .kortti-breadcrumb-sep, .kortti-breadcrumb-kat {{ display: none; }}
      .kortti-random-btn .btn-text {{ display: none; }}
      .kortti-random-btn {{ padding: 0.35rem 0.6rem; }}
    }}
    @media (pointer: coarse) {{
      .touch-vinkki {{ display: inline; }}
      .kortti-nav-vinkki kbd {{ display: none; }}
      /* Isommat kosketusalueet */
      .kortti-nav-btn {{ padding: 0.65rem 0.9rem; }}
      .kortti-random-btn {{ padding: 0.4rem 0.8rem; }}
    }}

    body {{ max-width: 860px; margin: 0 auto; padding: 2rem 1.5rem 4rem; }}
    .ilmio {{ margin-bottom: 0; }}
  </style>
</head>
<body>

  <div class="kortti-breadcrumb">
    <a href="index.html">← Kaikki ilmiöt</a>
    {cat_breadcrumb}
    <button class="kortti-random-btn" onclick="randomIlmio()" title="Satunnainen ilmiö (R)">
      <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="16 3 21 3 21 8"/><line x1="4" y1="20" x2="21" y2="3"/><polyline points="21 16 21 21 16 21"/><line x1="15" y1="15" x2="21" y2="21"/></svg>
      <span class="btn-text">Satunnainen</span>
    </button>
  </div>

  {card_html}

  <nav class="kortti-nav">
    {prev_link}
    <div class="kortti-nav-center">
      <span class="kortti-nav-laskuri">{n} / {total}</span>
      <span class="kortti-nav-vinkki">
        <kbd>&#8592;</kbd> <kbd>&#8594;</kbd> selaa &middot; <kbd>R</kbd> satunnainen
        <span class="touch-vinkki">&nbsp;· swipe &#8592;&#8594; tai &#8595; random</span>
      </span>
    </div>
    {next_link}
  </nav>

  {chartjs_init}

  <script>
{share_js}
  </script>

  <script>
(function () {{
  const IDS = {ids_js};
  const PREV = '{prev_url}';
  const NEXT = '{next_url}';

  function randomIlmio() {{
    let id;
    do {{ id = IDS[Math.floor(Math.random() * IDS.length)]; }} while (id === '{card_id}');
    window.location.href = id + '.html';
  }}
  window.randomIlmio = randomIlmio;

  /* ── Näppäimistö ── */
  document.addEventListener('keydown', function (e) {{
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    if (e.key === 'ArrowLeft'  && PREV) window.location.href = PREV;
    if (e.key === 'ArrowRight' && NEXT) window.location.href = NEXT;
    if (e.key === 'r' || e.key === 'R') randomIlmio();
  }});

  /* ── Swipe-eleet ── */
  var _tx = 0, _ty = 0;
  document.addEventListener('touchstart', function (e) {{
    _tx = e.touches[0].clientX;
    _ty = e.touches[0].clientY;
  }}, {{ passive: true }});
  document.addEventListener('touchend', function (e) {{
    var dx = e.changedTouches[0].clientX - _tx;
    var dy = e.changedTouches[0].clientY - _ty;
    var adx = Math.abs(dx), ady = Math.abs(dy);
    if (adx > ady * 1.5 && adx > 50) {{
      /* Horisontaalinen swipe */
      if (dx < 0 && NEXT) window.location.href = NEXT;  /* ← next */
      if (dx > 0 && PREV) window.location.href = PREV;  /* → prev */
    }} else if (ady > adx * 1.5 && ady > 80) {{
      if (dy > 0) {{
        /* Swipe alas (sormi alas) sivun pohjalla → random */
        var atBottom = window.scrollY + window.innerHeight >=
          document.documentElement.scrollHeight - 60;
        if (atBottom) randomIlmio();
      }} else {{
        /* Swipe ylös (sormi ylös) sivun yläosassa → takaisin */
        if (window.scrollY < 60) history.back();
      }}
    }}
  }}, {{ passive: true }});
}})();
  </script>

</body>
</html>"""
    return page


def build_hub(cards, categories, card_colors):
    # Ryhmittele kategorioittain järjestyksessä
    cat_order = []
    cat_cards = {}
    for card in cards:
        cid = card['id']
        cat = categories.get(cid, 'Muut')
        if cat not in cat_cards:
            cat_order.append(cat)
            cat_cards[cat] = []
        cat_cards[cat].append(card)

    sections_html = ''
    for cat in cat_order:
        cards_in_cat = cat_cards[cat]
        cards_html = ''
        for card in cards_in_cat:
            cid = card['id']
            h2 = card.find('h2')
            title = h2.get_text(strip=True) if h2 else cid
            num = get_card_number(card)
            accent = card_colors.get(cid, '#2c3e50')
            cards_html += (
                f'<a href="{cid}.html" class="hub-kortti" style="--c:{accent}">\n'
                f'  <span class="hub-numero">{num}</span>\n'
                f'  <span class="hub-nimi">{title}</span>\n'
                f'  <span class="hub-nuoli" aria-hidden="true">›</span>\n'
                f'</a>\n'
            )
        sections_html += (
            f'<div class="hub-kategoria">\n'
            f'  <p class="hub-kat-label">{cat}</p>\n'
            f'  <div class="hub-kortit">\n{cards_html}  </div>\n'
            f'</div>\n'
        )

    total = len(cards)
    return f"""<!DOCTYPE html>
<html lang="fi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Ilmiöitä — Miten valta toimii</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      font-family: 'Source Sans 3', system-ui, -apple-system, sans-serif;
      background: #f5f4f0;
      color: #1a1a1a;
      min-height: 100vh;
      -webkit-text-size-adjust: 100%;
    }}

    /* ── Header ── */
    .hub-header {{
      position: sticky;
      top: 0;
      z-index: 20;
      background: #fff;
      border-bottom: 1px solid #e5e3dc;
      padding: 0.85rem 1.5rem;
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }}
    .hub-header-left {{
      flex-shrink: 0;
      margin-right: 0.25rem;
    }}
    .hub-header-left h1 {{
      font-size: 1rem;
      font-weight: 700;
      color: #1a1a1a;
      line-height: 1.2;
    }}
    .hub-header-left p {{
      font-size: 0.75em;
      color: #aaa;
      margin-top: 0.1em;
    }}
    .hub-haku {{
      flex: 1;
      min-width: 0;
      border: 1.5px solid #e0ddd8;
      border-radius: 20px;
      padding: 0.45rem 1rem;
      font-size: 0.88em;
      font-family: inherit;
      outline: none;
      background: #faf9f7;
      transition: border-color 0.15s, background 0.15s;
      color: #1a1a1a;
    }}
    .hub-haku:focus {{ border-color: #2c3e50; background: #fff; }}
    .hub-haku::placeholder {{ color: #bbb; }}
    .random-btn {{
      flex-shrink: 0;
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      background: #2c3e50;
      color: #fff;
      border: none;
      border-radius: 8px;
      padding: 0.5rem 1rem;
      font-size: 0.82em;
      font-weight: 600;
      font-family: inherit;
      cursor: pointer;
      transition: background 0.12s;
      white-space: nowrap;
    }}
    .random-btn:hover {{ background: #1a252f; }}
    .random-btn:active {{ transform: scale(0.97); }}

    /* ── Main ── */
    .hub-main {{
      max-width: 1240px;
      margin: 0 auto;
      padding: 1.5rem 1.5rem 4rem;
    }}

    /* ── Kategoria ── */
    .hub-kategoria {{ margin-bottom: 1.8rem; }}
    .hub-kat-label {{
      font-size: 0.68em;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: #bbb;
      margin-bottom: 0.5rem;
      padding-left: 0.15rem;
    }}

    /* ── Grid ── */
    .hub-kortit {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(270px, 1fr));
      gap: 0.35rem;
    }}

    /* ── Kortti ── */
    .hub-kortti {{
      display: flex;
      align-items: center;
      gap: 0.6rem;
      padding: 0.6rem 0.8rem;
      background: #fff;
      border: 1.5px solid #ece9e3;
      border-left: 4px solid var(--c, #2c3e50);
      border-radius: 7px;
      text-decoration: none;
      color: #222;
      font-size: 0.865em;
      line-height: 1.3;
      transition: border-color 0.1s, box-shadow 0.1s, transform 0.1s;
    }}
    .hub-kortti:hover {{
      border-color: var(--c, #2c3e50);
      box-shadow: 0 2px 10px rgba(0,0,0,0.09);
      transform: translateX(3px);
    }}
    .hub-kortti.aktiv {{
      border-color: var(--c, #2c3e50);
      box-shadow: 0 0 0 2px var(--c, #2c3e50), 0 3px 12px rgba(0,0,0,0.1);
      transform: translateX(3px);
      outline: none;
    }}
    .hub-kortti.piilotettu {{ display: none; }}

    .hub-numero {{
      flex-shrink: 0;
      width: 1.9em;
      height: 1.9em;
      background: var(--c, #2c3e50);
      color: #fff;
      border-radius: 4px;
      font-size: 0.76em;
      font-weight: 700;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .hub-nimi {{ flex: 1; }}
    .hub-nuoli {{
      color: #d0cdc8;
      font-size: 1em;
      flex-shrink: 0;
      transition: color 0.1s;
    }}
    .hub-kortti:hover .hub-nuoli,
    .hub-kortti.aktiv .hub-nuoli {{ color: var(--c, #2c3e50); }}

    /* ── Ei tuloksia ── */
    .hub-tyhja {{
      text-align: center;
      color: #bbb;
      padding: 3rem;
      font-size: 0.95em;
      display: none;
    }}

    /* ── Näppäimistövinkki ── */
    .hub-vinkki {{
      text-align: center;
      color: #ccc;
      font-size: 0.73em;
      padding: 1.5rem 0 0;
      user-select: none;
    }}
    .hub-vinkki kbd {{
      background: #f0ede8;
      border: 1px solid #ddd;
      border-bottom-width: 2px;
      border-radius: 4px;
      padding: 0.1em 0.45em;
      font-family: inherit;
      font-size: 1em;
      color: #555;
    }}

    /* ── Mobile ── */
    @media (max-width: 640px) {{
      .hub-header {{ flex-wrap: wrap; padding: 0.75rem 1rem; }}
      .hub-header-left {{ order: 1; }}
      .random-btn {{ order: 2; }}
      .hub-haku {{ order: 3; width: 100%; }}
      .hub-kortit {{ grid-template-columns: 1fr; }}
      .hub-main {{ padding: 1rem 0.9rem 3rem; }}
    }}
    @media (max-width: 380px) {{
      .random-btn .btn-label {{ display: none; }}
    }}
  </style>
</head>
<body>

<header class="hub-header">
  <div class="hub-header-left">
    <h1>Ilmiöitä</h1>
    <p>{total} ilmiötä &middot; Miten valta toimii</p>
  </div>
  <input class="hub-haku" type="search" id="haku" placeholder="Etsi ilmiötä&hellip;" autocomplete="off" spellcheck="false">
  <button class="random-btn" onclick="randomIlmio()" title="Satunnainen ilmiö (R)">
    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="16 3 21 3 21 8"/><line x1="4" y1="20" x2="21" y2="3"/><polyline points="21 16 21 21 16 21"/><line x1="15" y1="15" x2="21" y2="21"/></svg>
    <span class="btn-label">Satunnainen</span>
  </button>
</header>

<main class="hub-main" id="hub-main">
{sections_html}
  <div class="hub-tyhja" id="hub-tyhja">Ei tuloksia haullesi.</div>
  <p class="hub-vinkki">
    <kbd>&#8592;</kbd> <kbd>&#8594;</kbd>&thinsp;selaa &nbsp;&middot;&nbsp;
    <kbd>Enter</kbd>&thinsp;avaa &nbsp;&middot;&nbsp;
    <kbd>R</kbd>&thinsp;satunnainen &nbsp;&middot;&nbsp;
    <kbd>Esc</kbd>&thinsp;tyhjennä haku
  </p>
</main>

<script>
(function () {{
  const kortit = Array.from(document.querySelectorAll('.hub-kortti'));
  const haku = document.getElementById('haku');
  const tyhja = document.getElementById('hub-tyhja');
  let aktivIdx = -1; // indeksi kortit-taulukossa

  function nakyvat() {{
    return kortit.filter(k => !k.classList.contains('piilotettu'));
  }}

  function setAktiv(nakyvatLista, i) {{
    if (aktivIdx >= 0 && kortit[aktivIdx]) kortit[aktivIdx].classList.remove('aktiv');
    if (nakyvatLista.length === 0) {{ aktivIdx = -1; return; }}
    i = ((i % nakyvatLista.length) + nakyvatLista.length) % nakyvatLista.length;
    aktivIdx = kortit.indexOf(nakyvatLista[i]);
    kortit[aktivIdx].classList.add('aktiv');
    kortit[aktivIdx].scrollIntoView({{ block: 'nearest', behavior: 'smooth' }});
  }}

  function randomIlmio() {{
    const n = nakyvat();
    if (n.length === 0) return;
    window.location.href = n[Math.floor(Math.random() * n.length)].href;
  }}
  window.randomIlmio = randomIlmio;

  // Haku
  haku.addEventListener('input', function () {{
    const q = this.value.trim().toLowerCase();
    kortit.forEach(k => {{
      const teksti = k.querySelector('.hub-nimi').textContent.toLowerCase();
      k.classList.toggle('piilotettu', Boolean(q && !teksti.includes(q)));
    }});
    document.querySelectorAll('.hub-kategoria').forEach(kat => {{
      const n = kat.querySelectorAll('.hub-kortti:not(.piilotettu)').length;
      kat.style.display = n === 0 ? 'none' : '';
    }});
    const n = nakyvat();
    tyhja.style.display = n.length === 0 ? 'block' : 'none';
    if (aktivIdx >= 0) kortit[aktivIdx].classList.remove('aktiv');
    aktivIdx = -1;
  }});

  // Näppäimistö
  document.addEventListener('keydown', function (e) {{
    const hakussa = document.activeElement === haku;

    if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {{
      e.preventDefault();
      haku.blur();
      const n = nakyvat();
      const ny = aktivIdx >= 0 ? n.indexOf(kortit[aktivIdx]) : -1;
      setAktiv(n, ny + 1);
    }} else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {{
      e.preventDefault();
      haku.blur();
      const n = nakyvat();
      const ny = aktivIdx >= 0 ? n.indexOf(kortit[aktivIdx]) : n.length;
      setAktiv(n, ny - 1);
    }} else if (e.key === 'Enter' && aktivIdx >= 0 && !hakussa) {{
      window.location.href = kortit[aktivIdx].href;
    }} else if ((e.key === 'r' || e.key === 'R') && !hakussa) {{
      randomIlmio();
    }} else if (e.key === 'Escape') {{
      haku.value = '';
      haku.dispatchEvent(new Event('input'));
      haku.blur();
    }} else if (!hakussa && !e.ctrlKey && !e.metaKey && !e.altKey && e.key.length === 1 && e.key !== ' ') {{
      haku.focus();
    }}
  }});
}})();
</script>

</body>
</html>"""


def main():
    source = load_source()
    soup = BeautifulSoup(source, 'html.parser')

    inline_css = extract_inline_css(soup)
    card_colors = extract_card_colors(inline_css)
    chartjs_raw, share_raw = extract_scripts(soup)
    chartjs_safe = make_chartjs_safe(chartjs_raw)
    share_fixed = fix_share_widget(share_raw)
    categories = get_categories(soup)

    cards = soup.select('.paasisu .ilmio[id]')
    total = len(cards)
    all_card_ids = [c['id'] for c in cards]
    print(f"Löydettiin {total} korttia.")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for i, card in enumerate(cards):
        prev_card = cards[i - 1] if i > 0 else None
        next_card = cards[i + 1] if i < total - 1 else None
        n = i + 1

        page_html = build_page(
            card, prev_card, next_card, n, total, all_card_ids,
            inline_css, chartjs_safe, share_fixed,
            categories, card_colors
        )

        out_path = os.path.join(OUTPUT_DIR, f"{card['id']}.html")
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(page_html)

    # Hub-sivu
    hub_html = build_hub(cards, categories, card_colors)
    hub_path = os.path.join(OUTPUT_DIR, 'index.html')
    with open(hub_path, 'w', encoding='utf-8') as f:
        f.write(hub_html)

    print(f"Generoitu: {total} ilmiösivua + index.html -> {OUTPUT_DIR}/")


if __name__ == '__main__':
    main()
