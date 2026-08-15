# Suosiodata ja etusivun nostot — kooste

Tila 15.8.2026. Kuvaa mitä rakennettiin, missä järjestyksessä, mikä kone tekee
mitä ja mitä on viety millekin palvelimelle. Tekninen muutoshistoria on
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

## Kolme konetta ja niiden roolit

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

**NAS on ainoa kone joka lähettää.** Työaseman cron on kommentoitu pois
15.8.2026. Ilman lippua `--laheta` ajavia koneita saa olla monta — ne
kirjoittavat vain omia paikallisia tiedostojaan — mutta kaksi lähettäjää
tarkoittaisi kahta eri viikon ilmiötä samalla sivustolla.

Yöajo ei koske `index.html`:ään. Suosiodata elää erillisessä `data/suosio.js`
:ssä, jonka etusivu lataa `defer`-skriptinä. Jos data kirjoitettaisiin HTML:ään,
joka yö työnnettäisiin 145 kt etusivu, joka voi ylikirjoittaa käsin tehtyjä
muutoksia — repon dokumentoitu pahin vikatila.

## Mitä on viety millekin palvelimelle

### Webhotelli — `cpanel06.webhotellit.com`, käyttäjä `inflaati`

| Tiedosto | Polku | Miten | Milloin |
|---|---|---|---|
| `index.html` | `~/public_html/kendom/ilmiöt/index.html` | käsin | kun etusivu muuttuu |
| `data/suosio.js` | `~/public_html/kendom/ilmiöt/data/suosio.js` | SFTP, `--laheta` | joka yö |
| julkinen avain | `~/.ssh/authorized_keys` | kerran | 15.8.2026 |

Dokumenttijuuri on **`ilmiöt` ö:llä**, ei `ilmiot`. Rinnalla on tyhjä
`kendom/ilmiot/`-kansio joka ei ole käytössä; ero on yhden kirjaimen mittainen
ja siksi vaarallinen. Todiste oikeasta: `~/public_html/kendom/ilmiöt/index.html`
on md5-identtinen livenä olevan kanssa (182 tiedostoa kansiossa, toisessa 1).

Turhia jäänteitä joita voi poistaa: `~/public_html/data`,
`~/public_html/kendom/data`, `~/.ssh/ilmiot-suosio-yoajo*` (webhotellille
vahingossa luotu avainpari — asiakasavain kuuluu NAS:ille).

### NAS — `192.168.32.100`, käyttäjä `dataneuvos`

| Mitä | Polku | Alkuperä |
|---|---|---|
| repo | `~/ilmiot` | GitHub main, tarball |
| Python-ympäristö | `~/ilmiot-venv` | `nas_asennus.sh` |
| asetukset | `~/ilmiot/.suosio.env` | kopioitu työasemalta, **ei versionhallinnassa** |
| viikon ilmiön historia | `~/ilmiot/data/.viikko-historia.json` | kopioitu, **ei versionhallinnassa** |
| SSH-avain | `~/.ssh/id_ed25519_ilmiot` | kopioitu työasemalta |
| loki | `~/.suosio.log` | jokainen ajo lisää aikaleimallisen lohkon |

`.suosio.env`:n neljä siirtoasetusta:

```
SFTP_HOST=cpanel06.webhotellit.com
SFTP_USER=inflaati
SFTP_KEY=/home/dataneuvos/.ssh/id_ed25519_ilmiot
SFTP_POLKU=/home/inflaati/public_html/kendom/ilmiöt/data
```

Kanta on samassa koneessa Dockerissa, joten kantayhteys ei kulje verkon yli.

### GitHub — `samulah/ilmiot-ja-virhepaatelmat`, haara `main`

Repo on julkinen, joten NAS hakee sen tarballina ilman avainta. **Haara on
`main`.** `suosio-ja-nostot` jäi jälkeen kun työ siirtyi mainiin, ja NAS haki
pitkään vanhentunutta versiota juuri siksi.

