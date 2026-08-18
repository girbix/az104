/* La barra di sito e il pulsante "Ricomincia le domande".
 *
 *     node test_ricomincia.js ["<cartella AZ-104>"]
 *
 * Due cose che nessun altro test guarda.
 *
 * La barra: e' l'unico modo per passare da una pagina all'altra senza il
 * pulsante indietro. Se una pagina la perde, ci si finisce dentro e non si
 * esce piu'.
 *
 * Il pulsante: cancella dati dell'utente e non si torna indietro. Se cancella
 * piu' di quello che il messaggio di conferma promette, se ne accorge chi ha
 * appena perso le sue note. Qui viene eseguito davvero, su una memoria locale
 * finta, e si controlla cosa resta.
 */
const fs = require("fs"), path = require("path"), vm = require("vm");

const base = process.argv[2] || path.resolve(__dirname, "..");
const PAGINE = ["index.html", "studia.html", "ripasso.html", "simulatore.html"];
const NOMI = { "index.html": "Home", "studia.html": "Teoria",
               "ripasso.html": "Ripasso", "simulatore.html": "Simulatore" };

let errori = 0;
const ko = (m) => { console.log(`  FAIL  ${m}`); errori++; };
const ok = (m) => console.log(`  ok    ${m}`);

const leggi = (n) => fs.readFileSync(path.join(base, n), "utf8");

/* ---------- 1. la barra c'e' su tutte, e porta a tutte ---------- */
console.log("barra di sito");
for (const nome of PAGINE) {
  const html = leggi(nome);
  const barra = html.match(/<nav class="sitenav"[\s\S]*?<\/nav>/);
  if (!barra) { ko(`${nome}: nessuna barra`); continue; }
  const b = barra[0];

  const mancanti = PAGINE.filter((p) => !b.includes(`href="${p}"`));
  if (mancanti.length) { ko(`${nome}: non porta a ${mancanti.join(", ")}`); continue; }

  const correnti = [...b.matchAll(/href="([^"]+)"[^>]*aria-current="page"/g)].map((m) => m[1]);
  if (correnti.length !== 1 || correnti[0] !== nome) {
    ko(`${nome}: si segna come pagina corrente ${correnti.join(", ") || "nessuna"}`);
    continue;
  }
  if (!b.includes('id="ricomincia"')) { ko(`${nome}: manca il pulsante Ricomincia`); continue; }
  ok(`${nome}: ${PAGINE.length} sezioni, corrente ${NOMI[nome]}, con Ricomincia`);
}

/* ---------- 2. una sola versione del pulsante ---------- */
console.log("\nstesso codice su tutte le pagine");
{
  const versioni = new Map();
  for (const nome of PAGINE) {
    const m = leggi(nome).match(/\(function ricomincia\(\)\{[\s\S]*?\n\}\)\(\);/);
    if (!m) { ko(`${nome}: la funzione ricomincia non c'e'`); continue; }
    const chiave = m[0];
    if (!versioni.has(chiave)) versioni.set(chiave, []);
    versioni.get(chiave).push(nome);
  }
  versioni.size === 1
    ? ok(`una sola versione, su ${[...versioni.values()][0].length} pagine`)
    : ko(`${versioni.size} versioni diverse: ${[...versioni.values()].map((v) => v.join("+")).join(" vs ")}`);
}

