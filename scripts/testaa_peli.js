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

  let talletus = {};
  const localStorage = {
    getItem(k) {
      if (asetukset.storageHeittaa) { throw new Error('yksityinen ikkuna'); }
      return Object.prototype.hasOwnProperty.call(talletus, k) ? talletus[k] : null;
    },
    setItem(k, v) {
      if (asetukset.storageHeittaa) { throw new Error('yksityinen ikkuna'); }
      talletus[k] = String(v);
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
  // estäisi tulevien erien testaamisen.
  const nyt = new Date(2026, 7, 23 + (asetukset.paiva || 0), 12, 0, 0);
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
    { clipboard: { writeText() { return Promise.resolve(); } } },
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
    napit[valinnat.vaaraLaji ? (LAJI_INDEKSI[k.l] + 1) % 3 : LAJI_INDEKSI[k.l]].click();

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
  const eka = teeYmparisto({ paiva: 0 });
  eka.kaynnista();
  pelaaEra(eka, 0);
  ok(eka.$('tTehoste').textContent === '1', 'ensimmäisenä päivänä tehoste on 1');

  // Sama selain, seuraava päivä: erän on vaihduttava.
  const eilen = eraKohdat(0).map((k) => k.id).join();
  const tanaan = eraKohdat(1).map((k) => k.id).join();
  ok(eilen !== tanaan, 'seuraavan päivän erä on eri');

  const toinen = teeYmparisto({ paiva: 1 });
  toinen.kaynnista();
  const t = pelaaEra(toinen, 1);
  ok(/^Vedätys #2 /.test(t.jako), 'toisena päivänä numero on #2');
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
  ok(rikki === 0, 'kaikissa 110 nimeämiskysymyksessä 3 eri vaihtoehtoa ja oikea vastaus mukana');
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

console.log('\n' + (virheita ? '✗ ' + virheita + ' VIRHETTÄ' : '✓ KAIKKI LÄPI'));
process.exit(virheita ? 1 : 0);
