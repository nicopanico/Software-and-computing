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
#FUNCTIONS USED FOR THE SCRIPT

##1
'''
 fucntion in order to create a list containing the ID of all the patients with a certain resume
 inputs:
  df=dataset containing the data
  key_word= word we would like to search in our dataset given as a string
  col_name=name of the column where we would like to search key_word given as a string
  
  '''
def create_target_ID_list(df, key_word, col_name):
   if col_name  not in df.columns:#check if the column is in the dataframe otherwise arise an error and break the cycle
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
    if 'DECEDUTO' not in df.columns:
        raise ValueError('{} is not in the dataframe columns,take a dataset with deceased data'.format('DECEDUTO'))
    else:
       deceased_list=[]
       for i in range(0, len(df.index)):
           if df['DECEDUTO'].iloc[i]==1:
                deceased_list.append(i)
       return(deceased_list)
   

#logging package da vedere!!



































