from cybersecurity import utils
from cybersecurity.entity import config_entity
from cybersecurity.entity import artifact_entity
from cybersecurity.exception import CSecurityException
from cybersecurity.logger import logging
import pandas as pd 
import numpy as np 
import os, sys
from sklearn.model_selection import train_test_split


class DataIngestion:
    
    def __init__(self, data_ingestion_config:config_entity.DataIngestionConfig):
        try:
            logging.info(f"{'>>'*20} Data Ingestion {'<<'*20}")
            self.data_ingestion_config = data_ingestion_config
        
        except Exception as e:
            raise CSecurityException(e, sys)


    def initiate_data_ingestion(self)->artifact_entity.DataIngestionArtifact:
        try:
            logging.info(f"Exporting collection data as pandas dataframe")
            #exporting collection data as pandas dataframe
            df:pd.DataFrame = utils.get_collection_as_dataframe(
                database_name=self.data_ingestion_config.database_name, 
                collection_name= self.data_ingestion_config.collection_name)

            #logging.info(f"extracting only numperic columns from the dataset")
            #converting df to df-numeric
            #df = df[[column for column in df.columns if df[column].dtype != 'O']]

            logging.info(f"replace na with np.NAN")
            #save data in feature store
            df.replace(to_replace = "na", value = np.NAN, inplace = True)

            logging.info(f"create feature store if not available")
            #create feature store if not available
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir, exist_ok = True)

            logging.info(f"save df to feature store folder")
            #save df to feature store folder
            df.to_csv(path_or_buf = self.data_ingestion_config.feature_store_file_path, index = False, header = True)

            logging.info(f"split dataset into train and test")
            #split dataset into train and test
            train_df, test_df = train_test_split(df, test_size = self.data_ingestion_config.test_size, 
                                                    train_size = self.data_ingestion_config.train_size, 
                                                    random_state = self.data_ingestion_config.random_state)

            logging.info("create dataset directory folder if not available")
            #create dataset directory folder if not available
            dataset_dir = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_dir,exist_ok=True)
            

            logging.info(f"save test and train split to feature store folder")
            #save the test and train split to feature store folder
            train_df.to_csv(path_or_buf = self.data_ingestion_config.train_file_path, index = False, header = True)
            train_df.to_csv(path_or_buf = self.data_ingestion_config.test_file_path, index = False, header = True)

            logging.info(f"preparing artifact")
            #prepare artifact
            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                feature_store_file_path=self.data_ingestion_config.feature_store_file_path,
                train_file_path=self.data_ingestion_config.train_file_path, 
                test_file_path=self.data_ingestion_config.test_file_path)

            logging.info(f"DataIngestionArtifact: {data_ingestion_artifact}")
            return data_ingestion_artifact

        except Exception as e:
            raise CSecurityException(e, sys)
