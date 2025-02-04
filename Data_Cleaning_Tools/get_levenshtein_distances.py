import pandas as pd
import os
from Levenshtein import distance as levenshtein_distance

# Note that levenshtein distances are being calculated with "Article Title"
# File path
file_name = "training_data_new.csv"
base_directory = os.path.join(os.path.expanduser("~"), "PycharmProjects", "IEEE_QualSyst", "Databases",
                                      "relevance_algo_training_data")
file_path = os.path.join(base_directory, file_name)

# Read the CSV file
df = pd.read_csv(file_path, dtype=str)

# Check if the column exists
if "Article Title" not in df.columns:
    raise ValueError("Column 'Article Title' not found in the CSV file.")

# Drop NaN values and ensure it's a list of strings
titles = df["Article Title"].dropna().astype(str).tolist()

# Ensure there is at least one entry
if len(titles) == 0:
    raise ValueError("No valid 'Article Title' entries found in the file.")

# List to store minimum distances for each title
min_distances = []

# Iterate over each title as a reference
for idx, reference_title in enumerate(titles):
    distances = set()

    # Compare with every other title
    for j, title in enumerate(titles):
        if idx != j:  # Skip self-comparison
            distance = levenshtein_distance(reference_title.lower(), title.lower())
            distances.add(distance)

    # Append the minimum distance found
    min_distances.append(min(distances) if distances else 0)

# Add the new column to the DataFrame
df["Min Levenshtein Distance"] = min_distances

# Save the updated DataFrame
output_file_path = file_path.replace(".csv", "_with_distances.csv")
df.to_csv(output_file_path, index=False)

print(f"Updated file saved to: {output_file_path}")
