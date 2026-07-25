# Tuotantoonvienti: kategoriasivut + ilmiön #8 poisto

**Päiväys:** 2026-07-25
**Tila:** valmis ajettavaksi — ei vielä ajettu
**Liittyy:** `kategoriasivut-2026-07-25.md` (suunnittelu ja perustelut)
**Kohde:** https://www.ilmiöt.fi/ (punycode `www.xn--ilmit-mua.fi`)

Tämä on ajolista, ei perusteludokumentti. Miksi-kysymyksiin vastaa suunnitelma.

---

## 1. Mitä viedään

Yksi muutos, kaksi puolta, jotka **eivät voi mennä erikseen**: uudet kategoriasivut ja
ilmiön `tilastoilla-valehtelu` poisto. Poistuvan sivun 301 ja seitsemän sisäistä
linkkiä osoittavat kategoriasivulle, joten kategoriasivun on oltava olemassa ensin.

Mitattu vaikutus (ajettu hiekkalaatikossa 2026-07-25):

| | Määrä |
|---|---:|
| Uusia sivuja | 12 kategoriasivua |
| Muuttuvia ilmiösivuja | 110 |
| Muuttuvia muita tiedostoja | `index.html`, `tietoa.html`, `llms.txt`, `sitemap.xml`, `search-index.js` |
| Siirtyviä | `tilastoilla-valehtelu.html` → `poistetut/` |
| Ilmiöitä ennen → jälkeen | 109 → 108 |
| Sitemap-URLeja ennen → jälkeen | 111 → 122 |

Ilmiösivuilla muuttuu neljä asiaa: `ilmio-tag`, `kortti-nav-laskuri`, `const IDS` ja
liittyvät-korttien numerot. Kahdella (`hajota-hallitse`, `bkt-harha`) myös
`PREV`/`NEXT` ja selausnappi.

---

## 2. Julkaistaanko kaikki 12 kerralla?

**Kyllä.** Tämä poikkeaa suunnitelman kohdasta 6, ja syy on muuttunut tilanne:

- Kohta 6 kirjoitettiin oletuksella "kirjoitetaan 5 esseetä ja mitataan". Nyt kaikki
  12 on kirjoitettu, joten porrastus ei enää säästä työtä.
- Etusivulla lukisi `Lue koko kategoria →` vain osassa kategorioita. Se näyttää
  keskeneräiseltä, ei vaiheistetulta.
- Kategorioiden edellinen/seuraava-navigaatio olettaa yhtenäisen ketjun. Skripti
  osaa hypätä puuttuvien yli, mutta lukijalle "Kategoria 2 / 12" ja kolmen sivun
  ketju on ristiriitainen.

**Mittaus ei kaadu tähän.** Kohdan 8 kysymys on "täydentävätkö kategoriasivut
etusivua vai kannibalisoivatko ne sen", ja siihen vastaa ennen/jälkeen-vertailu koko
sivustolla — ei kategorioiden keskinäinen vertailu.

**Riskinä pidetään kolmea ohutta kategoriaa** (`Kasvun dynamiikka`,
`Pesut ja maineenhallinta`, `Työelämän ilmiöt`, kussakin 3 ilmiötä). Jos ne eivät 8
viikossa kerää omia hakutermejä, ne ovat ensimmäiset `noindex`-ehdokkaat. Tämä on
päätös, joka tehdään datasta, ei etukäteen.

---

## 3. Ennen ajoa

**3.1 Lähtötaso Search Consolesta.** Tämä on ainoa vaihe, jota ei voi tehdä
jälkikäteen. Tallenna talteen (Performance → 3 kk, vertailua varten):

- `index.html`:n hakutermit, näyttökerrat, klikkaukset, keskisijainti
- `tilastoilla-valehtelu.html`:n samat luvut — sivu poistuu, joten tämä on ainoa
  tilaisuus tietää mitä se toi
- koko property-tason näyttökerrat ja klikkaukset

**3.2 Live vastaa localia.** Projektissa on dokumentoitu historia siitä, että live
laahaa jäljessä (`project_deploy_gap`). Varmista lähtötilanne ennen kuin muutat
mitään — muuten et tiedä jälkikäteen, johtuiko ero tästä muutoksesta.

```bash
for f in index.html tietoa.html llms.txt sitemap.xml; do
  echo -n "$f  local=$(md5sum $f | cut -c1-8)  "
  echo "live=$(curl -s https://www.xn--ilmit-mua.fi/$f | md5sum | cut -c1-8)"
done
```

**3.3 Puhdas työpuu.** `git status` tyhjä, tai ainakin tiedät mitä siellä on.

