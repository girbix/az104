#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rigenera le pagine pubblicate a partire dalla banca italiana.

    python build_pagine.py ["<cartella repo>"]

Perche' esiste: build_telefono.py trasforma il simulatore-artifact nella
versione offline, ma nel repo simulatore.html E' gia' la versione offline, con
la banca dentro. Quella build non e' quindi rieseguibile, e senza questo script
l'unico modo per aggiornare le domande nella pagina sarebbe modificarla a mano.

Qui il payload viene semplicemente sostituito sul posto, lasciando intatto tutto
il resto della pagina. Il ripasso viene ricostruito dal suo template.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
QUI = Path(__file__).parent

BANCA = BASE / "banca" / "az104_question_bank_it.json"
SIM = BASE / "simulatore.html"
RIP = BASE / "ripasso.html"

MARCA = "const BANCA_INCLUSA = "


def payload(banca):
    """JSON compatto. '</' va sfuggito o uno </script> dentro una spiegazione
    chiuderebbe il tag; '<\\/' e' un escape JSON valido."""
    return json.dumps(banca, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def rigenera_simulatore(banca):
    html = SIM.read_text("utf-8")
    i = html.find(MARCA)
    if i < 0:
        sys.exit(f"ERRORE: '{MARCA}' non trovato in {SIM.name}: la pagina e' cambiata.")
    inizio = html.find("[", i)
    # delimita l'array contando le quadre fuori dalle stringhe
    livello, j, in_str, esc = 0, inizio, False, False
    while j < len(html):
        c = html[j]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
        else:
            if c == '"':
                in_str = True
            elif c == "[":
                livello += 1
            elif c == "]":
                livello -= 1
                if livello == 0:
                    break
        j += 1
    if livello != 0:
        sys.exit("ERRORE: payload del simulatore non delimitabile.")

    vecchio = html[inizio:j + 1]
    try:
        n_vecchie = len(json.loads(vecchio.replace("<\\/", "</")))
    except Exception:
        n_vecchie = "?"

    nuovo = html[:inizio] + payload(banca) + html[j + 1:]
    SIM.write_text(nuovo, encoding="utf-8")
    print(f"  simulatore.html  {n_vecchie} -> {len(banca)} domande "
          f"({SIM.stat().st_size / 1024:.0f} KB)")


def rigenera_ripasso():
    """build_ripasso.py si aspetta banca e uscita con i nomi lunghi, affiancate.
    Gli si prepara quella disposizione in una cartella temporanea e poi si
    pubblica il risultato come ripasso.html."""
    import shutil
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        shutil.copy2(BANCA, td / "az104_question_bank_it.json")
        r = subprocess.run([sys.executable, str(QUI / "build_ripasso.py"), str(td)],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stdout)
            print(r.stderr, file=sys.stderr)
            sys.exit("ERRORE: build_ripasso.py non ha completato.")
        prodotto = td / "az104_ripasso.html"
        if not prodotto.exists():
            sys.exit("ERRORE: build_ripasso.py non ha scritto az104_ripasso.html.")
        shutil.copy2(prodotto, RIP)
        for riga in r.stdout.strip().splitlines():
            if riga.strip():
                print(f"    {riga.strip()}")
    print(f"  ripasso.html     ({RIP.stat().st_size / 1024:.0f} KB)")


def main():
    banca = json.loads(BANCA.read_text("utf-8"))
    print(f"Banca: {len(banca)} domande\n")
    rigenera_simulatore(banca)
    rigenera_ripasso()
    print("\nFatto. Rilancia i test prima di pubblicare.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
