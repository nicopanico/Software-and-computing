# -*- coding: utf-8 -*-

import os,sys
sys.path.append(os.path.dirname(os.path.realpath(__file__))) #to take the working dir as the curretn script directory
from Classes_for_user.init_data import covid_data as data
from script_modules import pre_processing,contingency_tables,Kaplan_Meier

"""
----------------
.. MAIN SCRIPT..
----------------
"""
#START OF THE CODE
#PRE PROCESS DATA FOR CONTINGENCIES ANALYSIS
dataset_bolo_patologies=pre_processing.create_data_patologies(data.patologies,data.ID_Bologna)
dataset_bolo_setting=pre_processing.create_data_settings(data.analysis_entries_updated,data.ID_Bologna)
database_pos_outcome=pre_processing.create_pos_outcome(data.positivi_unibo)
dataset_tracking_bologna_positives=pre_processing.create_tracking_pos_dataset(dataset_bolo_patologies,dataset_bolo_setting,database_pos_outcome)

#lists of settings
list_cov_setting,list_setting_nocov,list_setting_cov_noint=pre_processing.setting_lists()#lists of settings 
#PRE PROCESS DATA FOR KM ANALYSIS
dataset_bolo_exit_pos=pre_processing.create_dataset_exit(database_pos_outcome,data.ID_Bologna,data.analisi_uscite_updated)
dataset_bolo_hospital_path_pos=pre_processing.create_dataset_hospital_path(dataset_bolo_exit_pos,data.analysis_entries_updated)
df_pos_rec_KM=pre_processing.create_dataset_KM(dataset_bolo_hospital_path_pos,database_pos_outcome)
sex_bolo=pre_processing.create_df_sex(data.anag_comune_bo)
ID_list=pre_processing.create_intensive_ID_list(dataset_bolo_hospital_path_pos)
                                                    


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
OD_compare=contingency_tables.show_contingency_results(set_no_covid_result,set_int_result,set_covid_no_int_result)

#Kaplan-Meierfitting and plots
keplan_meier_db=Kaplan_Meier.kaplan_meier_dataset(df_pos_rec_KM,ID_list,sex_bolo)#create the right dataset for the kfm fitter
kfm=Kaplan_Meier.kfm_fitter(keplan_meier_db)#perform the fitting
Kaplan_Meier.show_plots_kfm(kfm)#first plots for generics kfm
Kaplan_Meier.show_plots_kfm_cumulative(kfm)
Kaplan_Meier.plot_M_F_fitter(keplan_meier_db,kfm)#kfm for distinction male and female