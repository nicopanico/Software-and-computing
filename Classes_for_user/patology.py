# -*- coding: utf-8 -*-
"""
Created on Sat Oct 15 19:43:30 2022

@author: nicop
"""
from dataclasses import dataclass
@dataclass(frozen=True)
class patologies:
    patlist=['DIABETE MELLITO-DIABETE MELLITO','IPERTENSIONE ESSENZIALE',
            'EMBOLIA E TROMBOSI DI ALTRE VENE (ESCLUSO SINDROME DI BUDD-CHIARI)',
          'SOGGETTI AFFETTI DA PATOLOGIE NEOPLASTICHE MALIGNE - SOGGETTI AFFETTI DA PATOLOGIE NEOPLASTICHE MALIGNE',
           'ARITMIE CARDIACHE','CARDIOPATIA IPERTENSIVA']
    
    