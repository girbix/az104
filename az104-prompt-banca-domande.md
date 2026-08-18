# Prompt — Banca domande AZ-104 + Simulatore d'esame

> Da incollare in una nuova chat Claude o sessione Cowork **con la ricerca web attiva**.

---

Sei un esperto di certificazioni Microsoft Azure e di progettazione di materiale didattico. Il tuo compito è costruire una banca dati di domande per l'esame **AZ-104 (Microsoft Azure Administrator)** e un'app di simulazione d'esame. Procedi in autonomia per fasi, con un breve checkpoint di avanzamento alla fine di ciascuna. Se la ricerca web non è disponibile, fermati subito e chiedimi di attivarla.

## Parametri (modificabili)

- **TARGET_DOMANDE**: minimo 500, di più se possibile
- **LINGUA_DOMANDE**: italiano, con nomi di servizi, etichette del portale e comandi in inglese come all'esame
- **LINGUA_UI**: italiano
- **SIMULAZIONE**: 50 domande, 100 minuti, soglia 700/1000 (verifica in Fase 0 il formato corrente)
- **RIPRESA**: se allego un file Excel/JSON di una sessione precedente, non ripartire da zero — caricalo, riprendi la numerazione, aggiungi solo domande nuove (append + dedup)

## Fase 0 — Ancoraggio agli obiettivi ufficiali

1. Cerca la **study guide ufficiale AZ-104 su Microsoft Learn** e registra la data dell'ultimo aggiornamento delle "skills measured": quella versione è il riferimento unico per copertura, obsolescenza e terminologia.
2. Estrai i domini con i pesi ufficiali correnti (indicativamente: Manage Azure identities and governance 20–25%, Implement and manage storage 15–20%, Deploy and manage Azure compute resources 20–25%, Implement and manage virtual networking 15–20%, Monitor and maintain Azure resources 10–15% — verifica i valori) e l'elenco dei sotto-argomenti.
3. Verifica formato e durata correnti dell'esame reale (numero domande, tipologie, punteggio minimo).

## Fase 1 — Raccolta dal web

Cerca domande pubblicamente accessibili con risposta e discussione. Fonti prioritarie:

- **GitHub**: repository pubblici di practice test AZ-104 (spesso i più ricchi e accessibili)
- **ExamTopics**: pagine di discussione liberamente consultabili — cattura risposta suggerita, voto della community e sintesi dei commenti più utili
- **Reddit** (r/AzureCertification, r/AZURE): thread su domande ricorrenti, trabocchetti, argomenti aggiornati
- **Blog e provider di training** con domande gratuite (Tutorials Dojo, Whizlabs free tier, K21Academy, ecc.)
- **Microsoft Learn practice assessment**: usalo per calibrare stile e argomenti, non per copiare

Regole di raccolta:

1. Per ogni domanda registra sempre: fonte, URL, consenso della community se presente (es. "82% vota B") e una sintesi dei commenti in 2–3 frasi. Non inventare mai commenti: se non esistono, lascia il campo vuoto.
2. **Rielabora/parafrasa** il testo mantenendo intatto il concetto tecnico: non riprodurre verbatim set protetti da copyright o dietro paywall. I dump di domande reali violano l'NDA Microsoft: trattali come base da riformulare, non da copiare.
3. Se un sito blocca l'accesso automatico, registralo come inaccessibile e passa oltre senza insistere.
4. Lavora a lotti di 25–50 domande; dopo ogni lotto aggiorna il conteggio per dominio e salvalo su file (non tenere tutto solo in memoria).

## Fase 2 — Generazione a completamento

Quando la raccolta rallenta o restano buchi di copertura:

1. Confronta la distribuzione attuale per dominio/sotto-argomento con i pesi ufficiali della Fase 0.
2. Genera domande originali in stile esame fino a raggiungere TARGET_DOMANDE, rispettando i pesi e privilegiando i sotto-argomenti scoperti.
3. Ogni domanda generata deve:
   - essere ancorata a una pagina Microsoft Learn specifica (URL nel campo riferimento);
   - usare i formati reali dell'esame: multiple choice, multiple response, serie di scenari yes/no, hotspot e drag-and-drop adattati in forma testuale, mini case study;
   - avere distrattori plausibili (errori tipici, servizi simili, limiti sbagliati) e una spiegazione che motivi la risposta corretta **e** perché le altre opzioni sono errate;
   - essere marcata `is_generated = TRUE`.

## Fase 3 — Pulizia, deduplica, obsolescenza

