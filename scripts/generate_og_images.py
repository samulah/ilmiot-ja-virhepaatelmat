#!/usr/bin/env python3
"""Generate 1200×630 OG images for all 69 kendom.fi/ilmiöt/ pages."""

import re
import sys
import urllib.request
from pathlib import Path

from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OG_DIR = PROJECT_ROOT / "og"
FONT_DIR = Path(__file__).resolve().parent / "fonts"

BASE_URL = "https://kendom.fi/ilmiöt"

C_BG = "#1C1400"
C_GOLD = "#C9A84C"
C_WHITE = "#FFFFFF"
C_CREAM = "#D4C090"
C_META = "#8B9A6E"
C_RULE = (42, 32, 0)     # Subtle separator line, slightly lighter than bg
C_FALLBACK = "#C9A84C"   # Gold fallback when no accent found

# Google Fonts GitHub raw TTF (static & variable)
_GH_BASE = "https://raw.githubusercontent.com/google/fonts/main/ofl"
FONT_URLS = {
    "Spectral-Bold.ttf":    f"{_GH_BASE}/spectral/Spectral-Bold.ttf",
    "Spectral-Regular.ttf": f"{_GH_BASE}/spectral/Spectral-Regular.ttf",
    # DM Sans is variable-only in repo; one file covers all weights
    "DMSans-Variable.ttf":  f"{_GH_BASE}/dmsans/DMSans%5Bopsz%2Cwght%5D.ttf",
}


def ensure_fonts():
    FONT_DIR.mkdir(exist_ok=True)
    for fname, url in FONT_URLS.items():
        out = FONT_DIR / fname
        if out.exists():
            continue
        try:
            urllib.request.urlretrieve(url, str(out))
            print(f"  ✓ {fname} ({out.stat().st_size // 1024} KB)")
        except Exception as e:
            print(f"  ✗ {fname}: {e} (will use fallback)")


def load_font(name, size):
    p = FONT_DIR / name
    if p.exists():
        try:
            return ImageFont.truetype(str(p), size)
        except Exception:
            pass
    return ImageFont.load_default(size=size)


def load_fonts():
    # DM Sans variable font covers all weights (regular + medium)
    return {
        "brand":      load_font("DMSans-Variable.ttf",  26),
        "brand_sm":   load_font("DMSans-Variable.ttf",  22),
        "meta":       load_font("DMSans-Variable.ttf",  22),
        "name_lg":    load_font("Spectral-Bold.ttf",    64),
        "name_md":    load_font("Spectral-Bold.ttf",    50),
        "desc":       load_font("Spectral-Regular.ttf", 28),
    }


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def text_width(font, text):
    bb = font.getbbox(text)
    return bb[2] - bb[0]


def draw_wrapped(draw, text, font, fill, x, y, max_w, max_lines=3):
    """Draw word-wrapped text. Returns y after last line."""
    words = text.split()
    lines = []
    cur = []
    overflow = False

    for word in words:
        candidate = " ".join(cur + [word])
        if text_width(font, candidate) <= max_w:
            cur.append(word)
        else:
            if cur:
                lines.append(" ".join(cur))
                if len(lines) >= max_lines:
                    overflow = True
                    cur = []
                    break
            cur = [word]

    if cur:
        if len(lines) < max_lines:
            lines.append(" ".join(cur))
        else:
            overflow = True

    if overflow and lines:
        last = lines[-1]
        while True:
            if text_width(font, last + "…") <= max_w:
                lines[-1] = last + "…"
                break
            if " " in last:
                last = last.rsplit(" ", 1)[0]
            elif len(last) > 1:
                last = last[:-1]
            else:
                break

    # Line height: ascent + descent + leading
    line_h = font.getbbox("Ägjpq")[3] + 12
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += line_h
    return y


def parse_page(path):
    """Extract OG image data from an ilmiö HTML file."""
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    slug = path.stem

    h1 = soup.find("h1")
    name = h1.get_text(strip=True) if h1 else slug.replace("-", " ").title()

    tag = soup.find(class_="ilmio-tag")
    number = tag.get_text(strip=True) if tag else ""

    kat = soup.find(class_="kortti-breadcrumb-kat")
    category = kat.get_text(strip=True) if kat else ""

    desc_tag = soup.find("meta", {"name": "description"})
    description = desc_tag["content"] if desc_tag else ""

    # Strip "Name: " prefix that seo_patch.py prepends to descriptions
    short_name = name.split(" —")[0].strip()
    prefix = short_name + ": "
    if description.startswith(prefix):
        description = description[len(prefix):]

    # Extract accent color from inline <style>: #slug { border-top-color: #HEX; }
    accent = C_FALLBACK
    style = soup.find("style")
    if style and style.string:
        css = style.string
        pat = rf"#{re.escape(slug)}\s+\{{[^}}]*border-top-color:\s*(#[0-9a-fA-F]{{3,6}})"
        m = re.search(pat, css)
        if m:
            accent = m.group(1)
        else:
            # Fallback: #slug .ilmio-tag { background: #HEX; }
            pat2 = rf"#{re.escape(slug)}\s+\.ilmio-tag\s*\{{[^}}]*background:\s*(#[0-9a-fA-F]{{3,6}})"
            m2 = re.search(pat2, css)
            if m2:
                accent = m2.group(1)

    return {
        "slug": slug,
        "name": name,
        "number": number,
        "category": category,
        "description": description,
        "accent": accent,
    }


