# Muutosloki — Ilmiöitä (www.ilmiöt.fi)

## 28.7.2026 — GSC-auditin korjaukset P1–P4

Search Console -auditin (`GSC-AUDIT-2026-07-28.md`) neljä ensimmäistä
prioriteettia toteutettu. Lähtötaso 18.6.–25.7.2026: 19 klikkiä, 1 419
näyttöä, CTR 1,34 %, keskisijoitus 11,1.

### P3 — Murupolku osoitti etusivulle, ei kategoriasivulle

Merkittävin yksittäinen korjaus. Kaikilla 108 ilmiösivulla murupolun toinen
taso osoitti etusivun ankkuriin (`https://www.ilmiöt.fi/#pesut-ja-...`), jonka
Google tulkitsee samaksi sivuksi kuin etusivun — murupolku oli käytännössä
"Etusivu › Etusivu › Ilmiö". Kategoriasivut julkaistiin 21.7.2026, joten oikea
kohde oli olemassa mutta jäi käyttämättä. Tämä on todennäköisin syy siihen,
miksi GSC:n Search appearance -raportti on täysin tyhjä.

`scripts/korjaa_murupolku.py` (uusi, idempotentti) korjasi kaksi asiaa, jotta
rakenteinen data vastaa näkyvää sisältöä:

| Kohde | Ennen | Nyt |
|---|---|---|
| JSON-LD `BreadcrumbList` taso 2 | `/#pesut-ja-maineenhallinta` | `/kategoria-pesut-ja-maineenhallinta.html` |
| Näkyvä murupolku | `<span class="kortti-breadcrumb-kat">` (ei linkki) | `<a href="kategoria-...html">` |

108 sivua, 108 JSON-LD-itemiä, 108 näkyvää linkkiä. Sivutuotteena jokainen
kategoriasivu sai 3–20 uutta sisältölinkkiä — ne olivat julkaisunsa jälkeen
keränneet 0 näyttökertaa.

### P1 — Sisääntulevat sisäiset linkit kärkisivuille

Auditin havainto: sivut, jotka jumittavat sijoituksilla 7–11, olivat myös
sisäisesti alilinkitettyjä. `darvo.html` (sija 4,2, CTR 10,7 %, 63 % koko
sivuston klikeistä) sai 11 sisääntulevaa linkkiä, `hyvesignalointi.html`
(sija 10,5, 0 klikkiä) vain 4 — joista 2 automaattista.

`scripts/lisaa_sisalinkit.py` (uusi) lisäsi 19 linkkiä 18 sivulle; lähdesivut
valittu käsin aihepiirin mukaan. Kortit rakensi `build_liittyvat.py`.

| Kohde | Näytöt | Sijoitus | Linkit ennen → nyt |
|---|---|---|---|
| hyvesignalointi.html | 115 | 9,79 | 4 → 9 |
| rage-bait.html | 86 | 10,98 | 6 → 10 |
| ai-slop.html | 117 | 9,08 | 9 → 12 |
| whataboutismi.html | 228 | 10,00 | 7 → 11 |
| brandolinin-laki.html | 69 | 7,43 | 8 → 10 |

Lisäksi `kuollut-kissa.html`:n leipätekstin ainoa linkittämätön ilmiömaininta
(`whataboutismi`) muutettiin linkiksi.

### P4 — robots.txt:n sitemap-rivi punycodeksi

`https://www.ilmiöt.fi/sitemap.xml` → `https://www.xn--ilmit-mua.fi/sitemap.xml`.
Google hyväksyy molemmat, muut robotit eivät välttämättä.

### P2 — Klusterisivut julkaistu: 108 → 113 ilmiötä

Viisi uutta sivua tukemaan kahden kärkisivun (hyvesignalointi, rage bait)
sijoitusta. Sivun pituusnormia (~260 sanaa) ei rikota — keskussivun sijaan
kasvatetaan sen ympärillä olevaa klusteria. 263–297 sanaa/sivu.

| Nro | Sivu | Alkuperäistermi | Kategoria |
|---|---|---|---|
| 93 | Klikkiotsikko | clickbait | Alustatalous ja algoritmit (8 → 10) |
| 94 | Engagement bait | engagement bait | Alustatalous ja algoritmit |
| 98 | Sinipesu | bluewashing | Pesut ja maineenhallinta (3 → 6) |
| 99 | Urheilupesu | sportswashing | Pesut ja maineenhallinta |
| 100 | Pinkkipesu | pinkwashing | Pesut ja maineenhallinta |

