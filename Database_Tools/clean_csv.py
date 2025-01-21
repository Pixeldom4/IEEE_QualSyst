import pandas as pd
import os

base_dir = os.path.dirname(__file__)

# Define the paths to the input and output directories
input_files = [
    os.path.join(base_dir, "../Databases/compiled_ovid.csv"),
    os.path.join(base_dir, "../Databases/compiled_proquest.csv"),
]
output_dir = "../Databases/Cleaned/"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Define required columns and their default values
required_columns = {
    "article title": None,
    "author(s)": "Unknown",
    "olivia (article link)": None,
}

def clean_csv(file_path, output_dir):
    """Clean the CSV file and save it to the output directory."""
    try:
        # Load the file
        df = pd.read_csv(file_path, header=0)
        print(f"Processing file: {file_path}")
        print(f"Columns before cleaning: {df.columns.tolist()}")

        # Normalize column names
        df.columns = df.columns.str.strip().str.lower()

        # Add missing required columns
        for col, default_value in required_columns.items():
            if col not in df.columns:
                print(f"Adding missing column: {col}")
                df[col] = default_value

        # Drop rows missing essential values in `article title` or `olivia (article link)`
        df = df.dropna(subset=["article title", "olivia (article link)"])

        # Fill missing values for `author(s)` with "Unknown"
        df["author(s)"] = df["author(s)"].fillna("Unknown")

        # Save the cleaned file
        output_path = os.path.join(output_dir, os.path.basename(file_path))
        df.to_csv(output_path, index=False)
        print(f"File cleaned and saved to: {output_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Process all files
for file in input_files:
    clean_csv(file, output_dir)
