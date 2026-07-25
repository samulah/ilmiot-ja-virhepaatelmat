---
kat_id: projekti-ja-ohjelmistokehitys
h1: Projekti- ja ohjelmistokehitys — miksi aikataulut pettävät järjestelmällisesti
otsikko: Projektien lait — 8 syytä siihen, miksi aikataulu pettää
kuvaus: Brooksin laki, Hofstadterin laki, tekninen velka, scope creep. Kahdeksan projektien lainalaisuutta ja se, mikä niitä yhdistää: aliarviointi ei ole huolimattomuutta.
vari: "#5d4037"
paivitetty: 2026-07-25
naapurit:
  - kategoria-byrokratia-ja-organisaatio | Byrokratia ja organisaatio →
  - kategoria-kasvun-dynamiikka | Kasvun dynamiikka →
---

Projektien lainalaisuuksissa on yksi piirre, joka erottaa ne muista tämän sivuston ilmiöistä: ne on nimetty ihmisten mukaan, jotka havaitsivat ne omassa työssään ja kirjoittivat ne ylös hieman vastentahtoisesti. Fred Brooks kirjoitti lakinsa IBM:n System/360-projektin jälkeen, Douglas Hofstadter muotoili omansa rekursiiviseksi vitsiksi, joka osoittautui todeksi.

Yhteinen havainto on epämukava: **aikatauluarvion pettäminen ei ole huolimattomuutta vaan järjestelmällistä.** Se toistuu samoilla ihmisillä, samoilla menetelmillä ja samoissa organisaatioissa vuodesta toiseen, myös silloin kun edellinen ylitys on tuoreessa muistissa. Siksi näitä kutsutaan laeiksi eikä virheiksi.

## Kolme mekanismia

**Aika ei skaalaudu.** [Hofstadterin laki](hofstadterin-laki.html) muotoilee perusongelman rekursiivisesti: kaikki kestää odotettua kauemmin, myös silloin kun otat Hofstadterin lain huomioon. [Yhdeksän-yhdeksän-sääntö](yhdeksanyhdeksan.html) tarkentaa mihin aika katoaa — ensimmäinen 90 % työstä vie 90 % ajasta ja viimeinen 10 % vie loput 90 %. [Brooksin laki](brooksin-laki.html) sulkee viimeisenkin pakotien: myöhässä olevaan projektiin lisätty työvoima myöhästyttää sitä lisää, koska kommunikaatiopolkujen määrä kasvaa neliöllisesti eikä lineaarisesti.

**Laajuus liikkuu.** [Scope creep](scope-creep.html) kasvattaa projektin palasina, joista yksikään ei yksin ansaitse aikataulukeskustelua. [Bikeshedding](bikeshedding.html) on sen huomiotalouden vastine: komitea käyttää tunnin polkupyöräkatoksen väriin, koska siitä kaikki osaavat olla mieltä, ja ydinvoimalan mitoitus menee läpi keskustelutta.

**Velalle kertyy korkoa.** [Tekninen velka](tekninen-velka.html) on kategorian tarkin metafora: oikotie nopeuttaa nyt ja peritään myöhemmin takaisin korkoineen. [Kuolonmarssi](kuolonmarssi.html) on tila, johon kertynyt velka johtaa — projekti, jonka kaikki tietävät epäonnistuvan mutta jota kukaan ei pysty pysäyttämään.

Näiden ulkopuolella on [Conwayn laki](conways-laki.html), joka on kategorian syvin havainto: järjestelmän arkkitehtuuri kopioi väistämättä sen suunnitelleen organisaation rakenteen. Se ei kuvaa virhettä vaan lainalaisuutta — ja siksi se on ainoa näistä, jota voi käyttää suunnittelutyökaluna. Jos haluat toisenlaisen järjestelmän, muuta ensin organisaatio.

## Kahdeksan lainalaisuutta

[[ILMIOT]]

## Miten nämä liittyvät toisiinsa

- **Hofstadterin laki ja yhdeksän-yhdeksän-sääntö kuvaavat samaa ilmiötä eri tarkkuudella.** Edellinen sanoo että arvio pettää, jälkimmäinen sanoo missä kohtaa: viimeistelyssä, integraatiossa ja siinä mitä ei osattu ennakoida.
- **Brooksin laki tekee myöhästymisestä peruuttamatonta.** Kun aikataulu on jo pettänyt, ainoa nopea korjausliike — lisää väkeä — pahentaa tilannetta. Jäljelle jää laajuuden leikkaaminen tai aikataulun siirto.
- **Scope creep ja tekninen velka syöttävät toisiaan.** Uusi ominaisuus rakennetaan olemassa olevan oikotien päälle, mikä tekee seuraavasta ominaisuudesta kalliimman, mikä houkuttelee uuteen oikotiehen.
- **Kuolonmarssi on tekninen velka plus [sunk cost -harha](sunk-cost-harha.html) plus [maalitolppien siirtäminen](maalitolppien-siirtaminen.html).** Velka tekee etenemisen mahdottomaksi, uponneet kustannukset estävät lopettamisen ja kriteerien siirtäminen tekee jatkamisesta muodollisesti onnistunutta.
- **Bikeshedding on [Parkinsonin lain](parkinsonin-laki.html) vähäpätöisyyslaki.** Sama havainto: aika täyttyy sillä, mikä on helposti käsiteltävissä, ei sillä mikä on tärkeää.
- **Conwayn laki selittää, miksi arkkitehtuurikorjaukset epäonnistuvat.** Jos rajapinta seuraa tiimirajaa, rajapinnan siirtäminen edellyttää tiimirajan siirtämistä.

## Mitä näistä seuraa lukijalle

1. **Älä hyväksy ”melkein valmista” tilatietona.** Kysy sen sijaan, mitä on vielä integroimatta, testaamatta ja siirtämättä tuotantoon. Yhdeksän-yhdeksän-sääntö sanoo, että juuri se työ vie loput puolet ajasta.
2. **Älä lisää väkeä myöhässä olevaan projektiin.** Leikkaa laajuutta tai siirrä päivämäärää — kolmatta vaihtoehtoa ei ole.
3. **Tee velasta näkyvää.** Kirjaamaton oikotie ei ole päätös vaan unohdus.
4. **Katso agendaa väristä.** Jos kokous käyttää eniten aikaa halvimpaan päätökseen, kalliit menivät jo läpi.

:::html
<div class="infolaatikko">
<h2 class="laatikko-otsikko">Yhteinen nimittäjä:</h2> ihminen aliarvioi monimutkaisuuden järjestelmällisesti, ja järjestelmällistä virhettä ei korjaa yrittämällä kovemmin. Sen korjaa vain menetelmä — pienemmät erät, kirjatut oletukset ja aiempien arvioiden toteutuma vertailukohtana.
</div>
:::

[[NAAPURIT]]
