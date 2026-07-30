/* Prova la logica dell'ascolto di studia.html senza un browser.
 *
 *     node test_ascolto.js ["<cartella AZ-104>"]
 *
 * Non puo' verificare che la voce esca dagli altoparlanti. Verifica le due
 * decisioni che si possono sbagliare in silenzio: quali voci vengono offerte
 * (e in che ordine) e come il testo viene spezzato in frasi. Se il taglio
 * sbaglia, l'evidenziazione salta e la lettura si interrompe a meta'.
 */
const fs = require("fs"), path = require("path"), vm = require("vm");

const base = process.argv[2] || path.resolve(__dirname, "..");
const html = fs.readFileSync(path.join(base, "studia.html"), "utf8");

let errori = 0;
const ko = (m) => { console.log(`  FAIL  ${m}`); errori++; };
const ok = (m) => console.log(`  ok    ${m}`);

/* Si estraggono dalla pagina pubblicata, non si riscrivono qui: un test che
   duplica la logica finisce per provare se stesso. */
function estrai(re, nome) {
  const m = html.match(re);
  if (!m) { ko(`non trovo ${nome} in studia.html`); process.exit(1); }
  return m[0];
}
const srcNat = estrai(/const naturale = v => [^;]+;/, "il filtro delle voci naturali");
const srcSort = estrai(/voci\.sort\(\(a, b\) => \{[\s\S]*?\n  \}\);/, "l'ordinamento delle voci");
const srcTaglio = estrai(/n\.nodeValue\.match\(([^)]+)\)/, "il taglio in frasi");

const ctx = { console };
vm.createContext(ctx);
vm.runInContext(srcNat + "\nglobalThis.__nat = naturale;", ctx);
const naturale = ctx.__nat;

/* riproduce la selezione di caricaVoci() usando i pezzi estratti */
function scegli(tutte) {
  const it = tutte.filter(v => /^it\b|^it[-_]/i.test(v.lang));
  const nat = it.filter(naturale);
  let voci = nat.length ? nat : it;
  vm.runInContext("globalThis.__v = " + JSON.stringify(voci) + ";" +
    "var voci = globalThis.__v;" + srcSort + "globalThis.__v = voci;", ctx);
  return ctx.__v;
}

const V = (name, lang, localService) => ({ name, lang, localService });

/* ---- 1. Windows con voci vecchie e naturali insieme ---- */
console.log("Windows, voci legacy + naturali:");
let r = scegli([
  V("Microsoft Elsa - Italian (Italy)", "it-IT", true),
  V("Microsoft Cosimo - Italian (Italy)", "it-IT", true),
  V("Microsoft Isabella Online (Natural) - Italian (Italy)", "it-IT", false),
  V("Microsoft Diego Online (Natural) - Italian (Italy)", "it-IT", false),
  V("Microsoft Zira - English (United States)", "en-US", true),
]);
r.every(v => naturale(v)) ? ok("le voci robotiche non vengono offerte")
                          : ko(`offerta una voce locale: ${r.map(v => v.name)}`);
/^Microsoft Isabella/.test(r[0] ? r[0].name : "")
  ? ok("Isabella e' la prima, quindi la predefinita")
  : ko(`la prima e' ${r[0] && r[0].name}`);
r.every(v => /^it/i.test(v.lang)) ? ok("nessuna voce non italiana") : ko("passata una voce non italiana");

/* ---- 2. sistema con sole voci vecchie: meglio una robotica che il silenzio ---- */
console.log("\nSolo voci legacy:");
r = scegli([V("Microsoft Elsa - Italian (Italy)", "it-IT", true)]);
r.length === 1 ? ok("si ripiega sulla voce disponibile invece di restare muta")
               : ko(`${r.length} voci invece di 1`);

/* ---- 3. nessuna voce italiana ---- */
console.log("\nNessuna voce italiana:");
r = scegli([V("Microsoft Zira - English (United States)", "en-US", true)]);
r.length === 0 ? ok("elenco vuoto, la pagina lo gestisce") : ko("offerta una voce inglese");

