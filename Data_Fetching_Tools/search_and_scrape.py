import pandas as pd
import tldextract
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class GoogleScholarScraper:
    """
    An OOP class to:
      1) Load article titles from a CSV.
      2) Search each title on Google Scholar using Selenium.
      3) Extract the page content and the domain name (database).
      4) Save the results to a new CSV.
    """

    def __init__(self, input_file_path, output_file_path, driver_path, headless=True):
        """
        :param input_file_path: Path to the input CSV file (containing 'Article Title').
        :param output_file_path: Where to save the final CSV with scraped content.
        :param driver_path: Path to the ChromeDriver executable.
        :param headless: Whether to run Chrome in headless mode (no GUI).
        """
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.driver_path = driver_path
        self.headless = headless
        self.df = None
        self.driver = None

    def load_data(self):
        """Load the CSV data, remove 'Unnamed' columns, verify 'Article Title' column, and drop NaN rows."""
        df = pd.read_csv(self.input_file_path)

        # 1) Remove columns whose name starts with "Unnamed"
        df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

        # Strip column names to avoid issues with extra whitespace
        df.columns = df.columns.str.strip()

        # Check that 'Article Title' is in the DataFrame
        if 'Article Title' not in df.columns:
            raise ValueError("The column 'Article Title' is not found in the CSV file.")

        # Drop NaN values in the 'Article Title' column
        df.dropna(subset=['Article Title'], inplace=True)

        self.df = df

    def init_driver(self):
        """Set up the Selenium Chrome WebDriver."""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")

        service = Service(self.driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def search_article(self, article_title):
        """
        Searches for an article title on Google Scholar, returns:
          - The scraped content (string)
          - The domain from which the content was retrieved
        """
        google_scholar_url = "https://scholar.google.com/"
        try:
            print(f"Searching for: {article_title}")
            self.driver.get(google_scholar_url)

            # Wait for the search box, clear it, and enter the article title
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            search_box.clear()
            search_box.send_keys(article_title)
            search_box.send_keys(Keys.RETURN)

            # Wait for the first result link
            results = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".gs_rt a"))
            )

            if results:
                first_result = results[0]
                article_url = first_result.get_attribute("href")
                print(f"Found URL: {article_url}")

                # Inline domain extraction
                # For example: sciencedirect.com, neurology.org, etc.
                extracted = tldextract.extract(article_url)
                database = (
                    f"{extracted.domain}.{extracted.suffix}" if extracted.suffix else extracted.domain
                )

                # Navigate to the article page
                self.driver.get(article_url)

                # Try to scrape from a <pre> element first; otherwise, fallback to the body
                try:
                    pre_element = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//pre"))
                    )
                    content = pre_element.text
                except Exception:
                    # Fallback: scrape the entire body text
                    content = self.driver.find_element(By.TAG_NAME, "body").text
                    print(f"Content extracted (first 500 chars): {content[:500]}...")

                return content if content else "No content found.", database
            else:
                return "No results found.", ""
        except Exception as e:
            print(f"Error occurred while searching '{article_title}': {e}")
            return f"Error: {e}", ""

    def scrape_articles(self):
        """
        Loop over each row, scrape the article, store the content and the domain in new columns.
        """
        contents = []
        databases = []

        for index, row in self.df.iterrows():
            article_title = row['Article Title']
            content, database = self.search_article(article_title)
            contents.append(content)
            databases.append(database)

        self.df['Article Content'] = contents
        self.df['Database'] = databases

    def save_data(self):
        """Write the updated DataFrame to the output CSV file."""
        self.df.to_csv(self.output_file_path, index=False)
        print(f"Updated CSV file saved to {self.output_file_path}")

    def run(self):
        """
        High-level method to run the entire process:
          1) Load data
          2) Initialize driver
          3) Scrape articles
          4) Quit driver
          5) Save results
        """
        self.load_data()
        self.init_driver()
        self.scrape_articles()
        self.driver.quit()
        self.save_data()


# -------------------------
#  Usage Example
# -------------------------
if __name__ == "__main__":
    # Adjust paths as needed
    input_file = r"C:\Users\Pixel\PycharmProjects\IEEE_QualSyst\Databases\search_and_scrape_data\filtering_training_data_truncated.csv"
    output_file = r"C:\Users\Pixel\PycharmProjects\IEEE_QualSyst\Databases\search_and_scrape_data\training_data_scraped.csv"
    chromedriver_path = r"C:\Users\Pixel\Downloads\chromedriver-win64\chromedriver.exe"

    # Create scraper instance
    scraper = GoogleScholarScraper(
        input_file_path=input_file,
        output_file_path=output_file,
        driver_path=chromedriver_path,
        headless=False  # Change to True if you want headless
    )

    # Run everything
    scraper.run()
