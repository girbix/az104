#!/usr/bin/env python3
"""Assembla la repo pubblica per GitHub Pages.

    python build_sito.py "<cartella AZ-104>" <utente-github> [nome-repo]

Perche' esiste: Firefox e DuckDuckGo su Android non aprono i file locali
(file://), quindi il bundle offline non parte sul telefono. Servito da GitHub
Pages via HTTPS il problema sparisce: qualsiasi browser lo apre.

La repo e' PUBBLICA, quindi la build fa una scansione anti-dati-personali e si
FERMA se trova qualcosa. Meglio una build fallita che un'email aziendale
pubblicata per sempre nella storia di git.
"""
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import build_anki_domande  # noqa: E402
import build_telefono  # noqa: E402

# Cose che non devono finire in una repo pubblica. Il confine e': dati personali
# o aziendali, e link privati. I nomi di servizio Microsoft (OneDrive, SharePoint)
# sono contenuto legittimo delle domande e non c'entrano nulla.
VIETATI = [
    (r"and\.cla@crssupport\.it", "email aziendale"),
    (r"liman\.mani@warptech\.it", "email aziendale"),
    (r"crssupport\.it", "dominio aziendale"),
    (r"warptech\.it", "dominio aziendale"),
    (r"Warp Tech Srl", "ragione sociale"),
    (r"\bMANILiman\b", "nome utente Windows"),
    (r"C:\\\\Users\\\\", "percorso locale"),
    (r"C:\\Users\\", "percorso locale"),
    (r"claude\.ai/code/artifact", "link artifact privato"),
    (r"\btirocin\w*", "contesto personale"),
    (r"\bWarptech\b", "azienda"),
]

BINARI = {".png", ".jpg", ".jpeg", ".gif", ".xlsx", ".pdf", ".zip"}