/* ---- 4. Android, voci di rete senza 'Natural' nel nome ---- */
console.log("\nAndroid:");
r = scegli([
  V("Italiano Italia", "it-IT", false),
  V("English United States", "en-US", false),
]);
r.length === 1 && r[0].name === "Italiano Italia"
  ? ok("riconosciuta come naturale perche' non locale")
  : ko(`selezione inattesa: ${r.map(v => v.name)}`);

/* ---- 5. il taglio in frasi, sul testo vero delle lezioni ---- */
console.log("\nTaglio in frasi:");
const reTaglio = eval(srcTaglio.match(/match\((.+)\)$/)[1]);
/* Il payload sta tutto su una riga: si taglia a fine riga. Cercare l'ultima
   "];" del file pescherebbe una parentesi del codice piu' sotto. */
const iniz = html.indexOf('[{"o":');
const raw = html.slice(iniz, html.indexOf("\n", iniz)).replace(/;\s*$/, "");
const lezioni = JSON.parse(raw.replace(/<\\\//g, "</"));
console.log(`  (${lezioni.length} lezioni)`);

/* Nella pagina il taglio non lavora sul markdown grezzo ma sui nodi di testo,
   e rendi() ha gia' separato paragrafi ed elenchi in elementi distinti. Qui si
   rifa' la stessa suddivisione, se no si misura una cosa che non accade. */
function blocchi(md) {
  return String(md).split(/\n\n+/).flatMap(b => {
    b = b.trim();
    if (!b || b.startsWith("```")) return [];        // il codice non si legge
    const righe = b.split("\n");
    return righe.every(r => r.trim().startsWith("- "))
      ? righe.map(r => r.trim().slice(2))            // un <li> per riga
      : [righe.join(" ")];                           // un <p>
  }).map(t => t.replace(/[*`]/g, ""));
}

let tot = 0, perse = 0, lunghe = [];
for (const l of lezioni) {
  for (const campo of ["c", "es", "tr"]) {
    for (const blocco of blocchi(l[campo])) {
      const pezzi = blocco.match(reTaglio) || [];
      tot += pezzi.length;
      // niente deve sparire: rimesso insieme deve tornare il blocco di partenza
      if (pezzi.join("") !== blocco) {
        perse++;
        if (perse <= 3) ko(`${l.t}/${campo}: testo perso nel taglio`);
      }
      // Chrome tronca le utterance lunghe: sopra i 300 caratteri si rischia
      pezzi.forEach(p => { if (p.length > 300) lunghe.push(`${l.t}/${campo}: ${p.length}`); });
    }
  }
}
perse === 0 ? ok(`nessun testo perso, ${tot} frasi in tutto`) : ko(`${perse} blocchi perdono testo`);
lunghe.length === 0 ? ok("nessuna frase oltre i 300 caratteri")
                    : ko(`${lunghe.length} frasi troppo lunghe: ${lunghe.slice(0, 3).join(" · ")}`);
console.log(`  info  ${Math.round(tot / lezioni.length)} frasi per lezione in media`);

/* ---- 6. i pezzi che devono esserci nella pagina ---- */
console.log("\nComandi nella pagina:");
[["pausa", /function pausa\(\)/], ["interruzione", /function ferma\(\)/],
 ["evidenziazione", /classList\.add\("leggo"\)/], ["conteggio ascolti", /ascolti\[l\.o\] = \(ascolti\[l\.o\] \|\| 0\) \+ 1/],
 ["stato da ascoltare", /da ascoltare/], ["stato riascolta", /↻ Riascolta/]
].forEach(([nome, re]) => re.test(html) ? ok(nome) : ko(`manca: ${nome}`));

console.log(errori === 0 ? "\nTutto verde: selezione voci e taglio in frasi coerenti."
                         : `\n${errori} problemi.`);
process.exit(errori ? 1 : 0);
