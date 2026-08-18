# AZ-104 — Piano di studio

**Sprint di 6 settimane e mezza: 19 agosto → esame venerdì 2 ottobre 2026.**
Studio autonomo, nessun tutor. Terraform, Azure DevOps e capstone restano fuori: non sono in syllabus.

> Il piano precedente puntava al 2 settembre. È superato: l'esame non era stato prenotato e la
> data è passata. Le appendici in fondo — mappa AWS→Azure, richieste al tutor, note del piano
> semestrale — valgono ancora e sono rimaste.

---

## 1. Il patto: 45 giorni, a queste condizioni

**Perché è fattibile:** M0–M5 coprono già circa metà del syllabus (storage, rete base,
App Service e SQL, Key Vault, Monitor), vieni da AWS CLF-C02 e lavori sul campo. Non parti da
zero.

**Perché è stretto:** Microsoft dà per scontati ~6 mesi di amministrazione Azure quotidiana. 45
giorni si reggono solo se le ore ci sono davvero **tutte**.

**Cosa serve da te:** 2,5–3 ore al giorno, 6 giorni su 7, domenica libera. Circa **105 ore in
totale**. Se salta una settimana, l'esame slitta di una settimana: meglio slittare che bruciare il
tentativo — e la riprogrammazione è di norma gratuita fino a 24–48 ore prima.

**La rete di sicurezza:** il Practice Assessment ufficiale di **sabato 26 settembre** decide se si
va o si sposta (capitolo 6). Si prenota la fiducia sui numeri, non sulle sensazioni.

---

## 2. Le prime due cose, oggi

### Prenota l'esame per venerdì 2 ottobre

Da `learn.microsoft.com/credentials/certifications/azure-administrator/` → *Schedule exam*
(Pearson VUE, in centro o online con proctoring). Una data fissata è il miglior antidoto al
rimandare, e se scegli l'online fai subito il **test di sistema**: webcam, stanza sgombra,
documento.

Sulla stessa pagina ci sono i due riferimenti fissi di questo sprint: la **study guide ufficiale**
e il **Practice Assessment gratuito**.

### Apri l'account Azure gratuito

200 $ di credito **per 30 giorni** più i servizi sempre gratuiti. Quei 30 giorni partono
all'attivazione: aprendolo il 19 agosto coprono fino al **18 settembre**, cioè le settimane 1–5 —
dove stanno i lab più cari (VM, VMSS, Bastion, Load Balancer, App Service S1).

I lab della settimana 6 (backup e Site Recovery) cadono fuori. Due strade oneste: passare a
pay-as-you-go per quell'ultima settimana di lab — sono pochi euro se pulisci in giornata — oppure fare
**P33 (Site Recovery)** come lettura guidata nel portale, senza abilitare la replica. Vedere le
schermate e i nomi dei pulsanti copre già la maggior parte delle domande.

**Metti subito un budget con alert a 20 €** (lab P06): è la tua rete di sicurezza per sei
settimane.

---

## 3. Come funziona ogni giorno

Il repo ha quattro pagine e il giro si chiude da solo: la teoria, il lab, le domande, e il
simulatore che ti rimanda alla lezione sbagliata.

| Blocco | Durata | Dove |
| --- | --- | --- |
| Teoria | 30–40′ | **studia.html** — le lezioni degli obiettivi del giorno. Se l'argomento è nuovo del tutto, prima il modulo Microsoft Learn corrispondente |
| Lab | 60–80′ | **pratica.html** — il lab del giorno. Guarda il chip del costo *prima* di lanciarlo, e fai la sezione Pulizia **in giornata** |
| Domande | 40′ | **simulatore.html → Studio**, filtrato sul sotto-argomento di oggi. Con «Mai viste» e «Sbagliate in passato» spuntate |
| Chiusura | 10′ | Segna le lezioni studiate, segna i lab fatti, guarda la tabella «A che punto sei» |

**Ritmo settimanale fisso:**

- **Da lunedì a venerdì:** teoria + lab + domande, come sopra.
- **Sabato:** Practice Assessment ufficiale intero, poi analisi di ogni errore. Registra i
  punteggi per dominio nella tabella del capitolo 7.
