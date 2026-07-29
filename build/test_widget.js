/* Disegna il widget di risposta di OGNI domanda, in entrambi gli stati.
 *
 *     node test_widget.js ["<cartella AZ-104>"]
 *
 * Gli altri test controllano la valutazione: se rispondi giusto, ti conta giusto.
 * Questo controlla che la domanda si riesca a *vedere* — un widget che va in
 * eccezione lascia la pagina bianca, e la valutazione non ci arriva nemmeno.
 * Serve un DOM finto: quel tanto che basta ad answerUI, senza browser.
 */
const fs = require("fs"), path = require("path"), vm = require("vm");

const base = process.argv[2] || path.resolve(__dirname, "..");
const html = fs.readFileSync(path.join(base, "simulatore.html"), "utf8");
const banca = JSON.parse(
  fs.readFileSync(path.join(base, "banca", "az104_question_bank_it.json"), "utf8"));

const taglia = (da, a) => {
  const i = html.indexOf(da), j = html.indexOf(a);
  if (i < 0 || j < 0) { console.error(`blocco non trovato: ${da.slice(0, 50)}`); process.exit(1); }
  return html.slice(i, j);
};
const src =
  taglia("/* ============================================================ answer logic */",
         "/* ============================================================ helpers */") +
  taglia("const el = (t, c, x)", "let toastT;") +
  taglia("/* ---------------- answer widgets ----------------",
         "/* ---------------- feedback ----------------");

/* DOM finto: solo i pezzi che answerUI tocca davvero. */
function Node(tag) {
  this.tag = tag; this.children = []; this.style = {};
  this.textContent = ""; this.innerHTML = ""; this.disabled = false; this.value = "";
  const classi = new Set();
  this.classList = {
    add: (...c) => c.forEach((x) => x && classi.add(x)),
    toggle: (c, on) => (on ? classi.add(c) : classi.delete(c)),
    contains: (c) => classi.has(c),
  };
  Object.defineProperty(this, "className", {
    set(v) { String(v || "").split(/\s+/).forEach((c) => c && classi.add(c)); },
    get() { return [...classi].join(" "); },
  });
  this.appendChild = (n) => { this.children.push(n); return n; };
  this.setAttribute = () => {};
}
const ctx = {
  console,
  document: { createElement: (t) => new Node(t) },
  Option: function (t, v) { const n = new Node("option"); n.textContent = t; n.value = v; return n; },
};
vm.createContext(ctx);
vm.runInContext(
  "let U={override:{}}; const correctOf = q => q.risposta_corretta;" + src +
  "\nglobalThis.__api = { answerUI };", ctx);
const { answerUI } = ctx.__api;

const piatto = (n) => { const o = []; (function w(x) { o.push(x); x.children.forEach(w); })(n); return o; };
const nOpzioni = (q) => ["a", "b", "c", "d", "e"].filter((c) => (q["opzione_" + c] || "").trim()).length;

const per = {}, rotte = [];
for (const q of banca) {
  const s = (per[q.tipo] = per[q.tipo] || { ok: 0, ko: 0 });
  try {
    /* 1. stato iniziale, come in esame: nessuna risposta ancora data. */
    const st = { ans: null };
    const vergine = answerUI(q, st, false, true, { mode: "exam" });
    /* 2. stato valutato, come nel ripasso dopo "Verifica". */
    const valutato = answerUI(q, { ans: st.ans }, true, false, { mode: "studio" });

    /* Una drag_drop che chiede meno azioni delle opzioni deve mostrare la linea
       che separa l'area risposta dalla riserva: senza, non si capisce che
       lasciarne fuori una fa parte della risposta. */
    if (q.tipo === "drag_drop") {
      const chiave = q.risposta_corretta.split(",").filter((x) => x.trim()).length;
      const atteso = chiave < nOpzioni(q) ? 1 : 0;
      const sep = piatto(vergine).filter((n) => n.classList.contains("dragsep")).length;
      if (sep !== atteso) throw new Error(`${sep} separatori invece di ${atteso}`);
      const righe = piatto(valutato).filter((n) => n.classList.contains("dragrow")).length;
      if (righe !== nOpzioni(q)) throw new Error(`${righe} righe per ${nOpzioni(q)} opzioni`);
    }
    s.ok++;
  } catch (e) {
    s.ko++;
    rotte.push(`${q.id} [${q.tipo}] ${e.message}`);
  }
}

for (const [t, v] of Object.entries(per))
  console.log(`  ${t.padEnd(19)} ok ${String(v.ok).padStart(3)}  ·  errori ${v.ko}`);
rotte.slice(0, 8).forEach((r) => console.log(`  FAIL  ${r}`));
if (rotte.length > 8) console.log(`  ... e altre ${rotte.length - 8}`);

console.log(rotte.length
  ? `\n${rotte.length} widget non si disegnano.`
  : `\nTutto verde: ${banca.length}/${banca.length} widget si disegnano, valutati e non.`);
process.exit(rotte.length ? 1 : 0);
