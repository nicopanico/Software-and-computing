# -*- coding: utf-8 -*-

#importing packages
import pandas as pd
import my_functions as ff
from Classes_for_user.sett_hosp import hospital as hosp
from Classes_for_user.sett_hosp import SettingList as settlist
from Classes_for_user.names import key_words as key
from Classes_for_user.patology import patologies as pat
from Classes_for_user.init_data import covid_data as data


trial_list=pat.patlist
def define_contingency_table_single(df, sett,table_name,patology=trial_list):
    """
    function to create contingencies and to append OR and p-value for all the patologies
    using the already tested fucntions for contingency (for a single setting)
    Inputs:
        df==dataframe already prepared for contingency
        sett==list containing the setting where you want to build the contingencies
        table_name==string variable to give a name to table column
        patology=trial list as default takes the patologies chosen a priori but can be modified with the lsit that you prefer to test
    Output:
        set_int_result==set containing p-value and OR taken from contingencies forr each patology
    @Nicola2022
    """

    
    set_int_results={}
    for ptlg in trial_list:
        ispat,isint=ff.create_contingency_single(df,ptlg,sett)
        contingency, OR, p = ff.build_contingency(ispat,isint,ptlg,table_name)
        set_int_results[ptlg] = [OR,p]
    return(set_int_results)
       
    
def define_contingency_table_multiple(df, sett_list,table_name,patology=trial_list):
    """
    function to create contingencies and to append OR and p-value for all the patologies
    using the already tested fucntions for contingency (for a list of settings)
    Inputs:
        df==dataframe already prepared for contingency
        sett_list==list containing the setting where you want to build the contingencies
        table_name==string variable to give a name to table column
        patology=trial list as default takes the patologies chosen a priori but can be modified with the lsit that you prefer to test
    Output:
        set_int_result==set containing p-value and OR taken from contingencies forr each patology
    @Nicola2022
    """ 
     
    set_int_result={}
    for ptlg in trial_list:
        ispat,isint = ff.create_contingency_multiple(df,ptlg,sett_list)
        contingency, OR, p = ff.build_contingency(ispat,isint,ptlg,table_name)
        set_int_result[ptlg] = [OR,p]
        
    return(set_int_result)
        
        
        
    
    
   


def show_contingency_results(list1,list2,list3):
    """
    Fucntion to show the reuslts of the contingency analisys
    give the table containing the OD and p-value for all the patologies for all the 3 trials
    @Nicola2022
    """

    
    OD_compare=pd.DataFrame.from_dict([list1,list2,list3])
    OD_compare=OD_compare.rename(index={0:'setting no covid',2:'covid intensive care',1:'covid settings no int'})
    return(OD_compare)
 