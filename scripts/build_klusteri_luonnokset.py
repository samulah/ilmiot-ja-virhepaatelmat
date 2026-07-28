#!/usr/bin/env python3
"""Generoi klusteriluonnokset kahdelle GSC-datan kärkisivulle (P2).

Tausta: GSC-AUDIT-2026-07-28.md. Hyvesignalointi (67 näyttöä, sija 10,5) ja
rage bait (86 näyttöä, sija 11,0) jäävät sivun 1 alalaitaan. Kumpikin on
kategoriansa yksinäinen kärki: Pesut ja maineenhallinta -kategoriassa on vain
kolme sivua, ja rage baitin ympäriltä puuttuvat sen lähimekanismit. Sivun
pituusnormi (~260 sanaa) on tietoinen valinta, joten keskussivua ei pidennetä
— sen ympärille rakennetaan klusteri.

Tuottaa 5 luonnosta kansioon luonnokset-klusterit/:
  Pesut ja maineenhallinta   3 → 6:  sinipesu, urheilupesu, pinkkipesu
  Alustatalous ja algoritmit 8 → 10: klikkiotsikko, engagement bait

Numerot 119–123 ovat väliaikaisia: luonnokset-media/ varaa 109–118, ja
julkaisu numeroi koko sivuston uudelleen kategorioittain.

Julkaistaessa: siirrä juureen, poista noindex-rivi, riisu ../-etuliitteet,
lisää hub-kortit index.html:ään ja aja build_liittyvat.py, paivita_maarat.py,
build_sitemap.py, build_search_index.py.

Ajo:  python3 scripts/build_klusteri_luonnokset.py
"""
import glob
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "aanekas-vahemmisto.html"
OUT = ROOT / "luonnokset-klusterit"

PVM_ISO = "2026-07-28"
PVM_FI = "28.7.2026"

VANHA_SLUG = "aanekas-vahemmisto"
VANHA_VARI = "#7b241c"
VANHA_TITLE = "Äänekäs vähemmistö — kommenttiosio ei ole mielipidemittari"
VANHA_DESC = ("Äänekäs vähemmistö vääristää kuvan yleisestä mielipiteestä: kärjekkäimmät "
              "kommentoijat näkyvät eniten, kun hiljainen enemmistö ei koskaan vastaa.")
VANHA_KAT = "Alustatalous ja algoritmit"
VANHA_KAT_SIVU = "kategoria-alustatalous-ja-algoritmit.html"

PESUT = ("Pesut ja maineenhallinta", "kategoria-pesut-ja-maineenhallinta.html")
ALUSTA = (VANHA_KAT, VANHA_KAT_SIVU)

EDELTAJA = ("p-hakkerointi", "P-hakkerointi — testataan kunnes jokin näyttää merkitsevältä")

OMAT_KORTIT = {
    "sinipesu": (119, "#1565c0", "Sinipesu",
        "Vapaaehtoiseen sitoumukseen liittyminen tuottaa vastuullisen maineen ilman valvontaa tai sanktioita."),
    "urheilupesu": (120, "#00838f", "Urheilupesu",
        "Maineongelmasta kärsivä ostaa urheilusta myönteistä huomiota — media siirtyy raportoimaan otteluista."),
    "pinkkipesu": (121, "#d81b60", "Pinkkipesu",
        "Sateenkaari tai pinkki nauha ilmestyy logoon kampanjakuukaudeksi ja katoaa sen päätyttyä."),
    "klikkiotsikko": (122, "#ef6c00", "Klikkiotsikko",
        "Otsikko on rakennettu tuottamaan klikki, ei kertomaan mitä juttu sisältää — tieto pidätetään tahallaan."),
    "engagement-bait": (123, "#5d4037", "Engagement bait",
        "Sisältö pyytää reaktiota suoraan, koska algoritmi palkitsee vuorovaikutuksesta riippumatta sen syystä."),
}


