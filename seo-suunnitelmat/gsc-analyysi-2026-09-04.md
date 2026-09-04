# Search Console -analyysi — www.ilmiöt.fi

**Data:** `datalake_analysis/04092026/` (Chart, Queries, Pages, Devices, Countries, Search appearance, Filters)
**Jakso:** 2026-06-18 – 2026-09-01 (GSC-suodatin "viimeiset 3 kk", haun tyyppi Web)
**Vertailuvienti:** `datalake_analysis/13082026/` (sama suodatin, jakso päättyi 12.8.)
**Aiemmat auditit:** `GSC-AUDIT-2026-08-13.md`, `GSC-AUDIT-2026-07-28.md`, `seo-suunnitelmat/gsc-analyysi-2026-07-25.md`
**Visuaalinen raportti:** https://claude.ai/code/artifact/b60cdc95-6e63-4eb4-a0e4-c8cdf693e81b
**Laadittu:** 4.9.2026

---

## 0. Kokonaisluvut

Sivuston koko jakso (Devices.csv ja Countries.csv täsmäävät):

| Mittari | Arvo |
|---|---|
| Näytöt | 9 062 |
| Klikit | 195 |
| CTR | 2,15 % |
| Keskisija | 8,56 |
| Suomen osuus näytöistä | 8 661 / 9 062 = 95,6 % |

**Huom.** `Pages.csv` summautuu eri lukuun (9 246 näyttöä, 197 klikkiä) kuin
`Devices.csv` / `Countries.csv` (9 062 / 195). Ero on GSC:n oma deduplikointi.
Käytä sivustotason lukuina Devices/Countries-arvoja ja sivutason vertailuissa
Pages-arvoja — älä sekoita niitä samaan laskuun.

---

## 1. Kehitys — kasvu on todellista

Laskettu suoraan `Chart.csv`:n päiväsarjasta, joten vertailujaksot eivät ole
päällekkäisiä (toisin kuin kumulatiiviset "viimeiset 3 kk" -viennit):

| Mittari | 8.7.–4.8. (28 pv) | 5.8.–1.9. (28 pv) | Muutos |
|---|---|---|---|
| Näytöt | 2 373 | **6 621** | +179 % |
| Klikit | 26 | **165** | +535 % |
| CTR | 1,10 % | **2,49 %** | +1,39 pp |
| Keskisija | 11,03 | **8,61** | −2,42 sijaa |

Kuukausitasolla:

| Kuukausi | Klikit | Näytöt | CTR | Keskisija |
|---|---|---|---|---|
| 2026-06 | 0 | 4 | 0 % | 6,33 |
| 2026-07 | 26 | 1 971 | 1,32 % | 11,51 |
| 2026-08 | 163 | 6 804 | 2,40 % | 8,74 |
| 2026-09 (1 pv) | 6 | 283 | 2,12 % | 9,30 |

**Nolla kadonnutta.** 13.8. → 4.9. -vertailussa kyselyitä tuli 103 lisää
(208 → 311) ja sivuja 32 lisää (114 → 146). Kummastakaan ei kadonnut yhtään
riviä. Indeksointi ja tekninen puoli ovat kunnossa; ongelma on sija.

Huomionarvoinen käänne: **viimeiset 14 pv olivat klikeissä edellisiä huonommat**
(76 vs. 89), vaikka näytöt kasvoivat (3 558 vs. 3 063). Kyse ei ole
heikkenemisestä vaan siitä, että kasvu tulee vyöhykkeeltä joka ei tuota klikkejä
(ks. luku 2). Elokuun 7. ja 24. päivän piikit ovat DARVO-piikkejä.

---

## 2. Tärkein löydös: sijakynnys on jyrkempi kuin aiemmin arvioitiin

`GSC-AUDIT-2026-08-13.md` sijoitti kynnyksen sijalle 5–7. Suuremmalla
aineistolla se on **noin sijalla 4**. Kyselytason jakauma (`Queries.csv`,
311 riviä, 5 099 näyttöä, 92 klikkiä):

| Sijavyöhyke | Kyselyitä | Näytöt | Osuus näytöistä | Klikit | CTR |
|---|---|---|---|---|---|
| 1,0–3,5 | 19 | 361 | 7,1 % | 54 | **14,96 %** |
| 3,5–5,0 | 12 | 82 | 1,6 % | 0 | 0 % |
| 5,0–8,0 | 50 | 1 910 | 37,5 % | 37 | 1,94 % |
| 8,0–11,0 | 54 | 1 828 | 35,9 % | 1 | **0,05 %** |
| 11,0–20,0 | 53 | 404 | 7,9 % | 0 | 0 % |
| yli 20 | 123 | 514 | 10,1 % | 0 | 0 % |

