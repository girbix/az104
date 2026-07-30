# AZ-104 — Banca flashcard Anki

Flashcard per l'esame **AZ-104 (Microsoft Azure Administrator)**, versione skills measured **17 aprile 2026**.

Repo git a sé, dentro la cartella `AZ-104/` che raccoglie tutto il materiale d'esame.
Le altre due cose lì accanto servono a scopi diversi e non vanno confuse con queste card:

| Cosa | A che serve |
|---|---|
| **queste flashcard** | memorizzare: definizioni, limiti, comandi. Ripetizione spaziata in AnkiDroid, tutti i giorni |
| `../az104_ripasso.html` | ripassare le 532 domande d'esame dal telefono, senza punteggio |
| `../simulatore.html` | simulazioni complete a tempo, con punteggio ed estrazione pesata |

## Stato

| # | Dominio | Peso ufficiale | Target card | Stato |
|---|---------|----------------|-------------|-------|
| 01 | Identità e governance | 20–25% | ~73 | ✅ completo (75) |
| 02 | Compute | 20–25% | ~73 | ⬜ da fare |
| 03 | Storage | 15–20% | ~57 | ⬜ da fare |
| 04 | Networking | 15–20% | ~57 | ⬜ da fare |
| 05 | Monitoraggio e backup | 10–15% | ~40 | ⬜ da fare |

Totale previsto: ~300 card.

## Formato

CSV per Anki, separatore `;`, tre campi: `Fronte;Retro;Tag`.
L'approfondimento (2–3 righe) sta nel Retro dopo un `<br>`.

Ogni file inizia con le direttive di import:

```
#separator:Semicolon
#html:true
#tags column:3
#deck:AZ104::<numero e nome dominio>
```

Un file CSV per dominio → un sottomazzo `AZ104::…`.

## Convenzioni

- Italiano, con nomi dei servizi e termini tecnici in inglese come all'esame.
- Terminologia ufficiale corrente: **Microsoft Entra ID** (mai "Azure AD"), modulo **Az** (mai AzureRM), **managed disk**, agente **Azure Monitor Agent** (mai MMA).
- Niente contenuti deprecati (classic/ASM, unmanaged disk, moduli AzureAD/MSOnline).
- Card atomiche: una card = un concetto.
- Tag: `<dominio> <sotto-argomento>` — es. `identita rbac`, `networking nsg`.

## Riferimento

Study guide ufficiale: <https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/az-104>
