# Suosiodata ja etusivun nostot

Miten järjestelmä toimii, mikä kone tekee mitä ja missä mikäkin tiedosto on.
Kuvaa nykytilan 15.8.2026. Muutoshistoria ja hylätyt ratkaisut ovat
`MUUTOSLOKI.md`:ssä, lukijalle näkyvä versio `muutokset.html`:ssä.

## Lopputulos

Etusivulla on viisi nostolohkoa, jotka päivittyvät liikennedatasta:

| Lohko | Mitä mittaa | Ikkunat |
|---|---|---|
| Viikon ilmiö | suhteellisesti eniten noussut sivu, valinta maanantaisin | 7 pv |
| Satunnainen ilmiö | ei mitään — arpoo sivun omasta korttilistasta | — |
| Luetuimmat | sivunäytöt (joku avasi sivun) | 7 / 30 pv |
| Googlatuimmat | Google-näytöt (sivu näkyi hakutuloksissa) | 7 / 30 pv |
| Eniten kasvua | kasvu edelliseen jaksoon verrattuna | 7 / 30 pv |

Lukumääriä ei näytetä lukijalle, vain järjestys ja kasvuprosentti
(`NAYTA_LUVUT=false`). Luonnoskopiossa luvut ovat näkyvissä.

## Koneet ja roolit

```
   NAS 192.168.32.100 (Asustor)      webhotelli cpanel06.webhotellit.com
   dataneuvos                        inflaati
   ┌────────────────────────┐        ┌──────────────────────────────────┐
   │ Postgres (Docker)      │        │ /home/inflaati/public_html/      │
   │   liikenne + GSC-data  │        │   kendom/ilmiöt/      ← docroot  │
   │                        │        │     index.html                   │
   │ ~/ilmiot   (repo)      │ SFTP   │     data/suosio.js    ← yöllä    │
   │ ~/ilmiot-venv          │───────►│                                  │
   │ yöajo cronista         │  vain  │                                  │
   └────────────────────────┘ tämä 1 └──────────────────────────────────┘
              ▲                         ▲
              │ tarball main-haarasta   │ index.html käsin, harvoin
         GitHub (julkinen)         työasema WSL 192.168.83.33
```

**NAS on ainoa kone joka lähettää.** Ilman `--laheta`-lippua ajavia koneita saa
olla monta — ne kirjoittavat vain omia paikallisia tiedostojaan — mutta kaksi
lähettäjää tarkoittaisi kahta eri viikon ilmiötä samalla sivustolla. Työaseman
cron on siksi kytketty pois.

**Yöajo ei koske `index.html`:ään.** Suosiodata elää erillisessä
`data/suosio.js`:ssä, jonka etusivu lataa `defer`-skriptinä. Jos data
kirjoitettaisiin HTML:ään, joka yö työnnettäisiin 145 kt etusivu, joka voi
ylikirjoittaa käsin tehtyjä muutoksia — repon dokumentoitu pahin vikatila.

**`data/suosio.js` sisältää vain slugit ja luvut.** Otsikot, kuvaukset ja värit
haetaan selaimessa sivun omista `.hub-kortti`-elementeistä. Siksi ilmiön
uudelleennimeäminen ei voi rikkoa nostolohkoa eikä poistettu ilmiö jää haamuksi.

## Mitä on missäkin

### Webhotelli — `cpanel06.webhotellit.com`, käyttäjä `inflaati`

| Tiedosto | Polku | Miten | Milloin |
|---|---|---|---|
| `index.html` | `~/public_html/kendom/ilmiöt/index.html` | käsin | kun etusivu muuttuu |
| `data/suosio.js` | `~/public_html/kendom/ilmiöt/data/suosio.js` | SFTP, `--laheta` | joka yö |
| julkinen avain | `~/.ssh/authorized_keys` | kerran | 15.8.2026 |

Dokumenttijuuri on **`ilmiöt` ö:llä**. Rinnalla on samannimistä muistuttava
`kendom/ilmiot/` ilman ö:tä, joka ei ole käytössä — ero on yhden kirjaimen
mittainen ja siksi vaarallinen. Oikean tunnistaa siitä, että sen `index.html`
on md5-identtinen livenä olevan kanssa.

cPanelin tiedostonhallinta näyttää polut muodossa `/public_html/…`, mutta
todellinen polku alkaa aina `/home/inflaati/`. Käytä SFTP-asetuksissa täyttä
polkua.

### NAS — `192.168.32.100`, käyttäjä `dataneuvos`, Asustor ADM

| Mitä | Polku | Alkuperä |
|---|---|---|
| repo | `~/ilmiot` | GitHub main, tarball |
| Python-ympäristö | `~/ilmiot-venv` | `nas_asennus.sh` |
| asetukset | `~/ilmiot/.suosio.env` | kopioitava käsin, **ei versionhallinnassa** |
| viikon ilmiön historia | `~/ilmiot/data/.viikko-historia.json` | kopioitava käsin, **ei versionhallinnassa** |
| SSH-avain | `~/.ssh/id_ed25519_ilmiot` | kopioitava käsin |
| dashboard | `~/ilmiot/luonnokset/suosio.html` | generoituu joka ajossa |
| loki | `~/.suosio.log` | jokainen ajo lisää aikaleimallisen lohkon |

