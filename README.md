# AZ-104 — teoria, domande, simulatore

Materiale di studio per l'esame **AZ-104 (Microsoft Azure Administrator)**, allineato alle
competenze misurate (*skills measured*) del **17 aprile 2026**. Tutto in italiano, con nomi di
servizi ed etichette del portale in inglese come all'esame.

## 👉 [Apri il sito](https://girbix.github.io/az104/)

Niente da installare, niente account, niente server: i progressi restano nel tuo browser.

| | | |
| --- | --- | --- |
| **[Studia](https://girbix.github.io/az104/studia.html)** | 82 lezioni | il concetto, un esempio, la trappola d'esame — una per obiettivo ufficiale |
| **[Pratica](https://girbix.github.io/az104/pratica.html)** | 33 lab | i comandi pronti, come verificare, e come smontare tutto. Ogni lab dice quanto costa prima che tu lo lanci |
| **[Ripasso](https://girbix.github.io/az104/ripasso.html)** | 591 domande | risposta a scomparsa, spiegazione, filtri e ricerca. Serve a capire, non a misurare |
| **[Simulatore](https://girbix.github.io/az104/simulatore.html)** | 50 in 100 min | estrazione pesata per dominio, soglia 700/1000, nessun feedback fino alla consegna |

> **30 domande su 591 hanno una verifica indipendente.** Le altre sono scritte sulla
> documentazione Microsoft Learn e ognuna cita la sua pagina, ma nessuno ne ha ricontrollato la
> chiave di risposta. Se una risposta ti convince poco, apri il link prima di darla per buona.

---

## Le quattro parti si parlano

`sotto_argomento` non è testo libero: è uno degli **82 obiettivi ufficiali** della study guide, ed
è lo stesso identico in tutte e quattro le pagine. È quello che tiene insieme il giro:

**sbagli** una domanda nel simulatore → la categoria compare fra le **categorie da ripassare** a
fine prova → **ci clicchi sopra** e si apre la lezione → *Provalo con le mani* apre il suo lab →
*Allenati su questo obiettivo* rimette il simulatore su quelle domande.

Un test controlla che nessuna categoria resti senza lezione, altrimenti il link porterebbe a una
pagina che non scorre da nessuna parte e non se ne accorgerebbe nessuno.

---

## Copertura

| Dominio | Domande | % | Peso ufficiale |
| --- | ---: | ---: | :---: |
| **Identità e governance**<br><sub>Manage Azure identities and governance</sub> | 138 | 23,4% | 20–25% ✓ |
| **Storage**<br><sub>Implement and manage storage</sub> | 112 | 19,0% | 15–20% ✓ |
| **Compute**<br><sub>Deploy and manage Azure compute resources</sub> | 147 | 24,9% | 20–25% ✓ |
| **Rete virtuale**<br><sub>Implement and manage virtual networking</sub> | 108 | 18,3% | 15–20% ✓ |
| **Monitoraggio e manutenzione**<br><sub>Monitor and maintain Azure resources</sub> | 86 | 14,6% | 10–15% ✓ |

Tutti e **82 gli obiettivi** hanno almeno 4 domande: nessuno scoperto. La teoria li copre uno per
uno, e i 33 lab li coprono tutti e 82 con le mani — 17,8 ore di pratica in tutto.

**Tipi:** 290 scelta singola · 99 hotspot · 94 scelta multipla · 71 serie Sì/No · 22 drag-and-drop
· 15 case study
**Difficoltà:** 126 base · 297 applicativa · 168 scenario

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

Diffusa sui blog, ma **falsa** — verificato diffando gli snapshot Wayback della study guide:

- ❌ «I pesi sono cambiati, identità sale e rete scende» → **i pesi sono identici** alla versione
  di aprile 2025.
- ❌ «Aggiunti Copilot, AI, Azure Arc, AKS, Private Link» → **zero occorrenze** negli obiettivi
  ufficiali.
- ✅ L'**unica** modifica sostanziale: *Configure Azure Disk Encryption* → **Configure encryption
  at host**.

---

## Com'è fatto

Pagine HTML autosufficienti: la banca domande è dentro il file, niente server, niente CDN, niente
richieste esterne. Scaricare una pagina e aprirla da `file://` funziona uguale.

```text
index.html          la home
studia.html         la teoria, 82 lezioni
pratica.html        i lab guidati, 33
ripasso.html        le domande, con filtri e ricerca
simulatore.html     l'esame a tempo
banca/              il JSON delle domande
teoria/             i JSON delle lezioni, uno per dominio
pratica/            i JSON dei lab, uno per dominio
build/              gli script per rigenerare tutto, e i test
```

<details>
<summary><b>Aggiungere domande e rigenerare le pagine</b></summary>

Crea `banca/sorgenti/nuove/`, scrivici dentro un lotto in JSON, poi:

```bash
cd build
python aggiungi_domande.py --scrivi   # id in coda, mai riusati
python build_pagine.py                # reinietta la banca in simulatore.html e ripasso.html
python build_teoria.py                # ricostruisce studia.html da teoria/
python build_pratica.py               # ricostruisce pratica.html da pratica/
```

`sotto_argomento` deve essere uno degli 82 obiettivi in
[`build/tassonomia.py`](build/tassonomia.py), altrimenti `aggiungi_domande.py` rifiuta il lotto:
due nomi per lo stesso obiettivo spezzerebbero in due la categoria, e il giro descritto sopra si
romperebbe in silenzio. `allinea_tassonomia.py` riporta alla forma ufficiale le etichette vecchie.

</details>

<details>
<summary><b>I test</b></summary>

Girano sul repo così com'è, senza argomenti, ed escono con codice diverso da zero se trovano
qualcosa — così si incatenano in un hook o in una action.

```bash
cd build
python test_contenuti.py   # dati: chiavi, hotspot, campi, copertura, i numeri di questo README
python test_teoria.py      # 82 lezioni per 82 obiettivi, link in italiano
python test_pratica.py     # 82 obiettivi coperti dai lab, e la pulizia cancella davvero
node test_esame.js         # simulazione: durata, n. domande, soglia, pesi
node test_widget.js        # ogni domanda si disegna, valutata e non
node test_ascolto.js       # voci offerte per l'ascolto e taglio in frasi
node test_ripasso.js       # payload del ripasso vs banca
node test_bank.js          # la risposta giusta viene contata giusta
node test_pagine.js        # pagine integre, il giro fra le tre, i numeri della home
node test_ricomincia.js    # la barra c'è ovunque, e Ricomincia cancella solo quello che dice
```

</details>

---

## Cosa è stato verificato, e cosa no

**Verificato dai test:** la logica di valutazione estratta dal simulatore ed eseguita su tutte le
domande (591/591); il payload delle pagine (591/591, ogni risposta risale alla banca); i parametri
della simulazione contro l'esame reale; le 82 lezioni contro gli 82 obiettivi ufficiali.

Hanno trovato bug veri:

- le hotspot con virgole nel valore (es. `@allowed(['dev', 'test'])`) venivano mal valutate;
- una drag-and-drop che chiede **4 azioni su 5 opzioni** (`AZ104-0292`) era impossibile da
  azzeccare: il simulatore pretendeva di ordinare tutte le opzioni. Ora l'area risposta tiene solo
  le azioni richieste e i distrattori restano sotto la linea, come nella prova vera;
- un hotspot distingueva due scelte che differivano solo per maiuscole, ma la valutazione
  normalizza in minuscolo: la risposta sbagliata sarebbe stata contata giusta.

Tutti corretti e riverificati. Un controllo incrocia anche la chiave con quello che la spiegazione
stessa dichiara (`Correct: c`, `Statement 2 - No`, `Dropdown 1 - Premium`): nessuna divergenza
reale. Non è una verifica contro Learn, ma esclude le chiavi copiate storte.

**Non verificato:** le pagine non sono mai state aperte in un browser reale. `test_widget.js`
disegna tutti e 591 i widget su un DOM finto, quindi esclude le eccezioni che lasciano la pagina
bianca — ma non dice niente su come vengono impaginati davvero. E soprattutto: **561 risposte su
591 non hanno una verifica indipendente**, comprese le lezioni, che ne hanno quanta ne hanno le
domande.

---

## Contribuire

Se trovi una risposta sbagliata, apri una issue citando l'id della domanda (`AZ104-0042`) e la
pagina Learn che lo prova. La correzione va fatta in `banca/az104_question_bank_it.json`, poi
`python build_pagine.py` la porta dentro le pagine.

**La priorità è la verifica, non il volume:** il target di 500 domande è superato, non servono
domande nuove — servono domande verificate.

---

## Licenza

Contenuto originale, scritto sulla documentazione pubblica Microsoft Learn. Microsoft, Azure e i
nomi dei servizi citati appartengono ai rispettivi proprietari. Materiale non ufficiale e non
affiliato a Microsoft.
