#!/usr/bin/env python3
"""
Sivukohtaiset jakokuvat: og/<slug>.png ja og/kategoria-<slug>.png (1200×630).

Ilman tätä jokainen jaettu linkki näyttää saman og/brand.png:n, eikä linkin
esikatselu kerro, mistä ilmiöstä on kyse. Kortissa on ilmiön nimi ja etusivun
kortin yhden virkkeen kuvaus — esikatselu opettaa ilman klikkausta.

Lähde on index.html:n korttilista (sama kuin build_kategoriat.py lukee), joten
kortin teksti ei voi ajautua erilleen etusivun kortista. Aja uudelleen, kun
kortin nimi tai kuvaus muuttuu.

Kuvassa EI ole ilmiön numeroa eikä ilmiöiden kokonaismäärää: lisaa_ilmiot.py
ja poista_ilmio.py numeroivat koko sivuston uudelleen, ja numero kuvassa
vanhenisi joka kerta. (og/brand.png:ssä lukee yhä "68 ilmiötä" tästä syystä.)

Ilmiösivuilla skripti vaihtaa kolme meta-riviä: og:image, twitter:image ja
og:image:alt. Kategoriasivuja ei muokata — ne ovat generoituja, ja
build_kategoriat.py käyttää kategoriakuvaa itse, jos tiedosto on olemassa.
Aja siis kategoriakuvan jälkeen build_kategoriat.py.

Vanha generate_og_images.py on kendom.fi-ajalta eikä sitä pidä ajaa.

    python3 scripts/build_og.py sealioning trollaus        # kuivaharjoitus
    python3 scripts/build_og.py --kategoria trollaus-ja-keskustelun-sabotointi
    python3 scripts/build_og.py --kaikki
    python3 scripts/build_og.py … --kirjoita               # kirjoittaa
"""
import html
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from build_kategoriat import DOMAIN, SISALTO, lue_kategoriat, lue_sisalto, tayta_maarat
from make_og_brand import flag

ROOT = Path(__file__).resolve().parent.parent
FONTIT = ROOT / "scripts" / "fonts"
OG = ROOT / "og"

W, H = 1200, 630
TAUSTA = (28, 20, 0)          # --c-primary-dark #1C1400
KULTA = "#C9A84C"             # --c-primary
KERMA = "#F5F0E5"             # --c-bg
KUVAUS = "#DDCFA6"
HIMMEA = (180, 162, 120)
VIIVA = (90, 68, 0)

VASEN, OIKEA = 84, 1116       # tekstipalstan reunat
YLA, ALA = 150, 530           # alue, jonka keskelle tekstilohko asetellaan
VALI = 38                     # otsikon ja kuvauksen väli


def fontti(nimi, koko, paino=None):
    f = ImageFont.truetype(str(FONTIT / nimi), koko)
    if paino:                 # muuttuva fontti: akselit ovat optinen koko ja paino
        f.set_variation_by_axes([max(9, min(koko, 40)), paino])
    return f


# scripts/fonts/DMSans-Medium.ttf ja -Regular.ttf ovat EOT-tiedostoja, joita
# PIL ei lue. Painot otetaan siksi muuttuvasta fontista.
DMSANS = "DMSans-Variable.ttf"


def puhdas(teksti):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", teksti))).strip()


def rivita(d, teksti, f, leveys):
    rivit, nyt = [], ""
    for sana in teksti.split():
        ehdokas = f"{nyt} {sana}".strip()
        if d.textlength(ehdokas, font=f) <= leveys or not nyt:
            nyt = ehdokas
        else:
            rivit.append(nyt)
            nyt = sana
    return rivit + [nyt] if nyt else rivit


def harvennettu(d, xy, teksti, f, vari, vali):
    """Versaaliteksti kirjainvälillä — PIL ei osaa letter-spacingia itse."""
    x, y = xy
    for merkki in teksti:
        d.text((x, y), merkki, font=f, fill=vari)
        x += d.textlength(merkki, font=f) + vali


def piirra(nimi, kuvaus, ylaotsikko, vari, alateksti="Tunnistaminen ja vastakeinot"):
    im = Image.new("RGB", (W, H), TAUSTA)
    d = ImageDraw.Draw(im)
    leveys = OIKEA - VASEN

    # Vasen reuna ilmiön omalla värillä — sama merkki kuin etusivun kortissa.
    d.rectangle([0, 0, 16, H], fill=vari)

    logo = flag(56)
    im.paste(logo, (VASEN - 8, 52), logo)
    d.text((VASEN + 58, 82), "Ilmiöitä", font=fontti("Spectral-Bold.ttf", 38),
           fill=KERMA, anchor="lm")
    d.text((OIKEA, 82), "ilmiöt.fi", font=fontti(DMSANS, 26, 500),
           fill=KULTA, anchor="rm")

    # Suurin otsikkokoko, jolla nimi mahtuu kahdelle riville ja kuvaus kolmelle
    # ilman katkaisua. Jos mikään ei mahdu, se on virhe eikä hiljainen "…".
    f_yla = fontti(DMSANS, 24, 600)
    valinta = None
    for koko_o in (104, 92, 82, 72, 64, 56):
        f_o = fontti("Spectral-Bold.ttf", koko_o)
        r_o = rivita(d, nimi, f_o, leveys)
        if len(r_o) > 2 or any(d.textlength(r, font=f_o) > leveys for r in r_o):
            continue
        for koko_k in (38, 34, 30):
            f_k = fontti("Spectral-Regular.ttf", koko_k)
            r_k = rivita(d, kuvaus, f_k, leveys)
            korkeus = (34 + 22 + len(r_o) * koko_o * 1.1 + VALI
                       + len(r_k) * koko_k * 1.36)
            if len(r_k) <= 3 and korkeus <= ALA - YLA:
                valinta = (f_o, r_o, koko_o, f_k, r_k, koko_k, korkeus)
                break
        if valinta:
            break
    if not valinta:
        raise SystemExit(f"VIRHE: {nimi!r} ei mahdu korttiin — lyhennä kuvausta")
    f_o, r_o, koko_o, f_k, r_k, koko_k, korkeus = valinta

    y = YLA + (ALA - YLA - korkeus) / 2
    harvennettu(d, (VASEN, y), ylaotsikko.upper(), f_yla, KULTA, 3)
    y += 34 + 22
    for rivi in r_o:
        d.text((VASEN, y), rivi, font=f_o, fill=KERMA)
        y += koko_o * 1.1
    y += VALI
    for rivi in r_k:
        d.text((VASEN, y), rivi, font=f_k, fill=KUVAUS)
        y += koko_k * 1.36

    d.rectangle([VASEN, 556, OIKEA, 557], fill=VIIVA)
    d.text((VASEN, 590), alateksti, font=fontti(DMSANS, 24, 400),
           fill=HIMMEA, anchor="lm")
    return im


