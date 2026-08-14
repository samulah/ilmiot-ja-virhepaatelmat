#!/usr/bin/env python3
"""Generoi Media ja julkisuus -kategorian (13.) sivuluonnokset — 10 kpl.

Pohjana aanekas-vahemmisto.html. Tuottaa luonnokset/-kansioon 10 sivua,
joissa on noindex-meta ja ../-alkuiset polut (kansiosta katsottuna toimivat).
Julkaistaessa: siirrä juureen, poista noindex-rivi, riisu ../-etuliitteet ja
aja scripts/build_liittyvat.py + paivita_maarat.py + build_sitemap.py +
build_search_index.py.

Ajo:  python3 scripts/build_media_luonnokset.py
"""
import glob
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "aanekas-vahemmisto.html"
OUT = ROOT / "luonnokset"

KATEGORIA_NIMI = "Media ja julkisuus"
KATEGORIA_ANKKURI = "#media-ja-julkisuus"
PVM_ISO = "2026-07-28"
PVM_FI = "28.7.2026"

# Pohjasivun tunnisteet, jotka korvataan
VANHA_SLUG = "aanekas-vahemmisto"
VANHA_VARI = "#7b241c"
VANHA_TITLE = "Äänekäs vähemmistö — kommenttiosio ei ole mielipidemittari"
VANHA_DESC = ("Äänekäs vähemmistö vääristää kuvan yleisestä mielipiteestä: kärjekkäimmät "
              "kommentoijat näkyvät eniten, kun hiljainen enemmistö ei koskaan vastaa.")
VANHA_KAT = "Alustatalous ja algoritmit"
VANHA_KAT_ANKKURI = "#alustatalous-ja-algoritmit"

EDELTAJA = ("p-hakkerointi", "P-hakkerointi — testataan kunnes jokin näyttää merkitsevältä")

# Julkaistujen ilmiöiden määrä luetaan index.html:stä — luonnosten numerot
# jatkavat siitä. Kovakoodattu luku vanhenee joka julkaisussa.
JULKAISTUJA = len(re.findall(
    r'<a href="[a-z0-9-]+\.html" class="hub-kortti"',
    (ROOT / "index.html").read_text(encoding="utf-8")))
YHTEENSA = JULKAISTUJA + 10

# Luonnosten omat kortit (uusia sivuja ei vielä löydy juuresta)
OMAT_KORTIT = {
    "uutiskynnys": (JULKAISTUJA + 1, "#455a64", "Uutiskynnys",
        "Tapahtuman on oltava tuore, yllättävä ja henkilöitävä — hidas ja rakenteellinen jää kertomatta."),
    "uutisautiomaa": (JULKAISTUJA + 2, "#546e7a", "Uutisautiomaa",
        "Kun paikallislehti lakkaa, kukaan ei enää istu valtuuston kokouksessa — eikä huomaa mitään."),
    "paasyjournalismi": (JULKAISTUJA + 3, "#6d4c41", "Pääsyjournalismi",
        "Kriittinen kysymys maksaa lähteen, joten kysymykset pehmenevät ja juttu kevenee."),
    "tiedotejournalismi": (JULKAISTUJA + 4, "#00796b", "Tiedotejournalismi",
        "Uutinen on kevyesti muokattu tiedote — lähettäjä valitsi aiheen, kulman ja sitaatit."),
    "branditurvallisuus": (JULKAISTUJA + 5, "#0277bd", "Bränditurvallisuus",
        "Mainostajan estolista tekee vakavasta aiheesta kannattamattoman — kukaan ei kiellä, raha vain katoaa."),
    "huonojen-uutisten-hautaaminen": (JULKAISTUJA + 6, "#4527a0", "Huonojen uutisten hautaaminen",
        "Ikävä tieto julkaistaan perjantaina klo 16.45 tai ison uutisen varjossa."),
    "vaara-tasapaino": (JULKAISTUJA + 7, "#ad1457", "Väärä tasapaino",
        "Kaksi näkemystä samalla palstatilalla saa 97–3-tilanteen näyttämään tasaväkiseltä kiistalta."),
    "keharaportointi": (JULKAISTUJA + 8, "#7b1fa2", "Kehäraportointi",
        "Sama alkulähde siteerattuna neljä kertaa näyttää neljältä riippumattomalta vahvistukselta."),
    "gell-mannin-amnesia": (JULKAISTUJA + 9, "#e65100", "Gell-Mannin amnesia",
        "Huomaat oman alasi jutun virheet, käännät sivua ja luotat seuraavaan yhtä paljon kuin ennen."),
    "vihamielisen-median-harha": (JULKAISTUJA + 10, "#33691e", "Vihamielisen median harha",
        "Molemmat osapuolet lukevat saman jutun ja kokevat sen puolueelliseksi itseään vastaan."),
}


def julkaistut_kortit():
    """Poimii liittyvät-korttien tiedot (numero, väri, nimi, kuvaus) juuren sivuilta."""
    kortit = {}
    kuvio = re.compile(
        r'<a href="([a-z0-9-]+)\.html" class="liittyvat-kortti" style="--c:(#[0-9a-f]+)">\s*'
        r'<span class="liittyvat-numero">(\d+)</span>\s*<span class="liittyvat-teksti">\s*'
        r'<span class="liittyvat-nimi">([^<]*)</span>\s*<span class="liittyvat-kuvaus">([^<]*)</span>')
    for f in glob.glob(str(ROOT / "*.html")):
        for m in kuvio.finditer(Path(f).read_text(encoding="utf-8")):
            kortit[m.group(1)] = (int(m.group(3)), m.group(2), m.group(4), m.group(5))
    return kortit


KORTIT = julkaistut_kortit()
KORTIT.update(OMAT_KORTIT)


def liittyvat_html(slugit):
    osat = ['  <aside class="liittyvat" aria-label="Liittyvät ilmiöt">',
            "    <h2>Liittyvät ilmiöt</h2>",
            '    <div class="liittyvat-kortit">']
    for s in slugit:
        num, vari, nimi, kuvaus = KORTIT[s]
        # oma luonnos → sama kansio, julkaistu ilmiö → juuri
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


PAGES = []


def page(slug, otsikko, kuvaus, sisalto, liittyvat):
    num, vari = OMAT_KORTIT[slug][0], OMAT_KORTIT[slug][1]
    PAGES.append(dict(slug=slug, num=num, vari=vari, otsikko=otsikko,
                      kuvaus=kuvaus, sisalto=sisalto, liittyvat=liittyvat))


