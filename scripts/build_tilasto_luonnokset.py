#!/usr/bin/env python3
"""Generoi Tilastoilla valehtelu -kategorian (ilmiöt 99–106) sivuluonnokset.

Pohjana tilastoilla-valehtelu.html. Tuottaa luonnokset-tilasto/-kansioon
8 sivua, joissa noindex-meta (poistetaan julkaistaessa). IDS-lista ja
PREV/NEXT ovat jo lopullisessa 106 ilmiön muodossa; julkaisuvaiheessa
sama lista päivitetään vanhoille 98 sivulle.

Ajo:  python3 scripts/build_tilasto_luonnokset.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "tilastoilla-valehtelu.html"
OUT = ROOT / "luonnokset-tilasto"

KATEGORIA_NIMI = "Tilastoilla valehtelu"
KATEGORIA_ANKKURI = "#tilastoilla-valehtelu-kategoria"
PVM_ISO = "2026-07-12"
PVM_FI = "12.7.2026"

UUDET = [
    "kaksois-y-akseli", "pinta-alaharha", "cherry-picking-aikavali",
    "keskiarvo-vs-mediaani", "suhteellinen-riski", "selviytymisharha",
    "simpsonin-paradoksi", "p-hakkerointi",
]

# Liittyvät-kortit luonnoksiin (julkaisussa build_liittyvat.py generoi uudelleen)
KORTTI = {
    "tilastoilla-valehtelu": (8, "#27ae60", "Tilastoilla valehtelu",
        "Katkaistut akselit, valikoidut aikavälit ja muut visuaaliset ansat — kokonaisuuden ankkurisivu."),
    "bkt-harha": (9, "#16a085", "BKT-harha",
        "BKT mittaa tuotannon arvoa, ei hyvinvointia — ja voi kasvaa, vaikka kansalaisten talous kurjistuu."),
    "omenoita-appelsiineja": (26, "#6a1b9a", "Omenoita ja appelsiineja",
        "Vertaillaan lukuja, jotka eivät ole vertailukelpoisia — ja vedetään johtopäätös silti."),
    "goodhartin-laki": (39, "#148f77", "Goodhartin laki",
        "Kun mittarista tulee tavoite, se lakkaa olemasta hyvä mittari."),
    "hippo-efekti": (40, "#5d4037", "HiPPO-efekti",
        "Korkeimmin palkatun mielipide jyrää datan päätöksenteossa."),
    "konsensus-fetissi": (25, "#01579b", "Konsensus-fetissi",
        "”Tiede on selvä” -argumentti, jolla keskustelu suljetaan lukuihin vetoamalla."),
    "kaksois-y-akseli": (99, "#1565c0", "Kaksois-y-akseli",
        "Kaksi vapaasti skaalattua asteikkoa saa mitkä tahansa käyrät kulkemaan käsi kädessä."),
    "pinta-alaharha": (100, "#8e24aa", "Pinta-alaharha",
        "Kaksinkertainen arvo piirretään kaksinkertaisena halkaisijana — ja näyttää nelinkertaiselta."),
    "cherry-picking-aikavali": (101, "#2e7d32", "Cherry-picking",
        "Aikavälin alku- ja loppupiste valitaan niin, että sama aikasarja todistaa mitä tahansa."),
    "keskiarvo-vs-mediaani": (102, "#5d4037", "Keskiarvoharha",
        "Vinossa jakaumassa keskiarvo ja mediaani kertovat eri tarinan — ja kertoja valitsee sopivamman."),
    "suhteellinen-riski": (103, "#c62828", "Suhteellinen riski",
        "”Riski kaksinkertaistui” voi tarkoittaa siirtymää yhdestä tapauksesta kahteen sataatuhatta kohden."),
    "selviytymisharha": (104, "#37474f", "Selviytymisharha",
        "Vain palanneet koneet lasketaan — data kertoo selviytyjistä, ei kadonneista."),
    "simpsonin-paradoksi": (105, "#00695c", "Simpsonin paradoksi",
        "Kokonaisuus näyttää kasvua, vaikka jokainen osaryhmä laskee — tai päinvastoin."),
    "p-hakkerointi": (106, "#ef6c00", "P-hakkerointi",
        "Testataan kunnes jokin näyttää merkitsevältä — ja julkaistaan vain se yksi tulos."),
}


def liittyvat_html(slugit):
    osat = ['  <aside class="liittyvat" aria-label="Liittyvät ilmiöt">',
            "    <h2>Liittyvät ilmiöt</h2>",
            '    <div class="liittyvat-kortit">']
    for s in slugit:
        num, vari, nimi, kuvaus = KORTTI[s]
        osat.append(f'''    <a href="{s}.html" class="liittyvat-kortti" style="--c:{vari}">
      <span class="liittyvat-numero">{num}</span>
      <span class="liittyvat-teksti">
        <span class="liittyvat-nimi">{nimi}</span>
        <span class="liittyvat-kuvaus">{kuvaus}</span>
      </span>
      <span class="liittyvat-nuoli" aria-hidden="true">›</span>
    </a>''')
    osat.append("    </div>\n  </aside>")
    return "\n".join(osat)


def nav_html(num, prev_slug, prev_nimi, next_slug, next_nimi):
    prev = (f'<a class="kortti-nav-btn" href="{prev_slug}.html">← {prev_nimi}</a>'
            if prev_slug else '<span class="kortti-nav-btn disabled">←</span>')
    nxt = (f'<a class="kortti-nav-btn" href="{next_slug}.html">{next_nimi} →</a>'
           if next_slug else '<span class="kortti-nav-btn disabled">→</span>')
    return f'''  <nav class="kortti-nav">
    {prev}
    <div class="kortti-nav-center">
      <span class="kortti-nav-laskuri">{num} / 106</span>
      <span class="kortti-nav-vinkki">
        <kbd>&#8592;</kbd> <kbd>&#8594;</kbd> selaa &middot; <kbd>R</kbd> satunnainen
        <span class="touch-vinkki">&nbsp;· swipe &#8592;&#8594; tai &#8595; random</span>
      </span>
    </div>
    {nxt}
  </nav>'''


PAGES = []


def page(slug, num, otsikko, kuvaus, vari, sisalto, liittyvat):
    PAGES.append(dict(slug=slug, num=num, otsikko=otsikko, kuvaus=kuvaus,
                      vari=vari, sisalto=sisalto, liittyvat=liittyvat))


# ────────────────────────── 99 · Kaksois-y-akseli ──────────────────────────
page("kaksois-y-akseli", 99,
     "Kaksois-y-akseli — kaksi asteikkoa, valmis korrelaatio",
     "Kun kaaviossa on kaksi eri y-akselia, kumpikin voidaan skaalata vapaasti — ja mitkä tahansa kaksi käyrää saadaan näyttämään kulkevan käsi kädessä.",
     "#1565c0", """
