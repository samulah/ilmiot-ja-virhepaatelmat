# SEO-auditointi — ilmiöt.fi

**Tehty:** 4.10.2026 · **URL:** https://www.ilmiöt.fi/ (`xn--ilmit-mua.fi`)
**Laajuus:** 185 live-URL:ää haettu (184 sitemapista + `/index.html`), kaikki 200. Live on md5-identtinen `main`-haaran HEADin kanssa kaikilla 185 sivulla.
**Edellinen auditointi:** 25.7.2026 — 80/100 (111 sivua)

## Kokonaispisteet: **72 / 100**

| Osa-alue | Paino | Pisteet | Ed. (25.7.) | Painotettu |
|---|---|---|---|---|
| Tekninen SEO | 22 % | 78 | 83 | 17,2 |
| Sisällön laatu | 23 % | 72 | 76 | 16,6 |
| On-page | 20 % | 66 | 78 | 13,2 |
| Schema | 10 % | 80 | 92 | 8,0 |
| Suorituskyky | 10 % | 76 | 74 | 7,6 |
| Tekoälyhaku (GEO) | 10 % | 66 | 82 | 6,6 |
| Kuvat | 5 % | 60 | 85 | 3,0 |
| **Yhteensä** | | | **80** | **72,1** |

**Miksi pisteet laskivat kahdeksalla.** Lasku jakautuu kahteen eri syyhyn, eikä niitä pidä sekoittaa:

- **Todellinen heikennys:** kahden uusimman erän (4.9. ja 3.10.) kaikki 26 sivua julkaistiin väärällä `<title>`-tagilla. Tämä yksin selittää suurimman osan on-page-pisteiden pudotuksesta.
- **Tarkempi mittaus:** tällä kierroksella mitattiin asioita, joita heinäkuussa ei mitattu. Layout-siirtymä mitattiin labrassa ensimmäistä kertaa, jakokuvan teksti luettiin, hakemistolistaus kokeiltiin, lähdelinkit laskettiin ja FAQ-merkintöjen teksti verrattiin sivun näkyvään tekstiin. Lisäksi Google lopetti FAQ-rikastetulokset 7.5.2026, mikä vie arvon 68 sivun merkinnältä. Nämä viat olivat pääosin olemassa jo heinäkuussa.

**Sivustotyyppi:** itsenäinen suomenkielinen tietopankki (julkaisija/hakuteos). Ei kaupallinen, ei paikallinen. Sovellettava ohjeisto on julkaisijan SEO: käsitekattavuus, kappaletason siteerattavuus ja luotettavuussignaalit.

---

## Yhteenveto

Indeksointia estäviä tai rangaistusriskiä aiheuttavia vikoja ei ole. Kaikki sivut vastaavat 200, kanoniset osoitteet ovat kunnossa, rikkinäisiä sisäisiä linkkejä ei ole ja jokainen sivu on yhden klikkauksen päässä etusivulta. Edellisen auditin pahin ongelma, neljä rinnakkaista isäntänimeä, on korjattu.

### Viisi tärkeintä ongelmaa

1. **26 artikkelilla on väärä `<title>`.** Kaikki 17 trollaussivua ja 9 Roolit ja valtapelit -sivua kantavat otsikkoa "DARVO — manipulaatiotaktiikka suomeksi | Ilmiöitä". Sama otsikko on siis 27 sivulla. `h1`, metakuvaus, `og:title` ja schema ovat oikein, ja vika on myös repossa.
2. **Fontit aiheuttavat layout-siirtymän ja latautuvat moneen kertaan.** Labrassa mobiilin CLS on etusivulla 0,21 ja artikkelissa 0,19 (hyvän raja 0,1); kun fontit estetään, CLS on 0. Artikkeli hakee 7 fonttitiedostoa (206 kt), joista noin 95 kt on saman tiedoston uudelleenlatausta.
3. **Jakokuva on vanhentunut ja yhteinen kaikille.** `og/brand.png` sanoo "68 yhteiskunnallista ilmiötä", ja se on kaikkien 185 sivun `og:image`. Sivukohtaiset kuvat (20 kpl) ovat valmiina paikallisesti mutta eivät palvelimella.
4. **Palvelin näyttää hakemistolistaukset ja sisäiset tiedostot.** `/scripts/`, `/kategoriat/`, `/pelidata/`, `/data/`, `/og/`, `/fonts/` ja `/js/` listautuvat. Julkisia ovat mm. `GSC-AUDIT-2026-08-13.md` (oikeaa Search Console -dataa), `suosio_kooste.md` (liikennelukuja, gitignoressa mutta palvelimella), `CLAUDE.md` ja kaikki skriptit. Hakusijoituksiin tämä ei vaikuta; kyse on tietovuodosta.
5. **Luotettavuuden perusrakenteet puuttuvat.** `tietoa.html`:ssä ei ole yhteystietoa, virheilmoituskanavaa eikä lähde- tai korjauskäytäntöä. 131 artikkelissa 165:stä jokainen leipätekstin ulkoinen linkki vie Wikipediaan tai linkkiä ei ole. `ponzi-pyramidi.html`:ssä on laskuvirhe.

