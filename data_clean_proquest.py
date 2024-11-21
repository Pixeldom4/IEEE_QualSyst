import os
import pandas as pd
import glob

# Define the folder containing the CSV files
folder_path = r"C:\Users\Pixel\OneDrive\Documents\Proquest_Papers"
output_file = r"C:\Users\Pixel\OneDrive\Documents\compiled_filtered_data.xlsx"

# Ensure the output directory exists
output_dir = os.path.dirname(output_file)
os.makedirs(output_dir, exist_ok=True)

# List all CSV files in the folder
csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
print(f"Found CSV files: {csv_files}")

# Initialize an empty DataFrame to store all filtered data
compiled_data = pd.DataFrame()

# Loop through each file and process it
for file in csv_files:
    try:
        # Load the CSV file
        df = pd.read_csv(file)

        # Debugging: Print the first few rows of the DataFrame
        print(f"Processing file: {file}")
        print(df.head())

        # Check if "Article Link" column exists
        if "Article Link" in df.columns:
            # Filter rows where "Article Link" contains 'sourcetype=Scholarly%20Journals'
            filtered_df = df[df["Article Link"].str.contains("sourcetype=Scholarly%20Journals", na=False)]
            print(f"Filtered rows: {len(filtered_df)}")
            compiled_data = pd.concat([compiled_data, filtered_df], ignore_index=True)
        else:
            print(f"'Article Link' column not found in {file}")
    except Exception as e:
        print(f"Error processing file {file}: {e}")

# Save the compiled data to a single Excel file if not empty
if not compiled_data.empty:
    compiled_data.to_excel(output_file, index=False)
    print(f"All filtered data compiled and saved to: {output_file}")
else:
    print("No matching data found. No file was saved.")
