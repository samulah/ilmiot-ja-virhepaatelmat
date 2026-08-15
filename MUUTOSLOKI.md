# Muutosloki — Ilmiöitä (www.ilmiöt.fi)

## 15.8.2026 — Viides nostolohko: eniten kasvua

`scripts/paivita_suosio.py` laskee nyt myös **eniten kasvua** -listan, joka
näkyy `luonnokset/etusivu-nostot.html`:ssä luetuimpien ja googlatuimpien
rinnalla. Kolmen listan rivi käyttää luokkaa `.nostot-kolme`
(`minmax(270px, 1fr)`); ≤ 640 px:ssä se putoaa yhteen sarakkeeseen kuten ennenkin.

Uusi `kasvulista()` ja kenttä `kasvu` `data/suosio.js`:ssä
(`{u, n, edellinen, kasvu}`, enintään `KASVU_MAX` = 8 riviä). Kolme ehtoa:

- **`KASVU_LATTIA` = 5**, ei viikon ilmiön 10. Yhden sivun nostaminen viikon
  ilmiöksi on isompi väite kuin listan viides rivi, ja lattialla 10 lista olisi
  juuri nyt kaksirivinen — kaksi riviä ei ole lista.
- **`nyt > ennen` ehdottomana.** Pelkkä tasoitettu suhde nostaisi listalle myös
  paikallaan pysyneitä, koska tasoitus vetää kaikki kohti ykköstä alhaalta päin.
- **Viikon ilmiö pois.** Se on jo omana lohkonaan saman näkymän yläpuolella;
  sama kortti kahdesti näyttää virheeltä. Suodatus tehdään Pythonissa, joten
  `data/suosio.js` sisältää sen mitä ruudulla on.

Prosentti on sama tasoitettu suhde kuin viikon ilmiössä ((nyt+5)/(ennen+5)), ei
raaka: 0 → 19 on listalla +380 %, ei ääretön. Muuten kaksi lohkoa väittäisi
samasta sivusta eri luvun.

Prosentti näkyy **myös tuotannossa** (`NAYTA_LUVUT=false`): se ei paljasta
liikennemäärää, ja ilman sitä rivi olisi pelkkä nimi ilman perustetta
järjestykselle. Absoluuttiluvut (`1→6`) tulevat vain testivaiheessa.

Renderöijä `rakennaLista()` sai kaksi parametria: `muotoile(r)` (palauttaa
rivin oikean laidan tekstin tai tyhjän) ja `minRivit` (kasvulla 3 — alle sen
lohko piiloutuu). Samalla `ikkuna.replace('g','d')` -kikka korvattiin
eksplisiittisellä `IKKUNA_RAJAT`-taulukolla, koska `'kasvu'` ei olisi mennyt
regexistä läpi oikein.

Ensimmäinen ajo oikealla datalla 15.8.: Hanlonin partaveitsi +83 % (1 → 6),
DARVO +79 % (29 → 56), Halo-efekti +63 % (3 → 8). Tasan kolme riviä eli
minimissä — hiljaisemmalla viikolla lohko piiloutuu itsestään.

### 30 pv:n kasvu — kytkeytyy päälle itsestään 29.8.2026

Lohko sai välilehdet kuten luetuimmat ja googlatuimmat: `k7` ja `k30`
(`KASVU_LATTIA_30` = 10, isompi ikkuna kestää isomman lattian). Sivunäyttökysely
haetaan nyt **60 päivältä** 30:n sijaan, jotta edellinen 30 pv:n jakso on
ylipäätään olemassa. Rajaus tehdään Pythonissa, joten leveämpi haku ei muuta
mitään muuta lukua.

**Vertailujakso skaalataan päivätahdiksi.** Kanta alkaa 1.7.2026; 15.8.
ajettuna edellinen 30 pv on 16.6.–15.7., josta dataa on 15 päivää eli puolet.
Raakoja summia ei voi verrata kun toinen ikkuna on puolityhjä — jokainen sivu
näyttäisi kaksinkertaistuneen. Vertailuluku kerrotaan siksi arvolla
`ikkunan pituus / katetut päivät` (nyt ×2,00), ja saate sanoo
"(osin arvioitu)". Skaalaus on **konservatiiviseen suuntaan**: vertailuluku
kasvaa, joten kasvuprosentti pienenee — se ei voi keksiä kasvua jota ei ole.
Kun kate on täysi, kerroin on 1,0 eikä koodi tee mitään; se lakkaa vaikuttamasta
itsestään eikä vaadi siivousta. Alle `KASVU_KATE_MIN` = 10 päivän katteesta ei
kerrota mitään: 3 päivästä ei ekstrapoloida kuukautta.

### Julkaisupäiväsuodatin — kasvulistat valehtelivat uutuuksista

Ensimmäinen 30 pv:n ajo tuotti kärkeen kolme riviä muotoa `0 → 12`:
*1 %:n sääntö* (julkaistu 14.7.), *Viherpesu* (6.7.) ja *Keskiarvoharha*.
Ne eivät kasvaneet vaan **ilmestyivät** — sivu jota ei ollut olemassa
vertailujakson aikana on aina "kasvanut nollasta". Sivustolla on 26 sivua
julkaistu 5.8. tai sen jälkeen, joten sama vika olisi täyttänyt myös 7 pv:n
listan seuraavina viikkoina.

Uusi `ehti_mukaan()` vaatii `datePublished <= vertailujakson alku`.
Julkaisupäivät luetaan sivujen JSON-LD:stä `lue_julkaisupaivat()`:llä, joka oli
jo olemassa dashboardia varten; kaikilla 139 sivulla päivä on olemassa, joten
suodatin ei pudota ketään vahingossa. 30 pv:n kelpoisuusraja on jakson
**todellinen** alku `max(ed30_alku, vanhin päivä kannassa)` = 1.7.2026, ei
nimellinen 16.6. — vertailuluku on laskettu siitä päivästä, joten kelpoisuuskin
on mitattava siitä.

Sama suodatin lisättiin `valitse_viikon_ilmio()`:hon. Tällä viikolla se ei
muuta valintaa (*Rage bait* on julkaistu 6.7. eli ennen vertailujaksoa 1.–7.8.),
mutta 14.8. julkaistut 12 sivua olisivat olleet ensi maanantaina ehdolla
pelkällä olemassaolollaan.

Ero listassa on iso: skaalattu ja suodatettu 30 pv:n kärki on DARVO +89 %
(50 → 99), Goodhartin laki +89 % (4 → 12), Välittäjän skimmaus +67 % (4 → 10) —
kaikki sivuja jotka olivat olemassa koko vertailujakson. Alle kolmen rivin
`k30` nollataan, jolloin välilehti piiloutuu itsestään.

Yleistys hyödyttää muitakin: `rakennaLista()` piilottaa nyt minkä tahansa
välilehden jonka takana ei ole rivejä, ja koko palkin jos vain yksi jää jäljelle.
Sama suoja koskee googlatuimpien 30 pv:tä jos GSC-kysely puuttuu.

Bugi matkan varrella: `.nosto-valilehdet` on `display: flex`, joka **kumoaa
selaimen oman `[hidden]`-säännön** — palkki jäi näkyviin vaikka JS asetti
attribuutin. Korjattu erillisellä `.nosto-valilehdet[hidden] { display: none }`
-säännöllä, samalla tavalla kuin `.nostot[hidden]` ja `.nosto[hidden]` jo tekevät.

Tarkistettu Chromiumilla 1280/900/390 px: ei JS-virheitä, 3 saraketta leveällä
ja 1 mobiilissa, sekä `NAYTA_LUVUT` true- että false-tilassa. Molemmat haarat
testattu: nykytila (ei välilehtiä) ja simuloitu `k30` (kaksi välilehteä,
klikkaus vaihtaa listan ja päivärajat oikein). `index.html` ei muuttunut —
tuotantoinjektio on yhä tekemättä.

### Yöajo siirretään NAS:ille

`scripts/nas_asennus.sh` pystyttää ajon aina päällä olevalle Linux-NAS:ille.
Työaseman cron on kommentoitu pois (`# SIIRRETTY NASILLE 15.8.2026`),
varmuuskopio otettu ennen muutosta. Syy: WSL:n cron ajaa vain kun WSL on
käynnissä, ja kolme väliin jäänyttä yötä piilottaa lohkot etusivulta
`TUOREUS_VRK`-tarkistuksen takia.

Skripti on idempotentti ja siinä on `--tarkista`-tila joka ei muuta mitään.
Se tarkistaa esivaatimukset, kloonaa repon (GitHub-repo on julkinen, joten
kloonaus ei tarvitse avainta), luo venvin repon **ulkopuolelle** jottei
`git status` sotkeennu, asentaa psycopg2-binaryn, testaa TCP-yhteyden kantaan,
luo SSH-avaimen ja lisää webhotellin `known_hosts`-tiedostoon.

Kaksi yksityiskohtaa jotka olisivat muuten kaatuneet hiljaa yöllä:

