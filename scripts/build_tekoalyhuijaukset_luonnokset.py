#!/usr/bin/env python3
"""Generoi Tekoälyhuijaukset-klusterin sivuluonnokset — 4 kpl.

Lähde: luonnokset/UUDET-KLUSTERIT-PLAN.md § 4 (klusteri 2, kärki).

POIKKEAMA SUUNNITELMASTA (tietoinen): suunnitelma sijoitti kaikki neljä sivua
kategoriaan "Huijaukset ja petokset" (11 → 15). Kolme niistä on huijauksia,
mutta **tekoälypsykoosi ei ole** — kukaan ei huijaa ketään, vaan myötäilevä
vastaustyyli vahvistaa ajattelua. Se menisi väärään naapurustoon ja rikkoisi
kategorian lukijalle antaman lupauksen, joten se sijoitetaan kategoriaan
"Alustatalous ja algoritmit" (parasosiaalinen suhde ja kaikukammio ovat siellä).
Huijaukset ja petokset kasvaa siis 11 → 14.

Pohjana qr-koodihuijaus.html (Huijaukset ja petokset). Kategoriakentät
(murupolku, articleSection, kategoriasivun linkki) korvataan vain siltä sivulta,
jonka kategoria poikkeaa pohjasta.

Numerot ovat alustavia ja **oletus on, ettei muita luonnoseriä ole julkaistu**:
76–78 pujotetaan rug-pullin (75) perään ja tekoälypsykoosi äänekkään
vähemmistön (100) perään. Sama paikka 101 on varattu myös pimeiden kuvioiden
erän ensimmäiselle sivulle — kumpi julkaistaan ensin, se saa numeron, ja
lisaa_ilmiot.py laskee loput.

Tuottaa luonnokset/-kansioon 4 sivua, joissa on noindex-meta ja ../-alkuiset
polut. Kansio on kaikkien erien yhteinen, joten skripti kirjoittaa vain omat
neljä sivuaan yli.

Ajo:  python3 scripts/build_tekoalyhuijaukset_luonnokset.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "qr-koodihuijaus.html"
OUT = ROOT / "luonnokset"

PVM_ISO = "2026-08-14"
PVM_FI = "14.8.2026"

# Pohjasivun tunnisteet, jotka korvataan
VANHA_SLUG = "qr-koodihuijaus"
VANHA_VARI = "#0d47a1"
VANHA_TITLE = "QR-koodihuijaus — väärä koodi, oikea lasku"
VANHA_DESC = ("QR-koodihuijaus: väärä tarra, oikea lasku. Selitämme miten koodinvaihtohuijaus "
              "toimii käytännössä ja millä rutiineilla suojaudut skannatessa.")
VANHA_KAT = "Huijaukset ja petokset"
VANHA_KAT_SIVU = "kategoria-huijaukset-ja-petokset.html"

INDEX = (ROOT / "index.html").read_text(encoding="utf-8")
JULKAISTUJA = len(re.findall(r'<a href="[a-z0-9-]+\.html" class="hub-kortti"', INDEX))
YHTEENSA = JULKAISTUJA + 4

# Omat kortit: slug → (numero, väri, nimi, kuvaus)
OMAT_KORTIT = {
    "aaniklooni-huijaus": (76, "#7f0000", "Ääniklooni-huijaus",
        "Muutaman sekunnin näyte riittää: tuttu ääni pyytää rahaa kiireellä, eikä kuulo enää todista mitään."),
    "smishing": (77, "#0b3d91", "Smishing",
        "Huijausviesti putoaa samaan ketjuun aitojen kanssa: paketti odottaa maksua, pankki pyytää vahvistusta."),
    "deepfake-sijoitushuijaus": (78, "#9c4dcc", "Deepfake-sijoitushuijaus",
        "Tuttu kasvo ja tutun näköinen uutissivu mainostavat alustaa, jolla saldo nousee mutta raha ei palaa."),
    "tekoalypsykoosi": (101, "#004d40", "Tekoälypsykoosi",
        "Myötäilevä chatbot ei ole koskaan eri mieltä — ja vie hauraan ajattelun loppuun asti."),
}

# Sivun kategoria, jos se poikkeaa pohjasta
POIKKEAVA_KATEGORIA = {
    "tekoalypsykoosi": ("Alustatalous ja algoritmit", "kategoria-alustatalous-ja-algoritmit.html"),
}

# Ketjut: (edeltäjän slug, edeltäjän otsikko) kunkin ketjun alkuun
KETJUT = {
    "huijaukset": ("rug-pull", "Rug pull — matto vedetään alta"),
    "alusta": ("aanekas-vahemmisto", "Äänekäs vähemmistö — kommenttiosio ei ole mielipidemittari"),
}


def julkaistut_kortit():
    """Poimii index.html:n hub-korteista (numero, väri, nimi, kuvaus)."""
    kortit = {}
    kuvio = re.compile(
        r'<a href="([a-z0-9-]+)\.html" class="hub-kortti" style="--c:(#[0-9a-f]+)">\s*'
        r'<span class="hub-numero">(\d+)</span>\s*<span class="hub-teksti">\s*'
        r'<span class="hub-nimi">([^<]*)</span>\s*<span class="hub-kuvaus">([^<]*)</span>')
    for m in kuvio.finditer(INDEX):
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


def page(slug, ketju, otsikko, kuvaus, sisalto, liittyvat, faq):
    num, vari = OMAT_KORTIT[slug][0], OMAT_KORTIT[slug][1]
    PAGES.append(dict(slug=slug, ketju=ketju, num=num, vari=vari, otsikko=otsikko,
                      kuvaus=kuvaus, sisalto=sisalto, liittyvat=liittyvat, faq=faq))


# ─────────────────────── 76 · Ääniklooni-huijaus ───────────────────────
page("aaniklooni-huijaus", "huijaukset",
     "Ääniklooni-huijaus — tuttu ääni puhelimessa ei enää todista mitään",
     "Ääniklooni-huijauksessa muutaman sekunnin ääninäyte riittää: soittaja kuulostaa lapselta tai toimitusjohtajalta ja pyytää rahaa kiireellä. Ääni ei enää todista henkilöllisyyttä.",
     r"""