# ────────────────────────── 109 · Uutiskynnys ──────────────────────────
page("uutiskynnys",
     "Uutiskynnys — miksi tärkeä asia ei koskaan päädy uutisiin",
     "Uutiskynnys ratkaisee, mistä uutisoidaan: asian on oltava tuore, yllättävä ja henkilöitävä. Hidas ja rakenteellinen ongelma jää siksi kertomatta.",
     r"""
<p><strong>Uutiskynnys</strong> (englanniksi <em>news threshold</em>, taustalla <em>news values</em>) tarkoittaa sitä rajaa, jonka tapahtuman on ylitettävä päästäkseen uutiseksi. Kynnys ei ole päätös yksittäisestä aiheesta vaan rutiini: toimitus arvioi joka päivä satoja mahdollisia aiheita muutaman vakiintuneen kriteerin läpi. Johan Galtung ja Mari Holmboe Ruge kuvasivat kriteerit jo vuonna 1965 — tuoreus, yllättävyys, suuruus, läheisyys, henkilöityminen, konflikti, eliittihenkilöt ja eliittimaat.</p>
<div class="mermaid">
flowchart TD
  A["Asia tapahtuu tai\njatkuu tapahtumasta"] --&gt; B{"Onko selvä\ntapahtumahetki?"}
  B -- ei --&gt; X["Ei ylitä kynnystä"]
  B -- kyllä --&gt; C{"Onko tunnistettava\ntekijä tai uhri?"}
  C -- ei --&gt; X
  C -- kyllä --&gt; D{"Yllättävä, lähellä,\nkonfliktinen?"}
  D -- ei --&gt; X
  D -- kyllä --&gt; U["Uutinen"]
  style X fill:#fdf0f0,stroke:#c0392b
    </div>
<p class="kaavio-selitys">Kynnys ei suodata epätärkeitä asioita pois — se suodattaa pois asiat, joilla ei ole tapahtuman muotoa.</p>
<p>Seuraukset ovat järjestelmällisiä. Läpi menee ryöstö, onnettomuus, eroilmoitus ja skandaali. Kynnyksen alle jää se, mikä muuttuu hitaasti ja ilman yksittäistä hetkeä: pienituloisten ostovoiman rapautuminen, hoitojonojen piteneminen, homekoulujen korjausvelka, lainsäädännön valmisteluvaiheet. Sama koskee maantiedettä — kaukaisen maan tuhannen ihmisen katastrofi voi jäädä pienemmäksi uutiseksi kuin lähialueen yksittäinen kuolema.</p>
<p>Olennaista on, ettei kyse ole salaliitosta. Kukaan ei päätä vaieta rakenteellisista ongelmista; ne vain eivät tapahdu minään päivänä. Juuri siksi kynnyksen tuntevat viestijät osaavat rakentaa asialleen tapahtuman: julkistus, kannanotto, mielenosoitus tai vuosipäivä on tekninen keino ylittää kynnys ilman että itse asia on muuttunut.</p>
<div class="infolaatikko">
<h2 class="laatikko-otsikko">Ero läheisiin käsitteisiin:</h2> Uutiskynnys on toimituksen rutiini, <a href="../manufactured-consent.html">manufactured consent</a> taas rakenteellinen malli siitä, miten omistus ja mainostulot suodattavat julkisuutta laajemmin. <a href="../portinvartija-kulttuuri.html">Portinvartija-kulttuurissa</a> tieto pysähtyy organisaation sisällä ennen kuin se edes päätyy toimituksen arvioitavaksi.
    </div>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2>
<ul style="margin:0.5em 0 0;">
<li>Erota kaksi kysymystä: "mikä tässä on uutta" ja "mikä tässä on tärkeää". Uutisvirta vastaa vain edelliseen.</li>
<li>Jos jostain ei uutisoida, älä tulkitse sitä todisteeksi ettei mitään tapahdu — kysy, olisiko asialla ylipäätään tapahtuman muotoa.</li>
<li>Seuraa lähteitä, joilla ei ole kynnystä: esityslistat, pöytäkirjat, tilastojulkistukset, valvontaviranomaisten päätökset, tilinpäätökset.</li>
<li>Jos itse viestit, tunnista että tapahtuman rakentaminen on legitiimi keino — mutta huomaa myös, kun joku muu tekee sen sinulle.</li>
</ul>
</div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Tutkimusta</span>
<ul class="lue-lisaa-lista">
<li><cite>The Structure of Foreign News</cite> — Johan Galtung &amp; Mari Holmboe Ruge (1965)</li>
<li><cite>What Is News? News Values Revisited</cite> — Tony Harcup &amp; Deirdre O'Neill (2017)</li>
</ul>
</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://en.wikipedia.org/wiki/News_values" target="_blank" rel="noopener">Wikipedia: News values (englanniksi)</a></li>
</ul>
</div>
</div>
""", ["uutisautiomaa", "tiedotejournalismi", "manufactured-consent", "portinvartija-kulttuuri"])

# ────────────────────────── 110 · Uutisautiomaa ──────────────────────────
page("uutisautiomaa",
     "Uutisautiomaa — kunta, jossa kukaan ei enää seuraa päätöksiä",
     "Uutisautiomaa syntyy, kun paikallislehti lakkaa: valtuuston kokouksissa ei istu ketään, virheet jäävät huomaamatta ja päätöksenteon hinta nousee.",
     r"""
<p><strong>Uutisautiomaa</strong> (englanniksi <em>news desert</em>) on alue, jolla ei ole enää yhtään toimitusta seuraamassa paikallista päätöksentekoa. Termin vakiinnutti Penelope Muse Abernathyn tutkimusryhmä, joka on seurannut yhdysvaltalaisten paikallislehtien katoamista 2000-luvulta lähtien. Ilmiö ei ole amerikkalainen erikoisuus: sama logiikka toimii aina, kun ilmoitustulot siirtyvät alustoille ja toimitukset keskitetään maakuntakeskuksiin.</p>
<div class="mermaid">
flowchart TD
  A["Ilmoitustulot\nsiirtyvät alustoille"] --&gt; B["Paikallislehti\nlakkaa tai ohenee"]
  B --&gt; C["Kukaan ei istu\nvaltuuston kokouksessa"]
  C --&gt; D["Päätökset, hankinnat ja\nvirheet jäävät huomaamatta"]
  D --&gt; E["Osallistuminen ja\nlukijoiden kiinnostus laskee"]
  E --&gt; A
  style D fill:#fdf0f0,stroke:#c0392b
    </div>
<p class="kaavio-selitys">Kierre ruokkii itseään: mitä vähemmän paikallista uutisointia, sitä vähemmän kysyntää sille.</p>
<p>Vaikutus ei jää symboliseksi. Yhdysvaltalaisessa tutkimuksessa <em>Financing Dies in Darkness?</em> (Gao, Lee &amp; Murphy, 2020) havaittiin, että kun kunnan paikallislehti lakkasi, kunnan lainanoton kustannukset nousivat mitattavasti — sijoittajat hinnoittelivat sen, ettei kukaan enää valvonut rahankäyttöä. Muissa tutkimuksissa on havaittu äänestysaktiivisuuden laskua, valtuustopaikkojen jäämistä ilman vastaehdokkaita ja puoluepolitiikan valtakunnallistumista: kun paikallisia asioita ei uutisoida, äänestäjä äänestää valtakunnan politiikan perusteella.</p>
<p>Autiomaa syntyy myös hiljaa, ilman lakkautusta. Lehti voi ilmestyä edelleen, mutta sisältö tulee maakuntakeskuksesta ja kunnasta kirjoitetaan vain silloin, kun sattuu jotain poikkeuksellista. Tätä kutsutaan aavelehdeksi (<em>ghost newspaper</em>).</p>
<div class="infolaatikko">
<h2 class="laatikko-otsikko">Ero läheisiin käsitteisiin:</h2> <a href="uutiskynnys.html">Uutiskynnyksessä</a> joku arvioi aiheen ja jättää sen tekemättä; uutisautiomaassa ei ole ketään, joka edes arvioisi. Tyhjiö ei jää tyhjäksi: se täyttyy sosiaalisen median huhuilla ja joskus poliittisesti rahoitetuilla valeverkkolehdillä, jotka jäljittelevät paikallislehden ulkoasua.
    </div>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2>
<ul style="margin:0.5em 0 0;">
<li>Tarkista, kuka kirjoittaa oman kuntasi päätöksistä. Jos jutuissa ei ole nimeä eikä paikallista haastateltavaa, sisältö tulee muualta.</li>
<li>Lue esityslistat ja pöytäkirjat suoraan kunnan sivuilta — ne julkaistaan, vaikka niistä ei uutisoitaisi.</li>
<li>Julkisuuslaki antaa oikeuden pyytää asiakirjoja itse; tietopyyntö on maksuton ja siihen on vastattava.</li>
<li>Epäile "paikallista" verkkosivustoa, jolla ei ole toimitusta, osoitetta eikä nimettyjä toimittajia.</li>
<li>Paikallisen journalismin tilaaminen on käytännössä ainoa vastakeino, joka vaikuttaa rakenteeseen eikä vain omaan tietotasoon.</li>
</ul>
</div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Tutkimusta</span>
<ul class="lue-lisaa-lista">
<li><cite>Financing Dies in Darkness? The Impact of Newspaper Closures on Public Finance</cite> — Gao, Lee &amp; Murphy (2020)</li>
<li><cite>The Expanding News Desert</cite> — Penelope Muse Abernathy (2018)</li>
</ul>
</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://en.wikipedia.org/wiki/News_desert" target="_blank" rel="noopener">Wikipedia: News desert (englanniksi)</a></li>
</ul>
</div>
</div>
""", ["uutiskynnys", "paasyjournalismi", "valta-suojelee-valtaa", "manufactured-consent"])

