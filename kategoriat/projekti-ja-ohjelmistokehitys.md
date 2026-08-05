---
kat_id: projekti-ja-ohjelmistokehitys
h1: Projekti- ja ohjelmistokehitys — miksi aikataulut pettävät järjestelmällisesti
otsikko: Projektien lait — 12 syytä siihen, miksi aikataulu ja budjetti pettävät
kuvaus: Brooksin laki, tekninen velka, strateginen aliarviointi. Kaksitoista projektien lainalaisuutta, joissa aliarviointi ei ole huolimattomuutta vaan tapa.
vari: "#5d4037"
paivitetty: 2026-08-05
naapurit:
  - kategoria-byrokratia-ja-organisaatio | Byrokratia ja organisaatio →
  - kategoria-kasvun-dynamiikka | Kasvun dynamiikka →
---

Projektien lainalaisuuksissa on yksi piirre, joka erottaa ne muista tämän sivuston ilmiöistä: ne on nimetty ihmisten mukaan, jotka havaitsivat ne omassa työssään ja kirjoittivat ne ylös hieman vastentahtoisesti. Fred Brooks kirjoitti lakinsa IBM:n System/360-projektin jälkeen, Douglas Hofstadter muotoili omansa rekursiiviseksi vitsiksi, joka osoittautui todeksi.

Yhteinen havainto on epämukava: **aikatauluarvion pettäminen ei ole huolimattomuutta vaan järjestelmällistä.** Se toistuu samoilla ihmisillä, samoilla menetelmillä ja samoissa organisaatioissa vuodesta toiseen, myös silloin kun edellinen ylitys on tuoreessa muistissa. Siksi näitä kutsutaan laeiksi eikä virheiksi.

## Neljä mekanismia

**Aika ei skaalaudu.** [Hofstadterin laki](hofstadterin-laki.html) muotoilee perusongelman rekursiivisesti: kaikki kestää odotettua kauemmin, myös silloin kun otat Hofstadterin lain huomioon. [Yhdeksän-yhdeksän-sääntö](yhdeksanyhdeksan.html) tarkentaa mihin aika katoaa — ensimmäinen 90 % työstä vie 90 % ajasta ja viimeinen 10 % vie loput 90 %. [Brooksin laki](brooksin-laki.html) sulkee viimeisenkin pakotien: myöhässä olevaan projektiin lisätty työvoima myöhästyttää sitä lisää, koska kommunikaatiopolkujen määrä kasvaa neliöllisesti eikä lineaarisesti.

**Laajuus liikkuu.** [Scope creep](scope-creep.html) kasvattaa projektin palasina, joista yksikään ei yksin ansaitse aikataulukeskustelua. [Bikeshedding](bikeshedding.html) on sen huomiotalouden vastine: komitea käyttää tunnin polkupyöräkatoksen väriin, koska siitä kaikki osaavat olla mieltä, ja ydinvoimalan mitoitus menee läpi keskustelutta.

**Velalle kertyy korkoa.** [Tekninen velka](tekninen-velka.html) on kategorian tarkin metafora: oikotie nopeuttaa nyt ja peritään myöhemmin takaisin korkoineen. [Kuolonmarssi](kuolonmarssi.html) on tila, johon kertynyt velka johtaa — projekti, jonka kaikki tietävät epäonnistuvan mutta jota kukaan ei pysty pysäyttämään.

**Arvio on hakemus.** Suurhankkeissa aliarviointi lakkaa olemasta erehdys ja muuttuu tekniikaksi. [Strateginen aliarviointi](strateginen-aliarviointi.html) on Bent Flyvbjergin havainto siitä, että kustannusarviot eivät hajoa satunnaisesti vaan systemaattisesti samaan suuntaan: rehellinen arvio häviää portilla optimistiselle, joten portin läpi menee vain optimistisia. [Lukittu päätös](lukittu-paatos.html) kertoo, milloin hanke tosiasiassa ratkaistiin — muodollinen käsittely vahvistaa päätöksen, jota on valmisteltu vuosia. [Päätösperäinen todistelu](paatosperainen-todistelu.html) on sen tukiaskel: selvitys tilataan vastaus valmiina. Ja kun hanke on kerran sidottu henkilön nimeen, [läpi hinnalla millä hyvänsä](lapi-hinnalla-milla-hyvansa.html) selittää miksi peruuttaminen käy mahdottomaksi — jokainen huono uutinen uhkaa päättäjää eikä hanketta.

