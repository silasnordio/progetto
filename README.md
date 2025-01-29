Nordio Silas 2069794

PROGETTO SULLA RETE TELEMAREOGRAFICA DELLA LAGUNA DI VENEZIA


#ESECUZIONE#
    -per eseguire l'applicazione occorre semplicemente fare ' uv run streamlit run Home.py'

N.B: è indifferente la scelta del tema (bianco/nero) nelle impostazioni, ma è consigliata la selzione centrata (NON wide mode) nelle pagine Data e Example in quanto, se modifico la dimensione della pagina web, i grafici mantengono la loro dimensione e non rallentano il programma (ciò non avviene se la wide mode è attiva).

Non dovrebbero esserci problemi col "path" in quanto gli unici percorsi sono i link per scaricare i csv dal CPSM (nel caso ci sia un problema con questo sito nel scaricare i dati, è presente in functions.py la possibilità di usare i csv in locale (cartella daticsv)usando la riga commentata numero 27 al posto della 28 e usando la 34 al posto della 35); facendo ciò però potrebbero esserci problemi col path nel caso si utlizzi linux. ->(l'unico link rimane comunque a riga 34)



#SCOPO#
L'applicazione svolta è indirizzata ad un pubblico più tecnico in quanto permette una prima interfaccia con i dati recuperati dalle stazioni telemareografiche di Venezia.
Questi dati sono file csv (uno per stazione) e contengono i valori dei parametri rilevati negli ultimi 3 mesi.

Lo scopo del programma non è vedere esattamente come sono correlati i dati tra di loro, ma permette di dare una prima occhiata a come si comportano (come spiegato nella descrizione degli esempi, se noto una possibile relazione tra 2 parametri o 2 stazioni, posso scaricare i dataframe e, sfruttando ad esempio R, studiarne la correlazione tra essi).



#DESCRIZIONE#
L'applicazione è suddivita in 3 pagine principali (con menù sidebar a sinistra) e un file functions.py con le relative funzioni:
    -Home: 
        Qui è presente una piccola descrizione del programma destinato a chi lo usa con possibilità di rimuovere i pragrafi grazie ai bottoni presenti a sinistra (in caso diano fastidio);
        In fondo, invece, è presente una mappa della laguna con le stazioni presenti marcate da un punto rosso. 
        qui è possibile vedere la tipologia dei dati rilevati per ogni stazione semplicemente andandoci sopra col cursore;
        Inoltre, sempre nel menù a sinistra, troviamo un link che ci porta direttamente al sito da cui ho preso spunto e scaricato i file csv.
    -Data:
        Qui abbiamo la pagina essenziale del programma che ci permette di selezionare i dati a nostro piacimento;
        Troviamo un bottone (Parametri / Stazione), in base alla scelta compaiono dei bottoni "pills" con tutti/e i/le parametri/stazioni trattate dal CPSM (Centro Previsioni e Segnalazioni Maree); da qui selezioniamo ciò che ci interessa vedere e ci compare la selezione temporale;
        Essa consiste in una selezione del singolo giorno o per un intervallo: questa parte non è obbligatoria da selezionare e infatti compare già il bottone GO per ottenere i dati (N.B. se NON selezioniamo un filtro temporale allora il programma selezionerà tutti i dati in suo possesso: ovvero 3 mesi) 
        [è presente un 'ATTENZIONE' che informa l'utente che i dati vengono leggermente distorti (viene fatta una media) per la rappresentazione grafica (non per i dataframe) in quanto, se creo un grafico con troppi record, tipo 200.000, questo non si muove e blocca il sito. Ciò avviene nel caso i dati vengano recuperati per un periodo di tempo]
        Col pultante GO appare un altro container con un tab (GRAFICI / DATAFRAME).
        Nel caso abbia selezionato Parametri all'inizio allora compariranno grafici e tabelle riferite ad essi(uno/a per parametro) con una legenda dei colori per tutte le stazioni che rilevato tale prametro; nel caso delle Stazioni invece appariranno i grafici di tutti i parametri rilevati dalla stazioni in maniera separata.

        A sinistra, nel menù, abbiamo un pulsante che ci stampa un dataframe scaricabile con tutti i dati GREZZI recuperati dal CPSM;
        questo dataframe è semplicimente l'unione dei 14 file csv (DATA in comune)
    -Example: 
        Questa sezione istruisce l'utente al corretto funzionamnto dell'applicazione e ne mostra un possibile approccio per come sfruttalo al meglio.
        Sono presenti 3 esempi con possibilità di deselezione a sinistra.

    -functions.py:
        In questo file sono presenti quasi tutte le funzioni del programma che vengono poi importate dalle 3 pagine principali.

Alcuni grafici mi hanno dato problemi nella loro realizzazione (direzione media vento e altri) ma ho preferito inserire lo stesso un grafico, non molto comprensibile, piuttosto che ignorare completamente il parametro.



