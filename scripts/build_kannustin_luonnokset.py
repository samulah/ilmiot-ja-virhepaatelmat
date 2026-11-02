#!/usr/bin/env python3
"""Generoi luonnokset 16. kategorialle "Kannustimet ja sivuvaikutukset" (9 ilmiötä).

Tausta: kobravaikutus kirjoitettiin 21.10.2026 yksittäiseksi luonnokseksi
Goodhartin lain perään (numero 40). 22.10. päätettiin koota siitä ja kahdeksasta
uudesta sivusta oma kategoria: hyvää tarkoittava sääntö, joka muuttaa käytöstä
tavalla, jota laatija ei ennakoinut. Kobravaikutus siirtyy siksi tähän erään,
eikä sitä enää julkaista Goodhartin lain perään.

Erän rakenne:
  166-168  kannustin kääntyy itseään vastaan: kobravaikutus, kannustinloukku,
           kynnysefekti
  169-171  joku muu kantaa riskin tai hyöty kuluu: moraalikato,
           riskikompensaatio, Jevonsin paradoksi
  172-174  yhteinen resurssi, kielto ja purkaminen: yhteismaan tragedia,
           kiellon rautainen laki, Chestertonin aita

Jokaisessa on vähintään yksi suomalainen tapaus; lähteet tarkistettiin
22.10.2026. Omat suomennokset, jotka käyttäjän on vielä tarkistettava:
"kynnysefekti" (notch / bunching) ja "kiellon rautainen laki" (iron law of
prohibition).

Numerot 166-174 olettavat, että sivustolla on julkaisuhetkellä 165 ilmiötä.
index.html:ään ei kirjoiteta mitään: hub-lohko kirjoitetaan tiedostoon
luonnokset/kannustin-hub-lohko.html, josta build_kategoriat.py --luonnos lukee
sen kategoriasivun esikatselua varten.

Erot trollauserän generaattoriin (build_trollaus_luonnokset.py):
  - pohja on goodhartin-laki.html, ja SEO-lohko johdetaan sen omasta
    JSON-LD:stä, joten skeema pysyy samanmuotoisena kuin seo_schema.py:n tulos
  - FAQPagea ei lisätä (FAQ-rikastetulokset lopetettiin 7.5.2026)
  - <title> asetetaan erikseen (ks. lisaa_ilmiot.py:tarkista_title)

Julkaisu: hub-lohko index.html:ään käsin trollaus-lohkon perään, lisaa_ilmiot.py:n
UUDET-taulukko tällä erällä, sitten
    python3 scripts/lisaa_ilmiot.py --kortit-valmiina --kirjoita

Ajo:  python3 scripts/build_kannustin_luonnokset.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from seo_rakenne import tunniste  # noqa: E402  (sama ankkurisääntö kuin julkaisussa)

TEMPLATE = ROOT / "goodhartin-laki.html"
OUT = ROOT / "luonnokset"

PVM_ISO = "2026-10-22"
PVM_FI = "22.10.2026"

VANHA_SLUG = "goodhartin-laki"
VANHA_KAT_SIVU = "kategoria-byrokratia-ja-organisaatio.html"
VANHA_KAT_NIMI = "Byrokratia ja organisaatio"

KAT_ID = "kannustimet-ja-sivuvaikutukset"
KAT_NIMI = "Kannustimet ja sivuvaikutukset"
KAT_SIVU = f"kategoria-{KAT_ID}.html"
KAT_NRO = 16
KAT_KUVAUS = ("Hyvää tarkoittava sääntö muuttaa käytöstä tavalla, jota sen laatija ei "
              "ennakoinut. Kobravaikutus, kannustinloukku, moraalikato ja yhteismaan "
              "tragedia — ja Chestertonin aita, joka muistuttaa, että purkaminenkin on päätös.")

# edellinen erä (149-165) — uuden kategorian PREV-ketju kiinnittyy sen viimeiseen
EDELTAJA = ("trollin-ruokkiminen", "Älä ruoki trollia — milloin hiljaisuus toimii ja milloin ei")

YHTEENSA = 174

# slug -> (numero, väri, nimi, kortin kuvaus)
OMAT_KORTIT = {
    # kannustin kääntyy itseään vastaan
    "kobravaikutus": (166, "#a04000", "Kobravaikutus",
        "Palkkio ongelman korjaamisesta tekee ongelmasta kannattavan — ja pahemman."),
    "kannustinloukku": (167, "#8d6e63", "Kannustinloukku",
        "Verot ja leikkautuvat tuet vievät lisätulosta lähes kaiken: työ ei kannata, vaikka sitä olisi."),
    "kynnysefekti": (168, "#6d4c41", "Kynnysefekti",
        "Kun sääntö muuttuu jyrkästi rajan kohdalla, ihmiset ja yritykset asettuvat juuri rajan alle."),
    # joku muu kantaa riskin tai hyöty kuluu
    "moraalikato": (169, "#5d4037", "Moraalikato",
        "Kun joku muu maksaa tappiot, riskiä otetaan enemmän — Suomen pankkikriisi oppikirjaesimerkkinä."),
    "riskikompensaatio": (170, "#e65100", "Riskikompensaatio",
        "Turvallisuuden tunne lisää riskinottoa, ja osa turvatoimen hyödystä kuluu kovempaan menoon."),
    "jevonsin-paradoksi": (171, "#2e7d32", "Jevonsin paradoksi",
        "Kun käyttö tehostuu, sitä käytetään enemmän: säästö kuluu osin tai kokonaan lisäkulutukseen."),
    # yhteinen resurssi, kielto ja purkaminen
    "yhteismaan-tragedia": (172, "#558b2f", "Yhteismaan tragedia",
        "Jokaisen kannattaa ottaa yhteisestä vähän lisää, kunnes yhteistä ei enää ole."),
    "kiellon-rautainen-laki": (173, "#37474f", "Kiellon rautainen laki",
        "Kun päihde kielletään, markkinoille jää sen väkevin muoto: kieltolain Suomessa pirtu, ei olut."),
    "chestertonin-aita": (174, "#455a64", "Chestertonin aita",
        "Älä pura sääntöä ennen kuin tiedät, miksi se on olemassa — ongelma voi olla piilossa, koska sääntö toimii."),
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
    assert len(kortit) == 165, f"kortteja {len(kortit)}, odotettiin 165"
    assert not set(kortit) & set(OMAT_KORTIT), "erän slug on jo julkaistu"
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


def seo_lohko(pohja_ld, slug, otsikko, termi, title, kuvaus):
    """Koko <!-- SEO --> … </script> uudelleen. JSON-LD on pohjasivun oma,
    vain sivukohtaiset kentät vaihdetaan — samat, jotka seo_schema.py johtaa."""
    url = f"https://www.ilmiöt.fi/{slug}.html"
    ld = json.loads(pohja_ld)
    murut, artikkeli = ld["@graph"]
    assert murut["@type"] == "BreadcrumbList" and artikkeli["@type"] == "Article"
    murut["itemListElement"][1].update(
        name=KAT_NIMI, item=f"https://www.ilmiöt.fi/{KAT_SIVU}")
    murut["itemListElement"][2].update(name=otsikko, item=url)
    artikkeli.update({"@id": f"{url}#article", "url": url, "headline": otsikko,
                      "description": kuvaus, "articleSection": KAT_NIMI,
                      "datePublished": PVM_ISO, "dateModified": PVM_ISO})
    artikkeli["image"]["url"] = "https://www.ilmiöt.fi/og/brand.png"
    artikkeli["about"].update(name=termi, description=kuvaus)
    ld_teksti = json.dumps(ld, ensure_ascii=False, indent=2)
    return f'''  <!-- SEO -->
  <meta name="description" content="{kuvaus}">
  <meta name="robots" content="noindex"><!-- POISTA-JULKAISTAESSA -->
  <link rel="canonical" href="{url}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{kuvaus}">
  <meta property="og:url" content="{url}">
  <meta property="og:type" content="article">
  <meta property="og:locale" content="fi_FI">
  <meta property="og:site_name" content="Ilmiöitä — Miten valta toimii">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{kuvaus}">
  <meta property="og:image" content="https://www.ilmiöt.fi/og/brand.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Ilmiöitä — Miten valta toimii">
  <meta name="twitter:image" content="https://www.ilmiöt.fi/og/brand.png">
  <style>.ilmio h1{{margin-top:0;font-family:'Spectral',Georgia,serif;}}</style>
  <script type="application/ld+json">
{ld_teksti}
</script>'''


PAGES = []


def page(slug, otsikko, title, kuvaus, sisalto, liittyvat):
    """otsikko = h1, title = <title> ja og:title, kuvaus = metakuvaus (≤ 160 merkkiä)."""
    assert len(kuvaus) <= 165, f"{slug}: metakuvaus {len(kuvaus)} merkkiä"
    assert all(s in KORTIT for s in liittyvat), f"{slug}: tuntematon liittyvä ilmiö"
    PAGES.append(dict(slug=slug, num=OMAT_KORTIT[slug][0], otsikko=otsikko, title=title,
                      kuvaus=kuvaus, sisalto=sisalto, liittyvat=liittyvat))


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


# ────────────────────────── 166 · Kobravaikutus ──────────────────────────
# Teksti siirretty luonnoksesta 21.10.2026; tapaukset tarkennettu 22.10.
page("kobravaikutus",
     "Kobravaikutus — kun palkkio pahentaa ongelmaa",
     "Kobravaikutus — kun palkkio pahentaa ongelmaa | Ilmiöitä",
     "Kobravaikutus: ongelman korjaamiseksi luotu palkkio pahentaa ongelmaa. Esimerkit Hanoista, pikavippien korkokatosta ja työttömyysputkesta sekä vastakeinot.",
     r"""
