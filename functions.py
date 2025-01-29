import streamlit as st
import altair as alt
import polars as pl
import pandas as pd
import numpy as np
import datetime
from datetime import date #per variabili oggi e inizio
from dateutil.relativedelta import relativedelta


#lista nomi stazioni per ottenere i file csv (i percorsi o i link per ottenere i csv differiscono solo dei seguenti nomi)
stazioni_nome = ["PuntaSalute_CanalGrande", "Piattaforma", "DigaSudLido", "DigaNordMalamocco", "DigaSudChioggia", "PalazzoCavalli", "ChioggiaCitta", "LagunaNord", "Misericordia", "Burano", "MalamoccoPorto", "ChioggiaPorto", "Fusina", "SanGiorgio"]
#lista codici stazioni presenti come colonne all'interno dei rispettivi csv (per la stazione DigaSudLido sono presenti 2 codici)
stazioni_codice = ["P. Salute", "Piattaforma CNR", ["D.S. Lido","Faro Diga Lido"], "D.N. Malamocco", "D.S.Chioggia", "Palazzo Cavalli", "Chioggia Vigo", "Laguna N.", "Misericordia", "Burano", "Malamocco Porto", "Chioggia Porto", "Fusina", "San Giorgio"]
#lista stringa stazioni necessaria per la parte grafica (pulsanti e titolo tabelle)
stazione_output = ["Punta Salute Canal Grande", "Piattaforma", "Diga Sud Lido e Faro", "Diga Nord Malamocco", "Diga Sud Chioggia", "Palazzo Cavalli", "Chioggia Citta'", "Laguna Nord", "Misericordia", "Burano", "Malamocco Porto", "Chioggia Porto", "Fusina", "San Giorgio"]
#matrice parametri stazione (in colonna avemo i parametri per ogni stazione)
stazioni = [stazioni_nome,stazioni_codice,stazione_output]

#lista codici parametri presenti nei file csv originari
parametri_codice=["Onda: Alt. max","Onda: Alt. sign.","D.Vento med. 10m", "L.Idrometrico", "Liv.Idrom. medio 1m", "Pioggia 5m", "Pressione", "Radiazione solare", "Temperatura", "Temp. Acqua", "Umidita'", "V.Vento max", "V.Vento med.10m"]
#lista dei parametri in formato comprensibile
parametri_output = ["Altezza massima onda", "Altezza significativa onda", "Direzione media vento", "Livello idrometrico", "Livello medio idrometrico", "Pioggia", "Pressione", "Radiazione solare", "Temperatura", "Temperatura Acqua", "Umidità", "Velocità max vento", "Velocità media vento"]
#lista parametri (analoga a lista stazioni)
parametri = [parametri_codice, parametri_output]

#oggi = date(2024,12,18)   #data per file csv scaricati in locale (da 2024-09-18 a 2024-12-18)
oggi = date.today()        #data per file csv scaricati dal sito di Venezia (ultimi 3 mesi)
inizio = oggi-relativedelta(months=3) # giorno iniziale del dataframe (avento come dati gli ultimi 3 mesi)

############################ GET DATA ######################################
#funzione per ottenere dataframe della stazione richiesta
def getData(stazione):
    #url = f"daticsv/Stazione_{stazione}.csv"   #percorso locale
    url = f"https://www.comune.venezia.it/sites/default/files/publicCPSM2/stazioni/trimestrale/Stazione_{stazione}.csv" #link dal sito di Venezia per i csv
    data = pl.read_csv(url) #lettura dati dal file csv della stazione
    riga = data.columns #variabili prima riga del file csv
    colonne = riga[0].split(";") #lista delle colonne del dataframe
    
    #creazione data set stazione
    data = (data.select(
                pl.col("*")
                .str.split(";")
                .list.to_struct(fields=colonne)
                .alias("combined_info"),
                pl.col("*").exclude(riga[0])            
            ).unnest("combined_info")
            .filter(pl.col("Data")>=f'{inizio} 00:00:00')
        )
    return data

