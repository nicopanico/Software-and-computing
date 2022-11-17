# -*- coding: utf-8 -*-


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




#------------------------------------------------------------------------------
#PRE PROCESSING OF THE DATA FOR CONTINGENCIES

def create_data_patologies(df_pat, df_ID):
    """
    Fucntion to create the dataset with the tracking of the patologies
    Input: 
        df_pat==data of the patologies
        df_ID==data with the ID of the patients
    Output:
        dataset_bolo_patologies==df containing the patologies for pat. ID  
    @Nicola2022
    """
    dataset_patologies=df_pat[[key.descrizione_esenzione,key.ID]]
    dataset_bolo_patologies=pd.merge(df_ID,dataset_patologies, how='left', on=[key.ID])
    dataset_bolo_patologies=dataset_bolo_patologies.fillna('NaN') #fill the NaN with the string NaN
    dataset_bolo_patologies=dataset_bolo_patologies.groupby([key.ID]).agg({key.descrizione_esenzione:','.join}) #group per ID the dataset
    return(dataset_bolo_patologies)

def create_data_settings(df_entries,df_ID):
    """
    Fucntion to create the dataset with the tracking of the settings
    Inputs: 
        df_entries==data of the hospital entry for all the patients
        df_ID==data with the ID of the patients
    Output:
        dataset_bolo_setting==df containing the settings for pat. ID (even if they were not hospitalized they will have a NaN)  
    @Nicola2022
    """
    dataset_setting=df_entries[[key.setting,key.ID]]
    dataset_bolo_setting=pd.merge(df_ID,dataset_setting, how='left', on=[key.ID])
    dataset_bolo_setting=dataset_bolo_setting.fillna('NaN')
    return(dataset_bolo_setting)

def create_pos_outcome(df_pos):
    """
    fucntion to create the tracking fo the positive pat. IDs
    Input: 
        df_pos==data of the positives 
    Output:
        database_pos_outcome==df with the positive patients
    @Nicola2022
    """
    iscovidnow=ff.create_target_ID_list(df_pos,[key.malattia],key.esito)
    database_pos_outcome=df_pos.drop(iscovidnow)#drop patients who still have covid
    database_pos_outcome.drop_duplicates(subset=[key.ID], inplace=True)#and remove the duplciates ID
    return (database_pos_outcome)
    
def create_tracking_pos_dataset(df_bolo_pat,df_bolo_sett,df_pos_outcome):
    """
    function to have the final dataset keep track of all the positive patients of Bologna
    Input:
        df_bolo_pat==df witht the patologies for patients
        df_bolo_sett==df with settings for patients
        df_pos_outcome==df with the positive patients with their settings and patologies
    Output:
        dataset_tracking_bologna_positives==dataset with complòete tracking of all the patologies and hospitalization for the positives
    @Nicola2022
    """
    dataset_tracking_bologna=pd.merge(df_bolo_pat,df_bolo_sett, how='left',on=[key.ID])
    ID_positives=df_pos_outcome[key.ID] 
    dataset_tracking_bologna_positives=pd.merge(dataset_tracking_bologna,ID_positives, how='inner', on=[key.ID])
    return(dataset_tracking_bologna_positives)
    
#------------------------------------------------------------------------------
##PRE PROCESSING FOR KM



def create_dataset_exit(df_out,df_ID,df_exit):
    """
    Function to create the dataset for the hospital path of bologna positives patients based on the key=ID_PER
    Inputs:
        df_out==df of the positive patients
        df_ID== df of the IDs of Bologna
        df_exit== df of the hospital exit containing IDs, settings, dates of entry and exit, esito
    Output:
        dataset_bolo_hospital_path_pos==df containign all the hospital path of the positive patients with their IDs, settings
        dates and if they are recovered or deceased
    @Nicola2022
    """
    ID_positives=df_out[key.ID] 
    dataset_bolo_exit=pd.merge(df_ID,df_exit,how='inner',on=[key.ID])#dataset with the hospital exits merged with the ID of the patients 
    dataset_bolo_exit_pos=pd.merge(ID_positives,dataset_bolo_exit,how='inner', on=[key.ID])#limiting the dataset to only positive patients
    
    #creating the 2 main datasets for the analysis
    return(dataset_bolo_exit_pos)

def create_dataset_hospital_path(df_pos_exit,df_entry):
    """
    function to create a dataset that keeps track of all the positive patients hospitalized 
    mixing the dataset of hospital entry and the the dataset of hospitale exit
    Inputs:
        df_pos_exit==df with the positive patients and their path in the hopsital taken from the dataset analisi_uscite
        df_entry== df containing the hospital path of the entry for patients
    Outputs:
        dataset_bolo_hospital_path_pos== df with complete hospital path from entry to exit with settings, aptologies, dates
    @Nicola2022
    """
    dataset_bolo_hospital_path_pos=pd.merge(df_pos_exit,df_entry,how='inner',on=[key.ID,key.setting,key.id_ricovero,key.inizio])#do the merge with the dataset of the hospital entries
    return(dataset_bolo_hospital_path_pos)

