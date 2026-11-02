#!/usr/bin/env python3
"""
Dataneuvoksen ilmiökalenteri: LinkedIn-karusellit (PDF, 1080×1350).

Jokainen luukut/NN-slug.json tuottaa kansioon valmis/:
  NN-slug.pdf      dokumenttipostaukseksi (kansi + sisältösivut)
  NN-slug-kansi.png esikatseluun
  NN-slug.txt      postausteksti ja ensimmäinen kommentti
sekä 00-ennakko.png/.txt ilmoituspostaukseksi 30.11.

Sunnuntain luukuissa ja aattona karusellin viimeinen sivu on koosteruudukko,
jossa avatut luukut näkyvät nimellä. Erillistä koostepostausta ei tehdä:
kaksi postausta samana päivänä kilpailisivat toistensa näkyvyydestä.

Paletti yhdistää Dataneuvoksen logon vihreän (#083E20, pohja)
ja ilmiöt.fi:n kullan (#C9A84C) ja kerman (#F5F0E5). Fontit ovat samat kuin
jakokuvissa (scripts/fonts/), jotta kuvat ovat sivuston näköisiä.

Jos teksti ei mahdu sivulle pienimmälläkään koolla, ajo kaatuu: lyhennä
tekstiä, älä hyväksy katkaisua.

    python3 build_kalenteri.py            # kaikki luukut
    python3 build_kalenteri.py 1 2        # valitut luukut (0 = ennakko)
"""
import datetime
import json
import re
import sys
import zlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
FONTIT = ROOT.parent / "scripts" / "fonts"
VALMIS = ROOT / "valmis"

W, H = 1080, 1350
TAUSTA = (8, 62, 32)         # dataneuvos_logo.png:n ympyrä, jotta logo sulautuu pohjaan
KULTA = "#C9A84C"
KERMA = "#F5F0E5"
SALVIA = (196, 206, 180)
KEHYS = (70, 110, 70)
VASEN, OIKEA = 140, W - 140
MERKKI = "DATANEUVOKSEN ILMIÖKALENTERI"


def fontti(nimi, koko, paino=None):
    f = ImageFont.truetype(str(FONTIT / nimi), koko)
    if paino:  # muuttuva DM Sans: akselit ovat optinen koko ja paino
        f.set_variation_by_axes([max(9, min(koko, 40)), paino])
    return f


def dm(koko, paino=500):
    return fontti("DMSans-Variable.ttf", koko, paino)


def serif(koko, lihava=False):
    return fontti("Spectral-Bold.ttf" if lihava else "Spectral-Regular.ttf", koko)


def harvennettu(d, x, y, teksti, f, vari, vali, keskelle=False):
    """Versaali kirjainvälillä — PIL ei osaa letter-spacingia itse."""
    if keskelle:
        x -= (sum(d.textlength(m, font=f) for m in teksti) + vali * (len(teksti) - 1)) / 2
    for m in teksti:
        d.text((x, y), m, font=f, fill=vari)
        x += d.textlength(m, font=f) + vali


def tahti(d, cx, cy, r, vari):
    d.polygon([(cx, cy - r), (cx + r * .28, cy), (cx, cy + r), (cx - r * .28, cy)], fill=vari)
    d.polygon([(cx - r, cy), (cx, cy - r * .28), (cx + r, cy), (cx, cy + r * .28)], fill=vari)


def pohja():
    im = Image.new("RGB", (W, H), TAUSTA)
    d = ImageDraw.Draw(im)
    m = 56
    d.rectangle([m, m, W - m, H - m], outline=KEHYS, width=2)
    d.rectangle([m + 12, m + 12, W - m - 12, H - m - 12], outline=KEHYS, width=1)
    return im, d


def ajot(teksti):
    """'**lihava** loput' → [(sana, lihava), …]; sanat säilyttävät lihavuutensa rivityksessä."""
    sanat = []
    for i, osa in enumerate(re.split(r"\*\*", teksti)):
        # vain tavallinen välilyönti katkaisee: sitova välilyönti pitää ”10 %” yhdessä
        sanat += [(s, i % 2 == 1) for s in re.split(r"[ \n\t]+", osa) if s]
    return sanat


