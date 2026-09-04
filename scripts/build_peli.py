#!/usr/bin/env python3
"""
Kääntää Vedätys-pelin pankin: pelidata/*.json -> data/peli-pankki.js

Tekee kolme asiaa:
  1. VALIDOI pankin (ks. tarkista_pankki) — kaatuu jos sisältö rikkoo sääntöjä.
  2. KOKOAA päivän erät käännösaikana, ei ajonaikana. Syy: koostumussäännöt
     ovat tällöin tarkistettavissa eivätkä riipu selaimen satunnaisuudesta,
     ja kaikki pelaajat saavat varmasti saman erän samana päivänä — ilman sitä
     tulosten vertailu ja jakaminen menettää merkityksensä.
  3. Kirjoittaa window.VEDATYS_PANKKI -datatiedoston.

Deterministinen: sama sisältö -> byte-identtinen tulos. Aja kahdesti ja diffaa.

    python3 scripts/build_peli.py --tarkista   # vain validointi, ei kirjoita
    python3 scripts/build_peli.py              # kirjoittaa data/peli-pankki.js
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
PELIDATA = ROOT / "pelidata"
ULOS = ROOT / "data" / "peli-pankki.js"

EPOKKI = "2026-08-23"          # Vedätys #1. Tämä on ainoa paikka jossa epokki
                               # määritellään: peli.html lukee sen datasta
                               # (P.epokki), joten sitä ei kovakoodata sivulle.
ERIA = 30                      # vaiheen 1 erämäärä
KOHTIA_ERASSA = 5
REHELLISIA_MIN = 1             # per erä
REHELLISIA_MAX = 2             # per erä
KONTEKSTEJA_MIN = 3            # eri kontekstia per erä
KOHTIA_PER_ILMIO_MIN = 4
REHELLISTEN_OSUUS_MIN = 0.25   # koko pankista

# Käyttöliittymän omat ansat: peli tekee tempun pelaajalle ja paljastaa sen.
# Rajaus on tarkoituksellinen (ks. CLAUDE.md): peli manipuloi pelaajaa vain
# opetuksessa, ei koskaan retentiossa.
ANSAT = [
    {"tyyppi": "ajastin", "ilmio": "painostusclose",
     "nimi": "Tekaistu ajastin",
     "selitys": "Kello ei tehnyt mitään. Se ei ollut kytketty mihinkään eikä vastausaikaa ollut rajattu. Kiireen tuntu on tekniikka: sillä ostetaan päätös ennen kuin ehdit ajatella."},
    {"tyyppi": "todiste", "ilmio": "sosiaalinen-todiste",
     "nimi": "Keksitty sosiaalinen todiste",
     "selitys": "Prosenttiluku oli keksitty. Emme mittaa mitään emmekä voisikaan — tämä sivu ei lähetä mitään minnekään. Tarkistamaton luku toimii silti, ja juuri se on sen tarkoitus."},
    {"tyyppi": "oletus", "ilmio": "oletusasetusansa",
     "nimi": "Esivalittu oletus",
     "selitys": "Yksi vaihtoehto oli valmiiksi valittuna. Oletus on vahvin yksittäinen käyttöliittymän keino: useimmat eivät muuta sitä, ja siksi sen valinta on se varsinainen päätös."},
    {"tyyppi": "syyllistys", "ilmio": "confirmshaming",
     "nimi": "Syyllistävä nappi",
     "selitys": "Ohitusnappi nolasi sinut valinnastasi. Confirmshaming ei väitä mitään — se vain tekee toisesta vaihtoehdosta noloa."},
]
ANSA_VALI = 3   # joka kolmas erä sisältää ansan


def kortit() -> dict:
    """slug -> {nro, nimi, kuvaus, vari} etusivun a.hub-kortti-elementeistä."""
    s = (ROOT / "index.html").read_text(encoding="utf-8")
    ulos = {}
    for href, vari, body in re.findall(
        r'<a\s+href="([^"]+)"\s+class="hub-kortti"\s+style="--c:([^"]+)"\s*>(.*?)</a>',
        s, re.S,
    ):
        def kentta(luokka):
            m = re.search(r'class="%s">(.*?)</span>' % luokka, body, re.S)
            return html.unescape(m.group(1)).strip() if m else ""
        ulos[href[:-5]] = {"nro": int(kentta("hub-numero")),
                           "nimi": kentta("hub-nimi"),
                           "kuvaus": kentta("hub-kuvaus"),
                           "vari": vari}
    return ulos


def lue_pankki(K: dict) -> list:
    """Lukee pelidata/*.json -> yksi litteä lista kohtia, vakaassa järjestyksessä."""
    kohdat = []
    for polku in sorted(PELIDATA.glob("*.json")):
        d = json.loads(polku.read_text(encoding="utf-8"))
        oletuslaji = d.get("laji", "taktiikka")
        for k in d["kohdat"]:
            k = dict(k)
            k.setdefault("laji", oletuslaji)
            k["ilmio"] = k.get("ilmio", d.get("ilmio"))
            k["_tiedosto"] = polku.name
            kohdat.append(k)
    kohdat.sort(key=lambda k: k["id"])
    return kohdat


def virhe(lista, viesti):
    lista.append(viesti)


def tarkista_pankki(kohdat: list, K: dict) -> list:
    """Palauttaa listan virheitä. Tyhjä lista = pankki kelpaa."""
    v = []
    nahdyt_idt, nahdyt_tekstit = set(), {}
    per_ilmio = {}

    for k in kohdat:
        tunnus = k.get("id", "<ei id:tä>")
        if tunnus in nahdyt_idt:
            virhe(v, f"{tunnus}: id esiintyy kahdesti")
        nahdyt_idt.add(tunnus)

        teksti = k.get("teksti", "").strip()
        if not teksti:
            virhe(v, f"{tunnus}: teksti puuttuu")
        avain = re.sub(r"\s+", " ", teksti.lower())
        if avain in nahdyt_tekstit:
            virhe(v, f"{tunnus}: sama teksti kuin {nahdyt_tekstit[avain]}")
        nahdyt_tekstit[avain] = tunnus

        if k["laji"] not in ("taktiikka", "vinouma", "rehellinen"):
            virhe(v, f"{tunnus}: tuntematon laji {k['laji']!r}")

        for kentta in ("mita", "miksi"):
            if not k.get("paljastus", {}).get(kentta, "").strip():
                virhe(v, f"{tunnus}: paljastus.{kentta} puuttuu")
        if "sanot" not in k.get("paljastus", {}):
            virhe(v, f"{tunnus}: paljastus.sanot puuttuu")

        if k["laji"] == "rehellinen":
            if k.get("ilmio"):
                virhe(v, f"{tunnus}: rehellisellä kohdalla ei saa olla ilmiötä")
            if k.get("harhauttajat"):
                virhe(v, f"{tunnus}: rehellisellä kohdalla ei saa olla harhauttajia")
            if k["paljastus"]["sanot"].strip():
                virhe(v, f"{tunnus}: rehellisellä kohdalla sanot on tyhjä")
        else:
            slug = k.get("ilmio")
            if slug not in K:
                virhe(v, f"{tunnus}: ilmiö {slug!r} ei ole etusivun korttilistalla")
                continue
            if not (ROOT / f"{slug}.html").exists():
                virhe(v, f"{tunnus}: {slug}.html puuttuu")
            per_ilmio.setdefault(slug, []).append(tunnus)
            h = k.get("harhauttajat", [])
            if len(h) != 2:
                virhe(v, f"{tunnus}: harhauttajia on {len(h)}, pitää olla 2")
            for x in h:
                if x not in K:
                    virhe(v, f"{tunnus}: harhauttaja {x!r} ei ole korttilistalla")
                if x == slug:
                    virhe(v, f"{tunnus}: harhauttaja on sama kuin oikea vastaus")
            if len(set(h)) != len(h):
                virhe(v, f"{tunnus}: sama harhauttaja kahdesti")
            if not k.get("konteksti") or not k.get("kanava"):
                virhe(v, f"{tunnus}: konteksti tai kanava puuttuu")

    for slug, idt in sorted(per_ilmio.items()):
        if len(idt) < KOHTIA_PER_ILMIO_MIN:
            virhe(v, f"{slug}: vain {len(idt)} kohtaa, vähintään {KOHTIA_PER_ILMIO_MIN}")

    rehellisia = sum(1 for k in kohdat if k["laji"] == "rehellinen")
    osuus = rehellisia / len(kohdat) if kohdat else 0
    if osuus < REHELLISTEN_OSUUS_MIN:
        virhe(v, f"rehellisiä {rehellisia}/{len(kohdat)} = {osuus:.0%}, "
                 f"vähintään {REHELLISTEN_OSUUS_MIN:.0%}")
    return v


def kokoa_erat(kohdat: list) -> list:
    """
    Jakaa kohdat 30 erään deterministisesti.

    Taktiikat jaetaan ahneella "eniten jäljellä ensin" -säännöllä, joka on sama
    algoritmi kuin tehtävien vuorottelussa jäähdytysajalla: se estää saman
    ilmiön osumisen kahdesti samaan erään ilman perääntymistä. Rehelliset
    kohdat täyttävät loput paikat.
    """
    taktiikat = [k for k in kohdat if k["laji"] != "rehellinen"]
    rehelliset = [k for k in kohdat if k["laji"] == "rehellinen"]

    # Montako rehellistä mihinkin erään: mahdollisimman tasan, 1-2 per erä.
    if not (ERIA * REHELLISIA_MIN <= len(rehelliset) <= ERIA * REHELLISIA_MAX):
        raise SystemExit(
            f"VIRHE: rehellisiä {len(rehelliset)} kpl — {ERIA} erään mahtuu "
            f"{ERIA * REHELLISIA_MIN}–{ERIA * REHELLISIA_MAX}")
    kakkosia = len(rehelliset) - ERIA * REHELLISIA_MIN
    reh_maara = [REHELLISIA_MIN + (1 if i < kakkosia else 0) for i in range(ERIA)]
    tak_maara = [KOHTIA_ERASSA - n for n in reh_maara]
    if sum(tak_maara) != len(taktiikat):
        raise SystemExit(
            f"VIRHE: taktiikkapaikkoja {sum(tak_maara)} mutta kohtia "
            f"{len(taktiikat)} — säädä eräkokoa tai pankkia")

    ilmioittain = {}
    for k in taktiikat:
        ilmioittain.setdefault(k["ilmio"], []).append(k)
    for lista in ilmioittain.values():
        lista.sort(key=lambda k: k["id"])

    erat = [[] for _ in range(ERIA)]
    kaytetyt_ilmiot = [set() for _ in range(ERIA)]
    while any(ilmioittain.values()):
        # Eniten jäljellä oleva ilmiö ensin; tasapelin ratkaisee slug.
        slug = max(sorted(ilmioittain), key=lambda s: (len(ilmioittain[s]), s))
        if not ilmioittain[slug]:
            del ilmioittain[slug]
            continue
        kohta = ilmioittain[slug].pop(0)
        if not ilmioittain[slug]:
            del ilmioittain[slug]
        # Vähiten täytetty erä, johon tämä ilmiö ei vielä osu.
        ehdokkaat = [i for i in range(ERIA)
                     if len(erat[i]) < tak_maara[i] and slug not in kaytetyt_ilmiot[i]]
        if not ehdokkaat:
            raise SystemExit(f"VIRHE: {kohta['id']} ei mahdu mihinkään erään")
        # Tasapaino ratkaisee ensin (muuten eräkoot menevät rikki), sen jälkeen
        # suositaan erää jossa tätä kontekstia ei vielä ole.
        kt = kohta.get("konteksti")
        i = min(ehdokkaat, key=lambda i: (
            len(erat[i]),
            1 if kt in {x.get("konteksti") for x in erat[i]} else 0,
            i))
        erat[i].append(kohta)
        kaytetyt_ilmiot[i].add(slug)

    # Rehelliset: erään, jossa on vähiten konteksteja edustettuna, jotta
    # kontekstivaatimus täyttyy ilman erillistä korjauskierrosta.
    rehelliset.sort(key=lambda k: k["id"])
    paikkoja = list(reh_maara)
    for kohta in rehelliset:
        kt = kohta.get("konteksti")
        ehdokkaat = [i for i in range(ERIA) if paikkoja[i] > 0]
        i = min(ehdokkaat, key=lambda i: (
            1 if kt in {x.get("konteksti") for x in erat[i]} else 0,
            len({x.get("konteksti") for x in erat[i]}),
            i))
        erat[i].append(kohta)
        paikkoja[i] -= 1

    korjaa_kontekstit(erat)
    for era in erat:
        era.sort(key=lambda k: k["id"])
    return erat


def korjaa_kontekstit(erat: list) -> None:
    """
    Vaihtaa kohtia erien välillä, kunnes jokaisessa erässä on tarpeeksi eri
    konteksteja. Deterministinen: erät ja ehdokkaat käydään läpi indeksijärjestyksessä
    ja ensimmäinen kelvollinen vaihto otetaan.

    Vaihto tehdään vain saman lajin kohtien välillä, jotta rehellisten määrä
    erässä säilyy — se on pelin tärkein koostumussääntö eikä sitä saa rikkoa
    kosmeettisen monipuolisuuden vuoksi.
    """
    def kontekstit(era):
        return {k.get("konteksti") for k in era}

    for _ in range(200):                       # kova katto: ei ikilooppia
        vajaat = [i for i, e in enumerate(erat)
                  if len(kontekstit(e)) < KONTEKSTEJA_MIN]
        if not vajaat:
            return
        vaihdettu = False
        for i in vajaat:
            for a_idx, a in enumerate(erat[i]):
                for j in range(len(erat)):
                    if j == i:
                        continue
                    for b_idx, b in enumerate(erat[j]):
                        if a["laji"] != b["laji"]:
                            continue
                        if a.get("konteksti") == b.get("konteksti"):
                            continue
                        # Ilmiö ei saa esiintyä kahdesti kummassakaan erässä.
                        muut_i = [x["ilmio"] for n, x in enumerate(erat[i])
                                  if n != a_idx and x["ilmio"]]
                        muut_j = [x["ilmio"] for n, x in enumerate(erat[j])
                                  if n != b_idx and x["ilmio"]]
                        if b["ilmio"] and b["ilmio"] in muut_i:
                            continue
                        if a["ilmio"] and a["ilmio"] in muut_j:
                            continue
                        uusi_i = erat[i][:a_idx] + [b] + erat[i][a_idx + 1:]
                        uusi_j = erat[j][:b_idx] + [a] + erat[j][b_idx + 1:]
                        # Vaihto kelpaa vain jos i paranee eikä j huonone
                        # kynnyksen alle.
                        if len(kontekstit(uusi_i)) <= len(kontekstit(erat[i])):
                            continue
                        if len(kontekstit(uusi_j)) < min(KONTEKSTEJA_MIN,
                                                         len(kontekstit(erat[j]))):
                            continue
                        erat[i], erat[j] = uusi_i, uusi_j
                        vaihdettu = True
                        break
                    if vaihdettu:
                        break
                if vaihdettu:
                    break
            if vaihdettu:
                break
        if not vaihdettu:
            return                              # tarkista_erat raportoi jäljelle jääneet
    return


def tarkista_erat(erat: list) -> list:
    v = []
    for i, era in enumerate(erat, 1):
        if len(era) != KOHTIA_ERASSA:
            virhe(v, f"erä {i}: {len(era)} kohtaa, pitää olla {KOHTIA_ERASSA}")
        reh = sum(1 for k in era if k["laji"] == "rehellinen")
        if not (REHELLISIA_MIN <= reh <= REHELLISIA_MAX):
            virhe(v, f"erä {i}: rehellisiä {reh}, sallittu {REHELLISIA_MIN}–{REHELLISIA_MAX}")
        ilmiot = [k["ilmio"] for k in era if k["ilmio"]]
        if len(set(ilmiot)) != len(ilmiot):
            virhe(v, f"erä {i}: sama ilmiö kahdesti")
        kontekstit = {k.get("konteksti") for k in era}
        if len(kontekstit) < KONTEKSTEJA_MIN:
            virhe(v, f"erä {i}: vain {len(kontekstit)} eri kontekstia, "
                     f"vähintään {KONTEKSTEJA_MIN}")
    kaikki = [k["id"] for era in erat for k in era]
    if len(set(kaikki)) != len(kaikki):
        virhe(v, "sama kohta esiintyy kahdessa erässä")
    return v


def kirjoita(kohdat: list, erat: list, K: dict) -> str:
    # Vain ne ilmiöt, joihin pankki viittaa — pidetään tiedosto pienenä.
    tarvitut = set()
    for k in kohdat:
        if k["ilmio"]:
            tarvitut.add(k["ilmio"])
            tarvitut.update(k.get("harhauttajat", []))
    for a in ANSAT:
        if a["ilmio"] in K:
            tarvitut.add(a["ilmio"])

    ilmiot = {s: {"n": K[s]["nimi"], "v": K[s]["vari"], "k": K[s]["kuvaus"]}
              for s in sorted(tarvitut)}

    indeksi = {}
    ulos_kohdat = []
    for k in kohdat:
        indeksi[k["id"]] = len(ulos_kohdat)
        rivi = {"id": k["id"], "t": k["teksti"], "l": k["laji"],
                "kn": k.get("kanava", ""), "kt": k.get("konteksti", ""),
                "p": [k["paljastus"]["mita"], k["paljastus"]["miksi"],
                      k["paljastus"]["sanot"]]}
        if k["ilmio"]:
            rivi["i"] = k["ilmio"]
            rivi["h"] = k["harhauttajat"]
        ulos_kohdat.append(rivi)

    ulos_erat = []
    for n, era in enumerate(erat):
        rivi = {"k": [indeksi[k["id"]] for k in era]}
        if n % ANSA_VALI == ANSA_VALI - 1:
            a = ANSAT[(n // ANSA_VALI) % len(ANSAT)]
            # Ansa osuu erän keskivaiheille, ei koskaan ensimmäiseen kierrokseen:
            # pelaajan on ensin opittava mitä peli tekee, ennen kuin peli tekee sen.
            rivi["a"] = {"t": a["tyyppi"], "r": 1 + (n // ANSA_VALI) % 3,
                         "n": a["nimi"], "s": a["selitys"], "i": a["ilmio"]}
        ulos_erat.append(rivi)

    data = {"versio": 1, "epokki": EPOKKI, "ilmiot": ilmiot,
            "kohdat": ulos_kohdat, "erat": ulos_erat}
    return ("window.VEDATYS_PANKKI=" +
            json.dumps(data, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")) + ";\n")


def main() -> None:
    vain_tarkista = "--tarkista" in sys.argv
    K = kortit()
    kohdat = lue_pankki(K)

    virheet = tarkista_pankki(kohdat, K)
    if virheet:
        print(f"PANKKI EI KELPAA — {len(virheet)} virhettä:")
        for x in virheet:
            print("  ·", x)
        sys.exit(1)

    erat = kokoa_erat(kohdat)
    virheet = tarkista_erat(erat)
    if virheet:
        print(f"ERÄT EIVÄT KELPAA — {len(virheet)} virhettä:")
        for x in virheet:
            print("  ·", x)
        sys.exit(1)

    taktiikat = sum(1 for k in kohdat if k["laji"] == "taktiikka")
    vinoumat = sum(1 for k in kohdat if k["laji"] == "vinouma")
    rehelliset = sum(1 for k in kohdat if k["laji"] == "rehellinen")
    ilmioita = len({k["ilmio"] for k in kohdat if k["ilmio"]})
    ansoja = sum(1 for n in range(len(erat)) if n % ANSA_VALI == ANSA_VALI - 1)
    print(f"Pankki kelpaa: {len(kohdat)} kohtaa "
          f"({taktiikat} taktiikkaa, {vinoumat} vinoumaa, "
          f"{rehelliset} rehellistä = {rehelliset/len(kohdat):.0%}), "
          f"{ilmioita} ilmiötä")
    print(f"Erät kelpaavat: {len(erat)} erää × {KOHTIA_ERASSA} kohtaa, "
          f"{ansoja} ansaa")

    if vain_tarkista:
        print("(--tarkista: ei kirjoitettu)")
        return

    ULOS.parent.mkdir(parents=True, exist_ok=True)
    ULOS.write_text(kirjoita(kohdat, erat, K), encoding="utf-8")
    koko = ULOS.stat().st_size
    print(f"→ {ULOS.relative_to(ROOT)}  ({koko:,} tavua)".replace(",", " "))


if __name__ == "__main__":
    main()
