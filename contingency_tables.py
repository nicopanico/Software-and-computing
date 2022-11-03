# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 17:27:36 2022

@author: iacop
"""
#importing packages
import pandas as pd
import my_functions as ff
from Classes_for_user.sett_hosp import hospital as hosp
from Classes_for_user.sett_hosp import SettingList as settlist
from Classes_for_user.names import key_words as key
from Classes_for_user.patology import patologies as pat
from Classes_for_user.init_data import covid_data as data


trial_list=pat.patlist
def define_contingency_tables(df1, df2, df3,list1,list2,trial_list=trial_list):

    # First contingency
    set_int_results={}
    for ptlg in trial_list:
        ispat,isint=ff.create_contingency_single(df1,ptlg,hosp.intensiva_covid)
        contingency, OR, p = ff.build_contingency(ispat,isint,ptlg,'Intensiva Covid')
        set_int_results[ptlg] = [OR,p]
       
    
    
    # Second contingency
    set_results_no_covid={}
    for ptlg in trial_list:
        ispat,isint = ff.create_contingency_multiple(df2,ptlg,list1)
        contingency, OR, p = ff.build_contingency(ispat,isint,ptlg,'Setting no covid')
        set_results_no_covid[ptlg] = [OR,p]
        
        
        
    
    
    # Third contingency
    set_results_covid_noint={}
    for ptlg in trial_list:
        ispat,isint = ff.create_contingency_multiple(df3,ptlg,list2)
        contingency,  OR, p = ff.build_contingency(ispat,isint,ptlg,'Setting covid without intensive care')
        set_results_covid_noint[ptlg] = [OR, p]
        
    return(set_int_results,set_results_no_covid,set_results_covid_noint)
    


def show_contingency_results(list1,list2,list3):
    OD_compare=pd.DataFrame.from_dict([list1,list2,list3])
    OD_compare=OD_compare.rename(index={0:'setting no covid',2:'covid intensive care',1:'covid settings no int'})
    print(OD_compare)