<p>Kaksois-y-akselisessa kaaviossa kaksi eri suuretta piirretään samaan kuvaan, kumpikin omalla asteikollaan. Kuulostaa käytännölliseltä — mutta koska kummankin akselin alku- ja loppupiste valitaan vapaasti, käyrät voidaan skaalata kulkemaan täsmälleen päällekkäin. Katsoja lukee muodon: ”nuo kaksi liikkuvat yhdessä, niiden välillä on yhteys.” Yhteys syntyi kuitenkin akselivalinnasta, ei datasta.</p>
<div class="tilasto-grid">
<div class="tilasto-esimerkki">
<h4>Harhaanjohtava (kaksi vapaasti skaalattua akselia)</h4>
<svg viewBox="0 0 300 150" style="width:100%;max-width:300px;border-bottom:2px solid #333;" role="img" aria-label="Kaksi käyrää eri asteikoilla kulkevat päällekkäin">
  <text x="6" y="14" font-size="9" fill="#2980b9">Myynti (M€)</text>
  <text x="294" y="14" font-size="9" fill="#c0392b" text-anchor="end">Someseuraajat (t.)</text>
  <polyline points="20,120 70,100 120,85 170,60 220,45 270,30" fill="none" stroke="#2980b9" stroke-width="3"/>
  <polyline points="20,125 70,104 120,88 170,64 220,48 270,34" fill="none" stroke="#c0392b" stroke-width="3" stroke-dasharray="6 3"/>
  <text x="8" y="125" font-size="8" fill="#2980b9">40</text>
  <text x="8" y="35" font-size="8" fill="#2980b9">48</text>
  <text x="292" y="128" font-size="8" fill="#c0392b" text-anchor="end">2</text>
  <text x="292" y="38" font-size="8" fill="#c0392b" text-anchor="end">90</text>
</svg>
<p style="font-size:0.8em;color:#c0392b;margin-top:0.5rem;">Näyttää: käyrät kulkevat käsi kädessä — some ajaa myyntiä!</p>
</div>
<div class="tilasto-esimerkki">
<h4>Rehellinen (yhteinen asteikko)</h4>
<svg viewBox="0 0 300 150" style="width:100%;max-width:300px;border-bottom:2px solid #333;" role="img" aria-label="Samat käyrät yhteisellä asteikolla: toinen lähes vaakasuora">
  <text x="6" y="14" font-size="9" fill="#555">Sama asteikko 0–100</text>
  <polyline points="20,90 70,84 120,80 170,72 220,68 270,62" fill="none" stroke="#2980b9" stroke-width="3"/>
  <polyline points="20,138 70,137 120,136 170,134 220,133 270,131" fill="none" stroke="#27ae60" stroke-width="3"/>
  <text x="8" y="142" font-size="8" fill="#555">0</text>
  <text x="8" y="30" font-size="8" fill="#555">100</text>
</svg>
<p style="font-size:0.8em;color:#27ae60;margin-top:0.5rem;">Todellisuus: toinen suure tuskin liikkuu — muutokset eri mittaluokkaa.</p>
</div>
</div>
<h3>Miksi temppu toimii</h3>
<p>Aivot vertaavat käyrien muotoa, eivät akseleiden lukuja. Kun kaksi viivaa nousee ja laskee samassa tahdissa, kausaalinen tarina syntyy itsestään — vaikka toinen suure vaihtelisi kahden ja kolmen välillä ja toinen miljoonissa. Klassikkoesimerkki on sivusto <em>Spurious Correlations</em>, joka tuottaa kaksois-akselilla ”täydellisiä” korrelaatioita vaikkapa juuston kulutuksen ja hukkumiskuolemien välille.</p>
<h3>Missä tähän törmää</h3>
<ul>
<li><strong>Talousuutisointi:</strong> pörssikurssi ja jokin indikaattori samassa kuvassa, akselit viritetty niin että käyrät ”ennustavat” toisiaan.</li>
<li><strong>Markkinointiraportit:</strong> ”somepanostukset ja liikevaihto kulkevat käsi kädessä” — kunnes akselit yhtenäistetään.</li>
<li><strong>Poliittinen viestintä:</strong> oman toimenpiteen käyrä skaalataan kulkemaan halutun kehityksen päällä.</li>
</ul>
<div class="infolaatikko">
<strong>Miten tunnistat:</strong> Jos kuvassa on kaksi y-akselia, kysy: mistä kumpikin akseli alkaa ja mihin päättyy? Piirrä (tai pyydä) sama data yhteisellä asteikolla tai indeksoituna samaan lähtöpisteeseen — jos ”yhteys” katoaa, se oli akselivalinta.
    </div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Kirjoja</span>
<ul class="lue-lisaa-lista">
<li><cite>How to Lie with Statistics</cite> — Darrell Huff (1954)</li>
<li><cite>Spurious Correlations</cite> — Tyler Vigen (2015)</li>
<li><cite>The Art of Statistics</cite> — David Spiegelhalter (2019)</li>
</ul>
</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://en.wikipedia.org/wiki/Misleading_graph" target="_blank" rel="noopener">Wikipedia: Misleading graph (englanniksi)</a></li>
</ul>
</div>
</div>
""", ["tilastoilla-valehtelu", "cherry-picking-aikavali", "pinta-alaharha", "omenoita-appelsiineja"])

# ────────────────────────── 100 · Pinta-alaharha ──────────────────────────
page("pinta-alaharha", 100,
     "Pinta-alaharha — kun kaksinkertainen näyttää nelinkertaiselta",
     "Kun luku kuvataan symbolin korkeutena mutta katsoja näkee pinta-alan, kaksinkertainen arvo näyttää nelinkertaiselta — ja 3D-kaavio vääristää vielä enemmän.",
     "#8e24aa", """
