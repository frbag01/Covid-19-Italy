# Introduzione
Il dataset utilizzato in questo progetto appartiene alla categoria dei dataset medico-sanitari e di analisi epidemiologica temporale (COVID-19 Regional Tracking Dataset). L'obiettivo principale è analizzare la diffusione e l'andamento della pandemia di COVID-19 nelle diverse regioni d'Italia, tracciando le dinamiche dei contagi e la pressione sulle strutture ospedaliere.  L'analisi inoltre esplora sia l'evoluzione storica a livello nazionale (tramite curve di crescita e trend giornalieri), sia le specificità regionali. 
# Background
## Metadati principali del dataset
Il dataset comprende 15 variabili che descrivono i dati epidemiologici giornalieri rilevati dalla Protezione Civile per ciascuna regione italiana:  
- SNo (Sno) – Identificatore progressivo della rilevazione
- Date (data) Data e ora dell'aggiornamento epidemiologico
- Country (stato) Nazione di riferimento (ITA)
- RegionCode (codice_regione) Codice numerico identificativo della regione
- RegionName Nome della regione italiana
- HospitalizedPatients (ricoverati_con_sintomi) Numero di pazienti ricoverati con sintomi nei reparti ordinari
- IntensiveCarePatients (terapia_intensiva) Numero di pazienti ricoverati in terapia intensiva
- TotalHospitalizedPatients (totale_ospedalizzati) Somma totale dei pazienti ospedalizzati (ricoverati + terapia intensiva)
-  HomeConfinement (isolamento_domiciliare) Persone in isolamento fiduciario presso il proprio domicilio
-  CurrentPositiveCases (totale_positivi) Totale dei soggetti attualmente positivi al virus
-  NewPositiveCases (nuovi_positivi) Incremento giornaliero dei nuovi casi confermati
-  Recovered (dimessi_guariti) Numero cumulativo di persone dimesse o guarite
-  Deaths (deceduti) Numero cumulativo di persone decedute
-  TotalPositiveCases (totale_casi) Conteggio totale cumulativo dei casi registrati dall'inizio dell'epidemia
-  TestsPerformed (tamponi) Numero totale di tamponi molecolari/antigenici effettuati

# Domande di Analisi

1. Classifica Regionale all'Ultimo Giorno: Qual è il totale accumulato dei casi per ciascuna regione considerando solo l'ultima data disponibile nel dataset, e quale si conferma la più colpita?
2. Identificazione del Picco Pandemico: Per ciascuna regione, in quale data esatta si è registrato il valore massimo assoluto di nuovi casi giornalieri (nuovi_positivi)?
3. Andamento Nazionale dei Nuovi Casi: Come si evolve la curva dei nuovi casi giornalieri a livello nazionale lungo tutto il periodo di rilevazione?
4. Confronto delle Regioni Top 5 (Growth Rate): Selezionando le 5 regioni più colpite per totale casi, quale tra esse ha mostrato la pendenza di salita logaritmica più ripida e una crescita più accelerata?
5. Heatmap Temporale ed "Effetto Lunedì": Esiste una stagionalità settimanale nei dati nell'aggregazione dei nuovi casi suddivisi per mese e giorno della settimana?

# Tools utilizzati
Durante lo sviluppo del progetto sono stati utilizzati diversi strumenti e tecnologie:

- Python per l’analisi dei dati e i test statistici
- SQL per interrogare e aggregare i dati
- Excel per la creazione di una dashboard riassuntiva e interattiva

Per supportare alcune fasi del processo analitico e migliorare l’efficienza nello sviluppo delle query e del codice, è stato utilizzato anche l’ausilio di strumenti di Intelligenza Artificiale.

Il progetto è stato inoltre ispirato ai progetti di data analysis realizzati da Luke Barousse, noto per i suoi contenuti educativi nel campo della data analytics e per i suoi esempi pratici di portfolio basati su SQL, Python e dashboard.

# Analisi
### 1. Classifica Regionale all'Ultimo Giorno
Trova il totale dei casi per ogni RegionName considerando solo l'ultima data disponibile nel dataset. Ordina per gravità.
```sql
SELECT denominazione_regione,totale_casi
FROM covid19_italy_region
ORDER BY data desc, totale_casi desc
LIMIT 21
```

#### Risultati e Insights

| Posizione | Regione (`denominazione_regione`) | Totale Casi Cumulativi (`totale_casi`) |
| :---: | :--- | :---: |
| **1** | **Lombardia** | **429.109** |
| **2** | **Piemonte** | **177.788** |
| **3** | **Campania** | **165.293** |
| **4** | **Veneto** | **165.249** |
| **5** | **Emilia-Romagna** | **133.761** |
| **6** | **Lazio** | **130.255** |
| **7** | **Toscana** | **108.397** |
| **8** | **Sicilia** | **71.489** |
| **9** | **Puglia** | **64.341** |
| **10** | **Liguria** | **53.779** |
| **11** | **Friuli Venezia Giulia** | **35.467** |
| **12** | **Marche** | **32.393** |
| **13** | **Abruzzo** | **30.274** |
| **14** | **P.A. Bolzano** | **25.361** |
| **15** | **Umbria** | **25.144** |
| **16** | **Sardegna** | **24.186** |
| **17** | **Calabria** | **18.537** |
| **18** | **P.A. Trento** | **17.103** |
| **19** | **Basilicata** | **8.940** |
| **20** | **Valle d'Aosta** | **6.726** |
| **21** | **Molise** | **5.286** |

