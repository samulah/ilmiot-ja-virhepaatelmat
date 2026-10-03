#!/usr/bin/env python3
"""Generoi luonnokset 15. kategorialle "Trollaus ja keskustelun sabotointi" (17 ilmiötä).

Tausta: sivustolla oli jo yksittäisiä keskustelun kaatamisen tekniikoita
(whataboutismi, argumenttitulva, maalitolppien siirtäminen, rage bait,
trollitehdas), mutta ei yhtään sivua sealioningista, JAQingista,
huolitrollauksesta, maalittamisesta — eikä trollauksesta itsestään. Vanhat
sivut jäävät kategorioihinsa; kategoriaessee linkittää ne naapureina.

Erän rakenne (28.9.2026 laajennettu 9 → 17):
  149-153  mekanismi ja motiivit: trollaus, verkon estottomuus (Suler 2004),
           pimeä tetradi (Buckels ym. 2014), kuka tahansa voi trollata
           (Cheng ym. 2017), "se oli vain vitsi"
  154-162  taktiikat, jotka näyttävät hyvältä keskustelulta (sealioning ...
           tone policing) sekä kafkatrapping, shitpostaus ja dunkkaus
  163-165  kohteena ihminen (maalittaminen, doksaus) ja vastakeino rajoineen

Numerot 149-165 olettavat, että valtapelit-erä (140-148) julkaistaan ensin.
index.html:ään EI kirjoiteta hub-lohkoa nyt, koska valtapelit-lohko on siellä
jo julkaisua odottamassa: toinen lohko ilman tiedostoja rikkoisi sen ajon.
Lohko kirjoitetaan valmiiksi tiedostoon luonnokset/trollaus-hub-lohko.html.

Julkaisu (valtapelien jälkeen): hub-lohko index.html:ään käsin, lisaa_ilmiot.py:n
UUDET-taulukko tällä erällä, sitten
    python3 scripts/lisaa_ilmiot.py --kortit-valmiina --kirjoita

Ajo:  python3 scripts/build_trollaus_luonnokset.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "darvo.html"
OUT = ROOT / "luonnokset"

PVM_ISO = "2026-09-28"
PVM_FI = "28.9.2026"

VANHA_SLUG = "darvo"
KAT_ID = "trollaus-ja-keskustelun-sabotointi"
KAT_NIMI = "Trollaus ja keskustelun sabotointi"
KAT_SIVU = f"kategoria-{KAT_ID}.html"
KAT_NRO = 15
KAT_KUVAUS = ("Miksi ihmiset trollaavat, ja miten keskustelu kaadetaan niin, että kaataja näyttää "
              "sen ainoalta asialliselta osapuolelta. Sealioning, kunhan kysyn, huolitrollaus, "
              "maalittaminen ja doksaus — ja mitä trollille kannattaa vastata, jos mitään.")

# edellinen erä (140-148) — uuden kategorian PREV-ketju kiinnittyy sen viimeiseen
EDELTAJA = ("harmaa-kivi", "Harmaa kivi — kun lähteminen ei ole vaihtoehto")

YHTEENSA = 165

# slug -> (numero, väri, nimi, kortin kuvaus)
OMAT_KORTIT = {
    # mekanismi ja motiivit
    "trollaus": (149, "#00838f", "Trollaus",
        "Provosointi, jonka palkkio on reaktio — ei se, kumpi on oikeassa."),
    "verkon-estottomuus": (150, "#00695c", "Verkon estottomuus",
        "Nimettömyys, näkymättömyys ja viive: miksi verkossa sanotaan, mitä kasvokkain ei sanottaisi."),
    "pimea-tetradi": (151, "#37474f", "Pimeä tetradi",
        "Narsismi, machiavellismi, psykopatia ja sadismi — ja se yksi, joka selittää trollausta parhaiten."),
    "kuka-tahansa-voi-trollata": (152, "#546e7a", "Kuka tahansa voi trollata",
        "Huono päivä ja valmiiksi myrkyllinen ketju riittävät: trollaus on myös tilanne, ei vain luonne."),
    "vain-vitsi": (153, "#8d6e63", "Se oli vain vitsi",
        "Ironia vastuun kiertämisenä: kommentti on vakava, jos se toimii, ja vitsi, jos siitä tulee seurauksia."),
    # taktiikat keskustelussa
    "sealioning": (154, "#006064", "Sealioning",
        "Kohtelias kysely, joka ei lopu koskaan: jokainen vastaus synnyttää uuden lähdepyynnön."),
    "kunhan-kysyn": (155, "#0277bd", "Kunhan kysyn",
        "Väite puetaan kysymykseksi, jolloin sitä ei tarvitse perustella eikä siitä voi joutua vastuuseen."),
    "huolitrollaus": (156, "#5d4037", "Huolitrollaus",
        "Vastustaja esiintyy huolestuneena kannattajana ja neuvoo luopumaan juuri siitä, mitä vastustaa."),
    "motte-and-bailey": (157, "#455a64", "Motte and bailey",
        "Rohkea väite pihalla, vaatimaton väite tornissa — ja perääntyminen aina kun joku kyseenalaistaa."),
    "nutpicking": (158, "#6a1b9a", "Nutpicking",
        "Vastapuolen hölmöin yksittäinen kommentti nostetaan koko joukon kasvoiksi."),
    "tone-policing": (159, "#ad1457", "Tone policing",
        "Keskustelu siirretään siihen, miten asia sanottiin — ettei tarvitse puhua siitä, mitä sanottiin."),
    "kafkatrapping": (160, "#4e342e", "Kafkatrapping",
        "Kiistäminen todistaa syyllisyyden: ansa, josta ei pääse ulos millään vastauksella."),
    "shitpostaus": (161, "#795548", "Shitpostaus",
        "Tahallisen arvotonta sisältöä niin paljon, ettei asiallista keskustelua enää löydä sen alta."),
    "dunkkaus": (162, "#d84315", "Dunkkaus ja ratio",
        "Lainausviestillä nolataan yleisön edessä — vastaus ei ole tarkoitettu sille, jolle se vastaa."),
    # kohteena ihminen ja vastakeino
    "maalittaminen": (163, "#c62828", "Maalittaminen",
        "Yksi osoittaa kohteen, joukko hoitaa loput: painostus, joka ei näytä kenenkään yksittäisen teolta."),
    "doksaus": (164, "#b71c1c", "Doksaus",
        "Henkilötiedot kaivetaan esiin ja julkaistaan: verkon riita siirtyy kotiovelle."),
    "trollin-ruokkiminen": (165, "#2e7d32", "Älä ruoki trollia",
        "Reaktio on trollin palkkio. Neuvo toimii yksittäiseen provosoijaan — ei maalittamiseen."),
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
    # 148 = 139 julkaistua + valtapelit-erän käsin kirjoitettu lohko
    assert len(kortit) >= 148, f"kortteja {len(kortit)}, odotettiin vähintään 148"
    return kortit


KORTIT = julkaistut_kortit()
# index.html:n korttijärjestys = sivuston IDS-järjestys ennen tätä erää
EDELLISET_IDS = list(KORTIT)
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



def lue_lisaa(kirjat, linkit):
    """Lue lisää -laatikko; kirjat = [(nimi, tekijä)], linkit = [(url, teksti)]."""
    osat = ['<div class="lue-lisaa">', '<div class="lue-lisaa-otsikko">Lue lisää</div>']
    if kirjat:
        osat += ['<div class="lue-lisaa-rivi">',
                 '<span class="lue-lisaa-tyyppi">Kirjoja ja tutkimuksia</span>',
                 '<ul class="lue-lisaa-lista">']
        osat += [f"<li><cite>{n}</cite> — {t}</li>" for n, t in kirjat]
        osat += ["</ul>", "</div>"]
    if linkit:
        osat += ['<div class="lue-lisaa-rivi">',
                 '<span class="lue-lisaa-tyyppi">Verkossa</span>',
                 '<ul class="lue-lisaa-lista">']
        osat += [f'<li><a href="{u}" target="_blank" rel="noopener">{t}</a></li>'
                 for u, t in linkit]
        osat += ["</ul>", "</div>"]
    osat.append("</div>")
    return "\n".join(osat)


# ────────────────────────── 149 · Trollaus ──────────────────────────
page("trollaus",
     "Trollaus — provosointi, jonka palkkio on reaktio",
     "Trollaus — mitä trollaus tarkoittaa ja miksi se toimii | Ilmiöitä",
     "Trollaus on tahallista provosointia, jonka tavoite on reaktio eikä keskustelu. Näin trolli tunnistetaan ja miksi väittely häviää aina.",
     [("Mitä trollaus tarkoittaa?",
       "Trollaus on tahallista provosointia verkkokeskustelussa. Trollin tavoite ei ole voittaa väittelyä eikä muuttaa kenenkään mieltä, vaan saada aikaan reaktio: suuttumusta, pitkiä vastineita ja riitaa muiden keskustelijoiden kesken. Siksi trollia ei voi voittaa perustelemalla — jokainen perusteellinen vastaus on juuri se, mitä hän tuli hakemaan."),
      ("Mistä sana trollaus tulee?",
       "Englannin trolling tarkoittaa alun perin vetouistelua: syötti vedetään veneen perässä ja katsotaan, mikä tarttuu. Usenet-keskusteluryhmissä 1990-luvun alussa sana alkoi tarkoittaa tahallista syöttiviestiä. Suomessa merkitys on sekoittunut tarinoiden peikkoon, mikä sopii kuvaan mutta ei ole sanan alkuperä."),
      ],
     r"""
