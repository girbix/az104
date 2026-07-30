# AZ-104 — Piano di studio

**Piano attivo: sprint di 6 settimane.** 20 luglio → esame tra il 31 agosto e il 4 settembre 2026 (consigliato: mercoledì 2 settembre).
Studio autonomo, io + Claude, nessun tutor. Terraform, Azure DevOps e capstone restano fuori: non sono in syllabus.

> Il precedente piano semestrale (~3 h/settimana, esame a fine tirocinio) è **superato** da questo sprint. Quello che vale ancora — la mappa mentale AWS→Azure e le richieste da fare al tutor — è conservato nelle appendici in fondo.

---

## 1. Il patto: fattibile, a queste condizioni

**Perché è fattibile:** hai già chiuso M0–M5 a velocità tripla (storage, rete base, App Service + SQL, Key Vault, Monitor) e questi coprono circa metà del syllabus. Nelle 6 settimane copriamo l'altra metà, pesata sui domini d'esame.

**Cosa serve da te:** 2,5–3 ore al giorno, 6 giorni su 7 (domenica libera), per un totale di ~16–19 ore a settimana. Se una settimana salta, l'esame slitta di una settimana: meglio slittare che bruciare il tentativo.

**Cosa fa Claude:** il lavoro del tutor — quiz giornalieri, correzione con spiegazione, interrogazioni, spiegazione degli errori dei lab, flashcard, simulazioni di scenario. I prompt pronti sono al capitolo 4: copiali e usali ogni giorno.

### Da dove partiamo (mappa onesta)

| Dominio d'esame (peso) | Già coperto (M0–M5) | Da coprire nello sprint |
| --- | --- | --- |
| Identità e governance (20–25%) | RBAC base, tag, budget, Key Vault, MI | Entra ID (utenti/gruppi/guest/SSPR), ruoli custom, lock, move, Azure Policy |
| Storage (15–20%) | Account, redundancy, tier, SAS, lifecycle, RBAC dati | AzCopy, versioning/soft delete, object replication, Azure Files avanzato, File Sync |
| Compute (20–25%) | App Service base, Azure SQL | VM in profondità, dischi, disponibilità, VMSS, ARM/Bicep, slot/autoscale, ACR/ACI/Container Apps |
| Networking (15–20%) | VNet, subnet, NSG, peering, Bastion | DNS, Load Balancer, route/UDR, service vs private endpoint, ASG, Network Watcher |
| Monitoraggio e manutenzione (10–15%) | Monitor, Log Analytics, KQL, alert, Defender | Backup VM/Files + restore, Recovery Services vault, ASR, action group, VM insights |

---

## 2. Prima cosa da fare: prenota l'esame