Sijoilla 5–11 on **73 % kaikista näytöistä** (3 780) ja niistä syntyy 38 klikkiä
eli 1,01 %. Sijoilla 8–11 koko sivusto sai 76 päivän jaksolla **yhden klikin**.

### DARVO-korjaus — tämä on se luku joka kannattaa muistaa

Vyöhykkeen 5,0–8,0 CTR (1,94 %) on lähes kokonaan DARVOn ansiota:

| Rajaus | Klikit | Näytöt | CTR |
|---|---|---|---|
| Kaikki kyselyt | 92 | 5 099 | 1,80 % |
| DARVO-kyselyt (7 kpl) | 80 | 448 | **17,86 %** |
| Kaikki muut (304 kpl) | 12 | 4 651 | **0,26 %** |
| Vyöhyke 5,0–8,0 ilman DARVOa | 11 | 1 729 | 0,64 % |
| Vyöhyke 5–11 ilman DARVOa | 12 | 3 599 | 0,33 % |

Sivutasolla `darvo.html` = 134 klikkiä 197:stä eli **68 %**. Keskittymä on
purkautunut hieman (13.8. se oli 71 %) mutta ei olennaisesti.

### Miksi tämä ei ole sisältöongelma

`darvo.html` on **396 sanaa** — pankin lyhyimpiä. Sillä on 10 sisääntulevaa
sisältölinkkiä, kun sivuston mediaani on 8. Se ei ole muita parempi sivu; se on
ainoa sivu sijalla 3,5, ja siellä se muuntaa 16,88 prosentilla.

Sisäisten linkkien ja sijan välillä **ei ole korrelaatiota** (mitattu: sisään
tulevat sisältölinkit vs. GSC-sija, 146 sivua). `rage-bait.html` on 15 linkillä
sijalla 8,24; `dunning-kruger.html` 6 linkillä sijalla 9,29. Sisäinen linkitys ei
ole enää pullonkaula — heinäkuun linkkityö on tehnyt tehtävänsä.

---

## 3. Missä näytöt hukkuvat

**113 kyselyä istuu sijoilla 5–11 ilman yhtäkään klikkiä. Yhteensä 2 646 näyttöä.**

| Kysely | Näytöt | Sija | Kohdesivu | Kilpailuluokka |
|---|---|---|---|---|
| hyvesignalointi | 474 | 7,10 | hyvesignalointi.html | Sanakirjatermi |
| dunning kruger | 225 | 9,54 | dunning-kruger.html | Media-termi |
| rage bait suomeksi | 199 | 9,36 | rage-bait.html | Media-termi |
| ragebait | 192 | 8,09 | rage-bait.html | Media-termi |
| dunning kruger ilmiö | 156 | 8,94 | dunning-kruger.html | Media-termi |
| hanlonin partaveitsi | 138 | 5,81 | hanlonin-partaveitsi.html | Sanakirjatermi |
| doomscrolling suomeksi | 129 | 5,30 | doomscrolling.html | Sanakirjatermi |
| parkinsonin laki | 86 | 10,93 | parkinsonin-laki.html | Sanakirjatermi |
| käärmeöljy | 85 | 9,99 | kaarmeoljy.html | **Vapaa termi** |
| sunk cost fallacy suomeksi | 65 | 9,25 | sunk-cost-harha.html | **Vapaa termi** |
| haloefekti | 63 | 6,86 | halo-efekti.html | Sanakirjatermi |
| doom scrolling suomeksi | 54 | 8,56 | doomscrolling.html | Sanakirjatermi |
| hyvesignalointi tarkoittaa | 52 | 9,00 | hyvesignalointi.html | Sanakirjatermi |
| bränditurvallisuus | 44 | 9,73 | branditurvallisuus.html | **Vapaa termi** |
| hyve signalointi | 42 | 10,29 | hyvesignalointi.html | Sanakirjatermi |
| uutiskynnys | 41 | 6,02 | uutiskynnys.html | **Vapaa termi** |
| whataboutismi suomeksi | 32 | 8,47 | whataboutismi.html | Sanakirjatermi |
| mikä on uutiskynnys | 30 | 9,23 | uutiskynnys.html | **Vapaa termi** |