# ────────────────────────── 111 · Pääsyjournalismi ──────────────────────────
page("paasyjournalismi",
     "Pääsyjournalismi — kriittinen kysymys maksaa lähteen",
     "Pääsyjournalismissa toimittaja on riippuvainen lähteen jatkuvasta pääsystä: kriittinen juttu katkaisisi suhteen, joten kysymykset pehmenevät.",
     r"""
<p><strong>Pääsyjournalismi</strong> (englanniksi <em>access journalism</em>) tarkoittaa asetelmaa, jossa toimittajan työ perustuu jatkuvaan pääsyyn vallankäyttäjän lähelle: haastatteluihin, taustatilaisuuksiin, ennakkotietoihin. Pääsy on lähteen omaisuutta, ja sen voi ottaa pois. Siksi kriittinen juttu ei maksa vain yhtä juttua vaan koko työn perustan — ja kysymykset pehmenevät ilman, että kukaan käskee.</p>
<div class="mermaid">
flowchart TD
  A["Toimittaja tarvitsee\npääsyn lähteelle"] --&gt; B["Juttu tehdään\nlähteen ehdoilla"]
  B --&gt; C["Palkkio: uusi haastattelu,\nvuoto, ennakkotieto"]
  C --&gt; A
  B --&gt; D["Kriittinen juttu\nolisi mahdollinen"]
  D --&gt; E["Pääsy katkeaa —\nkilpailija saa jutut"]
  style E fill:#fdf0f0,stroke:#c0392b
    </div>
<p class="kaavio-selitys">Rangaistus on hiljainen: puhelimeen ei vastata, seuraava haastattelu annetaan jollekulle muulle.</p>
<p>Asetelma tuottaa tunnistettavia jälkiä. Haastattelussa ei ole jatkokysymystä. Kysymykset on sovittu ennakkoon. Juttu perustuu nimettömään "lähipiiriin", jonka näkökulma on johdonmukaisesti sama. Yrityksestä kertova juttu nojaa toimitusjohtajan haastatteluun eikä yhteenkään entiseen työntekijään. Vastapainona syntyy myös hyötyä: pääsy tuottaa tietoa, jota ei muuten saisi. Ongelma ei ole pääsy vaan riippuvuus siitä.</p>
<p>Sama mekanismi toistuu urheilutoimituksissa (seura myöntää akkreditoinnit), viihdejournalismissa (levy-yhtiö sopii ehdot) ja teknologiajournalismissa (arvostelukappaleet ja embargot). Kaikissa kolmessa kriittisen jutun hinta on sama: seuraavaa kertaa ei tule.</p>
<div class="infolaatikko">
<h2 class="laatikko-otsikko">Ero läheisiin käsitteisiin:</h2> Rakenne on sama kuin <a href="../saantelijan-kaappaus.html">sääntelijän kaappauksessa</a> — valvoja tulee riippuvaiseksi valvottavasta — mutta instituutio on media. <a href="tiedotejournalismi.html">Tiedotejournalismissa</a> aineisto tulee valmiina; pääsyjournalismissa toimittaja tekee työn itse, mutta rajatusta asemasta.
    </div>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2>
<ul style="margin:0.5em 0 0;">
<li>Katso, esitetäänkö haastattelussa yhtään jatkokysymystä. Sen puuttuminen kertoo enemmän kuin kysymysten sisältö.</li>
<li>Kysy jokaisesta eksklusiivista: kuka hyötyi siitä, että juuri tämä toimittaja sai sen juuri nyt?</li>
<li>Arvosta juttuja, jotka nojaavat asiakirjoihin, tilastoihin ja entisiin työntekijöihin — ne eivät ole riippuvaisia kenenkään suosiosta.</li>
<li>Lue sama aihe kahdesta julkaisusta, joista toisella ei ole suhdetta lähteeseen.</li>
<li>Toimituksissa vastakeino on rakenteellinen: kierrätä vastuualueita ja pidä tutkiva työ erillään päivittäisestä seurannasta.</li>
</ul>
</div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Kirjoja</span>
<ul class="lue-lisaa-lista">
<li><cite>The Journalist and the Murderer</cite> — Janet Malcolm (1990)</li>
<li><cite>Flat Earth News</cite> — Nick Davies (2008)</li>
</ul>
</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://en.wikipedia.org/wiki/Access_journalism" target="_blank" rel="noopener">Wikipedia: Access journalism (englanniksi)</a></li>
</ul>
</div>
</div>
""", ["tiedotejournalismi", "uutiskynnys", "saantelijan-kaappaus", "portinvartija-kulttuuri"])

