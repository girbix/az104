/* Verifica az104_ripasso.html: estrae il payload dalla pagina costruita e
 * ricontrolla che sia integro e coerente con la banca di partenza.
 *
 *     node test_ripasso.js "<cartella AZ-104>"
 *
 * Non sostituisce una prova in un browser, ma copre l'errore piu' probabile:
 * un payload che non fa il parse, o risposte perse per strada nella conversione.
 */
const fs = require("fs");
const path = require("path");

const base = process.argv[2] || path.resolve(__dirname, "..");

/* Si controlla la pagina PUBBLICATA, quella che index.html collega: ripasso.html
   nella radice, con la banca in banca/. I nomi lunghi sono il ripiego per una
   pagina appena costruita e non ancora pubblicata.
   L'ordine conta: nel repo puo' esistere un az104_ripasso.html rimasto indietro
   da una build vecchia, e provare quello lascerebbe passare un deploy rotto. */
const scegli = (...cand) => {
  const hit = cand.find((p) => fs.existsSync(p));
  if (!hit) {
    console.error(`file non trovato, cercato:\n  ${cand.join("\n  ")}`);
    process.exit(1);
  }
  return hit;
};

const fPagina = scegli(
  path.join(base, "ripasso.html"),
  path.join(base, "az104_ripasso.html"));
const fBanca = scegli(
  path.join(base, "banca", "az104_question_bank_it.json"),
  path.join(base, "az104_question_bank_it.json"));
console.log(`  usa   ${path.basename(fPagina)} contro ${path.relative(base, fBanca)}`);
const html = fs.readFileSync(fPagina, "utf8");
const banca = JSON.parse(fs.readFileSync(fBanca, "utf8"));

let errori = 0;
const ko = (m) => { console.log(`  FAIL  ${m}`); errori++; };
const ok = (m) => console.log(`  ok    ${m}`);

// 1. Il payload si estrae e fa il parse.
// Il payload sta tutto su una riga: senza il flag /s il punto non attraversa
// il newline, quindi il match resta dentro quella riga (e CRLF non disturba).
const m = html.match(/const BANCA = (\[.*\]);/);
if (!m) { ko("payload non trovato nella pagina"); process.exit(1); }

let dati;
try {
  dati = JSON.parse(m[1]);
  ok(`payload valido, ${dati.length} domande`);
} catch (e) {
  ko(`payload non fa il parse: ${e.message}`);
  process.exit(1);
}

// 2. Nessuna domanda persa, id allineati.
dati.length === banca.length ? ok("nessuna domanda persa") : ko(`${banca.length} in banca, ${dati.length} in pagina`);
const idBanca = banca.map((q) => q.id).join("|");
const idPagina = dati.map((q) => q.id).join("|");
idBanca === idPagina ? ok("id allineati e nello stesso ordine") : ko("gli id divergono dalla banca");

// 3. Nessun </script> letterale: chiuderebbe il tag e romperebbe la pagina.
const corpo = m[1];
!corpo.includes("</script") ? ok("nessun </script> letterale nel payload") : ko("il payload contiene </script>");

// 4. Ogni domanda ha una risposta utilizzabile.
for (const d of dati) {
  if (d.t === "hotspot") {
    if (!d.o.length) ko(`${d.id}: hotspot senza menu`);
    for (const menu of d.o) {
      if (!menu.k) ko(`${d.id}: menu senza risposta -> ${menu.l}`);
      if (menu.c.length && !menu.c.includes(menu.k)) ko(`${d.id}: risposta "${menu.k}" non e' tra le scelte`);
      if (menu.c.length < 2) ko(`${d.id}: menu con meno di 2 scelte -> ${menu.l}`);
    }
  } else if (d.t === "yes_no_series") {
    if (d.a.length !== d.o.length) ko(`${d.id}: ${d.o.length} affermazioni, ${d.a.length} risposte`);
    for (const v of d.a) if (!["Yes", "No"].includes(v)) ko(`${d.id}: verdetto inatteso "${v}"`);
  } else if (d.t === "drag_drop") {
    if (new Set(d.a).size !== d.a.length) ko(`${d.id}: posizione ripetuta`);
    for (const l of d.a) {
      const i = "abcde".indexOf(l);
      if (i < 0 || i >= d.o.length) ko(`${d.id}: la sequenza punta a "${l}" che non esiste`);
    }
  } else {
    if (!d.a.length) ko(`${d.id}: nessuna risposta`);
    for (const l of d.a) {
      const i = "abcde".indexOf(l);
      if (i < 0 || i >= d.o.length) ko(`${d.id}: risposta "${l}" fuori dalle opzioni`);
    }
    if (d.t === "multiple_choice" && d.a.length !== 1) ko(`${d.id}: scelta singola con ${d.a.length} risposte`);
  }
  if (!d.q || !d.e) ko(`${d.id}: domanda o spiegazione vuota`);
  if (!/^https:\/\/learn\.microsoft\.com/.test(d.u)) ko(`${d.id}: url non punta a Learn -> ${d.u}`);
}
if (!errori) ok("tutte le risposte sono risolvibili e puntano a Learn");

// 5. Le hotspot con virgole nei valori: il caso che aveva rotto il simulatore.
const virgolose = dati.filter((d) => d.t === "hotspot" && d.o.some((x) => x.k && x.k.includes(",")));
console.log(`  info  ${virgolose.length} hotspot con virgole dentro un valore (il caso fragile)`);
for (const d of virgolose) {
  for (const menu of d.o) {
    if (menu.k && !menu.c.includes(menu.k)) ko(`${d.id}: valore con virgola mal risolto -> ${menu.k}`);
  }
}

// 6. Confronto a campione con la banca: la risposta mostrata deve derivare dall'originale.
for (const d of dati) {
  const q = banca.find((x) => x.id === d.id);
  if (d.t === "hotspot") {
    for (const menu of d.o) {
      if (menu.k && !q.risposta_corretta.includes(menu.k)) ko(`${d.id}: "${menu.k}" non e' nella risposta originale`);
    }
  } else if (d.t !== "yes_no_series" && d.t !== "drag_drop") {
    const orig = q.risposta_corretta.split(",").map((s) => s.trim().toLowerCase()).sort().join(",");
    if ([...d.a].sort().join(",") !== orig) ko(`${d.id}: risposta divergente -> ${d.a} vs ${orig}`);
  }
}
if (!errori) ok("ogni risposta risale alla banca originale");

console.log(errori ? `\n${errori} ERRORI\n` : `\nTutto verde: ${dati.length}/${dati.length}\n`);
process.exit(errori ? 1 : 0);
