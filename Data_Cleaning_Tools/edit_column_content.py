import pandas as pd

def clean_article_titles_inplace(file_path):
    """
    Reads a CSV file, removes quotation marks from the 'Article Title' column,
    removes the text 'article title:' from that column,
    strips leading/trailing whitespace,
    then saves the result back to the same CSV file.
    """
    # Read the CSV file
    df = pd.read_csv(file_path)

    # Check if the 'Article Title' column exists
    if 'Article Title' in df.columns:
        # 1) Remove all quotation marks
        df['Article Title'] = df['Article Title'].str.replace('"', '', regex=False)

        # 2) Remove the text "article title:" (case-sensitive)
        df['Article Title'] = df['Article Title'].str.replace("article title:", "", regex=False)

        # 3) Strip any leftover leading/trailing whitespace
        df['Article Title'] = df['Article Title'].str.strip()

        # Save the updated DataFrame back to the original CSV
        df.to_csv(file_path, index=False)
        print(f"Titles cleaned and saved back to the original file: {file_path}")
    else:
        print("The 'Article Title' column does not exist in the provided file.")


# Usage example
if __name__ == "__main__":
    file_path = r"C:\Users\Pixel\PycharmProjects\IEEE_QualSyst\Databases\search_and_scrape_data\filtering_training_data_truncated.csv"
    clean_article_titles_inplace(file_path)