# ────────────────────────── 112 · Tiedotejournalismi ──────────────────────────
page("tiedotejournalismi",
     "Tiedotejournalismi — uutinen, jonka kirjoitti viestintätoimisto",
     "Tiedotejournalismissa uutinen on kevyesti muokattu tiedote: aiheen, kulman ja sitaatit valitsi lähettäjä, ja toimitus tarkisti lähinnä kielen.",
     r"""
<p><strong>Tiedotejournalismi</strong> (englanniksi <em>churnalism</em>) tarkoittaa juttua, joka on käytännössä kevyesti muokattu tiedote tai uutistoimistosähke. Nick Davies popularisoi termin kirjassaan <em>Flat Earth News</em> (2008). Sen taustatutkimuksessa Cardiffin yliopisto kävi läpi 2 207 brittilehtijuttua: noin 60 prosenttia koostui kokonaan tai pääosin uutistoimisto- tai PR-aineistosta, ja vain 12 prosenttia oli kokonaan toimittajan itsensä hankkimaa.</p>
<div class="mermaid">
flowchart TD
  A["Organisaatio lähettää\nvalmiin tiedotteen"] --&gt; B["Toimitus: vähemmän\ntoimittajia, enemmän tilaa"]
  B --&gt; C["Otsikko ja kärki\nsäilyvät, kieli muokataan"]
  C --&gt; D["Juttu julkaistaan\nuutisena"]
  D --&gt; E["Muut siteeraavat juttua\n— eivät tiedotetta"]
  style E fill:#fdf0f0,stroke:#c0392b
    </div>
<p class="kaavio-selitys">Alkuperä katoaa matkalla: viides lukija näkee uutisen, ei viestintäosaston tekstiä.</p>
<p>Syy on rakenteellinen, ei laiskuus. Toimitusten henkilöstö on supistunut samaan aikaan kun julkaisualustoja ja päivitystahtia on tullut lisää, ja viestinnän ammattilaisia on länsimaissa nykyään moninkertaisesti toimittajiin nähden. Kun yhden toimittajan on tuotettava useita juttuja päivässä, valmis, siteerattava ja "uutismainen" aineisto on ainoa tapa selviytyä.</p>
<p>Lopputulos ei yleensä ole valheellinen. Se on valikoitunut: aiheen, ajankohdan, kulman, vertailukohdan ja haastateltavan on valinnut se, jonka etua juttu palvelee. Tutkimusuutisissa sama koskee yliopistojen tiedotteita, jotka kärjistävät tuloksen useammin kuin itse tutkimus.</p>
<div class="infolaatikko">
<h2 class="laatikko-otsikko">Ero läheisiin käsitteisiin:</h2> Tiedote on avoimesti lähettäjänsä teksti — <a href="../astroturf.html">astroturf</a> sen sijaan teeskentelee ruohonjuuritason liikettä. <a href="../viherpesu.html">Viherpesu</a> ja <a href="../tekoalypesu.html">tekoälypesu</a> ovat tyypillistä tiedotejournalismin sisältöä: väite kulkee läpi, koska kukaan ei ehdi tarkistaa sitä.
    </div>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2>
<ul style="margin:0.5em 0 0;">
<li>Kopioi jutun tunnistettavin virke hakukoneeseen lainausmerkeissä. Jos sama lause löytyy viidestä julkaisusta, kyseessä on tiedote.</li>
<li>Katso, onko jutussa yhtään haastateltavaa, joka ei kuulu tiedotteen lähettäjän organisaatioon.</li>
<li>Tutkimusuutisissa etsi alkuperäisjulkaisu ja vertaa sen johtopäätöstä otsikkoon.</li>
<li>Huomaa ero: "yritys kertoo" ei ole sama asia kuin "on selvitetty" — myös silloin kun juttu on muuten moitteeton.</li>
<li>Toimituksissa vastakeino on merkintäkäytäntö: kerro lukijalle avoimesti, kun juttu perustuu tiedotteeseen.</li>
</ul>
</div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Kirjoja</span>
<ul class="lue-lisaa-lista">
<li><cite>Flat Earth News</cite> — Nick Davies (2008)</li>
<li><cite>The Quality and Independence of British Journalism</cite> — Justin Lewis ym., Cardiff University (2008)</li>
</ul>
</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://en.wikipedia.org/wiki/Churnalism" target="_blank" rel="noopener">Wikipedia: Churnalism (englanniksi)</a></li>
</ul>
</div>
</div>
""", ["paasyjournalismi", "keharaportointi", "astroturf", "viherpesu"])

# ────────────────────────── 113 · Bränditurvallisuus ──────────────────────────
page("branditurvallisuus",
     "Bränditurvallisuus — mainostaja päättää, mistä aiheista kannattaa kirjoittaa",
     "Bränditurvallisuuden estolistat katkaisevat mainostulon vakavista aiheista: kukaan ei kiellä uutisointia, mutta sen tekeminen muuttuu kannattamattomaksi.",
     r"""
<p><strong>Bränditurvallisuus</strong> (englanniksi <em>brand safety</em>) tarkoittaa mainostajan pyrkimystä varmistaa, ettei sen mainos näy ei-toivotun sisällön vieressä. Käytännössä se toteutetaan avainsanojen estolistoilla: mainosjärjestelmä ohittaa sivut, joilta löytyy sanoja kuten <em>ampuminen</em>, <em>kuolema</em>, <em>sota</em> tai <em>koronavirus</em>. Ketään ei sensuroida — mutta juuri niiden juttujen tekeminen, jotka ovat journalistisesti tärkeimpiä, lakkaa tuottamasta rahaa.</p>
<div class="mermaid">
flowchart TD
  A["Mainostajan estolista:\nkielletyt avainsanat"] --&gt; B["Mainoksia ei näytetä\nvakavan jutun vierellä"]
  B --&gt; C["Vakava aihe tuottaa\nvähemmän kuin kevyt"]
  C --&gt; D["Toimitus painottaa\nturvallisia aiheita"]
  D --&gt; E["Tekijät välttelevät sanoja\nja kiertoilmaisevat"]
  style C fill:#fdf0f0,stroke:#c0392b
    </div>
<p class="kaavio-selitys">Vaikutus ei näy kieltona vaan tulorivinä — ja siirtyy sitä kautta sisältöön.</p>
<p>Ilmiö tuli näkyväksi koronapandemian alussa 2020, kun uutissivustot menettivät mainostuloja juuri sen aiheen kohdalla, jota kaikki lukivat. Estolistoilta on löydetty myös ihmisryhmiä kuvaavia sanoja, jolloin vähemmistöjä koskeva journalismi muuttuu automaattisesti "riskialttiiksi". Videopalveluissa sama näkyy suoraan tekijöiden kielessä: kiertoilmaisut kuolemasta tai seksuaalisuudesta ovat vastaus algoritmiselle demonetisoinnille, ei sattumaa.</p>
<p>Kyse on siis mainosrahan kautta kulkevasta aihevalinnasta. Se ei vaadi kenenkään pahaa tahtoa: mainostaja suojelee brändiään, alusta myy suojausta ja julkaisija sopeutuu tulovirtaan.</p>
<div class="infolaatikko">
<h2 class="laatikko-otsikko">Ero läheisiin käsitteisiin:</h2> Sensuurissa joku kieltää julkaisemisen; tässä julkaiseminen on vapaata mutta kannattamatonta. Vaikutus on <a href="../manufactured-consent.html">manufactured consentin</a> mainostajasuodattimen nykyversio, ja se selittää osaltaan, miksi <a href="../rage-bait.html">rage bait</a> ja <a href="../ai-slop.html">AI slop</a> ovat taloudellisesti järkevämpiä kuin vakava uutinen.
    </div>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2>
<ul style="margin:0.5em 0 0;">
<li>Huomaa kiertoilmaisut videoissa ja somessa — ne kertovat, mitä sanoja alusta rankaisee.</li>
<li>Älä tulkitse aiheen vähäistä käsittelyä todisteeksi siitä, ettei aihe ole tärkeä.</li>
<li>Mainostajana pyydä nähtäväksi käytetyt estolistat ja karsi niistä sanat, jotka estävät asiajournalismin. Konteksti&shy;analyysi on tarkempi työkalu kuin avainsanaesto.</li>
<li>Lukijana: tilaukset ja lahjoitukset ovat ainoa tulomuoto, johon estolistat eivät vaikuta.</li>
<li>Julkaisijana kannattaa mitata, kuinka suuri osa jutuista jää mainoksettomiksi — luku kertoo, kuinka paljon estolistat ohjaavat sisältöä.</li>
</ul>
</div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://en.wikipedia.org/wiki/Brand_safety" target="_blank" rel="noopener">Wikipedia: Brand safety (englanniksi)</a></li>
<li><a href="https://en.wikipedia.org/wiki/Demonetization_(YouTube)" target="_blank" rel="noopener">Wikipedia: YouTube-demonetisointi (englanniksi)</a></li>
</ul>
</div>
</div>
""", ["uutiskynnys", "manufactured-consent", "rage-bait", "ai-slop"])

