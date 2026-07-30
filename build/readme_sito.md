# AZ-104 — ripasso, banca domande e simulatore

Materiale di studio per l'esame **AZ-104 (Microsoft Azure Administrator)**, allineato alle
*skills measured* del **17 aprile 2026**. Funziona dal browser, da telefono e da PC.

### 👉 [Apri il sito](__SITO_URL__)

| | |
|---|---|
| **__N_DOMANDE__ domande** d'esame | con risposta, spiegazione e link alla pagina Microsoft Learn che la prova |
| **__N_CARD__ flashcard** | definizioni, limiti, comandi, differenze insidiose |
| **Simulatore** | 50 domande in 100 minuti, estrazione pesata per dominio, soglia 700/1000 |

Tutto in italiano, con nomi di servizi e termini tecnici in inglese come all'esame.

---

## ⚠️ Leggi prima di usarla: la verifica è incompleta

**Solo 30 domande su __N_DOMANDE__** sono state ricontrollate contro Microsoft Learn da un
verificatore indipendente. Le altre **502 sono in stato `da_rivedere`**: sono state scritte
consultando la documentazione e ognuna cita una pagina Learn specifica, ma **nessuno ha
ricontrollato la chiave di risposta in modo indipendente**.

**In pratica:** studiaci pure, ma se una risposta ti sembra sbagliata **apri il link di
riferimento prima di darla per buona**. Nel ripasso le non verificate hanno il bollino ambra; in
Anki le trovi con `tag:da-rivedere`.

La traduzione italiana **non è una verifica**: un eventuale errore presente nell'originale
inglese è stato tradotto fedelmente e si trova identico anche in italiano.

---

## Come si usa

### Dal browser

Apri il [sito](__SITO_URL__) e vai. Dal telefono, menu del browser → *Aggiungi a schermata Home*:
si apre come un'app. I progressi restano nel browser, in locale — nessun account, nessun server.

- **Ripasso** — le domande con risposta a scomparsa, filtri per dominio/tipo/difficoltà, ricerca,
  e segni "la sapevo / da rivedere". Serve a capire, non a misurare.
- **Simulatore** — l'esame vero: a tempo, pesato per dominio, con punteggio e revisione errori.

### In Anki

Scarica i CSV da [`flashcards/`](flashcards/) e importali in **AnkiDroid** (Android, gratuita) o
**AnkiMobile** (iPhone). Non toccare i menu di import: le direttive in testa ai file impostano
mazzo, separatore, HTML e tag da sole.

| File | Cosa contiene | Mazzo |
|---|---|---|
| `az104_flashcard_01_identita.csv` | __N_CARD__ flashcard atomiche | `AZ104::01 Identità e governance` |
| `az104_domande_esame.csv` | __N_DOMANDE__ domande d'esame | `AZ104::Domande::01…05` |

**Filtra con i tag** nella ricerca di Anki:

| Cerca | Ottieni |
|---|---|
| `tag:domande tag:hotspot` | solo le hotspot |
| `tag:networking tag:scenario` | scenari di rete |
| `tag:da-rivedere` | le 502 con risposta non verificata |
| `tag:verificata` | le 30 sicure |
| `deck:AZ104::Domande::03*` | tutto il Compute |

Tag disponibili: dominio (`identita` `storage` `compute` `networking` `monitoraggio`),
tipo (`scelta-singola` `scelta-multipla` `hotspot` `si-no` `ordinamento` `case-study`),
difficoltà (`base` `applicativa` `scenario`), stato (`verificata` `da-rivedere`).

---

## Copertura

| Dominio | Domande | % | Peso ufficiale |
|---|---:|---:|---|
| Manage Azure identities and governance | 125 | 23,5% | 20–25% ✓ |
| Implement and manage storage | 99 | 18,6% | 15–20% ✓ |
| Deploy and manage Azure compute resources | 133 | 25,0% | 20–25% ✓ |
| Implement and manage virtual networking | 100 | 18,8% | 15–20% ✓ |
| Monitor and maintain Azure resources | 75 | 14,1% | 10–15% ✓ |

