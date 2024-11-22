import os
import numpy as np
import colorgram as cg

#List targeted brands I am focusing on
BRAND_NAMES = ['facebook', 'netflix', 'microsoft', 'tiktok', 'amazon', 'paypal', 'instagram', 'steam', 'apple', 'whatsapp']
NUM_BRAND_FEATURES = len(BRAND_NAMES)
#How many colors to extract from each image
NUM_COLORS = 3
EXPECTED_FEATURES = NUM_COLORS + NUM_BRAND_FEATURES + 1 # + 1 is for phish_val

#Extracts the (NUM_COLORS) most dominant colors from each screenshot
def extract_colors(screenshot):
    hex_color_list = []
    colors  = cg.extract(screenshot, NUM_COLORS)

    for color in colors:
        #Convert to hex and normalize the value
        hex_val = float((color.rgb[0] << 16) + (color.rgb[1] << 8) + color.rgb[2]) / float(0xFFFFFF)
        hex_color_list.append(hex_val)
        
    #If there is less than NUM_COLORS in the screenshot, add dummy color (0.0)
    while len(hex_color_list) < NUM_COLORS :
        hex_color_list.append(0.0)

    return hex_color_list

#Creates the data strucutres [(colors) + (brands) + (0 or 1 <0 is phish, 1 is not>)]
def create_data_structure(screenshots_paths, brand_index, is_phish):
    data = []
    if is_phish == True:
        val = 0
    else:
        val = 1

    for path in screenshots_paths:
        colors = extract_colors(path)

        #Each brand has its own index related to BRAND_NAMES, values are binary
        #0 mean brand not present, 1 means brand is present
        brand_features = [0] * len(BRAND_NAMES)
        brand_features[brand_index] = 1
        features = colors + brand_features + [val]

        if(len(features) == EXPECTED_FEATURES):
            data.append(features) 
            print(f"Processed: {path} - {BRAND_NAMES[brand_index]}")
        else:
            print(f"Path at {path} has wrong feature length, ignoring...")
    
    
    data_array = np.array(data, dtype=float)
    
    return data_array
    
