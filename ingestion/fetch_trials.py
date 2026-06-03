import requests
from utils import save_raw_data

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

def run():
    data = fetch_trials("heart disease")
    studies = data["studies"]
    save_raw_data(studies, "trials_heart_disease.json")
    return "data/raw/trials_heart_disease.json"

if __name__ == "__main__":
    local_path = run()

