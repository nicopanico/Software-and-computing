#!/usr/bin/env python
# coding: utf-8
import sys,os
os.chdir('C:/Users/nicop/Desktop/software_computing/Software-and-computing')
sys.path.append(os.path.dirname(os.path.realpath(file)))
##importing packages used in the script

from dataclasses import dataclass
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as st
import statistics
from scipy.stats import chi2_contingency
from scipy.stats import fisher_exact
# get_ipython().system('{sys.executable} -m pip install lifelines')
import my_functions
import names
import sett_hosp

# # OPENING THE CSV FILES
# main datasets used for the script it could require time


anag_comune_bo=pd.read_csv('./Data_set/ANAGCOMUNEBO.csv')
positivi_unibo=pd.read_csv('./Data_set/Casi_covid_unibo_2021-11-22.csv',';')
positivi_unibo[names.names.accettazione]=pd.to_datetime(positivi_unibo[names.names.accettazione])
positivi_unibo[names.names.esito]=pd.to_datetime(positivi_unibo[names.names.esito])
analysis_entries_updated=pd.read_csv('./Data_set/ANALISI_ENTRATE_2021_10_13.csv',';')
analysis_entries_updated[names.names.inizio]=pd.to_datetime(analysis_entries_updated[names.names.inizio])
analysis_entries_updated=analysis_entries_updated.fillna(0)
analisi_uscite_updated=pd.read_csv('./Data_set/ANALISI_USCITE_2021_10_13.csv',';')
analisi_uscite_updated[names.names.inizio]=pd.to_datetime(analisi_uscite_updated[names.names.inizio])
analisi_uscite_updated[names.names.fine]=pd.to_datetime(analisi_uscite_updated[names.names.fine])
patologies=pd.read_csv('./Data_set/Patologie.csv',';')
ID_Bologna=anag_comune_bo[names.names.ID]#all the ID of Bologna




database_entries=analysis_entries_updated[[names.names.setting,names.names.ID,names.names.deceduto]]



sex_bolo=anag_comune_bo[[names.names.sesso,names.names.ID]]



# # Check on the database 'casi covid unibo' to make sure everything is matching in the database

# Removing the people that still have covid at the moment
#since the analysis is performed over the patients who have a complete track (start and end)


#dataset matching

still_sick=positivi_unibo.DATA_ESITO.isna().value_counts().loc[False] #patients still not healthy
still_pos=positivi_unibo.ESITO.isin([names.names.malattia]).value_counts().loc[False] #patients who still have covid

iscovidnow=my_functions.create_target_ID_list(positivi_unibo,names.names.malattia,names.names.esito2)
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
 
# database_pos_KM=positivi_unibo.drop(iscovidnow)

# Checking the number of positives deceased and comparing it with the patients deceased in covid departments
#create the database containing the ID of all the positives also the non-hospitalized ones
database_pos_bolo=pd.merge(database_pos_outcome,ID_Bologna,how='inner',on=[names.names.ID])
database_pos_bolo=database_pos_bolo.drop_duplicates(subset=[names.names.ID])

isPosDeceased=my_functions.create_target_ID_list(database_pos_bolo,names.keywords.decesso,names.keywords.esito)
print('number of positives deceased for bologna IDs:',len(isPosDeceased))

isCovDeceased=my_functions.deceased_list(database_entries_bo_covid)


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


# Checking if all the hospitalized patients in covid settings are positives



isPosinCovidint=my_functions.create_target_ID_list(dataset_tracking_bologna_positives,sett_hosp.hospital.intensiva_covid,
                                      names.names.setting)     
isinCovidint=my_functions.create_target_ID_list(dataset_tracking_bologna,sett_hosp.hospital.intensiva_covid,names.names.setting)

print('Number of patients hospitalized in covid intensive care:',len(isinCovidint),'\n',
      'Number of positive patients hospitalized in covid intensive care',len(isPosinCovidint))


# # Contingency tables of positive Bologna IDs

# In[13]:


