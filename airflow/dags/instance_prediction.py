from asyncio import tasks
import json
from textwrap import dedent
import pendulum
import os
from airflow import DAG
from airflow.operators.python import PythonOperator


with DAG(
    'cybersecurity_training',
    default_args={'retries': 2},
    # [END default_args]
    description='Cyber Security Phishing Domain Detection',
    schedule_interval="@weekly",
    start_date=pendulum.datetime(2022, 12, 11, tz="UTC"),
    catchup=False,
    tags=['example'],
) as dag:

    
    def training(**kwargs):
        from cybersecurity.pipeline.instance_prediction import start_instance_prediction
        start_instance_prediction(input_url)
    
    def sync_artifact_to_s3_bucket(**kwargs):
        bucket_name = os.getenv("BUCKET_NAME")
        os.system(f"aws s3 sync /app/artifact s3://{bucket_name}/artifacts")
        os.system(f"aws s3 sync /app/saved_models s3://{bucket_name}/saved_models")

    prediction  = PythonOperator(
            task_id="instance_prediction",
            python_callable=training

    )

    sync_data_to_s3 = PythonOperator(
            task_id="sync_data_to_s3",
            python_callable=sync_artifact_to_s3_bucket

    )

    prediction >> sync_data_to_s3