- **`known_hosts`.** `laheta()` käyttää `BatchMode=yes`:iä, joka ei voi kysyä
  isäntäavaimen vahvistusta kun tty puuttuu. Tuntematon isäntä = epäonnistuminen
  joka yö ilman että kukaan huomaa. Asennus ajaa `ssh-keyscan`:in.
- **`git pull` ennen ajoa.** Skripti lukee ilmiölistan `index.html`:stä ja
  julkaisupäivät sivujen JSON-LD:stä. Vanhentunut kopio jättäisi uudet ilmiöt
  pois listoilta ja pudottaisi ne julkaisupäiväsuodattimesta.

Kopioitavaa käsin on kaksi tiedostoa, koska niitä ei voi generoida eivätkä ne
ole versionhallinnassa: `.suosio.env` ja `data/.viikko-historia.json`.
Jälkimmäinen kantaa viikon ilmiön karenssin; ilman sitä karenssi alkaa tyhjästä.

**Vain yksi kone saa ajaa `--laheta`:n.** Ilman lippua ajavia koneita voi olla
monta, mutta kaksi lähettäjää tarkoittaisi kahta eri viikon ilmiötä.

### Tuotantoon vienti kesken

Livepalvelimen `index.html` on 15.8. klo 10:33 kirjoitettu, mutta tavulleen
sama kuin injektiota edeltävä versio (md5 `7ad2675f`, 127 188 tavua) — eli
nostoja ei ole livenä, ja etusivulla lukee yhä "Päivitetty 14.8.2026".
Paikallinen `index.html` (145 kt) on vietävä uudelleen. Vertaa aina md5:tä,
älä tiedoston olemassaoloa; tämä on sama deploy gap joka on purrut ennenkin.

### Nostot julkaistu etusivulle

`--tuotanto` ajettu: `index.html` 127 kt → 145 kt, `NAYTA_LUVUT=false` eli
lukumäärät piilossa, vain järjestys ja kasvuprosentti näkyvät. Ajo on
idempotentti — toinen peräkkäinen `--tuotanto` tuotti md5-identtisen tiedoston.
Etusivun haku näkee yhä tasan 139 `.hub-kortti`-elementtiä eli nostokortit
(2 kpl, luokka `.nosto-kortti`) eivät päätyneet hakutuloksiin tai arvontaan.

Julkaisun rutiini CLAUDE.md:n mukaan: `muutokset.html` sai merkinnän lukijan
kielellä (mukaan lukien kappale yksityisyydestä — lokipohjaiset summat, ei
evästeitä eikä kävijäseurantaa), `dateModified` 2026-08-15 molempiin,
etusivun `paivitetty-btn` samaan päivään, ja `build_sitemap.py` ajettu
(155 URLia). `search-index.js` ei muuttunut, kuten pitikin: nostot ovat
dynaamisia eivätkä sisältöä.

**Palvelinpolku korjattu.** Dokumenttijuuri on `/public_html/kendom/ilmiöt`
(todiste: `https://www.ilmiöt.fi/kendom/` → 404 mutta `search-index.js` ja
`style.css` vastaavat juuresta). `index.html` lataa `data/suosio.js`
suhteellisena, joten tiedoston on oltava index.html:n vieressä:
`SFTP_POLKU=/public_html/kendom/ilmiöt/data`. Aiempi `/public_html/data` ei näy
verkossa lainkaan.

**Avoin este: SSH-avainta ei ole.** `.suosio.env`:n
`SFTP_KEY=/home/samu/.ssh/id_ed25519_ilmiot` osoittaa tiedostoon jota ei ole
olemassa, joten `--laheta` ei ole koskaan ajettu onnistuneesti eikä
`data/suosio.js` ole palvelimella. Etusivu on siihen asti turvallisesti
puolikas: `TUOREUS_VRK`-tarkistus piilottaa neljä lohkoa datan puuttuessa ja
satunnainen ilmiö toimii ilman dataa, joten julkaisu ei riko mitään — se vain
ei vielä näytä listoja.

## 14.8.2026 — Googlatuimmat mukaan ja yöajo pystyyn

Neljäs lohko `fact_gsc_haku`-taulusta: **googlatuimmat**, eli sivut joilla on
eniten näyttöjä Google-hakutuloksissa. Se ei ole luetuimpien toisinto vaan eri
mittari — näyttö tarkoittaa että sivu näkyi hakutuloksissa, ei että joku luki
sen — ja järjestys eroaa selvästi:

| | Luetuimmat 7 pv | Googlatuimmat 7 pv |
|---|---|---|
| 1 | DARVO 73 | DARVO 163 |
| 2 | Rage bait 19 | Rage bait 98 |
| 3 | Halo-efekti 8 | Hyvesignalointi 92 |
| 4 | Hanlonin partaveitsi 6 | Dunning–Kruger 82 |

Ero on itsessään tieto. Hyvesignalointi on Googlessa kolmas mutta luetuissa
kuudes; Dunning–Kruger ei näy luetuimmissa lainkaan. Molemmat ovat
title/kuvaus-ongelmia, eivät sisältöongelmia.

Dashboard sai neljä uutta osiota, joista käyttökelpoisin on **"Näkyvyys ilman
klikkejä"** (≥ 30 näyttöä, 0 klikkiä 30 pv). Kärjessä *hyvesignalointi*: 236
näyttöä, 0 klikkiä, keskisija 7,1 — vertailukohtana *darvo suomeksi* konvertoi
15,5 % sijalta 2,7. Lisäksi hakulausekkeet (202 kpl), sivutason Google-taulukko
ja lista sivuista jotka saavat lukijoita muualta kuin hausta. Keskisija on
näytöillä painotettu, ei suora keskiarvo — muuten yhden näytön päivä painaisi
yhtä paljon kuin sadan.

Kysely on erillinen `SUOSIO_SQL_GSC` ja **valinnainen**: ilman sitä lohko jää
pois eikä muu putki häiriinny.

**Yöajo pystyssä** cronissa klo 3:10, `--laheta` **pois** — mikään ei mene
livepalvelimelle, vain `luonnokset/` päivittyy. Komento testattu riisutussa
ympäristössä (`env -i`, kotihakemisto, minimaalinen PATH), poistumiskoodi 0;
cron ajaa kotihakemistosta, joten skriptin polku on absoluuttinen. Jokainen ajo
kirjoittaa aikaleimallisen lohkon `~/.suosio.log`:iin, jotta hiljainen
epäonnistuminen erottuu onnistuneesta.

Testit 43/43 läpi, mukaan lukien että kahden listan välilehdet eivät vaikuta
toisiinsa ja että googlatuimmat piiloutuu datan puuttuessa.

Avoin: viikon ilmiö on nyt Rage bait, joka on myös luetuimpien #2. Päällekkäisyys
hyväksytään toistaiseksi — algoritmi on oikein, vika on otoskoossa (7 pv:ssä on
171 lukukertaa 40 sivulle, vain 2 sivua ylittää lattian 10). Kun liikenne kasvaa,
sama koodi alkaa toimia ilman muutoksia.

## 14.8.2026 — Suosiodata luonnostettu: luetuimmat, viikon ilmiö, satunnainen ilmiö

Uusi `scripts/paivita_suosio.py` hakee liikennekannasta sivukohtaiset lukukerrat
ja kirjoittaa niistä kolme tiedostoa. **Mitään ei ole julkaistu** — kaikki elää
`luonnokset/`-kansiossa haarassa `suosio-ja-nostot`, `index.html` on koskematon.

**Arkkitehtuuri.** Yöajo ei kirjoita `index.html`:ään. Suosiodata on erillisessä
`data/suosio.js`:ssä (8 kt demodatalla), jonka etusivu lataisi `defer`-skriptinä
ja joka on ainoa yöllä siirtyvä tiedosto. Vaihtoehto — data suoraan HTML:ään —
tarkoittaisi 300 kt etusivun työntämistä palvelimelle joka yö, eli tämän
projektin dokumentoidun pahimman vikatilan (deploy gap) automatisointia.

Datatiedostossa on vain slugit ja luvut. Nimet, kuvaukset, värit ja numerot
haetaan selaimessa sivun omista `.hub-kortti`-elementeistä, samaan tapaan kuin
haku tekee jo nyt. Siksi ilmiön uudelleennimeäminen tai poisto ei voi jättää
suosiolohkoon haamurivejä, eikä toista ylläpidettävää ilmiölistaa synny.

**Kolme lohkoa** injektoidaan `NOSTOT-ALKU`/`NOSTOT-LOPPU`-merkkien väliin
katnavin jälkeen, ennen ensimmäistä kategoriaa — kategorioiden väliin sijoitettu
lohko katkaisisi `.hub-kategoria + .hub-kategoria` -sisarussäännön. Ajo on
idempotentti. Kohde on oletuksena `luonnokset/etusivu-nostot.html`, `--tuotanto`
kirjoittaisi `index.html`:ään.