<p>Tarinan mukaan siirtomaa-ajan Delhissä maksettiin palkkio jokaisesta tapetusta kobrasta. Ihmiset alkoivat kasvattaa kobria, ja kun hallinto huomasi tämän ja lopetti palkkion, kasvattajat päästivät arvottomiksi käyneet käärmeet vapaaksi. Kobria oli lopulta enemmän kuin alussa. Saksalainen taloustieteilijä Horst Siebert antoi ilmiölle nimen (<em>cobra effect</em>, 2001). Delhin tarinalle ei ole löydetty aikalaislähteitä, mutta sama kuvio on dokumentoitu monesti muualla.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Mitä kobravaikutus tarkoittaa?</h2>
<p style="margin:0.4em 0 0;"><strong>Kobravaikutus</strong> tarkoittaa, että ongelman korjaamiseksi luotu kannustin pahentaa ongelmaa. Palkkio maksetaan todisteesta (tapettu käärme, rotan häntä, toteutunut myynti), ja kun todisteen tuottaminen tulee halvemmaksi kuin ongelman ratkaiseminen, ihmiset alkavat tuottaa todisteita. Joskus he tuottavat niiden mukana itse ongelmaakin.</p>
</div>
<div class="mermaid">
flowchart TD
  A["Ongelma X"] --&gt; B["Palkkio jokaisesta\npoistetusta X:stä"]
  B --&gt; C["X:n tuottaminen\nalkaa kannattaa"]
  C --&gt; D["Palkkioita maksetaan —\nX ei vähene"]
  D --&gt; E["Palkkio lopetetaan"]
  E --&gt; F["Varasto vapautuu:\nX pahempi kuin alussa"]
  style C fill:#fff3cd,stroke:#f39c12
  style F fill:#fdf0f0,stroke:#c0392b
    </div>
<p class="kaavio-selitys">Kobravaikutus: kannustin kääntää kehityksen suunnan, ja lopettaminen pahentaa tilannetta entisestään.</p>
<p>Ero <a href="goodhartin-laki.html">Goodhartin lakiin</a> on suunnassa. Goodhartin laissa mittari irtoaa tavoitteesta, ja tavoite jää saavuttamatta. Kobravaikutuksessa ongelma kasvaa, koska sääntö palkitsee juuri siitä, mitä sen piti vähentää.</p>
<div class="infolaatikko">
<h2 class="laatikko-otsikko">Dokumentoituja tapauksia:</h2>
<ul style="margin:0.5em 0 0;">
<li><strong>Hanoin rotat (1902):</strong> Ranskalainen siirtomaahallinto maksoi jokaisesta rotan hännästä. Pian kaduilla juoksi hännättömiä rottia. Pyytäjät katkaisivat hännän ja päästivät rotan lisääntymään, ja kaupungin laitamille ilmestyi rottafarmeja.</li>
<li><strong>Pikavippien korkokatto (Suomi, 2013):</strong> Vuonna 2012 pienlainayhtiön uusi laina oli keskimäärin 254 euroa. Kesäkuussa 2013 alle 2 000 euron lainoille tuli noin 50 prosentin korkokatto. Yhtiöt siirtyivät myymään vähintään 2 000 euron luottolimiittejä, joiden todellinen vuosikorko saattoi ylittää 100 prosenttia. Pienestä ja lyhyestä velasta tuli suuri ja pitkä. Katto ulotettiin kaikkiin kuluttajaluottoihin syyskuussa 2019.</li>
<li><strong>Työttömyysputki (Suomi, 1997):</strong> Ikääntynyt työtön sai päivärahaa 60-vuotiaaksi ja siirtyi sitten työttömyyseläkkeelle. Turvan piti suojata vaikeasti työllistyviä, mutta se teki putki-ikäisen irtisanomisesta helpon reitin varhaiseläkkeelle. Kun putken alaikäraja nostettiin 53 vuodesta 55 vuoteen, 53–54-vuotiaiden työttömyysriski pieneni ja jaksot lyhenivät. Ikäryhmä ei enää juuri eronnut 50–52-vuotiaista.</li>
<li><strong>Käänteinen esimerkki – maakotka (Suomi, 1998):</strong> Kotkien porovahingot korvataan paliskunnalle pesivien kotkien reviirien perusteella, ja onnistunut pesintä nostaa korvausta. Paliskunta siis hyötyy siitä, että kotka pesii. 1970-luvulla pesiviä pareja arvioitiin olevan noin sata, nykyään 330–464. Rengastajien mukaan korvausmalli oli ratkaiseva.</li>
</ul>
</div>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Testikysymys kuuluu: miten tästä palkkiosta voisi hyötyä pahentamalla ongelmaa? Toinen kysymys on, mitä tapahtuu sinä päivänä, kun palkkio lopetetaan. Jos vastaus on varasto, joka vapautuu, kobravaikutus on jo rakenteessa. Vastakeinot: palkitse lopputuloksesta (kobrakanta pienenee), älä kappalemäärästä (tapetut kobrat); muista, että jokainen raja kuten &rdquo;alle 2 000 euroa&rdquo; houkuttelee siirtymään rajan yli (ks. <a href="kynnysefekti.html">kynnysefekti</a>), ja kysy ennen päätöstä, mihin kannustin todennäköisesti siirtää toimintaa; kokeile pienessä mittakaavassa ja seuraa kokonaistilannetta, älä pelkkää palkittua lukua; ja kysy niiltä, joita kannustin koskee. He löytävät porsaanreiät ensimmäisinä.
    </div>
