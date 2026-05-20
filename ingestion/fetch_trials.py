import requests
import json
import os
from utils import save_raw_data, upload_to_s3

BASE_URL = "https://clinicaltrials.gov/api/v2/studies"

def fetch_trials(condition, page_size=50):
    params = {
        "query.cond": condition,
        "pageSize": page_size,
        "format": "json"
    }

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()

    return response.json()

if __name__ == "__main__":
    data = fetch_trials("heart disease")
    save_raw_data(data, "trials_heart_disease.json")
    upload_to_s3(
        local_filepath="data/raw/trials_heart_disease.json",
        bucket_name="clinical-data-platform-omiliauskas",
        s3_key="raw/trials_heart_disease.json"
    )