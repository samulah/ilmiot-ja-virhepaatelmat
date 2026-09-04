#!/usr/bin/env python3
"""
Kapea hakuaie 11 sivulle: title/meta + vastauslohko + FAQPage.

Tausta: seo-suunnitelmat/gsc-analyysi-2026-09-04.md (P2, P4 ja P5).

  - Sijoilla 5-11 on 73 % kaikista näytöistä ja CTR 1,0 % (ilman DARVOa
    0,33 %). Kynnys kulkee noin sijan 4 kohdalla, ei sijan 10.
  - Kuusi sivua kerää näyttöjä sijoilta 19-43 päätermeillä, joita ne eivät
    voi voittaa (viherpesu 52,1 · simple-sabotage 42,7 · smishing 38,1 ·
    ponzi-pyramidi 27,1 · gaslighting 25,8 · bkt-harha 19,2). Ne
    kohdistetaan kapeampaan aikeeseen, jonka sivu oikeasti palvelee.
  - Viideltä kärkisivulta puuttui FAQPage kokonaan; ne ovat sijoilla
    6,9-11,1 (uutiskynnys, klikkiotsikko, hajota-hallitse,
    parkinsonin-laki, kuollut-internet).

Kapea aie on valittu GSC:n omista kyselyistä, ei arvattu. Selvin tapaus on
bkt-harha: päätermeillä (bkt, bruttokansantuote) sija on 15-40, mutta
kyselyllä "mitä bkt mittaa" sija on jo 4,33. Sivu siis vastaa kapeaan
kysymykseen hyvin ja laajaan huonosti — title lupasi laajan.

Kolme muutosta per sivu:
  1. title + meta/og/twitter description  (kuten scripts/seo_titlet_ctr.py)
  2. näkyvä vastauslohko  (kuten scripts/seo_vastauslohko.py)
  3. FAQPage-schema @graphiin, kysymykset GSC:n sanamuodoilla

EI kosketa: H1, olemassa oleva leipäteksti, Article/DefinedTerm/breadcrumb,
ilmiönumerointi. H1 pysyy, koska lisaa_ilmiot.py ja paivita_maarat.py lukevat
siitä etusivun korttinimen — titlen vaihto ei aiheuta driftiä, H1:n vaihto
aiheuttaisi.

dateModified ja näkyvä "Päivitetty"-päivä nousevat, koska näkyvä sisältö
muuttuu. Aja jälkeen: build_sitemap.py ja build_search_index.py.

Deterministinen ja idempotentti: aja uudelleen turvallisesti.
    python3 scripts/seo_kapea_aie.py [--kirjoita]
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
MERKKI = "vastauslohko"
BRANDI = " | Ilmiöitä"
PVM_ISO = "2026-09-04"
PVM_NAKYVA = "4.9.2026"

# slug: {
#   "title":  title ilman brändihäntää (title + BRANDI <= 60 mk)
#   "kuvaus": meta description (<= 160 mk, ei lainausmerkkejä)
#   "lohko":  (h2-kysymys, vastaus-HTML) tai None = jätä nykyinen rauhaan
#   "faq":    [(kysymys, vastaus), ...]
#   "gsc":    mihin kyselyyn kapea aie osuu — dokumentaatio, ei koodia
# }
SIVUT = {

    # ---- P5: syvältä kapeampaan aikeeseen -----------------------------
    "bkt-harha": {
        "gsc": "mitä bkt mittaa (sija 4,33) vs. bkt/bruttokansantuote (15-40)",
        "title": "Mitä BKT mittaa — ja mitä se jättää pois",
        "kuvaus": "BKT mittaa rahassa mitattua tuotantoa, ei hyvinvointia. "
                  "Mitä bruttokansantuote jättää laskematta ja miksi kasvava "
                  "luku voi kertoa huonon uutisen.",
        "lohko": (
            "Mitä BKT mittaa — ja mitä se jättää mittaamatta?",
            "<strong>BKT</strong> mittaa vuoden aikana tuotettujen tavaroiden "
            "ja palveluiden markkina-arvon. Se laskee mukaan kaiken, mistä "
            "maksetaan — myös öljyvahingon siivouksen ja sairaanhoidon. "
            "Ulkopuolelle jäävät kotityö, vapaaehtoistyö, luonnonvarojen "
            "kuluminen ja tulonjako.",
        ),
        "faq": [
            ("Mitä BKT mittaa?",
             "BKT eli bruttokansantuote mittaa maan rajojen sisällä vuoden "
             "aikana tuotettujen lopputuotteiden ja palveluiden markkina-arvon. "
             "Mittari laskee mukaan kaiken maksullisen toiminnan riippumatta "
             "siitä, lisääkö se hyvinvointia vai korjaako se vahinkoa."),
            ("Miksi BKT ei mittaa hyvinvointia?",
             "Koska mittarin ehto on rahassa mitattu vaihdanta, ei hyöty. "
             "Kotityö, omaishoito ja vapaaehtoistyö jäävät kokonaan pois, "
             "kun taas onnettomuuden siivous, sairaanhoito ja pilaantuneen "
             "maan puhdistus kasvattavat lukua. Myöskään tulonjako ei näy: "
             "sama BKT voi jakautua hyvin eri tavoin."),
        ],
    },

    "viherpesu": {
        "gsc": "viherpesu (sija 52,1) — päätermi menetetty, tunnistaminen ei",
        "title": "Viherpesun tunnistaminen — seitsemän merkkiä",
        "kuvaus": "Viherpesu on vihreä mielikuva ilman tekoja. Seitsemän "
                  "tunnusmerkkiä, joilla erotat todennetun ympäristöväitteen "
                  "markkinointipuheesta.",
        "lohko": (
            "Miten viherpesun tunnistaa?",
            "Viherpesun tunnistaa <strong>väitteen tarkkuudesta</strong>. "
            "Todennettu väite kertoo, mitä mitattiin, millä menetelmällä ja "
            "kuka tarkasti. Viherpesu kertoo tunnelman: vihreä, luonnollinen, "
            "ilmastoystävällinen. EU-direktiivi 2024/825 kieltää juuri nämä "
            "yleisväitteet ilman näyttöä.",
        ),
        "faq": [
            ("Mitä viherpesu tarkoittaa?",
             "Viherpesu eli greenwashing tarkoittaa markkinointia, joka saa "
             "yrityksen tai tuotteen näyttämään ympäristöystävällisemmältä "
             "kuin se on. Raha käytetään vihreän mielikuvan rakentamiseen, ei "
             "toiminnan muuttamiseen. Termin keksi Jay Westerveld 1986."),
            ("Onko viherpesu laitonta?",
             "EU:n kuluttajansuojadirektiivi 2024/825 kieltää yleiset "
             "ympäristöväitteet kuten ympäristöystävällinen, vihreä tai "
             "ilmastoneutraali ilman todennettua näyttöä, samoin pelkkään "
             "päästökompensaatioon perustuvat neutraaliusväitteet. Sääntöjä "
             "sovelletaan syyskuusta 2026. Suomessa valvoo kuluttaja-asiamies."),
        ],
    },

    "gaslighting": {
        "gsc": "gaslighting (25,8) menetetty; tunnistaminen ja esimerkit auki",
        "title": "Gaslightingin tunnistaminen — merkit ja esimerkit",
        "kuvaus": "Gaslighting eli kaasuvalotus saa toisen epäilemään omaa "
                  "muistiaan ja havaintojaan. Tyypilliset lauseet, kolme tasoa "
                  "ja se mikä ei ole gaslightingia.",
        # Nykyinen vastauslohko vastaa kyselyyn "gaslighting suomeksi"
        # (14 näyttöä) eikä sitä kannata korvata. Vain title, meta ja FAQ.
        "lohko": None,
        "faq": [
            ("Miten gaslightingin tunnistaa?",
             "Tunnusmerkki on se, että keskustelu siirtyy tapahtuneesta sinun "
             "havaintokykyysi: et muista oikein, olet ylireagoiva, kuvittelet. "
             "Yksittäinen erimielisyys muistista ei ole gaslightingia — "
             "toistuva kaava, jossa oma muistikuvasi asetetaan kysymyksenalaiseksi, on."),
            ("Mitä gaslighting on suomeksi?",
             "Suomeksi käytetään sanoja kaasuvalotus ja kaasuvalottaminen. "
             "Molemmat ovat käännöslainoja Patrick Hamiltonin näytelmästä "
             "Gas Light (1938), jossa aviomies himmentää kaasuvaloja ja "
             "kiistää vaimon havainnon. Vakiintunein muoto on yhä gaslighting."),
        ],
    },

    "ponzi-pyramidi": {
        "gsc": "pyramidihuijaus (41,8) ja ponzi huijaus (22,0) — ero on kapea aie",
        "title": "Ponzi vai pyramidihuijaus — mikä on ero",
        "kuvaus": "Ponzissa järjestäjä maksaa tuotot uusien sijoittajien "
                  "rahoilla, pyramidissa uhrit värväävät itse. Näin erotat ne "
                  "ja tunnistat molemmat ajoissa.",
        "lohko": (
            "Mitä eroa on Ponzi-huijauksella ja pyramidihuijauksella?",
            "Molemmissa tuotot maksetaan uusien uhrien rahoilla, mutta värväys "
            "eroaa. <strong>Ponzissa</strong> järjestäjä hoitaa kaiken: "
            "sijoittaja saa tuotto-otteen eikä tiedä mistä raha tulee. "
            "<strong>Pyramidissa</strong> uhri värvää itse uusia jäseniä ja "
            "tienaa heidän maksuistaan. Molemmat romahtavat samasta syystä: "
            "uutta rahaa ei riitä.",
        ),
        "faq": [
            ("Mikä on pyramidihuijaus?",
             "Pyramidihuijauksessa jäsen maksaa liittymismaksun ja tienaa "
             "värväämällä uusia jäseniä, jotka maksavat hänelle. Rakenne on "
             "matemaattisesti mahdoton: jokainen taso vaatii moninkertaisen "
             "määrän uusia uhreja, ja väki loppuu kesken. Romahdus on varma, "
             "vain ajankohta on auki."),
            ("Miten Ponzi-huijauksen tunnistaa?",
             "Tuotto on epätavallisen hyvä ja epätavallisen tasainen — oikea "
             "sijoitus heiluu, huijaus ei. Strategiaa ei selitetä tai selitys "
             "on liian monimutkainen tarkistettavaksi, ja nostoja viivytellään "
             "tai palkitaan uudelleensijoittamisesta. Nimi tulee Charles "
             "Ponzilta (1920)."),
        ],
    },

    "simple-sabotage": {
        "gsc": "kaikki kyselyt koskevat itse käsikirjaa (field manual, pdf)",
        "title": "Simple Sabotage Field Manual suomeksi",
        "kuvaus": "OSS:n vuoden 1944 käsikirja opetti sabotoimaan "
                  "organisaatiota sisältäpäin. Mitä ohjeet sanovat ja miksi ne "
                  "kuvaavat monen nykyorganisaation arkea.",
        "lohko": (
            "Mikä Simple Sabotage Field Manual on?",
            "OSS:n eli CIA:n edeltäjän vuonna 1944 julkaisema käsikirja. "
            "Kuuluisin osa on <strong>byrokratiasabotaasi</strong>: vaadi asiat "
            "kirjallisina, vie päätökset komiteoihin, palaa jo päätettyihin "
            "kysymyksiin, pidä pitkiä puheenvuoroja. Teho perustuu siihen, "
            "että sabotoija näyttää tunnolliselta.",
        ),
        "faq": [
            ("Mitä Simple Sabotage Field Manual neuvoo?",
             "Byrokratiaosuus neuvoo vaatimaan asiat kirjallisina, viemään "
             "päätökset komiteoihin, palaamaan jo päätettyihin asioihin, "
             "pitämään pitkiä puheenvuoroja ja vaatimaan tarkkaa "
             "sääntöjen noudattamista. Ohjeiden teho perustuu siihen, että "
             "sabotoija näyttää tunnolliselta työntekijältä."),
            ("Onko Simple Sabotage Field Manual aito?",
             "On. Käsikirjan julkaisi Office of Strategic Services eli OSS, "
             "CIA:n edeltäjä, vuonna 1944, ja CIA on sittemmin julkaissut "
             "asiakirjan yleisesti saataville. Se ei ole nettihuhu vaan "
             "arkistoitu virastojulkaisu."),
        ],
    },

    "smishing": {
        "gsc": "ainoa kysely on phishing suomeksi (42,5) — omaa termiä ei haeta",
        "title": "Huijaustekstiviesti — näin tunnistat smishingin",
        "kuvaus": "Smishing on tekstiviestillä tehty kalastelu: viesti näyttää "
                  "tulevan Postilta tai pankilta. Näin tunnistat huijausviestin "
                  "ja mitä teet jos ehdit klikata.",
        "lohko": None,
        "faq": [
            ("Miten huijaustekstiviestin tunnistaa?",
             "Viesti luo kiireen ja pyytää klikkaamaan linkkiä: paketti "
             "odottaa, tili suljetaan, maksu epäonnistui. Osoite on lähes "
             "oikea mutta ei aivan. Luotettava lähettäjä ei koskaan pyydä "
             "pankkitunnuksia tai korttitietoja tekstiviestin linkin kautta."),
            ("Mitä teen jos klikkasin huijausviestin linkkiä?",
             "Pelkkä linkin avaaminen ei yleensä riitä vahinkoon. Jos syötit "
             "pankkitunnukset, sulje verkkopankki heti ja soita pankkiisi. "
             "Jos annoit korttitiedot, sulje kortti. Tee rikosilmoitus ja "
             "ilmoita viestistä Traficomin Kyberturvallisuuskeskukselle."),
        ],
    },

    # ---- P4: FAQ puuttui kokonaan, sija 6,9-11,1 ----------------------
    "uutiskynnys": {
        "gsc": "uutiskynnys 6,02 · mikä on uutiskynnys 9,23 · englanniksi 4,40",
        "title": "Mikä on uutiskynnys — ja miksi se ylitetään",
        "kuvaus": "Uutiskynnys on raja, jonka tapahtuman on ylitettävä "
                  "päästäkseen uutiseksi. Mitkä kriteerit ratkaisevat, mikä jää "
                  "alle ja miten kynnys ylitetään tarkoituksella.",
        "lohko": (
            "Mikä on uutiskynnys?",
            "<strong>Uutiskynnys</strong> (englanniksi <em>news threshold</em>) "
            "on toimituksen rutiini, ei mielipide aiheesta. Sen ylittää "
            "tapahtuma, jolla on hetki, tekijä ja uhri. Alle jää se, mikä "
            "muuttuu hitaasti ilman yksittäistä hetkeä: korjausvelka, "
            "hoitojonot, lainvalmistelu.",
        ),
        "faq": [
            ("Mikä on uutiskynnys?",
             "Uutiskynnys on se raja, jonka tapahtuman on ylitettävä "
             "päästäkseen uutiseksi. Kyse ei ole yksittäisestä päätöksestä "
             "vaan toimituksen päivittäisestä rutiinista, jossa satoja "
             "mahdollisia aiheita arvioidaan vakiintuneilla kriteereillä: "
             "tuoreus, yllättävyys, suuruus, läheisyys ja henkilöityminen."),
            ("Mitä uutiskynnys on englanniksi?",
             "Uutiskynnys on englanniksi news threshold. Taustalla oleva "
             "tutkimuskäsite on news values eli uutiskriteerit, jotka Johan "
             "Galtung ja Mari Holmboe Ruge kuvasivat vuonna 1965."),
        ],
    },

    "klikkiotsikko": {
        "gsc": "clickbait suomeksi 6,50 · klikkiotsikko englanniksi 11,0",
        "title": "Klikkiotsikko — clickbait suomeksi",
        "kuvaus": "Clickbait eli klikkiotsikko lupaa tiedon, jonka juttu "
                  "jättää antamatta. Vakiorakenteet, uteliaisuusaukon "
                  "mekanismi ja miten lakkaat klikkaamasta.",
        "lohko": (
            "Mikä on clickbait suomeksi?",
            "<strong>Clickbait</strong> on suomeksi <strong>klikkiotsikko</strong>; "
            "käytössä ovat myös <em>klikkiuutinen</em> ja <em>klikinkalastelu</em>. "
            "Vakiorakenteita on viisi: pidätetty subjekti, pidätetty "
            "lopputulos, lukija toisena persoonana, numerolista ja "
            "kysymysmuoto. Jokainen jättää saman aukon auki.",
        ),
        "faq": [
            ("Mitä clickbait tarkoittaa suomeksi?",
             "Clickbait tarkoittaa suomeksi klikkiotsikkoa, toisinaan myös "
             "klikkiuutista. Se on otsikko, jonka tehtävä on tuottaa klikki "
             "eikä kertoa mitä juttu sisältää: otsikko kertoo että jotain "
             "kiinnostavaa tapahtui, muttei mitä."),
            ("Miksi klikkiotsikot toimivat?",
             "Psykologi George Loewensteinin information gap -teorian (1994) "
             "mukaan uteliaisuus ei synny tietämättömyydestä vaan siitä, että "
             "huomaamme aukon omassa tiedossamme. Aukko tuntuu "
             "epämiellyttävältä ja sen sulkeminen palkitsee. Klikkiotsikko "
             "avaa aukon tarkoituksella ja myy sen sulkemisen."),
        ],
    },

    "hajota-hallitse": {
        "gsc": "divide et impera suomeksi 11,0 · hajota ja hallitse 12,4",
        "title": "Hajota ja hallitse — divide et impera suomeksi",
        "kuvaus": "Divide et impera tarkoittaa suomeksi hajota ja hallitse: "
                  "valta säilyy, kun mahdolliset haastajat taistelevat "
                  "keskenään. Näin tunnistat jakolinjan rakentamisen.",
        "lohko": (
            "Mitä divide et impera tarkoittaa suomeksi?",
            "Latinan <em>divide et impera</em> tarkoittaa suomeksi "
            "<strong>hajota ja hallitse</strong>. Ilmaus liitetään Rooman "
            "hallintotapaan, mutta sen tarkkaa alkuperää ei tunneta. Sääntönä "
            "se on halpa: hallitsijan ei tarvitse voittaa haastajiaan, riittää "
            "että ne pitävät toisiaan vihollisina.",
        ),
        "faq": [
            ("Mitä hajota ja hallitse tarkoittaa?",
             "Hajota ja hallitse on vallan ylläpitämisen strategia, jossa "
             "hallitseva taho pitää valtansa jakamalla mahdolliset "
             "vastavoiman muodostajat toisilleen vihamielisiin ryhmiin. "
             "Koalitio, joka voisi haastaa vallan, ei muodostu, koska sen "
             "osat taistelevat keskenään."),
            ("Mistä divide et impera on peräisin?",
             "Ilmaus on latinaa ja se on liitetty perinteisesti Rooman "
             "valtakunnan hallintotapaan, vaikka lauseen tarkkaa alkuperää ei "
             "tunneta. Samaa periaatetta on käytetty siirtomaahallinnossa, "
             "työmarkkinoilla ja politiikassa aina siellä, missä hallitsijan "
             "on halvempaa jakaa kuin voittaa."),
        ],
    },

    "parkinsonin-laki": {
        "gsc": "parkinsonin laki 10,93 — ainoa kysely, sija juuri kynnyksen alla",
        "title": "Parkinsonin laki — miksi työ venyy aikarajaan",
        "kuvaus": "Parkinsonin laki: työ laajenee täyttämään sille varatun "
                  "ajan. Mistä sääntö tulee, mitä Parkinson todella mittasi ja "
                  "miten aikarajan asettaa oikein.",
        "lohko": (
            "Mitä Parkinsonin laki tarkoittaa?",
            "<strong>Työ laajenee täyttämään sille varatun ajan.</strong> Jos "
            "tehtävälle varataan viikko, se vie viikon, vaikka olisi tehtävissä "
            "päivässä. Parkinsonin havainto koski hallintoa, jonka koko kasvoi "
            "vaikka työn määrä laski. Vastalääke on aikaraja, joka asetetaan "
            "ennen aloitusta eikä sen jälkeen.",
        ),
        "faq": [
            ("Mitä Parkinsonin laki tarkoittaa?",
             "Parkinsonin laki tarkoittaa sitä, että työ laajenee täyttämään "
             "sille varatun ajan. Jos tehtävälle annetaan viikko, se vie "
             "viikon, vaikka se olisi tehtävissä päivässä. Cyril Northcote "
             "Parkinson esitti lauseen The Economist -lehdessä vuonna 1955."),
            ("Pitääkö Parkinsonin laki paikkansa?",
             "Parkinsonin oma näyttö oli tilastollinen: Britannian laivaston "
             "hallintohenkilöstö kasvoi vuosina 1914–1928, vaikka aluksia ja "
             "merimiehiä oli entistä vähemmän. Havainto hallinnon "
             "itsekasvusta on toistunut myöhemmissä organisaatiotutkimuksissa, "
             "mutta laki on kuvaus taipumuksesta, ei luonnonlaki."),
        ],
    },

    "kuollut-internet": {
        "gsc": "dead internet teoria 11,64 · kuollut internet teoria 10,83",
        "title": "Dead internet -teoria — pitääkö se paikkansa",
        "kuvaus": "Kuollut internet -teoria väittää verkon täyttyneen "
                  "boteista. Mikä väitteessä on mitattua ja mikä "
                  "salaliittoteoriaa — ja mitä luvut oikeasti sanovat.",
        "lohko": (
            "Pitääkö kuollut internet -teoria paikkansa?",
            "Vahva muoto ei: väitteelle keskitetystä operaatiosta, jossa "
            "internet vaihdettiin koneelliseksi, ei ole näyttöä. "
            "<strong>Heikko muoto on mitattavissa</strong> — tietoturvayhtiö "
            "Impervan mittauksissa bottien osuus verkkoliikenteestä on noin "
            "puolet, ja generoitu halpasisältö täyttää haun.",
        ),
        "faq": [
            ("Mikä on dead internet -teoria?",
             "Dead internet theory eli kuollut internet -teoria väittää, että "
             "internet kuoli 2010-luvun puolivälissä: valtaosa verkon "
             "sisällöstä ja vuorovaikutuksesta olisi sen jälkeen ollut "
             "botteja ja koneellisesti tuotettua. Teoria sai nimensä Agora "
             "Road -foorumin postauksesta vuonna 2021."),
            ("Kuinka suuri osa verkkoliikenteestä on botteja?",
             "Tietoturvayhtiö Impervan mittauksissa bottien osuus "
             "verkkoliikenteestä on ylittänyt ihmisten osuuden rajan "
             "tuntumassa: noin puolet liikenteestä on automaattista. Luku "
             "koskee liikennettä, ei sisältöä tai käyttäjätilejä, joten se ei "
             "vielä todista teorian vahvaa muotoa."),
        ],
    },
}

FAQ_SIJAINTI = re.compile(
    r'(<div class="ilmio"[^>]*>.*?<p class="ilmio-byline">.*?</p>\s*<p>.*?</p>)',
    re.S,
)


def korvaa(html, kaava, uusi, slug, kentta):
    uusi_html, n = re.subn(kaava, lambda _: uusi, html, count=1)
    if n == 0:
        raise SystemExit(f"VIRHE {slug}: kenttää {kentta} ei löytynyt")
    return uusi_html


def lohko_html(kysymys, vastaus):
    return (
        f'\n<div class="infolaatikko {MERKKI}">\n'
        f'<h2 class="laatikko-otsikko">{kysymys}</h2>\n'
        f'<p style="margin:0.4em 0 0;">{vastaus}</p>\n'
        f'</div>'
    )


def faq_node(slug, faq):
    return {
        "@type": "FAQPage",
        "@id": f"https://www.ilmiöt.fi/{slug}.html#faq",
        "inLanguage": "fi",
        "mainEntity": [
            {"@type": "Question", "name": k,
             "acceptedAnswer": {"@type": "Answer", "text": v}}
            for k, v in faq
        ],
    }


def kasittele(slug, t, kuiva):
    polku = ROOT / f"{slug}.html"
    if not polku.exists():
        raise SystemExit(f"VIRHE: {polku.name} puuttuu")
    teksti = alkup = polku.read_text(encoding="utf-8")

    title = t["title"] + BRANDI
    kuvaus = " ".join(t["kuvaus"].split())
    if '"' in kuvaus or '"' in title:
        raise SystemExit(f"VIRHE {slug}: lainausmerkki title/kuvaus-kentässä")

    # 1. title + viisi meta-kenttää
    teksti = korvaa(teksti, r"<title>.*?</title>",
                    f"<title>{title}</title>", slug, "title")
    for kaava, arvo, nimi in [
        (r'<meta name="description" content=".*?">',
         f'<meta name="description" content="{kuvaus}">', "description"),
        (r'<meta property="og:title" content=".*?">',
         f'<meta property="og:title" content="{title}">', "og:title"),
        (r'<meta property="og:description" content=".*?">',
         f'<meta property="og:description" content="{kuvaus}">', "og:description"),
        (r'<meta name="twitter:title" content=".*?">',
         f'<meta name="twitter:title" content="{title}">', "twitter:title"),
        (r'<meta name="twitter:description" content=".*?">',
         f'<meta name="twitter:description" content="{kuvaus}">', "twitter:description"),
    ]:
        teksti = korvaa(teksti, kaava, arvo, slug, nimi)

    # 2. näkyvä vastauslohko (None = jätä nykyinen rauhaan)
    merkkeja = None
    if t["lohko"]:
        kysymys, vastaus = t["lohko"]
        teksti = re.sub(r'\n<div class="infolaatikko ' + MERKKI + r'">.*?</div>',
                        "", teksti, flags=re.S)
        osuma = FAQ_SIJAINTI.search(teksti)
        if not osuma:
            raise SystemExit(f"VIRHE {slug}: vastauslohkon paikkaa ei löytynyt")
        teksti = teksti.replace(
            osuma.group(1), osuma.group(1) + lohko_html(kysymys, vastaus), 1)
        merkkeja = len(re.sub(r"<[^>]+>", "", vastaus))

    # 3. FAQPage @graphiin
    def paivita_graph(m):
        data = json.loads(m.group(1))
        if "@graph" not in data:
            return m.group(0)
        data["@graph"] = [n for n in data["@graph"] if n.get("@type") != "FAQPage"]
        data["@graph"].append(faq_node(slug, t["faq"]))
        return ('<script type="application/ld+json">\n'
                + json.dumps(data, ensure_ascii=False, indent=2)
                + "\n</script>")

    teksti, n = re.subn(
        r'<script type="application/ld\+json">\s*(\{.*?"@graph".*?\})\s*</script>',
        paivita_graph, teksti, count=1, flags=re.S)
    if n == 0:
        raise SystemExit(f"VIRHE {slug}: @graph-lohkoa ei löytynyt")

    # 4. dateModified + näkyvä päivä (näkyvä sisältö muuttui)
    teksti = korvaa(teksti, r'"dateModified": "\d{4}-\d{2}-\d{2}"',
                    f'"dateModified": "{PVM_ISO}"', slug, "dateModified")
    teksti = re.sub(r'(<p class="ilmio-byline">.*?Päivitetty )[\d.]+(</p>)',
                    rf'\g<1>{PVM_NAKYVA}\g<2>', teksti, count=1, flags=re.S)

    varoitukset = []
    if len(title) > 60:
        varoitukset.append(f"title {len(title)} mk")
    if len(kuvaus) > 160:
        varoitukset.append(f"kuvaus {len(kuvaus)} mk")
    if merkkeja is not None and not 240 <= merkkeja <= 300:
        varoitukset.append(f"lohko {merkkeja} mk (tavoite 240-300)")

    if not kuiva and teksti != alkup:
        polku.write_text(teksti, encoding="utf-8")

    lohkotieto = f"lohko {merkkeja} mk" if merkkeja else "lohko ennallaan"
    varo = ("   ← " + ", ".join(varoitukset)) if varoitukset else ""
    return (f"{slug:<18} title {len(title):2d} mk · kuvaus {len(kuvaus):3d} mk · "
            f"{lohkotieto} · {len(t['faq'])} FAQ{varo}"), not varoitukset


def main():
    kuiva = "--kirjoita" not in sys.argv
    print("KUIVAHARJOITUS — mitään ei kirjoiteta. Kirjoita: --kirjoita\n"
          if kuiva else "KIRJOITETAAN\n")
    ok = True
    for slug, t in SIVUT.items():
        rivi, hyva = kasittele(slug, t, kuiva)
        print(rivi)
        ok = ok and hyva
    print(f"\n{len(SIVUT)} sivua käsitelty.")
    if not kuiva:
        print("Aja seuraavaksi:\n"
              "  python3 scripts/build_sitemap.py\n"
              "  python3 scripts/build_search_index.py")
    if not ok:
        print("\nVaroituksia — tarkista pituudet.")


if __name__ == "__main__":
    main()