Prenota per **mercoledì 2 settembre** (o giovedì 3): una data fissata è il miglior antidoto al rimandare. Si prenota da `learn.microsoft.com/credentials/certifications/azure-administrator/` → "Schedule exam" (Pearson VUE, in centro d'esame o online con proctoring).

- Se scegli l'esame online: fai subito il **test di sistema di Pearson VUE** (webcam, stanza sgombra, documento pronto).
- Di norma la riprogrammazione è gratuita fino a 24–48 ore prima: verifica le condizioni al momento della prenotazione, così il go/no-go del capitolo 7 non ti costa nulla.
- Sulla stessa pagina trovi la **study guide ufficiale** e il **Practice Assessment gratuito**: sono i due riferimenti fissi di questo piano. Il syllabus viene aggiornato periodicamente: controlla la study guide e segnala eventuali voci che non trovi in questo piano.
- **Formato d'esame** (verifica i dettagli correnti sulla pagina): circa 40–60 quesiti in ~100–120 minuti, punteggio minimo 700/1000, con scenari/case study e possibili item interattivi.

---

## 3. Come funziona ogni giorno (il metodo)

| Blocco | Durata | Cosa fai |
| --- | --- | --- |
| Teoria | 45–60′ | Il modulo Microsoft Learn del giorno (percorsi ufficiali AZ-104, gratuiti). Appunti essenziali nel diario. |
| Lab | 60–90′ | Il lab del giorno su Portale + CLI. Dove il modulo MS Learn offre la sandbox gratuita, usala: zero costi. |
| Quiz con Claude | 30′ | 10 domande stile esame sull'argomento del giorno (prompt n.1). Ogni errore diventa una flashcard. |
| Chiusura | 10′ | Diario: cosa ho imparato, cosa non mi torna, risorse da eliminare (fatto?). |

**Ritmo settimanale fisso:**

- **Venerdì:** Practice Assessment ufficiale su Microsoft Learn (intero). Registra il punteggio per dominio nella tabella del capitolo 8.
- **Sabato:** quiz lungo (30 domande miste sulla settimana) + ripasso di tutte le flashcard degli errori.
- **Domenica:** riposo. Serve alla memoria più di un'ora di studio in più.

---

## 4. Claude al posto del tutor: prompt pronti da copiare

Usali così come sono, cambiando solo l'argomento tra parentesi quadre.

1. **Quiz del giorno** — "Fammi 10 domande a scelta multipla in stile esame AZ-104 su [argomento di oggi], una alla volta. Aspetta la mia risposta, poi dimmi se è giusta e spiega perché le altre opzioni sono sbagliate."
2. **Spiegazione errore** — "Ho sbagliato questa domanda del practice: [incolla domanda e opzioni]. Spiegami il concetto da zero e dammi una regola pratica per ricordarlo."
3. **Flashcard** — "Genera 15 flashcard (domanda → risposta breve) su [argomento], in tabella."
4. **Interrogazione** — "Fingiti l'esaminatore: 5 domande aperte su [dominio]. Valuta ogni mia risposta da 1 a 5 e dimmi cosa mancava."
5. **Scenario/case study** — "Creami uno scenario pratico stile AZ-104 che combini [es. VM + Load Balancer + backup], con 4 domande collegate."
6. **Debug lab** — "Questo comando/deploy fallisce, ecco l'errore: [incolla]. Cosa è andato storto e come lo sistemo?"
7. **Ripasso serale** — "Riassumi in 10 punti chiave [argomento di oggi], poi fammi 3 domande a sorpresa."

> **Unica regola:** mai incollare segreti, chiavi, connection string o dati reali del cliente nei prompt.

---

## 5. Il calendario dello sprint in una tabella

| Sett. | Periodo 2026 | Tema | Dominio d'esame (peso) |
| --- | --- | --- | --- |
| 1 | 20 – 25 lug | Entra ID e governance | Identità e governance (20–25%) |
| 2 | 27 lug – 1 ago | Compute I: VM, dischi, disponibilità, VMSS | Compute (20–25%) |
| 3 | 3 – 8 ago | Compute II: ARM/Bicep, App Service avanzato, container | Compute (20–25%) |
| 4 | 10 – 14 ago | Networking avanzato (Ferragosto: weekend libero) | Networking (15–20%) |
| 5 | 17 – 22 ago | Storage avanzato + Backup e monitoraggio | Storage (15–20%) + Monitor (10–15%) |
| 6 | 24 – 29 ago | Simulazioni complete e ripasso mirato | Tutti |
| — | 31 ago – 4 set | **ESAME AZ-104** (consigliato: mer 2 set) | — |

---

## 6. Settimana per settimana, giorno per giorno

### Settimana 1 — Entra ID e governance (20–25 lug)

Percorso MS Learn: *"AZ-104: Manage identities and governance in Azure"*. È il dominio più pesante e il gap più grande: si parte da qui.

| Giorno | Studio e lab (2,5–3 h) | Con Claude, la sera (30′) |
| --- | --- | --- |
| Lun 20 | Utenti e gruppi Entra ID: membri vs guest, gruppi assegnati vs dinamici, licenze ai gruppi. **Lab:** 3 utenti test, 1 gruppo assegnato + 1 dinamico (department=IT), invita un guest con una mail esterna. | Quiz 10 domande: utenti e gruppi |
| Mar 21 | SSPR (metodi, registrazione combinata) + security default/MFA + administrative unit (teoria). **Lab:** abilita SSPR su un gruppo pilota e prova il reset completo. | Quiz 10: SSPR e MFA |
| Mer 22 | RBAC in profondità: assegnazione = principal+ruolo+scope, ereditarietà MG→sub→RG→risorsa, ruoli Azure vs ruoli Entra ID, control plane vs data plane. **Lab:** assegna ruoli a scope diversi e verifica con "Check access". | Quiz 10: RBAC + interrogazione (prompt 4) |
| Gio 23 | Ruoli custom (JSON, actions/notActions) e resource lock. **Lab:** ruolo custom "Reader + riavvio VM" assegnato sul RG; lock CanNotDelete e ReadOnly, prova cosa bloccano davvero. | Quiz 10: ruoli custom e lock |
| Ven 24 | Azure Policy: definizioni, initiative, effetti (deny/audit/append), remediation. **Lab:** policy tag obbligatorio + allowed locations, testa il deny. Poi: **PRACTICE ASSESSMENT n.1** (baseline) e registra i punteggi. | Analisi errori practice (prompt 2) |
| Sab 25 | Spostare risorse tra RG/subscription (vincoli), management group, ripasso Cost Management. **Lab:** sposta uno storage in un altro RG. | Quiz lungo 30 domande dominio 1 + flashcard |

### Settimana 2 — Compute I: VM, dischi, disponibilità, VMSS (27 lug – 1 ago)

Percorso MS Learn: *"AZ-104: Deploy and manage Azure compute resources"* (parte VM). Le VM sono le risorse più costose: **spegni/elimina ogni sera**.

| Giorno | Studio e lab (2,5–3 h) | Con Claude, la sera (30′) |
| --- | --- | --- |
| Lun 27 | Creazione VM, serie e dimensioni, resize, connessione (Bastion già noto). **Lab:** crea una VM, ridimensionala, documenta l'impatto. | Quiz 10: VM base e sizing |
| Mar 28 | Managed disk: Standard HDD/SSD, Premium, Ultra; data disk; snapshot e disco da snapshot. **Lab:** aggiungi data disk, snapshot, ricrea disco. | Quiz 10: dischi e snapshot |
| Mer 29 | Cifratura dischi: SSE (default), encryption at host, ADE — differenze e quando l'esame chiede quale. Immagini e Azure Compute Gallery. **Lab:** cattura un'immagine generalizzata. | Quiz 10: cifratura e immagini |
| Gio 30 | Disponibilità: availability set (fault/update domain) vs availability zone, SLA relativi, proximity placement (cenno). **Lab:** 2 VM in zone diverse. | Quiz 10: disponibilità e SLA |
| Ven 31 | VMSS: creazione, upgrade policy, scaling manuale e autoscale su metriche. **Lab:** VMSS con autoscale CPU (out >70%, in <30%) e stress test 2→4 istanze. Poi **PRACTICE n.2**. | Analisi errori practice |
| Sab 1 | Custom Script Extension e Run Command. **Lab:** installa un web server via extension. **ELIMINA** il VMSS e le VM della settimana. | Quiz lungo 30 domande VM + flashcard |

### Settimana 3 — Compute II: ARM/Bicep, App Service avanzato, container (3 – 8 ago)

Chiude il dominio compute. L'esame chiede **ARM/Bicep, non Terraform**: è quasi solo traduzione di concetti già usati al lavoro.

| Giorno | Studio e lab (2,5–3 h) | Con Claude, la sera (30′) |
| --- | --- | --- |
| Lun 3 | ARM template: parameters/variables/resources/outputs; export e redeploy; deployment mode incremental vs complete (**attenzione a complete!**). **Lab:** esporta il template dello storage, puliscilo, rideploya in un RG nuovo. | Quiz 10: ARM template |
| Mar 4 | Bicep: sintassi, param, moduli, decompile, what-if. Mappa mentale: plan→what-if, state→non esiste. **Lab:** `bicep decompile` del template di ieri, sistemalo, rideploya con what-if. | Quiz 10: Bicep |
| Mer 5 | App Service avanzato: piani e scaling (manuale/autoscale), deployment slot e swap, impostazioni sticky. **Lab:** slot "staging" sulla web app, deploy di una modifica, swap. | Quiz 10: App Service e slot |
| Gio 6 | Custom domain e certificati/TLS su App Service; backup dell'app (cenni). **Lab:** configura ciò che l'ambiente permette, il resto in teoria. | Quiz 10: domini e TLS |
| Ven 7 | ACR: build in cloud (`az acr build`), tier, autenticazione con Managed Identity (admin user off). **Lab:** Dockerfile "hello", build e push su ACR. Poi **PRACTICE n.3**. | Analisi errori practice |
| Sab 8 | ACI (container group, env var, restart policy) e Container Apps (ingress, revisioni, scale-to-zero). **Lab:** stessa immagine su ACI e su Container Apps, osserva lo scale-to-zero. Pulizia risorse. | Quiz lungo 30 domande compute + flashcard |

### Settimana 4 — Networking avanzato (10 – 14 ago, weekend di Ferragosto libero)

Percorso MS Learn: *"AZ-104: Configure and manage virtual networks for Azure administrators"*. Settimana da 5 giorni: sabato 15 è Ferragosto, riposati.

| Giorno | Studio e lab (2,5–3 h) | Con Claude, la sera (30′) |
| --- | --- | --- |
| Lun 10 | Azure DNS: zone pubbliche e private, record, auto-registration. **Lab:** private DNS zone collegata alla VNet, verifica la risoluzione tra 2 VM. | Quiz 10: DNS |
| Mar 11 | Azure Load Balancer: SKU, backend pool, health probe, regole LB e NAT inbound. **Lab:** LB Standard davanti a 2 VM con probe HTTP; spegni una VM e osserva il failover. | Quiz 10: Load Balancer |
| Mer 12 | Routing: route table/UDR, next hop, NAT Gateway per l'uscita. **Lab:** UDR che devia il traffico di una subnet, verifica con Network Watcher (next hop). | Quiz 10: routing |
| Gio 13 | Service endpoint vs private endpoint + Private DNS zone: **la differenza preferita dall'esame**. **Lab:** private endpoint su storage e SQL, disabilita l'accesso pubblico, verifica che la web app funzioni ancora. | Quiz 10: endpoint + interrogazione |
| Ven 14 | ASG per semplificare gli NSG; Network Watcher: IP flow verify, connection troubleshoot, NSG flow logs; VPN Gateway/ExpressRoute solo concetti. **Lab:** crea un blocco NSG ad hoc e dimostralo con IP flow verify. Poi **PRACTICE n.4**. Pulizia LB e VM extra. | Analisi errori practice + flashcard settimana |

### Settimana 5 — Storage avanzato + Backup e monitoraggio (17 – 22 ago)

Percorsi MS Learn: *"AZ-104: Implement and manage storage in Azure"* + *"AZ-104: Monitor and back up Azure resources"*. Venerdì c'è il practice che decide il **go/no-go**.

| Giorno | Studio e lab (2,5–3 h) | Con Claude, la sera (30′) |
| --- | --- | --- |
| Lun 17 | Strumenti: AzCopy e Storage Explorer; import/export (cenni). **Lab:** copia ~1 GB di file tra due storage account con AzCopy misurando i tempi. | Quiz 10: AzCopy e tool |
| Mar 18 | Blob avanzato: versioning, soft delete (blob e container), snapshot, point-in-time restore, object replication. **Lab:** 3 versioni di un blob, cancella, ripristina. | Quiz 10: protezione dati blob |
| Mer 19 | Azure Files avanzato: accesso identity-based, quota, snapshot; Azure File Sync (concetti). Ripasso SAS + stored access policy. **Lab:** share con snapshot e restore di un file. | Quiz 10: Files e SAS |
| Gio 20 | Recovery Services vault: backup VM (policy, on-demand), restore file-level e VM intera, soft delete del vault. **Lab:** backup completo della VM e i due tipi di restore. | Quiz 10: backup e restore |
| Ven 21 | Azure Site Recovery: replica, RPO/RTO, test failover (walkthrough o lab se il budget regge); backup Azure Files. Poi **PRACTICE n.5 — QUESTO DECIDE IL GO/NO-GO** (cap. 7). | Analisi errori practice |
| Sab 22 | Monitoraggio: alert + action group (mail/SMS/webhook), VM insights, ripasso KQL. **Lab:** alert CPU>80% con action group. **PULIZIA TOTALE:** vault (svuotato), repliche, VM. | Quiz lungo 30 domande storage+monitor |

### Settimana 6 — Simulazioni complete e ripasso mirato (24 – 29 ago)

Niente argomenti nuovi: si consolida. Ogni simulazione in condizioni reali (timer, niente pause, niente appunti).

| Giorno | Studio e lab (2,5–3 h) | Con Claude, la sera (30′) |
| --- | --- | --- |
| Lun 24 | **SIMULAZIONE COMPLETA n.1** (practice assessment intero, cronometrato). Pomeriggio: analisi di ogni errore, flashcard aggiornate. | Prompt 2 su ogni errore |
| Mar 25 | Ripasso mirato dei domini sotto l'80% — giorno 1: rileggi appunti, rifai i lab-lampo dei punti deboli (30′ l'uno). | Interrogazione sui domini deboli |
| Mer 26 | **SIMULAZIONE COMPLETA n.2.** Pomeriggio: analisi errori, confronto punteggi con lunedì. | Prompt 2 + scenario (prompt 5) |
| Gio 27 | Ripasso mirato — giorno 2: solo flashcard e domande, niente teoria nuova. | Quiz 30 domande sui punti deboli |
| Ven 28 | **SIMULAZIONE COMPLETA n.3.** Se ≥80% stabile: esame confermato. Ripasso leggero delle tabelle chiave (redundancy, SLA, endpoint, deployment mode). | Ripasso serale (prompt 7) |
| Sab 29 | Solo flashcard (max 2 h) + logistica esame: documento, tragitto o test di sistema Pearson VUE. Poi basta: da qui il cervello consolida da solo. | Interrogazione finale leggera |