---

## 4. Ajo

Oma haara, jotta diffin voi lukea ja hylätä.

```bash
git checkout -b kategoriasivut
```

**Vaihe 1 — etusivun numerointi ja linkit**

```bash
python3 scripts/lisaa_kategorialinkit.py --kaikki
```

Odotettu tuloste: `index.html: 12 numeroitu, 12 kategorialinkkiä`.

**Vaihe 2 — kategoriasivut, ensimmäinen ajo**

```bash
python3 scripts/build_kategoriat.py
```

Odotettu: 12 riviä, jokaisessa sanamäärä ≥ 300. **Jos jokin varoittaa alle 300
sanasta, pysähdy** — ohut kategoriasivu on suunnitelman kohdan 3 mukaan se ainoa
tapa, jolla hanke epäonnistuu.

> **Tämä ajo tehdään uudelleen vaiheessa 5.** Syy: `poista_ilmio.py` kieltäytyy
> kirjoittamasta, jos 301:n kohdesivua ei ole olemassa, joten kategoriasivut on
> luotava ensin. Mutta ne luetaan `index.html`:stä, joka muuttuu poistossa —
> ensimmäisellä ajolla `Informaatio ja propaganda` saa 14 korttia ja niiden joukossa
> linkin poistuvaan ilmiöön. Ilman toista ajoa sivulle jää kuollut linkki.
> Tämä havaittiin kohdan 5 tarkistuksella; se on siellä juuri tätä varten.

**Vaihe 3 — ilmiön poisto, ensin kuivana**

```bash
python3 scripts/poista_ilmio.py tilastoilla-valehtelu \
    --korvaa kategoria-tilastoilla-valehtelu.html
```

Skripti ei kirjoita mitään ilman `--kirjoita`. Tarkista tulosteesta:

- `109 → 108 ilmiötä`
- `hajota-hallitse` saa `NEXT → bkt-harha`, `bkt-harha` saa `PREV → hajota-hallitse`
- 7 sivua saa `linkki → kategoria-tilastoilla-valehtelu.html`
- `.htaccess: 301 ...`

Kun lista täsmää:

```bash
python3 scripts/poista_ilmio.py tilastoilla-valehtelu \
    --korvaa kategoria-tilastoilla-valehtelu.html --kirjoita
```

**Vaihe 4 — määrät kuntoon**

```bash
python3 scripts/paivita_maarat.py
```

Odotettu: `108 ilmiötä, 12 kategoriaa`. Tämä korjaa `index.html`:n laskurit ja
ItemListin, joista kaikki loput lukevat — siksi se on ennen niitä.

**Vaihe 5 — loput generoidut artefaktit**

Järjestys on sitova. `build_kategoriat` ja `build_liittyvat` lukevat `index.html`:ää,
joka on juuri korjattu; `build_sitemap` lukee kategoriasivujen `dateModified`-arvot,
joten se on niiden jälkeen.

```bash
python3 scripts/build_kategoriat.py     # uudelleen — ks. vaihe 2
python3 scripts/build_liittyvat.py
python3 scripts/build_sitemap.py
python3 scripts/build_search_index.py
```

Odotettu: `Informaatio ja propaganda` on nyt 13 ilmiötä (ei 14),
`sitemap.xml: 122 URLia`, `search-index.js: 108 sivua`.

---

## 5. Tarkistus ennen committia

**Tämä vaihe ei ole muodollisuus.** Se löysi tätä suunnitelmaa kirjoittaessa aidon
järjestysvirheen (kategoriasivun kuollut linkki, ks. vaihe 2).

```bash
# 1. Ei viittauksia poistuneeseen sivuun
grep -rl '"tilastoilla-valehtelu\.html"' --include="*.html" --include="*.txt" \
  --include="*.xml" --include="*.js" . | grep -v poistetut | grep -v luonnokset
# → tyhjä

# 2. Kaikki JSON-LD parsittavaa
python3 - <<'EOF'
import re, json, glob
n = 0
for f in glob.glob('*.html'):
    for s in re.findall(r'<script type="application/ld\+json">(.*?)</script>',
                        open(f, encoding='utf-8').read(), re.S):
        json.loads(s); n += 1
print(f'{n} JSON-LD-lohkoa ok')
EOF

# 3. Sisäiset linkit + numerointi kerralla
python3 - <<'EOF'
import re, os, glob
from collections import Counter
kuolleet, numerot = set(), []
for f in glob.glob('*.html'):
    t = open(f, encoding='utf-8').read()
    for m in re.finditer(r'href="([a-z0-9-]+\.html)"', t):
        if not os.path.exists(m.group(1)):
            kuolleet.add((f, m.group(1)))
    numerot += [int(x) for x in re.findall(r'class="ilmio-tag">Ilmiö (\d+)', t)]
dup = [k for k, v in Counter(numerot).items() if v > 1]
aukot = [i for i in range(1, max(numerot) + 1) if i not in set(numerot)]
print('kuolleet linkit:', sorted(kuolleet) or 'ei yhtään')
print(f'ilmiönumerot: {len(numerot)} kpl, {min(numerot)}-{max(numerot)}, '
      f'duplikaatit={dup or "ei"}, aukot={aukot or "ei"}')
EOF
# → kuolleet: ei yhtään · 108 kpl, 1-108, ei duplikaatteja, ei aukkoja

# 4. Silmämääräisesti
python3 -m http.server 8000   # → localhost:8000/kategoria-vallan-rakenteet.html
```