**Tipi:** 253 scelta singola · 92 hotspot · 88 scelta multipla · 63 serie Sì/No · 21 drag-and-drop
· 15 case study
**Difficoltà:** 126 base · 274 applicativa · 132 scenario

Le flashcard sono in costruzione: per ora c'è il dominio identità e governance.

---

## Provenienza: perché niente ExamTopics

Le domande sono **originali**, scritte a partire dalla documentazione pubblica Microsoft Learn.
Ognuna cita la pagina che ne prova la risposta.

**ExamTopics e gli altri siti di dump non sono stati usati.** Contengono item riprodotti da esami
reali in violazione dell'NDA Microsoft. Parafrasarli non risolve il problema, perché ciò che è
protetto è *lo scenario d'esame*, non la sua formulazione — e chi studia su dump rischia la
decertificazione.

I campi `sintesi_commenti` e `consenso_community` sono **vuoti su tutte le domande**: Reddit è
bloccato a livello di user-agent su ogni via d'accesso tentata, e un "82% vota B" inventato
darebbe falsa fiducia proprio dove serve cautela.

### Disinformazione smentita sull'aggiornamento di aprile 2026

Diffusa sui blog, ma **falsa** (verificato diffando gli snapshot Wayback della study guide):

- ❌ «I pesi sono cambiati, identità sale e rete scende» → **i pesi sono identici** alla versione
  di aprile 2025.
- ❌ «Aggiunti Copilot, AI, Azure Arc, AKS, Private Link» → **zero occorrenze** negli obiettivi
  ufficiali.
- ✅ L'**unica** modifica sostanziale: *Configure Azure Disk Encryption* → **Configure encryption
  at host**.

---

## Com'è fatto

Pagine HTML autosufficienti: la banca domande è inclusa nel file, niente server, niente CDN,
niente richieste esterne. Aprire il sito è l'unica cosa che richiede rete — dopo funziona tutto
in locale.

```
index.html          la home
ripasso.html        le domande, con filtri e ricerca
simulatore.html     l'esame a tempo
flashcards/         i CSV per Anki
banca/              i JSON delle domande, e i lotti sorgente
build/              gli script per rigenerare tutto, e i test
prompt/             il prompt che ha generato la banca
```

### Rigenerare

```bash
cd build
python assemble.py "<out>"          # banca inglese dai lotti sorgente
python build_it.py "<out>"          # banca italiana, con validazione
python build_ripasso.py "<out>"     # la pagina di ripasso
node test_ripasso.js "<out>"        # verifica il ripasso
node test_bank.js "<out>/az104_question_bank_it.json"   # verifica la valutazione
```

`build_it.py` **si rifiuta di scrivere** se la traduzione ha toccato una chiave tecnica.
`build_anki_domande.py` importa il parsing da `build_ripasso.py`: una sola fonte di verità per i
sei formati di risposta.

### Cosa è stato verificato, e cosa no

**Verificato:** le due banche confrontate campo per campo (0 errori, chiavi identiche byte per
byte); la logica di valutazione estratta ed eseguita su entrambe (532/532 su ciascuna); il
payload delle pagine (532/532, ogni risposta risale alla banca originale). Questo test ha trovato
un bug reale: le hotspot con virgole nel valore (es. `@allowed(['dev', 'test'])`) venivano mal
valutate. Corretto e riverificato.

**Non verificato:** le pagine non sono state provate in un browser reale, né l'import in Anki.
E soprattutto: **502 risposte su 532 non hanno una verifica indipendente**.

---

## Contribuire

Se trovi una risposta sbagliata, apri una issue citando l'id della domanda (`AZ104-0042`) e la
pagina Learn che lo prova. Le correzioni vanno fatte in **entrambe** le banche, stesso id, per non
farle divergere.

**La priorità è la verifica, non il volume:** il target di 500 domande è superato, non servono
domande nuove — servono domande verificate.

---

## Licenza

Contenuto originale, scritto sulla documentazione pubblica Microsoft Learn. Microsoft, Azure e i
nomi dei servizi citati appartengono ai rispettivi proprietari. Materiale non ufficiale e non
affiliato a Microsoft.