trial_list=['DIABETE MELLITO-DIABETE MELLITO','IPERTENSIONE ESSENZIALE',
            'EMBOLIA E TROMBOSI DI ALTRE VENE (ESCLUSO SINDROME DI BUDD-CHIARI)',
          'SOGGETTI AFFETTI DA PATOLOGIE NEOPLASTICHE MALIGNE - SOGGETTI AFFETTI DA PATOLOGIE NEOPLASTICHE MALIGNE',
           'ARITMIE CARDIACHE','CARDIOPATIA IPERTENSIVA']
list_setting_nocov=['DEGENZA MED GENERALE NO COVID',          
'DEGENZA CHIR SPECIALISTICA NO COVID',   
'DEGENZA MED SPECIALISTICA NO COVID',     
'ALTRO',                                 

'DEGENZA CHIR GENERALE NO COVID',         
'TERAPIA INTENSIVA NO COVID',            
'SUB INTENSIVA NO COVID',                
'EMERGENZA-URGENZA',                     
'SOSPETTI COVID',                          
'ORTOPEDIA']
list_setting_cov_noint=['DEGENZA ORDINARIA COVID'  ,'SUB INTENSIVA COVID', 'DEGENZA COVID BASSA INTENSITA']


# First contingency: taking into account only patients from covid intensive care

# In[14]:
isbothsetting=[]
for i in range(0,len(dataset_tracking_bologna_positives.index)):
    if ('DEGENZA ORDINARIA COVID' in dataset_tracking_bologna_positives['SETTING'].iloc[i] and 'TERAPIA INTENSIVA COVID' in dataset_tracking_bologna_positives['SETTING'].iloc[i]):
        isbothsetting.append(i)                                                                                          
    
    

isPosnotcovint=[]
for i in range(0,len(dataset_tracking_bologna_positives.index)):
    if ('DEGENZA ORDINARIA COVID' in dataset_tracking_bologna_positives['SETTING'].iloc[i] or 'DEGENZA COVID BASSA INTENSITA' in dataset_tracking_bologna_positives['SETTING'].iloc[i] or 'SUB INTENSIVA COVID' in dataset_tracking_bologna_positives['SETTING'].iloc[i]) and 'TERAPIA INTENSIVA COVID' not in dataset_tracking_bologna_positives['SETTING'].iloc[i]:
        isPosnotcovint.append(i)
dataset_pos_bolo_cov_int=dataset_tracking_bologna_positives.drop(isPosnotcovint)

l=[]
for i in range(0,len(dataset_pos_bolo_cov_int.index)):
    if 'TERAPIA INTENSIVA COVID' in dataset_pos_bolo_cov_int['SETTING'].iloc[i]:
        l.append(i)
print(len(l))


# Second contingency: taking into account only patients not from covid intensive care

# In[15]:


dataset_pos_bolo_no_cov_int=dataset_tracking_bologna_positives.drop(isPosinCovidint)


# Third contingency: taking into account only patients coming from noncovid settings

# In[16]:


isPoscov=[]
for i in range(0, len(dataset_tracking_bologna_positives.index)):
    if 'TERAPIA INTENSIVA COVID' in dataset_tracking_bologna_positives['SETTING'].iloc[i] or 'SUB INTENSIVA COVID' in dataset_tracking_bologna_positives['SETTING'].iloc[i] or 'DEGENZA ORDINARIA COVID' in dataset_tracking_bologna_positives['SETTING'].iloc[i] or 'DEGENZA COVID BASSA INTENSITA' in dataset_tracking_bologna_positives['SETTING'].iloc[i]:
        isPoscov.append(i)
dataset_pos_bolo_no_cov=dataset_tracking_bologna_positives.drop(isPoscov)
#all patients with are not in covid settings

# FIRST contingency

# In[17]:


ispat=[]
isint=[]

set_int_results={}
for ptlg in trial_list:
    ispat.clear()
    isint.clear()
    for i in range(0, len(dataset_pos_bolo_cov_int.index)):
        if ptlg in dataset_pos_bolo_cov_int['Descrizione_Esenzione'].iloc[i]:
            ispat.append('SI')
        else:
            ispat.append('NO')
        if 'TERAPIA INTENSIVA COVID' in dataset_pos_bolo_cov_int['SETTING'].iloc[i]:
            isint.append('SI')
        else:
            isint.append('NO')
    dp=pd.DataFrame({ptlg.lower() : ispat,
                   'intensiva' : isint
                  })
    contingency=pd.crosstab(dp[ptlg.lower()], dp['intensiva'])
    OR, p=fisher_exact(contingency)
    set_int_results[ptlg]=OR