def create_dataset_KM(df_path,df_out):
    """
    Function to create the pre-processed dataset that will be used in the KM analysis
    this is a normal merge, the real check of the function is made on those patients who have the DATA_ACCETTAZIONE>DATA_FINE
    which means patients that went out the hopsital before entering, those patients got eliminated (due to impossibilities on tracking them well)
    Inputs:
        df_path==df with the hospital path of patients
        df_out== df with the positive patients and their resume
    Output:
        df_pos_rec_KM==final dataset with corrected patients with a CLEAR hospital path
    @Nicola2022
    """
    ff.correct_dates(df_path,key.fine,'MESE_x') #first correct dates end
    ff.correct_dates(df_path,key.inizio,'MESE_y') #first correct dates start

    
    df_pos_rec=pd.merge(df_path[['ID_PER','SETTING','DATA_INIZIO','DATA_FINE','ID_RICOVERO','DURATA_GG','ETA_x']],
                        df_out[['ID_PER','DATA_ESITO','DATA_ACCETTAZIONE']],how='left', on=['ID_PER'])
 
    DateAcc=df_pos_rec['DATA_ACCETTAZIONE']
    DateEnd=df_pos_rec['DATA_FINE']
    DiffDateBool=DateAcc>DateEnd
    #rename the column ETA_x as simply ETA to define the age of the patients
    df_pos_rec_KM=df_pos_rec[~DiffDateBool]
    df_pos_rec_KM=df_pos_rec_KM.rename(columns={"ETA_x":"ETA" })
    return(df_pos_rec_KM)


def create_df_sex(df_anag):
    """
    fucntion to create the list of all the ppl of Bologna with their sex (M or F)
    Inputs:
        df_anag==df with anagrafic infos
    Output:
        sex_bolo==list with all the informations relative to the sex of IDs
    @Nicola2022
    """
    sex_bolo=data.anag_comune_bo[[key.sesso,key.ID]]
    return(sex_bolo)

def create_intensive_ID_list(df_path):
    """
    Function to get the list of ID patients who were in covid intensive care
    Inputs:
        df_path==df of the path of the patients inside the hospital
    Output:
        ID_list==list of all the patient IDs who were in covid intensive care
    @Nicola2022
    """
    #starting time= time of starting positivity
    #finale time= entry in intensive care covid or hospital exit
    # Restricting the analysis to all the hospitalized patients who had covid ongoing
    isIntCovid=df_path['SETTING'].isin(['TERAPIA INTENSIVA COVID'])
    df_int_covid=df_path[isIntCovid]
    ID_list=list(df_int_covid['ID_PER'])
    return(ID_list)


#------------------------------------------------------------------------------

# # CONTINGENCY TABLES DATASETS

def setting_lists():
    """
    define the settings lists from the classes
    @Nicola2022
    """
    list_cov_setting = settlist.covid_setting
    list_setting_nocov=settlist.nocovid_setting #list from the dataclass to take the list of
    #all the non covid settings
    list_setting_cov_noint=(settlist.covid_setting_no_int)
    return(list_cov_setting,list_setting_nocov,list_setting_cov_noint)


def contingency_datasets(df,settlist,sub_list=[]):
    """
    create the dataset for the contingency tables
    Inputs:
        df==dataset where to take patients
        settlist==list of setting to check
        sub_list=list of settings to exlude in case a patient has been hospitalized in multiple settings
    Output:
        dataset_final==dataset containing the patients for that settings
    @Nicola2022
    """
    if type(settlist)==str:
      settlist=[settlist]  
   
   
    settlist_complete=settlist
    settlist_complete.append('NaN')#to consider the non hospitalized ones
    isPosnotcovint=ff.create_target_ID_list(df,settlist_complete,key.setting)
    if not sub_list:
        dataset_final=df[df.index.isin(isPosnotcovint)]
        
    isPosInt=ff.create_target_ID_list(df,sub_list,key.setting)
    #now remove the patients that have been hospitalized also in setting unwanted
    isPosnotcovint=ff.common_elements(isPosnotcovint,isPosInt)
    #also obtain a dataset with intensive care patients but not the other covid settings, that will be usefull for the cntingency tables
    dataset_final=df[df.index.isin(isPosnotcovint)]
    settlist.remove('NaN')
    return(dataset_final)




