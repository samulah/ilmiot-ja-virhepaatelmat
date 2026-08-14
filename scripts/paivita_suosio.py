#!/usr/bin/env python3
"""Suosiodata Postgresista etusivun nostoihin ja omaan dashboardiin.

Ajaa yhden kyselyn liikennekantaan, kirjoittaa kolme tiedostoa ja voi työntää
niistä yhden livepalvelimelle:

    data/suosio.js                  ~12 kt, AINOA tiedosto joka siirtyy yöllä
    luonnokset/suosio.html          oma analytiikkanäkymä, ei siirry palvelimelle
    luonnokset/etusivu-nostot.html  proto etusivun kolmesta lohkosta

Yöajo ei kosketa index.html:ään. Suosiodata elää erillisessä js-tiedostossa,
jonka etusivu lataa <script src="data/suosio.js" defer>:llä — muuten joka yö
työnnettäisiin palvelimelle 300 kt etusivu, joka voi ylikirjoittaa käsin tehtyjä
muutoksia (repon dokumentoitu pahin vikatila on deploy gap).

data/suosio.js sisältää vain slugit ja luvut. Otsikot, kuvaukset ja värit
haetaan selaimessa sivun olemassa olevista .hub-kortti-elementeistä hrefin
perusteella, samaan tapaan kuin haku tekee jo nyt. Siksi ilmiön
uudelleennimeäminen ei voi rikkoa suosiolohkoa eikä poistettu ilmiö jää haamuksi.

Asetukset gitignoratussa .suosio.env:ssä repon juuressa; kannan osoite ei kuulu
versionhallintaan. Ks. .suosio.env.malli.

    python3 scripts/paivita_suosio.py --skeema        # mitä kannassa on
    python3 scripts/paivita_suosio.py --demo          # GSC-CSV:stä, ei kantaa
    python3 scripts/paivita_suosio.py --ei-kirjoita   # kysely + yhteenveto
    python3 scripts/paivita_suosio.py                 # kirjoittaa tiedostot
    python3 scripts/paivita_suosio.py --laheta        # + SFTP livepalvelimelle
"""

import argparse
import html
import json
import random
import re
import subprocess
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
ENV = ROOT / ".suosio.env"
DATA = ROOT / "data"
SUOSIO_JS = DATA / "suosio.js"
VIIKKO_TILA = DATA / ".viikko-historia.json"
LUONNOKSET = ROOT / "luonnokset"
DASHBOARD = LUONNOKSET / "suosio.html"
PROTO = LUONNOKSET / "etusivu-nostot.html"

# Viikon ilmiön valinta. Tällä liikennemäärällä naiivi "suurin kasvuprosentti"
# olisi pelkkää kohinaa: 1 → 4 näyttöä on +300 %. Kolme suojaa: lattia karsii
# yksinumeroiset sivut, Laplace-tasoitus vaimentaa pienten lukujen suhteet, ja
# karenssi estää saman sivun toiston.
VIIKKO_LATTIA = 10      # vähintään näin monta lukukertaa kuluvassa 7 pv:n ikkunassa
VIIKKO_TASOITUS = 5     # (nyt + t) / (ennen + t)
VIIKKO_KARENSSI = 4     # montako edellistä valintaa pidetään poissa

# Lattia kalibroitu oikeaa dataa vasten 14.8.2026: 7 pv:n ikkunassa on 171
# lukukertaa 40 sivulle, ja vain 2 sivua ylittää 10. Sitä alempana viikkoluvut
# ovat 3–8, jolloin kasvusuhde on kohinaa eikä signaalia — lattian laskeminen
# ei tuo lisää ilmiöitä vaan lisää arvontaa. Nosta lattiaa kun liikenne kasvaa.
# 30 pv vs. edellinen 30 pv olisi vakaampi mittari, mutta kannassa on dataa
# vasta 1.7.2026 alkaen, joten vertailuikkuna täyttyy vasta ~syyskuussa 2026.

HELSINKI = timezone(timedelta(hours=3))  # kesäaika; vain aikaleiman esitysmuotoon


# ─────────────────────────────────────────────────────────────────────────
#  Asetukset
# ─────────────────────────────────────────────────────────────────────────

def lue_env():
    """KEY=value-tiedosto sanakirjaksi. #-kommentit ja tyhjät rivit ohitetaan."""
    if not ENV.exists():
        return {}
    asetukset = {}
    for rivi in ENV.read_text(encoding="utf-8").splitlines():
        rivi = rivi.strip()
        if not rivi or rivi.startswith("#") or "=" not in rivi:
            continue
        avain, _, arvo = rivi.partition("=")
        asetukset[avain.strip()] = arvo.strip().strip('"').strip("'")
    return asetukset


# ─────────────────────────────────────────────────────────────────────────
#  index.html on ainoa auktoritatiivinen ilmiölista
# ─────────────────────────────────────────────────────────────────────────

def lue_ilmiot():
    """index.html:n hub-kortit → [{slug, nro, nimi, kuvaus, vari, kategoria}].

    Sama lähde jota build_search_index.py ja build_sitemap.py jo käyttävät.
    Uutta datatiedostoa ei tarvita eikä sellaista pidä luoda: kaksi listaa
    ajautuisi erilleen.
    """
    teksti = INDEX.read_text(encoding="utf-8")
    ilmiot = []

    # Kategoriablokkien rajat sijainneista, ei lopetustagin hahmontunnistuksesta:
    # viimeistä kategoriaa seuraa hub-tyhja sisennettynä ja tyhjän rivin takana,
    # eikä sitä saa luotettavasti kiinni lookaheadilla.
    alut = [(m.start(), m.group(1)) for m in
            re.finditer(r'<div class="hub-kategoria" id="([^"]+)">', teksti)]
    loppu = teksti.find('<div class="hub-tyhja"')
    if loppu < 0:
        loppu = len(teksti)
    rajat = [a[0] for a in alut[1:]] + [loppu]

    for (alku, kat_id), paate in zip(alut, rajat):
        lohko = teksti[alku:paate]
        nimi_osuma = re.search(r'<h2 class="hub-kat-label">.*?</span>([^<]+)<span', lohko, re.S)
        kat_nimi = nimi_osuma.group(1).strip() if nimi_osuma else kat_id

        for kortti in re.finditer(
                r'<a href="([a-z0-9-]+)\.html" class="hub-kortti" style="--c:(#[0-9a-fA-F]{6})">\s*'
                r'<span class="hub-numero">(\d+)</span>\s*'
                r'<span class="hub-teksti">\s*'
                r'<span class="hub-nimi">(.*?)</span>\s*'
                r'<span class="hub-kuvaus">(.*?)</span>',
                lohko, re.S):
            ilmiot.append({
                "slug": kortti.group(1),
                "vari": kortti.group(2),
                "nro": int(kortti.group(3)),
                "nimi": kortti.group(4).strip(),
                "kuvaus": re.sub(r"\s+", " ", kortti.group(5)).strip(),
                "kategoria": kat_nimi,
                "kategoria_id": kat_id,
            })

    # Kaadu mieluummin kuin laske hiljaa väärin: jos korttien muoto tai
    # kategoriarajaus muuttuu, alilaskenta näkyisi vain siinä että joku ilmiö ei
    # koskaan päädy listalle. Sama opetus kuin paivita_maarat.py:n maara-tarkistuksessa.
    raaka = teksti.count('class="hub-kortti"')
    assert len(ilmiot) == raaka, (
        f"jäsennin löysi {len(ilmiot)} korttia mutta index.html:ssä on {raaka} — "
        "korttien tai kategorioiden rakenne muuttui")
    assert len(alut) == teksti.count('class="hub-kategoria"')
    return ilmiot


def lue_julkaisupaivat(slugit):
    """Sivun JSON-LD:n datePublished → {slug: 'YYYY-MM-DD'}. Dashboardia varten."""
    paivat = {}
    for slug in slugit:
        polku = ROOT / f"{slug}.html"
        if not polku.exists():
            continue
        osuma = re.search(r'"datePublished":\s*"(\d{4}-\d{2}-\d{2})"',
                          polku.read_text(encoding="utf-8"))
        if osuma:
            paivat[slug] = osuma.group(1)
    return paivat


# ─────────────────────────────────────────────────────────────────────────
#  Datalähteet
# ─────────────────────────────────────────────────────────────────────────

def normalisoi(polku):
    """Kannan URL → slug.html, tai None jos ei ole ilmiösivu.

    Kanta voi sisältää saman sivun monessa muodossa: täytenä URLina, unicode-
    tai punycode-isännällä, kyselymerkkijonon tai fragmentin kanssa, kauttaviiva
    edessä tai ilman. Kaikki näistä kuuluvat samalle sluggille.
    """
    if not polku:
        return None
    p = polku.strip()
    p = re.sub(r"^https?://[^/]+", "", p)     # isäntä pois
    p = p.split("?", 1)[0].split("#", 1)[0]   # kysely ja fragmentti pois
    p = p.lstrip("/")
    if p in ("", "index.html"):
        return "index.html"
    osuma = re.fullmatch(r"([a-z0-9-]+)\.html", p)
    return osuma.group(0) if osuma else None


