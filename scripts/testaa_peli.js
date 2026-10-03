#!/usr/bin/env node
/*
 * Läpipeluutesti Vedätys-pelille.
 *
 * Rakentaa minimaalisen DOM-tyngän, lataa OIKEAN luonnokset/peli.html:n
 * inline-skriptin ja pelaa erän läpi napin painalluksesta loppuruutuun.
 * Ei selainta, ei jsdomia, ei package.jsonia — sivustolla ei ole
 * JS-työkaluketjua eikä sellaista tuoda tämän takia.
 *
 * Syntyi siitä, että peli oli hetken julkaisukelvoton täysin hiljaisesti:
 * data/peli-pankki.js ladattiin defer-attribuutilla, joten inline-skripti
 * ajettiin ennen sitä, "if (!P) return" poistui heti eikä yhtään nappia
 * kytketty. Mikään olemassa ollut tarkistus ei huomannut sitä. Testin
 * kohta 1 (kuunteleeko aloitusnappi ylipäätään) olisi.
 *
 * Ei kata: ulkoasua, CSS:ää, mobiililayoutia, oikeaa leikepöytää tai
 * prefers-reduced-motionia. Ne jäävät selaintestaukseen. Tämä todentaa
 * kytkennät ja pelin kulun, ei sitä miltä peli näyttää.
 *
 *     node scripts/testaa_peli.js
 */
'use strict';

const fs = require('fs');
const path = require('path');

const JUURI = path.join(__dirname, '..');
// Oletuksena luonnos. PELI_SIVU-ympäristömuuttujalla testin voi ajaa myös
// julkaistua juuren peli.html:ää vasten — tai rikottua kopiota vasten, kun
// halutaan varmistua siitä että testi oikeasti kaatuu.
const SIVU = process.env.PELI_SIVU || path.join(JUURI, 'luonnokset', 'peli.html');
const DATA = path.join(JUURI, 'data', 'peli-pankki.js');

let virheita = 0;
function ok(ehto, viesti) {
  if (ehto) { console.log('  ✓ ' + viesti); }
  else { console.log('  ✗ ' + viesti); virheita++; }
}

// ── DOM-tynkä ────────────────────────────────────────────────────────
function teeElementti(tag, rekisteri) {
  const el = {
    tagName: (tag || 'div').toUpperCase(),
    lapset: [],
    _teksti: '',
    hidden: false,
    disabled: false,
    className: '',
    style: {},
    kuuntelijat: {},
    appendChild(lapsi) { this.lapset.push(lapsi); return lapsi; },
    removeChild(lapsi) {
      const i = this.lapset.indexOf(lapsi);
      if (i >= 0) { this.lapset.splice(i, 1); }
      return lapsi;
    },
    get firstChild() { return this.lapset.length ? this.lapset[0] : null; },
    get children() { return this.lapset; },
    get textContent() {
      return this._teksti + this.lapset.map((l) => l.textContent).join('');
    },
    set textContent(v) { this._teksti = String(v); this.lapset = []; },
    setAttribute(nimi, arvo) { this[nimi] = arvo; },
    addEventListener(nimi, fn) {
      (this.kuuntelijat[nimi] = this.kuuntelijat[nimi] || []).push(fn);
    },
    click() { (this.kuuntelijat.click || []).forEach((fn) => fn({ preventDefault() {} })); },
    focus() {}, select() {},
    querySelectorAll(valitsin) {
      const luokka = valitsin.replace(/^\./, '');
      const ulos = [];
      (function kay(el) {
        el.lapset.forEach((l) => {
          if (typeof l.className === 'string' && l.className.split(/\s+/).indexOf(luokka) >= 0) {
            ulos.push(l);
          }
          if (l.lapset) { kay(l); }
        });
      })(el);
      return ulos;
    }
  };
  if (rekisteri && tag === undefined) { /* ei mitään */ }
  return el;
}

