# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 11:06:22 2022

@author: nicop
"""
#FUNCTIONS USED FOR THE SCRIPT

##1
# fucntions in order to create a list containing the ID of all the patients with a certain resume (ESITO)
## inputs:
    #dataframe which must contain an ESITO colums
    #key_word is the type of patients we would like to search
def create_target_list(df, key_word):
    target_list=[] #defining the list
    for i in range(0,len(df.index)):
        if key_word in df.ESITO.iloc[i]: #search if the key_word is in the column
            target_list.append(i)
    return(target_list) 