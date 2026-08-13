# Uudet aiheklusterit — kysyntäperusteinen valinta

Laadittu 13.8.2026 auditin `GSC-AUDIT-2026-08-13.md` pohjalta.
Ei julkaisupäätös, vaan valintapohja: **mitä kannattaa kirjoittaa seuraavaksi ja
mitä ei missään tapauksessa.**

Tämä täydentää `ANALYYSI.md`:tä, joka koski vaalierää. Vaalierän 3 luonnosta on
edelleen julkaisematta ja niillä on oma takaraja (syksy 2026, ks. `ANALYYSI.md`).
**Tämä suunnitelma tulee niiden jälkeen, ei tilalle.**

---

## 1. Sääntö, jonka data antaa

Kypsät sivut (julkaistu ennen 20.7.), näytöt per sivu:

| Kategoria | Sivuja | Näytöt/sivu | Mediaani |
|---|---|---|---|
| pesut-ja-maineenhallinta | 3 | 158,0 | 43 |
| alustatalous-ja-algoritmit | 8 | 96,1 | 35 |
| psykologia-ja-kognitio | 14 | 76,5 | 46 |
| informaatio-ja-propaganda | 13 | 42,6 | 11 |
| huijaukset-ja-petokset | 11 | 20,3 | 15 |
| byrokratia-ja-organisaatio | 15 | 20,1 | 17 |
| **myyntikikat-ja-painostus** | **15** | **4,9** | **2** |
| **tilastoilla-valehtelu** | **8** | **2,6** | **1** |

**23 sivua (18 % sivustosta) tuottaa 95 näyttöä (2,5 %).** 35 kypsää sivua 108:sta
saa alle 5 näyttöä.

> **Sääntö:** kysyntä ei seuraa aiheen tärkeyttä vaan sitä, **sanotaanko termi
> ääneen suomeksi**. Voittajat (darvo, gaslighting, rage bait, doomscrolling,
> AI slop, hyvesignalointi) ovat kaikki kiertäneet suomalaisessa mediassa tai
> ryhmächatissä. Häviäjät (*door-in-the-face, houkutinvaihtoehto, tilipuristus,
> kaksois-y-akseli, exposure-maksu, pinta-alaharha*) ovat oppikirjakäsitteitä,
> joita kukaan ei nimeä.

`paskuuttaminen.html` on tästä varoitus: **sija 2, yksi näyttö.** Sijoitus on
huippu, kysyntää ei ole, koska termi on itse keksitty. *Enshittification*
esiintyy sivulla kerran eikä lainkaan titlessä. Vrt. `CLAUDE.md`: suositaan
vakiintunutta lainasanaa.

**Paras asetelma on darvon asetelma:** termillä on todellista hakukysyntää,
mutta ei fi-Wikipedia-artikkelia eikä Ylen juttua.

---

## 2. Yhteenveto: ehdotettu järjestys

| # | Klusteri | Sivuja | Kysyntä | Kilpailu | Kategoria | Yhteensä |
|---|---|---|---|---|---|---|
| 1 | Pimeät kuviot (dark patterns) | 5 | ★★★ | ★☆☆ vapaa | Alustatalous (8→13) | **kärki** |
| 2 | Tekoälyhuijaukset | 4 | ★★★ | ★★☆ | Huijaukset (11→15) | **kärki** |
| 3 | Argumentointivirheet | 5 | ★★★ | ★★★ Wikipedia | Informaatio (13→18) | ehdollinen |

Kokonaisuus 14 sivua → 127 + 14 = **141 ilmiötä**. Yksikään ei vaadi uutta
kategoriaa, joten `lisaa_ilmiot.py` toimii ilman `--kortit-valmiina`-lippua.

---

## 3. Klusteri 1 — Pimeät kuviot (dark patterns) ★ kärki

**Miksi tämä on paras yksittäinen veto:** aihetta opetetaan (KKV Kampus,
"Kriittiseksi kuluttajaksi — pimeät käytännöt tutuiksi"), siitä tehdään
opinnäytteitä (Theseus, JYX) ja EU sääntelee sitä — mutta **fi-Wikipedia-artikkelia
ei ole ja nimeäminen on vakiintumatta.** Kukaan ei omista tätä SERPiä. Tämä on
darvon asetelma.

### Nimeämiskysymys — ratkaistava ennen kirjoittamista

Suomessa käytössä ainakin neljä muotoa:

| Muoto | Käyttäjä |
|---|---|
| *dark patterns* / *dark patternit* | vierityspalkki.fi, suunnittelijat |
| *synkät suunnittelumallit* | vierityspalkki.fi (2022) |
| *pimeät käytännöt* | **KKV** (kuluttajaviranomainen) |
| *deceptive patterns* | alkuperäistermin keksijä Harry Brignull vaihtoi nimen tähän |

**Suositus:** sivujen niminä käytetään yksittäisten kuvioiden nimiä, ei
yläkäsitettä — sivusto ei tee yläkäsitesivuja, kategoriasivu hoitaa sen.
Kategoriatekstissä mainitaan kaikki neljä muotoa, jotta kaikki hakutermit
kattautuvat. **Englanninkielinen alkuperäistermi kuuluu joka sivun ingressiin**
(`CLAUDE.md`).