# ─────────────────── 114 · Huonojen uutisten hautaaminen ───────────────────
page("huonojen-uutisten-hautaaminen",
     "Huonojen uutisten hautaaminen — hyvä päivä julkaista ikävä asia",
     "Ikävä tieto julkaistaan perjantai-iltapäivänä, juhlapyhän alla tai ison uutisen varjossa — muodollisesti avoimesti, käytännössä huomaamatta.",
     r"""
<p><strong>Huonojen uutisten hautaaminen</strong> (englanniksi <em>burying bad news</em>) tarkoittaa ikävän tiedon julkaisemista hetkellä, jolloin sillä on pienin mahdollisuus tulla huomatuksi. Ilmiön nimesi brittiläinen erityisavustaja Jo Moore, joka lähetti 11. syyskuuta 2001 sähköpostin: nyt on erittäin hyvä päivä haudata mitä tahansa, mitä haluamme haudata. Viestin vuotaminen maksoi hänen työpaikkansa — mutta kuvasi tarkasti vakiintuneen käytännön.</p>
<div class="mermaid">
flowchart TD
  A["Ikävä päätös tai\ntutkimustulos valmiina"] --&gt; B{"Milloin julkaistaan?"}
  B --&gt; C["Perjantai klo 16.45,\njuhlapyhän aatto"]
  B --&gt; D["Samana päivänä kun\nsuuri uutinen täyttää tilan"]
  C --&gt; E["Muodollisesti julkinen,\nkäytännössä huomaamaton"]
  D --&gt; E
  style E fill:#fdf0f0,stroke:#c0392b
    </div>
<p class="kaavio-selitys">Mitään ei salata — julkisuusvelvoite täyttyy, mutta huomioarvo lähestyy nollaa.</p>
<p>Ajoitus toimii, koska uutisvirran kapasiteetti on rajallinen ja lyhytkestoinen. Perjantai-iltana toimitukset ovat pienimmillään, seuraavan päivän lehti luetuin harvimmin, ja maanantaina aihe on jo vanha. Sama pätee juhlapyhiin, lomakausiin ja päiviin, joina jokin suuri tapahtuma vie kaiken tilan. Klassisia hautauskohteita ovat tappiolliset tulokset, palkkiopäätökset, sisäisten selvitysten loppuraportit, irtisanomiset ja hankkeiden kustannusylitykset.</p>
<p>Tekniikkaa on vaikea todistaa yksittäistapauksessa: kaikkea on julkaistava jonain päivänä. Todistusvoima syntyy toistosta — jos saman organisaation ikävät tiedotteet osuvat järjestelmällisesti perjantai-iltapäiviin ja hyvät tiistaiaamuihin, kyse ei ole sattumasta.</p>
<div class="infolaatikko">
<h2 class="laatikko-otsikko">Ero läheisiin käsitteisiin:</h2> <a href="../kuollut-kissa.html">Kuollut kissa -strategiassa</a> häiriö luodaan itse; tässä hyödynnetään olemassa olevaa melua. <a href="../streisand-ilmio.html">Streisand-ilmiö</a> on käänteinen riski: aktiivinen yritys estää tiedon leviäminen kasvattaa huomiota, kun taas hautaaminen ei anna mitään, mihin tarttua.
    </div>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2>
<ul style="margin:0.5em 0 0;">
<li>Katso tiedotteen kellonaika ja viikonpäivä. Perjantai klo 15–17 ja juhlapyhien aatot ovat tilastollisesti poikkeavia julkaisuhetkiä.</li>
<li>Kerää organisaation tiedotteet vuodelta ja vertaa ajankohtia sisältöön — kuvio näkyy vasta aineistossa.</li>
<li>Tilaa toimielinten esityslistat ja pörssitiedotteet suoraan, älä uutisvirran kautta.</li>
<li>Palaa suuren uutispäivän jälkeen katsomaan, mitä muuta samana päivänä julkaistiin.</li>
<li>Organisaatiossa: julkaisuajankohta on viestinnällinen valinta, jonka voi ja kannattaa kysyä ääneen kokouksessa.</li>
</ul>
</div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://en.wikipedia.org/wiki/Jo_Moore" target="_blank" rel="noopener">Wikipedia: Jo Moore ja "a good day to bury bad news" (englanniksi)</a></li>
<li><a href="https://en.wikipedia.org/wiki/News_dump" target="_blank" rel="noopener">Wikipedia: News dump (englanniksi)</a></li>
</ul>
</div>
</div>
""", ["kuollut-kissa", "uutiskynnys", "streisand-ilmio", "paskuuttaminen"])

