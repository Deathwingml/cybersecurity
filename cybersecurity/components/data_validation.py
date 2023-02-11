import pandas as pd
import numpy as np 
from scipy.stats import ks_2samp
import os, sys
from typing import Optional

from cybersecurity.exception import CSecurityException
from cybersecurity.logger import logging
from cybersecurity.entity import config_entity, artifact_entity
from cybersecurity import utils



class DataValidation:

    def __init__(self, data_validation_config:config_entity.DataValidationConfig, 
    data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
       
        try:
            logging.info(f"{'>>'*20} Data Validation {'<<'*20}")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.validation_error = dict()
        except Exception as e:
            raise CSecurityException(e, sys)


    def drop_missing_value_columns(self,df:pd.DataFrame,report_key_name:str)->Optional[pd.DataFrame]:
        '''
        This functions will drop columns with missing values more than 50%

        df: Accepts a pandas dataframe
        threshold: percentage criteria to drop a columns
        ==================================================================
        returns pandas dataframe if atleast 1 columns is available after dropping columns with missing values
        '''
        try:
            threshold = self.data_validation_config.missing_threshold
            logging.info(f"checking for columns with null values greater than threshold")
            null_report = df.isna().sum()/df.shape[0]
            logging.info(f"dropping columns with null values more than the threshold")
            drop_column_names = null_report[null_report > threshold].index

            logging.info(f"Columns to drop:{list(drop_column_names)}")
            self.validation_error["dropped_columns"] = list(drop_column_names)
            df.drop(list(drop_column_names), axis=1, inplace=True)
            logging.info(f"checking the number of columns after dropping is == 0")
            if len(df.columns)==0:
                logging.info(f"no columns to return")
                return None
            logging.info(f"returning remaining columns in a dataframe")
            return df

        except Exception as e:
            raise CSecurityException(e, sys)


    
    def is_req_column_exists(self, base_df:pd.DataFrame, current_df:pd.DataFrame, report_key_name:str)->bool: #fucntion to check if required columns exists
        try:
            logging.info(f"reading base and current columns")
            base_columns = base_df.columns
            current_columns = current_df.columns

            missing_columns = []
            for base_column in base_columns:
                if base_column not in current_columns:
                    logging.info(f"column:[{base_column} is not available]")
                    missing_columns.append(base_columns)

            if len(missing_columns)>0:
                self.validation_error[report_key_name]= missing_columns
                return False
            return True

        except Exception as e:
            raise CSecurityException(e, sys)


    def data_drift(self, base_df:pd.DataFrame, current_df:pd.DataFrame,report_key_name:str): #not returning anyting from this function. Just generating a data drift report
        try:
            drift_report = dict()
            base_columns = base_df.columns
            current_columns = current_df.columns

            for base_column in base_columns:
                base_data, current_data = base_df[base_column],current_df[base_column]
                logging.info(f"checking Null hypothesis: both column data drawn from same distribution")
                #Null hypothesis: both column data drawn from same distribution
                logging.info(f"Hypothesis {base_column}: {base_data.dtype}, {current_data.dtype} ")
                same_distribution = ks_2samp(base_data, current_data)

                if same_distribution.pvalue > 0.05:
                    logging.info(f"Accepting null hypothesis")
                    #we are accepting null hypothesis
                    drift_report[base_column]={
                        "pvalue":float(same_distribution.pvalue),
                        "same_distribution": True
                    }
                    
                else:
                    logging.info(f"Rejecting null hypothesis")
                    drift_report[base_column] = {
                        "pvalues": float(same_distribution.pvalue),
                        "same_distribution": False
                    }

            self.validation_error[report_key_name]=drift_report

        except Exception as e:
            raise CSecurityException(e, sys)


    def initiate_data_validation(self)->artifact_entity.DataValidationArtifact:
        try:
            logging.info(f"Reading base dataframe")
            base_df = pd.read_csv(self.data_validation_config.base_file_path)
            logging.info(f"replacing na with np.NAN")
            base_df.replace({"na":np.NAN}, inplace = True)

            #base_df has null
            logging.info(f"droping null value columns from base df")
            base_df = self.drop_missing_value_columns(df=base_df, report_key_name="missing_value_base_dataset")
            logging.info(f"Reading train dataframe")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            logging.info(f"Reading test dataframe")
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            #dropping categorical columns
            #logging.info(f"dropping categorical columns in base_df, train_df, test_df")
            #base_df = base_df[[column for column in base_df.columns if base_df[column].dtype != 'O']]
            #train_df = train_df[[column for column in train_df.columns if train_df[column].dtype != 'O']]
            #test_df = test_df[[column for column in test_df.columns if test_df[column].dtype != 'O']]

            logging.info(f"excluding non-float columns in base_df, train_df, test_df") #this can be dynamically done by wrtting a line to exclude categorical columns like in the code above
            exclude_columns = ['URL','Label','domain_match','path_match','query_string_match','fragment_match']
            base_df = utils.convert_columns_float(df = base_df, exclude_columns = exclude_columns)
            train_df = utils.convert_columns_float(df = train_df, exclude_columns = exclude_columns)
            test_df = utils.convert_columns_float(df = test_df, exclude_columns = exclude_columns)

            logging.info(f"checking if all the required columns are present in train df")
            tarin_df_column_status = self.is_req_column_exists(base_df = base_df, current_df=train_df, report_key_name="missing_column_train_dataset")
            logging.info(f"checking if all the required columns are present in test df")
            test_df_column_status = self.is_req_column_exists(base_df = base_df, current_df=test_df, report_key_name="missing_column_test_dataset")

            if tarin_df_column_status:
                logging.info(f"All columns available in train df. Checking for data drift")
                self.data_drift(base_df=base_df, current_df=train_df, report_key_name="data_drift_in_train_dataset")
                logging.info(f"No drift in train df")

            if test_df_column_status:
                logging.info(f"All columns available in test df. Checking for data drift")
                self.data_drift(base_df=base_df, current_df=train_df, report_key_name="data_drift_in_test_dataset")
                logging.info(f"No drift in test df")

            #write the report
            logging.info(f"Wrting the yaml report")
            utils.write_yaml_file(file_path=self.data_validation_config.report_file_path, data= self.validation_error)

            data_validation_artifact = artifact_entity.DataValidationArtifact(report_file_path =self.data_validation_config.report_file_path)
            logging.info(f"Data Validation artifact:{data_validation_artifact}")
            return data_validation_artifact

        except Exception as e:
            raise CSecurityException(e, sys)