function teeYmparisto(asetukset) {
  const idt = {};
  // Esiluodaan HTML-rungon elementit id-attribuuteista, jotta $() löytää ne.
  const runko = fs.readFileSync(SIVU, 'utf8').split('<script>')[0];
  (runko.match(/<[a-z][^>]*\bid="[^"]+"[^>]*>/g) || []).forEach((tagi) => {
    const id = tagi.match(/\bid="([^"]+)"/)[1];
    const el = teeElementti(tagi.match(/^<([a-z]+)/)[1]);
    el.id = id;
    // hidden-attribuutti on luettava rungosta: puolet pelin näkymistä on
    // aluksi piilotettuja, ja tynkä joka aloittaa kaiken näkyvänä antaisi
    // vihreän valon myös rikkinäiselle näkymänvaihdolle.
    el.hidden = /\shidden(?=[\s>=])/.test(tagi);
    idt[id] = el;
  });

  const body = teeElementti('body');
  const document = {
    lapset: [],
    body: body,
    kuuntelijat: {},
    getElementById(id) { return idt[id] || null; },
    createElement(tag) { return teeElementti(tag); },
    createTextNode(t) { return { _teksti: String(t), lapset: [], get textContent() { return this._teksti; } }; },
    addEventListener(nimi, fn) {
      (this.kuuntelijat[nimi] = this.kuuntelijat[nimi] || []).push(fn);
    },
    execCommand() { return true; }
  };

  // asetukset.talletus jaetaan ympäristöjen kesken, kun testataan samaa
  // selainta eri päivinä. Ilman sitä jokainen ympäristö on uusi selain.
  const talletus = asetukset.talletus || {};
  const localStorage = {
    getItem(k) {
      if (asetukset.storageHeittaa) { throw new Error('yksityinen ikkuna'); }
      return Object.prototype.hasOwnProperty.call(talletus, k) ? talletus[k] : null;
    },
    setItem(k, v) {
      if (asetukset.storageHeittaa) { throw new Error('yksityinen ikkuna'); }
      talletus[k] = String(v);
    },
    removeItem(k) {
      if (asetukset.storageHeittaa) { throw new Error('yksityinen ikkuna'); }
      delete talletus[k];
    }
  };

  const window = {
    location: { search: asetukset.search || '' },
    localStorage: localStorage,
    setInterval() { return 1; },
    clearInterval() {},
    setTimeout() { return 1; },
    scrollTo() {}
  };
  // Kiinteä "tänään": muuten arkiston kellonrajaus (paiva <= tamaPaiva())
  // estäisi tulevien erien testaamisen. Lasketaan pankin epokista eikä
  // kovakoodata: epokki vaihtuu julkaisussa, eikä testin pidä kaatua siihen.
  const ep = PANKKI.epokki.split('-').map(Number);
  const nyt = new Date(ep[0], ep[1] - 1, ep[2] + (asetukset.paiva || 0), 12, 0, 0);
  class PysahtynytDate extends Date {
    constructor(...a) { if (a.length === 0) { super(nyt.getTime()); } else { super(...a); } }
    static now() { return nyt.getTime(); }
  }

  // ── Suoritusjärjestys on selaimen järjestys, ja se on tässä koko juju ──
  // Sivulla on <script src="…" defer> ja heti perässä inline-<script>.
  // Selain ajaa INLINE-SKRIPTIN ENSIN (jäsennyshetkellä) ja deferoidun
  // vasta dokumentin jäsennyksen jälkeen. Jos tynkä lataisi datan ensin,
  // se antaisi vihreän valon koodille, joka lukee pankin moduulitasolla —
  // eli täsmälleen sille bugille, jonka takia tämä testi kirjoitettiin.
  const js = fs.readFileSync(SIVU, 'utf8').match(/<script>\n([\s\S]*?)\n<\/script>/)[1];
  new Function('window', 'document', 'navigator', 'Date', js)(
    window, document,
    asetukset.navigator || { clipboard: { writeText() { return Promise.resolve(); } } },
    PysahtynytDate
  );

  if (!asetukset.eiDataa) {
    new Function('window', fs.readFileSync(DATA, 'utf8'))(window);
  }

  return {
    $: (id) => idt[id],
    document: document,
    kaynnista() { (document.kuuntelijat.DOMContentLoaded || []).forEach((fn) => fn()); }
  };
}

// ── Apurit ───────────────────────────────────────────────────────────
const PANKKI = (() => { const w = {}; new Function('window', fs.readFileSync(DATA, 'utf8'))(w); return w.VEDATYS_PANKKI; })();
const LAJI_INDEKSI = { rehellinen: 0, vinouma: 1, taktiikka: 2 };

function eraKohdat(paiva) {
  return PANKKI.erat[paiva % PANKKI.erat.length].k.map((i) => PANKKI.kohdat[i]);
}

