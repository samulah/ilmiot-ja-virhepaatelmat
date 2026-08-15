#!/usr/bin/env bash
# Suosiodatan yöajon pystytys NAS:ille (tavallinen Linux).
#
# Ajetaan NAS:illa, ei tällä koneella:
#
#     HAARA=suosio-ja-nostot bash nas_asennus.sh
#     bash nas_asennus.sh --tarkista      # ei muuta mitään, kertoo mikä puuttuu
#
# Skripti on idempotentti: sen voi ajaa uudelleen milloin tahansa. Se ei koskaan
# ylikirjoita .suosio.env:iä eikä viikkohistoriaa, koska ne ovat ainoat
# tiedostot joita ei voi generoida uudelleen.
#
# Miksi NAS eikä työasema: yöajo on hyödyllinen vain jos se ajetaan joka yö.
# WSL:n cron ajaa vain kun WSL on käynnissä, ja jos ajo jää väliin kolmena
# yönä, etusivun tuoreustarkistus piilottaa lohkot. NAS on aina päällä.

set -uo pipefail

REPO_URL="${REPO_URL:-https://github.com/samulah/ilmiot-ja-virhepaatelmat.git}"
HAARA="${HAARA:-main}"
KOHDE="${KOHDE:-$HOME/ilmiot}"
VENV="${VENV:-$HOME/ilmiot-venv}"
LOKI="${LOKI:-$HOME/.suosio.log}"
AVAIN="${AVAIN:-$HOME/.ssh/id_ed25519_ilmiot}"
AJOAIKA="${AJOAIKA:-10 3 * * *}"

TARKISTA=0
[ "${1:-}" = "--tarkista" ] && TARKISTA=1

vihrea() { printf '\033[32m✓\033[0m %s\n' "$*"; }
kelt()   { printf '\033[33m!\033[0m %s\n' "$*"; }
puna()   { printf '\033[31m✗\033[0m %s\n' "$*"; }
otsikko(){ printf '\n\033[1m── %s\033[0m\n' "$*"; }

# Alusta ratkaisee sekä paketinhallinnan että ajastuksen. Synologyssa ei ole
# apt:ia, ja käyttäjän crontab on siellä ansa: DSM ylikirjoittaa sen
# päivityksissä, jolloin yöajo katoaa ilman varoitusta. Oikea paikka on
# Task Scheduler.
ALUSTA="linux"
if [ -f /etc/VERSION ] && grep -qi synology /etc/VERSION 2>/dev/null; then
  ALUSTA="synology"
elif [ -d /volume1/@appstore ]; then
  ALUSTA="synology"
fi

if command -v apt >/dev/null 2>&1;   then ASENNA="sudo apt install -y"
elif command -v opkg >/dev/null 2>&1; then ASENNA="opkg install"
else ASENNA=""
fi

PUUTTUU=0
vaadi() {  # vaadi <komento> <asennuspaketti>
  if command -v "$1" >/dev/null 2>&1; then
    vihrea "$1 löytyy"
    return
  fi
  PUUTTUU=1
  if [ -n "$ASENNA" ]; then
    puna "$1 puuttuu — asenna: $ASENNA $2"
  elif [ "$ALUSTA" = synology ]; then
    puna "$1 puuttuu. Synologyssa ei ole apt:ia — kaksi tapaa:"
    echo "      a) Package Center → asenna Python 3 / Git Server"
    echo "      b) Entware (opkg), jos haluat tavallisen pakettivalikoiman"
  else
    puna "$1 puuttuu, eikä tunnettua paketinhallintaa löytynyt"
  fi
}

# ──────────────────────────────────────────────────────────────────────
otsikko "1. Esivaatimukset"
vaadi git git
vaadi python3 python3
vaadi ssh openssh-client
vaadi sftp openssh-client
if ! python3 -c 'import venv' 2>/dev/null; then
  puna "python3-venv puuttuu — asenna: sudo apt install -y python3-venv"
  PUUTTUU=1
else
  vihrea "python3-venv löytyy"
fi
[ "$PUUTTUU" = 1 ] && { echo; puna "Asenna puuttuvat paketit ja aja uudelleen."; exit 1; }

# ──────────────────────────────────────────────────────────────────────
otsikko "2. Repo: $KOHDE (haara $HAARA)"
if [ -d "$KOHDE/.git" ]; then
  vihrea "repo on jo olemassa"
  if [ "$TARKISTA" = 0 ]; then
    git -C "$KOHDE" fetch --quiet origin "$HAARA" && \
    git -C "$KOHDE" checkout --quiet "$HAARA" && \
    git -C "$KOHDE" merge --quiet --ff-only "origin/$HAARA" && \
    vihrea "päivitetty: $(git -C "$KOHDE" log --oneline -1)"
  fi
elif [ "$TARKISTA" = 1 ]; then
  puna "repoa ei ole kansiossa $KOHDE"
  PUUTTUU=1
else
  git clone --quiet --branch "$HAARA" "$REPO_URL" "$KOHDE" \
    && vihrea "kloonattu: $(git -C "$KOHDE" log --oneline -1)" \
    || { puna "kloonaus epäonnistui"; exit 1; }
