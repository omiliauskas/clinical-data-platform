import os
import json

RAW_DATA_PATH = "data/raw"
os.makedirs(RAW_DATA_PATH, exist_ok=True)

def save_raw_data(data, filename):
    filepath = os.path.join(RAW_DATA_PATH, filename)

    with open(filepath, "w") as f:
        json.dump(data, f, indent = 2)

    print(f"Saved {filename} to {RAW_DATA_PATH}")