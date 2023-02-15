from cybersecurity.predictor import ModelResolver
from cybersecurity.exception import CSecurityException
from cybersecurity.logger import logging
from cybersecurity.entity import config_entity, artifact_entity
from cybersecurity import utils
from cybersecurity.utils import load_object
from cybersecurity.config import TARGET_COLUMN

from sklearn.metrics import f1_score
import os, sys
import pandas as pd


class ModelEvaluation:

    def __init__(self,
        model_eval_config:config_entity.ModelEvaluationConfig,
        data_ingestion_artifact:artifact_entity.DataIngestionArtifact,
        data_transformation_artifact:artifact_entity.DataTransformationArtifact,
        model_trainer_artifact:artifact_entity.ModelTrainerArtifact      
        ):
        try:
            logging.info(f"{'>>'*20}  Model Evaluation {'<<'*20}")
            self.model_eval_config=model_eval_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_transformation_artifact=data_transformation_artifact
            self.model_trainer_artifact=model_trainer_artifact
            self.model_resolver = ModelResolver()
        except Exception as e:
            raise SensorException(e,sys)


    def initate_model_evaluation(self,)->artifact_entity.ModelEvaluationArtifact:
        try:
            #if saved model folder has a model, we'll compare to find the best trained model
            latest_dir_path = self.model_resolver.get_latest_dir_path()
            if latest_dir_path == None:
                model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True, improved_accuracy=None)
                logging.info(f"Model Evaluation Artifact: {model_eval_artifact}")
                return model_eval_artifact


            #finding the location of transformer, model, and target_encoder
            logging.info(f"Finding the location of previously trained transformer, model, and target_encoder")
            transformer_path = self.model_resolver.get_latest_transformer_path()
            model_path = self.model_resolver.get_latest_model_path()
            target_encoder_path = self.model_resolver.get_latest_target_encoder_path()

            #loading previously objects
            logging.info(f"Loading previously trained transformer, model, and target_encoder")
            transformer = load_object(file_path=transformer_path)
            model = load_object(file_path=model_path)
            target_encoder = load_object(file_path=target_encoder_path)

            #currently trained model objects
            logging.info(f"Loading currently trained transformer, model, and target_encoder")
            current_transformer = load_object(file_path=self.data_transformation_artifact.transform_object_path)
            current_model = load_object(file_path=self.model_trainer_artifact.model_path)
            current_target_encoder = load_object(file_path=self.data_transformation_artifact.target_encoder_path)

            logging.info(f"Loading test_df from data ingestion to get target column and make predictions")
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            target_df = test_df[TARGET_COLUMN]
            y_true = target_encoder.transform(target_df)

            #Accuracy using previously trained model
            logging.info(f"Calculating accuracy for previously trained model")
            input_feature_name = list(transformer.feature_names_in_)
            input_arr = transformer.transform(test_df[input_feature_name])
            y_pred = model.predict(input_arr) #target_encoder.inverse_transform(prediction[:5]) -- put this in next line if needed
            
            y_pred_int = y_pred[:5].astype(int)   #--- converting just for showing the predictions
            logging.info(f"prediction using previous model{target_encoder.inverse_transform(y_pred_int[:5])}")
            previous_model_score = f1_score(y_true=y_true, y_pred = y_pred)

            #Accuracy using current trained model
            logging.info(f"Calculating accuracy for currently trained model")
            input_feature_name = list(current_transformer.feature_names_in_)
            input_arr = current_transformer.transform(test_df[input_feature_name])
            y_pred = current_model.predict(input_arr)
            y_true = current_target_encoder.transform(target_df)

            y_pred_int = y_pred[:5].astype(int)   #--- converting just for showing the predictions
            logging.info(f"prediction using current model{target_encoder.inverse_transform(y_pred_int[:5])}")
            previous_model_score = f1_score(y_true=y_true, y_pred = y_pred)
            current_model_score = f1_score(y_true=y_true, y_pred = y_pred)
            
            logging.info(f"Compairing previous model accuracy:{current_model_score} and current model accurcy:{previous_model_score}")
            if current_model_score < previous_model_score:
                logging.info(f"Current trained model is not better than previous model")
                raise Exception(f"Current trained model is not better than previous model")

            logging.info(f"current trained model is better than previously trained model")
            model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True, 
                                                                            improved_accuracy=current_model_score-previous_model_score)
            logging.info(f"Model Evaluation Artifact: {model_eval_artifact}")
            return model_eval_artifact

        except Exception as e:
            raise CSecurityException(e, sys)