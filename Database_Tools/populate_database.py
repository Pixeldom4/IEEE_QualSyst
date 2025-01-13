import pandas as pd
import requests
import math

# Correct API URL
API_URL = "http://127.0.0.1:5000/papers"

# Make sure to adjust your path accordingly.
file_path = "/Users/derrickwillis/PycharmProjects/IEEE_QualSyst/Databases/qualsyst_spreadsheet_proquest.xlsx"
df = pd.read_excel(file_path, header=0)

print("Columns in the Excel file:", df.columns)

for _, row in df.iterrows():
    try:
        if pd.notna(row["Article Title"]):
            # Prepare data
            paper_data = {
                "article_title": row["Article Title"],
                "authors": row.get("Author(s)", "Unknown"),
                "contact_info": row.get("Contact Info.", None),
                "year_published": int(row["Year Published"]) if not pd.isna(row["Year Published"]) else None,
                "institution": row.get("Institution", None),
                "num_publications_used": int(row["# of publications used"]) if not pd.isna(row["# of publications used"]) and str(row["# of publications used"]).isdigit() else 0,
                "full_link": row.get("Article Link", None),
                "shortened_link": row.get("Shortened article link", None),
                "is_duplicate": row["Duplicate?"].strip().lower() == "unique" if "Duplicate?" in row else True,
                "qual_score_method": row.get("Qual. Score Method", None),
                "study_type": row.get("Meta-analysis or Sytematic Review", None),
                "qualsyst_criteria": row.get("QualSyst", None),
            }

            # Replace NaN values with None
            paper_data = {key: (None if isinstance(value, float) and math.isnan(value) else value) for key, value in paper_data.items()}

            # Check for duplicates
            response = requests.get(API_URL, params={"title": paper_data["article_title"]})
            if response.status_code == 200 and response.json():  # Paper exists
                print(f"Duplicate found. Skipping: {row['Article Title']}")
                continue

            print("Data being sent:", paper_data)

            # Post data
            response = requests.post(API_URL, json=paper_data)
            if response.status_code == 201:
                print(f"Successfully added: {row['Article Title']}")
            else:
                print(f"Failed to add: {row['Article Title']} - Status Code: {response.status_code}")

    except Exception as e:
        print(f"Error processing entry: {row.get('Article Title', 'Unknown')} - {e}")
