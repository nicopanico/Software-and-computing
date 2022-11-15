# -*- coding: utf-8 -*-
import pandas as pd
from lifelines import KaplanMeierFitter
import matplotlib.pyplot as plt




def kaplan_meier_dataset(df,list_ID,sex_bolo):
    """
    fucntion to define the dataset to use in the kaplan-meier analisys, the only difference is that it takes into account patients
    from their entry since their arrive in the covid intensive care or exit from hospital
    then rename some columsn and assign binary values to sex and intensive care covid
    @Nicola2022
    """

  
    keplan_meier_db=pd.DataFrame(columns=['ID_PER','Giorni','Età','Intensiva'])
    tempID='0'
    tempdate=0
    wasintcovid=False
    for i in range(0,len(df.index)):
        #reorganizing the dates and taking as final time or the end of intensive care or exit from hospital and converting the time
            if tempID != df['ID_PER'].iloc[i]:
                    tempdate=df.DATA_FINE.iloc[i]
                    tempID=df['ID_PER'].iloc[i]
                    
                    if 'TERAPIA INTENSIVA COVID' not in df['SETTING'].iloc[i]:
                        keplan_meier_db=keplan_meier_db.append({'ID_PER':df.ID_PER.iloc[i],'Giorni': ((df.DATA_FINE.iloc[i]-df.DATA_ACCETTAZIONE.iloc[i]).total_seconds())/86400,'Età':df.ETA.iloc[i],'Intensiva':0},ignore_index=True)
                        wasintcovid=False
                        #print(tempID)   
                    else:
                        keplan_meier_db=keplan_meier_db.append({'ID_PER':df.ID_PER.iloc[i],'Giorni': ((df.DATA_INIZIO.iloc[i]-df.DATA_ACCETTAZIONE.iloc[i]).total_seconds())/86400,'Età':df.ETA.iloc[i],'Intensiva':0},ignore_index=True)
                        wasintcovid=True    
            elif tempID==df['ID_PER'].iloc[i] and 'TERAPIA INTENSIVA COVID' not in df['SETTING'].iloc[i] and not wasintcovid:
                    if tempdate<df.DATA_FINE.iloc[i]:
                        tempdate=df.DATA_FINE.iloc[i]
                        keplan_meier_db['Giorni'].iloc[-1]=((tempdate-df.DATA_ACCETTAZIONE.iloc[i]).total_seconds())/86400        
            elif tempID==df['ID_PER'].iloc[i] and 'TERAPIA INTENSIVA COVID' in df['SETTING'].iloc[i]:
                    wasintcovid=True
                
    #defining columns name and setting some variables as binary(sex and intensive care)  
    keplan_meier_db[['ID_PER','Intensiva']]=keplan_meier_db[['ID_PER','Intensiva']].astype(int)
    keplan_meier_db['Intensiva']=[1 if x in list_ID else 0 for x in keplan_meier_db['ID_PER']]
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
    print(kfm.event_table)
    return(kfm)



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
    