<p>Darrell Huff nimesi tämän jo 1954: kun tilasto esitetään kuvasymbolina — rahasäkkinä, ihmishahmona, ympyränä — ja arvon kasvu piirretään symbolin <em>korkeuteen</em>, pinta-ala kasvaa neliöllisesti. Kaksinkertainen arvo näyttää nelinkertaiselta, kolminkertainen yhdeksänkertaiselta. Silmä lukee pinta-alan (tai 3D-kuvassa tilavuuden), ei korkeutta.</p>
<div class="tilasto-grid">
<div class="tilasto-esimerkki">
<h4>Harhaanjohtava (arvo halkaisijassa)</h4>
<svg viewBox="0 0 300 150" style="width:100%;max-width:300px;border-bottom:2px solid #333;" role="img" aria-label="Kaksi ympyrää: toisen halkaisija on kaksinkertainen, jolloin pinta-ala on nelinkertainen">
  <circle cx="80" cy="105" r="28" fill="#c0392b" opacity="0.85"/>
  <circle cx="205" cy="77" r="56" fill="#c0392b"/>
  <text x="80" y="109" font-size="11" fill="#fff" text-anchor="middle">10</text>
  <text x="205" y="82" font-size="13" fill="#fff" text-anchor="middle">20</text>
</svg>
<div class="pylvas-label">Yritys A &nbsp;&nbsp;&nbsp; Yritys B</div>
<p style="font-size:0.8em;color:#c0392b;margin-top:0.5rem;">Näyttää: B on nelinkertainen (pinta-ala 4×).</p>
</div>
<div class="tilasto-esimerkki">
<h4>Rehellinen (arvo korkeudessa)</h4>
<div class="pylvas-wrapper">
<div style="display:flex;flex-direction:column;justify-content:flex-end;height:100%;width:36px;">
<div class="pylvas" style="height:50%;background:#27ae60;">10</div>
</div>
<div style="display:flex;flex-direction:column;justify-content:flex-end;height:100%;width:36px;">
<div class="pylvas" style="height:100%;background:#27ae60;">20</div>
</div>
</div>
<div class="pylvas-label">Yritys A &nbsp;&nbsp;&nbsp; Yritys B</div>
<p style="font-size:0.8em;color:#27ae60;margin-top:0.5rem;">Todellisuus: B on kaksinkertainen.</p>
</div>
</div>
<h3>Saman perheen temput</h3>
<ul>
<li><strong>Piktogrammit:</strong> ”palkat tuplaantuivat” — ja rahasäkki piirretään kaksi kertaa korkeampana <em>ja</em> leveämpänä.</li>
<li><strong>3D-piirakka:</strong> perspektiivi kasvattaa katsojaa lähinnä olevan lohkon pinta-alaa — oma osuus etualalle, kilpailijan taakse.</li>
<li><strong>Kuplakaaviot:</strong> jos arvo koodataan säteeseen eikä pinta-alaan, erot paisuvat neliöllisesti.</li>
</ul>
<div class="infolaatikko">
<strong>Miten tunnistat:</strong> Kun näet symboleilla tai ympyröillä esitetyn vertailun, etsi luvut ja laske suhde itse. Jos kuvio on 3D tai perspektiivissä, kysy miksi — syvyysulottuvuus ei koskaan lisää informaatiota, mutta lähes aina vääristää sitä.
    </div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Kirjoja</span>
<ul class="lue-lisaa-lista">
<li><cite>How to Lie with Statistics</cite> — Darrell Huff (1954)</li>
<li><cite>The Visual Display of Quantitative Information</cite> — Edward Tufte (1983)</li>
</ul>
</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://en.wikipedia.org/wiki/Misleading_graph" target="_blank" rel="noopener">Wikipedia: Misleading graph (englanniksi)</a></li>
</ul>
</div>
</div>
""", ["tilastoilla-valehtelu", "kaksois-y-akseli", "suhteellinen-riski", "omenoita-appelsiineja"])

# ─────────────────────── 101 · Cherry-picking ───────────────────────
page("cherry-picking-aikavali", 101,
     "Cherry-picking — valittu aikaväli kertoo halutun tarinan",
     "Kun tarkastelujakson alku- ja loppupiste valitaan sopivasti, sama aikasarja todistaa mitä tahansa: kasvua, romahdusta tai käännettä.",
     "#2e7d32", """
<p>Jokaisessa aikasarjassa on nousuja ja laskuja. Cherry-picking eli poimintaharha tarkoittaa, että tarkastelujakson alku- ja loppupiste valitaan sen mukaan, mitä halutaan todistaa. ”Kasvu on ollut 40 % vuodesta 2020” voi olla teknisesti totta — ja silti valhe, jos vuosi 2020 oli poikkeuksellinen pohja ja pidempi trendi on laskeva.</p>
<div class="tilasto-grid">
<div class="tilasto-esimerkki">
<h4>Harhaanjohtava (valittu ikkuna)</h4>
<svg viewBox="0 0 300 150" style="width:100%;max-width:300px;border-bottom:2px solid #333;" role="img" aria-label="Lyhyt nouseva jakso suurennettuna">
  <polyline points="20,120 80,100 150,75 220,55 280,35" fill="none" stroke="#c0392b" stroke-width="3"/>
  <text x="20" y="140" font-size="9" fill="#555">2020</text>
  <text x="280" y="140" font-size="9" fill="#555" text-anchor="end">2023</text>
  <text x="150" y="20" font-size="11" fill="#c0392b" text-anchor="middle" font-weight="bold">+40 %</text>
</svg>
<p style="font-size:0.8em;color:#c0392b;margin-top:0.5rem;">Näyttää: vahva kasvutrendi!</p>
</div>
<div class="tilasto-esimerkki">
<h4>Rehellinen (koko sarja)</h4>
<svg viewBox="0 0 300 150" style="width:100%;max-width:300px;border-bottom:2px solid #333;" role="img" aria-label="Pitkä laskeva sarja, jossa valittu ikkuna on pieni nousu pohjalta">
  <rect x="185" y="20" width="65" height="120" fill="#fdecea"/>
  <polyline points="15,35 55,45 95,55 135,70 175,90 195,115 215,105 235,98 255,92 285,95" fill="none" stroke="#27ae60" stroke-width="3"/>
  <text x="15" y="148" font-size="9" fill="#555">2010</text>
  <text x="285" y="148" font-size="9" fill="#555" text-anchor="end">2025</text>
  <text x="218" y="15" font-size="8" fill="#c0392b" text-anchor="middle">valittu ikkuna</text>
