import requests
import json
import os

BASE_URL = "https://clinicaltrials.gov/api/v2/studies"
RAW_DATA_PATH = "data/raw"

os.makedirs(RAW_DATA_PATH, exist_ok=True)

def fetch_trials_diabetes(condition, page_size=50):
    params = {
        "query.cond": condition,
        "format": "json",
        "pageSize": page_size
    }

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()

    return response.json()

def save_raw_data(data, filename):
    filepath = os.path.join(RAW_DATA_PATH, filename)

    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Saved {filename} to {RAW_DATA_PATH}")

if __name__ == "__main__":
    data = fetch_trials_diabetes("diabetes")
    save_raw_data(data, "trials_diabetes.json")