def rivita(d, teksti, koko, leveys, tavuta=False):
    """Rivittää sanat; tavuta=True sallii katkon yhdysmerkin jälkeen
    (Yhdeksän-|yhdeksän-|sääntö). Osat yhdistää rivin_teksti()."""
    f = {False: serif(koko), True: serif(koko, True)}
    rivit, nyt, x = [], [], 0
    vali = d.textlength(" ", font=f[False])
    sanat = ajot(teksti)
    if tavuta:
        sanat = [(o, lih) for sana, lih in sanat for o in re.findall(r"[^-–]+[-–]?|[-–]", sana)]
    for sana, lih in sanat:
        w = d.textlength(sana, font=f[lih])
        jatko = tavuta and nyt and nyt[-1][0][-1] in "-–"
        lisa = w if not nyt or jatko else vali + w
        if nyt and x + lisa > leveys:
            rivit.append(nyt)
            nyt, x, lisa = [], 0, w
        nyt.append((sana, lih))
        x += lisa
    return (rivit + [nyt] if nyt else rivit), f, vali


def rivin_teksti(rivi, tavuta=False):
    """Tavutetun rivin osat yhteen: yhdysmerkin jälkeen ei välilyöntiä."""
    ulos = ""
    for sana, _ in rivi:
        ulos += sana if not ulos or (tavuta and ulos[-1] in "-–") else " " + sana
    return ulos


def mahtuu(d, rivit, f, leveys, tavuta=False):
    return all(d.textlength(rivin_teksti(r, tavuta), font=f) <= leveys for r in rivit)


def piirra_rivit(d, x, y, rivit, f, vali, koko, vari, lihava_vari):
    for rivi in rivit:
        xx = x
        for sana, lih in rivi:
            d.text((xx, y), sana, font=f[lih], fill=lihava_vari if lih else vari)
            xx += d.textlength(sana, font=f[lih]) + vali
        y += koko * 1.42
    return y


def lohkon_korkeus(d, lohko, koko):
    leveys = OIKEA - VASEN
    if "luku" in lohko:
        rivit, _, _ = rivita(d, lohko["selite"], koko, leveys)
        return 230 + len(rivit) * koko * 1.42
    teksti = lohko.get("kohta") or lohko["kappale"]
    rivit, _, _ = rivita(d, teksti, koko, leveys - (34 if "kohta" in lohko else 0))
    return len(rivit) * koko * 1.42


def ylatunniste(d, luukku, sivu, sivuja):
    harvennettu(d, VASEN, 128, f"LUUKKU {luukku}", dm(24, 600), KULTA, 4)
    d.text((OIKEA, 142), f"{sivu} / {sivuja}", font=dm(24), fill=SALVIA, anchor="rm")


LOGO_TYYLI = "mitali"  # valkoinen | kulta | kulta-rengas | mitali


def _logokuva(koko):
    """Logon N-merkki ja ympyrä erotellaan maskeiksi ja väritetään tyylin mukaan.
    Ympyrä on pohjan värinen, joten valkoinen/kulta-tyylissä näkyy vain N."""
    alku = Image.open(ROOT / "dataneuvos_logo.png").convert("RGBA")
    r, g, b, a = alku.split()
    n_maski = r.point(lambda v: 255 if v > 128 else 0)                  # valkoinen N
    ympyra = a.point(lambda v: 255 if v > 128 else 0)
    kulta = Image.new("RGBA", alku.size, KULTA)
    pohja = Image.new("RGBA", alku.size, TAUSTA + (255,))
    kuva = Image.new("RGBA", alku.size, (0, 0, 0, 0))
    if LOGO_TYYLI == "mitali":                                           # kultainen ympyrä, vihreä N
        kuva.paste(kulta, (0, 0), ympyra)
        kuva.paste(pohja, (0, 0), n_maski)
        w = alku.width  # kiiltopiste kuten joulupalloissa
        ImageDraw.Draw(kuva).ellipse([w * .19, w * .17, w * .35, w * .33], fill=(232, 214, 160))
    else:
        vari = Image.new("RGBA", alku.size, "#FFFFFF") if LOGO_TYYLI == "valkoinen" else kulta
        kuva.paste(vari, (0, 0), n_maski)
        if LOGO_TYYLI == "kulta-rengas":
            d = ImageDraw.Draw(kuva)
            d.ellipse([18, 18, alku.width - 18, alku.height - 18], outline=KULTA, width=34)
    return kuva.resize((koko, koko), Image.LANCZOS)


