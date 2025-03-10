from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import base64

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

def scrape_second(url):
    driver = setup_driver()
    driver.get(url)

    # Wait for the page to load (adjust sleep time if necessary)
    time.sleep(3)

    # Get the page source
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    #buttons = WebDriverWait(driver, 120).until(
    #        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.read-more__btn.notranslate'))
    #   )

    buttons = driver.find_elements(By.CLASS_NAME, 'read-more__btn')
    
    # Find all the buttons with the class 'rea‘ME, 'read-more__btn')
    for idx, button in enumerate(buttons[:1]):
        button.click()
        print(f"Button {idx} clicked")


    elements = soup.find_all('div', class_='read-more__content')

    for element in elements:
        # Extract the product title (h5 card-title)
        product_title = element.find('p', class_='h5 card-title').get_text(strip=True)
        
        # Extract the description (descrizione-breve)
        description = element.find('div', class_='descrizione-breve').next_sibling.strip()

        # Print the extracted content
        print(f"Product Title: {product_title}")
        print(f"Description: {description}")

        extracted_data = []
        extracted_data.append({'Product Title': product_title, 
                               'Description': description})
        

    image_tags = soup.find_all("img", class_="card-img-top")
    # Download each image 
    img_list=[]
    for i, img_tag in enumerate(image_tags):
        # Get the high-resolution image URL from the `data-src-big` attribute
        img_url = img_tag.get("data-src-big")
        if not img_url:
            img_url = img_tag.get("src")  # Fallback to `src` attribute
    
        # Download the image
        try:
            if img_url:
                headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36" }
                response = requests.get(img_url, headers=headers)
                if response.status_code == 200:
                    # Save the image to the folder
                    image_base64 = base64.b64encode(response.content).decode('utf-8')
                    # img_filename = f"downloaded_images/image_{i + 1}.jpg"
                    #with open("image_base64.txt", "w") as file:
                        #file.write(image_base64)
                    print(f"Downloaded {i} successfully")
                    img_list.append(image_base64)
                else:
                    print(f"Failed to download: {img_url}")
            else:
                print("No valid image URL found.")
        except:
            continue
    extracted_data.append({'Images': img_list})
    df = pd.DataFrame(extracted_data) 
    df.to_csv("output_2.csv")


if __name__ == "__main__":
    # url = "https://m.italianmoda.com/companies/clothing/women/classic-and-chic"   # Replace with the target URL
    new_url = f"https://m.italianmoda.com/storefronts/eklam"
    scrpae(new_url)