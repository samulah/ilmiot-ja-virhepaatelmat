# Vedätys — tyyliopas pelipankin kirjoittamiseen

Tämä ohjaa sekä LLM-luonnostelua että ihmisen kuratointia. Jokainen kohta
`pelidata/<slug>.json`:issa on kirjoitettu näiden sääntöjen mukaan, ja
`scripts/build_peli.py --tarkista` valvoo niistä sen osan, joka on koneellisesti
tarkistettavissa. Loput ovat lukijan vastuulla.

Siemenaineisto on `pelidata/_siemen/<slug>.md` — se sisältää kaiken, mitä
sivusto jo sanoo ilmiöstä: määritelmän, vastakeinot, nimetyt alalajit ja
sivulla jo olevat repliikit. **Kirjoita niiden pohjalta, älä tyhjästä.** Pelin
ääni on sivuston ääni.

## Kohde

Yksi kohta on **1–3 virkettä** tekstiä, joka pelaajalle näytetään sellaisenaan.
Ei kehystystä, ei selittävää johdantoa, ei "kuvittele että…". Pelkkä se, mitä
ruudulla tai korvassa oikeasti olisi.

Hyvä:
> Et sä nyt taas ala. Mä olen se joka on tässä koko ajan joustanut, ja silti
> minusta tehdään syyllinen.

Huono:
> Kumppanisi käyttää DARVO-taktiikkaa ja kääntää roolit ympäri sanomalla…

## Kieli

- **Puhuttua suomea.** Lyhyitä lauseita, arkista sanajärjestystä, puhekielisiä
  muotoja siellä missä ne kuuluvat (*mä*, *sä*, *ei oo*, *tuun*). Virallinen
  yleiskieli kuulostaa käännökseltä.
- **Ei käännösrytmiä.** Jos lause voisi olla suora käännös englannista
  ("Minun täytyy sanoa, että olen hyvin pettynyt sinuun juuri nyt"), kirjoita
  se uusiksi.
- **Ei anglismeja** ellei termi ole vakiintunut (*deadline* on, *päivän lopussa*
  ei ole).
- Emojit ja kirjoitusvirheet ovat sallittuja ja usein tarpeen, kun kanava on
  tekstiviesti tai some.

## Konteksti

Käytä konkreettisia suomalaisia tilanteita. Kierrätä samaa tekniikkaa eri
konteksteissa — juuri se on inokulaatiotutkimuksen mittaama yleistyminen:

`tyo` · `parisuhde` · `perhe` · `myynti` · `puhelin` · `some` · `kauppa` ·
`viranomainen` · `vuokra` · `ajatus`

Esimerkkejä paikoista: työpaikan Teams-viesti, esihenkilön kehityskeskustelu,
vuokranantajan tekstari, puhelinmyyjä, appivanhemmat, verkkokaupan kassa,
Facebook-ryhmän kommentti, WhatsApp-ryhmä, sähköpostiketju, taloyhtiön kokous.

## Kiellot

- **Ei nimettyjä puolueita, poliitikkoja, yrityksiä tai todellisia kohuja.**
  Sama sääntö kuin `luonnokset/VAALIKESKUSTELU-LUKUOHJE-PLAN.md` § 1:
  nimeämättömiä tilannekuvauksia. Peli vanhenee muuten kuukaudessa ja saa
  vääränlaista huomiota.
- **Ei tunnistettavia yksityishenkilöitä.** Ei myöskään "erään tuttuni".
- **Ei henkilön nimiä**, ellei niitä tarvita (silloin: Anni, Jussi, Riku, Sanna
  — tavallisia, ei mitään erikoista).
- **Ei väkivallan kuvausta.** Parisuhdeaiheiset kohdat pysyvät verbaalisissa
  taktiikoissa. Jos aihe on raskas, `paljastus.sanot` ohjaa hakemaan tukea.

## `laji` — kolme arvoa, ja tämä on koko pelin ydin

| Arvo | Merkitys | Vastakeino jonka peli opettaa |
|---|---|---|
| `taktiikka` | Joku tekee tämän sinulle. Takana on valinta. | Nimeäminen ja rajan asettaminen |
| `vinouma` | Oman päättelyn järjestelmällinen poikkeama. Ei tekijää. | Menetelmä: tarkistuslista, ulkopuolinen arvio |
| `rehellinen` | Ihan tavallinen viesti. Ei mitään vikaa. | Ei mitään — ja se on vastaus |

