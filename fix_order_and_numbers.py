#!/usr/bin/env python3
"""
Korjaa ilmiot.html:
1. Siirtää divit oikeaan järjestykseen
2. Renumeroi kaikki 55 ilmiötä
"""
import re

fpath = '/home/samu/ilmiot_ja_virhe_paatelmat/ilmiot.html'
with open(fpath, 'r', encoding='utf-8') as f:
    html = f.read()

# ---------------------------------------------------------------------------
# Vaihe 1: Poimii kaikki siirrettävät divit tiedoston lopusta
# ---------------------------------------------------------------------------
# Siirrettävät divit (tiedoston lopussa väärässä paikassa):
# - gaslighting, maalitolppien-siirtaminen, argumenttitulva, sunk-cost-harha
#   → sijoitetaan omenoita-appelsiineja:n jälkeen, ennen simple-sabotage:a
# - blame-game
#   → sijoitetaan omenoita-appelsiineja:n jälkeen, kaikkein ensimmäiseksi
# - strateginen-osaamattomuus, fofo, sivustakatsojan-efekti
#   → sijoitetaan portinvartija-kulttuuri:n jälkeen, ennen brooksin-laki:a

def extract_div(html_content, div_id):
    """Poimii yhden ilmio-divin (kommenttirivi + div + sisältö sis. </div>)."""
    # Etsi kommenttirivi + div
    sep = '  <!-- ============================================================ -->'
    div_start = f'  <div class="ilmio" id="{div_id}">'

    # Löydä alkukohta (kommenttirivi ennen diviä)
    idx_sep = html_content.find(sep + '\n' + div_start)
    if idx_sep == -1:
        raise ValueError(f"Ei löydy: {div_id}")

    # Löydä loppukohta: seuraava kommenttirivi tai </main>
    search_from = idx_sep + len(sep)
    next_sep = html_content.find('\n' + sep, search_from)
    next_main = html_content.find('\n    </main>', search_from)

    if next_sep == -1:
        end_idx = next_main  # loppuu ennen </main>
    elif next_main == -1:
        end_idx = next_sep
    else:
        end_idx = min(next_sep, next_main)

    div_block = html_content[idx_sep:end_idx]
    return div_block

# Poimi kaikki siirrettävät divit
ids_to_move = [
    'blame-game',
    'gaslighting',
    'maalitolppien-siirtaminen',
    'argumenttitulva',
    'sunk-cost-harha',
    'strateginen-osaamattomuus',
    'fofo',
    'sivustakatsojan-efekti',
]

extracted = {}
for div_id in ids_to_move:
    extracted[div_id] = extract_div(html, div_id)
    print(f"Poimittu: {div_id} ({len(extracted[div_id])} merkkiä)")

# Poista divit nykyisistä sijainneistaan
sep = '  <!-- ============================================================ -->'

for div_id in ids_to_move:
    block = extracted[div_id]
    # Poista blokki + sitä edeltävä rivinvaihto (tai alkuosa jos ensimmäinen)
    html = html.replace('\n' + block, '', 1)
    if block in html:
        # Varastrategia: poista ilman eturivinvaihtoa
        html = html.replace(block, '', 1)
    print(f"Poistettu sijaintinsa: {div_id}")

# Varmista ettei tiedostossa enää ole näitä divejä väärässä paikassa
for div_id in ids_to_move:
    count = html.count(f'id="{div_id}"')
    # CSS-tyyleissä on #div_id, joten haetaan nimenomaan id="-attribuutti"
    print(f"  {div_id}: {count} esiintymää (pitää olla 1 CSS:stä, 0 div-attribuutteja)")

# ---------------------------------------------------------------------------
# Vaihe 2: Lisää divit oikeisiin kohtiin
# ---------------------------------------------------------------------------

# Ryhmä A: blame-game, gaslighting, maalitolppien-siirtaminen, argumenttitulva, sunk-cost-harha
# → lisätään ENNEN simple-sabotage:a (omenoita-appelsiineja:n jälkeen)
# Käytetään ankurina: sep + '\n  <div class="ilmio" id="simple-sabotage">'