Kortit käyttävät luokkia `.nosto-kortti` / `.nosto-rivi`, **eivät** `.hub-kortti`:a:
`index.html:2709` kerää kaikki `.hub-kortti`-elementit ja sama taulukko ajaa
hakua, nuolinäppäinnavigaatiota ja `randomIlmio()`:ta, joten duplikaatti näkyisi
hakutuloksissa kahdesti ja arvonnassa kaksinkertaisella painolla. Nostolohko
pysäyttää myös omat `keydown`-tapahtumansa, koska rivin 2813 käsittelijä
fokusoi hakukentän jokaisesta tulostuvasta merkistä.

**Viikon ilmiö** on suhteellisesti eniten noussut sivu, kolmella suojalla:
vähintään 20 lukukertaa viikossa (lattia), järjestys tasoitettuna kaavalla
(nyt+5)/(ennen+5), ja 4 edellistä valintaa karenssissa tilatiedostossa
`data/.viikko-historia.json`. Ilman näitä 1 → 4 näyttöä olisi +300 % ja lista
olisi pelkkää kohinaa. **Valinta lasketaan vain maanantaisin** ja pysyy koko
viikon; muina öinä luvut päivittyvät mutta valinta ei. Jos yksikään sivu ei
ylitä lattiaa, lohko piiloutuu — hiljainen tyhjä on parempi kuin arvottu nousija.

**Degradaatio.** Jos `window.ILMIO_SUOSIO` puuttuu tai `paivitetty` on yli 3 vrk
vanha, viikon ilmiö ja luetuimmat piiloutuvat itsestään; satunnainen ilmiö
toimii silti, koska sen lähde on sivun oma korttilista. Epäonnistunut yösiirto
ei siis näytä lukijalle viime kuun "luetuimpia 7 päivää".

**Testattu selaimessa** (playwright, 34 tarkistusta): renderöinti, välilehdet,
sekoituspussi (8 klikkausta = 8 eri ilmiötä, ei viikon ilmiötä eikä
kärkikolmikkoa), haku ja nuolinavigaatio ehjiä, 139 korttia yhä 139, ei
duplikaatteja hakutuloksissa, näppäimistö ei varasta fokusta, molemmat
degradaatiotilat, mobiili 380 px ilman vaakavieritystä, konsoli puhdas.

**Kaksi vikaa löytyi ja korjattiin testatessa:**

- Kategoriajäsennin hukkasi viimeisen kategorian 10 korttia (139 → 129), koska
  `hub-tyhja`-lopetin on sisennetty ja tyhjän rivin takana. Rajaus on nyt
  sijaintipohjainen, ja jäsennin **kaatuu** jos korttimäärä ei täsmää raakaan
  `hub-kortti`-laskuriin — sama opetus kuin `paivita_maarat.py`:n `maara`-tarkistuksessa.
- Dashboardin "Laskijat" listasi nousseita sivuja, koska lista täyttyi loppuun
  kun aitoja laskijoita oli vain yksi. Suunta on nyt suodatusehto, ei
  järjestysperuste.

**Kanta.** `scripts/suosio_lukijatunnus.sql` luo vain luku -roolin
(`default_transaction_read_only`, 30 s `statement_timeout`, 3 yhteyttä).
Kysely annetaan `.suosio.env`:n `SUOSIO_SQL`:ssä, koska tähtimallin taulunimet
ovat kantakohtaisia; se palauttaa kolme saraketta (polku, pvm, nayttoja) ja
kaikki ikkunointi tehdään Pythonissa missä sen voi testata. Osoite ja tunnukset
eivät ole versionhallinnassa; `.gitignore` sai `.suosio.env`:n, generoidut
tiedostot ja korjauksen `datalake-analysis/` → `datalake_analysis/` (väliviiva
ei ole koskaan osunut oikeaan kansioon, joten GSC-viennit ovat gitissä).

**Ei vielä tehty:** kantayhteys puuttuu, joten luvut ovat toistaiseksi
`--demo`-tilan synteettistä dataa GSC-viennistä. Skeema selvitetään
`--skeema`-lipulla kun lukijatunnus on luotu. Ennen tuotantoa on
ristiintarkistettava, ettei faktataulu laske botteja: sivusto saa GSC:n mukaan
~82 klikkiä/kk, joten kertaluokkaa suurempi summa tarkoittaa crawlereita.
`muutokset.html`:ää ei ole päivitetty eikä pidäkään ennen julkaisua.

## 14.8.2026 — Julkaistu 12 ilmiötä: 127 → 139, neljä kategoriaa kasvoi

Yksi ajo, kolme erää: vaalierä (3 sivua, luonnokset 4.8.), pimeät kuviot (5) ja
tekoälyhuijaukset (4). `lisaa_ilmiot.py --kirjoita` numeroi 120 vanhaa sivua
uudelleen; pienin muuttunut numero on 9. **Koostesivu (vaalikeskustelun lukuohje)
jätettiin julkaisematta** — se ei ole ilmiö eikä kulje `lisaa_ilmiot.py`:n läpi,
ja sen kausiluonteinen hyöty alkaa vasta kampanjahaussa (tavoite joulukuu 2026).

| Kategoria | Ennen | Jälkeen | Uudet |
|---|---|---|---|
| Vallan rakenteet | 7 | 8 | vaalilupauksen-hinnoittelu (8) |
| Huijaukset ja petokset | 11 | 14 | aaniklooni-huijaus (77), smishing (78), deepfake-sijoitushuijaus (79) |
| Alustatalous ja algoritmit | 10 | 17 | vaalikone-efekti (105), tekoalypsykoosi (106), evasteansa (107), piilokulut (108), pakotettu-jatkuvuus (109), confirmshaming (110), oletusasetusansa (111) |
| Tilastoilla valehtelu | 8 | 9 | kannatusmittausten-virhemarginaali (129) |

**Faktantarkistus ennen julkaisua — kolme virhettä löytyi.** Kaikki tarkistettavat
väitteet ajettiin lähteitä vasten, myös vaalierän 4.8. kirjoitetuilta sivuilta:

- **`kannatusmittausten-virhemarginaali`: virhemarginaali oli väärin.** Sivu
  väitti ±1,2 prosenttiyksikköä noin 2 000 vastaajan otoksella. Ylen ja
  Taloustutkimuksen oma menetelmäkuvaus: puoluekantansa ilmoittaa noin 1 200
  vastaajaa, ja marginaali riippuu kannatustasosta — 20 %:n kannatuksella ±2,3,
  10 %:n ±1,7 ja 5 %:n ±1,3. Korjattu, ja samalla sivu kertoo nyt sen mitä
  vanha versio piilotti: **marginaali ei ole yksi luku.** Myös eron kerroin
  tarkennettiin: "karkeasti kaksinkertainen" on oikea nyrkkisääntö kahden
  kärkipuolueen tapauksessa, mutta Suomen monipuoluetilanteessa kerroin on
  lähempänä 1,5:tä. Kynnysluku "alle kaksi prosenttiyksikköä" nostettiin 3–4:ään.
- **`vaalikone-efekti`: väärä etunimi.** Tutkijan nimi on **Tom** Louwerse, ei
  Thomas (Louwerse & Rosema, *Acta Politica* 49, 286–312, 2014). Kaksi esiintymää.
- **`vaalilupauksen-hinnoittelu`: 404-linkki.** CPB:n Wikipedia-artikkelin nimi on
  *Bureau for Economic Policy Analysis*, ei *CPB Netherlands Bureau…*.
- **`deepfake-sijoitushuijaus`: 404-linkki.** fi-Wikipedian artikkeli on
  *Syväväärennös*, ei *Syväväärennys*.

Neljä tarkennusta, joissa väite oli oikea mutta epätarkka:

- **CNIL:n sakot** ovat 31.12.2021 tehdyistä päätöksistä, jotka julkistettiin
  6.1.2022 → "tammikuussa 2022" muutettiin muotoon "vuodenvaihteessa 2021–2022".
  Summat (Google 150 M€, Facebook 60 M€) ja peruste (hylkääminen vaati useamman
  klikkauksen kuin hyväksyminen) pitävät paikkansa.
- **Smishing-sivun lähettäjätunnusrekisteri** oli epämääräinen. Traficomin
  määräyksen mukaan organisaatioiden on pitänyt **luvittaa** käyttämänsä
  lähettäjätunnukset ennakkoon 4.5.2026 alkaen. Sivu kertoo nyt tämän.
- **Tekoälypsykoosi sai alkuperän:** termin esitti tanskalainen psykiatri Søren
  Dinesen Østergaard pääkirjoituksessaan 2023, ja se levisi julkisuuteen 2025.
  Lisätty myös psykiatrien esittämä kritiikki (termi koskee vain harhaluuloja) ja
  linkki englanninkieliseen Wikipedia-artikkeliin *Chatbot psychosis*.
- **Villin kortin ehto täyttyi.** Suunnitelma sanoi: kirjoita tekoälypsykoosi vain
  jos termi näkyy vielä syksyllä. Sillä on nyt oma Wikipedia-artikkeli ja
  vertaisarvioitua kirjallisuutta → julkaistiin.