<p><strong>Trollaus</strong> (engl. <em>trolling</em>) on tahallista provosointia, jonka tavoite ei ole voittaa keskustelua vaan saada aikaan <strong>reaktio</strong>. Trolli ei tarvitse olla oikeassa. Hän tarvitsee jonkun, joka suuttuu, kirjoittaa pitkän vastineen tai riitautuu muiden kanssa — ja jokainen niistä on onnistuminen.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Mistä sana trollaus tulee?</h2>
<p style="margin:0.4em 0 0;">Englannin <em>trolling</em> on vetouistelua: syötti vedetään veneen perässä ja katsotaan, mikä tarttuu. Usenet-ryhmissä 1990-luvun alussa sana alkoi tarkoittaa tahallista syöttiviestiä. Suomessa merkitys on sekoittunut tarinoiden peikkoon — osuva mielikuva, mutta ei sanan alkuperä.</p>
</div>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Miksi trolli voittaa, vaikka häviää väittelyn?</h2>
<ul style="margin:0.5em 0 0;">
<li><strong>Epäsymmetrinen työ:</strong> provokaation kirjoittaminen vie sekunnin, sen kumoaminen tunnin. Sama epäsuhta on <a href="brandolinin-laki.html">Brandolinin laissa</a>.</li>
<li><strong>Yleisö ratkaisee:</strong> trolli ei kirjoita vastaajalle vaan kaikille muille. Riita näyttää ulkopuolisesta kahdelta yhtä kiihtyneeltä osapuolelta.</li>
<li><strong>Alusta palkitsee:</strong> suuttumus tuottaa kommentteja, ja kommentit nostavat viestiä syötteessä — sama mekanismi kuin <a href="rage-bait.html">rage baitissa</a>.</li>
</ul>
</div>
<p>Buckelsin, Trapnellin ja Paulhusin (2014) kyselytutkimuksessa itse raportoitu trollaaminen oli yhteydessä erityisesti sadismiin (ks. <a href="pimea-tetradi.html">pimeä tetradi</a>): osalle trolleista toisen ahdistus on itse palkkio. Kaikki trollaus ei silti ole yksilön huvia — samaa tekniikkaa käytetään järjestelmällisesti <a href="trollitehdas.html">trollitehtaissa</a>.</p>
<div class="vaaralatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Kysy, mitä viestin kirjoittaja voittaisi, jos saisi vastauksen. Jos vastaus on "ei mitään muuta kuin sen, että joku vastasi", kyse on syötistä. Merkkejä ovat liioiteltu varmuus, kohteen valinta suurimman tunnelatauksen mukaan ja se, ettei mikään vastaus kelpaa. Älä väittele trollin kanssa trollin ehdoilla: kirjoita tarvittaessa yksi asiallinen oikaisu <em>muille lukijoille</em> ja jätä jatko väliin. Tarkemmin: <a href="trollin-ruokkiminen.html">älä ruoki trollia</a> — ja milloin se neuvo ei riitä.
    </div>
""" + lue_lisaa(
        [("This Is Why We Can't Have Nice Things", "Whitney Phillips (2015)"),
         ("Trolls just want to have fun", "Buckels, Trapnell &amp; Paulhus, <em>Personality and Individual Differences</em> (2014)")],
        [("https://en.wikipedia.org/wiki/Internet_troll", "Wikipedia: Internet troll (englanniksi)")]),
     ["verkon-estottomuus", "pimea-tetradi", "sealioning", "trollin-ruokkiminen", "trollitehdas"])


# ────────────────────────── 150 · Verkon estottomuus ──────────────────────────
page("verkon-estottomuus",
     "Verkon estottomuus — miksi ruudun takaa sanotaan enemmän",
     "Verkon estottomuus (online disinhibition effect) — mitä se tarkoittaa? | Ilmiöitä",
     "Verkon estottomuus (engl. online disinhibition effect) selittää, miksi verkossa sanotaan asioita, joita kasvokkain ei sanottaisi. Suler 2004, suomeksi.",
     [("Mitä online disinhibition effect tarkoittaa?",
       "Online disinhibition effect eli verkon estottomuus tarkoittaa, että ihmiset sanovat ja tekevät verkossa asioita, joita he eivät tekisi kasvokkain. Psykologi John Suler kuvasi ilmiön vuonna 2004 ja erotti siitä kaksi puolta: hyvänlaatuisen, jossa ihminen uskaltaa kertoa itsestään avoimemmin, ja myrkyllisen, jossa hän loukkaa, uhkaa tai provosoi."),
      ("Mistä verkon estottomuus johtuu?",
       "Suler nimesi kuusi tekijää: nimettömyys, näkymättömyys, viive vastauksessa, kuvitelma toisen äänestä omassa päässä, tunne siitä että verkko on eri maailma kuin arki, ja auktoriteettien heikompi näkyvyys. Tärkein havainto on, että useimmat tekijät toimivat myös omalla nimellä kirjoitettaessa — nimettömyyden poistaminen ei siksi yksin poista ilmiötä."),
      ],
     r"""
<p><strong>Verkon estottomuus</strong> (engl. <em>online disinhibition effect</em>) tarkoittaa, että ihminen sanoo ruudun takaa asioita, joita ei sanoisi kasvokkain. Psykologi John Suler kuvasi ilmiön vuonna 2004. Hän huomautti, että se toimii kumpaankin suuntaan: sama estojen höltyminen, joka saa jonkun kertomaan vaikeasta asiasta avoimesti, saa toisen kirjoittamaan asioita, joista hän kasvokkain vaikenisi.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Miksi verkossa uskalletaan enemmän?</h2>
<p style="margin:0.4em 0 0;">Kasvokkain puhetta ohjaa jatkuva palaute: ilme, äänensävy ja hiljaisuus kertovat heti, meneekö jokin liian pitkälle. Verkossa tämä palautesilmukka puuttuu. Kirjoittaja ei näe, miltä viesti tuntuu, eikä hänen tarvitse katsoa vastaanottajaa silmiin.</p>
</div>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Sulerin tekijöistä tärkeimmät:</h2>
<ul style="margin:0.5em 0 0;">
<li><strong>Näkymättömyys:</strong> toisen reaktiota ei näe, eikä omaa kasvoa tarvitse näyttää.</li>
<li><strong>Viive:</strong> vastaus tulee myöhemmin tai ei ollenkaan, joten viestin voi "heittää ja lähteä".</li>
<li><strong>Nimettömyys:</strong> teko ei tunnu omalta, kun se ei kulje omalla nimellä.</li>
<li><strong>Eri maailma:</strong> verkko tuntuu peliltä, jonka säännöt eivät koske arkea.</li>
</ul>
</div>
<p>Olennaista on, että useimmat tekijät toimivat <strong>myös omalla nimellä</strong>. Siksi nimettömyyden kieltäminen ei yksin poista ilmiötä — myrkyllisiä kommentteja kirjoitetaan runsaasti myös omilla kasvoilla. Estottomuus selittää, miksi <a href="kuka-tahansa-voi-trollata.html">kuka tahansa voi trollata</a>, ei vain ne, joilla on <a href="pimea-tetradi.html">pimeitä piirteitä</a>.</p>
<div class="vaaralatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Itsessään ilmiön huomaa kysymällä: <em>sanoisinko tämän ääneen, jos hän istuisi vastapäätä?</em> Jos et, viesti on kirjoitettu estottomuuden varassa. Kirjoita kiukkuinen vastaus luonnokseksi ja lue se tunnin päästä. Muiden kohdalla ilmiö auttaa suhteuttamaan: raju kommentti kertoo usein enemmän välineestä kuin kirjoittajan todellisesta kannasta — mikä ei tee siitä hyväksyttävää, mutta tekee siitä vähemmän henkilökohtaista.
    </div>
""" + lue_lisaa(
        [("The Online Disinhibition Effect", "John Suler, <em>CyberPsychology &amp; Behavior</em> (2004)")],
        [("https://en.wikipedia.org/wiki/Online_disinhibition_effect", "Wikipedia: Online disinhibition effect (englanniksi)")]),
     ["trollaus", "kuka-tahansa-voi-trollata", "pimea-tetradi", "vain-vitsi", "rage-bait"])


# ────────────────────────── 151 · Pimeä tetradi ──────────────────────────
page("pimea-tetradi",
     "Pimeä tetradi — narsismi, machiavellismi, psykopatia ja sadismi",
     "Pimeä tetradi ja trollaus — mitä tutkimus sanoo? | Ilmiöitä",
     "Pimeä tetradi (engl. dark tetrad) kokoaa neljä persoonallisuuspiirrettä. Tutkimuksessa trollaamista selitti niistä parhaiten sadismi. Näin tulos luetaan oikein.",
     [("Mitä pimeä tetradi tarkoittaa?",
       "Pimeä tetradi on persoonallisuuspsykologian käsite neljälle haitalliselle piirteelle: narsismi, machiavellismi, psykopatia ja arkipäiväinen sadismi. Kolme ensimmäistä muodostavat pimeän triadin (Paulhus ja Williams 2002); sadismi lisättiin myöhemmin neljänneksi. Kyse on piirteistä, joita kaikilla on jonkin verran, ei diagnooseista."),
      ("Ovatko trollit sadisteja?",
       "Buckelsin, Trapnellin ja Paulhusin kyselytutkimuksessa (2014) itse raportoitu trollaamisesta nauttiminen oli yhteydessä erityisesti arkipäiväiseen sadismiin — vahvemmin kuin muihin pimeisiin piirteisiin. Tulos koskee osaa trolleista ja perustuu vastaajien omaan ilmoitukseen. Se ei tarkoita, että jokainen provosoiva kommentoija olisi sadisti."),
      ],
     r"""
<p><strong>Pimeä tetradi</strong> (engl. <em>dark tetrad</em>) on persoonallisuuspsykologian nimitys neljälle haitalliselle piirteelle: <strong>narsismi</strong>, <strong>machiavellismi</strong>, <strong>psykopatia</strong> ja <strong>arkipäiväinen sadismi</strong>. Kolme ensimmäistä muodostavat Paulhusin ja Williamsin (2002) <em>pimeän triadin</em>; sadismi lisättiin myöhemmin neljänneksi. Kaikilla on piirteitä jonkin verran — kyse on asteikosta, ei diagnoosista.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Mikä piirre selittää trollausta?</h2>
<p style="margin:0.4em 0 0;">Buckelsin, Trapnellin ja Paulhusin (2014) kyselyssä trollaamisesta nauttiminen oli yhteydessä kaikkiin pimeisiin piirteisiin paitsi narsismiin, ja vahvimmin <strong>sadismiin</strong>. Tutkijoiden tiivistys oli, että trollit "haluavat vain pitää hauskaa" — ja että hauskuus on toisen ahdistus.</p>
</div>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Neljä piirrettä lyhyesti:</h2>
<ul style="margin:0.5em 0 0;">
<li><strong>Narsismi:</strong> ihailun tarve ja oman erinomaisuuden tunne.</li>
<li><strong>Machiavellismi:</strong> muiden laskelmoiva käyttäminen omiin tavoitteisiin.</li>
<li><strong>Psykopatia:</strong> impulsiivisuus ja empatian puute.</li>
<li><strong>Sadismi:</strong> mielihyvä toisen kärsimyksestä.</li>
</ul>
</div>
<p>Tulosta on helppo lukea väärin. Se kertoo, keille trollaaminen on <em>mieluisaa</em>, ei sitä, keitä kaikki trollit ovat. <a href="kuka-tahansa-voi-trollata.html">Chengin ym. (2017) koe</a> näytti, että tavallinenkin ihminen trollaa huonona päivänä ja huonossa ketjussa. Luonne ja tilanne selittävät eri osan ilmiöstä.</p>
<div class="vaaralatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Käytännön seuraus on yksinkertainen: jos kirjoittaja nauttii reaktiostasi, <strong>perustelu ei auta</strong>, koska hän ei ole keskustelemassa. Merkkejä ovat ilahtuminen vastapuolen suuttumuksesta ja kiinnostuksen katoaminen heti, kun reaktio loppuu. Silloin paras vastaus on <a href="trollin-ruokkiminen.html">jättää palkkio antamatta</a>. Älä kuitenkaan diagnosoi ketään kommentin perusteella: "psykopaatti" on haukkumasana, ei havainto, ja se tekee keskustelusta yhtä huonon kuin trolli.
    </div>
