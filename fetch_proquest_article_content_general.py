import pandas as pd
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
import os


# Function to download PDF from a URL
def download_pdf(pdf_url, save_path):
    response = requests.get(pdf_url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {save_path}")
    else:
        print(f"Failed to download PDF: {pdf_url}")


# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return ""


# Main script
def process_excel_and_scrape_pdfs(excel_file, output_dir):
    # Read the Excel file
    df = pd.read_excel(excel_file)
    if 'Article Link' not in df.columns:
        print("Column 'Article Link' not found in the Excel file.")
        return

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Iterate through links
    for index, link in enumerate(df['Article Link']):
        try:
            response = requests.get(link)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the download PDF button (update this selector based on the website)
            pdf_button = soup.find('a', href=True, text=lambda t: t and "PDF" in t.upper())
            if pdf_button:
                pdf_url = pdf_button['href']
                if not pdf_url.startswith('http'):
                    # Make it absolute if it's relative
                    pdf_url = requests.compat.urljoin(link, pdf_url)

                # Download the PDF
                pdf_path = os.path.join(output_dir, f"article_{index + 1}.pdf")
                download_pdf(pdf_url, pdf_path)

                # Extract text from the PDF
                pdf_text = extract_text_from_pdf(pdf_path)
                print(f"Extracted text for article {index + 1}:\n", pdf_text[:500])  # Preview first 500 chars
            else:
                print(f"No PDF found for article {index + 1} at {link}")
        except Exception as e:
            print(f"Error processing link {link}: {e}")


# Run the script with your file path
excel_file = r"C:\Users\Pixel\OneDrive\Documents\compiled_journal_articles.xlsx"
output_dir = "downloaded_pdfs"
process_excel_and_scrape_pdfs(excel_file, output_dir)
