# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 16:04:48 2022

@author: iacop
"""
import os,sys
sys.path.append(os.path.dirname(os.path.realpath(__file__))) #to take the working dir as the curretn script directory

import pre_processing
import contingency_tables


# if '__name__'=='__main__':
dataset_tracking_bologna_positives=pre_processing.create_tracking_pos_dataset()
list_cov_setting,list_setting_nocov,list_setting_cov_noint=pre_processing.setting_lists()
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
    