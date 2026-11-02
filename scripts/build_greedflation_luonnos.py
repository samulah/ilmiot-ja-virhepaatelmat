#!/usr/bin/env python3
"""Generoi luonnoksen luonnokset/greedflation.html (2.11.2026).

Greedflation kirjoitetaan kokonaan suklaan hinnan näkökulmasta: kaakaon
maailmanmarkkinahinta nousi 2023–2025 nelinkertaiseksi ja putosi 2026 alussa
70 %, joten suklaa on harvinaisen puhdas koe sille, laskeeko hinta yhtä
nopeasti kuin nousi. Sivulla on kaksi itse piirrettyä SVG-kuvaajaa (ei
ulkoisia kirjastoja) ja mermaid-kaavio sivuston tapaan.

Sijainti: Myyntikikat ja painostus, heti shrinkflaation perään. Julkaisussa
    UUDET = {"greedflation": ("shrinkflaatio", VARI, NIMI, KUVAUS)}
    python3 scripts/lisaa_ilmiot.py --kirjoita
jolloin lisaa_ilmiot.py pujottaa kortin ja numeroi kaiken uudelleen. Luonnoksen
numero 93 / 166 olettaa, että kannustin-erä (166–174) julkaistaan vasta tämän
jälkeen. Jos kannustin-erä menee ensin, sen build_kannustin_luonnokset.py:n
`len(kortit) == 165`-tarkistus on päivitettävä kummassakin järjestyksessä.

Data (haettu 2.11.2026, upotettu tähän toistettavuuden vuoksi):
  KAAKAO  Maailmanpankki, Pink Sheet (CMO-Historical-Data-Monthly.xlsx),
          sarake "Cocoa", $/kg, kuukausikeskiarvo
  SUKLAA  Tilastokeskus, KHI 15b5 (2025=100), hyödyke 01.1.8.5
          "Suklaa, kaakao ja kaakaopohjaiset elintarvikkeet"
Molemmat indeksoidaan kuvaajaan tammikuu 2023 = 100.

Pohja ja apufunktiot ovat samat kuin kannustin-erässä (goodhartin-laki.html,
build_kannustin_luonnokset.py), jotta sivu on rakenteeltaan identtinen.

Ajo:  python3 scripts/build_greedflation_luonnos.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import build_kannustin_luonnokset as K  # noqa: E402  (ei kirjoita mitään importissa)

SLUG = "greedflation"
NUM = 93
YHTEENSA = 166
VARI = "#7b3f00"
NIMI = "Greedflation"
KORTTI_KUVAUS = "Kustannus laskee, hinta ei: suklaa paljastaa, milloin korotus on katetta eikä kulua."
EDELLINEN = "shrinkflaatio"
SEURAAVA = "suunniteltu-vanheneminen"

KAT_NIMI = "Myyntikikat ja painostus"
KAT_SIVU = "kategoria-myyntikikat-ja-painostus.html"

PVM_ISO = "2026-11-02"
PVM_FI = "2.11.2026"

# Kaksi versiota samasta sivusta. JULKAISTAVA kirjoitetaan nimelle greedflation.html
# (= se, jonka lisaa_ilmiot.py julkaisee), muut nimelle greedflation-<versio>.html.
JULKAISTAVA = "suklaa"

KUUKAUDET = [f"{v}M{k:02d}" for v in range(2022, 2027) for k in range(1, 13)][:57]  # → 2026M09
KAAKAO = [2.47, 2.55, 2.46, 2.46, 2.37, 2.32, 2.24, 2.32, 2.30, 2.31, 2.41, 2.51,
          2.62, 2.65, 2.75, 2.88, 2.96, 3.17, 3.39, 3.46, 3.61, 3.63, 4.03, 4.21,
          4.40, 5.56, 7.09, 9.74, 7.54, 8.27, 7.09, 6.88, 6.52, 6.66, 7.89, 10.32,
          10.75, 9.86, 8.08, 8.15, 8.99, 8.40, 7.37, 7.60, 7.03, 5.95, 5.61, 5.78,
          4.97, 3.59, 3.24, 3.40, 4.16, 4.40, 5.61, 5.95, 5.92]
SUKLAA = [66.52, 66.99, 66.82, 67.27, 69.36, 69.03, 70.34, 69.63, 71.01, 72.68, 71.95, 69.35,
          75.92, 76.56, 76.56, 74.54, 75.48, 78.33, 80.60, 76.43, 76.94, 76.54, 78.84, 74.87,
          78.71, 78.61, 79.33, 77.80, 81.96, 81.84, 84.03, 84.61, 88.69, 93.46, 94.44, 80.25,
          97.93, 98.87, 99.40, 96.56, 103.30, 99.07, 106.23, 99.16, 101.86, 100.58, 101.46, 95.52,
          100.13, 104.97, 104.86, 100.56, 99.44, 101.93, 106.07, 103.38, 101.30]
assert len(KUUKAUDET) == len(KAAKAO) == len(SUKLAA) == 57 and KUUKAUDET[-1] == "2026M09"


def kk(tunnus):
    return KUUKAUDET.index(tunnus)


def muutos(sarja, a, b):
    return round((sarja[kk(b)] / sarja[kk(a)] - 1) * 100)


# Tekstin luvut lasketaan datasta, jotta teksti ja kuvaaja eivät voi erota.
L = dict(
    kaakao_x=round(KAAKAO[kk("2025M01")] / KAAKAO[kk("2023M01")], 1),   # 4,1-kertainen
    suklaa_ylos=muutos(SUKLAA, "2023M01", "2025M01"),                   # +29
    kaakao_pohja=-muutos(KAAKAO, "2025M01", "2026M03"),                 # 70
    kaakao_nyt=-muutos(KAAKAO, "2025M01", "2026M09"),                   # 45
    suklaa_huipusta=-muutos(SUKLAA, "2025M07", "2026M09"),              # 5
    suklaa_helmikuusta=round((1 - SUKLAA[kk("2026M09")] / SUKLAA[kk("2026M02")]) * 100, 1),  # 3,5
    joulu24=-muutos(SUKLAA, "2024M11", "2024M12"),                      # 15
)
assert L == dict(kaakao_x=4.1, suklaa_ylos=29, kaakao_pohja=70, kaakao_nyt=45,
                 suklaa_huipusta=5, suklaa_helmikuusta=3.5, joulu24=15), L


# ── versio B: ruokakori ──
# Tilastokeskus KHI 15b5: 011 Elintarvikkeet ja SSS kokonaisindeksi, 2021M01–2026M09.
KUUKAUDET_B = [f"{v}M{k:02d}" for v in range(2021, 2027) for k in range(1, 13)][:69]
RUOKA = [81.79, 82.08, 82.41, 82.42, 82.03, 81.71, 81.66, 81.85, 81.96, 82.17, 82.71, 82.69,
         83.81, 85.19, 85.76, 86.58, 88.91, 90.2, 91.47, 91.82, 93.99, 95.2, 96.36, 96.32,
         97.44, 99.91, 100.89, 99.49, 99.54, 99.07, 99.38, 98.37, 98.4, 99.09, 99.27, 98.63,
         98.88, 99.15, 99.01, 98.65, 98.62, 98.18, 98.62, 97.65, 98.2, 98.8, 99.27, 98.33,
         99.1, 99.87, 100.37, 100.34, 100.28, 99.31, 100.52, 99.61, 100.22, 99.78, 100.45, 100.09,
         99.92, 100.84, 101.05, 101.15, 100.6, 99.55, 100.52, 100.43, 101.33]
KAIKKI = [84.9, 85.18, 85.47, 85.77, 85.83, 85.82, 86.07, 86.33, 86.65, 87.2, 87.69, 87.62,
          88.64, 89.01, 90.42, 90.66, 91.84, 92.51, 92.79, 92.89, 93.67, 94.43, 95.67, 95.6,
          96.08, 96.84, 97.57, 97.83, 98.08, 98.34, 98.82, 98.09, 98.82, 99.06, 98.83, 99.04,
          99.25, 99.75, 99.71, 99.69, 99.56, 99.62, 99.81, 99.27, 99.61, 100.15, 99.81, 99.73,
          99.95, 100.25, 100.21, 100.18, 100.05, 99.82, 100.01, 99.77, 100.11, 99.95, 99.71, 99.93,
          99.78, 100.83, 101.56, 101.68, 102.14, 101.89, 102.14, 101.95, 102.63]
assert len(KUUKAUDET_B) == len(RUOKA) == len(KAIKKI) == 69 and KUUKAUDET_B[-1] == "2026M09"
RUOKA_INFLAATIO_HUIPPU = 17.6   # KHI 15b5, 011 vuosimuutos 2023M03 (sarjan huippu)
SUKLAAN_PAINO = round(3.79 / 120.16 * 100)  # KHI 15bc painopromillet 2026: 01185 / 011 → 3 %

# Raaka-aine ja sitä vastaava hyllyhinta, kumpikin omasta huipustaan syyskuuhun 2026.
# (nimi, raaka-aine, huippukk, huippu, 9/2026, hylly, huippukk, huippu, 9/2026)
# Raaka-aineet: Maailmanpankki ($), hylly: KHI 15b5 (01185, 01220, 01151, 01181, 01112).
PARIT = [
    ("Suklaa", "kaakao", "1/2025", 10.75, 5.92, "suklaa", "7/2025", 106.23, 101.30),
    ("Kahvi", "arabica", "2/2025", 9.05, 7.26, "kahvi", "7/2025", 119.77, 102.06),
    ("Kasviöljy", "rypsiöljy", "4/2022", 2266.0, 1440.0, "kasviöljyt", "9/2024", 111.26, 89.54),
    ("Sokeri", "raakasokeri", "9/2023", 0.58, 0.41, "sokeri", "2/2024", 118.58, 99.16),
    ("Jauhot", "vehnä", "5/2022", 522.3, 347.0, "jauhot", "6/2023", 107.24, 98.06),
]
PARI_MUUTOS = [(p[0], round((p[4] / p[3] - 1) * 100), round((p[8] / p[7] - 1) * 100)) for p in PARIT]
assert PARI_MUUTOS == [("Suklaa", -45, -5), ("Kahvi", -20, -15), ("Kasviöljy", -36, -20),
                       ("Sokeri", -29, -16), ("Jauhot", -34, -9)], PARI_MUUTOS


def kk_b(tunnus):
    return KUUKAUDET_B.index(tunnus)


def muutos_b(sarja, a, b):
    return round((sarja[kk_b(b)] / sarja[kk_b(a)] - 1) * 100, 1)


LB = dict(
    ruoka_ylos=round(muutos_b(RUOKA, "2021M01", "2023M03")),     # +23
    kaikki_ylos=round(muutos_b(KAIKKI, "2021M01", "2023M03")),   # +15
    ruoka_sitten=muutos_b(RUOKA, "2023M03", "2026M09"),          # +0,4
    kaikki_sitten=muutos_b(KAIKKI, "2023M03", "2026M09"),        # +5,2
)
assert LB == dict(ruoka_ylos=23, kaikki_ylos=15, ruoka_sitten=0.4, kaikki_sitten=5.2), LB


def fi(x):
    return str(x).replace(".", ",")


# ──────────────────────────── kuvaajat ────────────────────────────

def kuvaaja_kaakao_suklaa():
    """Kaksi viivaa samalla akselilla, tammikuu 2023 = 100. Yksi akseli
    tarkoituksella: kaksois-y-akselilla käyrät saisi näyttämään miltä tahansa."""
    w, h, ml, mr, mt, mb = 400, 250, 30, 70, 14, 24
    ymax = 450
    x = lambda i: ml + i * (w - ml - mr) / (len(KUUKAUDET) - 1)
    y = lambda v: mt + (1 - v / ymax) * (h - mt - mb)
    pohja_k, pohja_s = KAAKAO[kk("2023M01")], SUKLAA[kk("2023M01")]
    ik = [v / pohja_k * 100 for v in KAAKAO]
    isu = [v / pohja_s * 100 for v in SUKLAA]

    def polku(sarja):
        return " ".join(f"{'M' if i == 0 else 'L'}{x(i):.1f},{y(v):.1f}" for i, v in enumerate(sarja))

    osat = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-labelledby="kv1-t kv1-d" '
            f'style="width:100%;height:auto;display:block;font-family:\'DM Sans\',system-ui,sans-serif">',
            '<title id="kv1-t">Kaakaon ja suklaan hinta 2022–2026</title>',
            f'<desc id="kv1-d">Kaakaon maailmanmarkkinahinta nousi tammikuusta 2023 tammikuuhun 2025 '
            f'{fi(L["kaakao_x"])}-kertaiseksi ja putosi maaliskuuhun 2026 mennessä {L["kaakao_pohja"]} prosenttia. '
            f'Suklaan kuluttajahinta Suomessa nousi samassa ajassa {L["suklaa_ylos"]} prosenttia eikä ole juuri laskenut.</desc>']
    for v in (100, 200, 300, 400):
        vahva = v == 100
        osat.append(f'<line x1="{ml}" x2="{w - mr}" y1="{y(v):.1f}" y2="{y(v):.1f}" '
                    f'stroke="{"#8B6914" if vahva else "#e3dccb"}" stroke-width="{1.2 if vahva else 1}"'
                    f'{"" if vahva else " stroke-dasharray=\"3 3\""}/>')
        osat.append(f'<text x="{ml - 6}" y="{y(v) + 4:.1f}" font-size="11" fill="#6b5a2e" text-anchor="end">{v}</text>')
    for vuosi in range(2022, 2027):
        i = kk(f"{vuosi}M01")
        osat.append(f'<line x1="{x(i):.1f}" x2="{x(i):.1f}" y1="{h - mb}" y2="{h - mb + 4}" stroke="#8B6914"/>')
        osat.append(f'<text x="{x(i):.1f}" y="{h - 8}" font-size="11" fill="#6b5a2e" text-anchor="middle">{vuosi}</text>')
    osat.append(f'<path d="{polku(ik)}" fill="none" stroke="#c97a2b" stroke-width="1.8" stroke-linejoin="round"/>')
    osat.append(f'<path d="{polku(isu)}" fill="none" stroke="#3e1f08" stroke-width="2.4" stroke-linejoin="round"/>')
    # suorat nimiöt viivojen päihin — ei erillistä selitettä
    n = len(KUUKAUDET) - 1
    osat.append(f'<text x="{x(n) + 6:.1f}" y="{y(ik[n]) + 4:.1f}" font-size="12" font-weight="600" fill="#a85f17">Kaakao {ik[n]:.0f}</text>')
    osat.append(f'<text x="{x(n) + 6:.1f}" y="{y(isu[n]) + 4:.1f}" font-size="12" font-weight="600" fill="#3e1f08">Suklaa {isu[n]:.0f}</text>')
    # kaksi merkittyä kohtaa: huippu ja pohja
    for tunnus, teksti, dx, dy, ank in (("2025M01", "huippu 1/2025", 0, -9, "middle"),
                                        ("2026M03", "pohja 3/2026", -8, 22, "end")):
        i = kk(tunnus)
        osat.append(f'<circle cx="{x(i):.1f}" cy="{y(ik[i]):.1f}" r="3" fill="#c97a2b"/>')
        osat.append(f'<text x="{x(i) + dx:.1f}" y="{y(ik[i]) + dy:.1f}" font-size="11" fill="#a85f17" '
                    f'text-anchor="{ank}">{teksti}: {ik[i]:.0f}</text>')
    osat.append("</svg>")
    return "\n".join(osat)


def kuvaaja_joulu():
    """Marras–joulu–tammi kolmena vuonna: joulukuun notkahdus on tarjouskausi,
    ei kaakaon hinta. Pylväät alkavat nollasta — sivusto, jolla on oma sivu
    katkaistuista akseleista, ei katkaise omiaan."""
    jaksot = [("2023–24", "2023M11", "2023M12", "2024M01"),
              ("2024–25", "2024M11", "2024M12", "2025M01"),
              ("2025–26", "2025M11", "2025M12", "2026M01")]
    w, h, mt, mb = 400, 220, 16, 40
    ymin, ymax = 0, 110
    y = lambda v: mt + (1 - (v - ymin) / (ymax - ymin)) * (h - mt - mb)
    osat = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-labelledby="kv2-t kv2-d" '
            f'style="width:100%;height:auto;display:block;font-family:\'DM Sans\',system-ui,sans-serif">',
            '<title id="kv2-t">Suklaan hinta marras-, joulu- ja tammikuussa</title>',
            f'<desc id="kv2-d">Suklaan hintaindeksi laskee joka joulukuu ja palaa tammikuussa. '
            f'Joulukuussa 2024 indeksi oli {L["joulu24"]} prosenttia marraskuuta alempana.</desc>']
    leveys, vali = 30, 3
    ryhma = 3 * leveys + 2 * vali
    alku = 14
    rako = (w - 2 * alku - 3 * ryhma) / 2
    for j, (nimi, *kuut) in enumerate(jaksot):
        x0 = alku + j * (ryhma + rako)
        for k, (tunnus, kuu) in enumerate(zip(kuut, ("marras", "joulu", "tammi"))):
            v = SUKLAA[kk(tunnus)]
            xx = x0 + k * (leveys + vali)
            vari = "#c97a2b" if kuu == "joulu" else "#3e1f08"
            osat.append(f'<rect x="{xx:.1f}" y="{y(v):.1f}" width="{leveys}" height="{y(ymin) - y(v):.1f}" fill="{vari}" rx="2"/>')
            osat.append(f'<text x="{xx + leveys / 2:.1f}" y="{y(v) - 5:.1f}" font-size="11" fill="#3e1f08" text-anchor="middle">{v:.0f}</text>')
            osat.append(f'<text x="{xx + leveys / 2:.1f}" y="{h - mb + 14}" font-size="10" fill="#6b5a2e" text-anchor="middle">{kuu}</text>')
        osat.append(f'<text x="{x0 + ryhma / 2:.1f}" y="{h - 8}" font-size="12" font-weight="600" fill="#3e1f08" text-anchor="middle">{nimi}</text>')
    osat.append(f'<line x1="{alku - 4}" x2="{w - alku + 4}" y1="{y(ymin):.1f}" y2="{y(ymin):.1f}" stroke="#8B6914"/>')
    osat.append("</svg>")
    return "\n".join(osat)


def kuvaaja_ruokakori():
    """Ruoka vs. kaikki kuluttajahinnat, tammikuu 2021 = 100."""
    w, h, ml, mr, mt, mb = 400, 230, 30, 92, 12, 24
    ymin, ymax = 95, 130
    x = lambda i: ml + i * (w - ml - mr) / (len(KUUKAUDET_B) - 1)
    y = lambda v: mt + (1 - (v - ymin) / (ymax - ymin)) * (h - mt - mb)
    r_ = [v / RUOKA[0] * 100 for v in RUOKA]
    k_ = [v / KAIKKI[0] * 100 for v in KAIKKI]

    def polku(sarja):
        return " ".join(f"{'M' if i == 0 else 'L'}{x(i):.1f},{y(v):.1f}" for i, v in enumerate(sarja))

    osat = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-labelledby="kv3-t kv3-d" '
            f'style="width:100%;height:auto;display:block;font-family:\'DM Sans\',system-ui,sans-serif">',
            '<title id="kv3-t">Ruoan hinta ja kaikki kuluttajahinnat 2021–2026</title>',
            f'<desc id="kv3-d">Ruoan hinta nousi tammikuusta 2021 maaliskuuhun 2023 {LB["ruoka_ylos"]} prosenttia, '
            f'kaikki kuluttajahinnat {LB["kaikki_ylos"]} prosenttia. Sen jälkeen ruoan hinta on pysynyt '
            f'paikallaan ja muut hinnat ovat kuroneet eroa kiinni.</desc>']
    for v in (100, 110, 120, 130):
        osat.append(f'<line x1="{ml}" x2="{w - mr}" y1="{y(v):.1f}" y2="{y(v):.1f}" '
                    f'stroke="{"#8B6914" if v == 100 else "#e3dccb"}"{"" if v == 100 else " stroke-dasharray=\"3 3\""}/>')
        osat.append(f'<text x="{ml - 6}" y="{y(v) + 4:.1f}" font-size="11" fill="#6b5a2e" text-anchor="end">{v}</text>')
    for vuosi in range(2021, 2027):
        i = kk_b(f"{vuosi}M01")
        osat.append(f'<text x="{x(i):.1f}" y="{h - 7}" font-size="11" fill="#6b5a2e" text-anchor="middle">{vuosi}</text>')
    i = kk_b("2023M03")
    osat.append(f'<line x1="{x(i):.1f}" x2="{x(i):.1f}" y1="{mt}" y2="{h - mb}" stroke="#c0392b" stroke-dasharray="2 3"/>')
    osat.append(f'<text x="{x(i) + 4:.1f}" y="{mt + 10}" font-size="10.5" fill="#c0392b">3/2023: ruoka pysähtyy</text>')
    osat.append(f'<path d="{polku(k_)}" fill="none" stroke="#c97a2b" stroke-width="1.8" stroke-linejoin="round"/>')
    osat.append(f'<path d="{polku(r_)}" fill="none" stroke="#3e1f08" stroke-width="2.4" stroke-linejoin="round"/>')
    n = len(KUUKAUDET_B) - 1
    osat.append(f'<text x="{x(n) + 6:.1f}" y="{y(r_[n]) - 2:.1f}" font-size="12" font-weight="600" fill="#3e1f08">Ruoka {r_[n]:.0f}</text>')
    osat.append(f'<text x="{x(n) + 6:.1f}" y="{y(k_[n]) + 12:.1f}" font-size="12" font-weight="600" fill="#a85f17">Kaikki {k_[n]:.0f}</text>')
    osat.append("</svg>")
    return "\n".join(osat)


def kuvaaja_parit():
    """Vaakapylväät: raaka-aineen ja hyllyhinnan lasku kumpikin omasta huipustaan.
    Asteikko alkaa nollasta, joten pylväiden pituudet ovat suoraan vertailukelpoisia."""
    w, rivi, ml, mt = 400, 46, 84, 20
    h = mt + rivi * len(PARIT) + 6
    skaala = (w - ml - 40) / 50          # 50 % = koko leveys
    osat = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-labelledby="kv4-t kv4-d" '
            f'style="width:100%;height:auto;display:block;font-family:\'DM Sans\',system-ui,sans-serif">',
            '<title id="kv4-t">Raaka-aineen ja hyllyhinnan lasku huipusta</title>',
            '<desc id="kv4-d">' + "; ".join(f"{n}: raaka-aine {r} %, hylly {s} %" for n, r, s in PARI_MUUTOS) + '</desc>',
            f'<rect x="{ml}" y="2" width="10" height="10" fill="#c97a2b"/>'
            f'<text x="{ml + 14}" y="11" font-size="11" fill="#6b5a2e">raaka-aine maailmalla</text>',
            f'<rect x="{ml + 150}" y="2" width="10" height="10" fill="#3e1f08"/>'
            f'<text x="{ml + 164}" y="11" font-size="11" fill="#6b5a2e">hyllyhinta Suomessa</text>']
    for j, ((nimi, raaka, *_), (_, rm, sm)) in enumerate(zip(PARIT, PARI_MUUTOS)):
        y0 = mt + j * rivi
        vahva = ' font-weight="700"' if nimi == "Suklaa" else ""
        osat.append(f'<text x="{ml - 8}" y="{y0 + 16}" font-size="12" fill="#3e1f08" text-anchor="end"{vahva}>{nimi}</text>')
        osat.append(f'<text x="{ml - 8}" y="{y0 + 29}" font-size="10" fill="#8B6914" text-anchor="end">({raaka})</text>')
        for k, (arvo, vari) in enumerate(((rm, "#c97a2b"), (sm, "#3e1f08"))):
            yy = y0 + 6 + k * 16
            pit = -arvo * skaala
            osat.append(f'<rect x="{ml}" y="{yy}" width="{pit:.1f}" height="13" fill="{vari}" rx="1.5"/>')
            osat.append(f'<text x="{ml + pit + 5:.1f}" y="{yy + 11}" font-size="11" fill="#3e1f08">−{-arvo} %</text>')
    osat.append(f'<line x1="{ml}" x2="{ml}" y1="{mt}" y2="{h - 4}" stroke="#8B6914"/>')
    osat.append("</svg>")
    return "\n".join(osat)


def kuva(svg, selitys):
    return (f'<figure style="margin:1.6rem 0 0;padding:0.9rem 0.9rem 0.4rem;background:#fdfaf2;'
            f'border:1px solid #e3dccb;">\n<div style="max-width:560px;margin:0 auto;">\n{svg}\n</div>\n</figure>\n'
            f'<p class="kaavio-selitys">{selitys}</p>')


# ──────────────────────────── sisältö ────────────────────────────

SISALTO_SUKLAA = rf"""
<p><strong>Greedflation</strong> (suomeksi myös <em>ahneusinflaatio</em>; taloustieteessä <em>sellers' inflation</em>, myyjien inflaatio) tarkoittaa inflaatiota, jossa yritykset nostavat hintoja enemmän kuin niiden kustannukset nousevat. Yleinen hintojen nousu antaa korotukselle suojan: kun kaikki kallistuu, yksittäinen korotus ei erotu joukosta. Suklaa on ilmiölle hyvä koekappale, koska sen pääraaka-aineen hinta on julkinen ja heilahti viime vuosina rajummin kuin minkään muun ruoan.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Onko jokainen hinnankorotus ahneutta?</h2>
<p style="margin:0.4em 0 0;">Ei ole. Greedflation tarkoittaa, että <strong>kate</strong> kasvaa, ei sitä, että hinta nousee. Jos kaakao nelinkertaistuu ja suklaa kallistuu, valmistaja voi silti tienata vähemmän kuin ennen. Ilmiön paljastaa vasta epäsymmetria: hinta seuraa kustannusta nopeasti ylös ja hitaasti alas. Bensiinin hinnoista tämä tunnetaan nimellä <em>rockets and feathers</em>, raketti ylös ja höyhen alas.</p>
</div>
{kuva(kuvaaja_kaakao_suklaa(),
      "Kaakaon maailmanmarkkinahinta (Maailmanpankki, $/kg) ja suklaan kuluttajahinta Suomessa "
      "(Tilastokeskus) samalla asteikolla, tammikuu 2023 = 100. Aloituskohta on valittu: kaakaon "
      "nousu alkoi silloin.")}
<p>Ylösmennessä suklaa jäi jälkeen. Kun kaakao oli tammikuussa 2025 {fi(L["kaakao_x"])}-kertainen kahden vuoden takaiseen, suklaa oli kallistunut {L["suklaa_ylos"]} prosenttia. Valmistajat söivät osan noususta katteistaan, joten tämä vaihe ei ollut greedflationia. Alas tullessa kuva kääntyy. Kaakao halpeni maaliskuuhun 2026 mennessä {L["kaakao_pohja"]} prosenttia ja oli syyskuussa yhä {L["kaakao_nyt"]} prosenttia huippuaan halvempaa. Suklaa oli syyskuussa vain {L["suklaa_huipusta"]} prosenttia kesän 2025 huippuaan halvempaa.</p>
<div class="infolaatikko">
<h2 class="laatikko-otsikko">Dokumentoituja tapauksia:</h2>
<ul style="margin:0.5em 0 0;">
<li><strong>Fazer (marraskuu 2025):</strong> Fazer selitti hitaan laskun suojauksilla. Kaakao ostetaan etukäteen sovittuun hintaan, ja kauppojen pitkät sopimukset hidastavat hyllyhintojen muutoksia.</li>
<li><strong>Luonnonvarakeskus (helmikuu 2026):</strong> Tutkimusprofessori Jyrki Niemi arvioi, että suklaa halpenee vielä saman vuoden aikana. Syyskuuhun mennessä hinta oli laskenut helmikuusta {fi(L["suklaa_helmikuusta"])} prosenttia.</li>
<li><strong>Lindt (syyskuu 2026):</strong> Toimitusjohtaja Adalbert Lechnerin mukaan Lindt ei suojaustensa takia juuri hyötynyt halvemmasta kaakaosta vuonna 2026. Yhtiö lupasi laskea joulutuotteiden hintoja heti ja muiden tuotteiden hintoja tammikuusta 2027.</li>
<li><strong>Nestlé (heinäkuu 2026):</strong> Nestlé kertoi odottavansa katteidensa paranevan, kun kaakao halpenee. Hintojen laskusta yhtiö ei puhunut.</li>
<li><strong>Euroalue (2022–2023):</strong> IMF:n tutkijoiden mukaan yritysten voittojen kasvu selitti 45 prosenttia euroalueen kuluttajahintojen noususta vuoden 2022 alusta vuoden 2023 alkuun. Tuontihinnat selittivät 40 prosenttia.</li>
</ul>
</div>
{kuva(kuvaaja_joulu(),
      "Suklaan hintaindeksi marras-, joulu- ja tammikuussa (Tilastokeskus, 2025 = 100). "
      "Joulukuun notkahdus toistuu joka vuosi.")}
<p>Joulusuklaa on poikkeus, joka hämää. Suklaan hintaindeksi painuu joka joulukuu, kun kaupat kilpailevat joulun tarjouksilla: joulukuussa 2024 se oli {L["joulu24"]} prosenttia marraskuuta alempana. Tammikuussa hinta palasi marraskuun tasolle tai sen yli. Halpa joulusuklaa kertoo kaupan kilpailusta, ei siitä, että suklaa olisi halventunut.</p>
<div class="mermaid">
flowchart TD
  A["Kustannus nousee"] --&gt; B["Hinta nousee heti\n(raketti)"]
  C["Kustannus laskee"] --&gt; D["Hinta laskee hitaasti\n(höyhen)"]
  D --&gt; E["Välissä kate kasvaa"]
  style B fill:#f0f6fd,stroke:#2980b9
  style E fill:#fdf0f0,stroke:#c0392b
    </div>
<p class="kaavio-selitys">Suojausviive selittää höyhenen hetken. Jos lasku ei tule koskaan, kyse on katteesta.</p>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Testikysymys kuuluu: laskeeko hinta, kun kustannus laskee? Anna vastaukselle aikaa, sillä suojaukset ja sopimukset ovat todellinen syy viiveeseen. Viive ei kuitenkaan selitä pysyvää eroa. Suklaan testi on vuosi 2027: jos kaakao pysyy halpana mutta hyllyhinta ei laske, kate kasvaa. Hinta ei kerro ahneudesta, kate kertoo, ja pörssiyhtiöiden liikevoittoprosentti löytyy osavuosikatsauksista. Katso kaupassa myös yksikköhintaa, sillä korotus voi piiloutua pienempään pakkaukseen (ks. <a href="shrinkflaatio.html">shrinkflaatio</a>). Kuluttajan tehokkain keino on vaihtaa merkkiä. Lindtin mukaan hintojen ja myyntimäärien välillä on suora yhteys, ja juuri myynnin hiipuminen sai yhtiön laskemaan hintoja. Suhtaudu varauksella myös sanaan itseensä: "ahneet yritykset" on helppo syyllinen, mutta oikea kysymys on, miksi kilpailu ei pakota hintoja alas.
    </div>
""" + K.lue_lisaa(
    [("Sellers' Inflation, Profits and Conflict", "Isabella M. Weber &amp; Evan Wasner, Review of Keynesian Economics 11:2 (2023)"),
     ("Euro Area Inflation after the Pandemic and Energy Shock", "Hansen, Toscani &amp; Zhou, IMF Working Paper 23/131 (2023)"),
     ("Rockets and feathers", "Robert W. Bacon, Energy Economics 13:3 (1991)")],
    [("https://pxdata.stat.fi/PxWeb/pxweb/fi/StatFin/StatFin__khi/statfin_khi_pxt_15b5.px/",
      "Tilastokeskus: Kuluttajahintaindeksi hyödykkeittäin (taulukko 15b5)"),
     ("https://www.worldbank.org/en/research/commodity-markets",
      "Maailmanpankki: Commodity Markets (Pink Sheet, englanniksi)"),
     ("https://www.ts.fi/a/6827743",
      "Turun Sanomat: Miksi suklaa ei halpene, vaikka kaakaon hinta on romahtanut? Fazer selittää (20.11.2025)"),
     ("https://yle.fi/a/74-20210155", "Yle: Suklaa halpenee pian – kaakaon hinta lähti laskuun (14.2.2026)"),
     ("https://www.swissinfo.ch/eng/lindt-to-cut-prices-as-chocolate-demand-wanes-in-key-markets/92135636",
      "Swissinfo/Bloomberg: Lindt to Cut Prices as Chocolate Demand Wanes (29.9.2026, englanniksi)"),
     ("https://www.cnbc.com/2026/07/26/cocoa-prices-chocolate-lindt-barry-callebaut-nestle.html",
      "CNBC: Cocoa prices are easing. So why is chocolate still so expensive? (26.7.2026, englanniksi)"),
     ("https://www.imf.org/en/publications/wp/issues/2023/06/23/euro-area-inflation-after-the-pandemic-and-energy-shock-import-prices-profits-and-wages-534837",
      "IMF Working Paper 23/131 (2023, englanniksi)")])

LIITTYVAT_SUKLAA = ["shrinkflaatio", "cherry-picking-aikavali", "kaksois-y-akseli", "piilokulut", "hintaankkurointi"]


SISALTO_RUOKAKORI = rf"""
<p><strong>Greedflation</strong> (suomeksi myös <em>ahneusinflaatio</em>; taloustieteessä <em>sellers' inflation</em>, myyjien inflaatio) tarkoittaa inflaatiota, jossa yritykset nostavat hintoja enemmän kuin niiden kustannukset nousevat. Ruoka on ilmiön tavallisin syytetty. Suomessa elintarvikkeiden vuosi-inflaatio oli pahimmillaan {fi(RUOKA_INFLAATIO_HUIPPU)} prosenttia maaliskuussa 2023, ja kysymys "kuka sen söi?" on kysytty siitä asti.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Nostiko ruokakauppa hintoja ahneuttaan?</h2>
<p style="margin:0.4em 0 0;">Tutkimus ei tue väitettä kokonaisuutena, mutta ei myöskään kumoa sitä. Suomen Pankin analyysin (2023) mukaan yritysten voitoissa ei näkynyt merkkejä hinnoittelun muuttumisesta, ja muiden maiden voitto-osuuksien kasvua oli tulkittu Suomeenkin virheellisesti. Pellervon taloustutkimuksen mukaan vilja-, maito- ja lihaketjussa hinnat välittyvät pitkällä aikavälillä melko symmetrisesti. Samalla tutkijat huomauttavat, ettei elintarviketeollisuuden ja kaupan katteista tilastoida vertailukelpoista tietoa. Juuri sillä luvulla ahneuden voisi todistaa.</p>
</div>
{kuva(kuvaaja_ruokakori(),
      "Elintarvikkeiden ja kaikkien kuluttajahintojen indeksi (Tilastokeskus), tammikuu 2021 = 100.")}
<p>Ruoka kallistui vuosina 2021–2023 muuta kulutusta nopeammin: {LB["ruoka_ylos"]} prosenttia, kun kaikki kuluttajahinnat nousivat {LB["kaikki_ylos"]} prosenttia. Sitten nousu pysähtyi. Maaliskuusta 2023 syyskuuhun 2026 ruoan hinta nousi {fi(LB["ruoka_sitten"])} prosenttia ja kuluttajahinnat kaikkiaan {fi(LB["kaikki_sitten"])} prosenttia. Suhteessa muuhun kulutukseen ruoka on siis halventunut kolme vuotta, vaikka kassalla ei siltä tunnu.</p>
{kuva(kuvaaja_parit(),
      "Raaka-aineen maailmanmarkkinahinta (Maailmanpankki) ja vastaavan tuoteryhmän kuluttajahinta "
      "(Tilastokeskus), kumpikin omasta huipustaan syyskuuhun 2026.")}
<p>Korin sisällä raaka-aineiden halpeneminen on näkynyt hyllyllä, vaikka vaimeampana. Kasviöljy, sokeri, kahvi ja jauhot ovat 9–20 prosenttia huippuaan halvempia. Vaimeus on odotettavaa, koska raaka-aine on vain osa hintaa. PTT:n mukaan viljan tuottajahinnan suuret heilahdukset eivät välity kuluttajahintoihin samassa mitassa kumpaankaan suuntaan.</p>
<p><strong>Suklaa on korin poikkeus.</strong> Kaakao ja kahvi olivat kalleimmillaan samaan aikaan, tammi–helmikuussa 2025, ja kummankin hyllyhinta huipentui heinäkuussa 2025. Sen jälkeen kahvi on halventunut hyllyllä 15 prosenttia ja suklaa 5 prosenttia, vaikka kaakao halpeni yli kaksi kertaa enemmän kuin kahvi. Suklaan osuus ruokakorista on noin {SUKLAAN_PAINO} prosenttia, joten koko korin hintaa se ei selitä. Se on silti korin paras koe sille, laskeeko hinta, kun kustannus laskee.</p>
<div class="infolaatikko">
<h2 class="laatikko-otsikko">Dokumentoituja tapauksia:</h2>
<ul style="margin:0.5em 0 0;">
<li><strong>Kaupan keskittyminen (Suomi, 2025):</strong> S-ryhmän osuus päivittäistavarakaupasta oli 49,0 ja K-ryhmän 33,5 prosenttia. Weberin ja Wasnerin (2023) mukaan keskittyneillä markkinoilla kustannusshokki toimii signaalina, jonka turvin kaikki voivat nostaa hintoja yhtä aikaa sopimatta mitään. Keskittyminen on greedflationin edellytys, ei todiste siitä.</li>
<li><strong>Suklaa (2026):</strong> Lindt lupasi laskea hintoja tammikuusta 2027, kun suojaukset ovat purkautuneet. Nestlé kertoi odottavansa katteidensa paranevan kaakaon halvetessa, mutta hintojen laskusta se ei puhunut.</li>
<li><strong>Euroalue (2022–2023):</strong> IMF:n tutkijoiden mukaan yritysten voittojen kasvu selitti 45 prosenttia euroalueen kuluttajahintojen noususta. Suomen Pankin mukaan Suomessa vastaavaa ei näkynyt.</li>
</ul>
</div>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Testikysymys kuuluu: laskeeko hinta, kun kustannus laskee, ja kuinka suuri osa hinnasta tuo kustannus on? Vertaa tuotetta raaka-aineeseen vain, kun raaka-aine on iso osa hintaa, kuten kahvissa ja suklaassa. Leivän hintaa ei voi verrata vehnän pörssihintaan (ks. <a href="omenoita-appelsiineja.html">omenoita ja appelsiineja</a>). Vertaa ruoan hintaa myös muihin hintoihin, sillä nimellinen hinta laskee harvoin. Jos ruoka pysyy paikallaan muun kallistuessa, se halpenee suhteessa. Pysyvän ylihinnan paljastaisi vasta kate, eikä Suomessa julkaista kaupan ja teollisuuden katteita tuoteryhmittäin. Siksi sekä syytökset että niiden kiistämiset lepäävät usein vajaan tiedon varassa. Kuluttajan keinot ovat kilohinta, kaupan omat merkit ja kauppojen vertailu, eli juuri ne, jotka pitävät kilpailun käynnissä. Suhtaudu varauksella sanaan ahneus: oikea kysymys on, miksi kilpailu ei pakota hintoja alas.
    </div>
""" + K.lue_lisaa(
    [("Sellers' Inflation, Profits and Conflict", "Isabella M. Weber &amp; Evan Wasner, Review of Keynesian Economics 11:2 (2023)"),
     ("Elintarvikeketjun vertikaaliset hintasiirtymät", "Mauri Yli-Liipola, PTT raportteja 306 (2025)")],
    [("https://www.eurojatalous.fi/artikkeli/analyysi/2023/yritysten-voitoissa-ei-viitteita-hinnoittelun-muuttumisesta/",
      "Suomen Pankki, Euro &amp; talous: Yritysten voitoissa ei viitteitä hinnoittelun muuttumisesta (2023)"),
     ("https://www.ptt.fi/wp-content/uploads/2025/11/PTTrap306.pdf",
      "PTT: Elintarvikeketjun vertikaaliset hintasiirtymät (2025)"),
     ("https://www.ptt.fi/wp-content/uploads/2025/12/Ruokamarkkinaseminaari-3.12.2025-esitysdiat.pdf",
      "PTT, Luke ja REINU: Suositukset kohti toimivampia ruokamarkkinoita (3.12.2025)"),
     ("https://www.pty.fi/wp-content/uploads/2026/06/Paivittaistavarakaupan-tilastot-2025_EN.pdf",
      "PTY: Päivittäistavarakaupan tilastot 2025 (englanniksi)"),
     ("https://pxdata.stat.fi/PxWeb/pxweb/fi/StatFin/StatFin__khi/statfin_khi_pxt_15b5.px/",
      "Tilastokeskus: Kuluttajahintaindeksi hyödykkeittäin (taulukko 15b5)"),
     ("https://www.worldbank.org/en/research/commodity-markets",
      "Maailmanpankki: Commodity Markets (Pink Sheet, englanniksi)"),
     ("https://www.swissinfo.ch/eng/lindt-to-cut-prices-as-chocolate-demand-wanes-in-key-markets/92135636",
      "Swissinfo/Bloomberg: Lindt to Cut Prices as Chocolate Demand Wanes (29.9.2026, englanniksi)")])

LIITTYVAT_RUOKAKORI = ["shrinkflaatio", "omenoita-appelsiineja", "cherry-picking-aikavali", "syntipukki", "piilokulut"]

VERSIOT = {
    "suklaa": dict(
        otsikko="Greedflation — miksi suklaa ei halpene, vaikka kaakao halpeni",
        title="Greedflation — miksi suklaa ei halpene, vaikka kaakao halpeni? | Ilmiöitä",
        kuvaus=("Greedflation eli ahneusinflaatio: hinta nousee enemmän kuin kustannus. Kaakao "
                "halpeni 70 %, suklaa ei. Näin erotat suojausviiveen katteen kasvusta."),
        sisalto=SISALTO_SUKLAA, liittyvat=LIITTYVAT_SUKLAA),
    "ruokakori": dict(
        otsikko="Greedflation — mitä ruokakori kertoo ahneudesta",
        title="Greedflation — kuka söi ruoan hinnannousun? | Ilmiöitä",
        kuvaus=("Greedflation eli ahneusinflaatio ruokakorissa: raaka-aineet halpenivat, ruoka "
                "ei juuri. Suklaa on korin poikkeus. Näin erotat katteen kustannuksesta."),
        sisalto=SISALTO_RUOKAKORI, liittyvat=LIITTYVAT_RUOKAKORI),
}


# ──────────────────────────── kokoaminen ────────────────────────────

def seo_lohko(pohja_ld, v):
    """Kuten build_kannustin_luonnokset.seo_lohko, mutta tämän sivun kategoriaan."""
    url = f"https://www.ilmiöt.fi/{SLUG}.html"   # kaikilla versioilla sama: valitaan yksi
    OTSIKKO, TITLE, KUVAUS = v["otsikko"], v["title"], v["kuvaus"]
    ld = json.loads(pohja_ld)
    murut, artikkeli = ld["@graph"]
    murut["itemListElement"][1].update(name=KAT_NIMI, item=f"https://www.ilmiöt.fi/{KAT_SIVU}")
    murut["itemListElement"][2].update(name=OTSIKKO, item=url)
    artikkeli.update({"@id": f"{url}#article", "url": url, "headline": OTSIKKO,
                      "description": KUVAUS, "articleSection": KAT_NIMI,
                      "datePublished": PVM_ISO, "dateModified": PVM_ISO})
    artikkeli["image"]["url"] = "https://www.ilmiöt.fi/og/brand.png"
    artikkeli["about"].update(name=NIMI, description=KUVAUS)
    ld_teksti = json.dumps(ld, ensure_ascii=False, indent=2)
    return f'''  <!-- SEO -->
  <meta name="description" content="{KUVAUS}">
  <meta name="robots" content="noindex"><!-- POISTA-JULKAISTAESSA -->
  <link rel="canonical" href="{url}">
  <meta property="og:title" content="{TITLE}">
  <meta property="og:description" content="{KUVAUS}">
  <meta property="og:url" content="{url}">
  <meta property="og:type" content="article">
  <meta property="og:locale" content="fi_FI">
  <meta property="og:site_name" content="Ilmiöitä — Miten valta toimii">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{TITLE}">
  <meta name="twitter:description" content="{KUVAUS}">
  <meta property="og:image" content="https://www.ilmiöt.fi/og/brand.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Ilmiöitä — Miten valta toimii">
  <meta name="twitter:image" content="https://www.ilmiöt.fi/og/brand.png">
  <style>.ilmio h1{{margin-top:0;font-family:'Spectral',Georgia,serif;}}</style>
  <script type="application/ld+json">
{ld_teksti}
</script>'''


def build():
    assert SLUG not in K.KORTIT, "greedflation on jo julkaistu"
    assert JULKAISTAVA in VERSIOT
    for nimi_, v in VERSIOT.items():
        build_versio(nimi_, v)
    print(f"  julkaisu: UUDET = {{\"{SLUG}\": (\"{EDELLINEN}\", \"{VARI}\", \"{NIMI}\",\n"
          f"      \"{KORTTI_KUVAUS}\")}}  — julkaistava versio: {JULKAISTAVA}")


def build_versio(versio, v):
    OTSIKKO, TITLE, KUVAUS = v["otsikko"], v["title"], v["kuvaus"]
    SISALTO, LIITTYVAT = v["sisalto"], v["liittyvat"]
    assert len(KUVAUS) <= 160, f"{versio}: metakuvaus {len(KUVAUS)} merkkiä"
    assert all(s in K.KORTIT and s not in K.OMAT_KORTIT for s in LIITTYVAT), \
        f"{versio}: liittyvä ilmiö puuttuu tai on julkaisematon"
    tpl = K.TEMPLATE.read_text(encoding="utf-8")

    ids = list(K.EDELLISET_IDS)
    ids.insert(ids.index(EDELLINEN) + 1, SLUG)
    assert ids[ids.index(SLUG) + 1] == SEURAAVA
    ids_js = "const IDS = [" + ", ".join(json.dumps(s) for s in ids) + "];"
    pohja_ld = re.search(r'<script type="application/ld\+json">\n(.*?)\n</script>', tpl, re.S).group(1)

    def nimi(s):
        return re.search(r"<h1>(.*?)</h1>", (ROOT / f"{s}.html").read_text(encoding="utf-8")).group(1)

    prev_href, next_href = f"../{EDELLINEN}.html", f"../{SEURAAVA}.html"

    html = tpl.replace(K.VANHA_SLUG, SLUG)
    html, n = re.subn(rf"(#{SLUG}\s+(?:\.ilmio-tag\s*)?\{{ (?:border-top-color|background): )#[0-9a-fA-F]{{6}}",
                      rf"\g<1>{VARI}", html)
    assert n == 2, f"sivun väri-CSS:ää ei löytynyt ({n})"
    html, n = re.subn(r"<title>.*?</title>", lambda m: f"<title>{TITLE}</title>", html, count=1)
    assert n == 1
    html, n = re.subn(r"  <!-- SEO -->.*?\n</script>", lambda m: seo_lohko(pohja_ld, v), html, count=1, flags=re.S)
    assert n == 1, "SEO-lohkoa ei löytynyt"
    html = html.replace(f'href="{K.VANHA_KAT_SIVU}" class="kortti-breadcrumb-kat">{K.VANHA_KAT_NIMI}<',
                        f'href="{KAT_SIVU}" class="kortti-breadcrumb-kat">{KAT_NIMI}<')

    uusi_ilmio = (f'<div class="ilmio" id="{SLUG}">\n'
                  f'<div class="ilmio-tag">Ilmiö {NUM}</div>\n'
                  f'<h1>{OTSIKKO}</h1>\n'
                  f'<p class="ilmio-byline">Kirjoittanut <a href="tietoa.html" rel="author">Ilmiömies</a> · Päivitetty {PVM_FI}</p>'
                  f'{K.ankkuroi(SISALTO)}</div>')
    html, n = re.subn(rf'<div class="ilmio" id="{SLUG}">.*?\n</div>\n\n  <aside',
                      lambda m: uusi_ilmio + "\n\n  <aside", html, count=1, flags=re.S)
    assert n == 1, "sisältölohkoa ei löytynyt"
    html, n = re.subn(r'<aside class="liittyvat".*?</aside>',
                      lambda m: K.liittyvat_html(LIITTYVAT).strip(), html, count=1, flags=re.S)
    assert n == 1

    K.YHTEENSA = YHTEENSA  # nav_html lukee kokonaismäärän moduulista
    html, n = re.subn(r'<nav class="kortti-nav">.*?</nav>',
                      lambda m: K.nav_html(NUM, prev_href, nimi(EDELLINEN), next_href, nimi(SEURAAVA)).strip(),
                      html, count=1, flags=re.S)
    assert n == 1
    html, n = re.subn(r"const IDS = \[.*?\];", lambda m: ids_js, html, count=1, flags=re.S)
    assert n == 1
    html, n = re.subn(r"const PREV = '[^']*';", lambda m: f"const PREV = '{prev_href}';", html)
    assert n == 1
    html, n = re.subn(r"const NEXT = '[^']*';", lambda m: f"const NEXT = '{next_href}';", html)
    assert n == 1

    sallitut = SISALTO.count(K.VANHA_SLUG) + LIITTYVAT.count(K.VANHA_SLUG) + ids_js.count(K.VANHA_SLUG)
    assert html.count(K.VANHA_SLUG) == sallitut, "pohjan slug jäi sivulle"
    assert K.VANHA_KAT_NIMI not in html, "pohjan kategoria jäi sivulle"

    html = K.alikansiopolut(html)
    for jaannos in ('href="index.html"', 'href="tietoa.html"', f'href="{KAT_SIVU}"', "s.src = 'js/"):
        assert jaannos not in html, f"{jaannos} jäi juuripolkuna"

    tiedosto = f"{SLUG}.html" if versio == JULKAISTAVA else f"{SLUG}-{versio}.html"
    (K.OUT / tiedosto).write_text(html, encoding="utf-8")
    teksti = re.sub(r'<figure.*?</figure>', " ", SISALTO, flags=re.S)
    teksti = re.sub(r'<div class="mermaid">.*?</div>', " ", teksti, flags=re.S)
    teksti = teksti.split('<div class="lue-lisaa">')[0]
    sanat = len(re.sub(r"<[^>]+>", " ", OTSIKKO + teksti).split())
    print(f"  {NUM}  luonnokset/{tiedosto}  ({len(html) // 1024} KB, {sanat} sanaa)")


if __name__ == "__main__":
    build()
