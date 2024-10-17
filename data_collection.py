import os
import csv
import colorgram as cg
import numpy as np

from threading import Thread, Lock
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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

#May need to adjust these filename filepaths based on if you download different from what I did
#Number, URL 
legit_urls_filename = "data/tranco_3N84L.csv"
legit_index = 1

#URLs from OpenPhish feed
phish_urls_filename = "data/phish.csv"
phish_index = 0

#Number of urls to extract from each file
NUM_OF_URLS = 100
#Seconds to try and load page before quiting
TIME_OUT = 10
#How many colors to extract from each image
NUM_COLORS = 5
#How many threads can run at a time
NUM_OF_THREADS = 5

#List of some of the more popular targeted websites to focus on
BRAND_NAMES = ['facebook', 'netflix', 'microsoft', 'tiktok', 'youtube', 'amazon', 'linkedin', 'x', 'paypal', 'instagram', 'steam', 'apple', 'dhl', 'whatsapp']

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

#Returns the brand name if it is in BRAND_NAMES, else returns -1
def determine_brand(screenshot):
    text = extract_text(screenshot)
    for i, name in enumerate(BRAND_NAMES):
        if name in text:
            return i
    return -1

#------------------------------------------------------------------------------------------------------#

def thread_process_url(url, i, folder, val, screenshots_with_brand, lock):
    try:
        print(f"Trying to access: {url}")
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(TIME_OUT)
        driver.get(url)

        #Ignores urls with error or 404 in title
        if "error" in driver.title.lower() or "404" in driver.title.lower():
            print(f"Error at this url: {url}")
            return

        save_path = f"screenshots/{folder}/" + str(i) + ".png"
        driver.save_screenshot(save_path)
            
        #Removes screenshot if it doesn't contain any brand from BRAND_NAMES
        brand = determine_brand(save_path)
        if brand == -1:
            print(f"Unrelated brand, not saving...")
            os.remove(save_path)
            return 
        
        #Lock must be aquired first before continuing
        with lock:
            screenshots_with_brand.append([save_path, brand, val])
        print(f"Screenshot successful: " + str(i) + f".png: {url}")
        driver.quit()
    except:
        print(f"Could not access: {url}")
        driver.quit()


#------------------------------------------------------------------------------------------------------#

#Takes and saves screenshots of each webpage to 'screenshots' and returns them in a list (now uses threading)
def get_screenshot_and_brand(urls, is_phish):
    screenshots_with_brand = []
    threads = []
    lock = Lock()

    if is_phish == True:
        folder = "phish"
        val = 0
    else:
        folder = "not_phish"
        val = 1
    
    #Creates threads for processing each url, depends pn NUM_OF_THREADS
    for i, url in enumerate(urls):
        thread = Thread(target=thread_process_url, args=(url, i, folder, val, screenshots_with_brand, lock))
        thread.start()
        threads.append(thread)
        #If the max threads has been reached, let them all finish then empty the list
        if len(threads) >= NUM_OF_THREADS:
            for thread in threads:
                thread.join()
            threads = []
    #Execute any remaining threads
    for thread in threads:
        thread.join()

    return screenshots_with_brand

#------------------------------------------------------------------------------------------------------#

#Extracts the 5 most dominant colors from each screenshot
def extract_colors(screenshot):
    color_list = []
    colors  = cg.extract(screenshot, NUM_COLORS)
    for color in colors:
        color_list.extend([color.rgb[0], color.rgb[1], color.rgb[2]])
    return color_list

#------------------------------------------------------------------------------------------------------#

#Creates the data strucutres [(15 values <5 * rgb>), (1 value <brand index>), (0 or 1 <0 is phish, 1 is not>)]
def create_data_structure(screenshots_with_brand):
    data = []
    for save_path, brand, val in screenshots_with_brand:
        colors_and_brand = extract_colors(save_path)
        features = colors_and_brand + [brand, val]
        data.append(features) 
    return np.array(data)

#------------------------------------------------------------------------------------------------------#

