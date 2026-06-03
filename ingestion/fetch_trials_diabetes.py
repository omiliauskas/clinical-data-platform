import requests
from utils import save_raw_data

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

def run():
    data = fetch_trials_diabetes("diabetes")
    studies = data["studies"]
    save_raw_data(studies, "trials_diabetes.json")
    return "data/raw/trials_diabetes.json"

if __name__ == "__main__":
    local_path = run()

