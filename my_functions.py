# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 11:06:22 2022

@author: nicop
"""
#FUNCTIONS USED FOR THE SCRIPT

##1
'''
 fucntions in order to create a list containing the ID of all the patients with a certain resume
 inputs:
  df=dataset containing the data
  key_word= word we would like to search in our dataset given as a string
  col_name=name of the column where we would like to search key_word given as a string
  
    '''
def create_target_list(df, key_word, col_name):
    target_list=[] #defining the list
    for i in range(0,len(df.index)):
        if key_word in df[col_name].iloc[i]: #search if the key_word is in the column
            target_list.append(i)
    return(target_list) 
