# AZ-104 sul telefono — Galaxy A55

Tutto il materiale d'esame **offline sul telefono**, senza PC e senza account.

Cartella **generata**: non modificare i file a mano, si rifanno con
`python build/build_telefono.py "<cartella AZ-104>"`. I sorgenti stanno in `../build/`.

## Prima cosa da sapere: i tuoi browser non aprono i file locali

Verificato, e vale per entrambi quelli che usi:

| Browser | Cosa fa con un file locale |
|---|---|
| **Firefox** | schermata bianca. Il supporto `file://` è stato tolto col rewrite (Fenix) e non è mai tornato |
| **DuckDuckGo** | «This kind of link cannot be opened» |
| **Samsung Internet** | dovrebbe funzionare (è Chromium, ed è già sul Galaxy) — *non provato su un A55 vero* |

Per questo **la via principale è AnkiDroid**, che è un'app nativa: niente browser, niente
`file://`, funziona sempre. Le due pagine HTML sono un extra: se il browser le apre, meglio;
se non le apre, non perdi niente perché in AnkiDroid c'è già tutto.

## Cosa c'è

| File | Cos'è | Dove si usa |
|---|---|---|
| `az104_flashcard_01_identita.csv` | 76 flashcard atomiche | **AnkiDroid** |
| `az104_domande_esame.csv` | le 532 domande d'esame come card | **AnkiDroid** |
| `index.html` | la pagina da cui parte tutto | browser |
| `ripasso.html` | le 532 domande con ricerca e filtri | browser |
| `simulatore.html` | esame da 50 domande a tempo, banca inclusa | browser |

Peso totale: **~4,6 MB**.

## 1. Copia i file sul telefono

App **OneDrive** → `Desktop/AZ-104/telefono/` → per ogni file: tieni premuto → **Salva/Scarica**.
Finiscono in `Download`.

Se vuoi solo la parte garantita, ti bastano i **due CSV**: sono 1,8 MB invece di 4,6.

## 2. AnkiDroid — la parte che funziona sempre

1. Play Store → installa **AnkiDroid** (gratuita).
2. AnkiDroid → ☰ → ⚙ → **Importa** → `az104_flashcard_01_identita.csv` → **Added 76 notes**.
3. Ripeti con `az104_domande_esame.csv` → **Added 532 notes**.

Non toccare i menu di import: le direttive in testa ai file impostano mazzo, separatore, HTML e
tag da sole.

Ti ritrovi due famiglie di mazzi, che servono a cose diverse:

```
AZ104::01 Identità e governance      76 card — definizioni, limiti, comandi
AZ104::Domande::01 Identità…        125 card — domande d'esame
AZ104::Domande::02 Storage           99
AZ104::Domande::03 Compute          133
AZ104::Domande::04 Networking       100
AZ104::Domande::05 Monitoraggio      75
```

**I tag** ti fanno filtrare senza cercare a mano. Nella schermata di ricerca di AnkiDroid:

| Cerca questo | Ottieni |
|---|---|
| `tag:domande tag:hotspot` | solo le hotspot |
| `tag:domande tag:networking tag:scenario` | scenari di rete |
| `tag:da-rivedere` | le 502 con risposta non verificata |
| `tag:verificata` | le 30 sicure |
| `deck:AZ104::Domande::03*` | tutto il Compute |

Tag disponibili: dominio (`identita` `storage` `compute` `networking` `monitoraggio`),
tipo (`scelta-singola` `scelta-multipla` `hotspot` `si-no` `ordinamento` `case-study`),
difficoltà (`base` `applicativa` `scenario`), stato (`verificata` `da-rivedere`).

## 3. Le pagine HTML — solo con Samsung Internet

Firefox e DuckDuckGo qui non servono. Usa **Samsung Internet**, già installato sul Galaxy:

1. Apri **Samsung Internet**.
2. Nella barra dell'indirizzo scrivi:
   ```
   file:///storage/emulated/0/Download/index.html
   ```
3. Tocca **★** per salvarlo nei preferiti.

Toccare il file da *My Files* di solito apre un editor di testo: passa dall'indirizzo.

Se nemmeno Samsung Internet apre il file, lascia perdere: usa AnkiDroid e tieni il simulatore
sul PC, che è dove ha più senso comunque (100 minuti seduto, non in piedi sul bus).

## Il salvataggio dei progressi

**AnkiDroid**: i progressi stanno nell'app e si perdono solo se la disinstalli. Per metterli al
sicuro collega un account **AnkiWeb** (gratuito) e sincronizza.

**Pagine HTML**: salvano su `localStorage`, cioè dentro quel browser. Niente rete, niente
account, ma se cancelli i dati di navigazione spariscono. Usa **Esporta** ogni tanto. Se compare
una barra ambra, quel browser non salva: i progressi durano solo finché la scheda resta aperta.

## Rifare la cartella

```bash
cd ../build
python build_ripasso.py "<cartella AZ-104>"     # rigenera il ripasso web
python build_telefono.py "<cartella AZ-104>"    # rigenera tutta questa cartella
node test_telefono.js "<cartella AZ-104>"       # verifica che sia autosufficiente
```

`build_telefono.py` fa tre cose: patcha il simulatore in quattro punti (storage, banca inclusa,
boot, pulsante "cambia banca"), genera il mazzo domande, copia il resto. **Si ferma** se il
simulatore è cambiato sotto i piedi, invece di sfornare in silenzio un file rotto.

Il parsing delle risposte non è duplicato: `build_anki_domande.py` importa da `build_ripasso.py`,
già verificato da `test_ripasso.js`. Una sola fonte di verità per i sei formati di domanda.

## Cosa NON è stato verificato

I test controllano l'autosufficienza — banca inclusa e integra, zero risorse esterne, zero link
assoluti, CSV con i campi e i tag giusti, 532 card nei 5 mazzi. **Non** è stato aperto un browser
reale, né un Galaxy A55, né provato un import in AnkiDroid vero. Se qualcosa si comporta male, è
lì che guarderei per primo.

E resta valido l'avviso grosso: **502 domande su 532 non hanno una verifica indipendente della
risposta**. Le trovi con `tag:da-rivedere`. Ogni card porta il link Learn: se una risposta ti
convince poco, aprilo.