Vahvistetut, muuttumattomina jätetyt: EU-komission 2022 selvityksen 97 %,
asetus 1008/2008 art. 23, kuluttajansuojalain 14 vrk etämyynnissä, Gabaix &
Laibson (QJE 2006), Johnson & Goldstein (*Science* 2003), privacy zuckering =
EFF:n Tim Jones 2010, Traficomin ja tietosuojavaltuutetun työnjako evästeissä,
Finanssivalvonnan varoituslistat, Sharma ym. 2023, Yle 1996, CPB vuodesta 1986,
Australian PBO, Groves & Lyberg 2010, AAPOR 2017. **Kaikki 18 ulkoista linkkiä
palauttavat 200.**

**Kategoriatekstit kirjoitettiin uusiksi neljälle kategorialle** (`kategoriat/*.md`).
Määrät korjattiin otsikoita ja leipätekstiä myöten ("Kymmenen ilmiötä" →
"Seitsemäntoista"), ja jokainen uusi sivu sai paikkansa kategorian omassa
jäsennyksessä — alustatalous sai viidennen kerroksen ("Miten valinta ohjataan"),
huijaukset kappaleen tekoälyn roolista kaavassa. **Dark patterns -termin neljä
suomalaista muotoa** (*dark patterns*, *synkät suunnittelumallit*, *pimeät
käytännöt*, *deceptive patterns*) mainitaan nyt kategoriatekstissä, kuten
suunnitelma edellytti — yläkäsitesivua ei tehty.

**Ajojärjestys:** `lisaa_ilmiot.py --kirjoita` → `build_kategoriat.py` (13 sivua)
→ `paivita_maarat.py` (index, tietoa, llms.txt) → `build_liittyvat.py` (133/139)
→ index.html:n nappi ja JSON-LD 14.8. → `muutokset.html` → `build_sitemap.py`
(155 URLia) → `build_search_index.py` (152 sivua, 437 kt).

**Ajautuma kiinni: etusivun `<title>` oli jäänyt 127:ään.** `paivita_maarat.py`
päivitti näkyvät määrät, kategorialaskurit ja ItemListin, mutta ei titleä,
`og:title`ea, `twitter:title`ea eikä JSON-LD:n `name`-kenttää — skriptin kuviot
eivät osuneet titlen sanamuotoon "— N ilmiötä". Docstring kuitenkin lupasi, että
ne päivittyvät. Lisättiin kuvio `maara=4`-tarkistuksella, joten sama ei toistu
hiljaisena: jos titlen muoto muuttuu, skripti kaatuu sen sijaan että jättäisi
luvun vanhaksi. Etusivun title on SERPin otsikko, joten virhe olisi näkynyt
hakutuloksissa.

**Tarkistettu julkaisun jälkeen:** numerot 1–139 ehjä sarja, 139 hub-korttia,
ei jäljelle jäänyttä `noindex`-merkintää (paitsi `random.html`, jossa se kuuluu
olla), ei `../`-polkuja, ei rikkinäisiä sisäisiä linkkejä, FAQPage-schema
yhdeksällä uudella sivulla.

## 14.8.2026 — Tekoälyhuijaukset-klusteri luonnosteltu (4 sivua, ei julkaistu)

Klusteri 2 suunnitelmasta `luonnokset/UUDET-KLUSTERIT-PLAN.md` § 4. Generaattori
`scripts/build_tekoalyhuijaukset_luonnokset.py`, pohjana `qr-koodihuijaus.html`.
**Mitään ei julkaistu.**

Sivut: **aaniklooni-huijaus** (voice cloning / vishing, 76), **smishing**
(SMS phishing, 77), **deepfake-sijoitushuijaus** (78) ja **tekoalypsykoosi**
(AI psychosis, 101). Rakenne sama kuin pimeissä kuvioissa: vastauslohko +
FAQPage-schema ja kysymysmuotoiset H2:t jo luonnoksessa. Sanamäärät 278–335.

**Poikkeama suunnitelmaan — kategoria.** Suunnitelma sijoitti kaikki neljä
kategoriaan Huijaukset ja petokset (11 → 15). *Tekoälypsykoosi ei ole huijaus:*
kukaan ei huijaa ketään, vaan myötäilevä vastaustyyli vahvistaa ajattelua.
Se olisi huijauskategoriassa väärä lupaus lukijalle, joten se meni
**Alustatalous ja algoritmit** -kategoriaan (`parasosiaalinen-suhde` ja
`kaikukammio` ovat siellä). Huijaukset kasvaa 11 → 14. Generaattori osaa
korvata kategoriakentät (murupolku, `articleSection`, kategoriasivun linkki)
sivukohtaisesti; muilla kolmella korvausta ei tehdä, koska pohja on jo oikeassa
kategoriassa.

**Villi kortti kirjoitettiin silti.** Suunnitelma jätti *tekoälypsykoosin*
ehdolle ("kirjoita vasta jos termi näkyy vielä syksyllä"). Luonnos ei maksa
julkaisua, joten **ehto siirrettiin julkaisuhetkeen**. Sivu sanoo suoraan, ettei
kyseessä ole diagnoosi, ja ohjaa terveydenhuoltoon; se on ainoa erän sivu, jossa
aihe on terveysläheinen.

**Numerointi menee päällekkäin.** Kumpikin luonnoserä on numeroitu ikään kuin se
julkaistaisiin yksin, joten `evasteansa` ja `tekoalypsykoosi` kantavat molemmat
numeroa 101 (kummankin paikka on Alustatalous ja algoritmit -kategorian lopussa).
Kumpi julkaistaan ensin, se saa paikan; `lisaa_ilmiot.py` laskee loput. Kirjattu
kansion `index.html`:ään ja suunnitelmaan.

**Tarkistettavia faktaväitteitä kolme:** SMS-lähettäjätunnusrekisteri Suomessa,
Finanssivalvonnan varoituslistat ja se, onko *tekoälypsykoosi* syksyllä yhä
elävä termi. Loput nojaavat vakiintuneisiin lähteisiin (Sharma ym. 2023
myötäilyvinoumasta, Mitnick 2002).

## 14.8.2026 — Pimeät kuviot -klusteri luonnosteltu (5 sivua, ei julkaistu)

Klusteri 1 suunnitelmasta `luonnokset/UUDET-KLUSTERIT-PLAN.md` § 3.
Generaattori `scripts/build_pimeat_kuviot_luonnokset.py`, tuotos
`luonnokset/` (5 sivua; erä syntyi kansioon `luonnokset-pimeat-kuviot/`, joka
yhdistettiin samana päivänä — ks. alla).
**Mitään ei julkaistu eikä juuren tiedostoja muutettu** — `muutokset.html`,
sitemap ja hakuindeksi pysyvät ennallaan.

Sivut: **evasteansa** (cookie consent dark pattern), **piilokulut** (drip
pricing), **pakotettu-jatkuvuus** (forced continuity), **confirmshaming**,
**oletusasetusansa** (privacy zuckering). Alustavat numerot 101–105,
kategoria **Alustatalous ja algoritmit** (10 → 15). Uutta kategoriaa ei tarvita,
joten julkaisu käy `lisaa_ilmiot.py`:llä ilman `--kortit-valmiina`-lippua.

**Pohjana `aanekas-vahemmisto.html`** — sama kategoria, joten murupolkua,
`articleSection`-kenttää tai hub-ankkuria ei tarvinnut korvata lainkaan.
Erot media-erän generaattoriin:

- **Vastauslohko ja FAQPage-schema kirjoitetaan jo luonnokseen.** Aiemmin ne
  lisättiin jälkikäteen `seo_vastauslohko.py`:llä ja vain top-15-sivuille; uusi
  sivu syntyi ilman. Kaksi kysymystä per sivu, sama teksti lohkossa ja schemassa.
- **Kysymysmuotoiset H2:t alusta asti** (auditin § 6b: kilpailijoilla lähes
  kaikki, ilmiöt.fi:llä 52/443 eli 12 %). Kolmesta H2:sta kaksi on kysymys;
  kolmas on normin vaatima "Tunnistaminen ja vastakeinot:".
- **Korjaus `alikansiopolut()`-listaan:** murupolun `href="kategoria-*.html"`
  tarvitsee `../`-etuliitteen luonnoskansiossa. Media-erän generaattori ei sitä
  tunne, koska kategorialinkit lisättiin sivuille vasta 28.7. — sama vika on
  vaalierän sivuilla, mutta se korjaantuu julkaisussa itsestään.

**Sanamäärät 311–351** (mittaus: ilmiölohko `<aside>`:en asti, "Lue lisää"
mukaan lukien). Sivuston oma mediaani samalla mittarilla on 333 ja keskiarvo
338, joten erä osuu keskelle jakaumaa eikä venytä normia.