def logo(im, cx, cy, koko):
    """Dataneuvoksen logo keskelle, sivuilla pienet tähdet (kutsuja piirtää)."""
    avain = (LOGO_TYYLI, koko)
    if avain not in _LOGOT:
        _LOGOT[avain] = _logokuva(koko)
    im.paste(_LOGOT[avain], (round(cx - koko / 2), round(cy - koko / 2)), _LOGOT[avain])


_LOGOT = {}


def alatunniste(im, d, teksti=None):
    if teksti:
        d.text((W / 2, H - 175), teksti, font=serif(36), fill=KULTA, anchor="mm")
    y = H - 235 if teksti else H - 180
    logo(im, W / 2, y, 60)
    for x in (W / 2 - 110, W / 2 + 110):
        tahti(d, x, y, 6, KULTA)
    d.text((W / 2, H - 120), "ilmiöt.fi  ·  dataneuvos.fi", font=dm(26), fill=KULTA, anchor="mm")


def pallot(im, pallot):
    """Joulupallot narussa kehyksen yläreunasta. Piirretään 4× koossa ja
    pienennetään, koska PIL:n ympyrät eivät ole reunapehmennettyjä.
    tayte "logo" ripustaa narun ja hatun Dataneuvoksen logolle."""
    k = 4
    kerros = Image.new("RGBA", (W * k, H * k), (0, 0, 0, 0))
    d = ImageDraw.Draw(kerros)
    for x, y, r, tayte in pallot:
        x, y, r = x * k, y * k, r * k
        d.line([(x, 69 * k), (x, y - r - r * .42)], fill=KULTA, width=2 * k)
        d.ellipse([x - r * .16, y - r - r * .62, x + r * .16, y - r - r * .30],
                  outline=KULTA, width=2 * k)
        d.rectangle([x - r * .26, y - r * 1.12, x + r * .26, y - r * .86], fill=KULTA)
        if tayte == "logo":
            continue
        if tayte:
            d.ellipse([x - r, y - r, x + r, y + r], fill=KULTA)
            for dy in (-.18, .18):  # kaksi koristeraitaa pohjan värillä
                d.line([(x - r * .97, y + dy * r), (x + r * .97, y + dy * r)], fill=TAUSTA, width=3 * k)
            d.ellipse([x - r * .62, y - r * .66, x - r * .30, y - r * .34], fill=(232, 214, 160))
        else:
            d.ellipse([x - r, y - r, x + r, y + r], outline=KULTA, width=3 * k)
            tahti(d, x, y, r * .45, KULTA)
    kerros = kerros.resize((W, H), Image.LANCZOS)
    im.paste(kerros, (0, 0), kerros)
    for x, y, r, tayte in pallot:
        if tayte == "logo":
            logo(im, x, y, 2 * r)


LOGOPALLO = (W / 2, 146, 40, "logo")  # keskimmäinen pallo on logo, vain yläreunassa
KANSIPALLOT = [(165, 330, 40, True), (236, 268, 20, False),
               (915, 380, 40, True), (846, 288, 22, False)]
# Ruudukko alkaa y=380, joten pallot roikkuvat lyhyemmässä narussa.
RUUDUKKOPALLOT = [(165, 300, 34, True), (236, 250, 18, False),
                  (915, 318, 34, True), (846, 262, 18, False)]