`.suosio.env`:n neljä siirtoasetusta — kaikkien on oltava täytettyjä:

```
SFTP_HOST=cpanel06.webhotellit.com
SFTP_USER=inflaati
SFTP_KEY=/home/dataneuvos/.ssh/id_ed25519_ilmiot
SFTP_POLKU=/home/inflaati/public_html/kendom/ilmiöt/data
```

Kanta pyörii samassa koneessa Dockerissa, joten kantayhteys ei kulje verkon yli.

Jos NAS pystytetään uudelleen: `scripts/nas_asennus.sh` hoitaa kaiken muun paitsi
kolme käsin kopioitavaa tiedostoa yllä. Skriptissä on `--tarkista`-tila joka ei
muuta mitään.

### GitHub — `samulah/ilmiot-ja-virhepaatelmat`, haara `main`

Repo on julkinen, joten NAS hakee sen tarballina ilman avainta. Haara on
**`main`** — yöajo hakee sen ennen jokaista ajoa, koska skripti lukee
ilmiölistan `index.html`:stä ja julkaisupäivät sivujen JSON-LD:stä. Vanhentunut
kopio jättäisi uudet ilmiöt pois listoilta.

## Ajastus

Ajastus on `/var/spool/cron/crontabs/dataneuvos`:ssa, ei käyttöliittymässä.
Asustorin ADM on BusyBox-pohjainen: ei systemd:tä, ei `/etc/crontab`ia, ja
`/usr/bin/crontab` on symlinkki busyboxiin ilman suid-bittiä, joten käyttäjän
`crontab`-komento ei toimi lainkaan. Rivi lisätään suoraan spooliin rootina:

```sh
sudo sh -c "printf '\n%s\n' '<rivi>' >> /var/spool/cron/crontabs/dataneuvos"
```

Muoto on **viisi aikakenttää ja komento suoraan**, ei käyttäjäkenttää; tiedoston
nimi määrää käyttäjän. BusyBoxin `crond` havaitsee muuttuneen tiedoston minuutin
sisällä, joten palvelua ei tarvitse käynnistää uudelleen.

```
10 3 * * * PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin; cd /home/dataneuvos/ilmiot && curl -sfL https://codeload.github.com/samulah/ilmiot-ja-virhepaatelmat/tar.gz/refs/heads/main | tar xz --strip-components=1 && /home/dataneuvos/ilmiot-venv/bin/python scripts/paivita_suosio.py --laheta >> /home/dataneuvos/.suosio.log 2>&1
```

Kaksi yksityiskohtaa estävät hiljaisen yöllisen epäonnistumisen: **absoluuttiset
polut** (BusyBoxin cron ei välttämättä aseta `HOME`:a, ja tyhjä `$HOME` tekisi
polusta `/ilmiot`) ja **eksplisiittinen `PATH`** (cronin ympäristö on riisuttu,
eikä `curl` tai `tar` välttämättä löydy).

### Kellonaika on sidoksissa ETL:ään

Samassa crontabissa on `0 3 * * * run_all_etl.sh`, joka lataa liikennedatan
kantaan. Suosioajo **on ajettava vasta sen jälkeen**. Kesken olevaa kantaa
vasten ajo ei kaadu vaan tuottaa vaimeat luvut, jolloin lohkot näyttävät
oikeilta mutta kertovat väärää — vaikeampi huomata kuin virheilmoitus.
Kymmenen minuutin marginaali on ohut; 04:00 on turvallisempi, eikä
kellonajalla ole muuten väliä koska data on päivätasoista.

## Mittareiden säännöt

Nämä eivät ole tyylivalintoja vaan estävät listoja valehtelemasta.

**Lattia.** Viikon ilmiö vaatii 10 lukukertaa, 7 pv:n kasvulista 5, 30 pv:n 10.
Ilman lattiaa 1 → 4 näyttöä olisi +300 % ja kärki olisi pelkkää kohinaa.

**Tasoitus.** Kasvusuhde on `(nyt + 5) / (ennen + 5)`, ei raaka suhde. Siksi
0 → 19 on +380 %, ei ääretön. Sama kaava kaikissa lohkoissa — jos toinen
laskisi raa'an suhteen, sama sivu saisi kaksi eri lukua samalla sivulla.

**Julkaisupäivä.** Sivun on oltava julkaistu ennen vertailujakson alkua. Sivu
jota ei ollut olemassa on aina "kasvanut nollasta", vaikka se ei kasvanut vaan
ilmestyi. Koskee sekä kasvulistoja että viikon ilmiön valintaa.

