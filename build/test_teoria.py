#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Controlla le lezioni di teoria: copertura, campi, link, coerenza con la banca.

    python test_teoria.py ["<cartella repo>"]

La teoria vale se sta agganciata agli stessi 82 obiettivi della banca domande:
e' quel legame che fa funzionare il giro studio -> domande -> simulatore. Se un
obiettivo perde la lezione, o se una lezione parla di qualcosa che nella
tassonomia non esiste, il giro si spezza in silenzio.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).parent))
from tassonomia import TUTTI, UFFICIALI, dominio_di  # noqa: E402

CAMPI = ["obiettivo", "titolo", "concetto", "esempio", "esame", "learn"]

errori = []
def ko(m):
    errori.append(m)


def main():
    file = sorted((BASE / "teoria").glob("*.json"))
    if not file:
        sys.exit("nessun file in teoria/")

    lezioni = []
    for p in file:
        try:
            d = json.loads(p.read_text("utf-8"))
        except Exception as e:
            ko(f"{p.name}: JSON non valido - {e}")
            continue
        if not isinstance(d, list):
            ko(f"{p.name}: deve essere un array")
            continue
        for l in d:
            l["_file"] = p.name
            lezioni.append(l)
        print(f"  {p.name}: {len(d)} lezioni")

    # campi presenti e non vuoti
    for l in lezioni:
        chi = f"{l.get('_file')}/{l.get('titolo', '?')}"
        for c in CAMPI:
            if not str(l.get(c) or "").strip():
                ko(f"{chi}: campo '{c}' mancante o vuoto")
        u = str(l.get("learn") or "")
        if u and not u.startswith("https://learn.microsoft.com/"):
            ko(f"{chi}: il link non punta a Microsoft Learn -> {u[:60]}")
        # italiano: il link deve essere la versione it-it, se no si apre in inglese
        if u.startswith("https://learn.microsoft.com/") and "/it-it/" not in u:
            ko(f"{chi}: link non in italiano (manca /it-it/) -> {u[:70]}")
        for c in ("concetto", "esempio", "esame"):
            t = str(l.get(c) or "")
            if t.count("**") % 2:
                ko(f"{chi}: grassetto non chiuso in '{c}'")
            if t.count("`") % 2:
                ko(f"{chi}: backtick non chiuso in '{c}'")

    # copertura esatta dei 82 obiettivi
    visti = [l.get("obiettivo") for l in lezioni]
    for o, n in Counter(visti).items():
        if n > 1:
            ko(f"obiettivo con {n} lezioni: {o}")
    for o in TUTTI:
        if o not in visti:
            ko(f"obiettivo senza lezione: {o}")
    for o in visti:
        if o not in TUTTI:
            ko(f"lezione fuori tassonomia: {o}")

    # ogni file deve contenere un dominio solo, e nell'ordine della study guide
    for p in file:
        della = [l for l in lezioni if l["_file"] == p.name]
        domini = {dominio_di(l["obiettivo"]) for l in della if l["obiettivo"] in TUTTI}
        if len(domini) > 1:
            ko(f"{p.name}: mescola piu' domini -> {domini}")
        elif domini:
            dom = domini.pop()
            atteso = [o for o in UFFICIALI[dom]]
            trovato = [l["obiettivo"] for l in della]
            if trovato != atteso:
                ko(f"{p.name}: ordine diverso dalla study guide")

    # coerenza con la banca domande
    banca = BASE / "banca" / "az104_question_bank_it.json"
    if banca.exists():
        B = json.loads(banca.read_text("utf-8"))
        sotto = {q["sotto_argomento"] for q in B}
        orfani = sotto - set(visti)
        if orfani:
            ko(f"{len(orfani)} obiettivi hanno domande ma nessuna lezione: {sorted(orfani)[:3]}")

    print(f"\n  lezioni: {len(lezioni)} su {len(TUTTI)} obiettivi ufficiali")
    for dom, lista in UFFICIALI.items():
        n = sum(1 for l in lezioni if l.get("obiettivo") in lista)
        print(f"    {n:3d}/{len(lista):<3d} {dom}")

    car = sum(len(str(l.get(c) or "")) for l in lezioni for c in ("concetto", "esempio", "esame"))
    print(f"\n  testo: {car / 1000:.1f}k caratteri, {car // max(1, len(lezioni))} per lezione in media")

    if errori:
        print(f"\n{len(errori)} problemi:")
        for e in errori[:25]:
            print(f"   - {e}")
        if len(errori) > 25:
            print(f"   ... e altri {len(errori) - 25}")
        return 1
    print("\nTutto verde: 82 obiettivi, 82 lezioni, nessun buco.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