def ruudukko(luukut, auki, otsikko, saate):
    """24 luukun kalenteri: avatut nimellä, seuraava kultareunalla, muut numerona."""
    im, d = pohja()
    pallot(im, RUUDUKKOPALLOT + [LOGOPALLO])
    for x in (W / 2 - 150, W / 2 + 150):
        tahti(d, x, LOGOPALLO[1], 7, KULTA)
    harvennettu(d, W / 2, 210, MERKKI, dm(26, 600), KULTA, 4, keskelle=True)
    d.text((W / 2, 300), otsikko, font=serif(60, True), fill=KERMA, anchor="mm")

    vali, x0, y0 = 12, 120, 380
    lev = (W - 2 * x0 - 3 * vali) / 4
    kork = 110
    nimet = {j["luukku"]: j["nimi"] for j in luukut}
    for n in range(1, 25):
        x = x0 + (n - 1) % 4 * (lev + vali)
        y = y0 + (n - 1) // 4 * (kork + vali)
        laatikko = [x, y, x + lev, y + kork]
        if n <= auki:
            d.rectangle(laatikko, fill=(20, 84, 46))
            d.text((x + 12, y + 10), str(n), font=dm(20, 600), fill=KULTA)
            for koko in (24, 22, 20, 18, 16):
                rivit, f, _ = rivita(d, nimet.get(n, "?"), koko, lev - 20, tavuta=True)
                if len(rivit) <= 3 and mahtuu(d, rivit, f[True], lev - 20, tavuta=True):
                    break
            else:
                raise SystemExit(f"VIRHE: luukun {n} nimi ei mahdu ruudukkoon")
            yy = y + kork / 2 + 8 - (len(rivit) - 1) * koko * .58
            for rivi in rivit:
                d.text((x + lev / 2, yy), rivin_teksti(rivi, tavuta=True), font=serif(koko, True),
                       fill=KERMA, anchor="mm")
                yy += koko * 1.16
        else:
            d.rectangle(laatikko, outline=KULTA if n == auki + 1 else KEHYS, width=2)
            d.text((x + lev / 2, y + kork / 2), str(n), font=serif(56, True),
                   fill=KULTA if n == auki + 1 else (120, 150, 110), anchor="mm")
    d.text((W / 2, H - 180), saate, font=serif(34), fill=SALVIA, anchor="mm")
    d.text((W / 2, H - 120), "ilmiöt.fi  ·  dataneuvos.fi", font=dm(26), fill=KULTA, anchor="mm")
    return im


def kansi(j):
    im, d = pohja()
    pallot(im, KANSIPALLOT + [LOGOPALLO])
    for x in (W / 2 - 150, W / 2 + 150):
        tahti(d, x, LOGOPALLO[1], 7, KULTA)
    harvennettu(d, W / 2, 210, MERKKI, dm(26, 600), KULTA, 4, keskelle=True)
    d.text((W / 2, 330), "LUUKKU", font=dm(28), fill=SALVIA, anchor="mm")
    d.text((W / 2, 520), str(j["luukku"]), font=serif(340, True), fill=KULTA, anchor="mm")
    d.line([(W / 2 - 60, 720), (W / 2 + 60, 720)], fill=KEHYS, width=2)

    for koko in (84, 76, 68, 60, 54):
        f = serif(koko, True)
        rivit, _, _ = rivita(d, j["nimi"], koko, OIKEA - VASEN)
        if len(rivit) <= 2 and mahtuu(d, rivit, f, OIKEA - VASEN):
            break
    else:
        raise SystemExit(f"VIRHE: luukun {j['luukku']} nimi ei mahdu kanteen")
    y = 810 if len(rivit) == 2 else 850
    for rivi in rivit:
        d.text((W / 2, y), rivin_teksti(rivi), font=f, fill=KERMA, anchor="mm")
        y += koko * 1.07

    rk, _, _ = rivita(d, j["kansi"], 40, OIKEA - VASEN + 80)
    if len(rk) > 3:
        raise SystemExit(f"VIRHE: luukun {j['luukku']} kansivirke on yli 3 riviä")
    y = 1010 if len(rivit) == 2 else 960
    for rivi in rk:
        d.text((W / 2, y), rivin_teksti(rivi), font=serif(40), fill=SALVIA, anchor="mm")
        y += 56
    d.text((W / 2, H - 130), "ilmiöt.fi  ·  dataneuvos.fi", font=dm(26), fill=KULTA, anchor="mm")
    return im


