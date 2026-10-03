#!/usr/bin/env python3
"""Generoi luonnokset 14. kategorialle "Roolit ja valtapelit" (9 ilmiötä).

Tausta: ihmissuhteiden roolidynamiikka puuttui sivustolta kokonaan. Repossa ei
ollut yhtään osumaa sanoihin draamakolmio, karpman, kaksoissidos, läheisriippu*,
välirikko tai syntipukki. Lähimmät sivut kattoivat yksittäiset taktiikat
(gaslighting 28, DARVO 23, blame game 27) mutta eivät sitä rakennetta, jossa
kaksi ihmistä jää kiinni samaan kuvioon vuosiksi.

Karsinta: Karpmanin 12 kolmiosta mukaan tulee neljä. False Perception on
päällekkäinen Hanlonin partaveitsen (34) kanssa, Indecision sunk cost -harhan
(31) kanssa, ja Question Mark / Trapping / Escape / Vicious Cycle / Oppression
jäävät pois koska niillä ei ole vakiintunutta suomennosta eikä hakukysyntää.
Liberation-kolmio tulee mukaan Choyn (1990) voittajakolmiona ja Alcoholic Family
-kolmio yleistettynä mahdollistajana.

Jokainen sivu näyttää saman mekanismin sekä työelämässä että läheissuhteessa.
Kolmella sivulla (välirikko, syntipukki, no contact) kulkee sama havainto:
irtautuminen on epäsymmetrinen: lähtijä maksaa siirtymän kerran, jäävä maksaa
ylläpitoa jatkuvasti.

Numerot 140-148 ovat lopulliset: lohko lisätään index.html:n hub-listan loppuun,
joten ilmiöt 1-139 eivät numeroidu uudelleen.

Julkaisu: index.html:ään käsin uusi hub-kategoria-lohko, sitten
    python3 scripts/lisaa_ilmiot.py --kortit-valmiina --kirjoita

Ajo:  python3 scripts/build_valtapelit_luonnokset.py
"""
import glob
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "darvo.html"
OUT = ROOT / "luonnokset"

PVM_ISO = "2026-09-22"
PVM_FI = "22.9.2026"

VANHA_SLUG = "darvo"
KAT_NIMI = "Roolit ja valtapelit"
KAT_SIVU = "kategoria-roolit-ja-valtapelit.html"

# viimeinen julkaistu ilmiö (139) — uuden kategorian PREV-ketju kiinnittyy tähän
EDELTAJA = ("vihamielisen-median-harha",
            "Vihamielisen median harha — sama juttu on molempien mielestä puolueellinen")

YHTEENSA = 148

# slug -> (numero, väri, nimi, kortin kuvaus)
OMAT_KORTIT = {
    "draamakolmio": (140, "#ad1457", "Draamakolmio",
        "Uhri, pelastaja ja vainooja — kolme roolia, joissa kukaan ei ratkaise sitä mistä riidellään."),
    "roolinvaihto": (141, "#880e4f", "Roolinvaihto",
        "Pelastajasta tulee vainooja ja auttajasta uhri — hetki, joka tekee kuviosta pelin."),
    "voittajakolmio": (142, "#00695c", "Voittajakolmio",
        "Sama kolmio ilman peliä: haavoittuva, välittävä ja jämäkkä uhrin, pelastajan ja vainoojan tilalla."),
    "kaksoissidos": (143, "#4a148c", "Kaksoissidos",
        "Kaksi vaatimusta, jotka sulkevat toisensa pois — eikä ristiriidasta saa mainita eikä tilanteesta poistua."),
    "mahdollistaja": (144, "#ef6c00", "Mahdollistaja",
        "Se joka paikkaa jäljet pitää ongelman käynnissä: seuraukset eivät koskaan osu siihen joka ne aiheuttaa."),
    "syntipukki": (145, "#b71c1c", "Syntipukki-rooli",
        "Ryhmällä on yksi nimetty kantaja — ja kun hän lähtee, tilalle valitaan uusi."),
    "valirikko": (146, "#37474f", "Välirikko",
        "Suhde katkaistaan kokonaan, ja lasku lankeaa eri tavalla lähtijälle kuin jäävälle."),
    "no-contact": (147, "#263238", "No contact",
        "Täydellinen katkaisu poistaa pelistä toisen pelaajan — myös satunnaiset viestit, jotka pitäisivät sen käynnissä."),
    "harmaa-kivi": (148, "#607d8b", "Harmaa kivi",
        "Kun lähteminen ei ole mahdollista: reaktio on palkkio, ja tylsyys vie palkkion pois."),
}


def julkaistut_kortit():
    """Korttitiedot index.html:n hub-korteista — yksi totuuden lähde."""
    kortit = {}
    hub = re.compile(
        r'<a href="([a-z0-9-]+)\.html" class="hub-kortti" style="--c:(#[0-9a-fA-F]+)">\s*'
        r'<span class="hub-numero">(\d+)</span>\s*<span class="hub-teksti">\s*'
        r'<span class="hub-nimi">([^<]*)</span>\s*<span class="hub-kuvaus">([^<]*)</span>')
    for m in hub.finditer((ROOT / "index.html").read_text(encoding="utf-8")):
        kortit[m.group(1)] = (int(m.group(3)), m.group(2), m.group(4), m.group(5))
    # 139 ennen erää, 148 sen jälkeen — lukumäärä ei saa pienentyä
    assert len(kortit) >= 139, f"kortteja {len(kortit)}, odotettiin vähintään 139"
    return kortit


KORTIT = julkaistut_kortit()
KORTIT.update(OMAT_KORTIT)


def liittyvat_html(slugit):
    osat = ['  <aside class="liittyvat" aria-label="Liittyvät ilmiöt">',
            "    <h2>Liittyvät ilmiöt</h2>",
            '    <div class="liittyvat-kortit">']
    for s in slugit:
        num, vari, nimi, kuvaus = KORTIT[s]
        href = f"{s}.html" if s in OMAT_KORTIT else f"../{s}.html"
        osat.append(f'''    <a href="{href}" class="liittyvat-kortti" style="--c:{vari}">
      <span class="liittyvat-numero">{num}</span>
      <span class="liittyvat-teksti">
        <span class="liittyvat-nimi">{nimi}</span>
        <span class="liittyvat-kuvaus">{kuvaus}</span>
      </span>
      <span class="liittyvat-nuoli" aria-hidden="true">›</span>
    </a>''')
    osat.append("    </div>\n  </aside>")
    return "\n".join(osat)


def nav_html(num, prev_href, prev_nimi, next_href, next_nimi):
    prev = (f'<a class="kortti-nav-btn" href="{prev_href}">← {prev_nimi}</a>'
            if prev_href else '<span class="kortti-nav-btn disabled">←</span>')
    nxt = (f'<a class="kortti-nav-btn" href="{next_href}">{next_nimi} →</a>'
           if next_href else '<span class="kortti-nav-btn disabled">→</span>')
    return f'''  <nav class="kortti-nav">
    {prev}
    <div class="kortti-nav-center">
      <span class="kortti-nav-laskuri">{num} / {YHTEENSA}</span>
      <span class="kortti-nav-vinkki">
        <kbd>&#8592;</kbd> <kbd>&#8594;</kbd> selaa &middot; <kbd>R</kbd> satunnainen
        <span class="touch-vinkki">&nbsp;· swipe &#8592;&#8594; tai &#8595; random</span>
      </span>
    </div>
    {nxt}
  </nav>'''


def seo_lohko(slug, otsikko, og_title, kuvaus, faq):
    """Koko <!-- SEO --> … </script> uudelleen: meta-tagit + JSON-LD @graph."""
    url = f"https://www.ilmiöt.fi/{slug}.html"
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Ilmiöitä",
                 "item": "https://www.ilmiöt.fi/"},
                {"@type": "ListItem", "position": 2, "name": KAT_NIMI,
                 "item": f"https://www.ilmiöt.fi/{KAT_SIVU}"},
                {"@type": "ListItem", "position": 3, "name": otsikko, "item": url}]},
            {"@type": "Article",
             "image": {"@type": "ImageObject", "url": "https://www.ilmiöt.fi/og/brand.png",
                       "width": 1200, "height": 630},
             "@id": f"{url}#article", "url": url, "headline": otsikko,
             "description": kuvaus, "inLanguage": "fi", "articleSection": KAT_NIMI,
             "isPartOf": {"@type": "CollectionPage", "@id": "https://www.ilmiöt.fi/"},
             "publisher": {"@type": "Organization", "name": "Ilmiöitä",
                           "url": "https://www.ilmiöt.fi/",
                           "@id": "https://www.ilmiöt.fi/#organization",
                           "logo": {"@type": "ImageObject",
                                    "url": "https://www.ilmiöt.fi/favicon.svg",
                                    "width": 64, "height": 64}},
             "about": {"@type": "DefinedTerm", "name": otsikko, "description": kuvaus,
                       "inDefinedTermSet": {"@type": "DefinedTermSet",
                                            "name": "Ilmiöitä — Miten valta toimii",
                                            "@id": "https://www.ilmiöt.fi/"}},
             "author": {"@type": "Person", "@id": "https://www.ilmiöt.fi/#ilmiomies",
                        "name": "Ilmiömies", "url": "https://www.ilmiöt.fi/tietoa.html",
                        "description": "Kirjoittajanimi, jonka takana on kiinnostus valtaan, vaikuttamiseen ja ihmisen päättelyn vinoumiin. Sisältö perustuu julkisiin lähteisiin ja vakiintuneeseen käsitteistöön."},
             "datePublished": PVM_ISO, "dateModified": PVM_ISO},
            {"@type": "FAQPage", "@id": f"{url}#faq", "inLanguage": "fi",
             "mainEntity": [{"@type": "Question", "name": q,
                             "acceptedAnswer": {"@type": "Answer", "text": a}}
                            for q, a in faq]},
        ],
    }
    ld = json.dumps(graph, ensure_ascii=False, indent=2)
    return f'''  <!-- SEO -->
  <meta name="description" content="{kuvaus}">
  <link rel="canonical" href="{url}">
  <meta property="og:title" content="{og_title}">
  <meta property="og:description" content="{kuvaus}">
  <meta property="og:url" content="{url}">
  <meta property="og:type" content="article">
  <meta property="og:locale" content="fi_FI">
  <meta property="og:site_name" content="Ilmiöitä — Miten valta toimii">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{og_title}">
  <meta name="twitter:description" content="{kuvaus}">
  <meta property="og:image" content="https://www.ilmiöt.fi/og/brand.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Ilmiöitä — Miten valta toimii">
  <meta name="twitter:image" content="https://www.ilmiöt.fi/og/brand.png">
  <style>.ilmio h1{{margin-top:0;font-family:'Spectral',Georgia,serif;}}</style>
  <script type="application/ld+json">
{ld}
</script>'''


