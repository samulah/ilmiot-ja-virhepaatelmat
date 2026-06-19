#!/usr/bin/env python3
"""Generate the single reusable brand OG image -> og/brand.png (1200x630)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent.parent
FB = ROOT / "scripts" / "fonts"
OUT = ROOT / "og" / "brand.png"

BG = (28, 20, 0)        # #1C1400
GOLD = "#C9A84C"
CREAM = "#F5F0E5"
MUTE = (180, 162, 120)


def flag(size):
    s = size / 64.0
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    b = lambda *p: [c * s for c in p]
    d.rounded_rectangle(b(17, 9, 56, 33), radius=3 * s, fill="#DC2626")
    d.rounded_rectangle(b(13, 6, 18.5, 58), radius=2.75 * s, fill=GOLD)
    d.ellipse(b(15.75 - 3.4, 7 - 3.4, 15.75 + 3.4, 7 + 3.4), fill=GOLD)
    d.rounded_rectangle(b(34, 12.5, 39.5, 23.5), radius=2.75 * s, fill="#FFC400")
    d.ellipse(b(36.75 - 2.9, 28 - 2.9, 36.75 + 2.9, 28 + 2.9), fill="#FFC400")
    return im


def main():
    title_f = ImageFont.truetype(str(FB / "Spectral-Bold.ttf"), 128)
    sub_f = ImageFont.truetype(str(FB / "Spectral-Regular.ttf"), 46)
    tag_f = ImageFont.truetype(str(FB / "DMSans-Variable.ttf"), 27)
    dom_f = ImageFont.truetype(str(FB / "DMSans-Variable.ttf"), 28)

    W, H = 1200, 630
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 12, H], fill=GOLD)
    lg = flag(150)
    im.paste(lg, (W // 2 - 75, 70), lg)
    d.text((W // 2, 300), "Ilmiöitä", font=title_f, fill=CREAM, anchor="mm")
    d.text((W // 2, 392), "Miten valta toimii", font=sub_f, fill=GOLD, anchor="mm")
    d.rectangle([W // 2 - 180, 440, W // 2 + 180, 441], fill=(90, 68, 0))
    d.text((W // 2, 485),
           "68 yhteiskunnallista ilmiötä — valta, propaganda, manipulaatio, huijaukset",
           font=tag_f, fill=MUTE, anchor="mm")
    d.text((W // 2, 545), "ilmiöt.fi", font=dom_f, fill=GOLD, anchor="mm")

    OUT.parent.mkdir(exist_ok=True)
    im.save(str(OUT), "PNG", optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
