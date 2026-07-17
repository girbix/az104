#!/usr/bin/env python3
"""Costruisce la cartella telefono/: tutto il materiale AZ-104 usabile offline.

    python build_telefono.py "<cartella AZ-104>"

Il simulatore nasce come artifact: si aspetta che l'utente ci trascini dentro il
JSON e persiste su window.storage, che esiste solo dentro claude.ai. Sul telefono
non c'e' ne' l'uno ne' l'altro. Invece di riscriverlo (1797 righe di grading gia'
testato) lo si patcha in quattro punti:

  1. store        window.storage -> localStorage
  2. banca        inclusa nel file, niente drag & drop
  3. boot         parte dritto sulla banca inclusa, salta la schermata di setup
  4. cambia banca il pulsante sparisce: offline svuoterebbe e basta

Ogni patch verifica che il suo pattern esista davvero. Se il simulatore cambia,
la build si ferma invece di produrre in silenzio un file rotto.
"""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import build_anki_domande  # noqa: E402

# ---------------------------------------------------------------- patch

STORE_ORIG = """/* ============================================================ storage
   Persistenza via window.storage (API degli artifact). Mai localStorage/sessionStorage. */
const K_BANK = "az104:bank", K_USER = "az104:user";
let storageOK = true;

const store = {
  async get(k){
    try{
      if(!window.storage) throw new Error("window.storage non disponibile");
      const v = await window.storage.getItem(k);
      return v ? JSON.parse(v) : null;
    }catch(e){ storageOK = false; return null; }
  },
  async set(k, v){
    try{
      if(!window.storage) throw new Error("window.storage non disponibile");
      await window.storage.setItem(k, JSON.stringify(v));
      return true;
    }catch(e){ storageOK = false; return false; }
  }
};"""

STORE_NUOVO = """/* ============================================================ storage
   Versione offline: persistenza su localStorage. La banca e' inclusa nel file,
   quindi non viene mai scritta in storage: ci finiscono solo note, correzioni e
   progressi, che sono pochi KB e stanno larghi nella quota. */
const K_BANK = "az104:bank", K_USER = "az104:user";
let storageOK = true;

const store = {
  async get(k){
    if(k === K_BANK) return null;
    try{
      const v = localStorage.getItem(k);
      return v ? JSON.parse(v) : null;
    }catch(e){ storageOK = false; return null; }
  },
  async set(k, v){
    if(k === K_BANK) return true;
    try{
      localStorage.setItem(k, JSON.stringify(v));
      return true;
    }catch(e){ storageOK = false; return false; }
  }
};"""

WARN_ORIG = '''  w.textContent = "Persistenza non disponibile in questo contesto: i progressi di questa sessione non verranno salvati. Usa Esporta per non perderli.";'''

WARN_NUOVO = '''  w.textContent = "Questo browser non salva i dati delle pagine locali: i progressi valgono solo finche' la scheda resta aperta. Usa Esporta prima di chiuderla, oppure apri il file con Chrome o Samsung Internet.";'''

BANK_ORIG = "let BANK = [];"
BANK_NUOVO = """let BANK = [];
/* La banca domande, inclusa qui dentro dalla build: il file e' autosufficiente. */
const BANCA_INCLUSA = /*__BANCA__*/[];"""

BOOT_ORIG = """  const b = await store.get(K_BANK);
  if(Array.isArray(b) && b.length){
    BANK = b; buildFilters(); go("studio");
  }else{
    go("setup");
  }"""

BOOT_NUOVO = """  BANK = normalizeBank(BANCA_INCLUSA);
  buildFilters();
  go("studio");"""

CAMBIA_ORIG = """  const rb = el("button", "btn sm danger", "Cambia banca domande");
  rb.onclick = () => {
    if(confirm("Caricare un'altra banca? Note, correzioni e progressi restano legati agli id delle domande.")){
      BANK = []; store.set(K_BANK, []); go("setup");
    }
  };
  row.appendChild(rp); row.appendChild(rb);"""

CAMBIA_NUOVO = """  row.appendChild(rp);"""

