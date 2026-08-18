#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Controlla i contenuti della banca domande.

    python test_contenuti.py ["<cartella repo>"]

I test in JavaScript coprono la *valutazione* (la risposta giusta viene contata
giusta). Questo copre i *dati*: chiavi che puntano a opzioni inesistenti, hotspot
con menu irrisolvibili, sì/No spaiati, campi mancanti,

Esce con codice 1 se trova qualcosa.
"""
import csv
import io
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent

DOMINI = [
    "Manage Azure identities and governance",
    "Implement and manage storage",
    "Deploy and manage Azure compute resources",
    "Implement and manage virtual networking",
    "Monitor and maintain Azure resources",
]
PESI_UFFICIALI = {
    "Manage Azure identities and governance": (20, 25),
    "Implement and manage storage": (15, 20),
    "Deploy and manage Azure compute resources": (20, 25),
    "Implement and manage virtual networking": (15, 20),
    "Monitor and maintain Azure resources": (10, 15),
}
TIPI = {"multiple_choice", "multiple_response", "yes_no_series",
        "hotspot", "drag_drop", "case_study"}
STATI = {"verificata", "contestata", "da_rivedere"}
CAMPI = ["id", "dominio", "sotto_argomento", "tipo", "domanda", "opzione_a", "opzione_b",
         "opzione_c", "opzione_d", "opzione_e", "risposta_corretta", "spiegazione",
         "url_riferimento", "fonte", "url_fonte", "sintesi_commenti", "consenso_community",
         "stato", "difficolta", "tags", "is_generated", "data_verifica"]

problemi = defaultdict(list)


def P(cat, qid, det=""):
    problemi[cat].append((qid, det))


def norm(s):
    return str(s or "").strip().lower()


def split_ans(s):
    return [x.strip() for x in norm(s).split(",") if x.strip()]


def opzioni(q):
    return [(c, (q.get("opzione_" + c) or "").strip())
            for c in "abcde" if (q.get("opzione_" + c) or "").strip()]


def trova_menu(op):
    """Delimita il menu '[...]' contando la profondità delle quadre.

    Un regex non basta: certe scelte annidano quadre proprie, come
    "@allowed(['dev', 'test'])", e chiuderebbero il menu alla prima interna.
    """
    i = op.find("[")
    if i == -1:
        return None
    livello = 0
    for j in range(i, len(op)):
        if op[j] == "[":
            livello += 1
        elif op[j] == "]":
            livello -= 1
            if livello == 0:
                return i, j
    return None


def spezza_scelte(corpo):
    """Divide sul '|' solo a livello zero, ignorando quelli dentro () o []."""
    out, buf, livello = [], [], 0
    for c in corpo:
        if c in "([":
            livello += 1
        elif c in ")]":
            livello -= 1
        if c == "|" and livello == 0:
            out.append("".join(buf).strip())
            buf = []
        else:
            buf.append(c)
    out.append("".join(buf).strip())
    return [x for x in out if x]


def hotspot_menu(q):
    menu = []
    for c, txt in opzioni(q):
        m = trova_menu(txt)
        if not m:
            menu.append((c, txt, None))
        else:
            i, j = m
            menu.append((c, txt[:i].rstrip().rstrip(":").strip(),
                         spezza_scelte(txt[i + 1:j])))
    return menu


def hotspot_chiavi(q):
    """Replica hotspotKeys() del simulatore, virgole dentro i valori comprese."""
    specs = [m[2] or [] for m in hotspot_menu(q)]
    raw = str(q.get("risposta_corretta") or "")
    parts = split_ans(raw)
    allineato = all(
        (not sp) or any(norm(c) == (parts[i] if i < len(parts) else None) for c in sp)
        for i, sp in enumerate(specs))
    if len(parts) == len(specs) and allineato:
        return parts
    rawN, cur, out = norm(raw), 0, []
    for sp in specs:
        best, pos = None, len(rawN) + 1
        for c in sp:
            p = rawN.find(norm(c), cur)
            if p < 0:
                continue
            if p < pos or (p == pos and best and len(c) > len(best)):
                best, pos = c, p
        if best:
            out.append(norm(best))
            cur = pos + len(norm(best))
        else:
            out.append(parts[len(out)] if len(out) < len(parts) else "")
    return out


def audit(banca, tag):
    for qid, n in Counter(q.get("id") for q in banca).items():
        if n > 1:
            P(f"{tag}: id duplicato", qid, f"{n} occorrenze")

    for q in banca:
        qid = q.get("id", "?")
        for c in CAMPI:
            if c not in q:
                P(f"{tag}: campo mancante", qid, c)

        if q.get("dominio") not in DOMINI:
            P(f"{tag}: dominio non valido", qid, repr(q.get("dominio")))
        if q.get("tipo") not in TIPI:
            P(f"{tag}: tipo non valido", qid, repr(q.get("tipo")))
        if q.get("stato") not in STATI:
            P(f"{tag}: stato non valido", qid, repr(q.get("stato")))
        if q.get("difficolta") not in (1, 2, 3):
            P(f"{tag}: difficoltà non valida", qid, repr(q.get("difficolta")))
        if not (q.get("sotto_argomento") or "").strip():
            P(f"{tag}: sotto_argomento vuoto", qid)
        if not (q.get("domanda") or "").strip():
            P(f"{tag}: domanda vuota", qid)
        if len((q.get("spiegazione") or "").strip()) < 60:
            P(f"{tag}: spiegazione troppo corta", qid)

        url = (q.get("url_riferimento") or "").strip()
        if not url:
            P(f"{tag}: url_riferimento mancante", qid)
        elif not url.startswith("https://learn.microsoft.com/"):
            P(f"{tag}: url_riferimento non punta a Learn", qid, url[:80])

        ops = opzioni(q)
        lettere = [c for c, _ in ops]
        tipo, key = q.get("tipo"), q.get("risposta_corretta") or ""

        if lettere and lettere != list("abcde")[:len(lettere)]:
            P(f"{tag}: opzioni non contigue", qid, ",".join(lettere))
        dup = [t for t, n in Counter(norm(t) for _, t in ops).items() if n > 1]
        if dup:
            P(f"{tag}: due opzioni identiche", qid, dup[0][:60])

        if not str(key).strip():
            P(f"{tag}: risposta_corretta vuota", qid)
            continue

        if tipo in ("multiple_choice", "case_study"):
            a = split_ans(key)
            if len(ops) < 3:
                P(f"{tag}: meno di 3 opzioni", qid, f"{len(ops)}")
            if len(a) != 1:
                P(f"{tag}: chiave non singola", qid, key)
            elif a[0] not in lettere:
                P(f"{tag}: chiave fuori range", qid, f"{key} · opzioni {lettere}")

        elif tipo == "multiple_response":
            a = split_ans(key)
            if len(a) < 2:
                P(f"{tag}: scelta multipla con una sola chiave", qid, key)
            if len(set(a)) != len(a):
                P(f"{tag}: chiave con ripetizioni", qid, key)
            if [x for x in a if x not in lettere]:
                P(f"{tag}: chiave fuori range", qid, f"{key} · opzioni {lettere}")
            if len(a) >= len(ops):
                P(f"{tag}: tutte le opzioni sono corrette", qid, f"{len(a)}/{len(ops)}")

        elif tipo == "yes_no_series":
            a = split_ans(key)
            if [x for x in a if x not in ("yes", "no")]:
                P(f"{tag}: valori estranei in una serie Sì/No", qid, key)
            if len(a) != len(ops):
                P(f"{tag}: serie Sì/No spaiata", qid,
                  f"{len(a)} risposte per {len(ops)} affermazioni")

        elif tipo == "drag_drop":
            a = split_ans(key)
            # La chiave può essere più corta: le opzioni in eccesso sono
            # distrattori da lasciare fuori dall'area risposta.
            if len(set(a)) != len(a):
                P(f"{tag}: ordine con ripetizioni", qid, key)
            if [x for x in a if x not in lettere]:
                P(f"{tag}: ordine fuori range", qid, f"{key} · opzioni {lettere}")
            if len(a) < 2:
                P(f"{tag}: ordinamento con meno di 2 passaggi", qid, key)

        elif tipo == "hotspot":
            menu = hotspot_menu(q)
            senza = [c for c, _, ch in menu if not ch]
            if senza:
                P(f"{tag}: hotspot senza menu", qid, f"opzione {','.join(senza)}")
                continue
            got = hotspot_chiavi(q)
            if len(got) != len(menu):
                P(f"{tag}: hotspot, valori e menu non tornano", qid,
                  f"{len(got)} vs {len(menu)}")
                continue
            for (c, lab, scelte), g in zip(menu, got):
                if not g:
                    P(f"{tag}: hotspot, valore non risolto", qid, f"menu {c} ({lab[:40]})")
                elif not any(norm(x) == g for x in scelte):
                    P(f"{tag}: hotspot, valore fuori dal menu", qid, f"menu {c}: '{g}'")
                if len(scelte) < 2:
                    P(f"{tag}: hotspot, menu con una sola scelta", qid, f"menu {c}")
                if len(set(norm(x) for x in scelte)) != len(scelte):
                    P(f"{tag}: hotspot, scelte duplicate nel menu", qid, f"menu {c}")

        # Terminologia ritirata. Il confronto è CASE SENSITIVE di proposito:
        # in italiano "Azure ad accesso pubblico" non è "Azure AD".
        testo = " ".join(str(q.get(f) or "") for f in
                         ("domanda", "opzione_a", "opzione_b", "opzione_c",
                          "opzione_d", "opzione_e"))
        for pat, nome in [
            (r"\bAzure Active Directory\b", "Azure Active Directory → Microsoft Entra ID"),
            (r"\bAzure AD\b", "Azure AD → Microsoft Entra ID"),
            (r"\bAzureRM\b", "modulo AzureRM ritirato"),
            (r"\bMicrosoft Monitoring Agent\b", "MMA ritirato → Azure Monitor Agent"),
        ]:
            if re.search(pat, testo):
                P(f"{tag}: terminologia ritirata nel testo della domanda", qid, nome)


def duplicati(banca):
    visti = {}
    for q in banca:
        t = unicodedata.normalize("NFKD", norm(q.get("domanda")))
        t = re.sub(r"[^a-z0-9 ]", " ", t)
        f = " ".join(sorted(set(w for w in t.split() if len(w) > 3)))
        if f in visti:
            P("possibile duplicato semantico", q["id"], f"~ {visti[f]}")
        visti[f] = q["id"]


def readme(IT):
    """I numeri scritti nel README.

    Sono a mano dentro la prosa e nessuno li ricalcola: la pagina di ripasso ha
    annunciato "532 domande" per settimane mentre ne conteneva 591, e a
    rileggerla non se n'era accorto nessuno. Qui si confrontano con la banca.
    """
    f = BASE / "README.md"
    if not f.exists():
        P("numeri del README", "README.md", "non esiste")
        return

    testo = f.read_text("utf-8")
    piatto = re.sub(r"\s+", " ", testo)  # il README va a capo a meta' frase

    tot = len(IT)
    ver = sum(1 for q in IT if q["stato"] == "verificata")
    dom = Counter(q["dominio"] for q in IT)
    tipi = Counter(q["tipo"] for q in IT)
    diff = Counter(q["difficolta"] for q in IT)

    def pretende(frase, cosa):
        if frase not in piatto:
            P("numeri del README", cosa, f"non dice piu' «{frase}»")

    pretende(f"{tot} domande", "totale")
    pretende(f"{ver} domande su {tot} hanno una verifica indipendente", "verificate")
    pretende(f"{tot - ver} risposte su {tot} non hanno una verifica indipendente", "da rivedere")
    pretende(f"{len(set(q['sotto_argomento'] for q in IT))} obiettivi", "obiettivi")

    # Tabella copertura: riconosco la riga dal nome ufficiale, che e' la chiave
    # vera. L'etichetta italiana accanto puo' cambiare senza rompere niente.
    for d in DOMINI:
        riga = re.search(re.escape(d) + r"</sub>\s*\|\s*(\d+)\s*\|\s*([\d,]+)%\s*\|\s*([\d–-]+)%", testo)
        if not riga:
            P("numeri del README", d, "riga della tabella copertura non trovata")
            continue
        n, perc, peso = int(riga.group(1)), riga.group(2).replace(",", "."), riga.group(3)
        if n != dom[d]:
            P("numeri del README", d, f"dice {n} domande, ne ha {dom[d]}")
        atteso = f"{dom[d] / tot * 100:.1f}"
        if perc != atteso:
            P("numeri del README", d, f"dice {perc}%, e' {atteso}%")
        lo, hi = PESI_UFFICIALI[d]
        if peso != f"{lo}–{hi}":
            P("numeri del README", d, f"peso ufficiale {peso}% invece di {lo}–{hi}%")

    for chiave, nome in (("multiple_choice", "scelta singola"), ("hotspot", "hotspot"),
                         ("multiple_response", "scelta multipla"), ("yes_no_series", "serie Sì/No"),
                         ("drag_drop", "drag-and-drop"), ("case_study", "case study")):
        pretende(f"{tipi[chiave]} {nome}", f"tipo {nome}")

    for chiave, nome in ((1, "base"), (2, "applicativa"), (3, "scenario")):
        pretende(f"{diff[chiave]} {nome}", f"difficoltà {nome}")


def main():
    IT = json.loads((BASE / "banca" / "az104_question_bank_it.json").read_text("utf-8"))

    audit(IT, "banca")
    duplicati(IT)
    readme(IT)

    print(f"Banca {len(IT)} domande" + chr(10))
    dom = Counter(q["dominio"] for q in IT)
    for d in DOMINI:
        n, (lo, hi) = dom[d], PESI_UFFICIALI[d]
        p = n / len(IT) * 100
        segno = "  " if lo <= p <= hi else "!!"
        print(f"  {n:4d}  {p:5.1f}%  {segno}  (uff. {lo}-{hi}%)  {d}")
        if not lo <= p <= hi:
            P("copertura fuori dai pesi ufficiali", d, f"{p:.1f}% invece di {lo}-{hi}%")

    print(f"\n  tipi:        {dict(Counter(q['tipo'] for q in IT))}")
    print(f"  stati:       {dict(Counter(q['stato'] for q in IT))}")
    print(f"  difficoltà:  {dict(Counter(q['difficolta'] for q in IT))}")
    print(f"  sotto-arg.:  {len(set(q['sotto_argomento'] for q in IT))} distinti")

    tot = sum(len(v) for v in problemi.values())
    print()
    if not tot:
        print("Tutto verde: banca senza problemi.")
        return 0
    print(f"{tot} problemi:\n")
    for cat in sorted(problemi, key=lambda c: -len(problemi[c])):
        v = problemi[cat]
        print(f"### {cat}  ({len(v)})")
        for qid, det in v[:12]:
            print(f"    {qid}  {det}")
        if len(v) > 12:
            print(f"    ... e altri {len(v) - 12}")
        print()
    return 1


if __name__ == "__main__":
    sys.exit(main())
