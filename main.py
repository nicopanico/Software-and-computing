# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 16:04:48 2022

@author: iacop
"""
import pre_processing
import contingency_tables

if '__name__'=='__main__':
    dataset_tracking_bologna_positives=pre_processing.create_tracking_pos_dataset()
    list_cov_setting,list_setting_nocov,list_setting_cov_noint=pre_processing.setting_lists()
    dataset_pos_bolo_cov_int=pre_processing.contingency_datasets(dataset_tracking_bologna_positives,['TERAPIA INTENSIVA COVID'])
    dataset_pos_bolo_no_cov=pre_processing.contingency_datasets(dataset_tracking_bologna_positives,list_setting_nocov)
    dataset_pos_bolo_no_cov_int=pre_processing.contingency_datasets(dataset_tracking_bologna_positives,list_setting_cov_noint)
    
    set_int_results,set_results_no_covid,set_results_covid_noint=contingency_tables.define_contingency_tables(dataset_pos_bolo_cov_int,
                                                                                                    dataset_pos_bolo_no_cov,
                                                                                                dataset_pos_bolo_no_cov_int,
                                                                                            list_setting_nocov,
                                                                                         list_setting_cov_noint )