<p><strong>Ääniklooni-huijaus</strong> (englanniksi <em>voice cloning scam</em>; puhelimitse tehdystä kalastelusta käytetään termiä <em>vishing</em>) tarkoittaa huijausta, jossa soittajan ääni on tuotettu koneellisesti tunnetun ihmisen näytteestä. Näytettä tarvitaan vähän, ja sitä on tarjolla siellä missä ihmiset puhuvat julkisesti: somevideoissa, podcasteissa, yritysten esittelyklipeissä. Vanha nyrkkisääntö "tunnistan hänen äänensä" lakkasi toimimasta.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Riittääkö tutun ääni todisteeksi puhelimessa?</h2>
<p style="margin:0.4em 0 0;">Ei. Ääni voidaan kloonata ja myös näytössä näkyvä numero väärentää, joten kumpikaan ei kerro, kuka soittaa. Ainoa varmistus on katkaista puhelu ja soittaa takaisin numeroon, jonka olet itse hakenut — ei siihen, josta soitto tuli, eikä siihen, jonka soittaja antaa. Poliisin ja pankkien ohje on sama vuodesta toiseen: kiire on huijauksen tunnusmerkki, ei kiireellisen asian.</p>
</div>
<div class="mermaid">
flowchart TD
  A["Ääninäyte julkisesta\nvideosta tai puhelusta"] --&gt; B["Ääni kloonataan"]
  B --&gt; C["Soitto: hädässä oleva läheinen\ntai toimitusjohtajan maksupyyntö"]
  C --&gt; D{"Soitatko takaisin\nitse hakemaasi numeroon?"}
  D -- ei --&gt; E["Maksu lähtee minuuteissa"]
  D -- kyllä --&gt; F["Huijaus paljastuu"]
  style E fill:#fdf0f0,stroke:#c0392b
  style F fill:#eafaf1,stroke:#27ae60
    </div>
