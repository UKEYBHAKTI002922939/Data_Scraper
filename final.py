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



def scrape_second(url, name):
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

    extracted_data = []
    titles=[]
    descriptions = []

    for element in elements:
        # Extract the product title (h5 card-title)
        product_title = element.find('p', class_='h5 card-title').get_text(strip=True)
        
        # Extract the description (descrizione-breve)
        product_description = element.find('div', class_='descrizione-breve').next_sibling.strip()

        # Print the extracted content
        #print(f"Product Title: {product_title}")
        #print(f"Description: {description}")
        titles.append(product_title)
        descriptions.append(product_description)

        
        
        

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
    
    # flattened_data = []
    # for name, title_list, description_list, image_list in zip(name, titles, descriptions, img_list):
    #     print(name, title_list, description_list, image_list)
    #     max_length = max(len(title_list), len(description_list), len(image_list))
    #     for i in range(max_length):
    #         title = title_list[i] if i < len(title_list) else None
    #         description = description_list[i] if i < len(description_list) else None
    #         image = image_list[i] if i < len(image_list) else None
    #         flattened_data.append({
    #             "name": name,
    #             "title": title,
    #             "description": description,
    #             "images": image
    #         })
    flattened_data = []
    max_length = max(len(titles), len(descriptions), len(img_list))
    for i in range(max_length):
        title = titles[i] if i < len(titles) else None
        description = descriptions[i] if i < len(descriptions) else None
        image = img_list[i] if i < len(img_list) else None
        flattened_data.append({
            "name": name,
            "title": title,
            "description": description,
            "images": image
        })
    # Create DataFrame
    
    df_2 = pd.DataFrame(flattened_data)
    # df_final = pd.DataFrame("")
    # for i in range(len(df_2)):
    #     df_final.append()
    print(df_2)
    
    df_2.to_csv("output_second.csv", index=False)
    # return df_2


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

        # Extract Bio (from <p class="card-text text-justify"> tags)
        bios = [bio.get_text(strip=True) for bio in soup.find_all('p', class_="card-text text-justify")]

        # Extract Contact (from <a href="tel:+..."> tags)
        contacts = [contact.get_text(strip=True) for contact in soup.find_all('a', href=True) 
                    if "tel:" in contact.get('href')]

        # Extract Website URL (from <a> tags with modal_iframe_open)
        website_urls = [f"https://m.italianmoda.com/storefronts/{name.replace(' ', '').lower()}" for name in names]

        # Synchronize lengths of all lists (fill missing values with None)
        max_length = max(len(names), len(bios), len(contacts), len(website_urls))
        names += [None] * (max_length - len(names))
        bios += [None] * (max_length - len(bios))
        contacts += [None] * (max_length - len(contacts))
        website_urls += [None] * (max_length - len(website_urls))

        # Create DataFrame with extracted values
        data = {'name': names, 'bio': bios, 'contact': contacts, 'website_url': website_urls}
        df = pd.DataFrame(data)

        return df

    finally:
        driver.quit()

# Usage example
if __name__ == "__main__":
    url = "https://m.italianmoda.com/companies/clothing/women/classic-and-chic"   # Replace with the target URL
    df = scrape_page_details(url)
    df.to_csv("output.csv")
    #print(df)

