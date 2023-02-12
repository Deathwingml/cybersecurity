from cybersecurity.exception import CSecurityException
from cybersecurity.logger import logging
from cybersecurity.entity import config_entity, artifact_entity
from cybersecurity import utils
from cybersecurity.config import TARGET_COLUMN

import os, sys
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score


class ModelTrainer:

    def __init__(self,model_trainer_config:config_entity.ModelTrainerConfig,
                data_transformation_artifact:artifact_entity.DataTransformationArtifact
                ):
        try:
            logging.info(f"{'>>'*20} Model Trainer {'<<'*20}")
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact

        except Exception as e:
            raise CSecurityException(e, sys)


    def fine_tune(self):
        try:
            #write code for finetuning using Grid Search CV
            pass
        except Exception as e:
            raise CSecurityException(e, sys)

    
    def train_model(self,x,y):
        try:
            logging.info(f"entring train_model() function")
            rf_clf = RandomForestClassifier()
            rf_clf.fit(x,y)
            return rf_clf
        except Exception as e:
            logging.info(f"train_model() function failed")
            raise CSecurityException(e, sys)



    def initiate_model_trainer(self,)->artifact_entity.ModelTrainerArtifact:
        try:
            logging.info(f"loading train and test arrays for model trainer")
            train_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_path)
            test_arr =  utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_path)

            logging.info(f"Splitting input and target feature from train and test array")
            x_train,y_train = train_arr[:,:-1],train_arr[:,-1]
            x_test,y_test = test_arr[:,:-1],test_arr[:,-1]

            logging.info(f"Training the model")
            model = self.train_model(x=x_train, y = y_train)

            logging.info(f"Calculating f1_train_score")
            yhat_train = model.predict(x_train)
            f1_train_score = f1_score(y_true = y_train, y_pred = yhat_train) #calculates f1 train score

            logging.info(f"calculating f1_test_score")
            yhat_test = model.predict(x_test)
            f1_test_score = f1_score(y_true = y_test, y_pred = yhat_test) #calculates f1 test score

            logging.info(f"checkiing for overfitting, underfitting, or expected score from the model")
            if f1_test_score < self.model_trainer_config.expected_score:
                raise Exception(f"Model is not optimal as it does not give an optimal accuracy of {self.model_trainer_config.expected_score}. Actual score is {f1_test_score}")
            
            diff = abs(f1_train_score - f1_test_score)
            
            logging.info(f"train_score:{f1_train_score}, test_score:{f1_test_score}")
            if diff > self.model_trainer_config.overfitting_threshold:
                raise Exception(f"Overfitting: Model is not optimal. the difference is {diff}")

            #save the trained model
            logging.info(f"Save the trained model")
            utils.save_object(file_path = self.model_trainer_config.model_path, obj=model)
            
            #prepare the artifact
            logging.info(f"Preparing the model artifact")
            model_trainer_artifact = artifact_entity.ModelTrainerArtifact(model_path=self.model_trainer_config.model_path, 
            f1_train_score=f1_train_score, f1_test_score=f1_test_score)
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact

        except Exception as e:
            raise CSecurityException(e, sys)