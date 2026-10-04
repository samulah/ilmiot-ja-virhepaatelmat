# SEO-toimenpidelista — ilmiöt.fi

Laadittu **4.10.2026**. Pisteet: **72/100** (25.7.: 80). Perustelut ja näyttö: `FULL-AUDIT-REPORT.md`.
Prioriteetti: Kriittinen > Korkea > Keskitaso > Matala.

**Kriittisiä ei ole.** Mikään ei estä indeksointia eikä aiheuta rangaistusriskiä. Vaihe 1 (kohdat 1, 6 asiavirheet, 7 ai-slop, 9 luvut) ja kohdat 2, 12, 13, 14 (osin) ja 17 on tehty repoon 4.10.2026 — ei vielä commitoitu eikä viety. Yksityiskohdat: `MUUTOSLOKI.md`. Tehdyt kohdat on merkitty ✅.

Työmääräarviot: **S** alle tunti, **M** muutama tunti, **L** päivä tai enemmän.

---

## Korkea (viikon sisällä)

### 1. Korjaa 26 väärää `<title>`-tagia — S ✅

Kaikilla alla olevilla sivuilla lukee nyt `DARVO — manipulaatiotaktiikka suomeksi | Ilmiöitä`. Ehdotukset on mitattu enintään 60 merkkiin. Yhdeksän sivun `og:title` käytti muotoa "— mitä se tarkoittaa", joka peruttiin 13.8.; niille ehdotus on johdettu `h1`:stä.

| Sivu | Ehdotettu `<title>` | Merkkiä |
|---|---|---|
| doksaus | Doksaus (doxxing) — mitä se on ja miten suojaudut | 49 |
| draamakolmio | Draamakolmio — Karpmanin kolme roolia suomeksi \| Ilmiöitä | 57 |
| dunkkaus | Dunkkaus ja ratio — mitä ne tarkoittavat somessa? \| Ilmiöitä | 60 |
| harmaa-kivi | Harmaa kivi (grey rock) — menetelmä suomeksi \| Ilmiöitä | 55 |
| huolitrollaus | Huolitrollaus — vastustaja esiintyy huolestuneena ystävänä | 58 |
| kafkatrapping | Kafkatrapping — kun kiistäminen todistaa syyllisyyden | 53 |
| kaksoissidos | Kaksoissidos (double bind) — käsky, jota ei voi totella | 55 |
| kuka-tahansa-voi-trollata | Kuka tahansa voi trollata — tutkimus huonosta päivästä | 54 |
| kunhan-kysyn | Kunhan kysyn (just asking questions) — väite kysymyksenä | 56 |
| maalittaminen | Maalittaminen — mitä se on ja miten siihen varaudutaan | 54 |
| mahdollistaja | Mahdollistaja (enabler) — apu, joka pitää ongelman käynnissä | 60 |
| motte-and-bailey | Motte and bailey — rohkea väite, turvallinen perääntymistie | 59 |
| no-contact | No contact — mitä täydellinen katkaisu tarkoittaa \| Ilmiöitä | 60 |
| nutpicking | Nutpicking — hölmöin kommentti koko joukon kasvoina | 51 |
| pimea-tetradi | Pimeä tetradi ja trollaus — mitä tutkimus sanoo? \| Ilmiöitä | 59 |
| roolinvaihto | Roolinvaihto draamakolmiossa — mikä on switch \| Ilmiöitä | 56 |
| sealioning | Sealioning eli merileijonointi — kun kysely ei lopu | 51 |
| shitpostaus | Shitpostaus (shitposting) — keskustelu hukutetaan roskaan | 57 |
| syntipukki | Syntipukki-rooli — miksi ryhmä tarvitsee yhden \| Ilmiöitä | 57 |
| tone-policing | Tone policing — puhutaan sävystä, ei asiasta | 44 |
| trollaus | Trollaus — mitä se on ja miksi trolli voittaa väittelyn | 55 |
| trollin-ruokkiminen | Älä ruoki trollia — toimiiko neuvo oikeasti? \| Ilmiöitä | 55 |
| vain-vitsi | ”Se oli vain vitsi” — kun ironia suojaa vastuulta \| Ilmiöitä | 60 |
| valirikko | Välirikko — miksi lähtijä ja jäävä maksavat eri hinnan | 54 |
| verkon-estottomuus | Verkon estottomuus — miksi netissä sanotaan enemmän | 51 |
| voittajakolmio | Voittajakolmio — Choyn vastine draamakolmiolle \| Ilmiöitä | 57 |