# Second contingency

# In[22]:


ispat1=[]
isint1=[]
set_results_no_covid={}
for ptlg in trial_list:
    ispat1.clear()
    isint1.clear()
    for i in range(0, len(dataset_pos_bolo_no_cov)):
                if ptlg in dataset_pos_bolo_no_cov['Descrizione_Esenzione'].iloc[i]:
                    ispat1.append('SI')
                else:
                    ispat1.append('NO')
                found=False
                for k in list_setting_nocov:
                    if k in dataset_pos_bolo_no_cov['SETTING'].iloc[i] and not found:
                        isint1.append('SI')
                        found=True
                if not found:
                    isint1.append('NO')
   
                   
    dp=pd.DataFrame({ptlg.lower() : ispat1,
                   'setting_noCovid' : isint1
                  })
    contingency=pd.crosstab(dp[ptlg.lower()], dp['setting_noCovid'])
    OR, p=fisher_exact(contingency)
    set_results_no_covid[ptlg]=OR
    


# Third contingency

# In[23]:


ispat2=[]
isint2=[]
set_results_covid_noint={}
for ptlg in trial_list:
    ispat2.clear()
    isint2.clear()
    for i in range(0, len(dataset_pos_bolo_no_cov_int.index)):
                if ptlg in dataset_pos_bolo_no_cov_int['Descrizione_Esenzione'].iloc[i]:
                    ispat2.append('SI')
                else:
                    ispat2.append('NO')
                found=False
                for k in list_setting_cov_noint:
                    if k in dataset_pos_bolo_no_cov_int['SETTING'].iloc[i] and not found:
                        isint2.append('SI')
                        found=True
                if not found:
                    isint2.append('NO')
   
                   
    dp=pd.DataFrame({ptlg.lower() : ispat2,
                   'setting_covid' : isint2
                  })
    contingency=pd.crosstab(dp[ptlg.lower()], dp['setting_covid'])
    OR, p=fisher_exact(contingency)
    set_results_covid_noint[ptlg]=OR


# # Results

# In[24]:


OD_compare=pd.DataFrame.from_dict([set_results_no_covid,set_results_covid_noint,set_int_results])
OD_compare=OD_compare.rename(index={0:'setting no covid',2:'covid intensive care',1:'covid settings no int'})
display(OD_compare)


# # Kaplan-Meier

# Processing of the data

# In[17]:


dataset_bolo_exit=pd.merge(ID_Bologna,analisi_uscite_updated,how='inner',on=['ID_PER'])
dataset_bolo_exit_pos=pd.merge(ID_positives,dataset_bolo_exit,how='inner', on=['ID_PER'])
test_2=pd.merge(dataset_bolo_exit_pos,analysis_entries_updated,how='inner',on=['ID_PER','SETTING','ID_RICOVERO','DATA_INIZIO'])
database_pos_KM=pd.merge(database_pos_KM,ID_Bologna,how='inner',on=['ID_PER'])





# Modifying the dataset in order to have all the dates in the same format

# In[48]:


from datetime import datetime,timedelta




for i in range(0, len(test_2.index)):
    if test_2.DATA_INIZIO.iloc[i].month!=test_2.MESE_y.iloc[i]: 
        month=test_2.DATA_INIZIO.iloc[i].month
        day=test_2.DATA_INIZIO.iloc[i].day
        test_2.DATA_INIZIO.iloc[i]=test_2['DATA_INIZIO'].iloc[i].replace(month=day,day=month)
    if test_2.DATA_FINE.iloc[i].month!=test_2.MESE_x.iloc[i]: 
        month1=test_2.DATA_FINE.iloc[i].month
        day1=test_2.DATA_FINE.iloc[i].day
        test_2.DATA_FINE.iloc[i]=test_2['DATA_FINE'].iloc[i].replace(month=day1,day=month1)

        
        