- **Domenica:** riposo. Serve alla memoria più di un'ora di studio in più.

**La regola sulle domande:** sono 591 e vanno viste tutte almeno una volta. A 25–30 al giorno per
30 giorni di contenuto ci stai dentro con margine — ma solo dal **Studio**, non dalle simulazioni:
il simulatore ne estrae 50 a caso, e le due simulazioni della settimana 7 sono 100 pescate con
ripetizioni.

> **Sui 561 su 591 senza verifica indipendente:** le domande del repo sono scritte sulla
> documentazione e ognuna cita la sua pagina, ma la chiave non è stata ricontrollata. Il metro
> vero è il Practice Assessment ufficiale del sabato. Se una risposta ti convince poco, apri il
> link Learn prima di darla per buona.

---

## 4. Il calendario in una tabella

| Sett. | Periodo 2026 | Tema | Lab | Peso d'esame |
| --- | --- | --- | --- | --- |
| 1 | mer 19 – sab 22 ago | Avvio, baseline, Entra ID e RBAC | P01–P03 | Identità (20–25%) |
| 2 | lun 24 – sab 29 ago | Governance, costi, storage I | P04–P09 | Identità + Storage |
| 3 | lun 31 ago – sab 5 set | Storage II, ARM/Bicep, VM | P10–P15 | Storage (15–20%) + Compute |
| 4 | lun 7 – sab 12 set | Compute II: disponibilità, container, App Service | P16–P20 | Compute (20–25%) |
| 5 | lun 14 – sab 19 set | Rete, dalla VNet al load balancer | P21–P27 | Rete (15–20%) |
| 6 | lun 21 – sab 26 set | Monitoraggio, backup, ASR + **go/no-go** | P28–P33 | Monitor (10–15%) |
| 7 | lun 28 set – ven 2 ott | Solo simulazioni e ripasso mirato | — | Tutti |
| — | **ven 2 ottobre** | **ESAME AZ-104** | — | — |

---

## 5. Settimana per settimana

### Settimana 1 — Avvio, Entra ID e RBAC (19 – 22 ago)

Quattro giorni. Il primo serve a mettere in piedi le cose, non a studiare.

| Giorno | Cosa fai |
| --- | --- |
| **Mer 19** | Prenota l'esame. Apri l'account Azure e metti il budget. Poi la **baseline**: premi *Ricomincia le domande* nella barra (le statistiche attuali sono sporche dai click di prova), fai una simulazione intera da 50 domande cronometrata, e subito dopo il **Practice Assessment n.1** ufficiale. Registra tutti e due i punteggi: sono il tuo punto di partenza, e servono solo a quello. |
| **Gio 20** | Utenti, gruppi, proprietà, licenze, utenti esterni, SSPR — 5 obiettivi. **Lab P01 e P02** (gratis). |
| **Ven 21** | RBAC: ruoli integrati, assegnazione a scope diversi, interpretare chi può cosa — 3 obiettivi. **Lab P03** (gratis). |
| **Sab 22** | **Practice n.2** + analisi di ogni errore. Le categorie sbagliate portano alla lezione: seguile. |

### Settimana 2 — Governance, costi, storage I (24 – 29 ago)

| Giorno | Cosa fai |
| --- | --- |
| **Lun 24** | Azure Policy, blocchi, tag — 3 obiettivi. **Lab P04 e P05.** P05 è la catena `Modify` → managed identity → remediation task: è letteralmente una domanda della banca. |
| **Mar 25** | Gruppi di risorse, sottoscrizioni, costi, management group — 4 obiettivi. **Lab P06** (gratis). |
| **Mer 26** | Nessun argomento nuovo: 60–70 domande del **dominio 1** nel Studio. È il dominio più pesante, e adesso l'hai finito. |
| **Gio 27** | Account di archiviazione, ridondanza, cifratura — 3 obiettivi. **Lab P07.** |
| **Ven 28** | Blob: container, tier, versioning, soft delete, lifecycle — 5 obiettivi. **Lab P08 e P09.** |
| **Sab 29** | **Practice n.3** + analisi. |

### Settimana 3 — Storage II, ARM/Bicep, VM (31 ago – 5 set)

