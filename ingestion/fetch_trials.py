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

def run(condition, file_name):
    data = fetch_trials(condition)
    studies = data["studies"]
    save_raw_data(studies, file_name)
    return f"data/raw/{file_name}"

if __name__ == "__main__":
    run("heart disease", "trials_heart_disease.json")
    run("diabetes", "trials_diabetes.json")
