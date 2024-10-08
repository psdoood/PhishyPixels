import data_collection as dc
import numpy as np

def main():
    legit_urls = dc.get_urls(dc.legit_urls_filename, dc.legit_index)
    phish_urls = dc.get_urls(dc.phish_urls_filename, dc.phish_index)
    print("All URLs collected.")

    legit_screenshots_with_brands = dc.get_screenshot_and_brand(legit_urls, False)
    phish_screenshots_with_brands = dc.get_screenshot_and_brand(phish_urls, True)
    print("Saved screenshots of relevent brand websites.")

    all_screenshots_with_brands = legit_screenshots_with_brands + phish_screenshots_with_brands
    feature_data = dc.create_data_structure(all_screenshots_with_brands)
    print("Finished creating feature data structures from screenshots.")

    #prepare and feed feature_data into a decision tree next

if __name__ == "__main__":
    main()