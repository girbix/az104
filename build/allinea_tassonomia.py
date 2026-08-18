#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Riscrive `sotto_argomento` nelle due banche secondo la tassonomia ufficiale.

    python allinea_tassonomia.py [--scrivi] ["<cartella repo>"]

Senza --scrivi mostra soltanto cosa cambierebbe. Le due banche vengono toccate
insieme e nello stesso modo: se divergessero, note e progressi salvati dagli
utenti punterebbero a categorie diverse a seconda della lingua.
"""
import json
import sys
from collections import Counter
from pathlib import Path

# La console di Windows parte in cp1252 e si strozza su '≤' e sui trattini lunghi.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).parent))
from tassonomia import UFFICIALI, TUTTI, normalizza, dominio_di  # noqa: E402

argv = [a for a in sys.argv[1:] if a != "--scrivi"]
SCRIVI = "--scrivi" in sys.argv
BASE = Path(argv[0]) if argv else Path(__file__).resolve().parent.parent

BANCA = BASE / "banca" / "az104_question_bank_it.json"


def main():
    banche = [(BANCA, json.loads(BANCA.read_text("utf-8")))]

    cambi = Counter()
    sconosciuti = Counter()
    for _, banca in banche:
        for q in banca:
            vecchio = q["sotto_argomento"]
            nuovo = normalizza(vecchio)
            if nuovo != vecchio:
                cambi[(vecchio, nuovo)] += 1
                q["sotto_argomento"] = nuovo
            # Coerenza dominio/obiettivo: un obiettivo vive in un dominio solo.
            atteso = dominio_di(q["sotto_argomento"])
            if atteso is None:
                sconosciuti[q["sotto_argomento"]] += 1
            elif atteso != q["dominio"]:
                print(f"  !! {q['id']}: '{q['sotto_argomento']}' appartiene a "
                      f"'{atteso}' ma la domanda è in '{q['dominio']}'")

    print("RINOMINE")
    for (v, n), c in sorted(cambi.items(), key=lambda x: -x[1]):
        print(f"  {c:3d}  {v}\n       -> {n}")
    if not cambi:
        print("  nessuna: già allineate.")

    if sconosciuti:
        print("\nETICHETTE FUORI TASSONOMIA (vanno mappate in tassonomia.py)")
        for s, c in sconosciuti.most_common():
            print(f"  {c:3d}  {s}")

    # Copertura per obiettivo ufficiale
    conteggio = Counter(q["sotto_argomento"] for q in banche[0][1])
    scoperti, sottili = [], []
    print("\nCOPERTURA DEI 82 OBIETTIVI UFFICIALI")
    for dom, lista in UFFICIALI.items():
        tot = sum(conteggio[s] for s in lista)
        print(f"\n  {dom}  —  {tot} domande su {len(lista)} obiettivi")
        for s in lista:
            n = conteggio[s]
            segno = "  " if n >= 4 else ("!!" if n == 0 else " ·")
            print(f"    {segno} {n:3d}  {s}")
            if n == 0:
                scoperti.append(s)
            elif n <= 3:
                sottili.append((s, n))

    print(f"\n  obiettivi ufficiali: {len(TUTTI)}")
    print(f"  a copertura ZERO:    {len(scoperti)}")
    for s in scoperti:
        print(f"      {s}")
    print(f"  con ≤3 domande:      {len(sottili)}")
    for s, n in sorted(sottili, key=lambda x: x[1]):
        print(f"      {n}  {s}")

    if SCRIVI:
        for p, banca in banche:
            p.write_text(json.dumps(banca, ensure_ascii=False, indent=1) + "\n",
                         encoding="utf-8")
            print(f"\nscritto {p.name}")
    else:
        print("\n(prova a vuoto: rilancia con --scrivi per applicare)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