def sisaltosivu(j, s, nro, sivuja, viimeinen):
    im, d = pohja()
    ylatunniste(d, j["luukku"], nro, sivuja)
    d.text((VASEN, 230), s["otsikko"], font=serif(68, True), fill=KERMA)
    d.line([(VASEN, 340), (VASEN + 90, 340)], fill=KULTA, width=3)

    yla, ala = 400, H - (290 if viimeinen else 230)
    for koko in (46, 42, 38, 35):
        korkeus = sum(lohkon_korkeus(d, l, koko) for l in s["lohkot"]) + 44 * (len(s["lohkot"]) - 1)
        if korkeus <= ala - yla:
            break
    else:
        raise SystemExit(f"VIRHE: luukku {j['luukku']}, sivu {nro} ei mahdu — lyhennä")

    y = yla + (ala - yla - korkeus) / 2
    for l in s["lohkot"]:
        if "luku" in l:
            d.text((VASEN, y - 20), l["luku"], font=serif(200, True), fill=KULTA)
            rivit, f, vali = rivita(d, l["selite"], koko, OIKEA - VASEN)
            y = piirra_rivit(d, VASEN, y + 230, rivit, f, vali, koko, SALVIA, KERMA)
        elif "kohta" in l:
            if not re.match(r"\*\*\d", l["kohta"]):  # numeroitu kohta ei tarvitse tähteä
                tahti(d, VASEN + 8, y + koko * 0.62, 8, KULTA)
            rivit, f, vali = rivita(d, l["kohta"], koko, OIKEA - VASEN - 34)
            y = piirra_rivit(d, VASEN + 34, y, rivit, f, vali, koko, SALVIA, KERMA)
        else:
            rivit, f, vali = rivita(d, l["kappale"], koko, OIKEA - VASEN)
            y = piirra_rivit(d, VASEN, y, rivit, f, vali, koko, SALVIA, KERMA)
        y += 44

    seuraava = "Huomenna luukku {}".format(j["luukku"] + 1) if j["luukku"] < 24 else "Hyvää joulua"
    alatunniste(im, d, seuraava if viimeinen else None)
    return im


def tallenna_pdf(kuvat, polku):
    """Minimaalinen PDF: sivu per kuva, raaka RGB zlib-pakattuna (häviötön).
    Koneen PIL:stä puuttuu JPEG-tuki, jota sen oma PDF-tallennus vaatii."""
    osat, sivut = [], []

    def lisaa(data):
        osat.append(data)
        return len(osat)

    puu = 3 * len(kuvat) + 1  # kuva, sisältö ja sivu per kuva, sitten sivupuu
    for k in kuvat:
        raaka = zlib.compress(k.convert("RGB").tobytes(), 9)
        kuva = lisaa(b"<< /Type /XObject /Subtype /Image /Width %d /Height %d "
                     b"/ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /FlateDecode "
                     b"/Length %d >>\nstream\n" % (k.width, k.height, len(raaka)) + raaka + b"\nendstream")
        piirto = b"q %d 0 0 %d 0 0 cm /Im Do Q" % (k.width, k.height)
        sisalto = lisaa(b"<< /Length %d >>\nstream\n%s\nendstream" % (len(piirto), piirto))
        sivut.append(lisaa(b"<< /Type /Page /Parent %d 0 R /MediaBox [0 0 %d %d] "
                           b"/Resources << /XObject << /Im %d 0 R >> >> /Contents %d 0 R >>"
                           % (puu, k.width, k.height, kuva, sisalto)))
    assert lisaa(b"<< /Type /Pages /Kids [%s] /Count %d >>"
                % (b" ".join(b"%d 0 R" % s for s in sivut), len(sivut))) == puu
    juuri = lisaa(b"<< /Type /Catalog /Pages %d 0 R >>" % puu)

    ulos, sijainnit = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"), []
    for i, data in enumerate(osat, 1):
        sijainnit.append(len(ulos))
        ulos += b"%d 0 obj\n" % i + data + b"\nendobj\n"
    xref = len(ulos)
    ulos += b"xref\n0 %d\n0000000000 65535 f \n" % (len(osat) + 1)
    ulos += b"".join(b"%010d 00000 n \n" % s for s in sijainnit)
    ulos += b"trailer\n<< /Size %d /Root %d 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(osat) + 1, juuri, xref)
    polku.write_bytes(bytes(ulos))