PAGES = []


def page(slug, otsikko, og_title, kuvaus, faq, sisalto, liittyvat):
    num, vari = OMAT_KORTIT[slug][0], OMAT_KORTIT[slug][1]
    PAGES.append(dict(slug=slug, num=num, vari=vari, otsikko=otsikko, og_title=og_title,
                      kuvaus=kuvaus, faq=faq, sisalto=sisalto, liittyvat=liittyvat))


# ────────────────────────── 140 · Draamakolmio ──────────────────────────
page("draamakolmio",
     "Draamakolmio — uhri, pelastaja ja vainooja",
     "Draamakolmio — Karpmanin kolme roolia suomeksi | Ilmiöitä",
     "Draamakolmio on Karpmanin malli kolmesta roolista: uhri, pelastaja ja vainooja. Näin tunnistat kuvion työpaikalla ja läheissuhteessa.",
     [("Mitä draamakolmio tarkoittaa?",
       "Draamakolmio on psykiatri Stephen Karpmanin vuonna 1968 kuvaama malli, jossa toistuva ristiriita asettuu kolmeen rooliin: uhri kokee olevansa voimaton, pelastaja ratkaisee toisen puolesta ja vainooja osoittaa syyllisen. Roolit eivät kerro siitä, kuka on oikeassa, vaan siitä minkä aseman kukin ottaa — ja niin kauan kuin asemat pysyvät, itse asia ei ratkea."),
      ("Miten draamakolmion tunnistaa?",
       "Tunnusmerkki on toisto ilman ratkaisua: sama keskustelu käydään uudelleen, samat repliikit toistuvat ja lopputulos on joka kerta sama. Toinen merkki on se, että kukaan ei puhu omasta osuudestaan — uhri puhuu siitä mitä hänelle tehdään, pelastaja siitä mitä hän tekee toisten puolesta ja vainooja siitä mitä muut jättävät tekemättä."),
      ],
     r"""
<p><strong>Draamakolmio</strong> (engl. <em>drama triangle</em>) on psykiatri Stephen Karpmanin vuonna 1968 kuvaama malli, jossa toistuva ristiriita asettuu kolmeen rooliin: <strong>uhri</strong>, <strong>pelastaja</strong> ja <strong>vainooja</strong>. Roolit eivät kerro siitä, kuka tosiasiassa on oikeassa tai kärsinyt vääryyttä. Ne kertovat asemasta, jonka kukin ottaa — ja siitä, että kolme asemaa yhdessä pitävät tilanteen paikallaan.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Mitä draamakolmio tarkoittaa suomeksi?</h2>
<p style="margin:0.4em 0 0;"><strong>Draamakolmio</strong> on vakiintunut suomennos termistä <em>Karpman drama triangle</em>. Roolien nimet ovat <strong>uhri</strong> (<em>Victim</em>), <strong>pelastaja</strong> (<em>Rescuer</em>) ja <strong>vainooja</strong> (<em>Persecutor</em>). Malli on peräisin transaktioanalyysistä: Karpman julkaisi sen artikkelissa <cite>Fairy Tales and Script Drama Analysis</cite> vuonna 1968.</p>
</div>
<div class="mermaid">
flowchart TD
  U["Uhri\n'En minä voi tälle mitään'"] --&gt; P["Pelastaja\n'Minä hoidan tämän'"]
  P --&gt; V["Vainooja\n'Tämä on sinun syytäsi'"]
  V --&gt; U
  V --&gt; A["Alkuperäinen asia\njää käsittelemättä"]
  style U fill:#fff3cd,stroke:#f39c12
  style P fill:#fff3cd,stroke:#f39c12
  style V fill:#fdf0f0,stroke:#c0392b
    </div>
<p class="kaavio-selitys">Kolme roolia pitävät toisiaan pystyssä: jokainen tarvitsee kaksi muuta.</p>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Kolme roolia käytännössä:</h2>
<ul style="margin:0.5em 0 0;">
<li><strong>Uhri:</strong> "en minä voi tälle mitään." Ei kyse ole siitä, ettei vääryyttä olisi tapahtunut — vaan siitä, että oma liikkumavara kiistetään kokonaan.</li>
<li><strong>Pelastaja:</strong> "minä hoidan tämän." Auttaa pyytämättä ja ratkaisee toisen puolesta, jolloin toinen ei koskaan joudu ratkaisemaan itse.</li>
<li><strong>Vainooja:</strong> "tämä on sinun syytäsi." Osoittaa syyllisen ja vaatii tiukkuutta, mutta ei tarjoa tietä ulos.</li>
</ul>
</div>
<p>Työpaikalla kuvio näyttää usein tältä: esimies ottaa alisuoriutuvan tiimiläisen työt hoitaakseen (pelastaja), muu tiimi kantaa kuorman ja kokee tulleensa jätetyksi yksin (uhri), ja lopulta joku vaatii puuttumista ja leimautuu koviksi (vainooja). Läheissuhteessa samat kolme asemaa jakautuvat sukulaisten kesken. Kummassakin tapauksessa riita siirtyy siihen, kuka käyttäytyy huonosti — ei siihen, mikä alun perin oli ongelma. Sama huomion siirto tapahtuu <a href="blame-game.html">syyllisen etsinnässä</a> ja <a href="darvo.html">DARVOssa</a>.</p>
<div class="vaaralatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Merkki kolmiosta ei ole riita vaan <strong>toisto ilman ratkaisua</strong>: sama keskustelu, samat repliikit, sama lopputulos. Toinen merkki on se, ettei kukaan puhu omasta osuudestaan. Ulos ei pääse vaihtamalla roolia — pelastajasta tulee helposti vainooja — vaan vaihtamalla tasoa: kysy mitä konkreettista pyydetään, mihin mennessä ja kuka sen tekee. Älä auta pyytämättä, äläkä ratkaise toisen puolesta sitä, minkä hän voi ratkaista itse. Huomaa myös, ettei malli sovi tilanteeseen, jossa joku oikeasti käyttää valtaa väärin: silloin kyse ei ole rooleista vaan teosta, ja "kaikki ovat osallisia" -tulkinta on itsessään vahingollinen.
    </div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Kirjoja</span>
<ul class="lue-lisaa-lista">
<li><cite>Games People Play</cite> — Eric Berne (1964)</li>
<li><cite>A Game Free Life</cite> — Stephen Karpman (2014)</li>
<li><cite>TA Today</cite> — Ian Stewart &amp; Vann Joines (1987)</li>
</ul>
</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://en.wikipedia.org/wiki/Karpman_drama_triangle" target="_blank" rel="noopener">Wikipedia: Karpman drama triangle (englanniksi)</a></li>
</ul>
</div>
</div>""",
     ["roolinvaihto", "voittajakolmio", "syntipukki", "blame-game", "darvo"])


