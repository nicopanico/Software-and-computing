y# -*- coding: utf-8 -*-


import pandas as pd
import datetime
from scipy.stats import fisher_exact
from Classes_for_user import names
import numpy as np


"""
Script containing all the basis functions used then in the other main scripts, those fucntions are all tested and used in the other
scripts of the repository
"""

    
    
def create_target_ID_list(df, key_word, col_name):
    '''
 function in order to create a list containing the ID of all the patients with a certain resume
 inputs:
    df=dataset containing the data
    key_word= word we would like to search in our dataset given as a string or also as a lsit of strings, e.g. if 
    you want to search for more settings you cant provide key_word=['sett1','sett2']...
    col_name=name of the column where we would like to search key_word given as a string
    @Nicola-2022
  
  '''
    if df.empty:
        target_list=[]
    if col_name  not in df.columns:
        raise ValueError('{} is not in the dataframe columns'.format(col_name)) 
        
    col=df[col_name]
    isKey=col.isin(key_word)
    df_key=df[isKey]
    target_list=list(df_key.index)

    return(target_list) 
  
 

def deceased_list(df):
     """
     Function in order to count the number of deceased patients in a certain dataframe
     inputs:
         df==dataframe where to count the deceased patients
     output:
         deceased_list==list containing the rows of patients thaat are deceased
    notes: the df provided has to containg a columns regarding the deceased patients otherwise the fucntion 
    will return an error
    @Nicola-2022
    """
     if names.key_words.deceduto not in df.columns:
        raise ValueError('{} is not in the dataframe columns,take a dataset with deceased data'.format('DECEDUTO'))
     
     isDead=df[names.key_words.deceduto].isin([1])
     df_dead=df[isDead]
     deceased_list=list(df_dead.index)
     return(deceased_list)
   



def common_elements(list1, list2):
    """
    function in order to remove from one the common elements of the other
    inputs:
        a==main list to remove elements from
        b==second list to comapre with a
    @Nicola-2022
    """
    for i in list1[:]:
        if i in list2:
            list1.remove(i)
    return(list1)

             
       

def create_contingency_pat(df,ptlg):
    """
    Function to create the contingency list with 'SI' or 'NO' base on if the patient has or not one of the patologies
    in ptlg
    Inputs:
        df==df to give as input
        ptlg== patology list containing all the wanted patologies
    Output:
        ispat==list with the 'SI' or 'NO' values
    @Nicola2022
    """
    patol=df[names.key_words.descrizione_esenzione]
    isPtlg=list(patol.isin(ptlg))
    ispat=['SI' if x else 'NO' for x in isPtlg]
    return(ispat)


def create_contingency_sett(df,key_word):
    """
    Function to create the contingency lsit with 'SI' or 'NO' based on if the patient is in the defined settings
    Inputs:
        df==df to give as input
        key_word==list of settings to pass as input
    Output:
        isint=list with the 'SI' or 'NO' values
    @Nicola2022
    """
    sett=df[names.key_words.setting]
    isSett=list(sett.isin(key_word))
    isint=['SI' if x else 'NO' for x  in isSett]
    return(isint)


  

def build_contingency(ispat,isint,ptlg='patology',setting='setting'):
    """
    Function to build the contingency table from the contingency lists and to get p-value and odds ratio
    input:
        ptlg==patology to give the name to first column
        setting== setting for which you did the contingency list (e.g. TERAPIA INTENSIVA COVID)
        ispat, isint==the contingency lists
    Output:
        contingency==contingency table
        p==p-value
        OR==odds-ratio
    @Nicola2022
    """
    dp=pd.DataFrame({ptlg.lower() : ispat,
                    setting : isint
                  })
    contingency=pd.crosstab(dp[ptlg.lower()], dp[setting])
    OR, p=fisher_exact(contingency)
    return(contingency,OR, p)

def correct_dates(df,date_column,month_col):
    """
    Function to reorder the dates ina  certain columns taking a value as refenrence for the month,
    If you have a complex dataset with a columns of months and a columns of dates which months are not corresponding
    this fucntion look at those dates and invert days with months,
    The dates are assured to be right...for for example not haveing dates like 2022-44-44 or day greaterr than 31 and months greater
    than 12
    Inputs:
        df== df where to take dates and columns
        date_columns== columns containing the complete dates
        month_col==columns containing the info regarding the month
    Output:
        Same df but with modified dates in the wanted column
    """
    #compare dates month with reference columns of month
    end_dates_month=pd.DatetimeIndex(df[names.key_words.fine]).month
    TrueMonthEnd=df['MESE_x']
    compareEndMonth=end_dates_month==TrueMonthEnd
    i=0
    for x in compareEndMonth:
        if not x:
            day=df['DATA_FINE'].iloc[i].day
            month=df['DATA_FINE'].iloc[i].month
            df['DATA_FINE'].iloc[i]=df['DATA_FINE'].iloc[i].replace(month=day, day=month)
        i=i+1
           
    


    
    
