""" + lue_lisaa(
        [("Der Kobra-Effekt", "Horst Siebert (2001)"),
         ("The Great Hanoi Rat Hunt", "Michael G. Vann (2018)")],
        [("https://en.wikipedia.org/wiki/Perverse_incentive", "Wikipedia: Perverse incentive (englanniksi)"),
         ("https://www.aalto.fi/sites/g/files/flghsv161/files/2020-05/KorkokattoLuotonenPuttonenRantapuska5-5-2020.pdf",
          "Luotonen, Puttonen &amp; Rantapuska: Korona-ajan korkokatto ei tuo helpotusta kuluttajalle (Aalto-yliopisto, 2020)"),
         ("https://urn.fi/URN:ISBN:951-561-638-7",
          "Kyyrä &amp; Wilke: Reduction in the Long-Term Unemployment of the Elderly (VATT, 2006, englanniksi)"),
         ("https://www.apu.fi/artikkelit/maakotka-oli-kadota-korvaus-poronhoitajille-muutti-kaiken",
          "Apu: Maakotka oli kadota – korvaus poronhoitajille muutti kaiken")]),
     ["goodhartin-laki", "kannustinloukku", "kynnysefekti", "moraalikato", "streisand-ilmio"])


# ────────────────────────── 167 · Kannustinloukku ──────────────────────────
page("kannustinloukku",
     "Kannustinloukku — kun työ ei kannata",
     "Kannustinloukku — miksi lisätyö ei aina kannata? | Ilmiöitä",
     "Kannustinloukku: verot ja leikkautuvat tuet vievät lisätulosta lähes kaiken. Vuonna 2021 loukussa oli 136 500 työtöntä. Näin loukku syntyy ja näin sen tunnistaa.",
     r"""
<p><strong>Kannustinloukku</strong> (engl. <em>welfare trap</em>) on tilanne, jossa työn vastaanottaminen tai lisätyö ei juuri kasvata käteen jäävää tuloa. Jokainen ansaittu euro nostaa veroja ja pienentää samalla useampaa tukea. Yksikään sääntö ei ole kohtuuton, mutta yhdessä ne voivat viedä lisätulosta lähes kaiken.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Mitä kannustinloukku tarkoittaa?</h2>
<p style="margin:0.4em 0 0;">Loukussa oleva ihminen ei ole laiska. Hän laskee oikein. Mittarina on <strong>työllistymisveroaste</strong>: kuinka suuri osa palkasta katoaa veroihin ja menetettyihin tukiin, kun työtön työllistyy. Jos veroaste on 80 prosenttia, 1 000 euron palkalla käteen jää vain 200 euroa enemmän kuin tuilla.</p>
</div>
<p>Loukku syntyy järjestelmien rajapinnoilla. Asumistuki, työttömyysturva, toimeentulotuki, päivähoitomaksut ja verot ovat kukin erikseen järkeviä, ja jokaisella on oma lakinsa. Kokonaisuutta, jonka tuensaaja kohtaa, ei ole suunnitellut kukaan.</p>
<div class="infolaatikko">
<h2 class="laatikko-otsikko">Dokumentoituja tapauksia:</h2>
<ul style="margin:0.5em 0 0;">
<li><strong>Työttömyysloukku (Suomi, 2021):</strong> ETLA:n laskelman mukaan loukussa oli 136 500 ihmistä, kun rajana on se, että työllistyessä käteen jää enintään 20 prosenttia palkasta. 25 prosentin rajalla heitä oli yli 300 000. Työllistymisveroasteen mediaani oli noin 69 prosenttia, ja yli puolella miljoonalla suomalaisella lisäansioista jäi käteen alle puolet.</li>
<li><strong>Suojaosan poisto (Suomi, 2024):</strong> Työttömyysetuuden ja asumistuen 300 euron suojaosa salli ansaita 300 euroa kuukaudessa ilman, että tuki pieneni. Se poistettiin 1.4.2024. Kelan seurannassa työnteon lopettaneita oli loppuvuonna 2024 noin 800–1 000 enemmän neljännestä kohden kuin aiempina vuosina. Kela korostaa, että muutos on ajallinen eikä todistettu syy-yhteys.</li>
<li><strong>Perustulokokeilu (Suomi, 2017–2018):</strong> 2 000 työtöntä sai 560 euroa kuukaudessa ilman, että työtulot pienensivät sitä. Ensimmäisenä vuonna työllisyys ei muuttunut. Toisena vuonna perustulon saajat tekivät keskimäärin 78 työpäivää, kuusi enemmän kuin vertailuryhmä. Loukun poistaminen ei siis yksin tuottanut suurta työllisyysloikkaa.</li>
</ul>
</div>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Testikysymys kuuluu: paljonko sadan euron lisätulosta jää käteen ihmiselle, joka saa yhtä aikaa kolmea tukea? Laske kaikkien sääntöjen yhteisvaikutus, älä yhden säännön. Vastakeinoja ovat suojaosat, loivemmat leikkautumisprosentit ja tukien yhdistäminen, mutta jokaisella on hintansa: loiva leikkautuminen ulottaa tuen suurempiin tuloihin ja maksaa enemmän. Se on valinta, ei laskuvirhe. Jos itse harkitset työtä tuilta, laske tilanne Kelan laskureilla ennen päätöstä. Muista myös, että palkkatyö kerryttää eläkettä ja työssäoloehtoa, joita laskuri ei näytä.
    </div>
""" + lue_lisaa(
        [("Kannustinloukut Suomessa", "Puonti, Kauppi, Kotamäki &amp; Ropponen, ETLA Raportti 124 (2022)")],
        [("https://www.etla.fi/wp-content/uploads/ETLA-Raportit-Reports-124.pdf",
          "ETLA: Kannustinloukut Suomessa (2022)"),
         ("https://www.kela.fi/ajankohtaista/tyottomien-osa-aikatulot-pienenivat-suojaosan-poistamisen-jalkeen",
          "Kela: Työttömien osa-aikatulot pienenivät suojaosan poistamisen jälkeen (2025)"),
         ("https://stm.fi/-/perustulokokeilun-tulokset-tyollisyysvaikutukset-vahaisia-toimeentulo-ja-psyykkinen-terveys-koettiin-paremmaksi",
          "STM ja Kela: Perustulokokeilun tulokset (2020)")]),
     ["kynnysefekti", "kobravaikutus", "moraalikato", "catch-22", "kafka-ilmio"])


# ────────────────────────── 168 · Kynnysefekti ──────────────────────────
page("kynnysefekti",
     "Kynnysefekti — kun raja ohjaa enemmän kuin sääntö",
     "Kynnysefekti — miksi kaikki asettuvat juuri rajan alle? | Ilmiöitä",
     "Kynnysefekti: kun sääntö muuttuu jyrkästi tietyssä rajassa, toiminta kasautuu juuri rajan alle. Esimerkit ALV-rajasta ja korkokatosta sekä keinot välttää ilmiö.",
     r"""