### Viisi nopeinta korjausta

1. Korjaa 26 otsikkoa (ehdotukset `ACTION-PLAN.md`:ssä) ja lisää julkaisuskriptiin tarkistus, joka kaatuu, jos `<title>` ei sisällä `h1`:n termiä.
2. Yksi `.htaccess`-kierros: `Options -Indexes`, sisäisten tiedostotyyppien esto, `data/suosio.js`:lle `no-cache`, CSP:n vanhentuneet isännät pois, oma 404-sivu.
3. Generoi `og/brand.png` uudelleen ilman lukumäärää ja vie 20 valmista sivukohtaista jakokuvaa palvelimelle (kuvat ensin, sitten HTML).
4. Sisältökorjaukset, joissa on yksi oikea vastaus: Ponzi-laskelma (6 tasoa → 8), `tekoälytauhka` ja `tekoälymoska` AI slop -sivulle, kolme vanhentunutta lukua kategoriaotsikoissa ja etusivun "139 ilmiötä".
5. Yksi `@font-face` per fonttiperhe ja `preload` kahdelle ensimmäisen näkymän fontille.

---

## Edistyminen 25.7.2026 auditista

| Kohta | Tila |
|---|---|
| Neljä isäntä-/protokollavarianttia palautti 200 | ✅ Korjattu — `http://`, `http://www.` ja apex ohjautuvat 301:llä yhdellä hypyllä |
| 97 sivulla vain kaksi otsikkoa (laatikoiden otsikot olivat `<strong>`) | ✅ Korjattu — jokaisella artikkelilla on vähintään yksi `h2` leipätekstissä, 154:llä vähintään kaksi |
| `llms.txt` kolme sivua jäljessä | ✅ Korjattu — 165 artikkelia ja 15 kategoriaa, ei vanhentuneita polkuja |
| Sitemapin `lastmod` ristiriidassa 93 sivulla | ✅ Korjattu — 0 ristiriitaa |
| 929 kt Mermaid-skripti CDN:stä | ◐ Osittain — itsehostattu ja laiska lataus, mutta 914 kt latautuu yhä (ks. Suorituskyky) |
| `chart.js` ilman `defer`-attribuuttia | ✅ Korjattu |
| Sivukohtaiset jakokuvat | ◐ 20 tehty paikallisesti, ei julkaistu |
| `SearchAction` | — Ei enää ajankohtainen; Google poisti sivustohakukentän hakutuloksista |

---

## 1. Tekninen SEO — 78

**Kunnossa.** 185/185 vastaa 200. Jokainen kanoninen osoite viittaa itseensä. `noindex`-sivuja ei ole. Sisäisiä linkkejä on 3 262, joista yksikään ei ole rikki, eikä orposivuja ole. Isäntäohjaukset toimivat yhdellä hypyllä. HSTS, `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy` ja `Permissions-Policy` ovat paikallaan. HTTP/2 ja brotli ovat käytössä, palvelimen vasteaika on 44–62 ms. Etusivun kaikki 165 korttia ja 15 kategoriaa ovat tavallisia linkkejä raaka-HTML:ssä, joten mikään indeksoitava ei riipu JavaScriptistä.

**Löydökset**