</svg>
<p style="font-size:0.8em;color:#27ae60;margin-top:0.5rem;">Todellisuus: pitkä trendi laskeva — ”kasvu” oli pomppu pohjalta.</p>
</div>
</div>
<h3>Kantavuoden valinta</h3>
<p>Saman tempun hienostuneempi muoto on indeksoinnin lähtöpiste. ”Hinnat ovat nousseet vain 5 % hallituskaudella” — kun lähtövuodeksi valitaan huippu. Tai käänteisesti: vertailu poikkeukselliseen pohjaan saa normaalitason näyttämään rajulta kasvulta. Sama data, eri kantavuosi, vastakkainen johtopäätös.</p>
<h3>Missä tähän törmää</h3>
<ul>
<li><strong>Sijoitusmarkkinointi:</strong> rahaston tuottokäyrä alkaa aina edellisen romahduksen pohjalta.</li>
<li><strong>Politiikka:</strong> hallitus aloittaa tarkastelun omasta aloitusvuodestaan, oppositio edellisestä huipusta.</li>
<li><strong>Ilmastokeskustelu:</strong> ”lämpeneminen pysähtyi” — kun alkupisteeksi valitaan poikkeuksellisen lämmin El Niño -vuosi.</li>
</ul>
<div class="infolaatikko">
<strong>Miten tunnistat:</strong> Kysy aina: miksi juuri tämä aikaväli? Mitä käy, jos alkupistettä siirtää kaksi vuotta kumpaankin suuntaan? Jos johtopäätös kaatuu siihen, se ei ollut trendi vaan valinta.
    </div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Kirjoja</span>
<ul class="lue-lisaa-lista">
<li><cite>How to Lie with Statistics</cite> — Darrell Huff (1954)</li>
<li><cite>Factfulness</cite> — Hans Rosling (2018)</li>
</ul>
</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://en.wikipedia.org/wiki/Cherry_picking" target="_blank" rel="noopener">Wikipedia: Cherry picking (englanniksi)</a></li>
</ul>
</div>
</div>
""", ["tilastoilla-valehtelu", "kaksois-y-akseli", "p-hakkerointi", "bkt-harha"])

# ─────────────────── 102 · Keskiarvo vs. mediaani ───────────────────
page("keskiarvo-vs-mediaani", 102,
     "Keskiarvoharha — keskiarvo vs. mediaani",
     "Vinossa jakaumassa keskiarvo ja mediaani kertovat eri tarinan: yksi miljonääri baarissa nostaa keskitulot kattoon, vaikka kenenkään palkka ei muutu.",
     "#5d4037", """
<p>”Keskiverto” kuulostaa neutraalilta, mutta sanan takana on valinta: keskiarvo, mediaani vai moodi? Vinossa jakaumassa — ja tulot, varallisuus, asuntojen hinnat ja odotusajat ovat käytännössä aina vinoja — nämä antavat hyvin eri luvut. Kertoja valitsee sen, joka tukee tarinaa. Klassikko: kun miljardööri astuu baariin, asiakkaiden <em>keskivarallisuus</em> nousee sataan miljoonaan. Mediaani ei värähdäkään.</p>
<div class="tilasto-grid">
<div class="tilasto-esimerkki">
<h4>Harhaanjohtava (pelkkä keskiarvo)</h4>
<div style="display:flex;flex-direction:column;justify-content:center;height:120px;border-bottom:2px solid #333;">
<div style="font-size:1.9em;font-weight:bold;color:#c0392b;">6 740 €/kk</div>
<div style="font-size:0.85em;color:#555;">”Työntekijöidemme keskipalkka”</div>
</div>
<p style="font-size:0.8em;color:#c0392b;margin-top:0.5rem;">Näyttää: hyväpalkkainen työpaikka!</p>
</div>
<div class="tilasto-esimerkki">
<h4>Rehellinen (koko jakauma)</h4>
<div class="pylvas-wrapper">
<div style="display:flex;flex-direction:column;justify-content:flex-end;height:100%;width:36px;">
<div class="pylvas" style="height:8%;background:#27ae60;font-size:0.6em;">2,0</div>
</div>
<div style="display:flex;flex-direction:column;justify-content:flex-end;height:100%;width:36px;">
<div class="pylvas" style="height:8.4%;background:#27ae60;font-size:0.6em;">2,1</div>
</div>
<div style="display:flex;flex-direction:column;justify-content:flex-end;height:100%;width:36px;">
<div class="pylvas" style="height:8.8%;background:#1a7044;font-size:0.6em;">2,2</div>
</div>
<div style="display:flex;flex-direction:column;justify-content:flex-end;height:100%;width:36px;">
<div class="pylvas" style="height:9.2%;background:#27ae60;font-size:0.6em;">2,3</div>
</div>
<div style="display:flex;flex-direction:column;justify-content:flex-end;height:100%;width:36px;">
<div class="pylvas" style="height:100%;background:#c0392b;font-size:0.6em;">25,1</div>
</div>
</div>
<div class="pylvas-label">4 työntekijää (t€/kk) + johtaja</div>
<p style="font-size:0.8em;color:#27ae60;margin-top:0.5rem;">Mediaani 2 200 € — keskiarvon nostaa yksi palkka.</p>
</div>
</div>
<h3>Kumpi luku, kumpi tarina</h3>
<ul>
<li><strong>”Keskipalkka nousi 5 %”</strong> — voi tarkoittaa, että johdon palkat nousivat ja mediaani laski.</li>
<li><strong>”Keskimääräinen asunnon hinta”</strong> — muutama kattohuoneisto vetää keskiarvoa; ostajalle mediaani on rehellisempi.</li>
<li><strong>”Keskimääräinen odotusaika 20 min”</strong> — jos joka kymmenes odottaa kolme tuntia, tyypillinen kokemus on aivan muuta.</li>
</ul>
<p>Toinen puoli samaa harhaa on <strong>keskiarvo ilman hajontaa</strong>: ”keskilämpötila 20 °C” kuvaa yhtä hyvin tasaista kevätpäivää kuin vuorokautta, jossa paahtaa +35 ja paleltaa +5.</p>
<div class="infolaatikko">
<strong>Miten tunnistat:</strong> Kun kuulet sanan ”keskimäärin”, kysy: keskiarvo vai mediaani — ja millainen hajonta? Jos jakauma on vino (tulot, hinnat, ajat), vaadi mediaani. Jos vain toinen luku kerrotaan, syy on yleensä se, että toinen kertoisi eri tarinan.
    </div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Kirjoja</span>
