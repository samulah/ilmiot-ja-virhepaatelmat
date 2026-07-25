#!/usr/bin/env python3
"""
Vaihe 2: "suomeksi"-vastauslohko + FAQPage-schema (top-15 sivua).

Tausta: seo-suunnitelmat/gsc-analyysi-2026-07-25.md
  - 30 % näytöistä (257/847) tulee kyselyistä, joissa on suomeksi /
    tarkoittaa / mitä on / mikä on / englanniksi. Klusterin keskisijainti
    on 11,6 eli sivuston heikoin.
  - "X suomeksi" -SERPejä hallitsevat sanakirjat, jotka vastaavat
    kysymykseen yhdellä rivillä. Ilmiöt.fi ei vastannut siihen lainkaan.
  - Koko sivustolla oli ennen tätä yksi ainoa FAQPage-schema (index.html).

POIKKEAMA SUUNNITELMASTA (tietoinen):
Suunnitelma ehdotti vastauslohkoa H1:n alle vastaamaan kysymykseen
"mitä X tarkoittaa". Kaikki 15 sivua kuitenkin JO avautuvat sillä
määritelmällä, joten lohko olisi toistanut ensimmäisen kappaleen.
Puuttuva pala on nimenomaan suomennos, ei määritelmä. Siksi lohko
vastaa käännöskysymykseen ja sijoittuu ensimmäisen kappaleen jälkeen.

SUOMENNOSLINJA:
Suunnitelman taulukko listaa "vakiintuneita suomennoksia", joita osa ei
ole. ai-slop.html sanoo itse leipätekstissään, ettei slopille ole
vakiintunutta suomennosta. Siksi lohko erottaa kaksi tapausta:
  - Vakiintunut vastine on olemassa  -> se sanotaan suoraan.
  - Vastinetta ei ole                -> se sanotaan suoraan, ja
                                        liikkeellä olevat muodot
                                        mainitaan sellaisina kuin ovat.
Keksittyä suomennosta ei esitetä vakiintuneena.

EI kosketa: H1, olemassa oleva leipäteksti, DefinedTerm- tai
Article-schema, breadcrumbit, title/meta (ne ovat vaiheen 1 vastuulla).

Deterministinen ja idempotentti: aja uudelleen turvallisesti.
    python3 scripts/seo_vastauslohko.py [--kuivaharjoitus]

Ajon jälkeen: python3 scripts/build_search_index.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
MERKKI = "vastauslohko"

# slug: (h2-kysymys, vastaus-HTML, [(faq-kysymys, faq-vastaus), ...])
#
# Vastaus mitoitettu 40-55 sanaan -> kelpaa featured snippetiksi ja
# AI-sitaatiksi. Vakiintunut vastine lihavoidaan ensimmäisessä virkkeessä.
# FAQ-vastaukset ovat omaa tekstiä, eivät leipätekstin kopioita.
SIVUT = {
    "whataboutismi": (
        "Mikä on whataboutismi suomeksi?",
        "<strong>Whataboutismi</strong> on jo suomenkielinen muoto englannin "
        "sanasta <em>whataboutism</em>. Samasta ilmiöstä käytetään myös "
        "nimityksiä <strong>entäs-argumentti</strong> ja <strong>mutkuttelu</strong>. "
        "Kaikki tarkoittavat samaa: esitettyyn kritiikkiin ei vastata, vaan "
        "vastataan vastasyytöksellä — \"entäs te itse?\"",
        [
            ("Mitä whataboutismi tarkoittaa?",
             "Whataboutismi tarkoittaa syytökseen tai kritiikkiin vastaamista "
             "vastasyytöksellä sen sijaan, että vastattaisiin itse asiaan. "
             "Keskustelu siirtyy alkuperäisestä aiheesta vastapuolen "
             "puutteisiin, eikä esitettyyn väitteeseen oteta kantaa. "
             "Tekniikka tunnetaan myös nimillä entäs-argumentti ja mutkuttelu."),
            ("Miten whataboutismiin kannattaa vastata?",
             "Nimeä siirto ääneen ja palauta keskustelu alkuperäiseen "
             "kysymykseen: \"Palataan siihen erikseen — vastaatko ensin "
             "tähän?\" Vastasyytös voi olla aiheellinen, mutta se ei kumoa "
             "alkuperäistä väitettä. Kaksi erillistä kysymystä käsitellään "
             "erikseen, ei toistensa vastauksina."),
        ],
    ),
    "ai-slop": (
        "Mikä on AI slop suomeksi?",
        "<strong>AI slopille ei ole vakiintunutta suomennosta.</strong> "
        "Liikkeellä ovat muodot <em>tekoälylieju</em> ja <em>tekoälyroska</em>, "
        "mutta yleisimmin käytetään englanninkielistä sanaa sellaisenaan. "
        "Slop tarkoittaa generatiivisella tekoälyllä massatuotettua sisältöä, "
        "jonka tarkoitus on kerätä klikkejä eikä palvella lukijaa.",
        [
            ("Mitä AI slop tarkoittaa?",
             "AI slop tarkoittaa generatiivisella tekoälyllä massatuotettua "
             "halpaa sisältöä — artikkeleita, kuvia, videoita — jonka "
             "tarkoitus ei ole palvella vastaanottajaa vaan kerätä klikkejä "
             "ja mainostuloja mahdollisimman pienellä vaivalla. Englannin "
             "slop tarkoittaa sioille kaadettavaa ruokajätettä."),
            ("Miten AI slopin tunnistaa?",
             "Tunnusmerkkejä ovat tekijän puuttuminen, lähteetön varmuus, "
             "geneerinen otsikkokaava sekä kuvat, joissa yksityiskohdat eivät "
             "kestä katsetta. Teksti on kieliopillisesti moitteetonta muttei "
             "sisällä yhtään havaintoa, jota kirjoittaja ei olisi voinut "
             "tehdä lukematta aiheesta mitään."),
        ],
    ),
    "hyvesignalointi": (
        "Mikä on hyvesignalointi suomeksi?",
        "<strong>Hyvesignalointi</strong> on vakiintunut suomennos englannin "
        "termistä <em>virtue signalling</em>. Rinnalla käytetään myös sanaa "
        "<strong>moraaliposeeraus</strong>. Molemmat tarkoittavat moraalisen "
        "kannan julkista esittämistä niin, että esittämisen ensisijainen "
        "tehtävä on kertoa esittäjästään hyvää — ei edistää itse asiaa.",
        [
            ("Mitä hyvesignalointi tarkoittaa?",
             "Hyvesignalointi tarkoittaa moraalisen kannan julkista "
             "esittämistä, jonka ensisijainen tehtävä on rakentaa esittäjän "
             "mainetta eikä edistää asiaa, jota kannanotto koskee. Ero "
             "aitoon kannanottoon näkyy siinä, mitä esittämisen jälkeen "
             "tapahtuu: seuraako sanoja mitään."),
            ("Onko hyvesignalointi aina kielteistä?",
             "Ei. Julkinen kannanotto voi olla sekä aito että maineelle "
             "hyödyllinen — motiivit eivät sulje toisiaan pois. Syytöstä "
             "hyvesignaloinnista käytetäänkin usein keskustelun "
             "vaientamiseen. Kysymys kannattaa kohdistaa tekoihin, ei "
             "toisen ihmisen oletettuihin vaikuttimiin."),
        ],
    ),
    "darvo": (
        "Mitä DARVO tarkoittaa suomeksi?",
        "<strong>DARVO</strong> on lyhenne sanoista <em>Deny, Attack, Reverse "
        "Victim and Offender</em> — suomeksi <strong>kiistä, hyökkää, käännä "
        "uhrin ja syyttäjän roolit</strong>. Vakiintunutta suomenkielistä "
        "lyhennettä ei ole, joten termi esiintyy suomeksikin muodossa DARVO. "
        "Psykologi Jennifer Freyd kuvasi mallin vuonna 1997.",
        [
            ("Mitä DARVO tarkoittaa?",
             "DARVO on reaktiostrategia, jota väärinkäytöksestä vastuulliseksi "
             "epäilty käyttää kolmessa vaiheessa: hän kiistää tapahtuneen, "
             "hyökkää syytöksen esittäjää vastaan ja esittää lopulta itsensä "
             "todellisena uhrina. Lopputulos on, että alkuperäinen kysymys "
             "jää käsittelemättä."),
            ("Miten DARVOn tunnistaa?",
             "Tunnusmerkki on roolien vaihtuminen kesken keskustelun: "
             "aihe siirtyy siitä, mitä tapahtui, siihen, miten epäoikeuden"
             "mukaisesti asian esiin nostanut on toiminut. Kun huomaat "
             "puolustavasi omaa oikeuttasi kysyä, roolit on jo käännetty."),
        ],
    ),
    "rage-bait": (
        "Mikä on rage bait suomeksi?",
        "<strong>Rage bait</strong> on suomeksi <strong>raivosyötti</strong>. "
        "Se tarkoittaa sisältöä, joka on tarkoituksella suunniteltu "
        "suututtamaan katsojansa — koska raivo tuottaa reaktioita, reaktiot "
        "näkyvyyttä ja näkyvyys rahaa. Ärsyttävyys ei ole tekijän "
        "epäonnistuminen vaan sen tarkoitus.",
        [
            ("Mitä rage bait tarkoittaa?",
             "Rage bait eli raivosyötti tarkoittaa sisältöä, jonka "
             "ensisijainen tavoite on herättää suuttumusta. Suuttumus saa "
             "jakamaan, kommentoimaan ja kiistelemään, ja jokainen reaktio "
             "kasvattaa sisällön näkyvyyttä algoritmissa. Virhe tai typerä "
             "väite on tällöin syötti, ei vahinko."),
            ("Miten raivosyöttiin kannattaa reagoida?",
             "Tehokkain vastaus on olla antamatta reaktiota: älä kommentoi, "
             "jaa tai lainaa sisältöä edes kritisoidaksesi sitä. Myös "
             "vihainen sitaatti on näkyvyyttä. Jos haluat vastata, tee se "
             "kuvakaappauksella ilman linkkiä, jolloin reaktio ei valu "
             "alkuperäisen julkaisijan hyväksi."),
        ],
    ),
    "dunning-kruger": (
        "Mitä Dunning–Kruger-ilmiö tarkoittaa?",
        "<strong>Dunning–Kruger-ilmiö</strong> tarkoittaa, että heikoimmin "
        "osaavat yliarvioivat osaamisensa eniten. Sama tietämättömyys, joka "
        "estää suoriutumasta hyvin, estää myös huomaamasta omaa "
        "heikkoutta. Suomeksi ilmiöstä puhutaan myös nimellä "
        "<strong>osaamisharha</strong>. Justin Kruger ja David Dunning "
        "osoittivat sen vuonna 1999.",
        [
            ("Mitä Dunning–Kruger-ilmiö tarkoittaa?",
             "Dunning–Kruger-ilmiö tarkoittaa, että heikoimmin osaavat "
             "arvioivat oman osaamisensa selvästi todellista paremmaksi. "
             "Arviointi vaatii samaa taitoa kuin suorittaminen, joten se "
             "jolta taito puuttuu ei myöskään näe puutetta. Osaamisen "
             "karttuessa itsearvio usein ensin laskee."),
            ("Kuinka Dunning–Kruger-ilmiötä voi torjua?",
             "Korvaa itsearvio ulkoisella mittarilla: pyydä palautetta, "
             "vertaa työtäsi alan parhaisiin esimerkkeihin ja testaa "
             "osaamista tilanteessa, jossa tulos on yksiselitteinen. "
             "Epävarmuuden tunne osaamisen karttuessa on merkki "
             "edistymisestä, ei taantumisesta."),
        ],
    ),
    "halo-efekti": (
        "Mikä on halo-efekti suomeksi?",
        "<strong>Halo-efekti</strong> tunnetaan suomeksi myös nimellä "
        "<strong>sädekehävaikutus</strong>. Se tarkoittaa kognitiivista "
        "vinoumaa, jossa yksi myönteinen piirre saa olettamaan muutkin "
        "piirteet myönteisiksi. Käänteistä versiota, jossa yksi kielteinen "
        "piirre värittää kaiken muun, kutsutaan stigmaksi eli "
        "sarvi-ilmiöksi.",
        [
            ("Mitä halo-efekti tarkoittaa?",
             "Halo-efekti tarkoittaa, että yhden myönteisen ominaisuuden "
             "havaitseminen saa päättelemään ihmisellä olevan muitakin "
             "myönteisiä ominaisuuksia, joista ei ole mitään tietoa. "
             "Edward Thorndike kuvasi ilmiön vuonna 1920 huomattuaan, että "
             "upseerien arviot alaisistaan korreloivat epäuskottavan vahvasti."),
            ("Miten halo-efektin vaikutusta voi vähentää?",
             "Arvioi yksi ominaisuus kerrallaan ja kirjaa arvio ylös ennen "
             "kuin siirryt seuraavaan. Rekrytoinnissa auttavat "
             "anonymisoidut työnäytteet ja se, että eri arvioijat "
             "käsittelevät eri osa-alueet toisistaan tietämättä. "
             "Yhteisarvio kannattaa muodostaa vasta lopuksi."),
        ],
    ),
    "bkt-harha": (
        "Mitä BKT-harha tarkoittaa?",
        "<strong>BKT-harha</strong> tarkoittaa bruttokansantuotteen "
        "lukemista hyvinvoinnin mittarina, vaikka se mittaa vain tuotannon "
        "arvoa — ei sitä, kenelle arvo päätyy. Irlanti on oppikirjaesimerkki: "
        "BKT hyppäsi vuonna 2015 yhdessä vuodessa 26 prosenttia ilman, että "
        "kotitalouksien tulot juuri muuttuivat.",
        [
            ("Mitä BKT mittaa ja mitä se ei mittaa?",
             "BKT mittaa maassa tuotettujen tavaroiden ja palvelujen "
             "yhteisarvon. Se ei kerro tulonjaosta, varallisuuden "
             "keskittymisestä, palkattomasta työstä eikä ympäristön "
             "kulumisesta. Siksi BKT voi kasvaa samalla kun mediaanitulo "
             "polkee paikallaan."),
            ("Mikä on leprechaun economics?",
             "Leprechaun economics on ekonomisti Paul Krugmanin nimitys "
             "Irlannin vuoden 2015 BKT-hypylle. Kasvun syy ei ollut "
             "tuottavuus vaan se, että monikansalliset yhtiöt siirsivät "
             "immateriaalioikeuksiaan kirjanpidollisesti Irlantiin matalan "
             "yhteisöveron takia."),
        ],
    ),
    "gaslighting": (
        "Mikä on gaslighting suomeksi?",
        "<strong>Gaslighting</strong> on suomeksi <strong>kaasuvalotus</strong>. "
        "Se tarkoittaa manipulaatiota, jossa toisen havainnot ja muisti "
        "kiistetään järjestelmällisesti, kunnes hän alkaa epäillä omaa "
        "arvostelukykyään. Nimi tulee näytelmästä "
        "<cite>Gas Light</cite> (1938), jossa aviomies himmentää "
        "kaasuvaloja ja kiistää vaimonsa havainnon.",
        [
            ("Mitä gaslighting tarkoittaa?",
             "Gaslighting eli kaasuvalotus tarkoittaa psykologista "
             "manipulaatiota, jossa toisen ihmisen havaintoja ja muistikuvia "
             "kyseenalaistetaan niin johdonmukaisesti, että hän lakkaa "
             "luottamasta omaan arviointikykyynsä. Yksittäinen kiistäminen "
             "ei ole gaslightingia — olennaista on toistuvuus."),
            ("Miten gaslightingin tunnistaa?",
             "Tavallisin merkki on oman muistin jatkuva epäily yhden ihmisen "
             "seurassa: joudut perustelemaan itsellesi, tapahtuiko jokin "
             "asia. Kirjaa havainnot ylös silloin kun ne tapahtuvat ja "
             "tarkista tulkintasi ulkopuolisella. Kirjattu havainto ei "
             "taivu jälkikäteen."),
        ],
    ),
    "hanlonin-partaveitsi": (
        "Mitä Hanlonin partaveitsi tarkoittaa?",
        "<strong>Hanlonin partaveitsi</strong> on nyrkkisääntö: "
        "<em>\"älä koskaan oleta pahantahtoisuutta siellä, missä tyhmyys "
        "riittää selitykseksi.\"</em> Se ei väitä, ettei pahantahtoisuutta "
        "olisi — se sanoo, että huolimattomuus on tavallisempaa ja olettaa "
        "vähemmän. Sääntö julkaistiin Robert J. Hanlonin nimissä vuonna 1980.",
        [
            ("Mitä Hanlonin partaveitsi tarkoittaa?",
             "Hanlonin partaveitsi neuvoo selittämään toisen ikävän toiminnan "
             "ensisijaisesti huolimattomuudella, kiireellä tai "
             "ymmärtämättömyydellä eikä pahalla tahdolla. Pahantahtoisuus "
             "vaatii motiivin, suunnittelun ja usein salailun; "
             "huolimattomuus ei vaadi mitään niistä."),
            ("Milloin Hanlonin partaveitsi ei päde?",
             "Sääntö on nyrkkisääntö, ei laki. Kun sama \"vahinko\" toistuu "
             "ja hyötyy johdonmukaisesti samasta osapuolesta, selitys ei "
             "enää ole huolimattomuus. Partaveitsi on lähtöoletus, jonka "
             "todisteet voivat kumota — ei syy jättää kuvio huomaamatta."),
        ],
    ),
    "peterin-periaate": (
        "Mitä Peterin periaate tarkoittaa?",
        "<strong>Peterin periaate</strong> kuuluu: <em>\"hierarkiassa jokainen "
        "työntekijä pyrkii ylenemään epäpätevyytensä tasolle.\"</em> Ylennys "
        "myönnetään nykyisessä työssä onnistumisesta, vaikka uusi tehtävä "
        "vaatii eri taitoja. Ylennykset loppuvat siihen tehtävään, jossa "
        "onnistuminen lakkaa — ja sinne jäädään.",
        [
            ("Mitä Peterin periaate tarkoittaa?",
             "Peterin periaate tarkoittaa, että hyvästä suoriutumisesta "
             "palkitaan ylennyksellä, kunnes vastaan tulee tehtävä, johon "
             "osaaminen ei riitä. Koska ylennys perustuu edellisen tehtävän "
             "tuloksiin eikä seuraavan vaatimuksiin, järjestelmä siirtää "
             "ihmisiä ennustettavasti liian pitkälle."),
            ("Miten Peterin periaatteen vaikutusta voi välttää?",
             "Erota urapolut johtamisesta: asiantuntijan on voitava edetä "
             "palkassa ja arvostuksessa ilman esihenkilötehtävää. Arvioi "
             "ylennyksessä seuraavan tehtävän taitoja, älä edellisen "
             "tuloksia, ja tee paluu entiseen rooliin mahdolliseksi ilman "
             "leimaa epäonnistumisesta."),
        ],
    ),
    "honeypot-huijaus": (
        "Mikä on honeypot suomeksi?",
        "<strong>Honeypot</strong> on suomeksi <strong>hunajapurkki</strong>. "
        "Huijauksena se tarkoittaa ansaa, joka houkuttelee uhrin sisään "
        "näennäisen helpolla voitolla ja sulkee uloskäynnin vasta kun uhri "
        "on jo sitoutunut. Olennaista ei ole houkutin vaan se, ettei "
        "poispääsy ole enää uhrin päätettävissä.",
        [
            ("Mitä honeypot-huijaus tarkoittaa?",
             "Honeypot-huijauksessa uhri houkutellaan mukaan lupauksella "
             "helposta hyödystä — voitosta, suhteesta tai sijoituksesta — "
             "ja ansa sulkeutuu vasta kun hän on antanut rahaa, tietoja tai "
             "jotain, jolla häntä voi painostaa. Houkutin on aito vain "
             "sisäänpääsyyn asti."),
            ("Miten honeypot-ansan tunnistaa?",
             "Varoitusmerkki on epäsuhta: tarjottu hyöty on selvästi "
             "suurempi kuin pyydetty vastine, ja kiire perustellaan "
             "tilaisuuden ainutkertaisuudella. Testaa aina poispääsy ennen "
             "sitoutumista — kysy, miten järjestelystä irtaudutaan. "
             "Vastauksen epämääräisyys on itsessään vastaus."),
        ],
    ),
    "doomscrolling": (
        "Mikä on doomscrolling suomeksi?",
        "<strong>Doomscrollingille ei ole vakiintunutta suomennosta.</strong> "
        "Käytössä ovat <em>kurjuusselaus</em>, <em>tuomioselailu</em> ja "
        "<em>huolisurffailu</em>. Sana tarkoittaa pakonomaista huonojen "
        "uutisten selaamista, joka jatkuu senkin jälkeen, kun se alkaa "
        "tuntua pahalta — sormi vetää syötettä yhä alaspäin.",
        [
            ("Mitä doomscrolling tarkoittaa?",
             "Doomscrolling tarkoittaa ahdistavan sisällön pakonomaista "
             "selaamista, joka ei lopu vaikka olo huononee. Aivot etsivät "
             "uhkatietoa turvallisuuden tunteen vuoksi, mutta syöte ei "
             "koskaan lopu, joten päätepistettä ei tule ja selaaminen "
             "jatkuu itseään ruokkien."),
            ("Miten doomscrollingin voi katkaista?",
             "Poista päätepisteettömyys: aseta selaamiselle kellotettu raja, "
             "siirrä puhelin pois makuuhuoneesta ja korvaa loputon syöte "
             "lähteellä, jolla on loppu — lehti, uutiskirje tai kerran "
             "päivässä luettava sivu. Kyse on rakenteesta, ei tahdonvoimasta."),
        ],
    ),
    "kaarmeoljy": (
        "Mikä on snake oil suomeksi?",
        "<strong>Snake oil</strong> on suomeksi <strong>käärmeöljy</strong>. "
        "Se on yleisnimitys tuotteelle, jota myydään suurilla, "
        "todistamattomilla lupauksilla ja joka ei tee mitä lupaa. "
        "Tunnusmerkki on lupausten laajuus: mitä useampaa vaivaa tuote "
        "väittää parantavansa, sitä epätodennäköisemmin se hoitaa yhtäkään.",
        [
            ("Mitä käärmeöljy tarkoittaa?",
             "Käärmeöljy tarkoittaa tuotetta tai palvelua, joka myydään "
             "vaikuttavilla väitteillä ilman näyttöä. Nimitys juontuu "
             "1800-luvun Yhdysvaltain kiertokauppiaista, jotka myivät "
             "käärmeöljyksi kutsuttuja ihmerohtoja jokaiseen vaivaan "
             "samasta pullosta."),
            ("Miten käärmeöljyn tunnistaa?",
             "Kolme merkkiä: lupaus kattaa epätavallisen monta erillistä "
             "ongelmaa, näyttönä esitetään kokemuskertomuksia eikä "
             "vertailukoetta, ja kritiikkiin vastataan vetoamalla "
             "vaiettuun totuuteen. Kysy, mikä tulos osoittaisi tuotteen "
             "tehottomaksi — jos vastausta ei ole, väite ei ole testattava."),
        ],
    ),
    "streisand-ilmio": (
        "Mitä Streisand-ilmiö tarkoittaa?",
        "<strong>Streisand-ilmiö</strong> tarkoittaa, että yritys piilottaa, "
        "poistaa tai sensuroida tieto kääntyy itseään vastaan ja "
        "moninkertaistaa tiedon huomion. Nimi tulee vuodesta 2003, jolloin "
        "Barbra Streisand vaati kotitalonsa ilmakuvaa poistettavaksi — "
        "kuvaa oli ladattu siihen mennessä kuusi kertaa.",
        [
            ("Mitä Streisand-ilmiö tarkoittaa?",
             "Streisand-ilmiö tarkoittaa tilannetta, jossa tiedon "
             "poistoyritys tekee tiedosta uutisen ja levittää sitä "
             "moninkertaisesti alkuperäiseen verrattuna. Poistovaatimus "
             "kertoo, että asialla on merkitystä, ja tekee siitä "
             "kiinnostavan myös niille, joita se ei muuten koskisi."),
            ("Miten Streisand-ilmiön voi välttää?",
             "Arvioi ennen poistovaatimusta, kuinka moni on tiedon jo "
             "nähnyt ja mitä vaatimus kertoo ulospäin. Usein tehokkaampaa "
             "on vastata asiasisältöön kuin yrittää poistaa se: vastaus "
             "ei tuota uutta uutista, poistoyritys tuottaa."),
        ],
    ),
}

FAQ_SIJAINTI = re.compile(
    r'(<div class="ilmio"[^>]*>.*?<p class="ilmio-byline">.*?</p>\s*<p>.*?</p>)',
    re.S,
)


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
            {
                "@type": "Question",
                "name": k,
                "acceptedAnswer": {"@type": "Answer", "text": v},
            }
            for k, v in faq
        ],
    }


def kasittele(slug, tiedot, kuiva):
    polku = ROOT / f"{slug}.html"
    teksti = polku.read_text(encoding="utf-8")
    alkup = teksti
    kysymys, vastaus, faq = tiedot

    # 1. Näkyvä vastauslohko. Idempotenssi: vanha lohko poistetaan ensin.
    teksti = re.sub(
        r'\n<div class="infolaatikko ' + MERKKI + r'">.*?</div>',
        "", teksti, flags=re.S,
    )
    osuma = FAQ_SIJAINTI.search(teksti)
    if not osuma:
        return f"{slug}: VAROITUS — insertointikohtaa ei löytynyt", False
    teksti = teksti.replace(
        osuma.group(1), osuma.group(1) + lohko_html(kysymys, vastaus), 1
    )

    # 2. FAQPage-schema @graphiin. Idempotenssi: vanha FAQPage korvataan.
    def paivita_graph(m):
        data = json.loads(m.group(1))
        if "@graph" not in data:
            return m.group(0)
        data["@graph"] = [n for n in data["@graph"] if n.get("@type") != "FAQPage"]
        data["@graph"].append(faq_node(slug, faq))
        return (
            '<script type="application/ld+json">\n'
            + json.dumps(data, ensure_ascii=False, indent=2)
            + "\n</script>"
        )

    teksti = re.sub(
        r'<script type="application/ld\+json">\s*(\{.*?"@graph".*?\})\s*</script>',
        paivita_graph, teksti, count=1, flags=re.S,
    )

    # Mitta on merkkejä, ei sanoja. Suunnitelma sanoi 40-55 sanaa, mutta se
    # luku on johdettu englanninkielisestä ohjeistuksesta. Googlen featured
    # snippet katkeaa noin 300 merkkiin, ja suomen yhdyssanaisuuden takia
    # 40-55 suomen sanaa on ~380-450 merkkiä eli katkeaisi kesken. 240-300
    # merkkiä vastaa samaa snippet-mittaa kuin 40-55 sanaa englanniksi.
    plain = re.sub(r"<[^>]+>", "", vastaus)
    merkkeja, sanoja = len(plain), len(plain.split())
    varoitus = "  ← 240–300 merkin ulkopuolella" if not 240 <= merkkeja <= 300 else ""
    if not kuiva and teksti != alkup:
        polku.write_text(teksti, encoding="utf-8")
    return (
        f"{slug}: {merkkeja} merkkiä ({sanoja} sanaa), "
        f"{len(faq)} FAQ-kysymystä{varoitus}"
    ), True


def main():
    kuiva = "--kuivaharjoitus" in sys.argv
    if kuiva:
        print("KUIVAHARJOITUS — mitään ei kirjoiteta\n")
    ok = True
    for slug, tiedot in SIVUT.items():
        rivi, onnistui = kasittele(slug, tiedot, kuiva)
        print(rivi)
        ok = ok and onnistui
    print(f"\n{len(SIVUT)} sivua käsitelty.")
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