<p class="kaavio-selitys">Huijaus ei nojaa tekniikkaan vaan tunteeseen: kloonattu ääni ostaa ne minuutit, joina kukaan ei tarkista mitään.</p>
<p>Muotoja on kaksi. Yksityishenkilölle soittaa hätääntynyt läheinen, joka on joutunut onnettomuuteen tai pidätetyksi ja tarvitsee rahaa heti; puhelu katkeaa juuri ennen kuin ehtii kysyä mitään. Yritykselle soittaa johtaja, joka pyytää poikkeuksellista maksua ja pyytää olemaan kertomatta siitä muille. Jälkimmäinen on vanha juoni: <a href="../toimitusjohtajahuijaus.html">toimitusjohtajahuijaus</a> teki saman sähköpostilla jo 2010-luvulla. Ääni on siihen lisätty kerros, ei uusi rakenne.</p>
<div class="infolaatikko">
<h2 class="laatikko-otsikko">Miksi ääni toimii paremmin kuin sähköposti?</h2> Sähköpostiversiossa uskottavuus rakennettiin osoitteesta ja kiireestä, ja epäilijä saattoi pysähtyä lukemaan rivin uudelleen. Puhelu ei anna sitä mahdollisuutta: ääni ohittaa harkinnan ja vastaa itse siihen kysymykseen, jonka epäilijä esittäisi. <a href="deepfake-sijoitushuijaus.html">Deepfake-sijoitushuijaus</a> tekee saman kuvalla.
    </div>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2>
<ul style="margin:0.5em 0 0;">
<li>Sopikaa perheen kesken turvasana, joka kysytään aina kun puhelimessa pyydetään rahaa. Se maksaa yhden keskustelun.</li>
<li>Katkaise ja soita takaisin itse hakemaasi numeroon. Aito hätä kestää kaksi minuuttia, huijaus ei.</li>
<li>Yrityksissä: maksun hyväksyy kaksi ihmistä eikä poikkeusta tehdä kiireeseen tai salassapitoon vedoten.</li>
<li>Älä vahvista soittajalle nimiä, rooleja tai tilitietoja. Sekä vastauksesi että äänesi ovat aineistoa seuraavaan soittoon.</li>
</ul>
</div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Kirjoja</span>
<ul class="lue-lisaa-lista">
<li><cite>The Art of Deception</cite> — Kevin Mitnick (2002)</li>
</ul>
</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://en.wikipedia.org/wiki/Voice_phishing" target="_blank" rel="noopener">Wikipedia: Voice phishing (englanniksi)</a></li>
</ul>
</div>
</div>
""",
     ["toimitusjohtajahuijaus", "smishing", "deepfake-sijoitushuijaus", "ennakkomaksuhuijaus"],
     [("Mikä on ääniklooni-huijaus?",
       "Ääniklooni-huijauksessa soittajan ääni on tuotettu koneellisesti tunnetun ihmisen näytteestä. Tyypillisiä muotoja ovat hädässä olevaksi läheiseksi tekeytyminen ja toimitusjohtajan äänellä esitetty kiireellinen maksupyyntö. Näytteeksi riittää lyhyt julkinen puhe, esimerkiksi somevideo tai podcast."),
      ("Riittääkö tutun ääni todisteeksi puhelimessa?",
       "Ei. Ääni voidaan kloonata ja näytössä näkyvä numero väärentää. Ainoa varmistus on katkaista puhelu ja soittaa takaisin numeroon, jonka olet itse hakenut — ei siihen, josta soitto tuli, eikä siihen, jonka soittaja antaa.")])

# ─────────────────────────── 77 · Smishing ───────────────────────────
page("smishing", "huijaukset",
     "Smishing — tekstiviesti, joka näyttää tulevan Postilta",
     "Smishing on tekstiviestillä tehtyä kalastelua: paketti odottaa maksua, pankki pyytää vahvistusta. Viesti näyttää aidolta, koska se putoaa samaan ketjuun aitojen kanssa.",
     r"""
<p><strong>Smishing</strong> (sanoista <em>SMS</em> ja <em>phishing</em>) tarkoittaa tekstiviestillä tehtyä kalastelua. Viesti kertoo, että paketti odottaa pientä maksua, tili on lukittu tai veronpalautus vaatii vahvistuksen, ja tarjoaa linkin. Linkin takana on sivu, joka näyttää oikealta ja pyytää juuri ne tiedot, joilla rahat siirretään: verkkopankkitunnukset ja vahvistuksen.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Mitä smishing tarkoittaa suomeksi?</h2>
<p style="margin:0.4em 0 0;">Vakiintunutta suomennosta ei ole. Käytössä ovat <strong>tekstiviestikalastelu</strong> ja <em>tekstiviestihuijaus</em>; viranomaiset puhuvat huijausviesteistä. Termi on yhdistelmä sanoista SMS ja phishing eli kalastelu. Suomenkielistä Wikipedia-artikkelia ei ole, vaikka ilmiö on yksi tunnistetuimmista — käytännössä jokainen suomalainen on saanut tällaisen viestin.</p>
</div>
<div class="mermaid">
flowchart TD
  A["Viesti: paketti odottaa\n2,50 € toimitusmaksua"] --&gt; B["Linkki näyttää\nkuljetusyhtiön sivulta"]
  B --&gt; C["Kortti- tai pankkitunnukset"]
  C --&gt; D["Vahvistus omalla\ntunnistusvälineellä"]
  D --&gt; E["Tililtä lähtee\nmuu kuin 2,50 €"]
  style E fill:#fdf0f0,stroke:#c0392b
    </div>