**Rajattu ulos tietoisesti:** yläkäsitesivua ("Mitä ovat dark patterns?") ei
tehdä — se kilpailisi omaa kategoriasivua vastaan. `tilausansa` (roach motel),
`painostusclose` (keinotekoinen niukkuus) ja `houkutinvaihtoehto` (decoy)
kattavat jo oman kuvionsa; niihin linkitetään eikä niitä kirjoiteta uudestaan.
Nimeämiskysymys (§ 3: neljä liikkeellä olevaa muotoa) ratkaistiin sivutasolla
yksittäisten kuvioiden nimillä; **kategoriatekstiin `kategoriat/alustatalous-ja-algoritmit.md`
kaikki neljä muotoa on vielä lisäämättä.**

**Julkaisujärjestys ei muutu:** vaalierän 3 luonnosta (takaraja syksy 2026)
julkaistaan ensin. Huomaa, että `lisaa_ilmiot.py`:n `UUDET`-taulukko sisältää yhä
loppuun ajetun media-erän — se vaihdetaan julkaisun yhteydessä, ja taulukko
**korvataan, ei täydennetä**.

## 14.8.2026 — Luonnoskansiot yhdistetty yhdeksi

`luonnokset-media/` ja `luonnokset-pimeat-kuviot/` → **`luonnokset/`**
(12 tiedostoa: 8 ilmiöluonnosta, koostesivu, 3 suunnitelmaa). Vanhat kansiot
poistettu. Syy: erien selaaminen, julkaisujärjestyksen näkeminen ja
tarkistuslistojen ylläpito kolmessa kansiossa oli turhaa jakoa — kaikki erät
kulkevat saman `lisaa_ilmiot.py`:n läpi.

**Kolme `index.html`:ää yhdistetty yhdeksi.** Uudessa hakemistossa neljä osiota:
vaalierä (3, loka–marras 2026), koostesivu (1, joulukuu 2026), pimeät kuviot (5)
ja suunnitelmat. Yhteinen julkaisun tarkistuslista on nyt yhdessä paikassa;
media-erän vanhentuneet kohdat (kategoria 13, laskurit x/13) poistettiin, koska
ne on ajettu 5.8.

**Skriptien vakiot osoittavat kaikki `luonnokset/`-kansioon:** `lisaa_ilmiot.py`
(`LUONNOKSET`), `build_kategoriat.py` (`LUONNOSKANSIO`), `build_media_luonnokset.py`,
`build_media_kategoria_luonnos.py` ja `build_pimeat_kuviot_luonnokset.py` (`OUT`).
Generaattorit kirjoittavat vain omat sivunsa yli, joten yhteinen kansio kestää
uudelleenajon. `build_klusteri_luonnokset.py`:n maininta on päivätty historiaa
eikä sitä muutettu.

**Sivujen sisältöä ei koskettu.** Kansiosyvyys ei muuttunut (yhä yksi taso),
joten `../`-etuliitteet, `noindex`-merkinnät ja PREV/NEXT-ketjut ovat ennallaan.
Juuren tiedostoihin ei koskettu — ei sitemap-, hakuindeksi- eikä
`muutokset.html`-muutosta.

**Samalla:** kansiosta poistettiin sen aiempi sisältö, 16 jo julkaistua
luonnoskopiota heinäkuulta (`UUDET-JUTUT-PLAN.md` oli merkinnyt kansion
turhaksi jo 28.7.). Ne ovat git-historiassa.

## 13.8.2026 — GSC-auditti ja geneeristen titlejen korvaus (11 sivua)

Auditti `GSC-AUDIT-2026-08-13.md`, data `datalake_analysis/13082026/`.
Jakso 18.6.–11.8.: **82 klikkiä / 3 783 näyttöä / CTR 2,17 % / sija 9,46**
(edellinen otos 19 / 1 419 / 1,34 % / 11,1). `darvo.html` = 71 % klikeistä.

**Löydös.** Sijoitusvälillä 6–12 vakioituna geneerisen titlen
(`X — mitä se tarkoittaa?`) sivut saivat 1 597 näyttöä ja 4 klikkiä (0,25 %,
ka. sija 9,10); kuvailevan titlen sivut 899 näyttöä ja 8 klikkiä (0,89 %,
ka. sija 9,12). Nuo 11 sivua kantavat 42 % koko sivuston näyttökerroista.
SERP-tarkistus vahvistaa mekanismin: haulla *hyvesignalointi* yläpuolella ovat
fi.wikipedia, Wikisanakirja ja Urbaani Sanakirja — title lupasi täsmälleen sen,
minkä lukija sai jo ylempää. Klikkiotos on pieni (p ≈ 0,06–0,10), näyttöotos ei.

