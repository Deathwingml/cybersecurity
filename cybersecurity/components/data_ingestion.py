from cybersecurity import utils
from cybersecurity.entity import config_entity
from cybersecurity.entity import artifact_entity
from cybersecurity.exception import CSecurityException
from cybersecurity.logger import logging
from cybersecurity.config import CHARACTER_LIST
import pandas as pd 
import numpy as np 
import os, sys
import re
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

            def extract_url_info(url):
                try:
                    domain_match = re.search("^[^/]+", url)
                    path_match = re.search("/[^?]+", url)
                    query_string_match = re.search("\?[^#]+", url)
                    fragment_match = re.search("#[^/]+", url)
                    return domain_match, path_match, query_string_match, fragment_match

                except Exception as e:
                    raise CSecurityException(e, sys)

            #logging.info(f"extracting only numperic columns from the dataset")
            #converting df to df-numeric
            #df = df[[column for column in df.columns if df[column].dtype != 'O']]
            
            #Extracting domain, path, query string, fragment
            logging.info(f"extracting domain, path, query string, fragment")
            df[['domain_match', 'path_match', 'query_string_match', 'fragment_match']] = df['URL'].apply(lambda x: pd.Series(extract_url_info(x)))
            df['domain_match'] = df['domain_match'].apply(lambda x: x.group() if x else None)
            df['path_match'] = df['path_match'].apply(lambda x: x.group() if x else None)
            df['query_string_match'] = df['query_string_match'].apply(lambda x: x.group() if x else None)
            df['fragment_match'] = df['fragment_match'].apply(lambda x: x.group() if x else None)

            def count_character_in_url(url, character):
                try:
                    count = {}
                    for c in CHARACTER_LIST:
                        count[c] = url.count(c)
                    return pd.Series(count)
                except Exception as e:
                    raise CSecurityException(e, sys)

            #Extracting character counts from the url and creating columns
            logging.info(f"extracting character counts from the url and creating columns")
            df[["qty_dot_url", "qty_hyphen_url", "qty_underline_url", "qty_slash_url", "qty_question_url",
                "qty_equal_sign_url", "qty_at_sign_url", "qty_and_sign_url", "qty_exclamation_url", "qty_space_url",
                "qty_comma_url", "qty_plus_url", "qty_star_url", "qty_hash_url", "qty_dollar_url", "qty_percent_url"]] = df["URL"].apply(lambda x: count_character_in_url(x, CHARACTER_LIST))

            def url_len(url):
                try:
                    return len(url)
                except Exception as e:
                    raise CSecurityException(e, sys)

            #Creating a column for URL length
            logging.info(f"Creating a column for URL length")
            df["url_length"] = df["URL"].apply(lambda x: url_len(x))

            logging.info(f"Moving the Lable column to the last position")
            # Get the column to move
            col = df.pop("Label")
            # Insert the column to a new position (here, it's being inserted at the end)
            df.insert(len(df.columns), "Label", col)

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