""" + lue_lisaa(
        [("Trolls just want to have fun", "Buckels, Trapnell &amp; Paulhus, <em>Personality and Individual Differences</em> (2014)"),
         ("The Dark Triad of personality", "Paulhus &amp; Williams, <em>Journal of Research in Personality</em> (2002)")],
        [("https://en.wikipedia.org/wiki/Dark_triad", "Wikipedia: Dark triad (englanniksi)")]),
     ["trollaus", "kuka-tahansa-voi-trollata", "verkon-estottomuus", "gaslighting", "darvo"])


# ────────────────────────── 152 · Kuka tahansa voi trollata ──────────────────────────
page("kuka-tahansa-voi-trollata",
     "Kuka tahansa voi trollata — huono päivä ja huono ketju",
     "Kuka tahansa voi trollata — miksi tavalliset ihmiset trollaavat? | Ilmiöitä",
     "Chengin ym. (2017) kokeessa huono mieliala ja myrkyllinen keskusteluketju lähes kaksinkertaistivat trollikommentit. Trollaus on myös tilanne, ei vain luonne.",
     [("Miksi tavalliset ihmiset trollaavat?",
       "Stanfordin ja Cornellin tutkijoiden kokeessa (Cheng ym. 2017) kaksi tilannetekijää lisäsi trollausta: huono mieliala ja se, että keskusteluketjussa oli jo valmiiksi trollikommentteja. Kun molemmat olivat läsnä, trollikommenttien osuus oli lähes kaksinkertainen verrokkiryhmään nähden. Trollaus ei siis ole vain pienen joukon ominaisuus."),
      ("Levittääkö trollaus itseään?",
       "Kyllä. Samassa tutkimuksessa aiemmat trollikommentit ketjussa lisäsivät uusien trollikommenttien todennäköisyyttä. Havaintoaineistossa trollaus myös yleistyi myöhään illalla ja alkuviikosta, jolloin ihmisten mieliala on keskimäärin heikompi. Siksi yksittäisen myrkyllisen viestin poistaminen varhain voi muuttaa koko ketjun sävyn."),
      ],
     r"""
<p>On houkuttelevaa ajatella, että trollit ovat erillinen joukko ihmisiä, joilla on <a href="pimea-tetradi.html">pimeitä piirteitä</a>. Stanfordin ja Cornellin tutkijoiden tutkimus <cite>Anyone Can Become a Troll</cite> (Cheng ym. 2017) näytti, että kuva on puutteellinen: <strong>tavallinen ihminen trollaa oikeissa olosuhteissa</strong>. Kaksi olosuhdetta riitti.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Mitkä tekijät saavat tavallisen ihmisen trollaamaan?</h2>
<p style="margin:0.4em 0 0;">Kokeessa osa osallistujista sai ensin vaikean tehtävän, joka huononsi mielialaa, ja osa näki keskusteluketjun, jossa oli jo trollikommentteja. Kun <strong>huono mieliala</strong> ja <strong>huono ketju</strong> yhdistyivät, trollikommenttien osuus oli lähes kaksinkertainen verrokkeihin nähden.</p>
</div>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Mitä tästä seuraa:</h2>
<ul style="margin:0.5em 0 0;">
<li><strong>Trollaus tarttuu:</strong> ensimmäinen myrkyllinen viesti tekee seuraavista todennäköisempiä.</li>
<li><strong>Kellonaika näkyy:</strong> tutkijoiden havaintoaineistossa trollaus yleistyi myöhään illalla ja alkuviikosta.</li>
<li><strong>Moderointi kannattaa varhain:</strong> ketjun sävy asettuu ensimmäisten kommenttien mukaan.</li>
</ul>
</div>
<p>Tulos täydentää <a href="verkon-estottomuus.html">verkon estottomuutta</a>: väline höllentää estoja, mieliala antaa syyn ja ketju näyttää, mikä on sallittua. Sama tartuntamekanismi tekee <a href="rage-bait.html">rage baitista</a> tehokasta.</p>
<div class="vaaralatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Omalla kohdalla: jos olet väsynyt tai ärtynyt ja ketju on jo kiehuvaa, <strong>älä kommentoi nyt</strong>. Juuri se yhdistelmä tuottaa viestit, joita kaduttaa. Ylläpitäjälle: poista tai piilota ensimmäinen myrkyllinen kommentti nopeasti, koska se määrää ketjun normin. Keskustelijalle: yksi asiallinen vastaus aikaisessa vaiheessa voi kääntää sävyn — myöhemmin se hukkuu. Ja muiden kohdalla: ilkeä kommentti ei välttämättä kerro ihmisestä, vaan hänen päivästään.
    </div>
""" + lue_lisaa(
        [("Anyone Can Become a Troll: Causes of Trolling Behavior in Online Discussions",
          "Cheng, Bernstein, Danescu-Niculescu-Mizil &amp; Leskovec, CSCW (2017)")],
        []),
     ["verkon-estottomuus", "pimea-tetradi", "trollaus", "rage-bait", "kaikukammio"])


# ────────────────────────── 153 · Se oli vain vitsi ──────────────────────────
page("vain-vitsi",
     "Se oli vain vitsi — ironia vastuun kiertämisenä",
     "”Se oli vain vitsi” — kun ironia suojaa vastuulta | Ilmiöitä",
     "”Se oli vain vitsi” on trollin suojakilpi: kommentti on tosissaan, jos se toimii, ja vitsi, jos siitä tulee seurauksia. Näin ironiakilven tunnistaa.",
     [("Mitä tarkoittaa, että ironia on suojakilpi?",
       "Ironiakilvessä sama kommentti voidaan jälkikäteen tulkita kahdella tavalla sen mukaan, miten se otettiin vastaan. Jos yleisö innostuu, kirjoittaja oli tosissaan. Jos tulee kritiikkiä, kyse oli vitsistä ja kriitikko on huumorintajuton. Kirjoittaja pääsee sanomaan asian joutumatta vastaamaan siitä."),
      ("Miten erottaa vitsin ja ironiakilven?",
       "Aidosta vitsistä voi kertoa, mikä siinä oli hauskaa, eikä sen kohde ole sattumalta sama kuin kirjoittajan tosissaan esittämät kannat. Ironiakilven tunnistaa siitä, että vitsi osuu toistuvasti samaan suuntaan ja että 'vitsi'-selitys ilmestyy vasta kritiikin jälkeen."),
      ],
     r"""
<p><strong>"Se oli vain vitsi"</strong> on trollin tavallisin suojakilpi. Kommentti kirjoitetaan niin, että sen voi jälkikäteen lukea kahdella tavalla: <strong>vakavana, jos se toimii</strong>, ja <strong>vitsinä, jos siitä tulee seurauksia</strong>. Englanninkielisessä netissä ilmiöllä on puolivakava nimi <em>Schrödinger's douchebag</em> — kommentin luonne ratkeaa vasta, kun yleisön reaktio nähdään.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Miksi ironia on niin hyvä suoja?</h2>
<p style="margin:0.4em 0 0;">Koska kritiikki kääntyy kriitikkoa vastaan. Joka tarttuu "vitsiin", on huumorintajuton; joka ei tartu, antaa sen olla. Whitney Phillips (2015) kuvasi trollikulttuurin <em>lulz</em>-huumoria juuri näin: huvi syntyy siitä, että joku ottaa asian vakavasti.</p>
</div>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Tuttuja muotoja:</h2>
<ul style="margin:0.5em 0 0;">
<li><em>"Eikö täällä enää saa edes vitsailla?"</em> — kritiikki kehystetään huumorin kieltämiseksi.</li>
<li><strong>Meemi:</strong> kuvan ja tekstin yhdistelmä, jossa viesti on selvä mutta kukaan ei ole sanonut sitä suoraan.</li>
<li><strong>Liioittelu:</strong> kanta esitetään niin räikeänä, että sen voi aina kiistää parodiana.</li>
</ul>
</div>
<p>Ironiakilpi toimii, koska verkossa vilpitöntä ja parodiaa on usein mahdoton erottaa — tämä on <a href="poen-laki.html">Poen laki</a>. Trolli hyödyntää sitä tahallaan. Sukua on <a href="kunhan-kysyn.html">kunhan kysyn</a>: kummassakin viesti välitetään muodossa, josta ei voi joutua vastuuseen.</p>
<div class="vaaralatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Katso <strong>suuntaa ja ajoitusta</strong>. Jos "vitsit" osuvat toistuvasti samaan kohteeseen ja "vitsi"-selitys ilmestyy vasta kritiikin jälkeen, kyse on kilvestä. Älä väittele siitä, oliko se hauska — se on keskustelu, jonka trolli voittaa. Kysy sen sijaan sisällöstä: <em>"Selvä, vitsi. Mitä mieltä olet asiasta tosissasi?"</em> Muista myös, että aito huumori ja satiiri ovat arvokkaita: kilven tunnistaa toistosta, ei yksittäisestä kärkevästä heitosta.
    </div>
""" + lue_lisaa(
        [("This Is Why We Can't Have Nice Things", "Whitney Phillips (2015)")],
        []),
     ["poen-laki", "kunhan-kysyn", "trollaus", "motte-and-bailey", "verkon-estottomuus"])


# ────────────────────────── 154 · Sealioning ──────────────────────────
page("sealioning",
     "Sealioning — kohtelias kysely, joka ei lopu koskaan",
     "Sealioning (merileijonointi) — mitä se tarkoittaa? | Ilmiöitä",
     "Sealioning eli merileijonointi on kohteliaalta näyttävää loputonta lähteiden ja perustelujen vaatimista. Näin tunnistat taktiikan ja lopetat sen.",
     [("Mitä sealioning tarkoittaa?",
       "Sealioning eli merileijonointi on keskustelutaktiikka, jossa joku vaatii kohteliaasti ja sitkeästi lähteitä, määritelmiä ja perusteluja väitteelle, johon hän ei aio suostua missään tapauksessa. Jokainen vastaus synnyttää uuden kysymyksen. Kohteliaisuus on taktiikan ydin: kun kohde lopulta tuskastuu, hän näyttää yleisön silmissä siltä, joka ei kestä asiallista keskustelua."),
      ("Mistä sealioning-termi tulee?",
       "Termi tulee David Malkin Wondermark-sarjakuvasta vuodelta 2014. Siinä merileijona kuulee pariskunnan sanovan, ettei pidä merileijonista, ja seuraa heitä sen jälkeen kaikkialle kohteliaasti vaatien perusteluja. Sarjakuva levisi saman vuoden verkkokiistojen aikana, ja nimi vakiintui englanninkieliseen keskusteluun."),
      ],
     r"""