def korvaa_yksi(sisalto, kuvio, uusi, mista):
    """Regex, joka ei osu täsmälleen kerran, on virhe — ei hiljainen ohitus."""
    tulos, maara = re.subn(kuvio, lambda m: uusi, sisalto)
    if maara != 1:
        raise SystemExit(f"VIRHE: {mista}: {kuvio!r} osui {maara} kertaa, pitää olla 1")
    return tulos


def paivita_metat(slug, alt):
    polku = ROOT / f"{slug}.html"
    vanha = polku.read_text(encoding="utf-8")
    kuva = f"{DOMAIN}/og/{slug}.png"
    alt = html.escape(alt, quote=True)
    uusi = korvaa_yksi(vanha, r'<meta property="og:image" content="[^"]*">',
                       f'<meta property="og:image" content="{kuva}">', polku.name)
    uusi = korvaa_yksi(uusi, r'<meta name="twitter:image" content="[^"]*">',
                       f'<meta name="twitter:image" content="{kuva}">', polku.name)
    uusi = korvaa_yksi(uusi, r'<meta property="og:image:alt" content="[^"]*">',
                       f'<meta property="og:image:alt" content="{alt}">', polku.name)
    return polku, vanha, uusi


def main(argv):
    kirjoita = "--kirjoita" in argv
    kaikki = "--kaikki" in argv
    arvot = [a for a in argv if a not in ("--kirjoita", "--kaikki")]
    kat_pyynnot, slugit = [], []
    while arvot:
        a = arvot.pop(0)
        if a == "--kategoria":
            kat_pyynnot.append(arvot.pop(0))
        elif a.startswith("--"):
            raise SystemExit(f"VIRHE: tuntematon lippu {a}")
        else:
            slugit.append(a)

    kategoriat = lue_kategoriat()
    kortit = {}                                   # slug -> (kortti, kategorian nimi)
    for k in kategoriat.values():
        for kortti in k["kortit"]:
            kortit[kortti["slug"]] = (kortti, k["label"])
    lyhyt = {re.sub(r"-kategoria$", "", kid): kid for kid in kategoriat}

    if kaikki:
        slugit, kat_pyynnot = list(kortit), list(lyhyt)
    for kat in kat_pyynnot:
        if kat not in lyhyt:
            raise SystemExit(f"VIRHE: kategoriaa {kat!r} ei ole index.html:ssä")
        slugit += [k["slug"] for k in kategoriat[lyhyt[kat]]["kortit"]]
    if not slugit and not kat_pyynnot:
        raise SystemExit(__doc__)

    OG.mkdir(exist_ok=True)
    kuvia = sivuja = 0
    for slug in dict.fromkeys(slugit):            # järjestys säilyy, ei tuplia
        if slug not in kortit:
            raise SystemExit(f"VIRHE: {slug} ei ole etusivun korttilistalla")
        kortti, kat_nimi = kortit[slug]
        nimi, kuvaus = puhdas(kortti["nimi"]), puhdas(kortti["kuvaus"])
        im = piirra(nimi, kuvaus, kat_nimi, kortti["vari"])
        polku, vanha, uusi = paivita_metat(slug, f"{nimi} — {kuvaus}")
        muuttuu = "metat muuttuvat" if uusi != vanha else "metat ennallaan"
        print(f"  og/{slug}.png  ·  {slug}.html: {muuttuu}")
        if kirjoita:
            im.save(str(OG / f"{slug}.png"), "PNG", optimize=True)
            kuvia += 1
            if uusi != vanha:
                polku.write_text(uusi, encoding="utf-8")
                sivuja += 1

    for kat in kat_pyynnot:
        meta, _ = lue_sisalto(SISALTO / f"{kat}.md")
        meta = tayta_maarat(meta, len(kategoriat[lyhyt[kat]]["kortit"]), f"{kat}.md")
        osat = meta["h1"].split(" — ", 1)
        ala = osat[1][0].upper() + osat[1][1:] if len(osat) > 1 else meta["kuvaus"]
        im = piirra(osat[0], ala, "Kategoria", meta["vari"], "Ilmiöt ja vastakeinot")
        print(f"  og/kategoria-{kat}.png  ·  aja build_kategoriat.py {kat}")
        if kirjoita:
            im.save(str(OG / f"kategoria-{kat}.png"), "PNG", optimize=True)
            kuvia += 1

    if kirjoita:
        print(f"\n{kuvia} kuvaa → og/, {sivuja} ilmiösivun metat päivitetty")
    else:
        print("\n(kuivaharjoitus — lisää --kirjoita)")


if __name__ == "__main__":
    main(sys.argv[1:])
