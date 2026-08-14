---
kat_id: tilastoilla-valehtelu-kategoria
h1: Tilastoilla valehtelu — miten luvuilla johdetaan harhaan valehtelematta
otsikko: Tilastoilla valehtelu — 8 tekniikkaa, joilla luvut johtavat harhaan
kuvaus: Katkaistu akseli, valikoitu aikaväli, väärä keskiluku. Yhdeksän tapaa johtaa harhaan tilastolla, joka on teknisesti oikein — ja viisi paljastavaa kysymystä.
vari: "#1565c0"
paivitetty: 2026-08-14
naapurit:
  - kategoria-informaatio-ja-propaganda | Informaatio ja propaganda →
  - kategoria-psykologia-ja-kognitio | Psykologia ja kognitio →
  - kategoria-byrokratia-ja-organisaatio | Byrokratia ja organisaatio →
  - kategoria-media-ja-julkisuus | Media ja julkisuus →
---

Tilastolla valehteleminen eroaa tavallisesta valehtelusta yhdessä ratkaisevassa kohdassa: yksikään luku ei ole väärä. Katkaistun akselin pylväät on piirretty täsmälleen oikein, valikoidun aikavälin kasvuprosentti on laskettu oikein, ja kaksinkertaistunut riski todella kaksinkertaistui. Harha syntyy siitä, mitä esitys korostaa ja mitä se jättää sanomatta. Juuri siksi nämä tekniikat ovat niin kestäviä — niistä ei voi jäädä kiinni valehtelusta.

Darrell Huff kokosi kikat kirjaan **How to Lie with Statistics** jo vuonna 1954. Seitsemänkymmentä vuotta myöhemmin ne toimivat edelleen, koska ne eivät hyödynnä tietämättömyyttä vaan havaitsemista: ihminen rekisteröi kuvan ennen lukuja ja vertaa muotoja, ei asteikkoja. Kun kaksi käyrää nousee samassa tahdissa, yhteys on ehtinyt syntyä katsojan päässä ennen kuin akselin numerot kiinnittävät kenenkään huomiota.

## Kolme perhettä

Kategorian yhdeksän ilmiötä eroavat toisistaan siinä, missä kohtaa ketjua harha syntyy. Sama jako toimii myös tarkistuslistana: kun tiedät kumpaan perheeseen väite kuuluu, tiedät mitä kysyä.

**Kuva valehtelee.** Data on kunnossa, mutta piirros vääristää sen. [Kaksois-y-akseli](kaksois-y-akseli.html) skaalaa kaksi eri suuretta päällekkäin ja tuottaa korrelaation tyhjästä. [Pinta-alaharha](pinta-alaharha.html) kasvattaa symbolin molempia mittoja, jolloin kaksinkertainen luku näyttää nelinkertaiselta. Näissä riittää yleensä, että katsoo akselin nollapisteen ennen käyrää.

**Valinta valehtelee.** Luvut ovat oikein, mutta ne ovat väärä osajoukko. [Cherry-picking](cherry-picking-aikavali.html) valitsee aikavälin alku- ja loppupisteen niin, että sama aikasarja todistaa mitä tahansa. [Selviytymisharha](selviytymisharha.html) laskee vain ne, jotka pääsivät mittauspisteeseen asti. [P-hakkerointi](p-hakkerointi.html) tekee saman tieteen muodossa: testataan kunnes jokin näyttää merkitsevältä, ja julkaistaan vain se yksi tulos.

**Luku itse valehtelee.** Tunnusluku on laskettu oikein, mutta se vastaa eri kysymykseen kuin lukija kuvittelee. [Keskiarvoharha](keskiarvo-vs-mediaani.html) antaa vinossa jakaumassa aivan toisen kuvan kuin mediaani. [Suhteellinen riski](suhteellinen-riski.html) kertoo muutoksen suuruuden kertomatta lähtötasoa. [Simpsonin paradoksi](simpsonin-paradoksi.html) on näistä ovelin: kokonaisluku voi kääntyä päinvastaiseksi kuin jokainen osaryhmä erikseen. [Kannatusmittausten virhemarginaali](kannatusmittausten-virhemarginaali.html) on saman perheen erikoistapaus: luku on oikein ja epätarkkuuskin ilmoitetaan, mutta ilmoitettu marginaali koskee yhtä lukua — ja uutinen kertoo kahden luvun erosta.

Jos luet kategorian läpi kerralla, tuo on myös järkevin järjestys. Kuvatemput oppii tunnistamaan silmällä, valintatemput vaativat kysymään mitä aineistosta puuttuu, ja lukutemput vaativat ymmärtämään mitä tunnusluku oikeastaan mittaa.

## Yhdeksän tekniikkaa

[[ILMIOT]]

## Klassikkoesimerkki: katkaistu y-akseli

Yleisin temppu on niin yksinkertainen, että se kannattaa nähdä kerran vierekkäin. Akseli aloitetaan nollan sijasta läheltä pienintä havaintoa, jolloin kahden prosentin muutos täyttää koko kuvan.

