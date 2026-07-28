# UUDET JUTUT — suunnitelma uusista kategorioista ja ilmiöistä

Laadittu 2026-07-06. Lähtötilanne: 68 ilmiötä, 8 kategoriaa.
Tavoite: laajentaa sivustoa propagandatekniikoihin ja 2020-luvun ilmiöihin
**hakupotentiaali edellä** — eli tehdään ensin ne sivut, joilla on paras
suhde (suomenkielinen hakuvolyymi) / (kilpailun heikkous fi-SERPissä).

> **Tilanne 2026-07-06: Prioriteetti 1 julkaistu.** Sivustolla nyt 76 ilmiötä
> ja 11 kategoriaa. Uudet kategoriat: Alustatalous ja algoritmit (nrot 71–74),
> Pesut ja maineenhallinta (75) ja Työelämän ilmiöt (76). Whataboutismi meni
> Informaatio ja propaganda -kategoriaan (nro 15) ja shrinkflaatio
> Myyntikikkoihin (nro 70). Pesut ja Työelämä avattiin poikkeuksellisesti
> yhdellä kortilla — ne täydennetään vähintään kolmeen P2:n alussa.
>
> **P2 julkaistu 2026-07-07:** kaikki 15 sivua siirretty juureen ja koko sivusto
> numeroitu uudelleen kategorioittain — nyt 91 ilmiötä, 11 kategoriaa.
> index.html, llms.txt, sitemap.xml, tietoa.html ja hakuindeksi päivitetty.
> `luonnokset/`-kansio jäi turhaksi, sen voi poistaa. Seuraavaksi: deploy +
> live-tarkistus (deploy-gap!), sitten P3.
>
> **P3:n ensimmäinen erä julkaistu 2026-07-10 — nimetyt lait.** Seitsemän sivua:
> Brandolinin laki (19), Poen laki (20), Godwinin laki (21), Hanlonin partaveitsi (34),
> Occamin partaveitsi (35), Parkinsonin laki (48), Peterin periaate (49). Koko sivusto
> numeroitu uudelleen — nyt **98 ilmiötä, 11 kategoriaa**. Uusia kategorioita ei
> avattu: lait sijoittuivat kolmeen olemassa olevaan kategoriaan.
> Vanhoille sivuille lisättiin 21 sisääntulevaa linkkiä uusiin.
> `scripts/build_liittyvat.py`:n korttimäärän assertointi nostettu 91 → 98.
> Seuraavaksi: deploy + live-tarkistus (deploy-gap!), sitten P3:n loput.

---

## Priorisointiperusteet

Jokainen ehdokas on arvioitu neljällä kriteerillä:

1. **Volyymi** — kuinka paljon termiä (ja sen "mikä on X" -muunnelmia) haetaan suomeksi.
2. **Kilpailu** — mitä fi-SERPissä on nyt: tyhjää, pelkkä Wikipedia-tynkä, vai Ylen/HS:n evergreen-artikkeleita.
3. **Kesto** — evergreen-termi vs. uutissyklin mukana kuoleva muotisana.
4. **Synergia** — tukeeko sivu sisäistä linkitystä ja kategorian avaamista.

Sivuston vahvuus on "mikä on X ja miksi se toimii" -selityssivut. Paras
voitettava maasto on **termi, jonka ihmiset kuulevat mediasta ja googlaavat,
mutta jolle ei ole kunnollista suomenkielistä selityssivua** (vain Wikipedia-tynkä
tai vanhenevia uutisjuttuja).

Volyymi- ja kilpailuarviot ovat suuntaa-antavia (ei keyword-dataa ajettu).
Ne voi validoida DataForSEO:lla tai julkaisun jälkeen GSC:stä — mutta
prioriteettijärjestys tuskin muuttuu dramaattisesti.

---

## Prioriteetti 1 — ✅ JULKAISTU 2026-07-06

Kaikki 8 sivua tuotannossa. Ilmiönumerot: whataboutismi 15, shrinkflaatio 70,
doomscrolling 71, kaikukammio 72, AI slop 73, parasosiaalinen suhde 74,
viherpesu 75, hiljainen irtisanoutuminen 76.