def render_og(data, fonts, out_path):
    img = Image.new("RGB", (1200, 630), hex_rgb(C_BG))
    draw = ImageDraw.Draw(img)

    accent = data["accent"]
    name = data["name"]
    number = data.get("number", "")
    category = data.get("category", "")
    description = data.get("description", "")

    # Left accent bar
    draw.rectangle([(0, 0), (8, 630)], fill=hex_rgb(accent))

    # Branding row
    draw.text((40, 34), "Ilmiöitä", font=fonts["brand"], fill=C_GOLD)
    draw.text((1160, 34), "kendom.fi", font=fonts["brand_sm"], fill=C_GOLD, anchor="ra")

    # Subtle horizontal rule
    draw.rectangle([(40, 80), (1160, 81)], fill=C_RULE)

    # Category · number
    parts = [p for p in (category, number) if p]
    meta_text = "  ·  ".join(parts)
    if meta_text:
        draw.text((40, 110), meta_text, font=fonts["meta"], fill=C_META)

    # Ilmiö name — switch to smaller font if name is very long
    name_font = fonts["name_lg"]
    # Estimate if name might take >3 lines at large size
    if text_width(name_font, name) > 1120 * 2.5:
        name_font = fonts["name_md"]

    draw_wrapped(draw, name, name_font, C_WHITE, x=40, y=190, max_w=1120, max_lines=3)

    # Description (near bottom, 2 lines max)
    if description:
        draw_wrapped(draw, description, fonts["desc"], C_CREAM, x=40, y=478, max_w=1120, max_lines=2)

    img.save(str(out_path), "PNG", optimize=True)
    return str(out_path)


def patch_html(html_path, slug):
    """Add og:image + twitter:image tags. Returns True if file was changed."""
    content = html_path.read_text(encoding="utf-8")

    if 'property="og:image"' in content:
        return False

    img_url = f"{BASE_URL}/og/{slug}.png"
    tags = (
        f'  <meta property="og:image" content="{img_url}">\n'
        f'  <meta property="og:image:width" content="1200">\n'
        f'  <meta property="og:image:height" content="630">\n'
        f'  <meta name="twitter:image" content="{img_url}">\n'
    )

    # Upgrade twitter:card to summary_large_image
    content = content.replace(
        'content="summary"',
        'content="summary_large_image"',
    )

    content = content.replace("</head>", tags + "</head>", 1)
    html_path.write_text(content, encoding="utf-8")
    return True


def main():
    print("=== OG Image Generator — kendom.fi/ilmiöt/ ===\n")

    print("Fonts...")
    ensure_fonts()
    fonts = load_fonts()
    OG_DIR.mkdir(exist_ok=True)

    html_files = sorted(PROJECT_ROOT.glob("*.html"))
    total = len(html_files)
    print(f"\n{total} HTML-tiedostoa löydetty\n")

    generated = patched = 0

    for i, html_path in enumerate(html_files, 1):
        slug = html_path.stem

        if slug == "index":
            data = {
                "slug": "index",
                "name": "Ilmiöitä",
                "number": "",
                "category": "68 sosiaalista ilmiötä",
                "description": "Valtarakenteet, propaganda, kognitiiviset harhat, byrokratia, projektihallinnan lait, myyntikikat ja petokset.",
                "accent": C_GOLD,
            }
        else:
            data = parse_page(html_path)

        out_path = OG_DIR / f"{slug}.png"
        render_og(data, fonts, out_path)
        generated += 1

        changed = patch_html(html_path, slug)
        if changed:
            patched += 1

        print(f"  [{i:2d}/{total}] {slug}.png  accent={data['accent']}")

    print(f"\n✓ Generoitu {generated} OG-kuvaa → og/")
    print(f"✓ Päivitetty {patched} HTML-tiedostoa (og:image + twitter:card)")
    if patched < total:
        print(f"  ({total - patched} tiedostoa ohitettu — og:image oli jo olemassa)")
    print("\nSeuraava askel: tarkista muutama PNG visuaalisesti, sitten git commit + deploy.")


if __name__ == "__main__":
    main()
