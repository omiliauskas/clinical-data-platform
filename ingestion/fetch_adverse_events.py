import requests
import os
import json

BASE_URL = "https://api.fda.gov/drug/event.json"
RAW_DATA_PATH = "data/raw"

os.makedirs(RAW_DATA_PATH, exist_ok=True)

def fetch_adverse_events(condition, page_size=50):
    params = {
    "search": "patient.reaction.reactionmeddrapt:" + condition,
    "limit": page_size
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
    data = fetch_adverse_events("heart+diseases")
    save_raw_data(data, "adverse_events_heart_disease.json")
