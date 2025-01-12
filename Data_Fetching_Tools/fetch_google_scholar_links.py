import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

def fetch_google_scholar_links(search_query, num_pages=1):
    base_url = "https://scholar.google.com/scholar"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    article_links = []

    for page in range(num_pages):
        start = page * 10
        params = {"q": search_query, "hl": "en", "start": start}
        response = requests.get(base_url, headers=headers, params=params)

        # Check for a valid response
        if response.status_code != 200:
            print("Request was blocked or failed. Status Code:", response.status_code)
            break

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract links based on current HTML structure
        for result in soup.find_all("h3", {"class": "gs_rt"}):
            link = result.a['href'] if result.a else None
            if link:
                article_links.append(link)

        time.sleep(2)  # Pause to avoid being blocked

    return article_links

def append_links_to_excel(excel_file_path, search_query, num_pages=1):
    # Load the existing Excel file
    df = pd.read_excel(excel_file_path)

    # Fetch links from Google Scholar across multiple pages
    article_links = fetch_google_scholar_links(search_query, num_pages=num_pages)

    if not article_links:
        print("No links were found.")
        return

    # Find the first available blank cell in the 'Link' column
    first_empty_index = df['Link'].first_valid_index() + 1 if df['Link'].isnull().all() else df['Link'].last_valid_index() + 1
    for link in article_links:
        if first_empty_index < len(df):
            df.at[first_empty_index, 'Link'] = link
        else:
            # Append at the end if no empty rows are available
            df = df.append({'Link': link}, ignore_index=True)
        first_empty_index += 1

    # Save back to the Excel file
    df.to_excel(excel_file_path, index=False)
    print(f"Updated file saved to '{excel_file_path}' with {len(article_links)} links added to the 'Link' column.")

# Usage
append_links_to_excel(r"C:\Users\Pixel\OneDrive\Documents\DEIPaper\DEI_Quan.xlsx", "DEI filetype:pdf", num_pages=1)
