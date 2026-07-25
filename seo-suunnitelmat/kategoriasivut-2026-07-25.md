# Suunnitelma: oikeat kategoriasivut

**Kohde:** https://www.ilmiöt.fi/
**Päiväys:** 2026-07-25
**Tila:** työkalut valmiit, kaikki 12 kategoriasivua + etusivu luonnoksena — ei vielä julkaistu
**Lähtökohta:** SEO-audit 2026-07-25 (`FULL-AUDIT-REPORT.md`), jossa tämä tunnistettiin
suurimmaksi käyttämättömäksi rakenteelliseksi mahdollisuudeksi

> **Päivitys 2026-07-25 (iltapäivä).** Toteutuskoneisto on rakennettu ja ajettu läpi
> hiekkalaatikossa. Pilottina on `Tilastoilla valehtelu`, koska sillä on erityispiirre,
> joka ratkaisee kohdan 9 suurimman avoimen kysymyksen: kategorialla on jo valmis
> johdantoessee samannimisen ilmiösivun muodossa. Ks. uusi luku 10.
>
> Valmiina: `scripts/build_kategoriat.py`, `scripts/poista_ilmio.py`,
> `scripts/lisaa_kategorialinkit.py`, sisällöt `kategoriat/*.md` (12 kpl) ja
> luonnokset `luonnokset-kategoriat/` (12 kategoriasivua + esikatselu etusivusta).
> Ks. luvut 10.7 ja 10.8.

---

## 1. Nykytila

12 kategoriaa on olemassa **vain ankkureina etusivulla** (`index.html#vallan-rakenteet`).
Jokaisella on jo:

- nimi (`hub-kat-label`)
- kuvaus­kappale (`hub-kat-desc`, 2–3 virkettä)
- 3–15 ilmiökorttia, joilla jokaisella on käsin kirjoitettu 1 virkkeen selitys

Sivuston oma skeema **mallintaa kategorian jo hierarkian tasoksi**: jokaisen artikkelin
`BreadcrumbList`-position 2 on kategoria. Se vain osoittaa fragmenttiin, ei sivuun.

| Kategoria | id | Ilmiöitä |
|---|---|---:|
| Byrokratia ja organisaatio | `byrokratia-ja-organisaatio` | 15 |
| Myyntikikat ja painostus | `myyntikikat-ja-painostus` | 15 |
| Informaatio ja propaganda | `informaatio-ja-propaganda` | 14 |
| Psykologia ja kognitio | `psykologia-ja-kognitio` | 14 |
| Huijaukset ja petokset | `huijaukset-ja-petokset` | 11 |
| Projekti- ja ohjelmistokehitys | `projekti-ja-ohjelmistokehitys` | 8 |
| Alustatalous ja algoritmit | `alustatalous-ja-algoritmit` | 8 |
| Tilastoilla valehtelu | `tilastoilla-valehtelu-kategoria` | 8 |
| Vallan rakenteet | `vallan-rakenteet` | 7 |
| Kasvun dynamiikka | `kasvun-dynamiikka` | 3 |
| Pesut ja maineenhallinta | `pesut-ja-maineenhallinta` | 3 |
| Työelämän ilmiöt | `tyoelaman-ilmiot` | 3 |

---

## 2. Miksi tämä on mahdollisuus

### 2.1 Sivustolta puuttuu kokonainen hakutaso

Tällä hetkellä on kaksi tasoa ja niiden välissä aukko:

| Taso | Kohdesivu | Esimerkkihaku |
|---|---|---|
| Yksittäinen ilmiö | 109 artikkelia | "dunning kruger", "astroturffaus", "shrinkflaatio" |
| **Aihepiiri** | **— ei mitään —** | **"manipulointitekniikat", "huijaustyypit", "kognitiiviset vinoumat lista", "painostusmyynnin keinot"** |
| Koko sivusto | `index.html` | "ilmiöt", "yhteiskunnalliset ilmiöt" |

