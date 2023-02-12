import pandas as pd
import numpy as np 
import os, sys
from typing import Optional

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from imblearn.combine import SMOTETomek

from cybersecurity.exception import CSecurityException
from cybersecurity.logger import logging
from cybersecurity.entity import config_entity, artifact_entity
from cybersecurity import utils
from cybersecurity.config import TARGET_COLUMN, EXCLUDE_COLUMNS


class DataTransformation:

    def __init__(self,data_transformation_config:config_entity.DataTransformationConfig,
                    data_ingestion_artifact: artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20} Data Transformation {'<<'*20}")
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact

        except Exception as e:
            raise CSecurityException(e, sys)



    @classmethod
    def get_data_tranformer_object(cls)->Pipeline:
        try:
            simple_imputer = SimpleImputer(strategy = "constant", fill_value =0)
            robust_scaler = RobustScaler()
            constant_pipeline = Pipeline(steps=[
                    ('Imputer',simple_imputer),
                    ('RobustScaler',robust_scaler)
                ])
            return constant_pipeline

        except Exception as e:
            raise CSecurityException(e, sys)



    def initiate_data_transformation(self,)-> artifact_entity.DataTransformationArtifact:
        try:
            #reading train and test files
            logging.info(f"reading train and test files")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            #selecting input feature for train and test dataframe
            logging.info(f"selecting input feature for train and test dataframe")
            input_feature_train_df = train_df.drop(EXCLUDE_COLUMNS, axis = 1)
            input_feature_test_df = test_df.drop(EXCLUDE_COLUMNS, axis = 1)

            #selecting target features for train and test dataframe
            logging.info(f"selecting target features for train and test dataframe")
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_test_df = test_df[TARGET_COLUMN]

            logging.info(f"Label Encoding the target column")
            label_encoder = LabelEncoder()
            label_encoder.fit(target_feature_train_df)
            
            #transformation on the target column
            logging.info(f"transformation on the target column")
            target_feature_train_arr = label_encoder.transform(target_feature_train_df)
            target_feature_test_arr = label_encoder.transform(target_feature_test_df)

            logging.info(f"initialize transformation pipeline")
            transformation_pipeline = DataTransformation.get_data_tranformer_object()
            transformation_pipeline.fit(input_feature_train_df)

            #transforming input features
            logging.info(f"transforming input features")
            input_feature_train_arr = transformation_pipeline.transform(input_feature_train_df)
            input_feature_test_arr = transformation_pipeline.transform(input_feature_test_df)

            #Sampling
            logging.info(f"initiate sampling")
            smt = SMOTETomek(sampling_strategy= "minority")
            logging.info(f"Before resampling in training set Input: {input_feature_train_arr.shape} Target:{target_feature_train_arr.shape}")
            input_feature_train_arr, target_feature_train_arr = smt.fit_resample(input_feature_train_arr, target_feature_train_arr)
            logging.info(f"After resampling in training set Input: {input_feature_train_arr.shape} Target:{target_feature_train_arr.shape}")

            logging.info(f"Before resampling in testing set Input: {input_feature_test_arr.shape} Target:{target_feature_test_arr.shape}")
            input_feature_test_arr, target_feature_test_arr = smt.fit_resample(input_feature_test_arr, target_feature_test_arr)
            logging.info(f"After resampling in testing set Input: {input_feature_test_arr.shape} Target:{target_feature_test_arr.shape}")

            #target encoder
            logging.info(f"concatinating input and target features ")
            train_arr = np.c_[input_feature_train_arr, target_feature_train_arr]
            test_arr = np.c_[input_feature_test_arr, target_feature_test_arr]

            #save numpy array
            logging.info(f"saving numpy arrays")
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_path, array=train_arr)
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_path, array=test_arr)
            utils.save_object(file_path=self.data_transformation_config.transform_object_path, obj=transformation_pipeline)
            utils.save_object(file_path=self.data_transformation_config.target_encoder_path, obj=label_encoder)

            logging.info(f"Generating Data transformation object")
            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transform_object_path=self.data_transformation_config.transform_object_path,
                transformed_train_path = self.data_transformation_config.transformed_train_path,
                transformed_test_path = self.data_transformation_config.transformed_test_path,
                target_encoder_path = self.data_transformation_config.target_encoder_path
                )

            logging.info(f"Data transformation object {data_transformation_artifact}")
            return data_transformation_artifact

        except Exception as e:
            raise CSecurityException(e, sys)
