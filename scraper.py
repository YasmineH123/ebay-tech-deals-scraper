import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time
from fake_useragent import UserAgent
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import os

def scrape_ebay_data():
    """Scrape eBay tech deals and return as list of dicts."""
    # Set up Selenium options
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    # Rotate User-Agent
    ua = UserAgent()
    options.add_argument(f"user-agent={ua.random}")

    # ChromeDriver setup
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://www.ebay.com/globaldeals/tech")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.dne-itemtile"))
    )

    # Scroll to load all items
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Extract product data
    products = driver.find_elements(By.CSS_SELECTOR, "div.dne-itemtile")
    data = []
    for product in products:
        try:
            title = product.find_element(By.XPATH, ".//span[@itemprop='name']").text
        except:
            title = "N/A"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            price = product.find_element(By.XPATH, ".//span[@itemprop='price']").text
        except:
            price = "N/A"
        try:
            original_price = product.find_element(By.CSS_SELECTOR, "span.itemtile-price-strikethrough").text
        except:
            original_price = "N/A"
        try:
            shipping = product.find_element(By.CSS_SELECTOR, "span.dne-itemtile-delivery").text
        except:
            shipping = "N/A"
        try:
            item_url = product.find_element(By.XPATH, ".//a[@itemprop='url']").get_attribute("href")
        except:
            item_url = "N/A"

        data.append({
            "title": title,
            "timestamp": timestamp,
            "price": price,
            "original_price": original_price,
            "shipping": shipping,
            "item_url": item_url
        })
        print(f"Extracted: {title}")

    driver.quit()
    return data

def save_to_csv(data):
    """Save scraped eBay data to CSV."""
    file_name = "ebay_tech_deals.csv"
    new_rows = pd.DataFrame(data, columns=[
        "timestamp", "title", "price", "original_price", "shipping", "item_url"
    ])

    if not os.path.exists(file_name) or os.path.getsize(file_name) == 0:
        new_rows.to_csv(file_name, index=False)
    else:
        existing = pd.read_csv(file_name, dtype=str)
        existing = existing[existing["timestamp"] != "timestamp"]  # drop accidental header rows
        df = pd.concat([existing, new_rows], ignore_index=True)
        df.to_csv(file_name, index=False)
        
if __name__ == "__main__":
    print("Scraping eBay tech deals...")
    scraped_data = scrape_ebay_data()  # now properly defined

    if scraped_data:
        save_to_csv(scraped_data)
        print("Data saved to ebay_tech_deals.csv")
    else:
        print("Failed to scrape data.")