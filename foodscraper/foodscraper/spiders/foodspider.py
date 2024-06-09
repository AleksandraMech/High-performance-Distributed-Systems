import scrapy


class FoodspiderSpider(scrapy.Spider):
    name = "foodspider"
   # allowed_domains = ["ubereats.com"]
    allowed_domains = ["pyszne.pl"]
    start_urls = ["https://www.pyszne.pl/na-dowoz/jedzenie/gdansk-gdansk-80-060"]
   # start_urls = ["https://ubereats.com"]

    def parse(self, response):
        pass