<ul class="lue-lisaa-lista">
<li><cite>How to Lie with Statistics</cite> — Darrell Huff (1954)</li>
<li><cite>Naked Statistics</cite> — Charles Wheelan (2013)</li>
</ul>
</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://en.wikipedia.org/wiki/Median" target="_blank" rel="noopener">Wikipedia: Median (englanniksi)</a></li>
</ul>
</div>
</div>
""", ["tilastoilla-valehtelu", "suhteellinen-riski", "simpsonin-paradoksi", "bkt-harha"])

# ─────────────────── 103 · Suhteellinen riski ───────────────────
page("suhteellinen-riski", 103,
     "Suhteellinen riski — ”riski kaksinkertaistui” yhdestä kahteen",
     "”Riski kasvoi 100 %” voi tarkoittaa siirtymää yhdestä tapauksesta kahteen sataatuhatta kohden. Suhteellinen luku pelottaa, absoluuttinen kertoo mittakaavan.",
     "#c62828", """
<p>”Riski kaksinkertaistui” on otsikko. ”Riski nousi 0,001 prosentista 0,002 prosenttiin” ei ole. Molemmat kuvaavat samaa muutosta. Suhteellinen riski (kuinka monta <em>prosenttia</em> riski muuttui) irrotettuna lähtötasosta on tehokkain tapa pelotella — tai myydä lääkettä — luvuilla, jotka ovat teknisesti tosia.</p>
<div class="tilasto-grid">
<div class="tilasto-esimerkki">
<h4>Harhaanjohtava (suhteellinen muutos)</h4>
<div class="pylvas-wrapper">
<div style="display:flex;flex-direction:column;justify-content:flex-end;height:100%;width:36px;">
<div class="pylvas" style="height:50%;background:#c0392b;">1</div>
</div>
<div style="display:flex;flex-direction:column;justify-content:flex-end;height:100%;width:36px;">
<div class="pylvas" style="height:100%;background:#c0392b;">2</div>
</div>
</div>
<div class="pylvas-label">Ennen &nbsp;&nbsp;&nbsp; Jälkeen</div>
<p style="font-size:0.8em;color:#c0392b;margin-top:0.5rem;">Näyttää: +100 % — riski kaksinkertaistui!</p>
</div>
<div class="tilasto-esimerkki">
<h4>Rehellinen (absoluuttinen taso)</h4>
<div class="pylvas-wrapper">
<div style="display:flex;flex-direction:column;justify-content:flex-end;height:100%;width:36px;">
<div class="pylvas" style="height:100%;background:#ccc;color:#333;font-size:0.6em;">100 000</div>
</div>
<div style="display:flex;flex-direction:column;justify-content:flex-end;height:100%;width:36px;">
<div class="pylvas" style="height:1px;background:#27ae60;"></div>
</div>
<div style="display:flex;flex-direction:column;justify-content:flex-end;height:100%;width:36px;">
<div class="pylvas" style="height:2px;background:#27ae60;"></div>
</div>
</div>
<div class="pylvas-label">Väestö &nbsp;&nbsp; Ennen &nbsp;&nbsp; Jälkeen</div>
<p style="font-size:0.8em;color:#27ae60;margin-top:0.5rem;">Todellisuus: 1 → 2 tapausta sataatuhatta kohden.</p>
</div>
</div>
<h3>Sama temppu molempiin suuntiin</h3>
<ul>
<li><strong>Pelottelu:</strong> ”Ruoka-aine X nostaa syöpäriskiä 18 %” — jos perusriski on 5 %, muutos on 5,0 → 5,9 prosenttiyksikköä elinaikana.</li>
<li><strong>Myynti:</strong> ”Lääke puolittaa riskin” kuulostaa paremmalta kuin ”200 ihmisen pitää syödä lääkettä vuosi, jotta yksi tapaus estyy” (NNT, number needed to treat).</li>
<li><strong>Vähättely:</strong> käänteisesti oma haitta esitetään absoluuttisena (”vain 0,001 %”) ja kilpailijan suhteellisena (”+100 %”).</li>
</ul>
<p>Lähisukulainen on <strong>”rikollisuus kaksinkertaistui”</strong> -otsikko pienistä luvuista: kahdesta tapauksesta neljään sadantuhannen asukkaan kaupungissa. Pienissä luvuissa satunnaisvaihtelu tuottaa rajuja prosentteja joka vuosi.</p>
<div class="infolaatikko">
<strong>Miten tunnistat:</strong> Kun kuulet prosenttimuutoksen riskissä, kysy kaksi lukua: mikä oli lähtötaso ja mikä on uusi taso — per kuinka monta ihmistä? Ilman absoluuttisia lukuja suhteellinen muutos on pelkkä tehokeino.
    </div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Kirjoja</span>
<ul class="lue-lisaa-lista">
<li><cite>Risk Savvy</cite> — Gerd Gigerenzer (2014)</li>
<li><cite>The Art of Statistics</cite> — David Spiegelhalter (2019)</li>
</ul>
</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://en.wikipedia.org/wiki/Relative_risk" target="_blank" rel="noopener">Wikipedia: Relative risk (englanniksi)</a></li>
</ul>
</div>
</div>
""", ["tilastoilla-valehtelu", "keskiarvo-vs-mediaani", "pinta-alaharha", "omenoita-appelsiineja"])

# ─────────────────── 104 · Selviytymisharha ───────────────────
page("selviytymisharha", 104,
     "Selviytymisharha — vain palanneet koneet lasketaan",
     "Abraham Wald huomasi, että palanneiden pommikoneiden osumakartta kertoo missä kone kestää osuman — panssari kuuluu sinne, missä reikiä ei näy.",
     "#37474f", """
<p>Toisen maailmansodan aikana Yhdysvaltain armeija kartoitti palanneiden pommikoneiden luodinreiät: eniten osumia siivissä ja rungossa, vähiten moottoreissa. Johtopäätös tuntui ilmeiseltä — panssaroidaan siivet ja runko. Tilastotieteilijä Abraham Wald käänsi päättelyn: data kuvaa koneita, jotka <em>palasivat</em>. Moottoriin osuneet eivät ole aineistossa, koska ne putosivat. Panssari kuuluu sinne, missä palanneissa koneissa ei ole reikiä.</p>
<div class="tilasto-grid">
<div class="tilasto-esimerkki">
<h4>Harhaanjohtava (näkyvä data)</h4>
<svg viewBox="0 0 300 150" style="width:100%;max-width:300px;border-bottom:2px solid #333;" role="img" aria-label="Lentokoneen ääriviiva, osumapisteet siivissä ja rungossa">
  <path d="M150 15 L160 60 L245 85 L245 100 L160 90 L158 120 L180 135 L180 143 L150 136 L120 143 L120 135 L142 120 L140 90 L55 100 L55 85 L140 60 Z" fill="#eceff1" stroke="#455a64" stroke-width="2"/>
  <g fill="#c0392b">
    <circle cx="90" cy="92" r="3"/><circle cx="110" cy="95" r="3"/><circle cx="200" cy="92" r="3"/>
    <circle cx="222" cy="95" r="3"/><circle cx="150" cy="45" r="3"/><circle cx="148" cy="105" r="3"/>
    <circle cx="152" cy="125" r="3"/><circle cx="128" cy="138" r="3"/><circle cx="172" cy="138" r="3"/>
  </g>