| Giorno | Cosa fai |
| --- | --- |
| **Lun 31** | SAS, criteri di accesso archiviati, chiavi, firewall — 4 obiettivi. **Lab P10 e P11.** P10 è la domanda più prevedibile del dominio: come si revoca un SAS già distribuito. |
| **Mar 1 set** | Azure Files, accesso basato su identità, AzCopy, replica degli oggetti — 5 obiettivi. **Lab P12 e P13.** A fine giornata **butta `rg-lab-st`**. |
| **Mer 2** | 60–70 domande del **dominio 2**. |
| **Gio 3** | ARM e Bicep: leggere, modificare, distribuire, esportare, convertire — 5 obiettivi. **Lab P14.** Occhio alla modalità Complete: leggila, non lanciarla. |
| **Ven 4** | VM: creazione, taglie, dischi — 3 obiettivi. **Lab P15** — *si paga a ore*, dealloca a fine sessione. |
| **Sab 5** | **Practice n.4** + analisi. |

### Settimana 4 — Compute II (7 – 12 set)

Il dominio più grande, 24 obiettivi. È la settimana più cara: pulisci ogni sera.

| Giorno | Cosa fai |
| --- | --- |
| **Lun 7** | **Encryption at host** e spostamento di una VM — 2 obiettivi. **Lab P16.** Encryption at host è l'unica novità vera della versione d'esame del 17 aprile 2026: falla, non leggerla. |
| **Mar 8** | Zone, set di disponibilità, VMSS — 2 obiettivi. **Lab P17** — cinque macchine accese, cancella tutto a fine giornata. |
| **Mer 9** | ACR, ACI, Container Apps, dimensionamento — 4 obiettivi. **Lab P18.** |
| **Gio 10** | App Service: piano, app, scalabilità, slot — 4 obiettivi. **Lab P19.** Il piano B1 non ha né slot né autoscale: quel vincolo è una domanda. |
| **Ven 11** | App Service: TLS, dominio personalizzato, backup, rete — 4 obiettivi. **Lab P20.** Poi **butta `rg-lab-app`**. |
| **Sab 12** | 60–70 domande del **dominio 3** + **Practice n.5**. |

### Settimana 5 — Rete (14 – 19 set)

| Giorno | Cosa fai |
| --- | --- |
| **Lun 14** | VNet, subnet, peering, IP pubblici — 3 obiettivi. **Lab P21** (gratis). Il peering non è transitivo, e Azure si tiene 5 indirizzi per subnet. |
| **Mar 15** | NSG, gruppi di sicurezza applicativi, regole effettive — 2 obiettivi. **Lab P22.** |
| **Mer 16** | Route definite da te e diagnosi — 2 obiettivi. **Lab P23.** Poi **Bastion**, 1 obiettivo, **lab P24**: fallo e cancellalo **nella stessa sessione**, è fra le voci più care di tutte. |
| **Gio 17** | Endpoint di servizio contro endpoint privati — 2 obiettivi. **Lab P25.** È la coppia che l'esame confonde di proposito. |
| **Ven 18** | Azure DNS e load balancer — 3 obiettivi. **Lab P26 e P27.** In P27 rompi apposta la health probe: è la risposta a quasi tutte le domande «non bilancia». Poi **butta `rg-lab-net`**. |
| **Sab 19** | 60–70 domande del **dominio 4** + **Practice n.6**. |

### Settimana 6 — Monitoraggio, backup, e il go/no-go (21 – 26 set)

| Giorno | Cosa fai |
| --- | --- |
| **Lun 21** | Log Analytics, impostazioni di diagnostica, KQL — 2 obiettivi. **Lab P28.** I log non arrivano da soli: è la regola che l'esame chiede in mille modi. |
| **Mar 22** | Metriche, avvisi, gruppi di azione, regole di elaborazione — 2 obiettivi. **Lab P29.** Poi Insights, 1 obiettivo, **lab P30**. |
| **Mer 23** | Network Watcher e Connection monitor — 1 obiettivo. **Lab P31.** Giornata corta: usa il tempo che avanza per le domande del dominio 5. |
| **Gio 24** | Backup: vault, criteri, ripristino, report — 5 obiettivi. **Lab P32.** Il vault non si cancella se contiene ancora elementi protetti: segui l'ordine della pulizia. |
| **Ven 25** | Site Recovery e failover — 2 obiettivi. **Lab P33** (o lettura guidata, se il credito è finito). Poi **pulizia totale**: controlla che non sia rimasto niente acceso in nessuna region. |
| **Sab 26** | **PRACTICE ASSESSMENT n.7 — QUESTO DECIDE IL GO/NO-GO.** Capitolo 6. |

