import scrapy
from scrapy_scraper.settings import SPIDER_URL

class BlueSpider(scrapy.Spider):
    name = "blue"

    start_urls = [SPIDER_URL[name]]

    def parse(self, response):
        # follow links to author pages
        for href in response.xpath('//ul[@class="thumbs"]/li/a/@href'):
            yield response.follow(href, self.parse_model)

    def parse_model(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        def extract_with_xpath(query):
            return response.xpath(query).extract_first().strip()

        yield {
            'telefone': extract_with_xpath('//p[contains(@class, "n-whatsapp-op")]::text()'),
        }