TITOLO_ORIG = "<title>Simulatore d'esame AZ-104</title>"
TITOLO_NUOVO = "<title>Simulatore AZ-104 — offline</title>"

PATCH = [
    ("storage su localStorage", STORE_ORIG, STORE_NUOVO),
    ("avviso di persistenza", WARN_ORIG, WARN_NUOVO),
    ("banca inclusa", BANK_ORIG, BANK_NUOVO),
    ("boot senza setup", BOOT_ORIG, BOOT_NUOVO),
    ("via il pulsante cambia banca", CAMBIA_ORIG, CAMBIA_NUOVO),
    ("titolo", TITOLO_ORIG, TITOLO_NUOVO),
]


def applica(html):
    for nome, prima, dopo in PATCH:
        n = html.count(prima)
        if n != 1:
            sys.exit(
                f"ERRORE patch '{nome}': il pattern compare {n} volte, ne serve 1.\n"
                f"Il simulatore e' cambiato: aggiorna build_telefono.py."
            )
        html = html.replace(prima, dopo)
        print(f"  ok  {nome}")
    return html


def main():
    if len(sys.argv) < 2:
        sys.exit("uso: build_telefono.py <cartella AZ-104>")
    base = Path(sys.argv[1])
    out = base / "telefono"
    out.mkdir(exist_ok=True)

    # -------------------------------------------------- simulatore offline
    print("Simulatore offline:")
    html = (base / "simulatore.html").read_text("utf-8")
    html = applica(html)

    banca = json.loads((base / "az104_question_bank_it.json").read_text("utf-8"))
    payload = json.dumps(banca, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = html.replace("/*__BANCA__*/[]", payload)

    sim = out / "simulatore.html"
    sim.write_text(html, encoding="utf-8")
    print(f"  -> {sim.name}  ({sim.stat().st_size / 1024:.0f} KB, {len(banca)} domande incluse)")

    # -------------------------------------------------- ripasso
    rip_src = base / "az104_ripasso.html"
    if not rip_src.exists():
        sys.exit("ERRORE: manca az104_ripasso.html. Lancia prima build_ripasso.py.")
    shutil.copy2(rip_src, out / "ripasso.html")
    print(f"\nRipasso:\n  -> ripasso.html  ({(out / 'ripasso.html').stat().st_size / 1024:.0f} KB)")

    # -------------------------------------------------- flashcard atomiche
    fc = sorted((base / "flashcards").glob("az104_flashcard_*.csv"))
    n_card = 0
    for f in fc:
        shutil.copy2(f, out / f.name)
        righe = f.read_text("utf-8").splitlines()
        n_card += sum(1 for r in righe if r.strip() and not r.startswith("#"))
    print(f"\nFlashcard:\n  -> {len(fc)} CSV copiati, {n_card} card in tutto")

    # -------------------------------------------------- domande come mazzo Anki
    # Firefox e DuckDuckGo non aprono file://: AnkiDroid e' la via che funziona
    # comunque, quindi anche le domande d'esame diventano card.
    csv_dom, n_dom, _ = build_anki_domande.genera(base, out)
    print(f"\nDomande in Anki:\n  -> {csv_dom.name}  ({csv_dom.stat().st_size / 1024:.0f} KB, {n_dom} card)")

    # -------------------------------------------------- indice
    # I conteggi arrivano dai file veri: cosi' l'indice non puo' mentire.
    idx = (Path(__file__).parent / "index_telefono.html").read_text("utf-8")
    idx = idx.replace("__N_CARD__", str(n_card)).replace("__N_DOMANDE__", str(len(banca)))
    for segnaposto in ("__N_CARD__", "__N_DOMANDE__"):
        if segnaposto in idx:
            sys.exit(f"ERRORE: segnaposto {segnaposto} non sostituito")
    (out / "index.html").write_text(idx, encoding="utf-8")
    print(f"\nIndice:\n  -> index.html  ({n_card} card, {len(banca)} domande)")

    peso = sum(f.stat().st_size for f in out.iterdir() if f.is_file())
    print(f"\nCartella pronta: {out}")
    print(f"Da copiare sul telefono: {peso / 1024 / 1024:.1f} MB")


if __name__ == "__main__":
    main()
