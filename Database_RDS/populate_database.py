import pandas as pd
import requests
import math
import os

# Correct API URL
API_URL = "http://127.0.0.1:5000/papers"

base_dir = os.path.dirname(__file__)

# List of relative file paths
files = [
    os.path.join(base_dir, "../Databases/compiled_pubmed.csv"),
    os.path.join(base_dir, "../Databases/compiled_ovid.csv"),
    os.path.join(base_dir, "../Databases/compiled_proquest.csv"),
]

# Process each file
for file_path in files:
    print(f"Processing file: {file_path}")

    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path, header=0)
        print(f"Columns in {file_path}:", df.columns)
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        continue

    # Iterate through rows in the DataFrame
    for _, row in df.iterrows():
        try:
            if pd.notna(row["Article Title"]):
                # Prepare data based on the database structure
                paper_data = {
                    "article_title": row["Article Title"],
                    "article_authors": row.get("Article Authors", "Unknown"),
                    "article_abstract": row.get("Article Abstract", None),
                    "article_link": row.get("Article Link", None),
                    "search_terms": row.get("Search Terms", None),
                }

                # Replace NaN values with None
                paper_data = {key: (None if isinstance(value, float) and math.isnan(value) else value) for key, value in
                              paper_data.items()}

                # Check for duplicates by title
                response = requests.get(f"{API_URL}/search", params={"title": paper_data["article_title"]})
                if response.status_code == 200 and response.json():  # Paper exists
                    print(f"Duplicate found. Skipping: {row['Article Title']}")
                    continue

                print("Data being sent:", paper_data)

                # Post data to the API
                response = requests.post(API_URL, json=paper_data)
                if response.status_code == 201:
                    print(f"Successfully added: {row['Article Title']}")
                else:
                    print(f"Failed to add: {row['Article Title']} - Status Code: {response.status_code}")

        except Exception as e:
            print(f"Error processing entry: {row.get('Article Title', 'Unknown')} - {e}")
