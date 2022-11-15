# -*- coding: utf-8 -*-


import my_functions as ff
from hypothesis import strategies as st
from hypothesis import settings
from hypothesis import given
from hypothesis.extra.pandas import data_frames, columns
from Classes_for_user.names import key_words as key
from script_modules.pre_processing import contingency_datasets as cntg_dt
from script_modules import pre_processing
import datetime
import pandas as pd

##TESTS OF THE MODULE my_fucntions.py

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
        assert len(test_list)==0, "len of the list expected to be 0 for " ""
    #normal assertion
    elif key_word in set(df[key.setting]):
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
    @Nicola2022
    """   
    outputList=ff.common_elements(list1, list2)
    #assert that the final list has elements from list1 that are not in list 2
    #First convert lists into set
    set2=set(list2)
    assert any(x in set2  for x in outputList)==False, "expected the output list and the list2 to not share elements"
    
        
"""
TESTS for the contingency tables functions
"""
@given(df=data_frames(columns=columns(["SETTING","Descrizione_Esenzione"],dtype=str),
                         rows=st.tuples(
                             st.from_regex("TERAPIA INTENSIVA\ (COVID|NO COVID)",fullmatch=True),
                             st.from_regex("(DIABETE MELLITO|IPERTENSIONE)",fullmatch=True))),
       key_word=st.from_regex("TERAPIA INTENSIVA COVID",fullmatch=True),ptlg=st.from_regex("IPERTENSIONE", fullmatch=True))    
@settings(max_examples = 5)

def test_create_contingency_single(df,ptlg,key_word):
    """
    Test that, given a certain dataset with settings and patologies the fucntion is correcting creating the 2 lists with 'SI'
    and 'NO' for the contingency tables
    Inputs:
       df== dataframe containing setting and patologies columns
       ptlg== one random patology to test
       key_list= list of settings to test the function
    Notes:
       providing empty df gives a message from the function itself
   @Nicola2022
    
    """
    
    if not df.empty:
        ispat,isint=ff.create_contingency_single(df,ptlg,key_word)
        #normal assert on the setting
        if key_word in set(df[key.setting]):
            assert isint.count('SI')==df[key.setting].value_counts()[key_word]   
        else:
            assert isint.count('SI')==0
        #asserts on the patient patology list
        if ptlg in set(df[key.descrizione_esenzione]):
            assert ispat.count('SI')==df[key.descrizione_esenzione].value_counts()[ptlg]
        else:
            assert ispat.count('SI')==0
            
        
       
 
    
@given(df=data_frames(columns=columns(["SETTING","Descrizione_Esenzione"],dtype=str),
                         rows=st.tuples(
                             st.from_regex("TERAPIA INTENSIVA\ (COVID|NO COVID)|OTHER SETTING",fullmatch=True),
                             st.from_regex("(DIABETE MELLITO|IPERTENSIONE)",fullmatch=True))),
       key_list=st.lists(st.from_regex("TERAPIA INTENSIVA \ (COVID|NO COVID)",fullmatch=True),unique=True),ptlg=st.from_regex("IPERTENSIONE", fullmatch=True))    
@settings(max_examples = 5)
def test_create_contingency_multiple(df,ptlg,key_list):  
    """
Test that, given a certain dataset with settings and patologies the fucntion is correcting creating the 2 lists with 'SI'
and 'NO' for the contingency tables
Inputs:
    df== dataframe containing setting and patologies columns
    ptlg== one random patology to test
    key_list= list of settings to test the function
Notes:
    providing empty df gives a message from the function itself
@Nicola2022


