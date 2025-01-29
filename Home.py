import streamlit as st
import pandas as pd
import pydeck as pdk #per la mappa

from functions import * #import delle funzioni presenti nel file functions.py

#configurazione pagina
st.set_page_config(
    page_title="Laguna di Venezia",#titolo (link)
    page_icon=":cyclone:",#icona
    layout="wide"
)

#titolo pagina in rosso
st.header(":red[Dati Telemareografici della Laguna di Venezia]", anchor=None)

#container
con0 = st.container(border=True)# per descrizione generale
con1 = st.container(border=True)# per stazioni
con2 = st.container(border=True)# per parametri
con3 = st.container(border=True)# per mappa

#menù sidebar a sinistra
with st.sidebar:    
    descrizione = st.checkbox("Descrizione generale", value=True)# checkbox per descrizione generale in container 0
    sta = st.checkbox("Descrizione stazioni", value=True)# checkbox per descrizione delle stazioni in container 1
    par = st.checkbox("Descrizione parametri", value=True)# checkbox per descrizione dei parametri in container 2

    # link_button che apre in una altra finestra il sito di venezia (dove ho preso spunto per il progetto)
    sito = st.link_button("www.comune.venezia.it", "https://www.comune.venezia.it/it/content/dati-dalle-stazioni-rilevamento")


#######################################################################################################################
#DESCRIZIONE GENERALE
# if checkbox descrizione è attivo allora stampa container 0 con descrizione generale  
if descrizione:
    con0.subheader(":blue[Descrizione generale]")
    con0.write("""La rete telemareografica della laguna di Venezia si occupa dell'acquisizione e della registrazione dei dati metereologici e marittimi del territorio.
               Tali dati vengono registrati da numerose stazioni attraverso l'utilizzo di particolari sensori con una frequenza di 5 minuti.  
               Questa applicazione, per motivi di comodità, si occupa essenzialmente dei dati degli ultimi 3 mesi, ma è possibile,
                tramite l'apposito pulsante nel menù a sinistra, visitare direttamente il sito ufficiale del 
               Centro Previsioni e Segnalazioni Maree e ottenere lo storico degli ultimi anni grazie ai loro database.  
               La funzionalità principale di questa applicazione è quella di recuperare i dati in base alle proprie esigenze 
               selezionando solo le stazioni o i parametri d'interesse; questo è possibile nella sezione "Data" presente nel menù a sinistra.  
               Oltre che a generare un database dei dati richiesti, l'applicazione mostra una rappresentazione grafica dei dati.
               Questo è utile del caso si vogliano confrontare i valori per capire l'andamento di un fenomeno, o se c'è la possibile presenza di
                correlazione con altri parametri.  
               Infine, nella sezione "Example" a sinistra, ci sono degli esempi sull'utilizzo di questo sito in base ai dati richiesti.""")

#######################################################################################################################
#STAZIONI
if sta:
    con1.subheader(":blue[Stazioni]")
    con1.write("""La rete telemareografica è costituita da varie stazioni automatiche che acquisiscono i dati registrati dai sensori e li
            trasmettono alla centrale situata nel centro storico di Venezia; questa li archivia in un database costruito in linguaggio SQL.  
            Le stazioni da noi gestite non presentano tutte le medesime caratteristiche: alcune si occupano solamente dei dati marittimi
             mentre altre, più complete, acquisiscono anche altri dati.  
            Nella mappa sottostante è possibile vedere, per ogni stazione, la tipologia dei valori raccolti.""")

#######################################################################################################################
#PARAMETRI
if par:
    con2.subheader(":blue[Parametri]")
    s="" #creazione stringa contenente in verticale tutti i parametri
    for p in parametri_output:
        s+=f"-{p}\n"
    con2.text(f"""I parametri gestiti dalla rete sono i seguenti: \n {s}
              I dati sono registrati nel database del Centro Previsioni e Segnalazioni Maree senza un controllo umano, quindi i dati non sono da considerare privi di errori e di qualche possibile valore anomalo.""")

#######################################################################################################################
# MAPPA

#dati per il posizionamento dei punti e dei nomi delle stazioni sulle mappe
dati = {
    #liste coordinate per le rispettive stazioni
    "lat": [45.431078, 45.323055, 45.423230, 45.334358, 45.228547, 45.436432, 45.223086, 45.495597, 45.445386, 45.487502, 45.339800, 45.232531, 45.408889, 45.4284095],
    "lon": [12.336378, 12.514722, 12.426553, 12.341539, 12.312767, 12.333535, 12.280142, 12.471972, 12.336205, 12.415472, 12.291967, 12.280593, 12.256944, 12.3462636],
    
    #lista nomi stazioni (presente in functions.py)
    "nome": stazione_output,

    #richiama una funzione che restituisce una lista di stazioni, per ogni stazione abbiamo i rispettivi parametri che troviamo nel suo database in formato html
    "parametri": [lista_param(s) for s in stazione_output]
}

df = pd.DataFrame(dati)#conversione dei dati in dataframe

# creazione nuova colonna nel data frame con le longitudi traslate di 0.004 per far apparire il nome della stazione più a destra rispetto al punto rosso
df["lon_text"] = df["lon"] + 0.004 

#configurazione della mappa
layer = pdk.Layer(
    "ScatterplotLayer",  #layer per i punti rossi
    data=df,
    get_position="[lon, lat]",
    get_radius=200,
    get_fill_color=[238, 0, 0, 200],
    pickable=True
)

testo = pdk.Layer(
    "TextLayer",  #layer di testo per i nomi delle stazioni
    data=df,
    get_position="[lon_text, lat]",
    get_text = "nome",
    get_size=12,
    get_color=[240, 255, 240],
    get_angle=0,
    get_text_anchor='"start"',
    get_alignment_baseline='"center"',
    pickable=True
)

view_state = pdk.ViewState( # posizione di partenza della mappa
    latitude=45.35,
    longitude=12.40,
    zoom=9.5
)

tooltip = {# piccolo menu che appare quando il cursore si trova sopra alla stazione
    "html": "<b>{nome}</b><br>{parametri}",# la funzione per ottenere i parametri ci restituisce una lista di elementi in html <li>
    "style": {
        "backgroundColor": "tomato",
        "color": "white"
    }
}

#generazione della mappa in container 1
con3.pydeck_chart(pdk.Deck(
    layers=[layer,testo],#unione dei 2 layer (pallino rosso e nome stazione)
    initial_view_state=view_state,
    tooltip=tooltip
))

########################################################################################################################