</svg>
<p style="font-size:0.8em;color:#c0392b;margin-top:0.5rem;">Näyttää: panssaroi siivet ja runko — sinne osutaan!</p>
</div>
<div class="tilasto-esimerkki">
<h4>Rehellinen (puuttuva data)</h4>
<svg viewBox="0 0 300 150" style="width:100%;max-width:300px;border-bottom:2px solid #333;" role="img" aria-label="Sama kone, moottorialueet korostettu: niihin osuneet eivät palanneet">
  <path d="M150 15 L160 60 L245 85 L245 100 L160 90 L158 120 L180 135 L180 143 L150 136 L120 143 L120 135 L142 120 L140 90 L55 100 L55 85 L140 60 Z" fill="#eceff1" stroke="#455a64" stroke-width="2"/>
  <ellipse cx="118" cy="80" rx="13" ry="9" fill="#27ae60" opacity="0.85"/>
  <ellipse cx="182" cy="80" rx="13" ry="9" fill="#27ae60" opacity="0.85"/>
  <text x="150" y="147" font-size="8.5" fill="#1a7044" text-anchor="middle">moottoriin osuneet eivät palanneet</text>
</svg>
<p style="font-size:0.8em;color:#27ae60;margin-top:0.5rem;">Todellisuus: panssari sinne, missä reikiä <em>ei</em> näy.</p>
</div>
</div>
<h3>Missä tähän törmää</h3>
<ul>
<li><strong>Menestystarinat:</strong> ”nämä 7 tapaa tekivät minusta miljonäärin” — tuhannet tekivät samat asiat ja epäonnistuivat, mutta heistä ei kirjoiteta kirjaa.</li>
<li><strong>Rahastojen tuottohistoria:</strong> huonot rahastot lakkautetaan tai fuusioidaan, jolloin ”keskimääräinen historiallinen tuotto” lasketaan vain selviytyjistä.</li>
<li><strong>”Ennen rakennettiin kestävää”</strong> — vanhoista rakennuksista ja laitteista näemme vain ne, jotka kestivät. Roju hajosi pois otoksesta.</li>
<li><strong>Yrittäjyyspuhe:</strong> ”koulupudokkaatkin onnistuvat, katso Jobs ja Zuckerberg” — otos on valikoitunut lopputuloksen perusteella.</li>
</ul>
<div class="infolaatikko">
<strong>Miten tunnistat:</strong> Kysy aina: keitä tästä aineistosta puuttuu, ja miksi? Jos otokseen pääsee vain onnistumalla (tai selviytymällä), data kertoo valikoitumisesta — ei syistä.
    </div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Kirjoja</span>
<ul class="lue-lisaa-lista">
<li><cite>The Art of Statistics</cite> — David Spiegelhalter (2019)</li>
<li><cite>Fooled by Randomness</cite> — Nassim Nicholas Taleb (2001)</li>
</ul>
</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://en.wikipedia.org/wiki/Survivorship_bias" target="_blank" rel="noopener">Wikipedia: Survivorship bias (englanniksi)</a></li>
</ul>
</div>
</div>
""", ["tilastoilla-valehtelu", "simpsonin-paradoksi", "p-hakkerointi", "hippo-efekti"])

# ─────────────────── 105 · Simpsonin paradoksi ───────────────────
page("simpsonin-paradoksi", 105,
     "Simpsonin paradoksi — trendi kääntyy kun ryhmät yhdistetään",
     "Sama aineisto voi näyttää kasvua kokonaisuutena ja laskua jokaisessa osaryhmässä. Berkeleyn sisäänpääsytilastot ovat kuuluisin esimerkki.",
     "#00695c", """
<p>Simpsonin paradoksi on tilastotieteen kummallisin ilmiö: trendi, joka näkyy jokaisessa osaryhmässä erikseen, voi kadota tai <em>kääntyä päinvastaiseksi</em>, kun ryhmät yhdistetään. Kumpikaan luku ei ole väärin laskettu — ne vastaavat eri kysymyksiin. Manipuloija valitsee sen tason, joka tukee haluttua johtopäätöstä.</p>
<div class="tilasto-grid">
<div class="tilasto-esimerkki">
<h4>Yhdistettynä: nouseva trendi</h4>
<svg viewBox="0 0 300 150" style="width:100%;max-width:300px;border-bottom:2px solid #333;" role="img" aria-label="Hajontakuvio, jossa yhdistetty trendiviiva nousee">
  <g fill="#7f8c8d">
    <circle cx="40" cy="115" r="4"/><circle cx="60" cy="122" r="4"/><circle cx="80" cy="128" r="4"/><circle cx="100" cy="133" r="4"/>
    <circle cx="190" cy="45" r="4"/><circle cx="215" cy="52" r="4"/><circle cx="240" cy="60" r="4"/><circle cx="262" cy="66" r="4"/>
  </g>
  <line x1="25" y1="130" x2="280" y2="42" stroke="#c0392b" stroke-width="3" stroke-dasharray="7 4"/>
</svg>
<p style="font-size:0.8em;color:#c0392b;margin-top:0.5rem;">Näyttää: mitä enemmän X:ää, sitä enemmän Y:tä.</p>
</div>
<div class="tilasto-esimerkki">
<h4>Ryhmittäin: molemmat laskevat</h4>
<svg viewBox="0 0 300 150" style="width:100%;max-width:300px;border-bottom:2px solid #333;" role="img" aria-label="Sama hajontakuvio ryhmäväreillä: kummankin ryhmän sisäinen trendi laskee">
  <g fill="#2980b9">
    <circle cx="40" cy="115" r="4"/><circle cx="60" cy="122" r="4"/><circle cx="80" cy="128" r="4"/><circle cx="100" cy="133" r="4"/>
  </g>
  <g fill="#27ae60">
    <circle cx="190" cy="45" r="4"/><circle cx="215" cy="52" r="4"/><circle cx="240" cy="60" r="4"/><circle cx="262" cy="66" r="4"/>
  </g>
  <line x1="32" y1="110" x2="108" y2="138" stroke="#2980b9" stroke-width="2.5"/>
  <line x1="182" y1="40" x2="270" y2="71" stroke="#27ae60" stroke-width="2.5"/>
