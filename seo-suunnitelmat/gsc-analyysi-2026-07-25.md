# GSC-analyysi ja CTR-toimenpidesuunnitelma

**Data:** `datalake_analysis/25.7. CSV data ilmiöt kategorioista.csv`
**Jakso:** 2.7.–24.7.2026 (23 vrk) · 60 sivua · 134 hakulauseketta
**Laadittu:** 25.7.2026

---

## 1. Lähtötilanne lukuina

| Mittari | Arvo |
|---|---|
| GSC-näyttöjä | 847 (≈1 100 / kk) |
| Klikkejä | **5** |
| Todellinen CTR | **0,59 %** |
| Odotettu CTR nykysijoituksilla | 2,52 % |
| Sivulatauksia (Sum of naytot) | 886, joista etusivu 347 (39 %) |

**Sivulataukset eivät tule Googlesta.** Etusivu sai 347 latausta mutta vain 3 GSC-näyttöä.
Orgaaninen liikenne on käytännössä nolla — kaikki nykyinen liikenne on suoraa tai
sosiaalisesta mediasta. Kasvuvara on siis kokonaan käyttämättä.

### Näyttöjen jakauma sijoituskaistoittain

| Kaista | Kyselyitä | Näyttöjä | Osuus |
|---|---|---|---|
| 1–3 (kärki) | 2 | 2 | 0,2 % |
| 4–5 | 9 | 76 | 9,0 % |
| 6–8 | 18 | 144 | 17,0 % |
| **9–10 (sivun 1 pohja)** | **16** | **320** | **37,8 %** |
| **11–13 (sivu 2 kärki)** | **20** | **138** | **16,3 %** |
| 14–20 | 13 | 34 | 4,0 % |
| 21–30 | 19 | 41 | 4,8 % |
| 31+ | 41 | 92 | 10,9 % |

> **54 % kaikista näytöistä on sijoilla 9–13.** Tämä on klassinen *striking distance*
> -vyöhyke: sisältö on jo relevanttia, mutta jää juuri kärjen ulkopuolelle.

---

## 2. Ydinlöydös: kaksi erillistä ongelmaa

Sijoitus ja CTR ovat tässä eri ongelmia, ja **CTR on halvempi korjata**.

### Ongelma A — CTR on 77 % odotettua heikompi

Nykysijoitukset tuottaisivat normaalilla klikkikäyrällä ~21 klikkiä. Todellisuus: 5.
Sijoitus ei siis selitä nollatulosta — **snippet ei houkuttele klikkaamaan**.

### Ongelma B — hakuintentio ja sivun lupaus eivät kohtaa

30 % näytöistä (257/847) tulee kyselyistä, joissa on
`suomeksi` / `tarkoittaa` / `mitä on` / `mikä on` / `englanniksi`.
Näiden keskisijainti on 11,6 — heikoin klusteri.

**Yksikään sivuston title ei sisällä sanoja "suomeksi" tai "tarkoittaa".**
103/113 titlestä noudattaa kaavaa `Termi — runollinen alaotsikko — Ilmiöitä`,
ja 48 titleä ylittää 60 merkkiä eli katkeaa SERPissä juuri alaotsikon kohdalta.

Runollinen alaotsikko syö SERP-tilan eikä osu yhteenkään hakusanaan.

---

## 3. Kilpailija-analyysi

Tarkistetut SERPit: `whataboutismi tarkoittaa`, `hyvesignalointi`, `ai slop suomeksi`,
`rage bait suomeksi`, `darvo suomeksi`, `doomscrolling tarkoittaa`, `hanlonin partaveitsi`.

### Havainto 1: "X suomeksi" -SERPejä hallitsevat sanakirjat

ilmainensanakirja.fi, sanakirja.org, suomienglantisanakirja.fi, goong.com, fluentti.fi,
fi.wiktionary.org, suomisanakirja.fi. Ne vastaavat kysymykseen *"mikä on suomenkielinen
sana"* yhdellä rivillä. Ilmiöt.fi ei vastaa siihen lainkaan.

