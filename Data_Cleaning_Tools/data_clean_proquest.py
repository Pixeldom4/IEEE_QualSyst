import pandas as pd
import requests
from bs4 import BeautifulSoup

# Load Excel file
file_path = r"C:\Users\Pixel\OneDrive\Documents\compiled_journal_articles.xlsx"
df = pd.read_excel(file_path)

# Ensure "Article Title" column exists
if 'Article Title' not in df.columns:
    raise ValueError("The column 'Article Title' is not found in the Excel file.")

# Remove double quotes around items in the 'Article Title' column
df['Article Title'] = df['Article Title'].str.strip('"')

# Save the updated DataFrame back to a new Excel file
output_file_path = 'updated_file_without_quotes.xlsx'
df.to_excel(output_file_path, index=False)

print(f"Updated Excel file saved to {output_file_path}")

