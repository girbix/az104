#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aggiunge i lotti di banca/sorgenti/nuove/ alla banca, in coda.

    python aggiungi_domande.py [--scrivi] ["<cartella repo>"]

Gli id si assegnano in coda e non si riusano mai: note, correzioni e progressi
salvati dagli utenti sono indicizzati per id, e rinumerare li spezzerebbe tutti.
"""
import json
import sys
from collections import Counter
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).parent))
from tassonomia import TUTTI, dominio_di  # noqa: E402

SCRIVI = "--scrivi" in sys.argv
argv = [a for a in sys.argv[1:] if a != "--scrivi"]
BASE = Path(argv[0]) if argv else Path(__file__).resolve().parent.parent

NUOVE = BASE / "banca" / "sorgenti" / "nuove"
P_IT = BASE / "banca" / "az104_question_bank_it.json"

TESTO = ["domanda", "opzione_a", "opzione_b", "opzione_c", "opzione_d", "opzione_e", "spiegazione"]
TECNICI = ["dominio", "sotto_argomento", "tipo", "risposta_corretta", "url_riferimento",
           "difficolta", "tags"]


def scheletro(q, qid):
    """Costruisce un record di banca completo."""
    out = {"id": qid}
    for c in ("dominio", "sotto_argomento", "tipo"):
        out[c] = q[c]
    for c in TESTO:
        out[c] = q.get(c) or ""
    out["risposta_corretta"] = q["risposta_corretta"]
    out["url_riferimento"] = q["url_riferimento"]
    out["fonte"] = "Microsoft Learn"
    out["url_fonte"] = q["url_riferimento"]
    out["sintesi_commenti"] = ""
    out["consenso_community"] = ""
    out["stato"] = q.get("stato", "da_rivedere")
    out["difficolta"] = q["difficolta"]
    out["tags"] = q.get("tags", "")
    out["is_generated"] = True
    out["data_verifica"] = ""
    return out


def controlla(q, dove, problemi):
    qid = f"{dove}:{q.get('domanda', '')[:40]}"
    if q["sotto_argomento"] not in TUTTI:
        problemi.append(f"{qid}: sotto_argomento fuori tassonomia -> {q['sotto_argomento']}")
    elif dominio_di(q["sotto_argomento"]) != q["dominio"]:
        problemi.append(f"{qid}: dominio non coerente con il sotto_argomento")
    for c in TECNICI:
        if c not in q:
            problemi.append(f"{qid}: manca il campo {c}")
    # la chiave deve puntare a opzioni esistenti (controllo grossolano, il
    # test_contenuti.py fa poi quello serio su tutta la banca)
    lettere = [c for c in "abcde" if (q.get("opzione_" + c) or "").strip()]
    if q["tipo"] in ("multiple_choice", "case_study", "multiple_response", "drag_drop"):
        for x in [v.strip().lower() for v in q["risposta_corretta"].split(",") if v.strip()]:
            if x not in lettere:
                problemi.append(f"{qid}: chiave '{x}' fuori dalle opzioni {lettere}")


def main():
    if not NUOVE.exists():
        sys.exit(f"nessuna cartella {NUOVE}")
    lotti = sorted(NUOVE.glob("*.json"))
    if not lotti:
        sys.exit("nessun lotto nuovo da aggiungere")

    nuove, problemi = [], []
    for p in lotti:
        d = json.loads(p.read_text("utf-8"))
        for q in d:
            controlla(q, p.name, problemi)
            nuove.append(q)
        print(f"  {p.name}: {len(d)}")

    if problemi:
        print(f"\n{len(problemi)} problemi nei lotti nuovi:")
        for x in problemi[:20]:
            print(f"   - {x}")
        sys.exit(1)

    IT = json.loads(P_IT.read_text("utf-8"))

    esistenti = {q["id"] for q in IT}
    prossimo = max(int(i.split("-")[1]) for i in esistenti) + 1

    for q in nuove:
        qid = f"AZ104-{prossimo:04d}"
        prossimo += 1
        IT.append(scheletro(q, qid))

    print(f"\n  aggiunte {len(nuove)} domande -> {len(IT)} totali")

    dom = Counter(q["dominio"] for q in IT)
    BANDE = {"Manage Azure identities and governance": (20, 25),
             "Implement and manage storage": (15, 20),
             "Deploy and manage Azure compute resources": (20, 25),
             "Implement and manage virtual networking": (15, 20),
             "Monitor and maintain Azure resources": (10, 15)}
    print("\n  copertura per dominio:")
    fuori = False
    for d, (lo, hi) in BANDE.items():
        p = dom[d] / len(IT) * 100
        ok = lo <= p <= hi
        fuori = fuori or not ok
        print(f"    {dom[d]:4d}  {p:5.1f}%  {'  ' if ok else '!!'}  (uff. {lo}-{hi}%)  {d}")
    if fuori:
        print("\n  ATTENZIONE: un dominio esce dalla sua banda ufficiale.")

    sotto = Counter(q["sotto_argomento"] for q in IT)
    scoperti = [s for s in TUTTI if sotto[s] == 0]
    sottili = sorted([(sotto[s], s) for s in TUTTI if 0 < sotto[s] < 4])
    print(f"\n  obiettivi a copertura zero: {len(scoperti)}")
    for s in scoperti:
        print(f"      {s}")
    print(f"  obiettivi con meno di 4 domande: {len(sottili)}")
    for n, s in sottili:
        print(f"      {n}  {s}")

    if SCRIVI:
        P_IT.write_text(json.dumps(IT, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"\nscritta la banca ({len(IT)} domande)")
        for p in lotti:
            p.rename(p.with_suffix(".json.aggiunto"))
        print("lotti rinominati in .aggiunto per non riaggiungerli")
    else:
        print("\n(prova a vuoto: rilancia con --scrivi per applicare)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
