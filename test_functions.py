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
import pandera as pa


schema = pa.DataFrameSchema({
    
    "column1": pa.Column(str
    ),
})
@given(schema.strategy(size=5))
def test_create_target_ID_list(schema,key_word,col_name):

    test_list=create_target_list(schema, key_word, col_name)
    assert len(test_list)==len(schema.columns), f"expected the same number"
    

    

    
    
    
    
    
    
    
    
    
    
    
if __name__ == "main":
    pass                
    