<p><strong>Kynnysefekti</strong> syntyy, kun sääntö muuttuu jyrkästi tietyn rajan kohdalla: vero alkaa, tuki loppuu tai uusi velvoite astuu voimaan. Ihmiset ja yritykset asettuvat juuri rajan alle tai siirtyvät reilusti sen yli. Taloustieteessä jyrkkää rajaa kutsutaan englanniksi nimellä <em>notch</em> ja siihen kasautumista nimellä <em>bunching</em>.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Miksi raja vääristää käytöstä?</h2>
<p style="margin:0.4em 0 0;">Liukuva sääntö, kuten progressiivinen vero, muuttaa kannustimia vähän kerrallaan. Kynnys muuttaa ne kerralla. Jos yksi lisäeuro myyntiä tuo mukanaan arvonlisäveron ilmoitusvelvollisuuden, rajan ylittäminen maksaa enemmän kuin tuottaa. Silloin raja alkaa ohjata päätöksiä enemmän kuin itse sääntö.</p>
</div>
<div class="infolaatikko">
<h2 class="laatikko-otsikko">Dokumentoituja tapauksia:</h2>
<ul style="margin:0.5em 0 0;">
<li><strong>ALV-raja (Suomi):</strong> Harju, Matikka ja Rauhanen kävivät läpi kaikkien suomalaisyritysten verotiedot. Yrityksiä kasautui selvästi juuri arvonlisäverorajan alapuolelle. Syy ei ollut veroprosentti vaan ilmoittamisen vaiva. Merkkejä verojen kiertämisestä ei löytynyt, joten yritykset näyttivät aidosti myyvän vähemmän. Kasautuminen oli pysyvää, eli raja hidasti pienyritysten kasvua. Raja on vuoden 2025 alusta 20 000 euroa vuodessa.</li>
<li><strong>Pikavippien korkokatto (Suomi, 2013):</strong> Katto koski vain alle 2 000 euron lainoja, joten lainanantajat siirtyivät rajan yli. Uuden pienlainan keskikoko oli ollut 254 euroa. Katon jälkeen tilalle tulivat vähintään 2 000 euron luottolimiitit (ks. <a href="kobravaikutus.html">kobravaikutus</a>).</li>
<li><strong>Ranskan 50 työntekijän raja:</strong> 50 työntekijän yritystä koskee Ranskassa joukko uusia työoikeudellisia velvoitteita. Garicano, Lelarge ja Van Reenen (2016) havaitsivat, että yrityksiä kasautuu juuri 49 työntekijän kohdalle.</li>
</ul>
</div>
<p>Kynnys on myös mittari. Kasautuminen rajan alle näkyy suoraan jakaumasta, ja sen koko kertoo, kuinka paljon raja maksaa. Siksi juuri kynnyksiä tutkimalla on saatu tarkimpia arvioita siitä, miten verot ja säännöt muuttavat käytöstä.</p>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Testikysymys kuuluu: mitä tapahtuu sille, joka ylittää rajan yhdellä eurolla? Jos hän menettää enemmän kuin saa, raja on kynnys. Vastakeinot: korvaa porras liukumalla eli velvoitteella, joka alkaa asteittain, tai tuella, joka pienenee vähitellen; jos raja on pakko vetää, katso jakaumaa ja seuraa, kasautuuko toiminta sen alle; ja kun sääntö koskee summaa, kysy, voiko toiminnan pilkkoa tai niputtaa niin, että raja kiertyy. Arvonlisäveron alarajahuojennus oli tällainen liukuma, ja se poistettiin vuoden 2025 alussa.
    </div>
""" + lue_lisaa(
        [("Compliance costs vs. tax incentives: Why do entrepreneurs respond to size-based regulations?",
          "Harju, Matikka &amp; Rauhanen, <em>Journal of Public Economics</em> (2019)"),
         ("Firm Size Distortions and the Productivity Distribution: Evidence from France",
          "Garicano, Lelarge &amp; Van Reenen, <em>American Economic Review</em> (2016)")],
        [("https://doria.fi/handle/10024/148733",
          "Harju, Matikka &amp; Rauhanen: The effects of size-based regulation on small firms (VATT, 2016, englanniksi)"),
         ("https://www.vero.fi/syventavat-vero-ohjeet/ohje-hakusivu/48658/arvonlisaveroton-vahainen-toiminta/",
          "Verohallinto: Arvonlisäveroton vähäinen toiminta")]),
     ["kannustinloukku", "kobravaikutus", "goodhartin-laki", "moraalikato", "chestertonin-aita"])


# ────────────────────────── 169 · Moraalikato ──────────────────────────
page("moraalikato",
     "Moraalikato — kun joku muu maksaa riskin",
     "Moraalikato (moral hazard) — mitä se tarkoittaa? | Ilmiöitä",
     "Moraalikato: kun joku muu kantaa tappiot, riskiä otetaan enemmän. Suomen 1990-luvun pankkikriisi on oppikirjaesimerkki. Näin moral hazard tunnistetaan.",
     r"""
<p><strong>Moraalikato</strong> (engl. <em>moral hazard</em>) tarkoittaa, että ihminen tai organisaatio ottaa enemmän riskiä, kun joku muu kantaa tappiot. Nimi on harhaanjohtava, koska kyse ei ole huonosta moraalista vaan kannustimesta. Vakuutettu auto pysäköidään huolettomammin, ja pankki, joka luottaa valtion pelastavan sen, lainaa rohkeammin.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Miten moraalikato syntyy?</h2>
<p style="margin:0.4em 0 0;">Moraalikato syntyy, kun riskin ottaja ja riskin maksaja ovat eri tahoja eikä maksaja näe, mitä ottaja tekee. Vakuutus, takaus ja pelastuslupaus ovat hyödyllisiä, mutta jokainen niistä siirtää osan seurauksista pois päättäjältä. Siksi niihin liitetään omavastuu, valvonta tai ehtoja.</p>
</div>
<div class="infolaatikko">
<h2 class="laatikko-otsikko">Dokumentoituja tapauksia:</h2>
<ul style="margin:0.5em 0 0;">
<li><strong>Säästöpankit ja pankkikriisi (Suomi, 1990-luku):</strong> Kun rahoitusmarkkinat vapautettiin 1980-luvulla, luotonantoaan kasvattivat aggressiivisimmin SKOP ja suuret säästöpankit. Kriisissä ne joutuivat suurimpiin vaikeuksiin, ja käytännössä koko pysyvä pankkituki meni säästöpankkiryhmälle. Tukeen kului lopulta summa, joka vastasi noin kymmentä prosenttia lamanaikaisesta kokonaistuotannosta (Kiander, VATT 2001). Vihriälän (1997) mukaan vääristyneet kannustimet selittävät kokonaan sen, että säästöpankkien luotonanto kasvoi 1980-luvun lopulla muita pankkeja nopeammin.</li>
<li><strong>Hyvinvointialueiden lisärahoitus (Suomi, 2023–):</strong> Hyvinvointialue ei voi mennä konkurssiin, ja rahoituslain 11 §:n mukaan valtio voi myöntää lisärahoitusta, jos rahat eivät riitä välttämättömiin palveluihin. Alue, joka tietää valtion tulevan apuun, voi lykätä kipeitä säästöjä. Laki varautuu tähän: vuoden 2024 muutoksen jälkeen jo yksi lisärahoituspäätös voi käynnistää arviointimenettelyn, jossa valtio puuttuu alueen talouteen. Syyskuussa 2024 ministeriöt hylkäsivät Vantaan ja Keravan hyvinvointialueen 74 miljoonan euron hakemukset sekä vuodelle 2024 että 2025.</li>
<li><strong>IT-projekti, joka luovutetaan ylläpidolle:</strong> Ohjelmistoprojektissa moraalikato syntyy, kun koodin kirjoittaja ei joudu ylläpitämään sitä. Projekti päättyy, tiimi siirtyy eteenpäin, ja oikotiet eli <a href="tekninen-velka.html">tekninen velka</a> jäävät ylläpidon maksettaviksi. Amazonin teknologiajohtaja Werner Vogels kuvasi vuonna 2006 ACM Queue -lehden haastattelussa yhtiön vastalääkkeen: <em>you build it, you run it</em>. Kehittäjätiimi vastaa palvelustaan myös tuotannossa, yöllisiä vikahälytyksiä myöten. Se on omavastuuta ohjelmistokehityksessä.</li>
</ul>
</div>
<p>Samassa kriisissä näkyi myös, miten moraalikatoa voi rajata. Muut pankit saivat valtiolta pääomatukea lainana ja maksoivat sen kriisin jälkeen takaisin, joten niistä ei jäänyt valtiolle pysyviä kustannuksia. Tuki, joka on maksettava takaisin, ei houkuttele riskiin samalla tavalla kuin tuki, jota ei tarvitse maksaa.</p>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Testikysymys kuuluu: kuka maksaa, jos tämä menee pieleen, ja onko hän sama, joka päättää? Jos ei ole, kysy, mikä estää päättäjää ottamasta liikaa riskiä. Vastakeinot ovat vanhoja ja toimivia: omavastuu, jolloin päättäjä maksaa osan itse; valvonta ja ehdot, jolloin riskin kantaja näkee, mitä tapahtuu; ja tuki lainana eikä lahjana. Kun pelastus on väistämätön, kohdista se niin, että se suojaa tallettajia ja asiakkaita mutta ei osakkeenomistajia eikä johtoa. Muuten seuraava johto oppii, että riski kannattaa.
    </div>
