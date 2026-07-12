# Content Brief: yhteiskunnalliset ilmiöt (etusivu, improve mode)

**Kohde:** https://www.ilmiöt.fi/ (etusivu)
**Päiväys:** 2026-07-12
**Tila:** suunnitelma — muutoksia ei ole vielä tehty (paitsi 91→98-korjaus, tehty samana päivänä)

---

## Huomiot ennen briefiä

1. **Domain:** `ilmiot.fi` (ä:tön) ei vastaa lainkaan. Sivusto toimii vain osoitteessa
   www.ilmiöt.fi (xn--ilmit-mua.fi). Jos ä:tön domain halutaan ohjaukseksi, se pitää
   hankkia ja ohjata erikseen.
2. **Korjattu 2026-07-12:** etusivulla oli kuusi vanhentunutta "91 yhteiskunnallista
   ilmiötä" -mainintaa (title, og:title, twitter:title, JSON-LD ×2, intro) → korjattu 98:aan.

---

## Search Intent

Informationaalinen. Geneerinen "ilmiöt"-SERP menee uutisosastoille (Yle, Apu) ja
sanastopalveluihin (Finto) — sitä ei voi voittaa eikä kannata tavoitella. Etusivun
realistinen rooli on **hub**, joka kerää pitkän hännän liikennettä kolmesta voitettavasta
klusterista: *kognitiiviset harhat*, *manipuloinnin keinot* ja *argumentointivirheet*.
Google palkitsee näissä pitkät, listamuotoiset selitysoppaat. Kohdeyleisö:
yleissivistynyt lukija ilman psykologian taustaa.

## Competitor Analysis

| # | URL | Key H2 Sections | Est. Words | Score | Main Gap |
|---|-----|-----------------|------------|-------|----------|
| 1 | skepsis.fi/jutut/virhelista.html | 17 argumentointivirhettä esimerkein | ~3 800 | 27/40 | Vuodelta 1998–99, ei vastakeinoja, ei mobiiliystävällinen |
| 2 | vaadifaktat.fi/sosiaalinen-manipulaatio… | Historia, tekniikat, suojautuminen | ~2 700 | 26/40 | Teoreettinen, ei konkreettisia esimerkkejä, ei tekijätietoja |
| 3 | evermind.fi/nain-meita-manipuloidaan… | Vaikuttaminen vs. manipulointi, keinot | ~1 300 | 25/40 | Suppea (5 keinoa), vähän suojautumisohjeita |
| 4 | terracognita.fi/jutut/ajattelun-vinoumat | Vinoumalista + kirjasuositukset | ~450 | 14/40 | Pelkkä lista ilman selityksiä, v. 2016 |

(Wikipedia, Yle, Finto ja oppilaitossivut suodatettu pois ei-kilpailijoina.)

## Content Gaps and Opportunities

- **Aihekattavuus:** yksikään kilpailija ei yhdistä harhoja + manipulointia + huijauksia
  + työelämää samaan kokonaisuuteen. Sivustolla on 98 sivua ja 11 kategoriaa — kukaan muu
  ei edes yritä tätä laajuutta suomeksi.
- **Vastakeinot:** kaikilta neljältä kilpailijalta puuttuvat systemaattiset vastakeinot
  (skepsis ja evermind tunnistavat, eivät neuvo). Jokaisella ilmiösivulla on jo
  vastakeino-osio — tämä on pääase, mutta etusivu ei kerro sitä tarpeeksi näkyvästi.
- **Tuoreus:** skepsis.fi (ykköskilpailija argumentointivirheissä) on 27 vuotta vanha;
  terracognita 10 vuotta. Näkyvä päivityspäivä on halpa voitto.
- **Etusivun ohuus:** nykyinen proosa on ~1 kappale introa + 3 FAQ-vastausta. Kortit
  eivät ole indeksoitavaa "sisältöä" samalla tavalla kuin selittävä teksti.

## Winning Outline

**H1:** Ilmiöitä — 98 yhteiskunnallista ilmiötä, harhaa ja manipulointikeinoa selitettynä
*(nykyinen H1 "Ilmiöitä" on liian ohut; jos visuaalinen H1 halutaan pitää lyhyenä,
laajennus voi olla visuaalisesti pienempi jatko-osa samassa H1-elementissä)*

**URL Slug:** / (etusivu, ei muutosta)

**Target Word Count:** ~1 800–2 200 sanaa proosaa korttien lisäksi
(kilpailijoiden ka. ~2 000; hub-sivulla kortit päälle; nykyinen ~1 850 sis. kortit)

### SÄILYTÄ (vahvaa jo nyt)

- Hub-kortit numeroineen ja kuvauksineen (98 kpl) — älä koske
- Kategoria-chipnav ja laskurit
- Hakutoiminto ja satunnainen-nappi
- JSON-LD ItemList

### VAHVISTA / LISÄÄ

1. **Intro-kappale** (~120 sanaa, nyt ~50) — lisää virke vastakeinoista ja virke siitä
   kenelle sivusto on. Ensisijainen avainsana ("yhteiskunnallista ilmiötä") ensimmäisen
   100 sanan sisällä — täyttyy jo.
2. **H2 per kategoria: 2–3 virkkeen johdantoteksti otsikon alle ennen kortteja**
   (11 × ~40 sanaa = ~450 sanaa). Kaikki 11 kategoriaa omalla H2:llaan (täyttyy jo):
   Vallan rakenteet, Informaatio ja propaganda, Psykologia ja kognitio, Byrokratia ja
   organisaatio, Projekti- ja ohjelmistokehitys, Kasvun dynamiikka, Huijaukset ja
   petokset, Myyntikikat ja painostus, Alustatalous ja algoritmit, Pesut ja
   maineenhallinta, Työelämän ilmiöt. Toissijaiset avainsanat H2-johdantoihin:
   - *kognitiiviset harhat* → Psykologia ja kognitio
   - *manipuloinnin keinot* → Myyntikikat ja painostus
   - *propagandan tekniikat* → Informaatio ja propaganda
   - *huijausten tunnistaminen* → Huijaukset ja petokset
