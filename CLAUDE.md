# Ilmiöitä — www.ilmiöt.fi

Suomenkielinen tietopankki: 165 yhteiskunnallista ilmiötä, 15 aihepiiriä. Staattinen
HTML, ei build-vaihetta — jokainen sivu on itsenäinen tiedosto repon juuressa. Osa
tiedostoista on kuitenkin **generoituja**, eikä niitä muokata käsin (ks. alla).

## Muutosloki — kaksi tiedostoa, eri yleisö

Muutoksista pidetään kirjaa kahdessa paikassa. Ne eivät ole kopioita toisistaan:

| Tiedosto | Yleisö | Sisältö |
|---|---|---|
| `MUUTOSLOKI.md` | tekijä ja tulevat sessiot | tekninen totuus: skriptinimet, sivumäärät, mitä ja miksi |
| `muutokset.html` | sivuston lukija | mitä lukijalle näkyy: uudet ilmiöt, parannukset, yksityisyys |

`muutokset.html` on **käsin kirjoitettu sivu, ei generoitu** `MUUTOSLOKI.md`:stä.
Syy: lukijaa ei kiinnosta `robots.txt`:n punycode-rivi tai CSS:n cache-bust, ja
suurin osa teknisistä merkinnöistä kääntyy lukijan kielelle vasta tulkittuna. Älä
siis kirjoita skriptiä, joka muuntaa MUUTOSLOKI.md:n HTML:ksi — se tuottaisi
sivun, jota kukaan ei lue.

### Kun sivustolle tehdään muutos, joka näkyy lukijalle

Lukijalle näkyviä ovat: uudet tai poistetut ilmiöt, uudet aihepiirit, sisällön
laajennukset (esim. vastakeino-osiot) ja navigoinnin muutokset. **Tekniset
muutokset eivät kuulu `muutokset.html`:ään** — eivät SEO-viilaukset, eivät
sitemap-päivitykset, ei cache-bust, eikä myöskään infrastruktuuri kuten
itsehostatut fontit. Nekin kuuluvat `MUUTOSLOKI.md`:hen, mutta lukijan sivulla
ne luetaan teknisenä selittelynä. Kysy: *mitä lukija saa?* Jos vastaus on
"ei mitään uutta luettavaa", merkintä jää pois.

1. **`MUUTOSLOKI.md`** — uusi osio tiedoston alkuun (uusin ensin), otsikko
   `## P.K.VVVV — mitä tehtiin`. Tekninen tarkkuus, skriptinimet mukaan.
2. **`muutokset.html`** — uusi `<article class="muutos">` `.loki`-divin **alkuun**
   (uusin ensin). Rakenne on kiinteä:
   ```html
   <article class="muutos">
     <span class="muutos-pvm">28.7.2026</span>
     <h3>Otsikko lukijan kielellä</h3>
     <p>Kaksi–neljä virkettä. Linkitä uudet ilmiösivut suoraan.</p>
   </article>
   ```
   Kirjoita siitä, *mitä lukija saa*, ei siitä mitä tiedostoja muutettiin.
3. **`muutokset.html`:n JSON-LD** — `"dateModified"` uuteen päivään.
4. **`index.html`** — kaksi kohtaa samalle päivälle:
   - headerin nappi: `<a class="paivitetty-btn" href="muutokset.html">Päivitetty
     P.K.VVVV ›</a>`
   - JSON-LD `CollectionPage` → `"dateModified"`
   Nämä ovat samat kaksi päivämäärää; jos ne eroavat, sitemapin `lastmod` menee
   pieleen (se lukee JSON-LD:n, ei näkyvää tekstiä).
5. **`python3 scripts/build_sitemap.py`** — poimii `lastmod`-arvot sivujen
   JSON-LD:stä. Aja aina vasta kohtien 3–4 jälkeen.

Etusivun nappi on ainoa sisääntulo sivulle headerissa; lisäksi linkki on
`index.html`:n ja `tietoa.html`:n footerissa. Jos header rakennetaan uusiksi,
nappi on säilytettävä — muuten sivu jää orvoksi.

## Generoidut tiedostot — älä muokkaa käsin

