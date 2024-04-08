import scrapy


class FoodspiderSpider(scrapy.Spider):
    name = "foodspider"
    allowed_domains = ["ubereats.com"]
    start_urls = ["https://ubereats.com"]

    def parse(self, response):
        pass