""" + lue_lisaa(
        [("Suomen 1990-luvun kriisin syyt ja seuraukset", "Jaakko Kiander, VATT-julkaisuja 27:5 (2001)")],
        [("https://www.doria.fi/handle/10024/148629",
          "Kiander: Suomen 1990-luvun kriisin syyt ja seuraukset (VATT, 2001)"),
         ("https://vm.fi/arviointimenettely", "Valtiovarainministeriö: Hyvinvointialueen arviointimenettely"),
         ("https://www.sttinfo.fi/tiedote/70525063/ministeriot-vantaan-ja-keravan-hyvinvointialueelle-ei-myonneta-lisarahoitusta?lang=fi",
          "STT Info: Vantaan ja Keravan hyvinvointialueelle ei myönnetä lisärahoitusta (20.9.2024)"),
         ("https://aws.amazon.com/blogs/aws/acm_queue_inter",
          "AWS-blogi: Werner Vogelsin ACM Queue -haastattelu (2006, englanniksi)"),
         ("https://en.wikipedia.org/wiki/Moral_hazard", "Wikipedia: Moral hazard (englanniksi)")]),
     ["riskikompensaatio", "yhteismaan-tragedia", "kobravaikutus", "saantelijan-kaappaus", "kannustinloukku"])


# ────────────────────────── 170 · Riskikompensaatio ──────────────────────────
page("riskikompensaatio",
     "Riskikompensaatio — turvallisuus, joka syö itseään",
     "Riskikompensaatio — miksi turvavarusteet lisäävät riskinottoa? | Ilmiöitä",
     "Riskikompensaatio: kun olo tuntuu turvallisemmalta, riskiä otetaan enemmän. Esimerkit ABS-takseista, Ruotsin H-päivästä ja suomalaisesta rengaskokeesta.",
     r"""
<p><strong>Riskikompensaatio</strong> (engl. <em>risk compensation</em>, myös <em>Peltzman effect</em>) tarkoittaa, että ihminen sopeuttaa käytöksensä siihen, miten vaaralliselta tilanne tuntuu. Kun turvallisuus paranee, ajetaan lujempaa tai tarkkaillaan vähemmän, ja osa hyödystä katoaa. Taloustieteilijä Sam Peltzman väitti vuonna 1975, että autojen turvavarusteiden hyöty kului kokonaan kovempaan ajoon. Hänen aineistostaan löytyi myöhemmin virheitä, mutta itse ilmiö on todettu monesti.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Kumoaako riskikompensaatio turvatoimet?</h2>
<p style="margin:0.4em 0 0;">Yleensä ei. Kompensaatio on tavallisesti osittaista: turvavyö, kypärä ja lukkiutumattomat jarrut pelastavat yhä henkiä, vaikka osa hyödystä kuluu muuttuneeseen käytökseen. Ilmiö toimii myös toiseen suuntaan. Kun tilanne tuntuu vaarallisemmalta, ihmiset varovat enemmän.</p>
</div>
<div class="infolaatikko">
<h2 class="laatikko-otsikko">Dokumentoituja tapauksia:</h2>
<ul style="margin:0.5em 0 0;">
<li><strong>Münchenin taksit (1981–1983):</strong> Osa taksiyhtiön autoista oli varustettu ABS-jarruilla, osa ei. Kolmen vuoden seurannassa ABS-takseilla oli hieman enemmän kolareita kuin muilla. Tutkijat selittivät eron tarkkaavaisuuden herpaantumisella ja sillä, että kuljettajat yliarvioivat jarrujen tuoman turvan.</li>
<li><strong>Ruotsin H-päivä (1967):</strong> Ruotsi siirtyi yhdessä yössä vasemmanpuoleisesta oikeanpuoleiseen liikenteeseen. Liikennekuolemat vähenivät selvästi noin puolentoista vuoden ajan, kun kaikki ajoivat varoen. Sen jälkeen luvut palasivat entiselle tasolle.</li>
<li><strong>Kitkarenkaat (Suomi, 1994):</strong> VTT:n kokeessa nastarenkaista kitkarenkaisiin siirtyneet kuljettajat ajoivat ensimmäisenä talvena hyvillä keleillä hieman lujempaa, mutta jyrkät kaarteet varovaisemmin ja jarruttivat liukkaalla pehmeämmin. Toisena talvena he pitivät jonossa 11 metriä pidemmän välin edellä ajavaan. Heikompi pito teki kuljettajasta varovaisemman.</li>
</ul>
</div>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Testikysymys kuuluu: muuttaako tämä turvatoimi sitä, miten turvalliseksi ihmiset tilanteen kokevat? Jos muuttaa, arvioi hyöty todellisesta käytöksestä eikä testiradalta. ABS lyhentää jarrutusmatkaa kokeessa, mutta liikenteessä hyöty riippuu siitä, mihin kuljettaja käyttää saamansa lisävaran. Vastakeinot: yhdistä tekninen turva käytöksen rajaan, kuten nopeusrajoitukseen ja valvontaan; älä markkinoi turvatoimea riskin poistajana; ja seuraa lopputulosta, kuten onnettomuuksia ja vammoja, älä pelkkää käyttöastetta. Omassa elämässä: kun hankit turvavarusteen, kysy, aiotko nyt tehdä jotain, mitä et ilman sitä tekisi.
    </div>
""" + lue_lisaa(
        [("Improved safety through improved technical measures?", "Aschenbrenner &amp; Biehl (1994)"),
         ("The Effects of Automobile Safety Regulation", "Sam Peltzman, <em>Journal of Political Economy</em> (1975)")],
        [("https://en.wikipedia.org/wiki/Risk_compensation", "Wikipedia: Risk compensation (englanniksi)"),
         ("https://asiakas.kotisivukone.com/files/nastatutkimus.kotisivukone.com/tiedostot/tutkimusraportit/lvm_nastarenkaiden_vahentamisen_lituvaik.malmivuo_2012.pdf",
          "Malmivuo: Nastarenkaiden vähentämisen liikenneturvallisuusvaikutukset (LVM, 2012)")]),
     ["moraalikato", "jevonsin-paradoksi", "kobravaikutus", "backfire-effect", "dunning-kruger"])


# ────────────────────────── 171 · Jevonsin paradoksi ──────────────────────────
page("jevonsin-paradoksi",
     "Jevonsin paradoksi — tehokkuus, joka lisää kulutusta",
     "Jevonsin paradoksi ja rebound — miksi säästö ei aina säästä? | Ilmiöitä",
     "Jevonsin paradoksi: kun resurssin käyttö tehostuu, sitä voidaan kuluttaa enemmän eikä vähemmän. Kivihiilestä lämpöpumppuihin: rebound-ilmiö ja miten se huomioidaan.",
     r"""