### Settimana d'esame (31 ago – 4 set)

- **Lun 31 e mar 1:** mezze giornate — solo flashcard e 20 domande al giorno. Niente argomenti nuovi: a questo punto peggiorano la sicurezza, non la aumentano.
- **Mer 2 set: ESAME.** Arriva/collegati 30 minuti prima. In sala: prima passata rispondendo a tutto, segna i dubbi e rivedili alla fine; nei case study **leggi prima le domande, poi lo scenario**.
- **Gio 3 – ven 4:** buffer se hai prenotato più tardi, oppure… festeggia e aggiorna il diario con "cosa rifarei".

---

## 7. Il go/no-go: la regola che ti protegge

Il **Practice n.5 di venerdì 21 agosto** decide, senza sentimenti:

| Risultato practice n.5 | Decisione |
| --- | --- |
| ≥ 75% con tutti i domini ≥ 70% | **GO:** esame confermato per il 2 settembre. |
| 70–75% | **GO con riserva:** sposta l'esame a giovedì 3 o venerdì 4 e dedica i giorni extra ai domini deboli. |
| < 70% | **NO-GO:** riprogramma l'esame a metà settembre (di norma gratis entro le 24–48 h). Due settimane in più valgono più di un tentativo bruciato. |

Nelle simulazioni della settimana 6 vale lo stesso principio: **si prenota la fiducia sui numeri, non sulle sensazioni.**