## Rakennusjärjestys

1. **Luonnos** — luetuimmat, viikon ilmiö, satunnainen ilmiö demodatalla.
2. **Kantayhteys** — oikea kysely, bottisuodatus, lattioiden kalibrointi.
3. **Googlatuimmat** — `fact_gsc_haku`-taulusta, oma valinnainen kysely.
4. **Eniten kasvua 7 pv** — 15.8.
5. **Eniten kasvua 30 pv** — 15.8., vertailujakson skaalaus.
6. **Julkaisupäiväsuodatin** — 15.8., korjasi kasvulistojen valheen.
7. **Tuotantoinjektio** — `--tuotanto` kirjoitti `index.html`:ään.
8. **Julkaisurutiini** — `muutokset.html`, `dateModified`, sitemap.
9. **index.html palvelimelle** — käsin.
10. **Yöajo NAS:ille** — `nas_asennus.sh`, työaseman cron pois.
11. **Ensimmäinen SFTP-siirto** — `data/suosio.js` livenä 15.8. klo 11:20.
12. **Ajastus NAS:in croniin** — rivi `/var/spool/cron/crontabs/dataneuvos`:iin.

## Ajastus

NAS on Asustor (ADM): BusyBox, ei systemd:tä, ei `/etc/crontab`ia, ja
`/usr/bin/crontab` on symlinkki busyboxiin **ilman suid-bittiä** — käyttäjän
`crontab`-komento ei siis toimi lainkaan (`must be suid to work properly`).
Rivi kirjoitetaan siksi suoraan spooliin rootina:

```sh
sudo sh -c "printf '\n%s\n' '<rivi>' >> /var/spool/cron/crontabs/dataneuvos"
```

Muoto on **viisi aikakenttää ja komento suoraan**, ei käyttäjäkenttää — sama
kuin laitteen omilla riveillä. Tiedoston nimi määrää käyttäjän. BusyBoxin
`crond` havaitsee muuttuneen tiedoston minuutin sisällä, joten palvelua ei
tarvitse käynnistää uudelleen; se on hyvä, koska `crontab_check` valvoo niitä.

Ajettava rivi (tarkista voimassa oleva kellonaika spoolitiedostosta):

```
10 3 * * * PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin; cd /home/dataneuvos/ilmiot && curl -sfL https://codeload.github.com/samulah/ilmiot-ja-virhepaatelmat/tar.gz/refs/heads/main | tar xz --strip-components=1 && /home/dataneuvos/ilmiot-venv/bin/python scripts/paivita_suosio.py --laheta >> /home/dataneuvos/.suosio.log 2>&1
```

Kaksi yksityiskohtaa jotka estävät hiljaisen yöllisen epäonnistumisen:
**absoluuttiset polut** (BusyBoxin cron ei välttämättä aseta `HOME`:a, ja tyhjä
`$HOME` tekisi polusta `/ilmiot`) ja **eksplisiittinen `PATH`** (cronin ympäristö
on riisuttu, eikä `curl` tai `tar` välttämättä löydy).

### Kellonaika ja ETL

Samassa crontabissa on rivi `0 3 * * * run_all_etl.sh` — se lataa liikennedatan
kantaan. Suosioajo **on ajettava vasta ETL:n jälkeen**. Jos ETL on kesken, ajo
ei kaadu vaan tuottaa vaimeat luvut, ja lohkot näyttävät oikeilta mutta kertovat
väärää — pahempi vika kuin virheilmoitus. Kymmenen minuutin marginaali on ohut;
04:00 on turvallisempi, eikä kellonajalla ole muuten mitään väliä koska data on
päivätasoista.

## Mittareiden säännöt

Nämä eivät ole tyylivalintoja vaan estävät listoja valehtelemasta.