**Sivustolta puuttuvat vakiintuneet suomenkieliset vastineet, joita kilpailijat rankkaavat:**

| Sivu | Vakiintunut suomennos | Mainintoja sivulla |
|---|---|---|
| ai-slop.html | **tekoälylieju** | 0 |
| doomscrolling.html | **tuomioselailu**, huolisurffailu | 0 |
| whataboutismi.html | **entäskunismi**, mutkuttelu | 0 |
| hyvesignalointi.html | **moraaliposeeraus** | 0 |
| rage-bait.html | raivosyötti | 4 ✅ |
| gaslighting.html | kaasuvalotus | 1 |

Tämä selittää suoraan sijoitukset 8–12: sivu on aiheeltaan oikea muttei vastaa
esitettyyn kysymykseen.

### Havainto 2: pisin sisältö voittaa

`whataboutismi` — kärkitulos on **tietoviisas.fi**, käytännössä sama konsepti kuin
ilmiöt.fi (suomenkielinen ilmiösanasto). Se on sijalla 1, ilmiöt.fi sijalla 10.

| | tietoviisas.fi | ilmiöt.fi |
|---|---|---|
| Pituus | 1 800–2 000 sanaa | **481 sanaa** |
| Väliotsikoita | ~10 H2 | 2 H2 |
| Suomenkielinen määritelmä omana osiona | kyllä | ei |

Sivuston sivut ovat 376–501 sanaa. Se riittää sijalle 9–12, ei kärkeen.

### Havainto 3: SERPit ovat pehmeitä

Kilpailijoina ovat pääosin sanakirjat, Vauva-keskustelut, blogit ja Wikipedia.
Yhtään vahvaa aihekohtaista auktoriteettia ei ole. **Kärkisijat ovat otettavissa** —
ne vaativat vain aidosti parhaan vastauksen, ei domain-auktoriteettia.

---

## 4. Priorisoitu tekemisjärjestys

Järjestys on tuotto/työmäärä-suhteessa. Vaihe 1 kannattaa tehdä ennen kuin mitään muuta.

---

### VAIHE 1 — Title- ja meta-remontti (1–2 h, ei uutta sisältöä) ✅ TEHTY 25.7.2026

**Toteutus:** `scripts/seo_titlet_ctr.py` (idempotentti, aja uudelleen turvallisesti).
15 sivua × 6 kenttää = 90 riviä. H1, leipäteksti ja JSON-LD koskemattomia.
Generoidut tiedostot (search-index.js, llms.txt, sitemap.xml) eivät muuttuneet.

**Poikkeama alkuperäisestä suunnitelmasta:** title ei lupaa suomennosta, jota sivun
leipätekstissä ei vielä ole. `tekoälylieju` (0 mainintaa) ja `tuomioselailu` (0) jäivät
pois titlestä — ne otetaan mukaan vaiheessa 2, kun vastauslohko on lisätty.
`raivosyötti` (4 mainintaa) ja `kaasuvalotus` (1) olivat jo tekstissä ja kelpasivat.

**Miksi ensin:** korjaa 77 %:n CTR-vajeen ilman että sijoituksen tarvitsee muuttua.
Vaikutus näkyy 1–2 viikossa.

Uusi kaava: **`Termi suomeksi — mitä se tarkoittaa | Ilmiöitä`**, alle 60 merkkiä.
Runollinen alaotsikko siirtyy H1:een ja description-tekstiin, pois titlestä.

Top-15 sivua näyttöjen mukaan (kattaa 74 % kaikista näytöistä):

