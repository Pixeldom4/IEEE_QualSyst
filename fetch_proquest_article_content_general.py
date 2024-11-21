from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import requests
from PyPDF2 import PdfReader
from io import BytesIO
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

def fetch_proquest_text(driver, proquest_url):
    # Navigate to the ProQuest URL
    driver.get(proquest_url)

    # Wait for the page to load
    time.sleep(5)  # Adjust as needed for page load time

    # Attempt to click the "Accept all" button for cookies
    try:
        accept_all_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept all')]"))
        )
        accept_all_button.click()
        print("Accepted cookies.")
    except NoSuchElementException:
        print("No 'Accept all' button found.")
    except Exception as e:
        print(f"Failed to click 'Accept all' button: {e}")

    # Now attempt to click "Get full text"
    try:
        get_full_text_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Get full text"))
        )
        get_full_text_button.click()
    except NoSuchElementException:
        print(f"Could not find 'Get full text' button on {proquest_url}")
        return None
    except Exception as e:
        print(f"Error clicking 'Get full text' button: {e}")
        return None

    # Switch to the new tab that opens with the PDF
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(5)  # Wait for the PDF to load in the new tab

    # Get the PDF URL and download it
    pdf_url = driver.current_url
    response = requests.get(pdf_url)
    if response.status_code != 200:
        print("Failed to download the PDF.")
        return None

    # Use PdfReader to extract text from the downloaded PDF
    pdf_text = ""
    try:
        pdf_file = BytesIO(response.content)
        pdf_reader = PdfReader(pdf_file)
        for page in pdf_reader.pages:
            pdf_text += page.extract_text()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        pdf_text = None

    # Close the PDF tab and switch back to the original tab
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    return pdf_text

def process_excel(file_path):
    # Load the Excel file
    df = pd.read_excel(file_path)

    # Check if "Article Link" column exists
    if "Article Link" not in df.columns:
        print("No 'Article Link' column found in the provided file.")
        return

    # Add a "Full-Text" column if it does not exist and set it as type 'object' for text compatibility
    if "Full-Text" not in df.columns:
        df["Full-Text"] = None
    df["Full-Text"] = df["Full-Text"].astype(object)  # Explicitly set as text-compatible type

    # Initialize the WebDriver using ChromeDriverManager
    driver = webdriver.Chrome(ChromeDriverManager().install())

    try:
        # Iterate over each link in the "Article Link" column
        for index, row in df.iterrows():
            proquest_url = row["Article Link"]

            # Strip any extraneous quotes or whitespace from the URL
            proquest_url = proquest_url.strip().strip('"')

            if pd.notna(proquest_url):
                print(f"Processing link: {proquest_url}")
                full_text = fetch_proquest_text(driver, proquest_url)

                # Append the full text to the "Full-Text" column
                df.at[index, "Full-Text"] = full_text if full_text is not None else ""
            else:
                print(f"No link found for row {index}")

    except Exception as e:
        print("An error occurred:", e)

    finally:
        driver.quit()

    # Save the updated Excel file
    df.to_excel(file_path, index=False)
    print("Updated Excel file saved.")


# Usage Example
file_path = r"C:\Users\Pixel\OneDrive\Documents\Proquest_Papers\test_data_link.xlsx"
process_excel(file_path)