<p><strong>Sealioning</strong> eli <strong>merileijonointi</strong> on taktiikka, jossa joku vaatii kohteliaasti ja väsymättä lähteitä, määritelmiä ja perusteluja — ei siksi, että aikoisi muuttaa kantaansa, vaan siksi, että vaatiminen itsessään kuluttaa vastapuolen. Jokainen vastaus avaa uuden kysymyksen, eikä yksikään vastaus riitä.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Mistä nimi merileijona tulee?</h2>
<p style="margin:0.4em 0 0;">David Malkin <cite>Wondermark</cite>-sarjakuvassa (2014) pariskunta mainitsee, ettei pidä merileijonista. Merileijona seuraa heitä kotiin asti, kohteliaasti: <em>"Anteeksi, voisitteko perustella?"</em> Nimi tarttui, koska kuva on tarkka: ongelma ei ole kysymys vaan se, ettei kysyjä lähde.</p>
</div>
<div class="mermaid">
flowchart LR
  K["Kohtelias kysymys"] --&gt; V["Perusteltu vastaus"]
  V --&gt; U["Uusi kysymys\n'entä tämä lähde?'"]
  U --&gt; V
  U --&gt; T["Kohde tuskastuu"]
  T --&gt; L["Yleisö näkee:\nkysyjä asiallinen,\nkohde vihainen"]
  style T fill:#fdf0f0,stroke:#c0392b
  style L fill:#fff3cd,stroke:#f39c12
    </div>
<p class="kaavio-selitys">Kehä päättyy vasta kun kohde menettää malttinsa — ja silloin kysyjä on voittanut.</p>
<p>Taktiikka toimii, koska se matkii hyvää keskustelua. Lähteiden kysyminen on hyve, ja kieltäytyminen näyttää ulkopuolisesta välttelyltä. Epäsymmetria on sama kuin <a href="argumenttitulva.html">argumenttitulvassa</a>: kysyä voi sekunnissa, vastaaminen vie illan. Usein kysymykset myös siirtyvät vaivihkaa aina uuteen kohtaan, kuten <a href="maalitolppien-siirtaminen.html">maalitolppien siirtämisessä</a>.</p>
<div class="vaaralatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Kysy itseltäsi: onko kysyjä reagoinut yhteenkään jo annettuun vastaukseen? Jos hän ei ole myöntänyt mitään eikä kiistänyt mitään, vaan vain kysynyt lisää, keskustelu ei etene. Vastakeino on kääntää pyyntö: <em>"Mikä näyttö muuttaisi kantasi?"</em> Aito kysyjä osaa vastata, merileijona ei. Voit myös vastata kerran kattavasti ja sanoa ääneen, ettet jatka — perustelu jää muiden luettavaksi. Muista silti, että useimmat lähdepyynnöt ovat aitoja: merileijonan tunnistaa toistosta, ei yksittäisestä kysymyksestä.
    </div>
""" + lue_lisaa(
        [],
        [("https://en.wikipedia.org/wiki/Sealioning", "Wikipedia: Sealioning (englanniksi)")]),
     ["trollaus", "kunhan-kysyn", "argumenttitulva", "maalitolppien-siirtaminen", "brandolinin-laki"])


# ────────────────────────── 155 · Kunhan kysyn ──────────────────────────
page("kunhan-kysyn",
     "Kunhan kysyn — väite kysymyksen muodossa",
     "Kunhan kysyn (just asking questions) — väite kysymyksenä | Ilmiöitä",
     "Kunhan kysyn -taktiikka (engl. just asking questions, JAQing) esittää väitteen kysymyksenä, jolloin sitä ei tarvitse perustella. Näin sen tunnistaa.",
     [("Mitä just asking questions tarkoittaa?",
       "Just asking questions eli JAQing on taktiikka, jossa väite esitetään kysymyksen muodossa: 'Eikö ole outoa, että…?' tai 'Kysyn vain, kuka tästä hyötyy.' Kysymys istuttaa ajatuksen kuulijan mieleen, mutta kysyjä voi aina vetäytyä: hänhän ei väittänyt mitään. Vastuu näytöstä siirtyy vastaajalle."),
      ("Onko kysyminen aina tätä taktiikkaa?",
       "Ei. Aito kysyjä haluaa vastauksen ja muuttaa käsitystään sen perusteella. Taktiikan tunnistaa siitä, että vastaus ei kelpaa: kysymys toistetaan tai tilalle tulee uusi, samaan suuntaan johdatteleva kysymys."),
      ],
     r"""
<p><strong>Kunhan kysyn</strong> (engl. <em>just asking questions</em>, lyhenne <em>JAQing</em>) on tekniikka, jossa väite puetaan kysymykseksi. <em>"Eikö ole outoa, että rokotteiden jälkeen…?" "Kysyn vain, kuka tästä oikeasti hyötyy."</em> Kysymys istuttaa ajatuksen, mutta kysyjä ei ole väittänyt mitään — eikä siksi joudu perustelemaan mitään.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Miksi kysymys toimii paremmin kuin väite?</h2>
<p style="margin:0.4em 0 0;">Väite herättää vastaväitteen, kysymys uteliaisuuden. Kuulija täydentää vastauksen itse, ja itse keksitty johtopäätös tuntuu omalta. Samalla <strong>todistustaakka kääntyy</strong>: vastaajan on osoitettava, ettei vihjattu asia pidä paikkaansa, vaikka kukaan ei ole osoittanut, että se pitäisi.</p>
</div>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Tuttuja muotoja:</h2>
<ul style="margin:0.5em 0 0;">
<li><strong>Otsikkona:</strong> <em>"Salaako ministeriö jotain?"</em> Kysymysotsikkoihin pätee usein <a href="betteridgen-laki.html">Betteridgen laki</a>: vastaus on ei.</li>
<li><strong>Keskustelussa:</strong> <em>"En väitä mitään, mutta eikö tämä ole vähän kummallista?"</em></li>
<li><strong>Perääntyessä:</strong> <em>"Eikö enää saa edes kysyä?"</em> — kritiikki kehystetään kysymisen kieltämiseksi.</li>
</ul>
</div>
<p>Tekniikka on <a href="sealioning.html">sealioningin</a> sisar. Merileijona kysyy väsyttääkseen, kunhan-kysyjä kysyäkseen vihjatakseen. Molemmat hyödyntävät sitä, että kysymistä pidetään lähtökohtaisesti viattomana.</p>
<div class="vaaralatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Käännä kysymys väitteeksi ja katso, kestääkö se: <em>"Kysytkö siis, vai väitätkö, että ministeriö salaa jotain? Jos väität, mihin perustat sen?"</em> Aito kysyjä hyväksyy vastauksen, taktikko toistaa kysymyksen toisin sanoin. Älä myöskään toista vihjausta kumotessasi sitä otsikkoon tai ensimmäiseen virkkeeseen — kiistäminenkin painaa kysymyksen muistiin. Kerro ensin, mikä pitää paikkansa.
    </div>
""" + lue_lisaa(
        [],
        [("https://en.wikipedia.org/wiki/Just_asking_questions", "Wikipedia: Just asking questions (englanniksi)")]),
     ["sealioning", "motte-and-bailey", "betteridgen-laki", "klikkiotsikko", "firehose-of-falsehood"])


# ────────────────────────── 156 · Huolitrollaus ──────────────────────────
page("huolitrollaus",
     "Huolitrollaus — vastustaja esiintyy huolestuneena ystävänä",
     "Huolitrollaus (concern trolling) — mitä se tarkoittaa? | Ilmiöitä",
     "Huolitrollaus (engl. concern trolling) tarkoittaa vastustajaa, joka esiintyy huolestuneena kannattajana ja neuvoo luopumaan tavoitteesta. Näin sen tunnistaa.",
     [("Mitä concern trolling eli huolitrollaus tarkoittaa?",
       "Huolitrollaus on taktiikka, jossa asian vastustaja esiintyy sen kannattajana tai huolestuneena sivullisena. Hän ei vastusta tavoitetta suoraan, vaan on 'huolissaan' siitä, että liike menee liian pitkälle, karkottaa kannattajia tai vahingoittaa omaa asiaansa. Neuvo on aina sama: hiljennä, hidasta tai luovu."),
      ("Miten huolitrollauksen erottaa aidosta kritiikistä?",
       "Aito sisäinen kritiikki ehdottaa parempaa tapaa päästä samaan tavoitteeseen. Huolitrollaus ehdottaa vain vähemmän: jokainen neuvo johtaa siihen, että tavoitteesta luovutaan tai sitä lykätään. Toinen merkki on se, ettei huolestunut ole koskaan tehnyt mitään asian hyväksi."),
      ],
     r"""
<p><strong>Huolitrollaus</strong> (engl. <em>concern trolling</em>) on taktiikka, jossa asian vastustaja esiintyy huolestuneena kannattajana. Hän ei sano vastustavansa tavoitetta — hän on vain <em>huolissaan</em>: että liike menee liian pitkälle, että se karkottaa tavalliset ihmiset tai että tämä tyyli vahingoittaa lopulta asiaa itseään.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Miksi huoli on tehokkaampi kuin vastustus?</h2>
<p style="margin:0.4em 0 0;">Suora vastustaja saa vastaansa perustelut. Huolestunut ystävä saa kuulijan epäröimään, koska hän näyttää olevan samalla puolella. Termi yleistyi 2000-luvun puolivälin yhdysvaltalaisilla poliittisilla blogeilla, joilla vastapuolen kirjoittajat esiintyivät kommenteissa pettyneinä kannattajina.</p>
</div>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Tyypillisiä repliikkejä:</h2>
<ul style="margin:0.5em 0 0;">
<li><em>"Kannatan kyllä tasa-arvoa, mutta tällainen meno vain lisää vastareaktiota."</em></li>
<li><em>"Olen itsekin huolissani ilmastosta, mutta nämä mielenosoitukset kääntävät ihmiset asiaa vastaan."</em></li>
<li><em>"Sanon tämän ystävänä: kannattaisiko odottaa parempaa hetkeä?"</em></li>
</ul>
</div>
<p>Kuvio on sukua <a href="tone-policing.html">tone policingille</a>: kummassakin puhutaan siitä, miten tavoitetta ajetaan, jottei tarvitse puhua itse tavoitteesta. Verkossa huolitrollaus yhdistyy usein valeprofiileihin, jolloin se lähestyy <a href="astroturf.html">astroturfia</a>.</p>
<div class="vaaralatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Katso, mihin suuntaan neuvot johtavat. Aito sisäinen kritiikki ehdottaa <em>parempaa</em> tapaa päästä samaan tavoitteeseen; huolitrollaus ehdottaa aina <em>vähemmän</em> — hiljempaa, hitaammin, myöhemmin, ei nyt. Kysy suoraan: <em>"Mikä olisi sinusta oikea tapa ajaa tätä asiaa?"</em> Jos vastausta ei tule, huoli ei koske tapaa vaan asiaa. Muista kuitenkin, että kannattajien oma taktiikkakritiikki on usein aiheellista — tunnusmerkki on neuvon suunta, ei se, että joku ylipäätään kritisoi.
    </div>