| Vakavuus | Löydös | Näyttö |
|---|---|---|
| Korkea | 27 sivulla sama `<title>` | ks. On-page |
| Keskitaso | Hakemistolistaus päällä | `Index of /scripts/` ym. seitsemässä hakemistossa |
| Keskitaso | Sisäiset tiedostot julkisia | `/GSC-AUDIT-2026-08-13.md`, `/suosio_kooste.md`, `/CLAUDE.md`, `/MUUTOSLOKI.md`, `/scripts/paivita_suosio.py`, `/.suosio.env.malli`, `/pelidata/TYYLI.md` → 200. `/.suosio.env`, `/data/.viikko-historia.json` → 404 ja `/.git/HEAD`, `/.htaccess` → 403, eli salaisuudet eivät vuoda |
| Keskitaso | `data/suosio.js` välimuistissa 7 vrk | `Cache-Control: public, max-age=604800`, ei versiomerkkiä. Tiedosto generoidaan joka yö, ja etusivu piilottaa lohkot, jos data on yli tuoreusrajan — palaava kävijä voi siis nähdä vanhan datan tai tyhjät lohkot |
| Keskitaso | `/index.html` on kaksoiskappale | palauttaa 200, kanoninen osoittaa `/`:ään, mutta 183 sivua linkittää `index.html`:ään |
| Keskitaso | CSP sallii isäntiä, joita ei käytetä | `cdn.jsdelivr.net`, `fonts.googleapis.com`, `fonts.gstatic.com`; lisäksi `'unsafe-inline'`, ei `base-uri`-, `form-action`- eikä `object-src`-sääntöä |
| Matala | 404-sivu on LiteSpeedin oletus | englanninkielinen, ei linkkiä sivustolle, ei viewport-metaa (`screenshots/404-mobile.png`) |
| Matala | `/random.html` on livenä tyhjä | 200 ja 0 tavua; repossa 2 650 tavua vanhalla 109 ilmiön listalla. Mikään ei linkitä siihen |
| Matala | Sitemapissa `<priority>` ja `<changefreq>` | Google ohittaa molemmat |
| Matala | `build_sitemap.py` voi pudottaa sivuja hiljaa | korttiregex vaatii täsmälleen `class="hub-kortti"`, eikä tulosta verrata tiedostolistaan. Tulos on tänään oikein (165/165) |
| Matala | HTML:llä ei ole `Cache-Control`-otsaketta | vain `Last-Modified`; ehdollinen haku palauttaa silti 304 |
| Matala | `style.css` kahdella versiomerkillä | 162 sivua `?v=20260725`, 18 sivua `?v=20260727`, sama tiedosto. `fonts.css`, `mermaid.min.js` ja `search-index.js` ovat versioimattomia |
| Matala | `favicon.ico` → 404 | vain `favicon.svg`; ei `apple-touch-icon`ia |

**Unicode vai punycode.** Kanoniset osoitteet, `og:url`, schema, sitemap ja `llms.txt` käyttävät kaikki muotoa `www.ilmiöt.fi`; vain `robots.txt`:n `Sitemap:`-rivi ja palvelimen ohjaukset käyttävät punycodea. Muoto on johdonmukainen, ja sivut indeksoituvat Search Consolen mukaan, joten muutosta ei tarvita. Varmista kuitenkin Search Consolen Sitemaps-raportista, että löydettyjen URL:ien määrä on 184.

**IndexNow** ei ole käytössä. Google ei käytä sitä; Bingille (ja sitä kautta Copilotille) se kannattaa lisätä vasta, kun Bing Webmaster Tools on vahvistettu.

---

## 2. Sisällön laatu — 72

Agentti luki noin 57 artikkelia (41 kokonaan). Osapisteet: E-E-A-T 56, syvyys 74, tarkkuus 80, rakenne ja luettavuus 82, tuoreus 80.

**Vahvuudet.** Tekstit ovat täsmällisiä: nimiä, vuosilukuja ja lukuja. Rakenne on yhtenäinen (määritelmä, mekanismi, esimerkki, vastakeino), virkkeet lyhyitä (mediaani 12,8 sanaa). Kopioitua tekstiä ei ole; suurin neljän sanan jaksojen päällekkäisyys kahden sivun välillä on 10,8 %. Kategoriasivuilla on omaa proosaa 366–766 sanaa. Näkyvä "Päivitetty"-päivä vastaa schemaa kaikilla 165 sivulla.

**Löydökset**

