# PhishyPixels 

This is a machine learning project for website phish detection using only color analysis. It extracts the 3 most dominant colors from each website to try and determine if a website is legitimate or not (from a specific list of 10 targeted brands), using a custom made decision tree. It produces consistent results of over 80% accuracy, but with an increased/improved data sample I beleive it could consistently be over 90%.

## Data
- List of non-legitimate URLS comes from [OpenPhish](https://openphish.com/). 
- List of legitimate URLS is custom made based on targeted brands.
- Targeted Brands:
    1. Facebook 
    2. Netflix
    3. Microsoft
    4. TikTok
    5. Amazon
    6. PayPal
    7. Instagram
    8. Steam 
    9. Apple
    10. WhatsApp

## Results
    <RESULTS>
    table?

## Required Libraries
- [numpy](https://github.com/numpy/numpy)
- [colorgram](https://github.com/obskyr/colorgram.py)
- [selenium](https://github.com/SeleniumHQ/selenium)
- [pytesseract](https://github.com/h/pytesseract)

## Warning
- I would advise using a VPN and a Virtual Machine if you are going to run this, visiting phishing websites is potentially dangerous 