#funzione per ottenere il dataframe completo di tutti i 14 csv 
def getDataFrame():
    data = getData(stazioni_nome[0]) #getData stazione_PuntaSalute_CanalGrande

    for i in stazioni_nome[1:]: #skip prima stazione per via del successivo join
        dataStazione = getData(i) #get data stazione
        data = data.join(dataStazione, on="Data", how="left") #join di volta in volta 
    return data

#variabile globale dataframe completo
data = getDataFrame()





########################### MAPPA ####################################
#funzione per la mappa(per creare un elenco dei parametri rilevati quando ci si muove sopra una stazione)
def lista_param(staz):
    params=[]
    colonne = data.columns
    staz = stazioni[1][stazioni[2].index(staz)]
    if isinstance(staz, list):#per  ["D.S. Lido","Faro Diga Lido"]
        for i in staz:
            for c in colonne:
                if c.startswith(i):
                    params.append(c.replace(i+" ", ""))
    else:
        for c in colonne:
            if c.startswith(staz):
                params.append(c.replace(staz+" ", ""))
    par=""
    for p in params:
        par+=(f"<li>{parametri[1][parametri[0].index(p)]}</li>")# stringa composta da un <li></li> per ogni paramtro
    return par





########################### GET COLONNE ####################################
#funzione che restituisce, per ogni parametro, una lista con i nomi di tutte le stazioni che lo rilevano
def getCol_param(data, param):
    colonne = []
    for p in param:#per ogni parametro
        p_col =[]
        for c in data.columns:#per ogni colonna
            if c.endswith(p):#se la colonna finisce col parametro p
                p_col.append(c)# allora aggiunge nella lista riferitasi al parametro il nome della colonna 
        colonne.append(p_col)
    return colonne #restituisce una matrice di dimensioni: parametri x stazioni 

#funzione che restituisce, per ogni stazione, una lista con i nomi di tutti i parametri rilevati (analoga a quella per i parametri)
def getCol_staz(data, staz):
    colonne = []
    for s in staz:
        s_col =["Data"]
        if isinstance(s, list):#necessaria per la stazione di DigaSudLido essendo una lista di diga e faro
            for i in s:
                for c in data.columns:
                    if c.startswith(i):#se la colonna inizia con il nome della stazione
                        s_col.append(c)
        else:
            for c in data.columns:
                if c.startswith(s):
                    s_col.append(c)
        colonne.append(s_col)
    return colonne #restituisce una matrice di dimensioni: parametri x stazioni





########################### GET DATAFRAME ####################################
#funzione che restituisce una lista di dataframe suddivisi in base ai parametri richiesti
def get_listaData_param(param, tempo):
    colonne = getCol_param(data, param)
    df_tot = []#lista che conterrà un dataframe per ogni parametro 
    for j in range(len(colonne)):
        df_list = []#lista che conterrà il dataframe di una stazione che lo rileva
        for i in colonne[j]:
            df = (data
                    .select(
                        pl.col("Data"),
                        pl.col(i).alias(i.replace(param[j], "")),
                    ).unpivot(#necessario per rendere i  dati tidy
                        index="Data",
                        value_name=param[j],
                        variable_name="Stazione"
                    ).with_columns(
                        pl.col("*").exclude("Data", "Stazione").cast(pl.Float64,strict=False),
                    )
                )
            if isinstance(tempo, tuple):#se è stato selezionato il tempo come periodo 
                df = df.filter((pl.col("Data") >=f'{tempo[0]} 00:00:00') & (pl.col("Data")<=f'{tempo[1]+ datetime.timedelta(days=1)} 00:00:00'))
            elif tempo:#se è stato selezionato il singolo giorno
                df = df.filter((pl.col("Data") >=f'{tempo} 00:00:00') & (pl.col("Data")<=f'{tempo+ datetime.timedelta(days=1)} 00:00:00'))
            #altrimenti selezione tutto senza filtro temporale
            df_list.append(df)
        df_tot.append(pl.concat(df_list))#concatenazione dei dataframe di tutte le stazioni che rilevano il parametro in questione
    return df_tot #restituisce una lista di dataframe: uno per ogni parametro