/** Pelaa erän läpi ja palauttaa lopputilan. */
function pelaaEra(ymp, paiva, valinnat) {
  valinnat = valinnat || {};
  const kohdat = eraKohdat(paiva);
  let lippuPalaute = '';
  ymp.$('aloitaNappi').click();

  for (let kierros = 0; kierros < kohdat.length; kierros++) {
    const k = kohdat[kierros];

    if (valinnat.lippuKierros === kierros) {
      ymp.$('lippuNappi').click();
      // Luetaan heti: seuraava piirraKierros() korvaa tekstin muistutuksella
      // siitä, että lippu on käytetty. Se on oikein, mutta erän lopussa
      // alkuperäistä palautetta ei enää ole näkyvissä.
      lippuPalaute = ymp.$('lippuSelite').textContent;
    }

    // Vaihe 1: luokittelu. Vastataan oikein, ellei toisin pyydetä.
    let napit = ymp.$('valinnat').querySelectorAll('.valinta');
    if (napit.length !== 3) { throw new Error('kierros ' + kierros + ': ' + napit.length + ' lajivaihtoehtoa'); }
    // valinnat.valitse(kierros, kohta, napit) saa nähdä kierroksen ennen
    // vastausta ja voi palauttaa oman valintansa (indeksi 0–2).
    const oma = valinnat.valitse ? valinnat.valitse(kierros, k, napit) : undefined;
    napit[oma !== undefined ? oma
      : (valinnat.vaaraLaji ? (LAJI_INDEKSI[k.l] + 1) % 3 : LAJI_INDEKSI[k.l])].click();

    // Vaihe 2: nimeäminen, jos se ilmestyi.
    if (ymp.$('paljastus').hidden) {
      napit = ymp.$('valinnat').querySelectorAll('.valinta');
      if (napit.length !== 3) { throw new Error('kierros ' + kierros + ': ' + napit.length + ' nimivaihtoehtoa'); }
      const oikeaNimi = PANKKI.ilmiot[k.i].n;
      let valinta = napit[0];
      napit.forEach((n) => {
        const osuu = n.children[1].textContent.indexOf(oikeaNimi) === 0;
        if (valinnat.vaaraNimi ? !osuu : osuu) { valinta = n; }
      });
      valinta.click();
    }

    if (ymp.$('paljastus').hidden) { throw new Error('kierros ' + kierros + ': paljastus ei tullut'); }
    if (valinnat.paljastuksessa) { valinnat.paljastuksessa(kierros, k); }
    ymp.$('seuraavaNappi').click();
  }
  return {
    luokitus: ymp.$('tLuokitus').textContent,
    nimeaminen: ymp.$('tNimeaminen').textContent,
    ruudukko: Array.from(ymp.$('ruudukko').textContent),
    jako: ymp.$('jakoTeksti').textContent,
    ansaRaporttiNakyy: !ymp.$('ansaRaportti').hidden,
    lippuPalaute: lippuPalaute
  };
}

// ══ Testit ═══════════════════════════════════════════════════════════
console.log('\n1. Käynnistys (regressio: defer-latausjärjestys)');
{
  const ymp = teeYmparisto({});
  ymp.kaynnista();
  const kuuntelijat = (ymp.$('aloitaNappi').kuuntelijat.click || []).length;
  ok(kuuntelijat > 0, 'aloitusnappiin on kiinnitetty click-kuuntelija');
  ok(ymp.$('latausvirhe').hidden, 'latausvirhe ei näy kun data on paikallaan');
}

console.log('\n2. Puuttuva data näkyy, ei kaadu hiljaa');
{
  const ymp = teeYmparisto({ eiDataa: true });
  ymp.kaynnista();
  ok(!ymp.$('latausvirhe').hidden, 'latausvirhe näkyy ilman dataa');
  ok(ymp.$('aloitaNappi').hidden, 'aloitusnappi piilotetaan');
}

console.log('\n3. Täysi läpipeluu, kaikki oikein');
{
  const ymp = teeYmparisto({});
  ymp.kaynnista();
  ok(ymp.$('peli').hidden && !ymp.$('aloitus').hidden, 'aluksi näkyvissä on aloitusruutu');
  const t = pelaaEra(ymp, 0);
  ok(ymp.$('loppu').hidden === false && ymp.$('peli').hidden, 'loppuruutu näkyy, pelinäkymä piiloutuu');
  ok(t.luokitus === '5/5', 'tunnistus 5/5 kun vastataan oikein (oli ' + t.luokitus + ')');
  ok(t.nimeaminen.split('/')[0] === t.nimeaminen.split('/')[1] && t.nimeaminen !== '0/0',
     'nimeäminen täydet ja nimeämisvaihe ilmestyi (' + t.nimeaminen + ')');
  ok(t.ruudukko.length === 5 && t.ruudukko.every((m) => m === '\u{1F7E9}'),
     'ruudukossa viisi vihreää');
  ok(/^Vedätys #1 /.test(t.jako) && t.jako.indexOf('?p=0&t=GGGGG0') > 0,
     'jakoteksti ja haastelinkki oikein');
}

