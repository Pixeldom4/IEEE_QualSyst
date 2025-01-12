import pandas as pd

def clean_article_links_inplace(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)

    # Check if the 'Article Link' column exists
    if 'Article Link' in df.columns:
        # Strip quotation marks from links in the 'Article Link' column
        df['Article Link'] = df['Article Link'].str.replace('"', '', regex=False)

        # Save the updated DataFrame back to the original file
        df.to_excel(file_path, index=False)
        print(f"Links cleaned and saved back to the original file: {file_path}")
    else:
        print("The 'Article Link' column does not exist in the provided file.")

# Usage
file_path = r"C:\Users\Pixel\OneDrive\Documents\compiled_journal_articles.xlsx"
clean_article_links_inplace(file_path)
