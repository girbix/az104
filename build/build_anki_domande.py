#!/usr/bin/env python3
"""Converte le 532 domande d'esame in un mazzo Anki.

    python build_anki_domande.py "<cartella AZ-104>"

Perche' esiste: Firefox Android e DuckDuckGo non aprono i file locali (file://),
quindi il ripasso HTML sul telefono non e' garantito. AnkiDroid e' un'app nativa:
niente browser, niente file://, funziona offline sempre.

Il parsing delle risposte NON viene riscritto: si importa da build_ripasso.py, che
e' gia' verificato da test_ripasso.js. Una sola fonte di verita' per i sei formati.

Le card finiscono in AZ104::Domande::<dominio>, separate dalle flashcard atomiche
di AZ104::<dominio>: sono due cose diverse e vanno ripassate a ritmi diversi.
"""
import csv
import html
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build_ripasso import DOMINI, compatta  # noqa: E402
import json  # noqa: E402

DOM_IT = {
    1: "01 Identità e governance",
    2: "02 Storage",
    3: "03 Compute",
    4: "04 Networking",
    5: "05 Monitoraggio",
}
DOM_TAG = {1: "identita", 2: "storage", 3: "compute", 4: "networking", 5: "monitoraggio"}
TIPO_IT = {
    "multiple_choice": "Scelta singola",
    "multiple_response": "Scelta multipla",
    "hotspot": "Hotspot",
    "yes_no_series": "Serie Sì/No",
    "drag_drop": "Ordinamento",
    "case_study": "Case study",
}
TIPO_TAG = {
    "multiple_choice": "scelta-singola",
    "multiple_response": "scelta-multipla",
    "hotspot": "hotspot",
    "yes_no_series": "si-no",
    "drag_drop": "ordinamento",
    "case_study": "case-study",
}
DIFF_TAG = {1: "base", 2: "applicativa", 3: "scenario"}
LETTERE = ["A", "B", "C", "D", "E"]

# Anki centra il testo di default: illeggibile su domande lunghe.
SX = "text-align:left"


def e(s):
    return html.escape(str(s))


def fronte(d):
    p = [f'<div style="{SX};font-size:.72em;opacity:.6">{e(d["id"])} · {e(TIPO_IT[d["t"]])}</div>']
    p.append(f'<div style="{SX};margin:.6em 0">{e(d["q"])}</div>')

    if d["t"] == "hotspot":
        for m in d["o"]:
            scelte = " &nbsp;|&nbsp; ".join(e(c) for c in m["c"])
            p.append(
                f'<div style="{SX};margin:.45em 0">'
                f'<b>{e(m["l"])}</b><br><span style="opacity:.75">{scelte}</span></div>'
            )
    elif d["t"] == "yes_no_series":
        p.append(f'<div style="{SX};opacity:.6;font-size:.8em">Sì o no per ognuna:</div>')
        p.append(f'<ol style="{SX};margin:.3em 0 0 1.1em">')
        for o in d["o"]:
            p.append(f"<li>{e(o)}</li>")
        p.append("</ol>")
    elif d["t"] == "drag_drop":
        p.append(f'<div style="{SX};opacity:.6;font-size:.8em">Mettile in ordine:</div>')
        p.append(f'<ul style="{SX};margin:.3em 0 0 1.1em">')
        for i, o in enumerate(d["o"]):
            p.append(f"<li><b>{LETTERE[i]}.</b> {e(o)}</li>")
        p.append("</ul>")
    else:
        p.append(f'<ul style="{SX};list-style:none;margin:.3em 0;padding:0">')
        for i, o in enumerate(d["o"]):
            p.append(f'<li style="margin:.25em 0"><b>{LETTERE[i]}.</b> {e(o)}</li>')
        p.append("</ul>")
    return "".join(p)


def risposta_breve(d):
    if d["t"] == "hotspot":
        return " · ".join(m["k"] or "?" for m in d["o"])
    if d["t"] == "yes_no_series":
        return " · ".join("SÌ" if v == "Yes" else "NO" for v in d["a"])
    if d["t"] == "drag_drop":
        return " → ".join(l.upper() for l in d["a"])
    return " + ".join(l.upper() for l in d["a"])


