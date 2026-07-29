#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Riallinea la chiave di risposta italiana delle hotspot alle scelte italiane.

    python chiavi_hotspot_it.py [--scrivi] ["<cartella repo>"]

Nelle hotspot `risposta_corretta` non contiene lettere ma i VALORI scelti nei
menu. Finche' i menu restavano in inglese in entrambe le banche la chiave poteva
essere identica; appena si traduce una scelta, la chiave italiana deve seguirla,
altrimenti nella banca IT non corrisponde piu' a nulla e la domanda diventa
impossibile.

La corrispondenza si ricava per posizione: la scelta i-esima del menu inglese e
quella i-esima del menu italiano sono la stessa scelta. Per questo i due menu
devono avere lo stesso numero di voci nello stesso ordine - cosa che
test_contenuti.py verifica.
"""
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).parent))
from test_contenuti import hotspot_menu, hotspot_chiavi, norm  # noqa: E402

SCRIVI = "--scrivi" in sys.argv
argv = [a for a in sys.argv[1:] if a != "--scrivi"]
BASE = Path(argv[0]) if argv else Path(__file__).resolve().parent.parent

P_EN = BASE / "banca" / "az104_question_bank.json"
P_IT = BASE / "banca" / "az104_question_bank_it.json"


def main():
    EN = json.loads(P_EN.read_text("utf-8"))
    IT = json.loads(P_IT.read_text("utf-8"))
    mIT = {q["id"]: q for q in IT}

    cambiate, problemi, gia_ok = 0, [], 0
    for q in EN:
        if q["tipo"] != "hotspot":
            continue
        it = mIT.get(q["id"])
        if not it:
            problemi.append(f"{q['id']}: assente nella banca IT")
            continue

        menu_en, menu_it = hotspot_menu(q), hotspot_menu(it)
        if len(menu_en) != len(menu_it):
            problemi.append(f"{q['id']}: {len(menu_en)} menu in EN, {len(menu_it)} in IT")
            continue

        chiavi_en = hotspot_chiavi(q)
        if len(chiavi_en) != len(menu_en) or not all(chiavi_en):
            problemi.append(f"{q['id']}: la chiave inglese non si risolve")
            continue

        nuove = []
        for (ce, _, scelte_en), (ci, _, scelte_it), valore in zip(menu_en, menu_it, chiavi_en):
            if not scelte_en or not scelte_it:
                problemi.append(f"{q['id']}: menu {ce} senza scelte")
                nuove = None
                break
            if len(scelte_en) != len(scelte_it):
                problemi.append(
                    f"{q['id']}: menu {ce} ha {len(scelte_en)} scelte in EN e "
                    f"{len(scelte_it)} in IT, corrispondenza non ricavabile")
                nuove = None
                break
            idx = next((i for i, s in enumerate(scelte_en) if norm(s) == valore), None)
            if idx is None:
                problemi.append(f"{q['id']}: menu {ce}, valore '{valore[:40]}' non fra le scelte EN")
                nuove = None
                break
            nuove.append(scelte_it[idx])
        if nuove is None:
            continue

        chiave_it = ",".join(nuove)
        if chiave_it == it["risposta_corretta"]:
            gia_ok += 1
        else:
            it["risposta_corretta"] = chiave_it
            cambiate += 1

    print(f"hotspot gia' allineate: {gia_ok}")
    print(f"hotspot con chiave IT riscritta: {cambiate}")
    if problemi:
        print(f"\n{len(problemi)} da guardare a mano:")
        for x in problemi[:20]:
            print(f"   - {x}")
        if len(problemi) > 20:
            print(f"   ... e altri {len(problemi) - 20}")

    if SCRIVI:
        P_IT.write_text(json.dumps(IT, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"\nscritta {P_IT.name}")
    else:
        print("\n(prova a vuoto: rilancia con --scrivi per applicare)")
    return 1 if problemi else 0


if __name__ == "__main__":
    sys.exit(main())