def julkaistut_kortit():
    """Korttitiedot ensisijaisesti index.html:n hub-korteista (yksi totuuden
    lähde, kattaa kaikki 108). Liittyvät-kortit luetaan täydennyksenä, koska
    niissä on sama data — mutta kaikkia ilmiöitä ei linkitetä joka sivulta."""
    kortit = {}
    hub = re.compile(
        r'<a href="([a-z0-9-]+)\.html" class="hub-kortti" style="--c:(#[0-9a-f]+)">\s*'
        r'<span class="hub-numero">(\d+)</span>\s*<span class="hub-teksti">\s*'
        r'<span class="hub-nimi">([^<]*)</span>\s*<span class="hub-kuvaus">([^<]*)</span>')
    for m in hub.finditer((ROOT / "index.html").read_text(encoding="utf-8")):
        kortit[m.group(1)] = (int(m.group(3)), m.group(2), m.group(4), m.group(5))
    kuvio = re.compile(
        r'<a href="([a-z0-9-]+)\.html" class="liittyvat-kortti" style="--c:(#[0-9a-f]+)">\s*'
        r'<span class="liittyvat-numero">(\d+)</span>\s*<span class="liittyvat-teksti">\s*'
        r'<span class="liittyvat-nimi">([^<]*)</span>\s*<span class="liittyvat-kuvaus">([^<]*)</span>')
    for f in glob.glob(str(ROOT / "*.html")):
        for m in kuvio.finditer(Path(f).read_text(encoding="utf-8")):
            kortit.setdefault(m.group(1),
                              (int(m.group(3)), m.group(2), m.group(4), m.group(5)))
    assert len(kortit) >= 108, f"kortteja {len(kortit)}, odotettiin vähintään 108"
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
      <span class="kortti-nav-laskuri">{num} / 123</span>
      <span class="kortti-nav-vinkki">
        <kbd>&#8592;</kbd> <kbd>&#8594;</kbd> selaa &middot; <kbd>R</kbd> satunnainen
        <span class="touch-vinkki">&nbsp;· swipe &#8592;&#8594; tai &#8595; random</span>
      </span>
    </div>
    {nxt}
  </nav>'''


PAGES = []


def page(slug, kategoria, otsikko, kuvaus, sisalto, liittyvat):
    num, vari = OMAT_KORTIT[slug][0], OMAT_KORTIT[slug][1]
    PAGES.append(dict(slug=slug, num=num, vari=vari, kat=kategoria, otsikko=otsikko,
                      kuvaus=kuvaus, sisalto=sisalto, liittyvat=liittyvat))


# ────────────────────────── 119 · Sinipesu ──────────────────────────
page("sinipesu", PESUT,
     "Sinipesu — vastuullisuus ilman valvontaa",
     "Sinipesu (bluewashing) tarkoittaa vastuullisen maineen ostamista liittymällä vapaaehtoiseen sitoumukseen, jolla ei ole mittareita eikä sanktioita.",
     r"""
<p><strong>Sinipesu</strong> (engl. <strong>bluewashing</strong>) tarkoittaa yhteiskuntavastuullisen maineen hankkimista liittymällä vapaaehtoiseen sitoumukseen tai kumppanuuteen, jolla ei ole mitattavia velvoitteita, riippumatonta valvontaa eikä sanktioita. Nimi tulee YK:n sinisestä: uskottavuus lainataan arvovaltaiselta taholta, ei omista teoista.</p>
<p>Termin vakiinnutti Transnational Resource &amp; Action Centerin raportti <cite>Tangled Up In Blue</cite> vuonna 2000, kun YK:n Global Compact -aloite avattiin yrityksille. Aloitteen logiikka on avoin kutsu: osallistuja sitoutuu kymmeneen periaatteeseen ja raportoi edistymisestään itse. Ainoa seuraamus on listalta poistaminen, ja sekin seuraa raportoimatta jättämisestä — ei periaatteiden rikkomisesta.</p>
<div class="mermaid">
flowchart TD
  M["Maine­ongelma tai\nvastuullisuuspaine"] --&gt; L["Liittyminen vapaaehtoiseen\naloitteeseen: halpaa"]
  L --&gt; R["Oma raportti\nedistymisestä"]
  R --&gt; T["Tunnus, logo ja\nmaininta aloitteessa"]
  T --&gt; U["Sidosryhmien\nluottamus kasvaa"]
  U --&gt; E["Toiminta ennallaan —\nei mittaria, ei sanktiota"]
  E --&gt; M
  style L fill:#fdf0f0,stroke:#c0392b
  style U fill:#fff3cd,stroke:#f39c12
    </div>
<p class="kaavio-selitys">Sinipesussa maksetaan jäsenyydestä, ei muutoksesta.</p>
<div class="infolaatikko">
<h2 class="laatikko-otsikko">Mistä sinipesun tunnistaa</h2>
<ul style="margin:0.5em 0 0;">
<li><strong>Sitoumus ilman lukua:</strong> luvataan "kunnioittaa" tai "edistää" — ei kerrota mitä, kuinka paljon ja mihin mennessä.</li>
<li><strong>Oma raportointi:</strong> edistymisen arvioi sama taho, jota arvioidaan.</li>
<li><strong>Sanktio puuttuu:</strong> rikkomisesta ei seuraa mitään, koska mitään ei ole määritelty rikottavaksi.</li>
<li><strong>Logo tekee työn:</strong> tunnus näkyy vuosikertomuksen kannessa, konkretia ei missään.</li>
<li><strong>Kumppanuus korvaa politiikan:</strong> lahjoitus järjestölle esitetään todisteena siitä, ettei ongelmaa ole.</li>
</ul>
</div>
<p>Sinipesu on viherpesun sosiaalinen sisar: sama mekanismi, eri väite. Siinä missä viherpesu koskee ympäristöä, sinipesu koskee ihmisoikeuksia, työoloja ja hyvää hallintoa — alueita, joiden mittaaminen on vaikeampaa ja väitteiden tarkistaminen siksi kalliimpaa. Juuri mittaamisen vaikeus tekee siitä houkuttelevaa.</p>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Kysy sitoumuksesta kolme asiaa. <strong>Onko mittari?</strong> Sitoumus ilman lukua ja määräaikaa on toivomus. <strong>Kuka varmentaa?</strong> Riippumaton auditointi maksaa ja siksi kertoo aikeesta enemmän kuin itse sitoumus. <strong>Mitä seuraa rikkomisesta?</strong> Jos vastaus on "poistaminen listalta raportoimatta jättämisen takia", kyse ei ole valvonnasta vaan kirjanpidosta. Vertaa lisäksi sitoumusta yrityksen lobbaukseen: sitoumus, jonka vastaista sääntelyä sama taho vastustaa, kumoaa itsensä.
    </div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://en.wikipedia.org/wiki/Bluewashing" target="_blank" rel="noopener">Wikipedia: Bluewashing (englanniksi)</a></li>
<li><a href="https://unglobalcompact.org/what-is-gc/mission/principles" target="_blank" rel="noopener">UN Global Compact: kymmenen periaatetta (englanniksi)</a></li>
</ul>
</div>
</div>""",
     ["viherpesu", "hyvesignalointi", "urheilupesu", "tekoalypesu", "astroturf"])

# ────────────────────────── 120 · Urheilupesu ──────────────────────────
page("urheilupesu", PESUT,
     "Urheilupesu — maine ostetaan otteluiden varjolla",
     "Urheilupesu (sportswashing) tarkoittaa myönteisen huomion ostamista urheilun kautta, jotta katse siirtyy pois maine- tai ihmisoikeusongelmasta.",
     r"""
<p><strong>Urheilupesu</strong> (engl. <strong>sportswashing</strong>) tarkoittaa sitä, että valtio, yritys tai yksityishenkilö rahoittaa urheilua saadakseen myönteistä huomiota, joka peittää alleen maine-, ihmisoikeus- tai ympäristöongelman. Kyse ei ole siitä, että urheilu itsessään olisi vilpillistä — vaan siitä, että urheilu tuottaa poikkeuksellisen tehokkaasti tunnesidettä, jota on vaikea kohdistaa kriittisesti rahoittajaan.</p>
<p>Ilmiö on vanha: Berliinin 1936 kisat ja Argentiinan 1978 jalkapallon MM-kisat sotilasjuntan aikana ovat oppikirjaesimerkkejä. Sana <em>sportswashing</em> yleistyi vasta 2010-luvun jälkipuoliskolla, kun öljyvarallisuutta alettiin kanavoida eurooppalaiseen huippu-urheiluun — Qatarin 2022 MM-kisat, Saudi-Arabian valtiollisen rahaston PIF:n ostama Newcastle United (2021) ja LIV Golf (2022), ja lopulta MM-kisojen 2034 myöntäminen Saudi-Arabialle joulukuussa 2024.</p>
<div class="mermaid">
flowchart TD
  O["Maine­ongelma:\nihmisoikeudet, sota, päästöt"] --&gt; I["Investointi urheiluun:\nseura, kisat, sarja"]
  I --&gt; H["Media raportoi\notteluista ja tähdistä"]
  H --&gt; S["Fanien tunneside\nsyntyy seuraan"]
  S --&gt; K["Kritiikki leimataan\nurheilun politisoinniksi"]
  K --&gt; N["Maine normalisoituu"]
  N --&gt; O
  style I fill:#fdf0f0,stroke:#c0392b
  style K fill:#fff3cd,stroke:#f39c12
    </div>
<p class="kaavio-selitys">Urheilupesun teho perustuu huomion siirtymään, ei väitteeseen.</p>
<div class="infolaatikko">
<h2 class="laatikko-otsikko">Miksi juuri urheilu toimii</h2>
<ul style="margin:0.5em 0 0;">
<li><strong>Toistuva näkyvyys:</strong> seura esiintyy mediassa viikoittain vuosikymmeniä — mainoskampanja loppuu, sarjataulukko ei.</li>
<li><strong>Tunneside siirtyy:</strong> fani kiintyy joukkueeseen, ja omistaja tulee kaupan päälle.</li>
<li><strong>Kritiikin hinta:</strong> ongelmasta puhuva toimittaja pilaa juhlan, joten kysymykset siirtyvät urheilusivujen ulkopuolelle.</li>
<li><strong>Valmis puolustus:</strong> "politiikkaa ei pidä sekoittaa urheiluun" kääntää kritiikin esittäjän syylliseksi.</li>
<li><strong>Vertaisvaikutus:</strong> kun yksi liiga ottaa rahan vastaan, muiden on vaikea kieltäytyä.</li>
</ul>
</div>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Erota tapahtuma ja isäntä. Otteluiden seuraaminen ei ole kannanotto, mutta isännän valinta on aina ollut jonkun päätös — ja sen päätöksen perustelut ovat julkista tietoa. <strong>Seuraa rahaa:</strong> onko omistaja yksityinen sijoittaja vai valtiollinen rahasto, ja mitä samalla rahalla tehdään muualla? <strong>Huomaa retoriikka:</strong> kun kritiikki torjutaan "politisoinnin" leimalla, kyse on aiheen sulkemisesta, ei vastaväitteestä. <strong>Katso ajoitusta:</strong> suurhankinnat osuvat usein juuri raportin, oikeudenkäynnin tai kansainvälisen huomion kanssa samaan hetkeen.
    </div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://en.wikipedia.org/wiki/Sportswashing" target="_blank" rel="noopener">Wikipedia: Sportswashing (englanniksi)</a></li>
<li><a href="https://www.amnesty.org/en/latest/news/2024/11/saudi-arabia-2034-world-cup-bid-evaluation-an-astonishing-whitewash/" target="_blank" rel="noopener">Amnesty International: 2034 World Cup bid evaluation (englanniksi)</a></li>
</ul>
</div>
</div>""",
     ["viherpesu", "sinipesu", "hyvesignalointi", "halo-efekti", "valta-suojelee-valtaa"])

# ────────────────────────── 121 · Pinkkipesu ──────────────────────────
page("pinkkipesu", PESUT,
     "Pinkkipesu — sateenkaari kampanjakuukaudeksi",
     "Pinkkipesu (pinkwashing) tarkoittaa vähemmistön tai hyväntekeväisyyden symbolin käyttöä markkinoinnissa ilman että tuki näkyy rahassa tai politiikassa.",
     r"""
<p><strong>Pinkkipesu</strong> (engl. <strong>pinkwashing</strong>) tarkoittaa sitä, että organisaatio ottaa käyttöön vähemmistön tai hyväntekeväisyyden symbolin — sateenkaaren, pinkin nauhan — ilman että sen takana on rahaa, politiikkaa tai pysyvyyttä. Symboli on ilmainen, tuki maksaa.</p>
<p>Sanalla on kaksi juurta. Vanhempi liittyy rintasyöväntorjuntaan: Breast Cancer Action käynnisti vuonna 2002 <cite>Think Before You Pink</cite> -kampanjan, koska pinkkiä nauhaa käytettiin tuotteissa, joiden tuotosta hyväntekeväisyyteen meni murto-osa tai ei mitään. Nuorempi merkitys syntyi 2010-luvulla seksuaali- ja sukupuolivähemmistöjen ympärillä, ja sitä käytetään sekä yritysmarkkinoinnista että valtioiden maakuvatyöstä.</p>
<div class="mermaid">
flowchart TD
  K["Kampanjakuukausi\nalkaa"] --&gt; L["Logo vaihtuu\nsateenkaareksi"]
  L --&gt; N["Näkyvyys ja\nmyönteinen huomio"]
  N --&gt; P["Kuukausi päättyy:\nlogo palaa"]
  P --&gt; T["Työehdot, lahjoitukset\nja lobbaus ennallaan"]
  T --&gt; K
  style L fill:#fdf0f0,stroke:#c0392b
  style N fill:#fff3cd,stroke:#f39c12
    </div>
<p class="kaavio-selitys">Tuki, joka alkaa ja päättyy kalenterin mukaan, on viestintää.</p>
<div class="infolaatikko">
<h2 class="laatikko-otsikko">Neljä tarkistuskysymystä</h2>
<ul style="margin:0.5em 0 0;">
<li><strong>Kestääkö se yli kuukauden?</strong> Kesäkuussa vaihtuva ja heinäkuussa palaava logo kertoo kampanjakalenterista, ei kannasta.</li>
<li><strong>Liikkuuko raha?</strong> Kerro summa ja saaja — "osa tuotosta" ilman lukua on markkinointifraasi.</li>
<li><strong>Onko viesti sama kaikkialla?</strong> Sateenkaari vain niissä maissa, joissa se on turvallista, on markkina-arvio.</li>
<li><strong>Vastaako oma talo?</strong> Henkilöstöpolitiikka, palkkaerot ja poliittiset lahjoitukset kertovat enemmän kuin kampanja.</li>
</ul>
</div>
<p>Ero lähikäsitteisiin: <strong>viherpesu</strong> koskee ympäristöväitettä ja <strong>sinipesu</strong> vastuullisuussitoumusta — pinkkipesussa lainataan kokonaisen ihmisryhmän tai potilasjärjestön symbolia, jolloin kritiikki on hankalampaa: symbolin arvostelu näyttää helposti asian itsensä arvostelulta. Juuri se tekee mekanismista tehokkaan.</p>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Katso jatkuvuutta ja rahaa, älä väriä. Aito tuki näkyy kolmessa paikassa: budjetissa (summa ja saaja julki), rakenteissa (työehdot, syrjimättömyys, edustus) ja ajassa (sama linja myös kampanjan ulkopuolella). Jos kysyt yritykseltä nämä kolme etkä saa lukuja, olet saanut vastauksen. Huomaa myös, että symbolin käyttö voi olla aitoa ja silti riittämätöntä — kyse ei ole moraalituomiosta vaan siitä, ettei symbolista voi päätellä tekoja.
    </div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://en.wikipedia.org/wiki/Pinkwashing_(LGBT)" target="_blank" rel="noopener">Wikipedia: Pinkwashing (englanniksi)</a></li>
<li><a href="https://www.bcaction.org/think-before-you-pink/" target="_blank" rel="noopener">Breast Cancer Action: Think Before You Pink (englanniksi)</a></li>
</ul>
</div>
</div>""",
     ["viherpesu", "hyvesignalointi", "sinipesu", "sosiaalinen-todiste", "tekoalypesu"])

# ────────────────────────── 122 · Klikkiotsikko ──────────────────────────
page("klikkiotsikko", ALUSTA,
     "Klikkiotsikko — lupaus, jota juttu ei lunasta",
     "Klikkiotsikko (clickbait) on rakennettu tuottamaan klikki eikä kertomaan sisällöstä: tieto pidätetään, jotta uteliaisuusaukko pakottaa avaamaan jutun.",
     r"""
<p><strong>Klikkiotsikko</strong> (engl. <strong>clickbait</strong>) on otsikko, jonka tehtävä on tuottaa klikki — ei kertoa, mitä juttu sisältää. Ratkaiseva ero tavalliseen otsikkoon ei ole kärjekkyys vaan <em>tiedon pidättäminen</em>: otsikko kertoo, että jotain kiinnostavaa tapahtui, muttei mitä.</p>
<p>Mekanismin selittää psykologi George Loewensteinin vuoden 1994 <em>information gap</em> -teoria: uteliaisuus ei synny tietämättömyydestä vaan siitä, että <em>huomaamme</em> aukon omassa tiedossamme. Aukko tuntuu epämiellyttävältä, ja sen sulkeminen palkitsee. Klikkiotsikko avaa aukon tarkoituksella ja myy sen sulkemisen. Kun mainostulo lasketaan näyttökerroista, otsikon arvo mitataan klikkeinä eikä luottamuksena — ja silloin lupauksen ja sisällön väliin kannattaa jättää kuilu.</p>
<div class="mermaid">
flowchart TD
  A["Ansainta perustuu\nnäyttökertoihin"] --&gt; O["Otsikko pidättää\nratkaisevan tiedon"]
  O --&gt; U["Uteliaisuusaukko:\n'mitä tapahtui?'"]
  U --&gt; K["Klikki"]
  K --&gt; P["Sisältö ei vastaa\nlupausta"]
  P --&gt; L["Luottamus laskee,\nklikkihinta nousee"]
  L --&gt; O
  style O fill:#fdf0f0,stroke:#c0392b
  style K fill:#fff3cd,stroke:#f39c12
    </div>
<p class="kaavio-selitys">Kuilu otsikon ja sisällön välillä on tuote, ei virhe.</p>
<div class="infolaatikko">
<h2 class="laatikko-otsikko">Klikkiotsikon vakiorakenteet</h2>
<ul style="margin:0.5em 0 0;">
<li><strong>Pidätetty subjekti:</strong> "Tämä yksi asia muutti kaiken" — mikä asia, ei otsikossa.</li>
<li><strong>Pidätetty lopputulos:</strong> "Katso mitä tapahtui seuraavaksi."</li>
<li><strong>Lukija toisena persoonana:</strong> "Et usko, mitä hän vastasi."</li>
<li><strong>Numerolista:</strong> lukumäärä lupaa nopean luettavuuden ja mitoittaa aukon.</li>
<li><strong>Kysymysmuoto:</strong> väite esitetään kysymyksenä, jolloin sitä ei tarvitse todistaa — ks. <strong>Betteridgen laki</strong>.</li>
</ul>
</div>
<p>Ero lähikäsitteisiin: <strong>rage bait</strong> tavoittelee suuttumusta ja <strong>engagement bait</strong> pyytää reaktiota suoraan — klikkiotsikko käyttää uteliaisuutta, ja se lakkaa toimimasta heti kun aukko sulkeutuu. Siksi sen kustannus lankeaa julkaisijalle itselleen: alustat ovat mitanneet klikin jälkeistä käyttäytymistä ja laskeneet sellaisten julkaisijoiden näkyvyyttä, joiden lukijat palaavat heti takaisin.</p>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Lue otsikko loppuun ja kysy, <strong>mitä se konkreettisesti väittää</strong>. Jos et osaa kertoa otsikon perusteella kuka teki mitä ja mikä oli lopputulos, tieto on pidätetty tarkoituksella. Kolme käytännön keinoa: hae aihe suoraan hakukoneesta ja lue se lähde, joka kertoo asian otsikossa; katso julkaisijan muita otsikoita — kuvio toistuu tai ei toistu; ja huomaa oma reaktiosi, sillä pakottava tarve klikata on itsessään merkki siitä, että aukko rakennettiin sinua varten.
    </div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://en.wikipedia.org/wiki/Clickbait" target="_blank" rel="noopener">Wikipedia: Clickbait (englanniksi)</a></li>
<li><a href="https://en.wikipedia.org/wiki/Information_gap_theory_of_curiosity" target="_blank" rel="noopener">Wikipedia: Information gap theory of curiosity (englanniksi)</a></li>
</ul>
</div>
</div>""",
     ["rage-bait", "betteridgen-laki", "engagement-bait", "doomscrolling", "ai-slop"])

# ────────────────────────── 123 · Engagement bait ──────────────────────────
page("engagement-bait", ALUSTA,
     "Engagement bait — reaktiota pyydetään suoraan",
     "Engagement bait tarkoittaa sisältöä, joka pyytää tykkäystä, jakoa tai kommenttia suoraan, koska algoritmi palkitsee vuorovaikutuksesta riippumatta sen syystä.",
     r"""
<p><strong>Engagement bait</strong> tarkoittaa sisältöä, joka pyytää reaktiota suoraan — tykkää, jaa, kommentoi, äänestä, tägää kaveri — saadakseen algoritmin levittämään sen. Termi on peräisin Facebookilta, joka nimesi ilmiön ja alkoi laskea sen näkyvyyttä joulukuussa 2017 ja erotteli viisi muotoa: äänestys-, reaktio-, jako-, kommentti- ja tägäyssyötin.</p>
<p>Logiikka on suoraviivainen. Suositteluagoritmi mittaa vuorovaikutusta, koska sitä on helppo laskea — mutta se ei erottele, syntyikö vuorovaikutus kiinnostuksesta vai pyynnöstä. Kun mittari on pyydettävissä, sitä pyydetään: kiinnostavan sisällön tekeminen on kallista, kehotuksen lisääminen ilmaista.</p>
<div class="mermaid">
flowchart TD
  A["Algoritmi mittaa\nvuorovaikutusta"] --&gt; B["Mittaria voi\npyytää suoraan"]
  B --&gt; C["'Tykkää jos olet\nsamaa mieltä'"]
  C --&gt; D["Reaktiot nousevat\nilman sisältöä"]
  D --&gt; E["Näkyvyys kasvaa,\nsyöte täyttyy"]
  E --&gt; A
  style B fill:#fdf0f0,stroke:#c0392b
  style E fill:#fff3cd,stroke:#f39c12
    </div>
<p class="kaavio-selitys">Kun mittarin voi pyytää, se lakkaa mittaamasta kiinnostusta.</p>
<div class="infolaatikko">
<h2 class="laatikko-otsikko">Viisi vakiomuotoa</h2>
<ul style="margin:0.5em 0 0;">
<li><strong>Äänestyssyötti:</strong> "Kumpi näistä? Tykkää A:sta, sydän B:stä."</li>
<li><strong>Reaktiosyötti:</strong> "Reagoi, jos olet samaa mieltä."</li>
<li><strong>Jakosyötti:</strong> "Jaa, jos välität" — jakaminen esitetään moraalisena tekona.</li>
<li><strong>Kommenttisyötti:</strong> "Kirjoita amen" tai "vain 1&nbsp;% osaa vastata".</li>
<li><strong>Tägäyssyötti:</strong> "Merkitse kaveri, joka tekee näin" — levitys ulkoistetaan lukijalle.</li>
</ul>
</div>
<p>Sama tekniikka on nykyään myös huijausten esivaihe. Tili kerää sitoutumista harmittomilla syöteillä, kasvattaa tavoittavuutta ja vaihtaa vasta sen jälkeen sisältönsä — mainostukseen, tilin myyntiin tai suoraan huijaukseen. Kerätty näkyvyys on vaihdettavissa rahaksi, joten sen rakentaminen kannattaa jo ennen kuin käyttötarkoitus on päätetty.</p>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Ajattele reaktiota maksuvälineenä: se on ainoa asia, jonka annat ilmaiseksi ja jolla on alustalla hinta. <strong>Älä anna sitä pyynnöstä.</strong> Käytännössä: jos julkaisu kertoo sinulle mitä sinun pitäisi tehdä sille, se on syötti eikä sisältö. Tarkista tilin historia ennen kuin jaat — vaihtuiko aihe äskettäin täysin? Ja huomaa ero omaan käytökseesi: ärsyttävän julkaisun kommentointi on <strong>rage baitin</strong> palkkio, tyhjän kysymyksen vastaaminen engagement baitin. Kummassakin maksat samalla valuutalla.
    </div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://about.fb.com/news/2017/12/news-feed-fyi-fighting-engagement-bait-on-facebook/" target="_blank" rel="noopener">Meta Newsroom: Fighting Engagement Bait on Facebook (englanniksi)</a></li>
<li><a href="https://en.wikipedia.org/wiki/Clickbait" target="_blank" rel="noopener">Wikipedia: Clickbait (englanniksi)</a></li>
</ul>
</div>
</div>""",
     ["rage-bait", "klikkiotsikko", "kaikukammio", "sosiaalinen-todiste", "ai-slop"])


def alikansiopolut(html):
    korvaukset = [
        ('href="style.css', 'href="../style.css'),
        ('href="fonts/', 'href="../fonts/'),
        ('src="favicon.svg"', 'src="../favicon.svg"'),
        ('href="favicon.svg"', 'href="../favicon.svg"'),
        ("s.src = 'js/mermaid.min.js';", "s.src = '../js/mermaid.min.js';"),
        ('href="index.html"', 'href="../index.html"'),
        ('href="tietoa.html"', 'href="../tietoa.html"'),
        ("window.location.href = id + '.html';", "window.location.href = '../' + id + '.html';"),
        ("naytaSiirtyma('Satunnainen ilmiö', id + '.html');",
         "naytaSiirtyma('Satunnainen ilmiö', '../' + id + '.html');"),
        ("'<img class=\"random-siirtyma-logo\" src=\"favicon.svg\" alt=\"\">'",
         "'<img class=\"random-siirtyma-logo\" src=\"../favicon.svg\" alt=\"\">'"),
    ]
    for vanha, uusi in korvaukset:
        html = html.replace(vanha, uusi)
    # kategoriasivun linkki murupolussa ja JSON-LD:ssä
    html = html.replace('href="kategoria-', 'href="../kategoria-')
    return html


def build():
    tpl = TEMPLATE.read_text(encoding="utf-8")
    OUT.mkdir(exist_ok=True)

    ids_match = re.search(r"const IDS = \[(.*?)\];", tpl, re.S)
    julkaistut = [s.strip().strip('"') for s in ids_match.group(1).split(",")]
    assert len(julkaistut) == 108, f"odotettiin 108 id:tä, saatiin {len(julkaistut)}"
    ids_js = "const IDS = [" + ", ".join(json.dumps(s) for s in julkaistut) + "];"

    for i, p in enumerate(PAGES):
        slug, num = p["slug"], p["num"]
        kat_nimi, kat_sivu = p["kat"]

        if i == 0:
            prev_href, prev_nimi = f"../{EDELTAJA[0]}.html", EDELTAJA[1]
        else:
            prev_href, prev_nimi = f"{PAGES[i-1]['slug']}.html", PAGES[i - 1]["otsikko"]
        if i < len(PAGES) - 1:
            next_href, next_nimi = f"{PAGES[i+1]['slug']}.html", PAGES[i + 1]["otsikko"]
        else:
            next_href = next_nimi = None

        html = tpl.replace(VANHA_SLUG, slug)
        html = html.replace(VANHA_VARI, p["vari"])
        html = html.replace(VANHA_TITLE, p["otsikko"])
        html = html.replace(VANHA_DESC, p["kuvaus"])
        # kategoria vaihdetaan vain jos sivu ei kuulu pohjan kategoriaan
        if kat_sivu != VANHA_KAT_SIVU:
            html = html.replace(VANHA_KAT_SIVU, kat_sivu)
            html = html.replace(VANHA_KAT, kat_nimi)
        html = html.replace('"datePublished": "2026-07-14"', f'"datePublished": "{PVM_ISO}"')
        html = html.replace('"dateModified": "2026-07-14"', f'"dateModified": "{PVM_ISO}"')

        uusi_ilmio = (f'<div class="ilmio" id="{slug}">\n'
                      f'<div class="ilmio-tag">Ilmiö {num}</div>\n'
                      f'<h1>{p["otsikko"]}</h1>\n'
                      f'<p class="ilmio-byline">Kirjoittanut <a href="tietoa.html" rel="author">Ilmiömies</a> · Päivitetty {PVM_FI}</p>'
                      f'{p["sisalto"]}</div>')
        html, n = re.subn(rf'<div class="ilmio" id="{slug}">.*?\n</div>\n\n  <aside',
                          lambda m: uusi_ilmio + "\n\n  <aside", html, count=1, flags=re.S)
        assert n == 1, f"{slug}: sisältölohkoa ei löytynyt"

        html, n = re.subn(r'<aside class="liittyvat".*?</aside>',
                          lambda m: liittyvat_html(p["liittyvat"]).strip(), html, count=1, flags=re.S)
        assert n == 1, f"{slug}: liittyvät-lohkoa ei löytynyt"
        html, n = re.subn(r'<nav class="kortti-nav">.*?</nav>',
                          lambda m: nav_html(num, prev_href, prev_nimi, next_href, next_nimi).strip(),
                          html, count=1, flags=re.S)
        assert n == 1, f"{slug}: navigointia ei löytynyt"

        html, n = re.subn(r"const IDS = \[.*?\];", lambda m: ids_js, html, count=1, flags=re.S)
        assert n == 1, f"{slug}: IDS-listaa ei löytynyt"
        html = html.replace("const PREV = '1-prosentin-saanto.html';", f"const PREV = '{prev_href}';")
        html = html.replace("const NEXT = 'viherpesu.html';", f"const NEXT = '{next_href or ''}';")

        html = html.replace(
            '<link rel="canonical"',
            '<meta name="robots" content="noindex"><!-- POISTA-JULKAISTAESSA -->\n  <link rel="canonical"')

        html = alikansiopolut(html)

        (OUT / f"{slug}.html").write_text(html, encoding="utf-8")
        print(f"  {num}  {slug}.html  ({len(html) // 1024} KB)")

    print(f"\nValmis: {len(PAGES)} luonnosta kansiossa {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    build()
