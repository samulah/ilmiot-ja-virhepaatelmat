#!/usr/bin/env python3
"""Rakentaa sitemap.xml:n index.html:n hub-korteista.

Miksi: sitemap oli ainoa buildiartefakti, jota ylläpidettiin käsin. Siksi se
ajautui erilleen sisällöstä — 2026-07-25 auditissa 93/111 <lastmod>-arvoa oli
eri kuin sivun oma schema dateModified, ja tuorein muokkaus (bikeshedding.html,
2026-07-21) näkyi sitemapissa vanhempana kuin oli.

  <loc>     : index.html:n hub-korttien järjestyksessä (etusivu → ilmiöt → tietoa)
  <lastmod> : sivun JSON-LD:n dateModified. Jos sitä ei ole (tietoa.html),
              käytetään tiedoston viimeisintä git-committipäivää.

Idempotentti; kaatuu assertiin jos kortin sivutiedosto tai päivämäärä puuttuu.

Ajo:  python3 scripts/build_sitemap.py
"""
import re
import subprocess
import xml.dom.minidom
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Vaihda tämä yhdellä rivillä, jos/kun isäntä siirretään punycodeen
# (https://www.xn--ilmit-mua.fi/) — ks. ACTION-PLAN.md kohta 8.
BASE = "https://www.ilmiöt.fi/"

# (polku, priority, changefreq)
ETUSIVU = ("", "1.0", "monthly")
ILMIO = ("{slug}.html", "0.8", "monthly")
TIETOA = ("tietoa.html", "0.5", "yearly")


def kortit_jarjestyksessa(html):
    slugit = re.findall(r'href="([a-z0-9-]+)\.html" class="hub-kortti"', html)
    assert slugit, "hub-kortteja ei löytynyt index.html:stä"
    assert len(slugit) == len(set(slugit)), "duplikaattikortti index.html:ssä"
    return slugit


def git_paiva(tiedosto):
    ulos = subprocess.run(["git", "log", "-1", "--format=%as", "--", tiedosto],
                          cwd=ROOT, capture_output=True, text=True).stdout.strip()
    return ulos or None


def lastmod(tiedosto):
    """Sivun schema dateModified, tai fallbackina git-committipäivä."""
    polku = ROOT / tiedosto
    assert polku.exists(), f"sivu puuttuu: {tiedosto}"
    osumat = re.findall(r'"dateModified":\s*"(\d{4}-\d{2}-\d{2})',
                        polku.read_text(encoding="utf-8"))
    if osumat:
        # sivulla voi olla useita solmuja (Article + CollectionPage) — tuorein voittaa
        return max(osumat)
    paiva = git_paiva(tiedosto)
    assert paiva, f"{tiedosto}: ei dateModifiedia eikä git-historiaa"
    return paiva


def rakenna():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    rivit = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']

    sivut = [(ETUSIVU[0], "index.html", ETUSIVU[1], ETUSIVU[2])]
    sivut += [(ILMIO[0].format(slug=s), f"{s}.html", ILMIO[1], ILMIO[2])
              for s in kortit_jarjestyksessa(html)]
    sivut.append((TIETOA[0], "tietoa.html", TIETOA[1], TIETOA[2]))

    for polku, tiedosto, prio, freq in sivut:
        rivit += ["  <url>",
                  f"    <loc>{BASE}{polku}</loc>",
                  f"    <lastmod>{lastmod(tiedosto)}</lastmod>",
                  f"    <priority>{prio}</priority>",
                  f"    <changefreq>{freq}</changefreq>",
                  "  </url>"]
    rivit.append("</urlset>")
    return "\n".join(rivit) + "\n", len(sivut)


if __name__ == "__main__":
    sisalto, n = rakenna()
    p = ROOT / "sitemap.xml"
    vanha = p.read_text(encoding="utf-8") if p.exists() else ""

    # varmistus: hyvin muodostunut XML ennen kirjoitusta
    xml.dom.minidom.parseString(sisalto.encode("utf-8"))

    p.write_text(sisalto, encoding="utf-8")
    print(f"sitemap.xml: {n} URLia")
    print("  ✎ päivitetty" if sisalto != vanha else "  oli jo ajan tasalla")