#### Key Takeaways:
- **Lombardia Prima per Distacco:** La Lombardia guida la classifica con un totale imponente di **429.109 casi**, registrando un volume che distanzia di oltre il **240%** la seconda regione in graduatoria (il Piemonte con 177.788 casi).
- **Prevalenza delle Regioni del Nord:** I territori settentrionali (Lombardia, Piemonte, Veneto, Emilia-Romagna) occupano quasi interamente le primissime posizioni del ranking, confermandosi le macro-aree storicamente e numericamente più colpite dall'emergenza sanitaria.
- **Rilevanza della Densità abitativa e della Popolazione:** Va sottolineato che l'elevato numero assoluto di casi risente in modo diretto della struttura demografica territoriale: regioni estremamente popolate e ad alta densità abitativa o con importanti nodi produttivi/urbani (come Lombardia, Campania e Lazio) tendono naturalmente a registrare volumi di contagio complessivi più elevati rispetto a regioni con un bacino di popolazione ridotto (es. Molise e Valle d'Aosta).

### 2. Identificazione del Picco Pandemico
Per ogni regione, identifica la data esatta in cui si è registrato il maggior incremento di nuovi casi giornalieri.
```sql
SELECT covid19_italy_region.denominazione_regione,
       covid19_italy_region.data,
       covid19_italy_region.nuovi_positivi
FROM covid19_italy_region 
JOIN (
    SELECT denominazione_regione,
           MAX(nuovi_positivi) AS max_positivi
    FROM covid19_italy_region
    GROUP BY denominazione_regione
) m
ON covid19_italy_region.denominazione_regione = m.denominazione_regione
AND covid19_italy_region.nuovi_positivi = m.max_positivi
ORDER BY covid19_italy_region.data;
```

#### Risultati e Insights

| Regione (`denominazione_regione`) | Data del Picco Massimo | Picco Nuovi Positivi (`nuovi_positivi`) |
| :--- | :---: | :---: |
| **Lombardia** | **07/11/2020** | **11.489** |
| **Piemonte** | 19/11/2020 | **5.349** |
| **Campania** | 08/11/2020 | **4.601** |
| **Veneto** | 26/11/2020 | **3.980** |
| **Lazio** | 14/11/2020 | **2.997** |
| **Emilia-Romagna** | 15/11/2020 | **2.822** |
| **Toscana** | 07/11/2020 | **2.787** |
| **Puglia** | 05/12/2020 | **1.884** |
| **Sicilia** | 19/11/2020 | **1.871** |
| **Friuli Venezia Giulia** | 28/11/2020 | **1.432** |
| **Liguria** | 13/11/2020 | **1.209** |
| **Abruzzo** | 14/11/2020 | **939** |
| **Calabria** | 18/11/2020 | **936** |
| **Marche** | 12/11/2020 | **834** |
| **P.A. Bolzano** | 13/11/2020 | **820** |
| **Umbria** | 12/11/2020 | **783** |
| **Sardegna** | 13/11/2020 | **623** |
| **P.A. Trento** | 31/10/2020 | **390** |
| **Basilicata** | 25/11/2020 | **329** |
| **Valle d'Aosta** | 14/11/2020 | **245** |
| **Molise** | 04/12/2020 | **176** |

#### Key Takeaways:
- **Concentrazione Temporale nel Mese di Novembre 2020:** La quasi totalità delle regioni italiane ha raggiunto il valore massimo di nuovi contagi giornalieri durante la seconda ondata, nello specifico **tra la prima e la terza settimana di novembre 2020**.
- **Coerenza con i Volumi Complessivi (Domanda 1):** I valori di picco rispecchiano fedelmente la proporzione e le grandezze viste nella classifica dei casi totali: **Lombardia (11.489)**, **Piemonte (5.349)** e **Campania (4.601)** si confermano le tre regioni con la pressione giornaliera più alta dell'intero territorio nazionale.
- **Inversione Anticipata del Trend in Lombardia:** Nonostante la Lombardia registri di gran lunga la cifra più alta in assoluto, il suo picco si colloca molto presto nella stagione autunnale (**7 novembre 2020**). Questo dato indica che, pur in presenza di volumi elevatissimi, la regione è stata tra le prime a mostrare gli effetti del rafforzamento delle misure di contenimento, invertendo la curva dei contagi prima di altre realtà.