Numerot 1–94 säilyivät ennallaan; vain 16 sivua numeroitiin uudelleen
(95–113). Julkaisun teki uusi `scripts/lisaa_ilmiot.py` — peilikuva
`poista_ilmio.py`:lle: se siirtää luonnokset juureen (noindex pois,
`../`-polut suoristetaan), lisää hub-kortin oikean kategorian sisään,
numeroi kaikki uudelleen ja rakentaa IDS-taulukot, PREV/NEXT-ketjun ja
selausnapit. Kuivaharjoitus oletuksena, kirjoitus `--kirjoita`-lipulla.

**Ristiinlinkitys.** Luonnokset linkittivät vain ulospäin, joten klusteri
olisi jäänyt yksisuuntaiseksi. `lisaa_sisalinkit.py` sai toisen aallon
(`KLUSTERI`): 19 paluulinkkiä 13 vakiintuneelta sivulta. Molemmat kolmikot
linkittyvät nyt keskenään täydellisesti:

- **Pesu-kolmikko** sinipesu ↔ urheilupesu ↔ pinkkipesu
- **Syöttiperhe** rage bait ↔ klikkiotsikko ↔ engagement bait

Uusilla sivuilla on 4–5 sisääntulevaa liittyvat-linkkiä + etusivu +
kategoriasivu + selausnapit. Korttimäärä pysyi vaihteluvälissä 3–7.

**Kategoriasivut kirjoitettu uusiksi.** Molempien kategorioiden proosa puhui
vanhoista määristä ("Kolme muotoa", "Kahdeksan ilmiötä"), joten
`kategoriat/*.md` päivitettiin ja sivut generoitiin uudelleen:

- Alustatalous: "Kolme kerrosta" → **"Neljä kerrosta"**, uusi taso *Miten
  huomio otetaan* esittelee kolme syöttiä yhtenä perheenä (uteliaisuus /
  suuttumus / suora pyyntö).
- Pesut: "Kolme muotoa" → **"Neljä muotoa"**, uusi kappale *Vastuu ja
  symbolit* kolmelle uudelle pesulle — ne lainaavat uskottavuuden
  kolmannelta osapuolelta, mikä erottaa ne viher- ja tekoälypesusta.

**Nimivalinnat:** sinipesu, urheilupesu ja pinkkipesu seuraavat sivuston
omaa viherpesu/tekoälypesu-mallia; klikkiotsikko on vakiintunut suomi;
engagement bait jätettiin englanniksi kuten rage bait ja AI slop.
Englanninkielinen termi on joka sivun ingressissä, joten molemmat
hakutermit ovat katettuja.

### Luonnoskansio uudelleennimetty

`luonnokset-uudet/` → **`luonnokset-media/`** (16 tiedostoa). Kansio sisältää
Media ja julkisuus -kategorian (13.) luonnokset 109–118. Huom: mukana on myös
neljä muuta luonnosta, jotka eivät kuulu media-kategoriaan —
`lapi-hinnalla-milla-hyvansa`, `lukittu-paatos`, `paatosperainen-todistelu`,
`strateginen-aliarviointi`. Ne käydään läpi myöhemmin.

## 27.7.2026 — Kaikki kolmannen osapuolen resurssit itsehostattu

Sivusto ei enää lataa mitään ulkopuoliselta palvelimelta. Aiemmin jokainen kävijä
paljasti IP-osoitteensa ja selaamansa sivun kahdelle ulkopuoliselle: jsDelivrille
(Fastly/Cloudflare) ja Google Fontsille. Todennettu headless-selaimella
(Chromium/Playwright): 9 eri tyyppistä sivua, **0 ulkoista pyyntöä, 0 konsolivirhettä**.

### Uudet paikalliset JS-kirjastot (`js/`)
| Tiedosto | Versio (kiinnitetty) | Koko | Käytössä |
|---|---|---|---|
| `js/chart.umd.min.js` | Chart.js **4.5.1** | 204 kB | 3 sivua |
| `js/mermaid.min.js` | Mermaid **11.16.0** | 3,5 MB | 89 sivua |

Aiemmin molemmat haettiin `cdn.jsdelivr.net`istä versioalueella `@4` / `@11`, eli
kirjaston sisältö saattoi vaihtua ilman että sivustolla muutettiin mitään. Nyt
versio on kiinnitetty. Mermaid ladataan yhä laiskasti (IntersectionObserver, vasta
kun kaavio tulee näkyviin), joten 3,5 MB ei rasita sivuja joilla ei ole kaaviota.
Mermaid 11.16.0:sta ei ole kevyempää `tiny`-buildia; sivustolla käytetään vain
`flowchart`-kaavioita (88 kpl).

### Google Fonts poistettu — kaikki fontit paikallisia
`style.css` rivi 1 sisälsi `@import url('https://fonts.googleapis.com/css2?...')`,
joka koski **kaikkia 120 sivua**, jotka linkittävät `style.css`:n. Hakemistossa
`fonts/` oli ennestään vain DM Sans (400/500/600) ja Spectral (600/700), eikä
`fonts.css` ollut linkitettynä kuin 90 sivulla — leipätekstifontti **Source Sans 3
ei ollut itsehostattu lainkaan**.