anchor_before_simple = sep + '\n  <div class="ilmio" id="simple-sabotage">'

group_a_ids = ['blame-game', 'gaslighting', 'maalitolppien-siirtaminen', 'argumenttitulva', 'sunk-cost-harha']
group_a_blocks = '\n'.join(extracted[d] for d in group_a_ids) + '\n'

new_anchor_a = group_a_blocks + anchor_before_simple

if anchor_before_simple not in html:
    raise ValueError("Ankuri simple-sabotage ei löydy!")
html = html.replace(anchor_before_simple, new_anchor_a, 1)
print("Lisätty ryhmä A ennen simple-sabotage:a")

# Ryhmä B: strateginen-osaamattomuus, fofo, sivustakatsojan-efekti
# → lisätään ENNEN brooksin-laki:a (portinvartija-kulttuuri:n jälkeen)

anchor_before_brooksin = sep + '\n  <div class="ilmio" id="brooksin-laki">'

group_b_ids = ['strateginen-osaamattomuus', 'fofo', 'sivustakatsojan-efekti']
group_b_blocks = '\n'.join(extracted[d] for d in group_b_ids) + '\n'

new_anchor_b = group_b_blocks + anchor_before_brooksin

if anchor_before_brooksin not in html:
    raise ValueError("Ankuri brooksin-laki ei löydy!")
html = html.replace(anchor_before_brooksin, new_anchor_b, 1)
print("Lisätty ryhmä B ennen brooksin-laki:a")

# ---------------------------------------------------------------------------
# Vaihe 3: Tarkista järjestys
# ---------------------------------------------------------------------------
ids_in_order = re.findall(r'<div class="ilmio" id="([^"]+)"', html)
print(f"\nDivit järjestyksessä ({len(ids_in_order)} kpl):")
for i, div_id in enumerate(ids_in_order, 1):
    print(f"  {i:2d}. {div_id}")

# Vaadittu järjestys
required_order = [
    'paskuuttaminen', 'starve-the-beast', 'overton-ikkuna', 'saantelijan-kaappaus',
    'rautainen-laki', 'valta-suojelee-valtaa', 'hajota-hallitse',
    'tilastoilla-valehtelu', 'bkt-harha', 'astroturf', 'firehose-of-falsehood',
    'manufactured-consent', 'betteridgen-laki', 'inokulointiteoria',
    'backfire-effect', 'darvo', 'halo-efekti', 'konsensus-fetissi',
    'omenoita-appelsiineja',
    'blame-game', 'gaslighting', 'maalitolppien-siirtaminen', 'argumenttitulva', 'sunk-cost-harha',
    'simple-sabotage', 'kafka-ilmio', 'catch-22', 'goodhartin-laki', 'hippo-efekti',
    'performatiivinen-lasnaolo', 'rituaalinen-raportointi', 'initiointirituaalit',
    'portinvartija-kulttuuri',
    'strateginen-osaamattomuus', 'fofo', 'sivustakatsojan-efekti',
    'brooksin-laki', 'yhdeksanyhdeksan', 'hofstadterin-laki', 'kuolonmarssi',
    'tekninen-velka', 'conways-laki', 'bikeshedding', 'scope-creep',
    'korkoa-korolle', 'negatiivinen-korkoa', 'korkokierre',
    'honeypot-huijaus', 'bait-and-switch', 'kaarmeoljy', 'ponzi-pyramidi',
    'pump-and-dump', 'pig-butchering', 'ennakkomaksuhuijaus', 'badger-game',
]

if ids_in_order != required_order:
    print("\nVIRHE: Järjestys ei täsmää!")
    for i, (got, want) in enumerate(zip(ids_in_order, required_order), 1):
        if got != want:
            print(f"  Kohta {i}: on '{got}', pitäisi olla '{want}'")
    if len(ids_in_order) != len(required_order):
        print(f"  Määrä: {len(ids_in_order)} vs vaadittu {len(required_order)}")
else:
    print("\nJärjestys OK!")

# ---------------------------------------------------------------------------
# Vaihe 4: Renumerointi temp-marker-tekniikalla
# ---------------------------------------------------------------------------

