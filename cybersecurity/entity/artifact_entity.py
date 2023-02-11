from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:  #creating a structure for data ingestion artifact
    feature_store_file_path:str
    train_file_path:str
    test_file_path:str


@dataclass
class DataValidationArtifact: #creating a structure for data validation artifact
    report_file_path:str


@dataclass
class DataTransformationArtifact:
    transform_object_path:str
    transformed_train_path:str
    transformed_test_path:str
    target_encoder_path:str



class ModelTrainerArtifact:...
class ModelEvaluationArtifact:...
class ModelPusherArtifact:...
