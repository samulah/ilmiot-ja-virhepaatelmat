# Muutosloki — Ilmiöitä (www.ilmiöt.fi)

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