dates=[]
df_pos_rec=pd.merge(test_2[['ID_PER','SETTING','DATA_INIZIO','DATA_FINE','ID_RICOVERO','DURATA_GG','ETA_x']],database_pos_KM[['ID_PER','DATA_ESITO','DATA_ACCETTAZIONE']],how='left', on=['ID_PER'])
#display(df_pos_rec)
for i in range(0, len(df_pos_rec.index)):
    if df_pos_rec.DATA_ACCETTAZIONE.iloc[i]>df_pos_rec.DATA_FINE.iloc[i]:
         dates.append(i)
    df_pos_rec1=df_pos_rec.drop(dates)
df_pos_rec1.rename(columns={'ETA_x':'ETA'}, inplace=True)
display(df_pos_rec1) 

#display(test_2)


# In[14]:


#tempo iniziale= tempo di inzio positività
#tempo finale= ingresso ter int covid or ultima dimissione dall'ospedale dell ID_PER


# Restricting the analysis to all the hospitalized patients who had covid ongoing

# In[19]:


list_intcovid=[]
list_ID=set()
for i in range(0, len(test_2.index)):
    if 'TERAPIA INTENSIVA COVID' in test_2['SETTING'].iloc[i]:
        list_intcovid.append(i)
        list_ID.add(test_2['ID_PER'].iloc[i])
        
        test_noint=test_2.drop(list_intcovid)


# Creating the datafarame for the Kaplan-Meier

# In[20]:
#the sex is set to be 1 for male and 0 for female, so the column of the sex is binary


keplan_meier_db=pd.DataFrame(columns=['ID_PER','Giorni','Età','Intensiva'])
tempID='0'
tempdate=0
wasintcovid=False
for i in range(0,len(df_pos_rec1.index)):
    
        if tempID != df_pos_rec1['ID_PER'].iloc[i]:
                tempdate=df_pos_rec1.DATA_FINE.iloc[i]
                tempID=df_pos_rec1['ID_PER'].iloc[i]
                
                if 'TERAPIA INTENSIVA COVID' not in df_pos_rec1['SETTING'].iloc[i]:
                    keplan_meier_db=keplan_meier_db.append({'ID_PER':df_pos_rec1.ID_PER.iloc[i],'Giorni': ((df_pos_rec1.DATA_FINE.iloc[i]-df_pos_rec1.DATA_ACCETTAZIONE.iloc[i]).total_seconds())/86400,'Età':df_pos_rec1.ETA.iloc[i],'Intensiva':0},ignore_index=True)
                    wasintcovid=False
                    #print(tempID)   
                else:
                    keplan_meier_db=keplan_meier_db.append({'ID_PER':df_pos_rec1.ID_PER.iloc[i],'Giorni': ((df_pos_rec1.DATA_INIZIO.iloc[i]-df_pos_rec1.DATA_ACCETTAZIONE.iloc[i]).total_seconds())/86400,'Età':df_pos_rec1.ETA.iloc[i],'Intensiva':0},ignore_index=True)
                    wasintcovid=True    
        elif tempID==df_pos_rec1['ID_PER'].iloc[i] and 'TERAPIA INTENSIVA COVID' not in df_pos_rec1['SETTING'].iloc[i] and not wasintcovid:
                if tempdate<df_pos_rec1.DATA_FINE.iloc[i]:
                    tempdate=df_pos_rec1.DATA_FINE.iloc[i]
                    keplan_meier_db['Giorni'].iloc[-1]=((tempdate-df_pos_rec1.DATA_ACCETTAZIONE.iloc[i]).total_seconds())/86400
                

                    
        elif tempID==df_pos_rec1['ID_PER'].iloc[i] and 'TERAPIA INTENSIVA COVID' in df_pos_rec1['SETTING'].iloc[i]:
                wasintcovid=True
            
    
keplan_meier_db[['ID_PER','Intensiva']]=keplan_meier_db[['ID_PER','Intensiva']].astype(int)
keplan_meier_db['Intensiva']=[1 if x in list_ID else 0 for x in keplan_meier_db['ID_PER']]
keplan_meier_db=pd.merge(keplan_meier_db,sex_bolo,how='inner', on=['ID_PER'])
keplan_meier_db.rename(columns={'PER_KEY_SESSO':'sesso'}, inplace=True)
keplan_meier_db['sesso']=[1 if x=='M' else 0 for x in keplan_meier_db['sesso'] ]
display(keplan_meier_db)