def retro(d):
    p = [
        f'<div style="{SX};font-weight:700;color:#2c7a58;margin-bottom:.5em">'
        f'{e(risposta_breve(d))}</div>'
    ]

    # Per hotspot e si/no la risposta breve da sola non dice a cosa si riferisce.
    if d["t"] == "hotspot":
        for m in d["o"]:
            p.append(
                f'<div style="{SX};font-size:.85em;margin:.2em 0">'
                f'{e(m["l"])}: <b>{e(m["k"] or "?")}</b></div>'
            )
    elif d["t"] == "yes_no_series":
        for i, o in enumerate(d["o"]):
            v = d["a"][i] if i < len(d["a"]) else "?"
            col = "#2c7a58" if v == "Yes" else "#86949e"
            p.append(
                f'<div style="{SX};font-size:.85em;margin:.2em 0">'
                f'<b style="color:{col}">{"SÌ" if v == "Yes" else "NO"}</b> — {e(o)}</div>'
            )
    elif d["t"] == "drag_drop":
        for pos, l in enumerate(d["a"], 1):
            i = "abcde".index(l)
            if i < len(d["o"]):
                p.append(
                    f'<div style="{SX};font-size:.85em;margin:.2em 0">'
                    f'<b>{pos}.</b> {e(d["o"][i])}</div>'
                )
        esclusi = [o for i, o in enumerate(d["o"]) if "abcde"[i] not in d["a"]]
        for o in esclusi:
            p.append(f'<div style="{SX};font-size:.8em;opacity:.5">non si usa — {e(o)}</div>')

    p.append(f'<hr style="margin:.7em 0;border:0;border-top:1px solid #ccc">')
    p.append(f'<div style="{SX};font-size:.82em;line-height:1.5">{e(d["e"])}</div>')

    if not d["v"]:
        p.append(
            f'<div style="{SX};font-size:.75em;color:#9c5c12;margin-top:.6em">'
            f"⚠ Risposta non verificata in modo indipendente: controlla il link.</div>"
        )
    p.append(
        f'<div style="{SX};font-size:.72em;margin-top:.5em">'
        f'<a href="{e(d["u"])}">{e(d["u"].replace("https://learn.microsoft.com", "learn.microsoft.com"))}</a></div>'
    )
    return "".join(p)


def tag(d):
    t = ["domande", DOM_TAG[d["d"]], TIPO_TAG[d["t"]], DIFF_TAG[d["df"]]]
    t.append("verificata" if d["v"] else "da-rivedere")
    return " ".join(t)


def genera(base, out_dir):
    """Scrive il CSV del mazzo domande. Ritorna (percorso, numero di card)."""
    banca = json.loads((base / "az104_question_bank_it.json").read_text("utf-8"))

    problemi = []
    domande = [compatta(q, problemi) for q in banca]
    if problemi:
        for p in problemi:
            print(f"   {p}")
        sys.exit(f"Build fermata: {len(problemi)} problemi di parsing da sistemare prima.")

    buf = io.StringIO()
    # QUOTE_ALL: le domande contengono ; e virgolette, il quoting le salva tutte.
    w = csv.writer(buf, delimiter=";", quoting=csv.QUOTE_ALL, lineterminator="\n")
    for d in domande:
        w.writerow([fronte(d), retro(d), tag(d), f"AZ104::Domande::{DOM_IT[d['d']]}"])

    testata = (
        "#separator:Semicolon\n"
        "#html:true\n"
        "#tags column:3\n"
        "#deck column:4\n"
        "#notetype:Basic\n"
    )
    out = out_dir / "az104_domande_esame.csv"
    out.write_text(testata + buf.getvalue(), encoding="utf-8")
    return out, len(domande), domande


def main():
    if len(sys.argv) < 2:
        sys.exit("uso: build_anki_domande.py <cartella AZ-104>")
    base = Path(sys.argv[1])
    out_dir = base / "telefono"
    out_dir.mkdir(exist_ok=True)
    out, n, domande = genera(base, out_dir)

    print(f"Card scritte: {n}")
    for k in sorted(DOM_IT):
        print(f"  {sum(1 for d in domande if d['d'] == k):>4}  {DOM_IT[k]}")
    print(f"\nNon verificate: {sum(1 for d in domande if not d['v'])} (tag da-rivedere)")
    print(f"Scritto: {out}  ({out.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
