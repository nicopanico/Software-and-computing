# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 17:25:31 2022

@author: nicop
"""

from dataclasses import dataclass
"""
Dataclass defining all the setting(hospital departments) in the datasets, for the patients
dividing them between covid and non-covid
"""


@dataclass(frozen=True)
class settings:
    #NORMAL SETTINGS
    degenza_generale_noCov="DEGENZA MED GENERALE NO COVID"
    degenza_chir_spec_noCov="DEGENZA CHIR SPECIALISTICA NO COVID"
    degenza_med_spec_noCov="DEGENZA MED SPECIALISTICA NO COVID"
    altro="ALTRO"
    degenza_chir_generale_noCov="DEGENZA CHIR GENERALE NO COVID"
    terapia_int_noCov="TERAPIA INTENSIVA NO COVID"
    sub_int_noCov="SUB INTENSIVA NO COVID"
    emergenza_urgenza="EMERGENZA-URGENZA"
    sospetti_covid="SOSPETTI COVID"
    ortopedia="ORTOPEDIA"
    #COVID SETTINGS
    degenza_ordinaria_covid="DEGENZA ORDINARIA COVID"
    sub_intensiva_covid="SUB INTENSIVA COVID"
    degenza_covid_bassa_intesita="DEGENZA COVID BASSA INTENSITA"
    intensiva_covid="TERAPIA INTENSIVA COVID"
    
    
    
    
    
                                 
        
                         