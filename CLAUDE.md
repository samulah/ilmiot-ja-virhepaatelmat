# Ilmiöitä — www.ilmiöt.fi

Suomenkielinen tietopankki: 139 yhteiskunnallista ilmiötä, 13 aihepiiriä. Staattinen
HTML, ei build-vaihetta — jokainen sivu on itsenäinen tiedosto repon juuressa. Osa
tiedostoista on kuitenkin **generoituja**, eikä niitä muokata käsin (ks. alla).

## Muutosloki — kaksi tiedostoa, eri yleisö

Muutoksista pidetään kirjaa kahdessa paikassa. Ne eivät ole kopioita toisistaan:

| Tiedosto | Yleisö | Sisältö |
|---|---|---|
| `MUUTOSLOKI.md` | tekijä ja tulevat sessiot | tekninen totuus: skriptinimet, sivumäärät, mitä ja miksi |
| `muutokset.html` | sivuston lukija | mitä lukijalle näkyy: uudet ilmiöt, parannukset, yksityisyys |

`muutokset.html` on **käsin kirjoitettu sivu, ei generoitu** `MUUTOSLOKI.md`:stä.
Syy: lukijaa ei kiinnosta `robots.txt`:n punycode-rivi tai CSS:n cache-bust, ja
suurin osa teknisistä merkinnöistä kääntyy lukijan kielelle vasta tulkittuna. Älä
siis kirjoita skriptiä, joka muuntaa MUUTOSLOKI.md:n HTML:ksi — se tuottaisi
sivun, jota kukaan ei lue.

### Kun sivustolle tehdään muutos, joka näkyy lukijalle

Lukijalle näkyviä ovat: uudet tai poistetut ilmiöt, uudet aihepiirit, sisällön
laajennukset (esim. vastakeino-osiot) ja navigoinnin muutokset. **Tekniset
muutokset eivät kuulu `muutokset.html`:ään** — eivät SEO-viilaukset, eivät
sitemap-päivitykset, ei cache-bust, eikä myöskään infrastruktuuri kuten
itsehostatut fontit. Nekin kuuluvat `MUUTOSLOKI.md`:hen, mutta lukijan sivulla
ne luetaan teknisenä selittelynä. Kysy: *mitä lukija saa?* Jos vastaus on
"ei mitään uutta luettavaa", merkintä jää pois.

1. **`MUUTOSLOKI.md`** — uusi osio tiedoston alkuun (uusin ensin), otsikko
   `## P.K.VVVV — mitä tehtiin`. Tekninen tarkkuus, skriptinimet mukaan.
2. **`muutokset.html`** — uusi `<article class="muutos">` `.loki`-divin **alkuun**
   (uusin ensin). Rakenne on kiinteä:
   ```html
   <article class="muutos">
     <span class="muutos-pvm">28.7.2026</span>
     <h3>Otsikko lukijan kielellä</h3>
     <p>Kaksi–neljä virkettä. Linkitä uudet ilmiösivut suoraan.</p>
   </article>
   ```
   Kirjoita siitä, *mitä lukija saa*, ei siitä mitä tiedostoja muutettiin.
3. **`muutokset.html`:n JSON-LD** — `"dateModified"` uuteen päivään.
4. **`index.html`** — kaksi kohtaa samalle päivälle:
   - headerin nappi: `<a class="paivitetty-btn" href="muutokset.html">Päivitetty
     P.K.VVVV ›</a>`
   - JSON-LD `CollectionPage` → `"dateModified"`
   Nämä ovat samat kaksi päivämäärää; jos ne eroavat, sitemapin `lastmod` menee
   pieleen (se lukee JSON-LD:n, ei näkyvää tekstiä).
5. **`python3 scripts/build_sitemap.py`** — poimii `lastmod`-arvot sivujen
   JSON-LD:stä. Aja aina vasta kohtien 3–4 jälkeen.

Etusivun nappi on ainoa sisääntulo sivulle headerissa; lisäksi linkki on
`index.html`:n ja `tietoa.html`:n footerissa. Jos header rakennetaan uusiksi,
nappi on säilytettävä — muuten sivu jää orvoksi.

## Generoidut tiedostot — älä muokkaa käsin

| Tiedosto | Generoi | Milloin ajetaan |
|---|---|---|
| `sitemap.xml` | `scripts/build_sitemap.py` | aina kun sivuja lisätään/poistetaan tai `dateModified` muuttuu |
| `search-index.js` | `scripts/build_search_index.py` | sisältömuutosten jälkeen |
| `llms.txt` (ilmiölista) | `scripts/paivita_maarat.py` | ilmiömäärän muuttuessa |
| `kategoria-*.html` | `scripts/build_kategoriat.py` | kun `kategoriat/*.md` muuttuu |
| `data/suosio.js` | `scripts/paivita_suosio.py` | yöllä cronista |
| `luonnokset/suosio.html` | `scripts/paivita_suosio.py` | samalla ajolla |
| `luonnokset/etusivu-nostot.html` | `scripts/paivita_suosio.py` | samalla ajolla |

