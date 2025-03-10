from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Function to scrape data
def scrape_website(url):
    # Set up Selenium WebDriver with webdriver-manager
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # Automatically download and manage the ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Load the website
        driver.get(url)

        # Wait for JavaScript to load (adjust if necessary)
        driver.implicitly_wait(5)

        # Extract the page source
        page_source = driver.page_source

        # Example: Interact with the page or parse the HTML
        print(page_source[:500])  # Print the first 500 characters of the page source

    finally:
        driver.quit()

# Example usage
if __name__ == "__main__":
    url = "https://m.italianmoda.com/companies/clothing/women/classic-and-chic"  # Replace with the target website
    scrape_website(url)