| # | Ilmiö | Slug | Kategoria | Päähakusanat | Volyymi | Kilpailu | Miksi kärkeen |
|---|-------|------|-----------|--------------|---------|----------|---------------|
| 1 | Viherpesu | `viherpesu.html` | Pesut (uusi) | viherpesu, mikä on viherpesu, viherpesu esimerkkejä, greenwashing suomeksi | **Korkea** — vakiintunut suomen sana, tasainen kysyntä | Kohtalainen (Wikipedia, järjestösivut, uutisjutut — ei yhtä hyvää selityssivua) | Suurin yksittäinen volyymi koko listalla; EU:n viherväiteasetus pitää aiheen pinnalla vuosia |
| 2 | Hiljainen irtisanoutuminen | `hiljainen-irtisanoutuminen.html` | Työelämä (uusi) | hiljainen irtisanoutuminen, quiet quitting, quiet quitting suomeksi | **Korkea** — tunnetuin 2020-luvun työelämätermi | Kohtalainen (2022–23 uutisjutut vanhenevat, evergreen-selitys puuttuu) | Kaksi hakutermiä (fi+en) samalle sivulle; kysyntä jatkuu joka työmarkkinasyklissä |
| 3 | Doomscrolling | `doomscrolling.html` | Alustatalous (uusi) | doomscrolling, doomscrollaus, miten lopettaa doomscrolling | Keskikorkea, tasainen | **Matala** — muutama uutisjuttu, ei selityssivua | Paras volyymi/kilpailu-suhde; avaa alustakategorian |
| 4 | Whataboutismi | `whataboutismi.html` | Informaatio ja propaganda | whataboutismi, whataboutism suomeksi, entäs-argumentti | Keskitaso, tasainen | **Matala** — käytännössä vain Wikipedia | Propagandateeman kärki; ajankohtaistuu jokaisissa vaaleissa |
| 5 | Shrinkflaatio | `shrinkflaatio.html` | Myyntikikat ja painostus | shrinkflaatio, shrinkflation, kutistuskikkailu, pakkauskoko pienentynyt hinta sama | Keskitaso + toistuvat uutispiikit | **Matala** — uutisjuttuja, ei pysyvää selityssivua | Jokainen inflaatiouutinen tuo hakupiikin; sivu on valmiina odottamassa |
| 6 | Kaikukammio | `kaikukammio.html` | Alustatalous (uusi) | kaikukammio, kaikukammioilmiö, filtterikupla, sosiaalinen media kupla | Keskitaso, tasainen | Kohtalainen (mediakasvatussivut) | Kysytään kouluissa ja mediassa jatkuvasti; vahva sisäinen linkityskohde |
| 7 | AI slop | `ai-slop.html` | Alustatalous (uusi) | ai slop, ai slop suomeksi, mikä on ai slop | Nouseva (2024–) | **Lähes nolla** suomeksi | First mover -tilaisuus: termille ei ole vielä suomenkielistä selityssivua — tämä sivu voi olla se (termi pidetään englanniksi, ei keksittyä suomennosta) |
| 8 | Parasosiaalinen suhde | `parasosiaalinen-suhde.html` | Alustatalous (uusi) | parasosiaalinen suhde, parasosiaalisuus, parasosiaalinen suhde tarkoittaa | Nouseva (influensserikulttuuri) | Matala–kohtalainen | Kytkeytyy suoraan pig butchering- ja finfluencer-huijauksiin → hyvä ristilinkitys |

**P1 avaa kaksi uutta kategoriaa** (Alustatalous 4 kortilla, ks. julkaisuerät alla)
ja täydentää kahta olemassa olevaa.

---

## Prioriteetti 2 — ✅ JULKAISTU 2026-07-07