| Vakavuus | Löydös | Näyttö |
|---|---|---|
| Korkea | Ei luotettavuuden perusrakenteita | `tietoa.html` (223 sanaa): ei yhteystietoa, ei virheilmoituskanavaa, ei lähde- tai korjauskäytäntöä. Johdanto luettelee 11 teemaa 15:stä (puuttuvat media, tilastot, roolit, trollaus) |
| Korkea | Laskuvirhe | `ponzi-pyramidi.html`: "6 tasoa jos jokainen värvää 6 uutta → > 2 milj." Oikea luku kuudella tasolla on 46 656 (kertymä noin 56 000); 2 miljoonaa ylittyy 8. tasolla. "13 tasoa ylittää maapallon väkiluvun" pitää paikkansa |
| Korkea | Lähteet nojaavat Wikipediaan | 126 artikkelissa kaikki leipätekstin ulkoiset linkit ovat Wikipediaan, 5:ssä linkkejä ei ole. 163 linkkiä 201:stä vie `en.wikipedia.org`iin. Tutkimukset nimetään mutta ei linkitetä |
| Korkea | Huijaussivuilta puuttuu "jos olet jo maksanut" | `pig-butchering`, `ennakkomaksuhuijaus`, `ponzi-pyramidi`, `pump-and-dump` (189–195 sanaa): ei toimintaohjetta uhrille eikä nimettyä suomalaista kanavaa. Sama koskee `no-contact`-, `harmaa-kivi`- ja `gaslighting`-sivuja |
| Keskitaso | Ehdottomia väitteitä | `tekoalypsykoosi`: "eikä tekoäly aiheuta psykoosia" on kategorinen kiisto aiheesta, josta näyttö on kesken. `houkutinvaihtoehto` esittää Arielyn koeasetelman The Economistin tilaustuloksena |
| Keskitaso | Vastakeino-lupaus | 16 artikkelilta puuttuu "vastakeinot"-otsikko. Näistä 13:ssa sisältö on olemassa toisella nimellä ("Työntekijälle:", "Hakijalle:"); kolmessa se on heikko: `parasosiaalinen-suhde`, `strateginen-osaamattomuus`, `yhdeksanyhdeksan` |
| Keskitaso | Missä 260 sanan normi maksaa | huijaussivut (yllä) sekä `hippo-efekti`, `scope-creep`, `door-in-the-face` ja `houkutinvaihtoehto`, joissa alkuperä jää ohueksi. Tilasto- ja trollaussivut ovat lyhyitä mutta täydellisiä |
| Keskitaso | Mallipohjan jälki | 87 metakuvauksessa "Selitämme", 28 sivulla "…suomeksi?"-`h2`, 35 sivua päättyy samaan pelikappaleeseen (vain termi vaihtuu) |
| Matala | Kieli | "Konsensus fetissi" (yhdyssana erikseen `h1`:ssä ja titlessä); `kafka-ilmio` käyttää samasta kirjasta nimiä *Oikeudenkäynti* ja *Oikeusjuttu*; `hajota-hallitse`n schema-otsikossa "—divide" ilman välilyöntiä |
| Matala | Väärä linkkikohde | `bait-and-switch.html`: "uponneiden kustannusten" vie `korkokierre.html`:ään, pitäisi `sunk-cost-harha.html`:ään |

Nimimerkki voi kantaa asiantuntemusta työn laadun kautta, ja tämä sivusto tekee sen. Se ei voi kantaa luottamusta, ellei *sivusto* tarjoa sitä, mitä henkilö ei tarjoa: tapaa ottaa yhteyttä, tapaa ilmoittaa virheestä ja kuvausta siitä, miten tekstit syntyvät.

---

## 3. On-page — 66

| Mittari | Arvo |
|---|---|
| Väärä `<title>` | 26 sivua (27 jakaa saman otsikon) |
| Otsikon pituus | mediaani 59, maksimi 90; 82 sivua yli 60 merkkiä, joista 51 mahtuisi ilman brändipäätettä |
| Brändipääte | 129 sivua `— Ilmiöitä`, 56 sivua `\| Ilmiöitä` |
| Metakuvaus | mediaani 144 merkkiä; 8 yli 160; ei puuttuvia, ei kaksoiskappaleita |
| `h1` | täsmälleen yksi joka sivulla |
| Kysymysmuotoinen `h2` | 68 artikkelilla; 97:llä ei |
| Otsikoiden `id` | 0 / 598 `h2`:sta |
| `<main>` / `<article>` | ei yhdelläkään sivulla |

**Väärät otsikot.** Luonnokset on tehty `darvo.html`:n pohjalta, ja `<title>` jäi vaihtamatta. Oikeat otsikot ovat sivujen `og:title`-kentissä, mutta niitä ei pidä kopioida sellaisenaan: yhdeksän niistä käyttää muotoa "— mitä se tarkoittaa", joka peruttiin 13.8., koska se laski klikkausprosenttia, ja kolme on 75–81 merkkiä pitkiä. Ehdotukset kaikille 26:lle ovat toimenpidelistassa.