# ────────────────────────── 115 · Väärä tasapaino ──────────────────────────
page("vaara-tasapaino",
     "Väärä tasapaino — kaksi näkemystä, joista toinen on kolmen prosentin",
     "Väärä tasapaino antaa marginaaliselle näkemykselle saman palstatilan kuin valtavirralle — ja tasapuolisuuden nimissä syntyy kuva tasaväkisestä kiistasta.",
     r"""
<p><strong>Väärä tasapaino</strong> (englanniksi <em>false balance</em> tai <em>bothsidesism</em>) syntyy, kun tasapuolisuuden periaatetta sovelletaan kysymykseen, jossa näytön paino on selvästi toisella puolella. Studiossa istuu kaksi asiantuntijaa, kummallakin sama puheaika — ja katsoja päättelee siitä, mitä hänelle ei kerrota: että tutkijakunta on suunnilleen kahtia jakautunut.</p>
<div class="mermaid">
flowchart TD
  A["Kysymys, jossa näyttö\non 97 % vs. 3 %"] --&gt; B["Tasapuolisuusnormi:\nmolemmat puolet kuuluviin"]
  B --&gt; C["Yhtä paljon puheaikaa\nja palstatilaa"]
  C --&gt; D["Katsoja päättelee:\nasiasta kiistellään 50–50"]
  D --&gt; E["Toiminta lykkääntyy —\n'odotetaan lisää tietoa'"]
  style D fill:#fdf0f0,stroke:#c0392b
    </div>
<p class="kaavio-selitys">Muoto viestii enemmän kuin sisältö: sama tila luetaan samaksi painoarvoksi.</p>
<p>Ilmiö on dokumentoitu tarkimmin ilmastonmuutoksen uutisoinnista. Maxwell ja Jules Boykoffin tutkimuksessa (2004) yli puolet yhdysvaltalaisten laatulehtien ilmastojutuista vuosina 1988–2002 antoi suunnilleen yhtä paljon tilaa ihmisen aiheuttamalle ilmastonmuutokselle ja sen kiistämiselle — vaikka tieteellinen kirjallisuus ei jakautunut lähellekään samoin. Britanniassa BBC:n tiedeuutisoinnin riippumaton arvio (2011) päätyi samaan johtopäätökseen ja johti ohjeistuksen muuttamiseen.</p>
<p>Väärä tasapaino ei tarkoita, etteikö erimielisyyttä saisi näyttää. Se tarkoittaa, että erimielisyyden <em>painoarvo</em> on osa faktaa: jos sitä ei kerrota, tasapuolisuus muuttuu harhaanjohtavuudeksi.</p>
<div class="infolaatikko">
<h2 class="laatikko-otsikko">Ero läheisiin käsitteisiin:</h2> Vastakkainen virhe on <a href="../konsensus-fetissi.html">konsensus-fetissi</a>, jossa yksimielisyydellä tukahdutetaan aiheellinenkin erimielisyys. <a href="../brandolinin-laki.html">Brandolinin laki</a> selittää, miksi asetelma on epäreilu jo lähtökohtaisesti: väitteen esittäminen vie sekunteja, sen kumoaminen minuutteja. Arvokysymyksissä — toisin kuin näyttökysymyksissä — kahden kannan esittäminen on aidosti oikein.
    </div>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2>
<ul style="margin:0.5em 0 0;">
<li>Kysy jokaisesta väittelystä: kuinka moni alan tutkija on kummallakin kannalla ja millä näytöllä?</li>
<li>Erota näyttökysymys ("nouseeko lämpötila") ja arvokysymys ("mitä sille pitäisi tehdä") — vain jälkimmäisessä tasapuolisuus on itsestään selvä hyve.</li>
<li>Huomaa yksittäisen eri mieltä olevan tutkijan retorinen voima: yksi ihminen studiossa näyttää yhtä suurelta kuin tuhat julkaisua.</li>
<li>Toimittajana kerro painoarvo ääneen: "valtaosa tutkimuksesta päätyy X:ään, yksittäiset tutkijat esittävät Y:tä."</li>
<li>Varo myös peilikuvaa: älä leimaa aitoa tieteellistä kiistaa "vääräksi tasapainoksi" vain siksi, että toinen kanta on epämiellyttävä.</li>
</ul>
</div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Tutkimusta</span>
<ul class="lue-lisaa-lista">
<li><cite>Balance as Bias: Global Warming and the US Prestige Press</cite> — Maxwell &amp; Jules Boykoff (2004)</li>
<li><cite>Merchants of Doubt</cite> — Naomi Oreskes &amp; Erik Conway (2010)</li>
</ul>
</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://en.wikipedia.org/wiki/False_balance" target="_blank" rel="noopener">Wikipedia: False balance (englanniksi)</a></li>
</ul>
</div>
</div>
""", ["keharaportointi", "konsensus-fetissi", "brandolinin-laki", "omenoita-appelsiineja"])

# ────────────────────────── 116 · Kehäraportointi ──────────────────────────
page("keharaportointi",
     "Kehäraportointi — sama lähde neljä kertaa näyttää neljältä lähteeltä",
     "Kehäraportoinnissa yksi alkuperäinen väite siteerataan ketjussa eteenpäin, kunnes se näyttää monen riippumattoman lähteen vahvistamalta.",
     r"""
<p><strong>Kehäraportointi</strong> (englanniksi <em>circular reporting</em>) tarkoittaa tilannetta, jossa yksi ainoa alkuperäinen lähde kiertää julkaisusta toiseen ja näyttää lopulta monelta toisistaan riippumattomalta vahvistukselta. Lukija tekee luonnollisen päätelmän: kun neljä julkaisua kertoo saman, asia on tarkistettu neljä kertaa. Todellisuudessa tarkistuksia oli nolla.</p>
<div class="mermaid">
flowchart TD
  A["Alkuperäinen väite\n(yksi lähde)"] --&gt; B["Julkaisu B siteeraa A:ta"]
  B --&gt; C["Julkaisu C siteeraa B:tä"]
  C --&gt; D["Julkaisu D:\n'useiden lähteiden mukaan'"]
  D --&gt; E["Wikipedia lähteistää\nväitteen D:hen"]
  E --&gt; A
  style D fill:#fdf0f0,stroke:#c0392b
    </div>
<p class="kaavio-selitys">Kun ketju sulkeutuu, alkuperää ei voi enää jäljittää — jokainen viittaa toiseen.</p>
<p>Havainnollisin todiste tehtiin vahingossa vuonna 2009: irlantilainen opiskelija Shane Fitzgerald lisäsi juuri kuolleen säveltäjän Maurice Jarren Wikipedia-artikkeliin itse keksimänsä sitaatin. Se päätyi useiden suurten lehtien muistokirjoituksiin, koska jokainen luotti edelliseen. Erikoistapaus on <em>sitogeneesi</em>, jossa Wikipedian virhe siteerataan lehtijuttuun ja lehtijuttu lisätään sitten Wikipedian lähteeksi — jolloin väite todistaa itsensä.</p>
<p>Sama rakenne toistuu tutkimusväitteissä: alkuperäisen julkaisun sijaan siteerataan artikkelia, joka siteerasi tiedotetta, joka tiivisti tutkimuksen. Toistojen määrä alkaa tuntua näytöltä, vaikka se on vain kaikua.</p>
<div class="infolaatikko">
<h2 class="laatikko-otsikko">Ero läheisiin käsitteisiin:</h2> <a href="../sosiaalinen-todiste.html">Sosiaalinen todiste</a> selittää, miksi toistuvuus vakuuttaa; kehäraportointi kuvaa, miten toisto syntyy ilman että kukaan huijaa tahallaan. <a href="tiedotejournalismi.html">Tiedotejournalismi</a> on ketjun tavallisin alkupää, ja <a href="../brandolinin-laki.html">Brandolinin laki</a> kertoo, miksi ketjun purkaminen on työläämpää kuin sen syntyminen.
    </div>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2>
<ul style="margin:0.5em 0 0;">
<li>Klikkaa lähdeketju loppuun asti. Kysymys on aina sama: mikä on ensimmäinen julkaisu, jolla oli oma havainto?</li>
<li>Katso päivämäärät. Jos kaikki "riippumattomat" jutut ovat parin päivän sisällä, kyseessä on yksi lähde.</li>
<li>Epäile ilmauksia "useiden lähteiden mukaan" ja "kansainvälisen median mukaan" ilman nimettyä alkuperää.</li>
<li>Wikipedia-viittauksissa tarkista, onko lähteenä oleva juttu julkaistu ennen vai jälkeen artikkelin muokkauksen.</li>
<li>Tutkimusväitteissä etsi alkuperäisjulkaisu — älä uutista uutisesta.</li>
</ul>
</div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://en.wikipedia.org/wiki/Circular_reporting" target="_blank" rel="noopener">Wikipedia: Circular reporting (englanniksi)</a></li>
<li><a href="https://en.wikipedia.org/wiki/Citogenesis" target="_blank" rel="noopener">Wikipedia: Citogenesis (englanniksi)</a></li>
</ul>
</div>
</div>
""", ["tiedotejournalismi", "vaara-tasapaino", "brandolinin-laki", "sosiaalinen-todiste"])

