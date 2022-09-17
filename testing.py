# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 11:42:15 2022

@author: nicop
"""
import my_functions
from hypothesis import given
import hypothesis
from hypothesis import strategies as st
from hypothesis import settings
import pandas as pd


def test_create_target_list(df,key_word,col_name):
    assert col_name in df.columns,f"Assert error: column {col_name} not in dataframe"
    test_list=create_target_list(df, key_word, col_name)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
if __name__ == "main":
    pass                
    