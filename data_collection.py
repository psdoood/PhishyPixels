import os
import csv
import numpy as np

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
options.binary_location = r"/usr/bin/chromium-browser"

service = Service(r"/usr/bin/chromedriver")

legit_urls_filename = "data/legit.csv"
legit_index = 0

phish_urls_filename = "data/phish.csv"
phish_index = 0

#Seconds to try and load page before quiting
TIME_OUT = 30
NUM_LEGIT_URLS = 80
NUM_PHISH_URLS = 500

#------------------------------------------------------------------------------------------------------#

#filename of the csv index, and index for the column the url is in.
def get_urls(filename, index, num_urls):
    urls = []
    with open(filename, "r") as file:
        csvreader = csv.reader(file)
        for i, row in enumerate(csvreader):
            if i >= num_urls:
                break
            else:
                url = row[index]
                #Add scheme if the csv file doesnt include them 
                if not url.startswith(("https://", "http://")):
                    url = "https://" + url
                urls.append(url)
    return urls 

#------------------------------------------------------------------------------------------------------#
'''
#How many threads can run at a time
NUM_OF_THREADS = 2
def thread_process_url(url, i, folder, val, screenshots_with_brand, lock):
    driver = None
    try:
        print(f"Trying to access: {url}")
        driver = webdriver.Chrome(service=service, options=options)
        if not driver:
            print(f"Failed to init driver for: {url}")
            return
        driver.set_page_load_timeout(TIME_OUT)
        driver.get(url)

        #Ignores urls with error or 404 in title
        if "error" in driver.title.lower() or "404" in driver.title.lower():
            print(f"Error at this url: {url}")
            return

        #Saves screenshots to its assigned folder
        screenshot_dir = f"screenshots/{folder}"
        os.makedirs(screenshot_dir, exist_ok=True)
        save_path = os.path.join(screenshot_dir, f"{i}.png")
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
    except:
        print(f"Could not access: {url}")

    finally:
        if driver:
            driver.quit()
'''

#------------------------------------------------------------------------------------------------------#

#Takes and saves screenshots of each webpage to 'screenshots' and returns them in a list (now uses threading)
def get_screenshots(urls, is_phish):
    #threads = []
    #lock = Lock()

    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(TIME_OUT)

    for i, url in enumerate(urls):
        try:
            if is_phish == True:
                folder = "phish"
                val = 0
            else:
                folder = "not_phish"
                val = 1

            print(f"Trying to access: {url}")
            driver.get(url)

            #Ignores urls with error or 404 in title
            if "error" in driver.title.lower() or "404" in driver.title.lower():
                print(f"Error at this url: {url}")
                continue

            #Saves screenshots to its assigned folder
            screenshot_dir = f"screenshots/{folder}"
            os.makedirs(screenshot_dir, exist_ok=True)
            save_path = os.path.join(screenshot_dir, f"{i}.png")
            driver.save_screenshot(save_path)
                
        except:
            print(f"Error in get_screenshots for: {url}")
    
    '''
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
    '''

#------------------------------------------------------------------------------------------------------#

def main():
    print("Collecting URLs...")
    legit_urls = get_urls(legit_urls_filename, legit_index, NUM_LEGIT_URLS)
    phish_urls = get_urls(phish_urls_filename, phish_index, NUM_PHISH_URLS)
    print("All URLs collected.")

    print("Saving screenshots...")
    get_screenshots(legit_urls, False)
    get_screenshots(phish_urls, True)
    print("Saved screenshots!")

#------------------------------------------------------------------------------------------------------#

if __name__ == '__main__':
    main()