import streamlit as st
import datetime

from functions import * #import delle funzioni presenti nel file functions.py

#configurazione pagina
st.set_page_config(
    page_title="Laguna di Venezia/Example",
    page_icon=":cyclone:",
    layout="centered"
)

with st.sidebar:    
    uno = st.checkbox("Esempio 1", value=True)# checkbox per Esempio 1
    due = st.checkbox("Esempio 2", value=False)# checkbox per Esempio 2
    tre = st.checkbox("Esempio 3", value=False)# checkbox per Esempio 3

#titolo pagina in rosso
st.header(":red[Esempi di utilizzo dell'applicazione]", anchor=None)

#container
con0 = st.container(border=True)# per esempio 1
con1 = st.container(border=True)# per esempio 2
con2 = st.container(border=True)# per esempio 3



######################### Altezza significativa onda e Velocità max vento ################################ 
if uno:
    con0.subheader(":blue[Relazione tra Altezza significativa onda e Velocità max vento]")
    con0.write("""Interroghiamo l'applicazione chiedendo i dati relativi ai parametri.  
               Selezioniamo Altezza significativa onda e Velocità max vento sul tutto il periodo
               per vedere c'è una qualche correlazione tra i due e controlliamo i grafici.""")

    tab1, tab2 = con0.tabs(["GRAFICI", "DATAFRAME"])
    lista = ["Onda: Alt. sign.", "V.Vento max"]#necessario per ottenere tabella
    param = ["Altezza significativa onda", "Velocità max vento"] #necessario per ottenere grafici

    tabella = get_listaData_param(lista, None)
    grafici = get_listaGraf_param(tabella, param)

    #stampa grafici e dataframe in bast ai parametri inseriti
    for i in range(len(tabella)):
        with con0:
            if(param[i] =="Velocità max vento" or param[i] =="Velocità media vento" or param[i]=="Livello medio idrometrico" or
                param[i] =="Direzione media vento" or param[i] == "Pioggia" or param[i] == "Radiazione solare"):
                tab1.subheader(f":green[{param[i]}]")
                tab1.altair_chart(grafici[i])
            else:
                tab1.subheader(f":green[{param[i]}]")
                tab1.altair_chart(grafici[i], use_container_width=True)

            tab2.subheader(f":green[{param[i]}]")
            tab2.dataframe(tabella[i], width=1000)

    con0.write("""Notiamo una evidente relazione tra i due parametri; allora decidiamo di verificare tale relazione per una delle stazioni che li registra entrambi
            tramite l'apposita ricerca per stazioni (ad esempio per la stazione Misericordia) per un periodo ridotto 
               (ad esempio per la prima settimana di dicembre.""")
    
    tab1, tab2 = con0.tabs(["GRAFICI", "DATAFRAME"])

    staz = ["Misericordia"]
    tempo = (datetime.date(2024, 12, 1), datetime.date(2024, 12, 7))#filtro temporale
    
    tabella = get_listaData_staz(staz, tempo)
    grafici = get_listaGraf_staz(tabella)

    #stampa grafici e dataframe in base alla stazione inserita
    for i in range(len(tabella)):
        with con0:
            tab1.subheader(f":green[{staz[i]}]")
            for g in grafici[i]:#stampa tutti i grafici per la stazione
                tab1.altair_chart(g, use_container_width=True)

            tab2.subheader(f":green[{staz[i]}]")
            tab2.dataframe(tabella[i], width=1000)

    con0.write("""Da qui "verifichiamo" la nostra ipotesi, cambiando per esempio periodo, e in caso abbiamo la possibilità di scaricare il dataframe 
            con i dati necessari per studiarne la correlazione con un apposito programma (ad esempio R).""")



######################### Umidità e Radiazione solare ################################ 
if due:#(ANALOGO)
    con1.subheader(":blue[Relazione tra  Umidità e Radiazione solare]")
    con1.write("""Interroghiamo l'applicazione chiedendo i dati relativi ai parametri: Umidità e Radiazione solare su tutto il periodo.""")

    tab1, tab2 = con1.tabs(["GRAFICI", "DATAFRAME"])
    lista = ["Umidita'", "Radiazione solare"]
    param = ["Umidità", "Radiazione solare"]

    tabella = get_listaData_param(lista, None)
    grafici = get_listaGraf_param(tabella, param)

    for i in range(len(tabella)):
        with con1:
            if(param[i] =="Velocità max vento" or param[i] =="Velocità media vento" or param[i]=="Livello medio idrometrico" or
                param[i] =="Direzione media vento" or param[i] == "Pioggia" or param[i] == "Radiazione solare"):
                tab1.subheader(f":green[{param[i]}]")
                tab1.altair_chart(grafici[i])
            else:
                tab1.subheader(f":green[{param[i]}]")
                tab1.altair_chart(grafici[i], use_container_width=True)

            tab2.subheader(f":green[{param[i]}]")
            tab2.dataframe(tabella[i], width=1000)

    con1.write("""Notiamo una evidente relazione opposta tra i due parametri (dove uno cresce allora l'altro crolla); allora decidiamo di verificare tale relazione per una delle stazioni che li registra entrambi
            tramite l'apposita ricerca per stazioni (ad esempio per la stazione Palazzo Cavalli) per la prima settimana di dicembre)""")

    tab1, tab2 = con1.tabs(["GRAFICI", "DATAFRAME"])

    staz = ["Palazzo Cavalli"]
    tempo = (datetime.date(2024, 12, 1), datetime.date(2024, 12, 7))

    tabella = get_listaData_staz(staz, tempo)
    grafici = get_listaGraf_staz(tabella)

    for i in range(len(tabella)):
        with con1:
            tab1.subheader(f":green[{staz[i]}]")
            for g in grafici[i]:
                tab1.altair_chart(g, use_container_width=True)

            tab2.subheader(f":green[{staz[i]}]")
            tab2.dataframe(tabella[i], width=1000)

    con1.write("""Da qui notiamo che, come ipotizzato, i parametri sono legati ma anche la temperatura è coinvolta nella relazione e quindi possiamo
               proseguire il nostro studio di conseguenza.""")


################################# Altezza significativa onda e Velocità max vento #################################
if tre:#(ANALOGO)
    con2.subheader(":blue[Recupero dati dighe: Malamocco, Lido e Chioogia]")
    con2.write("""Interroghiamo l'applicazione chiedendo i dati relativi alle 3 dighe.""")

    tab1, tab2 = con2.tabs(["DATAFRAME", "GRAFICI"])

    stazc = [["D.S. Lido","Faro Diga Lido"], "D.N. Malamocco", "D.S.Chioggia"]
    stazn = ["Diga Sud Lido e Faro", "Diga Nord Malamocco", "Diga Sud Chioggia"]

    tabella = get_listaData_staz(stazc, None)
    grafici = get_listaGraf_staz(tabella)

    for i in range(len(tabella)):
        with con2:
            tab2.subheader(f":green[{stazn[i]}]")
            for g in grafici[i]:
                tab2.altair_chart(g, use_container_width=True)

            tab1.subheader(f":green[{stazn[i]}]")
            tab1.dataframe(tabella[i], width=1000)

    con2.write("""Da qui possiamo scaricare i dataframe per analizzarli con un software adatto (ad esempio R)
                oppure anche controllare i grafici per eventuali dubbi su dei valori.""")