Sivutasolla, yli 100 näyttöä ja alle 1 % CTR (sisälinkit = sisääntulevat
sisältölinkit, ei nav/footer; sanat = `<main>`-alueen sanamäärä):

| Sivu | Näytöt | Klikit | Sija | Sisälinkit | Sanat |
|---|---|---|---|---|---|
| rage-bait.html | 893 | 0 | 8,24 | 15 | 482 |
| hyvesignalointi.html | 856 | 0 | 7,55 | 12 | 504 |
| dunning-kruger.html | 685 | 0 | 9,29 | 6 | 596 |
| ai-slop.html | 597 | 5 | 7,51 | 15 | 539 |
| whataboutismi.html | 402 | 3 | 9,62 | 9 | 487 |
| doomscrolling.html | 370 | 0 | 7,18 | 9 | 439 |
| hanlonin-partaveitsi.html | 198 | 1 | 6,46 | 9 | 505 |
| bkt-harha.html | 166 | 1 | 19,19 | 9 | — |
| kaarmeoljy.html | 158 | 0 | 8,39 | 13 | 336 |
| kuollut-internet.html | 132 | 0 | 11,13 | 4 | — |
| parkinsonin-laki.html | 125 | 1 | 10,13 | 10 | 512 |
| hajota-hallitse.html | 107 | 0 | 10,11 | 7 | — |
| gaslighting.html | 104 | 0 | 22,12 | 9 | — |

Eniten sijaa parantaneet sivut jaksolla 13.8. → 1.9.:
`keskiarvo-vs-mediaani.html` −9,3 · `kategoria-psykologia-ja-kognitio.html` −8,4
(21,0 → 12,6, kategoriasivut alkavat vihdoin liikkua) · `gaslighting.html` −6,4 ·
`scope-creep.html` −5,9 · `bkt-harha.html` −5,9 · `halo-efekti.html` −3,6.

Huonontuneet: `shrinkflaatio.html` +4,4 · `betteridgen-laki.html` +3,1 ·
`brandolinin-laki.html` +1,9 (169 → 240 näyttöä, sija 6,04 → 7,91).

---

## 4. Kolme kilpailutilannetta, ei yhtä

Nollaklikkikyselyt eivät ole yksi ongelma. Jaon voi tehdä yhdellä kysymyksellä:
**onko termillä suomenkielinen Wikipedia-artikkeli tai iso mediajuttu?**

| Luokka | Kuka on yläpuolella | Esimerkit | Realistinen tavoite |
|---|---|---|---|
| Media-termi | Yle, MTV, Voice.fi + Wikipedia | rage bait, dunning kruger | sija 5–6, ei kolmoseen |
| Sanakirjatermi | fi.wikipedia, Wikisanakirja, Urbaani Sanakirja, foorumit | hyvesignalointi, hanlonin partaveitsi, whataboutismi, klikkiotsikko | sija 3–4 saavutettavissa |
| Vapaa termi | ei Wikipediaa, ei uutiskattausta | darvo, uutiskynnys, käärmeöljy, bränditurvallisuus | sija 1–3, tässä sivusto voittaa |

fi.wikipedia-tarkistus (API, `action=query&redirects=1`, tehty 4.9.2026):

| Termi | fi.wikipedia |
|---|---|
| Hyvesignalointi | ON |
| Raivosyötti | ON |
| Whataboutismi | ON |
| Hanlonin partaveitsi | ON |
| Parkinsonin laki | ON |
| Doomscrolling | ON (*Tuomioselailu*) |
| Halo-efekti | ON (*Sädekehävaikutus*) |
| Klikkiotsikko | ON |
| Hajota ja hallitse | ON |
| Ylivertaisuusvinouma | ON |
| **Dunning–Kruger-ilmiö** | EI (mutta 2 Yle-juttua SERPissä → media-termi) |
| **DARVO** | EI |
| **Käärmeöljy** | EI |
| **Uutiskynnys** | EI |
| **Bränditurvallisuus** | EI |
| **Uponneiden kustannusten harha** | EI |

SERP-otos (US-pohjainen WebSearch, siis suuntaa antava eikä google.fi:n
paikallinen tulos):

- **hyvesignalointi** → fi.wikipedia, Wikisanakirja, Urbaani Sanakirja, kolme
  Vauva-ketjua, Lily-blogi, kaksi ohutta affiliate-sivustoa. Voitettavissa.