<p><strong>Jevonsin paradoksi</strong> (engl. <em>Jevons paradox</em>) tarkoittaa, että resurssin käytön tehostuminen voi lisätä sen kokonaiskulutusta. Brittiläinen taloustieteilijä William Stanley Jevons huomasi vuonna 1865 kirjassaan <cite>The Coal Question</cite>, että höyrykoneiden parantuminen ei vähentänyt Britannian hiilenkulutusta vaan kasvatti sitä. Kun hiili tuotti enemmän työtä, sitä kannatti käyttää yhä useampaan tarkoitukseen.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Mikä ero on rebound-ilmiöllä ja Jevonsin paradoksilla?</h2>
<p style="margin:0.4em 0 0;"><strong>Rebound-ilmiö</strong> (engl. <em>rebound effect</em>) tarkoittaa, että osa tehostamisen tuomasta säästöstä kuluu lisäkäyttöön. Jevonsin paradoksi on sen ääripää: lisäkäyttö syö koko säästön ja enemmänkin. Useimmiten rebound on osittainen. Säästö jää laskettua pienemmäksi, mutta se ei katoa kokonaan.</p>
</div>
<div class="infolaatikko">
<h2 class="laatikko-otsikko">Dokumentoitu tapaus:</h2>
<ul style="margin:0.5em 0 0;">
<li><strong>Lämpöpumput (Norja, 2013–2016):</strong> Lämpöpumppu voi pienentää sähkölämmitteisen talon sähkönkulutusta jopa neljänneksellä. Norjan tilastokeskuksen tutkijat havaitsivat kuitenkin, että talot, joissa oli lämpöpumppu, käyttivät sähköä keskimäärin yhtä paljon kuin muut. Kodeissa pidettiin lämpimämpää, lämmitettiin useampia huoneita ja luovuttiin yö- ja poissaololämpötilojen laskemisesta. Kokonaisenergiankulutus silti laski, koska puuta ja öljyä poltettiin vähemmän. Rebound söi sähkösäästön, mutta ei koko hyötyä.</li>
</ul>
</div>
<p>Paradoksi ei tarkoita, että tehokkuus olisi turhaa. Se tarkoittaa, että tehokkuus ei yksin takaa kulutuksen laskua. Jos tavoitteena on vähentää kokonaiskulutusta, tehokkuuden rinnalle tarvitaan jotain, mikä rajaa käytön määrää: hinta, kiintiö tai katto.</p>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Testikysymys kuuluu: tuleeko tämän asian käyttäminen tehostamisen jälkeen halvemmaksi? Jos tulee, oleta, että sitä käytetään enemmän, ja laske säästö vasta sen jälkeen. Vastakeinot: arvioi säästö toteutuneesta kulutuksesta, ei laitteen hyötysuhteesta; yhdistä tehokkuus kokonaismäärän rajaan, kuten päästökaupan kattoon, joka pitää kokonaismäärän kurissa, vaikka yksittäinen käyttö halpenee; ja omassa taloudessa päätä etukäteen, mihin säästetty raha menee, ettei se kulu samaan asiaan isompana.
    </div>
""" + lue_lisaa(
        [("The Coal Question", "William Stanley Jevons (1865)"),
         ("Revisiting household energy rebound: Perspectives from a multidisciplinary study",
          "Halvorsen, Larsen, Wilhite &amp; Winther, <em>Indoor and Built Environment</em> (2016)")],
        [("https://www.ssb.no/forskning/discussion-papers/how-do-investments-in-heat-pumps-affect-household-energy-consumption",
          "Statistics Norway: How do investments in heat pumps affect household energy consumption? (englanniksi)"),
         ("https://en.wikipedia.org/wiki/Jevons_paradox", "Wikipedia: Jevons paradox (englanniksi)")]),
     ["riskikompensaatio", "yhteismaan-tragedia", "kobravaikutus", "viherpesu", "goodhartin-laki"])


# ────────────────────────── 172 · Yhteismaan tragedia ──────────────────────────
page("yhteismaan-tragedia",
     "Yhteismaan tragedia — kun kaikkien on ei-kenenkään",
     "Yhteismaan tragedia — miksi yhteinen resurssi kuluu loppuun? | Ilmiöitä",
     "Yhteismaan tragedia: kun yhteistä resurssia käyttävät monet, jokaisen kannattaa ottaa vähän lisää. Suomen kuntaliitokset esimerkkinä ja keinot, jotka toimivat.",
     r"""
<p><strong>Yhteismaan tragedia</strong> (engl. <em>tragedy of the commons</em>) kuvaa tilannetta, jossa yhteistä resurssia käyttävät monet ja jokaisen kannattaa ottaa siitä hieman lisää. Hyöty tulee kokonaan ottajalle, mutta haitta jakautuu kaikille. Biologi Garrett Hardin teki ajatuksen tunnetuksi vuonna 1968 esimerkillä yhteislaitumesta, jolle jokainen paimen tuo vielä yhden lehmän, kunnes laidun on syöty paljaaksi.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Onko yhteismaan tragedia väistämätön?</h2>
<p style="margin:0.4em 0 0;">Ei ole. Elinor Ostrom sai vuonna 2009 taloustieteen Nobelin osoitettuaan, että yhteisöt ovat hoitaneet yhteisiä kalavesiä, laitumia ja kastelujärjestelmiä onnistuneesti vuosisatojen ajan. Ne onnistuvat, kun käyttäjät tuntevat toisensa, tekevät säännöt itse ja valvovat niitä. Tragedia syntyy, kun nämä puuttuvat: käyttäjiä on paljon, he eivät tunne toisiaan, eikä ottamista näe.</p>
</div>
<div class="infolaatikko">
<h2 class="laatikko-otsikko">Dokumentoituja tapauksia:</h2>
<ul style="margin:0.5em 0 0;">
<li><strong>Kuntaliitokset (Suomi, 2000-luku):</strong> Liitospäätöksen ja varsinaisen liitoksen välillä kunta päätti vielä itse rahoistaan, mutta sen velat siirtyivät yhteisen kunnan maksettaviksi. Saarimaa ja Tukiainen (2015) havaitsivat, että mitä pienempi osa laskusta jäi kunnan omille asukkaille, sitä enemmän kunta lisäsi velkaa asukasta kohden ja käytti kassavarojaan ennen liitosta. Rahat menivät pääosin investointeihin ja käyttömenoihin.</li>
<li><strong>Osakaskunnat (Suomi):</strong> Suomen jakamattomia vesialueita hallinnoivat osakaskunnat yhteisaluelain nojalla. Muuhun kuin onkimiseen, pilkkimiseen ja viehekalastukseen tarvitaan osakaskunnan lupa. Rakenne on juuri sitä, mitä Ostrom kuvasi: omistajat tunnetaan, säännöt tehdään paikallisesti ja luvista päättää yhteisö.</li>
</ul>
</div>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Testikysymys kuuluu: hyötyykö yksittäinen käyttäjä ottaessaan lisää, vaikka kaikki yhteensä häviävät? Jos hyötyy, tarvitaan sääntö, koska pelkkä vetoaminen ei kestä. Ostromin havaintojen mukaan toimivissa yhteisöissä on rajattu, ketkä resurssia käyttävät, käyttäjät tekevät säännöt ja valvovat niitä itse, ottaminen näkyy, ja seuraukset on porrastettu niin, että ensimmäinen rike maksaa vähän ja toistuva paljon. Kuntaliitosten kaltaisessa siirtymävaiheessa auttaisi, jos suuret talouspäätökset vaatisivat jo ennen liitosta tulevien kumppaneiden hyväksynnän.
    </div>
""" + lue_lisaa(
        [("The Tragedy of the Commons", "Garrett Hardin, <em>Science</em> (1968)"),
         ("Governing the Commons", "Elinor Ostrom (1990)")],
        [("https://urn.fi/URN:ISBN:978-952-274-104-2",
          "Saarimaa &amp; Tukiainen: Common Pool Problems in Voluntary Municipal Mergers (VATT, englanniksi)"),
         ("https://en.wikipedia.org/wiki/Tragedy_of_the_commons", "Wikipedia: Tragedy of the commons (englanniksi)")]),
     ["moraalikato", "sivustakatsojan-efekti", "jevonsin-paradoksi", "kobravaikutus", "kannustinloukku"])


# ────────────────────────── 173 · Kiellon rautainen laki ──────────────────────────
page("kiellon-rautainen-laki",
     "Kiellon rautainen laki — kielletty päihde väkevöityy",
     "Kiellon rautainen laki — miksi kielto tekee päihteistä vahvempia? | Ilmiöitä",
     "Kiellon rautainen laki: kun päihde kielletään, markkinoille jää sen väkevin muoto. Suomen kieltolaki 1919–1932 ja muuntohuumeet esimerkkeinä.",
     r"""