# LinkedIn pudottaa liitetyn tekstin tyhjät rivit. Rivi, jolla on näkymätön
# U+2800 (braille-tyhjä), ei ole tyhjä, joten kappalevälit säilyvät.
TYHJA = "\u2800"


def linkedin(teksti):
    return re.sub(r"\n[ \t]*\n", f"\n{TYHJA}\n", teksti.strip())


def postausteksti(j):
    """(postaus, kommentti) LinkedIniin liitettävässä muodossa."""
    tagit = " ".join(["#ilmiökalenteri"] + j["tagit"])
    url = (f"https://www.ilmiöt.fi/{j['slug']}.html?utm_source=linkedin&utm_medium=social"
           f"&utm_campaign=ilmiokalenteri&utm_content=luukku-{j['luukku']:02d}")
    postaus = (f"Dataneuvoksen ilmiökalenteri ✦ Luukku {j['luukku']}/24: {j['nimi']}\n\n"
               f"{j['teksti']}\n\n{j['kysymys']}\n\n"
               f"Koko ilmiö ja vastakeinot ensimmäisessä kommentissa.\n\n{tagit}")
    return linkedin(postaus), f"Koko ilmiö, tunnistusmerkit ja vastakeinot: {url}"


def kirjoita_txt(polku, postaus, kommentti=None):
    teksti = postaus + (f"\n\n--- ENSIMMÄINEN KOMMENTTI ---\n\n{kommentti}" if kommentti else "")
    polku.write_text(teksti.replace("\n", "\r\n") + "\r\n", encoding="utf-8")


def koostesivu(j, luukut):
    n = j["luukku"]
    if n == 24:
        return ruudukko(luukut, 24, "Kaikki luukut auki", "Hyvää joulua, ja kiitos, että avasit ne kanssani")
    return ruudukko(luukut, n, f"Viikko {(n + 1) // 7}", f"{n} luukkua auki, {24 - n} jäljellä")


def on_kooste(j):
    return j["luukku"] == 24 or datetime.date.fromisoformat(j["pvm"]).isoweekday() == 7


def rakenna(polku, luukut):
    j = json.loads(polku.read_text(encoding="utf-8"))
    kooste = on_kooste(j)
    sivuja = 1 + len(j["sivut"]) + kooste
    kuvat = [kansi(j)] + [
        sisaltosivu(j, s, i + 2, sivuja, i == len(j["sivut"]) - 1 and not kooste)
        for i, s in enumerate(j["sivut"])
    ]
    if kooste:
        kuvat.append(koostesivu(j, luukut))
    VALMIS.mkdir(exist_ok=True)
    nimi = polku.stem
    kuvat[0].save(VALMIS / f"{nimi}-kansi.png")
    for i, k in enumerate(kuvat[1:], 2):
        k.save(VALMIS / f"{nimi}-s{i}.png")
    tallenna_pdf(kuvat, VALMIS / f"{nimi}.pdf")
    kirjoita_txt(VALMIS / f"{nimi}.txt", *postausteksti(j))
    print(f"{nimi}: {sivuja} sivua" + (" (kooste)" if kooste else ""))
    return kuvat