<p class="kaavio-selitys">Pieni summa ei ole huijauksen saalis vaan sen sisäänpääsy: se saa vahvistuksen tuntumaan vaarattomalta.</p>
<p>Uskottavuus syntyy kahdesta asiasta. Ensinnäkin teema osuu ajankohtaan — pakettiviestit tulevat joulukuussa, veroviestit keväällä. Toiseksi viesti voi pudota samaan keskusteluketjuun aitojen viestien kanssa, jos lähettäjätunnus on väärennetty; silloin puhelin näyttää sen tutun nimen alla. Suomessa organisaatioiden on pitänyt luvittaa käyttämänsä lähettäjätunnukset ennakkoon toukokuusta 2026 alkaen, eikä suojattua tunnusta voi enää väärentää. Siksi huijausviesti tulee yhä useammin tavallisesta puhelinnumerosta tai muusta viestisovelluksesta.</p>
<div class="infolaatikko">
<h2 class="laatikko-otsikko">Miten smishing eroaa QR-koodihuijauksesta?</h2> Kanava on eri, loppu sama: molemmissa uhri ohjataan väärennetylle sivulle antamaan tunnuksensa. <a href="../qr-koodihuijaus.html">QR-koodihuijaus</a> odottaa fyysisessä paikassa, smishing tulee taskuun. Molemmissa suojaus on sama: mene palveluun itse, älä linkin kautta.
    </div>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2>
<ul style="margin:0.5em 0 0;">
<li>Älä avaa viestin linkkiä. Kirjoita palvelun osoite itse tai käytä sen omaa sovellusta — paketin seuranta löytyy sieltä.</li>
<li>Pankki ei kysy tunnuslukuja eikä pyydä vahvistamaan mitään viestin linkissä. Yksikään aito toimija ei tee sitä.</li>
<li>Epäile pientä summaa erityisesti: se on tehty näyttämään liian pieneltä tarkistettavaksi.</li>
<li>Jos annoit tunnukset, soita heti pankkiin ja sulje ne. Tee rikosilmoitus ja ilmoita viestistä Kyberturvallisuuskeskukselle.</li>
</ul>
</div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://en.wikipedia.org/wiki/SMS_phishing" target="_blank" rel="noopener">Wikipedia: SMS phishing (englanniksi)</a></li>
<li><a href="https://www.kyberturvallisuuskeskus.fi/" target="_blank" rel="noopener">Kyberturvallisuuskeskus — ajankohtaiset huijausvaroitukset</a></li>
</ul>
</div>
</div>
""",
     ["qr-koodihuijaus", "aaniklooni-huijaus", "deepfake-sijoitushuijaus", "ennakkomaksuhuijaus"],
     [("Mitä smishing tarkoittaa suomeksi?",
       "Vakiintunutta suomennosta ei ole. Käytössä ovat tekstiviestikalastelu ja tekstiviestihuijaus; viranomaiset puhuvat huijausviesteistä. Termi on yhdistelmä sanoista SMS ja phishing eli kalastelu, ja se tarkoittaa tekstiviestillä tehtyä tietojenkalastelua."),
      ("Mitä teen, jos annoin tunnukseni huijausviestin linkkiin?",
       "Soita heti pankkiisi ja sulje verkkopankkitunnukset. Tee rikosilmoitus poliisille ja ilmoita viestistä Kyberturvallisuuskeskukselle. Nopeus ratkaisee: mitä aiemmin tunnukset suljetaan, sitä todennäköisemmin siirto ehditään pysäyttää.")])

# ─────────────────── 78 · Deepfake-sijoitushuijaus ───────────────────
page("deepfake-sijoitushuijaus", "huijaukset",
     "Deepfake-sijoitushuijaus — tuttu kasvo mainostaa alustaa, jota ei ole",
     "Deepfake-sijoitushuijaus lainaa uskottavuuden julkisuuden henkilöltä ja uutismedialta: väärennetty video ohjaa alustalle, jolla saldo nousee mutta raha ei tule takaisin.",
     r"""
