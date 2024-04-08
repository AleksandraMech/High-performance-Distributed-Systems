import httpx 
import json
from selectolax.parser import HTMLParser

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

url = "https://wolt.com/pl/pol/gdansk/restaurant/lees-chinese"

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 OPR/108.0.0.0"}

resp = httpx.get(url, headers=headers)
html = HTMLParser(resp.text)

names = html.css("div h3")
prices = html.css("span.sc-de642809-3.hwSkqq")

products = []

headings = ("food", "price")

for name, price in zip(names, prices):
    product_name = name.text()
    product_price = price.text()
    product = Product(product_name, product_price)
    products.append(product)