**Vanhentuneet luvut.** Kategoriaotsikoissa: huijaukset "11" (sivuja 14), tilastot "8" (9), vallan rakenteet "7" (8). Etusivun satunnaislohkossa lukee "139 ilmiötä". Jakokuvassa "68".

**Puuttuvat suomalaiset rinnakkaistermit.** `ai-slop.html` ei mainitse sanoja *tekoälytauhka* tai *tekoälymoska*, vaikka suomenkielisen Wikipedian artikkeli on nimellä Tekoälytauhka. Kumpaakaan sanaa ei ole yhdelläkään 185 sivusta.

**Suomalainen konteksti.** Noin 20 artikkelissa 165:stä on leipätekstissä jokin Suomeen sidottu viite (kaksi eri laskentatapaa antoi 18 ja 23). Hakutuloksissa näkyneillä suomalaisilla kilpailijoilla (HS, Yle, Lääkärilehti) on kotimainen kytkös.

**Hakutulosvertailun rajat.** Vertailu jäi osittaiseksi: hakutyökalu palautti suomalaisille hauille enimmäkseen ulkomaisia tuloksia ja esti suurimmat suomalaiset uutissivustot, eikä Googlen tulossivua saatu luettua. Ainoa oikea järjestetty tuloslista oli Bingin `hyvesignalointi`, jossa ilmiöt.fi oli toisena fi.wikipedian jälkeen; Googlessa sama sivu on Search Consolen mukaan sijalla 7. Tekoälyvastauksia, esittelykatkelmia tai "Ihmiset kysyvät myös" -kysymyksiä ei havaittu, koska työkalu ei näytä niitä.

**Missä 260 sanaa riittää ja missä ei.** Riittää puhtaissa määritelmähauissa, joissa suomenkielistä kilpailua ei ole: `darvo.html` (221 sanaa) toi elokuun datassa 71 % sivuston klikeistä, ja fi.wikipedian tyngät aiheista *whataboutismi* ja *Hanlonin partaveitsi* ovat 110–140 sanaa. Ei riitä, kun haku on "miten vastata" tai kun Wikipedia on perusteellinen (*Brandolinin laki*, noin 1 500 sanaa). Halvin vastaus normin sisällä: kysymysmuotoiset `h2`:t, joiden alla on 40–60 sanan vastaus, ja lyhyt "Esimerkki Suomesta" -lohko.

---

## 4. Schema — 80

Kaikki 185 JSON-LD-lohkoa jäsentyvät. Murupolut osoittavat olemassa oleviin sivuihin, `articleSection` vastaa kategoriaa ja päivämäärät ovat johdonmukaiset kaikilla 165 artikkelilla. Väärän otsikon 26 sivulla schema-`headline` on oikein.

| Vakavuus | Löydös | Näyttö |
|---|---|---|
| Keskitaso | FAQPage ei vastaa sivua, eikä sillä ole enää Google-käyttöä | 68 artikkelia: 0/136 vastauksesta löytyy sivulta sanatarkasti. Google lopetti FAQ-rikastetulokset 7.5.2026 ja poisti dokumentaation 15.6.2026 |
| Keskitaso | `isPartOf` osoittaa solmuun, jota ei ole | 165 artikkelia viittaa `@id "https://www.ilmiöt.fi/"`; etusivun CollectionPage on `…/#collectionpage`. 139 artikkelilla sama IRI on lisäksi `DefinedTermSet` |
| Keskitaso | Julkaisijan logo alle Googlen vähimmäiskoon | `favicon.svg`, ilmoitettu 64×64; vähimmäiskoko on 112×112 |
| Matala | Scheman `description` vanhentunut | eroaa metakuvauksesta 115 artikkelilla; 59 katkeaa "…"-merkkiin |
| Matala | `tietoa.html` | ei `dateModified`ia; AboutPage, vaikka tekijäsivulle suositellaan ProfilePagea |
| Matala | `about`/DefinedTerm epäyhtenäinen | 139 artikkelilla on, 26:lla ei; `name` on koko otsikko, ei termi |
| Tieto | 20 sivua ilman `datePublished`ia | kaikki muita kuin artikkeleita (etusivu, 15 kategoriaa, peli, muutokset, tietoa) |

