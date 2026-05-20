import requests
import json
import os
from utils import save_raw_data, upload_to_s3

BASE_URL = "https://clinicaltrials.gov/api/v2/studies"

def fetch_trials_diabetes(condition, page_size=50):
    params = {
        "query.cond": condition,
        "format": "json",
        "pageSize": page_size
    }

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()

    return response.json()

if __name__ == "__main__":
    data = fetch_trials_diabetes("diabetes")
    save_raw_data(data, "trials_diabetes.json")
    upload_to_s3(
        local_filepath="data/raw/trials_diabetes.json",
        bucket_name="clinical-data-platform-omiliauskas",
        s3_key="raw/trials_diabetes.json"
    )