:::html
<div class="tilasto-grid">
<div class="tilasto-esimerkki">
<h4>Harhaanjohtava (akseli alkaa 97:stä)</h4>
<div class="pylvas-wrapper">
<div style="display:flex;flex-direction:column;justify-content:flex-end;height:100%;width:36px;">
<div class="pylvas" style="height:20%;background:#c0392b;">99</div>
</div>
<div style="display:flex;flex-direction:column;justify-content:flex-end;height:100%;width:36px;">
<div class="pylvas" style="height:60%;background:#c0392b;">100</div>
</div>
<div style="display:flex;flex-direction:column;justify-content:flex-end;height:100%;width:36px;">
<div class="pylvas" style="height:100%;background:#c0392b;">101</div>
</div>
</div>
<div class="pylvas-label">Vuosi A &nbsp; Vuosi B &nbsp; Vuosi C</div>
<p style="font-size:0.8em;color:#c0392b;margin-top:0.5rem;">Näyttää: +400 % kasvu!</p>
</div>
<div class="tilasto-esimerkki">
<h4>Rehellinen (akseli alkaa nollasta)</h4>
<div class="pylvas-wrapper">
<div style="display:flex;flex-direction:column;justify-content:flex-end;height:100%;width:36px;">
<div class="pylvas" style="height:97.8%;background:#27ae60;">99</div>
</div>
<div style="display:flex;flex-direction:column;justify-content:flex-end;height:100%;width:36px;">
<div class="pylvas" style="height:98.8%;background:#27ae60;">100</div>
</div>
<div style="display:flex;flex-direction:column;justify-content:flex-end;height:100%;width:36px;">
<div class="pylvas" style="height:100%;background:#27ae60;">101</div>
</div>
</div>
<div class="pylvas-label">Vuosi A &nbsp; Vuosi B &nbsp; Vuosi C</div>
<p style="font-size:0.8em;color:#27ae60;margin-top:0.5rem;">Todellinen muutos: +2 %</p>
</div>
</div>
:::

## Miten nämä liittyvät toisiinsa

- **Kaksois-y-akseli ja pinta-alaharha ovat sama virhe eri ulottuvuudessa.** Toinen venyttää pystysuunnassa, toinen pinta-alassa. Kummankin paljastaa sama kysymys: mistä asteikko alkaa ja mitä sen pituus oikeastaan mittaa.
- **Cherry-picking ja selviytymisharha ovat otantavirheitä eri suuntiin.** Edellinen rajaa ajan, jälkimmäinen joukon. Molemmissa aineisto on aito mutta otos ei edusta sitä, mistä puhutaan.
- **P-hakkerointi on cherry-picking siirrettynä hypoteeseihin.** Aikavälin sijasta valitaan jälkikäteen kysymys, johon data sattui vastaamaan. Yhdessä selviytymisharhan kanssa se tuottaa julkaisuharhan: kirjallisuuteen päätyvät vain onnistuneet tulokset, ja niistä lasketaan keskiarvo.
- **Keskiarvoharha ja Simpsonin paradoksi syntyvät molemmat yhdistämisestä.** Kun eri ryhmät lasketaan yhteen, painotus ratkaisee tuloksen. Simpsonin paradoksi on tämän ääritapaus, jossa suunta kääntyy päinvastaiseksi.
- **Suhteellinen riski ja katkaistu akseli tekevät saman tempun eri välineillä.** Molemmat suurentavat pientä muutosta poistamalla vertailukohdan — toinen kuvasta, toinen lauseesta.
- **Koko kategoria on propagandan työkalupakki.** Nämä tekniikat esiintyvät harvoin yksin: [firehose of falsehood](firehose-of-falsehood.html) tuottaa niitä nopeammin kuin faktantarkistus ehtii perässä, ja [astroturf](astroturf.html) antaa niille uskottavan lähettäjän. Organisaatioissa sama logiikka näkyy [Goodhartin lakina](goodhartin-laki.html): kun mittarista tulee tavoite, se lakkaa mittaamasta.

## Viisi kysymystä, jotka paljastavat lähes kaiken

1. **Mistä y-akseli alkaa?** Jos ei nollasta, muutoksen kokoa ei voi lukea kuvasta.
2. **Miksi juuri tämä aikaväli?** Siirrä alkupistettä vuodella ja katso, säilyykö trendi.
3. **Ketkä puuttuvat aineistosta?** Kysy erikseen niistä, jotka eivät päässeet mittaukseen asti.
4. **Mikä on absoluuttinen luku?** ”Kaksinkertaistui” tarkoittaa eri asiaa, jos lähtötaso on 1/100 000.
5. **Mitä tapahtuu, kun ryhmät erotellaan?** Jos kokonaisluku ja osaryhmät kertovat eri tarinan, osaryhmät ovat lähempänä totuutta.

:::html
<div class="infolaatikko">
<h2 class="laatikko-otsikko">Perussääntö:</h2> kun näet vakuuttavan kaavion, katso ensimmäisenä y-akselin nollapiste, aikavälin rajat ja se, mitä kuvasta <em>puuttuu</em>. Nämä kolme paljastavat suurimman osan tämän kategorian tekniikoista ilman yhtäkään laskutoimitusta.
</div>

<div class="lue-lisaa">
<div class="lue-lisaa-otsikko">Lue lisää</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Kirjoja</span>
<ul class="lue-lisaa-lista">
<li><cite>How to Lie with Statistics</cite> — Darrell Huff (1954)</li>
<li><cite>The Art of Statistics</cite> — David Spiegelhalter (2019)</li>
<li><cite>Factfulness</cite> — Hans Rosling (2018)</li>
</ul>
</div>
<div class="lue-lisaa-rivi">
<span class="lue-lisaa-tyyppi">Verkossa</span>
<ul class="lue-lisaa-lista">
<li><a href="https://en.wikipedia.org/wiki/Misleading_graph" target="_blank" rel="noopener">Wikipedia: Misleading graph (englanniksi)</a></li>
<li><a href="https://en.wikipedia.org/wiki/Lies,_damned_lies,_and_statistics" target="_blank" rel="noopener">Wikipedia: Lies, damned lies, and statistics (englanniksi)</a></li>
</ul>
</div>
</div>
:::

[[NAAPURIT]]