- **rage bait suomeksi** → Yle (Oxfordin vuoden sana 2025), MTV Uutiset,
  fi.wikipedia, Voice.fi. Ei voitettavissa sisältötyöllä.
- **dunning kruger suomeksi** → kaksi Yle-juttua, salkunrakentaja.fi, schedio.fi,
  ehona.fi, evermind.fi. Keskitason sisältösivustoja — vaikea mutta ei mahdoton.

---

## 5. Toimenpiteet vaikutusjärjestyksessä

### P1 — Kasvata sanakirjatermien pinta-alaa sisarilmiöillä (iso, 6–8 sivua)

Kohdista työ sivuihin, joiden yläpuolella on vain Wikipedia, sanakirjoja ja
foorumeita:

- `hyvesignalointi.html` — 856 näyttöä, sija 7,55, 0 klikkiä
- `hanlonin-partaveitsi.html` — 198, sija 6,46
- `whataboutismi.html` — 402, sija 9,62
- `doomscrolling.html` — 370, sija 7,18
- `kaarmeoljy.html` — 158, sija 8,39
- `klikkiotsikko.html` — 72, sija 8,44

Sivujen pituus on nyt 336–612 sanaa. **Projektin ~260 sanan normia ei rikota** —
lisäpinta-ala tulee sisarsivuista ja ristiinlinkityksestä, ei pidemmistä sivuista
(CLAUDE.md: "liian laaja aihe jaetaan useaksi ilmiöksi").

Kysyntä on jo mitattavissa ennen kuin sivua kirjoitetaan:
`hyveposeeraus` (16 näyttöä, sija 7,88) · `sädekehävaikutus` (15, sija 2,70) ·
`ylivertaisuusharha` (4, sija 7,00) · `bystander effect suomeksi` (8, sija 5,00).
Sädekehävaikutus on sijalla 2,7 ilman omaa sivua.

### P2 — Etsi lisää DARVOn kaltaisia vapaita termejä (keski, 8–10 sivua)

Korkein tuotto työtuntia kohti. DARVO tuottaa 68 % klikeistä koska sillä ei ole
kilpailua. Seula: käy ilmiölista läpi, tarkista fi.wikipedia-osuma per termi,
nosta ne joilta artikkeli puuttuu. Otoksessa artikkeli puuttui termeiltä
käärmeöljy, uutiskynnys, bränditurvallisuus ja uponneiden kustannusten harha —
kaikilla on jo näyttöjä mutta sija 9–10.

Perustelu: sanakirjatermissä sijan 7 → 4 nosto vaatii kilpailun voittamista;
vapaassa termissä sijan 1–3 saa käytännössä olemalla ainoa, joka on kirjoittanut
aiheesta suomeksi.

### P3 — Lyhennä title-tagit alle 60 merkkiin (pieni, 1 skripti)

**84 sivua 156:sta ylittää 60 merkkiä**, pisimmät 90:
`kannatusmittausten-virhemarginaali.html` (90), `pakotettu-jatkuvuus.html` (88),
`branditurvallisuus.html` (87), `vihamielisen-median-harha.html` (85),
`evasteansa.html` (83).

Mobiili tuottaa 61 % näytöistä (5 549/9 062) mutta **80 % klikeistä** (156/195),
ja mobiili-SERPissä title katkeaa noin 55–60 merkin kohdalla — juuri siitä, missä
`| Ilmiöitä` vie tilan kuvailevalta osalta. Vertailukohta: DARVO on 49 merkkiä.

Ei nosta sijaa mutta parantaa CTR:ää sillä sijalla, jolla sivu jo on.
Työaseman puolella halvin toimenpide listalla.

**Laitteet:** Mobiili 156 klikkiä / 5 549 näyttöä / CTR 2,81 % / sija 7,88.
Desktop 38 / 3 462 / 1,10 % / sija 11,38. Desktopin sija on 3,5 sijaa mobiilia
heikompi — sama sisältö, eri SERP-koostumus.

### P4 — Lisää puuttuva FAQ-merkintä viidelle sivulle (pieni, 5 sivua)

Sivustolla on 35 `FAQPage`-merkintää 156 sivulla. Kärkisivuista 12:lla se on ja
viideltä puuttuu — ja juuri ne viisi ovat sijoilla 6,9–11,1:

| Sivu | Sija | Näytöt |
|---|---|---|
| parkinsonin-laki.html | 10,13 | 125 |
| kuollut-internet.html | 11,13 | 132 |
| hajota-hallitse.html | 10,11 | 107 |
| klikkiotsikko.html | 8,44 | 72 |
| uutiskynnys.html | 6,88 | 110 |

