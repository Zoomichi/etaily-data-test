from bs4 import BeautifulSoup
import json
import requests
from datetime import datetime

def main():
    goodest_url = "https://www.lazada.com.ph/goodest/?q=All-Products&from=wangpu&langFlag=en&pageTypeId=2"
    goodest = requests.get(goodest_url).text
    goodest_soup = BeautifulSoup(goodest, 'html.parser')
    
    # Find all item listings in page
    items = goodest_soup.find_all('div', class_ = '_95X4G')
    id = 0
    dict = []
    
    # Iterate through all item listings
    for listing in items:
        id += 1
        url = listing.find('a')['href']
        item = requests.get(url).text
        soup = BeautifulSoup(item, 'html.parser')
        
        # Set item id and item name
        entry = {}
        entry['id'] = id
        entry['item_name'] = soup.find('h1', class_ = 'pdp-mod-product-badge-title').get_text() # Product name
        
        ### Set price, original price, and discount ###
        
        # Look for the code block which contains the pricing data
        pricing = soup.find('div', class_ = 'pdp-product-price')
        
        for idx, span in enumerate(pricing.find_all('span')):
            if idx == 0:
                entry['price'] = span.get_text()
                entry['original_price'] = span.get_text()
                entry['discount'] = '0%'
            elif idx == 1:  # The elif statements are for updating the data if there is a discount on the current item
                entry['original_price'] = span.get_text()
            elif idx == 2:
                entry['discount'] = span.get_text()
        
        # Set item rating and review count
        entry['item_rating'] = soup.find('span', class_ = 'score-average').get_text()
        entry['no_of_ratings'] = soup.find('div', class_ = 'count').get_text()
        
        dict.append(entry)
    
    # Get current date to use as file name for json dump
    today = datetime.today()
    date = today.strftime("%m-%d-%Y")
    with open("goodest_" + date + ".json", "w") as out:
        json.dumps(dict, out)


if __name__ == "__main__":
  main()