Kaikki 15 sivua tuotannossa. Ilmiönumerot: Streisand-ilmiö 16, trollitehdas 17,
kuollut kissa 18, Dunning–Kruger 30, QR-koodihuijaus 62, toimitusjohtajahuijaus 63,
rug pull 64, suunniteltu vanheneminen 78, tilausansa 79, kuollut internet 84,
rage bait 85, tekoälypesu 87, hyvesignalointi 88, hiljainen irtisanominen 90,
haamutyöpaikat 91. Tehdyt valinnat:
suunniteltu vanheneminen sijoitettiin Myyntikikat ja painostus -kategoriaan
(Kasvun dynamiikka pysyy korkoteemaisena) ja raivosyötti kulkee vakiintuneella
englanninkielisellä nimellä **rage bait** (slug `rage-bait.html`).

| Ilmiö | Slug-ehdotus | Kategoria | Päähakusanat | Arvio |
|-------|--------------|-----------|--------------|-------|
| Dunning–Kruger-ilmiö | `dunning-kruger.html` | Psykologia ja kognitio | dunning kruger, dunning kruger ilmiö | Iso volyymi mutta kova kilpailu — tehdään, koska pitkä häntä ("dunning kruger esimerkki työelämä") on voitettavissa ja sivu on sisäisen linkityksen solmukohta |
| Suunniteltu vanheneminen | `suunniteltu-vanheneminen.html` | Kasvun dynamiikka / Myyntikikat | suunniteltu vanheneminen, planned obsolescence | Vakiintunut termi, kohtalainen volyymi, kilpailu ohuehko |
| Tekoälypesu (AI-washing) | `tekoalypesu.html` | Pesut (uusi) | ai washing, tekoälypesu | Nouseva, lähes nollakilpailu; SEC:n 2024-sakot antavat konkretian |
| Hyvesignalointi | `hyvesignalointi.html` | Pesut (uusi) | hyvesignalointi, virtue signaling suomeksi | Keskitaso, matala kilpailu |
| Kuollut internet -teoria | `kuollut-internet.html` | Alustatalous | kuollut internet teoria, dead internet theory | Nouseva meemi-ilmiö, lähes nollakilpailu suomeksi |
| Raivosyötti (rage bait) | `rage-bait.html` | Alustatalous | rage bait, ragebait suomeksi | Nouseva nuoremmissa ikäluokissa, nollakilpailu |
| Streisand-ilmiö | `streisand-ilmio.html` | Informaatio ja propaganda | streisand ilmiö, streisand efekti | Pieni mutta ikivihreä; heikko kilpailu |
| Trollitehdas | `trollitehdas.html` | Informaatio ja propaganda | trollitehdas, trolliarmeija | Uutisvetoinen mutta toistuva; astroturfin sisarsivu |
| Kuollut kissa -strategia | `kuollut-kissa.html` | Informaatio ja propaganda | kuollut kissa strategia, dead cat strategy | Niche mutta nollakilpailu; ajankohtaistuu skandaalien yhteydessä |
| Tilausansa | `tilausansa.html` | Myyntikikat ja painostus | tilausansa, tilauksen peruminen vaikeaa, subscription trap | Kuluttaja-aihe, tasainen kysyntä, matala kilpailu |
| QR-koodihuijaus (quishing) | `qr-koodihuijaus.html` | Huijaukset ja petokset | qr koodihuijaus, quishing, qr koodi huijaus parkkimaksu | Poliisin varoitukset tuovat toistuvia piikkejä; matala kilpailu |
| Toimitusjohtajahuijaus (BEC) | `toimitusjohtajahuijaus.html` | Huijaukset ja petokset | toimitusjohtajahuijaus, ceo fraud, laskutushuijaus | Vakiintunut poliisin termi; deepfake-kulma tekee ajankohtaiseksi |
| Rug pull | `rug-pull.html` | Huijaukset ja petokset | rug pull, rug pull krypto | Kryptoyleisö, matala kilpailu suomeksi |
| Hiljainen irtisanominen (quiet firing) | `hiljainen-irtisanominen.html` | Työelämä (uusi) | hiljainen irtisanominen, quiet firing, savustaminen | Quiet quittingin peilikuva — luonteva pari P1:n #2:lle |
| Haamutyöpaikat (ghost jobs) | `haamutyopaikat.html` | Työelämä (uusi) | ghost jobs, haamutyöpaikka, valetyöpaikkailmoitus | Nouseva 2023–, nollakilpailu suomeksi |

