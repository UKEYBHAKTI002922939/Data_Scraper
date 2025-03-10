from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import pandas as pd

# Setup Selenium WebDriver
def setup_driver():
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless (without GUI)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # Initialize Chrome WebDriver using WebDriverManager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

# Scrape the page
def scrape_page_details(url):
    driver = setup_driver()

    try:
        # Navigate to the page
        driver.get(url)

        # Wait for the page to load (adjust sleep time if necessary)
        time.sleep(3)

        # Get the page source
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Extract Name (from <a> tags with modal_iframe_open in onclick)
        names = [link.get_text().strip() for link in soup.find_all('a', onclick=True) 
                 if "modal_iframe_open" in link.get('onclick') and link.get_text().strip() not in ['Showroom', 'Shooting']]
        
        for name in names[:1]:

            new_url = f"https://m.italianmoda.com/storefronts/{name}"

            # Navigate to the page
            driver.get(url)

            # Wait for the page to load (adjust sleep time if necessary)
            time.sleep(3)

            # Get the page source
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            print(soup)

        # # Extract Bio (from <p class="card-text text-justify"> tags)
        # bios = [bio.get_text(strip=True) for bio in soup.find_all('p', class_="card-text text-justify")]

        # # Extract Contact (from <a href="tel:+..."> tags)
        # contacts = [contact.get_text(strip=True) for contact in soup.find_all('a', href=True) 
        #             if "tel:" in contact.get('href')]

        # # Extract Website URL (from <a> tags with modal_iframe_open)
        # website_urls = [f"https://m.italianmoda.com/storefronts/{name.replace(' ', '').lower()}" for name in names]

        # # Synchronize lengths of all lists (fill missing values with None)
        # max_length = max(len(names), len(bios), len(contacts), len(website_urls))
        # names += [None] * (max_length - len(names))
        # bios += [None] * (max_length - len(bios))
        # contacts += [None] * (max_length - len(contacts))
        # website_urls += [None] * (max_length - len(website_urls))

        # # Create DataFrame with extracted values
        # data = {'name': names, 'bio': bios, 'contact': contacts, 'website_url': website_urls}
        # df = pd.DataFrame(data)

        # return df

    finally:
        driver.quit()

# Usage example
if __name__ == "__main__":
    url = "https://m.italianmoda.com/companies/clothing/women/classic-and-chic"   # Replace with the target URL
    df = scrape_page_details(url)
    df.to_csv("output.csv")
    #print(df)

