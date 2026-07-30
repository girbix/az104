/* Verifica la cartella telefono/: i file devono essere autosufficienti offline.
 *
 *     node test_telefono.js "<cartella AZ-104>"
 */
const fs = require("fs");
const path = require("path");

const base = process.argv[2];
if (!base) {
  console.error("uso: node test_telefono.js <cartella AZ-104>");
  process.exit(1);
}
const dir = path.join(base, "telefono");

let errori = 0;
const ko = (m) => { console.log(`  FAIL  ${m}`); errori++; };
const ok = (m) => console.log(`  ok    ${m}`);

// ---------------------------------------------------------------- simulatore
console.log("simulatore.html");
const sim = fs.readFileSync(path.join(dir, "simulatore.html"), "utf8");

// 1. Nessun aggancio residuo all'ambiente artifact.
!/window\.storage/.test(sim)
  ? ok("nessun riferimento a window.storage")
  : ko("c'e' ancora window.storage: offline non persisterebbe");

// 2. La banca e' dentro il file e fa il parse.
const m = sim.match(/const BANCA_INCLUSA = (\[.*\]);/);
if (!m) {
  ko("banca non inclusa nel file");
} else {
  try {
    const banca = JSON.parse(m[1]);
    banca.length === 532 ? ok(`banca inclusa, ${banca.length} domande`) : ko(`${banca.length} domande invece di 532`);
    const conRisposta = banca.filter((q) => q.risposta_corretta && q.domanda).length;
    conRisposta === banca.length ? ok("ogni domanda ha testo e risposta") : ko(`${banca.length - conRisposta} domande incomplete`);
  } catch (e) {
    ko(`la banca inclusa non fa il parse: ${e.message}`);
  }
}

// 3. Il boot non passa piu' dalla schermata di caricamento file.
/BANK = normalizeBank\(BANCA_INCLUSA\)/.test(sim)
  ? ok("parte dritto sulla banca inclusa")
  : ko("il boot non usa la banca inclusa");

// 4. Niente pulsante che offline svuoterebbe la banca senza modo di ricaricarla.
!/Cambia banca domande/.test(sim)
  ? ok("via il pulsante che svuoterebbe la banca")
  : ko("il pulsante 'Cambia banca domande' e' ancora li'");

// 5. localStorage usato davvero.
/localStorage\.setItem/.test(sim) && /localStorage\.getItem/.test(sim)
  ? ok("persistenza su localStorage")
  : ko("localStorage non usato");