/* ---------- 3. cosa cancella davvero ---------- */
console.log("\ncosa cancella");
{
  const sorgente = leggi("simulatore.html").match(/\(function ricomincia\(\)\{[\s\S]*?\n\}\)\(\);/);
  if (!sorgente) {
    ko("non riesco a estrarre la funzione");
  } else {
    /* stato di partenza: uno che ha studiato, risposto, sostenuto esami,
       scritto note e corretto due domande a mano */
    const pieno = () => ({
      "az104:user": JSON.stringify({
        note: { "AZ104-0042": "rileggere il limite" },
        override: { "AZ104-0100": { risposta_corretta: "b" } },
        flag: { "AZ104-0007": 1 },
        prog: { "AZ104-0001": { ok: true }, "AZ104-0002": { ok: false } },
        history: [{ ts: "2026-08-01", score: 720 }],
        theme: "dark",
      }),
      "az104-ripasso-v1": JSON.stringify({ "AZ104-0003": "ok", "AZ104-0004": "rev" }),
      "az104:teoria": JSON.stringify({ "Create users and groups": 1 }),
      "az104:teoria:ascolti": JSON.stringify({ "Create users and groups": 3 }),
      "az104:teoria:voce": "Isabella",
      "az104:tema": "dark",
    });

    const esegui = (rispostaAllaConferma) => {
      const dati = pieno();
      let ricaricata = false, chiesto = null, inMemoria = false;
      let click = null;
      const ctx = {
        document: { getElementById: () => ({ addEventListener: (_, f) => { click = f; } }) },
        localStorage: {
          getItem: (k) => (k in dati ? dati[k] : null),
          setItem: (k, v) => { dati[k] = String(v); },
          removeItem: (k) => { delete dati[k]; },
        },
        confirm: (m) => { chiesto = m; return rispostaAllaConferma; },
        location: { reload: () => { ricaricata = true; } },
        console,
      };
      ctx.window = ctx;
      ctx.window.azzeraInMemoria = () => { inMemoria = true; };
      vm.createContext(ctx);
      vm.runInContext(sorgente[0], ctx);
      if (!click) throw new Error("nessun gestore del click");
      click();
      return { dati, ricaricata, chiesto, inMemoria };
    };

    /* --- se dici di no, non deve succedere niente --- */
    {
      const r = esegui(false);
      const uguale = JSON.stringify(r.dati) === JSON.stringify(pieno());
      uguale && !r.ricaricata
        ? ok("annullando la conferma non tocca niente")
        : ko("annullando la conferma cancella lo stesso");
      r.chiesto && /non si torna indietro/i.test(r.chiesto)
        ? ok("la conferma avvisa che non si torna indietro")
        : ko("la conferma non avvisa che l'operazione e' definitiva");
    }

    /* --- se dici di si', deve cancellare esattamente quello che promette --- */
    {
      const r = esegui(true);
      const u = JSON.parse(r.dati["az104:user"]);

      const via = [
        ["risposte date", Object.keys(u.prog).length === 0],
        ["esami sostenuti", u.history.length === 0],
        ["segni del ripasso", !("az104-ripasso-v1" in r.dati)],
      ];
      const restano = [
        ["le note", u.note && u.note["AZ104-0042"] === "rileggere il limite"],
        ["le correzioni", u.override && !!u.override["AZ104-0100"]],
        ["le segnalazioni", u.flag && !!u.flag["AZ104-0007"]],
        ["il tema", u.theme === "dark"],
        ["le lezioni studiate", r.dati["az104:teoria"] === pieno()["az104:teoria"]],
        ["gli ascolti", r.dati["az104:teoria:ascolti"] === pieno()["az104:teoria:ascolti"]],
        ["la voce scelta", r.dati["az104:teoria:voce"] === "Isabella"],
      ];

      for (const [cosa, andato] of via) {
        andato ? ok(`azzera: ${cosa}`) : ko(`NON azzera: ${cosa}`);
      }
      for (const [cosa, rimasto] of restano) {
        rimasto ? ok(`lascia stare: ${cosa}`) : ko(`cancella anche: ${cosa}`);
      }
      r.inMemoria ? ok("avvisa la pagina di svuotare anche la copia in memoria")
                  : ko("non avvisa la pagina: il primo salvataggio riscriverebbe tutto");
      r.ricaricata ? ok("ricarica la pagina") : ko("non ricarica: la pagina resterebbe con i vecchi dati a video");
    }
  }
}

/* ---------- 4. le pagine che tengono dati in memoria sanno svuotarla ---------- */
console.log("\ncopia in memoria");
for (const nome of ["ripasso.html", "simulatore.html"]) {
  leggi(nome).includes("window.azzeraInMemoria =")
    ? ok(`${nome}: sa svuotare la sua copia`)
    : ko(`${nome}: tiene i dati in memoria ma non li svuota`);
}

/* ---------- 5. la barra si vede, anche al buio ----------
   Il CSS della barra e' uno solo per quattro pagine che hanno due sistemi di
   token diversi, quindi ogni colore e' scritto var(--questo, var(--quello)).
   Se una pagina smette di definire il suo, la barra non sparisce: eredita il
   colore di sfondo e diventa testo invisibile su fondo invisibile. Al buio
   succede da solo, perche' i blocchi scuri ridefiniscono solo una parte dei
   token. */
console.log("\ncolori della barra");
{
  const COPPIE = [["--card", "--surface"], ["--text-2", "--ink-2"], ["--text", "--ink"],
                  ["--signal", "--warn"], ["--accent-soft", null], ["--line", null]];
  for (const nome of PAGINE) {
    const css = leggi(nome).split("</style>")[0].replace(/\s+/g, "");
    const chiaro = (css.match(/:root\{([^}]*)\}/) || [])[1] || "";
    const scuro = (css.match(/:root\[data-theme="dark"\]\{([^}]*)\}/) || [])[1] || "";
    const manca = (blocco) => COPPIE
      .filter(([a, b]) => !blocco.includes(a + ":") && !(b && blocco.includes(b + ":")))
      .map(([a, b]) => (b ? `${a}/${b}` : a));

    const c = manca(chiaro), s = manca(scuro);
    if (!scuro) ko(`${nome}: nessun tema scuro dichiarato`);
    else if (c.length || s.length) {
      ko(`${nome}: la barra resta senza colore — chiaro ${c.join(", ") || "ok"}, scuro ${s.join(", ") || "ok"}`);
    } else ok(`${nome}: tutti i colori della barra esistono, chiaro e scuro`);
  }
}

console.log(errori === 0 ? "\nTutto verde: la barra c'e' ovunque e Ricomincia mantiene la promessa."
                         : `\n${errori} problemi.`);
process.exit(errori ? 1 : 0);
