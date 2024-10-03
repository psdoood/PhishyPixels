import csv
#import requests
import colorgram as cg
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

#Allows selenium to be run in a non GUI environment and downloads a chrome driver
options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-javascript")
options.add_argument("--disable-extensions")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

#May need to adjust these filename filepaths based on if you download different from what I did
#Number, URL 
legit_urls_filename = "data/tranco_3N84L.csv"
legit_index = 1

#phish_id, url, phish_detail_url, submission_time, verified, verification_time, online, target
phish_urls_filename = "data/verified_online.csv"
phish_index = 1

#Number of urls to extract from each file
NUM_OF_URLS = 20
#Seconds to try and load page before quiting
TIME_OUT = 10
SLEEP = 5

#------------------------------------------------------------------------------------------------------#

#filename of the csv index, and index for the column the url is in.
def get_urls(filename, index):
    urls = []
    with open(filename, "r") as file:
        csvreader = csv.reader(file)
        #Skip first line of csv file
        next(csvreader)
        for i, row in enumerate(csvreader):
            if i >= NUM_OF_URLS:
                break
            else:
                url = row[index]
                if not url.startswith(("https://", "http://")):
                    url = "https://" + url
                urls.append(url)
    return urls 

#------------------------------------------------------------------------------------------------------#

#Takes and saves screenshots of each webpage to 'screenshots' and returns them in a list
def get_screenshots(urls, folder):
    screenshots = []
    for i, url in enumerate(urls):
        try:
            print(f"Trying to access: {url}")
            driver.set_page_load_timeout(TIME_OUT)
            driver.get(url)

            time.sleep(SLEEP)

            if "error" in driver.title.lower() or "404" in driver.title.lower():
                print(f"Error at this url: {url}")
                continue

            save_path = f"screenshots/{folder}/" + str(i) + ".png"
            driver.save_screenshot(save_path)
            screenshots.append(save_path)
        except:
            print(f"Could not access: {url}")
        
    return screenshots

#------------------------------------------------------------------------------------------------------#

#Extracts the dominant colors from each screenshot 
def extract_colors(photos):
    pass

#------------------------------------------------------------------------------------------------------#

def create_data_structure():
    pass

#------------------------------------------------------------------------------------------------------#

urls_list = get_urls(legit_urls_filename, legit_index)
screenshots_list = get_screenshots(urls_list, "not_phish")
print(screenshots_list)

driver.quit()