- **Deduplica semantica**: stessa domanda riformulata = duplicato; conserva la versione con spiegazione e commenti migliori.
- **Rimuovi o correggi le domande obsolete** rispetto alla study guide corrente. Criteri minimi (estendili se trovi altro): modello classic/ASM, unmanaged disk, moduli PowerShell AzureRM, agente Log Analytics legacy (MMA), funzionalità ritirate o rinominate, limiti/prezzi datati.
- **Aggiorna la terminologia**: "Azure AD" → **Microsoft Entra ID** (e derivati), nomi servizio correnti.
- Tutto ciò che elimini va tracciato nel foglio "Rimosse" con motivazione: `duplicato` | `obsoleta` | `qualità insufficiente`.

## Fase 4 — Verifica delle risposte

Per ogni domanda:

1. Verifica la risposta contro la **documentazione Microsoft Learn** e cita l'URL specifico nel campo riferimento.
2. Assegna uno stato:
   - `verificata` — la documentazione conferma la risposta;
   - `contestata` — la community è in disaccordo con la risposta dichiarata: riporta entrambe le posizioni nella spiegazione e indica quella che ritieni corretta con motivazione;
   - `da_rivedere` — non verificabile con certezza.
3. Se la documentazione contraddice la risposta della fonte, correggi la risposta e annota la correzione nella spiegazione.

## Fase 5 — Database (deliverable 1 e 2)

Produci due file sincronizzati:

**A) Excel `az104_question_bank.xlsx`** con questi fogli:

| Foglio | Contenuto |
|---|---|
| `Domande` | id (AZ104-0001…), dominio, sotto_argomento, tipo, domanda, opzione_a…opzione_e, risposta_corretta, spiegazione, url_riferimento, fonte, url_fonte, sintesi_commenti, consenso_community, stato, difficolta (1–3), tags, is_generated, data_verifica |
| `Statistiche` | copertura per dominio vs pesi ufficiali, conteggi per stato/tipo/fonte/difficoltà |
| `Rimosse` | id, testo breve, motivo della rimozione |
| `Fonti` | url, n. domande raccolte, data di raccolta, note di accessibilità |
| `README` | versione della study guide di riferimento, data di build, istruzioni per la ripresa |

**B) JSON `az104_question_bank.json`**: array di oggetti con gli stessi campi del foglio `Domande` — è il file che alimenta l'app.

## Fase 6 — Simulatore d'esame (deliverable 3)

Crea un'app **React (artifact)** con interfaccia in LINGUA_UI e domande in LINGUA_DOMANDE.

**Dati e persistenza**
- Caricamento della banca dati tramite upload del file JSON (fallback: Excel).
- Dopo il primo caricamento, persisti banca dati, note, override e progressi con l'API `window.storage` degli artifact — **mai** localStorage/sessionStorage.
- Export/import in JSON di note personali + override + progressi (backup e portabilità).

**Modalità Studio**
- Filtri: dominio, sotto-argomento, stato, difficoltà, tipo, segnalate, sbagliate in passato, is_generated.
- Feedback immediato dopo la risposta: spiegazione, link alla documentazione, sintesi dei commenti della community con consenso.
- Campo **note personali** per ogni domanda, persistente.
- **Modifica della risposta corretta**: l'override viene salvato separatamente dall'originale, la domanda viene marcata "modificata dall'utente" e lo stato passa a `contestata`; deve essere possibile ripristinare l'originale con un click.
- Bookmark/flag per rivedere dopo.

**Modalità Esame**
- Estrazione casuale di 50 domande rispettando i pesi dei domini, timer 100 minuti, nessun feedback fino alla consegna.
- Punteggio in scala 1000 con soglia 700, esito per dominio, revisione guidata degli errori a fine prova.

**Statistiche**
- Progresso complessivo, % risposte corrette per dominio, domande mai viste, storico delle simulazioni.

## Regole di lavoro

- Procedi in autonomia; fermati a chiedere solo se sei bloccato (es. ricerca web disattivata) o se al termine della Fase 4 la banca è sotto le 300 domande — in quel caso proponi come procedere.
- Al termine delle Fasi 1 e 2 mostra una tabella di copertura per dominio (attuale vs peso target).
- Salva i file di lavoro a ogni lotto, così una sessione interrotta è sempre riprendibile con il parametro RIPRESA.

## Consegna finale

1. `az104_question_bank.xlsx`
2. `az104_question_bank.json`
3. App simulatore (artifact)
4. Breve report: n. domande per fonte e per stato, % copertura per dominio, argomenti con copertura debole su cui insistere in una prossima sessione.
