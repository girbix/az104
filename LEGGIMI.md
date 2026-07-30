# AZ-104 — Banca domande e simulatore d'esame

Tutto il materiale per la preparazione all'esame **AZ-104 (Microsoft Azure Administrator)**.

**Riferimento ufficiale:** [study guide Microsoft Learn](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/az-104) — *skills measured al 17 aprile 2026*.
**Data di build:** 16 luglio 2026 · **532 domande**

---

## ⚠️ Leggi prima di usarla: la verifica è incompleta

**Solo 30 domande su 532** sono state ricontrollate contro Microsoft Learn da un verificatore indipendente. Le altre **502 sono in stato `da_rivedere`**: sono state scritte consultando la documentazione e ognuna cita una pagina Learn specifica, ma **nessuno ha ricontrollato la chiave di risposta in modo indipendente**.

Il motivo è banale: la sessione di generazione ha esaurito il limite di utilizzo e i 35 agenti verificatori sono stati interrotti. Non è un giudizio sulla qualità delle domande.

**In pratica:** studiaci pure, ma se una risposta ti sembra sbagliata **apri il link in `url_riferimento` prima di darla per buona**. Il simulatore ti lascia correggere la risposta e salvare la correzione.

La traduzione italiana **non è una verifica**: un eventuale errore presente nell'originale inglese è stato tradotto fedelmente e si trova identico anche in italiano.

---

## Da dove si comincia

1. Apri il **simulatore**: <https://claude.ai/code/artifact/73618470-8c5f-4cf2-84f6-3ced9c763e47>
2. Trascinaci dentro `az104_question_bank_it.json` (italiano) oppure `az104_question_bank.json` (inglese).
3. La banca resta salvata: alla riapertura riparti da dove eri.

`simulatore.html` in questa cartella è la stessa app, se preferisci tenerne una copia locale.

> **Quale lingua?** Se pensi di sostenere l'esame **in inglese, allenati sulla versione inglese**: il lessico dei distrattori fa parte della difficoltà reale della prova. L'italiano ti fa capire i concetti più in fretta, ma non ti prepara a quello. Le due banche sono **allineate id per id** (AZ104-0001 è la stessa domanda in entrambe), quindi note e progressi restano validi anche se cambi lingua a metà strada.

---

## Cosa c'è in questa cartella

| File | Cos'è |
|---|---|
| `az104_ripasso.html` | **le 532 domande da telefono** — pagina sola, risposta a scomparsa, filtri, segni salvati in locale. Non è il simulatore: qui non c'è punteggio né estrazione pesata, si ripassa e basta |
| `az104_question_bank_it.json` | **532 domande in italiano** — questo carichi nel simulatore |
| `az104_question_bank_it.xlsx` | stesse domande in Excel (Domande, Statistiche, README) |
| `az104_question_bank.json` | le stesse 532 in **inglese**, allineate id per id |
| `az104_question_bank.xlsx` | versione inglese completa (anche i fogli Rimosse e Fonti) |
| `simulatore.html` | l'app, in copia locale |
| `az104-piano-studio.md` | **il piano di studio attivo** — sprint di 6 settimane, esame il 2 settembre 2026, con calendario giorno per giorno, prompt pronti e regola go/no-go |
| `az104-prompt-banca-domande.md` | il prompt che ha generato questo lavoro |
| `az104-prompt-flashcard-anki.md` | il prompt per generare le flashcard Anki dal telefono |
| `telefono/` | **tutto il materiale offline sul telefono** — repo git a sé, generata. Copi i 4 file nei Download del Galaxy e funziona senza rete e senza PC. Vedi il suo README |
| `flashcards/` | **le flashcard per Anki** — repo git a sé, con i CSV da importare in AnkiDroid. Vedi il suo README |
| `build/` | script per ricostruire tutto da zero, e i test |
| `sorgenti/domande-en/` | i 37 lotti grezzi come li hanno scritti gli agenti |
| `sorgenti/traduzioni-it/` | i 14 lotti di traduzione |

---

## Copertura per dominio

| Dominio | Domande | % | Peso ufficiale |
|---|---:|---:|---|
| Manage Azure identities and governance | 125 | 23,5% | 20–25% ✓ |
| Implement and manage storage | 99 | 18,6% | 15–20% ✓ |
| Deploy and manage Azure compute resources | 133 | 25,0% | 20–25% ✓ |
| Implement and manage virtual networking | 100 | 18,8% | 15–20% ✓ |
| Monitor and maintain Azure resources | 75 | 14,1% | 10–15% ✓ |

**Tipi:** 253 scelta singola · 92 hotspot · 88 scelta multipla · 63 serie Sì/No · 21 drag-and-drop · 15 case study
**Difficoltà:** 126 base · 274 applicativa · 132 scenario

---

## Provenienza: perché niente ExamTopics

Le 532 domande sono **originali**, scritte a partire dalla documentazione pubblica Microsoft Learn. Ognuna cita la pagina che ne prova la risposta.

