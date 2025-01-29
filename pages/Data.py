import streamlit as st
import datetime

from functions import * #import delle funzioni presenti nel file functions.py

#configurazione pagina
st.set_page_config(
    page_title="Laguna di Venezia/Data",
    page_icon=":cyclone:",
    layout="centered"
)

ct0, ct1, ct2, ct3, ct4 = (st.container(border=True) for _ in range(5))#container

param, staz, tempo = False , False, None #parametri necessari per la selezione

#funzione intermedia per bottone GO 
def fInter():
    tab1, tab2 = ct4.tabs(["GRAFICI", "DATAFRAME"])
    if param: #se viene selezionato il buttone per parametri entra nell'if
        #creazione lista con i parametri "convertiti" in parametri_codice
        lista=[]
        for i in param:
            lista.append(parametri[0][parametri[1].index(i)])
        
        tabella = get_listaData_param(lista, tempo) # restituisce lista di dataframe in base al tempo selezionato (un dataframe per ogni parametro)
        grafici = get_listaGraf_param(tabella, param) #restituisce una lista di grafici (un grafico per ogni parametro)
        
        for i in range(len(tabella)):
            with ct4:
                #if necessario in quanto, per i seguenti parametri, occorre mantenere la larghezza dei grafici scelta e non quella del container
                #stampa dei grafici nella parte "GRAFICI" del tab
                if(param[i] =="Velocità max vento" or param[i] =="Velocità media vento" or param[i]=="Livello medio idrometrico" or
                    param[i] =="Direzione media vento" or param[i] == "Pioggia" or param[i] == "Radiazione solare"):
                    tab1.subheader(f":green[{param[i]}]")
                    tab1.altair_chart(grafici[i])
                else:
                    tab1.subheader(f":green[{param[i]}]")
                    tab1.altair_chart(grafici[i], use_container_width=True)

                #stampa dei dataframe nella parte "DATAFRAME" del tab
                tab2.subheader(f":green[{param[i]}]")
                tab2.dataframe(tabella[i], width=1000)
    
    if staz: #se viene selezionato il buttone per stazioni entra nell'if
        #creazione della lista per le stazioni sotto forma di codice
        lista=[]
        for i in staz:
            lista.append(stazioni[1][stazioni[2].index(i)])

        tabella = get_listaData_staz(lista, tempo) #funzione per ottenere lista di dataframe, uno per ogni stazione 
        grafici = get_listaGraf_staz(tabella) # lista (in realtà lista di liste) di grafici (ogni stazione avrà la sua lista di grafici)
      
        for i in range(len(tabella)):#per ogni stazione
            with ct4:
                #stampa dei grafici
                tab1.subheader(f":green[{staz[i]}]")
                for g in grafici[i]:
                    tab1.altair_chart(g, use_container_width=True)
                #stampa dei dataframe
                tab2.subheader(f":green[{staz[i]}]")
                tab2.dataframe(tabella[i], width=1000)

 
#DATAFRAME COMPLETO (valori recuperati dai numerosi csv del sito di venezia, quindi i codici delle stazioni e dei parametri non sono stati modificati)
with st.sidebar:
    all = st.checkbox("Dataframe completo")
    
if all:
    ct0.subheader(":blue[Dataframe completo]")
    ct0.write(data)

#titolo
ct1.subheader(":red[Seleziona per Stazione o per Parametri (obbligatorio)]", divider="gray")

#bottone per la scelta parametri o stazioni (se non si seleziona non viene fuori il bottone successivo)
on1 = ct1.segmented_control(" ", ["Parametri", "Stazioni"], label_visibility="collapsed")
if on1=="Parametri":
    ct1.subheader(":red[Seleziona parametri (obbligatorio)]", divider="gray")
    #scelta dei parametri tra quelli presenti nella lista in funcions.py (parametri[1])
    param = ct1.pills(" ", parametri[1], selection_mode="multi", label_visibility="collapsed")
    
elif on1 == "Stazioni":
    ct1.subheader(":red[Seleziona stazioni (obbligatorio)]", divider="gray")
    #scelta delle stazioni tra quelle presenti nella lista in funcions.py (stazioni[2])
    staz = ct1.pills(" ", stazioni[2], selection_mode="multi", label_visibility="collapsed")

#selezione del tempo (non obbligatorio: SE NON SELEZIONO NIENTE IL PROGRAMMA INTERROGA IL DATAFRAME SU TUTTO IL PERIODO DISPONIBILE)
if param or staz:#bisogna per forza selezionare o parametri o stazione
    ct2.subheader(":red[Seleziona per Giorno o Periodo (facoltativo)]", divider="gray")
    ct2.write("""ATTENZIONE: per una questione di pesantezza dei grafici, questa applicazione aggrega i dati se il periodo è troppo grande
               (i valori vengono aggregati facendo una media ogni tot valori);  questo implica una leggera distorsione dei dati e si consiglia quindi,
               una volta individuato il periodo d'interesse, di selezionare solo pochi giorni in modo da avere un grafico più veritiero.""")
    on2 = ct2.segmented_control(" ", ["Giorno", "Periodo"], label_visibility="collapsed")
    if on2=="Giorno":#selezione per giorno
        ct2.subheader(":red[Seleziona Giorno]", divider="gray")
        #inizio = oggi - 3 mesi (questo perchè il programma tratta i dati degli ultimi 3 mesi)
        tempo = ct2.date_input("Seleziona giorno", 
                            datetime.date(inizio.year, inizio.month, inizio.day), 
                            min_value=datetime.date(inizio.year, inizio.month, inizio.day), 
                            max_value=datetime.date(oggi.year, oggi.month, oggi.day),
                            format="DD.MM.YYYY")
            
    elif on2 == "Periodo":#selezione per periodo
        ct2.subheader(":red[Seleziona Periodo]", divider="gray")
        tempo = ct2.date_input("Seleziona periodo",
                            (datetime.date(inizio.year, inizio.month, inizio.day) , datetime.date(oggi.year, oggi.month, oggi.day) ),
                                min_value=datetime.date(inizio.year, inizio.month, inizio.day),
                                max_value=datetime.date(oggi.year, oggi.month, oggi.day),
                                format="DD.MM.YYYY")

    #buttone che (passando per funzione intermedia fInter) avvia il programma di ricerca
    go = ct3.button("GO", type="primary", on_click=fInter, use_container_width=True)