# ────────────────────────── 141 · Roolinvaihto ──────────────────────────
page("roolinvaihto",
     "Roolinvaihto — hetki, jossa auttajasta tulee syyttäjä",
     "Roolinvaihto draamakolmiossa — mikä on switch | Ilmiöitä",
     "Roolinvaihto on hetki, jossa pelastajasta tulee vainooja ja auttajasta uhri. Se on draamakolmion moottori — ilman sitä kuvio ei toistuisi.",
     [("Mitä roolinvaihto tarkoittaa draamakolmiossa?",
       "Roolinvaihto tarkoittaa hetkeä, jossa osapuolten asemat kääntyvät kesken keskustelun: pelastaja alkaa syyttää, autettava alkaa puolustautua ja auttaja esittää itsensä uhrina. Stephen Karpman kutsui tätä käännettä nimellä switch, ja juuri se erottaa pelin tavallisesta erimielisyydestä."),
      ("Miksi roolinvaihto toistuu?",
       "Koska käänne tuottaa jotain, jota kumpikaan ei saisi suoraan pyytämällä: auttaja saa tunnustuksen tekemästään työstä ja autettava vapautuu vastuusta. Kun molemmat saavat jotain, kuvio ei pääty vaikka se tuntuu kummastakin pahalta."),
      ],
     r"""
<p><strong>Roolinvaihto</strong> (engl. <em>the switch</em>) on hetki, jossa <a href="draamakolmio.html">draamakolmion</a> asemat kääntyvät kesken keskustelun. Pelastaja alkaa syyttää, autettava puolustautuu ja auttaja esittää lopulta itsensä uhrina. Stephen Karpman piti tätä käännettä mallin ytimenä: ilman sitä kolmio olisi pelkkä roolilista, käänteen kanssa siitä tulee peli, joka toistuu.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Mitä roolinvaihto tarkoittaa suomeksi?</h2>
<p style="margin:0.4em 0 0;">Englanninkielinen termi on <em>the switch</em> tai <em>switching in the drama triangle</em>; suomeksi puhutaan <strong>roolinvaihdosta</strong> tai <strong>vaihdosta</strong>. Käsite on osa Eric Bernen (1964) pelianalyysiä, jossa vaihto on se kohta, joka tuottaa pelin lopputuloksen — kaikki sitä edeltävä on vain asetelman rakentamista.</p>
</div>
<div class="mermaid">
flowchart TD
  T["Tarjous: 'anna kun minä autan'"] --&gt; S["Suostumus:\n'no jos kerran ehdit'"]
  S --&gt; K["Kuorma kasvaa,\nkiitos jää tulematta"]
  K --&gt; V["VAIHTO: 'minä teen kaiken\netkä sinä arvosta mitään'"]
  V --&gt; L["Auttajasta uhri,\nautetusta syyllinen"]
  style V fill:#fdf0f0,stroke:#c0392b
  style L fill:#fff3cd,stroke:#f39c12
    </div>
<p class="kaavio-selitys">Vaihto tulee aina yllätyksenä — se on koko kuvion maksuhetki.</p>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Kolme tavallista käännettä:</h2>
<ul style="margin:0.5em 0 0;">
<li><strong>Pelastajasta vainooja:</strong> "minä olen tehnyt tämän puolestasi kuukausia" — apu muuttuu laskuksi, jota ei koskaan sovittu.</li>
<li><strong>Pelastajasta uhri:</strong> "kukaan ei arvosta sitä mitä teen." Auttaja siirtyy kolmion pohjalle ja odottaa nyt itse pelastajaa.</li>
<li><strong>Uhrista vainooja:</strong> "sinä et koskaan antanut minun yrittää itse" — autettu maksaa takaisin syytöksellä, ja kuvio alkaa alusta.</li>
</ul>
</div>
<p>Työpaikalla vaihto tapahtuu tyypillisesti kehityskeskustelussa tai sen jälkeisessä sähköpostissa: kollega, joka on vuoden ajan paikannut toisen jälkiä, luettelee yhtäkkiä kaiken tekemänsä. Lista on useimmiten tosi — mutta se esitetään vasta kun se toimii syytöksenä, ei silloin kun työnjaosta olisi voinut sopia. Läheissuhteessa sama käänne kuuluu lauseessa "kaiken sen jälkeen mitä olen tehnyt sinun vuoksesi". Käänteen jälkeen keskustelu koskee velkaa, ei alkuperäistä asiaa — samalla tavalla kuin <a href="maalitolppien-siirtaminen.html">maalitolppien siirtämisessä</a> kohde vaihtuu kesken pelin.</p>
<div class="vaaralatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Vaihdon tunnistaa <strong>yllätyksestä ja aikahypystä</strong>: syytös koskee asioita, joista ei ole puhuttu silloin kun ne tapahtuivat. Tyypillinen sanamuoto on "aina", "en koskaan" ja "kaiken sen jälkeen". Vastakeino on tylsä mutta toimiva: sovi apu etukäteen ääneen — mitä, kuinka paljon ja mihin asti — jolloin siitä ei voi myöhemmin tulla laskua. Jos käänne on jo tapahtunut, erottele kaksi asiaa: velkalista käsitellään omana keskusteluna ja alkuperäinen kysymys omanaan. Älä vastaa syytökseen vastasyytöksellä; se vain siirtää sinut kolmion seuraavaan kulmaan.
    </div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Kirjoja</span>
<ul class="lue-lisaa-lista">
<li><cite>Games People Play</cite> — Eric Berne (1964)</li>
<li><cite>A Game Free Life</cite> — Stephen Karpman (2014)</li>
<li><cite>Born to Win</cite> — Muriel James &amp; Dorothy Jongeward (1971)</li>
</ul>
</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://en.wikipedia.org/wiki/Karpman_drama_triangle" target="_blank" rel="noopener">Wikipedia: Karpman drama triangle (englanniksi)</a></li>
</ul>
</div>
</div>""",
     ["draamakolmio", "voittajakolmio", "mahdollistaja", "maalitolppien-siirtaminen", "darvo"])


# ────────────────────────── 142 · Voittajakolmio ──────────────────────────
page("voittajakolmio",
     "Voittajakolmio — sama kolmio ilman peliä",
     "Voittajakolmio — Choyn vastine draamakolmiolle | Ilmiöitä",
     "Voittajakolmio korvaa uhrin, pelastajan ja vainoojan haavoittuvalla, välittävällä ja jämäkällä. Acey Choyn 1990 malli draamakolmiosta ulos.",
     [("Mikä on voittajakolmio?",
       "Voittajakolmio on Acey Choyn vuonna 1990 esittämä vastine draamakolmiolle. Siinä jokaiselle kolmelle roolille on rakentava vastine: uhrin tilalla on haavoittuva, pelastajan tilalla välittävä ja vainoojan tilalla jämäkkä. Asemat säilyvät, mutta jokaiseen palautetaan vastuu ja toimintakyky."),
      ("Miten voittajakolmiota käytetään?",
       "Se on tarkistuslista omalle puheenvuorolle. Haavoittuva kertoo ongelman ja pyytää konkreettista apua. Välittävä kysyy mitä tarvitaan sen sijaan että ratkaisisi toisen puolesta. Jämäkkä kertoo oman rajansa ilman että arvioi toisen luonnetta. Yhden osapuolen siirtymä riittää muuttamaan keskustelun suunnan."),
      ],
     r"""
<p><strong>Voittajakolmio</strong> (engl. <em>the winner's triangle</em>) on transaktioanalyytikko Acey Choyn vuonna 1990 esittämä vastine <a href="draamakolmio.html">draamakolmiolle</a>. Ajatus on, että kolme asemaa eivät ole itsessään ongelma — ongelma on se, mitä kussakin asemassa tehdään. Choy antoi jokaiselle roolille rakentavan vastineen: <strong>haavoittuva</strong>, <strong>välittävä</strong> ja <strong>jämäkkä</strong>.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Mitä voittajakolmio tarkoittaa suomeksi?</h2>
<p style="margin:0.4em 0 0;"><strong>Voittajakolmio</strong> on suomennos termistä <em>the winner's triangle</em>, jonka Acey Choy julkaisi <cite>Transactional Analysis Journal</cite> -lehdessä vuonna 1990. Roolien englanninkieliset nimet ovat <em>Vulnerable</em> (haavoittuva), <em>Caring</em> (välittävä) ja <em>Assertive</em> (jämäkkä). Stephen Karpman käytti myöhemmin samasta ajatuksesta nimitystä <em>triangles of liberation</em>.</p>
</div>
<div class="mermaid">
flowchart TD
  U["Uhri:\n'en voi mitään'"] --&gt; H["Haavoittuva:\n'tarvitsen apua tässä'"]
  P["Pelastaja:\n'minä hoidan'"] --&gt; V["Välittävä:\n'mitä tarvitset?'"]
  X["Vainooja:\n'sinun syytäsi'"] --&gt; J["Jämäkkä:\n'tämä on minun rajani'"]
  style U fill:#fdf0f0,stroke:#c0392b
  style P fill:#fdf0f0,stroke:#c0392b
  style X fill:#fdf0f0,stroke:#c0392b
    </div>
<p class="kaavio-selitys">Sama kolme asemaa — mutta jokaisessa on vastuu ja liikkumavara.</p>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Mikä kussakin roolissa muuttuu:</h2>
<ul style="margin:0.5em 0 0;">
<li><strong>Uhrista haavoittuva:</strong> ongelma myönnetään, mutta myös se, että jotain on tehtävissä. Pyyntö on konkreettinen: mitä, keneltä, mihin mennessä.</li>
<li><strong>Pelastajasta välittävä:</strong> autetaan pyydettäessä ja pyydetyn verran. Kysymys "mitä tarvitset?" korvaa oletuksen siitä, mitä toinen tarvitsee.</li>
<li><strong>Vainoojasta jämäkkä:</strong> kerrotaan oma raja ja odotus teoista — ei arviota toisen luonteesta. "Tätä minä en tee" on eri asia kuin "sinä olet laiska".</li>
</ul>
</div>
<p>Käytännössä voittajakolmio on tarkistuslista omalle puheenvuorolle, ei toisen korjaamiseen tarkoitettu työkalu. Työpaikalla siirtymä kuuluu siinä, että palaveri lakkaa käsittelemästä sitä kuka mokasi ja alkaa käsitellä sitä mitä kukin tekee seuraavaksi. Läheissuhteessa se kuuluu siinä, että "sinä et koskaan" vaihtuu muotoon "minä tarvitsen". Yhden osapuolen siirtymä riittää yllättävän usein, koska peli vaatii vähintään kaksi pelaajaa — mutta se ei riitä aina, eikä malli tee mitään tilanteelle, jossa toinen käyttää valtaa väärin.</p>
<div class="vaaralatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Testaa oma puheenvuorosi kolmella kysymyksellä. <strong>Onko pyyntö konkreettinen?</strong> "Minulla on rankkaa" kutsuu pelastajaa; "voitko ottaa perjantain raportin" ei. <strong>Autanko pyytämättä?</strong> Jos et tiedä, oletko avuksi, kysy — arvaaminen on pelastajan liike. <strong>Puhunko teosta vai luonteesta?</strong> Raja kohdistuu tekoon ja on siksi neuvoteltavissa; luonnearvio ei ole. Huomaa, että jämäkkä asema tulkitaan usein aluksi vainoojaksi: kun joku lakkaa pelastamasta, häntä syytetään kylmyydestä. Se on merkki kuvion olemassaolosta, ei virheestä.
    </div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Kirjoja</span>
<ul class="lue-lisaa-lista">
<li><cite>TA Today</cite> — Ian Stewart &amp; Vann Joines (1987)</li>
<li><cite>A Game Free Life</cite> — Stephen Karpman (2014)</li>
<li><cite>Your Perfect Right</cite> — Robert Alberti &amp; Michael Emmons (1970)</li>
</ul>
</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://en.wikipedia.org/wiki/Karpman_drama_triangle" target="_blank" rel="noopener">Wikipedia: Karpman drama triangle (englanniksi)</a></li>
</ul>
</div>
</div>""",
     ["draamakolmio", "roolinvaihto", "mahdollistaja", "harmaa-kivi", "blame-game"])