### Ehdotetut sivut

| Sivu | Alkuperäistermi | Kysyntä | Huom |
|---|---|---|---|
| **Evästeansa** | cookie consent dark pattern | ★★★ | "Hyväksy kaikki" on yksi klikkaus, "Hylkää" viisi. Jokainen suomalainen kohtaa tämän päivittäin — korkein tunnistettavuus koko klusterissa |
| **Piilokulut** | drip pricing | ★★★ | Hinta paljastuu erissä: lentoliput, tapahtumaliput, autovuokraus. EU-sääntelyn kohde |
| **Pakotettu jatkuvuus** | forced continuity | ★★☆ | Ilmainen kokeilu muuttuu maksulliseksi ilman erillistä hyväksyntää |
| **Confirmshaming** | confirmshaming | ★★☆ | Kieltäytymisnappi syyllistää: "Ei kiitos, en halua säästää rahaa". Vakiintunut englanninkielinen termi, ei suomennosta → jätetään englanniksi kuten *rage bait* |
| **Oletusasetusansa** | privacy zuckering / default effect | ★★☆ | Oletukset on viritetty palvelun eduksi, ei käyttäjän |

### Päällekkäisyydet tarkistettu

`tilausansa.html` (roach motel) on jo olemassa ja kattaa peruutuksen vaikeuden —
**älä kirjoita sitä uudestaan**, vaan linkitä. `painostusclose.html` kattaa
keinotekoisen niukkuuden ("vain 2 jäljellä"), joten *fake urgency* jää pois.
`houkutinvaihtoehto.html` kattaa decoy-vaikutuksen.

### Kategoriasijoitus

**Alustatalous ja algoritmit** (8 → 13 sivua). Perustelu: kategoria on toiseksi
tuottavin (96,1 näyttöä/sivu) ja aihe on käyttöliittymämanipulaatiota, ei
myyntipuhetta. **Älä sijoita myyntikikat-kategoriaan** — se on sivuston heikoin
(4,9 näyttöä/sivu) eikä uusi sivu paranna huonoa naapurustoa.

---

## 4. Klusteri 2 — Tekoälyhuijaukset ★ kärki

**Miksi nyt:** Danske Bank julkaisi kesäkuussa 2026 katsauksen "Yleisimmät
verkkohuijaukset 2026 — miten tekoäly muuttaa huijauksia", EY varoittaa
suomalaisyrityksiä deepfake-huijauksista, ja aihe on poliisin ja pankkien
vakiovaroitus. Kysyntä on tuoretta ja kasvavaa.

**Riski:** pankit ja viranomaiset kirjoittavat samoista aiheista ja niillä on
auktoriteetti. Ero tehdään sivuston omalla kulmalla — **mekanismi ja vastakeino**,
ei uutisvaroitus.

### Ehdotetut sivut

| Sivu | Alkuperäistermi | Kysyntä | Huom |
|---|---|---|---|
| **Ääniklooni-huijaus** | voice cloning / vishing | ★★★ | "Lapsi soittaa hädässä" ja toimitusjohtajan äänellä soitettu maksupyyntö. `toimitusjohtajahuijaus.html` on tämän 2019-versio → linkitä ristiin, älä toista |
| **Smishing** | smishing (SMS phishing) | ★★★ | Posti- ja Traficom-teemaiset tekstiviestit. Erittäin korkea suomalainen tunnistettavuus. Ei fi-Wikipedia-artikkelia |
| **Deepfake-sijoitushuijaus** | deepfake investment scam | ★★☆ | Väärennetty julkkis tai Yle-uutinen mainostaa sijoitusalustaa. *Syväväärennös* on Wikipedian termi → mainitse molemmat |
| **Tekoälypsykoosi** | AI psychosis | ★☆☆ | Chatbot vahvistaa harhaista ajattelua. Suomenmaa ja Uusi Suomi kirjoittivat 2026. **Villi kortti:** termi on uusi eikä välttämättä jää elämään — kirjoita vasta jos se näkyy vielä syksyllä |

### Päällekkäisyydet tarkistettu

`pig-butchering` (romanssi + sijoitus), `qr-koodihuijaus`, `ennakkomaksuhuijaus`,
`honeypot-huijaus` ja `toimitusjohtajahuijaus` ovat olemassa. Romanssihuijaus
mainitaan `parasosiaalinen-suhde.html`:ssä ja sextortion `badger-game.html`:ssä —
kumpikaan ei ole oma sivunsa, mutta **älä tee niistä sivuja tämän erän yhteydessä**;
ne kannattaa arvioida erikseen.

### Kategoriasijoitus

**Huijaukset ja petokset** (11 → 15 sivua).

---

## 5. Klusteri 3 — Argumentointivirheet ⚠ ehdollinen