""" + lue_lisaa(
        [],
        [("https://en.wikipedia.org/wiki/Concern_troll", "Wikipedia: Concern troll (englanniksi)")]),
     ["tone-policing", "trollaus", "astroturf", "hyvesignalointi", "whataboutismi"])


# ────────────────────────── 157 · Motte and bailey ──────────────────────────
page("motte-and-bailey",
     "Motte and bailey — rohkea väite, turvallinen perääntymistie",
     "Motte and bailey -argumentti — mitä se tarkoittaa? | Ilmiöitä",
     "Motte and bailey on argumentointitaktiikka, jossa rohkea väite vaihtuu kiistattomaan heti kun sitä haastetaan — ja palaa takaisin kun paine hellittää.",
     [("Mitä motte and bailey tarkoittaa?",
       "Motte and bailey on argumentointitaktiikka, jossa puhuja esittää kaksi väitettä samalla nimellä: rohkean ja kiistanalaisen (bailey eli piha) sekä vaatimattoman ja lähes kiistattoman (motte eli torni). Haastettaessa hän perääntyy vaatimattomaan versioon ja väittää, ettei ole tarkoittanut muuta. Kun kriitikko lähtee, rohkea versio palaa käyttöön."),
      ("Kuka keksi motte and bailey -käsitteen?",
       "Filosofi Nicholas Shackel kuvasi taktiikan vuonna 2005 artikkelissa The Vacuity of Postmodernist Methodology. Laajemmin tunnetuksi sen teki Scott Alexanderin blogi Slate Star Codex vuonna 2014."),
      ],
     r"""
<p><strong>Motte and bailey</strong> on argumentointitaktiikka, jossa samalla nimellä kulkee kaksi väitettä: <strong>rohkea ja kiistanalainen</strong> sekä <strong>vaatimaton ja lähes kiistaton</strong>. Rohkeaa käytetään, kun kukaan ei vastusta. Kun joku haastaa, puhuja perääntyy vaatimattomaan ja kysyy loukkaantuneena, eihän kukaan voi olla tästä eri mieltä.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Mistä nimi tulee?</h2>
<p style="margin:0.4em 0 0;">Nimi on keskiaikaisesta linnatyypistä (suom. <em>motte-and-bailey-linna</em>): <em>bailey</em> on viljelty, mutta huonosti puolustettava piha, <em>motte</em> sen keskellä oleva kumpu ja torni, johon vetäydytään hyökkäyksen tullen. Filosofi Nicholas Shackel käytti vertausta vuonna 2005; laajalle sen levitti Scott Alexanderin blogi 2014.</p>
</div>
<div class="mermaid">
flowchart LR
  B["Piha: 'Luontaistuote X\nparantaa syövän'"] -- "haaste" --&gt; M["Torni: 'Tarkoitin vain,\nettä hyvinvointi auttaa jaksamaan'"]
  M -- "kriitikko lähtee" --&gt; B
  style B fill:#fdf0f0,stroke:#c0392b
  style M fill:#fff3cd,stroke:#f39c12
    </div>
<p class="kaavio-selitys">Tornia puolustetaan, mutta pihalla eletään.</p>
<p>Taktiikka on tehokas, koska kriitikko näyttää hyökkäävän itsestäänselvyyttä vastaan. Sen peilikuva on <a href="nutpicking.html">nutpicking</a>, jossa vastapuolen heikoin versio esitetään koko joukon kantana. Mottessa taas oma heikoin kohta piilotetaan vahvimman taakse.</p>
<div class="vaaralatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Merkki on se, että väitteen sisältö <strong>muuttuu kritiikin mukana</strong> mutta nimi pysyy samana. Vastakeino on erottaa versiot ääneen: <em>"Olen samaa mieltä siitä, että hyvinvointi auttaa jaksamaan. Väitätkö myös, että tuote parantaa syövän?"</em> Myönnä torni ja pyydä kantaa pihaan. Jos keskustelija ei suostu sitoutumaan kumpaankaan, se kertoo, kumpaa hän oikeasti ajaa.
    </div>
""" + lue_lisaa(
        [("The Vacuity of Postmodernist Methodology", "Nicholas Shackel, <em>Metaphilosophy</em> (2005)")],
        [("https://en.wikipedia.org/wiki/Motte-and-bailey_fallacy", "Wikipedia: Motte-and-bailey fallacy (englanniksi)")]),
     ["nutpicking", "kunhan-kysyn", "vain-vitsi", "kafkatrapping", "maalitolppien-siirtaminen"])


# ────────────────────────── 158 · Nutpicking ──────────────────────────
page("nutpicking",
     "Nutpicking — vastapuolen hölmöin edustaja koko joukon kasvoiksi",
     "Nutpicking — kun hölmöin kommentti esitetään koko joukon kantana | Ilmiöitä",
     "Nutpicking on taktiikka, jossa vastapuolen hölmöin yksittäinen kommentti nostetaan esiin kuin se edustaisi koko joukkoa. Näin sen tunnistaa.",
     [("Mitä nutpicking tarkoittaa?",
       "Nutpicking on taktiikka, jossa vastapuolen joukosta poimitaan hölmöin, äärimmäisin tai vihaisin yksittäinen kommentti ja esitetään se ikään kuin koko ryhmän kantana. Nimi on sanaleikki englannin sanoista nut (hörhö) ja cherry-picking (rusinoiden poiminta). Termin otti käyttöön toimittaja Kevin Drum vuonna 2006."),
      ("Miten nutpicking eroaa olkiukosta?",
       "Olkiukossa vastapuolen kanta keksitään tai vääristetään. Nutpickingissa kommentti on aito — joku todella sanoi sen — mutta sen edustavuus on keksitty. Siksi nutpicking on vaikeampi kumota: yksittäinen esimerkki pitää paikkansa."),
      ],
     r"""
<p><strong>Nutpicking</strong> on taktiikka, jossa vastapuolen joukosta poimitaan hölmöin, äärimmäisin tai vihaisin yksittäinen kommentti — ja esitetään se kuin se olisi koko joukon kanta. Nimi on sanaleikki: <em>nut</em> (hörhö) + <em>cherry-picking</em> (rusinoiden poiminta). Termin otti käyttöön yhdysvaltalainen toimittaja Kevin Drum vuonna 2006.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Miksi nutpicking on niin helppoa?</h2>
<p style="margin:0.4em 0 0;">Jokaisessa isossa joukossa on joku, joka sanoo jotain typerää. Verkossa se on myös aina löydettävissä ja kuvakaappattavissa. Esimerkki on <strong>aito</strong> — siksi sitä on vaikea kiistää. Keksitty on vain sen edustavuus.</p>
</div>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Näin se näkyy:</h2>
<ul style="margin:0.5em 0 0;">
<li><strong>Kuvakaappausketju:</strong> <em>"Katsokaa mitä ne sanovat"</em> — ja kuvassa on tili, jolla on kolme seuraajaa.</li>
<li><strong>Uutisjuttu:</strong> otsikossa "somessa raivotaan", jutussa neljä kommenttia.</li>
<li><strong>Väittely:</strong> vastapuolen maltillinen argumentti ohitetaan, ja keskustelu käydään sen äärimmäisintä versiota vastaan.</li>
</ul>
</div>
<p>Algoritmit tekevät nutpickingista vaivatonta, koska ne nostavat esiin juuri ne viestit, jotka herättävät eniten suuttumusta. Tulos on <a href="aanekas-vahemmisto.html">äänekkään vähemmistön</a> vääristymä kahteen suuntaan: kumpikin puoli näkee toisesta pelkät pahimmat edustajat, ja <a href="kaikukammio.html">kaikukammio</a> vahvistaa kuvan.</p>
<div class="vaaralatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Kysy <strong>kuka sanoi ja kuinka moni</strong>. Onko lainattu ihminen ryhmän edustaja, johtaja tai ohjelman kirjoittaja — vai satunnainen tili? Jos esimerkkiä ei voi yhdistää kehenkään, jolla on vaikutusvaltaa, se kertoo yksilöstä, ei ryhmästä. Omassa argumentoinnissa vastakeino on käänteinen: kumoa vastapuolen <em>vahvin</em> esitys, et heikointa. Jos et löydä sitä, et vielä tiedä, mistä kiistelet.
    </div>
""" + lue_lisaa(
        [],
        [("https://en.wikipedia.org/wiki/Straw_man", "Wikipedia: Straw man — sisältää nutpickingin (englanniksi)")]),
     ["motte-and-bailey", "dunkkaus", "aanekas-vahemmisto", "kaikukammio", "whataboutismi"])


# ────────────────────────── 159 · Tone policing ──────────────────────────
page("tone-policing",
     "Tone policing — sävystä puhutaan, ettei tarvitse puhua asiasta",
     "Tone policing — mitä se tarkoittaa? | Ilmiöitä",
     "Tone policing tarkoittaa, että keskustelu siirretään siihen, miten asia sanottiin, jottei tarvitse vastata siihen mitä sanottiin. Näin sen tunnistaa.",
     [("Mitä tone policing tarkoittaa?",
       "Tone policing on keskustelutaktiikka, jossa viestin sisältöön ei vastata, vaan sen sävy nostetaan pääasiaksi: 'Kuuntelisin, jos puhuisit asiallisemmin.' Sävystä tulee ehto, joka pitää täyttää ennen kuin asiaa käsitellään. Käytännössä ehto ei täyty koskaan, koska tyytymättömyyden voi aina tulkita liian tunteikkaaksi."),
      ("Onko jokainen sävyhuomautus tone policingia?",
       "Ei. Uhkailu, nimittely ja henkilöön käyvä loukkaaminen ovat asiallisia syitä puuttua viestiin. Tone policingista on kyse silloin, kun sävystä puhutaan asian sijasta — kun huomautuksen jälkeen varsinaiseen kysymykseen ei palata."),
      ],
     r"""
