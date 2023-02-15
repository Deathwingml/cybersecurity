from cybersecurity.logger import logging
from cybersecurity.exception import CSecurityException
from cybersecurity.predictor import ModelResolver
from cybersecurity.utils import load_object
from cybersecurity.config import CHARACTER_LIST

import pandas as pd
import numpy as np
from datetime import datetime
import os, sys
import pickle
import re

PREDICTION_DIR = "predictions"

def start_instance_prediction(input_url):
    try:

        logging.info(f"Creating model resolver object")
        model_resolver = ModelResolver(model_registry="saved_models")

        logging.info(f"Reading input from the user")
        user_input_data = {"URL": [input_url]} # input_url is the URL you want to make predictions on
        df = pd.DataFrame(user_input_data) # putting the user input in dataframe for the model

        def remove_trailing_slash(url):
                if url.endswith('/'):
                    url = url[:-1]
                    return url
                else:
                    return url

        logging.info(f"removing trailing / from the url")
        df["URL"] = df["URL"].apply(remove_trailing_slash)

        def count_character_in_url(url, character):
            try:
                count = {}
                for c in CHARACTER_LIST:
                    count[c] = url.count(c)
                return pd.Series(count)
            except Exception as e:
                raise CSecurityException(e, sys)

        #Extracting character counts from the url and creating columns
        logging.info(f"extracting character counts from the url and creating columns")
        df[["qty_dot_url", "qty_hyphen_url", "qty_underline_url", "qty_slash_url", "qty_question_url",
            "qty_equal_sign_url", "qty_at_sign_url", "qty_and_sign_url", "qty_exclamation_url", "qty_space_url",
            "qty_comma_url", "qty_plus_url", "qty_star_url", "qty_hash_url", "qty_dollar_url", "qty_percent_url"]] = df["URL"].apply(lambda x: count_character_in_url(x, CHARACTER_LIST))

        def url_len(url):
            try:
                return len(url)
            except Exception as e:
                raise CSecurityException(e, sys)

        #Creating a column for URL length
        logging.info(f"Creating a column for URL length")
        df["url_length"] = df["URL"].apply(lambda x: url_len(x))

        logging.info(f"replace na with np.NAN")
        #save data in feature store
        df.replace(to_replace = "na", value = np.NAN, inplace = True)

        logging.info(f"Loading transformer to transform dataset")
        transformer = load_object(file_path=model_resolver.get_latest_transformer_path())

        input_feature_names =  list(transformer.feature_names_in_)
        input_arr = transformer.transform(df[input_feature_names])

        logging.info(f"Loading model to make prediction")
        model = load_object(file_path=model_resolver.get_latest_model_path())
        prediction = model.predict(input_arr)
        prediction_int = prediction.astype(int)

        logging.info(f"Target encoder to convert predicted column into categorical")
        target_encoder = load_object(file_path=model_resolver.get_latest_target_encoder_path())

        cat_prediction = target_encoder.inverse_transform(prediction_int)
        # y_pred_int = y_pred[:5].astype(int)   #--- converting just for showing the predictions

        df["prediction"]=prediction
        df["cat_pred"]=cat_prediction

        #creating the prediction folder
        os.makedirs(PREDICTION_DIR, exist_ok=True)
        prediction_file_name = os.path.basename(input_url).replace(".csv",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.csv")
        prediction_file_path = os.path.join(PREDICTION_DIR,prediction_file_name)
        df.to_csv(prediction_file_path,index=False,header=True)
        return prediction_file_path

    except Exception as e:
        raise CSecurityException(e, sys)
