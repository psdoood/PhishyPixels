import os
import csv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
#Allows selenium to be run in a non GUI environment + other browser options
options.add_argument("--headless=new")
options.add_argument("--disable-javascript")
options.add_argument("--disable-extensions")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.binary_location = r"/usr/bin/chromium-browser"

service = Service(r"/usr/bin/chromedriver")

legit_urls_filename = "data/legit.csv"
legit_index = 0

phish_urls_filename = "data/phish.csv"
phish_index = 0

#Seconds to try and load page before quitting
TIME_OUT = 30
#Max amount of URLs to collect from each csv file on each run
NUM_LEGIT_URLS = 250
NUM_PHISH_URLS = 500


#Filename of the csv index, and index for the column the url is in.
def get_urls(filename, index, num_urls):
    urls = []
    with open(filename, "r") as file:
        csvreader = csv.reader(file)
        for i, row in enumerate(csvreader):
            if i >= num_urls:
                break
            else:
                url = row[index]
                #Add scheme if the csv file doesn't include them 
                if not url.startswith(("https://", "http://")):
                    url = "https://" + url
                urls.append(url)
    return urls 

#Takes and saves screenshots of each webpage to '/screenshots'
def get_screenshots(urls, is_phish):
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(TIME_OUT)

    for i, url in enumerate(urls):
        try:
            if is_phish == True:
                folder = "phish"
        
            else:
                folder = "not_phish"

            print(f"Trying to access: {url}")
            driver.get(url)

            if "error" in driver.title.lower() or "404" in driver.title.lower():
                print(f"Error at this url: {url}")
                continue

            screenshot_dir = f"screenshots/{folder}"
            os.makedirs(screenshot_dir, exist_ok=True)
            save_path = os.path.join(screenshot_dir, f"scan2-{i}.png")
            driver.save_screenshot(save_path)
                
        except:
            print(f"Error in get_screenshots for: {url}")

def main():
    print("Collecting URLs...")
    legit_urls = get_urls(legit_urls_filename, legit_index, NUM_LEGIT_URLS)
    phish_urls = get_urls(phish_urls_filename, phish_index, NUM_PHISH_URLS)
    print("All URLs collected.")

    print("Saving screenshots...")
    get_screenshots(legit_urls, False)
    get_screenshots(phish_urls, True)
    print("Saved screenshots!")

if __name__ == '__main__':
    main()