| Sivu | Näyttöjä | Sija | Nykyinen title | Ehdotus |
|---|---|---|---|---|
| whataboutismi | 184 | 10,1 | Whataboutismi — entäs-argumentti — Ilmiöitä | **Whataboutismi — mitä se tarkoittaa? \| Ilmiöitä** |
| ai-slop | 87 | 9,3 | AI slop — halpasisällön vyöry — Ilmiöitä | **AI slop suomeksi — mitä tekoälylieju tarkoittaa** |
| hyvesignalointi | 77 | 10,5 | Hyvesignalointi — hyvettä yleisölle — Ilmiöitä | **Hyvesignalointi — mitä se tarkoittaa? \| Ilmiöitä** |
| darvo | 60 | 4,5 | DARVO — uhrin ja syyttäjän roolien kääntäminen | **DARVO suomeksi — manipulaatiotaktiikka selitettynä** |
| rage-bait | 51 | 11,8 | Rage bait — raivo on rahaa — Ilmiöitä | **Rage bait suomeksi — mitä raivosyötti tarkoittaa** |
| dunning-kruger | 29 | 6,8 | Dunning–Kruger-ilmiö — itsevarmuus ilman taitoa | **Dunning–Kruger-ilmiö — mitä se tarkoittaa?** |
| halo-efekti | 24 | 16,5 | Halo-efekti ja stigma — ensivaikutelman loukku | **Halo-efekti — mitä se tarkoittaa? \| Ilmiöitä** |
| bkt-harha | 21 | 41,3 | — | **BKT-harha — mitä bruttokansantuote ei kerro** |
| gaslighting | 19 | 34,3 | Gaslighting — todellisuuden järjestelmällinen kiistäminen | **Gaslighting suomeksi — mitä kaasuvalotus tarkoittaa** |
| hanlonin-partaveitsi | 18 | 8,8 | Hanlonin partaveitsi — älä oleta pahuutta, jos tyhmyys riittää | **Hanlonin partaveitsi — mitä se tarkoittaa?** |
| peterin-periaate | 16 | 10,9 | — | **Peterin periaate — mitä se tarkoittaa?** |
| honeypot-huijaus | 14 | 9,7 | — | **Honeypot suomeksi — mikä on hunajapurkkihuijaus** |
| doomscrolling | 14 | 10,2 | Doomscrolling — kurjuusselauksen kierre | **Doomscrolling suomeksi — mitä tuomioselailu tarkoittaa** |
| kaarmeoljy | 14 | 11,4 | — | **Käärmeöljy — mitä se tarkoittaa? \| Ilmiöitä** |
| streisand-ilmio | 13 | 5,8 | — | **Streisand-ilmiö — mitä se tarkoittaa?** |

Samalla description: aloita suoralla määritelmällä ("X tarkoittaa …"), ei brändipuheella.

**Arvioitu vaikutus:** CTR 0,59 % → 2,0–2,5 % ⇒ **~5 → 22–28 klikkiä/kk** ilman sijoitusmuutosta.

---

### VAIHE 2 — "Suomeksi"-vastauslohko + FAQ-schema (1 pv, top-15 sivua) ✅ TEHTY 25.7.2026

**Toteutus:** `scripts/seo_vastauslohko.py` (idempotentti). 15 sivua, FAQPage-schemoja
1 → 16. Kaksi tietoista poikkeamaa alla olevasta suunnitelmasta:

1. **Lohko vastaa käännöskysymykseen, ei määritelmäkysymykseen.** Kaikki 15 sivua jo
   avautuvat lauseella "X tarkoittaa…", joten alla ehdotettu lohko H1:n alle olisi
   toistanut ensimmäisen kappaleen. Puuttuva pala oli suomennos, ei määritelmä.
2. **Mitta on merkkejä, ei sanoja.** Alla oleva 40–55 sanaa on johdettu
   englanninkielisestä ohjeesta. Suomeksi se on ~380–450 merkkiä eli ohi Googlen
   ~300 merkin snippet-katkaisun. Toteutetut lohkot ovat 253–295 merkkiä.