console.log('\n4. Väärä nimi antaa keltaisen, väärä laji punaisen');
{
  let ymp = teeYmparisto({});
  ymp.kaynnista();
  const kelt = pelaaEra(ymp, 0, { vaaraNimi: true });
  const kohdat = eraKohdat(0);
  const temppuja = kohdat.filter((k) => k.l !== 'rehellinen').length;
  ok(kelt.luokitus === '5/5', 'luokitus pysyy oikeana vaikka nimi menee väärin');
  ok(kelt.ruudukko.filter((m) => m === '\u{1F7E8}').length === temppuja,
     temppuja + ' keltaista = temppujen määrä erässä');

  ymp = teeYmparisto({});
  ymp.kaynnista();
  const pun = pelaaEra(ymp, 0, { vaaraLaji: true });
  ok(pun.luokitus === '0/5', 'väärä laji joka kierroksella = 0/5');
  ok(pun.ruudukko.every((m) => m === '\u{1F7E5}'), 'ruudukossa viisi punaista');
}

console.log('\n5. Ansa ja lippu');
{
  // Joka kolmas erä sisältää ansan; etsitään ensimmäinen.
  const ansaPaiva = PANKKI.erat.findIndex((e) => e.a);
  const ansa = PANKKI.erat[ansaPaiva].a;
  ok(ansaPaiva >= 0 && ansa.r >= 1, 'ansaerä löytyy (#' + (ansaPaiva + 1) + ', kierros ' + ansa.r + ')');

  let ymp = teeYmparisto({ paiva: ansaPaiva });
  ymp.kaynnista();
  const osui = pelaaEra(ymp, ansaPaiva, { lippuKierros: ansa.r });
  ok(osui.jako.indexOf('\u{1F6A9} huomasit ansan') > 0, 'osunut lippu näkyy jakotekstissä');
  ok(osui.ansaRaporttiNakyy, 'ansaraportti näkyy lopussa');

  ymp = teeYmparisto({ paiva: ansaPaiva });
  ymp.kaynnista();
  const ohi = pelaaEra(ymp, ansaPaiva, { lippuKierros: (ansa.r + 1) % 5 });
  ok(ohi.jako.indexOf('\u{1F6A9}') === -1, 'väärään kierrokseen osunut lippu ei tuota merkkiä');
  ok(ohi.lippuPalaute.indexOf('Ei tällä kertaa') === 0,
     'turha liputus ei rankaise, vaan kiittää katsomisesta');

  // Ansaton erä: liputus ei saa kaataa mitään.
  const puhdas = PANKKI.erat.findIndex((e) => !e.a);
  ymp = teeYmparisto({ paiva: puhdas });
  ymp.kaynnista();
  const t = pelaaEra(ymp, puhdas, { lippuKierros: 0 });
  ok(t.luokitus === '5/5' && t.jako.indexOf('\u{1F6A9}') === -1,
     'ansattomassa erässä liputus on vaaraton');
}