Keskimmäinen taso on tyypillisesti se, jolla on **eniten hakuvolyymia ja selkein
informaatiointentio**. Ihminen ei useimmiten tiedä etsivänsä "door-in-the-face" -nimistä
asiaa — hän etsii "myyntimiehen painostuskeinoja". Nyt ainoa ehdokas noihin hakuihin on
etusivu, joka on 109 kohdan lista: liian jäsentymätön sijoittuakseen mihinkään
yksittäiseen aiheeseen ja huono laskeutumissivu.

### 2.2 Sisältö on jo olemassa

Tämä ei ole "kirjoita 12 uutta sivua tyhjästä". Jokaisella kategorialla on jo kuvaus ja
lista ilmiöitä yhden virkkeen selityksineen. Uutta kirjoitettavaa on **johdantoessee ja
ilmiöiden väliset kytkennät** — eli juuri se, mitä yksittäisillä sivuilla ei voi olla.

### 2.3 Sisäisen linkityksen epätasapaino korjaantuu

Auditin havainto: `index.html` ja `tietoa.html` saavat 110 sisääntulevaa linkkiä, mutta
**12 ilmiösivua saa vain 3** (globaali navigaatio + edellinen/seuraava). Kategoriasivu luo
puuttuvan välitason: jokainen ilmiö linkittää ylös kategoriaansa, kategoria alas
ilmiöihinsä. Alilinkitetyt sivut saavat oikean vanhemman.

### 2.4 Murupolusta tulee todellinen

`BreadcrumbList`-position 2 osoittaa nyt fragmenttiin. Google käsittelee sen yleensä oikein,
mutta oikea URL on vahvempi signaali ja voi näkyä hakutuloksen murupolkuna.

### 2.5 AI-hakujen kannalta luonteva sitattava dokumentti

"Mitä eri huijaustyyppejä on?" on täsmälleen kysymys, johon retrieval hakee **yhtä
kokoavaa dokumenttia**, ei kymmentä erillistä. Kategoriasivu, joka nimeää ilmiöiden
väliset suhteet, on sellainen. Tämä täydentää juuri tehtyä h2-muutosta: yksittäiset sivut
ovat nyt pilkottavissa passageiksi, kategoriasivut antavat kokonaiskuvan.

---

## 3. Suurin riski: ohut duplikaatti

**Tämä on ainoa tapa, jolla hanke epäonnistuu.** Jos kategoriasivu on vain sama korttilista
kuin etusivulla eri URL:ssa, se on lähes-duplikaattia, joka laimentaa sivustoa sen sijaan
että vahvistaisi sitä — ja kolme 3 ilmiön kategoriaa on ohut jo rakenteeltaan.

Vaatimus: **jokaisella kategoriasivulla on 300–500 sanaa uniikkia proosaa**, jota ei ole
millään ilmiösivulla eikä etusivulla. Jos sitä ei synny, sivua ei tehdä.

Tästä seuraa priorisointi (kohta 6): 3 ilmiön kategoriat jätetään myöhemmäksi.

---

## 4. Mitä kategoriasivulla on

1. **H1 kysymysmuotoisena, ei pelkkä otsikko**
   `Vallan rakenteet` → *"Vallan rakenteet — miten valta keskittyy ja suojaa itseään"*
2. **Johdantoessee (300–500 sanaa)** — sivun ainoa varsinainen uusi sisältö. Ei toista
   yksittäisiä ilmiöitä vaan vastaa: mikä näitä yhdistää, miksi ne kuuluvat yhteen, missä
   järjestyksessä ne kannattaa lukea.
3. **Ilmiölista** korttimuodossa, kuvaukset suoraan `hub-kuvaus`-kentistä (generoitu).
4. **"Miten nämä liittyvät toisiinsa"** — 3–6 konkreettista kytkentää, esim. *"Astroturf
   tuottaa sosiaalisen todisteen, jota kaikukammio vahvistaa"*. Tämä on sivun toiseksi
   arvokkain osa ja sitä ei voi olla missään muualla.
5. **Linkit naapurikategorioihin** (2–3).
6. **Skeema:** `CollectionPage` + `ItemList` (kategorian ilmiöt) + `BreadcrumbList`
   (Etusivu → Kategoria), `about` → `DefinedTermSet`.