**Kysyntä on kiistaton ja toistuvaa.** Se tulee lukion äidinkielestä: ÄI4-kurssi
"Tekstit ja vaikuttaminen" käsittelee argumentointivirheitä, ja SERPissä on
peda.net, lyseo.org, Mediametka, sites.google.com/edu.hel.fi sekä Quizlet-korttipakkoja.
Kysyntä on kausiluontoista mutta palaa joka lukuvuosi.

**Mutta tämä on täsmälleen hyvesignalointi-ansa.** Kaikilla termeillä on
fi-Wikipedia-artikkeli (*Olkinukke*, *Ad hominem*, *Väärä dilemma*, *Kaltevan
pinnan argumentti*, *Auktoriteettiin vetoaminen*, *Argumentointivirhe*,
*Vahvistusharha*) **ja** vakiintunutta opetusmateriaalia. Realistinen sijoitus on
8–12, jossa auditin §2 mukaan klikkejä ei tule.

### Ehdotetut sivut

| Sivu | Alkuperäistermi | fi-Wikipedia | Huom |
|---|---|---|---|
| **Olkiukko** | straw man | ✅ *Olkinukke* | Suurin yksittäinen aukko. Mainitse molemmat muodot |
| **Vahvistusharha** | confirmation bias | ✅ | Tutkituin vinouma. Puuttuu sivustolta kokonaan |
| **Ad hominem** | ad hominem | ✅ | Mainitaan jo `hyvesignalointi.html`:ssä, ei omaa sivua |
| **Väärä dilemma** | false dilemma | ✅ | "Joko tämä tai kaaos" |
| **Kaltevan pinnan argumentti** | slippery slope | ✅ | |

### Päätös, joka pitää tehdä ennen kirjoittamista

Klusteri on jo puoliksi kasassa: `argumenttitulva` (Gish gallop), `whataboutismi`,
`maalitolppien-siirtaminen`, `godwinin-laki`, `poen-laki`, `vaara-tasapaino`,
`omenoita-appelsiineja`. Viisi sivua tekisi siitä kattavan.

**Kirjoita tämä vain jos hyväksyt, että se rakentaa kategorian kattavuutta eikä
tuo klikkejä lähikuukausina.** Jos tavoite on klikit, tee klusterit 1 ja 2 ensin
ja arvioi tämä uudelleen title-testin mittauspisteen (~10.9.2026) jälkeen.

### Kategoriasijoitus

**Informaatio ja propaganda** (13 → 18 sivua).

---

## 6. Mitä EI kirjoiteta

- **Ei lisää myyntikikkoja.** 15 sivua tuottaa 74 näyttöä. Kategoria on todistanut
  ettei kysyntää ole; 16. sivu ei muuta sitä.
- **Ei lisää tilastotemppuja.** 8 sivua, 21 näyttöä, mediaani 1.
- **Ei itse keksittyjä suomennoksia** vakiintuneen lainasanan tilalle. Vrt.
  `paskuuttaminen` (sija 2, yksi näyttö).
- **Ei yläkäsitesivuja** ("Mitä ovat dark patterns?"). Kategoriasivu hoitaa sen,
  ja yläkäsitesivu kilpailisi omaa kategoriasivua vastaan.
- **Ei termejä, joita ei sanota ääneen suomeksi.** Testi ennen kirjoittamista:
  löytyykö termi suomalaisesta uutisesta, viranomaisohjeesta tai
  keskustelupalstalta? Jos ei, se on oppikirjakäsite.

---

## 7. Työjärjestys

1. **Vaalierän 3 luonnosta ensin** (`ANALYYSI.md` § 4) — niillä on takaraja
   syksy 2026, tällä suunnitelmalla ei ole.
2. **Klusteri 1 (pimeät kuviot, 5 sivua)** — paras kysyntä/kilpailu-suhde.
3. **Klusteri 2 (tekoälyhuijaukset, 4 sivua)** — tuorein kysyntä; jos
   *tekoälypsykoosi* on syksyllä kuollut termi, erä on 3 sivua.
4. **Klusteri 3 (argumentointivirheet, 5 sivua)** — vasta erillisen päätöksen
   jälkeen (§ 5).

Kummallekin kärkierälle **kysymysmuotoiset H2-otsikot** heti alusta. Auditin
§ 6b: kilpailijoilla niitä on 10–11 sivua kohti, ilmiöt.fi:llä yksi. Se ei lisää
sanoja eikä riko ~260 sanan normia, mutta kalastaa pitkää häntää — joka tuottaa
57 % sivuston klikeistä.

## 8. Muistutukset julkaisuun

- `lisaa_ilmiot.py`:n `UUDET`-taulukko sisältää yhä media-erän sisällön ja on
  ajettu loppuun. **Taulukko korvataan, ei täydennetä** (`MUUTOSLOKI.md` 5.8.).
- Luonnokset kirjoitetaan omaan kansioon ja julkaistaan vasta vahvistettuna
  (`CLAUDE.md`).
- Tarkista luonnospohjasta periytyvät virheet ennen julkaisua: murupolun
  kategoria, `style.css`-versio, `datePublished`/`dateModified` julkaisupäiväksi.
  Kaikki kolme osuivat media-erään 5.8.