#funzione che restituisce una lista di dataframe suddivisi in base alle stazioni richieste (simile a quella per i parametri)
def get_listaData_staz(staz, tempo):
    colonne = getCol_staz(data, staz)
    df_tot=[]#lista che conterrà un dataframe per ogni stazione
    for j in range(len(colonne)):
        if isinstance(staz[j], list):#per  ["D.S. Lido","Faro Diga Lido"]
            expr = [pl.col("Data")]#espressione necessaria per il select
            for k in staz[j]:#per le 2 stazioni
                for i in colonne[j]:
                    if(i.startswith(k)):
                        expr += [pl.col(i).alias(i.replace(k+" ", ""))]
        else:
            expr = [pl.col(i).alias(i.replace(staz[j]+" ", "")) for i in colonne[j]]#espressione che consiste in un pl.col per ogni parametro della stazione

        df = (data.select(expr))
        if isinstance(tempo, tuple):#se selezionato periodo
            df = df.filter((pl.col("Data") >=f'{tempo[0]} 00:00:00') & (pl.col("Data")<=f'{tempo[1]+ datetime.timedelta(days=1)} 00:00:00'))
        elif tempo:#se selezionato singolo giorno
            df = df.filter((pl.col("Data") >=f'{tempo} 00:00:00') & (pl.col("Data")<=f'{tempo+ datetime.timedelta(days=1)} 00:00:00'))
        df_tot.append(df)#aggiunge alla lista df_tot il dataframe completo per la stazione selezionata

    return df_tot #restituisce una lista di dataframe: uno per stazione





