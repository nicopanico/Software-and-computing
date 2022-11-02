# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 19:24:54 2022

@author: iacop
"""



database_entries=analysis_entries_updated[[names.names.setting,names.names.ID,names.names.deceduto]]



sex_bolo=anag_comune_bo[[names.names.sesso,names.names.ID]]



# # Check on the database 'casi covid unibo' to make sure everything is matching in the database

# Removing the people that still have covid at the moment
#since the analysis is performed over the patients who have a complete track (start and end)


#dataset matching


iscovidnow=ff.create_target_ID_list(positivi_unibo,names.names.malattia,names.keywords.esito)
database_pos_outcome=positivi_unibo.drop(iscovidnow)#drop patients who still have covid
database_pos_outcome.drop_duplicates(subset=[names.names.ID], inplace=True)#and remove the duplciates ID

#taking the IDs of positive patients
ID_positives=database_pos_outcome[names.names.ID]  
"""
Now merge the IDs of the positive patients with the people in covid hopsital settings
to see how many positive patients got hospitalized
"""  
database_entries_bo=pd.merge(ID_Bologna,analysis_entries_updated[[names.names.setting,names.names.ID,names.names.deceduto]], 
                             how='left', on=[names.names.ID])

#define the sub-dataset containing the entries for all the covid settings
database_entries_bo_covid=database_entries_bo[database_entries_bo.SETTING.isin([sett_hosp.hospital.intensiva_covid,
                                                                                sett_hosp.hospital.degenza_ordinaria_covid,
                                                                                sett_hosp.hospital.sub_intensiva_covid,
                                                                                sett_hosp.hospital.degenza_covid_bassa_intesita])]
#database for all the patients that have covid and are in covid settings
database_entries_bo_covid_positives=pd.merge(database_entries_bo_covid,ID_positives,how='inner',on=[names.names.ID])
 


# Checking the number of positives deceased and comparing it with the patients deceased in covid departments
#create the database containing the ID of all the positives also the non-hospitalized ones
database_pos_bolo=pd.merge(database_pos_outcome,ID_Bologna,how='inner',on=[names.names.ID])
database_pos_bolo=database_pos_bolo.drop_duplicates(subset=[names.names.ID])

isPosDeceased=ff.create_target_ID_list(database_pos_bolo,names.keywords.decesso,names.keywords.esito)
print('number of positives deceased for bologna IDs:',len(isPosDeceased))

isCovDeceased=ff.deceased_list(database_entries_bo_covid)


# Checking if the total number of hopistalized in covid departments are positves
print('number of positive patients hospitalized in covid setting:', len(database_entries_bo_covid_positives.index),'\n',
      'total number of patients hospitalized in covid setting:',len(database_entries_bo_covid.index))


# Getting the datasets of 'SETTING' and 'Descrizione_Esenzione' per ID
dataset_setting=analysis_entries_updated[[names.names.setting,names.names.ID]]
dataset_patologies=patologies[[names.names.descrizione_esenzione,names.names.ID]]
dataset_patologies_per_setting=pd.merge(dataset_setting, dataset_patologies, how='left',on=[names.names.ID])

#narrowing down the analysis to just Bologna ID_PER
dataset_bolo_setting=pd.merge(ID_Bologna,dataset_setting, how='left', on=[names.names.ID])
dataset_bolo_setting=dataset_bolo_setting.fillna('NaN')
dataset_bolo_patologies=pd.merge(ID_Bologna,dataset_patologies, how='left', on=[names.names.ID])
dataset_bolo_patologies=dataset_bolo_patologies.fillna('NaN')


# Modelling the database to have the complete description of the setting and patology for each Bologna ID




dataset_bolo_patologies=dataset_bolo_patologies.groupby([names.names.ID]).agg({names.names.descrizione_esenzione:','.join})
dataset_bolo_setting=dataset_bolo_setting.groupby([names.names.ID]).agg({names.names.setting:','.join})
dataset_tracking_bologna=pd.merge(dataset_bolo_patologies,dataset_bolo_setting, how='left',on=[names.names.ID])
dataset_tracking_bologna_positives=pd.merge(dataset_tracking_bologna,ID_positives, how='inner', on=[names.names.ID])


# # Contingency tables of positive Bologna IDs
"""
Create contingency tables in order to see if there is some correlation between the covid intensive care hospitalized and 
the patologies:
    the list of patologies to test was given a priori, out of all the patologie sin the dataset only 6 were chosen 
"""

trial_list=patology.patologies.patlist

list_setting_nocov=sett_hosp.SettingList.nocovid_setting #list from the dataclass to take the list of
#all the non covid settings
list_setting_cov_noint=(sett_hosp.SettingList.covid_setting)
list_setting_cov_noint.remove(sett_hosp.hospital.intensiva_covid)


# First contingency: taking into account only patients from covid intensive care
  
isPosnotcovint=[]                                                                                 
for i in range(0, len(list_setting_cov_noint)):
    list_pat=ff.create_target_ID_list(dataset_tracking_bologna_positives,list_setting_cov_noint[i],names.names.setting)
    isPosnotcovint=list(set().union(list_pat,isPosnotcovint))

isPosInt=ff.create_target_ID_list(dataset_tracking_bologna_positives,sett_hosp.hospital.intensiva_covid,names.names.setting,)  

#now remove the patients that have been hospitalized also in covid intensive care setting
isPosnotcovint=ff.common_elements(isPosnotcovint,isPosInt)

#also obtain a dataset with intensive care patients but not the other covid settings, that will be usefull for the cntingency tables
dataset_pos_bolo_cov_int=dataset_tracking_bologna_positives.drop(isPosnotcovint)




# Second contingency: taking into account only patients not from covid intensive care

isPosinCovidint=ff.create_target_ID_list(dataset_tracking_bologna_positives,sett_hosp.hospital.intensiva_covid,
                                      names.names.setting)     
isinCovidint=ff.create_target_ID_list(dataset_tracking_bologna,sett_hosp.hospital.intensiva_covid,names.names.setting)

#dataset excluding patients who passed throught the covid intensive care setting
dataset_pos_bolo_no_cov_int=dataset_tracking_bologna_positives.drop(isPosinCovidint)


# Third contingency: taking into account only patients coming from noncovid settings


isPoscov=[]
list_cov_setting=sett_hosp.SettingList.covid_setting
for i in range(0, len(list_cov_setting)):
    sett_list=ff.create_target_ID_list(dataset_tracking_bologna_positives,list_cov_setting[i],names.names.setting)
    isPoscov=list(set().union(sett_list,isPoscov))
    
dataset_pos_bolo_no_cov=dataset_tracking_bologna_positives.drop(isPoscov)
#exclude all the patients from covid settings