def hae_kannasta(cfg, alku, loppu):
    """Yksi kysely → [(slug, pvm, nayttoja)] koko 30 pv:n ikkunalta.

    Kyselyn sopimus on tarkoituksella kapea: se palauttaa kolme saraketta
    päivätasolla, ja kaikki ikkunointi, ranking ja valinta tehdään Pythonissa
    missä sen voi testata. Kysely annetaan .suosio.env:n SUOSIO_SQL:ssä, koska
    tähtimallin taulunimet ovat kantakohtaisia — skripti ei arvaa niitä.
    """
    try:
        import psycopg2
    except ImportError:
        sys.exit("psycopg2 puuttuu: pip install psycopg2-binary")

    sql = cfg.get("SUOSIO_SQL")
    if not sql:
        sys.exit(
            "SUOSIO_SQL puuttuu .suosio.env:stä.\n"
            "Aja ensin --skeema, katso taulut, ja kirjoita kysely joka palauttaa\n"
            "kolme saraketta: polku (text), pvm (date), nayttoja (int).\n"
            "Parametrit %(alku)s ja %(loppu)s ovat ikkunan päivärajat.")

    yhteys = psycopg2.connect(
        host=cfg["PGHOST"], port=cfg.get("PGPORT", "5432"),
        dbname=cfg["PGDATABASE"], user=cfg["PGUSER"], password=cfg["PGPASSWORD"],
        connect_timeout=10)
    try:
        with yhteys.cursor() as kursori:
            kursori.execute(sql, {"alku": alku, "loppu": loppu})
            rivit = kursori.fetchall()
    finally:
        yhteys.close()

    tulos, hylatyt = [], defaultdict(int)
    for polku, pvm, nayttoja in rivit:
        slug = normalisoi(polku)
        if slug is None:
            hylatyt[str(polku)[:60]] += int(nayttoja or 0)
            continue
        if isinstance(pvm, datetime):
            pvm = pvm.date()
        tulos.append((slug, pvm, int(nayttoja or 0)))
    return tulos, dict(hylatyt)


def hae_gsc(cfg, alku, loppu):
    """Google-haun näytöt ja klikit → [(slug, pvm, lauseke, naytot, klikit, sija)].

    Eri asia kuin sivunäytöt: näyttö tarkoittaa että sivu näkyi hakutuloksissa,
    ei että joku luki sen. Siksi järjestys poikkeaa luetuimmista, ja siksi tämä
    kertoo mitä ihmiset etsivät eikä mitä he löysivät.

    Vapaaehtoinen: ilman SUOSIO_SQL_GSC:tä googlatuimmat-lohko jää pois eikä
    muu putki häiriinny.
    """
    sql = cfg.get("SUOSIO_SQL_GSC")
    if not sql:
        return [], {}
    import psycopg2

    yhteys = psycopg2.connect(
        host=cfg["PGHOST"], port=cfg.get("PGPORT", "5432"),
        dbname=cfg["PGDATABASE"], user=cfg["PGUSER"], password=cfg["PGPASSWORD"],
        connect_timeout=10)
    try:
        with yhteys.cursor() as kursori:
            kursori.execute(sql, {"alku": alku, "loppu": loppu})
            rivit = kursori.fetchall()
    finally:
        yhteys.close()

    tulos, hylatyt = [], defaultdict(int)
    for polku, pvm, lauseke, naytot, klikit, sija in rivit:
        slug = normalisoi(polku)
        if slug is None:
            hylatyt[str(polku)[:60]] += int(naytot or 0)
            continue
        if isinstance(pvm, datetime):
            pvm = pvm.date()
        tulos.append((slug, pvm, lauseke or "", int(naytot or 0),
                      int(klikit or 0), float(sija or 0)))
    return tulos, dict(hylatyt)


def summaa_gsc(rivit, alku, loppu):
    """GSC-rivit → {slug: {"naytot": n, "klikit": k}} annetulta väliltä."""
    summat = defaultdict(lambda: {"naytot": 0, "klikit": 0})
    for slug, pvm, _, naytot, klikit, _ in rivit:
        if alku <= pvm <= loppu:
            summat[slug]["naytot"] += naytot
            summat[slug]["klikit"] += klikit
    return dict(summat)


def summaa_lausekkeet(rivit, alku, loppu):
    """GSC-rivit → hakulausekkeet [(lauseke, slug, naytot, klikit, sija)].

    Sija on näytöillä painotettu keskiarvo: pelkkä AVG antaisi yhden näytön
    päivälle saman painon kuin sadan näytön päivälle.
    """
    kooste = defaultdict(lambda: {"naytot": 0, "klikit": 0, "sijasumma": 0.0,
                                  "sivut": defaultdict(int)})
    for slug, pvm, lauseke, naytot, klikit, sija in rivit:
        if not (alku <= pvm <= loppu) or not lauseke:
            continue
        k = kooste[lauseke]
        k["naytot"] += naytot
        k["klikit"] += klikit
        k["sijasumma"] += sija * naytot
        k["sivut"][slug] += naytot

    tulos = []
    for lauseke, k in kooste.items():
        paasivu = max(k["sivut"], key=k["sivut"].get) if k["sivut"] else None
        tulos.append((lauseke, paasivu, k["naytot"], k["klikit"],
                      k["sijasumma"] / k["naytot"] if k["naytot"] else 0.0))
    return sorted(tulos, key=lambda r: (-r[2], r[0]))


def hae_demo(alku, loppu, ilmiot):
    """Syntetisoi liikenne GSC-viennistä, jotta renderöinnin voi testata ilman kantaa.

    Ei ole oikeaa dataa eikä sitä pidä lähettää palvelimelle — --demo ja --laheta
    eivät toimi yhdessä.
    """
    csv_polku = ROOT / "datalake_analysis" / "13082026" / "Pages.csv"
    if not csv_polku.exists():
        sys.exit(f"Demodataa ei löydy: {csv_polku}")

    import csv as csv_moduuli
    pohja = {}
    with csv_polku.open(encoding="utf-8-sig", newline="") as f:
        for rivi in csv_moduuli.DictReader(f):
            slug = normalisoi(rivi.get("Top pages", ""))
            if slug and slug != "index.html":
                pohja[slug] = int(rivi.get("Impressions", 0) or 0)

    # Sivut joita GSC ei tunne saavat pienen taustaliikenteen, jottei
    # nollaliikennelista ole epärealistisen pitkä
    arpa = random.Random(20260814)
    for ilmio in ilmiot:
        pohja.setdefault(ilmio["slug"], arpa.randint(0, 6))

    rivit = []
    paiva = alku
    while paiva <= loppu:
        # Viikonloput hiljaisempia, viimeinen viikko hieman vilkkaampi
        kerroin = 0.7 if paiva.weekday() >= 5 else 1.0
        if (loppu - paiva).days < 7:
            kerroin *= 1.35
        for slug, kk in pohja.items():
            odotus = kk / 30.0 * kerroin
            n = arpa.poisson(odotus) if hasattr(arpa, "poisson") else _poisson(arpa, odotus)
            if n:
                rivit.append((slug, paiva, n))
        paiva += timedelta(days=1)
    return rivit, {}


def _poisson(arpa, lam):
    """Knuthin menetelmä — random-moduulissa ei ole poissonia."""
    if lam <= 0:
        return 0
    import math
    raja, k, p = math.exp(-lam), 0, 1.0
    while True:
        p *= arpa.random()
        if p <= raja:
            return k
        k += 1
        if k > 1000:
            return k


def tulosta_skeema(cfg):
    """Mitä kannassa on. Ilman tätä kyselyä ei voi kirjoittaa."""
    try:
        import psycopg2
    except ImportError:
        sys.exit("psycopg2 puuttuu: pip install psycopg2-binary")

    puuttuu = [k for k in ("PGHOST", "PGDATABASE", "PGUSER", "PGPASSWORD") if k not in cfg]
    if puuttuu:
        sys.exit(f".suosio.env: puuttuu {', '.join(puuttuu)} (ks. .suosio.env.malli)")

    yhteys = psycopg2.connect(
        host=cfg["PGHOST"], port=cfg.get("PGPORT", "5432"),
        dbname=cfg["PGDATABASE"], user=cfg["PGUSER"], password=cfg["PGPASSWORD"],
        connect_timeout=10)
    with yhteys.cursor() as k:
        k.execute("""
            SELECT table_schema, table_name, column_name, data_type
            FROM information_schema.columns
            WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
            ORDER BY table_schema, table_name, ordinal_position
        """)
        taulu = None
        for skeema, nimi, sarake, tyyppi in k.fetchall():
            if (skeema, nimi) != taulu:
                taulu = (skeema, nimi)
                print(f"\n{skeema}.{nimi}")
            print(f"    {sarake:<32} {tyyppi}")

        k.execute("""
            SELECT schemaname, relname, n_live_tup
            FROM pg_stat_user_tables ORDER BY n_live_tup DESC LIMIT 20
        """)
        print("\n\nSuurimmat taulut (rivimäärä):")
        for skeema, nimi, rivit in k.fetchall():
            print(f"    {skeema}.{nimi:<40} {rivit:>12,}".replace(",", " "))
    yhteys.close()


