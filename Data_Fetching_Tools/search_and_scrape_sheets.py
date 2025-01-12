import pandas as pd
import gspread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from oauth2client.client import flow_from_clientsecrets

# Set up the scopes for Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Path to the OAuth credentials file
client_secret_file = r"C:\Users\Pixel\Downloads\desktop_OAuth.json"  # Replace with the downloaded OAuth JSON file


# Authenticate with OAuth
def authenticate_with_oauth():
    storage = Storage('credentials.json')  # Save credentials locally
    credentials = storage.get()

    if not credentials or credentials.invalid:
        flow = flow_from_clientsecrets(client_secret_file, SCOPES)
        credentials = run_flow(flow, storage)

    return credentials


# Authenticate and access Google Sheets
credentials = authenticate_with_oauth()
gc = gspread.authorize(credentials)

# Open the Google Sheet
sheet_name = "compiled_journal_articles_test"  # Replace with your Google Sheet name
spreadsheet = gc.open(sheet_name)
worksheet = spreadsheet.sheet1

# Load Excel file
file_path = r"C:\Users\Pixel\OneDrive\Documents\compiled_journal_articles_test.xlsx"
df = pd.read_excel(file_path)

# Strip column names to avoid issues
df.columns = df.columns.str.strip()

if 'Article Title' not in df.columns:
    raise ValueError("The column 'Article Title' is not found in the Excel file.")

# Set up Selenium WebDriver
driver_path = r"C:\Users\Pixel\Downloads\chromedriver-win32\chromedriver-win32\chromedriver.exe"  # Replace with the path to your ChromeDriver
driver = webdriver.Chrome(executable_path=driver_path)

# Google Scholar URL
google_scholar_url = "https://scholar.google.com/"


def search_and_scrape(article_title):
    try:
        print(f"Searching for: {article_title}")
        driver.get(google_scholar_url)

        # Locate the search box and perform the search
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.clear()
        search_box.send_keys(article_title)
        search_box.send_keys(Keys.RETURN)

        # Wait for results to load and get the first result
        results = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".gs_rt a"))
        )
        if results:
            first_result = results[0]
            article_url = first_result.get_attribute("href")
            print(f"Found URL: {article_url}")

            # Navigate to the article link
            driver.get(article_url)

            # Wait for the <pre> or content element to load
            try:
                pre_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//pre"))
                )
                content = pre_element.text
            except Exception:
                # Fallback to body text if <pre> tag not found
                content = driver.find_element(By.TAG_NAME, "body").text
                print(f"Content extracted: {content[:500]}...")  # Show the first 500 characters

            return content if content else "No content found."
        else:
            return "No results found."
    except Exception as e:
        print(f"Error occurred: {e}")
        return f"Error: {e}"


# Append data to the Google Sheet
worksheet.append_row(['Article Title', 'Article Content'])  # Add column headers if not present

for index, row in df.iterrows():
    article_title = row['Article Title']
    article_content = search_and_scrape(article_title)
    worksheet.append_row([article_title, article_content])

# Close the browser
driver.quit()

print("Data successfully appended to Google Sheets.")
