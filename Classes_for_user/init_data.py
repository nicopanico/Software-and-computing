# -*- coding: utf-8 -*-


import pandas as pd
from Classes_for_user.names import key_words as key


class covid_data:
    anag_comune_bo=pd.read_csv('./Data_set/ANAGCOMUNEBO.csv')
    positivi_unibo=pd.read_csv('./Data_set/Casi_covid_unibo_2021-11-22.csv',';')
    positivi_unibo[key.accettazione]=pd.to_datetime(positivi_unibo[key.accettazione])
    positivi_unibo[key.data_esito]=pd.to_datetime(positivi_unibo[key.data_esito])
    analysis_entries_updated=pd.read_csv('./Data_set/ANALISI_ENTRATE_2021_10_13.csv',';')
    analysis_entries_updated[key.inizio]=pd.to_datetime(analysis_entries_updated[key.inizio])
    analysis_entries_updated=analysis_entries_updated.fillna(0)
    analisi_uscite_updated=pd.read_csv('./Data_set/ANALISI_USCITE_2021_10_13.csv',';')
    analisi_uscite_updated[key.inizio]=pd.to_datetime(analisi_uscite_updated[key.inizio])
    analisi_uscite_updated[key.fine]=pd.to_datetime(analisi_uscite_updated[key.fine])
    patologies=pd.read_csv('./Data_set/Patologie.csv',';')
    ID_Bologna=anag_comune_bo[key.ID]#all the ID of Bologna