# -*- coding: utf-8 -*-
import pandas as pd





def kaplan_meier_dataset(df,list_ID,sex_bolo):
    """
    fucntion to define the dataset to use in the kaplan-meier analisys, the only difference is taht it takes into account patients
    from their entry since their arrive in the covid intensive care or exit from hospital
    then rename some columsn and assign binary values to sex and intensive care covid
    """

  
    keplan_meier_db=pd.DataFrame(columns=['ID_PER','Giorni','Età','Intensiva'])
    tempID='0'
    tempdate=0
    wasintcovid=False
    for i in range(0,len(df.index)):
        #reorganizing the dates and taking as final time or the end of intensive care or exit from hospital
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