########################### GET GRAFICI ####################################
#funzione che restituisce una lista di grafici (una per ogni stazione)
def get_listaGraf_staz(tabella):
    list_grafici=[]
    for i in tabella:#per ogni stazione
        grafici=[]#lista (vuota) di grafici per la stazione
        param = i.columns[1:]
        expr = ["Data"]
        for r in range(len(param)):
            expr.append(parametri[1][parametri[0].index(param[r])])
        i.columns = expr
        param = i.columns[1:]
        for parametro in param:#per ogni parametro della stazione
            #creazione del dataframe per la signola stazione e il signolo parametro
            tab= i.select(
                pl.col("Data"),
                pl.col(f"{parametro}"))

            ##################AGGREGAZIONE################
            #  (necessaria per il problema dei troppi record) avendo un grafico con piu di 200mila record,
            #  questa aggregazione (media di tot valori) diventa necessaria per alleggerire il grafico e permetterne il movimento
            lunghezza = len(tab)#numero di record

            count=0
            while (lunghezza>2000):#ripete finche il numero di record non è inferiore a 2000 per comodità di rappresentazione del grafico
                lunghezza = lunghezza/2
                count+=1

            df = pd.DataFrame(tab,columns=["Data", parametro])#conversione del dataframe in pandas.DataFrame

            df["group"] = np.floor(df.index / (2**count))#aggiunge una colonna al dataframe con il valore intero della divisione con 2* count
            #se count =4 (ovvero se il numero di record è superiore 40mila circa) crea una colonna con 2*4 valori con lo stesso indice 
            # (questo per poi aggragare ogni 16 valori)
            df[f"{parametro}"]=pd.to_numeric(df[f"{parametro}"], errors='coerce')

            tab = df.groupby('group').agg({
                'Data': 'last', #mantiene l'ultimo valore della data in quanto la media è stata fatto sui precendeti 2^count valori
                f'{parametro}': 'mean'  #media dei 2^count valori
            }).reset_index(drop=True)
            ###############

            #switch per il parametro e creazione del grafico
            match parametro:
                case "Altezza massima onda":
                    chart = (
                        alt.Chart(tab)
                        .mark_line()
                        .encode(
                            alt.X("Data:T"),
                            alt.Y(f"{parametro}:Q", title="metri"),
                        ).interactive().properties(title=f"{parametro}")
                    )
                case "Altezza significativa onda":
                    chart = (
                        alt.Chart(tab)
                        .mark_line()
                        .encode(
                            alt.X("Data:T"),
                            alt.Y(f"{parametro}:Q", title="metri"),
                        ).interactive().properties(title=f"{parametro}")
                    )
                case "Direzione media vento":
                    chart = (
                        alt.Chart(tab)
                        .mark_point()
                        .encode(
                            alt.X("Data:T"),
                            alt.Y(f"{parametro}:Q", title="gradi (da 0 a 360)"),
                        ).interactive().properties(title=f"{parametro}")
                    )
                case "Livello idrometrico":
                    chart = (
                        alt.Chart(tab)
                        .mark_area()
                        .encode(
                            alt.X("Data:T"),
                            alt.Y(f"{parametro}:Q", title="metri")
                        ).interactive().properties(title=f"{parametro}")
                    )
                case "Livello medio idrometrico":
                    chart = (
                        alt.Chart(tab)
                        .mark_area()
                        .encode(
                            alt.X("Data:T"),
                            alt.Y(f"{parametro}:Q", title="metri")
                        ).interactive().properties(title=f"{parametro}")
                    )
                case "Pioggia":
                    chart = (
                        alt.Chart(tab)
                        .mark_bar()
                        .encode(
                            alt.X("Data:T"),
                            alt.Y(f"{parametro}:Q",title="mm")
                        ).interactive().properties(title=f"{parametro}")
                    )
                case "Pressione":
                    chart = (
                            alt.Chart(tab)
                            .mark_line()
                            .encode(
                                alt.X("Data:T"),
                                alt.Y(f"{parametro}:Q", scale=alt.Scale(domain=[985, 1040]), title="hPa")
                            ).interactive().properties(title=f"{parametro}")
                        )
                case "Radiazione solare":
                    chart = (
                        alt.Chart(tab)
                        .mark_bar()
                        .encode(
                            alt.X("Data:T"),
                            alt.Y(f"{parametro}:Q", title="W/m2")
                        ).interactive().properties(title=f"{parametro}")
                    )
                case "Temperatura":
                    chart = (
                        alt.Chart(tab)
                        .mark_line()
                        .encode(
                            alt.X("Data:T"),
                            alt.Y(f"{parametro}:Q", title="°C")
                        ).interactive().properties(title=f"{parametro}")
                    )
                case "Temperatura Acqua":
                    chart = (
                        alt.Chart(tab)
                        .mark_line()
                        .encode(
                            alt.X("Data:T"),
                            alt.Y(f"{parametro}:Q", title="°C")
                        ).interactive().properties(title=f"{parametro}")
                    )
                case "Umidità":
                    chart = (
                        alt.Chart(tab)
                        .mark_line()
                        .encode(
                            alt.X("Data:T"),
                            alt.Y(f"{parametro}:Q", title="%")
                        ).interactive().properties(title=f"{parametro}")
                    )
                case "Velocità max vento":
                    chart = (
                        alt.Chart(tab)
                        .mark_line()
                        .encode(
                            alt.X("Data:T"),
                            alt.Y(f"{parametro}:Q", title="m/s")
                        ).interactive().properties(title=f"{parametro}")
                    )
                case "Velocità media vento":
                    chart = (
                        alt.Chart(tab)
                        .mark_line()
                        .encode(
                            alt.X("Data:T"),
                            alt.Y(f"{parametro}:Q", title="m/s")
                        ).interactive().properties(title=f"{parametro}")
                    )
                case _:
                    st.write("error")
            grafici.append(chart)   #aggiunta del grafico alla lista della stazione
        list_grafici.append(grafici) #aggiunta della lista dei grafici della stazione alla lista finale con tutte le stazioni
    return list_grafici

