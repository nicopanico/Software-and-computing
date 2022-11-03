# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 16:36:11 2022

@author: nicop
"""
from dataclasses import dataclass

"""
Dataclass to define all the names used for the dataset columns

"""
@dataclass(frozen=True)
class key_words:
    #dataframe columns names
    inizio="DATA_INIZIO"
    fine="DATA_FINE"
    esito="DATA_ESITO"
    accettazione="DATA_ACCETTAZIONE"
    ID="ID_PER"
    setting="SETTING"
    deceduto="DECEDUTO"
    sesso="PER_KEY_SESSO"
    malattia="MALATTIA_IN_CORSO"
    descrizione_esenzione="Descrizione_Esenzione"
    id_ricovero = "ID_RICOVERO"
    #words inside the dataset columns as values
    decesso='DECESSO'
    esito="ESITO"


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
 