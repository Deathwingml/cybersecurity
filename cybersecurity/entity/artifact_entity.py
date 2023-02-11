from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:  #creating a structure for data ingestion artifact
    feature_store_file_path:str
    train_file_path:str
    test_file_path:str

@dataclass
class DataValidationArtifact: #creating a structure for data validation artifact
    report_file_path:str




class DataTransformationArtifact:...
class ModelTrainerArtifact:...
class ModelEvaluationArtifact:...
class ModelPusherArtifact:...
