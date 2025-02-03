import pandas as pd
import os

def flag_duplicates(file_name, base_directory=None):
    """Finds and flags duplicates in 'Article Abstract', 'Article Authors', or 'Article Title'."""

    # Default directory
    if base_directory is None:
        base_directory = os.path.join(os.path.expanduser("~"), "PycharmProjects", "IEEE_QualSyst", "Databases",
                                      "Training_Data", "relevance_algo")

    # Construct the full file path
    file_path = os.path.join(base_directory, file_name)

    # Read CSV file
    df = pd.read_csv(file_path, dtype=str)

    duplicate_reports = {}
    columns_to_check = ["Article Abstract", "Article Authors", "Article Title"]

    # Track row indices that are duplicates
    duplicate_indices = set()

    for col in columns_to_check:
        if col in df.columns:
            valid_entries = df[(df[col].notna()) & (df[col].str.lower() != "none") & (df[col] != "")]
            duplicate_counts = valid_entries[col].value_counts()
            duplicate_values = duplicate_counts[duplicate_counts > 1]  # Only values with duplicates
            duplicate_reports[col] = duplicate_values

            # Collect row indices that contain duplicates
            duplicate_rows = df[df[col].isin(duplicate_values.index)].index
            duplicate_indices.update(duplicate_rows)

    # Find rows that have duplicates in multiple columns
    df["is_duplicate"] = df.index.isin(duplicate_indices)

    # Print summary
    for col, duplicates in duplicate_reports.items():
        print(f"Total {col} duplicate values: {len(duplicates)}")
        print(f"Top 6 most common duplicates in '{col}':")
        print(duplicates.head(6).to_string())

    print(f"\nTotal duplicate rows flagged: {df['is_duplicate'].sum()} / {len(df)}")

    return df, file_path  # Return the DataFrame and file path for use in the next function


def remove_duplicates(df, file_path):
    """Removes duplicate rows and saves the cleaned data to a new CSV file."""

    # Drop duplicate rows and reset index
    df_cleaned = df.drop_duplicates(subset=["Article Abstract", "Article Authors", "Article Title"], keep="first").reset_index(drop=True)

    # Save the cleaned file
    cleaned_file_path = file_path.replace(".csv", "_cleaned.csv")
    df_cleaned.to_csv(cleaned_file_path, index=False)

    print(f"\n Removed {len(df) - len(df_cleaned)} duplicate rows.")
    print(f" Cleaned data saved to: {cleaned_file_path}")


# Example usage
file_name = "training_data.csv"
df_with_duplicates, file_path = flag_duplicates(file_name)

# Remove duplicates option
user_input = input("\nInput [y] to remove duplicates and save a cleaned version, or input [n] to stop the script: ").strip().lower()

if user_input == "n":
    print("\nScript stopped. No changes were made.")
elif user_input == "y":
    remove_duplicates(df_with_duplicates, file_path)