Älä lisää `SearchAction`-, `speakable`- tai `Quiz`-merkintää: yhdelläkään ei ole tälle sivustolle käyttäjää.

---

## 5. Suorituskyky — 76

**Kaikki luvut ovat labramittauksia.** Kenttädataa (CrUX) ei ole, koska Google-rajapinnan avainta ei ole määritetty. INP:tä ei mitattu. Lighthouse ajettiin vain kahdelle sivulle mobiiliprofiililla (hidas 4G, 4× CPU-hidastus); Mermaid-, kaavio-, kategoria- ja pelisivuja sekä työpöytää ei mitattu.

| Sivu | Lighthouse | LCP | CLS | TBT | Siirto | Fontit |
|---|---|---|---|---|---|---|
| `/` (3 ajoa) | 89 | 1,10 s | **0,214** | 28 ms | 372 kt | 5 tiedostoa, 157 kt |
| `/dunkkaus.html` (2 ajoa) | 91–92 | 1,04 s | **0,17–0,20** | 0–20 ms | 221 kt | 7 tiedostoa, 206 kt |

**CLS johtuu fonteista.** Erillinen mittaus (Playwright, sama mobiiliprofiili, 3 ajoa): etusivu 0,213 ja artikkeli 0,188 normaalisti, molemmat **0,000** kun `.woff2`-pyynnöt estetään. Siirtymä syntyy, kun varafontti vaihtuu verkkofonttiin. Etusivulla siirtyvät `main#hub-main` ja kategorianavigaatio, artikkelissa ensimmäinen kappale ja vastauslaatikko.

**Fontit latautuvat moneen kertaan.** DM Sansin painot 400, 500 ja 600 ovat tavulleen sama tiedosto kolmella osoitteella (md5 tarkistettu). Artikkeli hakee lisäksi Source Sansin kolmesti (`sourcesans-400`, `sourcesans-600`, `sourcesans3-var`), koska sekä `style.css` että `fonts/fonts.css` määrittelevät fontit. Noin 95 kt artikkelin 206 kt:n fonttikuormasta on turhaa. `preload`ia ei ole.

**Mermaid latautuu käytännössä heti.** 914 kt:n (brotli) skripti haetaan, kun kaavio on 200 px:n päässä näkymästä. Mobiilinäkymässä (412×823) se täyttyy ilman vieritystä 72 sivulla 129:stä, työpöydällä 128:lla. Pääsäikeen kuormaa ja kaavion piirtymisen aiheuttamaa siirtymää ei mitattu.

**Muut.** Etusivu lataa `search-index.js`:n (184 kt, 49 % sivun siirrosta) heti, vaikka sitä tarvitaan vasta haussa. Jokainen artikkeli kantaa noin 46 kt samaa upotettua CSS:ää ja JavaScriptiä, 78 % raaka-HTML:stä.

---

## 6. Kuvat — 60

Sivustolla ei ole sisältökuvia; ainoa `<img>` on `favicon.svg`. Kaaviot ovat Mermaidia ja kolmella sivulla Chart.js:ää.

| Vakavuus | Löydös | Näyttö |
|---|---|---|
| Korkea | Jakokuva vanhentunut | `og/brand.png`: "68 yhteiskunnallista ilmiötä", kaikilla 185 sivulla (`screenshots/og-brand-live.png`) |
| Keskitaso | Kolme vaakakaaviota lukukelvottomia mobiilissa | `sealioning`, `motte-and-bailey`, `brandolinin-laki` (`flowchart LR`): 12 px:n teksti näkyy noin 3 px:n kokoisena (`screenshots/sealioning-mermaid-mobile-viewport.png`). Muut 127 kaaviota ovat pystysuuntaisia ja luettavia |
| Keskitaso | Kaavioilla ei saavutettavaa nimeä eikä varasisältöä | SVG:ssä ei `aria-label`ia, `<title>`ä eikä `<desc>`iä. Ilman JavaScriptiä kävijä näkee Mermaid-lähdekoodin kappaleena (`screenshots/darvo-nojs-mermaid.png`). Chart.js-canvas on tyhjä ilman varatekstiä |
| Matala | `favicon.svg` ilman mittoja | `width`/`height` puuttuu 165 sivulla |

Julkaisemattomat sivukohtaiset jakokuvat (`og/trollaus.png` ym.) ovat hyviä ja luettavia pikkukuvakoossa.

