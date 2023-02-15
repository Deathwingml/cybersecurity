from cybersecurity.pipeline.training_pipeline import start_training_pipeline
from cybersecurity.pipeline.instance_prediction import start_instance_prediction
from cybersecurity.exception import CSecurityException
import os,sys

input_url = "https://phishtank.org/phish_detail.php?phish_id=8037563"

def remove_trailing_slash(url):
    if url.endswith('/'):
        url = url[:-1]
        return url
    else:
        return url

input_url = remove_trailing_slash(input_url)

print(__name__)
if __name__ == "__main__":
     try:
         #start_training_pipeline()
         output_file = start_instance_prediction(input_url= input_url)


     except Exception as e:
          raise CSecurityException(e, sys)