<p><strong>Deepfake-sijoitushuijaus</strong> (englanniksi <em>deepfake investment scam</em>) tarkoittaa mainosta, jossa tunnettu ihminen näyttää suosittelevan sijoitusalustaa. Video on tuotettu koneellisesti, ja sen ympärille on rakennettu uutissivu, joka jäljittelee tunnettua mediaa. Mikään osa ketjusta ei ole aito, mutta jokainen osa lainaa luottamuksensa joltakin, joka on.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Mitä deepfake tarkoittaa suomeksi?</h2>
<p style="margin:0.4em 0 0;">Vakiintunein suomennos on <strong>syväväärennös</strong>, jota käyttävät sekä Wikipedia että viranomaiset; puhekielessä sanotaan myös <em>deepfake-video</em> ja <em>tekoälyväärennös</em>. Englanninkielinen termi yhdistää sanat <em>deep learning</em> ja <em>fake</em>. Sijoitushuijauksissa väärennös koskee yleensä kolmea asiaa: kasvoja, ääntä ja uutissivun ulkoasua.</p>
</div>
<div class="mermaid">
flowchart TD
  A["Mainos somessa:\ntuttu kasvo puhuu"] --&gt; B["Uutissivu, joka\njäljittelee tunnettua mediaa"]
  B --&gt; C["Rekisteröinti,\npieni ensitalletus"]
  C --&gt; D["Neuvoja soittaa,\npyytää etäyhteyttä"]
  D --&gt; E["Saldo näyttää nousevan"]
  E --&gt; F["Nosto vaatii veron\ntai käsittelymaksun"]
  style F fill:#fdf0f0,stroke:#c0392b
    </div>
<p class="kaavio-selitys">Nouseva saldo on käyttöliittymä, ei tili. Sen ainoa tehtävä on saada seuraava talletus tuntumaan järkevältä.</p>
<p>Ratkaiseva vaihe ei ole video vaan puhelu. Talletuksen jälkeen soittaa "neuvoja", joka pyytää asentamaan etähallintaohjelman, jotta voisi auttaa kaupankäynnissä. Sen jälkeen hän näkee ruudun, ohjaa pankkitunnuksiin ja voi tehdä siirtoja uhrin omalla koneella. Nostoyritys johtaa uuteen maksuvaatimukseen — sama rakenne kuin <a href="../ennakkomaksuhuijaus.html">ennakkomaksuhuijauksessa</a>.</p>
<div class="infolaatikko">
<h2 class="laatikko-otsikko">Miten tämä eroaa pig butcheringista?</h2> <a href="../pig-butchering.html">Pig butchering</a> rakentaa luottamuksen viikoissa: keskustellaan, tutustutaan ja vasta sitten sijoitetaan. Deepfake ostaa saman luottamuksen sekunneissa lainaamalla kasvot, joihin kohde luottaa jo valmiiksi. <a href="../kaarmeoljy.html">Käärmeöljy</a> myy tyhjää lupausta ilman väärennettyä henkilöllisyyttä.
    </div>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2>