# ────────────────────────── 117 · Gell-Mannin amnesia ──────────────────────────
page("gell-mannin-amnesia",
     "Gell-Mannin amnesia — luet oman alasi jutun ja unohdat sen heti",
     "Gell-Mannin amnesia: huomaat oman erikoisalasi jutussa virheet, käännät sivua ja luotat seuraavaan juttuun aivan yhtä paljon kuin ennen.",
     r"""
<p><strong>Gell-Mannin amnesia</strong> (englanniksi <em>Gell-Mann amnesia effect</em>) kuvaa tuttua kokemusta: luet jutun aiheesta, jonka osaat itse, ja huomaat sen olevan täynnä virheitä, sekaannuksia ja väärinymmärryksiä. Käännät sivua — ja luet seuraavan jutun aiheesta, jota et osaa, aivan yhtä luottavaisesti kuin ennen. Kirjailija Michael Crichton kuvasi ilmiön puheessaan vuonna 2002 ja nimesi sen ystävänsä, fyysikko Murray Gell-Mannin mukaan.</p>
<div class="mermaid">
flowchart TD
  A["Luet jutun\nomalta erikoisalaltasi"] --&gt; B["Havaitset virheet:\n'tämähän on pielessä'"]
  B --&gt; C["Käännät sivua"]
  C --&gt; D["Luet jutun alalta,\njota et tunne"]
  D --&gt; E["Luotat siihen täysin —\nvirheitä ei näy"]
  E --&gt; A
  style E fill:#fdf0f0,stroke:#c0392b
    </div>
<p class="kaavio-selitys">Virhetaso on todennäköisesti sama molemmissa jutuissa. Vain havaintokykysi vaihtelee.</p>
<p>Syy on epäsymmetria: virheen havaitseminen vaatii saman osaamisen kuin sen välttäminen. Omalla alalla näet, mikä puuttuu ja mikä on käännetty väärin; vieraalla alalla juttu näyttää sujuvalta ja auktoritatiiviselta, koska sinulla ei ole mitään, mihin verrata. Lisäksi lukukokemus on tunteeton: turhautuminen omalta alalta ei siirry seuraavaan juttuun, koska se ei tuntunut yleiseltä havainnolta vaan yksittäiseltä kömmähdykseltä.</p>
<p>Havainto ei tarkoita, että media valehtelisi tai olisi hyödytön. Se tarkoittaa, että toimittaja työskentelee tuntikausissa aiheesta, jota lähde on tutkinut vuosia — ja lopputuloksen tarkkuus vaihtelee sen mukaan.</p>
<div class="infolaatikko">
<h2 class="laatikko-otsikko">Ero läheisiin käsitteisiin:</h2> <a href="../dunning-kruger.html">Dunning–Kruger-ilmiössä</a> osaamattomuus estää arvioimasta omaa suoritusta; tässä osaaminen paljastaa toisen suorituksen — mutta vain omalla kapealla kaistalla. <a href="../halo-efekti.html">Halo-efekti</a> vahvistaa vaikutusta: arvostettu julkaisu saa jutun näyttämään luotettavalta riippumatta aiheesta.
    </div>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2>
<ul style="margin:0.5em 0 0;">
<li>Kalibroi luottamuksesi omalta alaltasi havaitsemaasi virhetasoon — se on paras saatavilla oleva otos koko julkaisun tarkkuudesta.</li>
<li>Erota jutussa kaksi kerrosta: mitä tapahtui (yleensä oikein) ja mitä se tarkoittaa (usein liian varmaa).</li>
<li>Lue oman alansa asiantuntijoiden kommentteja isoista jutuista — ne paljastavat, mitä ulkopuolinen ei näe.</li>
<li>Kun aihe on sinulle tärkeä, mene alkuperäislähteeseen: raporttiin, tutkimukseen, päätökseen.</li>
<li>Toimittajana pienin tehokas vastakeino on antaa asiantuntijan tarkistaa faktat ennen julkaisua — ei koko juttua, vaan tekniset kohdat.</li>
</ul>
</div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Puheita</span>
<ul class="lue-lisaa-lista">
<li><cite>Why Speculate?</cite> — Michael Crichton (2002)</li>
</ul>
</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://en.wikipedia.org/wiki/Michael_Crichton#Gell-Mann_amnesia_effect" target="_blank" rel="noopener">Wikipedia: Gell-Mann amnesia effect (englanniksi)</a></li>
</ul>
</div>
</div>
""", ["vihamielisen-median-harha", "tiedotejournalismi", "dunning-kruger", "halo-efekti"])

