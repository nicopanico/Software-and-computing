# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 19:24:54 2022

@author: iacop
"""
##importing packages used in the script
import os,sys

os.chdir('C:\Desktop\software_computing\Software-and-computing')

sys.path.append(os.path.dirname(os.path.realpath(__file__))) #to take the working dir as the curretn script directory


import pandas as pd


# get_ipython().system('{sys.executable} -m pip install lifelines')
#import functions and clases
import my_functions as ff
from Classes_for_user.sett_hosp import hospital as hosp
from Classes_for_user.sett_hosp import SettingList as settlist
from Classes_for_user.names import key_words as key
from Classes_for_user.patology import patologies as pat
from Classes_for_user.init_data import covid_data as data

def create_tracking_pos_dataset():
    """
    function to create the dataset to use to create the various contingencies, dataset that tracks all the positives ID for bologna
    Inputs:
        Imported datasets from the class init_data
    Output:
        desired dataset containing one columns for ID, one columns for the patology, one column for setting
    """
    dataset_patologies=data.patologies[[key.descrizione_esenzione,key.ID]]
    dataset_bolo_patologies=pd.merge(data.ID_Bologna,dataset_patologies, how='left', on=[key.ID])
    dataset_bolo_patologies=dataset_bolo_patologies.fillna('NaN')
    dataset_bolo_patologies=dataset_bolo_patologies.groupby([key.ID]).agg({key.descrizione_esenzione:','.join})
    dataset_setting=data.analysis_entries_updated[[key.setting,key.ID]]
    dataset_bolo_setting=pd.merge(data.ID_Bologna,dataset_setting, how='left', on=[key.ID])
    dataset_bolo_setting=dataset_bolo_setting.fillna('NaN')
    dataset_tracking_bologna=pd.merge(dataset_bolo_patologies,dataset_bolo_setting, how='left',on=[key.ID])
    
    iscovidnow=ff.create_target_ID_list(data.positivi_unibo,key.malattia,key.esito)
    
    database_pos_outcome=data.positivi_unibo.drop(iscovidnow)#drop patients who still have covid
    database_pos_outcome.drop_duplicates(subset=[key.ID], inplace=True)#and remove the duplciates ID
    ID_positives=database_pos_outcome[key.ID] 

    dataset_tracking_bologna_positives=pd.merge(dataset_tracking_bologna,ID_positives, how='inner', on=[key.ID])
    return(dataset_tracking_bologna_positives)
    





sex_bolo=data.anag_comune_bo[[key.sesso,key.ID]]



# # Check on the database 'casi covid unibo' to make sure everything is matching in the database

# Removing the people that still have covid at the moment
#since the analysis is performed over the patients who have a complete track (start and end)


#dataset matching


iscovidnow=ff.create_target_ID_list(data.positivi_unibo,key.malattia,key.esito)
database_pos_outcome=data.positivi_unibo.drop(iscovidnow)#drop patients who still have covid
database_pos_outcome.drop_duplicates(subset=[key.ID], inplace=True)#and remove the duplciates ID

#taking the IDs of positive patients
ID_positives=database_pos_outcome[key.ID]  
"""
Now merge the IDs of the positive patients with the people in covid hopsital settings
to see how many positive patients got hospitalized
"""  
database_entries_bo=pd.merge(data.ID_Bologna,data.analysis_entries_updated[[key.setting,key.ID,key.deceduto]], 
                             how='left', on=[key.ID])

#define the sub-dataset containing the entries for all the covid settings
database_entries_bo_covid=database_entries_bo[database_entries_bo.SETTING.isin([hosp.intensiva_covid,
                                                                                hosp.degenza_ordinaria_covid,
                                                                                hosp.sub_intensiva_covid,
                                                                                hosp.degenza_covid_bassa_intesita])]
#database for all the patients that have covid and are in covid settings
database_entries_bo_covid_positives=pd.merge(database_entries_bo_covid,ID_positives,how='inner',on=[key.ID])
 


# Checking the number of positives deceased and comparing it with the patients deceased in covid departments
#create the database containing the ID of all the positives also the non-hospitalized ones
database_pos_bolo=pd.merge(database_pos_outcome,data.ID_Bologna,how='inner',on=[key.ID])
database_pos_bolo=database_pos_bolo.drop_duplicates(subset=[key.ID])

isPosDeceased=ff.create_target_ID_list(database_pos_bolo,key.decesso,key.esito)
print('number of positives deceased for bologna IDs:',len(isPosDeceased))

isCovDeceased=ff.deceased_list(database_entries_bo_covid)


# Checking if the total number of hopistalized in covid departments are positves
print('number of positive patients hospitalized in covid setting:', len(database_entries_bo_covid_positives.index),'\n',
      'total number of patients hospitalized in covid setting:',len(database_entries_bo_covid.index))


# Getting the datasets of 'SETTING' and 'Descrizione_Esenzione' per ID
dataset_setting=data.analysis_entries_updated[[key.setting,key.ID]]
dataset_patologies=data.patologies[[key.descrizione_esenzione,key.ID]]
dataset_patologies_per_setting=pd.merge(dataset_setting, dataset_patologies, how='left',on=[key.ID])

#narrowing down the analysis to just Bologna ID_PER
dataset_bolo_setting=pd.merge(data.ID_Bologna,dataset_setting, how='left', on=[key.ID])
dataset_bolo_setting=dataset_bolo_setting.fillna('NaN')
dataset_bolo_patologies=pd.merge(data.ID_Bologna,dataset_patologies, how='left', on=[key.ID])
dataset_bolo_patologies=dataset_bolo_patologies.fillna('NaN')


# Modelling the database to have the complete description of the setting and patology for each Bologna ID




dataset_bolo_patologies=dataset_bolo_patologies.groupby([key.ID]).agg({key.descrizione_esenzione:','.join})
dataset_bolo_setting=dataset_bolo_setting.groupby([key.ID]).agg({key.setting:','.join})
dataset_tracking_bologna=pd.merge(dataset_bolo_patologies,dataset_bolo_setting, how='left',on=[key.ID])
dataset_tracking_bologna_positives=pd.merge(dataset_tracking_bologna,ID_positives, how='inner', on=[key.ID])


# # Contingency tables of positive Bologna IDs
"""
Create contingency tables in order to see if there is some correlation between the covid intensive care hospitalized and 
the patologies:
    the list of patologies to test was given a priori, out of all the patologie sin the dataset only 6 were chosen 
