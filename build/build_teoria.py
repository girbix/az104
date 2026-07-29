#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Costruisce studia.html: le 82 lezioni in una pagina sola, autosufficiente.

    python build_teoria.py ["<cartella repo>"]

Legge teoria/*.json e teoria_template.html, inietta i dati compattati e scrive
studia.html nella radice. Come le altre pagine: nessun CDN, nessuna richiesta
esterna, funziona anche da file://.
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

# stesso ordine e stessa numerazione delle altre pagine
DOMINI = {d: i + 1 for i, d in enumerate(UFFICIALI)}


def main():
    lezioni = []
    for p in sorted((BASE / "teoria").glob("*.json")):
        lezioni += json.loads(p.read_text("utf-8"))

    ordine = {o: i for i, o in enumerate(o for lista in UFFICIALI.values() for o in lista)}
    mancanti = [l["titolo"] for l in lezioni if l["obiettivo"] not in ordine]
    if mancanti:
        sys.exit(f"ERRORE: lezioni fuori tassonomia: {mancanti}")
    lezioni.sort(key=lambda l: ordine[l["obiettivo"]])

    # payload ridotto ai soli campi che la pagina usa
    dati = [{
        "o": l["obiettivo"],
        "t": l["titolo"],
        "d": DOMINI[dominio_di(l["obiettivo"])],
        "c": l["concetto"],
        "es": l["esempio"],
        "tr": l["esame"],
        "u": l["learn"],
    } for l in lezioni]

    template = (QUI / "teoria_template.html").read_text("utf-8")
    if "/*__DATI__*/[]" not in template:
        sys.exit("ERRORE: segnaposto /*__DATI__*/[] non trovato nel template")

    payload = json.dumps(dati, ensure_ascii=False, separators=(",", ":"))
    # </script> dentro una lezione chiuderebbe il tag: <\/ e' escape JSON valido
    payload = payload.replace("</", "<\\/")

    out = BASE / "studia.html"
    out.write_text(template.replace("/*__DATI__*/[]", payload), encoding="utf-8")

    print(f"Lezioni:  {len(dati)}")
    for d, i in DOMINI.items():
        print(f"  {sum(1 for x in dati if x['d'] == i):3d}  {d}")
    print(f"\nScritto:  {out.name}  ({out.stat().st_size / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