fi

# ──────────────────────────────────────────────────────────────────────
otsikko "3. Python-ympäristö: $VENV"
# Oma venv repon ulkopuolella, jottei se sotke git statusta.
if [ -x "$VENV/bin/python" ]; then
  vihrea "venv on olemassa"
elif [ "$TARKISTA" = 1 ]; then
  puna "venviä ei ole"
  PUUTTUU=1
else
  python3 -m venv "$VENV" && vihrea "venv luotu"
fi
if [ -x "$VENV/bin/python" ]; then
  if "$VENV/bin/python" -c 'import psycopg2' 2>/dev/null; then
    vihrea "psycopg2 löytyy"
  elif [ "$TARKISTA" = 1 ]; then
    puna "psycopg2 puuttuu"
    PUUTTUU=1
  else
    "$VENV/bin/pip" install --quiet --upgrade pip
    if "$VENV/bin/pip" install --quiet psycopg2-binary; then
      vihrea "psycopg2-binary asennettu"
    else
      # psycopg2-binary tulee valmiina wheelinä vain osalle arkkitehtuureista.
      # x86_64 ja aarch64 ovat katettuja, armv7 ei — ja lähdekoodista
      # kääntäminen vaatii gcc:n ja libpq:n, joita NAS:illa harvoin on.
      puna "psycopg2-binary ei asentunut (arkkitehtuuri $(uname -m))"
      echo "      Todennäköisin syy: tälle arkkitehtuurille ei ole valmista"
      echo "      wheeliä. Siistein kiertotie on Docker:"
      echo "          docker run --rm -v $KOHDE:/repo -w /repo python:3-slim \\"
      echo "            sh -c 'pip install -q psycopg2-binary && \\"
      echo "                   python scripts/paivita_suosio.py --laheta'"
      PUUTTUU=1
    fi
  fi
fi

# ──────────────────────────────────────────────────────────────────────
otsikko "4. Asetukset ja tila"
# Nämä kaksi eivät ole versionhallinnassa eikä niitä voi generoida:
# .suosio.env sisältää kannan tunnukset, viikkohistoria estää saman ilmiön
# valinnan uudelleen. Molemmat on kopioitava työasemalta käsin.
if [ -f "$KOHDE/.suosio.env" ]; then
  vihrea ".suosio.env on paikallaan"
else
  puna ".suosio.env puuttuu — kopioi työasemalta:"
  echo "      scp ~/ilmiot_ja_virhe_paatelmat/.suosio.env $(whoami)@$(hostname):$KOHDE/"
  PUUTTUU=1
fi
if [ -f "$KOHDE/data/.viikko-historia.json" ]; then
  vihrea "viikkohistoria on paikallaan"
else
  kelt "viikkohistoria puuttuu — viikon ilmiön karenssi alkaa tyhjästä."
  echo "      scp ~/ilmiot_ja_virhe_paatelmat/data/.viikko-historia.json \\"
  echo "          $(whoami)@$(hostname):$KOHDE/data/"
fi

# ──────────────────────────────────────────────────────────────────────
otsikko "5. Yhteys kantaan"
if [ -f "$KOHDE/.suosio.env" ]; then
  PGH=$(grep -E '^PGHOST=' "$KOHDE/.suosio.env" | cut -d= -f2- | tr -d '"'"'"' ')
  PGP=$(grep -E '^PGPORT=' "$KOHDE/.suosio.env" | cut -d= -f2- | tr -d '"'"'"' ')
  PGP="${PGP:-5432}"
  if timeout 5 bash -c "cat < /dev/null > /dev/tcp/$PGH/$PGP" 2>/dev/null; then
    vihrea "portti $PGH:$PGP vastaa"
  else
    puna "kantaan $PGH:$PGP ei saada yhteyttä tältä koneelta"
    echo "      Kanta on lähiverkon osoitteessa. Tarkista että NAS on samassa"
    echo "      verkossa ja että kanta sallii yhteydet siltä (pg_hba.conf)."
    PUUTTUU=1
  fi
fi

# ──────────────────────────────────────────────────────────────────────
otsikko "6. SSH-avain webhotellille"
if [ -f "$AVAIN" ]; then
  vihrea "avain $AVAIN on olemassa"
elif [ "$TARKISTA" = 1 ]; then
  puna "avainta $AVAIN ei ole"
  PUUTTUU=1
else
  # Jos työaseman avain on jo viety webhotellin hallintaan, sen kopioiminen
  # säästää yhden käynnin hallintapaneelissa. Uusi avain on silti siistimpi:
  # yksi avain per kone, ja työaseman avaimen voi myöhemmin poistaa erikseen.
  kelt "Avainta ei ole. Vaihtoehto A: kopioi työaseman avainpari tänne"
  echo "      scp ~/.ssh/id_ed25519_ilmiot* $(whoami)@$(hostname):~/.ssh/"
  echo "      chmod 600 ~/.ssh/id_ed25519_ilmiot"
  echo "  Vaihtoehto B: luodaan uusi (tehdään nyt) ja viet sen hallintaan."
  mkdir -p "$(dirname "$AVAIN")" && chmod 700 "$(dirname "$AVAIN")"
  ssh-keygen -t ed25519 -f "$AVAIN" -N "" -C "ilmiot-suosio-nas" >/dev/null \
    && vihrea "uusi avain luotu"
