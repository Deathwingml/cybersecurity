import pandas as pd 
import pymongo
import json
import os, sys
from cybersecurity.config import mongo_client
from cybersecurity.exception import CSecurityException
from cybersecurity.logger import logging



def get_collection_as_dataframe(database_name:str, collection_name:str)->pd.DataFrame:
    
    """
    Description: This function return collection as dataframe
    =========================================================
    Params:
    database_name: database name
    collection_name: collection name
    =========================================================
    return Pandas dataframe of a collection
    """

    try:
        logging.info(f"Reading the database:{database_name} and collection:{collection_name}")
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        logging.info(f"Found columns: {df.columns}")
        if "_id" in df.columns:
            logging.info(f"Dropping column: _id")
            df = df.drop("_id", axis = 1)
        logging.info(f"Rows and columns: {df.shape}")
        return df
        
    except Exception as e:
        logging.info("get_collection_as_dataframe failed")
        raise CSecurityException(e, sys)