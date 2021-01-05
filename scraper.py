import requests
from bs4 import BeautifulSoup

user_item = input("Enter an item you are looking for: ")
print()

URL = "https://www.bestbuy.com/site/searchpage.jsp"

header = {
    "User-Agent": "Request's Python"
}
param = {
    "st": user_item
}
r = requests.get(URL, params=param, headers=header)

soup = BeautifulSoup(r.content, 'html.parser')


container = soup.find("ol", class_="sku-item-list")

try:
    items = container.find_all("li", class_="sku-item")
except AttributeError:
    print("No results found.")
    exit()

for item in items:
    name = item.find('div',class_="sku-title")
    prices = item.find('div',class_="priceView-hero-price priceView-customer-price")
    if prices is None:
        continue
    price = next(prices.children , None)

    check_stock = item.find('button', class_="add-to-cart-button")
   
    if check_stock.text == "Sold Out":
        availability = "Out of Stock"
    elif check_stock.text == "Check Stores":
        availability = "Unavailable Near By"
    elif check_stock.text == "Coming Soon":
        availability = "Coming Soon"
    else:
        availability = "In Stock"

    if None in (name,price):
        continue

    print(name.text + "   Price: " + price.text + "  Availability: " + availability , end='\n'*3)

print(r.url)