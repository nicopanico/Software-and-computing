# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 11:42:15 2022

@author: nicop
"""
import my_functions as ff
import pandas as pd
import hypothesis
from hypothesis import strategies as st
from hypothesis import settings
from hypothesis import given
from hypothesis.extra.pandas import data_frames, columns, column
import pandera as pa
from Classes_for_user import names,sett_hosp,patology





@given(df=data_frames(columns=columns(["SETTING","ID"],dtype=str),
                         rows=st.tuples(
                             st.from_regex("TERAPIA INTENSIVA\ (COVID|NO COVID)",fullmatch=True),
                             st.from_regex("PAT\-[0-9]",fullmatch=True))),key_word=st.from_regex("TERAPIA INTENSIVA COVID",fullmatch=True),col_name=st.from_regex("SETTING", fullmatch=True))

       
@settings(max_examples = 5)

def test_create_target_ID_list(df,key_word,col_name):
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
    @Nicola2022
    """
    
    
    test_list=ff.create_target_ID_list(df, key_word, col_name)
    
    #first check on the empty dataframe to see if it gets an empty list
    if df.empty:
        assert len(test_list)==0, "Empty dataframe should get list with no values"
    #chech on the keyword, if it is tha falsy value " " it gives you an empty list
    elif not key_word:
        assert len(test_list)==0, "expected to be 0"
    #normal assertion
    else:
        assert len(test_list)==df[col_name].value_counts()[key_word], "expected the same number "

   
@given(df=data_frames(columns=columns(["DECEDUTO"],dtype=str),
                        rows=st.tuples(
                             st.integers(0,1))))
@settings(max_examples = 5)
def test_deceased_list(df):
    """
    Test that given a dataset containing a deceased column the fucntion appends in the colums only the rows that have
    1 as value for deceased
    As input:
        Dataframe with a deceased column
    As output:
        list containing the row numbers of the deceased patients
    @Nicola2022
    """
    isdead=ff.deceased_list(df)
    assert len(isdead)==df.loc[df.DECEDUTO == 1, 'DECEDUTO'].count(), "expected the same number"


     
@given(list1=st.lists(st.integers()),
list2=st.lists(st.integers()))
@settings(max_examples = 5)

def test_common_elements(list1,list2):
    """
    test if the fucntion is correcting removing common elements of the 2 lists from list1
    """   
    outputList=ff.common_elements(list1, list2)
    #assert that the final list has elements from list1 that are not in list 2
    #First convert lists into set
    set2=set(list2)
    assert any(x in set2  for x in outputList)==False, "expected the output list and the list2 to not share elements"
    
        
                        
    
    
    
    
    
    
    
    
if __name__ == "main":
    pass                
    