</svg>
<p style="font-size:0.8em;color:#27ae60;margin-top:0.5rem;">Todellisuus: kummankin ryhmän sisällä yhteys on laskeva.</p>
</div>
</div>
<h3>Berkeley 1973</h3>
<p>Kuuluisin esimerkki: Kalifornian yliopistoa Berkeleyssä epäiltiin syrjinnästä, koska miehistä hyväksyttiin 44 % ja naisista 35 %. Laitoksittain tarkasteltuna useimmat laitokset hyväksyivät naisia <em>suuremmalla</em> osuudella. Selitys: naiset hakivat useammin suosittuihin laitoksiin, joihin oli vaikea päästä sukupuolesta riippumatta. Yhdistetty luku kertoi hakukohteista, ei syrjinnästä.</p>
<h3>Missä tähän törmää</h3>
<ul>
<li><strong>Sairaalavertailut:</strong> yliopistosairaalan kuolleisuus on korkeampi — koska sinne ohjataan vaikeimmat tapaukset. Potilasryhmittäin se voi olla joka ryhmässä parempi.</li>
<li><strong>Palkkaerot:</strong> kokonaiskeskiarvo ja ammattiryhmittäinen vertailu voivat osoittaa eri suuntiin — ja kumpikin osapuoli siteeraa omaansa.</li>
<li><strong>Koulujen tulokset:</strong> ”keskiarvo parani” voi syntyä pelkästä oppilaspohjan muutoksesta, vaikka jokainen ryhmä heikkeni.</li>
</ul>
<div class="infolaatikko">
<strong>Miten tunnistat:</strong> Kun kaksi osapuolta siteeraa ”samaa dataa” vastakkaisin johtopäätöksin, kysy: millä tasolla luvut on laskettu — yhdistettynä vai ryhmittäin? Ja mikä kolmas tekijä (hakukohde, potilasaines, ryhmien koko) jakaa aineiston?
    </div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Kirjoja</span>
<ul class="lue-lisaa-lista">
<li><cite>The Book of Why</cite> — Judea Pearl (2018)</li>
<li><cite>The Art of Statistics</cite> — David Spiegelhalter (2019)</li>
</ul>
</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://en.wikipedia.org/wiki/Simpson%27s_paradox" target="_blank" rel="noopener">Wikipedia: Simpson's paradox (englanniksi)</a></li>
</ul>
</div>
</div>
""", ["tilastoilla-valehtelu", "keskiarvo-vs-mediaani", "selviytymisharha", "goodhartin-laki"])

# ─────────────────── 106 · P-hakkerointi ───────────────────
page("p-hakkerointi", 106,
     "P-hakkerointi — testaa kunnes jokin näyttää merkitsevältä",
     "Kun samaa aineistoa testataan kahdellakymmenellä tavalla, yksi ”merkitsevä” tulos syntyy sattumalta. Julkaisuun päätyy se yksi — muut jäävät pöytälaatikkoon.",
     "#ef6c00", """
<p>Tieteessä tulosta pidetään perinteisesti ”tilastollisesti merkitsevänä”, jos sattuman todennäköisyys on alle 5 % (p&nbsp;&lt;&nbsp;0,05). Kääntöpuoli: jos testaat kahtakymmentä asiaa, keskimäärin yksi näyttää merkitsevältä <em>pelkästä sattumasta</em>. P-hakkerointi tarkoittaa, että aineistoa viipaloidaan, muuttujia vaihdetaan ja testejä toistetaan, kunnes jokin ylittää julkaisukynnyksen — ja vain se raportoidaan.</p>
<div class="tilasto-grid">
<div class="tilasto-esimerkki">
<h4>Harhaanjohtava (raportoitu tulos)</h4>
<div style="display:flex;flex-direction:column;justify-content:center;align-items:center;height:120px;border-bottom:2px solid #333;">
<div style="background:#c0392b;color:#fff;padding:0.7em 1em;font-size:0.9em;font-weight:bold;">Suklaa kiihdyttää laihtumista!<br><span style="font-weight:normal;font-size:0.85em;">p = 0,03</span></div>
</div>
<p style="font-size:0.8em;color:#c0392b;margin-top:0.5rem;">Näyttää: tieteellisesti todistettu löydös.</p>
</div>
<div class="tilasto-esimerkki">
<h4>Rehellinen (kaikki tehdyt testit)</h4>
<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:3px;height:120px;border-bottom:2px solid #333;padding-bottom:4px;">
<div style="background:#ddd;"></div><div style="background:#ddd;"></div><div style="background:#ddd;"></div><div style="background:#ddd;"></div><div style="background:#ddd;"></div>
<div style="background:#ddd;"></div><div style="background:#ddd;"></div><div style="background:#27ae60;display:flex;align-items:center;justify-content:center;color:#fff;font-size:0.6em;">p=0,03</div><div style="background:#ddd;"></div><div style="background:#ddd;"></div>
<div style="background:#ddd;"></div><div style="background:#ddd;"></div><div style="background:#ddd;"></div><div style="background:#ddd;"></div><div style="background:#ddd;"></div>
<div style="background:#ddd;"></div><div style="background:#ddd;"></div><div style="background:#ddd;"></div><div style="background:#ddd;"></div><div style="background:#ddd;"></div>
</div>
<div class="pylvas-label">20 testattua muuttujaa</div>
<p style="font-size:0.8em;color:#27ae60;margin-top:0.5rem;">Todellisuus: 1/20 ”osumaa” on juuri sattuman odotusarvo.</p>
</div>
</div>
<h3>Suklaatutkimus, joka meni läpi</h3>
<p>Vuonna 2015 toimittaja John Bohannon julkaisi tahallisen p-hakkerointitutkimuksen: pieni koeryhmä, 18 mitattua muuttujaa — jokin niistä ylittäisi merkitsevyysrajan lähes varmasti. Osuma sattui painonpudotukseen, ja ”suklaa auttaa laihtumaan” kiersi maailman lehdet. Sama mekanismi tuottaa vilpittömästikin vääriä löydöksiä: tutkija tekee kymmeniä pieniä valintoja (ketkä mukaan, mitä kontrolloidaan, mikä mittari), joista jokainen voi kääntää tuloksen — Andrew Gelman kutsuu tätä ”haarautuvien polkujen puutarhaksi”.</p>
<h3>Sama logiikka arjessa</h3>
<ul>
<li><strong>Markkinointi:</strong> ”9/10 testaajista suositteli” — kysely toistettiin, kunnes tuli hyvä otos.</li>
<li><strong>Sijoitusgurut:</strong> sadasta ennustajasta joku osuu aina oikeaan viisi kertaa putkeen — hänet nostetaan esiin, muut unohdetaan.</li>
<li><strong>Julkaisuharha:</strong> lehdet julkaisevat löydöksiä, eivät ”ei vaikutusta” -tuloksia — joten kirjallisuuteen kertyy sattumaosumia.</li>
</ul>
<div class="infolaatikko">
<strong>Miten tunnistat:</strong> Kysy: montako asiaa testattiin ennen tätä ”löydöstä”? Oliko hypoteesi lyöty lukkoon ennen datan keruuta (esirekisteröinti)? Onko tulos toistettu riippumattomassa aineistossa? Yksittäinen p &lt; 0,05 ilman näitä on arpalippu, ei todiste.
    </div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Kirjoja</span>
