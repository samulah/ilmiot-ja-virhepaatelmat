# Suunnitelma: oikeat kategoriasivut

**Kohde:** https://www.ilmiöt.fi/
**Päiväys:** 2026-07-25
**Tila:** suunnitelma — mitään ei ole vielä toteutettu
**Lähtökohta:** SEO-audit 2026-07-25 (`FULL-AUDIT-REPORT.md`), jossa tämä tunnistettiin
suurimmaksi käyttämättömäksi rakenteelliseksi mahdollisuudeksi

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
