# Luonnosten arviointi — hakuliikenne ja vaalihyöty

Laadittu 4.8.2026. Koskee tämän kansion 14 luonnossivua + kategoriasivua.
Ei julkaisupäätös, vaan priorisointipohja: mikä kannattaa julkaista ensin ja miksi.

> **Tila 5.8.2026 — kohdat 1 ja 2 aikataulusta on tehty.** Suurhanke-erä (4 sivua,
> numerot 54–57) ja media-erä (10 sivua + kategoria 13, numerot 118–127) on
> julkaistu; sivustolla on 127 ilmiötä ja 13 kategoriaa. Kansioon jää vaalierän
> 3 luonnosta (§ 4). Niiden numerot 8 / 97 / 114 ovat tämän julkaisun jäljiltä
> vanhentuneita — `lisaa_ilmiot.py` laskee oikeat numerot ajossa.

**Aikaikkuna:** seuraavat vaalit ovat eduskuntavaalit huhtikuussa 2027 (vaalipäivä
huhtikuun kolmas sunnuntai, ~18.4.2027). Kampanjahaku alkaa käytännössä
tammi–helmikuussa 2027. Sivu tarvitsee 6–12 kk noustakseen hakutuloksissa, joten
**takaraja julkaisulle on syksy 2026** — muuten sivu on olemassa mutta ei löydy
silloin kun sitä haetaan.

---

## 1. Yhteenveto: julkaisujärjestys

| # | Sivu | Haku | Vaalihyöty | Yhteensä |
|---|---|---|---|---|
| 1 | Strateginen aliarviointi | ★★★ | ★★★ | **kärki** |
| 2 | Uutiskynnys | ★★★ | ★★★ | **kärki** |
| 3 | Päätösperäinen todistelu | ★★☆ | ★★★ | **kärki** |
| 4 | Väärä tasapaino | ★★☆ | ★★★ | korkea |
| 5 | Läpi hinnalla millä hyvänsä | ★★★ | ★★☆ | korkea |
| 6 | Lukittu päätös | ★★☆ | ★★☆ | korkea |
| 7 | Vihamielisen median harha | ★☆☆ | ★★★ | korkea |
| 8 | Kehäraportointi | ★★☆ | ★★☆ | keski |
| 9 | Tiedotejournalismi | ★★☆ | ★★☆ | keski |
| 10 | Huonojen uutisten hautaaminen | ★☆☆ | ★★☆ | keski |
| 11 | Uutisautiomaa | ★★☆ | ★★☆ | keski |
| 12 | Gell-Mannin amnesia | ★★☆ | ★☆☆ | keski |
| 13 | Bränditurvallisuus | ★★☆ | ★☆☆ | matala |
| 14 | Pääsyjournalismi | ★☆☆ | ★★☆ | matala |

Suositus: **julkaise suurhanke-erä (4 sivua) ensin, media-erä (10 sivua +
kategoriasivu) heti perään syyskuussa 2026.** Perustelu alla.

---

## 2. Hakuliikenne

### Miksi suurhanke-erä on hakukoneessa vahvempi kuin media-erä

Neljä suurhankesivua sisältävät **nimettyjä hankkeita**: Länsimetro, Olkiluoto 3,
Apotti, Tampereen raitiotie. Näitä haetaan nimellä ja jatkuvasti — "länsimetro
kustannusarvio", "olkiluoto 3 kustannukset", "apotti epäonnistuminen". Entiteettihaku
on tasaista ja ympärivuotista, eikä se vaadi että lukija tuntee käsitteen etukäteen.
Sivu voi nousta pitkähäntähauilla, joissa kilpailijana on uutisarkisto ilman
selittävää kehystä.

