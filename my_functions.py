# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 11:06:22 2022

@author: nicop
"""
import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as st
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
            
   





































