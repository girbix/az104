/* Extracts the real answer-logic from simulatore.html and exercises it against every
   authored question: does submitting the documented correct answer actually grade as
   correct, is that answer even selectable in the UI, and does a wrong answer fail? */
const fs = require("fs"), path = require("path"), vm = require("vm");

/* Le pagine stanno nella radice del repo, gli script qui dentro in build/. */
const BASE = path.resolve(__dirname, "..");
const html = fs.readFileSync(path.join(BASE, "simulatore.html"), "utf8");

const start = html.indexOf("/* ============================================================ answer logic */");
const end = html.indexOf("/* ============================================================ helpers */");
if (start < 0 || end < 0) { console.error("markers not found"); process.exit(1); }
const src = html.slice(start, end);

const ctx = { console };
vm.createContext(ctx);
// stubs for the two model bindings the answer logic depends on
vm.runInContext(
  "let U={override:{}}; const correctOf = q => q.risposta_corretta;" + src +
  "\nglobalThis.__api = {grade, hotspotKeys, optionsOf, parseHotspot, norm, splitAns};", ctx);
const { grade, hotspotKeys, optionsOf, parseHotspot, norm, splitAns } = ctx.__api;

const TARGET = process.argv[2] || path.join(BASE, "banca", "az104_question_bank_it.json");
let all = JSON.parse(fs.readFileSync(TARGET,"utf8")).map(q=>{q._f=path.basename(TARGET);return q;});

const fail = { unselectable: [], notCorrect: [], wrongPasses: [] };
let tested = 0;

/* Build the answer a user would produce by picking the documented-correct choices. */
function correctAnswerFor(q) {
  const opts = optionsOf(q);
  switch (q.tipo) {
    case "multiple_response": return splitAns(q.risposta_corretta);
    case "yes_no_series": return splitAns(q.risposta_corretta).map(v => v === "yes" ? "Yes" : "No");
    /* Il widget tiene sempre in stato l'elenco completo: le azioni richieste
       in testa, i distrattori sotto la linea. */
    case "drag_drop": {
      const key = splitAns(q.risposta_corretta);
      return [...key, ...opts.map(o => o.key).filter(k => !key.includes(k))];
    }
    case "hotspot": {
      const want = hotspotKeys(q);
      const specs = opts.map(o => parseHotspot(o.text));
      return want.map((w, i) => {
        const hit = (specs[i].choices || []).find(c => norm(c) === w);
        if (!hit) fail.unselectable.push([q._f, q.id || q.domanda.slice(0, 45), specs[i].label, w]);
        return hit != null ? hit : w;
      });
    }
    default: return q.risposta_corretta;
  }
}
/* A deliberately different answer, to prove grade() isn't just returning true. */
function wrongAnswerFor(q) {
  const opts = optionsOf(q);
  switch (q.tipo) {
    case "multiple_response": {
      const key = splitAns(q.risposta_corretta);
      const other = opts.map(o => o.key).filter(k => !key.includes(k));
      return other.length ? [other[0]] : [key[0]];
    }
    case "yes_no_series": return splitAns(q.risposta_corretta).map(v => v === "yes" ? "No" : "Yes");
    case "drag_drop": {
      const key = splitAns(q.risposta_corretta);
      const full = [...key, ...opts.map(o => o.key).filter(k => !key.includes(k))];
      return full.length > 1 ? [full[1], full[0], ...full.slice(2)] : full;
    }
    case "hotspot": {
      const specs = opts.map(o => parseHotspot(o.text));
      const want = hotspotKeys(q);
      return want.map((w, i) => {
        const alt = (specs[i].choices || []).find(c => norm(c) !== w);
        return alt != null ? alt : w;
      });
    }
    default: {
      const key = norm(q.risposta_corretta);
      const other = opts.map(o => o.key).find(k => k !== key);
      return other != null ? other : key;
    }
  }
}

for (const q of all) {
  if (!q.domanda || !q.risposta_corretta) continue;
  tested++;
  const good = correctAnswerFor(q);
  if (grade(q, good) !== true) fail.notCorrect.push([q._f, q.tipo, q.id || q.domanda.slice(0, 45), JSON.stringify(q.risposta_corretta).slice(0, 70)]);
  const bad = wrongAnswerFor(q);
  if (JSON.stringify(bad) !== JSON.stringify(good) && grade(q, bad) === true)
    fail.wrongPasses.push([q._f, q.tipo, q.id || q.domanda.slice(0, 45)]);
}

console.log(`Testate ${tested} domande in ${path.basename(TARGET)}\n`);
const show = (name, arr) => {
  console.log(`${name}: ${arr.length}`);
  arr.slice(0, 6).forEach(r => console.log("   -", r.join(" | ")));
  if (arr.length > 6) console.log(`   ... e altre ${arr.length - 6}`);
};
show("La risposta corretta NON viene valutata corretta", fail.notCorrect);
show("Valore hotspot corretto NON selezionabile nel menu", fail.unselectable);
show("Una risposta ERRATA viene accettata come corretta", fail.wrongPasses);

const bad = fail.notCorrect.length + fail.unselectable.length + fail.wrongPasses.length;
console.log(bad === 0 ? "\nOK: logica di valutazione coerente con i dati." : `\n${bad} problemi da correggere.`);