# ────────────────────────── 143 · Kaksoissidos ──────────────────────────
page("kaksoissidos",
     "Kaksoissidos — käsky, jota ei voi totella eikä olla tottelematta",
     "Kaksoissidos (double bind) — mitä se tarkoittaa | Ilmiöitä",
     "Kaksoissidos tarkoittaa kahta vaatimusta, jotka sulkevat toisensa pois — eikä ristiriidasta saa mainita eikä tilanteesta poistua.",
     [("Mitä kaksoissidos tarkoittaa?",
       "Kaksoissidos tarkoittaa tilannetta, jossa ihminen saa kaksi vaatimusta, jotka sulkevat toisensa pois, eikä hän voi tehdä oikein kummallakaan tavalla. Ratkaisevaa on kaksi lisäehtoa: ristiriidasta ei saa huomauttaa, eikä tilanteesta voi poistua. Antropologi Gregory Bateson työryhmineen kuvasi rakenteen vuonna 1956."),
      ("Mitä kaksoissidokselle voi tehdä?",
       "Ainoa ulospääsy on rikkoa se ehto, joka kieltää ristiriidan mainitsemisen. Käytännössä se tarkoittaa ristiriidan kirjaamista näkyviin sellaisena kuin se on: molemmat ohjeet rinnakkain, kirjallisesti, ja kysymys siitä kumpi on voimassa. Ristiriidan nimeäminen siirtää ongelman takaisin sille, joka on sen luonut."),
      ],
     r"""
<p><strong>Kaksoissidos</strong> (engl. <em>double bind</em>) tarkoittaa tilannetta, jossa ihminen saa kaksi vaatimusta, jotka sulkevat toisensa pois: kumpaa tahansa hän noudattaa, hän rikkoo toista. Antropologi Gregory Bateson kuvasi rakenteen työryhmänsä kanssa vuonna 1956. Ratkaisevaa ei ole itse ristiriita vaan kaksi lisäehtoa: <strong>ristiriidasta ei saa huomauttaa</strong> eikä <strong>tilanteesta voi poistua</strong>.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Mitä kaksoissidos tarkoittaa suomeksi?</h2>
<p style="margin:0.4em 0 0;"><strong>Kaksoissidos</strong> on vakiintunut suomennos englannin termistä <em>double bind</em>. Käsite on peräisin Batesonin, Don Jacksonin, Jay Haleyn ja John Weaklandin artikkelista <cite>Toward a Theory of Schizophrenia</cite> (1956). Artikkelin alkuperäinen väite skitsofrenian syystä ei ole saanut tukea myöhemmässä tutkimuksessa, mutta itse viestinnän kuvauksena käsite on jäänyt käyttöön.</p>
</div>
<div class="mermaid">
flowchart TD
  A["Ohje 1: 'ole oma-aloitteinen'"] --&gt; R["Ristiriita"]
  B["Ohje 2: 'älä tee mitään kysymättä'"] --&gt; R
  R --&gt; K["Ristiriitaa ei saa mainita:\nvalitus on asenneongelma"]
  K --&gt; P["Tilanteesta ei voi poistua:\ntyö, perhe, riippuvuus"]
  P --&gt; S["Syy siirtyy tekijään:\n'hän ei vain osaa'"]
  style K fill:#fdf0f0,stroke:#c0392b
  style P fill:#fdf0f0,stroke:#c0392b
    </div>
<p class="kaavio-selitys">Ilman mainitsemiskieltoa kyse olisi vain huonosta ohjeesta.</p>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Neljä ehtoa, joiden on täytyttävä:</h2>
<ul style="margin:0.5em 0 0;">
<li><strong>Kaksi tasoa:</strong> sanottu ja sanaton ohje ovat ristiriidassa — "sano rehellinen mielipiteesi", mutta rehellisyys muistetaan kehityskeskustelussa.</li>
<li><strong>Mainitsemiskielto:</strong> ristiriidan osoittaminen tulkitaan hankaluudeksi, asenteeksi tai luottamuspulaksi.</li>
<li><strong>Ei ulospääsyä:</strong> suhde on sellainen, jota ei voi jättää kesken — työsuhde, perhe, hoitosuhde.</li>
<li><strong>Toisto:</strong> asetelma ei ole yksittäinen sekaannus vaan tapa, jolla asiat hoidetaan.</li>
</ul>
</div>
<p>Työelämän tavallisin muoto on vastuu ilman valtuuksia: sinä vastaat lopputuloksesta, mutta jokainen päätös on hyväksytettävä. Kun projekti myöhästyy, syy kirjataan sinun nimiisi — et ollut riittävän oma-aloitteinen. Läheissuhteessa muoto on usein tunnepuolella: "älä ole noin varautunut" ja samalla jokainen avautuminen palautuu myöhemmin aseena. Kaksoissidos muistuttaa <a href="catch-22.html">catch-22:ta</a>, mutta ne eivät ole sama asia: catch-22 on sääntö, joka kumoaa itsensä, ja <a href="kafka-ilmio.html">Kafka-ilmiössä</a> vastuuta ei löydy mistään. Kaksoissidoksessa toinen osapuoli on tiedossa ja läsnä — kielletty on vain ristiriidan nimeäminen.</p>
<div class="vaaralatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Tunnusmerkki on tunne siitä, että <strong>häviät kummallakin vaihtoehdolla</strong>, ja että asian esiin ottaminen tuntuu riskiltä. Vastakeino on rikkoa juuri sitä ehtoa, joka kieltää mainitsemisen: kirjaa molemmat ohjeet rinnakkain näkyviin — sähköpostilla, samaan viestiin, neutraalisti — ja kysy kumpi on voimassa. Pyydä vastaus kirjallisena. Tämä ei ole niuhotusta: se siirtää ristiriidan takaisin sille, joka on sen luonut, ja tekee siitä yhteisen ongelman ratkaistavaksi. Jos vastausta ei tule tai kysymys itsessään tulkitaan hyökkäykseksi, olet saanut tärkeimmän tiedon — ristiriita on tarkoituksellinen tai ainakin hyväksytty.
    </div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Kirjoja</span>
<ul class="lue-lisaa-lista">
<li><cite>Steps to an Ecology of Mind</cite> — Gregory Bateson (1972)</li>
<li><cite>Pragmatics of Human Communication</cite> — Watzlawick, Beavin &amp; Jackson (1967)</li>
<li><cite>Catch-22</cite> — Joseph Heller (1961)</li>
</ul>
</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://en.wikipedia.org/wiki/Double_bind" target="_blank" rel="noopener">Wikipedia: Double bind (englanniksi)</a></li>
</ul>
</div>
</div>""",
     ["catch-22", "kafka-ilmio", "gaslighting", "draamakolmio", "harmaa-kivi"])


