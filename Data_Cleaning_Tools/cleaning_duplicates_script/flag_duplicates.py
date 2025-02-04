import pandas as pd
import os

def flag_duplicates(file_path):
    """
    Analyzes duplicates in 'Article Abstract', 'Article Authors', and 'Article Title'.
    Reports:
    - The total count of duplicates per column.
    - The top 5 most common duplicate values per column.
    """

    # Ensure the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ Error: File '{file_path}' not found. Please check the path.")

    # Read CSV file
    df = pd.read_csv(file_path, dtype=str)

    duplicate_reports = {}
    columns_to_check = ["Article Abstract", "Article Authors", "Article Title"]

    # Analyze duplicates in each column
    for col in columns_to_check:
        if col in df.columns:
            valid_entries = df[(df[col].notna()) & (df[col].str.lower() != "none") & (df[col] != "")]
            duplicate_counts = valid_entries[col].value_counts()
            duplicate_values = duplicate_counts[duplicate_counts > 1]  # Only values with duplicates
            duplicate_reports[col] = duplicate_values

    # Print summary of duplicates
    print("\n🔎 Duplicate Analysis Report:")
    for col, duplicates in duplicate_reports.items():
        print(f"\n📌 {col}:")
        print(f"Total duplicate values: {len(duplicates)}")
        if not duplicates.empty:
            print("Top 5 most common duplicates:")
            print(duplicates.head(5).to_string())

    # Count total flagged duplicate rows (rows where at least one of the three fields is duplicated)
    total_duplicate_rows = df.duplicated(subset=columns_to_check, keep=False).sum()
    print(f"\n🟢 Total rows flagged as duplicate: {total_duplicate_rows} / {len(df)}")

    return {
        "total_duplicates": {col: len(duplicates) for col, duplicates in duplicate_reports.items()},
        "top_5_duplicates": {col: duplicates.head(5) for col, duplicates in duplicate_reports.items()}
    }