| Tiedosto | Generoi | Milloin ajetaan |
|---|---|---|
| `sitemap.xml` | `scripts/build_sitemap.py` | aina kun sivuja lisätään/poistetaan tai `dateModified` muuttuu |
| `search-index.js` | `scripts/build_search_index.py` | sisältömuutosten jälkeen |
| `llms.txt` (ilmiölista) | `scripts/paivita_maarat.py` | ilmiömäärän muuttuessa |
| `kategoria-*.html` | `scripts/build_kategoriat.py` | kun `kategoriat/*.md` muuttuu |
| `data/suosio.js` | `scripts/paivita_suosio.py` | yöllä cronista |
| `luonnokset/suosio.html` | `scripts/paivita_suosio.py` | samalla ajolla |
| `luonnokset/etusivu-nostot.html` | `scripts/paivita_suosio.py` | samalla ajolla |
| `data/peli-pankki.js` | `scripts/build_peli.py` | kun `pelidata/*.json` muuttuu |
| `og/<slug>.png`, `og/kategoria-<slug>.png` | `scripts/build_og.py` | kun etusivun kortin nimi tai kuvaus muuttuu |

`llms.txt`:n **otsikkolohko** (rivit 1–10) on käsin ylläpidetty; vain
ilmiölista synkronoituu skriptillä.

Kaksi skriptiä ei generoi tiedostoa vaan **johtaa osan ilmiösivusta muusta
sisällöstä**, ja ne ajetaan julkaisun jälkeen (`lisaa_ilmiot.py` tulostaa ne
ajolistaan) sekä aina kun lähde muuttuu:

- `scripts/seo_rakenne.py --kirjoita` — `id` jokaiselle `.ilmio`-säiliön `h2`:lle
  ja `<main>`. Olemassa olevaa `id`:tä ei muuteta. `.ilmio`-säiliö pysyy
  `<div>`:nä: luonnosskriptit tunnistavat sen tagista.
- `scripts/seo_schema.py --kirjoita` — JSON-LD:n `description` metakuvauksesta,
  `image` `og:image`sta, `about` kortin nimestä; poistaa FAQPagen. Aja, kun
  metakuvaus, kortin nimi tai jakokuva muuttuu. JSON-LD:tä ei muokata käsin
  näiltä osin.

Kategorian ilmiömäärää ei kirjoiteta `kategoriat/*.md`:n `h1`-, `otsikko`- tai
`kuvaus`-kenttään numerona: käytä `{n}` (ja `{n-1}`). `build_kategoriat.py`
täyttää ne korttimäärästä ja kaatuu, jos kentässä on `-toista`-lukusana, joka ei
vastaa määrää.

`lisaa_ilmiot.py` kaatuu, jos luonnoksen `<title>` on jo käytössä toisella
sivulla tai ei sisällä h1:n ensimmäistä sanaa — 26 sivua julkaistiin pohjasivun
titlellä ennen tätä tarkistusta.

Sivukohtaisia jakokuvia on toistaiseksi vain 20 sivulla (kategoria 15 ja kaksi
muuta, 3.10.2026); muut käyttävät `og/brand.png`:tä. `build_og.py --kirjoita`
vaihtaa myös ilmiösivun kolme `og:`-metariviä, joten **kuvat viedään palvelimelle
ennen HTML-sivuja** — muuten `og:image` osoittaa 404:ään. Kuvassa ei ole ilmiön
numeroa, koska uudelleennumerointi vanhentaisi sen.

## Suosiodata ja etusivun nostot

`scripts/paivita_suosio.py` hakee liikennekannasta luetuimmat sivut ja valitsee
viikon ilmiön. Kolme sääntöä:

1. **Yöajo ei kirjoita `index.html`:ään.** Suosiodata elää erillisessä
   `data/suosio.js`:ssä, jonka etusivu lataa `defer`-skriptinä ja joka on ainoa
   yöllä palvelimelle siirtyvä tiedosto. Jos data kirjoitettaisiin HTML:ään,
   joka yö työnnettäisiin 300 kt etusivu, joka voi ylikirjoittaa käsin tehtyjä
   muutoksia — se on tämän projektin dokumentoitu pahin vikatila.