# ────────────────────────── 144 · Mahdollistaja ──────────────────────────
page("mahdollistaja",
     "Mahdollistaja — apu, joka pitää ongelman käynnissä",
     "Mahdollistaja (enabler) — mitä se tarkoittaa | Ilmiöitä",
     "Mahdollistaja paikkaa toisen jäljet, jolloin seuraukset eivät koskaan osu siihen joka ne aiheuttaa. Näin mekanismi toimii tiimissä ja perheessä.",
     [("Mitä mahdollistaja tarkoittaa?",
       "Mahdollistaja on ihminen, joka ottaa kantaakseen ne seuraukset, jotka kuuluisivat toiselle: paikkaa virheet, keksii selitykset ja tekee tekemättä jääneet työt. Aikomus on lähes aina hyvä, mutta lopputulos on se, ettei ongelma näy missään — eikä siksi muutu."),
      ("Miten mahdollistajan roolista pääsee pois?",
       "Ei kieltäytymällä auttamasta kokonaan, vaan lopettamalla seurausten siirtämisen. Käytännössä se tarkoittaa, että työ tai virhe jää näkyviin sen nimiin jolle se kuuluu. Muutos tuntuu ensin kovuudelta ja aiheuttaa usein syytöksiä, koska se poistaa muilta hyödyn, johon on totuttu."),
      ],
     r"""
<p><strong>Mahdollistaja</strong> (engl. <em>enabler</em>) on ihminen, joka ottaa kantaakseen ne seuraukset, jotka kuuluisivat toiselle. Hän paikkaa virheet, keksii selitykset, soittaa poissaolot ja tekee tekemättä jääneet työt. Aikomus on lähes aina hyvä. Lopputulos on silti se, että ongelma ei näy missään — ja asia, joka ei näy, ei myöskään muutu.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Mitä mahdollistaja tarkoittaa suomeksi?</h2>
<p style="margin:0.4em 0 0;"><strong>Mahdollistaja</strong> on vakiintunut suomennos englannin sanasta <em>enabler</em>. Käsite tulee päihderiippuvuuden ja perheterapian kirjallisuudesta 1980-luvulta, ja se vastaa <a href="draamakolmio.html">draamakolmion</a> pelastajan asemaa. Nykyisessä päihdehoidossa sanaa käytetään varovasti, koska se kääntyy helposti syytökseksi läheistä kohtaan — mekanismi on rakenteellinen, ei luonnevika.</p>
</div>
<div class="mermaid">
flowchart TD
  O["Ongelma: myöhästely,\nvirheet, tekemättä jättäminen"] --&gt; S["Seuraus lankeaisi\ntekijälle"]
  S --&gt; M["Mahdollistaja\npaikkaa jäljet"]
  M --&gt; N["Seuraus ei näy:\nei mittarissa, ei palautteessa"]
  N --&gt; E["Ei syytä muuttaa\nmitään"]
  E --&gt; O
  style M fill:#fff3cd,stroke:#f39c12
  style N fill:#fdf0f0,stroke:#c0392b
    </div>
<p class="kaavio-selitys">Palaute ei katkea siksi että se puuttuu, vaan siksi että joku ottaa sen vastaan toisen puolesta.</p>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Miksi rooli pysyy:</h2>
<ul style="margin:0.5em 0 0;">
<li><strong>Se palkitaan heti:</strong> paikkaaminen lopettaa ahdistavan tilanteen tänään; hinta lankeaa vasta kuukausien päästä.</li>
<li><strong>Se tuottaa aseman:</strong> mahdollistajasta tulee korvaamaton — ja korvaamattomuus tuntuu arvostukselta.</li>
<li><strong>Vaihtoehto näyttää julmalta:</strong> seurausten antaminen tapahtua tulkitaan välinpitämättömyydeksi, myös omissa silmissä.</li>
<li><strong>Muut hyötyvät:</strong> kun joku hoitaa asian, kenenkään muun ei tarvitse ottaa sitä puheeksi.</li>
</ul>
</div>
<p>Tiimissä mahdollistaja on se, joka korjaa toisen koodin öisin, siivoaa esityksen ennen kokousta ja vastaa asiakkaalle kun kollega ei vastannut. Kukaan ei näe alisuoriutumista, koska se ei koskaan ehdi näkyä. Johto katsoo mittareita, ja mittarit ovat kunnossa. Perheessä sama rakenne kantaa juomista, rahankäyttöä tai väkivaltaa: ulospäin kaikki on hallinnassa, koska yksi ihminen käyttää kaiken aikansa siihen, että se näyttäisi siltä. Kun mahdollistaja lopulta väsyy, seuraa tyypillisesti <a href="roolinvaihto.html">roolinvaihto</a> — pitkä lista tehdyistä palveluksista, joita ei koskaan sovittu.</p>
<div class="vaaralatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Testikysymys on yksinkertainen: <strong>kenelle seuraus lankeaa, jos et tee mitään?</strong> Jos vastaus on "minulle", olet ottanut kannettavaksesi jotain, mikä ei ole sinun. Vastakeino ei ole auttamisen lopettaminen vaan seurausten palauttaminen: tee oma työsi, älä toisen, ja anna tekemättä jääneen näkyä sen nimissä jolle se kuuluu. Kirjaa mitä teet toisen puolesta — kahden viikon lista riittää yleensä yllättämään. Varaudu siihen, että muutos tulkitaan ensin kylmyydeksi: se ei ole merkki virheestä vaan siitä, että joku menetti hyödyn, johon oli tottunut. Hätätilanteessa autetaan — mutta hätätila, joka toistuu joka kuukausi, on järjestely.
    </div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Kirjoja</span>
<ul class="lue-lisaa-lista">
<li><cite>Codependent No More</cite> — Melody Beattie (1986)</li>
<li><cite>Another Chance</cite> — Sharon Wegscheider-Cruse (1981)</li>
<li><cite>Games People Play</cite> — Eric Berne (1964)</li>
</ul>
</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://en.wikipedia.org/wiki/Enabling" target="_blank" rel="noopener">Wikipedia: Enabling (englanniksi)</a></li>
</ul>
</div>
</div>""",
     ["draamakolmio", "roolinvaihto", "syntipukki", "voittajakolmio", "strateginen-osaamattomuus"])


# ────────────────────────── 145 · Syntipukki-rooli ──────────────────────────
page("syntipukki",
     "Syntipukki-rooli — ryhmän nimetty kantaja",
     "Syntipukki-rooli — miksi ryhmä tarvitsee yhden | Ilmiöitä",
     "Syntipukki ei ole se joka mokasi vaan se jonka nimiin moka kirjataan. Rooli on rakenteellinen: kun kantaja lähtee, tilalle valitaan uusi.",
     [("Mitä syntipukki-rooli tarkoittaa?",
       "Syntipukki on ryhmän jäsen, jonka nimiin ongelmat kirjataan riippumatta siitä, kuka ne aiheutti. Kyse ei ole yksittäisestä syytöksestä vaan pysyvästä asemasta: ryhmä säilyttää yhtenäisyytensä sillä, että syy on aina samalla ihmisellä. Rooli tunnetaan sekä perhetutkimuksessa että työyhteisöjen dynamiikassa."),
      ("Mistä tietää, että kyse on roolista eikä syystä?",
       "Ratkaiseva testi on lähtö. Jos syntipukki lähtee ja ongelmat loppuvat, syy oli hänessä. Jos ongelmat jatkuvat ja tilalle nimetään muutamassa kuukaudessa uusi kantaja, kyse oli rakenteesta — ja se rakenne jäi paikalleen."),
      ],
     r"""
<p><strong>Syntipukki</strong> (engl. <em>scapegoat</em>) ei ole ryhmässä se, joka mokasi, vaan se, jonka nimiin mokat kirjataan. Kyse ei ole yksittäisestä syytöksestä vaan pysyvästä asemasta. Ryhmä saa siitä jotain arvokasta: niin kauan kuin syy on yhdellä ihmisellä, kenenkään muun ei tarvitse tarkastella omaa osuuttaan eikä ryhmän toimintatapoja.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Mitä syntipukki tarkoittaa suomeksi?</h2>
<p style="margin:0.4em 0 0;"><strong>Syntipukki</strong> on vakiintunut suomen sana, englanniksi <em>scapegoat</em>; ilmiöstä puhutaan myös nimellä <em>scapegoating</em>. Perhetutkimuksessa samasta asemasta käytetään nimitystä <em>identified patient</em> — perheenjäsen, jonka oireet selittävät koko perheen ongelmat. Ero <a href="blame-game.html">syyllisen etsintään</a> on pysyvyys: syyllisen etsintä koskee yhtä tapahtumaa, syntipukki on rooli.</p>
</div>
<div class="mermaid">
flowchart TD
  J["Ryhmässä jännite:\nkiire, virheet, huono johto"] --&gt; N["Nimetään kantaja"]
  N --&gt; Y["Yhtenäisyys palaa:\nsyy on löytynyt"]
  Y --&gt; T["Toimintatavat\npysyvät ennallaan"]
  T --&gt; J
  N --&gt; L["Kantaja lähtee"]
  L --&gt; U["Uusi kantaja\nnimetään"]
  style N fill:#fdf0f0,stroke:#c0392b
  style U fill:#fdf0f0,stroke:#c0392b
    </div>
<p class="kaavio-selitys">Seuraajan ilmestyminen on todiste siitä, että kyse oli asemasta eikä ihmisestä.</p>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Kolme tunnusmerkkiä:</h2>
<ul style="margin:0.5em 0 0;">
<li><strong>Syy löytyy ennen selvitystä:</strong> nimi mainitaan jo silloin, kun kukaan ei vielä tiedä mitä tapahtui.</li>
<li><strong>Sama teko arvioidaan eri tavoin:</strong> muilta se on kiireestä johtuva lipsahdus, häneltä osoitus luonteesta — sama vinouma kuin <a href="halo-efekti.html">halo-efektissä</a> käänteisenä.</li>
<li><strong>Puolustautuminen todistaa syyllisyyden:</strong> vastaanväittäminen tulkitaan hankaluudeksi ja vahvistaa roolin.</li>
</ul>
</div>
<p>Perheessä rooli lankeaa usein sille lapselle, joka sanoo ääneen sen mistä muut vaikenevat. Työpaikalla se osuu tyypillisesti uusimmalle, eri tavalla ajattelevalle tai sille, jolla on vähiten liittolaisia. Rooli on rakenteellisesti hyödyllinen ryhmälle, ja siksi se harvoin katoaa itsestään. Kantajalle lasku on kuitenkin epäsymmetrinen: hän maksaa maineessa, terveydessä ja urassa siitä, että muut välttyvät epämukavalta keskustelulta. Juuri tämä epäsymmetria tekee <a href="valirikko.html">irtautumisesta</a> usein ainoan siirron, joka muuttaa jotain — ja samalla se paljastaa rakenteen, koska tilalle nimetään seuraava.</p>
<div class="vaaralatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Erota <strong>palaute ja rooli</strong>. Palaute koskee tekoa, on ajallisesti rajattu ja kertoo mitä pitäisi tehdä toisin; rooli koskee sinua, laajenee kaikkeen eikä sisällä tietä ulos. Jos tunnistat roolin, kirjaa tosiasiat sitä mukaa kun ne tapahtuvat — päivämäärät, päätökset, kuka pyysi mitäkin — koska jälkikäteen kertomus on jo kirjoitettu. Älä ota vastaan kollektiivisia syytöksiä, vaan pyydä yksilöity tapaus: "mikä konkreettinen asia, milloin". Ryhmän sisällä roolia voi purkaa vain joku, jolla on asemaa: se tarkoittaa kysymystä siitä, mitä muuta tapahtui kuin yhden ihmisen virhe. Jos rooli ei murru, lähtemisen arviointi ei ole antautumista vaan kustannuslaskentaa.
    </div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Kirjoja</span>
<ul class="lue-lisaa-lista">
<li><cite>Violence and the Sacred</cite> — René Girard (1972)</li>
<li><cite>Families and Family Therapy</cite> — Salvador Minuchin (1974)</li>
<li><cite>The Neurotic Organization</cite> — Kets de Vries &amp; Miller (1984)</li>
</ul>
</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://en.wikipedia.org/wiki/Scapegoating" target="_blank" rel="noopener">Wikipedia: Scapegoating (englanniksi)</a></li>
</ul>
</div>
</div>""",
     ["blame-game", "draamakolmio", "mahdollistaja", "valirikko", "hajota-hallitse"])


