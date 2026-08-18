#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Costruisce pratica.html: i lab guidati in una pagina sola, autosufficiente.

    python build_pratica.py ["<cartella repo>"]

Legge pratica/*.json e pratica_template.html, inietta i dati e scrive
pratica.html nella radice. Come le altre pagine: nessun CDN, nessuna richiesta
esterna, funziona anche da file://.

Gli obiettivi di ogni lab sono le stesse chiavi delle lezioni e delle domande.
E' quello che tiene insieme le quattro pagine: dalla lezione al lab, dal lab
alle domande. Un obiettivo scritto storto rompe il giro senza dare errore, per
questo qui viene rifiutato.
"""
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
QUI = Path(__file__).parent

sys.path.insert(0, str(QUI))
from tassonomia import UFFICIALI, dominio_di  # noqa: E402

DOMINI = {d: i + 1 for i, d in enumerate(UFFICIALI)}
COSTI = {"gratis", "centesimi", "ore"}
CAMPI = ["id", "d", "t", "min", "costo", "obiettivi", "perche", "passi", "verifica", "pulizia"]


def main():
    lab = []
    for p in sorted((BASE / "pratica").glob("*.json")):
        lab += json.loads(p.read_text("utf-8"))
    if not lab:
        sys.exit("ERRORE: nessun lab in pratica/")

    tutti = {o for lista in UFFICIALI.values() for o in lista}
    problemi = []
    visti = set()
    for l in lab:
        for c in CAMPI:
            if c not in l or l[c] in ("", [], None):
                problemi.append(f"{l.get('id', '?')}: manca il campo {c}")
        if l.get("id") in visti:
            problemi.append(f"{l['id']}: id ripetuto")
        visti.add(l.get("id"))
        if l.get("costo") not in COSTI:
            problemi.append(f"{l.get('id')}: costo '{l.get('costo')}' fuori da {sorted(COSTI)}")
        for o in l.get("obiettivi", []):
            if o not in tutti:
                problemi.append(f"{l.get('id')}: obiettivo fuori tassonomia -> {o}")
            elif DOMINI[dominio_di(o)] != l.get("d"):
                problemi.append(f"{l.get('id')}: l'obiettivo '{o}' non e' del dominio {l.get('d')}")
    if problemi:
        for p in problemi:
            print("  " + p)
        sys.exit(f"ERRORE: {len(problemi)} problemi nei lab.")

    lab.sort(key=lambda l: l["id"])

    template = (QUI / "pratica_template.html").read_text("utf-8")
    if "/*__DATI__*/[]" not in template:
        sys.exit("ERRORE: segnaposto /*__DATI__*/[] non trovato nel template")

    payload = json.dumps(lab, ensure_ascii=False, separators=(",", ":"))
    # </script> dentro un comando chiuderebbe il tag: <\/ e' escape JSON valido
    payload = payload.replace("</", "<\\/")

    out = BASE / "pratica.html"
    out.write_text(template.replace("/*__DATI__*/[]", payload), encoding="utf-8")

    coperti = {o for l in lab for o in l["obiettivi"]}
    print(f"Lab:      {len(lab)}")
    for d, i in DOMINI.items():
        n = sum(1 for x in lab if x["d"] == i)
        m = sum(x["min"] for x in lab if x["d"] == i)
        print(f"  {n:3d} lab, {m:4d} min   {d}")
    print(f"\nObiettivi toccati: {len(coperti)} di {len(tutti)}")
    print(f"Tempo totale:      {sum(l['min'] for l in lab) / 60:.1f} ore")
    print(f"\nScritto:  {out.name}  ({out.stat().st_size / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