<p><strong>Kiellon rautainen laki</strong> (engl. <em>iron law of prohibition</em>) tarkoittaa, että kun päihde kielletään, sen kauppa siirtyy yhä väkevämpiin muotoihin. Salakuljettaja ottaa saman riskin jokaisesta kuljetetusta litrasta, joten kannattaa kuljettaa mahdollisimman paljon vaikutusta mahdollisimman pienessä tilassa. Yhdysvaltalainen kirjoittaja Richard Cowan esitti periaatteen vuonna 1986.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Miksi kielto väkevöittää päihteen?</h2>
<p style="margin:0.4em 0 0;">Laillisilla markkinoilla myydään paljon miedompia juomia, koska niiden kuljettaminen ja varastointi on halpaa. Kun kaikki kuljettaminen on rikos, riski ja kustannus riippuvat tilavuudesta, eivät vahvuudesta. Siksi kieltolain Suomeen ei salakuljetettu olutta vaan pirtua, 96-prosenttista spriitä.</p>
</div>
<div class="infolaatikko">
<h2 class="laatikko-otsikko">Dokumentoituja tapauksia:</h2>
<ul style="margin:0.5em 0 0;">
<li><strong>Kieltolaki (Suomi, 1919–1932):</strong> Takavarikoidun alkoholin määrä kasvoi vuosi vuodelta ja ylitti miljoona litraa vuonna 1930. Vuodesta 1922 lähtien kieltolaki- ja juopumusrikokset olivat yli 80 prosenttia kaikista poliisin tietoon tulleista rikoksista. Vuonna 1929 surmattiin 375 ihmistä, ja pirtu oli mukana suurimmassa osassa henkirikoksista. Kun laki kumottiin kansanäänestyksen jälkeen keväällä 1932, henkirikokset puolittuivat nopeasti.</li>
<li><strong>Muuntohuumeet (Suomi, 2014–):</strong> Vuodesta 2014 Suomi on voinut kieltää uusia psykoaktiivisia aineita kuluttajamarkkinoilta asetuksella. Kiellettyjen tilalle tulee kemiallisesti hieman muunneltuja aineita, joten listaa täydennetään jatkuvasti. Vuonna 2022 siihen lisättiin 22 ainetta. Alkuvuonna 2025 viranomaiset tunnistivat neljä vaarallista uutta ainetta, joista kolme ei ollut lainkaan valvonnassa.</li>
</ul>
</div>
<p>Laki ei väitä, että jokainen kielto epäonnistuu. Kieltolaki vähensi alussa alkoholin kulutusta. Laki väittää, että kielto muuttaa myös sitä, mitä markkinoilla myydään, ja muutos on yleensä vaarallisempaan suuntaan.</p>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Testikysymys kuuluu: jos kielto toimii vain osittain, mitä jäljelle jäävillä markkinoilla myydään? Jos vastaus on vahvempaa, pienempää ja vaikeammin annosteltavaa, kielto voi lisätä haittoja, vaikka käyttäjiä olisi vähemmän. Vastakeinot: arvioi kieltoa haitoilla eikä takavarikoilla; seuraa markkinoilla liikkuvien aineiden vahvuutta, ei vain määrää; ja jos kiellosta luovutaan, päätä, mikä tulee tilalle. Suomi korvasi kieltolain valtion alkoholiyhtiöllä, joka avasi 48 myymälää 5.4.1932.
    </div>
""" + lue_lisaa(
        [("Väkivallan hyökyaalto", "Martti Lehti")],
        [("https://historia.hel.fi/fi/ilmiot/vallankayttoa-ja-hallintoa/kieltolaki-kalliiksi-tullut-kokeilu",
          "Helsingin historia: Kieltolaki, kalliiksi tullut kokeilu"),
         ("https://yle.fi/a/3-12368945",
          "Yle: Kieltolaki näkyi tilastossa murhien hyökyaaltona (2022)"),
         ("https://fi.wikipedia.org/wiki/Kieltolaki_(Suomi)", "Wikipedia: Kieltolaki (Suomi)"),
         ("https://en.wikipedia.org/wiki/Iron_law_of_prohibition", "Wikipedia: Iron law of prohibition (englanniksi)")]),
     ["kobravaikutus", "chestertonin-aita", "streisand-ilmio", "backfire-effect", "riskikompensaatio"])


# ────────────────────────── 174 · Chestertonin aita ──────────────────────────
page("chestertonin-aita",
     "Chestertonin aita — selvitä ensin, miksi aita on siinä",
     "Chestertonin aita — älä pura sääntöä, jonka syytä et tiedä | Ilmiöitä",
     "Chestertonin aita: ennen kuin purat säännön, selvitä miksi se on olemassa. Suomen taksiuudistus 2018 ja vuoden 2021 korjaukset esimerkkinä.",
     r"""