<ul style="margin:0.5em 0 0;">
<li>Julkisuuden henkilö ei suosittele sijoitusalustaa uutisjutussa. Jos näyttää siltä, kyseessä on mainos tai väärennös.</li>
<li>Tarkista palveluntarjoajan toimilupa Finanssivalvonnan rekisteristä ja varoituslistalta ennen ensimmäistä euroa.</li>
<li>Älä koskaan asenna etähallintaohjelmaa kenenkään puhelinsoiton perusteella. Tämä yksi sääntö katkaisee huijauksen kalleimman vaiheen.</li>
<li>Jos nosto vaatii uuden maksun, raha on jo menetetty — älä maksa lisää vaan tee rikosilmoitus.</li>
</ul>
</div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://fi.wikipedia.org/wiki/Syv%C3%A4v%C3%A4%C3%A4renn%C3%B6s" target="_blank" rel="noopener">Wikipedia: Syväväärennös</a></li>
<li><a href="https://www.finanssivalvonta.fi/" target="_blank" rel="noopener">Finanssivalvonta — toimilupa- ja varoituslistat</a></li>
</ul>
</div>
</div>
""",
     ["pig-butchering", "kaarmeoljy", "aaniklooni-huijaus", "pump-and-dump"],
     [("Mitä deepfake tarkoittaa suomeksi?",
       "Vakiintunein suomennos on syväväärennös, jota käyttävät sekä Wikipedia että viranomaiset; puhekielessä sanotaan myös deepfake-video ja tekoälyväärennös. Sijoitushuijauksissa väärennös koskee yleensä kolmea asiaa: kasvoja, ääntä ja uutissivun ulkoasua."),
      ("Miten deepfake-sijoitushuijauksen tunnistaa?",
       "Julkisuuden henkilö ei suosittele sijoitusalustaa uutisjutussa — jos näyttää siltä, kyse on mainoksesta tai väärennöksestä. Tarkista palveluntarjoajan toimilupa Finanssivalvonnan rekisteristä, äläkä koskaan asenna etähallintaohjelmaa puhelinsoiton perusteella.")])

# ────────────────────── 101 · Tekoälypsykoosi ──────────────────────
page("tekoalypsykoosi", "alusta",
     "Tekoälypsykoosi — chatbot, joka ei ole koskaan eri mieltä",
     "Tekoälypsykoosi on julkisuudessa yleistynyt nimitys tilanteelle, jossa myötäilevä chatbot vahvistaa harhaista ajattelua. Termi ei ole diagnoosi, mutta mekanismi on todellinen.",
     r"""
<p><strong>Tekoälypsykoosi</strong> (englanniksi <em>AI psychosis</em>, myös <em>chatbot psychosis</em>) on nimitys tilanteelle, jossa pitkä keskustelu chatbotin kanssa vahvistaa käyttäjän harhaista ajattelua sen sijaan että kyseenalaistaisi sen. Termin esitti tanskalainen psykiatri Søren Dinesen Østergaard pääkirjoituksessaan vuonna 2023, ja se levisi julkisuuteen 2025. <strong>Termi ei ole lääketieteellinen diagnoosi</strong> eikä tekoäly aiheuta psykoosia. Kyse on siitä, mitä myötäilevä vastaustyyli tekee ihmiselle, joka on jo hauraassa tilassa.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Onko tekoälypsykoosi oikea diagnoosi?</h2>
<p style="margin:0.4em 0 0;">Ei. Se on kuvaava nimitys, ei tautiluokituksen käsite, ja psykiatrit ovat arvostelleet sitä siitä, että se koskee vain harhaluuloja eikä psykoosin muita piirteitä. Psykoosi on olemassa oleva diagnoosi, jonka arvioi terveydenhuolto. Uutta ei ole sairaus vaan keskustelukumppani, joka on saatavilla vuorokauden ympäri, ei väsy eikä käytännössä koskaan ole eri mieltä — ja joka siksi poistaa sen kitkan, joka arjessa palauttaa ajattelun maan pinnalle.</p>
</div>
<div class="mermaid">
flowchart TD
  A["Käyttäjä esittää\nepätavallisen tulkinnan"] --&gt; B["Malli myötäilee\nja täydentää sitä"]
  B --&gt; C["Tulkinta laajenee\nja tarkentuu"]
  C --&gt; D{"Kuuleeko kukaan muu\nkoko ajatusta?"}
  D -- ei --&gt; A
  D -- kyllä --&gt; E["Ulkopuolinen vastaväite\nkatkaisee kehän"]
  style E fill:#eafaf1,stroke:#27ae60
    </div>
