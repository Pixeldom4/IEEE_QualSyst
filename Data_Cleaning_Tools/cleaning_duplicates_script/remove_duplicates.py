import pandas as pd
import os

def remove_duplicates(file_path):
    """
    Reads a CSV file, removes duplicate rows where all 3 fields match or if the Levenshtein distance is 0,
    then saves the cleaned data to a new CSV file.
    """
    # Ensure the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: File '{file_path}' not found.")

    # Read CSV file
    df = pd.read_csv(file_path, dtype=str)

    # Ensure required columns exist
    required_columns = ["Article Abstract", "Article Authors", "Article Title", "Min Levenshtein Distance"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in DataFrame. Ensure data is correctly formatted.")

    # Convert Levenshtein distance column to integer (CSV import may store it as string)
    df["Min Levenshtein Distance"] = pd.to_numeric(df["Min Levenshtein Distance"], errors="coerce").fillna(0).astype(int)

    # Standardize text data: Remove leading/trailing spaces and lowercase for consistency
    for col in ["Article Abstract", "Article Authors", "Article Title"]:
        df[col] = df[col].astype(str).str.strip().str.lower()

    # Identify exact duplicates
    exact_duplicate_rows = df.duplicated(subset=["Article Abstract", "Article Authors", "Article Title"], keep="first")
    num_exact_duplicates = exact_duplicate_rows.sum()

    # Remove exact duplicates
    df_cleaned = df[~exact_duplicate_rows]

    # Remove rows where Levenshtein distance is 0
    num_levenshtein_0 = (df_cleaned["Min Levenshtein Distance"] == 0).sum()
    df_cleaned = df_cleaned[df_cleaned["Min Levenshtein Distance"] > 0].reset_index(drop=True)

    # Save the cleaned file
    cleaned_file_path = file_path.replace(".csv", "_cleaned.csv")
    df_cleaned.to_csv(cleaned_file_path, index=False)

    # Print summary
    print(f"\nRemoved {num_exact_duplicates} exact duplicate rows.")
    print(f"Removed {num_levenshtein_0} rows with Levenshtein distance of 0.")
    print(f"Total rows removed: {num_exact_duplicates + num_levenshtein_0}")
    print(f"Cleaned data saved to: {cleaned_file_path}")

    return cleaned_file_path