`llms.txt`:n **otsikkolohko** (rivit 1–10) on käsin ylläpidetty; vain
ilmiölista synkronoituu skriptillä.

## Suosiodata ja etusivun nostot

`scripts/paivita_suosio.py` hakee liikennekannasta luetuimmat sivut ja valitsee
viikon ilmiön. Kolme sääntöä:

1. **Yöajo ei kirjoita `index.html`:ään.** Suosiodata elää erillisessä
   `data/suosio.js`:ssä, jonka etusivu lataa `defer`-skriptinä ja joka on ainoa
   yöllä palvelimelle siirtyvä tiedosto. Jos data kirjoitettaisiin HTML:ään,
   joka yö työnnettäisiin 300 kt etusivu, joka voi ylikirjoittaa käsin tehtyjä
   muutoksia — se on tämän projektin dokumentoitu pahin vikatila.
2. **`data/suosio.js` sisältää vain slugit ja luvut.** Otsikot, kuvaukset ja
   värit haetaan selaimessa sivun omista `.hub-kortti`-elementeistä. Älä lisää
   niitä datatiedostoon: kaksi listaa ajautuisi erilleen.
3. **Nostokortit eivät käytä luokkaa `hub-kortti`.** Etusivun haku,
   nuolinäppäinnavigaatio ja `randomIlmio()` keräävät kaikki `.hub-kortti`-
   elementit, joten duplikaatti näkyisi hakutuloksissa kahdesti.

Nostolohkot injektoidaan `NOSTOT-ALKU`/`NOSTOT-LOPPU`-merkkien väliin; ajo on
idempotentti ja poistaa edellisen injektion ensin. Oletuksena kohde on
`luonnokset/etusivu-nostot.html`, `--tuotanto` kirjoittaa `index.html`:ään.
Tunnukset ja kannan osoite ovat gitignoratussa `.suosio.env`:ssä
(ks. `.suosio.env.malli`) — eivät koskaan versionhallintaan.

Ilmiöiden numerointia ei koskaan korjata käsin: `scripts/lisaa_ilmiot.py` ja
`scripts/poista_ilmio.py` numeroivat koko sivuston uudelleen ja päivittävät
IDS-taulukot, PREV/NEXT-ketjun ja selausnapit. Molemmat ovat kuivaharjoituksia
oletuksena, kirjoitus `--kirjoita`-lipulla.

## Sivujen tyyli

- `index.html`, `tietoa.html` ja `muutokset.html` kantavat CSS:nsä `<style>`-lohkossa
  → ne ovat immuuneja `style.css`:n cache-bustille.
- Ilmiösivut linkittävät `style.css?v=YYYYMMDD`. Kun `style.css` muuttuu, versio on
  bumpattava kaikilla sivuilla, jotka siihen linkittävät.
- Väripaletti: `--c-primary #C9A84C`, `--c-primary-dark #1C1400`,
  `--c-primary-mid #8B6914`, `--c-bg #F5F0E5`. Kirjasimet Spectral (otsikot) ja
  DM Sans (leipäteksti), molemmat itsehostattuja `fonts/`-kansiossa.
- Sivusto ei lataa mitään ulkopuoliselta palvelimelta (27.7.2026 alkaen). Älä lisää
  CDN-linkkejä, Google Fontsia tai ulkoisia skriptejä.

## Sisältönormit

- Ilmiösivu on **~260 sanaa** (mediaani). Liian laaja aihe jaetaan useaksi ilmiöksi
  sen sijaan että yksi sivu kirjoitettaisiin pitkäksi.
- Nimeämisessä suositaan vakiintunutta lainasanaa (*shrinkflaatio*, *rage bait*)
  keksityn suomennoksen sijaan. Englanninkielinen alkuperäistermi kuuluu ingressiin.
- Jokainen ilmiösivu päättyy osioon **Tunnistaminen ja vastakeinot**. Etusivu lupaa
  tämän jokaisesta artikkelista — lupauksen on pidettävä.
- Uudet sivut kirjoitetaan ensin luonnoksiksi `luonnokset/`-kansioon (kaikki erät
  samassa kansiossa 14.8.2026 alkaen) ja julkaistaan vasta erikseen vahvistettuna.
  Kansion `index.html` on erien hakemisto ja julkaisun tarkistuslista.