**Mobiilikäytettävyys** (ei painotettu osa-alue, 72/100): perusta on kunnossa — 16 px:n fontti, ei vaakavieritystä, määritelmä näkyy ilman vieritystä. Huomiot: artikkelin tekstipalsta on noin 276 px leveä 57 px:n marginaalien takia; 10 kosketuskohdetta 15:stä on alle 48 px (jakonappi 28×19, satunnaisnappi 37×24); edellinen/seuraava-linkit katkeavat muotoon "← Shitp…"; näppäimistövihje näkyy kosketuslaitteilla; leipätekstin linkit ovat selaimen oletussinisiä; "LUE LISÄÄ" -otsikon kontrasti on 1,67:1.

---

## 7. Tekoälyhaku (GEO) — 66

**Kunnossa.** `robots.txt` sallii kaiken ja nimeää GPTBotin, OAI-SearchBotin, ClaudeBotin ja PerplexityBotin. Yhdeksällä eri user-agentilla tehty haku palautti saman sivun. `llms.txt` on ajan tasalla. Sisältö on staattista HTML:ää.

**Siteerattavuus.** 130 artikkelia 165:stä alkaa itsenäisellä määritelmällä; ensimmäisen kappaleen mediaani on 41 sanaa. 68 artikkelilla on kysymysotsikko ja sen alla 29–63 sanan vastaus. 76 mainitsee englanninkielisen alkuperäistermin ensimmäisessä kappaleessa.

| Vakavuus | Löydös | Näyttö |
|---|---|---|
| Korkea | 26 väärää otsikkoa | otsikko on keskeinen hakusignaali myös tekoälyhauissa |
| Korkea | Osioihin ei voi linkittää | yhdelläkään `h2`:lla ei ole `id`:tä; ei `<main>`- eikä `<article>`-elementtiä |
| Keskitaso | 13 artikkelia ei ala määritelmällä | `bkt-harha`, `korkokierre`, `kuka-tahansa-voi-trollata`, `lapi-hinnalla-milla-hyvansa`, `lukittu-paatos`, `p-hakkerointi`, `pinta-alaharha`, `portinvartija-kulttuuri`, `selviytymisharha`, `strateginen-aliarviointi`, `suhteellinen-riski`, `keskiarvo-vs-mediaani`, `simple-sabotage` |
| Keskitaso | 97 artikkelilla ei kysymys–vastaus-lohkoa | |
| Keskitaso | Kaaviot näkyvät ei-JS-roboteille lähdekoodina | lähdeteksti on HTML:ssä, joten sisältö ei katoa, mutta se on kaaviosyntaksia |

Pistemäärä on agentin 63:a korkeampi, koska sen auktoriteettiosio jäi mittaamatta: sivuston ulkopuolisia mainintoja, Wikipediaa, Wikidataa ja Bing-indeksointia ei tarkistettu. `llms-full.txt`:ää ei kannata lisätä; ei ole näyttöä siitä, että mikään suuri tekoälyjärjestelmä lukisi edes `llms.txt`:ää.

---

## 8. Sisäinen linkitys ja klusterit — 72 (ei painotettu)

Rakenne on ehjä: jokainen kategoriasivu linkittää jokaiseen sivuunsa kortilla ja johdantotekstissä, ja jokainen artikkeli linkittää takaisin kategoriaansa. Ankkuritekstit ovat hyviä: 207 leipätekstilinkistä yksikään ei ole geneerinen ja 92 % sisältää kohteen termin.

**Leipätekstilinkitys on ohutta.** 63 artikkeliin ei viittaa yksikään toinen artikkeli leipätekstistään. Keskittymät: media 8/10, alustatalous 9/17, tilastot 6/9, projektit 6/12, pesut 4/6. Median sivut linkittävät lähes pelkästään muihin kategorioihin (0,30 sisäistä vs. 2,0 ulkoista leipätekstilinkkiä sivua kohden). Elokuun GSC-auditointi neuvoi olemaan tekemättä uutta täyttä linkityskierrosta, joten tämä on hienosäätöä.

**Kannibalisointia ei testattu.** Hakutulosten päällekkäisyysvertailua ei ajettu yhdellekään epäillylle parille (`hiljainen-irtisanominen`/`hiljainen-irtisanoutuminen`, `trollaus`/`trollin-ruokkiminen`, `draamakolmio`/`voittajakolmio`/`roolinvaihto`). Työelämän ja Roolit-kategorian otsikot koostuvat omien alasivujensa nimistä, mikä on riski, mutta sekin on testaamatta.

