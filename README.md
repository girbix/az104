# AZ-104 — teoria, banca domande e simulatore

Materiale di studio per l'esame **AZ-104 (Microsoft Azure Administrator)**, allineato alle
*competenze misurate* (**skills measured**) del **17 aprile 2026**. Si apre nel browser,
senza installare niente.

### 👉 [Apri il sito](https://girbix.github.io/az104/)

| | |
|---|---|
| **82 lezioni** di teoria | il concetto, un esempio, e la trappola dell'esame — una per obiettivo ufficiale |
| **591 domande** d'esame | con risposta, spiegazione e link alla pagina Microsoft Learn che la prova |
| **Simulatore** | 50 domande in 100 minuti, estrazione pesata per dominio, soglia 700/1000 |

Tutto in italiano, con nomi di servizi e termini tecnici in inglese come all'esame.

---

## ⚠️ Leggi prima di usarla: la verifica è incompleta

**Solo 30 domande su 591** sono state ricontrollate contro Microsoft Learn da un
verificatore indipendente. Le altre **561 sono in stato `da_rivedere`**: sono state scritte
consultando la documentazione e ognuna cita una pagina Learn specifica, ma **nessuno ha
ricontrollato la chiave di risposta in modo indipendente**.

**In pratica:** studiaci pure, ma se una risposta ti sembra sbagliata **apri il link di
riferimento prima di darla per buona**. Nel ripasso le non verificate hanno il bollino ambra.

---

## Come si usa

### Dal browser

Apri il [sito](https://girbix.github.io/az104/) e vai. I progressi restano nel browser, in
locale — nessun account, nessun server.

- **Studia** — la teoria in italiano, una lezione per ognuno degli 82 obiettivi della study
  guide. Tre blocchi sempre uguali: **concetto**, **esempio**, **all'esame**. Da leggere prima
  delle domande, e dove tornare quando il simulatore ti dice cosa ripassare.
- **Ripasso** — le domande con risposta a scomparsa, filtri per dominio/tipo/difficoltà, ricerca,
  e segni "la sapevo / da rivedere". Serve a capire, non a misurare.
- **Simulatore** — l'esame vero: **50 domande in 100 minuti, soglia 700/1000**, estrazione pesata
  per dominio, nessun feedback fino alla consegna. A fine prova: punteggio, percentuale, esito per
  dominio, **le categorie da ripassare** (i sotto-argomenti in cui hai sbagliato, dal più critico)
  e la revisione guidata degli errori.

## Copertura

| Dominio | Domande | % | Peso ufficiale |
|---|---:|---:|---|
| Manage Azure identities and governance | 138 | 23,4% | 20–25% ✓ |
| Implement and manage storage | 112 | 19,0% | 15–20% ✓ |
| Deploy and manage Azure compute resources | 147 | 24,9% | 20–25% ✓ |
| Implement and manage virtual networking | 108 | 18,3% | 15–20% ✓ |
| Monitor and maintain Azure resources | 86 | 14,6% | 10–15% ✓ |

Tutti e **82 gli obiettivi** della study guide hanno almeno 4 domande: nessuno scoperto.

**Tipi:** 290 scelta singola · 99 hotspot · 94 scelta multipla · 71 serie Sì/No · 22 drag-and-drop
· 15 case study
**Difficoltà:** 126 base · 297 applicativa · 168 scenario
**Sotto-argomenti:** gli 82 obiettivi ufficiali, nomi identici alla study guide — sono la
granularità con cui il simulatore ti dice cosa ripassare.


**La teoria copre gli stessi 82 obiettivi, uno per uno.** È il legame che tiene insieme le tre
parti: sbagli una categoria nel simulatore, e quella categoria è il titolo della lezione da
riaprire. Le lezioni non hanno una verifica indipendente più di quanta ne abbiano le domande:
ognuna cita la sua pagina Learn, in italiano.

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
studia.html         la teoria, 82 lezioni
ripasso.html        le domande, con filtri e ricerca
simulatore.html     l'esame a tempo
banca/              il JSON delle domande
teoria/             i JSON delle lezioni, uno per dominio
build/              gli script per rigenerare tutto, e i test
prompt/             il prompt che ha generato la banca
```

### Rigenerare

Per aggiungere domande: scrivi un lotto in `banca/sorgenti/nuove/`, poi:

```bash
cd build
python aggiungi_domande.py --scrivi   # id in coda, mai riusati
python build_pagine.py                # reinietta la banca in simulatore.html e ripasso.html
python build_teoria.py                # ricostruisce studia.html da teoria/
```

`sotto_argomento` non è testo libero: deve essere uno degli 82 obiettivi in
[`build/tassonomia.py`](build/tassonomia.py), altrimenti `aggiungi_domande.py` rifiuta il lotto.
È la chiave con cui il simulatore dice cosa ripassare, e due nomi per lo stesso obiettivo
spezzerebbero in due la categoria. `allinea_tassonomia.py` riporta alla forma ufficiale le
etichette vecchie.

I test girano sul repo così com'è, senza argomenti:

```bash
cd build
python test_contenuti.py   # dati: chiavi, hotspot, campi, copertura per dominio
python test_teoria.py      # 82 lezioni per 82 obiettivi, link in italiano
node test_esame.js         # simulazione: durata, n. domande, soglia, pesi
node test_widget.js        # ogni domanda si disegna, valutata e non
node test_ascolto.js       # voci offerte per l'ascolto e taglio in frasi
node test_ripasso.js       # payload del ripasso vs banca
node test_bank.js          # la risposta giusta viene contata giusta
```

Escono tutti con codice diverso da zero se trovano qualcosa, così si incatenano in un hook o in
una action.

### Cosa è stato verificato, e cosa no

**Verificato:** la logica di valutazione estratta dal simulatore ed eseguita su tutte le
domande (591/591); il payload delle pagine (591/591, ogni risposta risale alla banca); i
parametri della simulazione contro l'esame reale; le 82 lezioni contro i 82 obiettivi ufficiali.
Questi test hanno trovato bug reali:

- le hotspot con virgole nel valore (es. `@allowed(['dev', 'test'])`) venivano mal valutate;
- una drag-and-drop che chiede **4 azioni su 5 opzioni** (`AZ104-0292`) era impossibile da
  azzeccare nel simulatore, che pretendeva di ordinare tutte le opzioni. Ora l'area risposta
  tiene solo le azioni richieste e i distrattori restano sotto la linea, come nella prova vera;
- un hotspot distingueva due scelte che differivano solo per maiuscole, ma la valutazione
  normalizza in minuscolo: la risposta sbagliata sarebbe stata contata giusta.

Tutti corretti e riverificati.

Un controllo incrocia anche la chiave di risposta con quello che la spiegazione stessa dichiara
("Correct: c", "Statement 2 - No", "Dropdown 1 - Premium"): non è emersa nessuna divergenza
reale. Non è una verifica contro Learn, ma esclude le chiavi copiate storte.

**Non verificato:** le pagine non sono state aperte in un browser reale. `test_widget.js` disegna
tutti e 591 i widget su un DOM finto, quindi esclude le eccezioni che lasciano la pagina bianca —
ma non dice niente su come vengono impaginati davvero. E soprattutto: **561 risposte su 591 non
hanno una verifica indipendente**.

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
