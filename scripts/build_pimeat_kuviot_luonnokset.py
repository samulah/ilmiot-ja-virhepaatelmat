#!/usr/bin/env python3
"""Generoi Pimeät kuviot (dark patterns) -klusterin sivuluonnokset — 5 kpl.

Lähde: luonnokset/UUDET-KLUSTERIT-PLAN.md § 3 (klusteri 1, kärki).
Sivut sijoittuvat OLEMASSA OLEVAAN kategoriaan "Alustatalous ja algoritmit"
(8 → 13 sivua), joten uutta hub-lohkoa ei tarvita ja lisaa_ilmiot.py toimii
ilman --kortit-valmiina-lippua.

Pohjana aanekas-vahemmisto.html — sama kategoria, joten kategoriakenttiä
(murupolku, articleSection, hub-ankkuri) ei tarvitse korvata lainkaan.

Erot media-erän generaattoriin:
  - "suomeksi"-vastauslohko + FAQPage-schema jo luonnoksessa (aiemmin ne
    lisättiin jälkikäteen seo_vastauslohko.py:llä vain top-15-sivuille)
  - kysymysmuotoiset H2-otsikot alusta asti (GSC-AUDIT-2026-08-13 § 6b:
    kilpailijoilla lähes kaikki, ilmiöt.fi:llä 12 %)

Tuottaa luonnokset/-kansioon 5 sivua, joissa on noindex-meta ja ../-alkuiset
polut. Kansio on kaikkien luonnosten yhteinen (yhdistetty 14.8.2026), joten
skripti kirjoittaa vain omat viisi sivuaan yli — muut luonnokset jäävät koskematta.
Julkaistaessa: täytä lisaa_ilmiot.py:n UUDET-taulukko (taulukko KORVATAAN, ei
täydennetä) ja aja kansion index.html:n tarkistuslista.

Ajo:  python3 scripts/build_pimeat_kuviot_luonnokset.py
"""
import bisect
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "aanekas-vahemmisto.html"
OUT = ROOT / "luonnokset"

PVM_ISO = "2026-08-14"
PVM_FI = "14.8.2026"

# Pohjasivun tunnisteet, jotka korvataan. Kategoria säilyy → ei korvausta.
VANHA_SLUG = "aanekas-vahemmisto"
VANHA_VARI = "#7b241c"
VANHA_TITLE = "Äänekäs vähemmistö — kommenttiosio ei ole mielipidemittari"
VANHA_DESC = ("Äänekäs vähemmistö vääristää kuvan yleisestä mielipiteestä: kärjekkäimmät "
              "kommentoijat näkyvät eniten, kun hiljainen enemmistö ei koskaan vastaa.")

# Erä pujotetaan kategorian viimeisen kortin (aanekas-vahemmisto, 100) perään.
EDELTAJA = ("aanekas-vahemmisto", "Äänekäs vähemmistö — kommenttiosio ei ole mielipidemittari")
ENSIMMAINEN_NUMERO = 101

INDEX = (ROOT / "index.html").read_text(encoding="utf-8")
JULKAISTUJA = len(re.findall(r'<a href="[a-z0-9-]+\.html" class="hub-kortti"', INDEX))
YHTEENSA = JULKAISTUJA + 5