---

## Prioriteetti 3 — pitkä häntä ja kategorioiden täydennys

Matala volyymi, mutta halpoja tehdä ja vahvistavat kokonaisuutta
(sisäinen linkitys, kategorioiden uskottava koko, "koko sanaston kattava
lähde" -asema AI-hauissa):

**Erä "nimetyt lait" — ✅ JULKAISTU 2026-07-10.** Brandolinin laki, Poen laki,
Godwinin laki, Hanlonin partaveitsi, Occamin partaveitsi, Parkinsonin laki,
Peterin periaate. Erä jatkaa sivuston olemassa olevaa lakikokoelmaa
(Betteridge, Brooks, Conway, Goodhart, Hofstadter, rautainen laki).
Vahva ristiinlinkitys: Hanlon ↔ strateginen osaamattomuus, Parkinson ↔
bikeshedding (= Parkinsonin oma triviaalisuuden laki), Brandolini ↔
argumenttitulva ja AI slop, Peter ↔ HiPPO-efekti ja Dunning–Kruger.

Vielä tekemättä:

- **Propaganda:** suuri valhe, peilisyytös (accusation in a mirror),
  refleksiivinen kontrolli, hyödyllinen idiootti, motte ja bailey,
  sealioning, moraalipaniikki, hostile media effect
- **Alustatalous:** algoritminen radikalisoituminen, audience capture,
  valearvostelut / review bombing, engagement farming
- **Työelämä:** zoom-väsymys, hustlekulttuuri
- **Pesut:** urheilupesu (sportswashing), pinkkipesu
- **Myyntikikat:** tippahinnoittelu (drip pricing), FOMO-markkinointi,
  dynaaminen hinnoittelu, loot boxit
- **Psykologia:** saatavuusheuristiikka
- **Kasvun dynamiikka:** Gartnerin hypekäyrä, verkostovaikutus

Brandolinin laki nostettiin P3:n kärkeen sivuston hengen takia, vaikka
volyymi on pieni — se on luonteva linkityskohde lähes joka propagandasivulta.
Se veti perässään koko "nimetyt lait" -erän (ks. yllä).

---

## Uudet kategoriat ja julkaisuerät

Kategoria avataan vasta kun sillä on vähintään 3–4 korttia (Kasvun
dynamiikka on nyt 3 kortilla sivuston ohuin — ei tehdä ohuempia).
Sivut julkaistaan erissä, jotta index, llms.txt ja numerointi
päivitetään kerralla eikä kortteja siirrellä kategoriasta toiseen
jälkikäteen:

| Erä | Avaa/täydentää | Sisältö | Tila |
|-----|----------------|---------|------|
| **A** | Uusi kategoria: **Alustatalous ja algoritmit** | doomscrolling, kaikukammio, AI slop, parasosiaalinen suhde | ✅ Julkaistu 2026-07-06 |
| **B** | Uusi kategoria: **Pesut ja maineenhallinta** | viherpesu, tekoälypesu, hyvesignalointi | ✅ Julkaistu 2026-07-07 (3 korttia) |
| **C** | Täydennys: **Informaatio ja propaganda** | whataboutismi, Streisand-ilmiö, trollitehdas, kuollut kissa | ✅ Julkaistu 2026-07-07 |
| **D** | Uusi kategoria: **Työelämän ilmiöt** | hiljainen irtisanoutuminen, hiljainen irtisanominen, haamutyöpaikat | ✅ Julkaistu 2026-07-07 (3 korttia) |
| **E** | Täydennykset olemassa oleviin | shrinkflaatio, tilausansa, QR-koodihuijaus, toimitusjohtajahuijaus, rug pull, Dunning–Kruger, suunniteltu vanheneminen, kuollut internet, rage bait | ✅ Julkaistu 2026-07-07 |

**Seuraava työjärjestys:** P2 ja P3:n "nimetyt lait" -erä on julkaistu —
seuraavaksi deploy ja live-tarkistus, sitten P3:n loput (ks. alla).

Kategoriakuvaukset (hub-kat-desc) luonnoksina:

- **Alustatalous ja algoritmit:** "Miten suosittelualgoritmit, ansaintalogiikka
  ja huomiotalous muokkaavat käyttäytymistä verkossa."
- **Pesut ja maineenhallinta:** "Viherpesusta tekoälypesuun — miten maine
  kiillotetaan ilman että mikään oikeasti muuttuu."
- **Työelämän ilmiöt:** "Etätyöajan uusi sanasto: hiljaiset irtisanoutumiset,
  haamutyöpaikat ja läsnäolon teatteri."

---

## Sivukohtainen SEO-resepti

Jokainen uusi sivu kohdistetaan "mikä on X" -hakuihin:

- **Title:** `Termi — lyhyt suomenkielinen selite — Ilmiöitä` (vakiintunut muoto)
- **H1 + ingressi:** sekä suomenkielinen että englanninkielinen termi heti
  alkuun (esim. "Shrinkflaatio (shrinkflation) tarkoittaa…") — sivu
  tavoittaa molemmat hakutermit
- **Rakenne:** määritelmä ensin (AI-siteerattavuus), sitten mekanismi,
  tunnistaminen, esimerkit, vastakeinot — kysymysmuotoisia H2:ia
  ("Miten X tunnistaa?") long tail -hakuja varten
- **Sisäinen linkitys:** vähintään 2–3 linkkiä aiheeseen liittyviltä
  vanhoilta sivuilta uudelle sivulle (esim. parasosiaalinen suhde ←
  pig-butchering, kaarmeoljy; whataboutismi ← argumenttitulva, darvo)
- **Meta description** ≤ 160 merkkiä, canonical `https://www.ilmiöt.fi/slug.html`

## Tekninen muistilista per erä

1. Luo sivut olemassa olevan sivun pohjalta (esim. `astroturf.html`) —
   samat og-tagit, JSON-LD (tekijä Ilmiömies, julkaisija Ilmiöitä)
2. Lisää hub-kortit `index.html`:ään (uusi kategoria: oma
   `hub-kat-label` + `hub-kat-desc` + `hub-kortit`-div; värikoodi `--c`)
3. Päivitä `llms.txt` (kategoria + ilmiömäärä otsikossa: "68 ilmiötä" → uusi luku)
4. Päivitä `sitemap.xml` (uudet urlit + lastmod)
5. Aja `scripts/build_search_index.py` ja committaa `search-index.js`
6. Tarvittaessa og-kuvat: `scripts/generate_og_images.py`
7. `/tarkista-kirjoitus` jokaiselle uudelle sivulle ennen julkaisua
8. Deployn jälkeen: varmista curlilla että live vastaa lokaalia
   (deploy-gap on purrut ennenkin)

---

## Mittarit

Julkaisun jälkeen seurataan GSC:stä per sivu: impressiot 4 ja 12 viikon
kohdalla, klikit, keskimääräinen sijainti päätermillä. Jos P1-sivu ei
saa impressioita 4 viikossa, tarkista indeksointi (URL inspection)
ennen sisältömuutoksia. Arvioidut volyymit voi validoida etukäteen
DataForSEO-työkaluilla, jos halutaan varmistus ennen kirjoitustyötä.

---

## Media ja julkisuus — 13. kategoria (luonnokset 2026-07-28)

Lähtökohta: sivustolla on jo runsaasti media-lähisukuisia ilmiöitä
(manufactured consent 11, Betteridgen laki 12, kuollut kissa 17, astroturf 9,
firehose 10, trollitehdas 16, kaikukammio 88, rage bait 92), mutta ne ovat
hajallaan Informaatio ja propaganda- sekä Alustatalous-kategorioissa.
Käyttämätön maasto on nimenomaan **julkisuuden aukot**: miksi jostain ei
uutisoida ja miksi asia kerrotaan juuri niin kuin kerrotaan.

**Luonnokset kansiossa `luonnokset-media/` (numerot 109–118, alustavia):**

| Nro | Sivu | Alkuperäistermi | Miksi |
|-----|------|-----------------|-------|
| 109 | Uutiskynnys | news threshold / news values | Kategorian ankkurisivu; hyvä suomenkielinen hakutermi, fi-SERPissä vain sanakirjatasoa |
| 110 | Uutisautiomaa | news desert | Ajankohtainen, tutkimuspohja vahva (Abernathy; Gao–Lee–Murphy 2020) |
| 111 | Pääsyjournalismi | access journalism | Vastaa suoraan "miksi ei kysytä vaikeita" -kysymykseen |
| 112 | Tiedotejournalismi | churnalism | Kovat luvut (Cardiff 2008), linkittyy astroturfiin ja pesuihin |
| 113 | Bränditurvallisuus | brand safety | Moderni, konkreettinen; selittää demonetisoinnin ja kiertoilmaisut |
| 114 | Huonojen uutisten hautaaminen | burying bad news | Nimetty tapaus (Jo Moore 2001), erottuu kuolleesta kissasta |
| 115 | Väärä tasapaino | false balance / bothsidesism | Klassikko, puuttui kokonaan; pari konsensus-fetissille |
| 116 | Kehäraportointi | circular reporting / citogenesis | Jaettava esimerkki (Jarre-sitaatti 2009) |
| 117 | Gell-Mannin amnesia | Gell-Mann amnesia effect | Nimetty ilmiö, fi-SERP käytännössä tyhjä — sivuston ydinaluetta |
| 118 | Vihamielisen median harha | hostile media effect | Klassinen tutkimus (Vallone ym. 1985), selittää mediakritiikin symmetrian |

**Vaihe 2 -ehdokkaat** (ei vielä luonnoksia): vaientamiskanne (SLAPP),
hiljaisuuden spiraali, symbolinen näkymättömyys, natiivimainonta/advertoriaali,
ajatushautomon pesu, oikaisukuilu, sitogeneesi omana sivunaan, uutisvälttely,
ilkeän maailman oireyhtymä, kolmannen henkilön efekti, tunnistettavan uhrin
vaikutus, myötätuntoväsymys, kontekstin poisto, uutisen puoliintumisaika,
vaaleanpunainen lima -journalismi (nimeäminen auki).

**Päällekkäisyysriskit, jotka on hoidettava ristiinlinkityksellä:**
hiljaisuuden spiraali ↔ äänekäs vähemmistö (94), uutisvälttely ↔ doomscrolling (87),
ajatushautomon pesu ↔ astroturf (9), oikaisukuilu ↔ Brandolinin laki (18).

**Kategorian avaamisen sivuvaikutus:** jos Media ja julkisuus perustetaan,
sinne kannattaa siirtää ainakin kuollut kissa, Betteridgen laki,
manufactured consent ja portinvartija-kulttuuri — mikä tarkoittaa koko
sivuston uudelleennumerointia kuten P3:ssa, sekä uutta kategoriasivua
(`kategoria-media-ja-julkisuus.html`) 12 nykyisen rinnalle. Kategoriasivun
sisältötiedosto on jo tehty: `kategoriat/media-ja-julkisuus.md` (~550 sanaa
uniikkia proosaa), ja esikatselu `luonnokset-media/kategoria-media-ja-julkisuus.html`.
Julkaisussa sivun tekee `build_kategoriat.py media-ja-julkisuus` — massa-ajo
ohittaa kategorian siihen asti, koska sitä ei ole vielä index.html:ssä.
Samalla 12 nykyisen kategoriasivun laskurit muuttuvat muotoon `x / 13`.

**Generointi:** `scripts/build_media_luonnokset.py` (pohjana
`aanekas-vahemmisto.html`). Luonnoksissa on `noindex` ja `../`-etuliitteiset
polut; julkaistaessa molemmat puretaan ja ajetaan build_liittyvat.py,
paivita_maarat.py, build_sitemap.py ja build_search_index.py.