Media-erän termeistä vain osa on hakutermejä. Käsitesivu löytyy vain jos joku hakee
käsitettä nimellä — tai jos sivu nousee kysymysmuotoisilla hauilla ("miksi tästä ei
uutisoida").

### Sivukohtainen arvio

**★★★ Vahva hakupotentiaali**

- **Uutiskynnys** — ainoa media-erän termi, joka on jo suomen kielessä vakiintunut ja
  jota haetaan sellaisenaan. Esiintyy medialukutaidon opetuksessa (yläkoulu, lukion
  ÄI) ja arkikielessä ("ei ylittänyt uutiskynnystä"). Kilpailu on ohutta: sanakirjamääritelmiä
  ja journalismin oppikirjalainauksia, ei yhtään kunnollista selittävää sivua.
  Tämä on koko erän paras yksittäinen hakuveto ja lisäksi kategorian ankkurisivu.
- **Strateginen aliarviointi / Läpi hinnalla millä hyvänsä** — kantavat mukanaan
  Olkiluoto 3:n ja Länsimetron hakuvolyymin. Flyvbjergin "rautainen laki" ja
  reference class forecasting tuovat myös englanninkielisiä hakuja suomenkieliseen
  osumaan, mikä on harvinaista.

**★★☆ Kohtalainen — kapea mutta kilpailuton**

- **Gell-Mannin amnesia** — nimetty käsite, jota haetaan täsmälleen nimellä. Volyymi
  pieni, mutta suomeksi ei ole yhtään kilpailevaa sivua → käytännössä varma
  ykkössija ja hyvä AI-sitaattikandidaatti (Crichton 2002 on siteerattava alkuperä).
  Myös erän jaettavin sivu: ilmiö tunnistetaan heti omakohtaisesti.
- **Kehäraportointi** — Wikipedian sitogeneesi-tapaus (Maurice Jarre 2009) on
  konkreettinen ja siteerattava. Haetaan enemmän englanniksi, mutta suomenkielinen
  selitys puuttuu kokonaan.
- **Tiedotejournalismi** — termi elää journalismin koulutuksessa; Cardiffin 60 %:n
  luku on juuri sellainen numero, jota lainataan eteenpäin.
- **Bränditurvallisuus** — poikkeus erässä: tämä on **markkinointialan hakutermi**
  eikä mediakritiikkitermi. Tuo eri yleisön (viestintä- ja markkinointiväki) ja
  siten linkkejä muualta kuin sivuston nykyisestä lukijakunnasta. Kaupallinen
  hakuintentio tarkoittaa myös kilpailua toimistojen sisältömarkkinoinnista.
- **Uutisautiomaa** — hyötyy siitä että paikallislehtien lakkautukset ovat toistuva
  uutisaihe; sivu voi nousta uutissyklin mukana.
- **Päätösperäinen todistelu / Lukittu päätös** — hakua tulee Apotin ja Länsimetron
  kautta, ei käsitteen nimellä. Käsitteet ovat suomeksi käytännössä nimeämättömiä,
  mikä on sekä riski (ei hakuvolyymia) että mahdollisuus (sivusto nimeää ne).

**★☆☆ Heikko suora haku**

- **Vihamielisen median harha** — hostile media effect on tutkimustermi, ei
  hakutermi. Sivun arvo on linkitys- ja vaalikäytössä, ei liikenteessä.
- **Pääsyjournalismi** — käsite on suomeksi tuntematon eikä sitä haeta. Sivu on
  perusteltu kategorian täydellisyyden takia, ei liikenteen.
- **Huonojen uutisten hautaaminen** — kukaan ei hae tätä nimellä, mutta ilmiö on
  erän tunnistettavin ja siihen viitataan reaaliajassa ("perjantai klo 16"). Tämän
  liikenne tulee sosiaalisesta jakamisesta ja sisäisistä linkeistä, ei Googlesta.

### Rakenteellinen huomio

Sivuston GSC-ongelma on tunnettu: näyttöjä tulee, klikkejä vain sijalta ≤5.
Tämä puoltaa **kilpailuttomia täsmätermejä** (Gell-Mannin amnesia, kehäraportointi,
uutisautiomaa) laajojen käsitteiden sijaan — sijalla 1 pienikin volyymi konvertoi,
sijalla 12 iso volyymi ei tuota mitään. Sama pätee uuteen kategoriasivuun:
"Media ja julkisuus" on liian yleinen kilpailtavaksi, joten sen arvo on
sisäisessä linkityksessä (joka on aiemmin toiminut) eikä omassa sijoituksessaan.

---

## 3. Vaalihyöty — mitä äänestäjä saa

Kysymys ei ole "kertooko sivu politiikasta", vaan: **antaako se lukijalle
työkalun, joka pysyy käytössä koko kampanjan yli.** Paras vaalisivu ei ota kantaa
yhteenkään puolueeseen — se antaa nimen sille, mitä kaikki puolueet tekevät.

### Kärki: kolme käsitettä, joilla on suurin vaikutus jos ne leviävät

**1. Strateginen aliarviointi (+ läpi hinnalla millä hyvänsä)**

Vaalikampanja on lista hankkeita ja niiden hintalappuja: sairaalat, ratahankkeet,
puolustushankinnat, sote-järjestelmät, tunnelit. Jokainen luku on annettu portilla,
ja portti palkitsee optimismin. Jos äänestäjä oppii yhden asian, tämän kannattaa olla
se: **kampanjassa esitetty kustannusarvio ei ole ennuste vaan hakemus.**

Vastakeino on lisäksi poikkeuksellisen konkreettinen ja poliittisesti neutraali —
vertailuluokkaan perustuva ennuste on kysymys, jonka voi esittää kenelle tahansa
ehdokkaalle: *mitä vastaavat jo toteutuneet hankkeet lopulta maksoivat?* Tämä on
sivuston koko valikoiman parhaiten yleistyvä vastakeino.

**2. Uutiskynnys**

Vaalikeskustelun agenda syntyy siitä, mikä ylittää kynnyksen. Hitaat ja
rakenteelliset kysymykset — hoitojonot, korjausvelka, ostovoiman rapautuminen,
lainvalmistelun vaiheet — eivät tapahdu minään päivänä eivätkä siksi pääse
agendalle, vaikka ne koskevat useampaa ihmistä kuin mikään kampanjan kohu.
Sivu antaa äänestäjälle kyvyn kysyä toisin päin: *mistä ei puhuta, ja johtuuko se
asian merkityksettömyydestä vai sen muodosta?*

Toinen puoli on yhtä tärkeä ja sivulla jo kirjoitettuna: kynnyksen tunteva viestijä
osaa **rakentaa asialleen tapahtuman**. Kampanja-aika on täynnä juuri tätä —
julkistus, kannanotto, avaus, vuosipäivä. Kun lukija tunnistaa tekniikan, kohu
lakkaa näyttämästä uutiselta.

**3. Väärä tasapaino**

Vaalitentti on formaattina väärän tasapainon tuotantokone: kaksi kantaa, sama
puheaika, katsoja päättelee muodosta että asia on 50–50. Sivun tärkein erottelu on
juuri se, jota vaalikeskustelussa käytännössä koskaan ei tehdä: **näyttökysymys vs.
arvokysymys.** Arvokysymyksessä kahden kannan esittäminen on oikein — se *on*
politiikkaa. Näyttökysymyksessä se on harhaanjohtavaa. Sekaannus näiden välillä on
yksi tehokkaimmista kampanjatekniikoista, ja sen purkaminen ei suosi ketään.

### Vahva tukikerros

**4. Vihamielisen median harha.** "Media on meitä vastaan" on vakiintunut
mobilisointikeino kaikilla laidoilla, ja Vallone–Ross–Lepper (1985) osoittaa, että
kokemus syntyy myös silloin kun juttu on tasapainoinen. Tämä on erän ainoa sivu,
joka puhuttelee molempia osapuolia samalla lauseella: *oma kokemus puolueellisuudesta
ei ole luotettava mittari sen olemassaolosta.* Hakuliikennettä ei tule, mutta
polarisaation kannalta tämä on erän arvokkain sivu — ja juuri siksi se kannattaa
julkaista vaikka luvut eivät sitä puolla.

**5. Päätösperäinen todistelu.** "Selvitys osoittaa" on kampanjaretoriikan vakiofraasi.
Sivun kolme kysymystä (kuka tilasi, mikä rajattiin pois, montako selvitystä samasta
asiasta on tehty) toimivat sellaisenaan vaalikeskustelun aikana.

**6. Kehäraportointi.** Kampanja-aikana väite kiertää nopeammin kuin sen alkuperä.
Sivu antaa faktantarkistuksen yksinkertaisimman säännön: *jos "useiden lähteiden
mukaan" -jutut ovat parin päivän sisällä, lähteitä on yksi.* Pariutuu jo julkaistun
[Brandolinin lain](../brandolinin-laki.html) kanssa.

**7. Tiedotejournalismi.** Puolueiden ja etujärjestöjen tiedotteet menevät
kampanja-aikana läpi juuri siksi, että toimituksilla ei ole aikaa. Vastakeino
(kopioi virke hakukoneeseen lainausmerkeissä) on niin helppo, että sen voi tehdä
puhelimella kesken lukemisen.

**8. Huonojen uutisten hautaaminen.** Vaalikalenteri tekee tästä ajankohtaisen
kahdesti: ikävät päätökset siirtyvät kampanjan yli, ja epäsuositut ratkaisut
julkaistaan heti vaalien jälkeen. Sivu antaa syyn katsoa **tiedotteen kellonaikaa**
ennen sen sisältöä.

**9. Uutisautiomaa.** Tutkimushavainto siitä, että paikallisuutisoinnin katoaminen
**valtakunnallistaa puoluepolitiikan**, on suoraan eduskuntavaaleja koskeva: kun
paikallista ei uutisoida, äänestäjä äänestää valtakunnan kehyksillä. Tämä on
harvinaisen hyvin dokumentoitu (Gao, Lee & Murphy 2020) ja Suomessa vähän puhuttu.

**10. Lukittu päätös.** Enemmän hallitusohjelman kuin kampanjan ilmiö — mutta juuri
siksi ajankohtainen heti vaalien jälkeen: hallitusohjelman rivi *on* se todellinen
päätös, jota myöhempi muodollinen käsittely vain vahvistaa. Sivu kannattaa
julkaista ennen vaaleja, mutta sen käyttöhetki on niiden jälkeen.

### Vähäisempi vaalihyöty

- **Gell-Mannin amnesia** — henkilökohtainen lukutaitohavainto, ei poliittinen
  työkalu. Erinomainen sivu, mutta ei vaalisyistä.
- **Pääsyjournalismi** — vaikuttaa kampanjahaastatteluihin (kysymykset sovitaan
  ennakolta, jatkokysymystä ei ole), mutta yleisö ei voi tehdä havainnolle mitään
  paitsi huomata sen.
- **Bränditurvallisuus** — mainosrahan logiikka; kiinnostava, mutta äänestäjän
  näkökulmasta etäinen.

---

## 4. Vaalierä — kolme lisäsivua (luonnostettu 4.8.2026)

Alkuperäiset 14 luonnosta kattoivat **julkisuuden ja suurhankkeet**, mutta eivät
vaalitilannetta itseään. Aukko on nyt täytetty kolmella luonnoksella. Ne eivät
muodosta omaa kategoriaa vaan sijoittuvat kolmeen nykyiseen — yhteys tehdään
koostesivulla, ei kategoriarakenteella.

1. **[Vaalilupauksen hinnoittelu](vaalilupauksen-hinnoittelu.html)** · Vallan rakenteet, nro 8 —
   miksi kampanjassa esitetty luku ei ole sama kuin toteutunut luku. Ero
   strategiseen aliarviointiin on portti: hankearvio joutuu edes muodollisesti
   tarkasteltavaksi, lupaus ei joudu minnekään. Kolme valinnanvaraa: aikajänne,
   brutto/netto, dynaamiset vaikutukset.
2. **[Vaalikone-efekti](vaalikone-efekti.html)** · Alustatalous ja algoritmit, nro 97 —
   kysymysvalinta tuottaa vastausavaruuden ja laskukaava tuottaa prosentin.
   Suomessa poikkeuksellisen relevantti (Yle avasi ensimmäisen verkkovaalikoneen
   1996, käyttöaste on kansainvälisesti korkea) eikä aiheesta ole suomeksi
   selittävää sivua. Erän suurin käyttämätön hakumahdollisuus.
3. **[Kannatusmittausten virhemarginaali](kannatusmittausten-virhemarginaali.html)** ·
   Tilastoilla valehtelu, nro 114 — eron marginaali on noin kaksinkertainen
   yksittäisen luvun marginaaliin nähden, joten useimmat "ohitukset" ovat otsikoita
   ilman havaintoa. Naapureina jo julkaistut
   [kaksois-y-akseli](../kaksois-y-akseli.html) ja
   [cherry picking](../cherry-picking-aikavali.html).

Numerot ovat alustavia: kaikki kolme sijoittuvat nykyisten kategorioiden **sisään**,
joten julkaisu siirtää niitä seuraavia numeroita eteenpäin. `lisaa_ilmiot.py` hoitaa
renumeroinnin.

### Avoin idea: vaalipaketit

Kolme uutta sivua eivät yksin tee sivustosta vaalikäyttöistä — jo julkaistussa
113 ilmiössä on iso määrä vaalimateriaalia, joka ei löydy kategoriajaosta.
Idea (ei vielä suunniteltu): **useita teemapaketteja**, jotka poimivat ilmiöitä
kategorioiden yli — esimerkiksi *lue vaalikeskustelua*, *lue vaalilupausta*,
*lue gallupia*, *lue ehdokasta*. Sama ilmiö voi esiintyä useassa paketissa.
Tämä on navigointi- ja jakamiskerros, ei uusi sisältö, joten se on halpa
toteuttaa ja helppo julkaista erillään ilmiösivuista. Suunnitellaan erikseen.

> **Suunniteltu 5.8.2026:** koostesivun sisältösuunnitelma on omassa
> tiedostossaan — `VAALIKESKUSTELU-LUKUOHJE-PLAN.md`. Ratkaisu: itsenäinen
> opas (~1400–1800 sanaa), joka jäsentyy vaalikeskustelun kulun mukaan
> kahdeksaan lukuun, ei linkkilista. Sivu imee myös paketti-ideat *lue
> vaalilupausta* ja *lue gallupia*.

Ensimmäisenä askeleena kannattaa harkita **koostesivua** (ei uusi ilmiö vaan navigointisivu):
*"Vaalikeskustelun lukuohje"* — kokoaa jo julkaistut ([Overton-ikkuna](../overton-ikkuna.html),
[astroturf](../astroturf.html), [firehose of falsehood](../firehose-of-falsehood.html),
[kuollut kissa](../kuollut-kissa.html), [maalitolppien siirtäminen](../maalitolppien-siirtaminen.html),
[cherry picking](../cherry-picking-aikavali.html)) ja uudet media-sivut yhdeksi
listaksi. Tällainen sivu voi nousta kausiluonteisilla hauilla
("vaalikeskustelu", "medialukutaito vaalit", "vaalilupaus") ja on jaettavuudeltaan
ylivoimainen yksittäisiin ilmiösivuihin nähden. Ajoitus: julkaistavaksi
**joulukuussa 2026**, jotta se on indeksoitu kampanjan alkaessa.

---

## 5. Julkaisuaikataulu

| Aika | Toimenpide | Peruste |
|---|---|---|
| Elo–syys 2026 | Suurhanke-erä (4 sivua) juureen | Entiteettihaku nousee nopeimmin; ei vaadi uutta kategoriaa |
| Syys 2026 | Media-erä (10 sivua) + kategoria 13 | Kategoriasivu vaatii 12 nykyisen laskurin päivityksen x/13 — tehdään kerralla |
| Loka–marras 2026 | Vaalierän 3 sivua (luonnokset valmiit 4.8.2026) | Ehtivät indeksoitua |
| Joulu 2026 | Vaalipaketit / lukuohje-koostesivu | Valmiina kun kampanjahaku alkaa |
| Tammi 2027 | Ei uutta — sisäisen linkityksen viilaus | Sisäinen linkitys on aiemmin nostanut sijoituksia; uusi sivu ei ehdi enää nousta |

Julkaisun tekninen tarkistuslista on `luonnokset-media/index.html`:ssä.
