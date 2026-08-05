#!/usr/bin/env python3
"""
Lisää sisääntulevia "Liittyvät ilmiöt" -linkkejä GSC-datan kärkisivuille.

Tausta (GSC-AUDIT-2026-07-28.md): viisi eniten näyttökertoja keräävää sivua
jumittaa sijoituksilla 7–11, kun taas darvo.html on sijalla 4,2. Ero korreloi
sisääntulevien sisäisten linkkien määrän kanssa — hyvesignalointi.html sai
vain 4 linkkiä (joista 2 automaattisia: index + kategoriasivu), darvo 11 ja
halo-efekti 15.

Skripti pudottaa kohdesivun linkin lähdesivun liittyvat-lohkoon tynkänä;
varsinaiset kortit (numero, väri, kuvaus) rakentaa build_liittyvat.py, joka
on ajettava heti tämän jälkeen. Lähdesivut on valittu käsin aihepiirin
mukaan — ei automaattisesti, koska linkin pitää olla lukijalle mielekäs.

Idempotentti: jos linkki on jo lohkossa, sivua ei kosketa.

Käyttö:
    python3 scripts/lisaa_sisalinkit.py
    python3 scripts/build_liittyvat.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent

# kohde → lähdesivut, joilta linkitetään. Aihepiiri ratkaisee, ei pelkkä numero.
SUUNNITELMA = {
    "hyvesignalointi.html": [
        "viherpesu.html",                # sama pesu-mekanismi, eri kohde
        "performatiivinen-lasnaolo.html",  # näkyvyys ilman sisältöä
        "astroturf.html",                # lavastettu ruohonjuuritaso
        "sosiaalinen-todiste.html",      # yleisö signaalin vastaanottajana
        "rituaalinen-raportointi.html",  # muodon täyttäminen ilman vaikutusta
    ],
    "rage-bait.html": [
        "doomscrolling.html",            # sama huomiotalouden silmukka
        "trollitehdas.html",             # ammattimainen raivon tuotanto
        "kaikukammio.html",              # raivo leviää kammiossa
        "kuollut-internet.html",         # syötin tuottaja ei aina ihminen
        "kuollut-kissa.html",            # huomion ohjaaminen tarkoituksella
    ],
    "ai-slop.html": [
        "brandolinin-laki.html",         # roskan kumoaminen maksaa
        "astroturf.html",                # massatuotettu valesisältö
        "firehose-of-falsehood.html",    # määrä laadun sijaan
        "1-prosentin-saanto.html",       # kuka sisällön enää tuottaa
    ],
    "whataboutismi.html": [
        "maalitolppien-siirtaminen.html",  # sama väistöperhe
        "argumenttitulva.html",          # väitteillä hukuttaminen
        "omenoita-appelsiineja.html",    # kelvoton rinnastus
        "darvo.html",                    # roolien kääntö vastasyytöksellä
    ],
    "brandolinin-laki.html": [
        "poen-laki.html",                # nimetty verkkokeskustelun laki
        "betteridgen-laki.html",         # väitteen ja todistustaakan suhde
        "godwinin-laki.html",            # nimetty verkkokeskustelun laki
    ],
}

# Toinen aalto: P2:n klusterisivut julkaistiin 28.7.2026. Ne linkittävät jo
# vakiintuneisiin sivuihin, mutta ilman paluulinkkejä klusteri jäisi
# yksisuuntaiseksi — uudet sivut eivät saisi linkkiarvoa eivätkä lukijat
# löytäisi niitä keskussivuilta. Korttimäärä pidetään 3–7:ssä, joten
# lähdesivut on valittu myös sen mukaan, kuinka täysi lohko jo on.
KLUSTERI = {
    "sinipesu.html": [
        "viherpesu.html",                # kategorian ankkuri, sama mekanismi
        "tekoalypesu.html",              # sisarpesu
        "hyvesignalointi.html",          # sitoumus vs. teko
    ],
    "urheilupesu.html": [
        "viherpesu.html",
        "hyvesignalointi.html",
        "halo-efekti.html",              # myönteinen piirre värittää kokonaisuuden
        "pinkkipesu.html",               # kolmikko linkittyy keskenään
    ],
    "pinkkipesu.html": [
        "tekoalypesu.html",
        "hyvesignalointi.html",
        "sosiaalinen-todiste.html",      # symboli yleisön signaalina
        "sinipesu.html",                 # kolmikko linkittyy keskenään
        "urheilupesu.html",
    ],
    "klikkiotsikko.html": [
        "rage-bait.html",                # syöttiperheen keskus
        "ai-slop.html",
        "doomscrolling.html",
        "betteridgen-laki.html",         # kysymysotsikko on klikkiotsikon alalaji
    ],
    "engagement-bait.html": [
        "rage-bait.html",
        "ai-slop.html",
        "kaikukammio.html",
    ],
}

# Kolmas aalto: TOIMENPIDESUUNNITELMA-2026-08-04 kohdat H2–H3. Kohteet ovat
# sivuja, joilla on näyttöjä muttei klikkejä sijalta 7–10 — GSC-datan mukaan
# klikkejä tulee vasta sijalta ≤5, joten kyse on sijoituksen nostosta.
# hyvesignalointi.html on H2:n nimetty kohde, mutta se oli jo 12 sisääntulevalla
# (darvo 11) toisen aallon jäljiltä; siksi tässä vain kaksi täydennystä.
GSC_ELOKUU = {
    "hanlonin-partaveitsi.html": [     # 38 näyttöä, sija 7,76, 8 linkkiä
        "occamin-partaveitsi.html",    # sisarpartaveitsi, sama päättelyperhe
        "dunning-kruger.html",         # tyhmyys selittää ennen pahuutta
        "blame-game.html",             # syyllisen etsintä ilman tahallisuutta
        "strateginen-osaamattomuus.html",  # osaamattomuus tahallisena
        "kafka-ilmio.html",            # järjestelmä vahingoittaa ilman aikomusta
    ],
    "doomscrolling.html": [            # 30 näyttöä, sija 9,38, 8 linkkiä
        "kaikukammio.html",            # sama syötteen mekanismi
        "fofo.html",                   # pelko ohjaa selaamista
        "engagement-bait.html",        # syöte on rakennettu pidättämään
        "parasosiaalinen-suhde.html",  # syötteen henkilöityminen
    ],
    "peterin-periaate.html": [         # 12 näyttöä, sija 8,00, 8 linkkiä
        "parkinsonin-laki.html",       # nimetty organisaatiolaki
        "rautainen-laki.html",         # organisaation väistämätön rappeutuminen
        "hiljainen-irtisanominen.html",  # ylennyksen kääntöpuoli
        "hippo-efekti.html",           # pätemättömän päätösvalta
        "strateginen-osaamattomuus.html",
    ],
    "hyvesignalointi.html": [          # 261 näyttöä, sija 7,89 — H2:n kärkikohde
        "konsensus-fetissi.html",      # yksimielisyyden esittäminen
        "manufactured-consent.html",   # signaali suostumuksen tuottajana
    ],
}

ASIDE_RE = re.compile(
    r'(<aside class="liittyvat" aria-label="Liittyvät ilmiöt">.*?)'
    r'(\n    </div>\n  </aside>)', re.S)


def main() -> None:
    lisatty = 0
    kosketut = set()
    for kohde, lahteet in {**SUUNNITELMA, **KLUSTERI, **GSC_ELOKUU}.items():
        assert (ROOT / kohde).exists(), f"{kohde} puuttuu"
        for lahde in lahteet:
            polku = ROOT / lahde
            assert polku.exists(), f"{lahde} puuttuu"
            src = polku.read_text(encoding="utf-8")
            m = ASIDE_RE.search(src)
            assert m, f"{lahde}: liittyvat-lohkoa ei tunnistettu"
            if f'href="{kohde}"' in m.group(1):
                continue
            tynka = f'\n    <a href="{kohde}" class="liittyvat-kortti"></a>'
            polku.write_text(
                src[:m.end(1)] + tynka + src[m.end(1):], encoding="utf-8")
            lisatty += 1
            kosketut.add(lahde)
    print(f"sisalinkit: {lisatty} linkkiä lisätty {len(kosketut)} sivulle")
    print("aja seuraavaksi: python3 scripts/build_liittyvat.py")


if __name__ == "__main__":
    main()
