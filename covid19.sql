
DROP TABLE IF EXISTS covid19_italy_region;

CREATE TABLE covid19_italy_region (

    Sno INT PRIMARY KEY,

    data TIMESTAMP,                     -- Data e ora rilevazione
    
    stato VARCHAR(50),                  -- Stato (Italia)
    
    codice_regione INT,                 -- Codice numerico regione
    
    denominazione_regione VARCHAR(100), -- Nome regione

    ricoverati_con_sintomi INT,
    
    terapia_intensiva INT,
    
    totale_ospedalizzati INT,
    
    isolamento_domiciliare INT,
    
    totale_positivi INT,
    
    nuovi_positivi INT,
    
    dimessi_guariti INT,
    
    deceduti INT,
    
    totale_casi INT,
    
    tamponi NUMERIC(8,1)

);



1. Classifica Regionale all'Ultimo Giorno:

Domanda: Trova il totale dei casi per ogni RegionName considerando solo l'ultima data disponibile nel dataset. Ordina per gravità.


SELECT denominazione_regione,totale_casi
FROM covid19_italy_region
ORDER BY data desc, totale_casi desc
LIMIT 21

2. Identificazione del Picco Pandemico:

Domanda: Per ogni regione, identifica la data esatta in cui si è registrato il maggior incremento di nuovi casi giornalieri.


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