Selaimessa vielä: nuolinäppäimet ← → vaihtavat kategoriaa, `Lue koko kategoria →`
näkyy etusivulla chippinä, kortit ovat tekstipalstan levyisiä, ja
`kategoria-informaatio-ja-propaganda.html` näyttää **13** korttia.

> Älä käytä numerointitarkistukseen muotoa
> `grep -o 'Ilmiö [0-9]*' *.html | grep -o '[0-9]*$' | uniq | wc -l`. Se antaa 109,
> koska `[0-9]*$` täsmää myös tyhjään merkkijonoon rivin lopussa. Yllä oleva
> Python-versio on yksiselitteinen ja kertoo lisäksi duplikaatit ja aukot.

Selaimessa vielä: nuolinäppäimet ← → vaihtavat kategoriaa, `Lue koko kategoria →`
näkyy etusivulla chippinä, kortit ovat tekstipalstan levyisiä.

---

## 6. Commit ja deploy

```bash
git add -A
git commit          # ks. viestiehdotus alla
git push -u origin kategoriasivut
gh pr create
```

Deploy tavalliseen tapaan **plus yksi käsityö:**

> ### `.htaccess` EI mene deployissa
>
> `.htaccess` on `.gitignore`ssa. `poista_ilmio.py` kirjoittaa sinne 301-ohjauksen,
> mutta se jää paikalliseksi. **Vie tämä palvelimelle käsin**, muuten
> `tilastoilla-valehtelu.html` palauttaa 404:n — sivu, jolla on olemassa olevia
> hakutuloksia ja sisääntulevia linkkejä.
>
> ```
> # Ilmiö siirretty kategoriasivuksi
> RewriteRule ^tilastoilla-valehtelu\.html$ /kategoria-tilastoilla-valehtelu.html [R=301,L]
> ```
>
> Rivi kuuluu kanonisen isännän säännön jälkeen ja turvaotsakkeiden eteen.

`style.css` ei muutu, joten `?v=`-cachebustia **ei tarvitse** bumpata
(`project_css_cachebust`). Kategoriasivujen tyylit ovat sivun omassa
`<style>`-lohkossa.

---

## 7. Deployn jälkeen livenä

```bash
# 301 toimii ja osoittaa oikeaan paikkaan
curl -sI https://www.xn--ilmit-mua.fi/tilastoilla-valehtelu.html | head -3
# → 301 + Location: /kategoria-tilastoilla-valehtelu.html

# Kategoriasivut vastaavat 200:lla
for s in vallan-rakenteet informaatio-ja-propaganda psykologia-ja-kognitio \
         byrokratia-ja-organisaatio projekti-ja-ohjelmistokehitys kasvun-dynamiikka \
         huijaukset-ja-petokset myyntikikat-ja-painostus alustatalous-ja-algoritmit \
         pesut-ja-maineenhallinta tyoelaman-ilmiot tilastoilla-valehtelu; do
  printf '%-32s %s\n' "$s" \
    "$(curl -s -o /dev/null -w '%{http_code}' https://www.xn--ilmit-mua.fi/kategoria-$s.html)"
done

# Live vastaa localia (deploy-gap)
for f in index.html sitemap.xml llms.txt; do
  echo -n "$f  local=$(md5sum $f | cut -c1-8)  "
  echo "live=$(curl -s https://www.xn--ilmit-mua.fi/$f | md5sum | cut -c1-8)"
done
```

Search Consolessa:

1. Lähetä `sitemap.xml` uudelleen.
2. URL Inspection → Request indexing kolmelle isoimmalle kategorialle
   (`myyntikikat-ja-painostus`, `byrokratia-ja-organisaatio`, `psykologia-ja-kognitio`).
   Loput löytyvät sitemapista.