- **Tehty 4.10.** (`scripts/korjaa_darvo_titlet.py`). `doksaus` ja `tone-policing` saivat lisäksi brändipäätteen, koska se mahtuu 60 merkkiin. Esto: `lisaa_ilmiot.py` → `tarkista_title()`.
- Päivitä samalla `og:title` ja `twitter:title` vastaamaan uutta otsikkoa.
- Nosta `dateModified` näillä 26 sivulla ja aja `scripts/build_sitemap.py`, jotta muutos näkyy sitemapissa.
- **Estä toistuminen:** lisää julkaisuun (`scripts/lisaa_ilmiot.py` tai luonnoskansion tarkistuslista) tarkistus, joka kaatuu, jos `<title>` ei sisällä `h1`:n ensimmäistä termiä. Vika syntyi, koska luonnokset kopioitiin `darvo.html`:stä.

### 2. Fontit: poista layout-siirtymä ja turhat lataukset — M ✅

**Tehty 4.10.** (`scripts/fontit_esilataus.py`): CLS 0,21 / 0,19 → 0,000 samalla mittausprofiililla, fonttipyynnöt 5 → 3 (etusivu) ja 7 → 4 (artikkeli). Varafontin mittasovitusta ei tarvittu.

Labrassa mobiilin CLS on 0,21 (etusivu) ja 0,19 (artikkeli), ja 0, kun fontit estetään.

- Yksi `@font-face` per perhe: DM Sans yhdestä tiedostosta `font-weight: 400 600`, Source Sans 3 muuttujafontista `font-weight: 200 900`. Poista päällekkäiset määrittelyt joko `style.css`:stä tai `fonts/fonts.css`:stä.
- `<link rel="preload" as="font" type="font/woff2" crossorigin>` kahdelle ensimmäisen näkymän fontille (otsikon Spectral 700 ja leipätekstin fontti).
- Varafontille mittasovitus (`size-adjust`, `ascent-override`, `descent-override`), jolloin vaihto ei siirrä riviä. Vaihtoehto: `font-display: optional`.
- `style.css` muuttuu → `?v=` nostettava kaikilla sivuilla. Yhtenäistä samalla kaksi nykyistä versiomerkkiä yhdeksi.
- Mittaa uudelleen: tavoite CLS alle 0,1 ja enintään 3–4 fonttipyyntöä artikkelilla.

### 3. Jakokuvat — S

- Generoi `og/brand.png` uudelleen **ilman lukumäärää** (nyt "68 yhteiskunnallista ilmiötä"). Sama peruste kuin sivukohtaisissa kuvissa: luku vanhenee.
- Vie 20 valmista kuvaa palvelimelle ja sen jälkeen niiden HTML-sivut (kuvat ensin).
- Laajenna `scripts/build_og.py` kattamaan loput 145 artikkelia ja 14 kategoriaa.

### 4. Sulje hakemistolistaus ja sisäiset tiedostot — S

Ei vaikuta hakusijoituksiin; syy on tietovuoto (Search Console -data, liikenneluvut, skriptit).

```apache
Options -Indexes
<FilesMatch "\.(md|py|sh|sql|malli|json)$">
  Require all denied
</FilesMatch>
```

- Tarkista ennen käyttöönottoa, ettei sääntö estä tiedostoa, jota sivusto oikeasti lataa (JSON-esto koskee esimerkiksi mahdollista manifestia; `data/*.js` ei kuulu sääntöön).
- `.htaccess` on gitignoressa, joten se viedään palvelimelle käsin.
- Parempi pitkän päälle: julkaisu sallittujen tiedostojen listalta, jolloin `suosio_kooste.md`:n kaltaiset tiedostot eivät päädy palvelimelle.
- Poista palvelimelta jo sinne päätyneet: `GSC-AUDIT-*.md`, `suosio_kooste.md`, `UUDET-JUTUT-PLAN.md`, `artikkelien_sisaltolistaus.md` ja auditointiraportit.

### 5. `tietoa.html`: luotettavuuden perusrakenteet — M