// 6. Nessuna risorsa esterna: offline deve funzionare senza rete.
const esterne = [...sim.matchAll(/(?:src|href)\s*=\s*["'](https?:)?\/\/[^"']+/gi)]
  .map((x) => x[0])
  .filter((x) => !/learn\.microsoft\.com/.test(x));
esterne.length === 0
  ? ok("nessuna risorsa esterna da caricare")
  : ko(`${esterne.length} risorse esterne: ${esterne.slice(0, 3).join(", ")}`);

// ---------------------------------------------------------------- ripasso
console.log("\nripasso.html");
const rip = fs.readFileSync(path.join(dir, "ripasso.html"), "utf8");
const mr = rip.match(/const BANCA = (\[.*\]);/);
if (!mr) ko("payload non trovato");
else {
  try {
    const d = JSON.parse(mr[1]);
    d.length === 532 ? ok(`${d.length} domande incluse`) : ko(`${d.length} domande invece di 532`);
  } catch (e) { ko(`payload non fa il parse: ${e.message}`); }
}
const ripEsterne = [...rip.matchAll(/(?:src|href)\s*=\s*["'](https?:)?\/\/[^"']+/gi)]
  .map((x) => x[0])
  .filter((x) => !/learn\.microsoft\.com/.test(x));
ripEsterne.length === 0 ? ok("nessuna risorsa esterna") : ko(`${ripEsterne.length} risorse esterne`);

// ---------------------------------------------------------------- indice
console.log("\nindex.html");
const idxPath = path.join(dir, "index.html");
if (!fs.existsSync(idxPath)) {
  ko("index.html manca");
} else {
  const idx = fs.readFileSync(idxPath, "utf8");
  // I link devono essere relativi: su file:// un assoluto punterebbe alla radice del telefono.
  const rotti = [...idx.matchAll(/href\s*=\s*["'](\/[^"'/][^"']*)["']/g)].map((x) => x[1]);
  rotti.length === 0 ? ok("nessun link assoluto") : ko(`link assoluti che su file:// non vanno: ${rotti.join(", ")}`);
  for (const f of ["simulatore.html", "ripasso.html"]) {
    idx.includes(f) ? ok(`collega ${f}`) : ko(`non collega ${f}`);
  }
}

// ---------------------------------------------------------------- CSV per Anki

/* Parser CSV con quoting: il CSV delle domande e' QUOTE_ALL perche' i testi
 * contengono ';' e virgolette, quindi contare i separatori non basta. */
function parseCSV(testo, delim) {
  const righe = [];
  let campo = "", riga = [], inQuote = false;
  for (let i = 0; i < testo.length; i++) {
    const c = testo[i];
    if (inQuote) {
      if (c === '"') {
        if (testo[i + 1] === '"') { campo += '"'; i++; }
        else inQuote = false;
      } else campo += c;
    } else if (c === '"') inQuote = true;
    else if (c === delim) { riga.push(campo); campo = ""; }
    else if (c === "\n") { riga.push(campo); righe.push(riga); riga = []; campo = ""; }
    else if (c !== "\r") campo += c;
  }
  if (campo || riga.length) { riga.push(campo); righe.push(riga); }
  return righe.filter((r) => r.length > 1 || (r[0] && r[0].trim()));
}

function testataDi(testo) {
  return testo.split(/\r?\n/).filter((r) => r.startsWith("#"));
}

console.log("\nflashcard atomiche");
for (const f of fs.readdirSync(dir).filter((x) => /^az104_flashcard_.*\.csv$/.test(x))) {
  const testo = fs.readFileSync(path.join(dir, f), "utf8");
  const righe = testo.split(/\r?\n/).filter((r) => r.trim() && !r.startsWith("#"));
  const male = righe.filter((r) => (r.match(/;/g) || []).length !== 2);
  male.length === 0 ? ok(`${f}: ${righe.length} card, tutte a 3 campi`) : ko(`${f}: ${male.length} righe malformate`);
  const t = testataDi(testo);
  t.includes("#separator:Semicolon") ? ok(`${f}: separatore dichiarato`) : ko(`${f}: manca #separator`);
  t.includes("#html:true") ? ok(`${f}: html attivo`) : ko(`${f}: manca #html:true`);
  t.some((x) => x.startsWith("#deck:")) ? ok(`${f}: mazzo dichiarato`) : ko(`${f}: manca #deck`);
}

console.log("\ndomande come mazzo Anki");
const fd = path.join(dir, "az104_domande_esame.csv");
if (!fs.existsSync(fd)) {
  ko("az104_domande_esame.csv manca");
} else {
  const testo = fs.readFileSync(fd, "utf8");
  const t = testataDi(testo);
  for (const dir_ of ["#separator:Semicolon", "#html:true", "#tags column:3", "#deck column:4", "#notetype:Basic"]) {
    t.includes(dir_) ? ok(`direttiva ${dir_}`) : ko(`manca la direttiva ${dir_}`);
  }
  const corpo = testo.split(/\r?\n/).filter((r) => !r.startsWith("#")).join("\n");
  const righe = parseCSV(corpo, ";");
  righe.length === 532 ? ok(`${righe.length} card`) : ko(`${righe.length} card invece di 532`);

  const male = righe.filter((r) => r.length !== 4);
  male.length === 0 ? ok("ogni card ha 4 campi") : ko(`${male.length} card con ${male[0] && male[0].length} campi invece di 4`);

  const vuote = righe.filter((r) => !r[0] || !r[1]);
  vuote.length === 0 ? ok("nessun fronte o retro vuoto") : ko(`${vuote.length} card con fronte o retro vuoto`);

  const deckStorti = righe.filter((r) => !/^AZ104::Domande::0[1-5] /.test(r[3]));
  deckStorti.length === 0 ? ok("tutte nei mazzi AZ104::Domande::") : ko(`${deckStorti.length} card con mazzo storto: ${deckStorti[0] && deckStorti[0][3]}`);

  // I tag Anki sono separati da spazi: uno con spazi interni si spezzerebbe.
  const tagStorti = righe.filter((r) => !r[2].split(" ").every((x) => /^[a-z0-9-]+$/.test(x)));
  tagStorti.length === 0 ? ok("tag validi per Anki") : ko(`${tagStorti.length} card con tag storti: ${tagStorti[0] && tagStorti[0][2]}`);

  const daRivedere = righe.filter((r) => r[2].includes("da-rivedere")).length;
  daRivedere === 502 ? ok(`${daRivedere} card taggate da-rivedere`) : ko(`${daRivedere} da-rivedere invece di 502`);

  const mazzi = [...new Set(righe.map((r) => r[3]))].sort();
  mazzi.length === 5 ? ok(`5 mazzi per dominio`) : ko(`${mazzi.length} mazzi invece di 5`);
}

// ---------------------------------------------------------------- peso
console.log("\npeso totale");
let tot = 0;
for (const f of fs.readdirSync(dir)) tot += fs.statSync(path.join(dir, f)).size;
console.log(`  info  ${(tot / 1024 / 1024).toFixed(1)} MB da copiare sul telefono`);

console.log(errori ? `\n${errori} ERRORI\n` : `\nTutto verde: la cartella funziona offline.\n`);
process.exit(errori ? 1 : 0);
