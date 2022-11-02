# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 19:48:27 2022

@author: iacop
"""


import pandas as pd
from Classes_for_user import names

class covid_data:
    anag_comune_bo=pd.read_csv('./Data_set/ANAGCOMUNEBO.csv')
    positivi_unibo=pd.read_csv('./Data_set/Casi_covid_unibo_2021-11-22.csv',';')
    positivi_unibo[names.names.accettazione]=pd.to_datetime(positivi_unibo[names.names.accettazione])
    positivi_unibo[names.names.esito]=pd.to_datetime(positivi_unibo[names.names.esito])
    analysis_entries_updated=pd.read_csv('./Data_set/ANALISI_ENTRATE_2021_10_13.csv',';')
    analysis_entries_updated[names.names.inizio]=pd.to_datetime(analysis_entries_updated[names.names.inizio])
    analysis_entries_updated=analysis_entries_updated.fillna(0)
    analisi_uscite_updated=pd.read_csv('./Data_set/ANALISI_USCITE_2021_10_13.csv',';')
    analisi_uscite_updated[names.names.inizio]=pd.to_datetime(analisi_uscite_updated[names.names.inizio])
    analisi_uscite_updated[names.names.fine]=pd.to_datetime(analisi_uscite_updated[names.names.fine])
    patologies=pd.read_csv('./Data_set/Patologie.csv',';')
    ID_Bologna=anag_comune_bo[names.names.ID]#all the ID of Bologna