- Yhteydenottotapa ja erikseen tapa ilmoittaa virheestä.
- Lyhyt lähde- ja korjauskäytäntö: mistä tieto tulee, miten virheet korjataan, mistä muutokset näkee (`muutokset.html`).
- Kuvaus siitä, miten tekstit syntyvät.
- Johdantoon kaikki 15 teemaa (nyt 11; puuttuvat media, tilastot, roolit, trollaus).
- Schemaan `dateModified`.

### 6. Asiavirheet ja huijaussivujen toimintaohjeet — M

- ✅ `ponzi-pyramidi.html`: "6 tasoa" → "8 tasoa" (kuudella värväyksellä kertymä ylittää 2 miljoonaa 8. tasolla; 6. tasolla se on noin 56 000).
- ✅ `tekoalypsykoosi.html`: muotoile "eikä tekoäly aiheuta psykoosia" näytön mukaiseksi, esimerkiksi "ei ole näyttöä, että tekoäly yksin aiheuttaisi psykoosin".
- ✅ `houkutinvaihtoehto.html`: nimeä Dan Arielyn koe, älä esitä lukuja The Economistin tilaustuloksena.
- Neljälle huijaussivulle (`pig-butchering`, `ennakkomaksuhuijaus`, `ponzi-pyramidi`, `pump-and-dump`) kappale "Jos olet jo maksanut": yhteys omaan pankkiin heti, rikosilmoitus poliisille, ilmoitus Kyberturvallisuuskeskukselle tai Finanssivalvonnalle tapauksen mukaan, ja Rikosuhripäivystys tueksi. Tarkista kanavien ajantasaiset nimet ja linkit ennen julkaisua.

### 7. Suomalaiset rinnakkaistermit — S

- ✅ `ai-slop.html`: lisää *tekoälytauhka* ja *tekoälymoska* ensimmäiseen kappaleeseen ja otsikkoon. (Tehty leipätekstiin ja vastauslohkoon; `<title>` jätetty ennalleen, koska 13.8. muutos on mittaamatta.) Suomenkielisen Wikipedian artikkeli on nimellä Tekoälytauhka; sanoja ei ole yhdelläkään sivulla.
- Käy sama tarkistus läpi kymmenelle eniten näyttöjä saavalle sivulle.

---

## Keskitaso (kuukauden sisällä)

### 8. Piirrä Mermaid-kaaviot valmiiksi SVG:ksi — L

914 kt:n skripti latautuu ilman vieritystä 72 sivulla 129:stä mobiilissa ja 128:lla työpöydällä.

- Skripti, joka renderöi jokaisen `.mermaid`-lohkon upotetuksi SVG:ksi kirjoitusvaiheessa (koneella on jo Playwright-Chromium). Sivuilta poistuu sekä skripti että latauslogiikka.
- Samalla: kolme vaakakaaviota (`sealioning`, `motte-and-bailey`, `brandolinin-laki`) pystyyn, ja jokaiselle kaaviolle `<figure>`, `<figcaption>`, `role="img"` ja `aria-label`.
- Chart.js-kaavioille (3 sivua) varateksti `<canvas>`-elementin sisään.

### 9. Otsikot ja vanhentuneet luvut — M

- Pudota brändipääte otsikoista, jotka ylittävät 60 merkkiä (51 mahtuu ilman sitä), ja valitse yksi erotin (`—` tai `|`).
- ✅ Kategoriaotsikot: huijaukset "11" → 14, tilastot "8" → 9, vallan rakenteet "7" → 8. Johda luku `scripts/build_kategoriat.py`:ssä tai jätä se pois.
- ✅ Etusivun `#random-vihje` "139 ilmiötä" → `scripts/paivita_maarat.py`:n hoidettavaksi, ja skriptiin tarkistus, joka kaatuu, jos korvauksia on nolla.
- ✅ `og:title` on pelkkä "X — Ilmiöitä" sivuilla `overton-ikkuna`, `paskuuttaminen` ja `starve-the-beast`.
- Muuta otsikoita yksi erä kerrallaan: 13.8. ja 4.9. tehtyjen muutosten vaikutus on vielä mittaamatta.

### 10. Ensisijaiset lähteet — L

131 artikkelissa ainoa ulkoinen lähde on Wikipedia tai ei mikään.

- Linkitä nimetyt tutkimukset DOI-osoitteeseen tai julkaisijan sivulle.
- Lisää suomalaiset viranomaislähteet sinne, missä ne ovat olemassa (Finlex, Poliisi, Kyberturvallisuuskeskus, Finanssivalvonta, KKV).
- Aloita 24 artikkelista, joissa ei ole yhtään kirjaa tai tutkimusta.

