import requests
import os
import json
from utils import save_raw_data

BASE_URL = "https://api.fda.gov/drug/event.json"

def fetch_adverse_events(condition, page_size=50):
    params = {
    "search": "patient.reaction.reactionmeddrapt:" + condition,
    "limit": page_size
    }

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()

    return response.json()

if __name__ == "__main__":
    data = fetch_adverse_events("heart+diseases")
    save_raw_data(data, "adverse_events_heart_disease.json")