# ─────────────── 10 · Vihamielisen median harha ───────────────
page("vihamielisen-median-harha",
     "Vihamielisen median harha — sama juttu on molempien mielestä puolueellinen",
     "Vihamielisen median harha: kaksi vastakkaista leiriä lukee saman jutun ja kumpikin kokee sen puolueelliseksi itseään vastaan.",
     r"""
<p><strong>Vihamielisen median harha</strong> (englanniksi <em>hostile media effect</em>) tarkoittaa taipumusta kokea sama uutisjuttu puolueelliseksi omaa kantaa vastaan riippumatta siitä, kummalla puolella on. Stanfordin tutkijat Robert Vallone, Lee Ross ja Mark Lepper osoittivat sen vuonna 1985: he näyttivät samat televisiouutiset Libanonin sodan tapahtumista opiskelijoille, jotka kannattivat eri osapuolia. Molemmat ryhmät arvioivat uutisoinnin vihamieliseksi omaa puoltaan kohtaan — ja pelkäsivät sen kääntävän puolueettomat katsojat vastapuolelle.</p>
<div class="mermaid">
flowchart TD
  A["Sama juttu, kaksi\nvastakkaista lukijaa"] --&gt; B["Oma kanta koetaan\nneutraaliksi lähtökohdaksi"]
  B --&gt; C["Omaa kantaa vastaan\nsanotut kohdat jäävät mieleen"]
  C --&gt; D["Molemmat: 'juttu on\npuolueellinen minua vastaan'"]
  D --&gt; E["Luottamus mediaan laskee\nmolemmilla puolilla"]
  style D fill:#fdf0f0,stroke:#c0392b
    </div>
<p class="kaavio-selitys">Kumpikin muistaa oikein — vain eri puolet samasta jutusta.</p>
<p>Mekanismi on kaksiosainen. Ensinnäkin oma kanta tuntuu neutraalilta lähtöpisteeltä, jolloin jokainen poikkeama siitä näyttää vinoumalta. Toiseksi muisti on valikoiva: omaa kantaa vastaan sanotut kohdat rekisteröityvät voimakkaammin kuin sitä tukevat, koska ne vaativat vastaväitteen. Lopputulos on julkisuuden kannalta epämiellyttävä — mitä tasapainoisempi juttu on, sitä useampi kokee sen vihamieliseksi.</p>
<p>Harha ei tarkoita, ettei puolueellisuutta olisi olemassa. Se tarkoittaa, ettei oma kokemus puolueellisuudesta ole luotettava mittari sen olemassaolosta.</p>
<div class="infolaatikko">
<h2 class="laatikko-otsikko">Ero läheisiin käsitteisiin:</h2> <a href="../kaikukammio.html">Kaikukammiossa</a> et kohtaa vastakkaista näkemystä lainkaan; tässä kohtaat sen ja tulkitset sen hyökkäykseksi. <a href="../backfire-effect.html">Backfire effect</a> kertoo, mitä siitä seuraa: vastakkaisen tiedon kohtaaminen voi vahvistaa alkuperäistä kantaa. <a href="../aanekas-vahemmisto.html">Äänekäs vähemmistö</a> selittää, miksi palaute näyttää yksipuoliselta myös toimituksen suunnasta.
    </div>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2>
<ul style="margin:0.5em 0 0;">
<li>Älä luota muistikuvaan — laske. Montako kriittistä lausetta juttu esittää kumpaakin osapuolta kohtaan?</li>
<li>Kysy itseltäsi: kokisiko vastapuolen edustaja tämän jutun puolueettomaksi? Jos ei, kumpi teistä on oikeassa ja millä perusteella?</li>
<li>Erota "juttu on virheellinen" ja "juttu ei ole minun puolellani". Vain edellinen on korjattavissa oikaisulla.</li>
<li>Jos aiot valittaa puolueellisuudesta, osoita konkreettinen virhe tai poisjätetty olennainen tieto — muuten palaute vahvistaa vain sitä, että kaikki valittavat.</li>
<li>Toimituksessa: symmetrinen valitusvirta on merkki tasapainosta, ei sen puutteesta. Epäsymmetria on se, mitä kannattaa tutkia.</li>
</ul>
</div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Tutkimusta</span>
<ul class="lue-lisaa-lista">
<li><cite>The Hostile Media Phenomenon</cite> — Robert Vallone, Lee Ross &amp; Mark Lepper (1985)</li>
</ul>
</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://en.wikipedia.org/wiki/Hostile_media_effect" target="_blank" rel="noopener">Wikipedia: Hostile media effect (englanniksi)</a></li>
</ul>
</div>
</div>
""", ["gell-mannin-amnesia", "kaikukammio", "backfire-effect", "aanekas-vahemmisto"])


def alikansiopolut(html):
    """Muuntaa juuren polut toimimaan luonnokset/-kansiosta."""
    korvaukset = [
        ('href="style.css', 'href="../style.css'),
        ('href="fonts/', 'href="../fonts/'),
        ('href="favicon.svg"', 'href="../favicon.svg"'),
        ('src="favicon.svg"', 'src="../favicon.svg"'),
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
    return html


def build():
    tpl = TEMPLATE.read_text(encoding="utf-8")
    OUT.mkdir(exist_ok=True)

    ids_match = re.search(r"const IDS = \[(.*?)\];", tpl, re.S)
    julkaistut = [s.strip().strip('"') for s in ids_match.group(1).split(",")]
    assert len(julkaistut) == JULKAISTUJA, \
        f"IDS {len(julkaistut)} ≠ index.html:n kortit {JULKAISTUJA}"
    # Luonnoksia ei lisätä random-kiertoon ennen julkaisua
    ids_js = "const IDS = [" + ", ".join(json.dumps(s) for s in julkaistut) + "];"

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

        # 1) Pohjan tunnisteet (id:t, URL:t, CSS-säännöt, otsikot, kategoria, päivät)
        html = tpl.replace(VANHA_SLUG, slug)
        html = html.replace(VANHA_VARI, p["vari"])
        html = html.replace(VANHA_TITLE, p["otsikko"])
        html = html.replace(VANHA_DESC, p["kuvaus"])
        html = html.replace(VANHA_KAT, KATEGORIA_NIMI)
        html = html.replace(VANHA_KAT_ANKKURI, KATEGORIA_ANKKURI)
        html = html.replace('"datePublished": "2026-07-14"', f'"datePublished": "{PVM_ISO}"')
        html = html.replace('"dateModified": "2026-07-14"', f'"dateModified": "{PVM_ISO}"')

        # 2) Sisältölohko
        uusi_ilmio = (f'<div class="ilmio" id="{slug}">\n'
                      f'<div class="ilmio-tag">Ilmiö {num}</div>\n'
                      f'<h1>{p["otsikko"]}</h1>\n'
                      f'<p class="ilmio-byline">Kirjoittanut <a href="tietoa.html" rel="author">Ilmiömies</a> · Päivitetty {PVM_FI}</p>'
                      f'{p["sisalto"]}</div>')
        html, n = re.subn(rf'<div class="ilmio" id="{slug}">.*?\n</div>\n\n  <aside',
                          lambda m: uusi_ilmio + "\n\n  <aside", html, count=1, flags=re.S)
        assert n == 1, f"{slug}: sisältölohkoa ei löytynyt"

        # 3) Liittyvät + navigointi (omat linkit, ei pohjan)
        html, n = re.subn(r'<aside class="liittyvat".*?</aside>',
                          lambda m: liittyvat_html(p["liittyvat"]).strip(), html, count=1, flags=re.S)
        assert n == 1, f"{slug}: liittyvät-lohkoa ei löytynyt"
        html, n = re.subn(r'<nav class="kortti-nav">.*?</nav>',
                          lambda m: nav_html(num, prev_href, prev_nimi, next_href, next_nimi).strip(),
                          html, count=1, flags=re.S)
        assert n == 1, f"{slug}: navigointia ei löytynyt"

        # 4) IDS palautetaan alkuperäisenä (kohta 1 muutti myös listan id:n)
        html, n = re.subn(r"const IDS = \[.*?\];", lambda m: ids_js, html, count=1, flags=re.S)
        assert n == 1, f"{slug}: IDS-listaa ei löytynyt"
        html = html.replace("const PREV = '1-prosentin-saanto.html';", f"const PREV = '{prev_href}';")
        html = html.replace("const NEXT = 'viherpesu.html';",
                            f"const NEXT = '{next_href or ''}';")

        # 5) noindex-luonnosmerkintä
        html = html.replace(
            '<link rel="canonical"',
            '<meta name="robots" content="noindex"><!-- POISTA-JULKAISTAESSA -->\n  <link rel="canonical"')

        # 6) Polut alikansiosta
        html = alikansiopolut(html)

        (OUT / f"{slug}.html").write_text(html, encoding="utf-8")
        print(f"  {num}  {slug}.html  ({len(html) // 1024} KB)")

    print(f"\nValmis: {len(PAGES)} luonnosta kansiossa {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    build()