2. **`data/suosio.js` sisältää vain slugit ja luvut.** Otsikot, kuvaukset ja
   värit haetaan selaimessa sivun omista `.hub-kortti`-elementeistä. Älä lisää
   niitä datatiedostoon: kaksi listaa ajautuisi erilleen.
3. **Nostokortit eivät käytä luokkaa `hub-kortti`.** Etusivun haku,
   nuolinäppäinnavigaatio ja `randomIlmio()` keräävät kaikki `.hub-kortti`-
   elementit, joten duplikaatti näkyisi hakutuloksissa kahdesti.

Nostolohkot injektoidaan `NOSTOT-ALKU`/`NOSTOT-LOPPU`-merkkien väliin; ajo on
idempotentti ja poistaa edellisen injektion ensin. Oletuksena kohde on
`luonnokset/etusivu-nostot.html`, `--tuotanto` kirjoittaa `index.html`:ään.
Tunnukset ja kannan osoite ovat gitignoratussa `.suosio.env`:ssä
(ks. `.suosio.env.malli`) — eivät koskaan versionhallintaan.

**Yöajo asuu NAS:illa, ei työasemalla** (15.8.2026 alkaen). Työaseman cron on
kommentoitu pois; WSL:n cron ajaa vain kun WSL on käynnissä, ja kolme väliin
jäänyttä yötä piilottaa lohkot etusivulta tuoreustarkistuksen takia. Pystytys
`scripts/nas_asennus.sh`:lla, joka on idempotentti ja jossa on `--tarkista`-tila.
NAS tekee `git pull` ennen jokaista ajoa: skripti lukee ilmiölistan
`index.html`:stä ja julkaisupäivät sivujen JSON-LD:stä, joten vanhentunut kopio
jättäisi uudet ilmiöt pois listoilta. Kaksi asiaa ei ole versionhallinnassa
eikä generoitavissa, joten ne on kopioitava koneelta toiselle käsin:
`.suosio.env` ja `data/.viikko-historia.json`.

Vain yksi kone saa ajaa `--laheta`:n. Ilman sitä ajavia koneita voi olla monta —
ne kirjoittavat vain omia paikallisia tiedostojaan — mutta kaksi lähettäjää
tarkoittaisi kahta eri viikon ilmiötä samalla sivustolla.

Viisi lohkoa: **viikon ilmiö** (nousija, valitaan maanantaisin), **satunnainen
ilmiö** (lähde on sivun oma korttilista, toimii ilman dataa), **luetuimmat**
(sivunäytöt), **googlatuimmat** (Google-näytöt) ja **eniten kasvua**
(7 pv vs. edellinen 7 pv). Luetuimmat ja googlatuimmat ovat eri asioita eivätkä
saman asian kaksi esitystä: luettu = joku avasi sivun, googlattu = sivu näkyi
hakutuloksissa. Sivu jolla on paljon näyttöjä ja vähän lukukertoja on title- tai
kuvausongelma, ei sisältöongelma — dashboardin "Näkyvyys ilman klikkejä" listaa
ne suoraan.

"Eniten kasvua" käyttää matalampaa lattiaa (`KASVU_LATTIA` 5) kuin viikon ilmiö
(`VIIKKO_LATTIA` 10) ja jättää viikon ilmiön pois listalta, joten lohkot eivät
näytä samaa korttia kahdesti. Prosentti on molemmissa sama tasoitettu suhde
(nyt+5)/(ennen+5) — jos toinen laskisi raa'an suhteen, sama sivu saisi kaksi eri
lukua samalla sivulla. Lohko vaatii vähintään kolme riviä tai piiloutuu.

Kasvulohkolla on 7 pv:n ja 30 pv:n välilehdet (`k7`, `k30`); sivunäyttökysely
haetaan siksi 60 päivältä, ei 30:ltä. Kanta alkaa 1.7.2026, joten edellinen
30 pv on toistaiseksi vain osittain katettu: vertailuluku **skaalataan
päivätahdiksi** (`ikkunan pituus / katetut päivät`) ja saate kertoo sen
"(osin arvioitu)". Skaalaus pienentää kasvuprosenttia, ei kasvata, eikä se voi
keksiä kasvua jota ei ole. Kerroin menee itsestään ykköseen kun kate on täysi.

