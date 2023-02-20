from cybersecurity.pipeline.training_pipeline import start_training_pipeline
from cybersecurity.pipeline.instance_prediction import start_instance_prediction

file_path="/config/workspace/raw_url_data.csv"
print(__name__)
if __name__=="__main__":
     try:
          #start_training_pipeline()
          output_file = start_instance_prediction(input_url=file_path)
          print(output_file)
     except Exception as e:
          print(e)