# In[21]:


borderline=[]
for i in range(0, len(keplan_meier_db.index)):
    if keplan_meier_db.Giorni.iloc[i]<0:
        borderline.append(i)
keplan_meier_db=keplan_meier_db.drop(borderline)
display(keplan_meier_db)


# In[22]:


keplan_meier_db2=pd.merge(keplan_meier_db,df_pos_rec1[['DATA_INIZIO','ID_PER']],how='inner', on=['ID_PER'])
keplan_meier_db2=keplan_meier_db2.drop_duplicates(subset='ID_PER',keep='first')
iswave=[]
for i in range(0,len(keplan_meier_db2.index)):
    if 2<=keplan_meier_db2.DATA_INIZIO.iloc[i].month<=5 and keplan_meier_db2.DATA_INIZIO.iloc[i].year==2020:
        iswave.append(1)
    elif 6<=keplan_meier_db2.DATA_INIZIO.iloc[i].month<=10 and keplan_meier_db2.DATA_INIZIO.iloc[i].year==2020:
        iswave.append(2)
    elif (11<=keplan_meier_db2.DATA_INIZIO.iloc[i].month<=12 and keplan_meier_db2.DATA_INIZIO.iloc[i].year==2020) or (1<=keplan_meier_db2.DATA_INIZIO.iloc[i].month<=4 and keplan_meier_db2.DATA_INIZIO.iloc[i].year==2021):
        iswave.append(3)
    else:
        iswave.append(4)
keplan_meier_db2['Ondata']=iswave
keplan_meier_db2=keplan_meier_db2.drop(columns=['DATA_INIZIO'])
display(keplan_meier_db2)


# Keplan-Meier curves

# In[23]:


from lifelines import KaplanMeierFitter


# In[51]:


kfm=KaplanMeierFitter()
kfm.fit(durations=keplan_meier_db['Giorni'], event_observed=keplan_meier_db['Intensiva'])
print(kfm.event_table)
kfm.plot(ci_show=True)
plt.xlabel('Number of days before covid intensive care')
plt.ylabel('Probability of survival')
# plt.savefig('C:/Users/nicop/Desktop/KM')
print(kfm.survival_function_,'\n','Median survival time:',kfm.median_survival_time_)


# In[52]:


kfm.plot_cumulative_density()
plt.xlabel('Number of days before covid intensive care')
plt.ylabel('Probability of going in intensive care')
# plt.savefig('C:/Users/nicop/Desktop/KM2')


# In[53]:


groups = keplan_meier_db['sesso']   
i1 = (groups == 1)      ## group i1 , having the pandas series  for the 1st cohort
i2 = (groups == 0)     ## group i2 , having the pandas series  for the 2nd cohort


## fit the model for 1st cohort
kfm.fit(keplan_meier_db['Giorni'][i1], keplan_meier_db['Intensiva'][i1], label='Males')
a1 = kfm.plot(ci_show=False)
kfm.fit(keplan_meier_db['Giorni'][i2], keplan_meier_db['Intensiva'][i2], label='Females')
plt.title('Survival curve for males and females')
plt.ylabel('Probability not to go in covid intensive care')
kfm.plot(ax=a1,ci_show=False)
# plt.savefig('C:/Users/nicop/Desktop/KM_sex')


# # Cox-Hazard regression

# Importing library and instantiate model

# In[27]:


from lifelines import CoxPHFitter
cox_sex_age=keplan_meier_db2.drop(columns=['ID_PER'])


# Cox_Hazard model using just sex age and wave as covariates

# In[29]:


cox1=CoxPHFitter()
cox1.fit(cox_sex_age, duration_col = 'Giorni', event_col = 'Intensiva')
cox1.print_summary()
plt.subplots(figsize = (10, 6))
cox1.plot()


# Cox-Hazard regression divided for sex considering just age as covariate

# In[30]:



#taking 2 different data for males and females 
cox_male=cox_sex_age[cox_sex_age['sesso']==1]
cox_female=cox_sex_age[cox_sex_age['sesso']==0]
print('numero di positivi di sesso maschile:',len(cox_male.index),'\n','numero di positivi di sesso femminile:',len(cox_female.index))
#dropping rows 'sesso' and 'Ondata'
cox_male=cox_male.drop(columns=['Ondata','sesso'])
cox_female=cox_female.drop(columns=['Ondata','sesso'])


# In[31]:


m=plt.hist(cox_male['Età'],color='y')
plt.axvline(cox_male['Età'].mean(), c='r')
plt.show()

f=plt.hist(cox_female['Età'],color='g')
plt.axvline(cox_female['Età'].mean(), c='r')
plt.show()

print('Età media positivi sesso maschile:',cox_male['Età'].mean(),'\n',
     'Età media positivi sesso femminile:',cox_female['Età'].mean())


# regression for males considering just age and wave as covariates

# In[32]:


cox2=CoxPHFitter()
cox2.fit(cox_male, duration_col = 'Giorni', event_col = 'Intensiva')
cox2.print_summary()
plt.subplots(figsize = (10, 6))
cox2.plot()


# In[33]:


cox2.plot_partial_effects_on_outcome(covariates = 'Età', values = [20,30,40,50, 60, 70, 80,90], cmap = 'coolwarm')


# Regression for females considering just age as covariate

# In[34]:


cox3=CoxPHFitter()
cox3.fit(cox_female, duration_col = 'Giorni', event_col = 'Intensiva')
cox3.print_summary()
plt.subplots(figsize = (10, 6))
cox3.plot()


# In[35]:


cox3.plot_partial_effects_on_outcome(covariates = 'Età', values = [20,30,40,50, 60, 70, 80,90], cmap = 'coolwarm')


# Preparing the Cox dataset with all covariates

# In[36]:


pre_cox_db=pd.merge(keplan_meier_db2,dataset_bolo_patologies, how='inner',on=['ID_PER'])
haspat=[]
for ptlg in trial_list:
    haspat.clear()
    for i in range(0,len(pre_cox_db.index)):
        if ptlg in pre_cox_db['Descrizione_Esenzione'].iloc[i]:
            haspat.append(1)
        else:
            haspat.append(0)
    pre_cox_db[ptlg]=haspat
pre_cox_db.rename(columns={'DIABETE MELLITO-DIABETE MELLITO': 'Diabete_mellito', 
                           'IPERTENSIONE ESSENZIALE': 'Ipertensione_essenziale',
                           'EMBOLIA E TROMBOSI DI ALTRE VENE (ESCLUSO SINDROME DI BUDD-CHIARI)':'Embolia_trombosi',
                          'SOGGETTI AFFETTI DA PATOLOGIE NEOPLASTICHE MALIGNE - SOGGETTI AFFETTI DA PATOLOGIE NEOPLASTICHE MALIGNE':'Soggetti_pat_neoplastiche',
                          'ARITMIE CARDIACHE':'Aritmie_cardiache',
                          'CARDIOPATIA IPERTENSIVA':'Cardiopatia_ipertensiva'}, inplace=True)
pre_cox_db=pre_cox_db.drop(columns=['Descrizione_Esenzione'])
Cox_db=pre_cox_db.drop(columns=['ID_PER'])

display(Cox_db)



        


# Cox fitter showing the summary table

# In[37]:


cox4=CoxPHFitter()
cox4.fit(Cox_db, duration_col = 'Giorni', event_col = 'Intensiva')
cox4.print_summary()


# Plotting results

# In[38]:


plt.subplots(figsize = (10, 6))
cox4.plot()


# In[39]:


cox4.plot_partial_effects_on_outcome(covariates = 'Età', values = [20,30,40,50, 60, 70, 80,90], cmap = 'coolwarm')


# In[40]:


cox4.plot_partial_effects_on_outcome(covariates = 'Ondata', values = [1,2,3,4], cmap = 'coolwarm')


# In[41]:


cox4.plot_partial_effects_on_outcome(covariates = 'sesso',values = [1,0], cmap = 'coolwarm')