ENNAKKO = """Joulukuussa avaan joka aamu yhden luukun: Dataneuvoksen ilmiökalenterissa on 24 työelämän ilmiötä, jotka jokainen asiantuntija on kohdannut.

Mukana on viikkoraportteja, joita kukaan ei lue, kokouksia, jotka venyvät täyttämään varatun ajan, ja projekteja, jotka ovat aina 90 % valmiita. Kevyestä aloitetaan, ja aattoa kohti luukut kovenevat.

Jokaisessa luukussa ilmiö, sen tunnusmerkit ja yksi vastakeino. Taustalla on ilmiöt.fi, suomenkielinen tietopankki yhteiskunnan ja työelämän ilmiöistä.

Ensimmäinen luukku aukeaa huomenna aamulla.

#ilmiökalenteri #työelämä #johtaminen #data
"""


def joululogo(koko, tausta=None):
    """Dataneuvoksen joulupallo erillisenä logona: kultamitali, hattu ja rengas.
    tausta=None → läpinäkyvä; muuten neliö annetulla värillä (profiilikuva)."""
    k = 4
    S = koko * k
    kuva = Image.new("RGBA", (S, S), (0, 0, 0, 0) if tausta is None else tausta + (255,))
    r = S * .34
    x, y = S / 2, S * .59                     # rengas .11 … pallon pohja .93: mahtuu myös pyöreään rajaukseen
    d = ImageDraw.Draw(kuva)
    # rengas kiinni hatussa: ilman narua irrallinen rengas näyttäisi leijuvan
    d.ellipse([x - r * .16, y - r * 1.42, x + r * .16, y - r * 1.10], outline=KULTA, width=round(S * .012))
    d.rectangle([x - r * .26, y - r * 1.12, x + r * .26, y - r * .86], fill=KULTA)
    mitali = _logokuva(round(2 * r))
    kuva.paste(mitali, (round(x - r), round(y - r)), mitali)
    return kuva.resize((koko, koko), Image.LANCZOS)


VIIKONPAIVAT = ["ma", "ti", "ke", "to", "pe", "la", "su"]