Näiden ulkopuolella on [Conwayn laki](conways-laki.html), joka on kategorian syvin havainto: järjestelmän arkkitehtuuri kopioi väistämättä sen suunnitelleen organisaation rakenteen. Se ei kuvaa virhettä vaan lainalaisuutta — ja siksi se on ainoa näistä, jota voi käyttää suunnittelutyökaluna. Jos haluat toisenlaisen järjestelmän, muuta ensin organisaatio.

## Kaksitoista lainalaisuutta

[[ILMIOT]]

## Miten nämä liittyvät toisiinsa

- **Hofstadterin laki ja yhdeksän-yhdeksän-sääntö kuvaavat samaa ilmiötä eri tarkkuudella.** Edellinen sanoo että arvio pettää, jälkimmäinen sanoo missä kohtaa: viimeistelyssä, integraatiossa ja siinä mitä ei osattu ennakoida.
- **Brooksin laki tekee myöhästymisestä peruuttamatonta.** Kun aikataulu on jo pettänyt, ainoa nopea korjausliike — lisää väkeä — pahentaa tilannetta. Jäljelle jää laajuuden leikkaaminen tai aikataulun siirto.
- **Scope creep ja tekninen velka syöttävät toisiaan.** Uusi ominaisuus rakennetaan olemassa olevan oikotien päälle, mikä tekee seuraavasta ominaisuudesta kalliimman, mikä houkuttelee uuteen oikotiehen.
- **Kuolonmarssi on tekninen velka plus [sunk cost -harha](sunk-cost-harha.html) plus [maalitolppien siirtäminen](maalitolppien-siirtaminen.html).** Velka tekee etenemisen mahdottomaksi, uponneet kustannukset estävät lopettamisen ja kriteerien siirtäminen tekee jatkamisesta muodollisesti onnistunutta.
- **Bikeshedding on [Parkinsonin lain](parkinsonin-laki.html) vähäpätöisyyslaki.** Sama havainto: aika täyttyy sillä, mikä on helposti käsiteltävissä, ei sillä mikä on tärkeää.
- **Conwayn laki selittää, miksi arkkitehtuurikorjaukset epäonnistuvat.** Jos rajapinta seuraa tiimirajaa, rajapinnan siirtäminen edellyttää tiimirajan siirtämistä.
- **Strateginen aliarviointi ja kuolonmarssi ovat saman ketjun päät.** Portille viritetty hinta tarkoittaa, että hanke aloitetaan resursseilla, jotka eivät riitä — ja kun se selviää, lopettaminen on jo poliittisesti kalliimpaa kuin jatkaminen.
- **Lukittu päätös tekee päätösperäisestä todistelusta väistämätöntä.** Kun ratkaisu on tehty ennen käsittelyä, selvityksen ainoa jäljellä oleva tehtävä on perustella se. Kysymys ei ole tutkijan rehellisyydestä vaan toimeksiannon rajauksesta.

## Mitä näistä seuraa lukijalle

1. **Älä hyväksy ”melkein valmista” tilatietona.** Kysy sen sijaan, mitä on vielä integroimatta, testaamatta ja siirtämättä tuotantoon. Yhdeksän-yhdeksän-sääntö sanoo, että juuri se työ vie loput puolet ajasta.
2. **Älä lisää väkeä myöhässä olevaan projektiin.** Leikkaa laajuutta tai siirrä päivämäärää — kolmatta vaihtoehtoa ei ole.
3. **Tee velasta näkyvää.** Kirjaamaton oikotie ei ole päätös vaan unohdus.
4. **Katso agendaa väristä.** Jos kokous käyttää eniten aikaa halvimpaan päätökseen, kalliit menivät jo läpi.
5. **Kysy vertailuluokkaa, älä perusteluja.** Yksittäisen arvion perustelut ovat aina hyvät. Ainoa kysymys, jota ne eivät kestä, on: *mitä vastaavat jo toteutuneet hankkeet lopulta maksoivat?*

:::html
<div class="infolaatikko">
<h2 class="laatikko-otsikko">Yhteinen nimittäjä:</h2> ihminen aliarvioi monimutkaisuuden järjestelmällisesti, ja järjestelmällistä virhettä ei korjaa yrittämällä kovemmin. Sen korjaa vain menetelmä — pienemmät erät, kirjatut oletukset ja aiempien arvioiden toteutuma vertailukohtana.
</div>
:::

[[NAAPURIT]]
