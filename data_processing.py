import os
import numpy as np
import colorgram as cg
from PIL import Image
import pytesseract

#For windows:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#For Linux (mint)
#pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"

#How many colors to extract from each image
NUM_COLORS = 5

#List of some of the more popular targeted websites to focus on
BRAND_NAMES = ['facebook', 'netflix', 'microsoft', 'tiktok', 'youtube', 'amazon', 'linkedin', 'twitter', 'paypal', 'instagram', 'steam', 'apple', 'whatsapp']

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

#Extracts the 5 most dominant colors from each screenshot
def extract_colors(screenshot):
    color_list = []
    colors  = cg.extract(screenshot, NUM_COLORS)
    for color in colors:
        color_list.extend([color.rgb[0], color.rgb[1], color.rgb[2]])
    return color_list

#------------------------------------------------------------------------------------------------------#

#Creates the data strucutres [(15 values <5 * rgb>), (1 value <brand index>), (0 or 1 <0 is phish, 1 is not>)]
def create_data_structure(screenshots_paths, is_phish):
    data = []
    if is_phish == True:
        val = 0
    else:
        val = 1

    for path in screenshots_paths:
        brand = determine_brand(path)
        if brand != -1:
            colors = extract_colors(path)
            features = colors + [brand, val]
            data.append(features) 
        else:
            print(f"No relevant brand found at: {path}")
            os.remove(path)
    return np.array(data)
