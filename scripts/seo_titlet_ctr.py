#!/usr/bin/env python3
"""
Vaihe 1: title- ja meta-remontti CTR:n korjaamiseksi (top-15 sivua).

Tausta: seo-suunnitelmat/gsc-analyysi-2026-07-25.md
  - Toteutunut CTR 0,59 % vs. nykysijoitusten odotettu 2,52 % (-77 %).
  - 30 % näytöistä tulee "suomeksi / tarkoittaa / mitä on" -kyselyistä,
    mutta yksikään title ei sisällä noita sanoja.
  - 48/113 titleä ylittää 60 merkkiä ja katkeaa SERPissä juuri runollisen
    alaotsikon kohdalla, joka ei osu yhteenkään hakusanaan.

Muutos per sivu (6 kenttää):
    <title>, meta description, og:title, og:description,
    twitter:title, twitter:description

EI kosketa: H1, leipäteksti, JSON-LD (headline / DefinedTerm / breadcrumb).
Runollinen alaotsikko säilyy H1:ssä — se poistuu vain titlestä.
Siksi tämä ei aiheuta driftiä: build_search_index.py lukee .ilmio-säiliöstä,
llms.txt käyttää omaa kuvaustaan eikä build_sitemap.py lue titleä.

Sääntö: title ei lupaa suomennosta, jota sivun leipätekstissä ei ole.
  - raivosyötti (rage-bait, 4 mainintaa) ja kaasuvalotus (gaslighting, 1) OK.
  - tekoälylieju / tuomioselailu / entäskunismi / moraaliposeeraus puuttuvat
    vielä → ne otetaan titleen vasta vaiheessa 2, kun lohko on lisätty.

Deterministinen ja idempotentti: aja uudelleen turvallisesti.
    python3 scripts/seo_titlet_ctr.py [--kuivaharjoitus]
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

# slug: (title ilman brändihäntää, description)
# Titlet mitoitettu niin että title + " | Ilmiöitä" mahtuu ~60 merkkiin.
# Descriptionit alkavat suoralla määritelmällä ("X tarkoittaa ..."), eivät
# brändipuheella. Huom: vain yksinkertaiset lainausmerkit — teksti menee
# HTML-attribuuttiin, jonka rajaimena on ".
SIVUT = {
    "whataboutismi": (
        "Whataboutismi — mitä se tarkoittaa?",
        "Whataboutismi tarkoittaa vastaamista kritiikkiin kysymällä 'entäs ne "
        "muut?'. Näin tunnistat huomionsiirron ja vastaat siihen tehokkaasti.",
    ),
    "ai-slop": (
        "AI slop suomeksi — mitä se tarkoittaa?",
        "AI slop tarkoittaa tekoälyllä massatuotettua halpasisältöä, joka "
        "täyttää verkon. Näin tunnistat koneellisen sisällön ja suojaudut siltä.",
    ),
    "hyvesignalointi": (
        "Hyvesignalointi — mitä se tarkoittaa?",
        "Hyvesignalointi tarkoittaa hyveen esittämistä yleisölle, ei asian "
        "edistämistä. Näin erotat signaalin todellisista teoista.",
    ),
    "darvo": (
        "DARVO — manipulaatiotaktiikka suomeksi",
        "DARVO tarkoittaa manipulaatiotaktiikkaa: kiistä, hyökkää, käännä "
        "roolit. Näin tunnistat sen, kun tekijä tekee itsestään uhrin.",
    ),
    "rage-bait": (
        "Rage bait suomeksi — mitä raivosyötti tarkoittaa",
        "Rage bait eli raivosyötti tarkoittaa sisältöä, joka ärsyttää "
        "tahallaan. Näin tunnistat koneiston ja lakkaat ruokkimasta sitä.",
    ),
    "dunning-kruger": (
        "Dunning–Kruger-ilmiö — mitä se tarkoittaa?",
        "Dunning–Kruger-ilmiö tarkoittaa sitä, että vähäinen taito tuottaa "
        "suurta itsevarmuutta. Mistä ilmiössä on kyse — ja vastalääkkeet.",
    ),
    "halo-efekti": (
        "Halo-efekti — mitä se tarkoittaa?",
        "Halo-efekti tarkoittaa sitä, että yksi hyvä piirre värittää koko "
        "arvion. Näin ensivaikutelma harhauttaa — ja näin suojaat päätöksesi.",
    ),
    "bkt-harha": (
        "BKT-harha — mitä bruttokansantuote ei kerro",
        "BKT-harha tarkoittaa sitä, että talous kasvaa paperilla muttei "
        "arjessa. Mitä BKT ei mittaa ja mihin lukuihin katsoa sen sijaan.",
    ),
    "gaslighting": (
        "Gaslighting suomeksi — mitä kaasuvalotus on",
        "Gaslighting eli kaasuvalotus tarkoittaa toisen todellisuudentajun "
        "järjestelmällistä kiistämistä. Näin tunnistat manipulaation ja torjut sen.",
    ),
    "hanlonin-partaveitsi": (
        "Hanlonin partaveitsi — mitä se tarkoittaa?",
        "Hanlonin partaveitsi tarkoittaa periaatetta: älä oleta pahuutta, jos "
        "tyhmyys riittää selitykseksi. Periaate, sen rajat ja käyttö arjessa.",
    ),
    "peterin-periaate": (
        "Peterin periaate — mitä se tarkoittaa?",
        "Peterin periaate tarkoittaa sitä, että jokainen ylenee epäpätevyytensä "
        "tasolle. Miksi hyvä tekijä voi olla huono esihenkilö — ja miten se korjataan.",
    ),
    "honeypot-huijaus": (
        "Honeypot-huijaus — mitä se tarkoittaa?",
        "Honeypot-huijaus tarkoittaa ansaa, johon on helppo mennä ja mahdoton "
        "palata. Näin houkutusansa toimii ja näin tunnistat sen ajoissa.",
    ),
    "doomscrolling": (
        "Doomscrolling suomeksi — mitä se tarkoittaa?",
        "Doomscrolling tarkoittaa pakonomaista huonojen uutisten selaamista. "
        "Miksi algoritmi syöttää ahdistusta ja miten katkaiset kierteen.",
    ),
    "kaarmeoljy": (
        "Käärmeöljy — mitä se tarkoittaa?",
        "Käärmeöljy tarkoittaa ihmetuotetta, joka lupaa parantaa kaiken eikä "
        "paranna mitään. Näin tunnistat katteettomat teho- ja terveysväitteet.",
    ),
    "streisand-ilmio": (
        "Streisand-ilmiö — mitä se tarkoittaa?",
        "Streisand-ilmiö tarkoittaa sitä, että salailuyritys levittää tiedon "
        "tehokkaammin kuin julkaisu. Mekanismi, esimerkit ja miten vältät ansan.",
    ),
}

BRANDI = " | Ilmiöitä"


def korvaa(html: str, kaava: str, uusi: str) -> tuple[str, bool]:
    """Korvaa yhden kentän. Palauttaa (html, muuttuiko)."""
    uusi_html, n = re.subn(kaava, lambda _: uusi, html, count=1)
    if n == 0:
        raise SystemExit(f"  VIRHE: kaavaa ei löytynyt: {kaava}")
    return uusi_html, uusi_html != html


def main() -> None:
    kuiva = "--kuivaharjoitus" in sys.argv
    muutettu = 0

    for slug, (otsikko, kuvaus) in SIVUT.items():
        polku = ROOT / f"{slug}.html"
        if not polku.exists():
            raise SystemExit(f"VIRHE: {polku.name} puuttuu")

        html = alkup = polku.read_text(encoding="utf-8")
        title = otsikko + BRANDI

        html, _ = korvaa(html, r"<title>.*?</title>", f"<title>{title}</title>")
        html, _ = korvaa(
            html,
            r'<meta name="description" content=".*?">',
            f'<meta name="description" content="{kuvaus}">',
        )
        html, _ = korvaa(
            html,
            r'<meta property="og:title" content=".*?">',
            f'<meta property="og:title" content="{title}">',
        )
        html, _ = korvaa(
            html,
            r'<meta property="og:description" content=".*?">',
            f'<meta property="og:description" content="{kuvaus}">',
        )
        html, _ = korvaa(
            html,
            r'<meta name="twitter:title" content=".*?">',
            f'<meta name="twitter:title" content="{title}">',
        )
        html, _ = korvaa(
            html,
            r'<meta name="twitter:description" content=".*?">',
            f'<meta name="twitter:description" content="{kuvaus}">',
        )

        if '"' in kuvaus:
            raise SystemExit(f"VIRHE: {slug} kuvauksessa lainausmerkki")

        varoitus = ""
        if len(title) > 60:
            varoitus = f"  <-- title {len(title)} mk, katkeaa SERPissä"
        if len(kuvaus) > 160:
            varoitus += f"  <-- kuvaus {len(kuvaus)} mk"

        if html != alkup:
            muutettu += 1
            if not kuiva:
                polku.write_text(html, encoding="utf-8")
            print(f"{'[kuiva] ' if kuiva else ''}{slug}")
            print(f"   T({len(title):>3}) {title}{varoitus}")
            print(f"   D({len(kuvaus):>3}) {kuvaus}")
        else:
            print(f"{slug}: jo ajan tasalla")

    print(f"\n{muutettu}/{len(SIVUT)} sivua {'muuttuisi' if kuiva else 'päivitetty'}.")


if __name__ == "__main__":
    main()
