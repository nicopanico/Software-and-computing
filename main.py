# -*- coding: utf-8 -*-

import os,sys
sys.path.append(os.path.dirname(os.path.realpath(__file__))) #to take the working dir as the curretn script directory

from script_modules import pre_processing,contingency_tables,Kaplan_Meier

"""
----------------
.. MAIN SCRIPT..
----------------
"""

#importing all the datasets for the analysis
dataset_tracking_bologna_positives=pre_processing.create_tracking_pos_dataset()#dataset for contingencies
list_cov_setting,list_setting_nocov,list_setting_cov_noint=pre_processing.setting_lists()#lists of settings 
df_for_KM,list_ID,sex_bolo=pre_processing.pre_processing_KM()#structures used for the kaplan-meier

#contingency analysis
dataset_pos_bolo_cov_int=pre_processing.contingency_datasets(dataset_tracking_bologna_positives,'TERAPIA INTENSIVA COVID')
dataset_pos_bolo_no_cov=pre_processing.contingency_datasets(dataset_tracking_bologna_positives,list_setting_nocov)
dataset_pos_bolo_no_cov_int=pre_processing.contingency_datasets(dataset_tracking_bologna_positives,list_setting_cov_noint)

set_int_result=contingency_tables.define_contingency_table_single(dataset_pos_bolo_cov_int,
                                                                                     'TERAPIA INTENSIVA COVID',
                                                                                     'Terapia intensiva covid')
set_covid_no_int_result=contingency_tables.define_contingency_table_multiple(dataset_pos_bolo_no_cov_int,
                                                                                     list_setting_cov_noint,
                                                                                     'covid settings without terapia int.')
set_no_covid_result=contingency_tables.define_contingency_table_multiple(dataset_pos_bolo_no_cov,
                                                                                     list_setting_nocov,
                                                                                     'non covid settings')
contingency_tables.show_contingency_results(set_no_covid_result,set_int_result,set_covid_no_int_result)

#Kaplan-Meierfitting and plots
keplan_meier_db=Kaplan_Meier.kaplan_meier_dataset(df_for_KM,list_ID,sex_bolo)#create the right dataset for the kfm fitter
kfm=Kaplan_Meier.kfm_fitter(keplan_meier_db)#perform the fitting
Kaplan_Meier.show_plots_kfm(kfm)#first plots for generics kfm
Kaplan_Meier.show_plots_kfm_cumulative(kfm)
Kaplan_Meier.plot_M_F_fitter(keplan_meier_db,kfm)#kfm for distinction male and female