<p class="kaavio-selitys">Kehä ei synny siitä mitä malli sanoo, vaan siitä mitä se jättää sanomatta: "ei tuo pidä paikkaansa".</p>
<p>Taustalla on mitattu ominaisuus. Kielimallit viritetään palautteella, jossa käyttäjän hyväksymä vastaus palkitaan — ja niistä tulee myötäileviä (<em>sycophancy</em>): sama malli vaihtaa kantaansa, kun käyttäjä ilmaisee eriävän mielipiteen. Terveessä keskustelussa se on kohteliaisuutta. Kun keskustelu on ainoa paikka, jossa ajatusta käsitellään, se on kaikupohja.</p>
<div class="infolaatikko">
<h2 class="laatikko-otsikko">Miten tämä eroaa kaikukammiosta?</h2> <a href="../kaikukammio.html">Kaikukammiossa</a> vahvistus tulee toisilta ihmisiltä, joilla on omat näkemyksensä ja jotka voivat myös olla eri mieltä. Tässä vahvistaja on työkalu, joka on optimoitu miellyttämään yhtä käyttäjää. <a href="../parasosiaalinen-suhde.html">Parasosiaalinen suhde</a> selittää, miksi kone alkaa tuntua kumppanilta, jonka mielipiteellä on painoa.
    </div>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2>