# Nykyiset numerot (ennen muutosta):
# 1-19 pysyvät paikoillaan → nämäkin kirjoitetaan uudelleen varmuuden vuoksi
# 20-47: simple-sabotage...badger-game (näiden numerot pysyvät samoina paitsi
#   shiftaantuvat koska uudet divit lisättiin väliin)
# Tiedoston lopussa olivat: gaslighting=49, maalitolppien=50, argumenttitulva=51,
#   sunk-cost=52, strateginen=53, fofo=54, sivustakatsojan=55, blame-game=48

# Nykyinen numerointi (ennen renumerointia):
current_numbers = {
    'paskuuttaminen': 1, 'starve-the-beast': 2, 'overton-ikkuna': 3,
    'saantelijan-kaappaus': 4, 'rautainen-laki': 5, 'valta-suojelee-valtaa': 6,
    'hajota-hallitse': 7, 'tilastoilla-valehtelu': 8, 'bkt-harha': 9,
    'astroturf': 10, 'firehose-of-falsehood': 11, 'manufactured-consent': 12,
    'betteridgen-laki': 13, 'inokulointiteoria': 14, 'backfire-effect': 15,
    'darvo': 16, 'halo-efekti': 17, 'konsensus-fetissi': 18,
    'omenoita-appelsiineja': 19,
    'blame-game': 48, 'gaslighting': 49, 'maalitolppien-siirtaminen': 50,
    'argumenttitulva': 51, 'sunk-cost-harha': 52,
    'simple-sabotage': 20, 'kafka-ilmio': 21, 'catch-22': 22,
    'goodhartin-laki': 23, 'hippo-efekti': 24, 'performatiivinen-lasnaolo': 25,
    'rituaalinen-raportointi': 26, 'initiointirituaalit': 27,
    'portinvartija-kulttuuri': 28,
    'strateginen-osaamattomuus': 53, 'fofo': 54, 'sivustakatsojan-efekti': 55,
    'brooksin-laki': 29, 'yhdeksanyhdeksan': 30, 'hofstadterin-laki': 31,
    'kuolonmarssi': 32, 'tekninen-velka': 33, 'conways-laki': 34,
    'bikeshedding': 35, 'scope-creep': 36,
    'korkoa-korolle': 37, 'negatiivinen-korkoa': 38, 'korkokierre': 39,
    'honeypot-huijaus': 40, 'bait-and-switch': 41, 'kaarmeoljy': 42,
    'ponzi-pyramidi': 43, 'pump-and-dump': 44, 'pig-butchering': 45,
    'ennakkomaksuhuijaus': 46, 'badger-game': 47,
}

# Uusi numerointi (järjestysluku = div:n sijainti listassa)
new_numbers = {div_id: i for i, div_id in enumerate(required_order, 1)}

print("\nNumeroinnin muutokset:")
for div_id in required_order:
    old = current_numbers[div_id]
    new = new_numbers[div_id]
    if old != new:
        print(f"  {div_id}: {old} → {new}")

# Kaikki vanhat numerot joita esiintyy
all_old_nums = sorted(set(current_numbers.values()), reverse=True)

# Vaihe 4a: Korvaa vanhat → temp-tagit (suurimmasta pienimpään)
for n in all_old_nums:
    html = html.replace(f'>Ilmiö {n}<', f'>T__{n}__<')
    html = html.replace(f'</span>{n}. ', f'</span>N__{n}__. ')

print("\nTemp-tagit asetettu.")

# Vaihe 4b: Rakenna käänteinen kartta: vanha numero → uusi numero
old_to_new = {current_numbers[div_id]: new_numbers[div_id] for div_id in required_order}

# Korvaa temp-tagit lopullisilla numeroilla
for old_n, new_n in old_to_new.items():
    html = html.replace(f'>T__{old_n}__<', f'>Ilmiö {new_n}<')
    html = html.replace(f'</span>N__{old_n}__. ', f'</span>{new_n}. ')

print("Lopulliset numerot asetettu.")

# ---------------------------------------------------------------------------
# Vaihe 5: Tallenna
# ---------------------------------------------------------------------------
with open(fpath, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nTiedosto tallennettu: {fpath}")
print("Valmis.")