**Suomennoslinja:** §3:n taulukko listaa "vakiintuneina suomennoksina" sanoja, jotka
eivät sitä ole — `ai-slop.html` sanoo itse leipätekstissään, ettei slopille ole
vakiintunutta suomennosta. Lohko erottaa siksi kaksi tapausta: vakiintunut vastine
sanotaan suoraan (kaasuvalotus, raivosyötti, hunajapurkki, sädekehävaikutus,
käärmeöljy), vakiintumaton sanotaan vakiintumattomaksi (AI slop, doomscrolling).
Keksittyä suomennosta ei esitetä vakiintuneena.

**Miksi:** korjaa intentiovajeen. Vaikuttaa **sekä** sijoitukseen että CTR:ään
(rich snippet). Nykyisin koko sivustolla on vain 1 FAQPage-schema.

Jokaisen top-15-sivun H1:n alle heti näkyviin lyhyt vastauslohko:

```
<h2>Mitä AI slop tarkoittaa suomeksi?</h2>
<p><strong>AI slop</strong> tarkoittaa suomeksi <strong>tekoälyliejua</strong>:
massana tuotettua tekoälysisältöä, jolla ei ole tekijää eikä tarkoitusta …</p>
```

Kolme sääntöä:
1. Vakiintunut suomennos **lihavoituna ensimmäisessä virkkeessä** (ks. taulukko §3).
2. Vastaus mahtuu 40–55 sanaan → kelpaa featured snippetiksi ja AI-sitaatiksi.
3. Lisää `FAQPage`-schema 2–3 kysymyksellä: *"Mitä X tarkoittaa?"*, *"Mikä on X suomeksi?"*,
   *"Miten X tunnistaa?"*.

Olemassa oleva `DefinedTerm`-schema kannattaa säilyttää — se on jo oikein.

**Arvioitu vaikutus:** "suomeksi"-klusterin keskisijainti 11,6 → 6–8. Klusteri on 30 % näytöistä.

---

### VAIHE 3 — Sisällön syventäminen, vain top-5 sivua (2–4 vk) ❌ HYLÄTTY 25.7.2026

> **Tätä vaihetta ei toteuteta tässä muodossa.** Kokeilu aloitettiin
> `whataboutismi`-sivulla ja peruttiin kesken: 355 → ~1 300 sanaa teki tekstistä
> tietosanakirjaa, ei popularisointia.
>
> **Perustelu, joka ei kestänyt.** Vaihe nojasi §3:n havaintoon "pisin sisältö
> voittaa": kärkitulos tietoviisas.fi on sijalla 1 noin 1 800–2 000 sanalla.
> Havainto pitää paikkansa, mutta johtopäätös ei: tietoviisas.fi on eri tuote.
> Tämän sivuston etu on, että ilmiön saa haltuun minuutissa. Pituus, jolla
> kilpailija voittaa, on täsmälleen se ominaisuus jota tällä sivustolla ei ole —
> eikä sitä kannata kopioida sijoituksen takia.
>
> Alla oleva osiolista on siis mitoitusohjeena kuollut. Yksittäinen kohta —
> **konkreettiset suomalaiset esimerkit** — on silti aitoa uutta tietoa eikä
> täytettä, ja se voidaan lisätä ~150–200 sanan kokoisena, jos mittaus antaa
> siihen aiheen.
>
> **Ennen kuin sisältöön kosketaan lainkaan: odota dataa.** Vaiheet 1, 2 ja 4
> ovat livenä vasta 25.7.2026. Niiden vaikutus näkyy 1–2 viikossa. Jos
> "suomeksi"-klusteri liikkuu ennustetusti sijalta 11,6 sijalle 6–8, pituutta ei
> tarvita lainkaan. Sisältötyötä ei kannata tehdä sokkona.