**Lattia.** Viikon ilmiö vaatii 10 lukukertaa, 7 pv:n kasvulista 5, 30 pv:n 10.
Ilman lattiaa 1 → 4 näyttöä olisi +300 % ja kärki olisi pelkkää kohinaa.

**Tasoitus.** Kasvusuhde on `(nyt + 5) / (ennen + 5)`, ei raaka suhde. Siksi
0 → 19 on +380 %, ei ääretön. Sama kaava kaikissa lohkoissa — jos toinen
laskisi raa'an suhteen, sama sivu saisi kaksi eri lukua samalla sivulla.

**Julkaisupäivä.** Sivun on oltava julkaistu ennen vertailujakson alkua.
Ilman tätä kasvulistan kärki oli `0 → 12`: sivuja jotka eivät kasvaneet vaan
ilmestyivät. 26 sivua on julkaistu 5.8. tai sen jälkeen, joten vika olisi
levinnyt myös viikon ilmiön valintaan.

**Karenssi.** Neljä edellistä viikon ilmiötä ovat poissa laskuista, ja valinta
tehdään vain maanantaisin — muuten "viikon ilmiö" vaihtuisi joka yö.

**Vertailujakson skaalaus.** Kanta alkaa 1.7.2026, joten 30 pv:n vertailujakso
on toistaiseksi katettu vain puoliksi (15/30 pv). Vertailuluku kerrotaan
2,00:lla ja saate lukee "(osin arvioitu)". Skaalaus **pienentää**
kasvuprosenttia, joten se ei voi keksiä kasvua jota ei ole. Kerroin menee
itsestään ykköseen 29.8.2026 eikä koodia tarvitse siivota.

**Tuoreus.** Yli 3 vrk vanhaa dataa ei näytetä. Jos yösiirto hajoaa, neljä
lohkoa katoaa itsestään ja satunnainen ilmiö jää — se toimii ilman dataa.

## Sudenkuopat jotka ratkaistiin

Nämä maksoivat eniten aikaa. Kirjattu, jottei niitä tarvitse löytää uudelleen.

**Kanta ei tunne yhtä sivustoa.** Ilmiöt.fi on kannassa kahtena
`sivusto_avain`-arvona (rajaa `sivusto_ryhma`), `http_status` sisältää runsaasti
301-ohjauksia jotka eivät ole sivunäyttöjä, eikä faktataulussa ole bottilippua —
ryömijät suodatetaan sillä, montako eri sivua sama kävijä avaa päivässä.

**`/dev/tcp` on bashismi.** Asennusskriptin kantayhteystesti antoi NAS:illa
väärän hälytyksen "ei saada yhteyttä" täysin toimivasta kannasta. `/dev/tcp` ei
ole tiedosto vaan bashin keksintö, eikä POSIX sh:ssa ole sitä lainkaan.
`dash -n` hyväksyy syntaksin — vika näkyy vasta ajossa. Testi tehdään nyt
python3:lla.

**NAS:illa ei ole bashia.** Eikä apt:ia. Skripti on siksi POSIX sh:lla.

**NAS on Asustor, ei Synology.** Tämä maksoi useita kierroksia: `/volume1`-polku
näytti Synologylta, mutta `/etc/VERSION` oli tyhjä eikä `/usr/syno`-hakemistoa
ollut. Kaikki DSM:ää koskevat ohjeet olivat siksi pielessä. Tunnusmerkit joista
Asustorin tunnistaa: `/usr/builtin`-symlinkki, `crond` s6:n valvomana
(`s6-supervise svc-cron`) ja `/usr/bin/crontab -> /bin/busybox`.

**`crontab: must be suid to work properly`.** Käyttäjän `crontab`-komento ei
toimi tässä laitteessa lainkaan, koska busybox-symlinkiltä puuttuu suid-bitti.
Rivi kirjoitetaan siksi suoraan spooliin rootina. `/etc/crontab`ia ei ole,
eikä systemd:tä — joten ei myöskään systemd-ajastimia.