fi
if [ -f "$AVAIN.pub" ]; then
  echo
  echo "  Vie tämä julkinen avain webhotellin hallintaan (SSH-avaimet):"
  echo
  sed 's/^/      /' "$AVAIN.pub"
  echo
fi

# Ilman tunnettua isäntäavainta BatchMode=yes epäonnistuu joka yö hiljaa —
# sftp ei voi kysyä vahvistusta kun tty puuttuu.
if [ -f "$KOHDE/.suosio.env" ]; then
  SFTPH=$(grep -E '^SFTP_HOST=' "$KOHDE/.suosio.env" | cut -d= -f2- | tr -d '"'"'"' ')
  if [ -n "$SFTPH" ]; then
    if ssh-keygen -F "$SFTPH" >/dev/null 2>&1; then
      vihrea "$SFTPH on known_hostsissa"
    elif [ "$TARKISTA" = 1 ]; then
      puna "$SFTPH puuttuu known_hostsista → yöajo epäonnistuisi hiljaa"
    else
      mkdir -p "$HOME/.ssh" && chmod 700 "$HOME/.ssh"
      ssh-keyscan -H "$SFTPH" >> "$HOME/.ssh/known_hosts" 2>/dev/null \
        && vihrea "$SFTPH lisätty known_hostsiin"
    fi
  fi
fi

# ──────────────────────────────────────────────────────────────────────
otsikko "7. Ajastus"
# git pull ennen ajoa: skripti lukee ilmiölistan index.html:stä ja
# julkaisupäivät sivujen JSON-LD:stä, joten vanhentunut kopio jättäisi uudet
# ilmiöt pois listoilta. --ff-only kaatuu mieluummin kuin tekee merge-commitin.
KOMENTO="cd $KOHDE && git pull --quiet --ff-only && $VENV/bin/python scripts/paivita_suosio.py --laheta >> $LOKI 2>&1"
RIVI="$AJOAIKA $KOMENTO"

if [ "$ALUSTA" = synology ]; then
  # DSM ylikirjoittaa käyttäjän crontabin päivityksissä, joten ajastus tehdään
  # Task Schedulerilla. Se myös näyttää ajon tuloksen käyttöliittymässä ja osaa
  # lähettää sähköpostin epäonnistumisesta — cronin MAILTO ei NAS:illa toimi
  # ilman erikseen pystytettyä postinvälitystä.
  kelt "Synology: älä käytä crontabia, DSM ylikirjoittaa sen päivityksissä."
  echo
  echo "  DSM → Ohjauspaneeli → Tehtävien ajoitus → Luo → Ajoitettu tehtävä →"
  echo "  Käyttäjän määrittämä komentosarja"
  echo
  echo "      Käyttäjä:   $(whoami)"
  echo "      Ajoitus:    päivittäin klo 03:10"
  echo "      Komento:"
  echo "$KOMENTO" | sed 's/^/          /'
  echo
  echo "  Laita lisäksi rasti kohtaan \"Lähetä ajon tulokset sähköpostitse\" ja"
  echo "  valitse että viesti tulee vain virheestä — muuten hiljainen"
  echo "  epäonnistuminen jää huomaamatta."
elif crontab -l 2>/dev/null | grep -qF "paivita_suosio.py"; then
  vihrea "cronissa on jo suosioajo:"
  crontab -l 2>/dev/null | grep -F "paivita_suosio.py" | sed 's/^/      /'
else
  kelt "cronissa ei ole suosioajoa. Lisää se komennolla:"
  echo
  echo "      (crontab -l 2>/dev/null; echo '$RIVI') | crontab -"
  echo
fi

# ──────────────────────────────────────────────────────────────────────
otsikko "Yhteenveto"
if [ "$PUUTTUU" = 1 ]; then
  puna "Jotain puuttuu vielä — ks. punaiset rivit yllä."
  exit 1
fi
vihrea "Esivaatimukset kunnossa."
echo
echo "  Koeajo ilman kirjoituksia ja ilman siirtoa:"
echo "      cd $KOHDE && $VENV/bin/python scripts/paivita_suosio.py --ei-kirjoita"
echo
echo "  Ensimmäinen oikea ajo siirtoineen (vasta kun avain on webhotellissa):"
echo "      cd $KOHDE && $VENV/bin/python scripts/paivita_suosio.py --laheta"
echo
echo "  Varmistus että tiedosto meni perille:"
echo "      curl -sI https://www.xn--ilmit-mua.fi/data/suosio.js | head -1"
echo
kelt "Muista sammuttaa työaseman cron, tai kaksi konetta kirjoittaa samaa"
kelt "tiedostoa ja viikon ilmiö eriytyy niiden välillä."