**Alkuperäinen perustelu (säilytetty kirjanpitoa varten):** kallein vaihe, mutta
ainoa keino päästä sijalta 9–10 kärkeen. Ei tehdä kaikille 109 sivulle — vain
niille, joilla on todistettua kysyntää.

Kohteet: `whataboutismi` (184 näyttöä), `ai-slop` (87), `hyvesignalointi` (77),
`darvo` (60), `rage-bait` (51) = **54 % kaikista näytöistä viidellä sivulla.**

480 sanaa → 1 200–1 500 sanaa. Lisättävät osiot (kilpailijan rakenteen mukaan):
- Suomenkielinen määritelmä ja synonyymit
- Alkuperä ja historia
- 3–4 konkreettista suomalaista esimerkkiä
- Miksi se toimii psykologisesti
- Miten tunnistat / miten vastaat *(sivustolla jo, syvennä)*
- Lähiterminologia ja rajanveto

Sivuston olemassa oleva vahvuus — vastakeino-lupaus jokaisella sivulla — on aito
erottautumistekijä sanakirjoihin nähden. Sitä kannattaa korostaa, ei laimentaa.

---

### VAIHE 4 — Kannibalisaatio ja hukkanäytöt (2–3 h) ✅ TEHTY 25.7.2026

**Kannibalisaatio: kaikki kolme paria purettu.** Poikkeus: `kuollut-kissa`in
Streisand-mainintaa ei poistettu vaan se linkitettiin. Termi on osa "ero
lähikäsitteisiin" -kohtaa, ja linkitys ohjaa signaalin oikeaan osoitteeseen ilman
sisältötappiota.

> **Hukkanäyttö-lista ei pitänyt paikkaansa — tarkista lähtödata ennen kuin
> tätä osiota käytetään uudelleen.** Seitsemästä kohteesta vain yksi
> (`conways-laki`, yhdyssana "tietovarastoarkkitehtuuri") oli aidosti korjattavissa.
>
> - **Neljässä sanaa ei ole sivulla lainkaan:** `jarjestelman-puolustelu`
>   ("sulautettu järjestelmä", "järjestelmällinen"), `gaslighting` ("kiittämätön"),
>   `hippo-efekti` ("tyrsky ylppö"), `firehose-of-falsehood` ("valaistusvyöhyke").
>   Google matchaa nämä semanttisesti, ei kirjaimellisesta sanasta. Poistettavaa ei ole.
> - **Kahta ei pidä koskea:** `konsensus-fetissi`n "itseisarvo" on sivun teesi
>   (H1, title, ensimmäinen virke), ja `bkt-harha`n Irlanti on sivun kanoninen
>   esimerkki 24 esiintymällä. Näiden poisto vaihtaisi hyvän sisällön mittariin.
>
> Yleisemmin: sijalla 30–90 olevat näytöt eivät vahingoita sijoituksia, ne vain
> vääristävät keskisijainnin. Se ei ole syy heikentää sisältöä.

Samasta kyselystä kilpailee kaksi sivua → Google ei valitse kumpaakaan:

| Kysely | Kilpailevat sivut | Toimenpide |
|---|---|---|
| streisand ilmiö / streisandin ilmiö | streisand-ilmio.html (5,2) **vs** kuollut-kissa.html (6,0) | kuollut-kissa: poista termi, linkitä |
| hanlonin partaveitsi | hanlonin-partaveitsi.html (8,8) **vs** occamin-partaveitsi.html (26) | occamin: rajaa maininta |
| hiljainen irtisanominen | hiljainen-irtisanominen.html (10) **vs** hiljainen-irtisanoutuminen.html (8) | selkeä erotus molempien alkuun |

**Aiheettomat näytöt** (sivu rankkaa täysin väärästä kyselystä, sija 30–90).
Nämä nostavat keskisijaintia keinotekoisesti; syy on yleensä irrallinen sana leipätekstissä:

- `jarjestelman-puolustelu.html` ← "sulautettu järjestelmä" (88,5), "järjestelmällinen" (67)
- `konsensus-fetissi.html` ← "itseisarvo tarkoittaa" (32), "mikä on itseisarvo" (50), "konsensuaalinen" (75)
- `gaslighting.html` ← "kiittämätön" (53)
- `hippo-efekti.html` ← "tyrsky ylppö" (55)
- `firehose-of-falsehood.html` ← "valaistusvyöhyke" (41)
- `conways-laki.html` ← "tietovarastoarkkitehtuuri" (46)
- `bkt-harha.html` ← "irlanti talous" (51), "irlannin talous" (56), "bkt englanniksi" (34)

> Huom: `bkt-harha.html` rankkaa 10 kyselyllä keskisijainnilla 41 — se yrittää olla
> sekä BKT-selitys että harhan kuvaus. Harkitse fokusointia pelkkään harhaan.

---

### VAIHE 5 — Kategoriasivut (jo suunniteltu)

`seo-suunnitelmat/kategoriasivut-2026-07-25.md` on edelleen oikea seuraava rakenteellinen
askel, mutta **vasta vaiheiden 1–3 jälkeen**: datassa ei ole vielä yhtään kategoriatason
kyselyä, joten kysyntä on toistaiseksi hypoteesi. Yksittäisillä ilmiösivuilla kysyntä on jo
todennettu.

---

## 5. Yhteenveto: mitä ensin

| # | Toimenpide | Työmäärä | Vaikutus | Riski | Tila |
|---|---|---|---|---|---|
| 1 | Title + meta, top-15 | 1–2 h | 5 → ~25 klikkiä/kk | ei mitään | ✅ livenä |
| 2 | Suomeksi-lohko + FAQ-schema, top-15 | 1 pv | sija 11,6 → 6–8 klusterissa | ei mitään | 🔨 committattu, ei livenä |
| 3 | Sisällön syventäminen, top-5 | 2–4 vk | sija 9–10 → 3–5 | työläs | ❌ hylätty — ks. vaihe 3 |
| 4 | Kannibalisaatio + hukkanäytöt | 2–3 h | siistii mittarit | pieni | 🔨 committattu, ei livenä |
| 5 | Kategoriasivut | 1–2 vk | uusi kysyntä | kysyntä todentamatta | ✅ livenä 25.7. |

**Livetilanne 25.7.2026.** Vaiheet 1 ja 5 ovat livenä ja tarkistettu: 12 kategoriasivua
vastaa 200:lla, `tilastoilla-valehtelu.html` → 301 kategoriasivulle, ja
`index.html` / `sitemap.xml` / `llms.txt` ovat md5-identtisiä `kategoriasivut`-haaran
kanssa. Vaiheet 2 ja 4 ovat haarassa `vaihe4-kannibalisaatio`, jota ei ole mergetty
eikä deployattu — niiden mittaus ei ala ennen sitä.

**Konservatiivinen kokonaisarvio vaiheiden 1–3 jälkeen:** ~1 100 näyttöä/kk nykysisällöllä,
striking-distance-kyselyt sijalle 3 ⇒ **~90 klikkiä/kk** (nyt 5). Näyttömäärä itsessään
kasvaa, kun sijoitukset paranevat, joten tämä on alaraja.

---

## Datan varaumat

- 23 vrk, 5 klikkiä yhteensä. **Klikkitason päätelmät ovat kohinaa** — priorisointi
  perustuu näyttöihin ja sijainteihin, jotka ovat 847 näytön otoksella käyttökelpoisia.
- `Sum of naytot` ja `distinctcount visitor key` ovat sivutason lukuja, jotka toistuvat
  jokaisella rivillä. Ne on luettava kertaalleen per sivu, ei summattava.
- Keskisijainti on laskettu näyttöpainotettuna.
- Klikkiarviot perustuvat yleiseen CTR-käyrään, ei sivuston omaan dataan (dataa ei riitä).