**Karenssi.** Neljä edellistä viikon ilmiötä ovat poissa laskuista, ja valinta
tehdään vain maanantaisin — muuten "viikon ilmiö" vaihtuisi joka yö.

**Vertailujakson skaalaus.** Kanta alkaa 1.7.2026, joten 30 pv:n vertailujakso
on toistaiseksi katettu vain puoliksi (15/30 pv). Vertailuluku kerrotaan
2,00:lla ja saate lukee "(osin arvioitu)". Skaalaus **pienentää**
kasvuprosenttia, joten se ei voi keksiä kasvua jota ei ole. Kerroin menee
itsestään ykköseen 29.8.2026 eikä koodia tarvitse siivota.

**Tuoreus.** Yli 3 vrk vanhaa dataa ei näytetä. Jos yösiirto hajoaa, neljä
lohkoa katoaa itsestään ja satunnainen ilmiö jää — se toimii ilman dataa.

**Alle kolmen rivin kasvulista piiloutuu** — mutta välilehtikohtaisesti, ei
koko lohkona. Kynnys arvioidaan jokaiselle ikkunalle erikseen, oletukseksi
valitaan ensimmäinen joka yltää siihen, ja lohko näkyy jos yksikin yltää. Tyhjä
tai kahden rivin "30 pv" olisi lupaus jota klikkaus ei lunasta, mutta lyhyt
"7 pv" ei saa viedä kelvollista "30 pv":tä mukanaan.

## Kannan erityispiirteet

Nämä on hoidettu kyselyssä ja ne on syytä muistaa jos kyselyä muokataan:

- Ilmiöt.fi on kannassa **kahtena** `sivusto_avain`-arvona — rajaa
  `sivusto_ryhma`, ei avainta.
- `http_status` sisältää runsaasti 301-ohjauksia, jotka eivät ole sivunäyttöjä.
- Faktataulussa ei ole bottilippua. Ryömijät suodatetaan sillä, montako eri
  sivua sama kävijä avaa yhdessä päivässä.
- Google-data laahaa 2–3 vrk, joten tuoreimmat päivät ovat aina vajaita.

## Avoimet asiat

1. **Ensimmäinen yöajo nähty 16.8. klo 03:10 — cron toimii, siirto kaatui.**
   Data laskettiin oikein ja `data/suosio.js` kirjoittui NAS:ille, mutta `sftp`
   ei ollut cronin PATH:issa (Asustorilla `/usr/builtin/bin/sftp`). Skripti
   paikantaa binäärin nyt itse; ks. MUUTOSLOKI 16.8.2026. **Korjaus on
   todennettu vain NAS:ille käsin kopioidulla skriptillä — koko yöajo on vielä
   näkemättä korjatulla koodilla.** Tarkista aamulla `tail -25 ~/.suosio.log`
   ja että live-tiedoston `paivitetty`-aikaleima on saman yön.
2. **Ei ilmoitusta epäonnistumisesta.** Kohta 1 on tästä ensimmäinen todellinen
   esiintymä: ajo epäonnistui hiljaa ja vika löytyi vain lokia lukemalla.
   Cronin `MAILTO` ei tässä laitteessa
   toimi ilman postinvälitystä. Rikkoutunut yöajo näkyy siis vasta siinä, että
   etusivun lohkot katoavat kolmen vuorokauden päästä. Tämä on putken heikoin
   kohta ja korjattavissa esimerkiksi niin, että onnistuminen kirjoittaa
   aikaleiman tiedostoon ja erillinen tarkistus huomauttaa jos se vanhenee.
3. **Kaksi committia on pushaamatta.** NAS hakee mainista ennen jokaista ajoa,
   joten se ei saa niitä ennen pushia.
4. **30 pv:n kasvu on osin arvioitu** 29.8.2026 asti.
5. **Dashboard elää vain NAS:illa.** Työaseman kopio vanhenee nyt kun ajo on
   siirtynyt pois.

## Komennot

```sh
# NAS: käsiajo ilman siirtoa
cd ~/ilmiot && ~/ilmiot-venv/bin/python scripts/paivita_suosio.py --ei-kirjoita

# NAS: ajo siirtoineen
cd ~/ilmiot && ~/ilmiot-venv/bin/python scripts/paivita_suosio.py --laheta

# NAS: asennuksen tarkistus, ei muuta mitään
sh ~/ilmiot/scripts/nas_asennus.sh --tarkista

# NAS: mikä ajastus on voimassa
sudo grep paivita_suosio /var/spool/cron/crontabs/dataneuvos

# Työasema: nostot luonnossivulle lukuineen
python3 scripts/paivita_suosio.py

# Työasema: nostot index.html:ään ilman lukuja (kertaluontoinen)
python3 scripts/paivita_suosio.py --tuotanto

# Varmistukset
curl -sI https://www.xn--ilmit-mua.fi/data/suosio.js | head -1
curl -s https://www.xn--ilmit-mua.fi/ | grep -c NOSTOT-ALKU   # 3
```