# ────────────────────────── 146 · Välirikko ──────────────────────────
page("valirikko",
     "Välirikko — kenelle lasku lankeaa, kun suhde katkeaa",
     "Välirikko — miksi lähtijä ja jäävä maksavat eri hinnan | Ilmiöitä",
     "Välirikko katkaisee suhteen kokonaan. Lasku on epäsymmetrinen: lähtijä maksaa siirtymän kerran, jäävä menettää jotain jota ei saa korvattua.",
     [("Mitä välirikko tarkoittaa?",
       "Välirikko tarkoittaa suhteen katkaisemista kokonaan tai lähes kokonaan: yhteydenpito loppuu eikä sitä ole tarkoitus jatkaa. Kyse ei ole riidasta vaan riidan lopettamisesta poistumalla. Sama rakenne toistuu sukulaissuhteissa ja työyhteisöissä, joissa kuormaa kantanut osapuoli lopulta lähtee."),
      ("Miksi välirikossa lähtijä pärjää usein paremmin?",
       "Koska kustannukset ovat erilaiset. Lähtijä maksaa siirtymän kerran: surun, järjestelyt ja menetetyt verkostot. Jäävä menettää jatkuvan hyödyn — tehdyn työn, tuen tai aseman — jota on vaikea korvata, koska se oli sidottu juuri siihen ihmiseen. Tämä ei tee lähtemisestä ilmaista eikä aina oikeaa, mutta selittää miksi lopputulos harvoin on symmetrinen."),
      ],
     r"""
<p><strong>Välirikko</strong> (engl. <em>estrangement</em>) tarkoittaa suhteen katkaisemista kokonaan tai lähes kokonaan: yhteydenpito loppuu eikä sitä ole tarkoitus jatkaa. Kyse ei ole riidasta vaan riidan lopettamisesta poistumalla. Ilmiö on yleisempi kuin siitä puhutaan: Karl Pillemerin yhdysvaltalaisaineistossa (2020) 27&nbsp;% aikuisista kertoi olevansa välirikossa jonkun sukulaisensa kanssa. Suomesta vastaavaa lukua ei ole.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Mitä välirikko tarkoittaa suomeksi?</h2>
<p style="margin:0.4em 0 0;"><strong>Välirikko</strong> on vakiintunut suomen sana; englanniksi puhutaan <em>family estrangementista</em> tai <em>cutoffista</em>. Perhetutkimuksessa erotetaan <strong>fyysinen etäisyys</strong> (yhteydenpito loppuu) ja <strong>tunne-etäisyys</strong> (yhteys jatkuu, mutta merkitys on kadonnut). Työelämän vastine ei ole irtisanoutuminen sinänsä vaan se, että lähtevä katkaisee myös suhteet, joita ei olisi pakko katkaista.</p>
</div>
<div class="mermaid">
flowchart TD
  S["Suhde, jossa toinen kantaa\nja toinen hyötyy"] --&gt; L["Kantava osapuoli lähtee"]
  L --&gt; A["Lähtijä: kustannus\nkerran — siirtymä, suru"]
  L --&gt; B["Jäävä: menetys jatkuu —\nhyöty oli henkilösidonnainen"]
  A --&gt; C["Kustannukset lakkaavat"]
  B --&gt; D["Korvaaminen maksaa\ntai jää tekemättä"]
  style A fill:#fff3cd,stroke:#f39c12
  style B fill:#fdf0f0,stroke:#c0392b
    </div>
<p class="kaavio-selitys">Epäsymmetria ei ole moraalinen tuomio vaan kustannusten ajoitus.</p>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Miksi lasku jakautuu epätasaisesti:</h2>
<ul style="margin:0.5em 0 0;">
<li><strong>Hyöty on henkilösidonnainen:</strong> juuri tämän ihmisen työpanos, tuki, sovittelu tai asema — sitä ei saa vaihtamalla ketä tahansa tilalle.</li>
<li><strong>Kustannus on yleinen:</strong> aika, uskottavuus ja terveys ovat samoja kaikkialla, ja ne lakkaavat kulumasta heti kun suhde päättyy.</li>
<li><strong>Ajoitus eroaa:</strong> lähtijän lasku on etupainotteinen ja kertaluonteinen, jäävän juokseva.</li>
<li><strong>Kuvio vaatii kaksi:</strong> <a href="draamakolmio.html">draamakolmio</a> ei pyöri yhdellä pelaajalla, joten poistuminen lopettaa sen ilman että kukaan suostuu mihinkään.</li>
</ul>
</div>
<p>Työelämässä sama näkyy siinä, kuka lähtee ensin. Kuormaa kantanut asiantuntija vie mukanaan tiedon, jota ei ollut kirjattu mihinkään, ja tiimin todellinen tila tulee näkyviin vasta hänen lähdettyään — siihen asti sen peitti yksi ihminen, joka teki liikaa. Sama rakenne kuin <a href="mahdollistaja.html">mahdollistajassa</a>: ongelma ei näkynyt, koska joku otti seuraukset vastaan toisen puolesta. Lähtijän kannalta tämä ei ole voitto siinä mielessä, että se tuntuisi hyvältä: menetettyjä ovat myös suhteet kolmansiin, perinnöt, suosittelijat ja yhteiset lapset. Hinta on kuitenkin määrä, joka maksetaan — ei summa, joka jatkaa juoksemistaan.</p>
<div class="vaaralatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Kysy kolme asiaa ennen kuin päätät mitään. <strong>Mikä muuttuisi, jos toinen muuttuisi?</strong> Jos et osaa nimetä konkreettista tekoa, jota pyydät, pyyntöä ei ole vielä esitetty — ja silloin sitä kannattaa kokeilla ensin. <strong>Mitä olet jo yrittänyt ja miten siihen vastattiin?</strong> Yritysten lista on tärkein tieto: toistuva vastaamatta jättäminen on vastaus. <strong>Mitkä kustannukset lakkaavat ja mitkä alkavat?</strong> Kirjaa molemmat, myös ne joita ei mielellään laskisi. Välirikko ei ole ainoa vaihtoehto: <a href="no-contact.html">täydellisen katkaisun</a> ja nykytilan väliin mahtuu rajattu yhteydenpito, ja silloin kun lähteminen ei ole mahdollista, jäljelle jää <a href="harmaa-kivi.html">harmaa kivi</a>. Vältä tekemästä päätöstä yhden riidan päivänä: rakenteellinen ongelma näkyy kuukausissa, ei yhdessä illassa.
    </div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Kirjoja</span>
<ul class="lue-lisaa-lista">
<li><cite>Fault Lines</cite> — Karl Pillemer (2020)</li>
<li><cite>Family Estrangement: A Matter of Perspective</cite> — Kylie Agllias (2016)</li>
<li><cite>Rules of Estrangement</cite> — Joshua Coleman (2021)</li>
</ul>
</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://en.wikipedia.org/wiki/Family_estrangement" target="_blank" rel="noopener">Wikipedia: Family estrangement (englanniksi)</a></li>
</ul>
</div>
</div>""",
     ["no-contact", "harmaa-kivi", "syntipukki", "draamakolmio", "hiljainen-irtisanominen"])


