# -*- coding: utf-8 -*-

from dataclasses import dataclass

"""
Dataclass to define all the names used for the dataset columns
@Nicola2022

"""
@dataclass(frozen=True)
class key_words:
    #dataframe columns names
    inizio="DATA_INIZIO"
    fine="DATA_FINE"
    data_esito="DATA_ESITO"
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


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
 