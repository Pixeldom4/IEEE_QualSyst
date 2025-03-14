import pandas as pd
import os
from Levenshtein import distance as levenshtein_distance

def calculate_min_levenshtein_distances(file_path: str, column_name: str = "Article Title"):
    """
    Calculates the minimum Levenshtein distance for each entry in a given column of a CSV file.
    Returns the updated file path with "_with_distances.csv" appended.
    """
    # Ensure the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ Error: File '{file_path}' not found. Please check the path.")

    # Read the CSV file
    df = pd.read_csv(file_path, dtype=str)

    # Check if the specified column exists
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in the CSV file.")

    # Drop NaN values and convert to a list of strings
    titles = df[column_name].dropna().astype(str).tolist()

    # Ensure there is at least one entry
    if not titles:
        raise ValueError(f"No valid '{column_name}' entries found in the file.")

    # Compute minimum Levenshtein distances
    min_distances = []
    for idx, reference_title in enumerate(titles):
        distances = [levenshtein_distance(reference_title.lower(), title.lower())
                     for j, title in enumerate(titles) if idx != j]
        min_distances.append(min(distances) if distances else 0)

    # Add the new column to the DataFrame
    df["Min Levenshtein Distance"] = min_distances

    # Save the updated DataFrame
    output_file_path = file_path.replace(".csv", "_with_distances.csv")
    df.to_csv(output_file_path, index=False)

    print(f"\n✅ Updated file saved to: {output_file_path}")
    return output_file_path  # Return new file path