# ────────────────────────── 147 · No contact ──────────────────────────
page("no-contact",
     "No contact — katkaisu, joka poistaa toisen pelaajan",
     "No contact — mitä täydellinen katkaisu tarkoittaa | Ilmiöitä",
     "No contact tarkoittaa yhteydenpidon lopettamista kokonaan, myös satunnaisten viestien. Osittainen katkaisu vahvistaa kuviota enemmän kuin jatkuva.",
     [("Mitä no contact tarkoittaa?",
       "No contact tarkoittaa yhteydenpidon lopettamista kokonaan: ei viestejä, ei puheluita, ei seuraamista sosiaalisessa mediassa eikä terveisiä kolmansien kautta. Termi on peräisin vertaistukikirjallisuudesta, ei kliinisestä tutkimuksesta, ja sillä tarkoitetaan rajanvetoa — ei rangaistusta."),
      ("Miksi satunnainen yhteydenpito ei toimi?",
       "Koska satunnainen palkkio vahvistaa käyttäytymistä tehokkaammin kuin säännöllinen. Jos yhdeksän yhteydenottoa jätetään huomiotta ja kymmenenteen vastataan, opittu läksy on että yrittämistä kannattaa jatkaa. Siksi puolittainen katkaisu pitää kuviota yllä pidempään kuin joko täysi yhteydenpito tai täysi katkaisu."),
      ],
     r"""
<p><strong>No contact</strong> tarkoittaa yhteydenpidon lopettamista kokonaan: ei viestejä, ei puheluita, ei seuraamista sosiaalisessa mediassa eikä terveisiä kolmansien kautta. Termi on peräisin vertaistukikirjallisuudesta, ei kliinisestä tutkimuksesta. Se on <a href="valirikko.html">välirikon</a> toteutustapa, ja sen ainoa tarkoitus on poistaa kuviosta toinen pelaaja — ei rangaista ketään.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Mitä no contact tarkoittaa suomeksi?</h2>
<p style="margin:0.4em 0 0;">Vakiintunutta suomennosta ei ole, joten termi esiintyy suomeksikin muodossa <strong>no contact</strong>; joskus käytetään sanaa <em>nollakontakti</em>. Läheinen käsite on <em>low contact</em> eli rajattu yhteydenpito, jossa tavataan ennalta sovituissa tilanteissa ja sovitun ajan. Erona <a href="hiljainen-irtisanominen.html">hiljaiseen vetäytymiseen</a> on se, että no contact on lausuttu päätös, ei hitaasti haipuva yhteys.</p>
</div>
<div class="mermaid">
flowchart TD
  Y["Yhteydenottoyritys"] --&gt; E{"Vastataanko?"}
  E --&gt;|"Joskus"| S["Satunnainen palkkio:\nyrittämistä kannattaa jatkaa"]
  S --&gt; Y
  E --&gt;|"Ei koskaan"| P["Piikki ensin:\nyritykset lisääntyvät"]
  P --&gt; L["Sitten laantuvat:\nkuvio menettää tehtävänsä"]
  style S fill:#fdf0f0,stroke:#c0392b
  style P fill:#fff3cd,stroke:#f39c12
    </div>
<p class="kaavio-selitys">Puolittainen katkaisu on tehokkain tapa pitää kuvio hengissä.</p>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Kolme asiaa, jotka yllättävät:</h2>
<ul style="margin:0.5em 0 0;">
<li><strong>Yritykset lisääntyvät ensin.</strong> Katkaisua seuraa tyypillisesti piikki: anteeksipyyntöjä, lahjoja, hätäviestejä, uusia numeroita. Se on kuvion viimeinen yritys, ei merkki muutoksesta.</li>
<li><strong>Kolmannet osapuolet joutuvat väliin.</strong> Viestit alkavat kulkea sukulaisten ja kollegoiden kautta, jolloin heidän on valittava puoli — myös silloin kun he eivät halua.</li>
<li><strong>Suru tulee erikseen.</strong> Helpotus ja menetys eivät sulje toisiaan pois, ja jälkimmäinen tulee usein vasta kuukausien päästä.</li>
</ul>
</div>
<p>Työelämässä täydellinen katkaisu on mahdollinen vasta jälkikäteen: entiseen työnantajaan, entiseen kollegaan tai entiseen asiakkaaseen. Nykyiseen esimieheen sitä ei voi soveltaa, koska työsuhteessa yhteydenpito on velvollisuus — silloin jäljelle jää <a href="harmaa-kivi.html">harmaa kivi</a> eli yhteydenpidon jatkaminen ilman sitä, mitä toinen siitä hakee. Kannattaa myös erottaa kaksi eri asiaa: no contact on rajanveto, jonka tarkoitus on suojata, kun taas hiljaisuus <em>rangaistuksena</em> on osa samaa kuviota, josta yritetään ulos. Jälkimmäinen tunnetaan nimellä <em>silent treatment</em>, ja sen tunnistaa siitä, että yhteys palaa heti kun toinen antaa periksi.</p>
<div class="vaaralatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Jos harkitset katkaisua, tee siitä <strong>päätös etukäteen, ei reaktio kerrallaan</strong>. Kirjoita itsellesi mitä katkaisu koskee (kanavat, kolmannet osapuolet, yhteiset tilaisuudet) ja mikä olisi ehto sen purkamiselle — ehto teoista, ei lupauksista. Kerro päätös kerran ja lyhyesti, tai älä ollenkaan; perustelu kutsuu neuvottelun, jota et halua käydä. Sovi yhden ihmisen kanssa, joka välittää tarvittaessa aidon hätätiedon, niin et joudu seuraamaan kanavia itse. Varaudu piikkiin ja päätä etukäteen, ettet tulkitse sitä muutokseksi. Jos katkaisuun liittyy uhkailua, omaisuutta, lapsia tai työsuhteen ehtoja, kyse ei ole enää vain ihmissuhteesta — hanki tuki ja kirjaa tapahtumat.
    </div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Kirjoja</span>
<ul class="lue-lisaa-lista">
<li><cite>Adult Children of Emotionally Immature Parents</cite> — Lindsay Gibson (2015)</li>
<li><cite>Fault Lines</cite> — Karl Pillemer (2020)</li>
<li><cite>Why Does He Do That?</cite> — Lundy Bancroft (2002)</li>
</ul>
</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://en.wikipedia.org/wiki/Family_estrangement" target="_blank" rel="noopener">Wikipedia: Family estrangement (englanniksi)</a></li>
</ul>
</div>
</div>""",
     ["valirikko", "harmaa-kivi", "gaslighting", "draamakolmio", "syntipukki"])