**Aukot, joita ei ole omistajan suunnitelmassa:** *pluralistinen tietämättömyys* (määritelty kahdella sivulla, ei omaa sivua) ja *ryhmäajattelu* (sama).

---

## 9. Backlinkit

**Saapuvat linkit: ei mitattavissa.** Moz- ja Bing-avaimia ei ole, joten viittaavia verkkotunnuksia, ankkuritekstejä tai linkkien laatua ei saatu. Halvin tapa on Search Consolen Linkit-raportin vienti tai Bing Webmaster Tools (ilmainen).

**Common Crawl ei tunne sivustoa.** Verkkotunnusta ei ole kahdessa uusimmassa verkkograafissa (kesä–elokuu ja heinä–syyskuu 2026), eikä sivustosta ole yhtään tallennetta neljässä tarkistetussa indeksissä. CCBotia ei ole estetty, joten sivustoa ei vain ole vielä haettu. Common Crawl on yleinen kielimallien koulutusaineiston lähde, joten tämä kannattaa tarkistaa uudelleen muutaman kuukauden päästä.

**Lähtevät linkit: 8 rikki 190:stä** (jokainen tarkistettu kahdesti, 404):

| Sivu | Rikkinäinen kohde |
|---|---|
| `branditurvallisuus` | en.wikipedia.org/wiki/Demonetization_(YouTube) |
| `huonojen-uutisten-hautaaminen` | en.wikipedia.org/wiki/News_dump |
| `klikkiotsikko` | en.wikipedia.org/wiki/Information_gap_theory_of_curiosity |
| `negatiivinen-korkoa` | en.wikipedia.org/wiki/Debt_spiral |
| `tilipuristus` | en.wikipedia.org/wiki/Pay_compression |
| `simple-sabotage` | cia.gov/…/SimpleSabotage.pdf |
| `urheilupesu` | amnesty.org/…/saudi-arabia-2034-world-cup-bid-evaluation… |
| `lapi-hinnalla-milla-hyvansa` | raitiotieallianssi.fi/tiedotteet/… |

Lisäksi kaksi ei vastannut lainkaan: `caltech.edu` (`rituaalinen-raportointi`) ja `bcaction.org` (`pinkkipesu`). Kolme palauttaa 403 roboteille mutta toimii selaimessa (theatlantic.com, sourcewatch.org, ssrn.com). Kaikissa 203 ulkoisessa linkissä on `rel="noopener"`.

**Realistiset linkkilähteet:** Vedätys-peli opettajien materiaalipankkeihin ja medialukutaitosivustoille; suomenkielisen Wikipedian ulkoiset linkit keskustelusivujen kautta; yliopistojen kurssisivut ja kirjastojen oppaat kategoriasivuihin; faktantarkistajat ja toimittajat trollaus- ja huijauskategorioihin.

---

## Mitä ei mitattu

- **Kenttädata:** CrUX, INP ja todellisten käyttäjien CLS. Vaatii Google-rajapinnan avaimen.
- **Google-sijoitukset ja klikit:** Search Console -rajapintaa ei ole kytketty, eikä lokakuun vientiä ole repossa. 13.8. ja 4.9. tehtyjen otsikkomuutosten vaikutus on siis mittaamatta.
- **Suomalaiset hakutulossivut:** ks. On-page-osion rajaus.
- **Kannibalisointi:** ei testattu.
- **Saapuvat linkit ja sivuston ulkopuoliset maininnat.**
- **Suorituskyky** Mermaid-, kaavio-, kategoria- ja pelisivuilla sekä työpöydällä.
- **Oikeinkirjoitus:** suomen morfologista tarkistinta ei ollut; kielihuomiot perustuvat lukemiseen.

## Menetelmä

Sivusto haettiin 4.10.2026 viidellä rinnakkaisella pyynnöllä ja sekunnin viiveellä; `robots.txt` sallii kaiken. Sivukohtaiset tiedot purettiin skriptillä kaikista 185 sivusta. Kymmenen erikoisagenttia analysoi saman tilannekuvan. Agenttien keskeiset väitteet tarkistettiin erikseen ennen raporttiin vientiä, ja yksi hylättiin (`harmaa-kivi.html`:n "sinä sinä aikana" on kieliopillisesti oikein). Näyttökuvat ovat kansiossa `screenshots/`.
