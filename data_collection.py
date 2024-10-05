import os
import csv
#import requests
import colorgram as cg

from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

#Allows selenium to be run in a non GUI environment and downloads a chrome driver
options = Options()
options.add_argument("-headless=new")
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
NUM_OF_URLS = 100
#Seconds to try and load page before quiting
TIME_OUT = 10
#How many colors to extract from each image
NUM_COLORS = 5

#List of some of the more popular targeted websites to focus on
BRAND_NAMES = ['facebook', 'netflix', 'microsoft', 'google', 'tiktok', 'youtube', 'amazon', 'linkedin', 'x', 'paypal', 'meta', 'instagram', 'steam', 'apple', 'dhl', 'whatsapp']

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
                #Add scheme if the csv file doesnt include them 
                if not url.startswith(("https://", "http://")):
                    url = "https://" + url
                urls.append(url)
    return urls 

#------------------------------------------------------------------------------------------------------#

#Extracts text out of an image (of a website)
def extract_text(screenshot):
    image = Image.open(screenshot)
    text = pytesseract.image_to_string(image)
    return text.lower()

#------------------------------------------------------------------------------------------------------#

#Returns the brand name if it is in BRAND_NAMES, else returns "ignore"
def determine_brand(screenshot):
    text = extract_text(screenshot)
    for name in BRAND_NAMES:
        if name in text:
            return name
    return "ignore"

#------------------------------------------------------------------------------------------------------#

#Takes and saves screenshots of each webpage to 'screenshots' and returns them in a list
def get_screenshots(urls, folder):
    screenshots_with_brand = []
    for i, url in enumerate(urls):
        try:
            print(f"Trying to access: {url}")
            driver.set_page_load_timeout(TIME_OUT)
            driver.get(url)

            #Ignores urls with error or 404 in title
            if "error" in driver.title.lower() or "404" in driver.title.lower():
                print(f"Error at this url: {url}")
                continue

            save_path = f"screenshots/{folder}/" + str(i) + ".png"
            driver.save_screenshot(save_path)
            
            #Removes screenshot if it doesn't contain any brand from BRAND_NAMES
            brand = determine_brand(save_path)
            if brand == "ignore":
                print(f"Unrelated brand, not saving...")
                os.remove(save_path)
                continue

            screenshots_with_brand.append([save_path, brand])
            print(f"Screenshot successful: " + str(i) +".png: {url}")
        except:
            print(f"Could not access: {url}")
        
    return screenshots_with_brand

#------------------------------------------------------------------------------------------------------#

#Extracts the 5 most dominant colors from each screenshot
def extract_colors(screenshot):
    color_list = []
    colors  = cg.extract(screenshot, NUM_COLORS)
    for color in colors:
        color_list.append([color.rgb[0], color.rgb[1], color.rgb[2]])
    return color_list
#------------------------------------------------------------------------------------------------------#

def create_data_structure():
    pass

#------------------------------------------------------------------------------------------------------#

urls_list = get_urls(legit_urls_filename, legit_index)
screenshots_list = get_screenshots(urls_list, "not_phish")
#print(screenshots_list)

driver.quit()