# ────────────────────────── 148 · Harmaa kivi ──────────────────────────
page("harmaa-kivi",
     "Harmaa kivi — kun lähteminen ei ole vaihtoehto",
     "Harmaa kivi (grey rock) — menetelmä suomeksi | Ilmiöitä",
     "Harmaa kivi tarkoittaa tylsäksi tulemista: reaktio on palkkio, ja ilman palkkiota kuvio menettää tarkoituksensa. Keino tilanteisiin joista ei voi lähteä.",
     [("Mitä harmaa kivi tarkoittaa?",
       "Harmaa kivi on menetelmä, jossa vuorovaikutuksesta poistetaan se, mitä toinen siitä hakee: tunnereaktio, uusi tieto ja pitkä keskustelu. Vastaukset ovat lyhyitä, asiallisia ja tylsiä. Menetelmä on tarkoitettu tilanteisiin, joista ei voi poistua — työsuhteeseen, yhteishuoltajuuteen tai pakollisiin sukutapaamisiin."),
      ("Toimiiko harmaa kivi?",
       "Se vähentää yleensä kontaktien määrää, koska käyttäytyminen menettää tehtävänsä ilman reaktiota. Se ei kuitenkaan korjaa suhdetta eikä sovi tilanteeseen, jossa yhteistyötä oikeasti tarvitaan. Ensimmäinen vaihe on usein kiihtyminen: kun reaktio jää saamatta, sitä haetaan voimakkaammin ennen kuin yritykset vähenevät."),
      ],
     r"""
<p><strong>Harmaa kivi</strong> (engl. <em>grey rock</em> tai <em>gray rock method</em>) tarkoittaa tylsäksi tulemista tarkoituksella. Vuorovaikutuksesta poistetaan se, mitä toinen siitä hakee: tunnereaktio, uusi tieto ja pitkä keskustelu. Ajatus on yksinkertainen — reaktio on palkkio, ja ilman palkkiota käyttäytyminen menettää tehtävänsä. Menetelmä on tarkoitettu tilanteisiin, joista ei voi poistua.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Mitä harmaa kivi tarkoittaa suomeksi?</h2>
<p style="margin:0.4em 0 0;">Termi on suora käännös englannin ilmauksesta <em>grey rock</em>: ole kuin harmaa kivi, jota kukaan ei poimi rannalta. Nimitys on peräisin vertaistukikirjoittelusta 2010-luvun alusta eikä ole kliininen käsite. Se on <a href="no-contact.html">no contactin</a> vastine silloin, kun katkaisu ei ole mahdollinen — yhteishuoltajuudessa, työsuhteessa tai pakollisissa sukutapaamisissa.</p>
</div>
<div class="mermaid">
flowchart TD
  P["Provokaatio, syytös\ntai koukku"] --&gt; R{"Saako reaktion?"}
  R --&gt;|"Kyllä"| T["Keskustelu jatkuu:\nkuvio sai tehtävänsä"]
  T --&gt; P
  R --&gt;|"Ei"| K["Kiihtyminen:\nkovempi yritys"]
  K --&gt; V["Yritykset vähenevät —\nei palkkiota"]
  style T fill:#fdf0f0,stroke:#c0392b
  style K fill:#fff3cd,stroke:#f39c12
    </div>
<p class="kaavio-selitys">Kiihtymisvaihe tulee ennen laantumista — se ei ole merkki epäonnistumisesta.</p>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Käytännössä kolme sääntöä:</h2>
<ul style="margin:0.5em 0 0;">
<li><strong>Lyhyt ja asiallinen:</strong> vastaa kysymykseen, älä sen ympärille. "Selvä." "En tiedä." "Palaan asiaan huomenna."</li>
<li><strong>Ei uutta tietoa:</strong> älä kerro suunnitelmia, tunteita tai muiden asioita — kaikki kerrottu on myöhemmin käytettävissä.</li>
<li><strong>Ei syöttiin tarttumista:</strong> jätä provokaatio vastaamatta ja vastaa vain siihen osaan, jossa on asia. Väärän tiedon voi korjata kerran, ei kahdesti.</li>
</ul>
</div>
<p>Työpaikalla harmaa kivi tarkoittaa käytännössä siirtymistä kirjalliseen kanavaan: vastaukset sähköpostilla, lyhyesti, faktoihin rajautuen ja niin että jälki jää. Se poistaa samalla <a href="gaslighting.html">gaslightingin</a> toimintaedellytykset, koska muistin sijasta kiistellään tekstistä. Kaksi rajausta on syytä tehdä. Harmaa kivi ei ole hiljainen rankaiseminen eikä <a href="hiljainen-irtisanoutuminen.html">vetäytyminen työstä</a>: työ tehdään, viesteihin vastataan, vain palkkio jää pois. Eikä se ole päämäärä vaan silta — se tekee tilanteesta siedettävän sillä aikaa kun järjestät itsellesi ulospääsyn.</p>
<div class="vaaralatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Menetelmän hinta kannattaa tietää etukäteen: <strong>se on väsyttävää</strong>, koska oman reaktion pidättäminen on työtä, ja pitkään jatkuessaan se turruttaa myös muut suhteet. Siksi kolme ehtoa. Aseta <strong>aikaraja</strong> — kuukausia, ei vuosia — ja päätä mitä sinä sinä aikana järjestät. Pidä <strong>yksi ihminen</strong>, jolle puhut suoraan, ettei tylsyydestä tule ainoa tapasi olla. Ja <strong>kirjaa tapahtumat</strong>, koska hiljaisuus ei todista mitään jälkikäteen. Jos tilanteeseen liittyy uhkaa, työturvallisuutta tai lasten asioita, menetelmä ei riitä: se hallitsee vuorovaikutusta, ei ratkaise valtasuhdetta.
    </div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Kirjoja</span>
<ul class="lue-lisaa-lista">
<li><cite>Why Does He Do That?</cite> — Lundy Bancroft (2002)</li>
<li><cite>In Sheep's Clothing</cite> — George Simon (1996)</li>
<li><cite>Adult Children of Emotionally Immature Parents</cite> — Lindsay Gibson (2015)</li>
</ul>
</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://en.wikipedia.org/wiki/Psychological_manipulation" target="_blank" rel="noopener">Wikipedia: Psychological manipulation (englanniksi)</a></li>
</ul>
</div>
</div>""",
     ["no-contact", "valirikko", "gaslighting", "kaksoissidos", "voittajakolmio"])


def alikansiopolut(html):
    """luonnokset/-kansiosta juureen: ../-etuliitteet.

    lisaa_ilmiot.py:juurisivuksi() purkaa täsmälleen nämä muodot — jos tänne
    lisää uuden polkutyypin, se on lisättävä myös sinne, tai julkaisu kaatuu
    assertiin "../-polku jäi jäljelle".
    """
    for vanha, uusi in [
        ('href="style.css', 'href="../style.css'),
        ('href="fonts/', 'href="../fonts/'),
        ('src="favicon.svg"', 'src="../favicon.svg"'),
        ('href="favicon.svg"', 'href="../favicon.svg"'),
        ("s.src = 'js/mermaid.min.js';", "s.src = '../js/mermaid.min.js';"),
        ("window.location.href = id + '.html';",
         "window.location.href = '../' + id + '.html';"),
        ("naytaSiirtyma('Satunnainen ilmiö', id + '.html');",
         "naytaSiirtyma('Satunnainen ilmiö', '../' + id + '.html');"),
        ('\'<img class="random-siirtyma-logo" src="favicon.svg" alt="">\'',
         '\'<img class="random-siirtyma-logo" src="../favicon.svg" alt="">\''),
    ]:
        html = html.replace(vanha, uusi)

    # kaikki juuren sivut ../-taakse; erän omat sivut ovat samassa kansiossa
    def korjaa(m):
        kohde = m.group(1)
        if kohde[:-5] in OMAT_KORTIT:
            return m.group(0)
        return f'href="../{kohde}"'

    return re.sub(r'href="(?!\.\./)([a-z0-9][a-z0-9.-]*\.html)"', korjaa, html)


def build():
    tpl = TEMPLATE.read_text(encoding="utf-8")
    OUT.mkdir(exist_ok=True)

    ids_match = re.search(r"const IDS = \[(.*?)\];", tpl, re.S)
    julkaistut = [s.strip().strip('"') for s in ids_match.group(1).split(",")]
    assert len(julkaistut) == 139, f"odotettiin 139 id:tä, saatiin {len(julkaistut)}"
    # uudet tulevat listan loppuun samassa järjestyksessä kuin korttinsa
    ids_js = ("const IDS = ["
              + ", ".join(json.dumps(s) for s in julkaistut + [p["slug"] for p in PAGES])
              + "];")

    for i, p in enumerate(PAGES):
        slug, num = p["slug"], p["num"]

        if i == 0:
            prev_href, prev_nimi = f"../{EDELTAJA[0]}.html", EDELTAJA[1]
        else:
            prev_href, prev_nimi = f"{PAGES[i-1]['slug']}.html", PAGES[i - 1]["otsikko"]
        if i < len(PAGES) - 1:
            next_href, next_nimi = f"{PAGES[i+1]['slug']}.html", PAGES[i + 1]["otsikko"]
        else:
            next_href = next_nimi = None

        html = tpl.replace(VANHA_SLUG, slug)
        html = html.replace("kategoria-psykologia-ja-kognitio.html", KAT_SIVU)
        html = html.replace("Psykologia ja kognitio", KAT_NIMI)

        html, n = re.subn(r"  <!-- SEO -->.*?\n</script>",
                          lambda m: seo_lohko(slug, p["otsikko"], p["og_title"],
                                              p["kuvaus"], p["faq"]),
                          html, count=1, flags=re.S)
        assert n == 1, f"{slug}: SEO-lohkoa ei löytynyt"

        uusi_ilmio = (f'<div class="ilmio" id="{slug}">\n'
                      f'<div class="ilmio-tag">Ilmiö {num}</div>\n'
                      f'<h1>{p["otsikko"]}</h1>\n'
                      f'<p class="ilmio-byline">Kirjoittanut <a href="tietoa.html" rel="author">Ilmiömies</a> · Päivitetty {PVM_FI}</p>'
                      f'{p["sisalto"]}</div>')
        html, n = re.subn(rf'<div class="ilmio" id="{slug}">.*?\n</div>\n\n  <aside',
                          lambda m: uusi_ilmio + "\n\n  <aside", html, count=1, flags=re.S)
        assert n == 1, f"{slug}: sisältölohkoa ei löytynyt"

        html, n = re.subn(r'<aside class="liittyvat".*?</aside>',
                          lambda m: liittyvat_html(p["liittyvat"]).strip(),
                          html, count=1, flags=re.S)
        assert n == 1, f"{slug}: liittyvät-lohkoa ei löytynyt"

        html, n = re.subn(r'<nav class="kortti-nav">.*?</nav>',
                          lambda m: nav_html(num, prev_href, prev_nimi,
                                             next_href, next_nimi).strip(),
                          html, count=1, flags=re.S)
        assert n == 1, f"{slug}: navigointia ei löytynyt"

        html, n = re.subn(r"const IDS = \[.*?\];", lambda m: ids_js, html, count=1, flags=re.S)
        assert n == 1, f"{slug}: IDS-listaa ei löytynyt"
        html = html.replace("const PREV = 'backfire-effect.html';",
                            f"const PREV = '{prev_href}';")
        html = html.replace("const NEXT = 'halo-efekti.html';",
                            f"const NEXT = '{next_href or ''}';")

        html = html.replace(
            '<link rel="canonical"',
            '<meta name="robots" content="noindex"><!-- POISTA-JULKAISTAESSA -->\n  <link rel="canonical"')

        html = alikansiopolut(html)

        # sama tarkistus kuin lisaa_ilmiot.py tekee julkaistessa
        for jaannos in ('href="index.html"', 'href="tietoa.html"',
                        f'href="{KAT_SIVU}"', "s.src = 'js/"):
            assert jaannos not in html, f"{slug}: {jaannos} jäi juuripolkuna"

        (OUT / f"{slug}.html").write_text(html, encoding="utf-8")
        sanat = len(re.sub(r"<[^>]+>", " ", p["otsikko"] + p["sisalto"]).split())
        print(f"  {num}  {slug}.html  ({len(html) // 1024} KB, {sanat} sanaa)")

    print(f"\nValmis: {len(PAGES)} luonnosta kansiossa {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    build()