<p><strong>Tone policing</strong> on taktiikka, jossa viestin sisältöön ei vastata, vaan sen <strong>sävystä tehdään pääasia</strong>: <em>"Kuuntelisin kyllä, jos osaisit puhua asiallisemmin."</em> Sävy muuttuu ehdoksi, joka on täytettävä ennen kuin asiaa käsitellään — ja joka ei koskaan täyty.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Miksi sävy on niin kätevä kohde?</h2>
<p style="margin:0.4em 0 0;">Sävy on tulkinnanvarainen, joten sen kritiikkiä ei voi kumota. Se myös kääntää asetelman: se, joka otti esiin epäkohdan, joutuu puolustamaan käytöstään, ja se, jota epäkohta koskee, pääsee tuomariksi. Mitä enemmän asia koskee puhujaa itseään, sitä helpommin tunne näkyy — ja sitä helpommin se voidaan ohittaa "tunteiluna".</p>
</div>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Tuttuja muotoja:</h2>
<ul style="margin:0.5em 0 0;">
<li><em>"Hyvä pointti, mutta tuolla asenteella et vakuuta ketään."</em></li>
<li><em>"Rauhoitu ensin, sitten voidaan jutella."</em></li>
<li><em>"Tällainen kiihkoilu vain vahingoittaa omaa asiaasi."</em> — tässä muodossa se on lähellä <a href="huolitrollaus.html">huolitrollausta</a>.</li>
</ul>
</div>
<p>Työpaikalla sama näkyy palautteessa, jossa ongelman esiin nostanut saa kuulla olevansa "negatiivinen". Vastuun kääntämisenä kuvio on sukua <a href="darvo.html">DARVOlle</a>.</p>
<div class="vaaralatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Katso, <strong>palataanko asiaan</strong> sävyhuomautuksen jälkeen. Jos ei, huomautus korvasi vastauksen. Vastakeino on erottaa kaksi keskustelua: <em>"Voin sanoa sen rauhallisemmin. Mitä mieltä olet itse asiasta?"</em> Sävy korjataan, ja kysymys jää pöydälle. Rajaus kuuluu mukaan: uhkailu, nimittely ja henkilöön käyvä loukkaaminen ovat aiheellisia syitä puuttua viestiin. Tone policingista on kyse vasta, kun sävystä puhutaan <em>asian sijasta</em>.
    </div>
""" + lue_lisaa(
        [],
        [("https://en.wikipedia.org/wiki/Tone_policing", "Wikipedia: Tone policing (englanniksi)")]),
     ["huolitrollaus", "darvo", "whataboutismi", "maalitolppien-siirtaminen", "godwinin-laki"])


# ────────────────────────── 160 · Kafkatrapping ──────────────────────────
page("kafkatrapping",
     "Kafkatrapping — kun kiistäminen todistaa syyllisyyden",
     "Kafkatrapping — mitä se tarkoittaa? | Ilmiöitä",
     "Kafkatrapping on argumentointiansa, jossa syytöksen kiistäminen tulkitaan todisteeksi sen puolesta. Näin ansan tunnistaa ja näin siitä pääsee ulos.",
     [("Mitä kafkatrapping tarkoittaa?",
       "Kafkatrapping on argumentointiansa, jossa syytöksen kiistäminen tulkitaan todisteeksi syyllisyydestä: 'Juuri se, että kiellät olevasi puolueellinen, osoittaa että olet.' Ohjelmistokehittäjä ja kirjoittaja Eric S. Raymond nimesi kuvion vuonna 2010 Franz Kafkan romaanin Oikeusjuttu mukaan. Romaanissa päähenkilöä syytetään rikoksesta, jota ei koskaan kerrota, ja jokainen puolustautuminen syventää epäilyä."),
      ("Miten kafkatrappingiin voi vastata?",
       "Kysy, mikä voisi osoittaa syytöksen vääräksi. Jos mikään vastaus — ei kiistäminen, ei myöntäminen eikä vaikeneminen — kelpaa todisteeksi syyttömyydestä, väite ei ole havainto vaan kehä. Sen voi sanoa ääneen ja pyytää konkreettista tekoa, johon syytös perustuu."),
      ],
     r"""
<p><strong>Kafkatrapping</strong> on ansa, jossa <strong>syytöksen kiistäminen tulkitaan todisteeksi syyllisyydestä</strong>. <em>"Juuri se, että puolustaudut noin kiivaasti, osoittaa että osuin oikeaan."</em> Ohjelmistokehittäjä Eric S. Raymond nimesi kuvion vuonna 2010 Franz Kafkan romaanin <cite>Oikeusjuttu</cite> mukaan: sen päähenkilö ei koskaan saa tietää, mistä häntä syytetään, ja jokainen puolustus syventää epäilyä.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Miksi ansasta ei pääse ulos?</h2>
<p style="margin:0.4em 0 0;">Koska kaikki vaihtoehdot on lukittu. Kiistäminen on todiste, myöntäminen on tunnustus ja vaikeneminen on myöntymistä. Väite, jota mikään ei voi kumota, ei kerro maailmasta mitään — se kertoo vain, että päätös on tehty etukäteen.</p>
</div>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Tuttuja muotoja:</h2>
<ul style="margin:0.5em 0 0;">
<li><em>"Jos et olisi syyllinen, et olisi noin puolustuskannalla."</em></li>
<li><em>"Kiistäminen on klassinen merkki siitä, että asia on sinulle kipeä."</em></li>
<li><em>"Tietysti he sanovat, ettei salaliittoa ole — niinhän salaliitto sanoisi."</em></li>
</ul>
</div>
<p>Viimeinen esimerkki näyttää, ettei ansa kuulu millekään yhdelle leirille: sama rakenne kantaa salaliittoteorioita, poliittisia syytöksiä ja riitoja parisuhteessa. Se on sukua <a href="gaslighting.html">gaslightingille</a>, jossa oma havainto kyseenalaistetaan, ja <a href="kaksoissidos.html">kaksoissidokselle</a>, jossa jokainen vastaus on väärä.</p>
<div class="vaaralatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Testi on yksi kysymys: <em>"Mikä voisi osoittaa, että olet väärässä?"</em> Jos mikään ei voisi, keskustelu ei koske näyttöä. Pyydä konkreettista tekoa: <em>mitä tein, milloin ja miten?</em> Älä yritä todistaa sisäistä tilaasi — sitä ei voi todistaa. Rajaus kuuluu mukaan: joskus kiivas kiistäminen todella paljastaa jotain, ja kritiikin torjuminen kafkatrappingina on itsessään kätevä pakotie. Ero on siinä, perustuuko syytös johonkin muuhun kuin kiistämiseen.
    </div>
""" + lue_lisaa(
        [("Oikeusjuttu (Der Process)", "Franz Kafka (1925)")],
        []),
     ["kaksoissidos", "gaslighting", "darvo", "motte-and-bailey", "tone-policing"])


# ────────────────────────── 161 · Shitpostaus ──────────────────────────
page("shitpostaus",
     "Shitpostaus — keskustelu hukutetaan roskaan",
     "Shitpostaus (shitposting) — mitä se tarkoittaa? | Ilmiöitä",
     "Shitpostaus (engl. shitposting) on tahallisen arvotonta sisältöä, joka hukuttaa keskustelun. Välillä se on harmitonta huumoria, välillä tietoinen taktiikka.",
     [("Mitä shitpostaus tarkoittaa?",
       "Shitpostaus (engl. shitposting) tarkoittaa tahallisen arvotonta, absurdia tai aiheen ohi menevää sisältöä verkkokeskustelussa. Osa siitä on harmitonta sisäpiirin huumoria. Taktiikkana se toimii määrän kautta: kun ketju täyttyy roskasta, asiallinen keskustelu katoaa näkyvistä eikä kenenkään tarvitse kumota yhtään argumenttia."),
      ("Miten shitpostaus liittyy disinformaatioon?",
       "Järjestelmällisenä se ei yritä saada ketään uskomaan mitään, vaan tehdä totuuden etsimisestä liian työlästä. Tämä on sama logiikka kuin valheiden paloletkussa (firehose of falsehood): tavoite ei ole vakuuttaa vaan väsyttää, ja väsynyt yleisö lakkaa erottelemasta."),
      ],
     r"""
<p><strong>Shitpostaus</strong> (engl. <em>shitposting</em>) on tahallisen arvotonta, absurdia tai aiheen ohi menevää sisältöä. Suurin osa siitä on harmitonta sisäpiirin huumoria, jolla ei ole mitään tavoitetta. Taktiikaksi se muuttuu, kun roskaa tuotetaan <strong>keskustelun päälle</strong>: ketju täyttyy meemeistä, vitseistä ja sekalaisista väitteistä, ja asiallinen viesti katoaa niiden alle.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Miksi roska toimii argumenttia paremmin?</h2>
<p style="margin:0.4em 0 0;">Argumentin voi kumota, roskaa ei. Shitpostaus ei väitä mitään, mihin voisi tarttua — se vain vie tilan. Kun keskustelussa on sata viestiä ja kolme niistä on asiaa, lukija ei löydä niitä, ja kirjoittaja lakkaa yrittämästä.</p>
</div>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Kolme käyttötapaa:</h2>
<ul style="margin:0.5em 0 0;">
<li><strong>Huumori:</strong> absurdia omalle porukalle. Harmitonta, kun se pysyy omassa ketjussaan.</li>
<li><strong>Hukutus:</strong> vakava keskustelu, esimerkiksi tapahtuneesta vahingosta, täytetään vitseillä, kunnes aihe muuttuu.</li>
<li><strong>Väsytys:</strong> järjestelmällinen roskan tuottaminen, jonka tavoite on, ettei mitään voi enää uskoa. Sama logiikka kuin <a href="firehose-of-falsehood.html">valheiden paloletkussa</a>.</li>
</ul>
</div>
<p>Shitpostaus on määrän taktiikka, kuten <a href="argumenttitulva.html">argumenttitulva</a>. Ero on, että argumenttitulva esittää liikaa väitteitä, shitpostaus liikaa ei-mitään. Tekoälyn tuottama massasisältö, <a href="ai-slop.html">AI slop</a>, tekee saman ilman tahtoakin.</p>
<div class="vaaralatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Erota huumori hukutuksesta kysymällä: <em>vaihtuiko aihe?</em> Jos vakava ketju on kymmenen viestin jälkeen muuttunut vitsailuksi, joku hyötyi siitä. Ylläpitäjälle: aiheen ohi menevä sisältö kannattaa siirtää tai piilottaa ennen kuin se asettaa ketjun normin. Lukijalle: älä vastaa roskaan roskalla. Jos asia on tärkeä, kirjoita se omaksi viestikseen, jonka voi linkittää ja johon voi palata.
    </div>
