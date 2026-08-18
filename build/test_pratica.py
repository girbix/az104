#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Controlla i lab della sezione Pratica.

    python test_pratica.py ["<cartella repo>"]

Due cose che nessun altro test guarda.

La copertura: i lab sono legati agli stessi 82 obiettivi ufficiali delle
lezioni e delle domande. Un obiettivo scritto storto non da' errore, rompe solo
il collegamento fra le pagine — e non se ne accorge nessuno finche' non ci
clicca sopra.

La pulizia: questi lab creano risorse vere su una sottoscrizione vera. Un lab
che accende una macchina e non dice come spegnerla costa soldi a chi lo segue.
Per i lab marcati «si paga a ore» la sezione Pulizia deve contenere un comando
che cancella davvero.

Esce con codice 1 se trova qualcosa.
"""
import json
import re
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

errori = []
ko = errori.append


def ok(m):
    print(f"  ok    {m}")


def main():
    lab = []
    for p in sorted((BASE / "pratica").glob("*.json")):
        lab += json.loads(p.read_text("utf-8"))
    print(f"Lab: {len(lab)}\n")

    tutti = {o for lista in UFFICIALI.values() for o in lista}

    # ---- 1. ogni obiettivo ufficiale ha almeno un lab
    coperti = {o for l in lab for o in l["obiettivi"]}
    fuori = sorted(coperti - tutti)
    scoperti = sorted(tutti - coperti)
    if fuori:
        ko(f"obiettivi fuori tassonomia: {fuori[:3]}")
    elif scoperti:
        ko(f"{len(scoperti)} obiettivi senza nessun lab: {scoperti[:3]}")
    else:
        ok(f"tutti gli {len(tutti)} obiettivi hanno almeno un lab")

    # ---- 2. l'obiettivo appartiene al dominio dichiarato dal lab
    incoerenti = [
        f"{l['id']} -> {o}"
        for l in lab for o in l["obiettivi"]
        if o in tutti and DOMINI[dominio_di(o)] != l["d"]
    ]
    if incoerenti:
        ko(f"obiettivi nel dominio sbagliato: {incoerenti[:3]}")
    else:
        ok("ogni obiettivo sta nel dominio del suo lab")

    # ---- 3. identificativi unici e in ordine
    ids = [l["id"] for l in lab]
    if len(set(ids)) != len(ids):
        ko("identificativi ripetuti")
    elif ids != sorted(ids):
        ko("gli identificativi non sono in ordine")
    else:
        ok(f"{len(ids)} identificativi, unici e in ordine")

    # ---- 4. costo dichiarato, e coerente con quello che il lab accende
    male = [l["id"] for l in lab if l.get("costo") not in COSTI]
    if male:
        ko(f"costo non riconosciuto: {male}")
    else:
        ok("ogni lab dichiara quanto costa")

    ACCENDE = re.compile(r"\baz (vm|vmss) create|az network bastion create|"
                         r"az containerapp env create|az appservice plan create|az acr create", re.I)
    sottostimati = [
        l["id"] for l in lab
        if l.get("costo") != "ore" and ACCENDE.search(l.get("cli", "") + " ".join(l["passi"]))
    ]
    if sottostimati:
        ko(f"accendono risorse a consumo ma non lo dicono: {sottostimati}")
    else:
        ok("nessun lab accende risorse a ore senza avvisare")

    # ---- 5. la pulizia c'e', e per i lab cari cancella davvero
    CANCELLA = re.compile(r"\baz \w[\w -]* delete\b|Disable replication|Delete", re.I)
    senza = [l["id"] for l in lab if not l.get("pulizia", "").strip()]
    finte = [
        l["id"] for l in lab
        if l.get("costo") == "ore" and not CANCELLA.search(l.get("pulizia", ""))
    ]
    if senza:
        ko(f"lab senza sezione Pulizia: {senza}")
    elif finte:
        ko(f"lab a pagamento la cui pulizia non cancella niente: {finte}")
    else:
        n = sum(1 for l in lab if l["costo"] == "ore")
        ok(f"tutti hanno la pulizia, e i {n} lab a ore cancellano davvero")

    # ---- 6. i link ai lab ufficiali puntano dove dicono
    esterni = [l.get("lab", {}).get("u", "") for l in lab if l.get("lab")]
    strani = [u for u in esterni if not u.startswith("https://microsoftlearning.github.io/")]
    if strani:
        ko(f"link a lab ufficiali fuori dal dominio Microsoft: {strani[:2]}")
    else:
        ok(f"{len(esterni)} rimandi al lab ufficiale, tutti su microsoftlearning.github.io")

    # ---- 7. il tempo dichiarato e' plausibile
    assurdi = [l["id"] for l in lab if not 10 <= l.get("min", 0) <= 120]
    if assurdi:
        ko(f"durata fuori scala (attesi 10-120 min): {assurdi}")
    else:
        ore = sum(l["min"] for l in lab) / 60
        ok(f"durate plausibili, {ore:.1f} ore in tutto")

    print()
    for d, i in DOMINI.items():
        n = sum(1 for l in lab if l["d"] == i)
        m = sum(l["min"] for l in lab if l["d"] == i)
        print(f"  {n:3d} lab  {m:4d} min   {d}")

    print()
    if not errori:
        print("Tutto verde: i lab coprono la tassonomia e sanno smontare quello che accendono.")
        return 0
    for e in errori:
        print(f"  FAIL  {e}")
    print(f"\n{len(errori)} problemi.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