def julkaisusivu(polut, luukut):
    """valmis/julkaisu.html: päivän postaus, kommentti ja karuselli yhdellä silmäyksellä,
    kopiointinapit LinkedIn-muotoiseen tekstiin. Avataan selaimessa paikallisesti."""
    kortit = []
    ennakko = (VALMIS / "00-ennakko.txt").read_text(encoding="utf-8").replace("\r\n", "\n").strip()
    kortit.append(("30.11. ma", "Ennakko", "00-ennakko.png", None, ennakko, None, []))
    for polku, j in zip(polut, luukut):
        pv = datetime.date.fromisoformat(j["pvm"])
        sivut = [f"{polku.stem}-kansi.png"] + sorted(
            (p.name for p in VALMIS.glob(f"{polku.stem}-s*.png")), key=lambda n: int(n.rsplit("-s", 1)[1][:-4]))
        postaus, kommentti = postausteksti(j)
        kortit.append((f"{pv.day}.{pv.month}. {VIIKONPAIVAT[pv.weekday()]}", f"{j['luukku']}. {j['nimi']}",
                       sivut[0], f"{polku.stem}.pdf", postaus, kommentti, sivut))
    osat = []
    for i, (pvm, nimi, kansi, pdf, postaus, kommentti, sivut) in enumerate(kortit):
        e = lambda t: t.replace("&", "&amp;").replace("<", "&lt;")
        napit = f'<button data-k="p{i}">Kopioi postaus</button>'
        if kommentti:
            napit += f'<button data-k="k{i}">Kopioi kommentti</button>'
        if pdf:
            napit += f'<a href="{pdf}">Karuselli (PDF)</a>'
        kuvat = "".join(f'<a href="{s}"><img src="{s}" loading="lazy" alt=""></a>' for s in sivut[1:])
        osat.append(f"""<section><img class="kansi" src="{kansi}" alt="">
<div><p class="pvm">{pvm}</p><h2>{e(nimi)}</h2><div class="napit">{napit}</div>
<pre id="p{i}">{e(postaus)}</pre>{f'<pre id="k{i}" class="kommentti">{e(kommentti)}</pre>' if kommentti else ''}
<div class="sivut">{kuvat}</div></div></section>""")
    (VALMIS / "julkaisu.html").write_text(f"""<!doctype html><html lang="fi"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Ilmiökalenteri – julkaisu</title>
<style>
body{{margin:0;background:#083e20;color:#F5F0E5;font:16px/1.5 system-ui,sans-serif;padding:24px}}
h1{{color:#C9A84C;font-weight:600;letter-spacing:.08em;font-size:18px;text-transform:uppercase}}
section{{display:grid;grid-template-columns:220px 1fr;gap:24px;padding:24px 0;border-top:1px solid #46704a}}
.kansi{{width:220px}} h2{{margin:0 0 12px;font-size:22px}} .pvm{{margin:0;color:#C9A84C}}
.napit{{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px}}
button,.napit a{{background:#C9A84C;color:#1C1400;border:0;padding:8px 14px;font:inherit;font-weight:600;cursor:pointer;text-decoration:none;border-radius:4px}}
button.ok{{background:#F5F0E5}}
pre{{white-space:pre-wrap;background:#145430;padding:12px;max-height:180px;overflow:auto;font:14px/1.45 system-ui,sans-serif;margin:0 0 8px}}
.kommentti{{max-height:none}} .sivut img{{width:110px;margin:4px 4px 0 0}}
@media (max-width:640px){{section{{grid-template-columns:1fr}}}}
</style><h1>Dataneuvoksen ilmiökalenteri – julkaisulista</h1>
<p>Napit kopioivat tekstin muodossa, jossa kappalevälit säilyvät LinkedInissä.
Karuselli: LinkedInin postausikkunassa <b>+</b> → <b>Add a document</b> → PDF.</p>
{''.join(osat)}
<script>
document.addEventListener('click', function (e) {{
  const b = e.target.closest('button'); if (!b) return;
  const t = document.getElementById(b.dataset.k).textContent;
  const valmis = function () {{ const v = b.textContent; b.textContent = 'Kopioitu ✓'; b.classList.add('ok');
    setTimeout(function () {{ b.textContent = v; b.classList.remove('ok'); }}, 1500); }};
  if (navigator.clipboard) navigator.clipboard.writeText(t).then(valmis, vara); else vara();
  function vara() {{ const a = document.createElement('textarea'); a.value = t; document.body.appendChild(a);
    a.select(); document.execCommand('copy'); a.remove(); valmis(); }}
}});
</script></html>
""", encoding="utf-8")
    print("julkaisu.html")


def main():
    valitut = {int(a) for a in sys.argv[1:]}
    polut = sorted((ROOT / "luukut").glob("*.json"))
    luukut = [json.loads(p.read_text(encoding="utf-8")) for p in polut]
    VALMIS.mkdir(exist_ok=True)
    if not valitut or 0 in valitut:
        ruudukko(luukut, 0, "Joulukuu 2026", "Luukku aukeaa joka aamu 1.–24.12.").save(VALMIS / "00-ennakko.png")
        kirjoita_txt(VALMIS / "00-ennakko.txt", linkedin(ENNAKKO))
        print("00-ennakko: ruudukko")
    for polku in polut:
        if not valitut or int(polku.name[:2]) in valitut:
            rakenna(polku, luukut)
    julkaisusivu(polut, luukut)
    joululogo(1024).save(VALMIS / "joululogo.png")
    joululogo(1024, TAUSTA).save(VALMIS / "joululogo-vihrea.png")


if __name__ == "__main__":
    main()
