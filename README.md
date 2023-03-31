* This project helps identifying Phishing URL
_____________________________________________________________________________________________________________________________________________________________________### Description:

* Phishing stands for a fraudulent process, where an attacker tries to obtain sensitive information from the victim. Usually, these kinds of attacks are done via emails, text messages, or websites. Phishing websites, which are nowadays in a considerable rise, have the same look as legitimate sites. However, their backend is designed to collect sensitive information that is inputted by the victim.

* This work discusses the implementation of a Machine learning algorithm to identify potential phishing attempts using the URL shared by the users and help them understand if they’ll be safe if the link is opened. 

* We won’t be opening the link to identify a potential phishing URL.
* We have used Random Forest Classifer model for this project
* Research paper: https://www.sciencedirect.com/science/article/pii/S2352340920313202
____________________________________________________________________________________________________________________________________________________________________
### Dataset:

* To download the dataset, please follow this link: https://data.mendeley.com/datasets/72ptz43s9v/1
* Environment used: Neurolab-> neurolab-mongo-python

____________________________________________________________________________________________________________________________________________________________________
### Step 1 - Install the requirements

```bash
pip install -r requirements.txt
```

### Step 2 - Run main.py file

```bash
python main.py
```
```
from glob import glob
```
The glob module provides a function for making file lists from directory wildcard searches. It is often used for quickly accessing a large number of files in a directory, especially when the file names match a pattern.

_________________________________________________________________________________________________________________________

_________________________________________________________________________________________________________________________


***The training pipeline:*** has 6 phases DI > DV > DT > MT > ME > MP
Each phase takes an input called as "config" and generates an output called "artifact"
_________________________________________________________________________________________________________________________
***Data Ingestion Component:***

1. Extracted the data from database, for this project we have used MongoDB. This is the input or Config.
2. This input file only has URL and Label columns. We extract all the features necessary from this and create a DataFrame
3. From this data, we created 3 artifacts and stored in the artifact folder: 
    a. first we store the extracted data in the artifact/data_ingestion/feature_store
    b. we generated a train file in the artifact/data_ingestion
    c. we generated a teset file in the artifact/data_ingestion
_________________________________________________________________________________________________________________________
***Data Validation Component***

1. Takes data ingestion artifacts as input
2. Validates if the data generated in the data ingestion phase is as per the findings in the EDA phase
3. This is done by using the handling null values and checking for required columns
4. We also check for data drift to ensure predictions in the future could be handled by the same model
5. Generates a report for the same as an artifact in the artifact/data_validation
_________________________________________________________________________________________________________________________
***Data Transformation Component***

1. We created the preprocessing pipeline
2. This pipeline has Simple Imputer and RobustScaler
3. This component takes train data from the Data Ingestion artifact and creates a trained pre-processing pipeline
4. Using this we generated transformed the train and test data into test.npz and train.npz in artifact/data_transformation/transformed
5. Our target feature was not numerical. We've used the LabelEncoder to encode the target feature. This is stored as an artifact in artifact/data_transformation/target_encoded
_______________________________________________________________________________________________________________________________________________________________________________
***Model Trainer***

1. Takes transformed train_arr and test_arr as config
2. Used RandomForest Classifier as the model and trained it
3. Created a Model.pkl file as an artifact and saved in artifact/model_trainer/model
_________________________________________________________________________________________________________________________
***Model Evaluation***

***Batch prediction*** is the process of applying a machine learning model to a large set of inputs and obtaining the corresponding output predictions in a batch, rather than one at a time. It is typically used for time-sensitive applications, where the goal is to process a large amount of data as quickly and efficiently as possible, rather than focusing on individual predictions.
____________________________________________________________________________________________________________________________________________________________________
***Instance prediction*** refers to the prediction of a target variable for a single instance or observation in a dataset. This is typically done by inputting the feature values for a specific instance into a trained machine learning model and getting a prediction for the target variable..

____________________________________________________________________________________________________________________________________________________________________
***Deployment*** is done using AWS - EC2 & Airflow

Please go through "Cybersecurity Expalanaiton file" folder for more information on the project