### Settimana 7 — Solo consolidamento (28 set – 2 ott)

Niente argomenti nuovi. Ogni simulazione in condizioni reali: timer, niente pause, niente appunti.

| Giorno | Cosa fai |
| --- | --- |
| **Lun 28** | **SIMULAZIONE COMPLETA n.1** (50 domande, 100 minuti, cronometrata). Pomeriggio: analisi di ogni errore, e dalle categorie da ripassare torna alle lezioni. |
| **Mar 29** | Ripasso mirato dei domini sotto l'80%: rileggi le lezioni deboli, rifai i lab-lampo dei punti dove hai sbagliato (20′ l'uno). |
| **Mer 30** | **SIMULAZIONE COMPLETA n.2.** Confronta con lunedì. Se il punteggio non sale, il problema non è la quantità: è che stai sbagliando *le stesse* cose. |
| **Gio 1 ott** | Solo domande già viste e le tabelle chiave (ridondanza, SLA, endpoint, modalità di distribuzione, SKU). Logistica: documento, tragitto o test di sistema. Poi basta: da qui il cervello consolida da solo. |
| **Ven 2 ott** | **ESAME.** Arriva o collegati 30 minuti prima. In sala: prima passata rispondendo a tutto, segna i dubbi e rivedili alla fine. Nei case study **leggi prima le domande, poi lo scenario**. |

---

## 6. Il go/no-go: la regola che ti protegge

Il **Practice n.7 di sabato 26 settembre** decide, senza sentimenti:

| Risultato | Decisione |
| --- | --- |
| ≥ 75% con tutti i domini ≥ 70% | **GO:** esame confermato per venerdì 2 ottobre. |
| 70–75% | **GO con riserva:** sposta l'esame a metà della settimana dopo e dedica i giorni extra ai domini deboli. |
| < 70% | **NO-GO:** riprogramma a metà ottobre. Due settimane in più valgono più di un tentativo bruciato. |

Vale lo stesso per le simulazioni della settimana 7. E vale la pena ricordarlo: la soglia è
**700/1000**, non 900. Non serve sentirsi pronti al 100%.

---

## 7. Tabella punteggi (compilala ogni sabato)

| Data | Prova | Identità | Storage | Compute | Rete | Monitor | Totale |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 19 ago | Simulatore (baseline) | | | | | | |
| 19 ago | Practice n.1 (baseline) | | | | | | |
| 22 ago | Practice n.2 | | | | | | |
| 29 ago | Practice n.3 | | | | | | |
| 5 set | Practice n.4 | | | | | | |
| 12 set | Practice n.5 | | | | | | |
| 19 set | Practice n.6 | | | | | | |
| 26 set | **Practice n.7 — go/no-go** | | | | | | |
| 28 set | Simulazione 1 | | | | | | |
| 30 set | Simulazione 2 | | | | | | |

---

## 8. Regole d'oro dello sprint

- **Il costo prima, non dopo.** Ogni lab ha il chip: gratis, pochi centesimi, si paga a ore. I 13
  in rosso accendono macchine, Bastion o piani App Service. La sezione Pulizia non è un consiglio.
- **Pulisci in giornata, non a fine settimana.** Una VM dimenticata un weekend si mangia una fetta
  del credito; Bastion e Site Recovery la mangiano tutta.
- **Vault e ASR:** un Recovery Services vault non si elimina finché contiene backup o repliche.
  Svuotalo e disattiva il soft delete prima di chiudere la settimana 6.
- **Segna mentre studi, non dopo.** Le lezioni segnate e i lab segnati alimentano la tabella «A che
  punto sei»: se non li segni, quella tabella ti mente proprio quando ti serve.
