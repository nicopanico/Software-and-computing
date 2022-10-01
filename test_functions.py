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

@given(df=data_frames(columns=columns(["SETTING","OTHER"],dtype=str),
                         rows=st.tuples(
                             st.from_regex("TERAPIA INTENSIVA\[COVIDNOCOVID]",fullmatch=True),
                             st.from_regex("bu\-[0-9]",fullmatch=True)))
                 
def test_create_target_ID_list(df,key_word,col_name):

    test_list=my_functions.create_target_ID_list(df, key_word, col_name)
    assert len(test_list)==len(schema.columns), f"expected the same number"
    

    

    
    
    
    
    
    
    
    
    
    
    
if __name__ == "main":
    pass                
    