"""
def setting_lists():
    """
    define the settings lists from the classes
    """
    list_cov_setting = settlist.covid_setting
    list_setting_nocov=settlist.nocovid_setting #list from the dataclass to take the list of
    #all the non covid settings
    list_setting_cov_noint=(settlist.covid_setting)
    list_setting_cov_noint=list_setting_cov_noint.remove(hosp.intensiva_covid)
    
    return(list_cov_setting,list_setting_nocov,list_setting_cov_noint)

def create_list_multiple_sett(df,target_list):
    """
    create a lsit containin the ID of patients that are in the list of settings
    Inputs:
        df==dataset where to take patients
        target_list==list of setting to check
    Output:
        complete list of all the patients that are in that setting
    """

    
    isPosnotcovint=[]
    for i in range(0, len(target_list)):
        list_pat=ff.create_target_ID_list(dataset_tracking_bologna_positives,target_list[i],key.setting)
        isPosnotcovint=list(set().union(list_pat,isPosnotcovint))
    return(isPosnotcovint)
    


def contingency_datasets(df,settlist,sub_list=[]):
    """
    create the dataset for the contingency tables
    Inputs:
        df==dataset where to take patients
        settlist==list of setting to check
        sub_list=list of settings to exlude in case a patient has been hospitalized in multiple settings
    Output:
        dataset_final==dataset containing the patients for that settings
    """

    isPosnotcovint=create_list_multiple_sett(df,settlist)
    if not sub_list:
        dataset_final=df[df.index.isin(isPosnotcovint)]
    else:
        isPosInt=create_list_multiple_sett(df, sub_list)
        #now remove the patients that have been hospitalized also in setting unwanted
        isPosnotcovint=ff.common_elements(isPosnotcovint,isPosInt)
        #also obtain a dataset with intensive care patients but not the other covid settings, that will be usefull for the cntingency tables
        dataset_final=df[df.index.isin(isPosnotcovint)]
    return(dataset_final)




