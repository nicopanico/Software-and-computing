# -*- coding: utf-8 -*-
import pandas as pd
from lifelines import KaplanMeierFitter
import matplotlib.pyplot as plt

def calculate_timediff_days(date1,date2):
    day_diff=((date1-date2).total_seconds())/86400
    return(day_diff)
    


def kaplan_meier_dataset(df,list_ID,sex_bolo):
    """
    Fucntion to create the final df for KM
    Inputs:
        df==df as input where there are all the resume for the ID with their hospitalization details (dates, covid status...)
        list_ID==list of ID that are in intensive care
        sex_bolo=list of all the sex for ID
    Output:
        keplan_meier_db==dataset containing ID of patients, days of hospitalization or days before going into covids intensive care
        sex and a binary columns with 1 if in intensive care 0 else and a columns with the age
    @Nicola2022
    """
    #create the dataset to be appended
    keplan_meier_db=pd.DataFrame(columns=['ID_PER','Giorni','Eta','Intensiva'])
    
    #search all the ID
    all_ID=set(df['ID_RICOVERO'])
    #divide them in the ID without intensive care
    ID_no_int=all_ID.difference(list_ID)
    
    #define patients that stayed only in intensive care or not in intensive care at all
    df_only_int=df[df['SETTING'] != 'TERAPIA INTENSIVA COVID']
    df_only_int=df[~df['ID_RICOVERO'].isin(df_only_int['ID_RICOVERO'])]
    ID_only_int=set(df_only_int['ID_RICOVERO'])
    
    ID_no_mix=ID_only_int.union(ID_no_int)
    for x in ID_no_mix:
        tempdf=df[df['ID_RICOVERO']==x]
        first=tempdf.iloc[0]
        last=tempdf.iloc[-1]
        hosp_days=last['DATA_FINE']-first['DATA_ACCETTAZIONE']
        keplan_meier_db=keplan_meier_db.append({'ID_PER':x, 'Giorni':hosp_days, 'Eta':first['ETA']},ignore_index=True)
        
    #patients that had intensive care in the middle of hospitalization
    ID_mix=all_ID.difference(ID_no_mix)
    for x in ID_mix:
        tempdf=df[df['ID_RICOVERO']==x]
        tempdf.reset_index(drop=True, inplace=True)
        int_index=tempdf.index[tempdf['SETTING']=='TERAPIA INTENSIVA COVID'].tolist()
        first_occ_int=tempdf.iloc[int_index[0]]
        if int_index==0:
            hosp_days=first_occ_int['DATA_FINE']-first_occ_int['DATA_ACCETTAZIONE']
        else:
             first_line=tempdf.iloc[0]
             hosp_days=first_occ_int['DATA_FINE']-first_line['DATA_ACCETTAZIONE']
             
        keplan_meier_db=keplan_meier_db.append({'ID_PER':x, 'Giorni':hosp_days, 'Eta':first_occ_int['ETA']},ignore_index=True)

           
    #defining columns name and setting some variables as binary(sex and intensive care)   to use them in the KM analysis
    keplan_meier_db['Intensiva']=[1 if x in list_ID else 0 for x in keplan_meier_db['ID_PER']]
    keplan_meier_db[['ID_PER','Intensiva']]=keplan_meier_db[['ID_PER','Intensiva']].astype(int)
   
    
    keplan_meier_db=pd.merge(keplan_meier_db,sex_bolo,how='inner', on=['ID_PER'])
    keplan_meier_db.rename(columns={'PER_KEY_SESSO':'sesso'}, inplace=True)
    keplan_meier_db['sesso']=[1 if x=='M' else 0 for x in keplan_meier_db['sesso'] ]
    return(keplan_meier_db)


def kfm_fitter(df):
    """
    Function in order to create the fitter for the Kaplam-Meier model
    Inputs:
        df==dataframe already filtered and prepared for the analisys
    Output:
        kfm=Kaplan-Meier fitter
    @Nicola2022
    """
    kfm=KaplanMeierFitter()
    kfm.fit(durations=df['Giorni'], event_observed=df['Intensiva'])
    return(kfm)


#------------------------------------------------------------------------------
#PLOT FUNCTIONS FOR THE KM FITS
def show_plots_kfm(kfm):
    """
    Fucntion to plot the 2 curves for the fitter
    one of the nuymber of days before covid intensive care
    the second for the number of days before intensive care but ta<king into account the probability to go in covid intensive care
    @Nicola2022
    """

   
    kfm.plot(ci_show=True)
    plt.xlabel('Number of days before covid intensive care')
    plt.ylabel('Probability of survival')
    # plt.savefig('C:/Users/nicop/Desktop/KM')
    plt.show()
    
    
def show_plots_kfm_cumulative(kfm):
    kfm.plot_cumulative_density()
    plt.xlabel('Number of days before covid intensive care')
    plt.ylabel('Probability of going in intensive care')
    plt.show()
    


def plot_M_F_fitter(df,kfm):
    """
    function to get the survival curves making a distinction between males and females
    @Nicola2022
    
    """

   
    groups = df['sesso']   
    i1 = (groups == 1)      ## group i1 , having the pandas series  for the 1st cohort
    i2 = (groups == 0)     ## group i2 , having the pandas series  for the 2nd cohort

    ## fit the model for 1st cohort
    kfm.fit(df['Giorni'][i1], df['Intensiva'][i1], label='Males')
    a1 = kfm.plot(ci_show=False)
    kfm.fit(df['Giorni'][i2], df['Intensiva'][i2], label='Females')
    plt.title('Survival curve for males and females')
    plt.ylabel('Probability not to go in covid intensive care')
    kfm.plot(ax=a1,ci_show=False)
    plt.show()
    

