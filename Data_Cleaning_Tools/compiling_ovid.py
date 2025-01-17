import os
import pandas as pd

# Path to the folder containing the CSV files
folder_path = r"C:\Users\Pixel\Downloads\Ovid_Uncompiled"

# Loop through all files in the folder
for file_name in os.listdir(folder_path):
    # Check if the file is a CSV
    if file_name.endswith(".csv"):
        file_path = os.path.join(folder_path, file_name)

        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Add a new column with the name of the file (without the .csv extension)
        df['Search Terms'] = os.path.splitext(file_name)[0]

        # Save the updated DataFrame back to the CSV file
        df.to_csv(file_path, index=False)