- **Gli errori tornano dal simulatore, non da un quaderno.** Spunta «Sbagliate in passato» nel
  Studio: è l'elenco degli errori tuoi, sempre aggiornato, e ogni categoria porta alla lezione.
- **Ricontrolla la study guide a metà sprint.** Se Microsoft ha aggiunto una voce che qui manca,
  infilala nella settimana giusta.

---

## 9. Cosa resta fuori (di proposito)

Terraform, Azure DevOps, il modulo AI e il capstone **non sono argomenti d'esame**: rientrano nel
percorso di lavoro, dopo il 2 ottobre. Questo piano ha un solo obiettivo e lo insegue senza
distrazioni.

---
---

## Appendice A — Mappa mentale AWS → Azure

Conoscendo già AWS (CLF-C02), gran parte del lavoro è **tradurre** concetti, non impararli da zero.

| Concetto | AWS (lo sai già) | Azure (da imparare) |
| --- | --- | --- |
| Identità / permessi | IAM users, roles, policies | **Microsoft Entra ID** + **RBAC** (ruoli su scope) |
| Account / organizzazione | Account, Organizations, OU | **Subscription**, **Management Group**, **Resource Group** |
| Governance | SCP, Tag policies | **Azure Policy**, **Tag**, **Resource Lock** |
| Object storage | S3 | **Blob Storage** (storage account) |
| File condivisi | EFS / FSx | **Azure Files** |
| Compute VM | EC2 | **Azure Virtual Machine** |
| Auto scaling | Auto Scaling Group | **VM Scale Set (VMSS)** |
| Rete | VPC, subnet | **VNet**, subnet |
| Firewall di rete | Security Group / NACL | **NSG** (Network Security Group) |
| Peering / VPN | VPC Peering, VPN GW | **VNet Peering**, **VPN Gateway**, ExpressRoute |
| Load balancer | ELB/ALB | **Azure Load Balancer**, **Application Gateway** |
| DNS | Route 53 | **Azure DNS**, Private DNS Zones |
| Monitoring/log | CloudWatch | **Azure Monitor** + **Log Analytics** |
| IaC nativo | CloudFormation | **ARM / Bicep** |

---

## Appendice B — Da chiedere al tutor in Warptech

- Un'ora "protetta" a settimana per studio/lab, oppure accesso esteso all'ambiente di test (è
  interesse dell'azienda: i partner Microsoft valorizzano il personale certificato).
- Copertura del **voucher d'esame** (~165 USD/equivalente) — spesso le aziende lo coprono per i
  tirocinanti.
- Affiancamento sui ticket L1 più "didattici", così l'esperienza pratica si mappa sui domini
  d'esame.

> **Diario degli errori L1:** tieni traccia degli incident che risolvi al lavoro, taggandoli per
> dominio (identità / storage / compute / networking / monitoring). A fine percorso hai una mappa
> reale delle tue competenze pratiche — utile sia per l'esame sia per il colloquio di fine
> tirocinio.

---

## Appendice C — Note che valgono ancora

1. **L'esame NON testa Terraform.** Al lavoro usi Terraform, ma l'AZ-104 verifica che tu sappia
   fare le stesse cose con **portale Azure, Azure CLI, PowerShell e Bicep/ARM**. Per ogni risorsa
   che vedi creata via Terraform al lavoro, esercitati a ricrearla *a mano* da portale o CLI.
2. **Sottoscrizione per i lab:** account Azure gratuito (credito iniziale + servizi sempre
   gratuiti) e, dove serve, pay-as-you-go con budget e alert. Spegni ed elimina sempre a fine lab.
3. **L'AZ-104 passa a 700/1000** e le certificazioni role-based si rinnovano **gratis** ogni anno
   con un assessment online: il rischio di prenotare "prima di sentirsi pronti al 100%" è basso.
4. **Collegamento col lavoro, dominio per dominio:** gli errori L1 sulle automazioni sono spesso
   **permessi** (identità o service principal senza il ruolo giusto → dominio 1); "due risorse non
   si parlano" è NSG, peering, route o DNS → dominio 4; leggere Log Analytics e KQL copre il
   dominio 5.