**Historia — tämä on peruutus, ei uusi koe.** Commit `fe90451` (25.7.,
"top 15 titlemuutokset") vaihtoi 15 suurimman sivun titlet kuvailevista
geneerisiksi (esim. "Hyvesignalointi — hyvettä yleisölle" → "— mitä se
tarkoittaa?"). Saman erän darvo sai kuvailevan titlen ja on ainoa toimiva sivu.
Aiempi kirjaus "28.7. title-remontti ei nostanut CTR:ää" osoittautui vääräksi
attribuutioksi: `9f07192` ja `8748380` eivät muuttaneet **yhtäkään** title-riviä
(0 osumaa diffissä) — niissä testattiin vastauslohkoa ja FAQPage-schemaa.
Titleä on muutettu tasan kerran, ja väärään suuntaan.

**Korjaus.** `scripts/korjaa_titlet.py` (kuivaharjoitus oletuksena,
`--kirjoita` kirjoittaa; ohittaa sivun jos nykyinen title ei vastaa odotettua).
Uusi title seuraa kunkin sivun omaa H1-kulmaa, joka oli jo kirjoitettu hyvin.
`og:title` ja `twitter:title` päivitettiin samalla — 3 riviä / sivu.

**Tietoisesti koskematta:** metakuvaukset, `dateModified`, näkyvä
"Päivitetty"-päivä. Syy: seuraava GSC-otos mittaa yhtä muuttujaa, ja sitemapin
`lastmod` pysyy totena. **Siksi `build_sitemap.py`:tä ei ajettu.**
`build_search_index.py` ajettiin (140 sivua, 401 kt) — `search-index.js` ei
muuttunut, indeksi ei lue `<title>`-tagia.

**Kilpailija-analyysi (auditin §6b).** Haettu SERPistä termeillä, joilla sivusto
on sijalla 7–12. Yläpuolella on kaksi ryhmää: auktoriteetit (fi.wikipedia, Yle,
MTV) ja pitkät artikkelisivut. Lähiluettu kolme: `tietoviisas.fi` (~1 300 sanaa,
11 kysymysotsikkoa), `yksipeli.fi` (~1 200 sanaa, 10 kysymysotsikkoa, **kasino-
affiliate ilman tekijää ja päiväystä** — silti hyvesignaloinnissa yläpuolella),
`diletantti.fi` (~1 150 sanaa, 3 kaaviota, linkki 1999-tutkimukseen). ilmiöt.fi
on ~260 sanaa ja 4 otsikkoa. Sivusto voittaa sisäisessä linkityksessä (12–16
aiheenmukaista linkkiä vs. kilpailijoiden 0–3), tekijätiedossa, lähteissä ja
schemassa — ei riitä kompensoimaan 5-kertaista pituuseroa. **Sanamäärän normia
ei muutettu**; jännite kirjattu audittiin päätöksentekoa varten.

**Termiaukot korjattu.** Kilpailijat käyttävät suomalaisia rinnakkaistermejä,
jotka puuttuivat. Tarkistettu 10 sivua, 17 aukkoa.

- **Kirjoitusvirhe `upponneiden` → `uponneiden`, 14 esiintymää neljässä
  tiedostossa** (11 `sunk-cost-harha.html`:ssä), myös `<title>`, `og:title`,
  `twitter:title`, metakuvaus ja JSON-LD. Sivusto käyttää muualla oikeaa muotoa
  (`bait-and-switch`, `lowball-hinnoittelu`, `lapi-hinnalla-milla-hyvansa`) →
  virhe, ei tyylivalinta. GSC: *uponneet kustannukset* 21 näyttöä sijalla 26,5 —
  sivun suomenkielinen päätermi ei ole vastannut yhtäkään hakua.
- Lisätty ingressiin 2–4 sanan tarkennuksina: `doom scrolling` (välilyönnillä,
  19 näyttöä sija 10,3), `ylivertaisuusharha` + `ylivertaisuusvinouma`
  (dunning-kruger; Yle ja Target Training käyttävät), `Ockham`
  (occamin-partaveitsi), `hyveposeeraus`, `entäskunismi`. Sanamäärät
  483→487, 633→639, 526→529, 560→563, 608→618 — normi kestää.
- HTML validoitu HTMLParserilla: ei sulkeutumattomia tageja, strong/em tasan.
- `build_search_index.py` ajettu uudelleen.

**Etusivun title (auditin P4).** `Ilmiöt — 127 yhteiskunnallista ilmiötä
selitettynä | Ilmiöitä` → **`Manipulointi, propaganda ja huijaukset — 127
ilmiötä | Ilmiöitä`** (63 merkkiä). Vanha tähtäsi sanaan *ilmiöt*, jota ei haeta
intentiolla, ja änkytti. Päivitetty myös `og:title`, `twitter:title` ja
`CollectionPage`in `name` — `dateModified` ja `paivitetty-btn` koskematta.
Etusivu sai 17 näyttöä / 3 kk, joten ongelma on näyttöjen puute, ei CTR.
Vaihtoehdot punnittu SERP-haulla: *ajattelun vinoumat* olisi kannibalisoinut
`kategoria-psykologia-ja-kognitio.html`:n, *retoriset keinot* on lukion
ÄI4-kysyntää eikä sivustolla ole eetos/paatos/logos-sisältöä, *ilmiösanakirja*
on itse keksitty. Tiedostettu varaus: *manipulointi*-SERP painottuu
narsisti/parisuhde-kulmaan.

**Aihevalinta seuraavalle erälle:** `luonnokset-media/UUDET-KLUSTERIT-PLAN.md`.
Kolme klusteria (pimeät kuviot 5, tekoälyhuijaukset 4, argumentointivirheet 5),
kategoriasijoitukset ja päällekkäisyystarkistukset tehty. Kaksi ensimmäistä ovat
darvon asetelma (kysyntää, ei fi-Wikipediaa); kolmas on tietoinen
hyvesignalointi-ansa ja vaatii erillisen päätöksen. Suunnitelma sisältää myös
kieltolistan: ei lisää myyntikikkoja (15 sivua → 74 näyttöä) eikä
tilastotemppuja (8 → 21), eikä itse keksittyjä suomennoksia.

**Ei `muutokset.html`:ään:** lukija ei saa uutta luettavaa.

**Mittauspiste ~10.9.2026:** jos näiden 11 sivun CTR sijalla 6–12 ei ole
noussut tasolle 0,7–0,9 %, hypoteesi on väärä ja titlet voi palauttaa
skriptin taulukosta.

**Kaksi hypoteesia kaatui testissä** (kirjattu ettei niitä testata uudelleen):
*fi-Wikipedia-artikkelin olemassaolo syö klikin* — ero oli kokonaan darvo, ja
ilman sitä 0,79 % vs. 0,57 %, ei vaikutusta; tarkistettu Wikipedia-API:lla
kaikille 127 ilmiölle (35 artikkelia olemassa, 92 ei). *FAQ-schema nostaa
CTR:ää* — sekoittajana sijoitus (8,90 vs. 15,15), ei schema.

**Tekniikka livenä 13.8.:** kanoniset 301:t toimivat kaikista kolmesta
varianteista, live = local (12/12 md5), 5.8. julkaistut 14 sivua 200,
sitemap 143 URL:ää. Ei korjattavaa.

## 5.8.2026 — Suurhanke-erä (4) ja media-erä (10) julkaistu: 113 → 127 ilmiötä, 13. kategoria

`luonnokset-media/ANALYYSI.md`:n julkaisujärjestyksen kaksi ensimmäistä erää
kerralla. Kansioon jää enää vaalierän 3 luonnosta (loka–marras 2026) ja
`ANALYYSI.md`.

**Erä 1 — suurhankkeet (113 → 117), Projekti- ja ohjelmistokehitys.**
`lisaa_ilmiot.py --kirjoita`, `LUONNOKSET` osoittamaan `luonnokset-media/`.
Kortit ankkuroitiin `kuolonmarssi`n perään ketjuna, joten numerot ovat
54–57 (`lukittu-paatos`, `strateginen-aliarviointi`, `paatosperainen-todistelu`,
`lapi-hinnalla-milla-hyvansa`) ja 60 vanhaa sivua numeroitiin uudelleen
(pienin muuttunut 58). Kategoria 8 → 12 ilmiötä.

**Erä 2 — Media ja julkisuus (117 → 127), uusi kategoria 13.**
`lisaa_ilmiot.py` **ei osaa rakentaa uutta `hub-kategoria`-lohkoa**, vain
pujottaa kortin olemassa olevan perään. Siksi skriptiin lisättiin lippu
`--kortit-valmiina`: lohko kortteineen (10 kpl, numerot 118–127) ja
`hub-katnav`-linkki kirjoitettiin `index.html`:ään käsin, ja skripti teki
loput — luonnokset juureen, `const IDS`, PREV/NEXT, selausnapit ja
`N / 127`-laskurit kaikille 127 sivulle. `index.html`:ään se ei koske
lainkaan, ja tarkistaa vain että numerointi on 1..N. Kategoria sijoitettiin
**viimeiseksi**, jolloin yksikään vanha sivu ei numeroitunut uudelleen.

**Luonnoksista periytyneet virheet (korjattu julkaisun yhteydessä).**

- Media-erän 10 sivun murupolku osoitti `kategoria-alustatalous-ja-algoritmit.html`:ään
  sekä näkyvässä murupolussa että JSON-LD:n `BreadcrumbList`issa — luonnospohjan
  jäänne ajalta, jolloin kategoriaa 13 ei ollut. Korvattu sedillä.
  Suurhanke-erän 4 sivua olivat oikein.
- Kaikki 14 sivua linkittivät `style.css?v=20260727`, muut 113 sivua
  `?v=20260725`. Yhtenäistetty jälkimmäiseen (`style.css` ei ole muuttunut).
  Kategoriasivut jäävät 20260727:ään — versio on kovakoodattu
  `build_kategoriat.py`:hyn (`CSS_VERSIO`), ja se on vanha ero.
- `datePublished`/`dateModified` ja näkyvä "Päivitetty" olivat luonnoksen
  kirjoituspäivä (27.–28.7.). Asetettu julkaisupäiväksi 2026-08-05, jotta
  sitemapin `lastmod` on totta.

**Kategoriasisältö.** `kategoriat/projekti-ja-ohjelmistokehitys.md`: "Kolme
mekanismia" → "Neljä mekanismia" (uusi lohko *Arvio on hakemus*), otsikko ja
kuvaus 8 → 12, kaksi uutta kytkentäbullettia ja viides lukijaohje
(vertailuluokka). `kategoriat/media-ja-julkisuus.md` oli valmiina;
vain `paivitetty` 2026-07-28 → 2026-08-05.

**Regeneroinnit.** `paivita_maarat.py` (127 ilmiötä / 13 kategoriaa; llms.txt
+14 entryä), `build_kategoriat.py` (13 sivua, laskurit `x / 13` automaattisesti),
`murupolku_kategoriaan.py`, `build_liittyvat.py`, `build_sitemap.py`,
`build_search_index.py`. Etusivun `paivitetty-btn` ja `CollectionPage`in
`dateModified` 5.8.2026; `muutokset.html` sai kaksi `article.muutos`-merkintää.

**Huom seuraavalle sessiolle:** `lisaa_ilmiot.py`:n `UUDET`-taulukko on nyt
media-erän sisältö. Se on ajettu loppuun — seuraavalla kerralla taulukko
korvataan, ei täydennetä.

## 4.8.2026 — Toimenpidesuunnitelman loput (H2, H3, M1, M2, M4, M5, M6)

Samana päivänä viikko 1:n jälkeen. **H1 (kategoriasivudiagnoosi) jäi tekemättä:**
se vaatii GSC-service accountin URL Inspectionia varten, eikä sitä ole. Kaikki
muu suunnitelmasta on tehty.

**H2 + H3 — sisääntulevat sisäiset linkit.** Kolmas aalto `lisaa_sisalinkit.py`:n
`GSC_ELOKUU`-taulukkoon, sen jälkeen `build_liittyvat.py`. Suunnitelman premissi
H2:sta oli **vanhentunut**: `hyvesignalointi.html` oli jo 12 sisääntulevalla
linkillä (darvo 11), eli toisen aallon jäljiltä tavoite oli jo täyttynyt. Vaje
oli muualla. Tulos: hyvesignalointi 12→14, doomscrolling 8→10, peterin-periaate
8→10, hanlonin-partaveitsi 8→9. Kahdeksan linkkiä oli jo olemassa (skripti on
idempotentti), eikä yhdenkään lähdesivun korttimäärä ylittänyt 7:ää.

**M4 — murupolun CSS-selektori (113 sivua).** Vika ei ollut selektorissa vaan
`murupolku_kategoriaan.py`:n **idempotenssissa**: se teki
`.replace(".kortti-breadcrumb-kat {…}", ".kortti-breadcrumb .kortti-breadcrumb-kat {…}")`,
ja koska tulos sisältää lähtökuvion osajonona, jokainen ajo kasvatti
jälkeläisketjua yhdellä tasolla. Kolmen ajon jälkeen selektori oli
nelinkertainen eikä täsmännyt mihinkään. Korvattu regexillä, joka normalisoi
ketjun aina yhteen tasoon. 113/113 oikein, ajo toistettavissa.

**M5 — 7 liian pitkää meta-kuvausta.** Kuusi kategoriakuvausta lyhennettiin
lähteessä `kategoriat/*.md` (184→134 … 166→157) ja sivut regeneroitiin;
`index.html` 172→140. Koko sivustolla 0 kuvausta yli 160 merkin.

**M1 — vastakeino-osion nimi.** Kaksi vaihetta.

*Mekaaninen osa.* `laatikko_otsikot.py` kattoi vain `.infolaatikko` ja
`.huomiolaatikko`, joten koko `.vaaralatikko`-perhe (~70 laatikkoa) oli jäänyt
`<strong>`-muotoon — ja **31 niistä oli jo nimeltään "Tunnistaminen ja
vastakeinot:"**. Lupaus siis piti, mutta merkkaus ei kertonut sitä.
Laajennuksessa kaksi ansaa, molemmat samasta syystä:

- Luokka on `vaaralatikko` **yhdellä a:lla** (vaara+latikko). Alternaatio
  `(?:info|huomio|vaara)laatikko` tuottaa `vaaralaatikko` eikä osu koskaan.
  Nyt vaihtoehdot luetellaan kokonaisina niminä.
- Samasta syystä silmukan esikarsinta `if 'laatikko">' not in html: continue`
  ohitti sivut, joilla oli vain vaaralaatikko — `vaaralatikko">` ei sisällä
  osajonoa `laatikko">`. Kolme sivua jäi ensimmäisellä korjatulla ajolla.

Tulos: 70 + 3 laatikkoa `<strong>` → `<h2 class="laatikko-otsikko">`. CSS-sääntö
päivitettiin paikalleen (`VANHA_CSS`-regex) eikä lisätty toisena kopiona.

*Käsityöosa.* Yhtenäistämislinja **kysyttiin käyttäjältä**, koska vaihtoehdot
tuottavat eri lopputuloksen. Valinta: nimetään uudelleen vain geneeriset,
säilytetään ne joissa nimi kertoo kenelle tai miten. 26 otsikkoa uudelleen
(`Suojaudu:`, `Mitä tehdä:`, `Ulospääsy:`, `Korjauskeino:`, `Käytännön testi:`,
`Vastakysymys:` …), 22 säilytettiin (`Vastakeinot projektijohdolle:`,
`Hakijalle:`, `Kuluttajalle:`, `Vastakeino — käänteinen Conwayn manööveri:` …).

**91/113 sivua kantaa nyt otsikkoa "Tunnistaminen ja vastakeinot:" h2-tasolla**
(ennen 34), ja kaikilla 113:lla vastakeino-osio on h2-ankkuri.

**M2 — vastauslohko + FAQPage 10 sivulle.** Toinen erä `seo_vastauslohko.py`:n
`SIVUT`-taulukkoon. Rajattu suunnitelman mukaan 10 sivuun, ei 98:aan: ensimmäisen
erän 15 sivun kohortti ei ole tuottanut klikkejä (CTR 1,19 % vs. 1,56 %).
Perustelu on AI-sitaatti ja featured snippet, ei CTR.

Kulma on eri kuin ensimmäisessä erässä. Ensimmäinen erä vastasi
käännöskysymykseen, koska sivut avautuivat jo määritelmällä. Näillä kymmenellä
**ensimmäinen kappale kertoo jo englanninkielisen termin**, joten käännöslohko
toistaisi sen. Lohko vastaa siksi määritelmäkysymykseen.

Ensimmäinen veto toisti silti liikaa: sanatason päällekkäisyys ensimmäisen
kappaleen kanssa oli `kaikukammio` 87 %, `maalitolppien-siirtaminen` 74 %,
`occamin-partaveitsi` 67 %, `pump-and-dump` 62 %, `overton-ikkuna` 59 %. Ne
viisi kirjoitettiin uusiksi eri kulmasta (kaikukammio: kyse ei ole vastapuolen
puuttumisesta vaan sen ennakkomitätöinnistä; Overton: kyse on siitä mitä
poliitikko *voi sanoa*, ei siitä mikä on oikein). Päällekkäisyys nyt 5–50 %,
kaikki vastaukset skriptin 240–300 merkin ikkunassa.

FAQPage 15 → 26 sivulla (25 ilmiösivua + etusivu). 128 JSON-LD-lohkoa, 0 virhettä.

**M6 — `hofstadterin-laki.html`.** Sivuston ainoa sivu ilman sisältö-`h2`:ta.
Kaksi orpoa kappaletta laatikoihin sivuston omalla kaavalla: `Miksi puskuri ei
riitä:` (huomiolaatikko) ja `Ilmiö arjessa:` (infolaatikko); `Korjauskeino:` →
`Tunnistaminen ja vastakeinot:` M1:n mukana. Nyt 3 sisältö-h2:ta. Todennettu
kuvakaappauksella.

**Lukijalle näkyvät muutokset → `muutokset.html`.** Toisin kuin viikko 1, M1 ja
M2 muuttavat sitä mitä sivulla lukee, joten uusi `<article class="muutos">`,
`dateModified` 2026-08-04 sekä `index.html`:n nappi ja JSON-LD samalle päivälle,
minkä jälkeen `build_sitemap.py`. `dateModified` nostettiin **vain niille 10
sivulle, joille tuli uutta tekstiä** — otsikoiden uudelleennimeäminen on
merkintää, ei sisältöä, joten M1:n 26 sivua eivät saaneet uutta päiväystä
(sama linja kuin 28.7. murupolkukorjauksessa, audit §6 C4). Lopuksi
`build_search_index.py` (125 sivua, 358 kt).

## 4.8.2026 — Toimenpidesuunnitelman viikko 1 (K1, K2, H4, H5, M3)

Lähde: `gsc/TOIMENPIDESUUNNITELMA-2026-08-04.md`, joka perustuu samana päivänä
tehtyyn auditointiin `gsc/SEO-AUDIT-2026-08-04.md`. Kaikki viisi kohtaa ovat
teknisiä, joten **ei merkintää `muutokset.html`:ään** eikä etusivun
`Päivitetty`-päiväyksen nostoa: lukijalle ei tullut uutta luettavaa.
Sisältö ei muuttunut millään sivulla, joten `dateModified` pysyy ennallaan
eikä `build_sitemap.py`:tä tarvinnut ajaa.

**K1 — CDN pois, paikalliset kopiot käyttöön (97 sivua).** `js/mermaid.min.js`
(3,5 Mt) ja `js/chart.umd.min.js` (208 kt) ladattiin levylle jo 28.7., mutta
HTML jäi osoittamaan `cdn.jsdelivr.net`iin — itsehostaminen oli puolivalmis
`CLAUDE.md`:n oman säännön vastaisesti. Uusi `scripts/korjaa_cdn_viittaukset.py`
(kuivaharjoitus oletuksena, `--kirjoita`) käänsi mermaidin 94 sivulla ja
chart.js:n 3 sivulla. Mermaid tulee inline-skriptin `s.src`-sijoituksesta,
chart.js `<script src>`-tagista — skripti hoitaa molemmat.

Järjestys oli tärkeä: renderöinti todennettiin **ennen** CSP:n kiristystä.
Playwright-testi `darvo`, `bikeshedding` (mermaid) ja `korkokierre` (chart.js)
→ SVG/canvas syntyy, nolla ulkoista pyyntöä. Paikallinen mermaid-nide on
esbuild-ESM, joka päättyy `globalThis["mermaid"] = …` — sama globaali API kuin
CDN-niteessä, joten sivujen `mermaid.initialize()` toimii muuttumattomana.
Vasta sitten `.htaccess`: `script-src 'self' 'unsafe-inline' cdn.jsdelivr.net`
→ `script-src 'self' 'unsafe-inline'`.

Testiä kirjoittaessa paljastui sivuston oma ansa: sivun pohjaan vierittäminen
laukaisee satunnaissiirtymän, joka navigoi toiselle ilmiösivulle — canvas katoaa
DOM:ista ja testi näyttää väärää epäonnistumista. Testi vierittää nyt
kaavioelementtiin, ei pohjaan.

Regressiosuoja: `scripts/seo_patch_v2.py` kirjoitti CDN-URLin uusiin sivuihin
(rivi 42) → osoittaa nyt `js/mermaid.min.js`. Sen `MERMAID_OLD`-vakio ja
`seo_patch.py`:n vastaava regex jätettiin ennalleen: ne ovat *hakukuvioita*
vanhalle merkkaukselle, eivät emittereitä.

**K2 — kategoriasivujen H1 (12 sivua).** `<h1 class="kat-nimi">Alustatalous ja
algoritmit<span class="kat-alaotsikko">miksi syöte…</span></h1>` luki tekstinä
`Alustatalous ja algoritmitmiksi syöte…` — `<span>` on inline-elementti ilman
välimerkkiä, joten hakukone, ruudunlukija ja LLM näkivät sanajonon, jota kukaan
ei hae. Korjaus `scripts/build_kategoriat.py`:hyn: alaotsikko on nyt oma `<p>`
`h1`:n **ulkopuolella**, ja 12 sivua regeneroitiin.

CSS-selektori `.kat-alaotsikko` → `p.kat-alaotsikko`; `display:block` poistui
(tarpeeton `<p>`:llä), tilalle `margin: 0.5rem 0 0` `<p>`:n oletusmarginaalien
kumoamiseksi. **`font-family` piti toistaa erikseen**: alaotsikko peri Spectralin
`h1`:ltä, eikä periytymisketju enää kulje sen kautta. Ulkoasu todennettiin
kuvakaappauksella ja `getComputedStyle`illa — identtinen.

**H4 — viisi titleä, jotka katkesivat kesken merkityksen.** Ei laajaa
title-remonttia: 56 titleä on yli 60 merkkiä, mutta useimmissa katkeaa vain
`— Ilmiöitä`, jonka Google usein pudottaa itsekin. Nämä viisi menettivät
sisältöä. Muutettiin `<title>`, `og:title` ja `twitter:title`; näkyvä `h1`
jätettiin ennalleen, koska kyse on SERP-näyttöongelmasta eikä sisältöongelmasta.

| Sivu | mrk | Uusi title | ydin |
|---|---|---|---|
| `brandolinin-laki` | 73→66 | Brandolinin laki — valhe on halpaa, kumoaminen kallista | 55 |
| `badger-game` | 85→68 | Badger game — lavastettu tilanne, kiristys vaikenemisesta | 57 |
| `rautainen-laki` | 81→64 | Rautainen laki oligarkiasta — väistämätön mätäneminen | 53 |
| `jarjestelman-puolustelu` | 76→65 | Järjestelmän puolustelu — miksi häviäjä puolustaa sitä | 54 |
| `lowball-hinnoittelu` | 74→68 | Lowball — matala aloitushinta nousee sitoutumisen jälkeen | 57 |

*ydin* = merkitysosa ilman `— Ilmiöitä`-loppuliitettä; kaikki alle 60, joten
katkaisu osuu enää loppuliitteeseen.

**H5 — `defer` etusivun hakuindeksiin.** `index.html`:
`<script src="search-index.js">` (363 kt, 3,4× sivun oma koko) esti
renderöinnin. Pelkkä `defer` olisi kuitenkin **rikkonut haun**: sitä seuraava
inline-IIFE luki `window.ILMIO_HAKU`:n heti, ja deferoitu skripti ajetaan vasta
myöhemmin — kokotekstihaku olisi pudonnut hiljaa pelkkään otsikko-osumaan.
Siksi IIFE `(function () {…})()` → `document.addEventListener('DOMContentLoaded',
function () {…})`; deferoitu skripti ajetaan ennen DOMContentLoadedia, joten
indeksi on valmis. Todennettu selaimessa: `ILMIO_HAKU` 125 entryä,
kokotekstiosumat (`budjettileikkauksilla`, `yksityistämistä`) löytyvät,
`window.randomIlmio` on yhä globaali, nolla sivuvirhettä.

**M3 — stray-tiedosto pois webbijuuresta.** `artikkelein_sisaltolustaus_not_article.html`
(74 kt, 28.7. vastakeino-auditoinnin työkalu) oli julkisesti haettavissa ilman
canonicalia ja schemaa; `noindex,nofollow` esti indeksoinnin muttei pääsyä.
`git mv` → `luonnokset/`. Ei `sitemap.xml`-muutosta — ei ollut siellä.

**Huom deployssa:** `.htaccess` on `.gitignore`ssa, joten CSP-muutos **ei tule
gitin mukana** vaan on vietävä palvelimelle käsin. Jos CSP menee livenä ennen
HTML:ää, 94 sivun kaaviot hajoavat — vie HTML ensin.

## 28.7.2026 — `honeypot-huijaus.html`: hullu hunaja ja kaksi lähdettä

- Uusi kappale tietoturva-kappaleen jälkeen: Mithridates VI:n joukot jättivät
  65 eaa. Pompeiuksen sotilaiden reitin varrelle *hullua hunajaa* (alppiruusun
  medestä, grayanotoksiini), ja huumaantuneet miehet surmattiin — Strabonin
  mukaan kolme manipulia. Kirjaimellinen hunajapurkkiansa, joka näyttää saman
  epäsymmetrian kuin sivun muut esimerkit.
- `Lue lisää` → Verkossa: Wikipedian *Honey trapping* (romanssiansa, kaava
  pätee sen ulkopuolellakin) ja *Mad honey* (65 eaa. tapaus).
- `dateModified` ja byline 19.6. → 28.7.2026, minkä jälkeen
  `build_sitemap.py` ja `build_search_index.py`.

Ei merkintää `muutokset.html`:ään: yhden kappaleen historiallinen esimerkki
yhdellä sivulla ei ole lukijalle uutta luettavaa sivustotasolla.

## 28.7.2026 — Muutosloki lukijalle: `muutokset.html`

Etusivun header näytti "Päivitetty 12.7.2026", vaikka sisältöä oli sen jälkeen
muutettu kuudesti — päiväys oli käsin ylläpidetty merkkijono ilman mitään, mikä
olisi pakottanut sen pysymään ajan tasalla. Nyt päiväys on nappi, joka vie
uudelle sivulle, ja sillä on kohde, jonka unohtaminen näkyy.

- **`muutokset.html`** (uusi) — lukijalle kirjoitettu aikajana seitsemästä
  päivityksestä 19.6.–28.7.2026. Käsin kirjoitettu, **ei generoitu tästä
  tiedostosta**: yleisö on eri. Sivulla kerrotaan uusista ilmiöistä ja
  sisällön parannuksista; skriptinimet, punycode-korjaukset ja infrastruktuuri
  jäävät tänne. CSS inlinenä.

  **Yläpalkki on etusivun, ei `tietoa.html`:n.** Ensimmäinen versio peri
  `tietoa.html`:n riisutun headerin (pelkkä otsikkorivi + tekstilinkki), mikä
  näytti eri sivustolta kuin se, jolta napin kautta juuri tultiin. Nyt sama
  rakenne kuin `index.html`:ssä: `favicon.svg` 36 px, `.hub-header-left`
  kaksirivisenä (`Ilmiöitä` + alaotsikko) ja `.random-btn`in tyylinen
  `.takaisin-btn` oikeassa reunassa nuoli-ikonilla. Alle 380 px:ssä nappi
  kutistuu pelkäksi ikoniksi kuten *Satunnainen* — siksi `aria-label`.

- **`tietoa.html`** — sama header, sama `.takaisin-btn`. Sivulla ei ollut
  lainkaan media queryjä, joten se sai samat kolme (`640px`, `380px`,
  `prefers-reduced-motion`). Alaotsikoksi molemmille alasivuille sivuston
  tunnuslause **"Miten valta toimii"** eikä sivun nimi: sivun nimi toistuisi
  sanasta sanaan heti alla olevassa `h2`:ssa. Etusivun vastaava rivi alkaa
  ilmiömäärällä, mutta sitä ei kopioitu alasivuille — käsin ylläpidetty luku,
  jota `paivita_maarat.py` ei näistä tiedostoista etsi, ajautuisi pian väärään
  arvoon.

  Rajaus tarkentui kirjoittaessa: 27.7. itsehostatut fontit ja JS-kirjastot
  olivat sivulla omana merkintänään, mutta ne poistettiin. Muutos on lukijalle
  merkittävä yksityisyyden kannalta, mutta sivulla se luki kuin tekninen
  selittely — muutosloki kertoo mitä lukija *saa*, ei mitä palvelimella
  tapahtuu.
- **`index.html`** — headerin `Päivitetty 12.7.2026` → `.paivitetty-btn`-nappi
  `Päivitetty 28.7.2026 ›`. Nappi on `.random-btn`in tyylinen (kulmikas,
  kullansävyinen reunus) mutta headerin alarivin kokoinen. JSON-LD
  `CollectionPage.dateModified` 2026-07-16 → 2026-07-28.
- **Footer-linkit** `index.html`:ään ja `tietoa.html`:ään, jottei sivu ole
  yhden napin varassa.
- **`scripts/build_sitemap.py`** — uusi `MUUTOKSET`-rivi (prio 0.4, monthly)
  `TIETOA`:n perään. Sitemap 127 → 128 URLia; etusivun `lastmod` päivittyi
  samalla 2026-07-16 → 2026-07-28.
- **`llms.txt`** — otsikkolohkoon rivi muutoslokin osoitteesta.
- **`CLAUDE.md`** (uusi) — repossa ei ollut lainkaan ohjetiedostoa. Sisältää
  muutoslokin ylläpito-ohjeen (viisi kohtaa: MUUTOSLOKI.md → muutokset.html →
  sen JSON-LD → index.html:n kaksi päiväystä → build_sitemap.py), listan
  generoiduista tiedostoista ja sisältönormit (~260 sanaa, vastakeino-osio,
  nimeäminen).

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