Kysymykset poimitaan **sanatarkasti** GSC:n kyselyistä, ei arvaamalla:
`mikä on uutiskynnys` (30 näyttöä) · `mitä ragebait tarkoittaa` (6) ·
`uutiskynnys englanniksi` (5) · `mitä bkt mittaa` (3) ·
`mitä tarkoittaa bruttokansantuote` (9).

### P5 — Päätä, mitä tehdään sivun 3 sivuille (pieni, päätös)

Kuusi sivua kerää näyttöjä sijoilta 19–43. Ne eivät koskaan tuota klikkejä
nykysijalla:

`bkt-harha.html` 166 n / sija 19,19 · `gaslighting.html` 104 / 22,12 ·
`viherpesu.html` 97 / 34,42 · `ponzi-pyramidi.html` 59 / 27,10 ·
`simple-sabotage.html` 58 / 42,69 · `smishing.html` 49 / 38,08

Kaikki ovat isoja, vahvasti kilpailtuja päätermejä. Vaihtoehdot: kohdista
kapeampaan hakuaikeeseen (*viherpesun tunnistaminen* eikä *viherpesu*) tai jätä
rauhaan ja käytä aika P2:een.

---

## 6. Mitä data ei kerro

- **Kysely × sivu -paria ei ole viennissä**, joten kannibalisointia (kaksi sivua
  samasta kyselystä) ei voi todentaa tästä aineistosta. Jos P1:n jako tehdään,
  tarkista jälkikäteen GSC:n sivukohtaisesta näkymästä.
- **Vertailuviennit ovat molemmat "viimeiset 3 kk"** ja siksi osin päällekkäisiä.
  Kesäkuun osuus on 4 näyttöä, joten kumulatiivinen erotus vastaa käytännössä
  jaksoa 13.8.–1.9. Luvun 1 päivävertailut on laskettu suoraan `Chart.csv`:stä
  eivätkä kärsi päällekkäisyydestä.
- **Kilpailuluokitus** perustuu fi.wikipedian API-tarkistukseen ja US-pohjaiseen
  hakutulosotokseen. Se on suuntaa antava, ei google.fi:n paikallinen SERP.
- **`Search appearance.csv` listaa vain "Product snippets"** (1 klikki, 27
  näyttöä, sija 8,48). Sivustolla ei ole `Product`-, `Offer`-, `Review`- eikä
  `AggregateRating`-merkintöjä — luokitus tulee siis jostain muualta. Ei
  toimenpiteitä, mutta pidä silmällä jos määrä kasvaa.

## 7. Mikä on muuttunut edellisestä auditista

| Havainto 13.8. | Tilanne 4.9. |
|---|---|
| Kynnys sijalla 5–7 | Tarkentunut: kynnys ~sijalla 4; 5–8 tuottaa ilman DARVOa 0,64 % |
| DARVO 71 % klikeistä | 68 % — keskittymä ei ole purkautunut |
| Geneerinen "mitä se tarkoittaa" -title maksoi 42 % näytöistä | Peruutettu; nyt ongelma on title-**pituus** (84/156 yli 60 merkkiä) |
| Sisäinen linkitys tuotti ~1,5 sijan noston | Kyllästynyt: linkkimäärän ja sijan välillä ei enää korrelaatiota |
| Kategoriasivuilla 0 näyttöä (2.8.) | `kategoria-psykologia-ja-kognitio.html` 110 näyttöä, sija 21,0 → 12,6 |

---

## 8. Toteutus 4.9.2026 — P2:n seula + P4 ja P5 tehty

### P2: fi.wikipedia-seula kaikille 139 ilmiölle

Tarkistettu API:lla (`action=query&redirects=1`, eräajo 40 otsikkoa kerrallaan).
**104/139 ilmiöllä ei ole fi.wikipedia-artikkelia.** "Vapaa termi" ei siis
yksin riitä suodattimeksi — kolme neljästä sivusta on jo vapaa. Ratkaiseva
yhdistelmä on **vapaa termi + todistettu kysyntä + parannettava sija**.

Seulan tulos kysynnän mukaan:

| Luokka | Sivuja | Tulkinta |
|---|---|---|
| Näyttöjä ≥ 20 | 39 | todistettu kysyntä, ei Wikipedia-kilpailua — tässä työ kannattaa |
| Näyttöjä 1–19 | 59 | orastava kysyntä, seuraa |
| Nolla näyttöä | 6 | ei kysyntää tällä nimellä |