Erottelu on sivuston oma teesi (`kategoriat/psykologia-ja-kognitio.md`):
*vinouma ei tarvitse tekijää, taktiikka tarvitsee* — ja väärä vastakeino
pahentaa molempia.

Vaiheessa 1 pankki on taktiikkapainotteinen (27 vuorovaikutusilmiötä).
Vinoumat tulevat vaiheessa 2.

## `rehellinen` — vaikeimmat kirjoittaa, ja ilman niitä peli opettaa väärin

Bad News -pelin replikaatiokritiikki (Modirrousta-Galian & Higham 2023): peli ei
parantanut erottelukykyä vaan siirsi vastetaipumusta — pelaajat epäilivät
valeuutisia enemmän **mutta yhtä paljon myös aitoja**. Se opetti kyynisyyttä.

Siksi jokaisessa päivän erässä on 1–2 rehellistä kohtaa, ja väärä hälytys
maksaa saman kuin ohitus.

Rehellisen kohdan on oltava **uskottavan epäilyttävä mutta oikeasti kunnossa**:

- aito deadline, joka on oikeasti olemassa ja perusteltu
- aito innostus, joka vain sattuu olemaan innostunutta
- aito anteeksipyyntö ilman "mutta"-osaa
- aito alennus, jolla on syy ja voimassaoloaika
- suora pyyntö, jossa kieltäytyminen on tehty helpoksi
- kehu, joka koskee tekoa eikä ihmistä

Kirjoita ne niin, että ne **osuvat samaan hermoon** kuin manipulatiiviset.
Rehellinen kohta joka ei herätä epäilystä lainkaan on hukkaan heitetty kohta.

Tarkista jokainen: *jos pelaaja vastaa "taktiikka", onko hän oikeasti väärässä?*
Jos vastaus on "no, riippuu", kohta ei kelpaa rehelliseksi.

## `harhauttajat`

Kaksi väärää vaihtoehtoa, jotka ovat **oikeasti lähellä** — mieluiten
siementiedoston "Liittyvät ilmiöt" -listalta tai samasta kategoriasta.

Kaukainen harhauttaja tekee tehtävästä helpon eikä opeta mitään; lähellä oleva
harhauttaja opettaa juuri sen erottelun, joka on vaikea. Gaslighting vs. DARVO,
foot-in-the-door vs. door-in-the-face, painostus-close vs. bait and switch.

Harhauttaja ei saa olla oikea vastaus. Jos kohta sopii yhtä hyvin kahteen
ilmiöön, kirjoita kohta terävämmäksi — älä valitse harhauttajaa löysemmin.

## `paljastus` — kolme riviä, sama muoto joka kerta

Muoto on lainattu `VAALIKESKUSTELU-LUKUOHJE-PLAN.md` § 2:sta.

| Kenttä | Mitä | Pituus |
|---|---|---|
| `mita` | Mitä tässä tapahtuu. Nimeä mekanismi, älä toista tekstiä. | 1 virke |
| `miksi` | Miksi se toimii — mihin se nojaa sinussa. | 1–2 virkettä |
| `sanot` | **Lause, jonka voi oikeasti sanoa ääneen.** | 1 virke |

`sanot` on pelin palkinto ja se kohta, joka jää käyttöön. Sen on oltava
sanottavissa oikeassa tilanteessa ilman että kuulostaa oppikirjalta — rauhallinen,
lyhyt, ei nokkela. Kysymysmuoto on usein paras, koska kysymys pysyy käytössä
silloinkin kun ei tiedä mitä ajattelee.

Hyvä: *"Mikä tarkalleen ottaen riittäisi? Kirjataan se ylös."*
Huono: *"Huomaan että siirrät maalitolppia, mikä on klassinen manipulaatiotekniikka."*

Rehellisillä kohdilla `sanot` on tyhjä tai kevyt — siinä ei ole mitään
torjuttavaa. `mita` kertoo miksi tämä on kunnossa ja `miksi` kertoo mikä siinä
näytti epäilyttävältä.

## Määrä

- Vähintään **4 kohtaa per ilmiö** (`--tarkista` kaatuu alle).
- Rehellisiä vähintään **25 %** koko pankista.
- Sama teksti ei saa esiintyä kahdesti koko pankissa.
