import sys, os
import re
from cybersecurity.exception import CSecurityException
from cybersecurity.logger import logging
from cybersecurity.utils import get_collection_as_dataframe
from cybersecurity.entity.config_entity import DataIngestionConfig
from cybersecurity.entity import config_entity
from cybersecurity.components.data_ingestion import DataIngestion
from cybersecurity.components.data_validation import DataValidation
from cybersecurity.components.data_transformation import DataTransformation
from cybersecurity.components.model_trainer import ModelTrainer
from cybersecurity.components.model_evaluation import ModelEvaluation
from cybersecurity.components.model_pusher import ModelPusher


def start_training_pipeline():
     try:
          training_pipeline_config = config_entity.TrainingPipelineConfig()

          #Data Ingestion
          logging.info(f"Data ingestion from main.py")
          data_ingestion_config  = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
          print(data_ingestion_config.to_dict())
          data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
          data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

          #Data Validation
          logging.info(f"Data Validation from main.py")
          data_validation_config = config_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
          data_validation = DataValidation(data_validation_config=data_validation_config, 
                                             data_ingestion_artifact= data_ingestion_artifact)
          data_validation_artifact = data_validation.initiate_data_validation()
          
          #Data Transformation
          logging.info(f"Data Transformation from main.py")
          data_transformation_config= config_entity.DataTransformationConfig(training_pipeline_config=training_pipeline_config)
          data_transformation = DataTransformation(data_transformation_config=data_transformation_config, 
                                                  data_ingestion_artifact=data_ingestion_artifact)
          data_transformation_artifact = data_transformation.initiate_data_transformation()

          #Model Trainer
          logging.info(f"Model Trainer from main.py")
          model_trainer_config = config_entity.ModelTrainerConfig(training_pipeline_config= training_pipeline_config)
          model_trainer = ModelTrainer(model_trainer_config=model_trainer_config, 
                                        data_transformation_artifact = data_transformation_artifact)
          model_trainer_artifact = model_trainer.initiate_model_trainer()

          #Model Evaluation
          logging.info(f"Model Evaluation from main.py")
          model_eval_config = config_entity.ModelEvaluationConfig(training_pipeline_config = training_pipeline_config)
          model_evaluation = ModelEvaluation(model_eval_config=model_eval_config, 
                              data_ingestion_artifact=data_ingestion_artifact, 
                              data_transformation_artifact=data_transformation_artifact, 
                              model_trainer_artifact=model_trainer_artifact)
          model_evaluation_artifact = model_evaluation.initate_model_evaluation()

          #Model Pusher
          logging.info(f"Model Pusher from main.py")
          model_pusher_config = config_entity.ModelPusherConfig(training_pipeline_config=training_pipeline_config)
          mondel_pusher = ModelPusher(model_pusher_config=model_pusher_config, 
                                        data_transformation_artifact=data_transformation_artifact, 
                                        model_trainer_artifact=model_trainer_artifact)
          model_pusher_artifact = mondel_pusher.initiate_model_pusher()


     except Exception as e:
          raise CSecurityException(e, sys)