### 11. "Esimerkki Suomesta" -lohko — M

Vain noin 20 artikkelissa on Suomeen sidottu viite. Lisää 40–60 sanan kotimainen esimerkki kymmenelle eniten näyttöjä saavalle sivulle. Pysyy 260 sanan normin hengessä.

### 12. Ankkurit ja semanttiset elementit — S ✅

**Tehty 4.10.** (`scripts/seo_rakenne.py`): 433 ankkuria ja `<main>` 165 sivulla. `<article>` jätetty tekemättä tarkoituksella — luonnosskriptit tunnistavat `<div class="ilmio">`-säiliön tagista.

- `id` jokaiselle `h2`:lle (nyt 0/598), jotta osioon voi linkittää.
- Artikkelin runko `<article>`-elementtiin ja sivun pääsisältö `<main>`-elementtiin.

### 13. Schema-siivous — M ✅

**Tehty 4.10.** (`scripts/seo_schema.py`, `og/logo.png`): kaikki alla olevat paitsi `tietoa.html`. FAQPage poistettu.

- `isPartOf` → `{"@type": "WebSite", "@id": "https://www.ilmiöt.fi/#website"}` kaikilla 165 artikkelilla (lohko on tavulleen sama joka sivulla).
- FAQPage 68 artikkelilta: poista, tai kirjoita vastaukset samoiksi kuin sivun näkyvä teksti. Googlen rikastetulosta ei enää ole.
- `description` metakuvauksesta (115 vanhentunutta, 59 katkennutta).
- Julkaisijan logoksi vähintään 112×112 px:n PNG (tiedosto on tehtävä ensin).
- `about`/DefinedTerm: joko kaikille 165:lle termin nimellä tai pois kaikilta.
- `hajota-hallitse.html`: "—divide" → "— divide" otsikossa ja murupolussa.

### 14. Leipätekstilinkit — M

- Yksi kategorian sisäinen leipätekstilinkki jokaiseen 63 artikkeliin, joihin ei nyt viitata. Aloita mediasta (8/10) ja alustataloudesta (9/17).
- ✅ `bait-and-switch.html`: "uponneiden kustannusten" → `sunk-cost-harha.html`.
- Tehty 4.10.: viisi luontevaa mainintaa linkitetty (`pump-and-dump`, `foot-in-the-door`, `klikkiotsikko`, `engagement-bait`, `sinipesu`). **58 artikkelia on yhä ilman saapuvaa leipätekstilinkkiä** — niistä ei ole linkittämätöntä mainintaa missään, joten jokainen vaatii uuden virkkeen.
- ✅ **Kahdeksan rikkinäistä ulkoista linkkiä** (+ caltech; `bcaction.org` ei vastannut täältäkään, jätetty ennalleen) (404, lista raportin kohdassa 9): viisi en.wikipedia-artikkelia, joiden nimi on muuttunut tai jota ei ole, sekä cia.gov, amnesty.org ja raitiotieallianssi.fi. Korjaa Wikipedia-osoitteet ja vaihda muut arkistokopioon tai toiseen lähteeseen. Tarkista samalla `caltech.edu` (`rituaalinen-raportointi`) ja `bcaction.org` (`pinkkipesu`), jotka eivät vastanneet.

### 15. Välimuisti — S

- `data/suosio.js`: `Cache-Control: no-cache` (generoidaan öisin, nyt 7 vrk välimuistissa).
- `search-index.js`: lataa vasta, kun hakukenttä saa kohdistuksen; lisää versiomerkki.
- Versioiduille tiedostoille `immutable`.

### 16. `/index.html` — S

301-ohjaus `/index.html` → `/`, tai vaihda 183 sivun linkit muotoon `./`. Ohjaus on yksi rivi samaan `.htaccess`-kierrokseen.

### 17. Vastakeino-otsikot — S

- ✅ Nimeä 13 osiota uudelleen niin, että otsikossa on "vastakeinot" (sisältö on jo olemassa).
- Vahvista kolme heikkoa: `parasosiaalinen-suhde`, `strateginen-osaamattomuus`, `yhdeksanyhdeksan`.

### 18. Mobiilin viimeistely — M