<p><strong>Chestertonin aita</strong> (engl. <em>Chesterton's fence</em>) on periaate, jonka mukaan sääntöä tai rakennetta ei pidä purkaa ennen kuin tietää, miksi se on olemassa. Englantilainen kirjailija G. K. Chesterton kuvasi vuonna 1929 uudistajan, joka löytää tieltä aidan eikä keksi sille syytä. Viisaampi uudistaja vastaa: jos et tiedä, miksi aita on siinä, en anna sinun purkaa sitä. Ota ensin selvää, ja kun tiedät, voimme puhua purkamisesta.</p>
<div class="infolaatikko vastauslohko">
<h2 class="laatikko-otsikko">Tarkoittaako Chestertonin aita, ettei mitään saa muuttaa?</h2>
<p style="margin:0.4em 0 0;">Ei tarkoita. Periaate ei puolusta aitaa vaan vaatii selvityksen. Moni vanha sääntö on turha, ja selvitys voi paljastaa juuri sen. Vaikeus on siinä, että toimiva sääntö näyttää usein turhalta: ongelmaa, jonka se estää, ei enää näe.</p>
</div>
<div class="infolaatikko">
<h2 class="laatikko-otsikko">Dokumentoitu tapaus:</h2>
<ul style="margin:0.5em 0 0;">
<li><strong>Taksiuudistus (Suomi, 2018):</strong> Heinäkuussa 2018 voimaan tullut liikennepalvelulaki purki taksilupien kuntakohtaiset kiintiöt, enimmäishinnat sekä asemapaikka- ja päivystysvelvoitteen. Kilpailu- ja kuluttajaviraston mukaan suurissa kunnissa taksin sai usein halvemmalla kuin ennen. Keskimäärin hinnat kuitenkin nousivat suurissa kunnissa noin 7 ja muualla noin 15 prosenttia. Saatavuus heikkeni pienillä paikkakunnilla kaukana asutuskeskuksista, ja rautatieasemilla ja satamissa asiakkaan oli vaikea tietää, mitä kyyti maksaa. Vuoden 2021 korjaussarja palautti osan aidoista: taksamittarin, kun hinta ei ole kiinteä, pakollisen taksivalaisimen ja tarkemman kuljettajakokeen.</li>
</ul>
</div>
<p>Esimerkki ei osoita, että uudistus olisi ollut virhe. Se osoittaa, että osa aidoista teki työtä, jota kukaan ei ollut kirjannut näkyviin. Enimmäishinta suojasi asiakasta, joka ei voi vertailla hintoja taksitolpalla, ja päivystysvelvoite piti taksin paikkakunnalla myös hiljaisina iltoina.</p>
<div class="huomiolaatikko">
<h2 class="laatikko-otsikko">Tunnistaminen ja vastakeinot:</h2> Testikysymys kuuluu: mitä ongelmaa tämän säännön alun perin piti estää, ja onko ongelma poissa vai vain piilossa? Vastakeinot: etsi säännön alkuperäinen perustelu, kuten hallituksen esitys, pöytäkirja tai ihminen, joka oli mukana sitä tekemässä; kysy niiltä, jotka elävät säännön kanssa, mitä tapahtuisi ilman sitä; pura kokeillen ja niin, että purkamisen voi perua, esimerkiksi alueittain tai määräajaksi; ja sovi etukäteen mittarit, joista näkee, palaako aidan estämä ongelma. Sama pätee työpaikalla: outo prosessivaihe on usein jäänne virheestä, jota kukaan ei halua toistaa.
    </div>
""" + lue_lisaa(
        [("The Thing", "G. K. Chesterton (1929)")],
        [("https://kkv.fi/uploads/sites/2/2022-03-policybrief-taksiuudistus.pdf",
          "KKV: Vuoden 2018 taksiuudistus (Policy Brief 3/2022)"),
         ("https://valtioneuvosto.fi/-/taksilainsaadannon-muutokset-voimaan-paaosin-1.-toukokuuta",
          "Valtioneuvosto: Taksilainsäädännön muutokset voimaan (2021)"),
         ("https://en.wikipedia.org/wiki/G._K._Chesterton#Chesterton's_fence",
          "Wikipedia: Chesterton's fence (englanniksi)")]),
     ["kiellon-rautainen-laki", "kynnysefekti", "kobravaikutus", "saantelijan-kaappaus", "tekninen-velka"])


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


def ankkuroi(sisalto):
    """h2-ankkurit valmiiksi samalla säännöllä kuin seo_rakenne.py."""
    def lisaa_id(m):
        attrs, teksti = m.group(1), m.group(2)
        if "id=" in attrs:
            return m.group(0)
        return f'<h2{attrs} id="{tunniste(teksti)}">{teksti}</h2>'
    return re.sub(r"<h2((?:\s[^>]*)?)>(.*?)</h2>", lisaa_id, sisalto, flags=re.S)


def kirjoita_hub_lohko():
    """index.html:n hub-lohko valmiiksi — liitetään käsin vasta julkaisussa,
    trollaus-lohkon perään. build_kategoriat.py --luonnos lukee tämän."""
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
    tiedosto = OUT / "kannustin-hub-lohko.html"
    tiedosto.write_text("<!-- Liitä index.html:ään trollaus-lohkon perään vasta julkaisussa. "
                        "Generoi scripts/build_kannustin_luonnokset.py -->\n" + lohko,
                        encoding="utf-8")
    print(f"  hub-lohko → {tiedosto.relative_to(ROOT)}")


def build():
    tpl = TEMPLATE.read_text(encoding="utf-8")
    OUT.mkdir(exist_ok=True)

    ids_match = re.search(r"const IDS = \[(.*?)\];", tpl, re.S)
    julkaistut = [s.strip().strip('"') for s in ids_match.group(1).split(",")]
    assert EDELLISET_IDS == julkaistut, f"index.html:n korttijärjestys ≠ {TEMPLATE.name}:n IDS"
    ids_js = ("const IDS = ["
              + ", ".join(json.dumps(s) for s in EDELLISET_IDS + [p["slug"] for p in PAGES])
              + "];")
    ld_match = re.search(r'<script type="application/ld\+json">\n(.*?)\n</script>', tpl, re.S)
    pohja_ld = ld_match.group(1)

    for i, p in enumerate(PAGES):
        slug, num = p["slug"], p["num"]
        termi = OMAT_KORTIT[slug][2]

        if i == 0:
            prev_href, prev_nimi = f"../{EDELTAJA[0]}.html", EDELTAJA[1]
        else:
            prev_href, prev_nimi = f"{PAGES[i-1]['slug']}.html", PAGES[i - 1]["otsikko"]
        if i < len(PAGES) - 1:
            next_href, next_nimi = f"{PAGES[i+1]['slug']}.html", PAGES[i + 1]["otsikko"]
        else:
            next_href = next_nimi = None

        # Pohjan slug esiintyy myös sivukohtaisessa CSS:ssä (#goodhartin-laki
        # { border-top-color }) ja randomIlmio():n ohitusehdossa, joten se
        # vaihdetaan kaikkialta ja väri asetetaan erikseen kortin väriin.
        html = tpl.replace(VANHA_SLUG, slug)
        vari = OMAT_KORTIT[slug][1]
        html, n = re.subn(rf"(#{slug}\s+(?:\.ilmio-tag\s*)?\{{ (?:border-top-color|background): )#[0-9a-fA-F]{{6}}",
                          rf"\g<1>{vari}", html)
        assert n == 2, f"{slug}: sivun väri-CSS:ää ei löytynyt ({n})"
        html, n = re.subn(r"<title>.*?</title>", lambda m: f"<title>{p['title']}</title>",
                          html, count=1)
        assert n == 1, f"{slug}: <title> puuttuu pohjasta"

        html, n = re.subn(r"  <!-- SEO -->.*?\n</script>",
                          lambda m: seo_lohko(pohja_ld, slug, p["otsikko"], termi,
                                              p["title"], p["kuvaus"]),
                          html, count=1, flags=re.S)
        assert n == 1, f"{slug}: SEO-lohkoa ei löytynyt"

        html = html.replace(f'href="{VANHA_KAT_SIVU}" class="kortti-breadcrumb-kat">{VANHA_KAT_NIMI}<',
                            f'href="{KAT_SIVU}" class="kortti-breadcrumb-kat">{KAT_NIMI}<')

        uusi_ilmio = (f'<div class="ilmio" id="{slug}">\n'
                      f'<div class="ilmio-tag">Ilmiö {num}</div>\n'
                      f'<h1>{p["otsikko"]}</h1>\n'
                      f'<p class="ilmio-byline">Kirjoittanut <a href="tietoa.html" rel="author">Ilmiömies</a> · Päivitetty {PVM_FI}</p>'
                      f'{ankkuroi(p["sisalto"])}</div>')
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
        html, n = re.subn(r"const PREV = '[^']*';", lambda m: f"const PREV = '{prev_href}';", html)
        assert n == 1, f"{slug}: PREV puuttuu"
        html, n = re.subn(r"const NEXT = '[^']*';", lambda m: f"const NEXT = '{next_href or ''}';", html)
        assert n == 1, f"{slug}: NEXT puuttuu"

        # Goodhartin lakiin saa viitata vain sisältö, liittyvät-kortit ja IDS
        sallitut = (p["sisalto"].count(VANHA_SLUG) + p["liittyvat"].count(VANHA_SLUG)
                    + ids_js.count(VANHA_SLUG))
        assert html.count(VANHA_SLUG) == sallitut, f"{slug}: pohjan slug jäi sivulle"
        assert VANHA_KAT_NIMI not in html, f"{slug}: pohjan kategoria jäi sivulle"

        html = alikansiopolut(html)

        # sama tarkistus kuin lisaa_ilmiot.py tekee julkaistessa
        for jaannos in ('href="index.html"', 'href="tietoa.html"',
                        f'href="{KAT_SIVU}"', "s.src = 'js/"):
            assert jaannos not in html, f"{slug}: {jaannos} jäi juuripolkuna"

        (OUT / f"{slug}.html").write_text(html, encoding="utf-8")
        teksti = re.sub(r'<div class="mermaid">.*?</div>', " ", p["sisalto"], flags=re.S)
        teksti = teksti.split('<div class="lue-lisaa">')[0]
        sanat = len(re.sub(r"<[^>]+>", " ", p["otsikko"] + teksti).split())
        print(f"  {num}  {slug}.html  ({len(html) // 1024} KB, {sanat} sanaa)")

    kirjoita_hub_lohko()
    print(f"\nValmis: {len(PAGES)} luonnosta kansiossa {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    build()