**Kasvulistat ja viikon ilmiö suodattavat julkaisupäivän mukaan**
(`ehti_mukaan()`): sivun on oltava julkaistu ennen vertailujakson alkua. Ilman
tätä listat täyttyvät vastajulkaistuista sivuista, jotka eivät kasvaneet vaan
ilmestyivät — uusi sivu on aina "kasvanut nollasta". Älä poista suodatinta
vaikka lista lyhenisi; lyhyt tosi lista on parempi kuin pitkä valheellinen.

Välilehdet piiloutuvat automaattisesti — `rakennaLista()` piilottaa minkä
tahansa välilehden jonka takana ei ole **vähintään `minRivit` riviä** (kasvulla
3, muilla 1) ja koko palkin jos vain yksi jää jäljelle. Oletusikkunaksi
valitaan ensimmäinen joka yltää kynnykseen, ja lohko näkyy jos yksikin yltää.
Älä siis "korjaa" puuttuvaa välilehteä; se ilmestyy itse.

Kynnys koskee **jokaista välilehteä erikseen**, ei vain oletusikkunaa. Jos se
katsoisi vain oletusta, kahden rivin `k7` piilottaisi myös kuuden rivin `k30`:n
— näin kävi 16.8.2026.

Kannan sudenkuopat, jotka on jo hoidettu kyselyssä ja jotka on syytä muistaa
jos kyselyä muokataan: ilmiöt.fi on kannassa **kahtena** `sivusto_avain`-arvona
(rajaa `sivusto_ryhma`, ei avainta), `http_status` sisältää runsaasti
301-ohjauksia jotka eivät ole sivunäyttöjä, eikä faktataulussa ole bottilippua
— ryömijät suodatetaan sillä, montako eri sivua sama kävijä avaa yhdessä
päivässä.

Ilmiöiden numerointia ei koskaan korjata käsin: `scripts/lisaa_ilmiot.py` ja
`scripts/poista_ilmio.py` numeroivat koko sivuston uudelleen ja päivittävät
IDS-taulukot, PREV/NEXT-ketjun ja selausnapit. Molemmat ovat kuivaharjoituksia
oletuksena, kirjoitus `--kirjoita`-lipulla.

## Vedätys — päivittäinen peli (`peli.html`)

Ensimmäinen sivu, joka **käyttää** ilmiösivuja sen sijaan että olisi yksi niistä
lisää. Sisältö tulee `pelidata/*.json`:ista, jotka `scripts/build_peli.py`
validoi ja kääntää tiedostoksi `data/peli-pankki.js`. Viisi sääntöä, joita ei
saa rikkoa:

1. **Päivän erä on kaikille sama.** Erät kootaan käännösaikana, ei selaimessa.
   Ilman tätä tulosten vertailu ja jakaminen menettää merkityksensä — ja se on
   ainoa syy, jonka takia kukaan kertoo pelistä eteenpäin.
2. **Jokaisessa erässä on 1–2 rehellistä kohtaa, ja väärä hälytys maksaa saman
   kuin ohitus.** Tämä ei ole tasapainotusta vaan korjaus Bad News -pelin
   replikaatiokritiikkiin (Modirrousta-Galian & Higham 2023): pelkkä epäilyn
   lisääminen siirtää vastetaipumusta eikä paranna erottelukykyä, eli opettaa
   kyynisyyttä. `--tarkista` kaatuu jos rehellisiä on alle 25 % pankista.
   Samasta syystä turha 🚩-liputus ei maksa pisteitä.
3. **Peli manipuloi pelaajaa opetuksessa, ei koskaan retentiossa.** Ansat
   (tekaistu ajastin, keksitty sosiaalinen todiste, esivalittu oletus,
   syyllistävä nappi) ovat sallittuja ja paljastetaan erän lopussa. Ilmoitukset,
   putkiahdistus, pakotettu jakaminen ja ostettavat armonpäivät eivät ole.
   Raja lukee pelin säännöissä ääneen — se on osa tuotetta, ei sisäinen ohje.
   Älä myöskään keksi lukuja: sivu ei mittaa mitään, joten se ei myöskään
   väitä mittaavansa.