"""          
    if not df.empty:
        ispat,isint=ff.create_contingency_multiple(df,ptlg,key_list)
        #normal assert on the settings
        d=df.isin(key_list)
        falsy_check=d['SETTING'].value_counts()[False]
        if falsy_check==len(df.index):
            assert isint.count('SI')==0
        else:
            occurencies=df['SETTING'].value_counts()
            assert isint.count('SI')==occurencies[key_list].sum()
        #asserts on the patient patology list
        if ptlg in set(df[key.descrizione_esenzione]):
            assert ispat.count('SI')==df[key.descrizione_esenzione].value_counts()[ptlg]
        else:
            assert ispat.count('SI')==0
    
    
##TESTS OF THE MODULE pre_processing.py
#test fucntions to create datasets for contingencies

#------------------------------------------------------------------------------
#testing the function create_data_patologies

#test1
df1=pd.DataFrame({'Descrizione_Esenzione':['patol1','patol2'],'ID_PER':[1,2]})
df2=pd.DataFrame({'ID_PER':[1,2]})
def test_create_data_patologies(df_pat=df1,df_ID=df2):
    """
    case1: the ID between 2 datasets are the same
    Test if the function correctly does the merge and groupby of the 2 input dataframes for the patologies and the ID
    Inputs:
        df1==dataframe containing a columns with patologies (Descrizione_Esenzione) and a columsn with patologies
        df2==dataframe containing a columsn with ID
    Outputs:
        Output dataframe has to be correctly merged using ID as a key,
        The Same ID have to be grouped with relative patologies
        df with 2 columns with ID: [1,2] and Decsrizione_Esenzione:[patol1,patol2] and a second
        df with ID:[1,2] the expected output df has to be 2 rows with ID=1 has patol1 and ID=2 has patol2
    """
    dataset_bolo_pat=pre_processing.create_data_patologies(df_pat,df_ID)
    #assert that equal IDs give a df with the same columns of the input df of the ID
    assert(len(dataset_bolo_pat.index))==len(df2.index) 
    #assert that ID=1 has patol1 in the column, which mean that the merge i corretcly assigning the patologies to the right ID
    assert(dataset_bolo_pat['Descrizione_Esenzione'].iloc[0]=='patol1')

#test2
df1=pd.DataFrame({'Descrizione_Esenzione':['patol1','patol2','patol3'],'ID_PER':[1,2,2]})
df2=pd.DataFrame({'ID_PER':[2,4]})
def test_create_data_patologies2(df_pat=df1,df_ID=df2):
    """
    case2: the first dataset has some ID that are repeating becasue they have different patologies 
    Test if the function correctly does the merge and groupby of the 2 input dataframes for the patologies and the ID
    Inputs:
        df1==df containing a columns with patologies (Descrizione_Esenzione) and a columsn with patologies
        df2==df containing a columsn with ID
    Outputs:
        Output dataframe has to be correctly merged using ID as a key,
        The Same ID have to be grouped with relative patologies
        df with 2 columns with ID: [1,2,2] and Decsrizione_Esenzione:[patol1,patol2,'patol3'] and a second
        df with ID:[2,4] the expected output df has to be  rows with ID=1 has patol1 and ID=2 has patol2,patol3
        to be sure the groupby is working correctly
        
    """
    dataset_bolo_pat=pre_processing.create_data_patologies(df_pat,df_ID)
    #assert that ID=2 has patol2,patol3 in the column, which mean that the groupby is working as intended
    data_test=dataset_bolo_pat
    patol_id=data_test[data_test['Descrizione_Esenzione'].isin(['patol2,patol3'])]
    assert patol_id.index==2


#test3
df1=pd.DataFrame({'Descrizione_Esenzione':['patol1','patol2','patol3'],'ID_PER':[1,2,2]})
df2=pd.DataFrame({'ID_PER':[5,6]})
def test_create_data_patologies3(df_pat=df1,df_ID=df2):
    """
    case3: no common ID
    Test if the function correctly does the merge and groupby of the 2 input dataframes for the patologies and the ID
    Inputs:
        df1==df containing a columns with patologies (Descrizione_Esenzione) and a columsn with patologies
        df2==df containing a columsn with ID which are different from the other df1
    Outputs:
        Output dataframe has to be correctly merged using ID as a key,
        The output df has to be formed by 2 rows with NaN in Descrizione_Esenzione and ID=5,6
        check the NaN to be corrected into strings
    """
    dataset_bolo_pat=pre_processing.create_data_patologies(df_pat,df_ID)
    #assert that ID=2 has patol2,patol3 in the column, which mean that the groupby is working as intended
    data_test=dataset_bolo_pat
    patol=data_test['Descrizione_Esenzione']
    assert((patol=='NaN').value_counts()[True])==2
    assert patol.index==2

#------------------------------------------------------------------------------
#Test the function create_data_settings
#test1
df1=pd.DataFrame({'SETTING':['sett1','sett2'],'ID_PER':[1,2]})
df2=pd.DataFrame({'ID_PER':[1,2]})
def test_create_data_settings(df_sett=df1,df_ID=df2):
    """
    case1: common IDs, the ID of the settings are the same in the ID reference df
    Test if the fucntion correctly does the merge for the 2 df of settings and IDs
    Inputs:
        df1==df containing a columns with setting and a column with ID
        df2==df containing a columns with all the IDs
    Outputs:
        Output df has to be correclty merged
        If the ID are shared the expected df have 2 rows with sett1 for ID=1 anbd sett2 for ID=2
    """
    test_df=pre_processing.create_data_settings(df_sett,df_ID)
    assert(len(test_df.index))==len(df2.index)
    assert(test_df['SETTING'].iloc[0]=='sett1')#to test if it correclty merging the ID=1 witht the setting: sett1

#test2
df1=pd.DataFrame({'SETTING':['sett1','sett2'],'ID_PER':[1,2]})
df2=pd.DataFrame({'ID_PER':[2,4]})
def test_create_data_settings2(df_sett=df1,df_ID=df2):
    """
    Test if the fucntion correclty does the merge in the case which the IDs of the 2 df are not all the same, taking
    the IDs of df2 as reference and also check that the NaN are properly filled with "NaN"
     Inputs:
        df1==df containing a columns with setting and a column with ID
        df2==df containing a columns with all the IDs
    Outputs:
        Output dataframe has to be correclty merged
        If the ID are not totally shared, the expected df have 2 rows with the IDs from df2 one ID with sett2 and the other with
        NaN properly filled as a string
    """
    test_df=pre_processing.create_data_settings(df_sett,df_ID)
    sett=test_df['SETTING']
    assert((sett=='NaN').value_counts()[True])==1
    assert sett.size==2
#------------------------------------------------------------------------------
#testing the function create_pos_outcome
#test1
df1=pd.DataFrame({'ID_PER':[1,2,2,2,3,3,4],'ESITO':['MALATTIA_IN_CORSO','Guarito',
                                                     'Guarito','Guarito','Guarito','Guarito','DECESSO']})
def test_crate_pos_outcome(df_pos=df1):
    """
    Test that the fucntion correclty takes into account only patients who are recovered or deceased from covid and not the one
    with the covid on-going
    Inputs:
        df1==df with the ID of the positives with the status of the covid in the column ESITO
    Outputs:
        Output dataframe has to have only patients with the covid recovered or dead from covid
        and the duplicates have to be properly dropped, so the final df is expetced to have 3 rows with IDs=[2,3,4]
    """
    test_df=pre_processing.create_pos_outcome(df_pos)
    status=test_df['ESITO']
    stillpos=status.str.contains('MALATTIA_IN_CORSO')
    #assert that there are no patients with covid still going
    assert test_df[stillpos].empty
    #assert that that the duplicates have been dropped
    assert len(test_df.index)==3

#------------------------------------------------------------------------------
#test the fucntion create_tracking_pos_dataset

#test1
df1=pd.DataFrame({'SETTING':['sett1','sett2','sett3','sett4'],'ID_PER':[1,2,3,4]})
df2=pd.DataFrame({'Descrizione_Esenzione':['patol1','patol2','patol3','patol4'],'ID_PER':[1,2,3,4]})
df3=pd.DataFrame({'ESITO':['pos','pos','pos','pos'],'ID_PER':[1,2,3,4]})
def test_create_tracking_pos_dataset(df_pat=df1,df_sett=df2, df_out=df3):
    """
    Test that the fucntion correclty creates a dataset with all the tracking for positives 
    with settings, patologies for the positive IDs
    Inputs:
        df1==df of the patologies with IDs
        df2== df of the settings with the IDs
        df3== containing the positive patients
    Outputs:
        The expected output df has to be correclty merged only for positive IDs containing for each ID its settings and
        patologies
        The test is expected to give as output a dataframe with 4 IDs with their setting and patol
        In the script this fucntion uses as input the df created in the previous 3 fucntion :
            create_data_patologies, create_data_setting, create_pos_outcome
            so it is already tested that the input df will be as wanted,
            Test that the inner merge will take the IDs as intended
        
    """
    test_df=pre_processing.create_tracking_pos_dataset(df_pat,df_sett,df_out)
    #test the ID to be taken in the correct way, expected to be 4
    assert len(test_df['ID_PER'])==4

#------------------------------------------------------------------------------

























@given(df=data_frames(columns=columns(["SETTING"],dtype=str),
                         rows=st.tuples(
                             st.from_regex("TERAPIA INTENSIVA\ (COVID|NO COVID)|OTHER SETTING",fullmatch=True),
                             )),settlist=st.lists(st.from_regex("TERAPIA INTENSIVA \ (COVID|NO COVID)",fullmatch=True),min_size=1,unique=True))
@settings(max_examples = 5)      
def test_contingency_datasets(df,settlist):
    if not df.empty:
        dataset_final=cntg_dt(df,settlist)
        if not dataset_final.empty:
            #first check that dataset final contains the wanted settings and the non hospitalized
            counts=dataset_final.SETTING.isin(settlist).value_counts()[True]
            df_counts=df.SETTING.isin(settlist).value_counts()[True]
            assert counts==df_counts, "Not the same values, you are missing some values"
            assert len(dataset_final.index)==df_counts
   
    
   
@given(df=data_frames(columns=columns(["DATA_INIZIO","MESE_y","DATA_FINE","MESE_x"],dtype=str),
                         rows=st.tuples(
                             st.datetimes(min_value=datetime.datetime(2020, 1, 1), max_value=datetime.datetime(2020, 1, 12),allow_imaginary=False),
                             st.integers(min_value=1,max_value=12),
                             st.datetimes(min_value=datetime.datetime(2020, 1, 1), max_value=datetime.datetime(2020, 1, 12),allow_imaginary=False),
                             st.integers(min_value=1,max_value=12)
                             )))
@settings(max_examples = 5)    

def test_correct_dates(df):
    
    """
    Test that the fucntion correctly exchanges the moth with the day in case the corresponding value in the columns
    mese doest not match with the motnh in the datetime
    simple datframe given as input ,the test only assures that the switch is done properly under the fucntion conditions

    """
    if not df.empty:
        months=[]
        days=[]
        for i in range(0,len(df.index)):
            months.append(df.DATA_INIZIO.iloc[i].month)
            days.append(df.DATA_INIZIO.iloc[i].day)
            
        df_corr=ff.correct_dates(df)
        
        months_corr=[]
        days_corr=[]
        for i in range(0,len(df_corr.index)):
            months_corr.append(df_corr.DATA_INIZIO.iloc[i].month)
            days_corr.append(df_corr.DATA_INIZIO.iloc[i].day)
        
        for i in range(0, len(df_corr.index)):
            if df.DATA_INIZIO.iloc[i].month != df.MESE_y.iloc[i]:
                assert months_corr[i]!=months[i]
                assert days_corr[i] != days[i]
            
        
        
        
    
      
    
    
    
    
    
    
    
                       
    
if __name__ == "main":
    pass                
    