3. **H2 "Miten suojautua: vastakeinot yhdellä silmäyksellä"** (~250 sanaa, uusi) —
   5–7 yleispätevää vastakeinoa bullet-listana, kukin linkittää 1–2 ilmiösivulle.
   **FS target** kyselylle "miten tunnistaa manipulointi". Suurin yksittäinen
   kilpailuetu, jota kukaan kilpailija ei tarjoa.
4. **Laajennettu FAQ** (nyt 3 kysymystä → 6; ~400 sanaa yhteensä). Uudet kysymykset:
   - "Mitä ovat kognitiiviset harhat?" (**FS target**)
   - "Miten manipuloinnin voi tunnistaa?"
   - "Mikä ero on harhalla ja argumentointivirheellä?"
   Kukin vastaus 40–60 sanaa, suora määritelmä ensimmäisenä virkkeenä.
   Päivitä FAQPage-JSON-LD vastaavasti.
5. **Näkyvä "Päivitetty: [pvm] · 98 ilmiötä" -rivi** heti H1:n alle — tuoreussignaali,
   jonka kaikki kilpailijat laiminlyövät.

Avainsanatiheys: "ilmiö"-sana toistuu korteissa luonnostaan; älä lisää sitä johdantoihin
väkisin. Toissijaiset termit kantavat.

## Recommended Meta Tags

**Title** (nykyinen on kunnossa 91→98-korjauksen jälkeen, 60 merkkiä)

    Ilmiöt — 98 yhteiskunnallista ilmiötä selitettynä | Ilmiöitä

**Meta Description** (nykyinen 155 merkkiä — hieman yli; tiivistetty 148:aan, CTA loppuun)

    Ilmiöt selitettynä suomeksi: 98 ilmiötä vallasta, propagandasta, harhoista,
    huijauksista ja myyntikikoista. Esimerkit ja vastakeinot — tutustu.

## Unique Angle and Information Gain

Ainoa suomenkielinen lähde, joka kattaa harhat, manipuloinnin, huijaukset ja
organisaatioilmiöt **yhtenä ristiinlinkitettynä järjestelmänä vastakeinoineen**.
Kilpailijat tarjoavat joko listan ilman selityksiä (Terra Cognita), selitykset ilman
vastakeinoja (Skepsis, Evermind) tai teorian ilman esimerkkejä (Vaadi Faktat).
Informaatiolisä konkreettisesti:

1. vastakeino jokaiselle 98 ilmiölle,
2. ilmiöiden väliset yhteydet ("Liittyvät ilmiöt"),
3. 2026-tason esimerkit (AI slop, pig butchering, tekoälypesu), joita vuosien
   1998–2020 kilpailijasisällöissä ei ole olemassakaan.

## E-E-A-T Requirements

- Näkyvä päivityspäivä etusivulle (ilmiösivuilla jo on)
- Tekijäesittely: "Kuka sivuston on kirjoittanut" -FAQ:sta linkki tietoa.html:ään —
  varmista että tietoa-sivu kertoo *miksi* tekijä osaa aiheen (kokemus, tausta)
- FAQ-vastauksiin 1–2 lähdeviittausta klassikkotutkimuksiin (esim. Kahneman, Cialdini) —
  nostaa koko sivuston uskottavuutta yhdellä muutoksella
- Ei YMYL-riskiä, mutta huijaus-kategoria sivuaa taloutta: pidä vastakeinot faktisina,
  ei sijoitusneuvontana

## Internal Linking Opportunities

Etusivu on jo täydellinen hub (98/98 linkitetty). Puuttuvat mahdollisuudet ovat
**tekstilinkkejä proosasta**:

1. Intro-kappaleesta → `dunning-kruger.html` ankkurilla "kognitiivista harhaa"
2. Vastakeino-osiosta → `inokulointiteoria.html` ankkurilla "mentaalinen rokotus
   disinformaatiota vastaan"
3. Vastakeino-osiosta → `painostusclose.html` ankkurilla "keinotekoinen kiire"
4. FAQ "Miten manipuloinnin tunnistaa" → `gaslighting.html` ja `foot-in-the-door.html`
5. FAQ "harha vs. argumentointivirhe" → `whataboutismi.html` ankkurilla "entäs-argumentti"

---

## Toteutusjärjestys (vaikutus / työmäärä)

1. Kategorioiden johdantotekstit (11 × 2–3 virkettä)
2. Vastakeino-osio (uusi H2 + bulletit)
3. FAQ-laajennus (3 uutta kysymystä + FAQPage-JSON-LD)
4. Päivitetty-rivi H1:n alle
5. Meta descriptionin tiivistys 148 merkkiin

Yhteensä ~1 100 uutta sanaa. Muista muutosten jälkeen:
`scripts/build_search_index.py` + sitemap lastmod + CSS-cache-bust ei tarvita
(index on inline-CSS-immuuni).

## Lähteet

- https://www.skepsis.fi/jutut/virhelista.html
- https://www.evermind.fi/nain-meita-manipuloidaan-tunnista-pahansuovat-vaikutuskeinot/
- https://vaadifaktat.fi/sosiaalinen-manipulaatio-ymmarra-ja-suojaudu-vaikutuskeinoilta/
- https://www.terracognita.fi/jutut/ajattelun-vinoumat/
- https://fi.wikipedia.org/wiki/Kognitiivinen_vinouma
- https://finto.fi/koko/fi/page/p34854
