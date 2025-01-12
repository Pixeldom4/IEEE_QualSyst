import pandas as pd
import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF


def remove_illegal_characters(text):
    # Filter out any non-printable characters that could cause issues in Excel
    return ''.join(char for char in text if char.isprintable())


def fetch_article_content(excel_file_path):
    # Load the Excel file
    df = pd.read_excel(excel_file_path)

    # Define headers to simulate a browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Define lists to store results
    titles = []
    full_texts = []

    # Iterate over the rows in the DataFrame
    for index, row in df.iterrows():
        link = row['Link']

        # Check if the link is valid and not NaN
        if isinstance(link, str) and (link.endswith(".pdf") or link.startswith("http")):
            try:
                if link.endswith(".pdf"):
                    # Handle PDF link
                    response = requests.get(link, headers=headers)
                    response.raise_for_status()

                    # Save PDF temporarily
                    with open("temp_article.pdf", "wb") as pdf_file:
                        pdf_file.write(response.content)

                    # Extract text from the PDF
                    pdf_text = ""
                    title_lines = []  # To collect multiple lines for the title
                    with fitz.open("temp_article.pdf") as pdf_doc:
                        for page_num, page in enumerate(pdf_doc):
                            if page_num == 0:  # Extract title from the first page
                                first_page_text = page.get_text().splitlines()
                                title_lines = first_page_text[:3]  # Take the first three lines
                            pdf_text += page.get_text()

                    # Join collected title lines with line breaks
                    title = '\n'.join(title_lines) if title_lines else row['Title']
                    clean_text = remove_illegal_characters(pdf_text)
                    titles.append(title)
                    full_texts.append(clean_text)

                else:
                    # Handle regular HTML link
                    response = requests.get(link, headers=headers)
                    response.raise_for_status()

                    # Parse HTML with BeautifulSoup
                    soup = BeautifulSoup(response.content, 'html.parser')
                    title = soup.title.string if soup.title else row['Title']
                    full_text = ' '.join([p.get_text() for p in soup.find_all('p')])

                    # Remove illegal characters
                    clean_text = remove_illegal_characters(full_text)
                    titles.append(title)
                    full_texts.append(clean_text)

            except Exception as e:
                print(f"Failed to fetch article at {link}: {e}")
                titles.append(row['Title'] if 'Title' in row else "Title Not Found")
                full_texts.append(None)
        else:
            # Handle NaN or invalid link cases
            print(f"Invalid or missing link at row {index}: {link}")
            titles.append(row['Title'] if 'Title' in row else "Title Not Found")
            full_texts.append(None)

    # Update the DataFrame with the fetched data
    df['Title'] = titles
    df['Full-Text'] = full_texts

    # Overwrite the existing Excel file with updated data
    df.to_excel(excel_file_path, index=False)
    print(f"Updated file saved to '{excel_file_path}'")


# Usage
fetch_article_content(r"C:\Users\Pixel\OneDrive\Documents\DEIPaper\DEI_Quan.xlsx")
