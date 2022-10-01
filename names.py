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
class names:
    inizio="DATA INIZIO"
    fine="DATA FINE"
    esito="DATA ESITO"
    accettazione="DATA ACCETTAZIONE"
    ID="ID PER"
    setting="SETTING"
    deceduto="DECEDUTO"
    sesso="PER KEY SESSO"
    malattia="MALATTIA IN CORSO"
    esito="ESITO"
    descrizione_esenzione="Descrizione esenzione"
    
    
    
    
    
    
    
    
    
    
    
    
    
    
 