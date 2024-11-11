import os
import numpy as np
import colorgram as cg
from PIL import Image
import pytesseract

#For windows:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#For Linux (mint)
#pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"

#List of some of the more popular targeted websites to focus on
BRAND_NAMES = ['facebook', 'netflix', 'microsoft', 'tiktok', 'amazon', 'paypal', 'instagram', 'steam', 'apple', 'whatsapp']
NUM_BRAND_FEATURES = len(BRAND_NAMES)
#How many colors to extract from each image
NUM_COLORS = 4
#This was from when I was also tracking proportion for each color, but I feel like it wasnt improving metrics
NUM_COLOR_FEATURES = 1
#How many features should be present in each data structure
EXPECTED_FEATURES = NUM_COLORS * NUM_COLOR_FEATURES + NUM_BRAND_FEATURES + 1 

#------------------------------------------------------------------------------------------------------#

#Extracts the 5 most dominant colors from each screenshot
def extract_colors(screenshot):
    hex_color_list = []
    colors  = cg.extract(screenshot, NUM_COLORS)

    for color in colors:
        #Convert to hex and normalize the value
        hex_val = float((color.rgb[0] << 16) + (color.rgb[1] << 8) + color.rgb[2]) / float(0xFFFFFF)
        hex_color_list.append(hex_val)
        
    #If there is less than NUM_COLORS in the screenshot, add dummy color
    while len(hex_color_list) < (NUM_COLORS * NUM_COLOR_FEATURES):
        hex_color_list.append(0.0)

    return hex_color_list

#------------------------------------------------------------------------------------------------------#

#Creates the data strucutres [(colors), (brands), (0 or 1 <0 is phish, 1 is not>)]
def create_data_structure(screenshots_paths, brand_index, is_phish):
    data = []
    if is_phish == True:
        val = 0
    else:
        val = 1

    for path in screenshots_paths:
        colors = extract_colors(path)

        #Each brand has its own index in the data structure, so the values are just 0 or 1
        brand_features = [0] * len(BRAND_NAMES)
        brand_features[brand_index] = 1
        features = colors + brand_features + [val]

        if(len(features) == EXPECTED_FEATURES):
            data.append(features) 
            print(f"Processed: {path} - {BRAND_NAMES[brand_index]}")
        else:
            print(f"Path at {path} has wrong feature length, ignoring...")
    
    if len(data) > 0:
        data_array = np.array(data, dtype=float)
        #Return the data in the correct array shape
        return data_array.reshape(len(data), EXPECTED_FEATURES)
    else:
        #Return an empty array if data wasnt created
        return np.array(data, dtype=float).reshape(0, EXPECTED_FEATURES)