# ─────────────────────────────────────────────────────────────────────────
#  Ikkunointi ja viikon ilmiö
# ─────────────────────────────────────────────────────────────────────────

def summaa(rivit, alku, loppu):
    """Päivärivit → {slug: yhteensä} annetulta väliltä, päät mukaan lukien."""
    summat = defaultdict(int)
    for slug, pvm, n in rivit:
        if alku <= pvm <= loppu:
            summat[slug] += n
    return dict(summat)


def valitse_viikon_ilmio(d7, edellinen7, tanaan, kirjoita, tunnetut):
    """Suhteellisesti eniten noussut sivu, lattialla ja tasoituksella suojattuna.

    Valinta lasketaan vain maanantaisin ja pysyy samana koko viikon — muuten
    "viikon ilmiö" vaihtuisi joka yö, mikä tekisi nimestä valheen.
    """
    tila = {"historia": []}
    if VIIKKO_TILA.exists():
        try:
            tila = json.loads(VIIKKO_TILA.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    historia = tila.get("historia", [])

    edellinen_valinta = historia[0] if historia else None
    maanantai = tanaan.weekday() == 0

    if not maanantai and edellinen_valinta:
        # Muina päivinä pidetään viikon valinta, mutta luvut päivitetään tuoreiksi
        slug = edellinen_valinta["u"]
        return {
            "u": slug,
            "n": d7.get(slug, 0),
            "edellinen": edellinen7.get(slug, 0),
            "kasvu": edellinen_valinta.get("kasvu", 0.0),
            "valittu": edellinen_valinta["valittu"],
        }, historia

    karenssissa = {v["u"] for v in historia[:VIIKKO_KARENSSI]}
    ehdokkaat = []
    for slug, nyt in d7.items():
        # Vain ilmiösivut: kanta tuntee myös etusivun, tietoa.html:n ja
        # kategoriasivut, mutta niillä ei ole hub-korttia josta selain hakisi
        # nimen ja kuvauksen — valinta näkyisi lukijalle piilotettuna lohkona.
        if slug not in tunnetut or nyt < VIIKKO_LATTIA or slug in karenssissa:
            continue
        ennen = edellinen7.get(slug, 0)
        kasvu = (nyt + VIIKKO_TASOITUS) / (ennen + VIIKKO_TASOITUS)
        ehdokkaat.append((kasvu, nyt, slug, ennen))

    if not ehdokkaat:
        # Hiljainen tyhjä on parempi kuin kohinasta arvottu "nousija"
        return None, historia

    kasvu, nyt, slug, ennen = max(ehdokkaat)
    valinta = {
        "u": slug,
        "n": nyt,
        "edellinen": ennen,
        "kasvu": round(kasvu, 3),
        "valittu": tanaan.isoformat(),
    }
    if kirjoita:
        historia = [valinta] + [h for h in historia if h["u"] != slug]
        VIIKKO_TILA.parent.mkdir(exist_ok=True)
        VIIKKO_TILA.write_text(
            json.dumps({"historia": historia[:12]}, ensure_ascii=False, indent=2),
            encoding="utf-8")
    return valinta, historia


# ─────────────────────────────────────────────────────────────────────────
#  data/suosio.js
# ─────────────────────────────────────────────────────────────────────────

def kirjoita_suosio_js(d7, d30, edellinen7, viikko, ikkunat, tunnetut, g7, g30):
    """Slugit ja luvut. Ei otsikoita — ne haetaan selaimessa DOM-korteista."""
    def lista(summat, mukaan_edellinen):
        rivit = []
        for slug in sorted(summat, key=lambda s: (-summat[s], s)):
            if slug not in tunnetut:
                continue
            rivi = {"u": slug, "n": summat[slug]}
            if mukaan_edellinen:
                rivi["edellinen"] = edellinen7.get(slug, 0)
            rivit.append(rivi)
        return rivit

    def gsc_lista(summat):
        rivit = []
        for slug in sorted(summat, key=lambda s: (-summat[s]["naytot"], s)):
            if slug not in tunnetut or not summat[slug]["naytot"]:
                continue
            rivit.append({"u": slug, "n": summat[slug]["naytot"],
                          "k": summat[slug]["klikit"]})
        return rivit

    data = {
        "paivitetty": datetime.now(HELSINKI).isoformat(timespec="seconds"),
        "ikkunat": {
            "d7": [ikkunat["d7"][0].isoformat(), ikkunat["d7"][1].isoformat()],
            "d30": [ikkunat["d30"][0].isoformat(), ikkunat["d30"][1].isoformat()],
        },
        "d7": lista(d7, True),
        "d30": lista(d30, False),
        "g7": gsc_lista(g7),
        "g30": gsc_lista(g30),
        "viikonIlmio": viikko,
    }
    SUOSIO_JS.parent.mkdir(exist_ok=True)
    SUOSIO_JS.write_text(
        "window.ILMIO_SUOSIO=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8")
    return SUOSIO_JS.stat().st_size


# ─────────────────────────────────────────────────────────────────────────
#  Etusivun nostot: CSS, HTML ja renderöijä
# ─────────────────────────────────────────────────────────────────────────

NOSTOT_CSS = """
<style>
/* Nostolohkojen tyylit — scripts/paivita_suosio.py injektoi, älä muokkaa käsin.
   Ei style.css:ään: etusivu kantaa CSS:nsä itse ollakseen immuuni cache-bustille. */
.nostot { margin: 0 0 1.6rem; }
.nostot[hidden] { display: none; }
.nostot-parit {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 0.9rem;
  margin-bottom: 0.9rem;
}
.nosto {
  background: #FDFAF2;
  border: 1.5px solid #D4C090;
  padding: 0.85rem 0.95rem 0.9rem;
}
.nosto[hidden] { display: none; }
.nosto-otsikko {
  font-family: 'DM Sans', system-ui, sans-serif;
  font-size: 0.67em;
  font-weight: 700;
  letter-spacing: 0.13em;
  text-transform: uppercase;
  color: var(--c-primary-mid);
  margin: 0 0 0.6rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
}
/* Korttien luokat ovat tarkoituksella eri kuin .hub-kortti: etusivun haku,
   nuolinäppäinnavigaatio ja randomIlmio() keräävät kaikki .hub-kortti-elementit,
   joten duplikaatti näkyisi hakutuloksissa kahdesti ja arvonnassa
   kaksinkertaisella painolla. */
.nosto-kortti {
  display: flex;
  align-items: flex-start;
  gap: 0.6rem;
  padding: 0.6rem 0.7rem;
  background: #fff;
  border-left: 4px solid var(--c, #2c3e50);
  border-top: 1px solid #E8DCBE;
  border-right: 1px solid #E8DCBE;
  border-bottom: 1px solid #E8DCBE;
  text-decoration: none;
  color: #1A1100;
  transition: border-color 0.1s, transform 0.1s;
}
.nosto-kortti:hover { border-color: var(--c, #2c3e50); transform: translateX(3px); }
.nosto-nro {
  flex: 0 0 auto;
  min-width: 1.5rem;
  height: 1.5rem;
  display: grid;
  place-items: center;
  background: var(--c, #2c3e50);
  color: #fff;
  font-family: 'DM Sans', system-ui, sans-serif;
  font-size: 0.7em;
  font-weight: 700;
  padding: 0 0.3rem;
}
.nosto-teksti { display: flex; flex-direction: column; gap: 0.15rem; min-width: 0; }
.nosto-nimi {
  font-family: 'Spectral', Georgia, serif;
  font-size: 1.02em;
  font-weight: 600;
  line-height: 1.25;
}
.nosto-kuvaus {
  font-size: 0.83em;
  line-height: 1.4;
  color: #4A3D1F;
}
.nosto-meta {
  margin: 0.55rem 0 0;
  font-family: 'DM Sans', system-ui, sans-serif;
  font-size: 0.76em;
  color: #6B5A2E;
  display: flex;
  align-items: center;
  gap: 0.6rem;
  flex-wrap: wrap;
}
.nosto-nappi {
  font-family: 'DM Sans', system-ui, sans-serif;
  font-size: 0.95em;
  font-weight: 600;
  color: var(--c-primary-dark);
  background: transparent;
  border: 1.5px solid var(--c-primary);
  padding: 0.3rem 0.7rem;
  cursor: pointer;
  transition: background 0.12s, color 0.12s;
}
.nosto-nappi:hover { background: var(--c-primary); color: #fff; }
.nosto-nappi:focus-visible { outline: 2px solid var(--c-primary-mid); outline-offset: 2px; }
.nosto-valilehdet { display: flex; gap: 0.3rem; }
.nosto-valilehti {
  font-family: 'DM Sans', system-ui, sans-serif;
  font-size: 1em;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: #8B7A4E;
  background: transparent;
  border: 1.5px solid transparent;
  padding: 0.15rem 0.45rem;
  cursor: pointer;
}
.nosto-valilehti[aria-selected="true"] {
  color: var(--c-primary-dark);
  border-color: var(--c-primary);
  background: #FBF3DC;
}
.nosto-lista { list-style: none; margin: 0; padding: 0; counter-reset: sija; }
.nosto-rivi { counter-increment: sija; }
.nosto-rivi a {
  display: flex;
  align-items: baseline;
  gap: 0.55rem;
  padding: 0.38rem 0.2rem;
  border-bottom: 1px solid #EFE6CE;
  text-decoration: none;
  color: #1A1100;
}
.nosto-rivi:last-child a { border-bottom: 0; }
.nosto-rivi a:hover { background: #FBF3DC; }
.nosto-rivi a::before {
  content: counter(sija);
  flex: 0 0 1.1rem;
  font-family: 'DM Sans', system-ui, sans-serif;
  font-size: 0.78em;
  font-weight: 700;
  color: var(--c-primary-mid);
  text-align: right;
}
.nosto-rivi-nimi {
  font-weight: 600;
  flex: 1 1 auto;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.nosto-rivi-luku {
  font-family: 'DM Sans', system-ui, sans-serif;
  font-size: 0.76em;
  color: #6B5A2E;
  flex: 0 0 auto;
  font-variant-numeric: tabular-nums;
}
@media (max-width: 640px) {
  .nostot-parit { grid-template-columns: 1fr; gap: 0.7rem; }
  .nosto-kuvaus { font-size: 0.86em; }
}
</style>
"""

NOSTOT_HTML = """
<!-- NOSTOT-ALKU — scripts/paivita_suosio.py injektoi, älä muokkaa käsin -->
<section class="nostot" id="nostot" hidden>
  <div class="nostot-parit">
    <article class="nosto" id="nosto-viikko" hidden>
      <h2 class="nosto-otsikko">Viikon ilmiö</h2>
      <a class="nosto-kortti" id="viikko-kortti" href="#">
        <span class="nosto-nro"></span>
        <span class="nosto-teksti">
          <span class="nosto-nimi"></span>
          <span class="nosto-kuvaus"></span>
        </span>
      </a>
      <p class="nosto-meta" id="viikko-meta"></p>
    </article>

    <article class="nosto" id="nosto-random">
      <h2 class="nosto-otsikko">Satunnainen ilmiö</h2>
      <a class="nosto-kortti" id="random-kortti" href="#">
        <span class="nosto-nro"></span>
        <span class="nosto-teksti">
          <span class="nosto-nimi"></span>
          <span class="nosto-kuvaus"></span>
        </span>
      </a>
      <p class="nosto-meta">
        <button type="button" class="nosto-nappi" id="arvo-uusi">Arvo uusi</button>
        <span id="random-vihje">139 ilmiötä, ei mitään järjestystä</span>
      </p>
    </article>
  </div>

  <div class="nostot-parit">
    <article class="nosto" id="nosto-luetuimmat" hidden>
      <h2 class="nosto-otsikko">
        Luetuimmat
        <span class="nosto-valilehdet" role="tablist" aria-label="Aikaväli">
          <button type="button" class="nosto-valilehti" role="tab" data-lista="luetuimmat" data-ikkuna="d7" aria-selected="true">7 pv</button>
          <button type="button" class="nosto-valilehti" role="tab" data-lista="luetuimmat" data-ikkuna="d30" aria-selected="false">30 pv</button>
        </span>
      </h2>
      <ol class="nosto-lista" id="luetuimmat-lista"></ol>
      <p class="nosto-meta" id="luetuimmat-meta"></p>
    </article>

    <article class="nosto" id="nosto-googlatuimmat" hidden>
      <h2 class="nosto-otsikko">
        Googlatuimmat
        <span class="nosto-valilehdet" role="tablist" aria-label="Aikaväli">
          <button type="button" class="nosto-valilehti" role="tab" data-lista="googlatuimmat" data-ikkuna="g7" aria-selected="true">7 pv</button>
          <button type="button" class="nosto-valilehti" role="tab" data-lista="googlatuimmat" data-ikkuna="g30" aria-selected="false">30 pv</button>
        </span>
      </h2>
      <ol class="nosto-lista" id="googlatuimmat-lista"></ol>
      <p class="nosto-meta" id="googlatuimmat-meta"></p>
    </article>
  </div>
</section>
<!-- NOSTOT-LOPPU -->
"""

NOSTOT_JS = r"""
<!-- NOSTOT-ALKU — scripts/paivita_suosio.py injektoi, älä muokkaa käsin -->
<script src="data/suosio.js" defer></script>
<script>
document.addEventListener('DOMContentLoaded', function () {
  // TESTIVAIHE: lukukerrat näkyvissä. Tuotantoon vietäessä tämä yksi rivi
  // falseksi — data sisältää luvut joka tapauksessa, vain esitys muuttuu.
  const NAYTA_LUVUT = __NAYTA_LUVUT__;

  // Yli tämän ikäistä dataa ei näytetä: "luetuimmat 7 päivää" viime kuun
  // luvuilla on pahempi kuin ei mitään. Jos yösiirto hajoaa, lohko katoaa itsestään.
  const TUOREUS_VRK = 3;

  const nostot = document.getElementById('nostot');
  if (!nostot) return;

  // Lähde on sivun oma korttilista, ei datatiedosto. Nimet, kuvaukset, värit ja
  // numerot ovat aina synkassa, koska niitä on vain yksi kappale.
  // Avaimena tiedostonimi, ei koko href: luonnoskopiossa polut ovat muotoa
  // ../darvo.html ja juuressa darvo.html, mutta data tuntee vain sluggin.
  const kortit = new Map();
  document.querySelectorAll('.hub-kategoria .hub-kortti').forEach(function (k) {
    const polku = k.getAttribute('href') || '';
    kortit.set(polku.replace(/^.*\//, ''), {
      avain: polku.replace(/^.*\//, ''),
      href: polku,
      nro: (k.querySelector('.hub-numero') || {}).textContent || '',
      nimi: (k.querySelector('.hub-nimi') || {}).textContent || '',
      kuvaus: (k.querySelector('.hub-kuvaus') || {}).textContent || '',
      vari: (k.getAttribute('style') || '').replace('--c:', '').trim()
    });
  });
  if (kortit.size === 0) return;

  // Näppäimistökäsittelijä sivun lopussa fokusoi hakukentän jokaisesta
  // tulostuvasta merkistä ja avaa aktiivisen kortin Enterillä. Ilman tätä
  // nostolohkon napit tappelisivat siitä fokuksesta.
  nostot.addEventListener('keydown', function (e) { e.stopPropagation(); });

  const data = window.ILMIO_SUOSIO || null;
  let tuore = false;
  if (data && data.paivitetty) {
    const ika = (Date.now() - new Date(data.paivitetty).getTime()) / 86400000;
    tuore = ika >= 0 && ika <= TUOREUS_VRK;
  }

  function taytaKortti(el, tieto) {
    el.setAttribute('href', tieto.href);
    el.style.setProperty('--c', tieto.vari);
    el.querySelector('.nosto-nro').textContent = tieto.nro;
    el.querySelector('.nosto-nimi').textContent = tieto.nimi;
    el.querySelector('.nosto-kuvaus').textContent = tieto.kuvaus;
  }

  function luku(n) {
    return n.toLocaleString('fi-FI') + (n === 1 ? ' lukukerta' : ' lukukertaa');
  }

  // ── Viikon ilmiö ──────────────────────────────────────────────────
  const varatut = new Set();
  if (tuore && data.viikonIlmio && kortit.has(data.viikonIlmio.u)) {
    const v = data.viikonIlmio;
    const tieto = kortit.get(v.u);
    taytaKortti(document.getElementById('viikko-kortti'), tieto);
    const kasvuPros = Math.round((v.kasvu - 1) * 100);
    const osat = [];
    if (kasvuPros > 0) osat.push('Lukukerrat nousivat ' + kasvuPros + ' % edellisviikosta');
    if (NAYTA_LUVUT) osat.push(luku(v.n) + ' viikossa');
    document.getElementById('viikko-meta').textContent = osat.join(' · ');
    document.getElementById('nosto-viikko').hidden = false;
    varatut.add(v.u);
  }

  // ── Luetuimmat ja googlatuimmat ───────────────────────────────────
  // Sama renderöijä molemmille: ne eroavat vain datakentästä ja saatteesta.
  // Luetuimmat = kuka oikeasti luki sivun, googlatuimmat = kuka näki sen
  // hakutuloksissa. Järjestys poikkeaa toisistaan, ja se ero on pointti.
  function pvm(iso) {
    const o = iso.split('-');
    return Number(o[2]) + '.' + Number(o[1]) + '.';
  }

  function rakennaLista(tunnus, oletusIkkuna, saate) {
    const lohko = document.getElementById('nosto-' + tunnus);
    const lista = document.getElementById(tunnus + '-lista');
    const meta = document.getElementById(tunnus + '-meta');
    if (!lohko || !lista) return null;
    const valilehdet = Array.from(
      document.querySelectorAll('.nosto-valilehti[data-lista="' + tunnus + '"]'));

    function piirra(ikkuna) {
      const rivit = (data[ikkuna] || [])
        .filter(function (r) { return kortit.has(r.u); }).slice(0, 6);
      lista.textContent = '';
      rivit.forEach(function (r) {
        const tieto = kortit.get(r.u);
        const li = document.createElement('li');
        li.className = 'nosto-rivi';
        const a = document.createElement('a');
        a.setAttribute('href', tieto.href);
        const nimi = document.createElement('span');
        nimi.className = 'nosto-rivi-nimi';
        nimi.textContent = tieto.nimi;
        a.appendChild(nimi);
        if (NAYTA_LUVUT) {
          const arvo = document.createElement('span');
          arvo.className = 'nosto-rivi-luku';
          arvo.textContent = r.n.toLocaleString('fi-FI');
          a.appendChild(arvo);
        }
        li.appendChild(a);
        lista.appendChild(li);
      });
      // g7/g30 käyttävät samoja päivärajoja kuin d7/d30
      const v = data.ikkunat && data.ikkunat[ikkuna.replace('g', 'd')];
      meta.textContent = (v ? pvm(v[0]) + ' – ' + pvm(v[1]) : '') +
                         (saate ? (v ? ' · ' : '') + saate : '');
      return rivit.length;
    }

    valilehdet.forEach(function (nappi) {
      nappi.addEventListener('click', function () {
        valilehdet.forEach(function (m) {
          m.setAttribute('aria-selected', String(m === nappi));
        });
        piirra(nappi.dataset.ikkuna);
      });
    });

    // Vain jos jotain oikeasti piirtyi: tyhjä otsikko välilehtineen on
    // huonompi kuin puuttuva lohko.
    if (piirra(oletusIkkuna) > 0) {
      lohko.hidden = false;
      return true;
    }
    return false;
  }

  if (tuore) {
    (data.d7 || []).slice(0, 3).forEach(function (r) { varatut.add(r.u); });
    rakennaLista('luetuimmat', 'd7', '');
    rakennaLista('googlatuimmat', 'g7', 'näkyi hakutuloksissa');
  }

  // ── Satunnainen ilmiö ─────────────────────────────────────────────
  // Toimii aina, myös ilman suosiodataa: lähde on sivun oma korttilista.
  const pooli = Array.from(kortit.values()).filter(function (t) { return !varatut.has(t.avain); });
  const kortti = document.getElementById('random-kortti');
  const vihje = document.getElementById('random-vihje');
  vihje.textContent = kortit.size + ' ilmiötä, ei mitään järjestystä';

  // Sekoituspussi: kaikki käydään läpi ennen kuin yksikään toistuu, joten
  // viisi peräkkäistä klikkausta antaa viisi eri ilmiötä.
  let pussi = [];
  function arvo() {
    if (!pussi.length) {
      pussi = pooli.slice();
      for (let i = pussi.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        const t = pussi[i]; pussi[i] = pussi[j]; pussi[j] = t;
      }
    }
    return pussi.pop();
  }

  if (pooli.length) {
    taytaKortti(kortti, arvo());
    document.getElementById('arvo-uusi').addEventListener('click', function () {
      taytaKortti(kortti, arvo());
    });
  } else {
    document.getElementById('nosto-random').hidden = true;
  }

  nostot.hidden = false;
});
</script>
<!-- NOSTOT-LOPPU -->
"""


def poista_nostot(teksti):
    """Aiemmat injektiot pois, jotta ajo on idempotentti."""
    return re.sub(r"\n?<!-- NOSTOT-ALKU.*?NOSTOT-LOPPU -->\n?", "\n", teksti, flags=re.S)


def injektoi(teksti, nayta_luvut):
    """Kolme lohkoa index.html:ään: CSS headiin, HTML katnavin jälkeen, JS loppuun."""
    teksti = poista_nostot(teksti)

    # CSS omaan <style>-lohkoonsa juuri ennen </head>. Ei style.css:ään: etusivu
    # kantaa CSS:nsä itse ollakseen immuuni cache-bustille (CLAUDE.md).
    css = "<!-- NOSTOT-ALKU -->" + NOSTOT_CSS.strip() + "<!-- NOSTOT-LOPPU -->"
    assert teksti.count("</head>") == 1
    teksti = teksti.replace("</head>", css + "\n</head>", 1)

    # HTML katnavin jälkeen, ennen ensimmäistä kategoriaa. Kategorioiden väliin
    # sijoitettuna se katkaisisi .hub-kategoria + .hub-kategoria -sisarussäännön,
    # joka piirtää kategorioiden väliviivat.
    ankkuri = '</nav>\n<div class="hub-kategoria"'
    assert teksti.count(ankkuri) == 1, "katnavin ja ensimmäisen kategorian raja ei osu"
    teksti = teksti.replace(ankkuri, "</nav>\n" + NOSTOT_HTML.strip() + '\n<div class="hub-kategoria"', 1)

    # JS sivun olemassa olevan skriptin jälkeen, ennen footeria
    ankkuri = '\n  <footer class="ilmio-footer">'
    assert teksti.count(ankkuri) == 1
    # Ei %-formatointia: JS sisältää prosenttimerkkejä näkyvässä tekstissä
    js = NOSTOT_JS.replace("__NAYTA_LUVUT__", "true" if nayta_luvut else "false").strip()
    assert "__NAYTA_LUVUT__" not in js
    teksti = teksti.replace(ankkuri, "\n" + js + ankkuri, 1)
    return teksti


def luonnossivuksi(teksti):
    """Juuren sivu → luonnoskansion sivu: noindex päälle, ../-etuliitteet polkuihin.

    Käänteinen operaatio lisaa_ilmiot.py:n juurisivuksi()-funktiolle. Ankkurit
    (#kohta), absoluutit URLit ja jo suhteutetut polut jätetään rauhaan.
    """
    def korjaa(osuma):
        attr, arvo = osuma.group(1), osuma.group(2)
        if re.match(r"^(#|https?:|//|mailto:|data:|\.\./)", arvo):
            return osuma.group(0)
        return f'{attr}="../{arvo}"'

    teksti = re.sub(r'\b(href|src)="([^"]*)"', korjaa, teksti)
    teksti = teksti.replace(
        "<head>",
        '<head>\n  <meta name="robots" content="noindex"><!-- POISTA-JULKAISTAESSA -->', 1)
    return teksti


# ─────────────────────────────────────────────────────────────────────────
#  Dashboard
# ─────────────────────────────────────────────────────────────────────────

def kirjoita_dashboard(ilmiot, d7, d30, edellinen7, viikko, ikkunat, julkaisut,
                       hylatyt, lahde, g7=None, g30=None, lausekkeet=None):
    """Oma analytiikkanäkymä: koko ranking, nousijat, nollat, kategoriat, erät."""
    def e(s):
        return html.escape(str(s), quote=True)

    def n(x):
        return f"{x:,}".replace(",", " ")

    g7 = g7 or {}
    g30 = g30 or {}
    lausekkeet = lausekkeet or []

    rivit = []
    for i in ilmiot:
        s = i["slug"] + ".html"
        nyt, ennen, kk = d7.get(s, 0), edellinen7.get(s, 0), d30.get(s, 0)
        gsc = g30.get(s, {"naytot": 0, "klikit": 0})
        rivit.append({**i, "d7": nyt, "ed7": ennen, "d30": kk,
                      "muutos": nyt - ennen,
                      "kasvu": (nyt + VIIKKO_TASOITUS) / (ennen + VIIKKO_TASOITUS),
                      "g30": gsc["naytot"], "klikit30": gsc["klikit"],
                      "julkaistu": julkaisut.get(i["slug"], "—")})

    yht7 = sum(r["d7"] for r in rivit)
    yht30 = sum(r["d30"] for r in rivit)
    nollat = [r for r in rivit if r["d30"] == 0]

    # Kategoriakooste
    katit = defaultdict(lambda: {"n": 0, "d7": 0, "d30": 0})
    for r in rivit:
        k = katit[r["kategoria"]]
        k["n"] += 1
        k["d7"] += r["d7"]
        k["d30"] += r["d30"]
    kat_rivit = sorted(katit.items(), key=lambda kv: -kv[1]["d30"])

    # Julkaisuerät: sivut niputettuna julkaisupäivän mukaan
    erat = defaultdict(lambda: {"n": 0, "d30": 0})
    for r in rivit:
        eb = erat[r["julkaistu"]]
        eb["n"] += 1
        eb["d30"] += r["d30"]
    era_rivit = sorted(erat.items(), reverse=True)

    # Suunta ratkaisee kuuluuko rivi listalle, ei pelkkä järjestys: ilman
    # muutos-ehtoa lyhyt laskijalista täyttyisi loppuun nousseilla sivuilla ja
    # väittäisi niitä laskijoiksi.
    nousijat = sorted([r for r in rivit if r["d7"] >= VIIKKO_LATTIA and r["muutos"] > 0],
                      key=lambda r: -r["kasvu"])[:12]
    laskijat = sorted([r for r in rivit if r["ed7"] >= VIIKKO_LATTIA and r["muutos"] < 0],
                      key=lambda r: r["kasvu"])[:12]

    def taulukko(otsikot, datarivit):
        th = "".join(f"<th>{e(o)}</th>" for o in otsikot)
        tr = "".join("<tr>" + "".join(f"<td>{s}</td>" for s in r) + "</tr>" for r in datarivit)
        return f"<table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>"

    def linkki(r):
        return f'<a href="../{e(r["slug"])}.html">{e(r["nimi"])}</a>'

    def merkki(x):
        if x > 0:
            return f'<span class="ylos">+{n(x)}</span>'
        if x < 0:
            return f'<span class="alas">{n(x)}</span>'
        return '<span class="nolla">0</span>'

    ranking = taulukko(
        ["#", "Ilmiö", "Kategoria", "7 pv", "Δ ed. 7 pv", "30 pv",
         "Google 30 pv", "Klikit", "Julkaistu"],
        [(r["nro"], linkki(r), e(r["kategoria"]), n(r["d7"]), merkki(r["muutos"]),
          n(r["d30"]), n(r["g30"]), n(r["klikit30"]), e(r["julkaistu"]))
         for r in sorted(rivit, key=lambda r: (-r["d7"], -r["d30"], r["nro"]))])

    def suunta_taulu(rivit_, tyhja):
        if not rivit_:
            return f"<p class='selite'>{tyhja}</p>"
        return taulukko(["Ilmiö", "Edellinen 7 pv", "Tämä 7 pv", "Muutos"],
                        [(linkki(r), n(r["ed7"]), n(r["d7"]), merkki(r["muutos"]))
                         for r in rivit_])

    nousu_taulu = suunta_taulu(nousijat, "Yksikään lattian ylittänyt sivu ei noussut.")
    lasku_taulu = suunta_taulu(laskijat, "Yksikään lattian ylittänyt sivu ei laskenut.")

    kat_taulu = taulukko(
        ["Kategoria", "Sivuja", "30 pv", "Per sivu", "Osuus"],
        [(e(k), v["n"], n(v["d30"]), n(round(v["d30"] / v["n"])),
          f'{v["d30"] / yht30 * 100:.1f} %' if yht30 else "—")
         for k, v in kat_rivit])

    era_taulu = taulukko(
        ["Julkaistu", "Sivuja", "30 pv", "Per sivu"],
        [(e(k), v["n"], n(v["d30"]), n(round(v["d30"] / v["n"])))
         for k, v in era_rivit])

    nolla_taulu = (
        taulukko(["#", "Ilmiö", "Kategoria", "Julkaistu"],
                 [(r["nro"], linkki(r), e(r["kategoria"]), e(r["julkaistu"]))
                  for r in sorted(nollat, key=lambda r: r["nro"])])
        if nollat else "<p class='ok'>Ei yhtään nollaliikenteen sivua.</p>")

    # ── Google ─────────────────────────────────────────────────────────
    gsc_yht = sum(r["g30"] for r in rivit)
    gsc_klikit = sum(r["klikit30"] for r in rivit)

    if gsc_yht:
        google_taulu = taulukko(
            ["Ilmiö", "Näytöt 30 pv", "Klikit", "CTR", "Luettu 30 pv"],
            [(linkki(r), n(r["g30"]), n(r["klikit30"]),
              f'{r["klikit30"] / r["g30"] * 100:.1f} %' if r["g30"] else "—",
              n(r["d30"]))
             for r in sorted(rivit, key=lambda r: -r["g30"])[:25] if r["g30"]])

        # Näkyvyys ilman klikkejä: sivu on hakutuloksissa mutta title tai
        # kuvaus ei myy. Tämä on suoraan seuraava CTR-työlista.
        aukot = sorted([r for r in rivit if r["g30"] >= 30 and r["klikit30"] == 0],
                       key=lambda r: -r["g30"])
        aukko_taulu = (
            taulukko(["Ilmiö", "Näytöt 30 pv", "Klikit", "Luettu 30 pv"],
                     [(linkki(r), n(r["g30"]), n(r["klikit30"]), n(r["d30"]))
                      for r in aukot[:20]])
            if aukot else "<p class='ok'>Ei näkyvyysaukkoja.</p>")

        # Sivut jotka saavat lukijoita muualta kuin Googlesta
        muualta = sorted([r for r in rivit if r["d30"] >= 5 and r["g30"] < r["d30"]],
                         key=lambda r: -(r["d30"] - r["g30"]))
        muualta_taulu = (
            taulukko(["Ilmiö", "Luettu 30 pv", "Google-näytöt", "Erotus"],
                     [(linkki(r), n(r["d30"]), n(r["g30"]), n(r["d30"] - r["g30"]))
                      for r in muualta[:15]])
            if muualta else "<p class='selite'>Ei tällaisia sivuja.</p>")

        lauseke_taulu = taulukko(
            ["Hakulauseke", "Näytöt", "Klikit", "CTR", "Keskisija", "Sivu"],
            [(e(l), n(nay), n(kli),
              f"{kli / nay * 100:.1f} %" if nay else "—",
              f"{sija:.1f}".replace(".", ","),
              (linkki(next(r for r in rivit if r["slug"] + ".html" == slug))
               if any(r["slug"] + ".html" == slug for r in rivit) else e(slug or "—")))
             for l, slug, nay, kli, sija in lausekkeet[:40]])

        google_osio = f"""
<section>
  <h2>Googlatuimmat</h2>
  <p class="selite">Näyttö tarkoittaa että sivu näkyi hakutuloksissa, ei että joku luki sen.
  Siksi järjestys poikkeaa luetuimmista — ja se ero on itsessään tieto. Yhteensä
  {n(gsc_yht)} näyttöä ja {n(gsc_klikit)} klikkiä 30 päivässä.
  <strong>Huom:</strong> Google-data laahaa 2–3 vrk, joten tuoreimmat päivät ovat vajaita.</p>
  {google_taulu}
</section>

<section>
  <h2>Näkyvyys ilman klikkejä</h2>
  <p class="selite">Vähintään 30 näyttöä, nolla klikkiä. Sivu löytyy mutta title tai
  kuvaus ei saa klikkaamaan — tai sija on liian matala. Tämä on suora CTR-työlista.</p>
  {aukko_taulu}
</section>

<section>
  <h2>Hakulausekkeet</h2>
  <p class="selite">Mitä ihmiset oikeasti kirjoittavat. Suomenkieliset rinnakkaistermit
  (&quot;suomeksi&quot;-loppuiset haut) kertovat mitä sanaa kannattaa käyttää otsikossa.</p>
  {lauseke_taulu}
</section>

<section>
  <h2>Lukijoita muualta kuin Googlesta</h2>
  <p class="selite">Enemmän lukukertoja kuin Google-näyttöjä: liikenne tulee suorana,
  sisäisistä linkeistä tai someen jaettuna. Nämä sivut eivät ole riippuvaisia hausta.</p>
  {muualta_taulu}
</section>"""
    else:
        google_osio = ('\n<section><h2>Googlatuimmat</h2><p class="selite">'
                       'Ei Google-dataa. Aseta <code>SUOSIO_SQL_GSC</code> '
                       '<code>.suosio.env</code>:iin.</p></section>')

    if viikko:
        v_nimi = next((r["nimi"] for r in rivit if r["slug"] + ".html" == viikko["u"]), viikko["u"])
        viikko_html = (f'<strong>{e(v_nimi)}</strong> — {n(viikko["n"])} lukukertaa '
                       f'(edellinen viikko {n(viikko["edellinen"])}), '
                       f'kasvu {round((viikko["kasvu"] - 1) * 100)} %. '
                       f'Valittu {e(viikko["valittu"])}.')
    else:
        viikko_html = ('Ei valintaa: yksikään sivu ei ylittänyt '
                       f'{VIIKKO_LATTIA} lukukerran lattiaa. Lohko piiloutuu etusivulla.')

    varoitus = ""
    if hylatyt:
        top = sorted(hylatyt.items(), key=lambda kv: -kv[1])[:10]
        varoitus = ('<div class="varoitus"><strong>Kannassa oli polkuja joita '
                    'index.html ei tunne</strong> — poistettuja sivuja, bottipolkuja tai '
                    'normalisoinnin aukko. Suurimmat:<ul>'
                    + "".join(f"<li><code>{e(p)}</code> — {n(m)}</li>" for p, m in top)
                    + "</ul></div>")

    demo = ('<div class="varoitus"><strong>DEMODATA.</strong> Luvut on syntetisoitu '
            'GSC-viennistä, eivät ole todellista liikennettä. Tarkoitettu vain '
            'renderöinnin testaamiseen ennen kuin kantayhteys on pystyssä.</div>'
            if lahde == "demo" else "")

    sivu = f"""<!DOCTYPE html>
<html lang="fi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex">
  <link rel="icon" type="image/svg+xml" href="../favicon.svg">
  <title>Suosio — Ilmiöitä</title>
  <link rel="stylesheet" href="../fonts/fonts.css">
  <link rel="stylesheet" href="../fonts/spectral.css">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{
      --c-primary: #C9A84C; --c-primary-dark: #1C1400;
      --c-primary-mid: #8B6914; --c-bg: #F5F0E5;
    }}
    body {{ font-family: 'DM Sans', system-ui, sans-serif; background: var(--c-bg);
           color: #1A1100; line-height: 1.55; }}
    .hub-header {{ position: sticky; top: 0; z-index: 20; display: flex; align-items: center;
      gap: 0.8rem; padding: 0.7rem 1.2rem; background: var(--c-primary-dark); color: #F5F0E5; }}
    .hub-header h1 {{ font-family: 'Spectral', Georgia, serif; font-size: 1.15rem; font-weight: 600; }}
    .hub-header p {{ font-size: 0.78rem; color: #C9B27A; }}
    .paluu-btn {{ margin-left: auto; color: var(--c-primary); text-decoration: none;
      border: 1.5px solid var(--c-primary); padding: 0.3rem 0.7rem; font-size: 0.8rem; }}
    .paluu-btn:hover {{ background: var(--c-primary); color: var(--c-primary-dark); }}
    main {{ max-width: 1240px; margin: 0 auto; padding: 1.4rem 1.2rem 4rem; }}
    section {{ margin-bottom: 2.2rem; }}
    h2 {{ font-family: 'Spectral', Georgia, serif; font-size: 1.3rem; font-weight: 600;
      margin-bottom: 0.2rem; border-bottom: 2px solid var(--c-primary); padding-bottom: 0.3rem; }}
    .selite {{ font-size: 0.85rem; color: #6B5A2E; margin: 0.35rem 0 0.8rem; max-width: 68ch; }}
    .luvut {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: 0.7rem; margin-bottom: 1.2rem; }}
    .luku {{ background: #FDFAF2; border: 1.5px solid #D4C090; border-left: 4px solid var(--c-primary);
      padding: 0.7rem 0.85rem; }}
    .luku b {{ display: block; font-family: 'Spectral', Georgia, serif; font-size: 1.7rem;
      line-height: 1.1; font-variant-numeric: tabular-nums; }}
    .luku span {{ font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.09em; color: #8B7A4E; }}
    table {{ width: 100%; border-collapse: collapse; background: #FDFAF2;
      border: 1.5px solid #D4C090; font-size: 0.86rem; }}
    th, td {{ padding: 0.34rem 0.6rem; text-align: left; border-bottom: 1px solid #EFE6CE; }}
    th {{ background: #F3E9CE; font-size: 0.71rem; text-transform: uppercase;
      letter-spacing: 0.07em; color: #6B5A2E; position: sticky; top: 3.1rem; }}
    td:nth-child(n+4) {{ text-align: right; font-variant-numeric: tabular-nums; }}
    tbody tr:hover {{ background: #FBF3DC; }}
    a {{ color: #8B6914; }}
    .ylos {{ color: #1e7a4a; font-weight: 600; }}
    .alas {{ color: #b03a2e; }}
    .nolla {{ color: #9a8c66; }}
    .ok {{ color: #1e7a4a; font-weight: 600; }}
    .varoitus {{ background: #FDF6DC; border-left: 4px solid #e67e22; padding: 0.8rem 1rem;
      margin-bottom: 1.4rem; font-size: 0.88rem; }}
    .varoitus ul {{ margin: 0.4rem 0 0 1.1rem; }}
    .rulla {{ max-height: 32rem; overflow: auto; border: 1.5px solid #D4C090; }}
    .rulla table {{ border: 0; }}
    .parit {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 1.2rem; }}
    code {{ background: #F3E9CE; padding: 0.05rem 0.3rem; font-size: 0.85em; }}
    footer {{ margin-top: 2.5rem; font-size: 0.78rem; color: #8B7A4E; }}
  </style>
</head>
<body>
<header class="hub-header">
  <img src="../favicon.svg" alt="" width="30" height="30">
  <div>
    <h1>Suosio</h1>
    <p>{e(ikkunat['d30'][0].isoformat())} – {e(ikkunat['d30'][1].isoformat())} &middot;
       päivitetty {e(datetime.now(HELSINKI).strftime('%-d.%-m.%Y %H:%M'))}</p>
  </div>
  <a class="paluu-btn" href="index.html">&larr; Luonnokset</a>
</header>
<main>
{demo}
{varoitus}

<div class="luvut">
  <div class="luku"><b>{n(yht7)}</b><span>lukukertaa 7 pv</span></div>
  <div class="luku"><b>{n(yht30)}</b><span>lukukertaa 30 pv</span></div>
  <div class="luku"><b>{n(gsc_yht)}</b><span>Google-näyttöä 30 pv</span></div>
  <div class="luku"><b>{n(gsc_klikit)}</b><span>Google-klikkiä 30 pv</span></div>
  <div class="luku"><b>{len(ilmiot)}</b><span>ilmiötä</span></div>
  <div class="luku"><b>{len(nollat)}</b><span>ilman liikennettä 30 pv</span></div>
</div>

<section>
  <h2>Viikon ilmiö</h2>
  <p class="selite">Suhteellisesti eniten noussut sivu. Ehdolle pääsee vain sivu jolla on
  vähintään {VIIKKO_LATTIA} lukukertaa kuluvalla viikolla, järjestys lasketaan tasoitetusti
  kaavalla (nyt+{VIIKKO_TASOITUS})/(ennen+{VIIKKO_TASOITUS}), ja {VIIKKO_KARENSSI} edellistä
  valintaa ovat karenssissa. Valinta tehdään maanantaisin ja pysyy koko viikon.</p>
  <p>{viikko_html}</p>
</section>

<div class="parit">
  <section>
    <h2>Nousijat</h2>
    <p class="selite">7 pv vs. edellinen 7 pv, lattian ylittäneet.</p>
    {nousu_taulu}
  </section>
  <section>
    <h2>Laskijat</h2>
    <p class="selite">Sivut joilla oli liikennettä ja joilta se väheni.</p>
    {lasku_taulu}
  </section>
</div>

{google_osio}

<section>
  <h2>Kategoriat</h2>
  <p class="selite">Mikä aihepiiri vetää. &quot;Per sivu&quot; on rehellisempi kuin
  kokonaissumma: iso kategoria kerää enemmän pelkällä koollaan.</p>
  {kat_taulu}
</section>

<section>
  <h2>Julkaisuerittäin</h2>
  <p class="selite">Uusi sivu tarvitsee 6–12 kuukautta noustakseen hakutuloksissa
  (ks. <a href="ANALYYSI.md">ANALYYSI.md</a> § 5), joten tuoreen erän matala luku ei
  vielä tarkoita floppia — vanhan erän matala luku tarkoittaa.</p>
  {era_taulu}
</section>

<section>
  <h2>Ei liikennettä 30 päivässä</h2>
  <p class="selite">Suoraan seuraava työlista: nämä sivut ovat olemassa mutta eivät löydy.</p>
  {nolla_taulu}
</section>

<section>
  <h2>Koko ranking</h2>
  <p class="selite">Kaikki {len(ilmiot)} ilmiötä 7 pv:n mukaan.</p>
  <div class="rulla">{ranking}</div>
</section>

<footer>
  Generoitu <code>scripts/paivita_suosio.py</code>:llä. Tämä sivu ei siirry
  palvelimelle eikä ole versionhallinnassa.
</footer>
</main>
</body>
</html>
"""
    DASHBOARD.write_text(sivu, encoding="utf-8")


# ─────────────────────────────────────────────────────────────────────────
#  Siirto
# ─────────────────────────────────────────────────────────────────────────

def laheta(cfg):
    """Yksi tiedosto SFTP:llä. Väliaikaisnimi + rename, jottei lukija näe puolikasta."""
    puuttuu = [k for k in ("SFTP_HOST", "SFTP_USER", "SFTP_POLKU") if k not in cfg]
    if puuttuu:
        sys.exit(f".suosio.env: puuttuu {', '.join(puuttuu)}")

    etä = cfg["SFTP_POLKU"].rstrip("/")
    komennot = (f"put {SUOSIO_JS} {etä}/suosio.js.uusi\n"
                f"-rm {etä}/suosio.js\n"
                f"rename {etä}/suosio.js.uusi {etä}/suosio.js\n"
                "bye\n")
    komento = ["sftp", "-b", "-", "-o", "BatchMode=yes"]
    if cfg.get("SFTP_KEY"):
        komento += ["-i", cfg["SFTP_KEY"]]
    if cfg.get("SFTP_PORT"):
        komento += ["-P", cfg["SFTP_PORT"]]
    komento.append(f'{cfg["SFTP_USER"]}@{cfg["SFTP_HOST"]}')

    tulos = subprocess.run(komento, input=komennot, capture_output=True, text=True, timeout=120)
    if tulos.returncode != 0:
        print(tulos.stdout, file=sys.stderr)
        print(tulos.stderr, file=sys.stderr)
        return False
    return True


# ─────────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--skeema", action="store_true", help="tulosta kannan taulut, älä tee muuta")
    ap.add_argument("--demo", action="store_true", help="syntetisoi data GSC-viennistä, ei kantayhteyttä")
    ap.add_argument("--ei-kirjoita", action="store_true", help="kysely ja yhteenveto ilman tiedostoja")
    ap.add_argument("--laheta", action="store_true", help="siirrä data/suosio.js palvelimelle")
    ap.add_argument("--tuotanto", action="store_true",
                    help="injektoi nostot suoraan index.html:ään luonnoskopion sijaan")
    args = ap.parse_args()

    cfg = lue_env()

    if args.skeema:
        tulosta_skeema(cfg)
        return

    if args.demo and args.laheta:
        sys.exit("--demo ja --laheta eivät toimi yhdessä: demodata ei kuulu palvelimelle.")

    kirjoita = not args.ei_kirjoita

    # Täydet päivät, tämä päivä pois: kesken oleva päivä vetäisi kärjen alas
    tanaan = datetime.now(HELSINKI).date()
    loppu = tanaan - timedelta(days=1)
    ikkunat = {
        "d7": (loppu - timedelta(days=6), loppu),
        "d30": (loppu - timedelta(days=29), loppu),
    }
    ed_alku, ed_loppu = loppu - timedelta(days=13), loppu - timedelta(days=7)

    ilmiot = lue_ilmiot()
    tunnetut = {i["slug"] + ".html" for i in ilmiot}

    if args.demo:
        rivit, hylatyt = hae_demo(ikkunat["d30"][0], loppu, ilmiot)
        gsc_rivit, gsc_hylatyt = [], {}
        lahde = "demo"
    else:
        rivit, hylatyt = hae_kannasta(cfg, ikkunat["d30"][0], loppu)
        gsc_rivit, gsc_hylatyt = hae_gsc(cfg, ikkunat["d30"][0], loppu)
        hylatyt = {**hylatyt, **gsc_hylatyt}
        lahde = "kanta"

    d7 = summaa(rivit, *ikkunat["d7"])
    d30 = summaa(rivit, *ikkunat["d30"])
    edellinen7 = summaa(rivit, ed_alku, ed_loppu)
    g7 = summaa_gsc(gsc_rivit, *ikkunat["d7"])
    g30 = summaa_gsc(gsc_rivit, *ikkunat["d30"])
    lausekkeet = summaa_lausekkeet(gsc_rivit, *ikkunat["d30"])

    viikko, _ = valitse_viikon_ilmio(d7, edellinen7, tanaan,
                                     kirjoita and not args.demo, tunnetut)

    # ── Yhteenveto ────────────────────────────────────────────────────
    yht7 = sum(v for k, v in d7.items() if k in tunnetut)
    yht30 = sum(v for k, v in d30.items() if k in tunnetut)
    nollia = len(tunnetut - {k for k, v in d30.items() if v})
    # Aikaleima ensimmäisenä: yöajo kirjoittaa lokiin append-tilassa, ja ilman
    # tätä peräkkäiset ajot sulautuvat toisiinsa eikä hiljaista epäonnistumista
    # erota onnistuneesta.
    print(f"\n=== {datetime.now(HELSINKI).strftime('%Y-%m-%d %H:%M:%S')} ===")
    print(f"Lähde        {lahde}")
    print(f"Ikkuna       {ikkunat['d30'][0]} – {loppu}  ({len(rivit)} päiväriviä)")
    print(f"Ilmiöitä     {len(ilmiot)}   ilman liikennettä 30 pv: {nollia}")
    print(f"Lukukertoja  {yht7} (7 pv)   {yht30} (30 pv)")
    if hylatyt:
        print(f"Tuntemattomia polkuja: {len(hylatyt)} kpl, "
              f"{sum(hylatyt.values())} osumaa — ks. dashboard")
    print("\nLuetuimmat 7 pv:")
    for slug in sorted((k for k in d7 if k in tunnetut), key=lambda s: -d7[s])[:10]:
        nimi = next(i["nimi"] for i in ilmiot if i["slug"] + ".html" == slug)
        print(f"    {d7[slug]:>7}  {nimi}")

    if g30:
        gsc_yht = sum(v["naytot"] for k, v in g30.items() if k in tunnetut)
        gsc_klikit = sum(v["klikit"] for k, v in g30.items() if k in tunnetut)
        print(f"\nGooglatuimmat 7 pv  (30 pv yhteensä {gsc_yht} näyttöä, "
              f"{gsc_klikit} klikkiä, {len(lausekkeet)} hakulauseketta):")
        for slug in sorted((k for k in g7 if k in tunnetut),
                           key=lambda s: -g7[s]["naytot"])[:10]:
            nimi = next(i["nimi"] for i in ilmiot if i["slug"] + ".html" == slug)
            print(f"    {g7[slug]['naytot']:>7}  {nimi}")
    else:
        print("\nGooglatuimmat: ei dataa (SUOSIO_SQL_GSC puuttuu tai on tyhjä)")
    if viikko:
        nimi = next((i["nimi"] for i in ilmiot if i["slug"] + ".html" == viikko["u"]), viikko["u"])
        print(f"\nViikon ilmiö: {nimi} "
              f"({viikko['edellinen']} → {viikko['n']}, kasvu {round((viikko['kasvu']-1)*100)} %)")
    else:
        print(f"\nViikon ilmiö: ei valintaa (lattia {VIIKKO_LATTIA} ei ylittynyt)")

    if not kirjoita:
        print("\n--ei-kirjoita: tiedostoja ei kirjoitettu.")
        return

    # ── Kirjoitukset ──────────────────────────────────────────────────
    koko = kirjoita_suosio_js(d7, d30, edellinen7, viikko, ikkunat, tunnetut, g7, g30)
    print(f"\n{SUOSIO_JS.relative_to(ROOT)}  {koko/1024:.1f} kt")

    kirjoita_dashboard(ilmiot, d7, d30, edellinen7, viikko, ikkunat,
                       lue_julkaisupaivat([i["slug"] for i in ilmiot]),
                       hylatyt, lahde, g7, g30, lausekkeet)
    print(f"{DASHBOARD.relative_to(ROOT)}")

    pohja = INDEX.read_text(encoding="utf-8")
    if args.tuotanto:
        INDEX.write_text(injektoi(pohja, nayta_luvut=False), encoding="utf-8")
        print("index.html  nostot injektoitu (NAYTA_LUVUT=false)")
    else:
        PROTO.write_text(luonnossivuksi(injektoi(pohja, nayta_luvut=True)), encoding="utf-8")
        print(f"{PROTO.relative_to(ROOT)}  (NAYTA_LUVUT=true)")

    if args.laheta:
        ok = laheta(cfg)
        print("SFTP        " + ("valmis" if ok else "EPÄONNISTUI"))
        if not ok:
            sys.exit(1)


if __name__ == "__main__":
    main()