3. Tarkista `tilastoilla-valehtelu.html` → pitäisi näkyä "Page with redirect".

---

## 8. Peruutus

Kaikki paitsi `.htaccess` on gitissä, joten peruutus on suoraviivainen:

```bash
git revert <commit>     # tai: git checkout main && deploy uudelleen
```

Poistettu ilmiösivu on `poistetut/`-kansiossa versionhallinnassa, joten se palautuu
revertillä. **Muista poistaa 301-rivi `.htaccess`ista käsin** — muuten palautettu
sivu ohjautuu edelleen kategoriasivulle, jota ei enää ole.

Peruutuksen kynnys kannattaa pitää matalana ensimmäiset 48 tuntia (rikkinäiset
linkit, 404:t, hajonnut layout) ja korkeana sen jälkeen: hakukoneiden reaktio näkyy
vasta viikoissa, eikä sitä pidä säikähtää ensimmäisestä notkahduksesta.

---

## 9. Mittaus

| Milloin | Mitä |
|---|---|
| +48 h | Coverage: onko 12 uutta URLia indeksoitu tai ainakin löydetty? 404-raportti tyhjä? |
| +2 vk | Onko kategoriasivuille tullut yhtään omaa hakutermiä? |
| +4–8 vk | **Ratkaiseva kysymys:** nousevatko sekä etusivun että kategoriasivujen näyttökerrat (täydentää) vai laskeeko etusivu kategorioiden noustessa (kannibalisoi)? |
| +8 vk | Kolmen ohuen kategorian tilanne: omia hakutermejä vai nolla? |

Jos vastaus on **täydentää**, seuraava askel on ilmiösivujen murupolku osoittamaan
kategoriasivulle fragmentin sijaan (suunnitelman kohta 2.4 ja 10.6).

Jos vastaus on **kannibalisoi**, ongelma on kohdennuksessa: kategoriasivut tähtäävät
samoihin laajoihin termeihin kuin etusivu. Korjaus on kategoriasivujen `title` ja
`h1` aihepiiritermeihin, ei sivujen poisto.

---

## 10. Commit-viestiehdotus

```
Julkaise 12 kategoriasivua ja poista ilmiö #8

Tilastoilla valehtelu ei ollut ilmiö samassa mielessä kuin muut 108: se
listasi viisi tekniikkaa, joista jokainen on nyt oma ilmiönsä (102-109).
Sivu oli yleiskatsaus kategoriaan, joten sen sisältö siirtyi kategoriasivun
johdantoesseeksi ja vanha URL ohjautuu 301:llä sinne.

Samalla sivustolle syntyy puuttunut hakutaso etusivun ja yksittäisen ilmiön
väliin: 12 kategoriasivua, joissa kussakin 395-666 sanaa uniikkia proosaa
ilmiöiden ryhmittelystä ja keskinäisistä kytkennöistä.

- kategoriasivut generoidaan skriptillä (scripts/build_kategoriat.py),
  sisältö kansiosta kategoriat/*.md
- ilmiöt numeroitu uudelleen 1-108 (scripts/poista_ilmio.py)
- kategoriat numeroitu 1-12 etusivulla ja kategoriasivuilla
- sitemap 111 -> 122 URLia, llms.txt saa kategoriasivurivit

Huom: .htaccessin 301-ohjaus on vietävä palvelimelle käsin, koska
.htaccess on .gitignoressa.
```

---

## 11. Avoimet, jotka EIVÄT kuulu tähän vientiin

Nämä on tunnistettu mutta rajattu ulos, jotta vienti pysyy yhtenä muutoksena:

- **Ilmiösivujen murupolku** osoittaa yhä `index.html#kategoria`-fragmenttiin.
  Tehdään vasta jos mittaus kohdassa 9 on positiivinen.
- **Kategoriasivut eivät ole etusivun haussa.** `build_search_index.py` indeksoi vain
  ilmiösivut.
- **Kategorian id** on yhä `tilastoilla-valehtelu-kategoria`. Nimitörmäys on poissa,
  mutta `-kategoria`-päätteen poisto rikkoisi olemassa olevat ankkurit.
- **`fonts.googleapis.com`-riippuvuus.** `style.css` rivi 1 tekee `@import`in Google
  Fontsiin, vaikka fontit ovat itse hostattuja ja `.htaccess`in kommentti väittää
  ettei yksikään sivu viittaa Google Fontsiin. Koskee koko sivustoa, ei vain
  kategoriasivuja — oma muutoksensa (ACTION-PLAN kohta 14).
