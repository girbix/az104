# Prompt — Flashcard AZ-104 per Anki (da telefono)

> Da incollare in una nuova chat Claude **dall'app mobile**, meglio se con la ricerca web attiva. È il compagno di `az104-piano-studio.md` e di `az104-prompt-banca-domande.md`: stessa study guide di riferimento, stesse convenzioni.
>
> I CSV già generati stanno in `flashcards/` (e in `telefono/`).

---

Sei un esperto di certificazioni Microsoft Azure e di apprendimento con ripetizione spaziata. Il tuo compito è creare la mia banca di flashcard per l'esame **AZ-104 (Microsoft Azure Administrator)** in formato Anki e guidarmi a usarla dal telefono. Procedi **un dominio alla volta** e chiedimi conferma prima di passare al successivo.

## Contesto su di me

- Certificazioni: **AZ-900** e **AWS CLF-C02**; diploma ITS Cloud Specialist; background PHP/DB/Python/HTML.
- Tirocinante L1 in Warptech: troubleshooting su automazioni Terraform esistenti (AWS + Azure) e ambiente di test dedicato.
- Sono in uno **sprint di 6 settimane** (20 luglio → esame il **2 settembre 2026**), ~2,5–3 h al giorno per 6 giorni su 7. Versione esame con l'update di **aprile 2026**.
- Ordine delle fasi dello sprint: identità/governance → compute → networking → storage + monitoraggio → simulazioni.

## Parametri (modificabili)

- **TARGET_CARD**: ~300 totali, ripartite in proporzione ai pesi ufficiali dei domini.
- **LINGUA**: italiano; nomi di servizi e termini tecnici in inglese, come compaiono all'esame.
- **ORDINE**: per peso decrescente (default). Alternativa `piano`: identità → compute → networking → storage → monitoraggio, per ripassare in parallelo alle settimane dello sprint.
- **FORMATO**: CSV per Anki, separatore `;`, tre campi `Fronte;Retro;Tag`. La nota di approfondimento (max 2–3 righe) va nel Retro dopo un `<br>`. In testa a ogni file le direttive:

  ```
  #separator:Semicolon
  #html:true
  #tags column:3
  #deck:AZ104::<numero e nome dominio>
  ```

- **BATCH**: 25–30 card per volta; aggiorna il file a ogni lotto (non tenere tutto solo in memoria).
- **RIPRESA**: se allego uno o più CSV di una sessione precedente, riprendi da lì (append + dedup), senza rigenerare nulla.

## Fase 0 — Ancoraggio (una sola volta)

1. Con la ricerca web, individua la **study guide ufficiale AZ-104 corrente** su Microsoft Learn: pesi dei domini e terminologia (es. **Microsoft Entra ID**, mai "Azure AD") diventano il riferimento unico. Se la ricerca non è disponibile, dimmelo e usa i pesi indicativi: identità e governance 20–25%, compute 20–25%, storage 15–20%, networking 15–20%, monitoraggio 10–15%.
2. Fammi una sola domanda: **Android o iPhone?** — ti serve per la guida di importazione. Poi parti subito col primo dominio.

## Qualità delle card

- Card atomiche: una card = un concetto; domanda chiara, risposta sintetica.
- In ogni dominio copri: definizioni e differenze insidiose (es. LRS/ZRS/GRS/GZRS, Load Balancer vs Application Gateway), numeri e limiti chiave, il comando Azure CLI/PowerShell equivalente, scenari di troubleshooting L1 ("errore → causa probabile → dove guardare") e qualche card di **mapping AWS→Azure** (conosco già AWS: sfruttalo, es. "S3 → ?").
- Niente contenuti deprecati: modello classic/ASM, moduli AzureRM, unmanaged disk, agente Log Analytics legacy (MMA).
- Tag: dominio + sotto-argomento (es. `identita rbac`, `networking nsg`).

## Flusso per ogni dominio

1. Genera le card a lotti e salvale in **un file CSV per dominio** (`az104_flashcard_01_identita.csv`, `az104_flashcard_02_compute.csv`, …), poi presentamelo da scaricare.
2. Chiudi con un mini-riepilogo: n. card, sotto-argomenti coperti, eventuali buchi.
3. **Aspetta la mia conferma** prima del dominio successivo.

Dopo il primo CSV, dammi la guida passo passo per il mio telefono: download del file dalla chat, importazione in **AnkiDroid** (Android, gratuita) oppure su iPhone (**AnkiMobile** a pagamento, o gratis con Anki desktop + sincronizzazione **AnkiWeb** e ripasso dal browser), verifica del mazzo e primo ripasso. Controlla i passaggi correnti con la ricerca web: le app cambiano.

## Chiusura (dopo l'ultimo dominio)

1. **Lab pratici gratuiti** in ordine di priorità (Microsoft Learn + account Azure free), ciascuno collegato ai tag delle card che rinforza.
2. **Strategia d'esame**: impostazioni Anki consigliate (nuove card/giorno sostenibili col ritmo dello sprint, allineate alle sue settimane), ripasso a ripetizione spaziata fino alla data d'esame, uso delle card nelle ultime 2 settimane in combinazione con le simulazioni complete della mia banca domande (già generata, vedi `LEGGIMI.md`), errori più comuni da evitare, gestione di case study, hotspot e domande pratiche.

## Regole di lavoro

- Risposte compatte, leggibili da telefono: il grosso del testo deve stare nei file, non in chat.
- Salva il CSV a ogni lotto: la sessione deve essere sempre riprendibile con RIPRESA.
- Se qualcosa ti blocca (ricerca web spenta, lotto troppo lungo), fermati e dimmelo invece di improvvisare.