console.log('\n6. Päivä vaihtuu ja tehosteputki kertyy');
{
  const selain = {};
  const eka = teeYmparisto({ paiva: 0, talletus: selain });
  eka.kaynnista();
  pelaaEra(eka, 0);
  ok(eka.$('tTehoste').textContent === '1', 'ensimmäisenä päivänä tehoste on 1');

  // Sama selain, seuraava päivä: erän on vaihduttava.
  const eilen = eraKohdat(0).map((k) => k.id).join();
  const tanaan = eraKohdat(1).map((k) => k.id).join();
  ok(eilen !== tanaan, 'seuraavan päivän erä on eri');

  const toinen = teeYmparisto({ paiva: 1, talletus: selain });
  toinen.kaynnista();
  const t = pelaaEra(toinen, 1);
  ok(/^Vedätys #2 /.test(t.jako), 'toisena päivänä numero on #2');
  ok(toinen.$('tTehoste').textContent === '2', 'toisena päivänä peräkkäin tehoste on 2');
}

console.log('\n7. Rikkinäinen localStorage ei kaada peliä');
{
  const ymp = teeYmparisto({ storageHeittaa: true });
  ymp.kaynnista();
  const t = pelaaEra(ymp, 0);
  ok(t.luokitus === '5/5', 'erä pelattavissa läpi ilman toimivaa talletusta');
}

console.log('\n8. Haastelinkki');
{
  const ymp = teeYmparisto({ search: '?p=0&t=GGRYG1' });
  ymp.kaynnista();
  ok(!ymp.$('haasteLaatikko').hidden, 'haastekutsu näkyy aloitusruudussa');
  ok(ymp.$('haasteLaatikko').textContent.indexOf('3/5') > 0, 'haastajan pisteet luetaan koodista');
  pelaaEra(ymp, 0);
  ok(!ymp.$('vertailu').hidden, 'vertailu näkyy lopussa');
}

console.log('\n9. Päiväindeksi (poimitaan funktiot suoraan sivulta)');
{
  // Testataan julkaistavaa koodia, ei kopiota siitä.
  const html = fs.readFileSync(SIVU, 'utf8');
  function poimi(nimi) {
    const m = html.match(new RegExp('\\n  function ' + nimi + '\\b[\\s\\S]*?\\n  \\}\\n'));
    if (!m) { throw new Error('funktiota ei löytynyt: ' + nimi); }
    return m[0];
  }
  const F = new Function('P', [
    'var VRK=864e5;', 'var EPOKKI=uusiPvm(P.epokki);',
    poimi('uusiPvm'), poimi('paivaIndeksi'), poimi('arpoja'), poimi('sekoita'),
    'return {paivaIndeksi:paivaIndeksi, sekoita:sekoita};'
  ].join('\n'))(PANKKI);

  const e = PANKKI.epokki.split('-').map(Number);
  ok(F.paivaIndeksi(new Date(e[0], e[1] - 1, e[2])) === 0,
     'epokki ' + PANKKI.epokki + ' = päivä 0 (Vedätys #1)');
  ok(F.paivaIndeksi(new Date(e[0], e[1] - 1, e[2] + 1)) === 1, 'seuraava päivä = 1');

  // Suomen kesäaika päättyy su 25.10.2026 klo 04 → 03. Ilman
  // setHours(0,0,0,0):aa molemmille päiville indeksi hyppäisi.
  const a = F.paivaIndeksi(new Date(2026, 9, 24, 12));
  const b = F.paivaIndeksi(new Date(2026, 9, 25, 12));
  const c = F.paivaIndeksi(new Date(2026, 9, 26, 12));
  ok(b - a === 1 && c - b === 1, 'kesäajan vaihtuminen 25.10.2026 ei hyppää');
  ok(F.paivaIndeksi(new Date(2026, 9, 25, 0, 30)) === F.paivaIndeksi(new Date(2026, 9, 25, 23, 30)),
     'sama vuorokausi antaa saman indeksin kellonajasta riippumatta');
  ok(F.paivaIndeksi(new Date(2027, 0, 1)) - F.paivaIndeksi(new Date(2026, 11, 31)) === 1,
     'vuodenvaihde ei hyppää');
  ok(JSON.stringify(F.sekoita(['a', 'b', 'c'], 42)) === JSON.stringify(F.sekoita(['a', 'b', 'c'], 42)),
     'sekoitus on deterministinen — kaikki näkevät saman vaihtoehtojärjestyksen');

  // Nimeämisvaihtoehdot koko pankin läpi, ei vain pelattujen päivien.
  let rikki = 0;
  PANKKI.erat.forEach((era, paiva) => {
    era.k.forEach((ki, nyt) => {
      const k = PANKKI.kohdat[ki];
      if (k.l === 'rehellinen') { return; }
      const v = F.sekoita([k.i].concat(k.h), paiva * 101 + nyt * 7);
      if (v.length !== 3 || new Set(v).size !== 3 || v.indexOf(k.i) === -1) { rikki++; }
      v.forEach((slug) => { if (!PANKKI.ilmiot[slug]) { rikki++; } });
    });
  });
  const nimettavia = PANKKI.kohdat.filter((k) => k.l !== 'rehellinen').length;
  ok(rikki === 0, 'kaikissa ' + nimettavia + ' nimeämiskysymyksessä 3 eri vaihtoehtoa ja oikea vastaus mukana');
}

console.log('\n10. Pankin eheys');
{
  const reh = PANKKI.kohdat.filter((k) => k.l === 'rehellinen').length;
  ok(reh / PANKKI.kohdat.length >= 0.25,
     'rehellisiä ' + reh + '/' + PANKKI.kohdat.length + ' = ' +
     Math.round(reh / PANKKI.kohdat.length * 100) + ' % (≥25 %)');
  ok(PANKKI.kohdat.every((k) => k.l === 'rehellinen' || k.p[2].trim()),
     'jokaisella tempulla on käyttökelpoinen "mitä sanot" -lause');
  const puuttuu = Object.keys(PANKKI.ilmiot)
    .filter((slug) => !fs.existsSync(path.join(JUURI, slug + '.html')));
  ok(puuttuu.length === 0,
     Object.keys(PANKKI.ilmiot).length + ' ilmiölinkkiä osoittaa olemassa olevaan sivuun');
  const kaytetyt = new Set();
  PANKKI.erat.forEach((e) => e.k.forEach((i) => kaytetyt.add(i)));
  ok(kaytetyt.size === PANKKI.kohdat.length, 'jokainen kohta on käytössä täsmälleen kerran');
}

const tilastot = (selain) => JSON.parse(selain['peli-tilastot'] || 'null');

console.log('\n11. Vanha erä ei koske tehosteeseen (regressio: arkisto nollasi putken)');
{
  // Pelaamaton arkistoerä: ennen korjausta tämä siirsi viimeisin-päivän
  // taaksepäin ja pudotti putken yhteen.
  const selain = {};
  [4, 5].forEach((p) => {
    const y = teeYmparisto({ paiva: p, talletus: selain });
    y.kaynnista();
    pelaaEra(y, p);
  });
  ok(tilastot(selain).tehoste === 2 && tilastot(selain).viimeisin === 5, 'lähtötilanne: putki 2, viimeisin päivä 5');

  const arkisto = teeYmparisto({ paiva: 5, talletus: selain, search: '?paiva=2' });
  arkisto.kaynnista();
  const t = pelaaEra(arkisto, 2);
  ok(/^Vedätys #3 /.test(t.jako), 'arkistosta avautui erä #3');
  ok(tilastot(selain).tehoste === 2, 'putki on yhä 2 arkistoerän jälkeen');
  ok(tilastot(selain).viimeisin === 5, 'viimeisin pelipäivä ei siirtynyt taaksepäin');
  ok(tilastot(selain).pelatut === 2, 'arkistoerä ei kasvata pelattujen päivien määrää');
  ok(JSON.parse(selain['peli-tulokset'])[2].m === 'GGGGG', 'arkistoerän tulos on silti tallessa');

  const haaste = teeYmparisto({ paiva: 5, talletus: selain, search: '?p=1&t=GGGGG0' });
  haaste.kaynnista();
  pelaaEra(haaste, 1);
  ok(tilastot(selain).tehoste === 2 && tilastot(selain).viimeisin === 5,
     'vanha haastelinkki ei koske putkeen');
}

console.log('\n12. Tulos säilyy: palaava pelaaja näkee sen ja voi jakaa');
{
  const selain = {};
  let y = teeYmparisto({ paiva: 0, talletus: selain });
  y.kaynnista();
  const eka = pelaaEra(y, 0, { vaaraNimi: true });

  y = teeYmparisto({ paiva: 0, talletus: selain });
  y.kaynnista();
  ok(!y.$('loppu').hidden && y.$('aloitus').hidden, 'paluu samana päivänä avaa loppuruudun');
  ok(!y.$('tallessa').hidden, 'ruutu kertoo, että tulos on tallessa');
  ok(y.$('jakoTeksti').textContent === eka.jako, 'jakoteksti on sama kuin pelatessa');
  ok(Array.from(y.$('ruudukko').textContent).join() === eka.ruudukko.join(), 'ruudukko on sama');
  ok(!y.$('uudelleenNappi').hidden, 'uudelleen pelaaminen on tarjolla');

  // Uusintakierros kaikki oikein: jaettava tulos ei saa parantua.
  const uusinta = pelaaEra(y, 0);
  ok(uusinta.luokitus === '5/5' && uusinta.ruudukko.every((m) => m === '\u{1F7E9}'),
     'uusintakierros näyttää oman ruudukkonsa');
  ok(uusinta.jako === eka.jako, 'jaettava tulos on yhä ensimmäinen pelikerta');
  ok(!y.$('jakoHuomio').hidden, 'ja se sanotaan ääneen');
  ok(tilastot(selain).pelatut === 1, 'uusinta ei kerry tilastoihin');

  y.$('arkistoNappi').click();
  const rivit = y.$('arkistoSisalto').querySelectorAll('.arkisto-rivi');
  ok(rivit.length === 1 && rivit[0].textContent.indexOf('\u{1F7E8}') > 0,
     'arkisto näyttää pelatun erän ruudukon');
}

console.log('\n13. Katkennut putki näkyy katkenneena');
{
  const selain = {};
  let y = teeYmparisto({ paiva: 0, talletus: selain });
  y.kaynnista();
  pelaaEra(y, 0);
  const luku = (p) => {
    const ymp = teeYmparisto({ paiva: p, talletus: selain });
    ymp.kaynnista();
    return ymp.$('tehosteLuku').textContent;
  };
  ok(luku(1) === '1', 'seuraavana päivänä putki on voimassa');
  ok(luku(2) === '1', 'yhden väliin jääneen päivän kattaa armonpäivä');
  ok(luku(3) === '0', 'kahden väliin jääneen päivän jälkeen putki on 0');
}

console.log('\n14. Erottelu: ohitukset ja väärät hälytykset lasketaan erikseen');
{
  const selain = {};
  const y = teeYmparisto({ paiva: 0, talletus: selain });
  y.kaynnista();
  const kohdat = eraKohdat(0);
  const rehellisia = kohdat.filter((k) => k.l === 'rehellinen').length;
  // Temput merkitään tavallisiksi ja tavalliset tempuiksi.
  pelaaEra(y, 0, { valitse: (kierros, k) => (k.l === 'rehellinen' ? 2 : 0) });
  const t = tilastot(selain);
  ok(t.oh === kohdat.length - rehellisia && t.os === 0,
     'jokainen temppu kirjautui ohitukseksi (' + t.oh + ')');
  ok(t.vh === rehellisia && t.oo === 0, 'jokainen tavallinen kirjautui vääräksi hälytykseksi (' + t.vh + ')');
  ok(y.$('erotteluEra').textContent.indexOf('ohituksia ' + t.oh) > 0 &&
     y.$('erotteluEra').textContent.indexOf('vääriä hälytyksiä ' + t.vh) > 0,
     'erän rivi näyttää molemmat luvut');
  ok(!y.$('erotteluLaatikko').hidden && y.$('erotteluTulkinta').hidden,
     'kokonaisluvut näkyvät, mutta tulkintaa ei anneta viiden kohdan perusteella');
}

console.log('\n15. Ohjaava ansa osoittaa aina väärään vastaukseen');
{
  const NIMET = ['Tavallinen viesti', 'Oma pää', 'Joku tekee tämän'];
  let tarkistettu = 0, oikeaan = 0, raportti = 0;
  PANKKI.erat.forEach((era, paiva) => {
    if (!era.a || (era.a.t !== 'oletus' && era.a.t !== 'todiste')) { return; }
    const y = teeYmparisto({ paiva: paiva });
    y.kaynnista();
    pelaaEra(y, paiva, {
      valitse(kierros, k, napit) {
        if (kierros !== era.a.r) { return undefined; }
        let ohjattu = -1;
        if (era.a.t === 'oletus') {
          napit.forEach((n, i) => { if (/\bsuositeltu\b/.test(n.className)) { ohjattu = i; } });
        } else {
          const teksti = y.$('ansaTodiste').textContent;
          const ajatus = k.kn === 'ajatus';
          NIMET.forEach((nimi, i) => {
            if (teksti.indexOf(i === 0 && ajatus ? 'Pätevä päättely' : nimi) > 0) { ohjattu = i; }
          });
        }
        tarkistettu++;
        if (ohjattu === -1 || ohjattu === LAJI_INDEKSI[k.l]) { oikeaan++; }
        return ohjattu === -1 ? undefined : ohjattu;   // seurataan ohjausta
      }
    });
    if (y.$('ansaLista').textContent.indexOf('Valitsit sen, mihin sinua ohjattiin') > 0) { raportti++; }
  });
  ok(tarkistettu > 0, 'pankissa on ohjaavia ansoja (' + tarkistettu + ')');
  ok(oikeaan === 0, 'yksikään ohjaus ei osoita oikeaan vastaukseen');
  ok(raportti === tarkistettu, 'ansaraportti kertoo, että ohjausta seurattiin');
}

console.log('\n16. Jakaminen: jakovalikko kun selain tukee, muuten leikepöytä');
{
  let y = teeYmparisto({});
  y.kaynnista();
  pelaaEra(y, 0);
  ok(y.$('jaaNappi').hidden && !y.$('jakoNappi').hidden, 'ilman jakovalikkoa tarjolla on vain kopiointi');

  const jaettu = [];
  y = teeYmparisto({ navigator: {
    share(d) { jaettu.push(d.text); return Promise.resolve(); },
    clipboard: { writeText() { return Promise.resolve(); } }
  } });
  y.kaynnista();
  const t = pelaaEra(y, 0);
  ok(!y.$('jaaNappi').hidden, 'jakonappi näkyy kun selain tukee jakamista');
  y.$('jaaNappi').click();
  ok(jaettu.length === 1 && jaettu[0] === t.jako, 'jakovalikko saa saman tekstin kuin esikatselu');
}

console.log('\n17. Epokin vaihtuminen nollaa talletuksen');
{
  const vanhat = () => ({
    'peli-tilastot': JSON.stringify({ pelatut: 9, kohtia: 45, luokitusOikein: 40, tehoste: 9, viimeisin: 40, armonpaiva: -99 }),
    'peli-tulokset': JSON.stringify({ 0: { m: 'RRRRR', o: 0, n: [0, 0] } }),
    'peli-nahty': JSON.stringify({ darvo: { p: 3, v: 1 } })
  });

  let selain = Object.assign(vanhat(), { 'peli-epokki': JSON.stringify('2020-01-01') });
  let y = teeYmparisto({ talletus: selain });
  y.kaynnista();
  ok(!selain['peli-tilastot'] && !selain['peli-tulokset'] && !selain['peli-nahty'],
     'eri epokin talletus poistetaan');
  ok(JSON.parse(selain['peli-epokki']) === PANKKI.epokki, 'uusi epokki kirjataan');
  ok(!y.$('aloitus').hidden && y.$('tehosteRivi').hidden, 'peli alkaa puhtaalta pöydältä');

  // Talletus ajalta ennen epokkisidontaa: avainta ei ole lainkaan.
  selain = vanhat();
  y = teeYmparisto({ talletus: selain });
  y.kaynnista();
  ok(!selain['peli-tilastot'], 'epokkimerkitsemätön vanha talletus poistetaan myös');

  // Sama epokki: mitään ei saa kadota.
  selain = Object.assign(vanhat(), { 'peli-epokki': JSON.stringify(PANKKI.epokki) });
  y = teeYmparisto({ talletus: selain });
  y.kaynnista();
  ok(JSON.parse(selain['peli-tilastot']).pelatut === 9, 'saman epokin talletus säilyy');
}

console.log('\n18. Vinoumat: "Oma pää" on oikea vastaus, ja kanava ei paljasta sitä');
{
  const vinoumia = PANKKI.kohdat.filter((k) => k.l === 'vinouma').length;
  ok(vinoumia / PANKKI.kohdat.length >= 0.15,
     'vinoumia ' + vinoumia + '/' + PANKKI.kohdat.length + ' (≥15 %) — keskimmäinen nappi ei ole aina väärä');
  const ajatus = PANKKI.kohdat.filter((k) => k.kn === 'ajatus');
  const lajit = new Set(ajatus.map((k) => k.l));
  ok(lajit.size === 3, 'ajatuskanavassa on kaikkia kolmea lajia (' + Array.from(lajit).sort().join(', ') + ')');
  ok(PANKKI.kohdat.every((k) => k.l !== 'vinouma' || k.kn === 'ajatus'),
     'jokainen vinouma on oma ajatus');

  // Pelataan erä, jossa on vinouma, ja katsotaan mitä paljastus sanoo.
  const paiva = PANKKI.erat.findIndex((e) => e.k.some((i) => PANKKI.kohdat[i].l === 'vinouma'));
  let y = teeYmparisto({ paiva: paiva });
  y.kaynnista();
  const nahty = { otsikko: '', teksti: '', kysymys: '' };
  const t = pelaaEra(y, paiva, {
    valitse(kierros, k) { if (k.l === 'vinouma') { nahty.kysymysEnnen = y.$('kysymys').textContent; } return undefined; },
    paljastuksessa(kierros, k) {
      if (k.l !== 'vinouma' || nahty.otsikko) { return; }
      nahty.otsikko = y.$('sanotOtsikko').textContent;
      nahty.teksti = y.$('pSanot').textContent;
      nahty.menetelma = k.p[2];
    }
  });
  ok(t.luokitus === '5/5' && t.ruudukko.every((m) => m === '\u{1F7E9}'),
     'vinoumaerä menee vihreäksi oikeilla vastauksilla (#' + (paiva + 1) + ')');
  ok(nahty.otsikko === 'Mitä teet', 'vinouman vastakeino on otsikolla "Mitä teet"');
  ok(nahty.teksti === nahty.menetelma && nahty.teksti.charAt(0) !== '"',
     'menetelmä näytetään ilman lainausmerkkejä');

  // Lajisekaannus: vinouma merkitään jonkun tempuksi.
  y = teeYmparisto({ paiva: paiva });
  y.kaynnista();
  let tuomio = '';
  pelaaEra(y, paiva, {
    valitse: (kierros, k) => (k.l === 'vinouma' ? 2 : undefined),
    paljastuksessa(kierros, k) { if (k.l === 'vinouma' && !tuomio) { tuomio = y.$('tuomio').textContent; } }
  });
  ok(tuomio.indexOf('Laji meni väärin') === 0 && tuomio.indexOf('oma pää') > 0,
     'vinouman merkitseminen tempuksi saa oman tuomionsa');
  ok(y.$('erotteluEra').textContent.indexOf('laji sekaisin') > 0, 'ja se näkyy erän erottelurivillä');

  // Rehellinen ajatus ei ole "viesti".
  const reh = PANKKI.erat.findIndex((e) => e.k.some((i) =>
    PANKKI.kohdat[i].l === 'rehellinen' && PANKKI.kohdat[i].kn === 'ajatus'));
  y = teeYmparisto({ paiva: reh });
  y.kaynnista();
  let nimi = '';
  pelaaEra(y, reh, {
    valitse(kierros, k, napit) {
      if (k.l === 'rehellinen' && k.kn === 'ajatus') { nimi = napit[0].children[1].textContent; }
      return undefined;
    }
  });
  ok(nimi === 'Pätevä päättely', 'kunnossa oleva ajatus on "Pätevä päättely", ei "Tavallinen viesti"');
}

console.log('\n' + (virheita ? '✗ ' + virheita + ' VIRHETTÄ' : '✓ KAIKKI LÄPI'));
process.exit(virheita ? 1 : 0);
