/* Controlli strutturali sulle pagine pubblicate.
 *
 *     node test_pagine.js ["<cartella AZ-104>"]
 *
 * Sono pagine autosufficienti, scritte a mano e rigenerate dalla build: gli
 * errori che le rompono non sono logici ma strutturali. Un getElementById che
 * punta a un elemento tolto, una risorsa esterna che dietro un proxy non
 * carica, un </script> finito nel payload. Nessuno di questi si vede finche'
 * non si apre la pagina, e a quel punto resta bianca.
 */
const fs = require("fs"), path = require("path"), vm = require("vm");

const base = process.argv[2] || path.resolve(__dirname, "..");
const PAGINE = ["index.html", "studia.html", "pratica.html", "ripasso.html", "simulatore.html"];

let errori = 0;
const ko = (m) => { console.log(`  FAIL  ${m}`); errori++; };
const ok = (m) => console.log(`  ok    ${m}`);

for (const nome of PAGINE) {
  const f = path.join(base, nome);
  if (!fs.existsSync(f)) { ko(`${nome}: non esiste`); continue; }
  const html = fs.readFileSync(f, "utf8");
  console.log(`\n${nome}  (${Math.round(html.length / 1024)} KB)`);

  const i = html.indexOf("<script>");
  const testa = i < 0 ? html : html.slice(0, i);
  const js = i < 0 ? "" : html.slice(i);

  /* 1. ogni getElementById deve trovare qualcosa */
  const ids = new Set([...testa.matchAll(/\bid="([^"]+)"/g)].map((m) => m[1]));
  /* Un id puo' nascere in tre modi: nell'HTML statico, con n.id = "x", oppure
     dentro una template string di markup. Il terzo caso e' quello che tradisce:
     l'elemento esiste a runtime ma non compare nell'HTML del file. */
  const creati = new Set([
    ...[...js.matchAll(/\.id\s*=\s*["']([^"']+)["']/g)].map((m) => m[1]),
    ...[...js.matchAll(/id="([^"$]+)"/g)].map((m) => m[1]),
  ]);
  const cercati = [...js.matchAll(/getElementById\(\s*["']([^"']+)["']\s*\)/g)].map((m) => m[1]);
  const orfani = [...new Set(cercati)].filter((x) => !ids.has(x) && !creati.has(x));
  orfani.length === 0
    ? ok(`${cercati.length} getElementById, tutti con il loro elemento`)
    : ko(`riferimenti a elementi inesistenti: ${orfani.join(", ")}`);

  /* 2. nessuna risorsa esterna: la pagina deve reggersi da sola */
  const esterne = [...html.matchAll(/(?:src|href)\s*=\s*["'](https?:\/\/[^"']+)/g)]
    .map((m) => m[1])
    .filter((u) => !/^https:\/\/(learn\.microsoft\.com|girbix\.github\.io|github\.com)/.test(u));
  esterne.length === 0 ? ok("nessuna risorsa esterna caricata")
                       : ko(`risorse esterne: ${esterne.slice(0, 3).join(", ")}`);

  /* 3. il JavaScript deve almeno compilare */
  if (js) {
    const corpo = js.slice(8, js.lastIndexOf("</script>"));
    try { new vm.Script(corpo); ok("il JavaScript compila"); }
    catch (e) { ko(`il JavaScript non compila: ${e.message}`); }
  }

  /* 4. niente </script> letterale nel payload: chiuderebbe il tag */
  const payload = js.match(/const (?:BANCA_INCLUSA|BANCA|LEZIONI) = (\[.*)/);
  if (payload && !payload[1].includes("</script")) ok("nessun </script> letterale nel payload");
  else if (payload) ko("il payload contiene </script>");
}


/* Il giro fra le pagine: ogni categoria che il simulatore puo' mostrare a fine
   prova deve avere una lezione raggiungibile con studia.html?o=<obiettivo>.
   Se un obiettivo resta senza lezione il collegamento porta a una pagina che
   non scorre da nessuna parte, e non se ne accorge nessuno finche' non ci
   clicca sopra. */
console.log("\ncollegamento simulatore -> teoria");
{
  const sim = fs.readFileSync(path.join(base, "simulatore.html"), "utf8");
  const stu = fs.readFileSync(path.join(base, "studia.html"), "utf8");
  const rigaBanca = sim.split("\n").find((r) => r.startsWith("const BANCA_INCLUSA"));
  const rigaLez = stu.split("\n").find((r) => r.startsWith("const LEZIONI"));
  if (!rigaBanca || !rigaLez) {
    ko("payload non trovato in una delle due pagine");
  } else {
    const leggi = (riga, chiave) =>
      new Set([...riga.matchAll(new RegExp('"' + chiave + '":"((?:[^"\\\\]|\\\\.)*)"', "g"))]
        .map((m) => JSON.parse('"' + m[1] + '"')));
    const obiettivi = leggi(rigaBanca, "sotto_argomento");
    const lezioni = leggi(rigaLez, "o");
    const senza = [...obiettivi].filter((o) => !lezioni.has(o));
    senza.length === 0
      ? ok(`${obiettivi.size} categorie, tutte con la loro lezione`)
      : ko(`categorie senza lezione: ${senza.slice(0, 3).join(" | ")}`);
    sim.includes('"studia.html?o="')
      ? ok("le categorie da ripassare linkano alla teoria")
      : ko("le categorie da ripassare non linkano piu' alla teoria");
    stu.includes('URLSearchParams(location.search).get("o")')
      ? ok("la teoria sa ricevere il rimando")
      : ko("la teoria non gestisce piu' il parametro ?o=");
  }
}

/* E il giro di ritorno: dalla lezione alle sue domande.
   Ogni lezione ha un link a simulatore.html?sub=<obiettivo>. Se quel
   sotto-argomento non ha domande in banca, il link apre uno Studio vuoto: non
   e' un errore, e' peggio — sembra che le domande non ci siano. */
console.log("\ncollegamento teoria -> simulatore");
{
  const sim = fs.readFileSync(path.join(base, "simulatore.html"), "utf8");
  const stu = fs.readFileSync(path.join(base, "studia.html"), "utf8");
  const rigaBanca = sim.split("\n").find((r) => r.startsWith("const BANCA_INCLUSA"));
  const rigaLez = stu.split("\n").find((r) => r.startsWith("const LEZIONI"));
  if (!rigaBanca || !rigaLez) {
    ko("payload non trovato in una delle due pagine");
  } else {
    const leggi = (riga, chiave) =>
      new Set([...riga.matchAll(new RegExp('"' + chiave + '":"((?:[^"\\\\]|\\\\.)*)"', "g"))]
        .map((m) => JSON.parse('"' + m[1] + '"')));
    const conDomande = leggi(rigaBanca, "sotto_argomento");
    const lezioni = leggi(rigaLez, "o");
    const vuote = [...lezioni].filter((o) => !conDomande.has(o));
    vuote.length === 0
      ? ok(`${lezioni.size} lezioni, tutte con domande da fare`)
      : ko(`lezioni che linkano a uno Studio vuoto: ${vuote.slice(0, 3).join(" | ")}`);

    stu.includes("simulatore.html?sub=")
      ? ok("ogni lezione porta alle sue domande")
      : ko("le lezioni non linkano piu' alle domande");
    sim.includes('URLSearchParams(location.search).get("sub")')
      ? ok("il simulatore sa ricevere il rimando")
      : ko("il simulatore non gestisce piu' il parametro ?sub=");
  }
}

/* I numeri scritti sulla homepage. Sono a mano dentro l'HTML, e nessuno li
   ricalcola: quando la banca cresce restano indietro in silenzio. E' gia'
   successo — il ripasso ha annunciato "532 domande" per settimane mentre ne
   conteneva 591. Qui si confrontano con quello che le pagine hanno davvero
   dentro, cosi' la prossima volta lo dice il test e non chi studia. */
console.log("\nnumeri dichiarati sulla homepage");
{
  const idx = fs.readFileSync(path.join(base, "index.html"), "utf8");
  const stu = fs.readFileSync(path.join(base, "studia.html"), "utf8");
  const sim = fs.readFileSync(path.join(base, "simulatore.html"), "utf8");
  const pra = fs.readFileSync(path.join(base, "pratica.html"), "utf8");

  const conta = (testo, inizio, pezzo) => {
    const riga = testo.split("\n").find((r) => r.startsWith(inizio));
    return riga ? riga.split(pezzo).length - 1 : -1;
  };
  const lezioni = conta(stu, "const LEZIONI", '{"o":"');
  const domande = conta(sim, "const BANCA_INCLUSA", '"id":"AZ104-');
  const lab = conta(pra, "const LAB", '"id":"P');

  const reale = {
    lezioni,
    domande,
    lab,
    n: Number((sim.match(/EXAM_N\s*=\s*(\d+)/) || [])[1]),
    min: Number((sim.match(/EXAM_MIN\s*=\s*(\d+)/) || [])[1]),
  };

  const atteso = [
    [reale.lezioni, "lezioni"],
    [reale.domande, "domande"],
    [reale.lab, "lab"],
    [reale.n, "domande estratte dal simulatore"],
    [reale.min, "minuti d'esame"],
  ];

  for (const [valore, cosa] of atteso) {
    if (!Number.isFinite(valore) || valore <= 0) { ko(`non riesco a contare: ${cosa}`); continue; }
    /* il numero deve comparire come numero intero, non dentro un altro numero */
    const trovato = new RegExp("(?<!\\d)" + valore + "(?!\\d)").test(idx);
    trovato ? ok(`${valore} ${cosa}`)
            : ko(`la homepage non dice ${valore} ${cosa}: il numero e' cambiato e il testo no`);
  }

  /* Numeri scritti in pagina che non corrispondono a niente di reale.
     Solo il testo visibile: nel codice i numeri sono codici e soglie, non
     promesse fatte a chi legge. */
  const noti = new Set(atteso.map(([v]) => String(v)).concat(["104", "1000", "700", "82", "17", "2026"]));
  const corpo = idx.slice(idx.indexOf("</style>"), idx.indexOf("<script>"));
  const sospetti = [...new Set([...corpo.matchAll(/(?<![\w.-])(\d{2,4})(?![\w.-])/g)].map((m) => m[1]))]
    .filter((n) => !noti.has(n));
  sospetti.length === 0
    ? ok("nessun numero orfano nel testo")
    : ko(`numeri che non tornano con niente: ${sospetti.join(", ")}`);
}

console.log(errori === 0 ? "\nTutto verde: le pagine sono integre."
                         : `\n${errori} problemi.`);
process.exit(errori ? 1 : 0);