---

## 8. Tabella punteggi (compilala ogni venerdì)

| Data | Practice | Identità | Storage | Compute | Rete | Monitor | Totale |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 24 lug | n.1 (baseline) | | | | | | |
| 31 lug | n.2 | | | | | | |
| 7 ago | n.3 | | | | | | |
| 14 ago | n.4 | | | | | | |
| 21 ago | **n.5 — go/no-go** | | | | | | |
| 24 ago | Sim. 1 | | | | | | |
| 26 ago | Sim. 2 | | | | | | |
| 28 ago | Sim. 3 | | | | | | |

---

## 9. Regole d'oro dello sprint

- **Costi:** questo sprint usa le risorse più care viste finora (più VM, VMSS, Load Balancer, vault di backup). Elimina tutto a fine giornata, tieni il budget con alert a 50 € e usa la sandbox gratuita di Microsoft Learn ogni volta che il modulo la offre.
- **Vault e ASR:** un Recovery Services vault non si elimina finché contiene backup o repliche — svuotalo (e disabilita il soft delete di lab) prima di chiudere la settimana 5.
- **Niente segreti nei prompt:** mai chiavi, password, connection string o dati del cliente.
- **Diario di bordo sempre:** ogni errore (lab o quiz) diventa una flashcard. È il motivo per cui la settimana 6 funziona.
- **Study guide ufficiale:** ricontrollala a metà sprint. Se Microsoft ha aggiunto una voce che qui manca, infilala nella settimana giusta.

