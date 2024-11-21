from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
from selenium.common.exceptions import NoSuchElementException

def fetch_proquest_text(driver, proquest_url):
    # Navigate to the ProQuest URL
    driver.get(proquest_url)

    # Wait for the page to load and look for "Download PDF"
    time.sleep(5)  # Adjust as needed for page load time
    try:
        download_pdf_button = driver.find_element(By.LINK_TEXT, "Download PDF")
        download_pdf_button.click()
    except NoSuchElementException:
        print(f"Could not find 'Download PDF' button on {proquest_url}")
        return None

    # Switch to the new tab that opens with the PDF
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(5)  # Wait for the PDF to load in the new tab

    # Extract text from the PDF viewer (assuming it's selectable text)
    try:
        pdf_text = driver.find_element(By.TAG_NAME, "body").text
    except NoSuchElementException:
        print("Failed to extract text from PDF viewer.")
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

    # Add a "Full-Text" column if it does not exist
    if "Full-Text" not in df.columns:
        df["Full-Text"] = None

    # Initialize the WebDriver using ChromeDriverManager
    driver = webdriver.Chrome(ChromeDriverManager().install())

    try:
        # Ensure the user logs in manually to ProQuest
        proquest_login_url = "https://www.proquest.com/"  # Replace with actual login URL if different
        driver.get(proquest_login_url)
        input("Please log in to ProQuest and press Enter to continue...")

        # Iterate over each link in the "Article Link" column
        for index, row in df.iterrows():
            proquest_url = row["Article Link"]
            if pd.notna(proquest_url):
                print(f"Processing link: {proquest_url}")
                full_text = fetch_proquest_text(driver, proquest_url)

                # Append the full text to the "Full-Text" column
                df.at[index, "Full-Text"] = full_text
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
file_path = r"C:\Users\Pixel\OneDrive\Documents\compiled_filtered_data.xlsx"
process_excel(file_path)