#funzione che restituisce una lista di grafici (una per ogni parametro)
def get_listaGraf_param(tabella, param):
    grafici = []
    for i in range(len(tabella)):#per ogni parametro
        tabella[i].columns = "Data", "Stazione", param[i] #colonne necessarie per il dataframe
        parametro = tabella[i].columns[2] #parametro_output necessario per grafico

        #AGGREGAZIONE
        df = pd.DataFrame(tabella[i],columns=["Data", "Stazione", param[i]])

        stazi =df["Stazione"].unique()#elenco di stazioni che rilevalo il parametro d'interesse

        indice = np.vectorize(lambda x: np.where(stazi == x)[0][0])#crea un vettore della lunghezza dei record per stazione (0 per la prima, 1 per la seconda...)
        
        risultato = indice(df["Stazione"])
        
        zeri = np.full(len(df), "000")#aggiunge 000 per permettere l'aggregazione senza unire i valori di diverse stazioni tra di loro

        #ripete finche il numero di record per stazione non è inferiore a 2000
        recXstaz = len(df)/len(stazi)
        count=0
        while (recXstaz>2000):
            recXstaz = recXstaz/2
            count+=1
        
        if parametro=="Livello idrometrico":count+=2#necessario per una migliore comprensione del grafico del Livello Idrometrico

        #concatena (risultato + 000 + indice uguale per 2^count valori)
        prova= np.char.add(risultato.astype(str),zeri)
        prova2 = np.char.add(prova , (np.floor(df.index / (2**count))).astype(str))
        
        df['group'] = prova2#aggiunge al dataframe la colonna group per una successiva aggregazione

        result = df.groupby('group').agg({#aggrega
            'Data': 'last',             #mantiene l'ultimo valore della data
            'Stazione': 'first',        #mantiene il primo valore della stazione ma in realtà sono tutti uguali
            f'{parametro}': 'mean'      #media dei valori del parametro
        }).reset_index(drop=True)

        #creazione grafici
        match parametro:
            case "Altezza massima onda":
                chart = (
                    alt.Chart(result)
                    .mark_line()
                    .encode(
                        alt.X("Data:T"),
                        alt.Y(f"{parametro}:Q".replace(f"{parametro}",param[i]), title="metri"),
                        alt.Color("Stazione:N")
                    ).interactive()
                )
            case "Altezza significativa onda":
                chart = (
                    alt.Chart(result)
                    .mark_line()
                    .encode(
                        alt.X("Data:T"),
                        alt.Y(f"{parametro}:Q".replace(f"{parametro}",param[i]), title="metri"),
                        alt.Color("Stazione:N")
                    ).interactive()
                )
            case "Direzione media vento":#grafico non chiaro e (per me) difficile da rappresentare in quanto i valori con in gradi (0 - 360)
                chart = (
                    alt.Chart(result)
                    .mark_point()
                    .encode(
                        alt.X("Data:T"),
                        alt.Y(f"{parametro}:Q".replace(f"{parametro}",param[i]), title="gradi (da 0 a 360)"),
                        alt.Color("Stazione:N"),
                        row=alt.Row("Stazione:N", title=None)#divide il grafico in righe: una per ogni stazione (per rendere il grafico leggibile)
                        #anche se rende le differenze tra le stazioni meno percettibili (RIPETUTO SU VARI GRAFICI CON TANTE STAZIONI)
                    ).interactive(
                    ).properties(height=100, width=400)
                )
            case "Livello idrometrico":
                chart = (
                    alt.Chart(result)
                    .mark_line()
                    .encode(
                        alt.X("Data:T"),
                        alt.Y(f"{parametro}:Q".replace(f"{parametro}",param[i]), title="metri"),
                        alt.Color("Stazione:N"),
                    ).interactive()
                )
            case "Livello medio idrometrico":
                chart = (
                    alt.Chart(result)
                    .mark_area()
                    .encode(
                        alt.X("Data:T"),
                        alt.Y(f"{parametro}:Q".replace(f"{parametro}",param[i]), title="metri"),
                        alt.Color("Stazione:N"),
                        row=alt.Row("Stazione:N", title=None)
                    ).interactive(
                    ).properties(height=100, width=400)
                )
            case "Pioggia":
                chart = (
                    alt.Chart(result)
                    .mark_bar()
                    .encode(
                        alt.X("Data:T"),
                        alt.Y(f"{parametro}:Q".replace(f"{parametro}",param[i]),title="mm"),
                        alt.Color("Stazione:N"),
                        row=alt.Row("Stazione:N", title=None)
                    ).interactive(
                    ).properties(height=400, width=400)
                )
            case "Pressione":
                chart = (
                        alt.Chart(result)
                        .mark_line()
                        .encode(
                            alt.X("Data:T"),
                            alt.Y(f"{parametro}:Q".replace(f"{parametro}",param[i]), scale=alt.Scale(domain=[985, 1040]), title="hPa"),
                            alt.Color("Stazione:N")
                        ).interactive()
                    )
            case "Radiazione solare":# sarebbe stato più comprensibile un mark_rect
                chart = (
                    alt.Chart(result)
                    .mark_bar()
                    .encode(
                        alt.X("Data:T"),
                        alt.Y(f"{parametro}:Q".replace(f"{parametro}",param[i]), title="W/m2"),
                        alt.Color("Stazione:N"),
                        row=alt.Row("Stazione:N", title=None)
                    ).interactive(
                    ).properties(height=400, width=400)
                )
            case "Temperatura":
                chart = (
                    alt.Chart(result)
                    .mark_line()
                    .encode(
                        alt.X("Data:T"),
                        alt.Y(f"{parametro}:Q".replace(f"{parametro}",param[i]), title="°C"),
                        alt.Color("Stazione:N")
                    ).interactive()
                )
            case "Temperatura Acqua":
                chart = (
                    alt.Chart(result)
                    .mark_line()
                    .encode(
                        alt.X("Data:T"),
                        alt.Y(f"{parametro}:Q".replace(f"{parametro}",param[i]), title="°C"),
                        alt.Color("Stazione:N")
                    ).interactive()
                )
            case "Umidità":
                chart = (
                    alt.Chart(result)
                    .mark_line()
                    .encode(
                        alt.X("Data:T"),
                        alt.Y(f"{parametro}:Q".replace(f"{parametro}",param[i]), title="%"),
                        alt.Color("Stazione:N")
                    ).interactive()
                )
            case "Velocità max vento":
                chart = (
                    alt.Chart(result)
                    .mark_line()
                    .encode(
                        alt.X("Data:T"),
                        alt.Y(f"{parametro}:Q".replace(f"{parametro}",param[i]), title="m/s"),
                        alt.Color("Stazione:N"),
                        row=alt.Row("Stazione:N", title=None)
                    ).interactive(
                    ).properties(height=100, width=400)
                )
            case "Velocità media vento":
                chart = (
                    alt.Chart(result)
                    .mark_line()
                    .encode(
                        alt.X("Data:T"),
                        alt.Y(f"{parametro}:Q".replace(f"{parametro}",param[i]), title="m/s"),
                        alt.Color("Stazione:N"),
                        row=alt.Row("Stazione:N", title=None)
                    ).interactive(
                    ).properties(height=100, width=400)
                )
            case _:
                st.write("error")
        grafici.append(chart)#aggiunge grafico
    return grafici