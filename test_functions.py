# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 11:42:15 2022

@author: nicop
"""
import my_functions
import pandas as pd
import hypothesis
from hypothesis import strategies as st
from hypothesis import settings
from hypothesis import given
from hypothesis.extra.pandas import data_frames, columns, column
import pandera as pa
import names
import sett_hosp




df=data_frames(columns=columns(["SETTING","ID"],dtype=str),
                         rows=st.tuples(
                             st.from_regex("TERAPIA INTENSIVA\ (COVID|NO COVID)",fullmatch=True),
                             st.from_regex("PAT\-[0-9]",fullmatch=True))).example()
def test_create_target_ID_list(df=df,key_word=sett_hosp.hospital.intensiva_covid,col_name=names.names.setting):
    """
    Test that given a certain dataset with random rows the fucntion append in the list only the rows with the wanted 
    Key word
    As input:
        Dataframe with 2 columns and random number of rows
        key_word as the word the want to search 
        column_name as the column where we want to search for it
    As output:
        list with the rows that contained the key_word
    Notes:
        if you provide a columns_name non existent you will get an error message from the function itself as default
        nothing happens if you search for a key_word that does not exist in the column_name.....your list will be len==0
    """
    
    test_list=my_functions.create_target_ID_list(df, key_word, col_name)
    assert len(test_list)==df[col_name].value_counts()[key_word], f"expected the same number"
    

   
df=data_frames(columns=columns(["DECEDUTO"],dtype=str),
                        rows=st.tuples(
                             st.integers(0,1))).example()
def test_deceased_list(df=df):
    """
    Test that given a dataset containing a deceased column the fucntion appends in the colums only the rows that have
    1 as value for deceased
    As input:
        Dataframe with a deceased column
    As output:
        list containing the row numbers of the deceased patients
    """
    isdead=my_functions.deceased_list(df)
    assert len(isdead)==df.loc[df.DECEDUTO == 1, 'DECEDUTO'].count(), f"expected the same number"
     
                                
    
    
    
    
    
    
    
    
if __name__ == "main":
    pass                
    