Nollan näytön kuusi ovat nimeämiskysymys, eivät sisältökysymys:
`lukittu-paatos`, `strateginen-aliarviointi`, `paatosperainen-todistelu`,
`lapi-hinnalla-milla-hyvansa`, `sinipesu`, `vaara-tasapaino`. Kaikki ovat
keksittyjä suomennoksia — vrt. projektin nimeämisnormi, joka suosii
vakiintunutta lainasanaa.

**Seulan rajoitus:** se antaa vääriä negatiivisia, kun fi.wikipedia käyttää
eri suomenkielistä nimeä. Kolme tunnistettua: `rage-bait` → *Raivosyötti*,
`dunning-kruger` → *Ylivertaisuusvinouma*, `halo-efekti` →
*Sädekehävaikutus*. Nämä ovat oikeasti kilpailtuja eivätkä kuulu vapaisiin.

### Tehty 4.9.: 11 sivua, `scripts/seo_kapea_aie.py`

Title + 5 meta-kenttää + näkyvä vastauslohko + FAQPage. Kapea aie valittu
GSC:n omista kyselyistä. Yksityiskohdat: `MUUTOSLOKI.md`, 4.9.2026.

P5:n kuusi syvällä ollutta sivua kohdistettiin kapeampaan aikeeseen, ja
P4:n viisi FAQ:tta puuttunutta sivua saivat sen. Neljä P5-sivua on samalla
P2-sivuja (vapaa termi + kysyntä): `bkt-harha`, `ponzi-pyramidi`,
`simple-sabotage`, `smishing`.

### Seuraava erä: P2:n jäljellä olevat kärkiehdokkaat

Vapaa termi, näyttöjä ≥ 20, sija ≥ 6, ei vielä käsitelty:

| Sivu | Näytöt | Klikit | Sija |
|---|---|---|---|
| `kaarmeoljy.html` | 158 | 0 | 8,39 |
| `sunk-cost-harha.html` | 148 | 2 | 12,60 |
| `overton-ikkuna.html` | 65 | 1 | 9,62 |
| `scope-creep.html` | 64 | 0 | 14,16 |
| `hiljainen-irtisanoutuminen.html` | 60 | 0 | 14,03 |
| `kafka-ilmio.html` | 51 | 2 | 13,18 |
| `1-prosentin-saanto.html` | 51 | 0 | 8,29 |
| `branditurvallisuus.html` | 43 | 0 | 8,35 |
| `honeypot-huijaus.html` | 39 | 0 | 9,05 |
| `shrinkflaatio.html` | 35 | 1 | 7,94 |
| `korkoa-korolle.html` | 33 | 0 | 22,88 |
| `keskiarvo-vs-mediaani.html` | 32 | 0 | 14,22 |
| `conways-laki.html` | 30 | 0 | 9,57 |
| `haamutyopaikat.html` | 30 | 1 | 8,33 |
| `rautainen-laki.html` | 28 | 3 | 8,57 |
| `fofo.html` | 27 | 0 | 6,04 |
| `hiljainen-irtisanominen.html` | 26 | 2 | 12,77 |
| `bait-and-switch.html` | 24 | 0 | 9,04 |
| `qr-koodihuijaus.html` | 24 | 0 | 10,38 |
| `strateginen-osaamattomuus.html` | 23 | 0 | 7,70 |
| `jarjestelman-puolustelu.html` | 22 | 0 | 32,36 |
| `portinvartija-kulttuuri.html` | 22 | 0 | 10,50 |
| `foot-in-the-door.html` | 22 | 0 | 8,68 |
| `manufactured-consent.html` | 21 | 1 | 8,90 |

Huomaa `hiljainen-irtisanoutuminen` (60 n) ja `hiljainen-irtisanominen`
(26 n): kaksi eri ilmiötä, joiden nimet eroavat kahdella kirjaimella. Ne
kilpailevat todennäköisesti samoista kyselyistä — tarkista kannibalisointi
GSC:n sivukohtaisesta näkymästä ennen kuin kumpaankaan koskee.

### Mittaus

Muutosten vaikutus näkyy aikaisintaan 2–4 viikossa. Seuraava vienti
`datalake_analysis/`-kansioon lokakuun alussa; verrattava mittari on **näiden
11 sivun sija**, ei sivuston kokonaisklikit — DARVO peittää alleen kaiken muun.