Otsikot `h2`:na alusta asti — sama konventio kuin juuri tehdyssä laatikkomuutoksessa.

---

## 5. URL-rakenne

**Suositus: litteä `kategoria-<slug>.html`** (esim. `kategoria-vallan-rakenteet.html`).

Perustelu:
- Sivusto on kauttaaltaan litteä; kaikki suhteelliset polut (`style.css`, `favicon.svg`,
  `fonts/`) toimivat sellaisenaan. Alihakemisto `/kategoriat/` vaatisi `../`-polut vain
  näille sivuille — poikkeus konventiosta pienen hyödyn vuoksi.
- **Nimitörmäys on todellinen:** `tilastoilla-valehtelu` on sekä ilmiö (#8) että kategoria.
  Siksi kategorian id on jo nyt `tilastoilla-valehtelu-kategoria`. Etuliite `kategoria-`
  ratkaisee tämän systemaattisesti kaikille.

Vaihtoehto `/kategoriat/<slug>.html` on hierarkiana hieman selkeämpi ja polkurakenne on
lievä positiivinen signaali, mutta ero on pieni eikä oikeuta poikkeusta.

---

## 6. Priorisointi — älä tee kaikkia 12:ta kerralla

**Vaihe 1 (5 sivua):** suurimmat ja hakuvolyymiltaan lupaavimmat.

| Kategoria | Ilmiöitä | Miksi ensin |
|---|---:|---|
| Myyntikikat ja painostus | 15 | Selkeä kaupallinen/arkinen intentio, paljon "miten tunnistan" -hakuja |
| Huijaukset ja petokset | 11 | Korkea intentio, ajankohtainen, hyvä sitaattipotentiaali |
| Psykologia ja kognitio | 14 | "Kognitiiviset vinoumat" on vakiintunut hakutermi |
| Informaatio ja propaganda | 14 | Ajankohtainen, erottuva kulma |
| Byrokratia ja organisaatio | 15 | Suurin, selkeä työelämäkulma |

**Vaihe 2 (4 sivua):** `Vallan rakenteet` (7), `Alustatalous ja algoritmit` (8),
`Projekti- ja ohjelmistokehitys` (8), `Tilastoilla valehtelu` (8).

**Vaihe 3 / ehkä ei lainkaan:** `Kasvun dynamiikka` (3), `Pesut ja maineenhallinta` (3),
`Työelämän ilmiöt` (3). Kolmen ilmiön kategoriasivu on ohut rakenteeltaan. Vaihtoehdot:
odota kunnes kategoriassa on ≥6 ilmiötä, tai yhdistä (esim. Pesut + Työelämä laajempaan
kokonaisuuteen). **Älä tee näitä vain symmetrian vuoksi.**

Vaiheen 1 jälkeen mitataan (kohta 8) ennen kuin jatketaan.

---

## 7. Toteutus

**Generoi skriptillä, älä ylläpidä käsin.** Tällä projektilla on dokumentoitu historia
käsin ylläpidettyjen artefaktien ajautumisesta (llms.txt, sitemap.xml — molemmat korjattu
2026-07-25). 12 uutta sivua on 12 uutta driftin lähdettä.

`scripts/build_kategoriat.py`:
- lukee kategoriat ja kortit `index.html`:stä (`lue_kortit()` on jo olemassa
  `paivita_maarat.py`:ssä ja palauttaa täsmälleen tarvittavan rakenteen)
- lukee johdantoesseen ja kytkennät erillisestä `kategoriat/<slug>.md`-tiedostosta
  (käsin kirjoitettu osuus pysyy käsin kirjoitettuna, generointi hoitaa loput)
- kirjoittaa sivun, skeeman ja ilmiölistan

Lisäksi:
- `build_sitemap.py`: lisää kategoriasivut (`priority` 0.7, `changefreq` monthly)
- `paivita_maarat.py`: kategoriasivut myös llms.txt:hen omaksi osiokseen
- Ilmiösivujen murupolku (`BreadcrumbList` position 2 + näkyvä murupolku) osoittamaan
  fragmentin sijaan oikeaan kategoriasivuun
- Etusivun kategoriaotsikoista linkit kategoriasivuille

---

## 8. Mittaus

Sivusto on varmennettu Search Consoleen punycode-propertyllä (`xn--ilmit-mua.fi`), joten
tämä on **mitattavissa oikeasti** eikä arvailtavissa:

1. **Ennen:** tallenna nykyiset näyttökerrat ja klikkaukset kategoriatason hauille
   (Performance → Queries) sekä `index.html`:n hakutermit. Tämä on lähtötaso.
2. **Julkaise vaihe 1** ja pyydä indeksointi (URL Inspection → Request indexing).
3. **4–8 viikon jälkeen:** onko kategoriasivuille tullut omia hakutermejä? Kannibalisoiko
   se etusivua (etusivun näyttökerrat laskevat ilman että kategorian nousevat) vai
   täydentääkö (molemmat nousevat)?
4. Jatka vaiheeseen 2 vain jos vastaus on täydentää.

Tämä on myös hyvä syy hakea GSC:n data koneellisesti — ks. pääkeskustelu.

---

## 9. Avoimet kysymykset

- **Johdantoesseiden kirjoittaja.** 5 × 400 sanaa = ~2000 sanaa uutta toimituksellista
  tekstiä vaiheessa 1. Tämä on hankkeen todellinen työmäärä, ei tekniikka.
- **Kannibalisoiko etusivua?** Etusivu tavoittelee nyt laajoja "ilmiöt"-termejä.
  Kategoriasivujen pitää tähdätä aihepiiritermeihin, ei brändiin. Jos molemmat
  tavoittelevat samaa, ne kilpailevat keskenään.
- **Näkyykö kategoria navigaatiossa?** Nykyinen `hub-katnav` on etusivulla; kategoriasivut
  kannattaa todennäköisesti lisätä myös ilmiösivujen murupolkuun näkyvästi.

---

## 10. Pilotti: Tilastoilla valehtelu (2026-07-25)

### 10.1 Miksi juuri tämä kategoria ensin

Priorisointitaulukossa (kohta 6) `Tilastoilla valehtelu` on vaiheessa 2. Se nostettiin
piloniksi yhdestä syystä: **kategorialla oli jo johdantoessee, se oli vain väärässä
paikassa.**

Ilmiö **#8 Tilastoilla valehtelu** ei ollut ilmiö samassa mielessä kuin muut 108. Se ei
kuvannut yhtä tunnistettavaa mekanismia vaan luetteli viisi eri tekniikkaa — katkaistun
akselin, cherry-pickingin, suhteelliset luvut, keskiarvon ja kokojen manipuloinnin —
joista jokainen on nykyään oma ilmiönsä numeroilla 102–109. Sivu oli siis *yleiskatsaus
kategoriaan*, ja se oli myös itse tunnistanut asian: sen lopussa oli huomiolaatikko
”Koko aihepiiri omana kategorianaan”, joka linkitti etusivun kategoria-ankkuriin.

Tästä seurasi myös kohdan 5 nimitörmäys: `tilastoilla-valehtelu` oli sekä ilmiö että
kategoria, ja kategorian id jouduttiin väistämään muotoon
`tilastoilla-valehtelu-kategoria`.

**Ratkaisu:** ilmiö poistetaan ja sen sisältö siirtyy kategoriasivun johdantoesseeksi.
Kohdan 9 kysymys ”kuka kirjoittaa 400 sanaa” ei tässä tapauksessa ollut ongelma
lainkaan — teksti oli jo olemassa, se piti vain kirjoittaa uudelleen kokoavaksi
esseeksi yksittäisen ilmiön selityksen sijaan.

### 10.2 Mitä ilmiön poistaminen oikeasti maksaa

Numerointi on juokseva 1–109, joten #8:n poisto siirtää **101 ilmiötä** yhdellä alaspäin.
Numero esiintyy neljässä paikassa (ks. muisti *Ilmiöiden numerointi*), ja lisäksi
liikkuvat `const IDS`, `PREV`/`NEXT`, selausnapit ja seitsemän sivun linkit.

Tämä ei ole käsityötä. `scripts/poista_ilmio.py` hoitaa kaiken ja on
**kuivaharjoitus oletuksena** — se tulostaa tiedostokohtaisen muutoslistan eikä kirjoita
mitään ilman `--kirjoita`-lippua.

```
python3 scripts/poista_ilmio.py tilastoilla-valehtelu \
    --korvaa kategoria-tilastoilla-valehtelu.html
```

Vaikutus (todennettu hiekkalaatikossa):

| Kohde | Muutos |
|---|---|
| `index.html` | kortti poistettu, 101 korttia uudelleennumeroitu, 109 → 108 |
| 108 ilmiösivua | `ilmio-tag`, `kortti-nav-laskuri`, `const IDS` |
| `hajota-hallitse` ↔ `bkt-harha` | `PREV`/`NEXT` + selausnapit kytketty toisiinsa |
| 7 sivua | liittyvät-linkki ohjattu kategoriasivulle |
| `omenoita-appelsiineja`, `index.html` | leipätekstin linkki ohjattu |
| `.htaccess` | `RewriteRule ^tilastoilla-valehtelu\.html$ → /kategoria-…  [R=301,L]` |
| `tilastoilla-valehtelu.html` | siirretty kansioon `poistetut/` |

Kaksi tietoista rajausta skriptissä:

- **Selausnappeihin kosketaan vain, jos ne osoittavat poistuvaan sivuun.** Nappien
  teksteissä on `<em>`-muotoilua (`Hajota ja hallitse — <em>divide et impera</em>`),
  jota H1:stä uudelleenrakentaminen hukkaisi. Kaikkien nappien regenerointi olisi
  hiljainen regressio.
- **301 vaatii kohteen olemassaolon.** `--kirjoita` kaatuu, jos korvaava sivu puuttuu —
  muuten ohjaus ja seitsemän sisäistä linkkiä osoittaisivat 404:ään.

### 10.3 Miten ilmiö → kategoria -linkki syntyy

Kohta 2.3 halusi ylöspäin osoittavan linkin jokaiselta ilmiöltä kategoriaansa. Tässä
se syntyy ilman uutta rakennetta: `build_liittyvat.py` lukee nyt index.html:stä myös
kategoriat, ja jos sivun ”Liittyvät ilmiöt” -lohkossa on linkki muotoa
`kategoria-<slug>.html`, se renderöityy kortiksi, jossa numeron paikalla on `⊞`.
Ne 7 sivua, jotka linkittivät poistuvaan ilmiöön, saivat tämän automaattisesti.

Ilmiösivujen näkyvä murupolku ja `BreadcrumbList`-position 2 osoittavat edelleen
fragmenttiin (kohta 2.4). Se on oma askeleensa, ks. 10.5.

### 10.4 Toteutuksen rakenne

**`scripts/build_kategoriat.py`** — generaattori, kaksi lähdettä:

1. `index.html`: kategorian nimi, kuvaus ja kortit (numero, väri, nimi, kuvaus)
2. `kategoriat/<slug>.md`: käsin kirjoitettu johdantoessee ja kytkennät

Sisältötiedostossa on front matter (`kat_id`, `h1`, `otsikko`, `kuvaus`, `vari`,
`paivitetty`, `naapurit`) ja kevyt markdown. Kaksi merkintää ohjaa generointia:
`[[ILMIOT]]` korvautuu korttilistalla ja `[[NAAPURIT]]` naapurikategorialinkeillä —
**kirjoittaja päättää siis niiden paikan sivulla**, ei generaattori. Lohko `:::html …
:::` menee läpi sellaisenaan, mikä on välttämätöntä: pilottisivun pylväskaavio ja
`lue-lisaa`-lohko ovat sivuston omaa merkkausta.

Suunnitelman kohta 7 oletti `.md`-tiedoston puhtaana markdownina. Se ei riitä — kuvat
ja laatikot ovat osa sisältöä, siksi `:::html`.

Generaattori varoittaa, jos uniikkia proosaa on alle 300 sanaa (kohta 3). Pilotissa
on **~660 sanaa**.

URL on suunnitelman mukainen litteä `kategoria-<slug>.html`. Slug johdetaan
`kat_id`:stä poistamalla `-kategoria`-pääte, ja generaattori tarkistaa, että
tiedostonimi vastaa sitä — muut skriptit johtavat URLin samalla säännöllä.

**Muut skriptit päivitetty:**

- `build_sitemap.py`: kategoriasivut mukaan (priority 0.7, monthly), etusivun jälkeen
  ennen ilmiöitä. Vain ne, joilla on tiedosto — vaiheittainen julkaisu ei kaada ajoa.
- `paivita_maarat.py`: `Kategoriasivu: <url>` -rivi llms.txt:n kategoriaotsikon alle.
- `build_liittyvat.py`: kategoriakortit (10.3) + kova `== 109` -tarkistus pois.

Koko ketju ajettu puhtaassa kopiossa ja **idempotentti** — toinen ajo ei muuta mitään.

### 10.5 Julkaisujärjestys

Järjestys ei ole vapaa: 301-ohjaus ja seitsemän sisäistä linkkiä osoittavat
kategoriasivuun, joten sen on oltava olemassa ensin.

1. `python3 scripts/build_kategoriat.py` → `kategoria-tilastoilla-valehtelu.html`
2. `python3 scripts/poista_ilmio.py tilastoilla-valehtelu --korvaa kategoria-tilastoilla-valehtelu.html --kirjoita`
3. `paivita_maarat.py` → `build_liittyvat.py` → `build_sitemap.py` → `build_search_index.py`
4. Silmämääräinen tarkistus + commit
5. Deploy ja **live vs. local -varmistus** (ks. muisti *Deploy-gap*)
6. Search Console: pyydä indeksointi uudelle URLille, tarkista että vanha palauttaa 301

### 10.6 Mitä pilotti jättää auki

- **Etusivun kategoriaotsikot eivät vielä linkitä kategoriasivuille.** Tämä on
  suunnitelman kohta 7, ja siinä on kytkös, joka kannattaa tietää etukäteen: kolme
  skriptiä lukee otsikkoa regexillä `<h2 class="hub-kat-label">([^<]+)<span…`.
  `<a>`-elementin lisääminen otsikon sisään rikkoo ne kaikki. Linkki kannattaa siis
  laittaa `hub-kat-desc`-kappaleen loppuun (”Lue koko kategoria →”) tai muuttaa
  kaikkien kolmen skriptin regexit samalla kertaa. Ei kummempaa, mutta ei myöskään
  yhden rivin muutos.
- **Kategoriasivut eivät ole etusivun haussa.** `build_search_index.py` indeksoi vain
  ilmiösivut. Tämä on tarkoituksellinen oletus, ei bugi — mutta jos kategoriasivuja
  tulee 12, haun pitäisi todennäköisesti löytää nekin.
- **Kategorian id säilyy muodossa `tilastoilla-valehtelu-kategoria`.** Nimitörmäys on
  poissa, joten `-kategoria`-pääte voisi lähteä. Se on kosmeettinen muutos, joka
  rikkoisi olemassa olevat `index.html#…`-ankkurit — ei kannata tehdä ilman syytä.
- **Kategorian id säilyy** (ks. yllä) — ei muutoksia ankkureihin.

### 10.7 Kaikki 12 kategoriaa luonnoksina

Pilotin jälkeen kirjoitettiin loput 11 esseetä, eli **kaikki 12 kategoriaa ovat nyt
luonnoksena** kansiossa `luonnokset-kategoriat/`. Mukana on myös
`luonnokset-kategoriat/index.html`, joka näyttää miltä etusivu näyttää
kategorialinkkien kanssa.

Kaikki luonnokset on generoitu **poiston jälkeisestä tilasta**, joten esikatselussa
näkyvät oikeat luvut: 108 ilmiötä, `Informaatio ja propaganda` 13 ilmiötä ja
uudelleennumeroidut kortit. Näin esikatselu vastaa lopputulosta eikä nykytilaa.

| Kategoria | Ilmiöitä | Uniikkia proosaa |
|---|---:|---:|
| Tilastoilla valehtelu | 8 | ~666 |
| Informaatio ja propaganda | 13 | ~563 |
| Psykologia ja kognitio | 14 | ~539 |
| Myyntikikat ja painostus | 15 | ~512 |
| Byrokratia ja organisaatio | 15 | ~505 |
| Vallan rakenteet | 7 | ~502 |
| Alustatalous ja algoritmit | 8 | ~499 |
| Projekti- ja ohjelmistokehitys | 8 | ~498 |
| Huijaukset ja petokset | 11 | ~498 |
| Pesut ja maineenhallinta | 3 | ~434 |
| Työelämän ilmiöt | 3 | ~407 |
| Kasvun dynamiikka | 3 | ~395 |

Jokainen ylittää kohdan 3 vaatimuksen (300 sanaa uniikkia proosaa), eikä yksikään
essee toista ilmiösivujen sisältöä — ne nimeävät ryhmittelyn, lukujärjestyksen ja
ilmiöiden väliset kytkennät, joita ei voi olla yksittäisellä sivulla.

**Kohdan 6 priorisointi koskee edelleen julkaisua, ei kirjoittamista.** Se, että kaikki
12 on kirjoitettu, ei kumoa mittausargumenttia: kannattaa silti julkaista vaiheittain
ja katsoa Search Consolesta, täydentävätkö kategoriasivut etusivua vai kannibalisoivatko
ne sen (kohta 8).

**Kolme pienintä ovat edelleen ohuita rakenteeltaan** — `Kasvun dynamiikka`,
`Pesut ja maineenhallinta` ja `Työelämän ilmiöt` sisältävät kukin 3 ilmiötä. Niiden
esseet ovat riittävän pitkiä, mutta korttilista on lyhyt eikä kategoriasivu tuo yhtä
paljon lisäarvoa. Kahdessa niistä on tämä sanottu ääneen huomiolaatikossa. Suositus
säilyy: julkaise nämä vasta, jos vaihe 1 mittautuu positiivisesti.

### 10.8 Etusivun kategorialinkit

`scripts/lisaa_kategorialinkit.py` toteuttaa kohdan 7 viimeisen puuttuvan palan.
Linkki (`Lue koko kategoria →`) menee `hub-kat-desc`-kappaleen loppuun, **ei
otsikkoon** — syy on 10.6:ssa kuvattu regex-kytkös, ja skripti dokumentoi sen itse.

- oletuksena vain kategoriat, joilla on olemassa oleva sivu → vaiheittainen julkaisu
  toimii ilman erillistä kirjanpitoa
- `--kaikki` pakottaa kaikki 12 mukaan (esikatselua varten)
- `--luonnos` kirjoittaa `luonnokset-kategoriat/index.html`:ään
- idempotentti, ja poistetun kategoriasivun linkki siivotaan pois automaattisesti

### 10.9 Ulkoasu: kategoriasivu on luvun aloitus, ei artikkeli

Ensimmäinen versio näytti liikaa ilmiösivulta: sama valkoinen kortti, sama värillinen
yläreuna, sama chip-tagi. Sivustolla oli kolme tasoa mutta vain kaksi ulkoasua.

Nykyinen jako:

| Taso | Pohja | Mitta | Tunnus |
|---|---|---|---|
| Etusivu | tumma tarttuva header, kerma | leveä (1240px) | koko sivuston laskuri |
| **Kategoriasivu** | **tumma täysleveä aloitus, kerma** | **660px** | **numeroväli** |
| Ilmiösivu | valkoinen kortti kermalla | 860px | yksi numero |

Erottelu on **rakenteellinen, ei koristeellinen**:

- **Tumma täysleveä aloituspalkki** (`--c-primary-dark`). Väri on lainattu etusivun
  headerista, eli se on jo sivuston sanastoa — kategoriasivu asettuu visuaalisesti
  etusivun ja artikkelin väliin, mikä on täsmälleen sen paikka hierarkiassa.
- **Ei valkoista korttia.** Essee on suoraan kermataustalla. Tämä on muutoksen ainoa
  varsinainen riski: valkoinen kortti on sivuston "tämä on luettava dokumentti"
  -merkki, ja sen poistaminen tekee sivusta sisäänkäynnin eikä arkistokappaleen.
- **Numeroväli otsikkotiedoissa** (`7 ilmiötä · Ilmiöt 1–7`). Ilmiöt on numeroitu
  juoksevasti kategorioiden yli, joten väli on aitoa tietoa. Se on myös se yksi asia,
  jota ilmiösivulla ei voi olla — ilmiöllä on yksi numero, luvulla väli.
- **Luvun numero vesileimana** aloituspalkin oikeassa reunassa
  (`rgba(201,168,76,0.10)`). Sivun ainoa koristeellinen elementti; piilotetaan alle
  860px:n. Muuta liikettä tai efektejä ei lisätty — ne olisivat riidelleet muun
  sivuston kanssa.

> **Hylätty idea: korttiruudukon ulosmurto.** Ensimmäisessä versiossa korttiruudukko
> levisi 1080 pikseliin tekstipalstan 660:n yli, ajatuksena että leveys on
> hub-signaali. Kuvakaappauksessa se ei toiminut: mikään pystyreuna ei ollut
> linjassa, ja ruudukko irtosi muusta sivusta. Kortit ovat nyt täsmälleen
> tekstipalstan levyisiä (mitattu: molemmat x=310, leveys=660).

### 10.10 Kategoriasta toiseen — ja miksi ei vaakaswipeä

Sivun lopussa on `edellinen`/`seuraava`-korttipari, jossa näkyy kohteen numero ja
nimi, sekä laskuri `Kategoria 2 / 12` linkkinä etusivulle. Työpöydällä toimivat myös
nuolinäppäimet ← →, kuten ilmiösivuilla.

**Mobiilissa ei ole swipeä, tarkoituksella.** Vaakaswipe olisi ollut suora vastine
ilmiösivujen eleelle, mutta se on tällä sivutyypillä huono:

- se törmää selaimen omaan takaisin-eleeseen (iOS Safari, Chrome Android)
- se törmää tekstin maalaamiseen, ja kategoriasivu on pitkä lukusivu
- se on näkymätön: mikään ei kerro että ele on olemassa

Tilalla on **nimetty kortti siinä kohtaa, missä lukeminen loppuu**. Se on
löydettävä, iso peukalokohde, kertoo mihin ollaan menossa, eikä kaappaa yhtään
selaimen elettä. Kirjametaforan oma vastaus: luvun lopussa lukee mikä luku on
seuraava.

Lisäksi toimituksellinen `Aiheeseen liittyvät kategoriat` -chiprivi säilyy erillään.
Siitä karsitaan automaattisesti ne kategoriat, jotka ovat jo edellinen/seuraava —
muuten sama kategoria näkyisi kahdesti peräkkäin eri sanamuodolla.

**Etusivun `Lue koko kategoria →`** siirrettiin kuvauskappaleen sisältä sen jälkeen
omaksi chipikseen. Kappaleen sisällä se katosi: `.hub-kat-desc` on `0.76em`, joten
peritty koko oli liian pieni erottumaan linkiksi.

**Kategorioiden numerointi** on aitoa HTML:ää (`<span class="hub-kat-nro">`), ei
CSS-counteria. Syy: etusivun haku piilottaa kategorioita, ja counter numeroisi
näkyvät uudelleen kesken haun. Numerospan lisättiin viiteen regexiin valinnaisena
(`(?:<span class="hub-kat-nro">\d+</span>)?`), joten vanha ja uusi merkkaus kelpaavat
molemmat.

**Kaksi bugia löytyi ja korjattiin tässä yhteydessä:**

1. `lisaa_kategorialinkit.py` lisää linkin `hub-kat-desc`-kappaleeseen, ja
   `build_kategoriat.py` luki saman kappaleen skeeman `about.description`-kentäksi →
   `<a href="...">` päätyi JSON-merkkijonoon ja rikkoi koko skeeman. Kuvaus
   puhdistetaan nyt tageista.
2. Skeema rakennettiin f-string-mallipohjalla, jolloin mikä tahansa lainausmerkki
   index.html:n tekstissä olisi rikkonut sen. Nyt se rakennetaan dictinä ja
   `json.dumps`illa, ja generaattori validoi tuloksen ennen kirjoitusta.
