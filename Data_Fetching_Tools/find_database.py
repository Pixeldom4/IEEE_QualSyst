import time
import pandas as pd
from urllib.parse import urlparse
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options  # <-- import Options

# Define file paths and chromedriver path
input_file = r"C:\Users\Pixel\PycharmProjects\IEEE_QualSyst\Databases\search_and_scrape_data\filtering_training_data_10.csv"
chromedriver_path = r"C:\Users\Pixel\Downloads\chromedriver-win64\chromedriver.exe"

# Split into the base path and extension
base, ext = os.path.splitext(input_file)
output_file = f"{base}_databases{ext}"

# Set up Chrome options to run headless
chrome_options = Options()
chrome_options.add_argument("--headless")

# Create the Chrome WebDriver in headless mode
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Read the input CSV file using pandas
data = pd.read_csv(input_file)

# List to collect results
results = []

# Loop over each row in the input CSV
for index, row in data.iterrows():
    article_title = row['Article Title']
    print(f"Searching for: {article_title}")

    # Navigate to Google Scholar
    driver.get("https://scholar.google.com")

    try:
        # Wait for the search box to load (Google Scholar uses the name "q")
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        # Clear the search box (if needed) and enter the article title
        search_box.clear()
        search_box.send_keys(article_title)
        search_box.send_keys(Keys.RETURN)

        # Wait for the search results to load; Google Scholar results usually contain an <h3> element with class "gs_rt"
        first_result = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h3.gs_rt a"))
        )
        first_link = first_result.get_attribute("href")
        print(f"First result URL: {first_link}")

        # Use the URL's domain as the "database"
        parsed_url = urlparse(first_link)
        database = parsed_url.netloc

    except Exception as e:
        print(f"Error processing '{article_title}': {e}")
        first_link = ""
        database = ""

    # Append the scraped information to the results list
    results.append({
        "Article Title": article_title,
        "First Link": first_link,
        "Database": database
    })

    # Pause between searches to avoid overwhelming Google Scholar
    time.sleep(3)

# Close the browser after processing all rows
driver.quit()

# Write the results to the output CSV file
output_df = pd.DataFrame(results)
output_df.to_csv(output_file, index=False)

print("Scraping complete. Results saved to:", output_file)
