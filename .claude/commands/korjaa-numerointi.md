Korjaa ilmiöiden numerointi ilmiot.html-tiedostossa. Käyttö: /korjaa-numerointi

Tarkista nykyinen numerointitilanne ja korjaa kaikki epäjohdonmukaisuudet niin, että ilmiöt numeroidaan 1:stä alkaen siinä järjestyksessä kuin ne esiintyvät HTML:ssä — ei nav-linkkien, vaan varsinaisten `<div class="ilmio">` -divien järjestyksessä.

## Toimintajärjestys

### 1. Selvitä nykytilanne

```bash
cd /home/samu/ilmiot_ja_virhe_paatelmat

# Ilmiö-tagit järjestyksessä (sisältö)
grep -n "ilmio-tag.*Ilmiö" ilmiot.html

# Nav-numerot
grep -E ">[0-9]+\. " ilmiot.html | grep "hak-piste"

# Kokonaismäärä
grep -c 'class="ilmio-tag"' ilmiot.html
```

### 2. Päättele oikea järjestys

Ilmiöt numeroidaan siinä järjestyksessä kuin `<div class="ilmio" id="...">` -elementit esiintyvät HTML:ssä. Nykyinen järjestys on kategorioittain:

1–7: Vallan rakenteet  
8–14: Informaatio ja propaganda  
15–N: Psykologia ja kognitio  
N+1–M: Byrokratia ja organisaatio  
M+1–K: Projekti- ja ohjelmistokehitys  
K+1–L: Kasvun dynamiikka  
L+1–loppu: Huijaukset ja petokset

### 3. Korjaa Python-skriptillä

Käytä **temp-marker-tekniikkaa** — korvaa vanhat numerot ensin väliaikaistunnisteilla (suurimmasta pienimpään), sitten vaihda oikeiksi:

```python
import re

fpath = '/home/samu/ilmiot_ja_virhe_paatelmat/ilmiot.html'
with open(fpath, 'r', encoding='utf-8') as f:
    html = f.read()

# Vaihe 1: Selvitä divien järjestys HTML:ssä
ids_in_order = re.findall(r'<div class="ilmio" id="([^"]+)"', html)
print("Divit järjestyksessä:", ids_in_order)

# Vaihe 2: Selvitä nykyiset numerot jokaiselle id:lle
current_nums = {}
for m in re.finditer(r'<div class="ilmio" id="([^"]+)".*?<div class="ilmio-tag">Ilmiö (\d+)</div>', html, re.DOTALL):
    current_nums[m.group(1)] = int(m.group(2))
print("Nykyiset numerot:", current_nums)

# Vaihe 3: Rakenna mapping (vanha → uusi)
mapping = {}
for new_num, div_id in enumerate(ids_in_order, start=1):
    old_num = current_nums.get(div_id)
    if old_num and old_num != new_num:
        mapping[old_num] = new_num

print("Tarvittavat muutokset (vanha → uusi):", mapping)

if not mapping:
    print("Numerointi on jo oikein!")
else:
    # Vaihe 4: Korvaa temp-merkeillä (suurimmasta pienimpään törmäysten välttämiseksi)
    for old in sorted(mapping.keys(), reverse=True):
        html = html.replace(f'>Ilmiö {old}<', f'>T__{old}__<')
        html = html.replace(f'</span>{old}. ', f'</span>N__{old}__. ')

    # Vaihe 5: Korvaa temp-merkit oikeilla numeroilla
    for old, new in mapping.items():
        html = html.replace(f'>T__{old}__<', f'>Ilmiö {new}<')
        html = html.replace(f'</span>N__{old}__. ', f'</span>{new}. ')

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Korjattu {len(mapping)} numeroa.")
```

### 4. Verifioi

```bash
# Ilmiöt järjestyksessä — ei saa olla aukkoja tai toistoja
grep "ilmio-tag" ilmiot.html | grep "Ilmiö"

# Ei lojuvia temp-merkkejä
grep "T__\|N__" ilmiot.html && echo "VIRHE: temp-merkkejä jäi" || echo "OK"

# Kokonaismäärä säilyi
grep -c 'class="ilmio-tag"' ilmiot.html
```

### 5. Päivitä muistio

Päivitä kategoriajärjestys tiedostoon:
`/home/samu/.claude/projects/-home-samu-ilmiot-ja-virhe-paatelmat/memory/project_ilmiot_numerointi.md`

## Muistettavaa

- Numerot esiintyvät **kahdessa paikassa**: `<div class="ilmio-tag">Ilmiö N</div>` ja `</span>N. Nimi</a>` nav-linkeissä
- Nav-linkit voivat olla eri kategoriaryhmissä kuin divien järjestys — kumpikin päivitetään
- Temp-marker-tekniikka on pakollinen: ilman sitä esim. "19" → "20" saattaa osua myös "19":ään joka jo muutettiin
