# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 11:06:22 2022

@author: nicop
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stat
import statistics
from scipy.stats import chi2_contingency
from scipy.stats import fisher_exact
from Classes_for_user import names,sett_hosp,patology
#FUNCTIONS USED FOR THE SCRIPT

##1

def create_target_ID_list(df, key_word, col_name):
    '''
 function in order to create a list containing the ID of all the patients with a certain resume
 inputs:
    df=dataset containing the data
    key_word= word we would like to search in our dataset given as a string
    col_name=name of the column where we would like to search key_word given as a string
    @Nicola-2022
  
  '''
    if df.empty:
        target_list=[]
    else:
       if col_name  not in df.columns:
           raise ValueError('{} is not in the dataframe columns'.format(col_name))
       else:
         target_list=[] #defining the list
         for i in range(0,len(df.index)):              
            if key_word in df[col_name].iloc[i]: #search if the key_word is in the column
                       target_list.append(i)
            else:
                continue
                          
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
     if names.names.deceduto not in df.columns:
        raise ValueError('{} is not in the dataframe columns,take a dataset with deceased data'.format('DECEDUTO'))
     else:
       deceased_list=[]
       for i in range(0, len(df.index)):
           if df['DECEDUTO'].iloc[i]==1:
                deceased_list.append(i)
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
            


def create_contingency_single(df,ptlg,key_word):
    """
    Function in order to get the lists to build a contingency table for a single key_word
    Input:
        df==dataframe to give as input to build the lists
        ptlg==name of the patology to build the contingency lists
        key_word==setting to take as reference to check the patology
    Output:
        ispat==list containing 'SI' for the aptient who have the patology 'NO' otherwise
        isin==list containing 'SI' for the patients who are in the key_word setting 'NO' otherwise
    @Nicola2022
    """
    if df.empty:
        print("Can't get any List with an empty df")
        return
    else:
 
       ispat=[]
       isint=[]
   
       for i in range(0, len(df.index)):
            if ptlg in df[names.names.descrizione_esenzione].iloc[i]:
                ispat.append('SI')
            else:
              ispat.append('NO')
            if key_word in df[names.names.setting].iloc[i]:
               isint.append('SI')
            else:
              isint.append('NO')
       
       return(ispat,isint)


def create_contingency_multiple(df,ptlg,key_list):
    """
    Function in order to get the lists  to build a contingency table for a key_list
    Input:
        df==dataframe to give as input to build the lists
        ptlg==name of the patology to build the contingency lists
        key_list==settings to take as reference to check the patology (given as a list of strings saying all the setting where you would like to search the ptlg)
    Output:
        ispat==list containing 'SI' for the aptient who have the patology 'NO' otherwise
        isin==list containing 'SI' for the patients who are in the key_list settings 'NO' otherwise
    @Nicola2022
    """
    if df.empty:
        print("Can't get any List with an empty df")
        return
    else:
      ispat=[]
      isint=[]
      for i in range(0, len(df)):
                if ptlg in df[names.names.descrizione_esenzione].iloc[i]:
                    ispat.append('SI')
                else:
                    ispat.append('NO')
                found=False
                for k in key_list:
                    if k in df[names.names.setting].iloc[i] and not found:
                        isint.append('SI')
                        found=True
                if not found:
                    isint.append('NO')
      return(ispat,isint)





