""" + lue_lisaa(
        [],
        [("https://en.wikipedia.org/wiki/Shitposting", "Wikipedia: Shitposting (englanniksi)")]),
     ["argumenttitulva", "firehose-of-falsehood", "ai-slop", "trollaus", "vain-vitsi"])


# ────────────────────────── 162 · Dunkkaus ja ratio ──────────────────────────
page("dunkkaus",
     "Dunkkaus ja ratio — nolaaminen yleisön edessä",
     "Dunkkaus ja ratio — mitä ne tarkoittavat somessa? | Ilmiöitä",
     "Dunkkaus on somen lainausviesti, jolla toinen nolataan omalle yleisölle. Ratio on sen mittari. Miksi se palkitaan ja miten dunkkauksen kohteeksi joutuu.",
     [("Mitä dunkkaus tarkoittaa somessa?",
       "Dunkkaus (engl. dunking) tarkoittaa, että toisen viesti jaetaan lainausviestinä omalle yleisölle pilkaten tai nolaten. Vastaus ei ole tarkoitettu alkuperäiselle kirjoittajalle vaan omille seuraajille. Sana tulee koripallon ilmasta tehtävästä, näyttävästä korinteosta."),
      ("Mitä ratio tarkoittaa?",
       "Ratio tarkoittaa, että viestin vastauksilla tai lainauksilla on enemmän tykkäyksiä kuin itse viestillä. Se tulkitaan merkiksi siitä, että yleisö on kirjoittajaa vastaan. Somessa sana esiintyy usein pelkkänä vastauksena: 'ratio'."),
      ],
     r"""
<p><strong>Dunkkaus</strong> (engl. <em>dunking</em>, koripallon näyttävästä korinteosta) tarkoittaa, että toisen viesti jaetaan <strong>lainausviestinä omalle yleisölle</strong> pilkaten tai nolaten. Vastaus ei ole tarkoitettu alkuperäiselle kirjoittajalle vaan omille seuraajille. <strong>Ratio</strong> on dunkkauksen mittari: kun vastauksilla on enemmän tykkäyksiä kuin itse viestillä, kirjoittaja on "hävinnyt".</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Miksi dunkkaus palkitaan?</h2>
<p style="margin:0.4em 0 0;">Moraalinen suuttumus leviää. Bradyn ym. (2017) aineistossa jokainen moraalis-tunteellinen sana viestissä lisäsi sen jakoja noin viidenneksellä. Nolaava lainaus on juuri tätä: se tarjoaa omalle yleisölle yhteisen vihollisen ja hetken yhteenkuuluvuutta.</p>
</div>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Miten dunkkaus eroaa kritiikistä:</h2>
<ul style="margin:0.5em 0 0;">
<li><strong>Kenelle:</strong> kritiikki puhuu kirjoittajalle, dunkkaus hänestä muille.</li>
<li><strong>Mittakaava:</strong> pienen tilin viesti nostetaan suuren tilin yleisön eteen. Kohde ei ole valinnut tätä yleisöä.</li>
<li><strong>Kehys:</strong> viesti irrotetaan asiayhteydestään ja esitetään esimerkkinä jostain laajemmasta — usein <a href="nutpicking.html">nutpickingina</a>.</li>
</ul>
</div>
<p>Dunkkaus on usein <a href="maalittaminen.html">maalittamisen</a> ensimmäinen askel, vaikka lainaaja ei sitä tarkoittaisi. Yksi lainaus riittää osoittamaan kohteen tuhansille, ja parvi hoitaa loput.</p>
<div class="vaaralatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Ennen lainaamista kysy: <em>kenelle tämä vastaus on?</em> Jos se on omille seuraajille, kyse on esityksestä, ei keskustelusta. Vastaa mieluummin suoraan viestiin — tai ota kuvakaappaus ilman nimeä, jos haluat puhua ilmiöstä etkä ihmisestä. Kohteelle: dunkkaukseen ei tarvitse vastata, eikä ratio kerro, kuka on oikeassa, vaan kenellä on isompi yleisö. Jos lainaus alkaa tuottaa häirintää, lukitse tili hetkeksi.
    </div>
""" + lue_lisaa(
        [("Emotion shapes the diffusion of moralized content in social networks",
          "Brady, Wills, Jost, Tucker &amp; Van Bavel, <em>PNAS</em> (2017)")],
        []),
     ["maalittaminen", "nutpicking", "rage-bait", "engagement-bait", "trollaus"])


# ────────────────────────── 163 · Maalittaminen ──────────────────────────
page("maalittaminen",
     "Maalittaminen — joukko kohdistetaan yhteen ihmiseen",
     "Maalittaminen — mitä se on ja miten siihen voi varautua? | Ilmiöitä",
     "Maalittaminen on järjestelmällistä painostusta, jossa yksi osoittaa kohteen ja joukko hoitaa loput. Näin se toimii ja näin siihen voi varautua.",
     [("Mitä maalittaminen tarkoittaa?",
       "Maalittaminen tarkoittaa järjestelmällistä häirintää, jossa yksi toimija nostaa esiin henkilön — usein toimittajan, tutkijan, viranomaisen tai poliitikon — ja joukko seuraajia kohdistaa häneen viestejä, valituksia, uhkauksia tai henkilötietojen levittämistä. Tavoite on vaikuttaa siihen, miten kohde tekee työtään, tai saada hänet vetäytymään julkisuudesta."),
      ("Onko maalittaminen rikos?",
       "Maalittamiseen kuuluvat yksittäiset teot voivat täyttää esimerkiksi laittoman uhkauksen, kunnianloukkauksen, yksityiselämää loukkaavan tiedon levittämisen tai vainoamisen tunnusmerkistön. Vaikeus on siinä, että yksittäinen viesti jää usein rangaistavan rajan alle ja vahinko syntyy vasta niiden määrästä. Kohteen kannattaa tallentaa viestit ja tehdä rikosilmoitus poliisille."),
      ],
     r"""
<p><strong>Maalittaminen</strong> on järjestelmällistä häirintää, jossa <strong>yksi osoittaa kohteen ja joukko hoitaa loput</strong>. Joku nostaa esiin toimittajan, tutkijan, virkamiehen tai tavallisen kirjoittajan — usein vain jakamalla nimen ja kuvakaappauksen — ja seuraajat täyttävät kohteen sähköpostin, kommentit ja työnantajan palautekanavan. Englanniksi lähikäsitteitä ovat <em>dogpiling</em> ja <em>brigading</em>.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Miksi maalittamiseen on vaikea puuttua?</h2>
<p style="margin:0.4em 0 0;">Vastuu hajoaa. Maalittaja ei itse uhkaa ketään — hän "vain kertoi asiasta". Yksittäinen viesti jää usein rangaistavan rajan alle, ja vahinko syntyy vasta niiden määrästä. Yksittäiset teot voivat silti täyttää esimerkiksi laittoman uhkauksen, kunnianloukkauksen tai vainoamisen tunnusmerkistön.</p>
</div>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Maalittamisen vaiheet:</h2>
<ul style="margin:0.5em 0 0;">
<li><strong>Osoitus:</strong> kohde nimetään ja kehystetään viholliseksi, usein irrotetulla lainauksella.</li>
<li><strong>Parvi:</strong> seuraajat lähestyvät kohdetta joukolla, jolloin kukaan ei tunne olevansa yksittäinen häiritsijä.</li>
<li><strong>Laajennus:</strong> kotiosoite, perhe tai työnantaja kaivetaan esiin.</li>
<li><strong>Vaikutus:</strong> kohde jättää aiheen tai alan — ja muut näkevät, mitä siitä seuraa.</li>
</ul>
</div>
<p>Viimeinen vaihe on koko ilmiön tarkoitus. Valtioneuvoston selvitys <cite>Viha vallassa</cite> (Knuutila ym. 2019) kuvasi, miten vihapuhe ja häirintä saavat päättäjiä ja asiantuntijoita välttämään aiheita. Vaikutus ulottuu niihin, joita ei ole koskaan maalitettu.</p>
<div class="vaaralatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Kohteelle: <strong>tallenna kaikki</strong> kuvakaappauksina päivämäärineen, kerro työnantajalle heti ja tee rikosilmoitus uhkauksista. Älä vastaa parvelle — yksi vastaus on uusi maali. Työnantajalle: kohtele maalittamista työturvallisuusasiana, älä kohteen imago-ongelmana. Sivulliselle: älä jaa maalitusviestiä edes kauhistellaksesi, ja muista, ettei <a href="sivustakatsojan-efekti.html">sivustakatsojan</a> hiljaisuus ole neutraalia. Tukiviesti kohteelle yksityisesti auttaa enemmän kuin julkinen väittely maalittajan kanssa.
    </div>
""" + lue_lisaa(
        [("Viha vallassa: vihapuheen vaikutukset yhteiskunnalliseen päätöksentekoon",
          "Knuutila, Kosonen, Saresma, Haara &amp; Pöyhtäri, Valtioneuvoston selvitys- ja tutkimustoiminta (2019)")],
        []),
     ["doksaus", "dunkkaus", "trollin-ruokkiminen", "trollitehdas", "sivustakatsojan-efekti"])


# ────────────────────────── 164 · Doksaus ──────────────────────────
page("doksaus",
     "Doksaus — verkon riita siirtyy kotiovelle",
     "Doksaus (doxxing) — mitä se on ja miten siltä suojautuu? | Ilmiöitä",
     "Doksaus (engl. doxxing) tarkoittaa henkilötietojen kaivamista ja julkaisemista kohteen painostamiseksi. Näin se toimii ja näin omia tietojaan voi suojata.",
     [("Mitä doksaus tarkoittaa?",
       "Doksaus (engl. doxxing tai doxing, sanasta docs eli dokumentit) tarkoittaa ihmisen henkilötietojen kaivamista esiin ja julkaisemista ilman hänen suostumustaan: kotiosoite, työpaikka, puhelinnumero, perheenjäsenet tai valokuvat. Tavoite on painostaa, pelotella tai tehdä kohteesta helposti löydettävä muille häiritsijöille."),
      ("Miten omia tietojaan voi suojata doksaukselta?",
       "Tarkista, mitä itsestäsi löytyy hakukoneilla ja henkilöhakupalveluista. Suomessa Digi- ja väestötietovirastolta voi pyytää osoitetietojen luovutuskieltoja esimerkiksi suoramarkkinointiin, ja perustellusta syystä turvakiellon. Poista kuvista sijaintitiedot, käytä eri käyttäjänimiä eri palveluissa ja tallenna mahdolliset uhkaukset poliisia varten."),
      ],
     r"""
