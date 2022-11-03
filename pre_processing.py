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
    

# # Contingency tables of positive Bologna IDs

def setting_lists():
    """
    define the settings lists from the classes
    """
    list_cov_setting = settlist.covid_setting
    list_setting_nocov=settlist.nocovid_setting #list from the dataclass to take the list of
    #all the non covid settings
    list_setting_cov_noint=(settlist.covid_setting_no_int)
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
    if type(target_list)==str:
        target_list=[target_list]
    
    isPosnotcovint=[]
    for i in range(0, len(target_list)):
        list_pat=ff.create_target_ID_list(df,target_list[i],key.setting)
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
    if type(settlist)==str:
      settlist=[settlist]  
      
    settlist_complete=settlist
    settlist_complete.append('NaN')#to consider the non hospitalized ones
    isPosnotcovint=create_list_multiple_sett(df,settlist_complete)
    if not sub_list:
        dataset_final=df[df.index.isin(isPosnotcovint)]
    else:
        isPosInt=create_list_multiple_sett(df, sub_list)
        #now remove the patients that have been hospitalized also in setting unwanted
        isPosnotcovint=ff.common_elements(isPosnotcovint,isPosInt)
        #also obtain a dataset with intensive care patients but not the other covid settings, that will be usefull for the cntingency tables
        dataset_final=df[df.index.isin(isPosnotcovint)]
    settlist.remove('NaN')
    return(dataset_final)




