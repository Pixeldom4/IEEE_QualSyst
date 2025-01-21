import pandas as pd
import requests
import math
import os
from concurrent.futures import ThreadPoolExecutor

# Correct API URL
API_URL = "http://127.0.0.1:5000/papers/batch"
BATCH_SIZE = 100

base_dir = os.path.dirname(__file__)

# List of relative file paths
files = [
    os.path.join(base_dir, "../Databases/Cleaned/compiled_ovid.csv"),
    os.path.join(base_dir, "../Databases/Cleaned/compiled_proquest.csv"),
]

def send_batch(batch):
    """Send a batch of papers to the API."""
    try:
        response = requests.post(API_URL, json=batch)
        if response.status_code == 201:
            print(f"Batch added successfully. {len(batch)} records processed.")
        else:
            print(f"Failed to add batch. Status Code: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error sending batch: {e}")


def process_file(file_path):
    """Process a single file and send data in batches."""
    if not os.path.exists(file_path):
        print(f"File does not exist: {file_path}")
        return

    try:
        # Load the CSV
        df = pd.read_csv(file_path, header=0)
        print(f"Processing file: {file_path}")
        print(f"Columns before cleaning: {df.columns.tolist()}")  # Debugging

        # Clean column names
        df.columns = df.columns.str.strip().str.lower()  # Normalize column names
        print(f"Columns after cleaning: {df.columns.tolist()}")  # Debugging

        # Ensure required columns exist
        required_columns = ["article title", "author(s)", "olivia (article link)"]
        for col in required_columns:
            if col not in df.columns:
                print(f"Warning: Missing column '{col}' in file '{file_path}'. Adding default values.")
                df[col] = None  # Add missing column with default values

        batch = []
        for _, row in df.iterrows():
            try:
                if pd.notna(row["article title"]):
                    paper_data = {
                        "article_title": row["article title"],
                        "article_authors": row.get("author(s)", "Unknown") or "Unknown",  # Ensure a default value
                        "article_abstract": None,  # Abstract not in this example
                        "article_link": row.get("olivia (article link)", None),
                        "search_terms": None,  # Search terms not in this example
                    }
                    paper_data = {k: (None if pd.isna(v) else v) for k, v in paper_data.items()}

                    batch.append(paper_data)
                    if len(batch) >= BATCH_SIZE:
                        send_batch(batch)
                        batch = []  # Reset batch
            except Exception as e:
                print(f"Error processing row: {row.to_dict()} - {e}")

        if batch:
            send_batch(batch)  # Send remaining records

    except Exception as e:
        print(f"Error reading file {file_path}: {e}")


# Process files concurrently
with ThreadPoolExecutor() as executor:
    executor.map(process_file, files)