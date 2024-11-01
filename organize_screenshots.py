import os
import pytesseract
from PIL import Image
from data_processing import BRAND_NAMES
import shutil

def get_brandname(screenshot):
    image = Image.open(screenshot)
    image_text = pytesseract.image_to_string(image).lower()

    for brand in BRAND_NAMES:
        if brand in image_text:
            return brand
    return None

#Organizes the screenshots that are in the screenshots folder into their
#respective brand names
def organize():
    legit_dir = "screenshots/not_phish";
    phish_dir = "screenshots/phish";

    for brand in BRAND_NAMES:
        os.makedirs(f"screenshots/brands/{brand}/legit", exist_ok=True)
        os.makedirs(f"screenshots/brands/{brand}/phish", exist_ok=True)

    for file in os.listdir(legit_dir):
        if file.endswith(".png"):
            path = os.path.join(legit_dir, file)
            brand = get_brandname(path)
            if brand == None:
                continue
            else:
                shutil.copy(path, f"screenshots/brands/{brand}/legit/{file}")

    for file in os.listdir(phish_dir):
        if file.endswith(".png"):
            path = os.path.join(phish_dir, file)
            brand = get_brandname(path)
            if brand == None:
                continue
            else:
                shutil.copy(path, f"screenshots/brands/{brand}/phish/{file}")

if __name__ == "__main__":
    organize()
