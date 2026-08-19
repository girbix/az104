/* Verifica i parametri e l'estrazione della simulazione, contro l'esame reale.
 *
 *     node test_esame.js ["<cartella AZ-104>"]
 *
 * L'esame vero (associate role-based senza lab) dura 100 minuti, ha 40-60
 * domande e la soglia e' 700/1000: qui si controlla che il simulatore dichiari
 * gli stessi numeri e che l'estrazione pesata li rispetti davvero.
 * Riferimento: learn.microsoft.com/credentials/support/exam-duration-exam-experience
 */
const fs = require("fs"), path = require("path"), vm = require("vm");

const base = process.argv[2] || path.resolve(__dirname, "..");
const html = fs.readFileSync(path.join(base, "simulatore.html"), "utf8");
const banca = JSON.parse(
  fs.readFileSync(path.join(base, "banca", "az104_question_bank_it.json"), "utf8"));

let errori = 0;
const ko = (m) => { console.log(`  FAIL  ${m}`); errori++; };
const ok = (m) => console.log(`  ok    ${m}`);
const info = (m) => console.log(`  info  ${m}`);

/* ---- 1. i parametri dichiarati nella pagina ---- */
const cost = html.match(/const EXAM_N = (\d+), EXAM_MIN = (\d+), PASS = (\d+);/);
if (!cost) { ko("costanti EXAM_N / EXAM_MIN / PASS non trovate"); process.exit(1); }
const [, N, MIN, PASS] = cost.map(Number);

MIN === 100 ? ok(`durata ${MIN} minuti, come l'esame reale`)
            : ko(`durata ${MIN} minuti: l'esame reale ne dura 100`);
N >= 40 && N <= 60 ? ok(`${N} domande, dentro la forbice reale 40-60`)
                   : ko(`${N} domande: fuori dalla forbice reale 40-60`);
PASS === 700 ? ok(`soglia ${PASS}/1000, come l'esame reale`)
             : ko(`soglia ${PASS}: l'esame reale passa a 700/1000`);

/* Il timer deve partire dal valore dichiarato, non da un numero scritto a mano. */
/end:\s*Date\.now\(\) \+ EXAM_MIN \* 60000/.test(html)
  ? ok("il timer parte da EXAM_MIN, non da una costante duplicata")
  : ko("il timer non usa EXAM_MIN: durata e conto alla rovescia possono divergere");

/* ---- 2. i pesi ufficiali ---- */
const UFFICIALI = {
  "Manage Azure identities and governance": [20, 25],
  "Implement and manage storage": [15, 20],
  "Deploy and manage Azure compute resources": [20, 25],
  "Implement and manage virtual networking": [15, 20],
  "Monitor and maintain Azure resources": [10, 15],
};

const ctx = { console };
vm.createContext(ctx);
const pezzi = ["const DOMAINS = [", "const WEIGHTS = {", "function allocate(n){"];
let src = "";
for (const p of pezzi) {
  const i = html.indexOf(p);
  if (i < 0) { ko(`blocco non trovato: ${p}`); process.exit(1); }
  const fine = p.startsWith("function")
    ? html.indexOf("\n}", i) + 2
    : html.indexOf("\n", html.indexOf(p.endsWith("[") ? "];" : "};", i)) ;
  src += html.slice(i, fine) + "\n";
}
vm.runInContext(
  `let BANK = ${JSON.stringify(banca.map(q => ({ dominio: q.dominio })))};` +
  src + "\nglobalThis.__api = { DOMAINS, WEIGHTS, allocate };", ctx);
const { DOMAINS, WEIGHTS, allocate } = ctx.__api;

for (const d of DOMAINS) {
  const [lo, hi] = UFFICIALI[d] || [];
  if (lo == null) { ko(`dominio non riconosciuto: ${d}`); continue; }
  const w = WEIGHTS[d];
  w >= lo && w <= hi
    ? ok(`peso ${w}% dentro l'intervallo ufficiale ${lo}-${hi}%  ·  ${d}`)
    : ko(`peso ${w}% fuori dall'intervallo ufficiale ${lo}-${hi}%  ·  ${d}`);
}

/* ---- 3. l'estrazione reale ---- */
const alloc = allocate(N);
const totale = DOMAINS.reduce((s, d) => s + (alloc[d] || 0), 0);
totale === N ? ok(`l'estrazione compone esattamente ${N} domande`)
             : ko(`l'estrazione compone ${totale} domande invece di ${N}`);

console.log("\n  Composizione della prova:");
for (const d of DOMAINS) {
  const n = alloc[d] || 0, p = n / totale * 100;
  const [lo, hi] = UFFICIALI[d];
  const dentro = p >= lo && p <= hi;
  console.log(`    ${String(n).padStart(2)}  ${p.toFixed(1).padStart(5)}%  ` +
              `${dentro ? "  " : "!!"}  (uff. ${lo}-${hi}%)  ${d}`);
  if (!dentro) ko(`la quota estratta per "${d}" (${p.toFixed(1)}%) esce dall'intervallo ufficiale`);
}