<ul class="lue-lisaa-lista">
<li><cite>Science Fictions</cite> — Stuart Ritchie (2020)</li>
<li><cite>The Art of Statistics</cite> — David Spiegelhalter (2019)</li>
</ul>
</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://en.wikipedia.org/wiki/Data_dredging" target="_blank" rel="noopener">Wikipedia: Data dredging (englanniksi)</a></li>
<li><a href="https://xkcd.com/882/" target="_blank" rel="noopener">xkcd 882: Significant (vihreät hernekarkit)</a></li>
</ul>
</div>
</div>
""", ["tilastoilla-valehtelu", "cherry-picking-aikavali", "selviytymisharha", "konsensus-fetissi"])


def build():
    tpl = TEMPLATE.read_text(encoding="utf-8")
    OUT.mkdir(exist_ok=True)

    ids_match = re.search(r"const IDS = \[(.*?)\];", tpl, re.S)
    vanhat = [s.strip().strip('"') for s in ids_match.group(1).split(",")]
    assert len(vanhat) == 98, f"odotettiin 98 id:tä, saatiin {len(vanhat)}"
    kaikki = vanhat + UUDET
    ids_js = "const IDS = [" + ", ".join(json.dumps(s) for s in kaikki) + "];"

    old_title = "Tilastoilla valehtelu — visuaaliset ansat"
    old_desc = ("Darrell Huff dokumentoi kirjassaan How to Lie with Statistics (1954) "
                "tekniikat, joilla tilastoja voidaan esittää harhaanjohtavasti — teknisesti…")

    for i, p in enumerate(PAGES):
        slug, num = p["slug"], p["num"]
        prev_slug = UUDET[i - 1] if i > 0 else "haamutyopaikat"
        prev_nimi = (PAGES[i - 1]["otsikko"] if i > 0 else "Haamutyöpaikat — ilmoitukset joita ei ole tarkoituskaan täyttää")
        next_slug = UUDET[i + 1] if i < len(PAGES) - 1 else None
        next_nimi = PAGES[i + 1]["otsikko"] if i < len(PAGES) - 1 else None

        html = tpl

        # 1) Sisältölohko
        uusi_ilmio = (f'<div class="ilmio" id="{slug}">\n'
                      f'<div class="ilmio-tag">Ilmiö {num}</div>\n'
                      f'<h1>{p["otsikko"]}</h1>\n'
                      f'<p class="ilmio-byline">Kirjoittanut <a href="tietoa.html" rel="author">Ilmiömies</a> · Päivitetty {PVM_FI}</p>'
                      f'{p["sisalto"]}</div>')
        html = re.sub(r'<div class="ilmio" id="tilastoilla-valehtelu">.*?\n</div>\n\n  <aside',
                      lambda m: uusi_ilmio + "\n\n  <aside", html, count=1, flags=re.S)

        # 2) Liittyvät + navigointi
        html = re.sub(r'<aside class="liittyvat".*?</aside>', lambda m: liittyvat_html(p["liittyvat"]).strip(),
                      html, count=1, flags=re.S)
        html = re.sub(r'<nav class="kortti-nav">.*?</nav>',
                      lambda m: nav_html(num, prev_slug, prev_nimi, next_slug, next_nimi).strip(),
                      html, count=1, flags=re.S)

        # 3) IDS / PREV / NEXT / random-poissulku
        html = re.sub(r"const IDS = \[.*?\];", lambda m: ids_js, html, count=1, flags=re.S)
        html = html.replace("const PREV = 'hajota-hallitse.html';", f"const PREV = '{prev_slug}.html';")
        html = html.replace("const NEXT = 'bkt-harha.html';",
                            f"const NEXT = '{next_slug + '.html' if next_slug else ''}';")
        html = html.replace("id === 'tilastoilla-valehtelu'", f"id === '{slug}'")

        # 4) Otsikot, kuvaukset, URL:t, kategoria, päivämäärät
        html = html.replace(old_title, p["otsikko"])
        html = html.replace(old_desc, p["kuvaus"])
        html = html.replace("tilastoilla-valehtelu.html", f"{slug}.html")
        html = html.replace("Informaatio ja propaganda", KATEGORIA_NIMI)
        html = html.replace("#informaatio-ja-propaganda", KATEGORIA_ANKKURI)
        html = html.replace('"datePublished": "2026-06-19"', f'"datePublished": "{PVM_ISO}"')
        html = html.replace('"dateModified": "2026-06-19"', f'"dateModified": "{PVM_ISO}"')

        # 5) noindex-luonnosmerkintä + sivun väri
        html = html.replace(
            '<link rel="canonical"',
            '<meta name="robots" content="noindex"><!-- POISTA-JULKAISTAESSA -->\n  <link rel="canonical"')
        html = html.replace(
            "</head>",
            f"  <style>#{slug} {{ border-top-color: {p['vari']}; }} "
            f"#{slug} .ilmio-tag {{ background: {p['vari']}; }}</style>\n</head>")

        (OUT / f"{slug}.html").write_text(html, encoding="utf-8")
        print(f"  {num}  {slug}.html  ({len(html) // 1024} KB)")

    print(f"\nValmis: {len(PAGES)} luonnosta kansiossa {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    build()
