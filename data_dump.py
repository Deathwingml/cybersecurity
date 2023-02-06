import pymongo
import json
import pandas as pd

#MongoDB local host url to connect to the DB
client = pymongo.MongoClient("mongodb://localhost:27017/")

DATA_FILE_PATH = "/config/workspace/cleaned_phishing_data.csv"
DATABASE_NAME = "cybersecurity"
COLLECTION_NAME = "phishing_domain"


if __name__ == "__main__":
    df = pd.read_csv(DATA_FILE_PATH)
    print(f"Rows and Columns: {df.shape}")

    #Covert dataframe to json and dump the dataset to MongoDB
    df.reset_index(drop = True, inplace = True)

    json_record = list(json.loads(df.T.to_json()).values())
    print(json_record)

    #insert converted json record to mongo db
    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)