# Omat kortit: slug → (numero, väri, nimi, kuvaus). Numerot ovat alustavia —
# lisaa_ilmiot.py laskee lopulliset ja siirtää 101→ eteenpäin viidellä.
OMAT_KORTIT = {
    "evasteansa": (ENSIMMAINEN_NUMERO, "#0288d1", "Evästeansa",
        "Hyväksyminen on yksi klikkaus, kieltäytyminen viisi — banneri on rakennettu tuottamaan suostumus."),
    "piilokulut": (ENSIMMAINEN_NUMERO + 1, "#ff6f00", "Piilokulut",
        "Mainostettu hinta on ensimmäinen erä; loput valutetaan esiin vasta kun vertailu on tehty."),
    "pakotettu-jatkuvuus": (ENSIMMAINEN_NUMERO + 2, "#3e2723", "Pakotettu jatkuvuus",
        "Ilmainen kokeilu muuttuu laskuksi automaattisesti — ilman muistutusta ja ilman uutta hyväksyntää."),
    "confirmshaming": (ENSIMMAINEN_NUMERO + 3, "#a31545", "Confirmshaming",
        "Kieltäytymisnappi kirjoitetaan itseä alentavaksi: ”Ei kiitos, en halua säästää rahaa”."),
    "oletusasetusansa": (ENSIMMAINEN_NUMERO + 4, "#1b5e20", "Oletusasetusansa",
        "Seuranta ja jakaminen ovat valmiiksi päällä, koska oletusvalinta ratkaisee useimmiten."),
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


def page(slug, otsikko, kuvaus, sisalto, liittyvat, faq):
    num, vari = OMAT_KORTIT[slug][0], OMAT_KORTIT[slug][1]
    PAGES.append(dict(slug=slug, num=num, vari=vari, otsikko=otsikko,
                      kuvaus=kuvaus, sisalto=sisalto, liittyvat=liittyvat, faq=faq))


# ────────────────────────── 101 · Evästeansa ──────────────────────────
page("evasteansa",
     "Evästeansa — hyväksyminen yhdellä klikkauksella, kieltäytyminen viidellä",
     "Evästeansa on evästebanneri, jossa suostumus on yksi klikkaus ja kieltäytyminen viisi. Sääntely vaatii yhtä helppoa hylkäämistä — käytännössä epäsymmetria on sääntö.",
     r"""
<p><strong>Evästeansa</strong> (englanniksi <em>cookie consent dark pattern</em>) on evästebanneri, joka on rakennettu tuottamaan suostumus riippumatta siitä, mitä käyttäjä haluaisi. Kikka ei ole valheessa vaan epäsymmetriassa: <em>Hyväksy kaikki</em> on värillinen nappi heti ensimmäisellä näytöllä, kieltäytyminen taas vaatii asetusvalikon, kytkinlistan ja erillisen tallennuksen. Valinta on sama, hinta ei.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Saako evästeiden hylkäämisen tehdä vaikeammaksi kuin hyväksymisen?</h2>
<p style="margin:0.4em 0 0;">Ei. Tietosuoja-asetus edellyttää, että suostumus on vapaaehtoinen ja yhtä helppo perua kuin antaa. Ranskan tietosuojaviranomainen CNIL sakotti vuodenvaihteessa 2021–2022 Googlea 150 ja Facebookia 60 miljoonalla eurolla nimenomaan siitä, että kieltäytyminen vaati useamman klikkauksen kuin hyväksyminen. Suomessa evästeitä valvoo Traficomin Kyberturvallisuuskeskus ja henkilötietojen käsittelyä tietosuojavaltuutettu.</p>
</div>
<div class="mermaid">
flowchart TD
  B["Banneri avautuu sisällön päälle"] --&gt; H["Hyväksy kaikki\n1 klikkaus, värillinen nappi"]
  B --&gt; A["Asetukset\nharmaa tekstilinkki"]
  A --&gt; K["Kytkinlista,\nosa valmiiksi päällä"]
  K --&gt; T["Tallenna valinnat"]
  T --&gt; P["Banneri palaa\nseuraavalla käynnillä"]
  H --&gt; M["Valinta muistetaan 12 kk"]
  style H fill:#eafaf1,stroke:#27ae60
  style A fill:#fdf0f0,stroke:#c0392b
  style K fill:#fdf0f0,stroke:#c0392b
    </div>
<p class="kaavio-selitys">Molemmat polut päätyvät valintaan. Toinen on yksi klikkaus, toinen viisi — ja vain toinen muistetaan.</p>
<p>Epäsymmetria toimii, koska banneri on este halutun asian edessä. Käyttäjä ei ole tekemässä tietosuojavalintaa vaan lukemassa uutista, ja nopein ulospääsy voittaa. Euroopan komission vuonna 2022 julkaisema selvitys löysi vähintään yhden pimeän kuvion 97 prosentilta suosituimmista EU-sivustoista ja -sovelluksista. Evästebanneri on niistä näkyvin, koska se kohdataan uudelleen joka kerta.</p>
<div class="infolaatikko">
<h2 class="laatikko-otsikko">Miten evästeansa eroaa läheisistä ilmiöistä?</h2> Kyse on käyttöliittymän muodosta, ei suostuttelusta: mitään ei luvata eikä kiistetä, vaan toinen polku tehdään pidemmäksi. <a href="../tilausansa.html">Tilausansa</a> käyttää samaa keinoa peruuttamiseen, <a href="../houkutinvaihtoehto.html">houkutinvaihtoehto</a> taas ohjaa valintaa lisäämällä vaihtoehdon eikä piilottamalla sitä.
    </div>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2>
<ul style="margin:0.5em 0 0;">
<li>Etsi <em>Hylkää kaikki</em> ensimmäiseltä näytöltä. Jos sitä ei ole, banneri ei täytä vaatimusta yhtä helposta kieltäytymisestä.</li>
<li>Avaa <em>oikeutettu etu</em> -välilehti erikseen: kytkimet ovat siellä usein päällä, vaikka olisit hylännyt kaiken muun.</li>
<li>Jos banneri palaa joka käynnillä vain kieltäytyneille, kyse ei ole vahingosta vaan kannustimesta.</li>
<li>Selaimen asetus, joka estää kolmannen osapuolen evästeet, tekee suuren osan bannerin lupauksista merkityksettömiksi.</li>
</ul>
</div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Kirjoja ja selvityksiä</span>
<ul class="lue-lisaa-lista">
<li><cite>Deceptive Patterns</cite> — Harry Brignull (2023)</li>
<li><cite>Behavioural study on unfair commercial practices in the digital environment</cite> — Euroopan komissio (2022)</li>
</ul>
</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://www.deceptive.design/" target="_blank" rel="noopener">deceptive.design — Harry Brignullin hakemisto (englanniksi)</a></li>
<li><a href="https://en.wikipedia.org/wiki/Dark_pattern" target="_blank" rel="noopener">Wikipedia: Dark pattern (englanniksi)</a></li>
</ul>
</div>
</div>
""",
     ["oletusasetusansa", "confirmshaming", "piilokulut", "tilausansa"],
     [("Mikä on evästeansa?",
       "Evästeansa on evästebanneri, jossa suostumuksen antaminen on tehty selvästi helpommaksi kuin sen epääminen: hyväksyminen on yksi värillinen nappi, kieltäytyminen vaatii asetusvalikon, kytkinlistan ja erillisen tallennuksen. Suostumus syntyy tällöin bannerin muodosta eikä käyttäjän tahdosta."),
      ("Saako evästeiden hylkäämisen tehdä vaikeammaksi kuin hyväksymisen?",
       "Ei. Tietosuoja-asetus edellyttää, että suostumus on vapaaehtoinen ja yhtä helppo perua kuin antaa. Ranskan tietosuojaviranomainen CNIL sakotti vuodenvaihteessa 2021–2022 Googlea 150 ja Facebookia 60 miljoonalla eurolla siitä, että kieltäytyminen vaati useamman klikkauksen kuin hyväksyminen.")])

# ────────────────────────── 102 · Piilokulut ──────────────────────────
page("piilokulut",
     "Piilokulut — hinta paljastuu erissä vasta kassalla",
     "Piilokulut eli drip pricing: mainostettu hinta on vain ensimmäinen erä, ja lopullinen summa selviää vasta maksuvaiheessa — sen jälkeen kun vertailu on jo tehty.",
     r"""
<p><strong>Piilokulut</strong> (englanniksi <em>drip pricing</em>) tarkoittaa hinnoittelua, jossa mainostettu luku on vain ensimmäinen erä. Lentolippu maksaa 29 euroa, kunnes mukaan tulee matkatavara, istumapaikka, maksutapalisä ja palvelumaksu. Kokonaishinta ei ole salaisuus — se vain kerrotaan vaiheittain, sen jälkeen kun vertailu vaihtoehtoihin on jo tehty.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Mitä drip pricing tarkoittaa suomeksi?</h2>
<p style="margin:0.4em 0 0;">Vakiintunutta suomennosta ei ole. Käytössä ovat <strong>piilokulut</strong>, <em>pilkottu hinnoittelu</em> ja <em>hinnan valuttaminen</em>; viranomaiset puhuvat kokonaishinnan ilmoittamisesta. EU:n lentoliikenneasetus (1008/2008) edellyttää, että lopullinen hinta veroineen ja maksuineen on nähtävissä koko varausprosessin ajan, ja kuluttajansuojalaki vaatii hinnan ilmoittamista niin, ettei kokonaiskustannus jää arvailun varaan.</p>
</div>
<div class="mermaid">
flowchart TD
  A["Mainos: 29 €"] --&gt; B["Valinta tehty,\nvertailu ohi"]
  B --&gt; C["+ matkatavara"]
  C --&gt; D["+ istumapaikka"]
  D --&gt; E["+ maksutapalisä"]
  E --&gt; F["Maksettavaa 71 €"]
  style A fill:#eafaf1,stroke:#27ae60
  style F fill:#fdf0f0,stroke:#c0392b
    </div>
<p class="kaavio-selitys">Jokainen erä on pieni suhteessa jo tehtyyn valintaan — siksi jatkaminen tuntuu halvemmalta kuin aloittaminen alusta.</p>
<p>Mekanismi on kaksiosainen. Ensimmäinen luku jää ankkuriksi, johon kaikkia myöhempiä lisiä verrataan, ja jokainen vaihe kuluttaa aikaa, joka menetetään jos peruuttaa. Xavier Gabaix ja David Laibson osoittivat vuonna 2006, ettei kilpailu korjaa tätä itsestään: yritys, joka ilmoittaisi kokonaishinnan heti, näyttäisi vertailussa kalliimmalta kuin se on.</p>
<div class="infolaatikko">
<h2 class="laatikko-otsikko">Miten piilokulut eroavat läheisistä ilmiöistä?</h2> <a href="../bait-and-switch.html">Bait and switchissä</a> vaihtuu tuote, piilokuluissa vain hinnan esitystapa — luvattu asia myös toimitetaan. <a href="../shrinkflaatio.html">Shrinkflaatiossa</a> hinta pysyy ja sisältö pienenee. <a href="../hintaankkurointi.html">Hintaankkurointi</a> selittää, miksi ensimmäinen luku jää päähän silloinkin kun se osoittautuu vääräksi.
    </div>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2>
<ul style="margin:0.5em 0 0;">
<li>Vertaile vasta viimeisellä ruudulla. Hakukoneen ja vertailusivuston hinnat ovat eri erästä kuin maksettava summa.</li>
<li>Vie ostos maksusivulle asti kahdella palveluntarjoajalla ennen kuin päätät — vasta siellä luvut ovat vertailukelpoisia.</li>
<li>Tunnista kohta, jossa hinta lakkaa muuttumasta. Jos sitä ei tule ennen korttitietoja, kyse ei ole vertailusta vaan suostuttelusta.</li>
<li>Aika, jonka olet jo käyttänyt varaukseen, ei ole peruste jatkaa — se on <a href="../sunk-cost-harha.html">uponnut kustannus</a>.</li>
</ul>
</div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Tutkimusta</span>
<ul class="lue-lisaa-lista">
<li><cite>Shrouded Attributes, Consumer Myopia, and Information Suppression in Competitive Markets</cite> — Xavier Gabaix &amp; David Laibson (2006)</li>
<li><cite>Deceptive Patterns</cite> — Harry Brignull (2023)</li>
</ul>
</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://en.wikipedia.org/wiki/Drip_pricing" target="_blank" rel="noopener">Wikipedia: Drip pricing (englanniksi)</a></li>
</ul>
</div>
</div>
""",
     ["hintaankkurointi", "bait-and-switch", "pakotettu-jatkuvuus", "shrinkflaatio"],
     [("Mitä drip pricing tarkoittaa suomeksi?",
       "Vakiintunutta suomennosta ei ole. Käytössä ovat piilokulut, pilkottu hinnoittelu ja hinnan valuttaminen; viranomaiset puhuvat kokonaishinnan ilmoittamisesta. Kyse on hinnoittelusta, jossa mainostettu luku on vain ensimmäinen erä ja loput lisät paljastuvat vaiheittain ostoprosessin aikana."),
      ("Ovatko piilokulut laillisia?",
       "Lopullinen hinta on kerrottava. EU:n lentoliikenneasetus (1008/2008) edellyttää, että hinta veroineen ja maksuineen on nähtävissä koko varausprosessin ajan, ja kuluttajansuojalaki vaatii hinnan ilmoittamista niin, ettei kokonaiskustannus jää arvailun varaan. Rajanveto koskee sitä, missä vaiheessa ja miten näkyvästi summa esitetään.")])

# ─────────────────────── 103 · Pakotettu jatkuvuus ───────────────────────
page("pakotettu-jatkuvuus",
     "Pakotettu jatkuvuus — ilmainen kokeilu, joka muuttuu laskuksi ilman kysymystä",
     "Pakotettu jatkuvuus eli forced continuity: ilmainen kokeilu vaatii korttitiedot etukäteen ja muuttuu maksulliseksi automaattisesti, ilman muistutusta ja ilman uutta hyväksyntää.",
     r"""
<p><strong>Pakotettu jatkuvuus</strong> (englanniksi <em>forced continuity</em>) tarkoittaa järjestelyä, jossa ilmainen kokeilu vaatii korttitiedot etukäteen ja muuttuu maksulliseksi tilaukseksi itsestään. Käyttäjä ei tee toista päätöstä: hän tekee ensimmäisen päätöksen ilmaisesta ja saa laskun siitä, ettei tehnyt kolmatta. Muistutus jää tulematta juuri silloin, kun se olisi hyödyllisin.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Mitä forced continuity tarkoittaa suomeksi?</h2>
<p style="margin:0.4em 0 0;">Vakiintunutta suomennosta ei ole. Käytössä ovat <strong>pakotettu jatkuvuus</strong> ja <em>automaattinen jatkuminen</em>; sopimusehdoissa puhutaan jatkuvasta sopimuksesta ja kuluttajaviranomaiset toistuvasta veloituksesta. Etämyynnissä kuluttajalla on kuluttajansuojalain mukaan 14 vuorokauden peruuttamisoikeus, mutta se lasketaan sopimuksen tekemisestä — ei siitä päivästä, jona veloitus alkaa.</p>
</div>
<div class="mermaid">
flowchart TD
  A["Ilmainen kokeilu\nkorttitiedot etukäteen"] --&gt; B["30 vrk käyttöä"]
  B --&gt; C{"Muistuttaako\npalvelu?"}
  C -- ei --&gt; D["Veloitus alkaa\nautomaattisesti"]
  C -- kyllä --&gt; E["Käyttäjä valitsee"]
  D --&gt; F["Peruutus löytyy eri\npaikasta kuin tilaus"]
  style D fill:#fdf0f0,stroke:#c0392b
  style F fill:#fdf0f0,stroke:#c0392b
    </div>
<p class="kaavio-selitys">Tilaus alkaa yhdellä klikkauksella etusivulta; sen lopettaminen alkaa asetuksista, joita ei mainita missään.</p>
<p>Järjestely on laillinen, kun ehdot kerrotaan selvästi ennen tilausta. Raja ylittyy siinä, mitä jätetään tekemättä: veloituspäivää ei muistuteta, kuittia ei lähetetä ennakkoon, ja irtisanominen sijoitetaan valikkoon, johon ei pääse samalta sivulta kuin tilaamiseen. Jokainen näistä on erikseen pieni, ja yhdessä ne ratkaisevat, kuinka moni kokeilija maksaa vuoden.</p>
<div class="infolaatikko">
<h2 class="laatikko-otsikko">Miten pakotettu jatkuvuus eroaa tilausansasta?</h2> <a href="../tilausansa.html">Tilausansa</a> koskee ulospääsyä: peruuttaminen on tehty tahallaan hankalaksi. Pakotettu jatkuvuus koskee ajoitusta — sisäänkäynti on ilmainen ja päätös maksamisesta tehdään puolestasi hiljaisuudella. <a href="../lowball-hinnoittelu.html">Lowball-hinnoittelussa</a> taas aloitushinta on tosi mutta väliaikainen.
    </div>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2>
<ul style="margin:0.5em 0 0;">
<li>Merkitse veloituspäivä kalenteriin heti tilauksen jälkeen — kahta päivää aikaisemmaksi.</li>
<li>Peruuta tilaus samana päivänä kun aloitat kokeilun. Useimmat palvelut antavat käyttöoikeuden kokeilujakson loppuun asti.</li>
<li>Etsi ehdoista sanat <em>jatkuu automaattisesti</em>, <em>toistaiseksi voimassa</em> ja <em>irtisanomisaika</em> ennen kuin annat korttitiedot.</li>
<li>Käy tiliotteen toistuvat veloitukset läpi kerran vuodessa; pakotettu jatkuvuus näkyy juuri niissä maksuissa, joita ei muista tehneensä.</li>
</ul>
</div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Kirjoja</span>
<ul class="lue-lisaa-lista">
<li><cite>Deceptive Patterns</cite> — Harry Brignull (2023)</li>
</ul>
</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://en.wikipedia.org/wiki/Negative_option_billing" target="_blank" rel="noopener">Wikipedia: Negative option billing (englanniksi)</a></li>
</ul>
</div>
</div>
""",
     ["tilausansa", "piilokulut", "lowball-hinnoittelu", "oletusasetusansa"],
     [("Mitä forced continuity tarkoittaa suomeksi?",
       "Vakiintunutta suomennosta ei ole. Käytössä ovat pakotettu jatkuvuus ja automaattinen jatkuminen; sopimusehdoissa puhutaan jatkuvasta sopimuksesta. Kyse on järjestelystä, jossa ilmainen kokeilu vaatii korttitiedot etukäteen ja muuttuu maksulliseksi tilaukseksi ilman erillistä hyväksyntää."),
      ("Miten pakotetulta jatkuvuudelta välttyy?",
       "Merkitse veloituspäivä kalenteriin heti tilauksen jälkeen tai peruuta tilaus samana päivänä kun aloitat kokeilun — useimmat palvelut antavat käyttöoikeuden kokeilujakson loppuun asti. Etämyynnissä kuluttajalla on lisäksi 14 vuorokauden peruuttamisoikeus, joka lasketaan sopimuksen tekemisestä.")])

# ─────────────────────── 104 · Confirmshaming ───────────────────────
page("confirmshaming",
     "Confirmshaming — kieltäytymisnappi, joka nolaa käyttäjän",
     "Confirmshaming tarkoittaa kieltäytymisvaihtoehtoa, joka on kirjoitettu itseä alentavaksi: ”Ei kiitos, en halua säästää rahaa”. Nolaus on suunniteltu osa nappia.",
     r"""
<p><strong>Confirmshaming</strong> tarkoittaa kieltäytymisvaihtoehtoa, joka on kirjoitettu käyttäjän suuhun itseä alentavana. Ponnahdusikkunan alalaidassa lukee <em>Ei kiitos, en halua säästää rahaa</em> tai <em>Jatkan mieluummin ilman parempaa työpaikkaa</em>. Nappi ei kerro mitään tuotteesta — se kertoo jotain lukijasta, ja juuri siinä on koko kikka.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Mitä confirmshaming tarkoittaa suomeksi?</h2>
<p style="margin:0.4em 0 0;">Vakiintunutta suomennosta ei ole. Sanasta sanaan kyse on vahvistuksen yhteydessä tapahtuvasta häpäisystä; suomeksi ilmiöstä puhutaan <em>syyllistävänä kieltäytymisenä</em> tai <em>nolaavana ei-napina</em>. Termi vakiintui 2010-luvun puolivälissä, kun verkkoon alettiin kerätä esimerkkejä tällaisista napeista. Sivusto käyttää englanninkielistä muotoa samasta syystä kuin <a href="../rage-bait.html">rage baitin</a> kohdalla: keksitty suomennos ei vastaisi sitä, mitä ihmiset todella sanovat.</p>
</div>
<div class="mermaid">
flowchart TD
  A["Ponnahdusikkuna\nkeskeyttää lukemisen"] --&gt; B["Kyllä-nappi:\nsuuri, värillinen"]
  A --&gt; C["Ei-nappi:\npieni, harmaa teksti"]
  C --&gt; D["”Ei kiitos, en halua\nsäästää rahaa”"]
  D --&gt; E["Kieltäytyminen vaatii\nväitteen itsestä"]
  style B fill:#eafaf1,stroke:#27ae60
  style D fill:#fdf0f0,stroke:#c0392b
    </div>
<p class="kaavio-selitys">Kumpikin nappi vie eteenpäin. Vain toisessa on hinta, jota ei mitata rahassa.</p>
<p>Keino toimii, koska ihminen ei mielellään vahvista itsestään väitettä, jonka joku muu on kirjoittanut. Vaikutus on kuitenkin lyhyt: napin sävy jää mieleen silloinkin, kun tarjous unohtuu, ja sähköpostilistalle päätyy ihmisiä, jotka liittyivät ärsyyntyneinä. Tästä syystä confirmshaming on pimeistä kuvioista helpoimmin havaittava — se on ainoa, joka kertoo lukijalle suoraan, mitä mieltä sivusto on hänestä.</p>
<div class="infolaatikko">
<h2 class="laatikko-otsikko">Miten confirmshaming eroaa läheisistä ilmiöistä?</h2> <a href="../painostusclose.html">Painostusclose</a> käyttää aikarajaa ja <a href="../vastavuoroisuuden-ansa.html">vastavuoroisuuden ansa</a> vastapalvelusta. Confirmshaming ei tarjoa mitään eikä uhkaa millään: se tekee kieltäytymisestä epämiellyttävän lauseen, joka on pakko lausua ääneen itselle.
    </div>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2>
<ul style="margin:0.5em 0 0;">
<li>Lue kieltäytymisnappi ääneen. Jos se kuvailee sinua eikä valintaasi, tekstin on kirjoittanut joku, jolla on asiassa etu.</li>
<li>Sulje ikkuna ristillä tai Esc-näppäimellä — kumpikaan ei vaadi vastaamista kysymykseen.</li>
<li>Muista, että nappi on kirjoitettu ennen kuin kukaan tiesi sinusta mitään. Sen väite ei koske sinua.</li>
<li>Jos rakennat itse tällaista lomaketta: neutraali <em>Ei kiitos</em> tuottaa vähemmän liittyjiä ja enemmän niitä, jotka pysyvät.</li>
</ul>
</div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Kirjoja</span>
<ul class="lue-lisaa-lista">
<li><cite>Deceptive Patterns</cite> — Harry Brignull (2023)</li>
</ul>
</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://www.deceptive.design/types/confirmshaming" target="_blank" rel="noopener">deceptive.design: Confirmshaming (englanniksi)</a></li>
</ul>
</div>
</div>
""",
     ["evasteansa", "oletusasetusansa", "painostusclose", "vastavuoroisuuden-ansa"],
     [("Mitä confirmshaming tarkoittaa suomeksi?",
       "Vakiintunutta suomennosta ei ole. Sanasta sanaan kyse on vahvistuksen yhteydessä tapahtuvasta häpäisystä; suomeksi puhutaan syyllistävästä kieltäytymisestä tai nolaavasta ei-napista. Käytännössä kieltäytymisvaihtoehto on kirjoitettu käyttäjän suuhun itseä alentavana, esimerkiksi ”Ei kiitos, en halua säästää rahaa”."),
      ("Miksi confirmshaming toimii?",
       "Ihminen ei mielellään vahvista itsestään väitettä, jonka joku muu on kirjoittanut. Kieltäytyminen vaatii tällöin pienen myönnytyksen omasta järkevyydestä tai kunnianhimosta, ja hyväksyminen on nopeampi tapa päästä eroon ikkunasta. Vaikutus on kuitenkin lyhyt ja jättää jälkeensä ärsyyntyneen käyttäjän.")])

# ─────────────────────── 105 · Oletusasetusansa ───────────────────────
page("oletusasetusansa",
     "Oletusasetusansa — valinta on tehty valmiiksi palvelun eduksi",
     "Oletusasetusansa: seuranta, jakaminen ja uutiskirje ovat valmiiksi päällä, koska oletusvalinta ratkaisee useimmiten. Tietosuoja-asetus vaatii päinvastaista.",
     r"""
<p><strong>Oletusasetusansa</strong> (englanniksi <em>privacy zuckering</em>, taustalla <em>default effect</em>) tarkoittaa palvelua, jonka asetukset on viritetty valmiiksi palvelun eduksi eikä käyttäjän. Sijainti on päällä, profiili on julkinen, uutiskirje on tilattu ja markkinointilupa on annettu — kaikki ilman että kukaan on valehdellut. Valinta on olemassa, mutta se on tehty jo puolestasi.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Mitä privacy zuckering tarkoittaa?</h2>
<p style="margin:0.4em 0 0;">Termin esitti Electronic Frontier Foundationin Tim Jones vuonna 2010, ja se on nimetty Mark Zuckerbergin mukaan: käyttäjä houkutellaan jakamaan enemmän kuin hän tarkoitti. Suomeksi termiä ei käytetä — puhutaan oletusasetuksista. Tietosuoja-asetuksen 25 artikla vaatii päinvastaista kuin ansa tekee: oletusarvoisesti saa käsitellä vain ne tiedot, jotka ovat käyttötarkoituksen kannalta välttämättömiä.</p>
</div>
<div class="mermaid">
flowchart TD
  A["Tili luodaan"] --&gt; B["Oletukset päällä:\nseuranta, jakaminen,\nmarkkinointi"]
  B --&gt; C{"Käykö käyttäjä\nasetukset läpi?"}
  C -- ei --&gt; D["Oletus jää voimaan"]
  C -- kyllä --&gt; E["12 valikkoa,\n40 kytkintä"]
  E --&gt; F["Päivitys tuo\nuuden ominaisuuden\nja uuden oletuksen"]
  F --&gt; B
  style D fill:#fdf0f0,stroke:#c0392b
    </div>
<p class="kaavio-selitys">Oletus ei ole kertaluontoinen valinta vaan kehä: jokainen uusi ominaisuus palauttaa lähtötilanteen.</p>
<p>Oletusarvon voima on mitattu tarkasti. Eric Johnson ja Daniel Goldstein vertasivat vuonna 2003 Euroopan maita, joissa elinluovutukseen joko liitytään tai siitä poistutaan: suostumusaste vaihteli muutamasta prosentista lähes sataan pelkän lomakkeen oletusvalinnan mukaan. Kyse ei siis ole laiskuudesta vaan siitä, että oletus luetaan suositukseksi — jonkun asiantuntevan arvioksi siitä, mikä on tavallista.</p>
<div class="infolaatikko">
<h2 class="laatikko-otsikko">Miten oletusasetusansa eroaa läheisistä ilmiöistä?</h2> <a href="../houkutinvaihtoehto.html">Houkutinvaihtoehto</a> ohjaa valintaa lisäämällä vaihtoehdon, <a href="../hintaankkurointi.html">hintaankkurointi</a> ensimmäisellä luvulla. Oletusasetusansa ei kysy mitään. <a href="evasteansa.html">Evästeansa</a> on sen tunnetuin erikoistapaus, jossa oletukset on pakattu yhteen banneriin.
    </div>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2>
<ul style="margin:0.5em 0 0;">
<li>Käy asetukset läpi heti tilin luomisen jälkeen, ennen kuin palvelusta tulee tarpeellinen. Silloin kieltäytyminen ei vielä maksa mitään.</li>
<li>Lue oletus tarjouksena, älä suosituksena. Se kertoo, mikä hyödyttää palvelua — ei mikä on sinulle tavallista.</li>
<li>Tarkista asetukset uudelleen suurten päivitysten jälkeen: uusi ominaisuus tuo lähes aina oman oletuksensa päälle.</li>
<li>Kiinnitä huomiota kaksoiskiellettyihin ruutuihin (<em>en halua, etten saisi tarjouksia</em>) — muotoilu on merkki siitä, että vastaus on jo valittu.</li>
</ul>
</div>
<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Tutkimusta ja kirjoja</span>
<ul class="lue-lisaa-lista">
<li><cite>Do Defaults Save Lives?</cite> — Eric J. Johnson &amp; Daniel Goldstein, Science (2003)</li>
<li><cite>Nudge</cite> — Richard Thaler &amp; Cass Sunstein (2008)</li>
</ul>
</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://en.wikipedia.org/wiki/Default_effect" target="_blank" rel="noopener">Wikipedia: Default effect (englanniksi)</a></li>
</ul>
</div>
</div>
""",
     ["evasteansa", "confirmshaming", "houkutinvaihtoehto", "pakotettu-jatkuvuus"],
     [("Mitä privacy zuckering tarkoittaa?",
       "Termin esitti Electronic Frontier Foundationin Tim Jones vuonna 2010, ja se on nimetty Mark Zuckerbergin mukaan. Se tarkoittaa palvelua, jonka oletusasetukset saavat käyttäjän jakamaan enemmän tietoa kuin hän tarkoitti. Suomeksi termiä ei käytetä — puhutaan oletusasetuksista."),
      ("Miksi oletusasetus ratkaisee valinnan?",
       "Oletus luetaan suositukseksi: arvioksi siitä, mikä on tavallista ja järkevää. Eric Johnson ja Daniel Goldstein vertasivat vuonna 2003 maita, joissa elinluovutukseen joko liitytään tai siitä poistutaan, ja suostumusaste vaihteli muutamasta prosentista lähes sataan pelkän lomakkeen oletusvalinnan mukaan.")])


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
    uusi = json.dumps(data, ensure_ascii=False, indent=2)
    return html[:m.start(1)] + "\n" + uusi + "\n" + html[m.end(1):]


def alikansiopolut(html):
    """Muuntaa juuren polut toimimaan alikansiosta."""
    korvaukset = [
        ('href="style.css', 'href="../style.css'),
        ('href="fonts/', 'href="../fonts/'),
        ('href="favicon.svg"', 'href="../favicon.svg"'),
        ('src="favicon.svg"', 'src="../favicon.svg"'),
        ("s.src = 'js/mermaid.min.js';", "s.src = '../js/mermaid.min.js';"),
        ('href="index.html"', 'href="../index.html"'),
        ('href="tietoa.html"', 'href="../tietoa.html"'),
        # murupolun kategorialinkki (lisätty sivuille 28.7., media-erän
        # generaattori ei sitä vielä tuntenut)
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

        # 1) Pohjan tunnisteet (id:t, URL:t, CSS-säännöt, otsikot, päivät)
        html = tpl.replace(VANHA_SLUG, slug)
        html = html.replace(VANHA_VARI, p["vari"])
        html = html.replace(VANHA_TITLE, p["otsikko"])
        html = html.replace(VANHA_DESC, p["kuvaus"])
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

        # 4) FAQPage-schema (vastauslohkon kysymykset)
        html = lisaa_faq(html, slug, p["faq"])

        # 5) IDS palautetaan alkuperäisenä (kohta 1 muutti myös listan id:n)
        html, n = re.subn(r"const IDS = \[.*?\];", lambda m: ids_js, html, count=1, flags=re.S)
        assert n == 1, f"{slug}: IDS-listaa ei löytynyt"
        html = html.replace("const PREV = '1-prosentin-saanto.html';", f"const PREV = '{prev_href}';")
        html = html.replace("const NEXT = 'viherpesu.html';", f"const NEXT = '{next_href or ''}';")

        # 6) noindex-luonnosmerkintä
        html = html.replace(
            '<link rel="canonical"',
            '<meta name="robots" content="noindex"><!-- POISTA-JULKAISTAESSA -->\n  <link rel="canonical"')

        # 7) Polut alikansiosta
        html = alikansiopolut(html)

        (OUT / f"{slug}.html").write_text(html, encoding="utf-8")

        sanat = len(re.sub(r"<[^>]+>", " ", p["sisalto"]).split())
        print(f"  {num}  {slug}.html  ({len(html) // 1024} KB, ~{sanat} sanaa)")

    print(f"\nValmis: {len(PAGES)} luonnosta kansiossa {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    build()
