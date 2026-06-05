import sys
sys.path.append('/opt/airflow/ingestion')

from airflow.decorators import dag, task
from datetime import datetime

@dag(
    schedule='@daily',
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['clinical']
)

def clinical_pipeline():

    @task
    def fetch_trials():
        from fetch_trials import run
        return run()

    @task
    def fetch_adverse_events():
        from fetch_adverse_events import run
        return run()

    @task
    def fetch_trials_diabetes():
        from fetch_trials_diabetes import run
        return run()

    @task
    def convert_to_parquet(input_path: str):
        import pandas as pd

        df = pd.read_json(input_path)
        output_path = input_path.replace(".json", ".parquet")
        df.to_parquet(output_path)
        return output_path

    @task
    def upload_to_s3(parquet_path: str, s3_key: str):
        from utils import upload_to_s3 as upload_fn
        upload_fn(
            local_filepath=parquet_path,
            bucket_name="clinical-data-platform-omiliauskas",
            s3_key=s3_key
        )
        return parquet_path

    @task
    def trigger_glue_crawler():
        import boto3 

        glue = boto3.client("glue", region_name="eu-north-1")
        glue.start_crawler(Name="clinical-data-platform-crawler")
    
    trials_path = fetch_trials()
    upload_to_s3.override(task_id="upload_raw_trials")(trials_path, "raw/trials_heart_disease/trials_heart_disease.json")
    trials_parquet_path = convert_to_parquet.override(task_id="convert_trials")(trials_path)
    trials_heart_uploaded = upload_to_s3.override(task_id="upload_trials")(trials_parquet_path, "staging/trials_heart_disease/trials_heart_disease.parquet")

    adverse_events_path = fetch_adverse_events()
    upload_to_s3.override(task_id="upload_raw_adverse_events")(adverse_events_path, "raw/adverse_events/adverse_events.json")
    adverse_events_parquet_path = convert_to_parquet.override(task_id="convert_adverse_events")(adverse_events_path)
    adverse_events_uploaded = upload_to_s3.override(task_id="upload_adverse_events")(adverse_events_parquet_path, "staging/adverse_events/adverse_events.parquet")

    trials_diabetes_path = fetch_trials_diabetes()
    upload_to_s3.override(task_id="upload_raw_trials_diabetes")(trials_diabetes_path, "raw/trials_diabetes/trials_diabetes.json")
    trials_diabetes_parquet_path = convert_to_parquet.override(task_id="convert_trials_diabetes")(trials_diabetes_path)
    trials_diabetes_uploaded = upload_to_s3.override(task_id="upload_trials_diabetes")(trials_diabetes_parquet_path, "staging/trials_diabetes/trials_diabetes.parquet")

    [trials_heart_uploaded, adverse_events_uploaded, trials_diabetes_uploaded] >> trigger_glue_crawler()


clinical_pipeline()

    