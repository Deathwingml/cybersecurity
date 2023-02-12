import os,sys
from datetime import datetime
from cybersecurity.exception import CSecurityException
from cybersecurity.logger import logging

FILE_NAME = "cybersecurity.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"
TRANSFORMER_OBJECT_FILE_NAME = "tramsformer.pkl"
TARGET_ENCODER_OBJECT_FILE_NAME = "target_encoder.pkl"
MODEL_FILE_NAME = "model.pkl"


class TrainingPipelineConfig: #creating a class which will create an artifact folder to store all the files generated in the trianing pipeline

    def __init__(self):
        try:
            self.artifact_dir = os.path.join(os.getcwd(), "artifact", f"{datetime.now().strftime('%m%d%Y__%H%M%S')}") #will create the 'artifact' folder in the current directory with another folder in it with the timestamp
        except Exception as e:
            raise CSecurityException(e, sys)

class DataIngestionConfig: #create a folder within artifact folder with the data ingestion output

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





class DataValidationConfig:

    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        try:
            self.data_validation_dir = os.path.join(training_pipeline_config.artifact_dir, "data_validation")
            self.report_file_path = os.path.join(self.data_validation_dir,"report.yaml")
            self.missing_threshold:float = 0.99
            self.base_file_path = os.path.join("raw_url_data.csv")

        except Exception as e:

            raise CSecurityException(e, sys)


class DataTransformationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        try:
            self.data_transformation_dir = os.path.join(training_pipeline_config.artifact_dir, "data_transformation")
            self.transform_object_path = os.path.join(self.data_transformation_dir,"transformer",TRANSFORMER_OBJECT_FILE_NAME)
            self.transformed_train_path =  os.path.join(self.data_transformation_dir,"transformed",TRAIN_FILE_NAME.replace("csv", "npz"))
            self.transformed_test_path =os.path.join(self.data_transformation_dir,"transformed",TEST_FILE_NAME.replace("csv", "npz"))
            self.target_encoder_path = os.path.join(self.data_transformation_dir,"target_encoder",TARGET_ENCODER_OBJECT_FILE_NAME)

        except Exception as e:
            raise CSecurityException(e, sys)


class ModelTrainerConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        try:
            self.model_trainer_dir = os.path.join(training_pipeline_config.artifact_dir, "model_trainer")
            self.model_path = os.path.join(self.model_trainer_dir,"model",MODEL_FILE_NAME)
            self.expected_score = 0.7
            self.overfitting_threshold = 0.15

        except Exception as e:
            raise CSecurityException(e, sys)


class ModelEvaluationConfig:
        def __init__(self,training_pipeline_config: TrainingPipelineConfig):
            try:
                self.change_threshold = 0.01  #we'll accept the new model when there is atleast an improvement of 1%
  
            except Exception as e:
                raise CSecurityException(e, sys)


class ModelPusherConfig:...
