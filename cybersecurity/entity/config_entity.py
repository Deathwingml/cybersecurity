import os,sys
from datetime import datetime
from cybersecurity.exception import CSecurityException
from cybersecurity.logger import logging

FILE_NAME = "cybersecurity.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"
TRANSFORMER_OBJECT_FILE_NAME = "tramsformer.pkl"
TARGET_ENCODER_OBJECT_FILE_NAME = "target_encoder.pkl"
MODEL_FILENAME = "model.pkl"


class TrainingPipelineConfig:

    def __init__(self):
        try:
            self.artifact_dir = os.path.join(os.getcwd(), "artifact", f"{datetime.now().strftime('%m%d%Y__%H%M%S')}") #will create the 'artifact' folder in the current directory with another folder in it with the timestamp
        except Exception as e:
            raise CSecurityException(e, sys)

class DataIngestionConfig:

    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        try:
            self.database_name = "cybersecurity"
            self.collection_name = "phishing_domain"
            self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir, "data_ingestion")
            self.feature_store_file_path = os.path.join(self.data_ingestion_dir, "feature_store", FILE_NAME)
            self.train_file_path = os.path.join(self.data_ingestion_dir, "dataset", TRAIN_FILE_NAME)
            self.test_file_path = os.path.join(self.data_ingestion_dir, "dataset", TEST_FILE_NAME)
            self.test_size = 0.2
            self.train_size = 0.8
            self.random_state = 1
        except Exception as e:
            raise CSecurityException(e, sys)
            
    
    def to_dict(self,)->dict:
        try:
            return self.__dict__
        except Exception as e:
            raise CSecurityException(e, sys)





class DataValidationConfig:...
class DataTransformationConfig:...
class ModelTrainerConfig:...
class ModelEvaluationConfig:...
class ModelPusherConfig:...