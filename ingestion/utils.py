import os
import json
import boto3

RAW_DATA_PATH = "data/raw"
os.makedirs(RAW_DATA_PATH, exist_ok=True)

def save_raw_data(data, filename):
    filepath = os.path.join(RAW_DATA_PATH, filename)

    with open(filepath, "w") as f:
        json.dump(data, f, indent = 2)

    print(f"Saved {filename} to {RAW_DATA_PATH}")

def upload_to_s3(local_filepath, bucket_name, s3_key):
    s3_client = boto3.client("s3")
    s3_client.upload_file(local_filepath, bucket_name, s3_key)
    print(f"Uploaded {local_filepath} to s3://{bucket_name}/{s3_key}")