- Ladattu puuttuvat: Source Sans 3 (muuttujafontti, painot 200–900, yksi tiedosto
  per osajoukko) sekä Spectral 400 ja Spectral 400 kursiivi. Osajoukot `latin` ja
  `latin-ext`, formaatti woff2, lisenssi SIL OFL 1.1.
- `fonts/fonts.css` koottu uudelleen: 16 `@font-face`-lohkoa, kaikki kolme perhettä.
- `style.css` rivi 1: `@import url('fonts/fonts.css')`. Yksi muutos kattaa kaikki
  sivut, joten sivukohtaisia `<link>`-lisäyksiä ei tarvittu.

### CSS cache-bust
`style.css` muuttui → `?v=20260721` → **`?v=20260727`** kaikilla 120 sivulla.

## 13.7.2026 — Vastakeino-audit (aallot 1–4) + Google-snippet-korjaus

**Lähtötilanne:** Etusivu lupaa, että jokainen artikkeli kertoo 1) mistä ilmiössä on
kyse, 2) miten se toimii käytännössä ja 3) miten siltä suojaudutaan. Auditointi
(12.7.2026) osoitti, että lupaus piti vain 84/106 artikkelissa. Korjaukset tehtiin
neljänä aaltona; täysi seuranta ja artikkelikohtaiset muutokset:
`artikkelein_sisaltolustaus_not_article.html` (noindex-sivu repon juuressa).

### Aalto 1 — puuttuvat vastakeinot (8 artikkelia)
Uusi vastakeino-loppuosio (huomiolaatikko ennen "Lue lisää" -osiota) artikkeleihin:
Overton-ikkuna (3), Valta suojelee valtaa (6), Simple sabotage (36), Catch-22 (38),
Performatiivinen läsnäolo (41), Initiointirituaalit (43), Brooksin laki (50),
Korkoa korolle (58).

### Aalto 2 — ohuet/väärin sijoitetut vastakeinot (14 artikkelia)
Olemassa oleva aines nostettu omaksi loppuosioksi ja konkretisoitu:
Starve the beast (2), Rautainen laki (5), Manufactured consent (12),
Inokulointiteoria (14), Backfire effect (22), Halo-efekti (24),
Omenoita ja appelsiineja (26), Goodhartin laki (39), Rituaalinen raportointi (42),
Kuolonmarssi (53), Tekninen velka (54), Conwayn laki (55), Korkokierre (60),
Hiljainen irtisanoutuminen (96).

### Aalto 3 — suppeiden laajennus + otsakeyhtenäistys
- Käytännön esimerkit lisätty: Paskuuttaminen (1), Yhdeksän-yhdeksän-sääntö (51),
  Hofstadterin laki (52).
- Kuolonmarssiin (53) lisätty mermaid-kierre-kaavio + puuttunut mermaid-lataajaskripti.
- Loppuosioiden geneeriset otsakkeet ("Tunnistaminen", "Miten tunnistat",
  "Tunnistaminen ja torjunta", "Vastakeino(t)", "Vastalääke/-lääkkeet") yhtenäistetty
  muotoon **"Tunnistaminen ja vastakeinot"** 53 sivulla. Kohdennetut otsakkeet
  (esim. "Vastakeinot projektijohdolle", "Suojaudu kierteeltä") jätettiin ennalleen.

### Google-snippet-korjaus (kaikki 106 artikkelia)
Meta-kuvaukset olivat koneellisesti katkaistuja lauseenpätkiä ("…"-loppuisia), joten
Google hylkäsi ne ja poimi hakutuloskorttiin satunnaista tekstiä sivulta. Jokaiselle
artikkelille kirjoitettiin oma ~150 merkin kuvaus kaavalla *koukku + "selitämme mistä
on kyse, miten se toimii käytännössä ja miten suojaudut"*. Sama teksti vietiin
kolmeen tagiin: `description`, `og:description`, `twitter:description`.
Snippetit päivittyvät, kun Google indeksoi sivut uudelleen (Search Consolen
uudelleenindeksointipyyntö nopeuttaa).

### Aalto 4 — julkaisu
- Muokatuille sisältösivuille päivitetty bylinen "Päivitetty"-päiväys ja JSON-LD:n
  `dateModified` (pelkän otsakkeen vaihtaneille sivuille ei).
- Hakuindeksi ajettu: `scripts/build_search_index.py` → `search-index.js` (106 sivua).
- Kaikki mergetty main-haaraan ja julkaistu; live varmistettu curlilla.

**Lopputulos:** etusivun lupaus pitää paikkansa kaikissa 106 artikkelissa.