---

## 10. Cosa resta fuori (di proposito)

Terraform (chiudi pure M6 se ti va, ma fuori da queste ore), Azure DevOps, il modulo AI e il capstone **non sono argomenti d'esame**: rientrano nel percorso di lavoro, dopo il 4 settembre. Questo piano ha un solo obiettivo e lo insegue senza distrazioni: il badge AZ-104 entro la prima settimana di settembre.

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

- Un'ora "protetta" a settimana per studio/lab, oppure accesso esteso all'ambiente di test (è interesse dell'azienda: i partner Microsoft valorizzano il personale certificato).
- Copertura del **voucher d'esame** (~165 USD/equivalente) — spesso le aziende lo coprono per i tirocinanti.
- Affiancamento sui ticket L1 più "didattici", così l'esperienza pratica si mappa sui domini d'esame.

> **Diario degli errori L1:** tieni traccia degli incident che risolvi al lavoro, taggandoli per dominio (identità / storage / compute / networking / monitoring). A fine percorso hai una mappa reale delle tue competenze pratiche — utile sia per l'esame sia per il colloquio di fine tirocinio.

---

## Appendice C — Note dal piano semestrale (superato)

Vale ancora la pena ricordarle:

1. **L'esame NON testa Terraform.** Al lavoro usi Terraform, ma l'AZ-104 verifica che tu sappia fare le stesse cose con **Portale Azure, Azure CLI, PowerShell e Bicep/ARM**. Per ogni risorsa che vedi creata via Terraform al lavoro, esercitati a ricrearla/modificarla *a mano* da portale o CLI.
2. **Subscription per i lab:** account Azure free (crediti iniziali + servizi sempre gratuiti) e, dove serve, pay-as-you-go con budget/alert. Spegni/elimina sempre le risorse a fine lab.
3. **L'AZ-104 passa a 700/1000** e le certificazioni role-based si rinnovano **gratis** ogni anno con un assessment online: il rischio di prenotare "prima di sentirsi pronti al 100%" è basso.
4. **Collegamento col lavoro, dominio per dominio:** gli errori L1 su automazioni sono spesso **permessi** (identità/SP senza il ruolo giusto → dominio 1); "due risorse non si parlano" è NSG/peering/route/DNS → dominio 4; leggere Log Analytics e KQL copre il dominio 5.

---

*Profilo personale, certificazioni già ottenute e contesto lavorativo: vedi `00-LEGGIMI.md` nella cartella superiore.*