# PYTHON 

Puoi vedere il codice principale qui: [1] [Python Script](cov19.py)

### 3. Andamento Nazionale
Crea un grafico a linee dei nuovi casi giornalieri a livello nazionale
![Grafico per osservare l'andamento del fenomeno](https://github.com/frbag01/Covid-19-Italy/blob/main/grafico.png?raw=true)

- **La Prima Ondata (Primavera 2020):** L'inizio dell'emergenza epidemiologica a marzo mostra la prima importante impennata della curva, raggiungendo il suo massimo il **21 marzo 2020** con **6.557 nuovi casi giornalieri**. 
- **La Fase Estiva di Calo:** Durante i mesi estivi (giugno - agosto 2020) si osserva una netta ed evidente flessione della curva con un minimo toccato a metà luglio (114 casi il 14/07/2020). Questo appiattimento evidenzia la stagionalità estiva e il temporaneo contenimento del virus.
- **La Seconda Ondata Autunnale (Forte Spinta di Crescita):** A partire da ottobre 2020 si registra una ripartenza esponenziale dei contagi che sfocia nel picco assoluto del **13 novembre 2020** con **40.902 nuovi casi in 24 ore**. La seconda ondata ha mostrato volumi giornalieri oltre **6 volte superiori** rispetto al picco primaverile (fenomeno legato sia ad una maggiore diffusione virale, sia all'enorme incremento nella capacità di tracciamento e nel numero di tamponi effettuati).



### 4.Confronto tra Regioni
Scegli le 5 regioni più colpite e confronta la loro curva di crescita logaritmica. Quale regione ha mostrato la salita più ripida?

![andamento logaritmico](https://github.com/frbag01/Covid-19-Italy/blob/main/lomb.png?raw=true)

- **Dinamica di Crescita della Lombardia:** 
  - **Fase Primaverile:** La salita di marzo 2020 mostra una pendenza rettilinea e quasi verticale, caratteristica tipica della **crescita esponenziale incontrollata** delle fasi iniziali (passando da poche decine a oltre 3.000 casi al giorno).
  - **Ripresa Autunnale (Ottobre 2020):** La ripartenza registrata in autunno mostra la **salita più ripida e costante dell'intero grafico**, dove la Lombardia passa da **324 nuovi casi** (1° ottobre) a ben **8.919 nuovi casi** (1° novembre).
- **Omogeneità del Pattern tra le Top 5 Regioni:** La curva logaritmica della Lombardia ricalca perfettamente l'andamento osservato nelle altre principali regioni per numero di casi (Piemonte, Campania, Veneto ed Emilia-Romagna) e a livello nazionale.
- **Conclusione:** L'analisi logaritmica dimostra che, sebbene i volumi assoluti differiscano tra i territori, **la velocità di propagazione del virus durante le fasi di recrudescenza ha seguito dinamiche strutturali del tutto analoghe** su tutto il territorio nazionale.



### 5.Heatmap Temporale:

Crea una barplot che mostri i giorni della settimana sull'asse X e i mesi, sull'asse Y il numero di nuovi casi. Esiste un "effetto lunedì" nel reporting dei dati?

![analisi lunedì](https://github.com/frbag01/Covid-19-Italy/blob/main/luned%C3%AC.png?raw=true)

- **Evidenza del Ciclismo Settimanale:** Il grafico evidenzia in modo sistematico (specialmente nei mesi di picco come ottobre e novembre 2020) che il lunedì (`Monday`) registra **costantemente il minor numero di nuovi casi confermati** rispetto al resto della settimana.
- **Fattori Amministrativi e di Tracciamento (Driver Principale):**
  - **Minor Numero di Tamponi Processati la Domenica:** Nel fine settimana laboratori di analisi, strutture sanitarie e medici di medicina generale operano a regime ridotto. I tamponi effettuati o refertati la domenica (comunicati nel report del lunedì) sono numericamente inferiori.
  - **Ritardo di Notifica (Reporting Delay):** I dati comunicati dalla Protezione Civile il lunedì riflettono l'attività amministrativa delle 24 ore precedenti (domenica). Il carico di lavoro accumulato nel weekend viene poi smaltito ed elaborato tra martedì e venerdì, generando il progressivo crescendo delle notifiche a metà settimana.
- **Fattori Comportamentali e Sociali:**
  - **Dinamica dei Contatti Familiare vs Lavorativo:** Il rientro da periodi di riposo nel weekend — vissuti spesso in contesti familiari o con cerchie ristrette — riduce temporaneamente le occasioni di tracciamento formale, mentre la ripresa delle attività lavorative e scolastiche del lunedì incentiva i controlli.
- **Conclusione per la Data Analysis:** L' "Effetto Lunedì" non rappresenta una reale diminuzione della circolazione del virus all'inizio della settimana, bensì un **artefatto nei flussi di raccolta dati**. 

