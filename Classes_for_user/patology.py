# -*- coding: utf-8 -*-

from dataclasses import dataclass
"""
Dataclass with all the patologies used for the study, the set of aptologies was chosen a priori and was fixed
@Nicola2022
"""
@dataclass(frozen=True)
class patologies:
    patlist=['DIABETE MELLITO-DIABETE MELLITO','IPERTENSIONE ESSENZIALE',
            'EMBOLIA E TROMBOSI DI ALTRE VENE (ESCLUSO SINDROME DI BUDD-CHIARI)',
          'SOGGETTI AFFETTI DA PATOLOGIE NEOPLASTICHE MALIGNE - SOGGETTI AFFETTI DA PATOLOGIE NEOPLASTICHE MALIGNE',
           'ARITMIE CARDIACHE','CARDIOPATIA IPERTENSIVA']
    
    