**ExamTopics e gli altri siti di dump non sono stati usati.** Contengono item riprodotti da esami reali in violazione dell'NDA Microsoft. Parafrasarli non risolve il problema, perché ciò che è protetto è *lo scenario d'esame*, non la sua formulazione — e chi studia su dump rischia la decertificazione. Il foglio `Fonti` della versione inglese traccia l'esclusione.

**I campi `sintesi_commenti` e `consenso_community` sono vuoti su tutte le domande.** Reddit (r/AzureCertification, r/AZURE) è bloccato a livello di user-agent su ogni via d'accesso tentata. Senza un consenso reale i campi restano vuoti: un "82% vota B" inventato darebbe falsa fiducia proprio dove serve cautela. È un requisito del prompt originale **non soddisfatto**, non un dettaglio risolto.

### Disinformazione smentita sull'aggiornamento di aprile 2026

Diffondendosi sui blog, ma **falso** (verificato diffando gli snapshot Wayback della study guide):

- ❌ «I pesi sono cambiati, identità sale e rete scende» → **i pesi sono identici** alla versione di aprile 2025.
- ❌ «Aggiunti Copilot, AI, Azure Arc, AKS, Private Link» → **zero occorrenze** negli obiettivi ufficiali.
- ✅ L'**unica** modifica sostanziale: *Configure Azure Disk Encryption* → **Configure encryption at host**.

---

## Il campo `stato`

| Valore | Significato |
|---|---|
| `verificata` | la documentazione Learn conferma la risposta (30 domande) |
| `contestata` | due letture difendibili; la spiegazione riporta entrambe |
| `da_rivedere` | non ancora ricontrollata in modo indipendente (502 domande) |

---

## Cosa è tradotto e cosa no

**Tradotti:** `domanda`, `opzione_a`…`opzione_e`, `spiegazione`.

**NON tradotti** — e non è una svista:

- **Le chiavi tecniche** (`id`, `dominio`, `sotto_argomento`, `tipo`, `risposta_corretta`, `stato`, `tags`…). Il simulatore confronta `dominio` con le stringhe inglesi esatte per estrarre le 50 domande pesate per dominio: tradurlo romperebbe estrazione e statistiche. L'interfaccia le mostra comunque in italiano.
- **I valori dentro le parentesi quadre delle hotspot.** `risposta_corretta` contiene quei valori letterali: tradurli renderebbe quelle 92 domande impossibili da valutare. Il risultato è un'etichetta italiana con scelte inglesi — ibrido, ma è l'unico modo per non rompere il punteggio.
- **Nomi di servizio, ruoli, SKU, cmdlet e codice** (Microsoft Entra ID, Contributor, Standard_LRS, `New-AzVM`…): sono gli stessi termini che trovi nel portale e nell'esame.
- **Le serie Sì/No** hanno `risposta_corretta` in inglese (`Yes,No,No`) ma l'interfaccia mostra i pulsanti Sì/No.

---

## Come è stato verificato

La validazione ha confrontato le 532 italiane contro le inglesi campo per campo: **0 errori, 0 avvisi** — chiavi identiche byte per byte, parentesi hotspot intatte, nessuna opzione comparsa o sparita.

Poi la logica di valutazione è stata estratta dal simulatore ed eseguita su entrambe le banche: **532/532 su ciascuna**. Per ogni domanda si verifica che la risposta documentata come corretta venga valutata corretta, che ogni valore hotspot sia davvero selezionabile nel menu, e che una risposta errata venga respinta.

Questo test ha trovato un bug reale nell'app: le hotspot con virgole nel valore (es. `@allowed(['dev', 'test'])`) venivano mal valutate. Corretto e riverificato.

**Non verificato:** l'app non è stata provata in un browser reale. La persistenza usa `window.storage`, che esiste solo nel contesto artifact. Se al caricamento compare una barra ambra in alto, la persistenza non è attiva: usa **Esporta** per non perdere note e progressi.

---

## Ricostruire tutto da zero

```bash
cd build
python assemble.py "<cartella di output>"    # banca inglese da sorgenti/domande-en/
python build_it.py "<cartella di output>"    # banca italiana, con validazione
node test_bank.js "<...>/az104_question_bank_it.json"   # test di valutazione
```

`assemble.py` si aspetta i lotti in `batches/` e `build_it.py` le traduzioni in `tx/`: se li sposti, aggiorna i percorsi in cima agli script. `build_it.py` **si rifiuta di scrivere** se la traduzione ha toccato una chiave tecnica.

---

## Prossimi passi

**Priorità assoluta: completare la verifica (Fase 4) sulle 502 domande `da_rivedere`.** Il target di 500 è già superato: **non servono nuove domande, servono domande verificate.**

1. Allega `az104_question_bank.json` a una nuova sessione con la ricerca web attiva.
2. Gli id sono progressivi: riprendi dall'ultimo, non rinumerare.
3. Se correggi una risposta, correggila in **entrambe** le banche (stesso id) per non farle divergere.
4. Ricontrolla l'ancoraggio: se la study guide è stata aggiornata dopo il 17 aprile 2026, rivedi pesi e obsolescenza prima di aggiungere altro.