- Kavenna artikkelin sivumarginaaleja (nyt 57 px, palsta noin 276 px).
- Kosketuskohteet vähintään 48 px: jakonappi, satunnaisnappi, murupolun linkki.
- Edellinen/seuraava-linkit kahdelle riville katkaisun sijaan.
- Piilota näppäimistövihje kosketuslaitteilla.
- Leipätekstin linkeille paletin väri; "LUE LISÄÄ" -otsikon kontrasti vähintään 4,5:1.

### 19. Oma 404-sivu — S

Suomenkielinen sivu, jossa on linkki etusivulle ja haku. `ErrorDocument 404 /404.html`.

---

## Matala (työjono)

- **CSP:** poista `cdn.jsdelivr.net`, `fonts.googleapis.com` ja `fonts.gstatic.com`; lisää `base-uri 'self'`, `form-action 'self'`, `object-src 'none'`.
- **Sitemap:** poista `<priority>` ja `<changefreq>`; lisää `build_sitemap.py`:hyn vertailu juuren `*.html`-tiedostoihin.
- **`random.html`:** poista palvelimelta tai vie ajantasainen versio (live on 0 tavua, repon IDS-lista on 109 ilmiön ajalta).
- **Kuvakkeet:** `favicon.ico`, `apple-touch-icon`, ja `width`/`height` `favicon.svg`-kuvalle.
- **Metakuvaukset:** ✅ lyhennetty 7 yli 160-merkkistä (kahdeksatta ei löytynyt); vaihtele 87 kuvauksen "Selitämme"-alkua.
- **Määritelmä ensin:** 13 artikkelia ei ala määritelmällä (lista raportin GEO-osiossa).
- **Kysymys–vastaus-lohko** niille 97 artikkelille, joilta se puuttuu, aloittaen eniten näyttöjä saavista.
- **Upotettu CSS ja JS** (noin 46 kt per artikkeli) erilliseen välimuistitettavaan tiedostoon; mahdollistaa myös `'unsafe-inline'`n poiston.
- ✅ **Kieli:** "Konsensus fetissi" → "Konsensusfetissi"; `kafka-ilmio`ssa yksi suomenkielinen nimi Kafkan romaanille (*Oikeusjuttu*).
- **Erottelurivit** sivuille `hiljainen-irtisanominen` ja `hiljainen-irtisanoutuminen`.
- **Bing Webmaster Tools** käyttöön, sen jälkeen IndexNow. Antaa samalla backlink-datan.
- **`tietoa.html`:** ProfilePage-merkintä tekijälle.

---

## Mittaamatta jääneet — tee ennen seuraavaa auditointia

1. **Search Console -vienti lokakuulta.** Ilman sitä 13.8. ja 4.9. otsikkomuutosten tulos on tuntematon, eikä uusia otsikkomuutoksia voi arvioida.
2. **Sitemaps-raportti Search Consolessa:** löydettyjen URL:ien määrä pitäisi olla 184.
3. **Google-rajapinnan avain** (`GOOGLE_API_KEY`), jolloin CLS, LCP ja INP saadaan oikeilta käyttäjiltä.
4. **Kannibalisointitesti** epäillyille pareille: `hiljainen-irtisanominen`/`-irtisanoutuminen`, `trollaus`/`trollin-ruokkiminen`, `draamakolmio`/`voittajakolmio`/`roolinvaihto`. Testaa myös luonnos `mita-vastata-trollille` sivua `trollin-ruokkiminen` vastaan ennen julkaisua.
5. **Viittaavat verkkotunnukset** Search Consolen Linkit-raportista.
6. **Common Crawl:** sivustosta ei ole yhtään tallennetta. Tarkista uudelleen alkuvuodesta 2027.

---

## Ehdotettu järjestys

| Vaihe | Kohdat | Miksi yhdessä |
|---|---|---|
| 1 | 1, 7, 6 (Ponzi), 9 (luvut) | pelkkiä tekstikorjauksia, yksi julkaisu |
| 2 | 4, 15, 16, 19, CSP | yksi `.htaccess`-kierros käsin |
| 3 | 3 | kuvat ensin, HTML perään |
| 4 | 2 | vaatii `style.css`-version noston kaikilla sivuilla |
| 5 | 5, 6 (loput), 10, 11 | sisältötyö |
| 6 | 8, 12, 13 | rakenteelliset muutokset skripteillä |
