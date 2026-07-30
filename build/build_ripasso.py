#!/usr/bin/env python3
"""Costruisce az104_ripasso.html: la banca domande in una pagina sola per telefono.

    python build_ripasso.py "<cartella AZ-104>"

Legge az104_question_bank_it.json e ripasso_template.html, inietta i dati
compattati e scrive az104_ripasso.html.

Il payload viene ridotto ai soli campi che la pagina usa (via ~25% di peso) e le
risposte vengono pre-risolte qui, a build time, cosi il JS non deve interpretare
i sei formati diversi di risposta_corretta.
"""
import json
import re
import sys
from pathlib import Path

DOMINI = {
    "Manage Azure identities and governance": 1,
    "Implement and manage storage": 2,
    "Deploy and manage Azure compute resources": 3,
    "Implement and manage virtual networking": 4,
    "Monitor and maintain Azure resources": 5,
}

def trova_menu(opzione):
    """Delimita il menu '[...]' contando la profondita' delle quadre.

    Un regex non basta: certe scelte annidano quadre proprie, come
    "@allowed(['dev', 'test', 'prod'])", e un match non bilanciato chiuderebbe
    il menu alla prima quadra interna.
    """
    inizio = opzione.find("[")
    if inizio == -1:
        return None
    livello = 0
    for i in range(inizio, len(opzione)):
        if opzione[i] == "[":
            livello += 1
        elif opzione[i] == "]":
            livello -= 1
            if livello == 0:
                return inizio, i
    return None


def spezza_scelte(corpo):
    """Divide sul '|' solo a livello zero, ignorando quelli dentro () o []."""
    scelte, buffer, livello = [], [], 0
    for c in corpo:
        if c in "[(":
            livello += 1
        elif c in "])":
            livello -= 1
        if c == "|" and livello == 0:
            scelte.append("".join(buffer).strip())
            buffer = []
        else:
            buffer.append(c)
    scelte.append("".join(buffer).strip())
    return [s for s in scelte if s]


def leggi_menu(opzione):
    span = trova_menu(opzione)
    if not span:
        return {"l": opzione.strip(), "c": []}
    a, b = span
    return {
        "l": opzione[:a].strip().rstrip(":").strip(),
        "c": spezza_scelte(opzione[a + 1 : b]),
    }


def risolvi_hotspot(opzioni, risposta):
    """Allinea i valori di risposta_corretta ai menu, in ordine.

    risposta_corretta e' la concatenazione dei valori separati da virgola, uno
    per menu. Non si puo' splittare sulle virgole perche' alcuni valori ne
    contengono di proprie: si consuma la stringa da sinistra, menu per menu,
    cercando quale scelta la prefissa. A parita' vince la piu' lunga, cosi
    "Succeeds" non ruba il posto a "Succeeds - the lock is inherited".
    """
    menu = [leggi_menu(o) for o in opzioni]
    resto = risposta.strip()
    for m in menu:
        resto = resto.lstrip(" ,")
        candidati = [s for s in m["c"] if resto.startswith(s)]
        if candidati:
            scelta = max(candidati, key=len)
            m["k"] = scelta
            resto = resto[len(scelta) :]
        else:
            m["k"] = None
    if all(m["k"] for m in menu) and not resto.strip(" ,"):
        return menu, True
    # Ripiego: match per contenuto, meno affidabile ma recupera i casi storti.
    for m in menu:
        if m["k"]:
            continue
        presenti = [s for s in m["c"] if s and s in risposta]
        m["k"] = max(presenti, key=len) if presenti else None
    return menu, False


def compatta(q, problemi):
    tipo = q["tipo"]
    risposta = q["risposta_corretta"]
    opzioni = [q.get(f"opzione_{c}") or "" for c in "abcde"]
    opzioni = [o for o in opzioni if o.strip()]

    out = {
        "id": q["id"],
        "d": DOMINI[q["dominio"]],
        "s": q["sotto_argomento"],
        "t": tipo,
        "q": q["domanda"],
        "e": q["spiegazione"],
        "u": q["url_riferimento"],
        "df": q["difficolta"],
        "tg": [t.strip() for t in (q.get("tags") or "").split(",") if t.strip()],
        "v": q["stato"] == "verificata",
    }
    if q["stato"] == "contestata":
        out["ct"] = True

    if tipo == "hotspot":
        menu, sequenziale = risolvi_hotspot(opzioni, risposta)
        irrisolti = [m["l"] for m in menu if m["k"] is None]
        if irrisolti:
            problemi.append(f"{q['id']}: menu hotspot non risolti -> {irrisolti}")
        elif not sequenziale:
            problemi.append(f"{q['id']}: hotspot risolto solo per contenuto, ricontrollare")
        out["o"] = menu
    elif tipo == "yes_no_series":
        valori = [v.strip() for v in risposta.split(",")]
        if len(valori) != len(opzioni):
            problemi.append(
                f"{q['id']}: {len(opzioni)} affermazioni ma {len(valori)} risposte"
            )
        out["o"] = opzioni
        out["a"] = valori
    elif tipo == "drag_drop":
        ordine = [v.strip().lower() for v in risposta.split(",")]
        lettere = "abcde"[: len(opzioni)]
        # Un drag_drop puo' chiedere N azioni su piu' opzioni: le restanti sono
        # distrattori e non vanno ordinate. Sospetto solo un ordine incoerente.
        fuori = [l for l in ordine if l not in lettere]
        if fuori or len(set(ordine)) != len(ordine):
            problemi.append(f"{q['id']}: ordine drag_drop incoerente -> {risposta}")
        out["o"] = opzioni
        out["a"] = ordine
    else:  # multiple_choice, multiple_response, case_study
        lettere = [v.strip().lower() for v in risposta.split(",")]
        fuori = [l for l in lettere if l not in "abcde"[: len(opzioni)]]
        if fuori:
            problemi.append(f"{q['id']}: risposta fuori range -> {fuori}")
        out["o"] = opzioni
        out["a"] = lettere
    return out


def main():
    if len(sys.argv) < 2:
        sys.exit("uso: build_ripasso.py <cartella AZ-104>")
    base = Path(sys.argv[1])
    banca = json.loads((base / "az104_question_bank_it.json").read_text("utf-8"))
    template = (Path(__file__).parent / "ripasso_template.html").read_text("utf-8")

    problemi = []
    domande = [compatta(q, problemi) for q in banca]

    payload = json.dumps(domande, ensure_ascii=False, separators=(",", ":"))
    # </script> dentro una spiegazione chiuderebbe il tag: \/ e' escape JSON valido.
    payload = payload.replace("</", "<\\/")

    if "/*__DATI__*/[]" not in template:
        sys.exit("ERRORE: segnaposto /*__DATI__*/[] non trovato nel template")
    html = template.replace("/*__DATI__*/[]", payload)

    out = base / "az104_ripasso.html"
    out.write_text(html, encoding="utf-8")

    print(f"Domande:   {len(domande)}")
    print(f"Verificate: {sum(1 for d in domande if d['v'])}")
    for n, tipo in sorted(
        ((sum(1 for d in domande if d["t"] == t), t) for t in {d["t"] for d in domande}),
        reverse=True,
    ):
        print(f"  {n:>4}  {tipo}")
    print(f"Scritto:   {out}  ({out.stat().st_size / 1024:.0f} KB)")
    if problemi:
        print(f"\n!! {len(problemi)} PROBLEMI DI PARSING:")
        for p in problemi:
            print(f"   {p}")
    else:
        print("\nParsing pulito: 0 problemi.")


if __name__ == "__main__":
    main()