/* Ogni dominio deve avere abbastanza domande in banca per la sua quota. */
for (const d of DOMAINS) {
  const disp = banca.filter(q => q.dominio === d).length;
  if (disp < (alloc[d] || 0)) ko(`banca insufficiente per "${d}": ${disp} disponibili, ${alloc[d]} richieste`);
}

/* ---- 4. il punteggio ---- */
/EX\.score = Math\.round\(ok \/ EX\.qs\.length \* 1000\)/.test(html)
  ? ok("punteggio scalato su 1000 sul totale effettivo della prova")
  : ko("il calcolo del punteggio non e' quello atteso");
/const pass = EX\.score >= PASS/.test(html)
  ? ok("l'esito confronta il punteggio con PASS")
  : ko("l'esito non usa la costante PASS");

/* ---- 5. il ritorno utile: cosa ripassare ---- */
/Categorie da ripassare/.test(html)
  ? ok("il risultato elenca le categorie da ripassare")
  : ko("manca l'elenco delle categorie da ripassare");
/sub:q\.sotto_argomento|sub: ?q\.sotto_argomento/.test(html)
  ? ok("il sotto-argomento arriva fino al risultato")
  : ko("il sotto-argomento non viene propagato nei risultati");
/Esito per dominio/.test(html)
  ? ok("il risultato elenca l'esito per dominio")
  : ko("manca l'esito per dominio");

/* ---- 4. errori e domande in bianco sono due segnali diversi ----
   Chi si ferma a meta' prova lascia decine di domande in bianco. Se contano
   come errori, il pannello "categorie da ripassare" gli dice di riaprire trenta
   lezioni su cui non ha nemmeno letto la domanda — e il primo effetto e' che
   smette di fidarsi del pannello.
   Lo scenario provato qui e' reale: 50 domande, abbandono alla diciottesima. */
console.log("\nCategorie da ripassare:");
{
  const m = html.match(/function categorieDaRipassare\(results\)\{[\s\S]*?\n\}/);
  if (!m) {
    ko("categorieDaRipassare() non trovata nella pagina");
  } else {
    const ctx = { console };
    vm.createContext(ctx);
    vm.runInContext(m[0], ctx);
    const calcola = ctx.categorieDaRipassare;

    /* 6 giuste e 12 sbagliate fra le prime 18, le altre 32 mai aperte */
    const risultati = [];
    const dove = (i) => (i < 18 ? "Risposte " + (i % 4) : "Mai viste " + (i % 9));
    for (let i = 0; i < 50; i++) {
      risultati.push(i < 18
        ? { sub: dove(i), dominio: "Compute", ok: i % 3 === 0, blank: false }
        : { sub: dove(i), dominio: "Compute", ok: false, blank: true });
    }

    const cat = calcola(risultati);
    const conta = (f) => cat.reduce((t, [, s]) => t + f(s), 0);

    conta((s) => s.ko) === 12
      ? ok("conta 12 sbagliate, quelle a cui hai davvero risposto")
      : ko(`conta ${conta((s) => s.ko)} sbagliate invece di 12`);
    conta((s) => s.blank) === 32
      ? ok("conta 32 in bianco, tenute separate")
      : ko(`conta ${conta((s) => s.blank)} in bianco invece di 32`);

    /* la cosa che conta: chi ha sbagliato viene prima di chi non c'e' arrivato */
    const primoVuoto = cat.findIndex(([, s]) => s.ko === 0);
    const ultimoErrore = cat.map(([, s]) => s.ko > 0).lastIndexOf(true);
    primoVuoto === -1 || ultimoErrore < primoVuoto
      ? ok("le categorie sbagliate stanno sopra quelle lasciate in bianco")
      : ko("una categoria mai aperta compare sopra una che hai sbagliato davvero");

    const soloBianche = cat.filter(([, s]) => s.ko === 0 && s.blank > 0);
    soloBianche.length > 0
      ? ok(`${soloBianche.length} categorie compaiono come "non ci sei arrivato"`)
      : ko("le categorie mai aperte spariscono: nessun segnale su cosa manca");

    /* nessuna categoria pulita deve finire nell'elenco */
    cat.every(([, s]) => s.ko > 0 || s.blank > 0)
      ? ok("nessuna categoria senza errori nell'elenco")
      : ko("nell'elenco c'e' una categoria in cui non hai sbagliato niente");

    /* e la pagina deve saperlo dire, non solo calcolarlo */
    /non ci sei arrivato/.test(html)
      ? ok("la pagina distingue a parole «non ci sei arrivato» da «tutte sbagliate»")
      : ko("la pagina chiama ancora «tutte sbagliate» anche le domande mai aperte");
    /a cui hai risposto/.test(html)
      ? ok("il riepilogo mostra anche la percentuale sulle domande date")
      : ko("il riepilogo mostra solo la percentuale grezza sulle 50");
  }
}

const sotto = new Set(banca.map(q => q.sotto_argomento).filter(Boolean));
info(`${sotto.size} sotto-argomenti distinti in banca`);

console.log(errori === 0
  ? `\nTutto verde: la simulazione rispecchia l'esame reale (${N} domande, ${MIN} minuti, soglia ${PASS}).`
  : `\n${errori} problemi da correggere.`);
process.exit(errori ? 1 : 0);
