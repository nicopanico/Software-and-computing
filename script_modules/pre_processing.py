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

def create_tracking_pos_dataset():
    """
    function to create the dataset to use to create the various contingencies, dataset that tracks all the positives ID for bologna
    Inputs:
        Imported datasets from the class init_data
    Output:
        desired dataset containing one columns for ID, one columns for the patology, one column for setting
    @Nicola2022
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
    

##PRE PROCESSING FOR KM

def pre_processing_KM():
    
    """
    This fucntions takes the imported data and do some merges and clearing of the data to have them ready for the analisys
    as inputs it takes the original data from the ini_data class
    the final result will be a dataframe, result of some merges and filtering (using already tested fucntions in my_fucntions)
    and a list of ID as --> list_ID
    @Nicola2022
    """

   
    #some pre processing with the imported data
    iscovidnow=ff.create_target_ID_list(data.positivi_unibo,key.malattia,key.esito)
    database_pos_outcome=data.positivi_unibo.drop(iscovidnow)
    database_pos_outcome.drop_duplicates(subset=[key.ID], inplace=True)
    ID_positives=database_pos_outcome[key.ID] 
    sex_bolo=data.anag_comune_bo[[key.sesso,key.ID]]
    
    database_pos_KM=data.positivi_unibo.drop(iscovidnow)
    database_pos_KM=pd.merge(database_pos_KM,data.ID_Bologna,how='inner',on=[key.ID])
    
     
    database_pos_KM=data.positivi_unibo.drop(iscovidnow) #remove patients with on going covid using list created at line 63
    dataset_bolo_exit=pd.merge(data.ID_Bologna,data.analisi_uscite_updated,how='inner',on=[key.ID])#dataset with the hospital exits merged with the ID of the patients 
    dataset_bolo_exit_pos=pd.merge(ID_positives,dataset_bolo_exit,how='inner', on=[key.ID])#limiting the dataset to only positive patients
    
    #creating the 2 main datasets for the analysis
    dataset_bolo_hospital_path_pos=pd.merge(dataset_bolo_exit_pos,data.analysis_entries_updated,how='inner',on=[key.ID,key.setting,key.id_ricovero,key.inizio])#do the merge with the dataset of the hospital entries
    database_pos_KM=pd.merge(database_pos_KM,data.ID_Bologna,how='inner',on=[key.ID])
    
    #the dates need to be corrected bcs some of them are bad written, not standard format
    dataset_bolo_hospital_path_pos=ff.correct_dates(dataset_bolo_hospital_path_pos)
    
    dates=[]
    df_pos_rec=pd.merge(dataset_bolo_hospital_path_pos[['ID_PER','SETTING','DATA_INIZIO','DATA_FINE','ID_RICOVERO','DURATA_GG','ETA_x']],database_pos_KM[['ID_PER','DATA_ESITO','DATA_ACCETTAZIONE']],how='left', on=['ID_PER'])
    for i in range(0, len(df_pos_rec.index)):
        if df_pos_rec.DATA_ACCETTAZIONE.iloc[i]>df_pos_rec.DATA_FINE.iloc[i]:
             dates.append(i)
        df_pos_rec1=df_pos_rec.drop(dates)
    df_pos_rec1.rename(columns={'ETA_x':'ETA'}, inplace=True)
    
    
    #starting time= time of starting positivity
    #finale time= entry in intensive care covid or hospital exit
    # Restricting the analysis to all the hospitalized patients who had covid ongoing
    list_ID=set()
    for i in range(0, len(dataset_bolo_hospital_path_pos.index)):
        if 'TERAPIA INTENSIVA COVID' in dataset_bolo_hospital_path_pos['SETTING'].iloc[i]:
            list_ID.add(dataset_bolo_hospital_path_pos['ID_PER'].iloc[i])
           
    return(df_pos_rec1,list_ID,sex_bolo)





# from lifelines import KaplanMeierFitter


# # In[51]:


# kfm=KaplanMeierFitter()
# kfm.fit(durations=keplan_meier_db['Giorni'], event_observed=keplan_meier_db['Intensiva'])
# print(kfm.event_table)
# kfm.plot(ci_show=True)
# plt.xlabel('Number of days before covid intensive care')
# plt.ylabel('Probability of survival')
# # plt.savefig('C:/Users/nicop/Desktop/KM')
# print(kfm.survival_function_,'\n','Median survival time:',kfm.median_survival_time_)


# # In[52]:


# kfm.plot_cumulative_density()
# plt.xlabel('Number of days before covid intensive care')
# plt.ylabel('Probability of going in intensive care')
# # plt.savefig('C:/Users/nicop/Desktop/KM2')


# # In[53]:


# groups = keplan_meier_db['sesso']   
# i1 = (groups == 1)      ## group i1 , having the pandas series  for the 1st cohort
# i2 = (groups == 0)     ## group i2 , having the pandas series  for the 2nd cohort


# ## fit the model for 1st cohort
# kfm.fit(keplan_meier_db['Giorni'][i1], keplan_meier_db['Intensiva'][i1], label='Males')
# a1 = kfm.plot(ci_show=False)
# kfm.fit(keplan_meier_db['Giorni'][i2], keplan_meier_db['Intensiva'][i2], label='Females')
# plt.title('Survival curve for males and females')
# plt.ylabel('Probability not to go in covid intensive care')
# kfm.plot(ax=a1,ci_show=False)


































# # Contingency tables of positive Bologna IDs

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


def create_list_multiple_sett(df,target_list):
    """
    create a lsit containin the ID of patients that are in the list of settings
    Inputs:
        df==dataset where to take patients
        target_list==list of setting to check
    Output:
        complete list of all the patients that are in that setting
    @Nicola2022
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
    @Nicola2022
    """
    if type(settlist)==str:
      settlist=[settlist]  
    if df.empty:
        print("The input dataframe is empty, no operation performed")
        return
    else:
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