**`display: flex` kumoaa `[hidden]`:in.** Välilehtipalkki jäi näkyviin vaikka
JS asetti attribuutin. Sama ansa kuin `.nostot[hidden]`:ssa, joka oli jo
suojattu — mutta uusi elementti ei perinyt suojaa.

**Tyhjä asetus ei ole puuttuva asetus.** `.suosio.env` sisälsi rivit
`SFTP_HOST=` ja `SFTP_USER=` ilman arvoa. Tarkistus katsoi vain onko avain
sanakirjassa, joten tyhjä meni läpi ja johti sftp-yritykseen tyhjällä
tunnuksella — siksi mitään ei siirtynyt.

**Väärä haara.** NAS haki `suosio-ja-nostot`-haaraa, joka jäi jälkeen kun työ
siirtyi mainiin. Diagnoosi näytti pushaamattomilta committeilta, vaikka työ oli
GitHubissa koko ajan — vain eri haarassa kuin mistä NAS luki.

**cPanelin polut näyttävät absoluuteilta.** Tiedostonhallinta näyttää
`/public_html/…`, mutta todellinen polku on `/home/inflaati/public_html/…`.
Ensimmäinen datakansio syntyi paikkaan jota ei ole verkossa olemassa.

## Avoimet asiat

1. **Ensimmäistä yöajoa ei ole vielä nähty.** Rivi on lisätty ja komento on
   todistettu käsin, mutta cronin poimintaa ei ole havaittu käytännössä.
   Tarkista aamulla: `tail -25 ~/.suosio.log` (uusi aikaleimallinen lohko ja
   `SFTP valmis`) ja `curl -sI https://www.xn--ilmit-mua.fi/data/suosio.js |
   grep -i last-modified`. Jos lokissa ei ole uutta lohkoa, cron ei poiminut
   riviä; jos lohko on mutta luvut ovat nollissa, ETL oli vielä kesken.
2. **Ei ilmoitusta epäonnistumisesta.** Cronin `MAILTO` ei tässä laitteessa
   toimi ilman postinvälitystä, eikä ADM:ssä ole Synologyn kaltaista ajastinta
   joka lähettäisi sähköpostin. Rikkoutunut yöajo näkyy siis vasta siinä, että
   etusivun lohkot katoavat kolmen vuorokauden päästä tuoreustarkistuksen
   takia. Tämä on putken heikoin kohta.
3. **Kaksi committia on pushaamatta** (tyhjän asetuksen tunnistus ja tämä
   kooste). NAS hakee mainista, joten se ei saa niitä ennen pushia.
4. **30 pv:n kasvu on osin arvioitu** 29.8.2026 asti.
5. **Dashboard elää NAS:illa**, `~/ilmiot/luonnokset/suosio.html`. Se ei siirry
   palvelimelle eikä ole versionhallinnassa. Työaseman kopio vanhenee nyt, kun
   ajo on siirtynyt pois.

## Komennot

```sh
# NAS: käsiajo ilman siirtoa
cd ~/ilmiot && ~/ilmiot-venv/bin/python scripts/paivita_suosio.py --ei-kirjoita

# NAS: ajo siirtoineen
cd ~/ilmiot && ~/ilmiot-venv/bin/python scripts/paivita_suosio.py --laheta

# NAS: asennuksen tarkistus, ei muuta mitään
sh ~/ilmiot/scripts/nas_asennus.sh --tarkista

# Työasema: nostot luonnossivulle lukuineen
python3 scripts/paivita_suosio.py

# Työasema: nostot index.html:ään ilman lukuja (kertaluontoinen)
python3 scripts/paivita_suosio.py --tuotanto

# Varmistukset
curl -sI https://www.xn--ilmit-mua.fi/data/suosio.js | head -1
curl -s https://www.xn--ilmit-mua.fi/ | grep -c NOSTOT-ALKU   # 3
```