def scansiona(cartella):
    """Cerca dati personali in ogni file di testo. Ritorna la lista dei guai."""
    guai = []
    for f in sorted(cartella.rglob("*")):
        if not f.is_file() or ".git" in f.parts:
            continue
        if f.suffix.lower() in BINARI:
            continue
        try:
            testo = f.read_text("utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for pat, perche in VIETATI:
            for m in re.finditer(pat, testo, re.IGNORECASE):
                riga = testo.count("\n", 0, m.start()) + 1
                guai.append(f"{f.relative_to(cartella)}:{riga} — {perche}: {m.group()!r}")
    return guai


def main():
    if len(sys.argv) < 3:
        sys.exit("uso: build_sito.py <cartella AZ-104> <utente-github> [nome-repo] [cartella-out]")
    base = Path(sys.argv[1])
    utente = sys.argv[2]
    repo_nome = sys.argv[3] if len(sys.argv) > 3 else "az104"
    # Fuori da OneDrive per default: la sincronizzazione tiene lock su .git e fa
    # fallire le riscritture, e questa repo e' personale su un OneDrive aziendale.
    out = Path(sys.argv[4]) if len(sys.argv) > 4 else Path.home() / repo_nome

    # La cartella si rifa' da zero a ogni build, ma .git sopravvive: la storia
    # dei commit non va persa solo perche' si rigenerano i file.
    if out.exists():
        for f in out.iterdir():
            if f.name == ".git":
                continue
            shutil.rmtree(f) if f.is_dir() else f.unlink()
    out.mkdir(parents=True, exist_ok=True)
    (out / "flashcards").mkdir()
    (out / "banca").mkdir()
    (out / "build").mkdir()
    (out / "prompt").mkdir()

    repo_url = f"https://github.com/{utente}/{repo_nome}"
    sito_url = f"https://{utente}.github.io/{repo_nome}/"

    # ---------------------------------------------------------- pagine
    print("Pagine:")
    html = (base / "simulatore.html").read_text("utf-8")
    html = build_telefono.applica(html)
    banca = json.loads((base / "az104_question_bank_it.json").read_text("utf-8"))
    payload = json.dumps(banca, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    (out / "simulatore.html").write_text(html.replace("/*__BANCA__*/[]", payload), encoding="utf-8")
    print(f"  -> simulatore.html  ({(out / 'simulatore.html').stat().st_size / 1024:.0f} KB)")

    rip = base / "az104_ripasso.html"
    if not rip.exists():
        sys.exit("ERRORE: manca az104_ripasso.html. Lancia prima build_ripasso.py.")
    shutil.copy2(rip, out / "ripasso.html")
    print(f"  -> ripasso.html  ({(out / 'ripasso.html').stat().st_size / 1024:.0f} KB)")

    # ---------------------------------------------------------- flashcard
    print("\nFlashcard:")
    n_card = 0
    for f in sorted((base / "flashcards").glob("az104_flashcard_*.csv")):
        shutil.copy2(f, out / "flashcards" / f.name)
        n_card += sum(
            1 for r in f.read_text("utf-8").splitlines() if r.strip() and not r.startswith("#")
        )
        print(f"  -> flashcards/{f.name}")
    csv_dom, n_dom, _ = build_anki_domande.genera(base, out / "flashcards")
    print(f"  -> flashcards/{csv_dom.name}  ({n_dom} card)")

    # ---------------------------------------------------------- indice
    idx = (Path(__file__).parent / "index_sito.html").read_text("utf-8")
    idx = (
        idx.replace("__N_CARD__", str(n_card))
        .replace("__N_DOMANDE__", str(len(banca)))
        .replace("__REPO_URL__", repo_url)
    )
    for s in ("__N_CARD__", "__N_DOMANDE__", "__REPO_URL__"):
        if s in idx:
            sys.exit(f"ERRORE: segnaposto {s} non sostituito")
    (out / "index.html").write_text(idx, encoding="utf-8")
    print(f"\nIndice:\n  -> index.html  ({n_card} card, {len(banca)} domande)")

    # ---------------------------------------------------------- banca e sorgenti
    print("\nBanca e build:")
    for f in ("az104_question_bank_it.json", "az104_question_bank.json"):
        shutil.copy2(base / f, out / "banca" / f)
        print(f"  -> banca/{f}")
    shutil.copytree(base / "sorgenti", out / "banca" / "sorgenti")
    print(f"  -> banca/sorgenti/  ({sum(1 for _ in (out / 'banca' / 'sorgenti').rglob('*.json'))} file)")

    # build_sito.py resta fuori di proposito: contiene la lista dei dati da non
    # pubblicare, domini aziendali compresi. Copiarlo pubblicherebbe proprio cio'
    # che deve tenere nascosto.
    sorgenti_build = [
        f
        for f in sorted((base / "build").glob("*.py"))
        + sorted((base / "build").glob("*.js"))
        + sorted((base / "build").glob("*.html"))
        if f.name != "build_sito.py"
    ]
    for f in sorgenti_build:
        shutil.copy2(f, out / "build" / f.name)
    print(f"  -> build/  ({len(sorgenti_build)} file, build_sito.py escluso apposta)")

    shutil.copy2(
        base / "az104-prompt-banca-domande.md",
        out / "prompt" / "banca_domande_simulatore.md",
    )
    print("  -> prompt/banca_domande_simulatore.md")

    # ---------------------------------------------------------- README
    rd = (Path(__file__).parent / "readme_sito.md").read_text("utf-8")
    rd = (
        rd.replace("__N_CARD__", str(n_card))
        .replace("__N_DOMANDE__", str(len(banca)))
        .replace("__SITO_URL__", sito_url)
    )
    for s in ("__N_CARD__", "__N_DOMANDE__", "__SITO_URL__"):
        if s in rd:
            sys.exit(f"ERRORE: segnaposto {s} non sostituito nel README")
    (out / "README.md").write_text(rd, encoding="utf-8")
    print("  -> README.md")

    # ---------------------------------------------------------- Pages
    (out / ".nojekyll").write_text("", encoding="utf-8")
    (out / ".gitignore").write_text(
        "# artefatti locali\n__pycache__/\n*.pyc\n.DS_Store\nThumbs.db\n", encoding="utf-8"
    )
    print("\nGitHub Pages:\n  -> .nojekyll, .gitignore")

    # ---------------------------------------------------------- controllo privacy
    print("\nScansione dati personali:")
    guai = scansiona(out)
    if guai:
        print(f"  !! {len(guai)} TROVATI — la repo NON e' pubblicabile cosi':")
        for g in guai[:25]:
            print(f"     {g}")
        if len(guai) > 25:
            print(f"     ... e altri {len(guai) - 25}")
        sys.exit("\nBuild fermata. Togli questi riferimenti prima di pubblicare.")
    print("  ok  nessun dato personale o aziendale")

    peso = sum(f.stat().st_size for f in out.rglob("*") if f.is_file() and ".git" not in f.parts)
    print(f"\nRepo pronta: {out}")
    print(f"Peso: {peso / 1024 / 1024:.1f} MB")
    print(f"\nDiventera':\n  repo:  {repo_url}\n  sito:  {sito_url}")


if __name__ == "__main__":
    main()