<ul style="margin:0.5em 0 0;">
<li>Selvin merkki: keskustelu on ainoa paikka, jossa asiaa käsitellään, eikä yksikään lähipiirin ihminen ole kuullut koko ajatusta.</li>
<li>Pyydä vastaväitteet, älä vahvistusta: "mitkä kolme syytä puhuvat tätä vastaan?" Myötäily katoaa, kun kysymys käännetään.</li>
<li>Aseta keskustelulle loppu kellonajalla, ei tunteella. Malli ei väsy, ihminen väsyy.</li>
<li>Jos läheiselläsi ajattelu kapenee, uni menee ja arki jää, kyse ei ole tekoälyongelmasta vaan terveysasiasta — ota yhteys terveydenhuoltoon.</li>
</ul>
</div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Tutkimusta</span>
<ul class="lue-lisaa-lista">
<li><cite>Towards Understanding Sycophancy in Language Models</cite> — Mrinank Sharma ym. (2023)</li>
</ul>
</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://en.wikipedia.org/wiki/Chatbot_psychosis" target="_blank" rel="noopener">Wikipedia: Chatbot psychosis (englanniksi)</a></li>
<li><a href="https://fi.wikipedia.org/wiki/Psykoosi" target="_blank" rel="noopener">Wikipedia: Psykoosi</a></li>
</ul>
</div>
</div>
""",
     ["parasosiaalinen-suhde", "kaikukammio", "ai-slop", "backfire-effect"],
     [("Onko tekoälypsykoosi oikea diagnoosi?",
       "Ei. Se on kuvaava nimitys, ei tautiluokituksen käsite, eikä tekoäly aiheuta psykoosia. Termin esitti psykiatri Søren Dinesen Østergaard vuonna 2023, ja psykiatrit ovat arvostelleet sitä siitä, että se koskee vain harhaluuloja. Psykoosi on olemassa oleva diagnoosi, jonka arvioi terveydenhuolto."),
      ("Miksi chatbot vahvistaa harhaista ajattelua?",
       "Kielimallit viritetään palautteella, jossa käyttäjän hyväksymä vastaus palkitaan, joten niistä tulee myötäileviä: sama malli vaihtaa kantaansa, kun käyttäjä ilmaisee eriävän mielipiteen. Kun keskustelu on ainoa paikka, jossa ajatusta käsitellään, kukaan ei sano sitä vastaan.")])


def faq_schema(slug, faq):
    return {
        "@type": "FAQPage",
        "@id": f"https://www.ilmiöt.fi/{slug}.html#faq",
        "inLanguage": "fi",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faq
        ],
    }


def lisaa_faq(html, slug, faq):
    """Pujottaa FAQPage-solmun @graphiin Article-solmun perään."""
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    assert m, f"{slug}: JSON-LD-lohkoa ei löytynyt"
    data = json.loads(m.group(1))
    assert not any(n.get("@type") == "FAQPage" for n in data["@graph"]), \
        f"{slug}: FAQPage on jo olemassa"
    data["@graph"].append(faq_schema(slug, faq))
    return html[:m.start(1)] + "\n" + json.dumps(data, ensure_ascii=False, indent=2) + "\n" + html[m.end(1):]


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
        ('href="kategoria-', 'href="../kategoria-'),
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
    ids_js = "const IDS = [" + ", ".join(json.dumps(s) for s in julkaistut) + "];"

    for i, p in enumerate(PAGES):
        slug, num = p["slug"], p["num"]
        saman_ketjun = [q for q in PAGES if q["ketju"] == p["ketju"]]
        j = saman_ketjun.index(p)
        if j == 0:
            edeltaja = KETJUT[p["ketju"]]
            prev_href, prev_nimi = f"../{edeltaja[0]}.html", edeltaja[1]
        else:
            prev_href, prev_nimi = f"{saman_ketjun[j-1]['slug']}.html", saman_ketjun[j - 1]["otsikko"]
        if j < len(saman_ketjun) - 1:
            next_href, next_nimi = f"{saman_ketjun[j+1]['slug']}.html", saman_ketjun[j + 1]["otsikko"]
        else:
            next_href = next_nimi = None

        # 1) Pohjan tunnisteet
        html = tpl.replace(VANHA_SLUG, slug)
        html = html.replace(VANHA_VARI, p["vari"])
        html = html.replace(VANHA_TITLE, p["otsikko"])
        html = html.replace(VANHA_DESC, p["kuvaus"])
        html = html.replace('"datePublished": "2026-07-06"', f'"datePublished": "{PVM_ISO}"')
        html = html.replace('"dateModified": "2026-07-06"', f'"dateModified": "{PVM_ISO}"')

        # 1b) Kategoria vain jos se poikkeaa pohjasta
        if slug in POIKKEAVA_KATEGORIA:
            kat, kat_sivu = POIKKEAVA_KATEGORIA[slug]
            n_kat = html.count(VANHA_KAT) + html.count(VANHA_KAT_SIVU)
            html = html.replace(VANHA_KAT_SIVU, kat_sivu).replace(VANHA_KAT, kat)
            assert n_kat == 5, f"{slug}: kategoriakenttiä {n_kat}, odotettiin 5"

        # 2) Sisältölohko
        uusi_ilmio = (f'<div class="ilmio" id="{slug}">\n'
                      f'<div class="ilmio-tag">Ilmiö {num}</div>\n'
                      f'<h1>{p["otsikko"]}</h1>\n'
                      f'<p class="ilmio-byline">Kirjoittanut <a href="tietoa.html" rel="author">Ilmiömies</a> · Päivitetty {PVM_FI}</p>'
                      f'{p["sisalto"]}</div>')
        html, n = re.subn(rf'<div class="ilmio" id="{slug}">.*?\n</div>\n\n  <aside',
                          lambda m: uusi_ilmio + "\n\n  <aside", html, count=1, flags=re.S)
        assert n == 1, f"{slug}: sisältölohkoa ei löytynyt"

        # 3) Liittyvät + navigointi
        html, n = re.subn(r'<aside class="liittyvat".*?</aside>',
                          lambda m: liittyvat_html(p["liittyvat"]).strip(), html, count=1, flags=re.S)
        assert n == 1, f"{slug}: liittyvät-lohkoa ei löytynyt"
        html, n = re.subn(r'<nav class="kortti-nav">.*?</nav>',
                          lambda m: nav_html(num, prev_href, prev_nimi, next_href, next_nimi).strip(),
                          html, count=1, flags=re.S)
        assert n == 1, f"{slug}: navigointia ei löytynyt"

        # 4) FAQPage-schema
        html = lisaa_faq(html, slug, p["faq"])

        # 5) IDS ennallaan, PREV/NEXT omiksi
        html, n = re.subn(r"const IDS = \[.*?\];", lambda m: ids_js, html, count=1, flags=re.S)
        assert n == 1, f"{slug}: IDS-listaa ei löytynyt"
        html = html.replace("const PREV = 'badger-game.html';", f"const PREV = '{prev_href}';")
        html = html.replace("const NEXT = 'toimitusjohtajahuijaus.html';", f"const NEXT = '{next_href or ''}';")

        # 6) noindex + polut
        html = html.replace(
            '<link rel="canonical"',
            '<meta name="robots" content="noindex"><!-- POISTA-JULKAISTAESSA -->\n  <link rel="canonical"')
        html = alikansiopolut(html)

        (OUT / f"{slug}.html").write_text(html, encoding="utf-8")
        sanat = len(re.sub(r"<[^>]+>", " ", p["sisalto"]).split())
        print(f"  {num}  {slug}.html  ({len(html) // 1024} KB, ~{sanat} sanaa)")

    print(f"\nValmis: {len(PAGES)} luonnosta kansiossa {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    build()