<p><strong>Doksaus</strong> (engl. <em>doxxing</em>, sanasta <em>docs</em>, dokumentit) tarkoittaa ihmisen henkilötietojen kaivamista ja julkaisemista ilman hänen suostumustaan: <strong>kotiosoite, työpaikka, puhelinnumero, perheenjäsenet</strong>. Tavoite on siirtää verkon riita fyysiseen maailmaan — tehdä kohteesta helposti löydettävä kaikille, jotka haluavat painostaa häntä.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Miksi julkisetkin tiedot voivat olla doksausta?</h2>
<p style="margin:0.4em 0 0;">Moni tieto löytyy erikseen julkisista lähteistä. Vahinko syntyy <strong>kokoamisesta ja kohdistamisesta</strong>: yksittäinen osoite rekisterissä on eri asia kuin sama osoite julkaistuna vihaisen joukon keskelle kuvan ja työpaikan kanssa. Julkaisija ei itse uhkaa ketään — hän vain antaa muille keinot.</p>
</div>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Mistä tiedot tyypillisesti löytyvät:</h2>
<ul style="margin:0.5em 0 0;">
<li><strong>Käyttäjänimet:</strong> sama nimimerkki eri palveluissa yhdistää anonyymin tilin oikeaan nimeen.</li>
<li><strong>Kuvat:</strong> taustalla näkyvä katu, ikkunanäkymä tai kuvan sijaintitieto.</li>
<li><strong>Rekisterit ja henkilöhakupalvelut:</strong> osoite, yritysroolit ja syntymäaika.</li>
<li><strong>Läheiset:</strong> perheenjäsenten ja työkavereiden avoimemmat tilit.</li>
</ul>
</div>
<p>Doksaus on <a href="maalittaminen.html">maalittamisen</a> laajennusvaihe. Yksittäiset teot voivat täyttää esimerkiksi yksityiselämää loukkaavan tiedon levittämisen tai vainoamisen tunnusmerkistön, ja henkilötietojen käsittelyä rajaa myös tietosuojalainsäädäntö.</p>
<div class="vaaralatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Ennakoi: hae itseäsi hakukoneella ja henkilöhakupalveluista ja pyydä poistoja. Digi- ja väestötietovirastolta voi pyytää osoitetietojen luovutuskieltoja, ja perustellusta syystä <strong>turvakiellon</strong>. Poista kuvista sijaintitiedot ja käytä eri nimimerkkejä eri palveluissa. Jos sinut doksataan: tallenna julkaisut kuvakaappauksina, ilmoita alustalle, kerro työnantajalle ja tee rikosilmoitus, jos mukana on uhkauksia. Sivulliselle: älä jaa julkaisua, edes paheksuaksesi — jokainen jako vie osoitteen uusille silmille.
    </div>
""" + lue_lisaa(
        [],
        [("https://en.wikipedia.org/wiki/Doxing", "Wikipedia: Doxing (englanniksi)")]),
     ["maalittaminen", "trollin-ruokkiminen", "dunkkaus", "trollaus", "sivustakatsojan-efekti"])


# ────────────────────────── 165 · Älä ruoki trollia ──────────────────────────
page("trollin-ruokkiminen",
     "Älä ruoki trollia — milloin hiljaisuus toimii ja milloin ei",
     "Älä ruoki trollia — toimiiko neuvo oikeasti? | Ilmiöitä",
     "Älä ruoki trollia on verkon vanhin neuvo: reaktio on trollin palkkio. Se toimii yksittäiseen provosoijaan, mutta ei maalittamiseen. Näin erotat ne.",
     [("Mitä älä ruoki trollia tarkoittaa?",
       "Älä ruoki trollia (engl. don't feed the trolls) on Usenet-ajoilta periytyvä neuvo: koska trollin palkkio on reaktio, sen saa loppumaan jättämällä reaktion antamatta. Jokainen vastine, suuttumus ja vastaväite on ruokaa, joka pitää provosoinnin käynnissä."),
      ("Milloin trollin sivuuttaminen ei toimi?",
       "Sivuuttaminen toimii yksittäiseen provosoijaan, joka hakee huomiota. Se ei toimi, kun kyse on järjestelmällisestä häirinnästä tai maalittamisesta: silloin hiljaisuus ei vie palkkiota, koska tavoite ei ole reaktio vaan kohteen vetäytyminen. Tällöin tarvitaan moderointia, tallentamista ja tarvittaessa rikosilmoitus."),
      ],
     r"""
<p><strong>Älä ruoki trollia</strong> (engl. <em>don't feed the trolls</em>) on verkon vanhimpia neuvoja. Logiikka on yksinkertainen: jos <a href="trollaus.html">trollin</a> palkkio on reaktio, provosointi loppuu kun reaktiota ei tule. Jokainen vastine, suuttumus ja vastaväite on ruokaa. Sama periaate on <a href="harmaa-kivi.html">harmaan kiven</a> taustalla ihmissuhteissa: tylsyys vie palkkion pois.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Toimiiko trollin sivuuttaminen?</h2>
<p style="margin:0.4em 0 0;">Yksittäiseen huomionhakijaan usein toimii. Mutta neuvo olettaa, että trolli haluaa <em>reaktion</em>. Jos tavoite on saada joku lopettamaan kirjoittaminen, hiljaisuus on juuri se, mitä haetaan — ja silloin neuvo toimii häiritsijän eduksi.</p>
</div>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Erota kaksi tilannetta:</h2>
<ul style="margin:0.5em 0 0;">
<li><strong>Provosoija:</strong> yksi tili, tavoite huomio, kiinnostus loppuu kun vastausta ei tule. <strong>Sivuuta.</strong></li>
<li><strong>Häirintä tai <a href="maalittaminen.html">maalittaminen</a>:</strong> monta tiliä, tavoite kohteen vetäytyminen, jatkuu vaikka kukaan ei vastaa. <strong>Sivuuttaminen ei riitä</strong> — tarvitaan moderointia, estoja, tallentamista ja tarvittaessa rikosilmoitus.</li>
</ul>
</div>
<p>Neuvolla on myös hiljainen sivuvaikutus: kun sitä toistetaan häirinnän kohteelle, vastuu siirtyy häirityn käytökseen. "Älä välitä" kuulostaa tuelta, mutta tarkoittaa usein "hoida itse".</p>
<div class="vaaralatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Jos haluat vastata, vastaa <strong>yleisölle, ei trollille</strong>: yksi lyhyt asiallinen oikaisu ilman lainausta, jota ei jatketa. Älä jaa provokaatiota kauhistellaksesi — kuvakaappaus levittää sen uusille lukijoille, kuten <a href="rage-bait.html">rage baitissa</a>. Käytä estoa ja ilmiantoa vapaasti: ne eivät ole sensuuria vaan sen päättämistä, kenen kanssa käytät aikaasi. Ja jos joku kertoo olevansa häirinnän kohteena, älä neuvo häntä vain olemaan välittämättä — kysy, mitä hän tarvitsee.
    </div>
""" + lue_lisaa(
        [("This Is Why We Can't Have Nice Things", "Whitney Phillips (2015)")],
        [("https://en.wikipedia.org/wiki/Internet_troll", "Wikipedia: Internet troll (englanniksi)")]),
     ["trollaus", "maalittaminen", "doksaus", "pimea-tetradi", "harmaa-kivi"])


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


def kirjoita_hub_lohko():
    """index.html:n hub-lohko valmiiksi — liitetään käsin vasta julkaisussa,
    valtapelit-lohkon perään. Ei kirjoiteta index.html:ään nyt (ks. docstring)."""
    kortit = []
    for p in PAGES:
        num, vari, nimi, kuvaus = OMAT_KORTIT[p["slug"]]
        kortit.append(f'''<a href="{p["slug"]}.html" class="hub-kortti" style="--c:{vari}">
  <span class="hub-numero">{num}</span>
  <span class="hub-teksti">
    <span class="hub-nimi">{nimi}</span>
    <span class="hub-kuvaus">{kuvaus}</span>
  </span>
  <span class="hub-nuoli" aria-hidden="true">›</span>
</a>''')
    lohko = (f'<div class="hub-kategoria" id="{KAT_ID}">\n'
             f'  <h2 class="hub-kat-label"><span class="hub-kat-nro">{KAT_NRO}</span>{KAT_NIMI}'
             f'<span class="hub-kat-count"> · {len(PAGES)} ilmiötä</span></h2>\n'
             f'  <p class="hub-kat-desc">{KAT_KUVAUS}</p>\n'
             f'  <a class="hub-kat-linkki" href="{KAT_SIVU}">Lue koko kategoria '
             f'<span aria-hidden="true">&rarr;</span></a>\n'
             f'  <div class="hub-kortit">\n' + "\n".join(kortit) + "\n  </div>\n</div>\n")
    tiedosto = OUT / "trollaus-hub-lohko.html"
    tiedosto.write_text("<!-- Liitä index.html:ään valtapelit-lohkon perään vasta julkaisussa. "
                        "Generoi scripts/build_trollaus_luonnokset.py -->\n" + lohko,
                        encoding="utf-8")
    print(f"  hub-lohko → {tiedosto.relative_to(ROOT)}")


def build():
    tpl = TEMPLATE.read_text(encoding="utf-8")
    OUT.mkdir(exist_ok=True)

    ids_match = re.search(r"const IDS = \[(.*?)\];", tpl, re.S)
    julkaistut = [s.strip().strip('"') for s in ids_match.group(1).split(",")]
    assert len(julkaistut) == 139, f"odotettiin 139 id:tä, saatiin {len(julkaistut)}"
    # valtapelit-erä (140-148) on index.html:ssä muttei vielä sivujen IDS:ssä
    assert EDELLISET_IDS[:139] == julkaistut, "index.html:n korttijärjestys ≠ darvo.html:n IDS"
    assert len(EDELLISET_IDS) == 148, f"odotettiin 148 korttia, saatiin {len(EDELLISET_IDS)}"
    ids_js = ("const IDS = ["
              + ", ".join(json.dumps(s) for s in EDELLISET_IDS + [p["slug"] for p in PAGES])
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

    kirjoita_hub_lohko()
    print(f"\nValmis: {len(PAGES)} luonnosta kansiossa {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    build()