4. **Ydinvalinta on vinouma vai taktiikka**, ei "mikä näistä 139 ilmiöstä".
   Peruste on `kategoriat/psykologia-ja-kognitio.md` riveillä 17–21. Nimeäminen
   on erillinen toinen vaihe, koska ihminen voi selvitä tilanteesta oikein
   tunnistamatta tekniikkaa — ja nimeäminen on se osa, joka yleistyy.
   Valinta on aito vain, jos kumpikin voi olla oikea vastaus samassa
   kanavassa: `--tarkista` kaatuu, jos vinoumia on alle 15 % pankista (vaiheessa
   1 niitä oli nolla, ja "Oma pää" oli aina väärin) tai jos `ajatus`-kanavassa
   ei ole myös pätevää päättelyä ja jonkun toisen tempun jälkiä. Säännöt ovat
   `pelidata/TYYLI.md`:ssä.
5. **Pelisivu ei ole ilmiö.** Ei numeroa, ei `const IDS`-taulukkoa, ei
   PREV/NEXT-ketjua, **eikä luokkaa `hub-kortti`**. Sitemapiin se vaatii oman
   vakion `scripts/build_sitemap.py`:hyn; hakuindeksiin sitä ei lisätä.

Päiväindeksi lasketaan epokista (epokki = Vedätys #1) **paikallisen**
keskiyön mukaan, ja `setHours(0,0,0,0)` ajetaan molemmille päiville. Ilman
jälkimmäistä kesäajan vaihtuminen siirtää indeksiä yhdellä. Epokki määritellään
**vain** `scripts/build_peli.py`:ssä; `peli.html` lukee sen datasta
(`P.epokki`), joten sitä ei kovakoodata sivulle. Selaimen talletus on sidottu
epokkiin (`peli-epokki`): kun epokki vaihtuu, tilastot, tulokset ja
kertaushistoria nollataan, koska vanhat päiväindeksit osoittaisivat vääriin
eriin. **Epokin muuttaminen julkaisun jälkeen nollaa siis jokaisen pelaajan
putken.**

**Tilastot ja tehoste kertyvät vain päivän omasta erästä, ja vain kerran.**
Arkistosta tai vanhasta haastelinkistä pelattu erä tallentaa tuloksensa
(`peli-tulokset`), mutta ei koske putkeen — ennen 3.10.2026 se siirsi
viimeisin-päivän taaksepäin ja nollasi putken. Erän ensimmäinen tulos jää
voimaan ja on se, joka jaetaan; uusintakierros ei korvaa sitä.

**Pankin kasvattaminen kokoaa kaikki erät uudelleen.** `kokoa_erat()` jakaa koko
pankin alusta, joten yksikin uusi kohta muuttaa myös jo pelattuja eriä: kokeessa
3.10.2026 (200 → 260 kohtaa) 0/40 erästä säilyi samana. Arkiston tulokset
(`peli-tulokset`) osoittaisivat silloin eri eriin kuin mitä pelattiin. Uudet
kohdat odottavat siksi `luonnokset/pelidata/`:ssa, kunnes on päätetty, lukitaanko
pelatut erät vai hyväksytäänkö uudelleenkokoaminen.

**Ohjaava ansa osoittaa aina väärään vastaukseen** (`ansanKohde()`). Esivalittu
oletus ja keksitty prosentti, jotka sattuvat osumaan oikeaan, palkitsevat
tottelemisen ja opettavat päinvastaista kuin paljastus sanoo.

**`data/peli-pankki.js` on defer-skripti, joten sitä ei saa lukea
moduulitasolla.** `peli.html`:n inline-skripti ajetaan jäsennyshetkellä, siis
*ennen* deferoitua datatiedostoa. Pankki luetaan `DOMContentLoaded`-
käsittelijässä, samoin kuin etusivu lukee `window.ILMIO_SUOSIO`:n
(`index.html:3059`). Tästä syntyi 23.8.2026 vika, jossa koko peli poistui
hiljaa eikä yhtään nappia kytketty; siksi puuttuva data näyttää nyt myös
näkyvän virheilmoituksen.

`node scripts/testaa_peli.js` pelaa erän läpi DOM-tyngällä ja on ajettava
jokaisen `peli.html`- tai pankkimuutoksen jälkeen. Tynkä ajaa inline-skriptin
ennen datatiedostoa nimenomaan siksi, että yllä kuvattu vika jäisi kiinni —
älä käännä järjestystä. `PELI_SIVU=<polku>` ajaa testin muuta kopiota vasten.

Uudet kohdat kirjoitetaan `pelidata/TYYLI.md`:n mukaan ja
`pelidata/_siemen/<slug>.md`:n pohjalta — siemenaineisto on louhittu
ilmiösivuilta (`scripts/build_peli_siemen.py`), jotta pelin ääni on sivuston
ääni. Rehelliset kohdat ovat pankin vaikeimmat: niiden on oltava uskottavan
epäilyttäviä mutta oikeasti kunnossa.

## Sivujen tyyli

- `index.html`, `tietoa.html` ja `muutokset.html` kantavat CSS:nsä `<style>`-lohkossa
  → ne ovat immuuneja `style.css`:n cache-bustille.
- Ilmiö- ja kategoriasivut linkittävät `style.css?v=YYYYMMDD`. Kun `style.css` tai
  `fonts/fonts.css` muuttuu: nosta `VERSIO` skriptissä `scripts/fontit_esilataus.py`
  ja `CSS_VERSIO` skriptissä `scripts/build_kategoriat.py` (sama arvo) ja aja
  molemmat. Älä vaihda versiota käsin sivu kerrallaan.
- **Sivu linkittää fontit vain yhdestä paikasta:** `style.css` (ilmiöt, kategoriat)
  tai `fonts/fonts.css` (index, tietoa, muutokset, peli). Sama `@font-face`-lohko
  on molemmissa tiedostoissa ja muutetaan aina yhdessä. Kaksi lähdettä samalla
  sivulla haki saman fontin kolmesti ja aiheutti mobiilissa CLS:n 0,2 (4.10.2026).
  Jokaisella sivulla on `<link rel="preload">` kahdelle ensimmäisen näkymän
  fontille; `fontit_esilataus.py` ylläpitää ne.
- Väripaletti: `--c-primary #C9A84C`, `--c-primary-dark #1C1400`,
  `--c-primary-mid #8B6914`, `--c-bg #F5F0E5`. Kirjasimet: Spectral (otsikot),
  Source Sans 3 (ilmiö- ja kategoriasivujen leipäteksti) ja DM Sans (etusivu,
  muut sivut ja käyttöliittymä), kaikki itsehostattuja `fonts/`-kansiossa.
- Sivusto ei lataa mitään ulkopuoliselta palvelimelta (27.7.2026 alkaen). Älä lisää
  CDN-linkkejä, Google Fontsia tai ulkoisia skriptejä.

## Sisältönormit

- Ilmiösivu on **~260 sanaa** (mediaani). Liian laaja aihe jaetaan useaksi ilmiöksi
  sen sijaan että yksi sivu kirjoitettaisiin pitkäksi.
- Nimeämisessä suositaan vakiintunutta lainasanaa (*shrinkflaatio*, *rage bait*)
  keksityn suomennoksen sijaan. Englanninkielinen alkuperäistermi kuuluu ingressiin.
- Jokainen ilmiösivu päättyy osioon **Tunnistaminen ja vastakeinot**. Etusivu lupaa
  tämän jokaisesta artikkelista — lupauksen on pidettävä.
- Uudet sivut kirjoitetaan ensin luonnoksiksi `luonnokset/`-kansioon (kaikki erät
  samassa kansiossa 14.8.2026 alkaen) ja julkaistaan vasta erikseen vahvistettuna.
  Kansion `index.html` on erien hakemisto ja julkaisun tarkistuslista.
